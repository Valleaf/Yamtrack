"""Last.fm statistics provider.

The API key is configured server-side with ``LASTFM_API_KEY``. Usernames are
user-supplied, so responses are cached per username and failures are treated
as an unavailable optional integration.
"""

import logging

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

API_URL = "https://ws.audioscrobbler.com/2.0/"
CACHE_TTL = 60 * 30


def _request(username: str, method: str, limit: int = 10) -> dict:
    api_key = getattr(settings, "LASTFM_API_KEY", "")
    if not api_key or not username:
        return {}
    response = requests.get(
        API_URL,
        params={
            "api_key": api_key,
            "format": "json",
            "method": method,
            "user": username,
            "limit": limit,
        },
        timeout=15,
    )
    response.raise_for_status()
    payload = response.json()
    if "error" in payload:
        return {}
    return payload


def user_stats(username: str, *, refresh: bool = False) -> dict:
    """Return normalized Last.fm stats, or an empty dict if unavailable."""
    username = (username or "").strip()
    if not username or not getattr(settings, "LASTFM_API_KEY", ""):
        return {}

    cache_key = f"lastfm_stats_{username.casefold()}"
    if not refresh:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    try:
        recent = _request(username, "user.getrecenttracks")
        top_artists = _request(username, "user.gettopartists")
        top_albums = _request(username, "user.gettopalbums")
        top_tracks = _request(username, "user.gettoptracks")
    except requests.RequestException:
        logger.warning("Last.fm request failed for %s", username, exc_info=True)
        return {}

    result = {
        "username": username,
        "recent_tracks": recent.get("recenttracks", {}).get("track", []),
        "top_artists": top_artists.get("topartists", {}).get("artist", []),
        "top_albums": top_albums.get("topalbums", {}).get("album", []),
        "top_tracks": top_tracks.get("toptracks", {}).get("track", []),
    }
    cache.set(cache_key, result, CACHE_TTL)
    return result
