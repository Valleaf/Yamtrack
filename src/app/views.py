import logging
from pathlib import Path
from urllib.parse import urlencode

from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import prefetch_related_objects
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.text import slugify
from django.utils.timezone import datetime
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from app import config, helpers, history_processor
from app import statistics as stats
from app.date_utils import get_release_year_from_metadata
from app.forms import EpisodeForm, ManualItemForm, get_form_class
from app.models import (
    TV,
    BasicMedia,
    Item,
    MediaTypes,
    Season,
    Sources,
    Status,
    UserMessage,
)
from app.providers import manual, services, tmdb
from app.templatetags import app_tags
from users.models import (
    DateFormatChoices,
    HomeSortChoices,
    MediaSortChoices,
    MediaStatusChoices,
)

logger = logging.getLogger(__name__)


@require_GET
def home(request):
    """Home page with media items in progress and planning."""
    sort_by = request.user.update_preference("home_sort", request.GET.get("sort"))
    media_type_to_load = request.GET.get("load_media_type")
    status_to_load = request.GET.get("load_status", Status.IN_PROGRESS.value)
    items_limit = 14

    # If this is an HTMX request to load more items for a specific media type
    if request.headers.get("HX-Request") and media_type_to_load:
        list_by_type = BasicMedia.objects.get_home_status(
            user=request.user,
            status=status_to_load,
            sort_by=sort_by,
            items_limit=items_limit,
            specific_media_type=media_type_to_load,
        )
        context = {
            "media_list": list_by_type.get(media_type_to_load, []),
            "home_status": status_to_load,
        }
        return render(request, "app/components/home_grid.html", context)

    home_sections = []
    for status in (Status.IN_PROGRESS.value, Status.PLANNING.value):
        media_types = BasicMedia.objects.get_home_status(
            user=request.user,
            status=status,
            sort_by=sort_by,
            items_limit=items_limit,
        )
        home_sections.append(
            {
                "key": status,
                "id": slugify(status),
                "media_types": media_types,
                "count": sum(
                    media_list["total"] for media_list in media_types.values()
                ),
            },
        )

    context = {
        "home_sections": home_sections,
        "current_sort": sort_by,
        "sort_choices": HomeSortChoices.choices,
        "items_limit": items_limit,
    }
    return render(request, "app/home.html", context)


@require_POST
def progress_edit(request, media_type, instance_id):
    """Increase or decrease the progress of a media item from home page."""
    operation = request.POST["operation"]

    media = BasicMedia.objects.get_media_prefetch(
        request.user,
        media_type,
        instance_id,
    )

    if operation == "increase":
        media.increase_progress()
    elif operation == "decrease":
        media.decrease_progress()

    if media_type == MediaTypes.SEASON.value:
        # clear prefetch cache to get the updated episodes
        media.refresh_from_db()
        prefetch_related_objects([media], "episodes")

    context = {
        "media": media,
    }
    return render(
        request,
        "app/components/progress_changer.html",
        context,
    )


@require_GET
def media_list(request, media_type):
    """Return the media list page."""
    layout = request.user.update_preference(
        f"{media_type}_layout",
        request.GET.get("layout"),
    )
    sort_filter = request.user.update_preference(
        f"{media_type}_sort",
        request.GET.get("sort"),
    )
    status_filter = request.user.update_preference(
        f"{media_type}_status",
        request.GET.get("status"),
    )
    search_query = request.GET.get("search", "")
    page = request.GET.get("page", 1)

    # Prepare status filter for database query
    if not status_filter:
        status_filter = MediaStatusChoices.ALL

    # Get media list with filters applied
    media_queryset = BasicMedia.objects.get_media_list(
        user=request.user,
        media_type=media_type,
        status_filter=status_filter,
        sort_filter=sort_filter,
        search=search_query,
    )

    # Paginate results
    items_per_page = 32
    paginator = Paginator(media_queryset, items_per_page)
    media_page = paginator.get_page(page)

    BasicMedia.objects.annotate_max_progress(
        media_page.object_list,
        media_type,
    )

    context = {
        "media_type": media_type,
        "media_type_plural": app_tags.media_type_readable_plural(media_type).lower(),
        "media_list": media_page,
        "current_layout": layout,
        "layout_class": ".media-grid" if layout == "grid" else "tbody",
        "current_sort": sort_filter,
        "current_status": status_filter,
        "sort_choices": MediaSortChoices.choices,
        "status_choices": MediaStatusChoices.choices,
    }

    # Handle HTMX requests for partial updates
    if request.headers.get("HX-Request"):
        # Filtering from empty list
        if request.headers.get("HX-Target") == "empty_list":
            # If still empty, keep user in the same page
            if not media_page.object_list:
                return HttpResponse(status=204)
            response = HttpResponse()
            response["HX-Redirect"] = reverse("medialist", args=[media_type])
            return response
        if layout == "grid":
            template_name = "app/components/media_grid_items.html"
        else:
            template_name = "app/components/media_table_items.html"
    else:
        template_name = "app/media_list.html"

    return render(request, template_name, context)


MUSIC_TYPE_TABS = [
    ("", "All"),
    ("album", "Albums"),
    ("ep", "EPs"),
    ("single", "Singles"),
    ("artist", "Artists"),
]


@require_GET
def media_search(request):
    """Return the media search page."""
    media_type = request.user.update_preference(
        "last_search_type",
        request.GET["media_type"],
    )
    query = request.GET["q"]
    page = int(request.GET.get("page", 1))
    layout = request.GET.get("layout", "grid")

    # For music, mb_type is the type filter (album/ep/single/artist)
    mb_type = request.GET.get("mb_type", "")

    source = request.GET.get("source") or config.get_default_source_name(media_type).value
    search_source = mb_type if media_type == MediaTypes.MUSIC.value else source
    data = services.search(media_type, query, page, search_source)

    # Enrich search results with user tracking data
    # Skip enrichment for artist results (not trackable items)
    if data.get("results"):
        artists = [r for r in data["results"] if r.get("media_type") == "music_artist"]
        non_artists = [r for r in data["results"] if r.get("media_type") != "music_artist"]

        enriched = []
        if non_artists:
            enriched = helpers.enrich_items_with_user_data(request, non_artists, "search")

        # Wrap artist dicts so template can use result.media and result.is_artist
        artist_entries = [{"media": r, "item": None, "is_artist": True} for r in artists]

        # Preserve original order
        enriched_iter = iter(enriched)
        artist_iter = iter(artist_entries)
        merged = []
        for r in data["results"]:
            if r.get("media_type") == "music_artist":
                merged.append(next(artist_iter))
            else:
                merged.append(next(enriched_iter))
        data["results"] = merged

    context = {
        "data": data,
        "source": source,
        "media_type": media_type,
        "layout": layout,
        "music_type_tabs": MUSIC_TYPE_TABS,
    }

    return render(request, "app/search.html", context)


def get_country_display(metadata):
    """Resolve a media metadata dict's country to a human-readable name.

    Skips resolution if the provider already supplies a readable name in
    metadata["details"]["country"] (e.g. TMDB), since that's rendered
    directly by the generic details loop in the template.
    """
    if metadata.get("details", {}).get("country"):
        return None
    country_code = metadata.get("country")
    if not country_code:
        return None
    return stats._ISO_TO_NAME.get(country_code, country_code)


@require_GET
def media_details(request, source, media_type, media_id, title):  # noqa: ARG001 title for URL
    """Return the details page for a media item."""
    media_metadata = services.get_media_metadata(media_type, media_id, source)
    user_medias = BasicMedia.objects.filter_media_prefetch(
        request.user,
        media_id,
        media_type,
        source,
    )
    current_instance = user_medias[0] if user_medias else None

    # Enrich related items with user tracking data
    if media_metadata.get("related"):
        for section_name, related_items in media_metadata["related"].items():
            if related_items:
                media_metadata["related"][section_name] = (
                    helpers.enrich_items_with_user_data(
                        request, related_items, section_name
                    )
                )

    if media_type in ["tv", "movie"]:
        watch_providers = tmdb.filter_providers(
            media_metadata.get("providers"), request.user.watch_provider_region
        )
    else:
        watch_providers = None

    # Collections this item belongs to
    from media_collections.models import Collection
    this_item = Item.objects.filter(
        source=source,
        media_type=media_type,
        media_id=media_id,
    ).first()
    item_collections = []
    if this_item:
        item_collections = list(
            Collection.objects.filter(
                collectionitem__item=this_item,
                owner=request.user,
            ).distinct()
        )

    # Find the Collection record for the collection/series this media belongs to
    tmdb_collection_obj = None
    collection_banner = None
    try:
        from app.providers.collections_providers import get_collection_for_media
        source_key_map = {
            (Sources.TMDB.value, MediaTypes.MOVIE.value): "tmdb_collection",
            (Sources.IGDB.value, MediaTypes.GAME.value): "igdb_collection",
            (Sources.HARDCOVER.value, MediaTypes.BOOK.value): "hardcover_series",
            (Sources.BNF.value, MediaTypes.COMIC.value): "bnf_series",
            (Sources.COMICVINE.value, MediaTypes.COMIC.value): "comicvine_volume",
        }
        source_key = source_key_map.get((source, media_type))
        if source_key:
            col_data = media_metadata.get(source_key)
            if col_data and col_data.get("name"):
                collection_banner = col_data["name"]
                tmdb_collection_obj = get_collection_for_media(
                    request.user, media_metadata, source_key
                )
                # Lazy sync: user is tracking but collection wasn't created yet
                if tmdb_collection_obj is None and current_instance is not None:
                    from app.providers.collections_providers import (
                        sync_tmdb_collection,
                        sync_igdb_collection,
                        sync_hardcover_series,
                        sync_bnf_series,
                        sync_comicvine_volume,
                    )
                    sync_map = {
                        "tmdb_collection": sync_tmdb_collection,
                        "igdb_collection": sync_igdb_collection,
                        "hardcover_series": sync_hardcover_series,
                        "bnf_series": sync_bnf_series,
                        "comicvine_volume": sync_comicvine_volume,
                    }
                    sync_fn = sync_map.get(source_key)
                    if sync_fn:
                        # If metadata has no collection data, the cache is stale — bust it
                        if not col_data or not col_data.get("id"):
                            cache_key = f"{source}_{media_type}_{media_id}"
                            cache.delete(cache_key)
                            media_metadata = services.get_media_metadata(
                                media_type, media_id, source
                            )
                            col_data = media_metadata.get(source_key)
                            collection_banner = (col_data or {}).get("name")
                        tmdb_collection_obj = sync_fn(request.user, media_metadata)
    except Exception:
        logger.exception("Failed to look up collection for %s/%s", source, media_id)

    context = {
        "media": media_metadata,
        "media_type": media_type,
        "media_source": source,
        "media_id": media_id,
        "user_medias": user_medias,
        "current_instance": current_instance,
        "watch_providers": watch_providers,
        "watch_provider_region": request.user.watch_provider_region,
        "item_collections": item_collections,
        "tmdb_collection_obj": tmdb_collection_obj,
        "collection_banner": collection_banner,
        "country_display": get_country_display(media_metadata),
    }
    return render(request, "app/media_details.html", context)


def _get_user_movie_directors(user):
    """Return tracked directors for the user's movie collection.

    Reads cached metadata first; any movie missing from the cache is
    fetched live (and cached) the same way the generic person-grouping
    helper does for games/music/comics/books, so this page never silently
    drops movies just because their detail page hasn't been visited yet.
    """
    from concurrent.futures import ThreadPoolExecutor  # noqa: PLC0415

    movies = BasicMedia.objects.get_media_list(
        user=user,
        media_type=MediaTypes.MOVIE.value,
        status_filter=MediaStatusChoices.ALL,
        sort_filter="title",
    )

    tmdb_movies = [m for m in movies if m.item.source == Sources.TMDB.value]
    total_movies = len(tmdb_movies)

    cached_metadata = {}
    uncached = []
    for movie in tmdb_movies:
        cache_key = f"{Sources.TMDB.value}_{MediaTypes.MOVIE.value}_{movie.item.media_id}"
        metadata = cache.get(cache_key)
        if metadata is not None:
            cached_metadata[movie.item.media_id] = metadata
        else:
            uncached.append(movie)

    if uncached:
        def _fetch(movie):
            try:
                return movie.item.media_id, services.get_media_metadata(
                    MediaTypes.MOVIE.value, movie.item.media_id, Sources.TMDB.value,
                )
            except Exception:
                logger.exception(
                    "Failed to fetch metadata for movie %s", movie.item.media_id,
                )
                return movie.item.media_id, None

        with ThreadPoolExecutor(max_workers=8) as executor:
            for media_id, metadata in executor.map(_fetch, uncached):
                if metadata is not None:
                    cached_metadata[media_id] = metadata

    directors = {}
    cached_movie_count = 0
    for movie in tmdb_movies:
        metadata = cached_metadata.get(movie.item.media_id)
        if metadata is None:
            continue

        cached_movie_count += 1
        for director in metadata.get("directors", []):
            director_id = director["id"]
            director_record = directors.setdefault(
                director_id,
                {
                    "id": director_id,
                    "name": director["name"],
                    "image": director.get("image"),
                    "movies": [],
                },
            )
            director_record["movies"].append(
                {
                    "metadata": metadata,
                    "item": movie.item,
                    "status": movie.status,
                },
            )

    return directors, total_movies, cached_movie_count


@require_GET
def movie_directors(request):
    """Return the director subtab for tracked movies."""
    directors, total_movies, cached_movie_count = _get_user_movie_directors(request.user)

    director_list = []
    for director in directors.values():
        movie_count = len(director["movies"])
        percentage = round(movie_count / total_movies * 100, 1) if total_movies else 0

        director_list.append(
            {
                "id": director["id"],
                "name": director["name"],
                "image": director.get("image"),
                "movie_count": movie_count,
                "percentage": percentage,
                "filmography_count": None,  # loaded lazily on detail page
            }
        )

    director_list.sort(key=lambda entry: (-entry["movie_count"], entry["name"]))

    return render(
        request,
        "app/movie_directors.html",
        {
            "directors": director_list,
            "total_movies": total_movies,
            "cached_movie_count": cached_movie_count,
        },
    )


@require_GET
def movie_director(request, director_id, name):
    """Return the director detail page for a tracked movie director."""
    directors, total_movies, cached_movie_count = _get_user_movie_directors(request.user)
    director = directors.get(director_id)
    if not director:
        raise Http404("Director not found")

    movie_count = len(director["movies"])
    percentage = round(movie_count / total_movies * 100, 1) if total_movies else 0

    tracked_movies = {
        str(movie["metadata"]["media_id"]): movie
        for movie in director["movies"]
    }

    return render(
        request,
        "app/movie_director.html",
        {
            "director": {
                "id": director_id,
                "name": director["name"],
                "image": director.get("image"),
                "movie_count": movie_count,
                "percentage": percentage,
            },
            "tracked_movies": tracked_movies,
            "total_movies": total_movies,
            "cached_movie_count": cached_movie_count,
        },
    )


@require_GET
def movie_director_filmography(request, director_id):
    """HTMX endpoint: load a director's full filmography from TMDB."""
    directors, total_movies, _ = _get_user_movie_directors(request.user)
    director = directors.get(director_id)

    tracked_movies = {}
    if director:
        tracked_movies = {
            str(movie["metadata"]["media_id"]): movie
            for movie in director["movies"]
        }

    try:
        filmography = tmdb.person_credits(director_id) or []
    except Exception:
        logger.exception("Failed to fetch filmography for director %s", director_id)
        filmography = []

    movies = []
    for film in filmography:
        media_id = str(film["media_id"])
        tracked_movie = tracked_movies.get(media_id)
        if tracked_movie:
            link = reverse(
                "media_details",
                kwargs={
                    "source": tracked_movie["item"].source,
                    "media_type": MediaTypes.MOVIE.value,
                    "media_id": media_id,
                    "title": slugify(film["title"]),
                },
            )
        else:
            link = film["source_url"]

        movie_status = tracked_movie["status"] if tracked_movie else None
        movies.append(
            {
                "id": media_id,
                "title": film["title"],
                "image": film["image"],
                "release_date": film.get("release_date"),
                "release_year": film.get("release_date", "")[:4] if film.get("release_date") else None,
                "tracked": bool(tracked_movie),
                "status": movie_status,
                "completed": movie_status == Status.COMPLETED.value,
                "dropped": movie_status == Status.DROPPED.value,
                "link": link,
                "external": not bool(tracked_movie),
            }
        )

    # Recalculate percentage now we have the real filmography count
    movie_count = len(tracked_movies)
    filmography_count = len(movies)
    if filmography_count:
        percentage = round(movie_count / filmography_count * 100, 1)
    elif total_movies:
        percentage = round(movie_count / total_movies * 100, 1)
    else:
        percentage = 0

    return render(
        request,
        "app/components/director_filmography.html",
        {
            "movies": movies,
            "filmography_count": filmography_count,
            "percentage": percentage,
            "movie_count": movie_count,
        },
    )


@require_GET
def music_artist(request, artist_id, name):  # noqa: ARG001 name for URL
    """Return the MusicBrainz artist page."""
    from app.providers import musicbrainz
    artist_data = musicbrainz.artist(artist_id)
    return render(request, "app/music_artist.html", {"artist": artist_data})


# ── Generic person/studio grouping ────────────────────────────────────────────

def _get_media_by_person(user, media_type, person_key, source_filter=None, cached_only=False):
    """Generic helper: group a user's tracked media by a person/studio field.

    Returns (persons_dict, total_count, cached_count).
    persons_dict maps person_id -> {id, name, image, media: [...]}
    person_key is the metadata key that holds a list of {id, name, image} dicts.
    If cached_only=True, skips API fetching and only uses Redis-cached metadata.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed  # noqa: PLC0415

    tracked = BasicMedia.objects.get_media_list(
        user=user,
        media_type=media_type,
        status_filter=MediaStatusChoices.ALL,
        sort_filter="title",
    )
    if source_filter:
        tracked = [m for m in tracked if m.item.source == source_filter]
    else:
        tracked = list(tracked)

    total_count = len(tracked)
    cached_metadata = {}
    uncached = []

    for m in tracked:
        cache_key = f"{m.item.source}_{media_type}_{m.item.media_id}"
        metadata = cache.get(cache_key)
        if metadata is not None:
            cached_metadata[m.item.media_id] = metadata
        else:
            uncached.append(m)

    if uncached and not cached_only:
        def _fetch(m):
            try:
                return m.item.media_id, services.get_media_metadata(
                    media_type, m.item.media_id, m.item.source
                )
            except Exception:
                logger.exception("Failed to fetch metadata for %s %s", media_type, m.item.media_id)
                return m.item.media_id, None

        with ThreadPoolExecutor(max_workers=8) as executor:
            for media_id, metadata in executor.map(_fetch, uncached):
                if metadata is not None:
                    cached_metadata[media_id] = metadata

    persons = {}
    cached_count = 0
    for m in tracked:
        metadata = cached_metadata.get(m.item.media_id)
        if metadata is None:
            continue
        cached_count += 1
        for person in metadata.get(person_key) or []:
            pid = str(person.get("id") or person.get("name", ""))
            if not pid:
                continue
            record = persons.setdefault(pid, {
                "id": pid,
                "name": person.get("name", ""),
                "image": person.get("image"),
                "media": [],
            })
            record["media"].append({"metadata": metadata, "item": m.item, "status": m.status})

    return persons, total_count, cached_count


def _build_person_list(persons, total_count):
    """Build a sorted list of person dicts with media_count and percentage."""
    result = []
    for p in persons.values():
        count = len(p["media"])
        result.append({
            "id": p["id"],
            "name": p["name"],
            "image": p.get("image"),
            "media_count": count,
            "percentage": round(count / total_count * 100, 1) if total_count else 0,
        })
    result.sort(key=lambda x: (-x["media_count"], x["name"]))
    return result


# ── Game studios ──────────────────────────────────────────────────────────────

@require_GET
def game_studios(request):
    """List view: tracked games grouped by developer studio."""
    persons, total_count, cached_count = _get_media_by_person(
        request.user, MediaTypes.GAME.value, "developers", Sources.IGDB.value
    )
    studio_list = _build_person_list(persons, total_count)
    return render(request, "app/persons_list.html", {
        "persons": studio_list,
        "total_count": total_count,
        "cached_count": cached_count,
        "media_type": MediaTypes.GAME.value,
        "person_type": "studio",
        "person_type_plural": "Studios",
        "list_url_name": "game_studios",
        "detail_url_name": "game_studio",
        "medialist_url_name": "medialist",
        "page_title": "Game Studios",
    })


@require_GET
def game_studio(request, studio_id, name):  # noqa: ARG001
    """Detail view: a specific developer studio and their tracked games."""
    persons, total_count, _ = _get_media_by_person(
        request.user, MediaTypes.GAME.value, "developers", Sources.IGDB.value
    )
    person = persons.get(studio_id)
    if not person:
        raise Http404("Studio not found")

    media_count = len(person["media"])
    percentage = round(media_count / total_count * 100, 1) if total_count else 0

    tracked_items = [
        {
            "id": m["metadata"]["media_id"],
            "title": m["metadata"]["title"],
            "image": m["metadata"].get("image"),
            "release_year": (m["metadata"].get("details", {}).get("release_date") or "")[:4],
            "tracked": True,
            "status": m["status"],
            "completed": m["status"] == Status.COMPLETED.value,
            "link": reverse("media_details", kwargs={
                "source": m["item"].source,
                "media_type": MediaTypes.GAME.value,
                "media_id": m["metadata"]["media_id"],
                "title": slugify(m["metadata"]["title"]),
            }),
            "external": False,
        }
        for m in person["media"]
    ]
    tracked_items.sort(key=lambda x: x["title"])

    return render(request, "app/person_detail.html", {
        "person": {
            "id": studio_id,
            "name": person["name"],
            "image": person.get("image"),
            "media_count": media_count,
            "percentage": percentage,
        },
        "media_items": tracked_items,
        "media_type": MediaTypes.GAME.value,
        "person_type": "studio",
        "person_type_plural": "Studios",
        "list_url_name": "game_studios",
        "medialist_url_name": "medialist",
        "page_title": f"{person['name']} — Studio",
        "total_count": total_count,
    })


# ── Music artists ─────────────────────────────────────────────────────────────

@require_GET
def movie_director_bio(request, director_id):
    """HTMX endpoint: load a director's bio and external links from TMDB."""
    try:
        bio = tmdb.person_details(director_id)
    except Exception:
        logger.exception("Failed to fetch bio for director %s", director_id)
        bio = None
    return render(request, "app/components/person_bio.html", {"bio": bio})


@require_GET
def music_artist_bio(request, artist_id):
    """HTMX endpoint: fetch Wikipedia extract for a MusicBrainz artist."""
    import requests as _requests  # noqa: PLC0415
    from app.providers import musicbrainz  # noqa: PLC0415

    bio_html = ""
    bio_url = ""
    try:
        artist_data = musicbrainz.artist(artist_id)
        bio_url = artist_data.get("bio_url", "")
        if bio_url and "wikipedia.org/wiki/" in bio_url:
            title = bio_url.split("/wiki/")[-1]
            resp = _requests.get(
                f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}",
                headers={"User-Agent": "Yamtrack/1.0"},
                timeout=5,
            )
            if resp.ok:
                bio_html = resp.json().get("extract", "")
    except Exception:
        logger.exception("Failed to fetch Wikipedia bio for artist %s", artist_id)

    return render(request, "app/components/person_bio.html", {
        "bio": {"biography": bio_html, "tmdb_url": "", "imdb_id": ""},
        "source_url": bio_url,
        "source_label": "Wikipedia",
    })


@require_GET
def music_artists(request):
    """List view: tracked music grouped by artist."""
    persons, total_count, cached_count = _get_media_by_person(
        request.user, MediaTypes.MUSIC.value, "artist_links", Sources.MUSICBRAINZ.value
    )
    artist_list = _build_person_list(persons, total_count)
    return render(request, "app/persons_list.html", {
        "persons": artist_list,
        "total_count": total_count,
        "cached_count": cached_count,
        "media_type": MediaTypes.MUSIC.value,
        "person_type": "artist",
        "person_type_plural": "Artists",
        "list_url_name": "music_artists",
        "detail_url_name": "music_artist",
        "medialist_url_name": "medialist",
        "page_title": "Music Artists",
    })


# ── Comic creators ────────────────────────────────────────────────────────────

@require_GET
def comic_people(request):
    """List view: tracked comics grouped by writer/creator."""
    persons, total_count, cached_count = _get_media_by_person(
        request.user, MediaTypes.COMIC.value, "creators", Sources.COMICVINE.value
    )
    people_list = _build_person_list(persons, total_count)
    return render(request, "app/persons_list.html", {
        "persons": people_list,
        "total_count": total_count,
        "cached_count": cached_count,
        "media_type": MediaTypes.COMIC.value,
        "person_type": "creator",
        "person_type_plural": "Creators",
        "list_url_name": "comic_people",
        "detail_url_name": "comic_person",
        "medialist_url_name": "medialist",
        "page_title": "Comic Creators",
    })


@require_GET
def comic_person(request, person_id, name):  # noqa: ARG001
    """Detail view: a specific comic writer/creator."""
    persons, total_count, _ = _get_media_by_person(
        request.user, MediaTypes.COMIC.value, "creators", Sources.COMICVINE.value
    )
    person = persons.get(person_id)
    if not person:
        raise Http404("Creator not found")

    media_count = len(person["media"])
    percentage = round(media_count / total_count * 100, 1) if total_count else 0

    tracked_items = [
        {
            "id": m["metadata"]["media_id"],
            "title": m["metadata"]["title"],
            "image": m["metadata"].get("image"),
            "release_year": str(get_release_year_from_metadata(m["metadata"]) or ""),
            "tracked": True,
            "status": m["status"],
            "completed": m["status"] == Status.COMPLETED.value,
            "link": reverse("media_details", kwargs={
                "source": m["item"].source,
                "media_type": MediaTypes.COMIC.value,
                "media_id": m["metadata"]["media_id"],
                "title": slugify(m["metadata"]["title"]),
            }),
            "external": False,
        }
        for m in person["media"]
    ]
    tracked_items.sort(key=lambda x: x["title"])

    return render(request, "app/person_detail.html", {
        "person": {
            "id": person_id,
            "name": person["name"],
            "image": person.get("image"),
            "media_count": media_count,
            "percentage": percentage,
        },
        "media_items": tracked_items,
        "media_type": MediaTypes.COMIC.value,
        "person_type": "creator",
        "person_type_plural": "Creators",
        "list_url_name": "comic_people",
        "medialist_url_name": "medialist",
        "page_title": f"{person['name']} — Creator",
        "total_count": total_count,
    })


# ── Manga authors ────────────────────────────────────────────────────────────

@require_GET
def manga_authors(request):
    """List view: tracked manga grouped by author."""
    persons, total_count, cached_count = _get_media_by_person(
        request.user, MediaTypes.MANGA.value, "authors"
    )
    author_list = _build_person_list(persons, total_count)
    return render(request, "app/persons_list.html", {
        "persons": author_list,
        "total_count": total_count,
        "cached_count": cached_count,
        "media_type": MediaTypes.MANGA.value,
        "person_type": "author",
        "person_type_plural": "Authors",
        "list_url_name": "manga_authors",
        "detail_url_name": "manga_author",
        "medialist_url_name": "medialist",
        "page_title": "Manga Authors",
    })


@require_GET
def manga_author(request, author_id, name):
    """Detail view: a specific manga author (fast initial render; items load via HTMX)."""
    # Use only cached metadata so the page renders immediately without MAL API calls.
    persons, total_count, _ = _get_media_by_person(
        request.user, MediaTypes.MANGA.value, "authors", cached_only=True
    )
    person = persons.get(author_id)

    if person:
        person_data = {
            "id": author_id,
            "name": person["name"],
            "image": person.get("image"),
        }
    else:
        # Author not yet in cache — reconstruct name from URL slug as placeholder.
        person_data = {
            "id": author_id,
            "name": name.replace("-", " ").title(),
            "image": None,
        }

    items_url = reverse(
        "manga_author_items",
        kwargs={"author_id": author_id, "name": name},
    )

    return render(request, "app/person_detail.html", {
        "person": person_data,
        "items_htmx_url": items_url,
        "media_type": MediaTypes.MANGA.value,
        "person_type": "author",
        "person_type_plural": "Authors",
        "list_url_name": "manga_authors",
        "medialist_url_name": "medialist",
        "page_title": f"{person_data['name']} — Author",
        "total_count": total_count,
    })


@require_GET
def manga_author_items(request, author_id, name):  # noqa: ARG001
    """HTMX endpoint: load a manga author's tracked items (may call MAL API)."""
    persons, total_count, _ = _get_media_by_person(
        request.user, MediaTypes.MANGA.value, "authors"
    )
    person = persons.get(author_id)
    if not person:
        return render(request, "app/components/person_tracked_items.html", {
            "media_items": [],
            "media_type": MediaTypes.MANGA.value,
            "media_count": 0,
            "percentage": 0,
            "total_count": total_count,
        })

    media_count = len(person["media"])
    tracked_items = [
        {
            "id": m["metadata"]["media_id"],
            "title": m["metadata"]["title"],
            "image": m["metadata"].get("image"),
            "release_year": str(get_release_year_from_metadata(m["metadata"]) or ""),
            "tracked": True,
            "status": m["status"],
            "completed": m["status"] == Status.COMPLETED.value,
            "link": reverse("media_details", kwargs={
                "source": m["item"].source,
                "media_type": MediaTypes.MANGA.value,
                "media_id": m["metadata"]["media_id"],
                "title": slugify(m["metadata"]["title"]),
            }),
            "external": False,
        }
        for m in person["media"]
    ]
    tracked_items.sort(key=lambda x: x["title"])

    return render(request, "app/components/person_tracked_items.html", {
        "media_items": tracked_items,
        "media_type": MediaTypes.MANGA.value,
        "media_count": media_count,
        "percentage": round(media_count / total_count * 100, 1) if total_count else 0,
        "total_count": total_count,
    })


# ── Book authors ───────────────────────────────────────────────────────────

@require_GET
def book_authors(request):
    """List view: tracked books grouped by author."""
    persons, total_count, cached_count = _get_media_by_person(
        request.user, MediaTypes.BOOK.value, "authors"
    )
    author_list = _build_person_list(persons, total_count)
    return render(request, "app/persons_list.html", {
        "persons": author_list,
        "total_count": total_count,
        "cached_count": cached_count,
        "media_type": MediaTypes.BOOK.value,
        "person_type": "author",
        "person_type_plural": "Authors",
        "list_url_name": "book_authors",
        "detail_url_name": "book_author",
        "medialist_url_name": "medialist",
        "page_title": "Book Authors",
    })


@require_GET
def book_author(request, author_id, name):  # noqa: ARG001
    """Detail view: a specific book author."""
    persons, total_count, _ = _get_media_by_person(
        request.user, MediaTypes.BOOK.value, "authors"
    )
    person = persons.get(author_id)
    if not person:
        raise Http404("Author not found")

    media_count = len(person["media"])
    percentage = round(media_count / total_count * 100, 1) if total_count else 0

    tracked_items = [
        {
            "id": m["metadata"]["media_id"],
            "title": m["metadata"]["title"],
            "image": m["metadata"].get("image"),
            "release_year": str(m["metadata"].get("details", {}).get("publish_date") or "")[:4],
            "tracked": True,
            "status": m["status"],
            "completed": m["status"] == Status.COMPLETED.value,
            "link": reverse("media_details", kwargs={
                "source": m["item"].source,
                "media_type": MediaTypes.BOOK.value,
                "media_id": m["metadata"]["media_id"],
                "title": slugify(m["metadata"]["title"]),
            }),
            "external": False,
        }
        for m in person["media"]
    ]
    tracked_items.sort(key=lambda x: x["title"])

    return render(request, "app/person_detail.html", {
        "person": {
            "id": author_id,
            "name": person["name"],
            "image": person.get("image"),
            "media_count": media_count,
            "percentage": percentage,
        },
        "media_items": tracked_items,
        "media_type": MediaTypes.BOOK.value,
        "person_type": "author",
        "person_type_plural": "Authors",
        "list_url_name": "book_authors",
        "medialist_url_name": "medialist",
        "page_title": f"{person['name']} — Author",
        "total_count": total_count,
    })


@require_GET
def season_details(request, source, media_id, title, season_number):  # noqa: ARG001 For URL
    """Return the details page for a season."""
    tv_with_seasons_metadata = services.get_media_metadata(
        "tv_with_seasons",
        media_id,
        source,
        [season_number],
    )
    season_metadata = tv_with_seasons_metadata[f"season/{season_number}"]

    user_medias = BasicMedia.objects.filter_media_prefetch(
        request.user,
        media_id,
        MediaTypes.SEASON.value,
        source,
        season_number=season_number,
    )

    current_instance = user_medias[0] if user_medias else None
    episodes_in_db = current_instance.episodes.all() if current_instance else []

    if source == Sources.MANUAL.value:
        season_metadata["episodes"] = manual.process_episodes(
            season_metadata,
            episodes_in_db,
        )
    else:
        season_metadata["episodes"] = tmdb.process_episodes(
            season_metadata,
            episodes_in_db,
        )

    # Enrich related items with user tracking data
    if season_metadata.get("related"):
        for section_name, related_items in season_metadata["related"].items():
            if related_items:
                season_metadata["related"][section_name] = (
                    helpers.enrich_items_with_user_data(
                        request,
                        related_items,
                        section_name,
                    )
                )

    context = {
        "media": season_metadata,
        "tv": tv_with_seasons_metadata,
        "media_type": MediaTypes.SEASON.value,
        "media_source": source,
        "media_id": media_id,
        "season_number": season_number,
        "user_medias": user_medias,
        "current_instance": current_instance,
        "watch_providers": tmdb.filter_providers(
            season_metadata.get("providers"), request.user.watch_provider_region
        ),
        "watch_provider_region": request.user.watch_provider_region,
        "country_display": get_country_display(season_metadata),
    }
    return render(request, "app/media_details.html", context)


@require_POST
def update_media_score(request, media_type, instance_id):
    """Update the user's score for a media item."""
    media = BasicMedia.objects.get_media(
        request.user,
        media_type,
        instance_id,
    )

    score = float(request.POST.get("score"))
    media.score = score
    media.save()
    logger.info(
        "%s score updated to %s",
        media,
        score,
    )

    return JsonResponse(
        {
            "success": True,
            "score": score,
        },
    )


@require_POST
def sync_metadata(request, source, media_type, media_id, season_number=None):
    """Refresh the metadata for a media item."""
    if source == Sources.MANUAL.value:
        msg = "Manual items cannot be synced."
        messages.error(request, msg)
        return HttpResponse(
            msg,
            status=400,
            headers={"HX-Redirect": request.POST.get("next", "/")},
        )

    cache_key = f"{source}_{media_type}_{media_id}"
    if media_type == MediaTypes.SEASON.value:
        cache_key += f"_{season_number}"

    ttl = cache.ttl(cache_key)
    logger.debug("%s - Cache TTL for: %s", cache_key, ttl)

    if ttl is not None and ttl > (settings.CACHE_TIMEOUT - 3):
        msg = "The data was recently synced, please wait a few seconds."
        messages.error(request, msg)
        logger.error(msg)
    else:
        deleted = cache.delete(cache_key)
        logger.debug("%s - Old cache deleted: %s", cache_key, deleted)

        metadata = services.get_media_metadata(
            media_type,
            media_id,
            source,
            [season_number],
        )
        item, _ = Item.objects.update_or_create(
            media_id=media_id,
            source=source,
            media_type=media_type,
            season_number=season_number,
            defaults={
                "title": metadata["title"],
                "image": metadata["image"],
                "country": metadata.get("country", ""),
            },
        )
        if item.release_year is None:
            release_year = get_release_year_from_metadata(metadata)
            if release_year is not None:
                item.release_year = release_year
                item.save(update_fields=["release_year"])
        title = metadata["title"]
        if season_number:
            title += f" - Season {season_number}"

        if media_type == MediaTypes.SEASON.value:
            metadata["episodes"] = tmdb.process_episodes(
                metadata,
                [],
            )

            # Create a dictionary of existing episodes keyed by episode number
            existing_episodes = {
                ep.episode_number: ep
                for ep in Item.objects.filter(
                    source=source,
                    media_type=MediaTypes.EPISODE.value,
                    media_id=media_id,
                    season_number=season_number,
                )
            }

            episodes_to_update = []
            episode_count = 0

            for episode_data in metadata["episodes"]:
                episode_number = episode_data["episode_number"]
                if episode_number in existing_episodes:
                    episode_item = existing_episodes[episode_number]
                    episode_item.title = metadata["title"]
                    episode_item.image = episode_data["image"]
                    episodes_to_update.append(episode_item)
                    episode_count += 1

            logger.info(
                "Found %s existing episodes to update for %s",
                episode_count,
                title,
            )

            if episodes_to_update:
                updated_count = Item.objects.bulk_update(
                    episodes_to_update,
                    ["title", "image"],
                    batch_size=100,
                )
                logger.info(
                    "Successfully updated %s episodes for %s",
                    updated_count,
                    title,
                )

        item.fetch_releases(delay=False)

        msg = f"{title} was synced to {Sources(source).label} successfully."
        messages.success(request, msg)

    if request.headers.get("HX-Request"):
        return HttpResponse(
            status=204,
            headers={
                "HX-Redirect": request.POST["next"],
            },
        )
    return helpers.redirect_back(request)


@require_GET
def track_modal(
    request,
    source,
    media_type,
    media_id,
    season_number=None,
):
    """Return the tracking form for a media item."""
    instance_id = request.GET.get("instance_id")
    if instance_id:
        media = BasicMedia.objects.get_media(
            request.user,
            media_type,
            instance_id,
        )
    elif request.GET.get("is_create"):
        media = None
    else:
        # no specific instance, try to find the first one
        user_medias = BasicMedia.objects.filter_media(
            request.user,
            media_id,
            media_type,
            source,
            season_number=season_number,
        )
        media = user_medias.first()
        if media:
            instance_id = media.id

    initial_data = {
        "media_id": media_id,
        "source": source,
        "media_type": media_type,
        "season_number": season_number,
        "instance_id": instance_id,
    }

    if media:
        title = media.item
        if media_type == MediaTypes.GAME.value:
            initial_data["progress"] = helpers.minutes_to_hhmm(media.progress)
    else:
        title = services.get_media_metadata(
            media_type,
            media_id,
            source,
            [season_number],
        )["title"]
        if media_type == MediaTypes.SEASON.value:
            title += f" S{season_number}"

    form_class = get_form_class(media_type)
    if form_class is None:
        return HttpResponseBadRequest(
            f"Media type '{media_type}' cannot be tracked directly. "
            "Please use a specific subtype (album, ep, or single)."
        )
    form = form_class(instance=media, initial=initial_data)

    return render(
        request,
        "app/components/fill_track.html",
        {
            "title": title,
            "form": form,
            "media": media,
            "return_url": request.GET["return_url"],
        },
    )


def _get_or_create_media_instance(
    request,
    media_type,
    media_id,
    source,
    season_number,
    instance_id,
):
    """Fetch an existing tracked instance, or build an unsaved one for a new item.

    Shared by media_save and quick_plan so both entry points create/patch
    Items identically and stay in sync as provider logic evolves.
    """
    if instance_id:
        return BasicMedia.objects.get_media(
            request.user,
            media_type,
            instance_id,
        )

    metadata = services.get_media_metadata(
        media_type,
        media_id,
        source,
        [season_number],
    )
    item, _ = Item.objects.get_or_create(
        media_id=media_id,
        source=source,
        media_type=media_type,
        season_number=season_number,
        defaults={
            "title": metadata["title"],
            "image": metadata["image"],
            "country": metadata.get("country", ""),
            "release_year": get_release_year_from_metadata(metadata),
        },
    )
    # Patch image/country/release_year if the item already existed with
    # blank/placeholder/unset values. Title is always re-synced to the
    # freshly-fetched provider metadata (not just when empty) -- a
    # pre-existing Item can have a wrong title left over from a
    # bad import match or stub creation, and since we already paid for a live
    # metadata fetch for this exact media_id/source, it's always the source of
    # truth. Mirrors the unconditional title overwrite in sync_metadata.
    update_fields = []
    real_image = metadata["image"] and metadata["image"] != settings.IMG_NONE
    if (not item.image or item.image == settings.IMG_NONE) and real_image:
        item.image = metadata["image"]
        update_fields.append("image")
    if metadata["title"] and item.title != metadata["title"]:
        item.title = metadata["title"]
        update_fields.append("title")
    if not item.country and metadata.get("country"):
        item.country = metadata["country"]
        update_fields.append("country")
    if item.release_year is None:
        release_year = get_release_year_from_metadata(metadata)
        if release_year is not None:
            item.release_year = release_year
            update_fields.append("release_year")
    if update_fields:
        item.save(update_fields=update_fields)
    model = apps.get_model(app_label="app", model_name=media_type)
    return model(item=item, user=request.user, country=metadata.get("country") or "")


def _sync_media_collections(request, source, media_type, media_id):
    """Auto-sync the relevant collection/series after a media item is saved.

    Shared by media_save and quick_plan so both entry points trigger the
    same downstream collection syncing.
    """
    # Auto-sync TMDB movie collections
    if source == Sources.TMDB.value and media_type == MediaTypes.MOVIE.value:
        try:
            from app.providers.collections_providers import sync_tmdb_collection
            # Bust cache so we always get fresh collection data
            cache.delete(f"{Sources.TMDB.value}_{MediaTypes.MOVIE.value}_{media_id}")
            movie_metadata = services.get_media_metadata(
                media_type, media_id, source
            )
            sync_tmdb_collection(request.user, movie_metadata)
        except Exception:
            logger.exception("Failed to sync TMDB collection for %s", media_id)

    # Auto-sync IGDB game series
    if source == Sources.IGDB.value and media_type == MediaTypes.GAME.value:
        try:
            from app.providers.collections_providers import sync_igdb_collection
            # Bust the cache first so we always get fresh collection data
            cache.delete(f"{Sources.IGDB.value}_{MediaTypes.GAME.value}_{media_id}")
            game_metadata = services.get_media_metadata(
                media_type, media_id, source
            )
            sync_igdb_collection(request.user, game_metadata)
        except Exception:
            logger.exception("Failed to sync IGDB collection for %s", media_id)

    # Auto-sync Hardcover book series
    if source == Sources.HARDCOVER.value and media_type == MediaTypes.BOOK.value:
        try:
            from app.providers.collections_providers import sync_hardcover_series
            book_metadata = services.get_media_metadata(
                media_type, media_id, source
            )
            sync_hardcover_series(request.user, book_metadata)
        except Exception:
            logger.exception("Failed to sync Hardcover series for %s", media_id)

    # Auto-sync BnF BD series
    if source == Sources.BNF.value and media_type == MediaTypes.COMIC.value:
        try:
            from app.providers.collections_providers import sync_bnf_series
            comic_metadata = services.get_media_metadata(
                media_type, media_id, source
            )
            sync_bnf_series(request.user, comic_metadata)
        except Exception:
            logger.exception("Failed to sync BnF series for %s", media_id)

    # Auto-sync ComicVine volume (issue-tracked comics only -- comic()
    # only embeds "comicvine_volume" for "i<id>" media_ids; legacy
    # volume-tracked comics have no such key, so this is a no-op for them)
    if source == Sources.COMICVINE.value and media_type == MediaTypes.COMIC.value:
        try:
            from app.providers.collections_providers import sync_comicvine_volume
            comic_metadata = services.get_media_metadata(
                media_type, media_id, source
            )
            sync_comicvine_volume(request.user, comic_metadata)
        except Exception:
            logger.exception("Failed to sync ComicVine volume for %s", media_id)


@require_POST
def media_save(request):
    """Save or update media data to the database."""
    media_id = request.POST["media_id"]
    source = request.POST["source"]
    media_type = request.POST["media_type"]
    season_number = request.POST.get("season_number")
    instance_id = request.POST.get("instance_id")

    instance = _get_or_create_media_instance(
        request,
        media_type,
        media_id,
        source,
        season_number,
        instance_id,
    )

    # Validate the form and save the instance if it's valid
    form_class = get_form_class(media_type)
    form = form_class(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        logger.info("%s saved successfully.", form.instance)
        _sync_media_collections(request, source, media_type, media_id)
    else:
        logger.error(form.errors.as_json())
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request,
                    f"{field.replace('_', ' ').title()}: {error}",
                )

    return helpers.redirect_back(request)


@require_POST
def quick_plan(request):
    """Mark a media item as Planning directly from a grid/search quick-action.

    Skips the track form entirely: updates an existing tracked instance's
    status in place (leaving score/progress/dates/notes untouched), or
    creates a new minimal entry with status=Planning for untracked items.
    """
    media_id = request.POST["media_id"]
    source = request.POST["source"]
    media_type = request.POST["media_type"]
    season_number = request.POST.get("season_number")
    instance_id = request.POST.get("instance_id")

    if media_type == MediaTypes.EPISODE.value:
        return HttpResponseBadRequest("Episodes don't have a Planning status.")

    instance = _get_or_create_media_instance(
        request,
        media_type,
        media_id,
        source,
        season_number,
        instance_id,
    )
    instance.status = Status.PLANNING.value
    instance.save()
    logger.info("%s marked as Planning.", instance)
    _sync_media_collections(request, source, media_type, media_id)

    messages.success(request, f"{instance.item.title} added to Planning.")

    return helpers.redirect_back(request)


@require_POST
def media_delete(request):
    """Delete media data from the database."""
    instance_id = request.POST["instance_id"]
    media_type = request.POST["media_type"]
    model = apps.get_model(app_label="app", model_name=media_type)

    try:
        media = BasicMedia.objects.get_media(
            request.user,
            media_type,
            instance_id,
        )
        media.delete()
        logger.info("%s deleted successfully.", media)

    except model.DoesNotExist:
        logger.warning("The %s was already deleted before.", media_type)

    return helpers.redirect_back(request)


@require_POST
def mark_user_messages_shown(request):
    """Mark all unseen persistent messages for the user as shown."""
    message_ids = [
        int(message_id)
        for message_id in request.POST.getlist("message_ids")
        if message_id.isdigit()
    ]
    if not message_ids:
        return HttpResponse(status=204)

    UserMessage.objects.filter(
        id__in=message_ids,
        user=request.user,
        shown_at__isnull=True,
    ).update(shown_at=timezone.now())
    return HttpResponse(status=204)


@require_POST
def episode_save(request):
    """Handle the creation, deletion, and updating of episodes for a season."""
    media_id = request.POST["media_id"]
    season_number = int(request.POST["season_number"])
    episode_number = int(request.POST["episode_number"])
    source = request.POST["source"]

    form = EpisodeForm(request.POST)
    if not form.is_valid():
        logger.error("Form validation failed: %s", form.errors)
        return HttpResponseBadRequest("Invalid form data")

    try:
        related_season = Season.objects.get(
            item__media_id=media_id,
            item__source=source,
            item__season_number=season_number,
            item__episode_number=None,
            user=request.user,
        )
    except Season.DoesNotExist:
        tv_with_seasons_metadata = services.get_media_metadata(
            "tv_with_seasons",
            media_id,
            source,
            [season_number],
        )
        season_metadata = tv_with_seasons_metadata[f"season/{season_number}"]

        item, _ = Item.objects.get_or_create(
            media_id=media_id,
            source=Sources.TMDB.value,
            media_type=MediaTypes.SEASON.value,
            season_number=season_number,
            defaults={
                "title": tv_with_seasons_metadata["title"],
                "image": season_metadata["image"],
            },
        )
        related_season = Season.objects.create(
            item=item,
            user=request.user,
            score=None,
            status=Status.IN_PROGRESS.value,
            notes="",
        )

        logger.info("%s did not exist, it was created successfully.", related_season)

    related_season.watch(episode_number, form.cleaned_data["end_date"])

    return helpers.redirect_back(request)


@require_http_methods(["GET", "POST"])
def create_entry(request):
    """Return the form for manually adding media items."""
    if request.method == "GET":
        media_types = MediaTypes.values
        return render(request, "app/create_entry.html", {"media_types": media_types})

    # Process the form submission
    form = ManualItemForm(request.POST, user=request.user)
    if not form.is_valid():
        # Handle form validation errors
        logger.error(form.errors.as_json())
        helpers.form_error_messages(form, request)
        return redirect("create_entry")

    # Try to save the item
    try:
        item = form.save()
    except IntegrityError:
        # Handle duplicate item
        media_name = form.cleaned_data["title"]
        if form.cleaned_data.get("season_number"):
            media_name += f" - Season {form.cleaned_data['season_number']}"
        if form.cleaned_data.get("episode_number"):
            media_name += f" - Episode {form.cleaned_data['episode_number']}"

        logger.exception("%s already exists in the database.", media_name)
        messages.error(request, f"{media_name} already exists in the database.")
        return redirect("create_entry")

    media_type = item.media_type

    # Prepare and validate the media form
    updated_request = request.POST.copy()
    updated_request.update({"source": item.source, "media_id": item.media_id})
    media_form = get_form_class(media_type)(updated_request)

    if not media_form.is_valid():
        # Handle media form validation errors
        logger.error(media_form.errors.as_json())
        helpers.form_error_messages(media_form, request)

        # Delete the item since the media creation failed
        item.delete()
        logger.info("%s was deleted due to media form validation failure", item)
        return redirect("create_entry")

    # Save the media instance
    media_form.instance.user = request.user
    media_form.instance.item = item

    # Handle relationships based on media type
    if item.media_type == MediaTypes.SEASON.value:
        media_form.instance.related_tv = form.cleaned_data["parent_tv"]
    elif item.media_type == MediaTypes.EPISODE.value:
        media_form.instance.related_season = form.cleaned_data["parent_season"]

    media_form.save()

    # Success message
    msg = f"{item} added successfully."
    messages.success(request, msg)
    logger.info(msg)

    return redirect("create_entry")


@require_GET
def search_parent_tv(request):
    """Return the search results for parent TV shows."""
    query = request.GET.get("q", "").strip()

    if len(query) <= 1:
        return render(request, "app/components/search_parent_tv.html")

    logger.debug(
        "%s - Searching for TV shows with query: %s",
        request.user.username,
        query,
    )

    parent_tvs = TV.objects.filter(
        user=request.user,
        item__source=Sources.MANUAL.value,
        item__media_type=MediaTypes.TV.value,
        item__title__icontains=query,
    )[:5]

    return render(
        request,
        "app/components/search_parent_tv.html",
        {"results": parent_tvs, "query": query},
    )


@require_GET
def search_parent_season(request):
    """Return the search results for parent seasons."""
    query = request.GET.get("q", "").strip()

    if len(query) <= 1:
        return render(request, "app/components/search_parent_tv.html")

    logger.debug(
        "%s - Searching for seasons with query: %s",
        request.user.username,
        query,
    )

    parent_seasons = Season.objects.filter(
        user=request.user,
        item__source=Sources.MANUAL.value,
        item__media_type=MediaTypes.SEASON.value,
        item__title__icontains=query,
    )[:5]

    return render(
        request,
        "app/components/search_parent_season.html",
        {"results": parent_seasons, "query": query},
    )


@require_GET
def history_modal(
    request,
    source,
    media_type,
    media_id,
    season_number=None,
    episode_number=None,
):
    """Return the history page for a media item."""
    user_medias = BasicMedia.objects.filter_media(
        request.user,
        media_id,
        media_type,
        source,
        season_number=season_number,
        episode_number=episode_number,
    )

    total_medias = user_medias.count()
    timeline_entries = []
    for index, media in enumerate(user_medias, start=1):
        if history := media.history.all():
            media_entry_number = total_medias - index + 1
            timeline_entries.extend(
                history_processor.process_history_entries(
                    history,
                    media_type,
                    media_entry_number,
                    request.user,
                ),
            )
    return render(
        request,
        "app/components/fill_history.html",
        {
            "media_type": media_type,
            "timeline": timeline_entries,
            "total_medias": total_medias,
            "return_url": request.GET["return_url"],
        },
    )


@require_http_methods(["DELETE"])
def delete_history_record(request, media_type, history_id):
    """Delete a specific history record."""
    try:
        historical_model = apps.get_model(
            app_label="app",
            model_name=f"historical{media_type.lower()}",
        )

        historical_model.objects.get(
            history_id=history_id,
            history_user=request.user,
        ).delete()

        logger.info(
            "Deleted history record %s",
            str(history_id),
        )

        # Return empty 200 response - the element will be removed by HTMX
        return HttpResponse()

    except historical_model.DoesNotExist:
        logger.exception(
            "History record %s not found for user %s",
            str(history_id),
            str(request.user),
        )
        return HttpResponse("Record not found", status=404)


def _parse_statistics_date_range(request):
    """Parse start-date/end-date query params, defaulting to All Time."""
    start_date_str = request.GET.get("start-date") or "all"
    end_date_str = request.GET.get("end-date") or "all"

    if start_date_str == "all" and end_date_str == "all":
        return None, None

    start_date = parse_date(start_date_str)
    end_date = parse_date(end_date_str)

    if start_date and end_date:
        # Convert to datetime with timezone awareness
        start_date = timezone.make_aware(
            datetime.combine(start_date, datetime.min.time()),
        )

        # End date should be end of day
        end_date = timezone.make_aware(
            datetime.combine(end_date, datetime.max.time()),
        )

    return start_date, end_date


@require_GET
def statistics(request):
    """Return the statistics page shell.

    The shell renders immediately without touching the (potentially slow,
    cache-cold) statistics computation -- the actual content is loaded
    right after via HTMX from `statistics_content`, so a cold cache shows
    a spinner instead of blocking the whole page load.
    """
    start_date, end_date = _parse_statistics_date_range(request)

    context = {
        "date_format_values": DateFormatChoices.values,
        "start_date": start_date,
        "end_date": end_date,
        "start_date_param": request.GET.get("start-date") or "all",
        "end_date_param": request.GET.get("end-date") or "all",
    }

    return render(request, "app/statistics.html", context)


@require_GET
def statistics_content(request):
    """HTMX endpoint: the actual (potentially expensive) statistics content.

    Loaded by the statistics page shell right after initial render, so a
    cache-cold computation shows a spinner in place instead of blocking
    the whole page.
    """
    start_date, end_date = _parse_statistics_date_range(request)

    context = {**stats.get_statistics_context(request.user, start_date, end_date)}

    return render(request, "app/components/statistics_content.html", context)


@require_POST
def statistics_refresh(request):
    """Invalidate this user's statistics cache before the next HTMX load."""
    stats.invalidate_statistics_cache(request.user.id)
    start_date = request.POST.get("start-date", "all")
    end_date = request.POST.get("end-date", "all")
    query = urlencode({"start-date": start_date, "end-date": end_date})
    return redirect(f"{reverse('statistics')}?{query}")


@require_GET
def award_progress_detail(request, award_slug):
    """HTMX endpoint: full per-winner breakdown for one award category."""
    detail = stats.get_award_winners_detail(request.user, award_slug)
    if detail is None:
        raise Http404("Award not found")
    return render(request, "app/components/award_detail.html", {"award": detail})


@require_GET
def list_progress_detail(request, list_slug):
    """HTMX endpoint: full per-entry breakdown for one curated list."""
    detail = stats.get_list_winners_detail(request.user, list_slug)
    if detail is None:
        raise Http404("List not found")
    return render(request, "app/components/list_detail.html", {"curated_list": detail})


@require_GET
def service_worker():
    """Serve the service worker file."""
    sw_path = Path(settings.STATICFILES_DIRS[0]) / "js" / "serviceworker.js"
    with sw_path.open() as f:
        response = HttpResponse(f.read(), content_type="application/javascript")
        response["Service-Worker-Allowed"] = "/"
        return response
