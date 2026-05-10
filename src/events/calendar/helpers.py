from app.date_utils import parse_calendar_date


def date_parser(date_str):
    """Parse string in %Y-%m-%d to datetime. Raises ValueError if invalid."""
    return parse_calendar_date(date_str)

