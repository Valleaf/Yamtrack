import calendar
import datetime
import heapq
import itertools
import logging
import math
from collections import defaultdict
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models import (
    Prefetch,
    Q,
)
from django.urls import reverse
from django.utils import timezone

from app import config
from app.date_utils import get_release_year_from_metadata
from app.models import (
    TV,
    BasicMedia,
    Episode,
    Item,
    MediaManager,
    MediaTypes,
    Season,
    Sources,
    Status,
)
from app.templatetags import app_tags

logger = logging.getLogger(__name__)

STATISTICS_CACHE_TIMEOUT = getattr(settings, "STATISTICS_CACHE_TIMEOUT", 60 * 60 * 24)
_STATISTICS_CACHE_VERSION_KEY = "statistics:context:version:{user_id}"
_STATISTICS_SECTION_CACHE_KEY = (
    "statistics:section:{section}:{user_id}:{version}:{media_types}:{start_date}:{end_date}"
)


def invalidate_statistics_cache(user_id):
    """Bump the per-user stats cache version so old cached sections are ignored."""
    cache.set(
        _STATISTICS_CACHE_VERSION_KEY.format(user_id=user_id),
        timezone.now().isoformat(),
        timeout=None,
    )


def _get_statistics_version(user_id):
    version = cache.get(_STATISTICS_CACHE_VERSION_KEY.format(user_id=user_id))
    if version is None:
        version = timezone.now().isoformat()
        cache.set(
            _STATISTICS_CACHE_VERSION_KEY.format(user_id=user_id),
            version,
            timeout=None,
        )
    return version


def _get_section_cache_key(section, user_id, start_date, end_date, active_media_types, version):
    return _STATISTICS_SECTION_CACHE_KEY.format(
        section=section,
        user_id=user_id,
        version=version,
        media_types="-".join(active_media_types),
        start_date=_date_cache_part(start_date),
        end_date=_date_cache_part(end_date),
    )


def _date_cache_part(value):
    if value is None:
        return "all"
    return value.isoformat()


# Sections that only need `user_media` (the date-range-filtered queryset dict)
# to compute. Each is cached and recomputed independently, so a slow or
# failing section never blanks out the rest of the page, and only the
# sections actually missing from cache get recomputed on a partial hit.
_USER_MEDIA_SECTIONS = {
    "media_type_distribution": lambda user_media, media_count: get_media_type_distribution(media_count),
    "progress_distribution": lambda user_media, media_count: get_progress_distribution(user_media),
    "country_distribution": lambda user_media, media_count: get_country_distribution(user_media),
    "media_by_type_country": lambda user_media, media_count: get_media_by_type_country_data(user_media),
    "genre_distribution": lambda user_media, media_count: get_genre_distribution(user_media),
    "people_stats": lambda user_media, media_count: get_people_stats(user_media),
}


def get_statistics_context(user, start_date, end_date):
    """Return the rendered statistics context, assembled from independently cached sections.

    Each section is cached under its own key so a cold or failing section
    never blanks out the rest of the page, and a partial cache hit only
    recomputes what's actually missing instead of rebuilding everything.
    """
    active_media_types = tuple(user.get_active_media_types())
    version = _get_statistics_version(user.id)

    def section_key(section):
        return _get_section_cache_key(
            section, user.id, start_date, end_date, active_media_types, version,
        )

    context = {"start_date": start_date, "end_date": end_date}
    missing_sections = []

    all_section_names = [
        "media_count", "activity_data", *_USER_MEDIA_SECTIONS.keys(),
        "score_distribution", "top_rated", "status_distribution",
        "status_pie_chart_data", "extended_statistics", "timeline",
        "year_chart_data", "decade_chart_data", "release_year_chart_data",
        "release_decade_chart_data", "list_progress", "awards_progress",
        "personal_best",
    ]
    for section in all_section_names:
        cached_value = cache.get(section_key(section))
        if cached_value is None:
            missing_sections.append(section)
        else:
            context[section] = cached_value["value"]

    if missing_sections:
        logger.info(
            "%s - Rebuilding statistics sections: %s", user, missing_sections,
        )
        rebuilt = build_statistics_sections(
            user, start_date, end_date, missing_sections,
        )
        for section, value in rebuilt.items():
            cache.set(
                section_key(section),
                {"value": value},
                timeout=STATISTICS_CACHE_TIMEOUT,
            )
            context[section] = value
    else:
        logger.info("%s - Retrieved statistics context from cache", user)

    return context


def build_statistics_sections(user, start_date, end_date, sections=None):
    """Compute the requested statistics sections (all of them if unspecified).

    Shares the underlying queries (user_media, all_time_media, extended_statistics)
    across whichever sections were actually requested, so a partial rebuild
    doesn't refetch data that isn't needed for the missing sections -- but
    since most sections derive from the same one or two querysets, this is
    mainly about avoiding duplicate work on a full (cold-cache) build.
    """
    want = set(sections) if sections is not None else None

    def needed(*names):
        return want is None or any(n in want for n in names)

    result = {}

    user_media, media_count = get_user_media(user, start_date, end_date)
    if needed("media_count"):
        result["media_count"] = media_count

    for section, fn in _USER_MEDIA_SECTIONS.items():
        if needed(section):
            result[section] = fn(user_media, media_count)

    if needed("score_distribution", "top_rated"):
        score_distribution, top_rated = get_score_distribution(user_media)
        result["score_distribution"] = score_distribution
        result["top_rated"] = top_rated

    if needed("status_distribution", "status_pie_chart_data"):
        status_distribution = get_status_distribution(user_media)
        result["status_distribution"] = status_distribution
        result["status_pie_chart_data"] = get_status_pie_chart_data(status_distribution)

    extended_statistics = None
    if needed("extended_statistics", "year_chart_data", "decade_chart_data"):
        extended_statistics = get_extended_statistics(user_media)
        if needed("extended_statistics"):
            result["extended_statistics"] = extended_statistics
        if needed("year_chart_data"):
            result["year_chart_data"] = get_year_chart_data(extended_statistics["year_rows"])
        if needed("decade_chart_data"):
            result["decade_chart_data"] = get_decade_chart_data(extended_statistics["year_rows"])

    if needed("release_year_chart_data", "release_decade_chart_data"):
        release_year_dist = get_release_year_distribution(user_media)
        if needed("release_year_chart_data"):
            result["release_year_chart_data"] = get_release_year_chart_data(release_year_dist)
        if needed("release_decade_chart_data"):
            result["release_decade_chart_data"] = get_release_decade_chart_data(release_year_dist)

    # Timeline and Personal Best are always all-time and independent of the
    # date filter (timeline shows full history regardless of range; personal
    # best is keyed by release year/decade, not consumption date) -- they
    # share one unfiltered fetch instead of querying the DB twice.
    if needed("timeline", "personal_best"):
        if start_date is None and end_date is None:
            all_time_media = user_media
        else:
            all_time_media, _ = get_user_media(user, None, None)
        if needed("timeline"):
            result["timeline"] = get_timeline(all_time_media)
        if needed("personal_best"):
            result["personal_best"] = get_personal_best(all_time_media)

    if needed("activity_data"):
        result["activity_data"] = get_activity_data(user, start_date, end_date)

    if needed("list_progress"):
        result["list_progress"] = get_list_progress(user)

    if needed("awards_progress"):
        result["awards_progress"] = get_awards_progress(user)

    return result


def build_statistics_context(user, start_date, end_date):
    """Calculate all statistics for the requested date range, uncached.

    Kept for callers that want a full synchronous rebuild without going
    through the per-section cache (e.g. the Celery warm-up task).
    """
    sections = build_statistics_sections(user, start_date, end_date)
    return {
        "start_date": start_date,
        "end_date": end_date,
        **sections,
    }


def get_user_media(user, start_date, end_date):
    """Get all media items and their counts for a user within date range."""
    media_models = [
        apps.get_model(app_label="app", model_name=media_type)
        for media_type in user.get_active_media_types()
    ]
    user_media = {}
    media_count = {"total": 0}

    # Cache the base episodes query
    base_episodes = None
    if TV in media_models or Season in media_models:
        if start_date is None and end_date is None:
            base_episodes = Episode.objects.filter(related_season__user=user)
        else:
            base_episodes = Episode.objects.filter(
                related_season__user=user,
                end_date__range=(start_date, end_date),
            )

    for model in media_models:
        media_type = model.__name__.lower()
        queryset = None

        if model == TV:
            tv_ids = base_episodes.values_list(
                "related_season__related_tv", flat=True
            ).distinct()
            queryset = TV.objects.filter(id__in=tv_ids).prefetch_related(
                Prefetch(
                    "seasons",
                    queryset=Season.objects.select_related("item").prefetch_related(
                        Prefetch(
                            "episodes",
                            queryset=base_episodes.filter(
                                related_season__related_tv__in=tv_ids,
                            ),
                        ),
                    ),
                ),
            )
        elif model == Season:
            season_ids = base_episodes.values_list(
                "related_season", flat=True
            ).distinct()
            queryset = Season.objects.filter(id__in=season_ids).prefetch_related(
                Prefetch("episodes", queryset=base_episodes),
            )
        elif start_date is None and end_date is None:
            queryset = model.objects.filter(user=user)
        else:
            queryset = model.objects.filter(user=user).filter(
                (
                    Q(start_date__isnull=False)
                    & Q(end_date__isnull=False)
                    & ~(Q(end_date__lt=start_date) | Q(start_date__gt=end_date))
                )
                | (
                    Q(start_date__isnull=False)
                    & Q(end_date__isnull=True)
                    & Q(start_date__gte=start_date)
                    & Q(start_date__lte=end_date)
                )
                | (
                    Q(start_date__isnull=True)
                    & Q(end_date__isnull=False)
                    & Q(end_date__gte=start_date)
                    & Q(end_date__lte=end_date)
                ),
            )

        queryset = queryset.select_related("item")
        user_media[media_type] = queryset
        count = queryset.count()
        media_count[media_type] = count
        media_count["total"] += count

    logger.info(
        "%s - Retrieved media %s",
        user,
        "for all time" if start_date is None else f"from {start_date} to {end_date}",
    )
    return user_media, media_count


def get_media_type_distribution(media_count):
    """Get data formatted for Chart.js pie chart."""
    chart_data = {
        "labels": [],
        "datasets": [{"data": [], "backgroundColor": []}],
    }
    for media_type, count in media_count.items():
        if media_type != "total" and count > 0:
            label = app_tags.media_type_readable(media_type)
            chart_data["labels"].append(label)
            chart_data["datasets"][0]["data"].append(count)
            chart_data["datasets"][0]["backgroundColor"].append(
                config.get_stats_color(media_type),
            )
    return chart_data


def get_status_distribution(user_media):
    """Get status distribution for each media type within date range."""
    distribution = {}
    total_completed = 0
    status_order = list(Status.values)
    for media_type, media_list in user_media.items():
        status_counts = dict.fromkeys(status_order, 0)
        counts = media_list.values("status").annotate(count=models.Count("id"))
        for count_data in counts:
            status_counts[count_data["status"]] = count_data["count"]
            if count_data["status"] == Status.COMPLETED.value:
                total_completed += count_data["count"]
        distribution[media_type] = status_counts

    return {
        "labels": [app_tags.media_type_readable(x) for x in distribution],
        "datasets": [
            {
                "label": status,
                "data": [
                    distribution[media_type][status] for media_type in distribution
                ],
                "background_color": get_status_color(status),
                "total": sum(
                    distribution[media_type][status] for media_type in distribution
                ),
            }
            for status in status_order
        ],
        "total_completed": total_completed,
    }


def get_status_pie_chart_data(status_distribution):
    """Get status distribution as a pie chart."""
    chart_data = {
        "labels": [],
        "datasets": [{"data": [], "backgroundColor": []}],
    }
    for dataset in status_distribution["datasets"]:
        status_label = dataset["label"]
        status_count = dataset["total"]
        status_color = dataset["background_color"]
        if status_count > 0:
            chart_data["labels"].append(status_label)
            chart_data["datasets"][0]["data"].append(status_count)
            chart_data["datasets"][0]["backgroundColor"].append(status_color)
    return chart_data


def get_extended_statistics(user_media):
    """Build report-style statistics from the filtered media set."""
    media_type_rows = []
    source_stats = {}
    year_stats = {}
    score_buckets = {
        score: {
            "score": score,
            "count": 0,
            "percentage": 0,
            "bar_percentage": 0,
            "bar_color": (
                "bg-emerald-400" if score >= 8
                else "bg-yellow-400" if score >= 6
                else "bg-orange-400" if score >= 4
                else "bg-red-400"
            ),
        }
        for score in range(10, -1, -1)
    }
    rating_bands = [
        {"label": "Favorites", "range": "8-10", "min": 8, "max": 10, "count": 0, "color": "bg-emerald-400"},
        {"label": "Positive", "range": "6-7", "min": 6, "max": 7, "count": 0, "color": "bg-yellow-400"},
        {"label": "Mixed", "range": "4-5", "min": 4, "max": 5, "count": 0, "color": "bg-orange-400"},
        {"label": "Low", "range": "0-3", "min": 0, "max": 3, "count": 0, "color": "bg-red-400"},
    ]
    score_values = []
    total_items = 0
    completed_items = 0
    scored_items = 0
    highest_rated = None
    lowest_rated = None

    for media_type, media_list in user_media.items():
        items = list(media_list.select_related("item"))
        total = len(items)
        completed = 0
        scored = 0
        score_sum = Decimal("0")
        best_media = None

        for media in items:
            total_items += 1

            if media.status == Status.COMPLETED.value:
                completed += 1
                completed_items += 1

            add_year_stat(year_stats, media, "start_date", "started")
            add_year_stat(year_stats, media, "end_date", "completed")

            source_stats.setdefault(
                media.item.source,
                {
                    "source": Sources(media.item.source).label,
                    "count": 0,
                    "scored": 0,
                    "score_sum": Decimal("0"),
                    "average_score": None,
                    "percentage": 0,
                },
            )
            source_stats[media.item.source]["count"] += 1

            if media.score is None:
                continue

            scored += 1
            scored_items += 1
            score_sum += media.score
            score_values.append(float(media.score))
            score_buckets[int(media.score)]["count"] += 1

            for band in rating_bands:
                if band["min"] <= media.score <= band["max"]:
                    band["count"] += 1
                    break

            source_stats[media.item.source]["scored"] += 1
            source_stats[media.item.source]["score_sum"] += media.score

            if best_media is None or media.score > best_media.score:
                best_media = media
            if highest_rated is None or media.score > highest_rated.score:
                highest_rated = media
            if lowest_rated is None or media.score < lowest_rated.score:
                lowest_rated = media

        average_score = round(score_sum / scored, 2) if scored else None
        media_type_rows.append(
            {
                "media_type": media_type,
                "label": app_tags.media_type_readable(media_type),
                "total": total,
                "completed": completed,
                "completion_percentage": round(completed / total * 100) if total else 0,
                "scored": scored,
                "rated_percentage": round(scored / total * 100) if total else 0,
                "average_score": average_score,
                "best_media": best_media,
            },
        )

    median_score = get_median(score_values)
    completion_percentage = (
        round(completed_items / total_items * 100) if total_items else 0
    )

    max_bucket_count = max((b["count"] for b in score_buckets.values()), default=0)
    for bucket in score_buckets.values():
        if scored_items:
            bucket["percentage"] = round(bucket["count"] / scored_items * 100)
        if max_bucket_count > 0 and bucket["count"] > 0:
            bucket["bar_percentage"] = max(round(bucket["count"] / max_bucket_count * 100), 2)
        else:
            bucket["bar_percentage"] = 0

    max_band_count = max((b["count"] for b in rating_bands), default=0)
    for band in rating_bands:
        band["percentage"] = round(band["count"] / scored_items * 100) if scored_items else 0
        if max_band_count > 0 and band["count"] > 0:
            band["bar_percentage"] = max(round(band["count"] / max_band_count * 100), 2)
        else:
            band["bar_percentage"] = 0

    source_rows = []
    for stats in source_stats.values():
        if stats["scored"]:
            stats["average_score"] = round(stats["score_sum"] / stats["scored"], 2)
        if total_items:
            stats["percentage"] = round(stats["count"] / total_items * 100)
        source_rows.append(stats)

    source_rows.sort(key=lambda row: (-row["count"], row["source"]))
    media_type_rows.sort(key=lambda row: (-row["total"], row["label"]))
    year_rows = sorted(year_stats.values(), key=lambda row: row["year"], reverse=True)

    return {
        "summary": {
            "total_items": total_items,
            "completed_items": completed_items,
            "completion_percentage": completion_percentage,
            "scored_items": scored_items,
            "unrated_items": total_items - scored_items,
            "median_score": median_score,
            "highest_rated": highest_rated,
            "lowest_rated": lowest_rated,
        },
        "rating_bands": rating_bands,
        "score_buckets": list(score_buckets.values()),
        "media_type_rows": media_type_rows,
        "source_rows": source_rows,
        "year_rows": year_rows,
    }


def add_year_stat(year_stats, media, date_attr, counter_key):
    """Add a start or completion date to the yearly report."""
    media_date = getattr(media, date_attr, None)
    if not media_date:
        return
    year = local_date(media_date).year
    year_stats.setdefault(year, {"year": year, "started": 0, "completed": 0})
    year_stats[year][counter_key] += 1


def local_date(value):
    """Return a local date for date or datetime values."""
    if isinstance(value, datetime.datetime):
        return timezone.localdate(value)
    return value


def get_median(values):
    """Return the median score for a list of numbers."""
    if not values:
        return None
    sorted_values = sorted(values)
    midpoint = len(sorted_values) // 2
    if len(sorted_values) % 2:
        return round(sorted_values[midpoint], 2)
    return round((sorted_values[midpoint - 1] + sorted_values[midpoint]) / 2, 2)


def get_score_distribution(user_media):
    """Get score distribution for each media type within date range."""
    distribution = {}
    total_scored = 0
    total_score_sum = 0
    top_rated = []
    top_rated_count = 14
    counter = itertools.count()
    score_range = range(11)

    for media_type, media_list in user_media.items():
        score_counts = dict.fromkeys(score_range, 0)
        scored_media = media_list.exclude(score__isnull=True).select_related("item")

        for media in scored_media:
            if len(top_rated) < top_rated_count:
                heapq.heappush(top_rated, (float(media.score), next(counter), media))
            else:
                heapq.heappushpop(
                    top_rated, (float(media.score), next(counter), media)
                )
            binned_score = int(media.score)
            score_counts[binned_score] += 1
            total_scored += 1
            total_score_sum += media.score

        distribution[media_type] = score_counts

    average_score = (
        round(total_score_sum / total_scored, 2) if total_scored > 0 else None
    )
    top_rated_media = [
        media for _, _, media in sorted(top_rated, key=lambda x: (-x[0], x[1]))
    ]
    top_rated_media = _annotate_top_rated_media(top_rated_media)

    return {
        "labels": [str(score) for score in score_range],
        "datasets": [
            {
                "label": app_tags.media_type_readable(media_type),
                "data": [distribution[media_type][score] for score in score_range],
                "background_color": config.get_stats_color(media_type),
            }
            for media_type in distribution
        ],
        "average_score": average_score,
        "total_scored": total_scored,
    }, top_rated_media


def _annotate_top_rated_media(top_rated_media):
    """Apply prefetch_related and annotate max_progress for top rated media."""
    if not top_rated_media:
        return top_rated_media

    media_by_type = {}
    for media in top_rated_media:
        media_type = media.item.media_type
        if media_type not in media_by_type:
            media_by_type[media_type] = []
        media_by_type[media_type].append(media)

    media_manager = MediaManager()

    for media_type, media_list in media_by_type.items():
        model = apps.get_model(app_label="app", model_name=media_type)
        media_ids = [media.id for media in media_list]
        queryset = model.objects.filter(id__in=media_ids)
        queryset = media_manager._apply_prefetch_related(queryset, media_type)
        media_manager.annotate_max_progress(queryset, media_type)
        prefetched_media_map = {media.id: media for media in queryset}
        for i, media in enumerate(top_rated_media):
            if media.item.media_type == media_type:
                top_rated_media[i] = prefetched_media_map[media.id]

    return top_rated_media


def get_status_color(status):
    """Get the color for the status of the media."""
    try:
        return config.get_status_stats_color(status)
    except KeyError:
        return "rgba(201, 203, 207)"


def get_timeline(user_media):
    """Build a timeline of media consumption organized by month-year."""
    timeline = defaultdict(list)

    for media_type, queryset in user_media.items():
        if media_type == MediaTypes.TV.value:
            continue
        for media in queryset:
            local_start_date = local_date(media.start_date) if media.start_date else None
            local_end_date = local_date(media.end_date) if media.end_date else None

            if media.start_date and media.end_date:
                current_date = local_start_date
                while current_date <= local_end_date:
                    year = current_date.year
                    month = current_date.month
                    month_name = calendar.month_name[month]
                    month_year = f"{month_name} {year}"
                    timeline[month_year].append(media)
                    current_date += relativedelta(months=1)
                    current_date = current_date.replace(day=1)
            elif media.start_date:
                year = local_start_date.year
                month = local_start_date.month
                month_name = calendar.month_name[month]
                timeline[f"{month_name} {year}"].append(media)
            elif media.end_date:
                year = local_end_date.year
                month = local_end_date.month
                month_name = calendar.month_name[month]
                timeline[f"{month_name} {year}"].append(media)

    sorted_items = []
    for month_year, media_list in timeline.items():
        month_name, year_str = month_year.split()
        year = int(year_str)
        month = list(calendar.month_name).index(month_name)
        sorted_items.append((month_year, media_list, year, month))

    sorted_items.sort(key=lambda x: (x[2], x[3]), reverse=True)

    result = {}
    for month_year, media_list, _, _ in sorted_items:
        result[month_year] = sorted(media_list, key=time_line_sort_key, reverse=True)
    return result


def time_line_sort_key(media):
    """Sort media items in the timeline."""
    if media.end_date is not None:
        return local_date(media.end_date)
    return local_date(media.start_date)


def get_activity_data(user, start_date, end_date):
    """Get daily activity counts for the last year."""
    if end_date is None:
        end_date = timezone.localtime()

    start_date_aligned = get_aligned_monday(start_date)
    combined_data = get_filtered_historical_data(start_date_aligned, end_date, user)

    if start_date is None:
        dates = [item["date"] for item in combined_data]
        start_date = datetime.datetime.combine(
            min(dates) if dates else timezone.localdate(),
            datetime.time.min,
        )
        start_date_aligned = get_aligned_monday(start_date)

    date_counts = {}
    for item in combined_data:
        date = item["date"]
        date_counts[date] = date_counts.get(date, 0) + item["count"]

    date_range = [
        start_date_aligned.date() + datetime.timedelta(days=x)
        for x in range((end_date.date() - start_date_aligned.date()).days + 1)
    ]

    most_active_day, day_percentage = calculate_day_of_week_stats(
        date_counts, start_date.date()
    )
    current_streak, longest_streak = calculate_streaks(date_counts, end_date.date())

    activity_data = [
        {
            "date": current_date.strftime("%Y-%m-%d"),
            "count": date_counts.get(current_date, 0),
            "level": get_level(date_counts.get(current_date, 0)),
        }
        for current_date in date_range
    ]

    calendar_weeks = [activity_data[i : i + 7] for i in range(0, len(activity_data), 7)]

    months = []
    mondays_per_month = []
    current_month = date_range[0].strftime("%b")
    monday_count = 0

    for current_date in date_range:
        if current_date.weekday() == 0:
            month = current_date.strftime("%b")
            if current_month != month:
                if current_month is not None:
                    if monday_count > 1:
                        months.append(current_month)
                        mondays_per_month.append(monday_count)
                    else:
                        months.append("")
                        mondays_per_month.append(monday_count)
                current_month = month
                monday_count = 0
            monday_count += 1

    if monday_count > 1:
        months.append(current_month)
        mondays_per_month.append(monday_count)

    return {
        "calendar_weeks": calendar_weeks,
        "months": list(zip(months, mondays_per_month, strict=False)),
        "stats": {
            "most_active_day": most_active_day,
            "most_active_day_percentage": day_percentage,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
        },
    }


def get_aligned_monday(datetime_obj):
    """Get the Monday of the week containing the given date."""
    if datetime_obj is None:
        return None
    days_to_subtract = datetime_obj.weekday()
    return datetime_obj - datetime.timedelta(days=days_to_subtract)


def get_level(count):
    """Calculate intensity level (0-4) based on count."""
    thresholds = [0, 3, 6, 9]
    for i, threshold in enumerate(thresholds):
        if count <= threshold:
            return i
    return 4


def get_filtered_historical_data(start_date, end_date, user):
    """Return [{"date": datetime.date, "count": int}]."""
    historical_models = BasicMedia.objects.get_historical_models()
    local_tz = timezone.get_current_timezone()
    day_buckets = defaultdict(int)

    for model_name in historical_models:
        model = apps.get_model("app", model_name)
        qs = model.objects.filter(history_user_id=user)
        if start_date:
            qs = qs.filter(history_date__gte=start_date)
        if end_date:
            qs = qs.filter(history_date__lte=end_date)
        for ts in qs.values_list("history_date", flat=True).iterator(chunk_size=2_000):
            aware_ts = timezone.localtime(ts, local_tz)
            day_buckets[aware_ts.date()] += 1

    combined_data = [
        {"date": day, "count": count} for day, count in day_buckets.items()
    ]
    logger.info("%s - built historical data (%s rows)", user, len(combined_data))
    return combined_data


def calculate_day_of_week_stats(date_counts, start_date):
    """Calculate the most active day of the week based on activity frequency."""
    day_counts = defaultdict(int)
    total_active_days = 0

    for date in date_counts:
        if date < start_date:
            continue
        if date_counts[date] > 0:
            day_name = date.strftime("%A")
            day_counts[day_name] += 1
            total_active_days += 1

    if not total_active_days:
        return None, 0

    most_active_day = max(day_counts.items(), key=lambda x: x[1])
    percentage = (most_active_day[1] / total_active_days) * 100
    return most_active_day[0], round(percentage)


def calculate_streaks(date_counts, end_date):
    """Calculate current and longest activity streaks."""
    active_dates = sorted(
        [date for date, count in date_counts.items() if count > 0], reverse=True
    )

    if not active_dates:
        return 0, 0

    longest_streak = 1
    streak_count = 1
    is_current = active_dates[0] == end_date
    current_streak = 1 if is_current else 0

    for i in range(1, len(active_dates)):
        if (active_dates[i - 1] - active_dates[i]).days == 1:
            streak_count += 1
            if is_current:
                current_streak += 1
        else:
            longest_streak = max(longest_streak, streak_count)
            streak_count = 1
            if is_current:
                is_current = False

    longest_streak = max(longest_streak, streak_count)
    return current_streak, longest_streak


_MAX_COUNTRY_TITLES = 12

# ── ISO 3166-1 alpha-2 → English country name ─────────────────────────────────
_ISO_TO_NAME: dict[str, str] = {
    "AD": "Andorra", "AE": "United Arab Emirates", "AF": "Afghanistan",
    "AG": "Antigua and Barbuda", "AL": "Albania", "AM": "Armenia",
    "AO": "Angola", "AR": "Argentina", "AT": "Austria", "AU": "Australia",
    "AZ": "Azerbaijan", "BA": "Bosnia and Herzegovina", "BB": "Barbados",
    "BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso", "BG": "Bulgaria",
    "BH": "Bahrain", "BI": "Burundi", "BJ": "Benin", "BN": "Brunei",
    "BO": "Bolivia", "BR": "Brazil", "BS": "Bahamas", "BT": "Bhutan",
    "BW": "Botswana", "BY": "Belarus", "BZ": "Belize", "CA": "Canada",
    "CD": "DR Congo", "CF": "Central African Republic", "CG": "Congo",
    "CH": "Switzerland", "CI": "Cote d'Ivoire", "CL": "Chile",
    "CM": "Cameroon", "CN": "China", "CO": "Colombia", "CR": "Costa Rica",
    "CU": "Cuba", "CV": "Cape Verde", "CY": "Cyprus", "CZ": "Czechia",
    "DE": "Germany", "DJ": "Djibouti", "DK": "Denmark", "DM": "Dominica",
    "DO": "Dominican Republic", "DZ": "Algeria", "EC": "Ecuador",
    "EE": "Estonia", "EG": "Egypt", "ER": "Eritrea", "ES": "Spain",
    "ET": "Ethiopia", "FI": "Finland", "FJ": "Fiji", "FR": "France",
    "GA": "Gabon", "GB": "United Kingdom", "GD": "Grenada", "GE": "Georgia",
    "GH": "Ghana", "GM": "Gambia", "GN": "Guinea", "GQ": "Equatorial Guinea",
    "GR": "Greece", "GT": "Guatemala", "GW": "Guinea-Bissau", "GY": "Guyana",
    "HN": "Honduras", "HR": "Croatia", "HT": "Haiti", "HU": "Hungary",
    "ID": "Indonesia", "IE": "Ireland", "IL": "Israel", "IN": "India",
    "IQ": "Iraq", "IR": "Iran", "IS": "Iceland", "IT": "Italy",
    "JM": "Jamaica", "JO": "Jordan", "JP": "Japan", "KE": "Kenya",
    "KG": "Kyrgyzstan", "KH": "Cambodia", "KI": "Kiribati", "KM": "Comoros",
    "KN": "Saint Kitts and Nevis", "KP": "North Korea", "KR": "South Korea",
    "KW": "Kuwait", "KZ": "Kazakhstan", "LA": "Laos", "LB": "Lebanon",
    "LC": "Saint Lucia", "LI": "Liechtenstein", "LK": "Sri Lanka",
    "LR": "Liberia", "LS": "Lesotho", "LT": "Lithuania", "LU": "Luxembourg",
    "LV": "Latvia", "LY": "Libya", "MA": "Morocco", "MC": "Monaco",
    "MD": "Moldova", "ME": "Montenegro", "MG": "Madagascar",
    "MH": "Marshall Islands", "MK": "North Macedonia", "ML": "Mali",
    "MM": "Myanmar", "MN": "Mongolia", "MR": "Mauritania", "MT": "Malta",
    "MU": "Mauritius", "MV": "Maldives", "MW": "Malawi", "MX": "Mexico",
    "MY": "Malaysia", "MZ": "Mozambique", "NA": "Namibia", "NE": "Niger",
    "NG": "Nigeria", "NI": "Nicaragua", "NL": "Netherlands", "NO": "Norway",
    "NP": "Nepal", "NR": "Nauru", "NZ": "New Zealand", "OM": "Oman",
    "PA": "Panama", "PE": "Peru", "PG": "Papua New Guinea", "PH": "Philippines",
    "PK": "Pakistan", "PL": "Poland", "PT": "Portugal", "PW": "Palau",
    "PY": "Paraguay", "QA": "Qatar", "RO": "Romania", "RS": "Serbia",
    "RU": "Russia", "RW": "Rwanda", "SA": "Saudi Arabia",
    "SB": "Solomon Islands", "SC": "Seychelles", "SD": "Sudan",
    "SE": "Sweden", "SG": "Singapore", "SI": "Slovenia", "SK": "Slovakia",
    "SL": "Sierra Leone", "SM": "San Marino", "SN": "Senegal",
    "SO": "Somalia", "SR": "Suriname", "SS": "South Sudan",
    "ST": "Sao Tome and Principe", "SV": "El Salvador", "SY": "Syria",
    "SZ": "Eswatini", "TD": "Chad", "TG": "Togo", "TH": "Thailand",
    "TJ": "Tajikistan", "TL": "Timor-Leste", "TM": "Turkmenistan",
    "TN": "Tunisia", "TO": "Tonga", "TR": "Turkey", "TT": "Trinidad and Tobago",
    "TV": "Tuvalu", "TZ": "Tanzania", "UA": "Ukraine", "UG": "Uganda",
    "US": "United States", "UY": "Uruguay", "UZ": "Uzbekistan",
    "VA": "Vatican City", "VC": "Saint Vincent and the Grenadines",
    "VE": "Venezuela", "VN": "Vietnam", "VU": "Vanuatu", "WS": "Samoa",
    "YE": "Yemen", "ZA": "South Africa", "ZM": "Zambia", "ZW": "Zimbabwe",
}


def get_country_distribution(user_media):
    """Get media count and sample titles by country name for each media type.

    Reads the ISO 3166-1 alpha-2 code from Media.country (the field on each
    concrete media model row) and resolves it to a human-readable country name.
    Returns:
        { media_type: { "United States": {"count": 5, "titles": [...]}, ... }, ... }
    Titles are capped per country (see _MAX_COUNTRY_TITLES) so the page's
    embedded JSON doesn't blow up for countries with huge libraries -- the
    map tooltip shows a "+N more" suffix using the real count instead.
    """
    country_data_by_type = {}

    for media_type, media_list in user_media.items():
        country_entries = defaultdict(lambda: {"count": 0, "titles": []})

        for media in media_list:
            code = (
                getattr(media, "country", None)
                or getattr(media.item, "country", None)
                or ""
            ).strip().upper()
            if not code or len(code) != 2:
                continue
            name = _ISO_TO_NAME.get(code, code)
            entry = country_entries[name]
            entry["count"] += 1
            if len(entry["titles"]) < _MAX_COUNTRY_TITLES:
                entry["titles"].append(str(media.item))

        if country_entries:
            country_data_by_type[media_type] = dict(
                sorted(
                    country_entries.items(),
                    key=lambda x: x[1]["count"],
                    reverse=True,
                ),
            )

    return country_data_by_type


def get_progress_distribution(user_media):
    """Get distribution of media by completion percentage."""
    progress_buckets = {
        "Not Started": 0,
        "1-25%": 0,
        "26-50%": 0,
        "51-75%": 0,
        "76-99%": 0,
        "100%": 0,
    }

    for media_type, media_list in user_media.items():
        for media in media_list:
            max_progress = getattr(media, "max_progress", None)
            progress = getattr(media, "progress", 0) or 0

            if max_progress and max_progress > 0:
                percentage = (progress / max_progress) * 100
            elif progress > 0:
                percentage = 100
            else:
                percentage = 0

            if percentage == 0:
                progress_buckets["Not Started"] += 1
            elif percentage < 26:
                progress_buckets["1-25%"] += 1
            elif percentage < 51:
                progress_buckets["26-50%"] += 1
            elif percentage < 76:
                progress_buckets["51-75%"] += 1
            elif percentage < 100:
                progress_buckets["76-99%"] += 1
            else:
                progress_buckets["100%"] += 1

    return progress_buckets


def get_media_by_type_country_data(user_media):
    """Format country data per media type for world map display.

    Returns the same shape as get_country_distribution — kept as a separate
    function so the view can pass both independently to the template.
    """
    return get_country_distribution(user_media)


# ── Genre / People / Time chart helpers ──────────────────────────────────────

_GENRE_MEDIA_TYPES = frozenset({
    "movie", "tv", "anime", "manga", "game", "book", "music", "comic",
})


def get_genre_distribution(user_media):
    """Return genre counts and average score per media type using only cached metadata.

    Items whose metadata isn't already cached are silently skipped — no live
    API calls are made from the statistics page. Average score per genre only
    counts media the user has actually scored; unscored items still count
    toward the vote total but are excluded from the average.
    """
    genre_data = {}

    for media_type, media_list in user_media.items():
        if media_type not in _GENRE_MEDIA_TYPES:
            continue

        genre_counts: dict[str, int] = defaultdict(int)
        genre_score_sum: dict[str, Decimal] = defaultdict(Decimal)
        genre_score_count: dict[str, int] = defaultdict(int)

        for media in media_list:
            cache_key = f"{media.item.source}_{media.item.media_type}_{media.item.media_id}"
            metadata = cache.get(cache_key)
            if metadata is None:
                continue

            for genre in (metadata.get("genres") or []):
                if not genre:
                    continue
                genre_str = str(genre)
                genre_counts[genre_str] += 1
                if media.score is not None:
                    genre_score_sum[genre_str] += media.score
                    genre_score_count[genre_str] += 1

        if not genre_counts:
            continue

        sorted_genres = sorted(genre_counts.items(), key=lambda x: (-x[1], x[0]))[:15]
        max_count = sorted_genres[0][1] if sorted_genres else 1

        entries = []
        for name, count in sorted_genres:
            average_score = (
                round(genre_score_sum[name] / genre_score_count[name], 2)
                if genre_score_count[name]
                else None
            )
            avg_bar_pct = (
                max(round(float(average_score) / 10 * 100), 2)
                if average_score is not None
                else 0
            )
            entries.append(
                {
                    "name": name,
                    "count": count,
                    "bar_pct": max(round(count / max_count * 100), 2),
                    "average_score": average_score,
                    "avg_bar_pct": avg_bar_pct,
                },
            )

        genre_data[media_type] = {
            "label": app_tags.media_type_readable(media_type),
            "color": config.get_stats_color(media_type),
            "entries": entries,
        }

    return genre_data


def get_people_stats(user_media):
    """Return top directors, actors, and artists using only cached provider metadata.

    Items whose metadata isn't already cached are silently skipped — no live
    API calls are made from the statistics page.
    """
    directors: dict = {}
    actors: dict = {}
    artists: dict = {}

    for media in user_media.get("movie", []):
        cache_key = f"{media.item.source}_{media.item.media_type}_{media.item.media_id}"
        metadata = cache.get(cache_key)
        if metadata is None:
            continue

        for person in metadata.get("directors", []):
            pid = person.get("id")
            if not pid:
                continue
            entry = directors.setdefault(
                pid,
                {"id": pid, "name": person["name"], "image": person.get("image"), "count": 0},
            )
            entry["count"] += 1

        for person in metadata.get("cast", []):
            pid = person.get("id")
            if not pid:
                continue
            entry = actors.setdefault(
                pid,
                {"id": pid, "name": person["name"], "image": person.get("image"), "count": 0},
            )
            entry["count"] += 1

    for media in user_media.get("music", []):
        cache_key = f"{media.item.source}_{media.item.media_type}_{media.item.media_id}"
        metadata = cache.get(cache_key)
        if metadata is None:
            continue

        for artist in metadata.get("artist_links", []):
            aid = artist.get("id")
            if not aid:
                continue
            entry = artists.setdefault(
                aid,
                {"id": aid, "name": artist["name"], "image": None, "count": 0},
            )
            entry["count"] += 1

    top_n = 10
    return {
        "directors": sorted(directors.values(), key=lambda x: (-x["count"], x["name"]))[:top_n],
        "actors": sorted(actors.values(), key=lambda x: (-x["count"], x["name"]))[:top_n],
        "artists": sorted(artists.values(), key=lambda x: (-x["count"], x["name"]))[:top_n],
    }


def get_year_chart_data(year_rows):
    """Format yearly activity for a grouped Chart.js bar chart."""
    if not year_rows:
        return None
    sorted_rows = sorted(year_rows, key=lambda r: r["year"])
    return {
        "labels": [str(r["year"]) for r in sorted_rows],
        "datasets": [
            {
                "label": "Completed",
                "data": [r["completed"] for r in sorted_rows],
                "background_color": "rgba(99, 102, 241, 0.85)",
            },
            {
                "label": "Started",
                "data": [r["started"] for r in sorted_rows],
                "background_color": "rgba(52, 211, 153, 0.85)",
            },
        ],
    }


def get_decade_chart_data(year_rows):
    """Aggregate yearly activity into decades for a Chart.js bar chart."""
    if not year_rows:
        return None

    buckets: dict[int, dict] = {}
    for row in year_rows:
        decade = (row["year"] // 10) * 10
        b = buckets.setdefault(decade, {"started": 0, "completed": 0})
        b["started"] += row["started"]
        b["completed"] += row["completed"]

    sorted_decades = sorted(buckets.items())
    return {
        "labels": [f"{d}s" for d, _ in sorted_decades],
        "datasets": [
            {
                "label": "Completed",
                "data": [v["completed"] for _, v in sorted_decades],
                "background_color": "rgba(99, 102, 241, 0.85)",
            },
            {
                "label": "Started",
                "data": [v["started"] for _, v in sorted_decades],
                "background_color": "rgba(52, 211, 153, 0.85)",
            },
        ],
    }


_RELEASE_YEAR_SKIP = frozenset({"season", "episode"})


def get_release_year_distribution(user_media: dict) -> "dict[int, int]":
    """Count tracked media items by their release year.

    Reads Item.release_year first (denormalized at save/sync time, so this
    never depends on the metadata cache being warm). For any item where
    it isn't set yet -- tracked before this field existed and not yet
    covered by the backfill task -- falls back to cached provider metadata
    so accuracy doesn't regress while the backfill runs.

    TV seasons and episodes are skipped — the parent TV show already covers them.
    Returns a {year: count} mapping.
    """
    year_counts: dict = defaultdict(int)

    for media_type, media_list in user_media.items():
        if media_type in _RELEASE_YEAR_SKIP:
            continue
        for media in media_list:
            year = media.item.release_year
            if year is None:
                cache_key = (
                    f"{media.item.source}_{media.item.media_type}_{media.item.media_id}"
                )
                metadata = cache.get(cache_key)
                if metadata is not None:
                    year = get_release_year_from_metadata(metadata)
            if year is not None:
                year_counts[year] += 1

    return dict(year_counts)


def get_release_year_chart_data(year_dist: "dict[int, int]") -> "dict | None":
    """Format the release year distribution for a Chart.js bar chart."""
    if not year_dist:
        return None

    min_year = min(year_dist)
    max_year = max(year_dist)
    all_years = list(range(min_year, max_year + 1))
    data = [year_dist.get(y, 0) for y in all_years]

    return {
        "labels": [str(y) for y in all_years],
        "datasets": [
            {
                "label": "Items",
                "data": data,
                "background_color": "rgba(99, 102, 241, 0.85)",
            }
        ],
    }


def get_release_decade_chart_data(year_dist: "dict[int, int]") -> "dict | None":
    """Aggregate the release year distribution into decades for a Chart.js bar chart."""
    if not year_dist:
        return None

    buckets: dict = defaultdict(int)
    for year, count in year_dist.items():
        decade = (year // 10) * 10
        buckets[decade] += count

    sorted_decades = sorted(buckets.items())
    return {
        "labels": [f"{d}s" for d, _ in sorted_decades],
        "datasets": [
            {
                "label": "Items",
                "data": [count for _, count in sorted_decades],
                "background_color": "rgba(99, 102, 241, 0.85)",
            }
        ],
    }


_PERSONAL_BEST_SKIP = frozenset({"season", "episode"})


def get_personal_best(user_media: dict) -> dict:
    """Return the user's rated items per media type, grouped by release year and decade.

    Grouping key is the item's *release* year (Item.release_year, falling back
    to cached provider metadata -- same lookup strategy as
    get_release_year_distribution), never the consumption/tracked date. Only
    scored items are eligible, since "personal best" is meaningless without a
    rating. TV seasons and episodes are skipped -- the parent TV show already
    represents them.

    Buckets are returned as flat, pre-sorted lists (rather than nested dicts)
    so the template can iterate them directly without needing a dynamic
    dict-by-key lookup filter.

    Returns:
        {
            "year_periods": [
                {
                    "period": year,
                    "groups": [{"media_type": ..., "label": ..., "media_list": [...]}, ...],
                },
                ...
            ],  # sorted by year desc
            "decade_periods": [ ... same shape, "period" is the decade start year ... ],
            "media_types": [(media_type, label), ...] present across any bucket,
        }
    """
    year_buckets: dict[int, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    decade_buckets: dict[int, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    media_types_seen: set[str] = set()

    for media_type, media_list in user_media.items():
        if media_type in _PERSONAL_BEST_SKIP:
            continue

        for media in media_list:
            if media.score is None:
                continue

            year = media.item.release_year
            if year is None:
                cache_key = (
                    f"{media.item.source}_{media.item.media_type}_{media.item.media_id}"
                )
                metadata = cache.get(cache_key)
                if metadata is not None:
                    year = get_release_year_from_metadata(metadata)
            if year is None:
                continue

            decade = (year // 10) * 10
            year_buckets[year][media_type].append(media)
            decade_buckets[decade][media_type].append(media)
            media_types_seen.add(media_type)

    def _build_periods(buckets):
        periods = []
        for period in sorted(buckets.keys(), reverse=True):
            by_type = buckets[period]
            groups = []
            for media_type in sorted(by_type.keys(), key=app_tags.media_type_readable):
                items = sorted(
                    by_type[media_type],
                    key=lambda m: (-float(m.score), str(m.item)),
                )
                groups.append({
                    "media_type": media_type,
                    "label": app_tags.media_type_readable(media_type),
                    "media_list": items,
                })
            periods.append({"period": period, "groups": groups})
        return periods

    year_periods = _build_periods(year_buckets)
    decade_periods = _build_periods(decade_buckets)

    media_types = sorted(
        ((mt, app_tags.media_type_readable(mt)) for mt in media_types_seen),
        key=lambda x: x[1],
    )

    return {
        "year_periods": year_periods,
        "decade_periods": decade_periods,
        "media_types": media_types,
    }


# SVG donut constants (r=40 circle, full 360°)
_DONUT_R = 40
_DONUT_CIRCUMFERENCE = round(2 * math.pi * _DONUT_R, 2)  # ≈ 251.33


def get_awards_progress(user):
    """Return per-user tracking progress for each configured award category.

    Returns a list of dicts, each containing: name, icon, tracked, total,
    percentage, dash_offset.
    """
    from app.awards_data import AWARDS  # noqa: PLC0415

    result = []
    for award in AWARDS:
        source = award["source"]
        media_type = award["media_type"]
        id_key = f"{source}_id"
        winner_ids = {str(w[id_key]) for w in award["winners"] if w.get(id_key)}
        total = len(winner_ids)

        if not total:
            continue

        try:
            model = apps.get_model("app", media_type)
        except LookupError:
            continue

        tracked = (
            model.objects.filter(
                user=user,
                item__source=source,
                item__media_type=media_type,
                item__media_id__in=winner_ids,
            )
            .values("item__media_id")
            .distinct()
            .count()
        )

        pct = round(tracked / total * 100) if total else 0
        offset = round(_DONUT_CIRCUMFERENCE * (1 - pct / 100), 2)

        result.append({
            "slug": award["slug"],
            "name": award["name"],
            "icon": award["icon"],
            "tracked": tracked,
            "total": total,
            "percentage": pct,
            "dash_offset": offset,
        })

    return result


def get_award_winners_detail(user, award_slug):
    """Return the full per-winner breakdown for one award category.

    Used by the awards-progress "open on click" dropdown. Title lookups
    never hit a live provider API (matching the no-live-calls-from-stats
    rule): a winner's title comes from the shared Item row if anyone has
    ever tracked it, then falls back to cached provider metadata, then to
    a generic placeholder if neither is available.

    Returns None if the slug doesn't match a configured award.
    """
    from app.awards_data import AWARDS  # noqa: PLC0415

    award = next((a for a in AWARDS if a["slug"] == award_slug), None)
    if award is None:
        return None

    source = award["source"]
    media_type = award["media_type"]
    id_key = f"{source}_id"

    try:
        model = apps.get_model("app", media_type)
    except LookupError:
        return None

    winners = []
    seen_ids = set()
    for winner in award["winners"]:
        media_id = winner.get(id_key)
        if not media_id or str(media_id) in seen_ids:
            continue
        seen_ids.add(str(media_id))
        winners.append({"media_id": str(media_id), "year": winner.get("year")})

    media_ids = [w["media_id"] for w in winners]

    # Item rows are shared across users -- if anyone has ever tracked a
    # winner its title/image is already here, no cache or API call needed.
    items_by_media_id = {
        item.media_id: item
        for item in Item.objects.filter(
            source=source,
            media_type=media_type,
            media_id__in=media_ids,
        )
    }

    # Which of those winners does *this* user actually track?
    tracked_media_ids = set(
        model.objects.filter(
            user=user,
            item__source=source,
            item__media_type=media_type,
            item__media_id__in=media_ids,
        ).values_list("item__media_id", flat=True),
    )

    entries = []
    for winner in winners:
        media_id = winner["media_id"]
        item = items_by_media_id.get(media_id)

        if item is not None:
            title = item.title
        else:
            cache_key = f"{source}_{media_type}_{media_id}"
            metadata = cache.get(cache_key)
            title = metadata["title"] if metadata else f"Unknown title (ID {media_id})"

        entries.append({
            "media_id": media_id,
            "year": winner["year"],
            "title": title,
            "tracked": media_id in tracked_media_ids,
            "link": reverse(
                "media_details",
                kwargs={
                    "source": source,
                    "media_type": media_type,
                    "media_id": media_id,
                    "title": app_tags.slug(title),
                },
            ),
        })

    entries.sort(key=lambda e: e["year"] or 0, reverse=True)

    return {
        "slug": award_slug,
        "name": award["name"],
        "icon": award["icon"],
        "entries": entries,
        "tracked_count": sum(1 for e in entries if e["tracked"]),
        "total_count": len(entries),
    }


def get_list_progress(user):
    """Return per-user tracking progress for each configured curated list.

    Mirrors get_awards_progress -- reads the static LISTS fixture instead
    of a synced DB table. Returns a list of dicts, each containing: slug,
    name, icon, tracked, total, percentage, dash_offset.
    """
    from app.external_lists_data import LISTS  # noqa: PLC0415

    result = []
    for curated_list in LISTS:
        source = curated_list["source"]
        media_type = curated_list["media_type"]
        id_key = f"{source}_id"
        item_ids = {str(i[id_key]) for i in curated_list["items"] if i.get(id_key)}
        total = len(item_ids)

        if not total:
            continue

        try:
            model = apps.get_model("app", media_type)
        except LookupError:
            continue

        tracked = (
            model.objects.filter(
                user=user,
                item__source=source,
                item__media_type=media_type,
                item__media_id__in=item_ids,
            )
            .values("item__media_id")
            .distinct()
            .count()
        )

        pct = round(tracked / total * 100) if total else 0
        offset = round(_DONUT_CIRCUMFERENCE * (1 - pct / 100), 2)

        result.append({
            "slug": curated_list["slug"],
            "name": curated_list["name"],
            "icon": curated_list["icon"],
            "tracked": tracked,
            "total": total,
            "percentage": pct,
            "dash_offset": offset,
        })

    return result


def get_list_winners_detail(user, list_slug):
    """Return the full per-entry breakdown for one curated list.

    Used by the list-progress "open on click" dropdown. Same lookup
    strategy as get_award_winners_detail: no live provider API calls,
    title comes from the shared Item row, then cached provider metadata,
    then a placeholder.

    Returns None if the slug doesn't match a configured list.
    """
    from app.external_lists_data import LISTS  # noqa: PLC0415

    curated_list = next((lst for lst in LISTS if lst["slug"] == list_slug), None)
    if curated_list is None:
        return None

    source = curated_list["source"]
    media_type = curated_list["media_type"]
    id_key = f"{source}_id"

    try:
        model = apps.get_model("app", media_type)
    except LookupError:
        return None

    entries_cfg = []
    seen_ids = set()
    for entry in curated_list["items"]:
        media_id = entry.get(id_key)
        if not media_id or str(media_id) in seen_ids:
            continue
        seen_ids.add(str(media_id))
        entries_cfg.append({"media_id": str(media_id), "rank": entry.get("rank")})

    media_ids = [e["media_id"] for e in entries_cfg]

    items_by_media_id = {
        item.media_id: item
        for item in Item.objects.filter(
            source=source,
            media_type=media_type,
            media_id__in=media_ids,
        )
    }

    tracked_media_ids = set(
        model.objects.filter(
            user=user,
            item__source=source,
            item__media_type=media_type,
            item__media_id__in=media_ids,
        ).values_list("item__media_id", flat=True),
    )

    entries = []
    for entry in entries_cfg:
        media_id = entry["media_id"]
        item = items_by_media_id.get(media_id)

        if item is not None:
            title = item.title
        else:
            cache_key = f"{source}_{media_type}_{media_id}"
            metadata = cache.get(cache_key)
            title = metadata["title"] if metadata else f"Unknown title (ID {media_id})"

        entries.append({
            "media_id": media_id,
            "rank": entry["rank"],
            "title": title,
            "tracked": media_id in tracked_media_ids,
            "link": reverse(
                "media_details",
                kwargs={
                    "source": source,
                    "media_type": media_type,
                    "media_id": media_id,
                    "title": app_tags.slug(title),
                },
            ),
        })

    entries.sort(key=lambda e: e["rank"] or 0)

    return {
        "slug": list_slug,
        "name": curated_list["name"],
        "icon": curated_list["icon"],
        "entries": entries,
        "tracked_count": sum(1 for e in entries if e["tracked"]),
        "total_count": len(entries),
    }
