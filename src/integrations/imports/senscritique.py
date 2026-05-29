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

Confidence tiers for fuzzy matching:
    score >= HIGH_CONFIDENCE_THRESHOLD  → imported automatically
    score >= REVIEW_THRESHOLD           → queued for user review
    score <  REVIEW_THRESHOLD           → skipped / warning
"""

import csv
import io
import json
import logging
import re
import unicodedata
from collections import defaultdict
from datetime import datetime
from difflib import SequenceMatcher

from django.apps import apps
from django.utils import timezone

from app.models import Item, MediaTypes, Sources, Status
from app.providers import services
from integrations.imports import helpers
from integrations.imports.helpers import MediaImportError

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Constants                                                                     #
# --------------------------------------------------------------------------- #

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

# Matching thresholds
HIGH_CONFIDENCE_THRESHOLD = 0.82  # auto-import above this
REVIEW_THRESHOLD = 0.50           # queue for review between this and high


# --------------------------------------------------------------------------- #
# Public entry point                                                            #
# --------------------------------------------------------------------------- #

def importer(file, user, mode):
    """Entry point called by the shared import_media task helper.

    Returns (imported_counts, warnings_str).
    Items that need user review are stored in Redis under a key specific to
    the user and can be retrieved via get_pending_review / confirm_pending.
    """
    sc_importer = SensCritiqueImporter(file, user, mode)
    return sc_importer.import_data()


# --------------------------------------------------------------------------- #
# Redis helpers for pending-review items                                        #
# --------------------------------------------------------------------------- #

PENDING_KEY_PREFIX = "sc_review:"
PENDING_TTL = 60 * 60 * 24 * 7  # 7 days


def _redis():
    """Return the shared Redis client from services."""
    return services.redis_db


def store_pending_review(user_id: int, pending: list[dict]) -> None:
    """Persist pending-review items for the user in Redis."""
    key = f"{PENDING_KEY_PREFIX}{user_id}"
    _redis().set(key, json.dumps(pending), ex=PENDING_TTL)


def get_pending_review(user_id: int) -> list[dict]:
    """Retrieve pending-review items for the user from Redis."""
    key = f"{PENDING_KEY_PREFIX}{user_id}"
    raw = _redis().get(key)
    if not raw:
        return []
    try:
        return json.loads(raw)
    except Exception:
        return []


def clear_pending_review(user_id: int) -> None:
    """Remove pending-review items for the user from Redis."""
    _redis().delete(f"{PENDING_KEY_PREFIX}{user_id}")


def confirm_pending_items(
    user_id: int,
    confirmed_indices: list[int],
    mode: str,
) -> tuple[dict, str | None]:
    """Import the user-confirmed subset of pending items.

    ``confirmed_indices`` is a list of integer positions in the pending list
    that the user approved.  Items not in the list are discarded.

    Returns (imported_counts, warnings_str) just like the main importer.
    """
    from django.contrib.auth import get_user_model

    user = get_user_model().objects.get(id=user_id)
    pending = get_pending_review(user_id)

    if not pending:
        return {}, "No pending review items found."

    existing_media = helpers.get_existing_media(user)
    to_delete: dict = defaultdict(lambda: defaultdict(set))
    bulk_media: dict = defaultdict(list)
    warnings: list[str] = []

    confirmed_set = set(confirmed_indices)

    for idx, item_data in enumerate(pending):
        if idx not in confirmed_set:
            continue

        media_type = item_data["media_type"]
        media_id = item_data["media_id"]
        source = item_data["source"]
        title = item_data["sc_title"]
        score = item_data.get("score")
        status = item_data.get("status", Status.IN_PROGRESS.value)
        notes = item_data.get("notes", "")
        date_added = item_data.get("date_added")

        if not helpers.should_process_media(
            existing_media,
            to_delete,
            media_type,
            source,
            str(media_id),
            mode,
        ):
            continue

        db_item, _ = Item.objects.get_or_create(
            media_id=media_id,
            source=source,
            media_type=media_type,
            defaults={"title": title, "image": ""},
        )

        model = apps.get_model(app_label="app", model_name=media_type)
        params = {
            "item": db_item,
            "user": user,
            "score": score,
            "status": status,
            "notes": notes,
        }

        aware_date = None
        if date_added:
            try:
                naive = datetime.fromisoformat(date_added)
                aware_date = timezone.make_aware(naive) if timezone.is_naive(naive) else naive
            except Exception:
                pass

        if aware_date and media_type not in _NO_DATE_FIELDS:
            params["start_date"] = aware_date
            if status == Status.COMPLETED.value:
                params["end_date"] = aware_date

        instance = model(**params)
        if aware_date:
            instance._history_date = aware_date
        bulk_media[media_type].append(instance)

    helpers.cleanup_existing_media(to_delete, user)
    helpers.bulk_create_media(bulk_media, user)

    # Remove pending items now they've been processed
    clear_pending_review(user_id)

    imported_counts = {mt: len(items) for mt, items in bulk_media.items()}
    warnings_str = "\n".join(warnings) if warnings else None
    return imported_counts, warnings_str


# --------------------------------------------------------------------------- #
# Importer class                                                                #
# --------------------------------------------------------------------------- #

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
        # Items whose match confidence is between REVIEW_THRESHOLD and
        # HIGH_CONFIDENCE_THRESHOLD — stored for user validation.
        self.pending_review: list[dict] = []

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

        # Persist pending-review items so the view can display them
        if self.pending_review:
            store_pending_review(self.user.id, self.pending_review)
            logger.info(
                "SensCritique: %d items queued for user review",
                len(self.pending_review),
            )

        imported_counts = {
            mt: len(items) for mt, items in self.bulk_media.items()
        }
        warnings_str = "\n".join(self.warnings) if self.warnings else None
        return imported_counts, warnings_str

    # ------------------------------------------------------------------ #
    # Private                                                              #
    # ------------------------------------------------------------------ #

    def _process_row(self, row: dict, media_type: str):
        """Process a single CSV row, auto-import or queue for review."""
        source = SOURCE_FOR[media_type]

        # Prefer original title (usually English → better API match)
        title = (row.get("titre_original") or "").strip()
        if not title:
            title = (row.get("titre") or "").strip()
        if not title:
            return

        # SC display title (may be in French) — useful to show in review UI
        sc_display_title = (row.get("titre") or title).strip()

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

        media_id, resolved_source, confidence, candidate = _resolve(
            title, year, media_type, source
        )

        if media_id and confidence >= HIGH_CONFIDENCE_THRESHOLD:
            # High confidence → auto-import
            self._enqueue_item(
                media_type=media_type,
                media_id=media_id,
                source=resolved_source,
                title=title,
                score=score,
                status=status,
                notes=notes,
                date_added=date_added,
            )

        elif media_id and confidence >= REVIEW_THRESHOLD:
            # Medium confidence → queue for user review
            self.pending_review.append({
                "sc_title": sc_display_title,
                "sc_original_title": title,
                "sc_year": year,
                "media_type": media_type,
                "source": resolved_source,
                "media_id": str(media_id),
                "candidate_title": candidate.get("title", ""),
                "candidate_year": str(candidate.get("year") or candidate.get("release_date", ""))[:4],
                "candidate_image": candidate.get("image", ""),
                "confidence": round(confidence, 3),
                "score": score,
                "status": status,
                "notes": notes,
                "date_added": date_added.isoformat() if date_added else None,
            })

        else:
            # No usable match
            self.warnings.append(
                f"{sc_display_title} ({media_type}): no confident match found"
            )

    def _enqueue_item(
        self,
        *,
        media_type: str,
        media_id: str,
        source: str,
        title: str,
        score,
        status: str,
        notes: str,
        date_added,
    ):
        """Validate and add item to the bulk-create queue."""
        if not helpers.should_process_media(
            self.existing_media,
            self.to_delete,
            media_type,
            source,
            str(media_id),
            self.mode,
        ):
            return

        item, _ = Item.objects.get_or_create(
            media_id=media_id,
            source=source,
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

        if date_added and media_type not in _NO_DATE_FIELDS:
            params["start_date"] = date_added
            if status == Status.COMPLETED.value:
                params["end_date"] = date_added

        instance = model(**params)
        if date_added:
            instance._history_date = date_added
        self.bulk_media[media_type].append(instance)


# --------------------------------------------------------------------------- #
# Module-level helpers                                                          #
# --------------------------------------------------------------------------- #

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
        "ost", "original soundtrack", "hd remaster", "remastered",
        "definitive edition", "goty edition", "game of the year edition",
        "collector edition",
    ]
    for n in noisy:
        title = title.replace(n, "")

    # Remove punctuation
    title = re.sub(r"[^a-z0-9\s]", " ", title)

    # Collapse spaces
    return " ".join(title.split())


def _resolve(
    title: str,
    year: int | None,
    media_type: str,
    source: str,
) -> tuple[str | None, str, float, dict]:
    """Search provider and return (media_id, source, confidence, candidate).

    Returns (None, '', 0.0, {}) on failure.
    """
    try:
        response = services.search(media_type, title, page=1)
        results = (response or {}).get("results", [])

        if not results:
            return None, "", 0.0, {}

        normalized_target = _normalize_title(title)

        best_match: dict = {}
        best_score: float = 0.0

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
                result.get("year") or result.get("release_date", "")
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

        if best_match:
            return str(best_match["media_id"]), source, best_score, best_match

        return None, "", 0.0, {}

    except Exception as exc:
        logger.debug("SC resolve error for '%s': %s", title, exc)
        return None, "", 0.0, {}
