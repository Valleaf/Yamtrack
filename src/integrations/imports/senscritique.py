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
    comic book  → manga (MAL) if CJK authors,
                   comic (BnF)       if French BD heuristic matches,
                   comic (ComicVine) for western comics

Status mapping:
    acheve = TRUE  → COMPLETED
    envie  = TRUE  → PLANNING
    otherwise      → IN_PROGRESS

Score mapping:
    SensCritique 1-10 → Yamtrack 1-10 (no conversion needed)

Confidence tiers for fuzzy matching:
    score >= HIGH_CONFIDENCE_THRESHOLD  → imported automatically
    score >= REVIEW_THRESHOLD           → review page, pre-selected
    score <  REVIEW_THRESHOLD           → review page, unchecked
    no match found                      → review page, disabled (cannot confirm)
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
from functools import lru_cache

from django.apps import apps
from django.conf import settings
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
# Note: 'comic book' is handled separately via _resolve_comic_media_type()
SC_TYPE_MAP: dict[str, str] = {
    "movie":       MediaTypes.MOVIE.value,
    "tv show":     MediaTypes.TV.value,
    "book":        MediaTypes.BOOK.value,
    "game":        MediaTypes.GAME.value,
    "music album": MediaTypes.MUSIC.value,
    "comic book":  "_comic_auto",  # resolved dynamically
}

# Map Yamtrack media_type to its default source
SOURCE_FOR: dict[str, str] = {
    MediaTypes.MOVIE.value: Sources.TMDB.value,
    MediaTypes.TV.value:    Sources.TMDB.value,
    MediaTypes.BOOK.value:  Sources.HARDCOVER.value,
    MediaTypes.GAME.value:  Sources.IGDB.value,
    MediaTypes.MUSIC.value: Sources.MUSICBRAINZ.value,
    MediaTypes.MANGA.value: Sources.MAL.value,
    MediaTypes.COMIC.value: Sources.COMICVINE.value,  # western comics; BD overrides to BNF
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
REVIEW_THRESHOLD = 0.50           # pre-selected in review UI above this; unchecked below


# --------------------------------------------------------------------------- #
# Public entry point                                                            #
# --------------------------------------------------------------------------- #

def importer(file, user, mode, allowed_sc_types=None):
    """Entry point called by the shared import_media task helper.

    ``allowed_sc_types`` is an optional collection of raw SensCritique type
    strings (e.g. ``["movie", "tv show", "comic book"]``).  When provided,
    only rows whose ``type`` column matches one of these values are processed.
    ``None`` or an empty iterable means *all* types are imported.

    Returns (imported_counts, warnings_str).
    Items that need user review are stored in Redis under a key specific to
    the user and can be retrieved via get_pending_review / confirm_pending.
    """
    sc_importer = SensCritiqueImporter(file, user, mode, allowed_sc_types)
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


def get_pending_review_ttl(user_id: int) -> int | None:
    """Return the remaining TTL (in seconds) of the pending review key.

    Returns None if the key does not exist or has no expiry.
    """
    key = f"{PENDING_KEY_PREFIX}{user_id}"
    ttl = _redis().ttl(key)
    return ttl if ttl > 0 else None


def clear_pending_review(user_id: int) -> None:
    """Remove pending-review items for the user from Redis."""
    _redis().delete(f"{PENDING_KEY_PREFIX}{user_id}")


def confirm_pending_items(
    user_id: int,
    confirmed_indices: list[int],
    mode: str,
    candidate_overrides: dict | None = None,
    manual_overrides: dict | None = None,
) -> tuple[dict, str | None]:
    """Import the user-confirmed subset of pending items.

    ``confirmed_indices`` is a list of integer positions in the pending list
    that the user approved.

    ``candidate_overrides`` maps pending item index → candidate list index,
    allowing users to pick an alternate match from the candidate picker.

    ``manual_overrides`` maps pending item index → {"media_id", "source",
    "title"} dict for items where the user ran a manual re-search and picked
    a result that wasn't in the original candidates list.

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
    overrides = candidate_overrides or {}
    manuals = manual_overrides or {}

    for idx, item_data in enumerate(pending):
        if idx not in confirmed_set:
            continue

        media_type = item_data["media_type"]

        # Priority: manual override > candidate override > top candidate
        manual = manuals.get(idx)
        if manual and manual.get("media_id"):
            media_id = manual["media_id"]
            source = manual.get("source") or item_data["source"]
            title = manual.get("title") or item_data["sc_title"]
        else:
            source = item_data["source"]
            candidates = item_data.get("candidates", [])
            candidate_idx = overrides.get(idx, 0)
            if candidates and 0 <= candidate_idx < len(candidates):
                chosen = candidates[candidate_idx]
                media_id = chosen["media_id"]
                title = chosen.get("title", item_data["sc_title"])
            else:
                media_id = item_data.get("media_id", "")
                title = item_data["sc_title"]

        # Items with no match cannot be confirmed
        if not media_id:
            continue

        score = item_data.get("score")
        status = item_data.get("status", Status.IN_PROGRESS.value)
        notes = item_data.get("notes", "")
        date_added = item_data.get("date_added")

        aware_date = None
        if date_added:
            try:
                naive = datetime.fromisoformat(date_added)
                aware_date = timezone.make_aware(naive) if timezone.is_naive(naive) else naive
            except Exception:
                pass

        # Smart dedup: check if item exists and whether any field changed
        media_id_str = str(media_id)
        existing = existing_media[media_type][source].get(media_id_str)

        if existing is not None:
            if mode == "new":
                logger.debug(
                    "Confirm: skipping existing %s: %s (mode: new)",
                    media_type, media_id_str,
                )
                continue
            elif mode == "overwrite":
                if not _item_differs(existing, score, status, notes, aware_date, media_type):
                    logger.debug(
                        "Confirm: skipping unchanged %s: %s",
                        media_type, media_id_str,
                    )
                    continue
                to_delete[media_type][source].add(media_id_str)

        # Extract image from the selected candidate
        if manual and manual.get("media_id"):
            item_image = manual.get("image", "")
        elif candidates and 0 <= candidate_idx < len(candidates):
            item_image = candidates[candidate_idx].get("image", "")
        else:
            item_image = item_data.get("candidate_image", "")

        saved_image = item_image or settings.IMG_NONE
        db_item, created = Item.objects.get_or_create(
            media_id=media_id,
            source=source,
            media_type=media_type,
            defaults={"title": title, "image": saved_image},
        )
        # Patch image if the existing item has no real artwork
        if not created and item_image and (not db_item.image or db_item.image == settings.IMG_NONE):
            db_item.image = item_image
            db_item.save(update_fields=["image"])

        model = apps.get_model(app_label="app", model_name=media_type)
        params = {
            "item": db_item,
            "user": user,
            "score": score,
            "status": status,
            "notes": notes,
        }

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

    def __init__(self, file, user, mode, allowed_sc_types=None):
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
        self._seen_import_keys: set[tuple[str, str]] = set()
        # None → import everything; non-empty set → restrict to listed SC types
        self.allowed_sc_types: frozenset[str] | None = (
            frozenset(t.strip().lower() for t in allowed_sc_types if t)
            if allowed_sc_types
            else None
        )

        logger.info(
            "Initialized SensCritique importer for user %s with mode %s (allowed types: %s)",
            user.username,
            mode,
            self.allowed_sc_types if self.allowed_sc_types is not None else "all",
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
            # Compare raw SC type strings (e.g. "comic book") against
            # allowed_sc_types, never the mapped values.  SC_TYPE_MAP maps
            # "comic book" → "_comic_auto" (a sentinel resolved later in
            # _process_row); "_comic_auto" is never present in
            # allowed_sc_types, so this filter always operates correctly.
            if self.allowed_sc_types is not None and raw_type not in self.allowed_sc_types:
                continue
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
        # Resolve dynamic comic type → returns (media_type, source_override)
        source_override: str | None = None
        if media_type == "_comic_auto":
            media_type, source_override = _resolve_comic_media_type(row)

        source = source_override or SOURCE_FOR[media_type]

        # Prefer original title (usually English → better API match)
        title = (row.get("titre_original") or "").strip()
        if not title:
            title = (row.get("titre") or "").strip()
        if not title:
            return

        # SC display title (may be in French) — useful to show in review UI
        sc_display_title = (row.get("titre") or title).strip()

        dedup_key = (media_type, _normalize_title(title))
        if dedup_key in self._seen_import_keys:
            return
        self._seen_import_keys.add(dedup_key)

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

        # Pass author/studio info for extra scoring on games
        authors = (row.get("auteurs") or "").strip()

        media_id, resolved_source, confidence, candidates = _resolve(
            title, year, media_type, source, authors
        )

        if media_id and confidence >= HIGH_CONFIDENCE_THRESHOLD:
            # High confidence → auto-import
            top_image = candidates[0].get("image", "") if candidates else ""
            self._enqueue_item(
                media_type=media_type,
                media_id=media_id,
                source=resolved_source,
                title=title,
                image=top_image,
                score=score,
                status=status,
                notes=notes,
                date_added=date_added,
            )

        else:
            # Medium / low confidence / no match → queue for user review
            top = candidates[0] if candidates else {}
            self.pending_review.append({
                "sc_title": sc_display_title,
                "sc_original_title": title,
                "sc_year": year,
                "media_type": media_type,
                "source": resolved_source or source,
                # top candidate quick-access fields (also used by the review card)
                "media_id":        top.get("media_id", ""),
                "confidence":      top.get("confidence", 0.0),
                "candidate_title": top.get("title", ""),
                "candidate_year":  top.get("year", ""),
                "candidate_image": top.get("image", ""),
                # full candidate list for the candidate picker UI (up to 5)
                "candidates": candidates,
                "score": score,
                "status": status,
                "notes": notes,
                "date_added": date_added.isoformat() if date_added else None,
            })

    def _enqueue_item(
        self,
        *,
        media_type: str,
        media_id: str,
        source: str,
        title: str,
        image: str = "",
        score,
        status: str,
        notes: str,
        date_added,
    ):
        """Validate and add item to the bulk-create queue.

        Handles mode logic and smart dedup (skip if no field changed).
        """
        media_id_str = str(media_id)
        existing = self.existing_media[media_type][source].get(media_id_str)

        if existing is not None:
            if self.mode == "new":
                logger.debug(
                    "Skipping existing %s: %s (mode: new)", media_type, media_id_str
                )
                return
            elif self.mode == "overwrite":
                if not _item_differs(existing, score, status, notes, date_added, media_type):
                    logger.debug(
                        "Skipping unchanged %s: %s", media_type, media_id_str
                    )
                    return
                # Mark for deletion so it will be replaced
                self.to_delete[media_type][source].add(media_id_str)

        saved_image = image or settings.IMG_NONE
        item, created = Item.objects.get_or_create(
            media_id=media_id,
            source=source,
            media_type=media_type,
            defaults={"title": title, "image": saved_image},
        )
        # Patch image if the existing item has no real artwork
        if not created and image and (not item.image or item.image == settings.IMG_NONE):
            item.image = image
            item.save(update_fields=["image"])

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


def _item_differs(existing, score, status, notes, date_added, media_type) -> bool:
    """Return True if any tracked field differs from the existing record.

    Used to skip re-importing items that haven't changed, even in overwrite mode.
    """
    # Compare score (handle None vs None, float vs Decimal, etc.)
    existing_score = existing.score
    try:
        if existing_score is None and score is None:
            scores_equal = True
        elif existing_score is None or score is None:
            scores_equal = False
        else:
            scores_equal = abs(float(existing_score) - float(score)) < 0.001
    except (TypeError, ValueError):
        scores_equal = existing_score == score
    if not scores_equal:
        return True

    if existing.status != status:
        return True

    existing_notes = (getattr(existing, "notes", "") or "").strip()
    new_notes = (notes or "").strip()
    if existing_notes != new_notes:
        return True

    # Compare start date (skip for types where dates are not applicable)
    if media_type not in _NO_DATE_FIELDS and date_added:
        existing_start = getattr(existing, "start_date", None)
        if existing_start is None:
            return True
        try:
            existing_day = existing_start.date()
            new_day = date_added.date() if hasattr(date_added, "date") else date_added
            if existing_day != new_day:
                return True
        except Exception:
            pass

    return False


_JAPANESE_NAME_RE = re.compile(
    r"[\u3000-\u9fff\uff00-\uffef]",  # CJK / fullwidth chars
    re.UNICODE,
)

# Well-known French/Belgian BD publishers (lowercase)
_BD_PUBLISHERS = frozenset([
    "dargaud", "dupuis", "casterman", "le lombard", "lombard", "soleil",
    "glenat", "glc3a9nat", "bdkids", "bdkg", "rue de sevres",
    "futuropolis", "humanoides", "humanoid", "sandawe",
])

# Well-known BD series/character names (lowercase)
_BD_SERIES = frozenset([
    "asterix", "ast\u00e9rix", "tintin", "lucky luke", "spirou",
    "thorgal", "gaston lagaffe", "gaston", "lanfeust", "valerian",
    "blueberry", "michel vaillant", "blake et mortimer",
    "les schtroumpfs", "schtroumpfs", "boule et bill",
    "largo winch", "le chat", "titeuf",
])

# Well-known BD authors (lowercase; last names or common forms)
_BD_AUTHORS = frozenset([
    "herge", "herg\u00e9", "goscinny", "uderzo", "van hamme", "rosinski",
    "franquin", "moebius", "bilal", "juillard", "yslaire", "peyo",
    "gregoire", "loisel", "trondheim", "sfar", "blain", "joann sfar",
    "lewis trondheim", "christophe blain",
])

_MANGA_KEYWORDS = frozenset([
    "manga", "sh\u014dnen", "shonen", "sh\u014djo", "shoujo", "seinen",
    "kodansha", "shueisha", "jump", "tankobon",
])


def _resolve_comic_media_type(row: dict) -> tuple[str, str]:
    """Three-way classification: manga, French BD, or western comic.

    Returns ``(media_type, source)`` tuples:
        * manga   → (MediaTypes.MANGA,  Sources.MAL)
        * BD      → (MediaTypes.COMIC,  Sources.BNF)
        * western → (MediaTypes.COMIC,  Sources.COMICVINE)
    """
    authors_raw = row.get("auteurs") or ""
    title_raw   = row.get("titre") or ""
    orig_raw    = row.get("titre_original") or ""

    # Normalise for keyword matching (lowercase, no accents)
    authors_low = authors_raw.lower()
    title_low   = (title_raw + " " + orig_raw).lower()
    combined    = f"{authors_low} {title_low}"

    # ── Manga detection ───────────────────────────────────────────────────
    if _JAPANESE_NAME_RE.search(authors_raw):
        return MediaTypes.MANGA.value, Sources.MAL.value

    manga_score = sum(1 for kw in _MANGA_KEYWORDS if kw in combined)

    # ── BD / French comic detection ───────────────────────────────────────
    bd_score = 0
    bd_score += sum(1 for kw in _BD_PUBLISHERS if kw in combined)
    bd_score += sum(1 for kw in _BD_SERIES    if kw in combined)
    bd_score += sum(2 for kw in _BD_AUTHORS   if kw in combined)

    if manga_score > bd_score and manga_score > 0:
        return MediaTypes.MANGA.value, Sources.MAL.value

    if bd_score > 0:
        return MediaTypes.COMIC.value, Sources.BNF.value

    # Default: treat as western comic
    return MediaTypes.COMIC.value, Sources.COMICVINE.value


@lru_cache(maxsize=512)
def _cached_search(media_type: str, title: str, source: str = "") -> list:
    """Cache provider search results to avoid duplicate API calls."""
    try:
        response = services.search(media_type, title, page=1, source=source or None)
        return (response or {}).get("results", [])
    except Exception as exc:
        logger.debug("SC search error for '%s' (%s): %s", title, media_type, exc)
        return []


def _resolve(
    title: str,
    year: int | None,
    media_type: str,
    source: str,
    authors: str = "",
) -> tuple[str | None, str, float, list]:
    """Search provider and return (best_media_id, source, best_confidence, candidates).

    ``candidates`` is a list of up to 5 dicts, each with keys:
        media_id, title, year, image, confidence
    sorted best-first.

    Special handling:
    * Books: Hardcover first, falls back to OpenLibrary on empty results.
    * French BDs (source=BNF): BnF search first, falls back to ComicVine.
      Candidates from both sources are merged and labelled.

    Returns (None, '', 0.0, []) on failure.
    """
    # ── BD: BnF first, ComicVine fallback ──────────────────────────────────
    if source == Sources.BNF.value and media_type == MediaTypes.COMIC.value:
        return _resolve_bd(title, year, authors)

    results = _cached_search(media_type, title, source)

    # Book fallback: if Hardcover returns nothing, try OpenLibrary
    actual_source = source
    if not results and media_type == MediaTypes.BOOK.value and source == Sources.HARDCOVER.value:
        logger.debug("Hardcover returned no results for '%s', falling back to OpenLibrary", title)
        results = _cached_search(media_type, title, Sources.OPENLIBRARY.value)
        if results:
            actual_source = Sources.OPENLIBRARY.value

    if not results:
        return None, "", 0.0, []

    candidates = _score_and_rank(results, title, year, authors, media_type, actual_source)

    if not candidates:
        return None, "", 0.0, []

    best = candidates[0]
    return best["media_id"], actual_source, best["confidence"], candidates


def _resolve_bd(
    title: str,
    year: int | None,
    authors: str,
) -> tuple[str | None, str, float, list]:
    """BnF → ComicVine fallback resolver for French BDs.

    Tries BnF first.  If the best BnF confidence does not reach
    HIGH_CONFIDENCE_THRESHOLD, also queries ComicVine and merges the top
    candidates (BnF results first, then ComicVine, de-duplicated by title).
    """
    bnf_results   = _cached_search(MediaTypes.COMIC.value, title, Sources.BNF.value)
    bnf_cands     = _score_and_rank(
        bnf_results, title, year, authors, MediaTypes.COMIC.value, Sources.BNF.value
    ) if bnf_results else []

    best_bnf_conf = bnf_cands[0]["confidence"] if bnf_cands else 0.0

    if best_bnf_conf >= HIGH_CONFIDENCE_THRESHOLD:
        # BnF match is confident enough — use it directly
        best = bnf_cands[0]
        return best["media_id"], Sources.BNF.value, best["confidence"], bnf_cands[:5]

    # BnF didn't return a confident match — also try ComicVine
    cv_results = _cached_search(MediaTypes.COMIC.value, title, Sources.COMICVINE.value)
    cv_cands   = _score_and_rank(
        cv_results, title, year, authors, MediaTypes.COMIC.value, Sources.COMICVINE.value
    ) if cv_results else []

    # Merge: BnF candidates first (they match French titles better), then
    # ComicVine candidates for items not already represented
    seen_titles: set[str] = set()
    merged: list[dict] = []
    for cand in bnf_cands + cv_cands:
        key = cand["title"].lower().strip()
        if key not in seen_titles:
            seen_titles.add(key)
            merged.append(cand)
        if len(merged) >= 5:
            break

    if not merged:
        return None, "", 0.0, []

    best = merged[0]
    # Use the source attached to the best candidate
    best_source = best.get("_source", Sources.BNF.value)
    return best["media_id"], best_source, best["confidence"], merged


def _score_and_rank(
    results: list,
    title: str,
    year: int | None,
    authors: str,
    media_type: str,
    source: str,
) -> list[dict]:
    """Score, rank, and normalise a provider result list.

    Returns up to 5 candidate dicts with keys:
        media_id, title, year, image, confidence, _source (internal)
    sorted best-first.
    """
    normalized_target  = _normalize_title(title)
    normalized_authors = _normalize_title(authors) if authors else ""

    scored: list[tuple[float, dict]] = []

    for result in results[:15]:
        r_title = result.get("title") or ""
        normalized_result = _normalize_title(r_title)

        similarity = SequenceMatcher(
            None, normalized_target, normalized_result,
        ).ratio()

        score = similarity

        r_year_raw = result.get("year") or result.get("release_date", "") or ""
        r_year = str(r_year_raw)[:4]

        if year and r_year == str(year):
            score += 0.15

        if normalized_target == normalized_result:
            score += 0.25

        if normalized_authors and media_type == MediaTypes.GAME.value:
            r_companies = result.get("companies") or []
            r_companies_str = (
                " ".join(r_companies) if isinstance(r_companies, list)
                else str(r_companies)
            )
            normalized_companies = _normalize_title(r_companies_str)
            if normalized_companies:
                author_tokens  = normalized_authors.split()
                company_tokens = normalized_companies.split()
                matches = sum(1 for tok in author_tokens if tok in company_tokens)
                if matches:
                    score += 0.15 * (matches / max(len(author_tokens), 1))

        scored.append((score, result))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:5]

    return [
        {
            "media_id":   str(result.get("media_id", "")),
            "title":      result.get("title", ""),
            "year":       str(result.get("year") or result.get("release_date", "") or "")[:4],
            "image":      result.get("image", ""),
            "confidence": round(conf, 3),
            # Store source so callers can identify which backend matched
            "_source":    source,
        }
        for conf, result in top
    ]
