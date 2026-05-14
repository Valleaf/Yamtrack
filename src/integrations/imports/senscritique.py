"""
Import from SensCritique via CSV file.

CSV format (from s2l or our sc_export.py tool):
    Title, Year, Rating10, WatchedDate, Review[, Category]

If Category column is absent, defaults to "movie" (s2l default output).
Category values: movie, tv, anime, game, book, comic, music
"""

import csv
import io
import logging
from collections import defaultdict

from celery import shared_task
from django.apps import apps
from django.contrib.auth import get_user_model

from app.models import Item, MediaTypes, Status
from app.providers import services
from integrations.imports import helpers

logger = logging.getLogger(__name__)
User = get_user_model()

VALID_MEDIA_TYPES = {mt.value for mt in MediaTypes}

# Map CSV Category values to Yamtrack media types
CATEGORY_MAP = {
    "movie":   MediaTypes.MOVIE.value,
    "tv":      MediaTypes.TV.value,
    "anime":   MediaTypes.ANIME.value,
    "game":    MediaTypes.GAME.value,
    "book":    MediaTypes.BOOK.value,
    "comic":   MediaTypes.COMIC.value,
    "music":   MediaTypes.MUSIC.value,
}


class SensCritiqueCSVImporter:
    def __init__(self, user, overwrite: bool = False):
        self.user = user
        self.overwrite = overwrite
        self.imported = 0
        self.skipped = 0
        self.errors = 0

    def run(self, csv_content: str) -> str:
        reader = csv.DictReader(io.StringIO(csv_content))
        products = []

        for row in reader:
            title = (row.get("Title") or "").strip()
            if not title:
                continue

            category = (row.get("Category") or "movie").strip().lower()
            media_type = CATEGORY_MAP.get(category, MediaTypes.MOVIE.value)

            year_str = (row.get("Year") or "").strip()
            year = int(year_str) if year_str and year_str.isdigit() else None

            rating_str = (row.get("Rating10") or "").strip()
            score = int(rating_str) if rating_str and rating_str.isdigit() else None

            products.append({
                "title": title,
                "year": year,
                "score": score,
                "media_type": media_type,
            })

        if not products:
            return "No valid items found in CSV."

        bulk_media = defaultdict(list)

        for product in products:
            try:
                obj = self._build_obj(product)
                if obj:
                    bulk_media[product["media_type"]].append(obj)
            except Exception as e:
                logger.error("SC CSV import error for '%s': %s", product.get("title"), e)
                self.errors += 1

        helpers.bulk_create_media(bulk_media, self.user)
        self.imported = sum(len(v) for v in bulk_media.values())

        return (
            f"SensCritique CSV import complete: {self.imported} imported, "
            f"{self.skipped} skipped, {self.errors} errors."
        )

    def _build_obj(self, product: dict):
        title = product["title"]
        year = product.get("year")
        score = product.get("score")
        media_type = product["media_type"]

        # Try to resolve to external provider ID
        media_id, source = self._resolve(title, year, media_type)

        if not media_id:
            source = "manual"
            media_id = f"sc_{title[:40]}"

        model = apps.get_model(app_label="app", model_name=media_type)
        exists = model.objects.filter(
            user=self.user,
            item__media_id=media_id,
            item__source=source,
            item__media_type=media_type,
        ).exists()

        if exists and not self.overwrite:
            self.skipped += 1
            return None

        item, _ = Item.objects.get_or_create(
            media_id=media_id,
            source=source,
            media_type=media_type,
            defaults={"title": title, "image": ""},
        )

        return model(
            item=item,
            user=self.user,
            score=score * 10 if score is not None else None,
            status=Status.COMPLETED.value,
        )

    def _resolve(self, title: str, year, media_type: str) -> tuple[str | None, str]:
        """Search the appropriate external provider. Returns (media_id, source)."""
        try:
            response = services.search(media_type, title, page=1)
            results = (response or {}).get("results", [])
            if not results:
                return None, ""

            for result in results[:5]:
                r_year = str(result.get("year") or result.get("release_date", ""))[:4]
                title_match = result.get("title", "").lower() == title.lower()
                year_match = year is None or str(year) == r_year
                if title_match and year_match:
                    return str(result["media_id"]), self._source_for(media_type)

            return str(results[0]["media_id"]), self._source_for(media_type)
        except Exception as e:
            logger.debug("SC resolve error for '%s': %s", title, e)
            return None, ""

    @staticmethod
    def _source_for(media_type: str) -> str:
        source_map = {
            MediaTypes.MOVIE.value:     "tmdb",
            MediaTypes.TV.value:        "tmdb",
            MediaTypes.ANIME.value:     "mal",
            MediaTypes.GAME.value:      "igdb",
            MediaTypes.BOOK.value:      "openlibrary",
            MediaTypes.COMIC.value:     "comicvine",
            MediaTypes.MUSIC.value:     "musicbrainz",
        }
        return source_map.get(media_type, "manual")


@shared_task(name="Import from SensCritique CSV")
def import_from_senscritique_csv(
    user_id: int,
    csv_content: str,
    overwrite: bool = False,
) -> str:
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return f"User {user_id} not found."

    importer = SensCritiqueCSVImporter(user, overwrite=overwrite)
    return importer.run(csv_content)
