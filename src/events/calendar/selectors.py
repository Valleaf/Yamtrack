import logging

from django.db.models import Exists, OuterRef, Q, Subquery
from django.utils import timezone

from app.models import Item, MediaTypes, Sources
from app.providers import services, tmdb
from events.models import Event

logger = logging.getLogger(__name__)


def get_items_to_process(user=None):
    """Get items to process for the calendar."""
    media_types = [
        choice.value
        for choice in MediaTypes
        if choice not in [MediaTypes.SEASON, MediaTypes.EPISODE]
    ]

    query = Q()

    for media_type in media_types:
        media_query = Q(**{f"{media_type}__isnull": False})

        if user:
            media_query &= Q(**{f"{media_type}__user": user})

        query |= media_query

    query &= ~Q(source=Sources.MANUAL.value)

    items = Item.objects.filter(query).distinct()

    return filter_items_to_fetch(items)


def filter_items_to_fetch(items):
    """Filter items that need calendar events according to specific rules."""
    now = timezone.now()
    one_year_ago = now - timezone.timedelta(days=365)

    tv_items = items.filter(
        media_type=MediaTypes.TV.value,
        source=Sources.TMDB.value,
    )
    tv_items_to_include = get_tv_items_to_include(tv_items)

    movie_items = items.filter(
        media_type=MediaTypes.MOVIE.value,
        source=Sources.TMDB.value,
    )
    movie_items_to_include = get_movie_items_to_include(movie_items)

    future_events = Event.objects.filter(
        item=OuterRef("pk"),
        datetime__gte=now,
    )

    latest_comic_event = Event.objects.filter(
        item=OuterRef("pk"),
        item__media_type=MediaTypes.COMIC.value,
    ).order_by("-datetime")

    annotated = items.annotate(
        has_future_events=Exists(future_events),
        latest_comic_event_datetime=Subquery(latest_comic_event.values("datetime")[:1]),
    )

    tv_q = Q(id__in=tv_items_to_include)
    movie_q = Q(id__in=movie_items_to_include)

    comic_q = Q(media_type=MediaTypes.COMIC.value) & (
        Q(event__isnull=True) | Q(latest_comic_event_datetime__gte=one_year_ago)
    )

    other_q = (
        ~Q(media_type__in=[MediaTypes.TV.value, MediaTypes.COMIC.value])
        & ~Q(media_type=MediaTypes.MOVIE.value, source=Sources.TMDB.value)
        & (Q(event__isnull=True) | Q(has_future_events=True))
    )

    return annotated.filter(tv_q | movie_q | comic_q | other_q).distinct()


def get_tv_items_to_include(tv_items):
    """Return tracked TMDB TV item ids that should be refreshed."""
    tracked_count = tv_items.count()
    if not tracked_count:
        return []

    changed_tv_ids = get_changed_tmdb_tv_ids()
    season_events = Event.objects.filter(
        item__media_id=OuterRef("media_id"),
        item__source=OuterRef("source"),
        item__media_type=MediaTypes.SEASON.value,
    )

    tv_items_with_events = tv_items.annotate(
        has_season_events=Exists(season_events),
    )

    included_tv_rows = list(
        tv_items_with_events.filter(
            Q(media_id__in=changed_tv_ids) | Q(has_season_events=False),
        )
        .values("id", "media_id", "title", "has_season_events"),
    )

    unchanged_tv_items_with_events = tv_items_with_events.filter(
        ~Q(media_id__in=changed_tv_ids),
        has_season_events=True,
    )

    additional_tv_rows = []
    additional_tv_ids = set()
    for tv_item in unchanged_tv_items_with_events:
        if _tv_item_has_missing_seasons(tv_item):
            additional_tv_rows.append(
                {
                    "id": tv_item.id,
                    "media_id": tv_item.media_id,
                    "title": tv_item.title,
                    "has_season_events": True,
                },
            )
            additional_tv_ids.add(tv_item.id)

    selected_rows = included_tv_rows + additional_tv_rows

    logger.info(
        "TV selection: %d tracked TMDB shows, %d changed ids, %d selected",
        tracked_count,
        len(changed_tv_ids),
        len(selected_rows),
    )

    for item in selected_rows:
        if item["media_id"] in changed_tv_ids:
            logger.info(
                "TV selection: including %s (%s) because TMDB reported changes",
                item["title"],
                item["media_id"],
            )
        elif item["id"] in additional_tv_ids:
            logger.info(
                "TV selection: including %s (%s) because it has new seasons available",
                item["title"],
                item["media_id"],
            )
        else:
            logger.info(
                "TV selection: including %s (%s) because it has no season events yet",
                item["title"],
                item["media_id"],
            )

    return [item["id"] for item in selected_rows]


def _tv_item_has_missing_seasons(tv_item):
    """Return True if TMDB knows of seasons not yet represented by season events."""
    try:
        tv_metadata = tmdb.tv(tv_item.media_id)
    except services.ProviderAPIError:
        logger.warning(
            "Failed to fetch TMDB metadata for %s while selecting TV items to refresh",
            tv_item,
        )
        return False

    season_numbers = {
        season["season_number"]
        for season in tv_metadata.get("related", {}).get("seasons", [])
        if season.get("season_number") is not None
    }

    if not season_numbers:
        return False

    existing_season_numbers = set(
        Event.objects.filter(
            item__media_id=tv_item.media_id,
            item__source=tv_item.source,
            item__media_type=MediaTypes.SEASON.value,
        ).values_list("item__season_number", flat=True),
    )

    return any(
        season_number not in existing_season_numbers
        for season_number in season_numbers
    )


def get_movie_items_to_include(movie_items):
    """Return tracked TMDB movie item ids that should be refreshed."""
    if not movie_items.exists():
        return []

    changed_movie_ids = get_changed_tmdb_movie_ids()

    return list(
        movie_items.filter(
            Q(media_id__in=changed_movie_ids) | Q(event__isnull=True),
        ).values_list("id", flat=True),
    )


def get_changed_tmdb_tv_ids():
    """Return changed TMDB TV ids, tolerating provider errors."""
    try:
        return tmdb.tv_changes()
    except services.ProviderAPIError:
        logger.warning("Failed to fetch TMDB TV changes")
        return set()


def get_changed_tmdb_movie_ids():
    """Return changed TMDB movie ids, tolerating provider errors."""
    try:
        return tmdb.movie_changes()
    except services.ProviderAPIError:
        logger.warning("Failed to fetch TMDB movie changes")
        return set()
