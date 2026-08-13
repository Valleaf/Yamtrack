"""Providers for auto-sourcing media collections from external APIs."""

import logging

from app.models import Item, MediaTypes, Sources
from app.providers import services, tmdb

logger = logging.getLogger(__name__)


def _series_position(value):
    try:
        position = int(str(value).strip())
    except (TypeError, ValueError):
        return None
    return position if position >= 0 else None

SOURCE_CHOICES = [
    ("manual", "Manual"),
    ("tmdb_collection", "TMDB Collection"),
    ("igdb_collection", "IGDB Game Series"),
    ("hardcover_series", "Hardcover Book Series"),
    ("comicvine_arc", "ComicVine Story Arc"),
    ("comicvine_volume", "ComicVine Volume (Issues)"),
    ("bnf_series", "BnF Series (BD)"),
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
    if source == "comicvine_arc":
        return _fetch_comicvine_arc(source_id)
    if source == "comicvine_volume":
        return _fetch_comicvine_volume(source_id)
    if source == "bnf_series":
        return _fetch_bnf_series(source_id)
    msg = f"Unknown collection source: {source}"
    raise ValueError(msg)


def search(source, query):
    """Search for collections by name on the given source."""
    if source == "tmdb_collection":
        return _search_tmdb_collection(query)
    if source == "igdb_collection":
        return _search_igdb_collection(query)
    if source == "comicvine_arc":
        return _search_comicvine_arc(query)
    if source == "bnf_series":
        return _search_bnf_series(query)
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
        # Sync title to the provider-verified value if it differs (not just when
        # empty) -- a stub Item can have a stale/wrong title left over from an
        # earlier sync or an unrelated import match, and this collection part data
        # is always freshly fetched from the source provider, so it's authoritative.
        # Image is only backfilled when missing -- a placeholder is a worse signal
        # than "different" so we don't want to flap between two valid covers.
        if not item_new:
            update_fields = []
            if title and item.title != title:
                item.title = title
                update_fields.append("title")
            if not item.image and image:
                item.image = image
                update_fields.append("image")
            if update_fields:
                item.save(update_fields=update_fields)
        series_position = _series_position(part.get("series_position"))
        collection_item, item_created = CollectionItem.objects.get_or_create(
            collection=collection,
            item=item,
            defaults={"notes": "", "series_position": series_position},
        )
        if not item_created and collection_item.series_position != series_position:
            collection_item.series_position = series_position
            collection_item.save(update_fields=["series_position"])
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


def sync_comicvine_arc(user, arc_data):
    """Create/update a Collection from a ComicVine story arc data dict.

    Unlike TMDB/IGDB/Hardcover this is not called automatically on save
    because a ComicVine volume can belong to many story arcs simultaneously,
    making auto-selection ambiguous.  The caller must pass the normalised
    arc data dict (as returned by _fetch_comicvine_arc) directly.
    """
    return _sync_collection(user, arc_data, "comicvine_arc")


def sync_comicvine_volume(user, comic_metadata):
    """Auto-create/update a Collection from a Comic Vine issue's volume data.

    `comic_metadata` is what `comicvine.comic()` returns for an
    issue-tracked comic (media_id starting with "i") -- its
    `comicvine_volume` key holds every issue in that issue's parent
    volume, built by `comicvine._build_volume_collection()`. Mirrors
    `sync_bnf_series` below.
    """
    return _sync_collection(
        user, comic_metadata.get("comicvine_volume"), "comicvine_volume",
    )


def sync_bnf_series(user, comic_metadata):
    """Auto-create/update a Collection from a BnF comic's series data."""
    return _sync_collection(user, comic_metadata.get("bnf_series"), "bnf_series")


def get_collection_for_media(user, media_metadata, source_key):
    """Return the Collection DB object for this media's collection, if it exists."""
    from media_collections.models import Collection

    field_map = {
        "tmdb_collection": "tmdb_collection",
        "igdb_collection": "igdb_collection",
        "hardcover_series": "hardcover_series",
        "bnf_series": "bnf_series",
        "comicvine_volume": "comicvine_volume",
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


_COMICVINE_BASE_URL = "https://comicvine.gamespot.com/api"
_COMICVINE_HEADERS = {"User-Agent": "Mozilla/5.0"}


def _search_comicvine_arc(query):
    """Search ComicVine for story arcs whose name matches *query*."""
    from django.conf import settings as django_settings

    params = {
        "api_key": django_settings.COMICVINE_API,
        "format": "json",
        "query": query,
        "resources": "story_arc",
        "field_list": "id,name,image",
        "limit": 10,
    }
    try:
        response = services.api_request(
            Sources.COMICVINE.value,
            "GET",
            f"{_COMICVINE_BASE_URL}/search/",
            params=params,
            headers=_COMICVINE_HEADERS,
        )
    except Exception:
        logger.exception("ComicVine story arc search failed for %r", query)
        return []

    return [
        {
            "id": str(item["id"]),
            "name": item.get("name", ""),
            "image": (item.get("image") or {}).get("medium_url", ""),
            "year": None,
        }
        for item in (response.get("results") or [])[:10]
    ]


def _fetch_comicvine_arc(source_id):
    """Fetch a ComicVine story arc and return normalised collection data.

    The arc's issue list is used to derive the set of unique *volumes* that
    belong to the story.  Issue images are not used — volume-level covers will
    be populated naturally as users track individual comics (the Item record is
    created/updated at tracking time).

    ComicVine story arc IDs use the ``4045-`` type prefix on the detail
    endpoint, so ``source_id`` must be the bare numeric ID only.
    """
    from django.conf import settings as django_settings

    params = {
        "api_key": django_settings.COMICVINE_API,
        "format": "json",
        "field_list": "id,name,image,issues",
    }
    try:
        response = services.api_request(
            Sources.COMICVINE.value,
            "GET",
            f"{_COMICVINE_BASE_URL}/story_arc/4045-{source_id}/",
            params=params,
            headers=_COMICVINE_HEADERS,
        )
    except Exception:
        logger.exception("ComicVine story arc fetch failed for source_id=%s", source_id)
        return None

    arc = response.get("results") or {}
    if not arc:
        return None

    # Derive the deduplicated volume list from the arc's issues.
    # Each issue carries a 'volume' sub-object: {id, name}.
    seen_volume_ids: set[int] = set()
    parts = []
    for issue in arc.get("issues") or []:
        volume = issue.get("volume") or {}
        vol_id = volume.get("id")
        if not vol_id or vol_id in seen_volume_ids:
            continue
        seen_volume_ids.add(vol_id)
        parts.append(
            {
                "source": Sources.COMICVINE.value,
                "media_id": str(vol_id),
                "media_type": MediaTypes.COMIC.value,
                "title": volume.get("name", ""),
                "image": "",
            }
        )

    logger.info(
        "ComicVine arc '%s' resolved to %d unique volumes",
        arc.get("name", source_id),
        len(parts),
    )

    return {
        "id": str(arc.get("id", source_id)),
        "name": arc.get("name", ""),
        "description": "",
        "image": (arc.get("image") or {}).get("medium_url", ""),
        "source_id": str(source_id),
        "items": parts,
        "parts": parts,  # _sync_collection reads 'parts', fetch() callers read 'items'
    }


def _fetch_comicvine_volume(source_id):
    """Re-fetch a Comic Vine volume's issue list for the manual Sync button.

    Reuses ``comicvine._build_volume_collection()`` -- the same builder that
    seeds the collection the first time an issue in this volume is tracked
    (see ``sync_comicvine_volume``) -- so a manual re-sync picks up any new
    issues Comic Vine has added since.

    Deliberately doesn't refetch the volume *name*: ``_build_volume_collection``
    has no name lookup of its own (the name comes from the issue payload's
    nested ``volume.name`` at first-sync time), so this returns ``name=""``.
    ``_sync_items`` only overwrites ``Collection.name`` when truthy, so the
    existing name is left alone on re-sync.
    """
    from app.providers import comicvine

    col_data = comicvine._build_volume_collection(source_id)
    if not col_data:
        return None
    # _sync_collection/_sync_items read 'parts'/'items' respectively (see
    # _fetch_comicvine_arc above for the same dual-key shim).
    return {**col_data, "items": col_data["parts"]}


def _search_bnf_series(query: str) -> list[dict]:
    """Return the query itself as a single selectable series candidate.

    BnF has no "series catalogue" endpoint — series are just a MARC field
    on individual records.  The user types the series name they want
    (e.g. "Astérix"), we echo it back as a result so they can confirm it,
    then ``_fetch_bnf_series`` does the real lookup.

    Diacritics are normalised by BnF\'s SRU engine, so plain ASCII input
    ("Asterix") will still match accented records ("Astérix").
    """
    q = query.strip()
    if len(q) < 2:  # noqa: PLR2004
        return []
    return [{"id": q, "name": q, "image": "", "year": None}]


def _fetch_bnf_series(series_name: str) -> dict | None:
    """Fetch all BnF albums in *series_name* and return normalised collection data.

    Calls ``bnf.search_by_series()``, which searches BnF's ``bib.anywhere``
    full-text index and keeps only records whose own Collection statement
    (in dc:description) matches *series_name*. Each matched record becomes
    a collection part with ``source=bnf``.

    The collection image is taken from the first matched album\'s cover so
    the collection card has something to show immediately.
    """
    from app.providers import bnf as bnf_provider

    records = bnf_provider.search_by_series(series_name)
    if not records:
        logger.warning("BnF series %r returned no results", series_name)
        return None

    parts = [
        {
            "source": Sources.BNF.value,
            "media_id": r["media_id"],
            "media_type": MediaTypes.COMIC.value,
            "title": r["title"],
            "image": r.get("image", ""),
            "series_position": r.get("series_position"),
        }
        for r in records
    ]

    # Use the first album\'s cover as a representative image for the collection card.
    collection_image = next((p["image"] for p in parts if p["image"]), "")

    return {
        "id": series_name,
        "name": series_name,
        "description": "",
        "image": collection_image,
        "source_id": series_name,
        "items": parts,
        "parts": parts,
    }
