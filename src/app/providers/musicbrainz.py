"""
MusicBrainz API provider for Yamtrack.
Uses the MusicBrainz JSON API (no auth needed, open data).
API docs: https://musicbrainz.org/doc/MusicBrainz_API
"""

import logging
import time

import requests
from django.core.cache import cache

from app import helpers
from app.models import MediaTypes

logger = logging.getLogger(__name__)

MB_BASE = "https://musicbrainz.org/ws/2"
HEADERS = {
    "User-Agent": "Yamtrack/1.0 (https://github.com/Valleaf/Yamtrack)",
    "Accept": "application/json",
}

CAA_BASE = "https://coverartarchive.org/release-group"
RESULTS_PER_PAGE = 15


def _get(endpoint: str, params: dict) -> dict:
    """Make a GET request to the MusicBrainz API."""
    params["fmt"] = "json"
    resp = requests.get(f"{MB_BASE}/{endpoint}", params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    time.sleep(1)  # MusicBrainz rate limit: 1 req/sec
    return resp.json()


def _cover_url(mb_id: str) -> str:
    return f"{CAA_BASE}/{mb_id}/front-250"


def _format_artist(rg: dict) -> str:
    for ac in rg.get("artist-credit", []):
        if isinstance(ac, dict):
            name = ac.get("name") or (ac.get("artist") or {}).get("name", "")
            if name:
                return name
    return ""


def search_music(query: str, page: int = 1) -> dict:
    """Search MusicBrainz for release groups. Returns paginated response dict."""
    cache_key = f"search_musicbrainz_{query}_{page}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    offset = (page - 1) * RESULTS_PER_PAGE
    data = _get("release-group", {
        "query": query,
        "limit": RESULTS_PER_PAGE,
        "offset": offset,
    })

    total = data.get("release-group-count", 0)
    results = []
    for rg in data.get("release-groups", []):
        artist = _format_artist(rg)
        primary_type = rg.get("primary-type", "")
        secondary_types = rg.get("secondary-types", [])
        type_label = primary_type
        if secondary_types:
            type_label = f"{primary_type} / {', '.join(secondary_types)}"

        results.append({
            "media_id": rg["id"],
            "title": rg.get("title", ""),
            "media_type": MediaTypes.MUSIC.value,
            "source": "musicbrainz",
            "image": _cover_url(rg["id"]),
            "year": (rg.get("first-release-date") or "")[:4],
            "artists": [artist] if artist else [],
            "type": type_label,
        })

    response = helpers.format_search_response(page, RESULTS_PER_PAGE, total, results)
    cache.set(cache_key, response, 300)
    return response


def album(mb_id: str) -> dict:
    """Fetch album metadata from MusicBrainz by release-group ID."""
    cache_key = f"musicbrainz_album_{mb_id}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    data = _get(f"release-group/{mb_id}", {
        "inc": "artists+releases+genres+tags",
    })

    artist_names = []
    for ac in data.get("artist-credit", []):
        if isinstance(ac, dict):
            name = ac.get("name") or (ac.get("artist") or {}).get("name", "")
            if name:
                artist_names.append(name)

    genres = [g["name"] for g in (data.get("genres") or [])]
    if not genres:
        genres = [t["name"] for t in (data.get("tags") or [])[:5]]

    primary_type = data.get("primary-type", "")
    secondary_types = data.get("secondary-types", [])
    type_label = primary_type
    if secondary_types:
        type_label = f"{primary_type} / {', '.join(secondary_types)}"

    result = {
        "media_id": mb_id,
        "title": data.get("title", ""),
        "source": "musicbrainz",
        "image": _cover_url(mb_id),
        "synopsis": f"By {', '.join(artist_names)}" if artist_names else "",
        "genres": genres,
        "release_date": data.get("first-release-date", ""),
        "rating": None,
        "artists": artist_names,
        "type": type_label,
        "recommendations": [],
    }

    cache.set(cache_key, result, 3600)
    return result
