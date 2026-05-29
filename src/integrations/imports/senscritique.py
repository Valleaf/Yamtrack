"""
Import from SensCritique official data export.

Expected file: ``user_XXXXXX_collections.csv`` from the SensCritique
data-export ZIP (senscritique.com → account settings → export data).

Column layout:
    date_notation, type, titre, titre_original, auteurs, sortie,
    oeuvre_principale, note, recommande, acheve, envie,
    titre_critique, critique, vues_critique, likes

Type mapping (SC → Yamtrack):
    movie       → movie   (TMDB)
    tv show     → tv      (TMDB)
    book        → book    (OpenLibrary)
    game        → game    (IGDB)
    music album → music   (MusicBrainz)
    comic book  → manga   (MAL — closest fit)

Status mapping:
    acheve = TRUE  → COMPLETED
    envie  = TRUE  → PLANNING
    otherwise      → IN_PROGRESS

Score mapping:
    SensCritique 1-10 → Yamtrack 1-10 (no conversion needed)
"""

import csv
import io
import logging
import re
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher

from django.apps import apps
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from app.models import Item, MediaTypes, Sources, Status
from app.providers import services
from integrations.imports import helpers
from integrations.imports.helpers import MediaImportError

logger = logging.getLogger(__name__)

# Map SensCritique 'type' column values to Yamtrack media_type strings
SC_TYPE_MAP: dict[str, str] = {
    "movie":       MediaTypes.MOVIE.value,
    "tv show":     MediaTypes.TV.value,
    "book":        MediaTypes.BOOK.value,
    "game":        MediaTypes.GAME.value,
    "music album": MediaTypes.MUSIC.value,
    "comic book":  MediaTypes.MANGA.value,
}

# Map Yamtrack media_type to its default source
SOURCE_FOR: dict[str, str] = {
    MediaTypes.MOVIE.value: Sources.TMDB.value,
    MediaTypes.TV.value:    Sources.TMDB.value,
    MediaTypes.BOOK.value:  Sources.OPENLIBRARY.value,
    MediaTypes.GAME.value:  Sources.IGDB.value,
    MediaTypes.MUSIC.value: Sources.MUSICBRAINZ.value,
    MediaTypes.MANGA.value: Sources.MAL.value,
}

# TV/Season/Episode use computed properties for start_date/end_date — skip them
_NO_DATE_FIELDS = frozenset({
    MediaTypes.TV.value,
    MediaTypes.SEASON.value,
    MediaTypes.EPISODE.value,
})

# SC types that cannot be mapped — silently skipped
UNSUPPORTED_TYPES: set[str] = set()


def importer(file, user, mode):
    """Entry point called by the shared import_media task helper."""
    sc_importer = SensCritiqueImporter(file, user, mode)
    return sc_importer.import_data()


class SensCritiqueImporter:
    """Import media from a SensCritique collections CSV export."""

    def __init__(self, file, user, mode):
        self.file = file
        self.user = user
        self.mode = mode
        self.warnings: list[str] = []
        self.existing_media = helpers.get_existing_media(user)
        self.to_delete: dict = defaultdict(lambda: defaultdict(set))
        self.bulk_media: dict = defaultdict(list)

        logger.info(
            "Initialized SensCritique importer for user %s with mode %s",
            user.username,
            mode,
        )

    # ------------------------------------------------------------------ #
    # Public                                                               #
    # ------------------------------------------------------------------ #

    def import_data(self):
        """Parse CSV and bulk-create media. Returns (counts, warnings)."""
        try:
            raw = self.file.read()
            csv_text = raw.decode("utf-8-sig")  # handles BOM if present
        except UnicodeDecodeError as exc:
            raise MediaImportError(
                "Invalid file encoding — please upload the collections CSV "
                "from your SensCritique data export."
            ) from exc

        reader = csv.DictReader(io.StringIO(csv_text))
        rows = list(reader)

        if not rows:
            return {}, "No rows found in CSV."

        # Validate that this looks like the right file
        expected = {"type", "titre", "note", "acheve", "envie"}
        if not expected.issubset(set(reader.fieldnames or [])):
            raise MediaImportError(
                "Unexpected CSV format. Make sure you upload "
                "user_XXXXXX_collections.csv from your SensCritique export."
            )

        # Group rows by media type
        rows_by_type: dict[str, list[dict]] = defaultdict(list)
        for row in rows:
            raw_type = (row.get("type") or "").strip().lower()
            media_type = SC_TYPE_MAP.get(raw_type)
            if media_type:
                rows_by_type[media_type].append(row)
            elif raw_type and raw_type not in UNSUPPORTED_TYPES:
                logger.debug("Unknown SC type '%s' — skipped", raw_type)

        for media_type, type_rows in rows_by_type.items():
            logger.info(
                "SensCritique: processing %d %s rows", len(type_rows), media_type
            )
            for row in type_rows:
                self._process_row(row, media_type)

        helpers.cleanup_existing_media(self.to_delete, self.user)
        helpers.bulk_create_media(self.bulk_media, self.user)

        imported_counts = {
            mt: len(items) for mt, items in self.bulk_media.items()
        }
        warnings_str = "\n".join(self.warnings) if self.warnings else None
        return imported_counts, warnings_str

    # ------------------------------------------------------------------ #
    # Private                                                              #
    # ------------------------------------------------------------------ #

    def _process_row(self, row: dict, media_type: str):
        """Process a single CSV row and append to bulk_media if valid."""
        source = SOURCE_FOR[media_type]

        # Prefer original title (usually English → better API match)
        title = (row.get("titre_original") or "").strip()
        if not title:
            title = (row.get("titre") or "").strip()
        if not title:
            return

        # Release year from 'sortie' column (YYYY or YYYY-MM-DD)
        sortie = (row.get("sortie") or "").strip()
        year: int | None = None
        if sortie and len(sortie) >= 4 and sortie[:4].isdigit():
            year = int(sortie[:4])

        score = _parse_score(row.get("note") or "")
        status = _parse_status(row.get("acheve") or "", row.get("envie") or "")
        if score is None and status != Status.PLANNING.value:
            return
        date_added = _parse_date(row.get("date_notation") or "")
        notes = (row.get("critique") or "").strip()

        media_id, resolved_source = _resolve(title, year, media_type, source)
        if not media_id:
            self.warnings.append(
                f"{title} ({media_type}): ambiguous or no confident match via {source}"
            )
            return

        if not helpers.should_process_media(
            self.existing_media,
            self.to_delete,
            media_type,
            resolved_source,
            str(media_id),
            self.mode,
        ):
            return

        item, _ = Item.objects.get_or_create(
            media_id=media_id,
            source=resolved_source,
            media_type=media_type,
            defaults={"title": title, "image": ""},
        )

        model = apps.get_model(app_label="app", model_name=media_type)
        params = {
            "item": item,
            "user": self.user,
            "score": score,
            "status": status,
            "notes": notes,
        }

        # TV/Season/Episode have computed properties for dates — skip them
        if date_added and media_type not in _NO_DATE_FIELDS:
            params["start_date"] = date_added
            if status == Status.COMPLETED.value:
                params["end_date"] = date_added

        instance = model(**params)
        if date_added:
            instance._history_date = date_added
        self.bulk_media[media_type].append(instance)


# ------------------------------------------------------------------ #
# Module-level helpers                                                #
# ------------------------------------------------------------------ #

def _parse_status(acheve: str, envie: str) -> str:
    if acheve.strip().upper() == "TRUE":
        return Status.COMPLETED.value
    if envie.strip().upper() == "TRUE":
        return Status.PLANNING.value
    return Status.IN_PROGRESS.value


def _parse_score(note: str) -> float | None:
    note = note.strip()
    if not note:
        return None
    try:
        return float(note)
    except ValueError:
        return None


def _parse_date(date_notation: str):
    """Parse SensCritique dates into aware datetime."""
    date_notation = date_notation.strip()

    if not date_notation:
        return None

    formats = [
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
    ]

    for fmt in formats:
        try:
            naive = datetime.strptime(date_notation, fmt)
            return timezone.make_aware(naive)
        except ValueError:
            continue

    return None

def _normalize_title(title: str) -> str:
    """Normalize titles for safer matching."""

    if not title:
        return ""

    title = unicodedata.normalize("NFKD", title)
    title = title.encode("ascii", "ignore").decode("ascii")

    title = title.lower()

    # Remove stuff in brackets
    title = re.sub(r"\(.*?\)", "", title)
    title = re.sub(r"\[.*?\]", "", title)

    # Remove common noisy suffixes
    noisy = [
        "ost",
        "original soundtrack",
        "hd remaster",
        "remastered",
        "definitive edition",
        "goty edition",
        "game of the year edition",
        "collector edition",
    ]

    for n in noisy:
        title = title.replace(n, "")

    # Remove punctuation
    title = re.sub(r"[^a-z0-9\s]", " ", title)

    # Collapse spaces
    title = " ".join(title.split())

    return title


def _resolve(
    title: str,
    year: int | None,
    media_type: str,
    source: str,
) -> tuple[str | None, str]:
    """Search provider and return a safe high-confidence match."""

    try:
        response = services.search(media_type, title, page=1)
        results = (response or {}).get("results", [])

        if not results:
            return None, ""

        normalized_target = _normalize_title(title)

        best_match = None
        best_score = 0

        for result in results[:10]:
            r_title = result.get("title") or ""
            normalized_result = _normalize_title(r_title)

            similarity = SequenceMatcher(
                None,
                normalized_target,
                normalized_result,
            ).ratio()

            score = similarity

            r_year = str(
                result.get("year")
                or result.get("release_date", "")
            )[:4]

            # Strong bonus for matching year
            if year and r_year == str(year):
                score += 0.15

            # Exact normalized match bonus
            if normalized_target == normalized_result:
                score += 0.25

            if score > best_score:
                best_score = score
                best_match = result

        # Require decent confidence
        if best_match and best_score >= 0.72:
            return str(best_match["media_id"]), source

        return None, ""

    except Exception as exc:
        logger.debug("SC resolve error for '%s': %s", title, exc)
        return None, ""
