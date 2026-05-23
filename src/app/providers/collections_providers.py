"""Providers for auto-sourcing media collections from external APIs."""

import logging

from app.models import Item, MediaTypes, Sources
from app.providers import services, tmdb

logger = logging.getLogger(__name__)

SOURCE_CHOICES = [
    ("manual", "Manual"),
    ("tmdb_collection", "TMDB Collection"),
]


def get_source_label(source):
    """Return human-readable label for a source key."""
    return dict(SOURCE_CHOICES).get(source, source)


def fetch(source, source_id):
    """Fetch collection data from the given source.

    Returns dict with keys: name, description, image, source_id, items[]
    Each item: media_id, source, media_type, title, image
    """
    if source == "tmdb_collection":
        return _fetch_tmdb_collection(source_id)
    msg = f"Unknown collection source: {source}"
    raise ValueError(msg)


def search(source, query):
    """Search for collections by name on the given source.

    Returns list of dicts: id, name, image, year
    """
    if source == "tmdb_collection":
        return _search_tmdb_collection(query)
    return []


def sync_tmdb_collection(user, movie_metadata):
    """Auto-create or update a Collection from TMDB collection data.

    Called after a TMDB movie is saved. Creates a shared Collection owned
    by the user (or updates it) with all parts from the TMDB collection.
    Idempotent - safe to call multiple times.
    """
    from media_collections.models import Collection, CollectionItem

    tmdb_col = movie_metadata.get("tmdb_collection")
    if not tmdb_col or not tmdb_col.get("id"):
        return None

    collection_id = str(tmdb_col["id"])
    collection_name = tmdb_col["name"]
    collection_image = tmdb_col.get("image", "")

    # Find or create the Collection record for this TMDB collection
    collection, created = Collection.objects.get_or_create(
        source="tmdb_collection",
        source_id=collection_id,
        owner=user,
        defaults={
            "name": collection_name,
            "description": "",
        },
    )

    if not created:
        # Update name in case it changed on TMDB
        if collection.name != collection_name:
            collection.name = collection_name
            collection.save(update_fields=["name"])

    logger.info(
        "%s TMDB collection '%s' for user %s",
        "Created" if created else "Found existing",
        collection_name,
        user,
    )

    # Sync all parts into CollectionItems
    parts = tmdb_col.get("parts", [])
    added = 0
    for part in parts:
        media_id = str(part["media_id"])
        item, _ = Item.objects.get_or_create(
            media_id=media_id,
            source=Sources.TMDB.value,
            media_type=MediaTypes.MOVIE.value,
            defaults={
                "title": part["title"],
                "image": part.get("image", ""),
            },
        )
        _, item_created = CollectionItem.objects.get_or_create(
            collection=collection,
            item=item,
            defaults={"notes": ""},
        )
        if item_created:
            added += 1

    if added:
        logger.info("Added %d new items to collection '%s'", added, collection_name)

    return collection


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
