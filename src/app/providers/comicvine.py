import logging

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.cache import cache

from app import helpers
from app.models import MediaTypes, Sources
from app.providers import services

logger = logging.getLogger(__name__)
base_url = "https://comicvine.gamespot.com/api"
headers = {
    "User-Agent": "Mozilla/5.0",
}


def handle_error(error):
    """Handle ComicVine API errors."""
    error_resp = error.response
    status_code = error_resp.status_code

    try:
        error_json = error_resp.json()
    except requests.exceptions.JSONDecodeError as json_error:
        logger.exception("Failed to decode JSON response")
        raise services.ProviderAPIError(Sources.COMICVINE.value, error) from json_error

    # Handle invalid API key
    if status_code == requests.codes.unauthorized:
        details = error_json["error"]
        raise services.ProviderAPIError(Sources.COMICVINE.value, error, details)

    raise services.ProviderAPIError(Sources.COMICVINE.value, error)


def _issue_title(item, volume_name=None):
    """Build a display title for an issue, falling back when `name` is blank.

    Many issues -- especially single-issue American comics -- have no
    populated `name` at all. Falls back to "<volume> #<number>" when both
    are available, then just the volume name, then "Untitled".
    """
    name = item.get("name")
    if name:
        return name
    volume_name = volume_name or (item.get("volume") or {}).get("name")
    number = item.get("issue_number")
    if volume_name and number:
        return f"{volume_name} #{number}"
    return volume_name or "Untitled"


def _issue_to_result(item):
    """Convert a raw Comic Vine issue dict (from /search/ or /issues/) into
    the standard provider search-result format.

    `media_id` is stored with an "i" prefix (e.g. "i12345") to distinguish
    issue-tracked comics from the legacy volume-tracked ones, which use a
    bare numeric id -- see `comic()`'s docstring for why that distinction
    matters.
    """
    volume = item.get("volume") or {}
    cover_date = item.get("cover_date") or ""
    return {
        "media_id": f"i{item['id']}",
        "source": Sources.COMICVINE.value,
        "media_type": MediaTypes.COMIC.value,
        "title": _issue_title(item, volume.get("name")),
        "image": get_image(item),
        "year": cover_date[:4] if cover_date else None,
        "subtitle": volume.get("name") or None,
    }


def search(query, page):
    """Search for individual comic issues on Comic Vine.

    Searches the `issue` resource (not `volume` -- see the conversation
    notes on why a volume-level search doesn't fit how BD/single-album
    comics are tracked here). Each result is one issue, trackable on its
    own; its parent volume shows up as `subtitle` for context and, once
    tracked, as the auto-detected `comicvine_volume` collection on its
    detail page (see `_build_volume_collection`).
    """
    cache_key = (
        f"search_{Sources.COMICVINE.value}_{MediaTypes.COMIC.value}_{query}_{page}"
    )
    data = cache.get(cache_key)

    if data is None:
        params = {
            "api_key": settings.COMICVINE_API,
            "format": "json",
            "query": query,
            "resources": "issue",
            "field_list": "id,name,issue_number,image,cover_date,volume",
            "limit": settings.PER_PAGE,
            "page": page,
        }

        try:
            response = services.api_request(
                Sources.COMICVINE.value,
                "GET",
                f"{base_url}/search/",
                params=params,
                headers=headers,
            )
        except requests.exceptions.HTTPError as error:
            handle_error(error)

        results = [_issue_to_result(item) for item in response["results"]]

        total_results = response["number_of_total_results"]
        data = helpers.format_search_response(
            page,
            settings.PER_PAGE,
            total_results,
            results,
        )

        cache.set(cache_key, data)

    return data


def comic(media_id):
    """Return the metadata for the selected comic from Comic Vine.

    `media_id` is one of two shapes, dispatched accordingly:
      - "i<id>" -- a single issue. This is what `search()` returns now,
        so every comic tracked via Comic Vine going forward is one of
        these.
      - a bare numeric id -- a whole volume. This was the *only* shape
        before `search()` switched to issue-level results, so it's kept
        working here for any comic tracked under the old behaviour --
        otherwise every existing volume-tracked entry would break (same
        media_id, reinterpreted as an issue id, fetching the wrong thing
        or 404ing).
    """
    if media_id.startswith("i"):
        return _issue_comic(media_id[1:])
    return _volume_comic(media_id)


def _issue_comic(issue_id):
    """Return full metadata for a single Comic Vine issue.

    Embeds `comicvine_volume`: the parent volume's full issue list, in
    the same shape as `bnf_series`/`tmdb_collection`/etc., so the generic
    collection auto-detect/lazy-sync in app/views.py picks it up (see
    `_build_volume_collection`). Mirrors how BnF embeds `bnf_series`.
    """
    cache_key = f"{Sources.COMICVINE.value}_{MediaTypes.COMIC.value}_i{issue_id}"
    data = cache.get(cache_key)

    if data is None:
        params = {
            "api_key": settings.COMICVINE_API,
            "format": "json",
            "field_list": (
                "id,name,issue_number,volume,site_detail_url,image,"
                "description,cover_date,store_date,person_credits"
            ),
        }

        try:
            response = services.api_request(
                Sources.COMICVINE.value,
                "GET",
                f"{base_url}/issue/4000-{issue_id}/",
                params=params,
                headers=headers,
            )
        except requests.exceptions.HTTPError as error:
            handle_error(error)

        response = response.get("results", {})

        if not response:
            services.raise_not_found_error(
                Sources.COMICVINE.value,
                f"i{issue_id}",
                "comic",
            )

        volume = response.get("volume") or {}
        volume_id = volume.get("id")
        cover_date = response.get("cover_date") or ""

        data = {
            "media_id": f"i{issue_id}",
            "source": Sources.COMICVINE.value,
            "source_url": response.get("site_detail_url"),
            "media_type": MediaTypes.COMIC.value,
            "title": _issue_title(response, volume.get("name")),
            "max_progress": None,
            "max_issue_number": None,
            "image": get_image(response),
            "synopsis": get_synopsis(response),
            "genres": None,
            "score": None,
            "score_count": None,
            "details": {
                "start_date": cover_date[:10] if cover_date else None,
                "series": volume.get("name") or None,
                "series_position": response.get("issue_number"),
            },
            "creators": get_issue_creators(response),
            "related": {"recommendations": []},
            # No ongoing-series "next issue" concept for a standalone
            # issue -- unlike the legacy volume path, see _volume_comic.
            "last_issue_id": None,
            "comicvine_volume": (
                _build_volume_collection(volume_id, volume.get("name"))
                if volume_id
                else None
            ),
        }

        cache.set(cache_key, data)

    return data


def _build_volume_collection(volume_id, volume_name=None):
    """Build the `comicvine_volume` collection dict for a volume's full
    issue list.

    Same shape as `bnf_series`/`tmdb_collection`/`igdb_collection`/
    `hardcover_series`: {id, name, image, parts}. Consumed by
    app/views.py's generic collection auto-detect and by
    collections_providers.sync_comicvine_volume().
    """
    issues = get_volume_issues(volume_id)
    if not issues:
        return None

    parts = [
        {
            "source": Sources.COMICVINE.value,
            "media_id": f"i{cv_issue['id']}",
            "media_type": MediaTypes.COMIC.value,
            "title": _issue_title(cv_issue, volume_name),
            "image": get_image(cv_issue),
        }
        for cv_issue in issues
    ]

    return {
        "id": str(volume_id),
        "name": volume_name or "",
        "image": next((p["image"] for p in parts if p["image"]), ""),
        "parts": parts,
    }


# ---------------------------------------------------------------------------
# Legacy volume-level path -- kept only for comics tracked before `search()`
# switched to issue-level results. Not reachable from search() anymore.
# ---------------------------------------------------------------------------
def _volume_comic(media_id):
    """Return the metadata for the selected comic volume from Comic Vine."""
    cache_key = f"{Sources.COMICVINE.value}_{MediaTypes.COMIC.value}_{media_id}"
    data = cache.get(cache_key)

    if data is None:
        params = {
            "api_key": settings.COMICVINE_API,
            "format": "json",
            "field_list": (
                "publisher,site_detail_url,name,last_issue,image,description,"
                "concepts,start_year,count_of_issues,people,date_last_updated"
            ),
        }

        try:
            response = services.api_request(
                Sources.COMICVINE.value,
                "GET",
                f"{base_url}/volume/4050-{media_id}/",
                params=params,
                headers=headers,
            )
        except requests.exceptions.HTTPError as error:
            handle_error(error)

        response = response.get("results", {})

        # Check if response is empty (no results found)
        if not response:
            services.raise_not_found_error(
                Sources.COMICVINE.value,
                media_id,
                "comic",
            )

        publisher_id = response.get("publisher", {}).get("id")
        publisher_comics = []
        if publisher_id:
            publisher_comics = get_publisher_comics(publisher_id, media_id)

        data = {
            "media_id": media_id,
            "source": Sources.COMICVINE.value,
            "source_url": response["site_detail_url"],
            "media_type": MediaTypes.COMIC.value,
            "title": response["name"],
            "max_progress": None,
            "max_issue_number": get_issue_number(
                response["last_issue"]["issue_number"],
            ),
            "image": get_image(response),
            "synopsis": get_synopsis(response),
            "genres": get_genres(response),
            "score": None,
            "score_count": None,
            "details": {
                "start_date": get_start_year(response),
                "publisher": get_publisher_name(response),
                "issues_count": get_issues_count(response),
                "last_issue_name": get_last_issue_name(response),
                "last_issue_number": get_last_issue_number(response),
                "people": get_people(response),
                "last_updated": response.get("date_last_updated").split()[0],
            },
            "creators": get_creators(response),
            "related": {
                "recommendations": publisher_comics,
            },
            # used for events fetching
            "last_issue_id": response["last_issue"]["id"],
        }

        cache.set(cache_key, data)

    return data


def get_image(response):
    """Return the image URL."""
    if "image" in response:
        return response["image"]["medium_url"]
    return settings.IMG_NONE


def get_synopsis(response):
    """Return the synopsis."""
    if not response.get("description"):
        return "No synopsis available"

    soup = BeautifulSoup(response["description"], "html.parser")
    text = soup.get_text(separator=" ")
    return " ".join(text.split())


def get_genres(response):
    """Return the list of genres."""
    if "concepts" in response:
        return [concept["name"] for concept in response["concepts"][:5]]
    return None


def get_start_year(response):
    """Return the start year of the comic volume."""
    return response.get("start_year")


def get_publisher_name(response):
    """Return the publisher name of the comic volume."""
    publisher = response.get("publisher")
    if publisher and isinstance(publisher, dict):
        return publisher.get("name")
    return None


def get_issues_count(response):
    """Return the count of issues in the comic volume."""
    return response.get("count_of_issues")


def get_last_issue_name(response):
    """Return the name of the last issue in the comic volume."""
    last_issue = response.get("last_issue")
    if last_issue and isinstance(last_issue, dict):
        return last_issue.get("name")
    return None


def get_issue_number(issue_number):
    """Return the last issue number as an integer if possible.

    For compound issue numbers (like "463-464"), returns the highest number.
    Returns None if no valid issue number can be extracted.
    """
    try:
        return int(issue_number)

    except ValueError:
        # Handle compound issue numbers like "463-464"
        try:
            # Split by hyphen and get the highest number
            parts = [int(part.strip()) for part in issue_number.split("-")]
            return max(parts)

        except (ValueError, AttributeError):
            return None


def get_last_issue_number(response):
    """Return the last issue number."""
    last_issue = response.get("last_issue")
    if last_issue and isinstance(last_issue, dict):
        return last_issue.get("issue_number")
    return None


def get_people(response):
    """Return the people associated with the comic volume as display strings."""
    people = response.get("people", [])
    return [person["name"] for person in people[:5] if isinstance(person, dict)]


def get_creators(response):
    """Return structured writer/author info with id and name, for a volume.

    Reads the `people` field -- Comic Vine's Volume resource. For a
    single issue, see `get_issue_creators()`, which reads `person_credits`
    instead (the Issue resource uses a different field name).
    """
    people = response.get("people", [])
    return _filter_writer_credits(people)


def get_issue_creators(response):
    """Return structured writer/author info with id and name, for an issue.

    Reads `person_credits` -- Comic Vine's Issue resource uses this field
    name instead of `people` (which Volume uses; see `get_creators()`).
    """
    people = response.get("person_credits", [])
    return _filter_writer_credits(people)


def _filter_writer_credits(people):
    """Shared filter: keep only writer-role credits, in the app's creator shape."""
    creators = []
    writer_roles = {"writer", "plotter", "scripter", "story"}
    for person in people:
        if not isinstance(person, dict):
            continue
        roles = [r.strip().lower() for r in (person.get("role") or "").split(",")]
        if any(r in writer_roles for r in roles):
            creators.append({
                "id": str(person.get("id", "")),
                "name": person.get("name", ""),
                "image": None,  # ComicVine person images need a separate API call
            })
    return creators


def get_publisher_comics(publisher_id, current_id, limit=15):
    """Get comics from the same publisher."""
    cache_key = f"{Sources.COMICVINE.value}_publisher_{publisher_id}_{current_id}"
    data = cache.get(cache_key)

    if data is None:
        params = {
            "api_key": settings.COMICVINE_API,
            "format": "json",
            "field_list": "id,name,image,start_year,publisher",
            "filter": f"publisher:{publisher_id}",
            "limit": limit + 1,  # Get one extra to account for current comic
        }

        try:
            response = services.api_request(
                Sources.COMICVINE.value,
                "GET",
                f"{base_url}/volumes/",
                params=params,
                headers=headers,
            )
        except requests.exceptions.HTTPError as error:
            handle_error(error)

        # Filter out the current comic and format the response
        data = [
            {
                "media_id": str(item["id"]),
                "source": Sources.COMICVINE.value,
                "media_type": MediaTypes.COMIC.value,
                "title": item["name"],
                "image": get_image(item),
            }
            for item in response["results"]
            if str(item["id"]) != current_id
        ][:limit]

        cache.set(cache_key, data)

    return data


def issue(media_id):
    """Return the metadata for the selected comic issue from Comic Vine.

    Internal helper used for new-release event checks on legacy
    volume-tracked comics (see `_volume_comic`'s `last_issue_id`) --
    unrelated to the issue-level tracking added in `_issue_comic`, which
    fetches full issue metadata itself rather than just dates.
    """
    cache_key = f"{Sources.COMICVINE.value}_issue_{media_id}"
    data = cache.get(cache_key)

    if data is None:
        params = {
            "api_key": settings.COMICVINE_API,
            "format": "json",
            "field_list": ("cover_date,store_date"),
        }

        try:
            response = services.api_request(
                Sources.COMICVINE.value,
                "GET",
                f"{base_url}/issue/4000-{media_id}/",
                params=params,
                headers=headers,
            )
        except requests.exceptions.HTTPError as error:
            handle_error(error)

        response = response.get("results", {})

        data = {
            "cover_date": response.get("cover_date"),
            "store_date": response.get("store_date"),
        }

        cache.set(cache_key, data)

    return data


def get_issue_by_number(volume_id, issue_number):
    """Return the single issue matching `issue_number` within `volume_id`.

    Uses Comic Vine's combined volume+issue_number filter, so this is one
    API call regardless of how many issues the volume has -- no need to
    page through the whole series like `get_volume_issues()` below.

    Returns None if no matching issue is found.
    """
    cache_key = (
        f"{Sources.COMICVINE.value}_issue_by_number_{volume_id}_{issue_number}"
    )
    data = cache.get(cache_key)

    if data is None:
        params = {
            "api_key": settings.COMICVINE_API,
            "format": "json",
            "filter": f"volume:{volume_id},issue_number:{issue_number}",
            "field_list": "id,name,issue_number,image,cover_date,store_date",
        }

        try:
            response = services.api_request(
                Sources.COMICVINE.value,
                "GET",
                f"{base_url}/issues/",
                params=params,
                headers=headers,
            )
        except requests.exceptions.HTTPError as error:
            handle_error(error)

        results = response.get("results") or []
        # Cache "{}" (not None) for a confirmed no-match so a repeat
        # lookup for the same volume+number doesn't re-hit the API.
        data = results[0] if results else {}

        cache.set(cache_key, data)

    return data or None


def get_volume_issues(volume_id):
    """Return every issue in a Comic Vine volume, sorted by issue number.

    Mainly a verification/debugging helper, e.g. to eyeball whether a
    volume's numbering lines up with another source's. To look up one
    specific issue, use `get_issue_by_number()` instead -- one API call
    versus paginating the whole series here.

    Comic Vine caps each response at 100 results and ignores `&page=`
    for filtered /issues/ calls -- only `&offset=` advances the page --
    so this loops until a response comes back short of the limit.

    Comic Vine also sorts `issue_number` as a *string*, not a number
    (so "8" sorts after "72") -- harmless for pagination since every
    issue still gets returned exactly once across pages regardless of
    order, but it means the API's own `sort=` param is useless for
    actually presenting these in reading order, so results are re-sorted
    numerically here before returning.
    """
    cache_key = f"{Sources.COMICVINE.value}_volume_issues_{volume_id}"
    data = cache.get(cache_key)

    if data is None:
        data = []
        offset = 0
        limit = 100
        while True:
            params = {
                "api_key": settings.COMICVINE_API,
                "format": "json",
                "filter": f"volume:{volume_id}",
                "field_list": "id,name,issue_number,image,cover_date,store_date",
                "limit": limit,
                "offset": offset,
            }

            try:
                response = services.api_request(
                    Sources.COMICVINE.value,
                    "GET",
                    f"{base_url}/issues/",
                    params=params,
                    headers=headers,
                )
            except requests.exceptions.HTTPError as error:
                handle_error(error)

            page_results = response.get("results") or []
            data.extend(page_results)

            if len(page_results) < limit:
                break
            offset += limit

        data.sort(
            key=lambda i: get_issue_number(i.get("issue_number")) or 0,
        )
        cache.set(cache_key, data)

    return data


def search_issues(query, *, volume_id=None, limit=10):
    """Search Comic Vine issues by name.

    Comic Vine's general /search/ endpoint supports `resources=issue`,
    matching against each issue's `name` field. Unlike
    `get_issue_by_number`, this needs no known volume_id/issue_number --
    useful for two cases:
      - matching a BnF album that has no `series_position` (so
        `get_issue_by_number` has nothing to filter on) by title instead
      - discovering which volume_id is the right one for a *new* series:
        search one distinctive album title and read off `volume.id` from
        the result, instead of hand-browsing comicvine.gamespot.com

    Results aren't scoped to one volume unless `volume_id` is given, in
    which case non-matching volumes are filtered out client-side (the
    search endpoint itself has no volume filter param).

    Caveat: many issues -- especially single-issue American comics --
    have no populated `name` at all, so this only works where the
    content actually has per-issue titles, which BD albums reliably do.
    """
    cache_key = f"{Sources.COMICVINE.value}_search_issue_{volume_id}_{query}"
    data = cache.get(cache_key)

    if data is None:
        params = {
            "api_key": settings.COMICVINE_API,
            "format": "json",
            "query": query,
            "resources": "issue",
            "field_list": "id,name,issue_number,image,cover_date,volume",
            "limit": limit,
        }

        try:
            response = services.api_request(
                Sources.COMICVINE.value,
                "GET",
                f"{base_url}/search/",
                params=params,
                headers=headers,
            )
        except requests.exceptions.HTTPError as error:
            handle_error(error)

        results = response.get("results") or []
        if volume_id:
            results = [
                r
                for r in results
                if str((r.get("volume") or {}).get("id")) == str(volume_id)
            ]
        data = results

        cache.set(cache_key, data)

    return data
