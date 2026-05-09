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


def _get(endpoint: str, params: dict) -> dict:
    """Make a GET request to the MusicBrainz API."""
    params["fmt"] = "json"
    resp = requests.get(f"{MB_BASE}/{endpoint}", params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    time.sleep(1)  # MusicBrainz rate limit: 1 req/sec
    return resp.json()


def search_music(query: str) -> list[dict]:
    """Search MusicBrainz for release groups (albums) by query."""
    data = _get("release-group", {
        "query": query,
        "type": "album",
        "limit": 10,
    })
    results = []
    for rg in data.get("release-groups", []):
        artist = ""
        if rg.get("artist-credit"):
            artist = rg["artist-credit"][0].get("name", "")
        results.append({
            "media_id": rg["id"],
            "title": rg.get("title", ""),
            "source": "musicbrainz",
            "image": f"https://coverartarchive.org/release-group/{rg['id']}/front-250",
            "year": (rg.get("first-release-date") or "")[:4],
            "artists": [artist] if artist else [],
        })
    return results


def album(mb_id: str) -> dict:
    """Fetch album metadata from MusicBrainz by release-group ID."""
    data = _get(f"release-group/{mb_id}", {
        "inc": "artists+releases+genres+tags",
    })

    artist_names = [
        ac.get("name", "") or ac.get("artist", {}).get("name", "")
        for ac in data.get("artist-credit", [])
        if isinstance(ac, dict)
    ]

    genres = [g["name"] for g in data.get("genres", [])]
    if not genres:
        genres = [t["name"] for t in data.get("tags", [])[:5]]

    first_release = (data.get("first-release-date") or "")

    return {
        "media_id": mb_id,
        "title": data.get("title", ""),
        "source": "musicbrainz",
        "image": f"https://coverartarchive.org/release-group/{mb_id}/front-250",
        "synopsis": "",
        "genres": genres,
        "release_date": first_release,
        "rating": None,
        "artists": artist_names,
        "recommendations": [],
    }