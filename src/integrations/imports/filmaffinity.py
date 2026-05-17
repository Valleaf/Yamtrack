"""
Import from FilmAffinity HTML export.

FilmAffinity's data export is a ZIP containing HTML files.
Upload movie-ratings.html for ratings, or any list-N.html for lists.

movie-ratings.html format per row:
    <tr>
        <td><div class="user-rating">8</div></td>
        <td>Film Title (Year)</td>
        <td><em>10 de mayo de 2026, 15:06</em></td>
    </tr>

list-N.html format per row:
    <tr>
        <th>1</th>
        <td>Film Title (Year)</td>
    </tr>

All items from FA are treated as movies and resolved via TMDB.
TV episodes and music videos are resolved as-is (TMDB handles them).
"""

import logging
import re
from collections import defaultdict

from bs4 import BeautifulSoup
from celery import shared_task
from django.apps import apps
from django.contrib.auth import get_user_model

from app.models import Item, MediaTypes, Status
from app.providers import services
from integrations.imports import helpers

logger = logging.getLogger(__name__)
User = get_user_model()

SPANISH_MONTHS = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12",
}


def parse_title_year(raw: str) -> tuple[str, int | None]:
    """Extract title and year from 'Title (Year)' string."""
    m = re.search(r"\((\d{4})\)\s*$", raw.strip())
    year = int(m.group(1)) if m else None
    title = re.sub(r"\s*\(\d{4}\)\s*$", "", raw.strip()).strip()
    return title, year


def parse_spanish_date(date_str: str) -> str | None:
    """Convert 'DD de MES de YYYY, HH:MM' to YYYY-MM-DD."""
    m = re.search(r"(\d+)\s+de\s+(\w+)\s+de\s+(\d{4})", date_str, re.IGNORECASE)
    if not m:
        return None
    day, month_str, year = m.group(1), m.group(2).lower(), m.group(3)
    month = SPANISH_MONTHS.get(month_str)
    if not month:
        return None
    return f"{year}-{month}-{int(day):02d}"


def parse_ratings_html(html_content: str) -> list[dict]:
    """Parse movie-ratings.html. Returns list of film dicts."""
    soup = BeautifulSoup(html_content, "html.parser")
    films = []

    for row in soup.select("table.movie-ratings tr"):
        try:
            rating_el = row.select_one("div.user-rating")
            title_el = row.select_one("td:nth-child(2)")
            date_el = row.select_one("em")

            if not rating_el or not title_el:
                continue

            rating = int(rating_el.get_text(strip=True))
            title, year = parse_title_year(title_el.get_text(strip=True))
            watch_date = parse_spanish_date(date_el.get_text(strip=True) if date_el else "")

            films.append({
                "title": title,
                "year": year,
                "score": rating,
                "watch_date": watch_date,
                "media_type": MediaTypes.MOVIE.value,
            })
        except Exception as e:
            logger.debug("FA ratings parse error: %s", e)

    return films


def parse_list_html(html_content: str) -> tuple[str, list[dict]]:
    """
    Parse a list-N.html file.
    Returns (list_name, [film dicts]).
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract list name from h1 or title
    name_el = soup.find("h1") or soup.find("h2") or soup.find("title")
    list_name = name_el.get_text(strip=True) if name_el else "FilmAffinity List"

    # Strip FA boilerplate from name e.g. 'Películas en mi lista "Mis favoritas"'
    m = re.search(r'"([^"]+)"', list_name)
    if m:
        list_name = m.group(1)

    films = []
    for row in soup.select("table.lists tr"):
        try:
            title_el = row.select_one("td")
            if not title_el:
                continue
            title, year = parse_title_year(title_el.get_text(strip=True))
            if title:
                films.append({"title": title, "year": year, "media_type": MediaTypes.MOVIE.value})
        except Exception as e:
            logger.debug("FA list parse error: %s", e)

    return list_name, films


def resolve_tmdb(title: str, year: int | None) -> tuple[str | None, str, str]:
    """
    Search TMDB for movie or TV. Returns (media_id, source, media_type).
    Strategy:
      1. Search as movie — exact title+year match wins.
      2. If no match, search as TV show.
      3. If still no match, return (None, '', media_type) → caller uses manual.
    TV episodes and video clips that don't match anything go to manual/movie.
    """
    def _search(media_type: str) -> list[dict]:
        try:
            response = services.search(media_type, title, page=1)
            return (response or {}).get("results", []) or []
        except Exception as e:
            logger.debug("FA TMDB search error (%s) for '%s': %s", media_type, title, e)
            return []

    def _best_match(results: list, media_type: str) -> tuple[str | None, str, str]:
        for result in results[:5]:
            r_year = str(result.get("year") or result.get("release_date", ""))[:4]
            title_match = result.get("title", "").lower() == title.lower()
            year_match = year is None or str(year) == r_year
            if title_match and year_match:
                return str(result["media_id"]), "tmdb", media_type
        return None, "", media_type

    # 1. Try as movie
    movie_results = _search(MediaTypes.MOVIE.value)
    media_id, source, mt = _best_match(movie_results, MediaTypes.MOVIE.value)
    if media_id:
        return media_id, source, mt

    # 2. Try as TV show
    tv_results = _search(MediaTypes.TV.value)
    media_id, source, mt = _best_match(tv_results, MediaTypes.TV.value)
    if media_id:
        return media_id, source, mt

    # 3. Fallback: use first movie result if any, else give up
    if movie_results:
        return str(movie_results[0]["media_id"]), "tmdb", MediaTypes.MOVIE.value
    if tv_results:
        return str(tv_results[0]["media_id"]), "tmdb", MediaTypes.TV.value

    return None, "", MediaTypes.MOVIE.value





class FilmAffinityRatingsImporter:
    def __init__(self, user, overwrite: bool = False):
        self.user = user
        self.overwrite = overwrite
        self.imported = 0
        self.skipped = 0
        self.errors = 0

    def run(self, html_content: str) -> str:
        films = parse_ratings_html(html_content)
        if not films:
            return "No films found in the HTML file. Make sure you upload movie-ratings.html."

        bulk_media = defaultdict(list)

        for film in films:
            try:
                obj = self._build_obj(film)
                if obj:
                    bulk_media[MediaTypes.MOVIE.value].append(obj)
            except Exception as e:
                logger.error("FA import error for '%s': %s", film.get("title"), e)
                self.errors += 1

        helpers.bulk_create_media(bulk_media, self.user)
        self.imported = sum(len(v) for v in bulk_media.values())

        return (
            f"FilmAffinity import complete: {self.imported} imported, "
            f"{self.skipped} skipped, {self.errors} errors."
        )

    def _build_obj(self, film: dict):
        title = film["title"]
        year = film.get("year")
        score = film.get("score")

        media_id, source, media_type = resolve_tmdb(title, year)
        if not media_id:
            source = "manual"
            media_type = MediaTypes.MOVIE.value
            media_id = f"fa_{title[:40]}"

        model = apps.get_model(app_label="app", model_name=media_type)
        exists = model.objects.filter(
            user=self.user,
            item__media_id=media_id,
            item__source=source,
            item__media_type=media_type,
        ).exists()

        if exists and not self.overwrite:
            self.skipped += 1
            return None

        item, _ = Item.objects.get_or_create(
            media_id=media_id,
            source=source,
            media_type=media_type,
            defaults={"title": title, "image": ""},
        )

        return model(
            item=item,
            user=self.user,
            score=score * 10 if score is not None else None,
            status=Status.COMPLETED.value,
        )


class FilmAffinityListImporter:
    """Import a FilmAffinity list-N.html into a Yamtrack custom list."""

    def __init__(self, user):
        self.user = user
        self.added = 0
        self.skipped = 0
        self.errors = 0

    def run(self, html_content: str) -> str:
        from lists.models import CustomList, CustomListItem

        list_name, films = parse_list_html(html_content)
        if not films:
            return "No films found in the list file."

        custom_list, created = CustomList.objects.get_or_create(
            owner=self.user,
            name=list_name,
            defaults={"description": "Imported from FilmAffinity"},
        )
        action = "Created" if created else "Updated"

        for film in films:
            try:
                title = film["title"]
                year = film.get("year")

                media_id, source, media_type = resolve_tmdb(title, year)
                if not media_id:
                    source = "manual"
                    media_type = MediaTypes.MOVIE.value
                    media_id = f"fa_{title[:40]}"

                item, _ = Item.objects.get_or_create(
                    media_id=media_id,
                    source=source,
                    media_type=media_type,
                    defaults={"title": title, "image": ""},
                )

                _, item_created = CustomListItem.objects.get_or_create(
                    custom_list=custom_list,
                    item=item,
                )
                if item_created:
                    self.added += 1
                else:
                    self.skipped += 1
            except Exception as e:
                logger.error("FA list import error for '%s': %s", film.get("title"), e)
                self.errors += 1

        return (
            f"{action} list '{list_name}': {self.added} added, "
            f"{self.skipped} already in list, {self.errors} errors."
        )


@shared_task(name="Import from FilmAffinity HTML")
def import_from_filmaffinity_html(
    user_id: int,
    html_content: str,
    overwrite: bool = False,
    import_type: str = "ratings",
) -> str:
    """
    Import from FilmAffinity HTML.
    import_type: 'ratings' for movie-ratings.html, 'list' for list-N.html
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return f"User {user_id} not found."

    if import_type == "list":
        importer = FilmAffinityListImporter(user)
    else:
        importer = FilmAffinityRatingsImporter(user, overwrite=overwrite)

    return importer.run(html_content)


@shared_task(name="Import from FilmAffinity CSV")
def import_from_filmaffinity_csv(user_id: int, csv_content: str, overwrite: bool = False) -> str:
    return "CSV import not configured. Please upload movie-ratings.html instead."
