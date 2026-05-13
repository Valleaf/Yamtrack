"""Tests for SensCritique CSV import."""

import unittest.mock
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from app.models import Item, Movie, TV, Anime, Game, Book, Comic, Music, Status
from integrations.imports.senscritique import (
    SensCritiqueCSVImporter,
    import_from_senscritique_csv,
    CATEGORY_MAP,
)

User = get_user_model()


class TestCategoryMap(TestCase):
    """Test CATEGORY_MAP covers all expected types."""

    def test_all_types_mapped(self):
        expected = {"movie", "tv", "anime", "game", "book", "comic", "music"}
        self.assertEqual(set(CATEGORY_MAP.keys()), expected)


class TestSensCritiqueCSVImporter(TestCase):
    """Test SensCritiqueCSVImporter."""

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="12345")

        def _bulk_create(objs, model, batch_size=500, default_user=None):
            model.objects.bulk_create(objs)
            return objs

        patcher = unittest.mock.patch(
            "integrations.imports.helpers.bulk_create_with_history",
            side_effect=_bulk_create,
        )
        self.mock_bulk = patcher.start()
        self.addCleanup(patcher.stop)

    def _csv(self, rows, header="Title,Year,Rating10,WatchedDate,Review,Category"):
        lines = [header] + [",".join(str(v) for v in r) for r in rows]
        return "\r\n".join(lines) + "\r\n"

    @patch("app.providers.services.search")
    def test_import_movie(self, mock_search):
        mock_search.return_value = {
            "results": [{"media_id": "550", "title": "Inception", "year": 2010}]
        }
        csv = self._csv([["Inception", 2010, 9, "2024-01-01", "", "movie"]])
        importer = SensCritiqueCSVImporter(self.user)
        result = importer.run(csv)
        self.assertEqual(importer.imported, 1)
        self.assertIn("1 imported", result)
        self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)

    @patch("app.providers.services.search")
    def test_import_tv(self, mock_search):
        mock_search.return_value = {
            "results": [{"media_id": "1396", "title": "Breaking Bad", "year": 2008}]
        }
        csv = self._csv([["Breaking Bad", 2008, 10, "2024-01-01", "", "tv"]])
        SensCritiqueCSVImporter(self.user).run(csv)
        self.assertEqual(TV.objects.filter(user=self.user).count(), 1)

    @patch("app.providers.services.search")
    def test_score_converted(self, mock_search):
        mock_search.return_value = {
            "results": [{"media_id": "550", "title": "Inception", "year": 2010}]
        }
        csv = self._csv([["Inception", 2010, 8, "2024-01-01", "", "movie"]])
        SensCritiqueCSVImporter(self.user).run(csv)
        movie = Movie.objects.get(user=self.user)
        self.assertEqual(movie.score, 80)

    @patch("app.providers.services.search")
    def test_no_rating_stored_as_none(self, mock_search):
        mock_search.return_value = {
            "results": [{"media_id": "550", "title": "Inception", "year": 2010}]
        }
        csv = self._csv([["Inception", 2010, "", "2024-01-01", "", "movie"]])
        SensCritiqueCSVImporter(self.user).run(csv)
        movie = Movie.objects.get(user=self.user)
        self.assertIsNone(movie.score)

    @patch("app.providers.services.search")
    def test_no_category_defaults_to_movie(self, mock_search):
        """s2l output has no Category column — should default to movie."""
        mock_search.return_value = {
            "results": [{"media_id": "550", "title": "Inception", "year": 2010}]
        }
        csv = "Title,Year,Rating10,WatchedDate,Review\r\nInception,2010,9,2024-01-01,\r\n"
        SensCritiqueCSVImporter(self.user).run(csv)
        self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)

    @patch("app.providers.services.search")
    def test_fallback_to_manual_when_no_results(self, mock_search):
        mock_search.return_value = {"results": []}
        csv = self._csv([["Obscure Film XYZ", 2023, 7, "2024-01-01", "", "movie"]])
        importer = SensCritiqueCSVImporter(self.user)
        importer.run(csv)
        self.assertEqual(importer.imported, 1)
        movie = Movie.objects.get(user=self.user)
        self.assertEqual(movie.item.source, "manual")

    @patch("app.providers.services.search")
    def test_deduplication_skips_existing(self, mock_search):
        mock_search.return_value = {
            "results": [{"media_id": "550", "title": "Inception", "year": 2010}]
        }
        item = Item.objects.create(
            media_id="550", source="tmdb", media_type="movie",
            title="Inception", image=""
        )
        Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)

        csv = self._csv([["Inception", 2010, 9, "2024-01-01", "", "movie"]])
        importer = SensCritiqueCSVImporter(self.user)
        importer.run(csv)
        self.assertEqual(importer.skipped, 1)
        self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)

    @patch("app.providers.services.search")
    def test_overwrite_reimports_existing(self, mock_search):
        mock_search.return_value = {
            "results": [{"media_id": "550", "title": "Inception", "year": 2010}]
        }
        item = Item.objects.create(
            media_id="550", source="tmdb", media_type="movie",
            title="Inception", image=""
        )
        Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)

        csv = self._csv([["Inception", 2010, 9, "2024-01-01", "", "movie"]])
        importer = SensCritiqueCSVImporter(self.user, overwrite=True)
        importer.run(csv)
        self.assertEqual(importer.skipped, 0)
        self.assertEqual(importer.imported, 1)

    def test_empty_csv_returns_message(self):
        csv = "Title,Year,Rating10,WatchedDate,Review,Category\r\n"
        result = SensCritiqueCSVImporter(self.user).run(csv)
        self.assertIn("No valid items", result)

    def test_invalid_user_id(self):
        result = import_from_senscritique_csv(user_id=99999, csv_content="", overwrite=False)
        self.assertIn("not found", result)

    @patch("app.providers.services.search")
    def test_year_matching_picks_correct_result(self, mock_search):
        mock_search.return_value = {
            "results": [
                {"media_id": "100", "title": "Batman", "year": 2022},
                {"media_id": "200", "title": "Batman", "year": 1989},
            ]
        }
        csv = self._csv([["Batman", 1989, 8, "2024-01-01", "", "movie"]])
        SensCritiqueCSVImporter(self.user).run(csv)
        movie = Movie.objects.get(user=self.user)
        self.assertEqual(movie.item.media_id, "200")

    @patch("app.providers.services.search")
    def test_multiple_types_in_one_csv(self, mock_search):
        mock_search.return_value = {"results": [{"media_id": "1", "title": "X", "year": 2020}]}
        rows = [
            ["Film A", 2020, 8, "2024-01-01", "", "movie"],
            ["Show B", 2020, 7, "2024-01-01", "", "tv"],
            ["Album C", 2020, 9, "2024-01-01", "", "music"],
        ]
        csv = self._csv(rows)
        importer = SensCritiqueCSVImporter(self.user)
        importer.run(csv)
        self.assertEqual(importer.imported, 3)
        self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
        self.assertEqual(TV.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Music.objects.filter(user=self.user).count(), 1)
