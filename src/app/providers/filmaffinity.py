"""
FilmAffinity scraper for Yamtrack.
Scrapes public user ratings from filmaffinity.com/en/userratings.php?user_id=XXXXX

No official API exists. Uses BeautifulSoup (already a Yamtrack dependency).
"""

import logging
import time

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

FA_BASE = "https://www.filmaffinity.com"
FA_RATINGS_URL = FA_BASE + "/en/userratings.php"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# FA type strings → Yamtrack media types
FA_TYPE_MAP = {
    "movie": "movie",
    "tvshow": "tv",
    "tvseries": "tv",
    "tv series": "tv",
    "tv show": "tv",
    "miniseries": "tv",
    "short film": "movie",
    "documentary": "movie",
    "animation": "movie",
}


def scrape_user_ratings(user_id: str) -> list[dict]:
    """
    Scrape all rated items from a public FilmAffinity profile.
    Returns list of normalized dicts.
    """
    all_items = []
    page = 1

    while True:
        url = f"{FA_RATINGS_URL}?user_id={user_id}&p={page}&orderby=4"
        logger.info("FA scrape: fetching page %d for user %s", page, user_id)

        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            logger.error("FA scrape error on page %d: %s", page, e)
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        items = _parse_page(soup)

        if not items:
            break

        all_items.extend(items)

        # Check if there's a next page
        next_link = soup.select_one("a.next-page, .pagination .next, a[rel='next']")
        if not next_link:
            # Also check by counting: FA shows 30 items per page
            if len(items) < 30:
                break

        page += 1
        time.sleep(0.5)  # Be polite

    logger.info("FA scrape: total %d items for user %s", len(all_items), user_id)
    return all_items


def _parse_page(soup: BeautifulSoup) -> list[dict]:
    """Parse a single ratings page and return list of item dicts."""
    items = []

    # FA uses different selectors depending on version
    # Try multiple selectors for robustness
    movie_cells = (
        soup.select("div.user-ratings-movie")
        or soup.select("div.movie-card")
        or soup.select("li[class*='movie']")
        or soup.select("div[class*='movie-item']")
    )

    if not movie_cells:
        # Fallback: look for the ratings table structure
        movie_cells = soup.select("div.fa-film")

    for cell in movie_cells:
        item = _parse_cell(cell)
        if item:
            items.append(item)

    return items


def _parse_cell(cell) -> dict | None:
    """Parse a single movie/show cell from the ratings page."""
    try:
        # Title
        title_el = (
            cell.select_one("div.mc-title a")
            or cell.select_one("a.mc-title")
            or cell.select_one("[class*='title'] a")
            or cell.select_one("a[href*='/film']")
        )
        if not title_el:
            return None
        title = title_el.get_text(strip=True)

        # FA film ID from URL
        href = title_el.get("href", "")
        fa_id = None
        if "/film" in href:
            import re
            match = re.search(r"/film(\d+)\.html", href)
            if match:
                fa_id = match.group(1)

        # Year
        year_el = (
            cell.select_one("div.mc-title span.year")
            or cell.select_one("span.mc-year")
            or cell.select_one("[class*='year']")
        )
        year = None
        if year_el:
            import re
            year_match = re.search(r"\d{4}", year_el.get_text())
            if year_match:
                year = int(year_match.group())

        # Rating (user's own rating)
        rating_el = (
            cell.select_one("div.ur-interest-rating")
            or cell.select_one("[class*='user-rating']")
            or cell.select_one("[class*='ur-interest']")
        )
        score = None
        if rating_el:
            import re
            rating_text = rating_el.get_text(strip=True)
            rating_match = re.search(r"\d+", rating_text)
            if rating_match:
                score = int(rating_match.group())
        
        # Also try image-based rating (older FA format)
        if score is None:
            rating_img = cell.select_one("img[src*='myratings']")
            if rating_img:
                import re
                src = rating_img.get("src", "")
                match = re.search(r"myratings/(\d+)_", src)
                if match:
                    score = int(match.group(1))

        # Media type — FA marks TV content in title or has a type indicator
        media_type = _detect_media_type(cell, title)

        # Poster
        poster_el = cell.select_one("img[src*='filmaffinity']") or cell.select_one("div.mc-poster img")
        poster = poster_el.get("src", "") if poster_el else ""

        return {
            "fa_id": fa_id,
            "title": title,
            "year": year,
            "score": score,
            "media_type": media_type,
            "poster": poster,
        }

    except Exception as e:
        logger.debug("FA parse error on cell: %s", e)
        return None


def _detect_media_type(cell, title: str) -> str:
    """Detect whether this is a movie or TV show."""
    # Check for type indicators in the cell
    type_el = cell.select_one("[class*='mc-type'], [class*='entity-type']")
    if type_el:
        type_text = type_el.get_text(strip=True).lower()
        for key, value in FA_TYPE_MAP.items():
            if key in type_text:
                return value

    # FA marks TV series with "(TV Series)" or "(Mini-Series)" in title area
    title_lower = title.lower()
    full_text = cell.get_text().lower()

    if any(marker in full_text for marker in ["tv series", "tv show", "miniseries", "mini-series", "(serie"]):
        return "tv"

    return "movie"
