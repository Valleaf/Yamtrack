"""Date parsing and manipulation utilities for media tracking."""

from datetime import date, datetime
from zoneinfo import ZoneInfo

from django.utils import timezone

YEAR_ONLY_PARTS = 1
YEAR_MONTH_PARTS = 2


def parse_date_with_precision(date_value, current_date=None, use_sentinel=False):
    """
    Parse a date value with flexible precision.

    Handles partial dates (e.g., "2024", "2024-01", "2024-01-15") by filling
    missing parts with defaults (month=01, day=01).

    Parameters
    ----------
    date_value : datetime | date | str | None
        The date to parse. Can be:
        - datetime: Converted to date (timezone-aware datetime converted to local date)
        - date: Used directly
        - str: Parsed as YYYY, YYYY-MM, or YYYY-MM-DD format
        - None: Treated as missing/invalid

    current_date : date | None, optional
        The current date for comparisons. Defaults to today's local date if None.

    use_sentinel : bool, optional
        If True, sets time to SentinelDatetime values (for calendar events).
        If False, returns datetime at midnight (default).
        Only applies when returning datetime objects.

    Returns
    -------
    datetime | date | bool
        For use_sentinel=False (default):
        - Returns datetime at midnight UTC if date_value is str
        - Returns date if date_value is date/datetime and used_for_comparison=False
        - Returns bool (True/False) if used for date comparison

        For use_sentinel=True (calendar mode):
        - Returns datetime with SentinelDatetime values set
        - Only valid with str input
    """
    normalized_date = None

    if isinstance(date_value, datetime):
        # Convert datetime to date, respecting timezone
        if timezone.is_naive(date_value):
            normalized_date = date_value.date()
        else:
            normalized_date = timezone.localtime(date_value).date()
    elif isinstance(date_value, date):
        normalized_date = date_value
    elif isinstance(date_value, str):
        # Parse flexible date string format
        parts = date_value.split("-")
        if len(parts) == YEAR_ONLY_PARTS:
            date_value = f"{date_value}-01-01"
        elif len(parts) == YEAR_MONTH_PARTS:
            date_value = f"{date_value}-01"

        try:
            normalized_date = date.fromisoformat(date_value)
        except ValueError:
            return False if use_sentinel is False else None

        # For string input, return datetime with optional sentinel values
        if use_sentinel:
            # Import here to avoid circular dependency
            from events.models import SentinelDatetime

            dt = datetime.strptime(date_value, "%Y-%m-%d").replace(
                tzinfo=ZoneInfo("UTC")
            )
            return dt.replace(
                hour=SentinelDatetime.HOUR,
                minute=SentinelDatetime.MINUTE,
                second=SentinelDatetime.SECOND,
                microsecond=SentinelDatetime.MICROSECOND,
                tzinfo=ZoneInfo("UTC"),
            )
        else:
            return datetime.fromisoformat(date_value).replace(
                tzinfo=ZoneInfo("UTC")
            )
    else:
        return False

    # For datetime/date input, return boolean for comparison
    if not isinstance(date_value, str):
        if current_date is None:
            current_date = timezone.localdate()
        return normalized_date <= current_date

    return normalized_date


def is_released_date(air_date, current_date=None):
    """
    Check if a release date has already passed.

    Convenience wrapper around parse_date_with_precision for release date
    comparisons. Handles partial dates and flexible input types.

    Parameters
    ----------
    air_date : datetime | date | str | None
        The release/air date to check

    current_date : date | None, optional
        Current date for comparison. Defaults to today if None.

    Returns
    -------
    bool
        True if air_date has passed, False otherwise
    """
    return parse_date_with_precision(air_date, current_date, use_sentinel=False)


def parse_calendar_date(date_str):
    """
    Parse calendar event date string with SentinelDatetime values.

    Used by the calendar generation system to parse event dates with
    flexible precision (YYYY, YYYY-MM, or YYYY-MM-DD format).

    Parameters
    ----------
    date_str : str
        Date string in flexible format

    Returns
    -------
    datetime
        Datetime with SentinelDatetime sentinel values set

    Raises
    ------
    ValueError
        If date_str is invalid format
    """
    result = parse_date_with_precision(date_str, use_sentinel=True)
    if result is None:
        raise ValueError(f"Invalid date format: {date_str}")
    return result


# Provider "details" dicts store the release year under different keys
# depending on the source:
#   release_date     - TMDB movie, IGDB game, MusicBrainz album
#   first_air_date   - TMDB tv
#   publish_date     - OpenLibrary book, Hardcover book
#   start_date       - MAL anime/manga, ComicVine issue/volume, BnF comic
#   year / start_year - BGG boardgame (string), MangaUpdates manga (int)
_RELEASE_YEAR_DETAIL_KEYS = (
    "year",
    "start_year",
    "release_date",
    "first_air_date",
    "publish_date",
    "start_date",
)

_MIN_RELEASE_YEAR = 1800
_MAX_RELEASE_YEAR = 2200


def _coerce_release_year(value):
    """Coerce a details value (int year or date-like string) into a plausible year."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        year = value
    elif isinstance(value, str) and len(value) >= 4:
        try:
            year = int(value[:4])
        except ValueError:
            return None
    else:
        return None

    return year if _MIN_RELEASE_YEAR <= year <= _MAX_RELEASE_YEAR else None


def get_release_year_from_metadata(metadata):
    """
    Extract the release year from cached provider metadata.

    Checks every key any provider uses to store a release year/date in the
    metadata "details" dict (see _RELEASE_YEAR_DETAIL_KEYS), so callers don't
    need to know which key a given source uses. Values may be a 4-digit int
    or a date-like string ("YYYY", "YYYY-MM-DD", etc).

    Parameters
    ----------
    metadata : dict
        Cached provider metadata for a media item (must be a dict; its
        "details" key may be missing or empty).

    Returns
    -------
    int | None
        The release year, or None if it can't be determined.
    """
    details = metadata.get("details") or {}
    for key in _RELEASE_YEAR_DETAIL_KEYS:
        year = _coerce_release_year(details.get(key))
        if year is not None:
            return year
    return None
