"""
Import from FilmAffinity.
Scrapes a public FilmAffinity user profile and imports ratings into Yamtrack.

Supports: movies, TV series. Other types imported as manual entries.
"""

import logging
from collections import defaultdict

from celery import shared_task
from django.apps import apps
from django.contrib.auth import get_user_model

from app.models import Item, MediaTypes
from app.providers import filmaffinity
from integrations.imports import helpers

logger = logging.getLogger(__name__)
User = get_user_model()

FA_TO_YAMTRACK = {
    "movie": MediaTypes.MOVIE.value,
    "tv": MediaTypes.TV.value,
}


class FilmAffinityImporter:
    def __init__(self, user, user_id: str, overwrite: bool = False):
        self.user = user
        self.fa_user_id = user_id
        self.overwrite = overwrite
        self.skipped = 0
        self.errors = 0

    def run(self) -> str:
        products = filmaffinity.scrape_user_ratings(self.fa_user_id)
        logger.info("FA import: fetched %d items for user_id %s", len(products), self.fa_user_id)

        bulk_media = defaultdict(list)

        for product in products:
            media_type = product.get("media_type", "movie")
            yamtrack_type = FA_TO_YAMTRACK.get(media_type, MediaTypes.MOVIE.value)

            try:
                obj = self._build_obj(product, yamtrack_type)
                if obj:
                    bulk_media[yamtrack_type].append(obj)
            except Exception as e:
                logger.error("FA import error for '%s': %s", product.get("title"), e)
                self.errors += 1

        helpers.bulk_create_media(bulk_media, self.user)

        imported = sum(len(v) for v in bulk_media.values())
        return (
            f"FilmAffinity import complete: {imported} imported, "
            f"{self.skipped} skipped, {self.errors} errors."
        )

    def _build_obj(self, product: dict, yamtrack_type: str):
        title = product.get("title", "")
        year = product.get("year")
        score = product.get("score")
        poster = product.get("poster") or ""
        fa_id = product.get("fa_id")

        # Try to resolve to TMDB
        media_id, source = self._resolve_tmdb(title, year, yamtrack_type)

        if not media_id:
            source = "manual"
            media_id = f"fa_{fa_id}" if fa_id else f"fa_{title[:30]}"

        model = apps.get_model(app_label="app", model_name=yamtrack_type)
        exists = model.objects.filter(
            user=self.user,
            media_id=media_id,
            source=source,
        ).exists()

        if exists and not self.overwrite:
            self.skipped += 1
            return None

        return model(
            user=self.user,
            media_id=media_id,
            source=source,
            title=title,
            image=poster,
            score=score * 10 if score is not None else None,  # FA 1-10 → internal 0-100
            status=Item.Status.COMPLETED,
        )

    def _resolve_tmdb(self, title: str, year, yamtrack_type: str) -> tuple[str | None, str]:
        """Search TMDB for this item. Returns (media_id, source) or (None, '')."""
        try:
            from app.providers import services
            response = services.search(yamtrack_type, title, page=1)
            results = response.get("results", [])
            if not results:
                return None, ""

            for result in results[:5]:
                result_year = str(result.get("year") or result.get("release_date", ""))[:4]
                title_match = result.get("title", "").lower() == title.lower()
                year_match = year is None or str(year) == result_year

                if title_match and year_match:
                    return str(result["media_id"]), "tmdb"

            # Fallback: first result
            return str(results[0]["media_id"]), "tmdb"

        except Exception as e:
            logger.debug("FA TMDB resolve error for '%s': %s", title, e)
            return None, ""


@shared_task(name="Import from FilmAffinity")
def import_from_filmaffinity(
    user_id: int,
    fa_user_id: str,
    overwrite: bool = False,
) -> str:
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return f"User {user_id} not found."

    importer = FilmAffinityImporter(user, fa_user_id, overwrite)
    return importer.run()
