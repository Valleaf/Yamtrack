"""
MusicBrainz API provider for Yamtrack.
Uses the MusicBrainz JSON API (no auth needed, open data).
API docs: https://musicbrainz.org/doc/MusicBrainz_API
"""

import logging
import time

import requests

logger = logging.getLogger(__name__)

MB_BASE = "https://musicbrainz.org/ws/2"
HEADERS = {
    "User-Agent": "Yamtrack/1.0 (https://github.com/Valleaf/Yamtrack)",
    "Accept": "application/json",
}

CAA_BASE = "https://coverartarchive.org/release-group"


def _get(endpoint: str, params: dict) -> dict:
    """Make a GET request to the MusicBrainz API."""
    params["fmt"] = "json"
    resp = requests.get(f"{MB_BASE}/{endpoint}", params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    time.sleep(1)  # MusicBrainz rate limit: 1 req/sec
    return resp.json()


def _cover_url(mb_id: str) -> str:
    """Return cover art URL — falls back to empty string if not available."""
    return f"{CAA_BASE}/{mb_id}/front-250"


def search_music(query: str) -> list[dict]:
    """Search MusicBrainz for release groups by query (albums, EPs, singles)."""
    data = _get("release-group", {
        "query": query,
        "limit": 15,
    })
    results = []
    for rg in data.get("release-groups", []):
        artist = ""
        if rg.get("artist-credit"):
            ac = rg["artist-credit"][0]
            artist = ac.get("name") or (ac.get("artist") or {}).get("name", "")

        primary_type = rg.get("primary-type", "")
        secondary_types = rg.get("secondary-types", [])
        type_label = primary_type
        if secondary_types:
            type_label = f"{primary_type} / {', '.join(secondary_types)}"

        results.append({
            "media_id": rg["id"],
            "title": rg.get("title", ""),
            "source": "musicbrainz",
            "image": _cover_url(rg["id"]),
            "year": (rg.get("first-release-date") or "")[:4],
            "artists": [artist] if artist else [],
            "type": type_label,
        })
    return results


def album(mb_id: str) -> dict:
    """Fetch album metadata from MusicBrainz by release-group ID."""
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

    first_release = (data.get("first-release-date") or "")

    primary_type = data.get("primary-type", "")
    secondary_types = data.get("secondary-types", [])
    type_label = primary_type
    if secondary_types:
        type_label = f"{primary_type} / {', '.join(secondary_types)}"

    return {
        "media_id": mb_id,
        "title": data.get("title", ""),
        "source": "musicbrainz",
        "image": _cover_url(mb_id),
        "synopsis": f"By {', '.join(artist_names)}" if artist_names else "",
        "genres": genres,
        "release_date": first_release,
        "rating": None,
        "artists": artist_names,
        "type": type_label,
        "recommendations": [],
    }
