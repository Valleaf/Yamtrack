"""
Import from FilmAffinity via CSV file.

CSV format (FilmAffinity export):
We'll support it once we know the exact format from FilmAffinity's data export.
For now this module is a placeholder that accepts a CSV upload.
"""

import csv
import io
import logging
from collections import defaultdict

from celery import shared_task
from django.apps import apps
from django.contrib.auth import get_user_model

from app.models import Item, MediaTypes
from app.providers import services
from integrations.imports import helpers

logger = logging.getLogger(__name__)
User = get_user_model()

# Will be updated once FA CSV format is confirmed
FA_TYPE_MAP = {
    "movie":   MediaTypes.MOVIE.value,
    "tv":      MediaTypes.TV.value,
    "tvshow":  MediaTypes.TV.value,
    "serie":   MediaTypes.TV.value,
}


class FilmAffinityCSVImporter:
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
            title = (row.get("Title") or row.get("title") or "").strip()
            if not title:
                continue

            type_str = (row.get("Type") or row.get("type") or "movie").strip().lower()
            media_type = FA_TYPE_MAP.get(type_str, MediaTypes.MOVIE.value)

            year_str = (row.get("Year") or row.get("year") or "").strip()
            year = int(year_str) if year_str and year_str.isdigit() else None

            rating_str = (row.get("Rating") or row.get("rating") or row.get("Rating10") or "").strip()
            score = int(float(rating_str)) if rating_str and rating_str.replace(".", "").isdigit() else None

            products.append({
                "title": title,
                "year": year,
                "score": score,
                "media_type": media_type,
            })

        if not products:
            return "No valid items found in CSV. Please check the file format."

        bulk_media = defaultdict(list)

        for product in products:
            try:
                obj = self._build_obj(product)
                if obj:
                    bulk_media[product["media_type"]].append(obj)
            except Exception as e:
                logger.error("FA CSV import error for '%s': %s", product.get("title"), e)
                self.errors += 1

        helpers.bulk_create_media(bulk_media, self.user)
        self.imported = sum(len(v) for v in bulk_media.values())

        return (
            f"FilmAffinity CSV import complete: {self.imported} imported, "
            f"{self.skipped} skipped, {self.errors} errors."
        )

    def _build_obj(self, product: dict):
        title = product["title"]
        year = product.get("year")
        score = product.get("score")
        media_type = product["media_type"]

        media_id, source = self._resolve(title, year, media_type)

        if not media_id:
            source = "manual"
            media_id = f"fa_{title[:40]}"

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
            status=Item.Status.COMPLETED,
        )

    def _resolve(self, title: str, year, media_type: str) -> tuple[str | None, str]:
        source = "tmdb" if media_type in (MediaTypes.MOVIE.value, MediaTypes.TV.value) else "manual"
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
                    return str(result["media_id"]), source

            return str(results[0]["media_id"]), source
        except Exception as e:
            logger.debug("FA resolve error for '%s': %s", title, e)
            return None, ""


@shared_task(name="Import from FilmAffinity CSV")
def import_from_filmaffinity_csv(
    user_id: int,
    csv_content: str,
    overwrite: bool = False,
) -> str:
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return f"User {user_id} not found."

    importer = FilmAffinityCSVImporter(user, overwrite=overwrite)
    return importer.run(csv_content)
