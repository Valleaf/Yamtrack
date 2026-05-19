import calendar
import datetime
import heapq
import itertools
import logging
from collections import defaultdict
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.db import models
from django.db.models import (
    Prefetch,
    Q,
)
from django.utils import timezone

from app import config
from app.models import (
    TV,
    BasicMedia,
    Episode,
    MediaManager,
    MediaTypes,
    Season,
    Sources,
    Status,
)
from app.templatetags import app_tags

logger = logging.getLogger(__name__)


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
            # No date filtering for "All Time"
            base_episodes = Episode.objects.filter(
                related_season__user=user,
            )
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
                "related_season__related_tv",
                flat=True,
            ).distinct()
            queryset = TV.objects.filter(id__in=tv_ids).prefetch_related(
                Prefetch(
                    "seasons",
                    queryset=Season.objects.select_related(
                        "item",
                    ).prefetch_related(
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
                "related_season",
                flat=True,
            ).distinct()
            queryset = Season.objects.filter(
                id__in=season_ids,
            ).prefetch_related(
                Prefetch("episodes", queryset=base_episodes),
            )
        # For other models, apply date filtering conditionally
        elif start_date is None and end_date is None:
            # No date filtering for "All Time"
            queryset = model.objects.filter(user=user)
        else:
            queryset = model.objects.filter(user=user).filter(
                # Case 1: Media has both start_date and end_date
                # Include if ranges overlap
                # (exclude if media ends before filter start or starts after filter end)
                (
                    Q(start_date__isnull=False)
                    & Q(end_date__isnull=False)
                    & ~(Q(end_date__lt=start_date) | Q(start_date__gt=end_date))
                )
                |
                # Case 2: Media only has start_date (end_date is null)
                # Include if start_date is within filter range
                (
                    Q(start_date__isnull=False)
                    & Q(end_date__isnull=True)
                    & Q(start_date__gte=start_date)
                    & Q(start_date__lte=end_date)
                )
                |
                # Case 3: Media only has end_date (start_date is null)
                # Include if end_date is within filter range
                (
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
    # Define colors for each media type
    # Format for Chart.js
    chart_data = {
        "labels": [],
        "datasets": [
            {
                "data": [],
                "backgroundColor": [],
            },
        ],
    }

    # Only include media types with counts > 0
    for media_type, count in media_count.items():
        if media_type != "total" and count > 0:
            # Format label with first letter capitalized
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
    # Define status order to ensure consistent stacking
    status_order = list(Status.values)
    for media_type, media_list in user_media.items():
        status_counts = dict.fromkeys(status_order, 0)
        counts = media_list.values("status").annotate(count=models.Count("id"))
        for count_data in counts:
            status_counts[count_data["status"]] = count_data["count"]
            if count_data["status"] == Status.COMPLETED.value:
                total_completed += count_data["count"]

        distribution[media_type] = status_counts

    # Format the response for charting
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
    # Format for Chart.js pie chart
    chart_data = {
        "labels": [],
        "datasets": [
            {
                "data": [],
                "backgroundColor": [],
            },
        ],
    }

    # Process each status dataset
    for dataset in status_distribution["datasets"]:
        status_label = dataset["label"]
        status_count = dataset["total"]
        status_color = dataset["background_color"]

        # Only include statuses with counts > 0
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
        score: {"score": score, "count": 0, "percentage": 0}
        for score in range(10, -1, -1)
    }
    rating_bands = [
        {"label": "Favorites", "range": "8-10", "min": 8, "max": 10, "count": 0},
        {"label": "Positive", "range": "6-7", "min": 6, "max": 7, "count": 0},
        {"label": "Mixed", "range": "4-5", "min": 4, "max": 5, "count": 0},
        {"label": "Low", "range": "0-3", "min": 0, "max": 3, "count": 0},
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
                "completion_percentage": round(completed / total * 100)
                if total
                else 0,
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

    for bucket in score_buckets.values():
        if scored_items:
            bucket["percentage"] = round(bucket["count"] / scored_items * 100)

    for band in rating_bands:
        if scored_items:
            band["percentage"] = round(band["count"] / scored_items * 100)
        else:
            band["percentage"] = 0

    source_rows = []
    for stats in source_stats.values():
        if stats["scored"]:
            stats["average_score"] = round(stats["score_sum"] / stats["scored"], 2)
        if total_items:
            stats["percentage"] = round(stats["count"] / total_items * 100)
        source_rows.append(stats)

    source_rows.sort(key=lambda row: (-row["count"], row["source"]))
    media_type_rows.sort(key=lambda row: (-row["total"], row["label"]))
    year_rows = sorted(
        year_stats.values(),
        key=lambda row: row["year"],
        reverse=True,
    )

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

    year = timezone.localdate(media_date).year
    year_stats.setdefault(
        year,
        {
            "year": year,
            "started": 0,
            "completed": 0,
        },
    )
    year_stats[year][counter_key] += 1


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
    counter = itertools.count()  # Ensures stable sorting for equal scores
    score_range = range(11)

    for media_type, media_list in user_media.items():
        score_counts = dict.fromkeys(score_range, 0)
        scored_media = media_list.exclude(score__isnull=True).select_related("item")

        for media in scored_media:
            if len(top_rated) < top_rated_count:
                heapq.heappush(
                    top_rated,
                    (float(media.score), next(counter), media),
                )
            else:
                heapq.heappushpop(
                    top_rated,
                    (float(media.score), next(counter), media),
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

    # Group by media type to batch database operations
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

        # Fetch fresh instances with proper relationships and annotations
        queryset = model.objects.filter(id__in=media_ids)
        queryset = media_manager._apply_prefetch_related(queryset, media_type)
        media_manager.annotate_max_progress(queryset, media_type)

        prefetched_media_map = {media.id: media for media in queryset}

        # Replace original instances with enhanced ones
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

    # Process each media type
    for media_type, queryset in user_media.items():
        if media_type == MediaTypes.TV.value:
            continue
        for media in queryset:
            local_start_date = timezone.localdate(media.start_date)
            local_end_date = timezone.localdate(media.end_date)

            if media.start_date and media.end_date:
                # add media to all months between start and end
                current_date = local_start_date
                while current_date <= local_end_date:
                    year = current_date.year
                    month = current_date.month
                    month_name = calendar.month_name[month]
                    month_year = f"{month_name} {year}"

                    timeline[month_year].append(media)

                    # Move to next month
                    current_date += relativedelta(months=1)
                    current_date = current_date.replace(day=1)
            elif media.start_date:
                # If only start date, add to the start month
                year = local_start_date.year
                month = local_start_date.month
                month_name = calendar.month_name[month]
                month_year = f"{month_name} {year}"

                timeline[month_year].append(media)
            elif media.end_date:
                # If only end date, add to the end month
                year = local_end_date.year
                month = local_end_date.month
                month_name = calendar.month_name[month]
                month_year = f"{month_name} {year}"

                timeline[month_year].append(media)

    # Convert to sorted dictionary with media sorted by start date
    # Create a list sorted by year and month in reverse order
    sorted_items = []
    for month_year, media_list in timeline.items():
        month_name, year_str = month_year.split()
        year = int(year_str)
        month = list(calendar.month_name).index(month_name)
        sorted_items.append((month_year, media_list, year, month))

    # Sort by year and month in reverse chronological order
    sorted_items.sort(key=lambda x: (x[2], x[3]), reverse=True)

    # Create the final result dictionary
    result = {}
    for month_year, media_list, _, _ in sorted_items:
        # Sort the media list using our custom sort key
        result[month_year] = sorted(media_list, key=time_line_sort_key, reverse=True)
    return result


def time_line_sort_key(media):
    """Sort media items in the timeline."""
    if media.end_date is not None:
        return timezone.localdate(media.end_date)
    return timezone.localdate(media.start_date)


def get_activity_data(user, start_date, end_date):
    """Get daily activity counts for the last year."""
    if end_date is None:
        end_date = timezone.localtime()

    start_date_aligned = get_aligned_monday(start_date)

    combined_data = get_filtered_historical_data(start_date_aligned, end_date, user)

    # update start_date values from historical records if not provided
    if start_date is None:
        dates = [item["date"] for item in combined_data]
        start_date = datetime.datetime.combine(
            min(dates) if dates else timezone.localdate(),
            datetime.time.min,
        )
        start_date_aligned = get_aligned_monday(start_date)

    # Aggregate counts by date
    date_counts = {}
    for item in combined_data:
        date = item["date"]
        date_counts[date] = date_counts.get(date, 0) + item["count"]

    date_range = [
        start_date_aligned.date() + datetime.timedelta(days=x)
        for x in range((end_date.date() - start_date_aligned.date()).days + 1)
    ]

    # Calculate activity statistics
    most_active_day, day_percentage = calculate_day_of_week_stats(
        date_counts,
        start_date.date(),
    )
    current_streak, longest_streak = calculate_streaks(
        date_counts,
        end_date.date(),
    )

    # Create complete date range including padding days
    activity_data = [
        {
            "date": current_date.strftime("%Y-%m-%d"),
            "count": date_counts.get(current_date, 0),
            "level": get_level(date_counts.get(current_date, 0)),
        }
        for current_date in date_range
    ]

    # Format data into calendar weeks
    calendar_weeks = [activity_data[i : i + 7] for i in range(0, len(activity_data), 7)]

    # Generate months list with their Monday counts
    months = []
    mondays_per_month = []
    current_month = date_range[0].strftime("%b")
    monday_count = 0

    for current_date in date_range:
        if current_date.weekday() == 0:  # Monday
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
    # For the last month
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

    days_to_subtract = datetime_obj.weekday()  # 0=Monday, 6=Sunday
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

        # We only need the timestamp, stream results to keep memory usage flat
        for ts in qs.values_list("history_date", flat=True).iterator(chunk_size=2_000):
            aware_ts = timezone.localtime(ts, local_tz)

            day_buckets[aware_ts.date()] += 1

    combined_data = [
        {"date": day, "count": count} for day, count in day_buckets.items()
    ]

    logger.info("%s - built historical data (%s rows)", user, len(combined_data))
    return combined_data


def calculate_day_of_week_stats(date_counts, start_date):
    """Calculate the most active day of the week based on activity frequency.

    Returns the day name and its percentage of total activity.
    """
    # Initialize counters for each day of the week
    day_counts = defaultdict(int)
    total_active_days = 0

    # Count occurrences of each day of the week where activity happened
    for date in date_counts:
        if date < start_date:
            continue
        if date_counts[date] > 0:
            day_name = date.strftime("%A")  # Get full day name
            day_counts[day_name] += 1
            total_active_days += 1

    if not total_active_days:
        return None, 0

    # Find the most active day
    most_active_day = max(day_counts.items(), key=lambda x: x[1])
    percentage = (most_active_day[1] / total_active_days) * 100

    return most_active_day[0], round(percentage)


def calculate_streaks(date_counts, end_date):
    """Calculate current and longest activity streaks."""
    # Get active dates and sort them in descending order (newest first)
    active_dates = sorted(
        [date for date, count in date_counts.items() if count > 0],
        reverse=True,
    )

    if not active_dates:
        return 0, 0

    longest_streak = 1
    streak_count = 1

    # Check if the most recent active date is today/end_date
    is_current = active_dates[0] == end_date

    current_streak = 1 if is_current else 0

    for i in range(1, len(active_dates)):
        # Check if this date is consecutive with the previous one
        if (active_dates[i - 1] - active_dates[i]).days == 1:
            streak_count += 1

            if is_current:
                current_streak += 1
        else:
            longest_streak = max(longest_streak, streak_count)
            streak_count = 1

            if is_current:
                is_current = False

    # Check final streak for longest calculation
    # needed if the last date is today/end_date
    longest_streak = max(longest_streak, streak_count)

    return current_streak, longest_streak


def get_country_distribution(user_media):
    """Get media count by country for each media type.
    
    Currently uses sample data demonstrating the structure.
    When country metadata is cached from providers, this will aggregate real country data.
    """
    country_data_by_type = {}
    
    # Sample country mapping for demonstration
    # In production, this would come from cached provider metadata
    country_samples = {
        "movie": {"United States": 45, "Japan": 12, "United Kingdom": 8, "France": 6, "South Korea": 5},
        "tv": {"United States": 38, "Japan": 15, "South Korea": 10, "United Kingdom": 7},
        "anime": {"Japan": 85, "South Korea": 5, "United States": 3},
        "manga": {"Japan": 78, "South Korea": 8, "United States": 4},
        "game": {"United States": 42, "Japan": 28, "Canada": 12, "Germany": 8, "United Kingdom": 6},
        "book": {"United States": 55, "United Kingdom": 20, "Japan": 8, "France": 5, "Germany": 4},
    }
    
    # Try to aggregate real country data if available, otherwise use structure only
    for media_type, media_list in user_media.items():
        country_counts = defaultdict(int)
        total_media = 0
        
        # Try to extract real country data from metadata
        for media in media_list.select_related("item"):
            total_media += 1
            # In future, country would come from cached metadata
            # For now, use sample data if available
            if media_type in country_samples:
                continue
        
        # Use sample data for demonstration if we have it
        if media_type in country_samples and total_media > 0:
            country_data_by_type[media_type] = country_samples[media_type]
    
    return country_data_by_type


def get_source_distribution(user_media):
    """Get distribution of media by source (provider) for each media type."""
    source_data_by_type = defaultdict(lambda: defaultdict(int))
    
    for media_type, media_list in user_media.items():
        for media in media_list.select_related("item"):
            source = media.item.source
            source_label = app_tags.source_readable(source)
            source_data_by_type[media_type][source_label] += 1
    
    return dict(source_data_by_type)


def get_release_year_distribution(user_media):
    """Get distribution of media by release year."""
    year_data = defaultdict(int)
    
    for media_type, media_list in user_media.items():
        for media in media_list.select_related("item"):
            # Try to extract year from metadata if available
            # This would need provider metadata to be cached
            year = getattr(media, "release_year", None)
            if year:
                year_data[year] += 1
    
    return dict(year_data)


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
            # Calculate progress percentage
            max_progress = getattr(media, "max_progress", None)
            progress = getattr(media, "progress", 0)
            
            if max_progress and max_progress > 0:
                percentage = (progress / max_progress) * 100
            elif progress > 0:
                percentage = 100
            else:
                percentage = 0
            
            # Bucket the percentage
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


def get_media_count_by_country(user_media):
    """Get media count per country across all media types.
    
    Note: Country data is not persisted in the database.
    This function provides framework for future enhancement.
    
    Returns dict: { country_code: count, ... }
    """
    # Placeholder for future implementation
    return {}


def get_media_by_type_country_data(user_media):
    """Format country data for world map display per media type.
    
    Note: Country data is not currently stored. This provides the framework
    for future enhancement when provider metadata is cached.
    
    Returns a dict mapping media types to lists of {country, count, percentage}.
    """
    # Placeholder for future implementation when country data is stored
    return {}
