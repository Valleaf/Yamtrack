"""
Import from FilmAffinity HTML export.

FilmAffinity's data export is a ZIP containing HTML files.
The relevant file is html/movie-ratings.html which lists all rated films.

Format of each row:
    <tr>
        <td><div class="user-rating">8</div></td>
        <td>Film Title (Year)</td>
        <td><em>date string</em></td>
    </tr>

All items from FA are movies/films. Upload the movie-ratings.html file directly.
"""

import logging
import re
from collections import defaultdict

from bs4 import BeautifulSoup
from celery import shared_task
from django.apps import apps
from django.contrib.auth import get_user_model

from app.models import Item, MediaTypes
from app.providers import services
from integrations.imports import helpers

logger = logging.getLogger(__name__)
User = get_user_model()


class FilmAffinityHTMLImporter:
    def __init__(self, user, overwrite: bool = False):
        self.user = user
        self.overwrite = overwrite
        self.imported = 0
        self.skipped = 0
        self.errors = 0

    def parse_html(self, html_content: str) -> list[dict]:
        """Parse movie-ratings.html and return list of film dicts."""
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

                # Title cell contains "Film Title (Year)"
                title_raw = title_el.get_text(strip=True)
                year_match = re.search(r"\((\d{4})\)\s*$", title_raw)
                year = int(year_match.group(1)) if year_match else None
                title = re.sub(r"\s*\(\d{4}\)\s*$", "", title_raw).strip()

                # Parse Spanish date string e.g. "10 de mayo de 2026, 15:06"
                watch_date = self._parse_date(date_el.get_text(strip=True) if date_el else "")

                films.append({
                    "title": title,
                    "year": year,
                    "score": rating,
                    "watch_date": watch_date,
                    "media_type": MediaTypes.MOVIE.value,
                })
            except Exception as e:
                logger.debug("FA parse error on row: %s", e)

        return films

    @staticmethod
    def _parse_date(date_str: str) -> str | None:
        """Convert Spanish date 'DD de MES de YYYY, HH:MM' to YYYY-MM-DD."""
        months = {
            "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
            "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
            "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12",
        }
        m = re.search(r"(\d+)\s+de\s+(\w+)\s+de\s+(\d{4})", date_str, re.IGNORECASE)
        if not m:
            return None
        day, month_str, year = m.group(1), m.group(2).lower(), m.group(3)
        month = months.get(month_str)
        if not month:
            return None
        return f"{year}-{month}-{int(day):02d}"

    def run(self, html_content: str) -> str:
        films = self.parse_html(html_content)
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
        media_type = MediaTypes.MOVIE.value

        media_id, source = self._resolve_tmdb(title, year)

        if not media_id:
            source = "manual"
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
            status=Item.Status.COMPLETED,
        )

    def _resolve_tmdb(self, title: str, year) -> tuple[str | None, str]:
        """Search TMDB for the film. Returns (media_id, source)."""
        try:
            response = services.search(MediaTypes.MOVIE.value, title, page=1)
            results = (response or {}).get("results", [])
            if not results:
                return None, ""

            for result in results[:5]:
                r_year = str(result.get("year") or result.get("release_date", ""))[:4]
                title_match = result.get("title", "").lower() == title.lower()
                year_match = year is None or str(year) == r_year
                if title_match and year_match:
                    return str(result["media_id"]), "tmdb"

            # Fallback: first result
            return str(results[0]["media_id"]), "tmdb"
        except Exception as e:
            logger.debug("FA TMDB resolve error for '%s': %s", title, e)
            return None, ""


@shared_task(name="Import from FilmAffinity HTML")
def import_from_filmaffinity_html(
    user_id: int,
    html_content: str,
    overwrite: bool = False,
) -> str:
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return f"User {user_id} not found."

    importer = FilmAffinityHTMLImporter(user, overwrite=overwrite)
    return importer.run(html_content)


# Keep CSV importer as fallback for other formats
@shared_task(name="Import from FilmAffinity CSV")
def import_from_filmaffinity_csv(
    user_id: int,
    csv_content: str,
    overwrite: bool = False,
) -> str:
    """Fallback CSV importer — format TBD."""
    return "CSV import not yet configured. Please upload movie-ratings.html instead."
