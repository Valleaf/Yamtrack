"""
Import from SensCritique.
Fetches a user's rated/collected items and creates Yamtrack media entries.

Supports: movies, TV, anime, games, books, comics, music (new).
"""

import logging
from collections import defaultdict

from celery import shared_task
from django.apps import apps
from django.contrib.auth import get_user_model

from app.models import Item, MediaTypes
from app.providers import senscritique
from integrations.imports import helpers

logger = logging.getLogger(__name__)
User = get_user_model()

# SC media_type strings → Yamtrack MediaTypes enum values
SC_TO_YAMTRACK = {
    "movie": MediaTypes.MOVIE.value,
    "tv": MediaTypes.TV.value,
    "anime": MediaTypes.ANIME.value,
    "game": MediaTypes.GAME.value,
    "book": MediaTypes.BOOK.value,
    "comic": MediaTypes.COMIC.value,
    "music": MediaTypes.MUSIC.value,
}

# SC media_type → Yamtrack source
SC_TO_SOURCE = {
    "movie": "tmdb",
    "tv": "tmdb",
    "anime": "mal",
    "game": "igdb",
    "book": "openlibrary",
    "comic": "comicvine",
    "music": "senscritique",
}


class SensCritiqueImporter:
    def __init__(self, user, username: str, password: str | None = None, overwrite: bool = False):
        self.user = user
        self.username = username
        self.overwrite = overwrite
        self.token = None
        self.skipped = 0
        self.errors = 0

        if password:
            try:
                self.token = senscritique._get_firebase_token(
                    username if "@" in username else f"{username}@senscritique.com",
                    password,
                )
            except Exception as e:
                logger.warning("SC auth failed, falling back to public access: %s", e)

    def run(self) -> str:
        products = senscritique.get_user_collection(self.username, token=self.token)
        logger.info("SC import: fetched %d items for %s", len(products), self.username)

        # Build dict of {media_type: [model_instances]}
        bulk_media = defaultdict(list)

        for product in products:
            media_type = product.get("media_type")
            if not media_type or media_type not in SC_TO_YAMTRACK:
                self.skipped += 1
                continue

            yamtrack_type = SC_TO_YAMTRACK[media_type]
            source = SC_TO_SOURCE[media_type]

            try:
                obj = self._build_obj(product, yamtrack_type, source)
                if obj:
                    bulk_media[yamtrack_type].append(obj)
            except Exception as e:
                logger.error("SC import error for '%s': %s", product.get("title"), e)
                self.errors += 1

        helpers.bulk_create_media(bulk_media, self.user)

        imported = sum(len(v) for v in bulk_media.values())
        return (
            f"SensCritique import complete: {imported} imported, "
            f"{self.skipped} skipped, {self.errors} errors."
        )

    def _build_obj(self, product: dict, yamtrack_type: str, source: str):
        """Build a model instance for a SC product."""
        title = product.get("title", "")
        sc_id = product.get("sc_id")
        score = product.get("score")
        poster = product.get("poster") or ""

        if yamtrack_type == MediaTypes.MUSIC.value:
            media_id = sc_id
        else:
            media_id = self._resolve_external_id(
                title, product.get("year"), yamtrack_type
            )
            if not media_id:
                source = "manual"
                media_id = f"sc_{sc_id}"

        # Skip if already exists and not overwriting
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
            score=score * 10 if score is not None else None,
            status=Item.Status.COMPLETED,
        )

    def _resolve_external_id(self, title: str, year, yamtrack_type: str) -> str | None:
        """Search the external provider for this item by title+year."""
        try:
            from app.providers import services
            results = services.search_media(yamtrack_type, title)
            if not results:
                return None

            for result in results[:5]:
                result_year = str(result.get("year") or result.get("release_date", ""))[:4]
                title_match = result.get("title", "").lower() == title.lower()
                year_match = year is None or str(year) == result_year

                if title_match and year_match:
                    return str(result["media_id"])

            return str(results[0]["media_id"])
        except Exception as e:
            logger.debug("SC resolve error for '%s': %s", title, e)
            return None


@shared_task(name="Import from SensCritique")
def import_from_senscritique(
    user_id: int,
    username: str,
    password: str | None = None,
    overwrite: bool = False,
) -> str:
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return f"User {user_id} not found."

    importer = SensCritiqueImporter(user, username, password, overwrite)
    return importer.run()
