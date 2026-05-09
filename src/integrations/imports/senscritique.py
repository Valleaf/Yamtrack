"""
Import from SensCritique.
Fetches a user's rated/collected items and creates Yamtrack media entries.

Supports: movies, TV, anime, games, books, comics, music (new).
"""

import logging

from celery import shared_task
from django.contrib.auth import get_user_model

from app.models import Item, MediaTypes
from app.providers import senscritique, services
from integrations.helpers import (
    bulk_create_new_with_history,
    get_or_create_season,
)

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

# SC media_type → Yamtrack source (the provider used for ID resolution)
SC_TO_SOURCE = {
    "movie": "tmdb",
    "tv": "tmdb",
    "anime": "mal",
    "game": "igdb",
    "book": "openlibrary",
    "comic": "comicvine",
    "music": "senscritique",  # music uses SC itself as source
}


class SensCritiqueImporter:
    def __init__(self, user, username: str, password: str | None = None, overwrite: bool = False):
        self.user = user
        self.username = username
        self.overwrite = overwrite
        self.token = None
        self.imported = 0
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

        bulk_media = []

        for product in products:
            media_type = product.get("media_type")
            if not media_type or media_type not in SC_TO_YAMTRACK:
                self.skipped += 1
                continue

            yamtrack_type = SC_TO_YAMTRACK[media_type]
            source = SC_TO_SOURCE[media_type]

            try:
                item = self._build_item(product, yamtrack_type, source)
                if item:
                    bulk_media.append(item)
            except Exception as e:
                logger.error("SC import error for %s: %s", product.get("title"), e)
                self.errors += 1

        if bulk_media:
            created = bulk_create_new_with_history(bulk_media, Item, self.user)
            self.imported = created

        return (
            f"SensCritique import complete: {self.imported} imported, "
            f"{self.skipped} skipped, {self.errors} errors."
        )

    def _build_item(self, product: dict, yamtrack_type: str, source: str) -> Item | None:
        """
        Resolve the SC item to a Yamtrack Item.
        For music (source=senscritique), use SC ID directly.
        For others, try to match by title+year to the appropriate provider.
        """
        title = product.get("title", "")
        year = product.get("year")
        sc_id = product.get("sc_id")
        score = product.get("score")
        poster = product.get("poster")

        if yamtrack_type == MediaTypes.MUSIC.value:
            # Music: use SC as source, store SC id directly
            media_id = sc_id
        else:
            # Try to resolve to external provider ID via title search
            media_id = self._resolve_external_id(title, year, yamtrack_type, source)
            if not media_id:
                logger.debug("SC: could not resolve external ID for '%s', using manual", title)
                source = "manual"
                media_id = f"sc_{sc_id}"

        # Check if already tracked (skip unless overwrite)
        exists = Item.objects.filter(
            user=self.user,
            media_id=media_id,
            media_type=yamtrack_type,
            source=source,
        ).exists()

        if exists and not self.overwrite:
            self.skipped += 1
            return None

        return Item(
            user=self.user,
            media_id=media_id,
            media_type=yamtrack_type,
            source=source,
            title=title,
            image=poster or "",
            score=score * 10 if score is not None else None,  # SC 0-10 → internal 0-100
            status=Item.Status.COMPLETED,
        )

    def _resolve_external_id(
        self, title: str, year: int | None, yamtrack_type: str, source: str
    ) -> str | None:
        """
        Search the appropriate external provider for this item by title and year.
        Returns the external ID string if found, else None.
        """
        try:
            results = services.search_media(yamtrack_type, title)
            if not results:
                return None

            # Pick best match: prefer exact title + year match
            for result in results[:5]:
                result_year = result.get("year") or result.get("release_date", "")[:4]
                title_match = result.get("title", "").lower() == title.lower()
                year_match = year is None or str(result_year) == str(year)

                if title_match and year_match:
                    return str(result["media_id"])

            # Fallback: return first result
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
