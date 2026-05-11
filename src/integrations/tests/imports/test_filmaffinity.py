"""Tests for FilmAffinity CSV import."""

import unittest.mock
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from app.models import Item, Movie, TV, Status
from integrations.imports.filmaffinity import (
    FilmAffinityCSVImporter,
    import_from_filmaffinity_csv,
    FA_TYPE_MAP,
)

User = get_user_model()


class TestFATypeMap(TestCase):
    def test_movie_mapped(self):
        self.assertIn("movie", FA_TYPE_MAP)

    def test_tv_mapped(self):
        self.assertIn("tv", FA_TYPE_MAP)


class TestFilmAffinityCSVImporter(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="12345")

        def _bulk_create(objs, model, batch_size=500, default_user=None):
            model.objects.bulk_create(objs)
            return objs

        patcher = unittest.mock.patch(
            "simple_history.utils.bulk_create_with_history",
            side_effect=_bulk_create,
        )
        self.mock_bulk = patcher.start()
        self.addCleanup(patcher.stop)

    def _csv(self, rows, header="Title,Year,Rating,Type"):
        lines = [header] + [",".join(str(v) for v in r) for r in rows]
        return "\r\n".join(lines) + "\r\n"

    @patch("app.providers.services.search")
    def test_import_movie(self, mock_search):
        mock_search.return_value = {
            "results": [{"media_id": "550", "title": "Inception", "year": 2010}]
        }
        csv = self._csv([["Inception", 2010, 8, "movie"]])
        importer = FilmAffinityCSVImporter(self.user)
        importer.run(csv)
        self.assertEqual(importer.imported, 1)
        self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)

    @patch("app.providers.services.search")
    def test_import_tv(self, mock_search):
        mock_search.return_value = {
            "results": [{"media_id": "1396", "title": "Breaking Bad", "year": 2008}]
        }
        csv = self._csv([["Breaking Bad", 2008, 9, "tv"]])
        FilmAffinityCSVImporter(self.user).run(csv)
        self.assertEqual(TV.objects.filter(user=self.user).count(), 1)

    @patch("app.providers.services.search")
    def test_score_converted(self, mock_search):
        mock_search.return_value = {
            "results": [{"media_id": "550", "title": "Inception", "year": 2010}]
        }
        csv = self._csv([["Inception", 2010, 7, "movie"]])
        FilmAffinityCSVImporter(self.user).run(csv)
        movie = Movie.objects.get(user=self.user)
        self.assertEqual(movie.score, 70)

    @patch("app.providers.services.search")
    def test_no_score_stored_as_none(self, mock_search):
        mock_search.return_value = {
            "results": [{"media_id": "550", "title": "Inception", "year": 2010}]
        }
        csv = self._csv([["Inception", 2010, "", "movie"]])
        FilmAffinityCSVImporter(self.user).run(csv)
        movie = Movie.objects.get(user=self.user)
        self.assertIsNone(movie.score)

    @patch("app.providers.services.search")
    def test_fallback_to_manual(self, mock_search):
        mock_search.return_value = {"results": []}
        csv = self._csv([["Obscure Film XYZ", 2023, 6, "movie"]])
        importer = FilmAffinityCSVImporter(self.user)
        importer.run(csv)
        self.assertEqual(importer.imported, 1)
        movie = Movie.objects.get(user=self.user)
        self.assertEqual(movie.item.source, "manual")

    @patch("app.providers.services.search")
    def test_deduplication(self, mock_search):
        mock_search.return_value = {
            "results": [{"media_id": "550", "title": "Inception", "year": 2010}]
        }
        item = Item.objects.create(
            media_id="550", source="tmdb", media_type="movie",
            title="Inception", image=""
        )
        Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)

        csv = self._csv([["Inception", 2010, 9, "movie"]])
        importer = FilmAffinityCSVImporter(self.user)
        importer.run(csv)
        self.assertEqual(importer.skipped, 1)
        self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)

    @patch("app.providers.services.search")
    def test_overwrite(self, mock_search):
        mock_search.return_value = {
            "results": [{"media_id": "550", "title": "Inception", "year": 2010}]
        }
        item = Item.objects.create(
            media_id="550", source="tmdb", media_type="movie",
            title="Inception", image=""
        )
        Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)

        csv = self._csv([["Inception", 2010, 9, "movie"]])
        importer = FilmAffinityCSVImporter(self.user, overwrite=True)
        importer.run(csv)
        self.assertEqual(importer.skipped, 0)
        self.assertEqual(importer.imported, 1)

    def test_empty_csv(self):
        csv = "Title,Year,Rating,Type\r\n"
        result = FilmAffinityCSVImporter(self.user).run(csv)
        self.assertIn("No valid items", result)

    def test_invalid_user(self):
        result = import_from_filmaffinity_csv(user_id=99999, csv_content="", overwrite=False)
        self.assertIn("not found", result)

    @patch("app.providers.services.search")
    def test_year_matching(self, mock_search):
        mock_search.return_value = {
            "results": [
                {"media_id": "100", "title": "Batman", "year": 2022},
                {"media_id": "200", "title": "Batman", "year": 1989},
            ]
        }
        csv = self._csv([["Batman", 1989, 8, "movie"]])
        FilmAffinityCSVImporter(self.user).run(csv)
        movie = Movie.objects.get(user=self.user)
        self.assertEqual(movie.item.media_id, "200")

    @patch("app.providers.services.search")
    def test_unknown_type_defaults_to_movie(self, mock_search):
        mock_search.return_value = {
            "results": [{"media_id": "550", "title": "Inception", "year": 2010}]
        }
        csv = self._csv([["Inception", 2010, 8, "documentary"]])
        FilmAffinityCSVImporter(self.user).run(csv)
        self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
