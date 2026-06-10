"""
MusicBrainz API provider for Yamtrack.
Uses the MusicBrainz JSON API (no auth needed, open data).
API docs: https://musicbrainz.org/doc/MusicBrainz_API
"""

import logging
import time

import requests
from django.core.cache import cache
from requests_ratelimiter import LimiterSession

from app import helpers
from app.models import MediaTypes, Sources
logger = logging.getLogger(__name__)

MB_BASE = "https://musicbrainz.org/ws/2"
HEADERS = {
    "User-Agent": "Yamtrack/1.0 (https://github.com/FuzzyGrim/Yamtrack)",
    "Accept": "application/json",
}

# One request per second, shared across all threads — MusicBrainz requirement.
# LimiterSession is thread-safe and blocks the calling thread until the slot is free.
_MB_SESSION = LimiterSession(per_second=1)
_MB_SESSION.headers.update(HEADERS)

CAA_BASE = "https://coverartarchive.org/release-group"
RESULTS_PER_PAGE = 15

# MB type filter values
TYPE_FILTERS = {
    "album": "Album",
    "ep": "EP",
    "single": "Single",
    "broadcast": "Broadcast",
    "other": "Other",
    "artist": None,  # special: search artists not release groups
}


def _get(endpoint: str, params: dict, retries: int = 2) -> dict:
    from app.providers.services import ProviderAPIError  # noqa: PLC0415
    params["fmt"] = "json"
    last_error = None
    for attempt in range(retries + 1):
        try:
            resp = _MB_SESSION.get(f"{MB_BASE}/{endpoint}", params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.Timeout as error:
            last_error = error
            logger.warning(
                "MusicBrainz timeout on %s (attempt %d/%d)",
                endpoint, attempt + 1, retries + 1,
            )
            if attempt < retries:
                time.sleep(2 ** attempt)  # 1s, 2s backoff
        except requests.exceptions.RequestException as error:
            raise ProviderAPIError(Sources.MUSICBRAINZ.value, error) from None
    raise ProviderAPIError(Sources.MUSICBRAINZ.value, last_error, "Request timed out after retries") from None


def _cover_url(mb_id: str) -> str:
    return f"{CAA_BASE}/{mb_id}/front-250"


def _format_artists(obj: dict) -> list[str]:
    names = []
    for ac in obj.get("artist-credit", []):
        if isinstance(ac, dict):
            name = ac.get("name") or (ac.get("artist") or {}).get("name", "")
            if name:
                names.append(name)
    return names


def _artist_id(obj: dict) -> str | None:
    for ac in obj.get("artist-credit", []):
        if isinstance(ac, dict) and ac.get("artist"):
            return ac["artist"].get("id")
    return None


def search_music(query: str, page: int = 1, mb_type: str = "") -> dict:
    """Search MusicBrainz. mb_type: album|ep|single|artist or empty for all."""
    if mb_type == "artist":
        return search_artists(query, page)

    cache_key = f"search_musicbrainz_{query}_{page}_{mb_type}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    offset = (page - 1) * RESULTS_PER_PAGE
    params = {
        "query": query,
        "limit": RESULTS_PER_PAGE,
        "offset": offset,
    }
    if mb_type and mb_type in TYPE_FILTERS:
        params["type"] = mb_type

    data = _get("release-group", params)
    total = data.get("release-group-count", 0)
    results = []

    for rg in data.get("release-groups", []):
        artists = _format_artists(rg)
        primary_type = rg.get("primary-type", "")
        secondary_types = rg.get("secondary-types", [])
        type_label = primary_type
        if secondary_types:
            type_label = f"{primary_type} / {', '.join(secondary_types)}"

        results.append({
            "media_id": rg["id"],
            "title": rg.get("title", ""),
            "media_type": MediaTypes.MUSIC.value,
            "source": Sources.MUSICBRAINZ.value,
            "image": _cover_url(rg["id"]),
            "year": (rg.get("first-release-date") or "")[:4] or None,
            "artists": artists,
            "subtitle": ", ".join(artists) if artists else None,
            "type": type_label,
        })

    response = helpers.format_search_response(page, RESULTS_PER_PAGE, total, results)
    cache.set(cache_key, response, 300)
    return response


def search_artists(query: str, page: int = 1) -> dict:
    """Search MusicBrainz for artists."""
    cache_key = f"search_mb_artists_{query}_{page}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    offset = (page - 1) * RESULTS_PER_PAGE
    data = _get("artist", {
        "query": query,
        "limit": RESULTS_PER_PAGE,
        "offset": offset,
    })

    total = data.get("count", 0)
    results = []
    for artist in data.get("artists", []):
        tags = [t["name"] for t in (artist.get("tags") or [])[:3]]
        results.append({
            "media_id": artist["id"],
            "title": artist.get("name", ""),
            "media_type": "music_artist",  # special type for routing
            "source": Sources.MUSICBRAINZ.value,
            "image": "",
            "year": (artist.get("life-span") or {}).get("begin", "")[:4],
            "artists": tags,  # reuse artists field for genre tags display
            "type": artist.get("type", ""),
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

    artist_names = _format_artists(data)
    artist_id = _artist_id(data)

    genres = [g["name"] for g in (data.get("genres") or [])]
    if not genres:
        genres = [t["name"] for t in (data.get("tags") or [])[:5]]

    primary_type = data.get("primary-type", "")
    secondary_types = data.get("secondary-types", [])
    type_label = primary_type
    if secondary_types:
        type_label = f"{primary_type} / {', '.join(secondary_types)}"

    first_release = data.get("first-release-date", "")

    # Get tracklist from first official release
    tracklist = _get_tracklist(mb_id)

    # Get other albums by same artist for recommendations
    recommendations = []
    if artist_id:
        recommendations = _get_artist_albums(artist_id, exclude_id=mb_id)

    # Build artist link for the detail page
    artist_links = []
    for ac in data.get("artist-credit", []):
        if isinstance(ac, dict) and ac.get("artist"):
            artist_links.append({
                "id": ac["artist"]["id"],
                "name": ac.get("name") or ac["artist"].get("name", ""),
            })

    result = {
        "media_id": mb_id,
        "source": Sources.MUSICBRAINZ.value,
        "source_url": f"https://musicbrainz.org/release-group/{mb_id}",
        "media_type": MediaTypes.MUSIC.value,
        "title": data.get("title", ""),
        "max_progress": 1,
        "image": _cover_url(mb_id),
        "synopsis": f"By {', '.join(artist_names)}" if artist_names else "",
        "genres": genres,
        "score": None,
        "score_count": 0,
        "details": {
            "format": type_label or "Album",
            "release_date": first_release,
            "artists": ", ".join(artist_names),
        },
        "artist_links": artist_links,
        "tracklist": tracklist,
        "cast": [],
        "total_cast_count": 0,
        "related": {
            "More by this artist": recommendations,
        },
    }

    cache.set(cache_key, result, 3600)
    return result


def _get_tracklist(rg_id: str) -> list[dict]:
    """Fetch tracklist from the first official release of a release group."""
    cache_key = f"musicbrainz_tracklist_{rg_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    try:
        # Get releases in this release group
        rg_data = _get(f"release", {
            "release-group": rg_id,
            "inc": "recordings",
            "limit": 1,
        })
        releases = rg_data.get("releases", [])
        if not releases:
            cache.set(cache_key, [], 3600)
            return []

        release_id = releases[0]["id"]
        release_data = _get(f"release/{release_id}", {
            "inc": "recordings",
        })

        tracks = []
        for medium in release_data.get("media", []):
            for track in medium.get("tracks", []):
                recording = track.get("recording", {})
                duration_ms = recording.get("length") or track.get("length")
                duration = ""
                if duration_ms:
                    secs = duration_ms // 1000
                    duration = f"{secs // 60}:{secs % 60:02d}"
                tracks.append({
                    "number": track.get("number", ""),
                    "title": track.get("title") or recording.get("title", ""),
                    "duration": duration,
                })
        cache.set(cache_key, tracks, 3600)
        return tracks

    except Exception as e:
        logger.warning("MusicBrainz tracklist error for %s: %s", rg_id, e)
        return []


def artist(artist_id: str) -> dict:
    """Fetch artist metadata and discography."""
    cache_key = f"musicbrainz_artist_{artist_id}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    data = _get(f"artist/{artist_id}", {
        "inc": "release-groups+genres+tags+url-rels",
    })

    genres = [g["name"] for g in (data.get("genres") or [])]
    if not genres:
        genres = [t["name"] for t in (data.get("tags") or [])[:8]]

    # Find Wikipedia/Wikidata URL for bio
    bio_url = ""
    for rel in data.get("relations", []) or []:
        if rel.get("type") in ("wikipedia", "wikidata"):
            bio_url = (rel.get("url") or {}).get("resource", "")
            break

    # Group release groups by type
    all_rgs = data.get("release-groups", [])
    discography = {}
    for rg in all_rgs:
        rg_type = rg.get("primary-type", "Other")
        if rg_type not in discography:
            discography[rg_type] = []
        discography[rg_type].append({
            "media_id": rg["id"],
            "title": rg.get("title", ""),
            "media_type": MediaTypes.MUSIC.value,
            "source": Sources.MUSICBRAINZ.value,
            "image": _cover_url(rg["id"]),
            "year": (rg.get("first-release-date") or "")[:4],
            "type": rg.get("primary-type", ""),
        })

    # Sort each group by year descending
    for rg_type in discography:
        discography[rg_type].sort(key=lambda x: x.get("year", ""), reverse=True)

    life_span = data.get("life-span") or {}
    result = {
        "artist_id": artist_id,
        "name": data.get("name", ""),
        "sort_name": data.get("sort-name", ""),
        "type": data.get("type", ""),
        "genres": genres,
        "begin": life_span.get("begin", ""),
        "ended": life_span.get("ended", False),
        "end": life_span.get("end", ""),
        "source_url": f"https://musicbrainz.org/artist/{artist_id}",
        "bio_url": bio_url,
        "discography": discography,
    }

    cache.set(cache_key, result, 3600)
    return result


def _get_artist_albums(artist_id: str, exclude_id: str = "", limit: int = 10) -> list[dict]:
    """Get other release groups by an artist for recommendations."""
    try:
        cache_key = f"musicbrainz_artist_albums_{artist_id}"
        cached = cache.get(cache_key)
        if not cached:
            data = _get("release-group", {
                "artist": artist_id,
                "type": "album|ep|single",
                "limit": 25,
            })
            cached = data.get("release-groups", [])
            cache.set(cache_key, cached, 3600)

        results = []
        for rg in cached:
            if rg["id"] == exclude_id:
                continue
            results.append({
                "media_id": rg["id"],
                "title": rg.get("title", ""),
                "media_type": MediaTypes.MUSIC.value,
                "source": Sources.MUSICBRAINZ.value,
                "image": _cover_url(rg["id"]),
                "year": (rg.get("first-release-date") or "")[:4],
            })
            if len(results) >= limit:
                break
        return results
    except Exception as e:
        logger.debug("MusicBrainz artist albums error: %s", e)
        return []
