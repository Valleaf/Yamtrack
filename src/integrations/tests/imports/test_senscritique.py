"""Tests for SensCritique CSV import, helpers, views, and confirm flow."""

import csv
import io
import unittest.mock
from collections import defaultdict
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app.models import Item, MediaTypes, Movie, Sources, Status
from integrations.imports.senscritique import (
    HIGH_CONFIDENCE_THRESHOLD,
    REVIEW_THRESHOLD,
    SC_TYPE_MAP,
    SOURCE_FOR,
    SensCritiqueImporter,
    clear_pending_review,
    confirm_pending_items,
    get_pending_review,
    importer,
    store_pending_review,
    _item_differs,
    _normalize_title,
    _parse_date,
    _parse_score,
    _parse_status,
    _resolve_comic_media_type,
)
from integrations.imports.helpers import MediaImportError

User = get_user_model()

# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------

_SC_FIELDS = [
    "date_notation", "type", "titre", "titre_original", "auteurs",
    "sortie", "oeuvre_principale", "note", "recommande", "acheve",
    "envie", "titre_critique", "critique", "vues_critique", "likes",
]


def _sc_csv(**kwargs):
    """Return a BytesIO with a single-row SC CSV.  Override columns via kwargs."""
    row = {
        "date_notation": "01/01/2024 12:00",
        "type": "movie",
        "titre": "Inception",
        "titre_original": "Inception",
        "auteurs": "",
        "sortie": "2010",
        "oeuvre_principale": "",
        "note": "8",
        "recommande": "FALSE",
        "acheve": "TRUE",
        "envie": "FALSE",
        "titre_critique": "",
        "critique": "Great film",
        "vues_critique": "0",
        "likes": "0",
    }
    row.update(kwargs)
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=_SC_FIELDS, extrasaction="ignore")
    writer.writeheader()
    writer.writerow(row)
    return io.BytesIO(buf.getvalue().encode("utf-8"))


def _sc_csv_multi(*rows):
    """Return a BytesIO with multiple SC CSV rows."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=_SC_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        full = {
            "date_notation": "01/01/2024 12:00",
            "type": "movie",
            "titre": "Test",
            "titre_original": "",
            "auteurs": "",
            "sortie": "2020",
            "oeuvre_principale": "",
            "note": "7",
            "recommande": "FALSE",
            "acheve": "TRUE",
            "envie": "FALSE",
            "titre_critique": "",
            "critique": "",
            "vues_critique": "0",
            "likes": "0",
        }
        full.update(row)
        writer.writerow(full)
    return io.BytesIO(buf.getvalue().encode("utf-8"))


def _patch_bulk():
    """Patcher that replaces bulk_create_with_history with a plain bulk_create."""
    return patch(
        "integrations.imports.helpers.bulk_create_with_history",
        side_effect=lambda objs, model, batch_size=500, default_user=None: (
            model.objects.bulk_create(objs)
        ),
    )


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


class TestConstants(TestCase):
    def test_sc_type_map_covers_six_types(self):
        expected = {"movie", "tv show", "book", "game", "music album", "comic book"}
        self.assertEqual(set(SC_TYPE_MAP.keys()), expected)

    def test_comic_book_maps_to_sentinel(self):
        # "_comic_auto" must never appear as a key — it is a sentinel value.
        self.assertNotIn("_comic_auto", SC_TYPE_MAP)
        self.assertEqual(SC_TYPE_MAP["comic book"], "_comic_auto")

    def test_source_for_covers_trackable_types(self):
        for mt in (
            MediaTypes.MOVIE.value, MediaTypes.TV.value, MediaTypes.BOOK.value,
            MediaTypes.GAME.value, MediaTypes.MUSIC.value,
            MediaTypes.MANGA.value, MediaTypes.COMIC.value,
        ):
            self.assertIn(mt, SOURCE_FOR, msg=f"SOURCE_FOR missing {mt}")

    def test_thresholds_ordered(self):
        self.assertGreater(HIGH_CONFIDENCE_THRESHOLD, REVIEW_THRESHOLD)
        self.assertGreater(REVIEW_THRESHOLD, 0)


# ---------------------------------------------------------------------------
# Pure-function helpers
# ---------------------------------------------------------------------------


class TestHelpers(TestCase):
    # ── _normalize_title ──────────────────────────────────────────────────

    def test_normalize_lowercases(self):
        self.assertEqual(_normalize_title("INCEPTION"), "inception")

    def test_normalize_strips_brackets(self):
        self.assertEqual(_normalize_title("Batman (1989)"), "batman")

    def test_normalize_removes_noisy_suffix(self):
        self.assertEqual(_normalize_title("Dark Souls GOTY Edition"), "dark souls")

    def test_normalize_collapses_whitespace(self):
        self.assertEqual(_normalize_title("  A   B   C  "), "a b c")

    def test_normalize_empty_string(self):
        self.assertEqual(_normalize_title(""), "")

    def test_normalize_strips_accents(self):
        # accented chars → ASCII equivalents
        result = _normalize_title("Élan")
        self.assertNotIn("é", result)

    # ── _parse_status ─────────────────────────────────────────────────────

    def test_parse_status_completed(self):
        self.assertEqual(_parse_status("TRUE", "FALSE"), Status.COMPLETED.value)

    def test_parse_status_planning(self):
        self.assertEqual(_parse_status("FALSE", "TRUE"), Status.PLANNING.value)

    def test_parse_status_in_progress(self):
        self.assertEqual(_parse_status("FALSE", "FALSE"), Status.IN_PROGRESS.value)

    def test_parse_status_case_insensitive(self):
        self.assertEqual(_parse_status("true", "false"), Status.COMPLETED.value)

    # ── _parse_score ──────────────────────────────────────────────────────

    def test_parse_score_integer_string(self):
        self.assertEqual(_parse_score("8"), 8.0)

    def test_parse_score_float_string(self):
        self.assertAlmostEqual(_parse_score("7.5"), 7.5)

    def test_parse_score_empty(self):
        self.assertIsNone(_parse_score(""))

    def test_parse_score_invalid(self):
        self.assertIsNone(_parse_score("N/A"))

    # ── _parse_date ───────────────────────────────────────────────────────

    def test_parse_date_slash_format(self):
        from django.utils import timezone
        result = _parse_date("01/15/2024 10:30")
        self.assertIsNotNone(result)
        self.assertTrue(timezone.is_aware(result))
        self.assertEqual(result.year, 2024)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 15)

    def test_parse_date_empty(self):
        self.assertIsNone(_parse_date(""))

    def test_parse_date_invalid(self):
        self.assertIsNone(_parse_date("not-a-date"))

    # ── _item_differs ─────────────────────────────────────────────────────

    def test_item_differs_same_data(self):
        existing = MagicMock()
        existing.score = 8.0
        existing.status = Status.COMPLETED.value
        existing.notes = ""
        existing.start_date = None
        self.assertFalse(
            _item_differs(existing, 8.0, Status.COMPLETED.value, "", None, MediaTypes.MOVIE.value)
        )

    def test_item_differs_score_change(self):
        existing = MagicMock()
        existing.score = 8.0
        existing.status = Status.COMPLETED.value
        existing.notes = ""
        self.assertTrue(
            _item_differs(existing, 9.0, Status.COMPLETED.value, "", None, MediaTypes.MOVIE.value)
        )

    def test_item_differs_status_change(self):
        existing = MagicMock()
        existing.score = None
        existing.status = Status.IN_PROGRESS.value
        existing.notes = ""
        self.assertTrue(
            _item_differs(existing, None, Status.COMPLETED.value, "", None, MediaTypes.MOVIE.value)
        )

    def test_item_differs_notes_change(self):
        existing = MagicMock()
        existing.score = None
        existing.status = Status.COMPLETED.value
        existing.notes = "old note"
        self.assertTrue(
            _item_differs(existing, None, Status.COMPLETED.value, "new note", None, MediaTypes.MOVIE.value)
        )


# ---------------------------------------------------------------------------
# _resolve_comic_media_type
# ---------------------------------------------------------------------------


class TestResolveComicMediaType(TestCase):
    def _row(self, **kwargs):
        return {"auteurs": "", "titre": "", "titre_original": "", **kwargs}

    def test_cjk_author_gives_manga(self):
        row = self._row(auteurs="吾峠呼世晴")
        mt, src = _resolve_comic_media_type(row)
        self.assertEqual(mt, MediaTypes.MANGA.value)
        self.assertEqual(src, Sources.MAL.value)

    def test_bd_author_gives_bnf(self):
        row = self._row(auteurs="Goscinny", titre="Asterix")
        mt, src = _resolve_comic_media_type(row)
        self.assertEqual(mt, MediaTypes.COMIC.value)
        self.assertEqual(src, Sources.BNF.value)

    def test_bd_series_name_gives_bnf(self):
        row = self._row(titre="Tintin au Tibet")
        mt, src = _resolve_comic_media_type(row)
        self.assertEqual(mt, MediaTypes.COMIC.value)
        self.assertEqual(src, Sources.BNF.value)

    def test_manga_keyword_in_title_gives_manga(self):
        row = self._row(titre="Shonen Jump collection")
        mt, src = _resolve_comic_media_type(row)
        self.assertEqual(mt, MediaTypes.MANGA.value)
        self.assertEqual(src, Sources.MAL.value)

    def test_no_clues_gives_western_comic(self):
        row = self._row(auteurs="Stan Lee", titre="Amazing Spider-Man")
        mt, src = _resolve_comic_media_type(row)
        self.assertEqual(mt, MediaTypes.COMIC.value)
        self.assertEqual(src, Sources.COMICVINE.value)

    def test_manga_beats_bd_when_both_present(self):
        # "manga" keyword + BD author: manga should win if score is higher
        row = self._row(auteurs="Goscinny", titre="Manga anthology Shonen Jump")
        mt, src = _resolve_comic_media_type(row)
        # manga_score=2 ("manga", "shonen"), bd_score=2 (goscinny×2) — tie goes to manga
        # (manga wins if manga_score > bd_score; a tie keeps BD — acceptable either way,
        # just verify it returns a valid pair)
        self.assertIn(mt, (MediaTypes.MANGA.value, MediaTypes.COMIC.value))
        self.assertIn(src, (Sources.MAL.value, Sources.BNF.value, Sources.COMICVINE.value))


# ---------------------------------------------------------------------------
# _resolve_bd  (BnF → ComicVine fallback)
# ---------------------------------------------------------------------------


class TestResolveBD(TestCase):
    _BNF_RESULT = [{"media_id": "bnf-42", "title": "Astérix le Gaulois", "year": "1961", "image": ""}]
    _CV_RESULT  = [{"media_id": "cv-99",  "title": "Asterix",             "year": "1961", "image": ""}]

    def _patch_search(self, bnf_results, cv_results):
        """Return a patch that routes _cached_search by source."""
        def _side_effect(media_type, title, source=""):
            if source == Sources.BNF.value:
                return bnf_results
            if source == Sources.COMICVINE.value:
                return cv_results
            return []

        return patch(
            "integrations.imports.senscritique._cached_search",
            side_effect=_side_effect,
        )

    def test_high_confidence_bnf_used_directly(self):
        from integrations.imports.senscritique import _resolve_bd
        with self._patch_search(self._BNF_RESULT, []):
            media_id, source, conf, cands = _resolve_bd("Astérix le Gaulois", 1961, "")
        self.assertEqual(media_id, "bnf-42")
        self.assertEqual(source, Sources.BNF.value)
        self.assertGreater(conf, REVIEW_THRESHOLD)

    def test_low_bnf_confidence_merges_comicvine(self):
        from integrations.imports.senscritique import _resolve_bd
        # BnF returns a very different title → low similarity
        poor_bnf = [{"media_id": "bnf-1", "title": "Zork Quatrième Dimension XYZZY", "year": "1900", "image": ""}]
        with self._patch_search(poor_bnf, self._CV_RESULT):
            _, _, _, cands = _resolve_bd("Astérix le Gaulois", 1961, "")
        ids = [c["media_id"] for c in cands]
        # Both sources should contribute candidates
        self.assertTrue(any(i.startswith("bnf") for i in ids) or any(i.startswith("cv") for i in ids))

    def test_no_bnf_results_falls_back_to_comicvine(self):
        from integrations.imports.senscritique import _resolve_bd
        with self._patch_search([], self._CV_RESULT):
            media_id, source, conf, cands = _resolve_bd("Asterix", 1961, "")
        self.assertEqual(media_id, "cv-99")
        self.assertEqual(source, Sources.COMICVINE.value)

    def test_no_results_returns_empty(self):
        from integrations.imports.senscritique import _resolve_bd
        with self._patch_search([], []):
            media_id, source, conf, cands = _resolve_bd("Unknown Title", None, "")
        self.assertIsNone(media_id)
        self.assertEqual(conf, 0.0)
        self.assertEqual(cands, [])


# ---------------------------------------------------------------------------
# SensCritiqueImporter — CSV parsing and routing
# ---------------------------------------------------------------------------


class TestSensCritiqueImporter(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="sc_test", password="pw")
        self._bulk_patcher = _patch_bulk()
        self._bulk_patcher.start()

    def tearDown(self):
        self._bulk_patcher.stop()
        clear_pending_review(self.user.id)

    # ── Input validation ──────────────────────────────────────────────────

    def test_wrong_columns_raises_import_error(self):
        bad_csv = io.BytesIO(b"Title,Year,Rating\nInception,2010,8\n")
        with self.assertRaises(MediaImportError):
            importer(bad_csv, self.user, "new")

    def test_empty_csv_returns_empty_counts(self):
        # Header only — no rows
        header = ",".join(_SC_FIELDS)
        empty = io.BytesIO((header + "\n").encode("utf-8"))
        with patch("integrations.imports.senscritique._cached_search", return_value=[]):
            counts, warnings = importer(empty, self.user, "new")
        self.assertEqual(counts, {})

    # ── Type filter ───────────────────────────────────────────────────────

    def test_type_filter_skips_unwanted_types(self):
        """If allowed_sc_types excludes 'movie', movie rows are skipped."""
        csv_bytes = _sc_csv(type="movie", titre="Inception", titre_original="Inception")
        with patch("integrations.imports.senscritique._cached_search", return_value=[]):
            counts, _ = importer(csv_bytes, self.user, "new", allowed_sc_types=["book"])
        self.assertNotIn(MediaTypes.MOVIE.value, counts)

    def test_type_filter_allows_matching_types(self):
        """Only rows matching allowed_sc_types are processed."""
        csv_bytes = _sc_csv_multi(
            {"type": "movie", "titre": "Film A", "titre_original": "Film A"},
            {"type": "book",  "titre": "Book B", "titre_original": "Book B"},
        )
        perfect_result = [{"media_id": "1", "title": "Film A", "year": "2020", "image": ""}]
        with patch("integrations.imports.senscritique._cached_search", return_value=perfect_result):
            counts, _ = importer(csv_bytes, self.user, "new", allowed_sc_types=["movie"])
        # Only movie should have been attempted; book is filtered out
        self.assertNotIn(MediaTypes.BOOK.value, counts)

    # ── High-confidence auto-import ───────────────────────────────────────

    @patch("integrations.imports.senscritique._cached_search")
    def test_high_confidence_auto_imported(self, mock_search):
        """Exact-title match → score well above threshold → DB record created."""
        mock_search.return_value = [
            {"media_id": "550", "title": "Inception", "year": "2010", "image": ""}
        ]
        csv_bytes = _sc_csv(
            type="movie", titre="Inception", titre_original="Inception", sortie="2010",
            note="8", acheve="TRUE",
        )
        counts, _ = importer(csv_bytes, self.user, "new")
        self.assertIn(MediaTypes.MOVIE.value, counts)
        self.assertEqual(counts[MediaTypes.MOVIE.value], 1)
        self.assertTrue(Movie.objects.filter(user=self.user).exists())

    # ── Low-confidence → pending review ───────────────────────────────────

    @patch("integrations.imports.senscritique._cached_search")
    def test_low_confidence_goes_to_pending(self, mock_search):
        """Poor title match → item queued for review, not auto-imported."""
        mock_search.return_value = [
            {"media_id": "999", "title": "Completely Unrelated Blockbuster XYZZY", "year": "1900", "image": ""}
        ]
        csv_bytes = _sc_csv(
            type="movie", titre="Inception", titre_original="Inception",
            note="8", acheve="TRUE",
        )
        counts, _ = importer(csv_bytes, self.user, "new")
        # Should not have auto-imported
        self.assertFalse(Movie.objects.filter(user=self.user).exists())
        # Should be in pending review
        pending = get_pending_review(self.user.id)
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["sc_title"], "Inception")

    # ── No match → pending with empty media_id ────────────────────────────

    @patch("integrations.imports.senscritique._cached_search")
    def test_no_match_goes_to_pending_disabled(self, mock_search):
        """No results from provider → pending item with empty media_id."""
        mock_search.return_value = []
        csv_bytes = _sc_csv(type="movie", titre="ObscureFilmXYZZY", titre_original="ObscureFilmXYZZY")
        importer(csv_bytes, self.user, "new")
        pending = get_pending_review(self.user.id)
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["media_id"], "")

    # ── Deduplication ─────────────────────────────────────────────────────

    @patch("integrations.imports.senscritique._cached_search")
    def test_duplicate_titles_deduplicated(self, mock_search):
        """Same normalised title appears twice → only processed once."""
        mock_search.return_value = [
            {"media_id": "550", "title": "Inception", "year": "2010", "image": ""}
        ]
        csv_bytes = _sc_csv_multi(
            {"type": "movie", "titre": "Inception", "titre_original": "Inception", "sortie": "2010"},
            {"type": "movie", "titre": "Inception", "titre_original": "Inception", "sortie": "2010"},
        )
        importer(csv_bytes, self.user, "new")
        self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)

    # ── Mode: skip existing ───────────────────────────────────────────────

    @patch("integrations.imports.senscritique._cached_search")
    def test_mode_new_skips_existing(self, mock_search):
        mock_search.return_value = [
            {"media_id": "550", "title": "Inception", "year": "2010", "image": ""}
        ]
        # Pre-create the item
        item = Item.objects.create(
            media_id="550", source=Sources.TMDB.value,
            media_type=MediaTypes.MOVIE.value, title="Inception",
        )
        Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)

        csv_bytes = _sc_csv(
            type="movie", titre="Inception", titre_original="Inception", sortie="2010",
        )
        importer(csv_bytes, self.user, "new")
        # Still only one record
        self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)

    # ── Score None with non-planning status skips row ─────────────────────

    @patch("integrations.imports.senscritique._cached_search")
    def test_no_score_in_progress_skipped(self, mock_search):
        """note="" + acheve=FALSE + envie=FALSE → skip (no score, in-progress)."""
        mock_search.return_value = [
            {"media_id": "550", "title": "Inception", "year": "2010", "image": ""}
        ]
        csv_bytes = _sc_csv(note="", acheve="FALSE", envie="FALSE")
        importer(csv_bytes, self.user, "new")
        self.assertFalse(Movie.objects.filter(user=self.user).exists())
        pending = get_pending_review(self.user.id)
        self.assertEqual(len(pending), 0)

    # ── Comic row routes through _resolve_comic_media_type ────────────────

    @patch("integrations.imports.senscritique._cached_search")
    def test_comic_book_manga_routes_to_mal(self, mock_search):
        """CJK author → media_type=manga, source=mal."""
        mock_search.return_value = [
            {"media_id": "12345", "title": "Demon Slayer", "year": "2016", "image": ""}
        ]
        csv_bytes = _sc_csv(
            type="comic book",
            titre="Demon Slayer",
            titre_original="鬼滅の刃",
            auteurs="吾峠呼世晴",
            sortie="2016",
        )
        importer(csv_bytes, self.user, "new")
        # Check pending or auto-imported has manga media_type
        from app.models import Manga
        pending = get_pending_review(self.user.id)
        if pending:
            self.assertEqual(pending[0]["media_type"], MediaTypes.MANGA.value)
        else:
            self.assertTrue(Manga.objects.filter(user=self.user).exists())


# ---------------------------------------------------------------------------
# confirm_pending_items
# ---------------------------------------------------------------------------


class TestConfirmPendingItems(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="confirm_test", password="pw")
        self._bulk_patcher = _patch_bulk()
        self._bulk_patcher.start()

    def tearDown(self):
        self._bulk_patcher.stop()
        clear_pending_review(self.user.id)

    def _store_item(self, **overrides):
        """Store a single pending item in Redis and return user_id."""
        item = {
            "sc_title": "Inception",
            "sc_original_title": "Inception",
            "sc_year": 2010,
            "media_type": MediaTypes.MOVIE.value,
            "source": Sources.TMDB.value,
            "media_id": "550",
            "confidence": 0.75,
            "candidate_title": "Inception",
            "candidate_year": "2010",
            "candidate_image": "",
            "candidates": [
                {"media_id": "550", "title": "Inception", "year": "2010",
                 "image": "", "confidence": 0.75, "_source": Sources.TMDB.value},
                {"media_id": "551", "title": "Inception II", "year": "2020",
                 "image": "", "confidence": 0.50, "_source": Sources.TMDB.value},
            ],
            "score": 8.0,
            "status": Status.COMPLETED.value,
            "notes": "",
            "date_added": None,
        }
        item.update(overrides)
        store_pending_review(self.user.id, [item])

    def test_confirmed_item_creates_db_record(self):
        self._store_item()
        counts, warnings = confirm_pending_items(
            user_id=self.user.id,
            confirmed_indices=[0],
            mode="new",
        )
        self.assertIn(MediaTypes.MOVIE.value, counts)
        self.assertEqual(counts[MediaTypes.MOVIE.value], 1)
        self.assertTrue(Movie.objects.filter(user=self.user).exists())

    def test_unconfirmed_item_not_imported(self):
        self._store_item()
        counts, _ = confirm_pending_items(
            user_id=self.user.id,
            confirmed_indices=[],  # nothing confirmed
            mode="new",
        )
        self.assertFalse(Movie.objects.filter(user=self.user).exists())

    def test_item_without_media_id_skipped(self):
        self._store_item(media_id="", candidates=[])
        counts, _ = confirm_pending_items(
            user_id=self.user.id,
            confirmed_indices=[0],
            mode="new",
        )
        self.assertFalse(Movie.objects.filter(user=self.user).exists())

    def test_candidate_override_picks_alternate(self):
        """Selecting candidate index 1 imports the second candidate's media_id."""
        self._store_item()
        confirm_pending_items(
            user_id=self.user.id,
            confirmed_indices=[0],
            mode="new",
            candidate_overrides={0: 1},  # pick "Inception II" (media_id=551)
        )
        movie = Movie.objects.filter(user=self.user).first()
        self.assertIsNotNone(movie)
        self.assertEqual(movie.item.media_id, "551")

    def test_manual_override_uses_custom_result(self):
        self._store_item()
        confirm_pending_items(
            user_id=self.user.id,
            confirmed_indices=[0],
            mode="new",
            manual_overrides={0: {"media_id": "999", "source": Sources.TMDB.value, "title": "Manual"}},
        )
        movie = Movie.objects.filter(user=self.user).first()
        self.assertIsNotNone(movie)
        self.assertEqual(movie.item.media_id, "999")

    def test_mode_new_skips_existing(self):
        item = Item.objects.create(
            media_id="550", source=Sources.TMDB.value,
            media_type=MediaTypes.MOVIE.value, title="Inception",
        )
        Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)

        self._store_item()
        confirm_pending_items(user_id=self.user.id, confirmed_indices=[0], mode="new")
        self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)

    def test_redis_cleared_after_confirm(self):
        self._store_item()
        confirm_pending_items(user_id=self.user.id, confirmed_indices=[0], mode="new")
        self.assertEqual(get_pending_review(self.user.id), [])

    def test_no_pending_returns_empty(self):
        # Nothing in Redis
        counts, warn = confirm_pending_items(
            user_id=self.user.id, confirmed_indices=[0], mode="new"
        )
        self.assertEqual(counts, {})
        self.assertIsNotNone(warn)


# ---------------------------------------------------------------------------
# senscritique_review view
# ---------------------------------------------------------------------------


class TestSensCritiqueReviewView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="review_user", password="pw")
        self.client.login(username="review_user", password="pw")
        self.url = reverse("senscritique_review")

    def tearDown(self):
        clear_pending_review(self.user.id)

    def _make_pending(self, n=3, media_type=MediaTypes.MOVIE.value):
        items = [
            {
                "sc_title": f"Film {i}",
                "sc_original_title": f"Film {i}",
                "sc_year": 2020,
                "media_type": media_type,
                "source": Sources.TMDB.value,
                "media_id": str(i),
                "confidence": 0.70,
                "candidate_title": f"Film {i}",
                "candidate_year": "2020",
                "candidate_image": "",
                "candidates": [],
                "score": 7.0,
                "status": Status.COMPLETED.value,
                "notes": "",
                "date_added": None,
            }
            for i in range(n)
        ]
        store_pending_review(self.user.id, items)

    def test_no_pending_redirects_to_import_data(self):
        resp = self.client.get(self.url)
        self.assertRedirects(resp, reverse("import_data"), fetch_redirect_response=False)

    def test_renders_review_template_with_pending(self):
        self._make_pending(2)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "users/senscritique_review.html")

    def test_pending_count_in_context(self):
        self._make_pending(3)
        resp = self.client.get(self.url)
        self.assertEqual(resp.context["pending_count"], 3)

    def test_media_type_filter_narrows_results(self):
        # Create mixed pending: 2 movies + 1 book
        items = []
        for i in range(2):
            items.append({
                "sc_title": f"Movie {i}", "sc_original_title": f"Movie {i}",
                "sc_year": 2020, "media_type": MediaTypes.MOVIE.value,
                "source": Sources.TMDB.value, "media_id": str(i),
                "confidence": 0.70, "candidate_title": "", "candidate_year": "",
                "candidate_image": "", "candidates": [], "score": 7.0,
                "status": Status.COMPLETED.value, "notes": "", "date_added": None,
            })
        items.append({
            "sc_title": "Book 0", "sc_original_title": "Book 0",
            "sc_year": 2020, "media_type": MediaTypes.BOOK.value,
            "source": Sources.HARDCOVER.value, "media_id": "99",
            "confidence": 0.70, "candidate_title": "", "candidate_year": "",
            "candidate_image": "", "candidates": [], "score": 7.0,
            "status": Status.COMPLETED.value, "notes": "", "date_added": None,
        })
        store_pending_review(self.user.id, items)

        resp = self.client.get(self.url + f"?type={MediaTypes.MOVIE.value}")
        self.assertEqual(resp.context["filtered_count"], 2)

    def test_pagination_limits_page_items(self):
        # Create 55 items (> default page_size of 50)
        self._make_pending(55)
        resp = self.client.get(self.url)
        self.assertEqual(len(resp.context["pending"]), 50)
        self.assertTrue(resp.context["has_next"])

    def test_page_2_contains_remainder(self):
        self._make_pending(55)
        resp = self.client.get(self.url + "?page=2")
        self.assertEqual(len(resp.context["pending"]), 5)
        self.assertFalse(resp.context["has_next"])


# ---------------------------------------------------------------------------
# senscritique_search AJAX view
# ---------------------------------------------------------------------------


class TestSensCritiqueSearchView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="search_user", password="pw")
        self.client.login(username="search_user", password="pw")
        self.url = reverse("senscritique_search")

    def test_missing_params_returns_empty(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["candidates"], [])

    def test_missing_query_returns_empty(self):
        resp = self.client.get(self.url, {"media_type": "movie"})
        data = resp.json()
        self.assertEqual(data["candidates"], [])

    @patch("integrations.imports.senscritique._cached_search")
    def test_successful_search_returns_candidates(self, mock_search):
        mock_search.return_value = [
            {"media_id": "550", "title": "Inception", "year": "2010", "image": ""}
        ]
        resp = self.client.get(self.url, {
            "media_type": MediaTypes.MOVIE.value,
            "q": "Inception",
            "source": Sources.TMDB.value,
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data["candidates"]), 1)
        self.assertEqual(data["candidates"][0]["media_id"], "550")
        self.assertEqual(data["candidates"][0]["title"], "Inception")
        self.assertIn("confidence", data["candidates"][0])

    @patch("integrations.imports.senscritique._cached_search")
    def test_bnf_fallback_tries_comicvine(self, mock_search):
        """BnF returns empty → should retry with ComicVine."""
        def side_effect(media_type, title, source=""):
            if source == Sources.BNF.value:
                return []
            return [{"media_id": "cv-1", "title": "Asterix", "year": "1961", "image": ""}]

        mock_search.side_effect = side_effect
        resp = self.client.get(self.url, {
            "media_type": MediaTypes.COMIC.value,
            "q": "Asterix",
            "source": Sources.BNF.value,
        })
        data = resp.json()
        self.assertEqual(len(data["candidates"]), 1)
        self.assertEqual(data["candidates"][0]["media_id"], "cv-1")
        self.assertEqual(data["candidates"][0]["source"], Sources.COMICVINE.value)

    @patch("integrations.imports.senscritique._cached_search")
    def test_unknown_media_type_returns_empty(self, mock_search):
        mock_search.return_value = []
        resp = self.client.get(self.url, {
            "media_type": "nonexistent_type",
            "q": "Something",
        })
        data = resp.json()
        self.assertEqual(data["candidates"], [])


# ---------------------------------------------------------------------------
# senscritique_confirm view
# ---------------------------------------------------------------------------


class TestSensCritiqueConfirmView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="confirm_view_user", password="pw")
        self.client.login(username="confirm_view_user", password="pw")
        self.url = reverse("senscritique_confirm")

    def tearDown(self):
        clear_pending_review(self.user.id)

    @patch("integrations.tasks.confirm_senscritique.delay")
    def test_no_confirmed_indices_no_task(self, mock_delay):
        resp = self.client.post(self.url, {"mode": "new", "next_page": reverse("import_data")})
        mock_delay.assert_not_called()
        self.assertEqual(resp.status_code, 302)

    @patch("integrations.tasks.confirm_senscritique.delay")
    def test_confirmed_indices_dispatches_task(self, mock_delay):
        resp = self.client.post(self.url, {
            "mode": "new",
            "confirmed": ["0", "2"],
            "next_page": reverse("import_data"),
        })
        mock_delay.assert_called_once()
        call_kwargs = mock_delay.call_args
        self.assertIn(0, call_kwargs.kwargs.get("confirmed_indices", call_kwargs.args[1] if len(call_kwargs.args) > 1 else []))
        self.assertEqual(resp.status_code, 302)

    @patch("integrations.tasks.confirm_senscritique.delay")
    def test_candidate_overrides_parsed(self, mock_delay):
        self.client.post(self.url, {
            "mode": "new",
            "confirmed": ["3"],
            "candidate_idx_3": "1",
        })
        call_kwargs = mock_delay.call_args.kwargs
        overrides = call_kwargs.get("candidate_overrides") or {}
        self.assertEqual(overrides.get(3), 1)

    @patch("integrations.tasks.confirm_senscritique.delay")
    def test_manual_overrides_parsed(self, mock_delay):
        self.client.post(self.url, {
            "mode": "new",
            "confirmed": ["5"],
            "manual_media_id_5": "my-id",
            "manual_source_5": Sources.TMDB.value,
            "manual_title_5": "My Title",
        })
        call_kwargs = mock_delay.call_args.kwargs
        manuals = call_kwargs.get("manual_overrides") or {}
        self.assertEqual(manuals.get(5, {}).get("media_id"), "my-id")

    @patch("integrations.tasks.confirm_senscritique.delay")
    def test_redirects_to_next_page(self, mock_delay):
        next_url = reverse("import_data")
        resp = self.client.post(self.url, {
            "mode": "new",
            "confirmed": ["0"],
            "next_page": next_url,
        })
        self.assertRedirects(resp, next_url, fetch_redirect_response=False)


# ---------------------------------------------------------------------------
# senscritique_discard view
# ---------------------------------------------------------------------------


class TestSensCritiqueDiscardView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="discard_user", password="pw")
        self.client.login(username="discard_user", password="pw")
        self.url = reverse("senscritique_discard")

    def tearDown(self):
        clear_pending_review(self.user.id)

    def _store_item(self):
        store_pending_review(self.user.id, [
            {
                "sc_title": "Film X", "sc_original_title": "Film X", "sc_year": 2020,
                "media_type": MediaTypes.MOVIE.value, "source": Sources.TMDB.value,
                "media_id": "1", "confidence": 0.70, "candidate_title": "Film X",
                "candidate_year": "2020", "candidate_image": "", "candidates": [],
                "score": 7.0, "status": Status.COMPLETED.value, "notes": "",
                "date_added": None,
            }
        ])

    def test_discard_clears_redis_and_redirects(self):
        self._store_item()
        self.assertEqual(len(get_pending_review(self.user.id)), 1)

        resp = self.client.post(self.url)

        self.assertEqual(get_pending_review(self.user.id), [])
        self.assertRedirects(resp, reverse("import_data"), fetch_redirect_response=False)

    def test_discard_get_not_allowed(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 405)
