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
    if source == "igdb_collection":
        return _fetch_igdb_collection(source_id)
    msg = f"Unknown collection source: {source}"
    raise ValueError(msg)


def search(source, query):
    """Search for collections by name on the given source."""
    if source == "tmdb_collection":
        return _search_tmdb_collection(query)
    if source == "igdb_collection":
        return _search_igdb_collection(query)
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
    seen_ids = set()
    for part in col_data.get("parts", []):
        key = (str(part["media_id"]), part["source"], part["media_type"])
        if key in seen_ids:
            continue
        seen_ids.add(key)
        title = (part["title"] or "").strip()
        image = part.get("image", "")
        item, item_new = Item.objects.get_or_create(
            media_id=str(part["media_id"]),
            source=part["source"],
            media_type=part["media_type"],
            defaults={"title": title, "image": image},
        )
        # Backfill title/image if the stub was created with empty values
        if not item_new and (not item.title or not item.image):
            update_fields = []
            if not item.title and title:
                item.title = title
                update_fields.append("title")
            if not item.image and image:
                item.image = image
                update_fields.append("image")
            if update_fields:
                item.save(update_fields=update_fields)
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


def _fetch_igdb_collection(source_id):
    """Fetch an IGDB game series/collection by ID and return normalised data."""
    from django.conf import settings as django_settings
    from app.providers import igdb as igdb_provider

    access_token = igdb_provider.get_access_token()
    url = f"{igdb_provider.base_url}/collections"
    query = (
        f"fields name,games.id,games.name,games.cover.image_id;"
        f"where id = {source_id};"
    )
    headers = {
        "Client-ID": django_settings.IGDB_ID,
        "Authorization": f"Bearer {access_token}",
    }
    response = services.api_request(
        Sources.IGDB.value,
        "POST",
        url,
        data=query,
        headers=headers,
    )
    if not response:
        return None
    col = response[0]
    parts = [
        {
            "source": Sources.IGDB.value,
            "media_id": str(g["id"]),
            "media_type": MediaTypes.GAME.value,
            "title": g["name"],
            "image": igdb_provider.get_image_url(g),
        }
        for g in col.get("games", [])
    ]
    return {
        "name": col.get("name", ""),
        "description": "",
        "image": parts[0]["image"] if parts else "",
        "source_id": str(source_id),
        "items": parts,
    }


def _search_igdb_collection(query):
    """Search IGDB for game series/collections matching query."""
    from django.conf import settings as django_settings
    from app.providers import igdb as igdb_provider

    access_token = igdb_provider.get_access_token()
    url = f"{igdb_provider.base_url}/collections"
    body = (
        f'fields id,name; search "{query}"; limit 10;'
    )
    headers = {
        "Client-ID": django_settings.IGDB_ID,
        "Authorization": f"Bearer {access_token}",
    }
    try:
        response = services.api_request(
            Sources.IGDB.value,
            "POST",
            url,
            data=body,
            headers=headers,
        )
    except Exception:
        logger.exception("IGDB collection search failed")
        return []
    return [
        {
            "id": str(item["id"]),
            "name": item.get("name", ""),
            "image": "",
            "year": None,
        }
        for item in (response or [])
    ]
