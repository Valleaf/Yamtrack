"""Providers for auto-sourcing media collections from external APIs."""

import logging

from app.models import Item, MediaTypes, Sources
from app.providers import services, tmdb

logger = logging.getLogger(__name__)

SOURCE_CHOICES = [
    ("manual", "Manual"),
    ("tmdb_collection", "TMDB Collection"),
    ("igdb_collection", "IGDB Game Series"),
    ("hardcover_series", "Hardcover Book Series"),
]


def get_source_label(source):
    """Return human-readable label for a source key."""
    return dict(SOURCE_CHOICES).get(source, source)


def fetch(source, source_id):
    """Fetch collection data from the given source."""
    if source == "tmdb_collection":
        return _fetch_tmdb_collection(source_id)
    msg = f"Unknown collection source: {source}"
    raise ValueError(msg)


def search(source, query):
    """Search for collections by name on the given source."""
    if source == "tmdb_collection":
        return _search_tmdb_collection(query)
    return []


def _sync_collection(user, col_data, source_key):
    """Generic helper: create/update a Collection and sync its parts."""
    from media_collections.models import Collection, CollectionItem

    if not col_data or not col_data.get("id"):
        return None

    collection, created = Collection.objects.get_or_create(
        source=source_key,
        source_id=str(col_data["id"]),
        owner=user,
        defaults={"name": col_data["name"], "description": ""},
    )

    if not created and collection.name != col_data["name"]:
        collection.name = col_data["name"]
        collection.save(update_fields=["name"])

    logger.info(
        "%s %s collection '%s' for user %s",
        "Created" if created else "Found",
        source_key,
        col_data["name"],
        user,
    )

    added = 0
    for part in col_data.get("parts", []):
        item, _ = Item.objects.get_or_create(
            media_id=str(part["media_id"]),
            source=part["source"],
            media_type=part["media_type"],
            defaults={"title": part["title"], "image": part.get("image", "")},
        )
        _, item_created = CollectionItem.objects.get_or_create(
            collection=collection,
            item=item,
            defaults={"notes": ""},
        )
        if item_created:
            added += 1

    if added:
        logger.info("Added %d new items to '%s'", added, col_data["name"])

    return collection


def sync_tmdb_collection(user, movie_metadata):
    """Auto-create/update a Collection from a TMDB movie's collection data."""
    return _sync_collection(user, movie_metadata.get("tmdb_collection"), "tmdb_collection")


def sync_igdb_collection(user, game_metadata):
    """Auto-create/update a Collection from an IGDB game's collection data."""
    return _sync_collection(user, game_metadata.get("igdb_collection"), "igdb_collection")


def sync_hardcover_series(user, book_metadata):
    """Auto-create/update a Collection from a Hardcover book's series data."""
    return _sync_collection(user, book_metadata.get("hardcover_series"), "hardcover_series")


def get_collection_for_media(user, media_metadata, source_key):
    """Return the Collection DB object for this media's collection, if it exists."""
    from media_collections.models import Collection

    field_map = {
        "tmdb_collection": "tmdb_collection",
        "igdb_collection": "igdb_collection",
        "hardcover_series": "hardcover_series",
    }
    field = field_map.get(source_key)
    if not field:
        return None
    col_data = media_metadata.get(field)
    if not col_data or not col_data.get("id"):
        return None
    return Collection.objects.filter(
        owner=user,
        source=source_key,
        source_id=str(col_data["id"]),
    ).first()


def _fetch_tmdb_collection(source_id):
    """Fetch a TMDB collection by ID and return normalised data."""
    base_url = "https://api.themoviedb.org/3"
    response = services.api_request(
        Sources.TMDB.value,
        "GET",
        f"{base_url}/collection/{source_id}",
        params={"language": "en-US"},
    )
    parts = tmdb.get_collection(response)
    return {
        "name": response.get("name", ""),
        "description": response.get("overview", ""),
        "image": tmdb.get_image_url(response.get("poster_path")),
        "source_id": str(source_id),
        "items": parts,
    }


def _search_tmdb_collection(query):
    """Search TMDB for collections matching query."""
    base_url = "https://api.themoviedb.org/3"
    response = services.api_request(
        Sources.TMDB.value,
        "GET",
        f"{base_url}/search/collection",
        params={"query": query, "language": "en-US"},
    )
    results = []
    for item in response.get("results", [])[:10]:
        results.append({
            "id": str(item["id"]),
            "name": item.get("name", ""),
            "image": tmdb.get_image_url(item.get("poster_path")),
            "year": None,
        })
    return results
