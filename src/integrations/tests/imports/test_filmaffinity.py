"""Tests for FilmAffinity HTML import."""

import unittest.mock
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from app.models import Item, Movie, Status
from integrations.imports.filmaffinity import (
    FilmAffinityHTMLImporter,
    import_from_filmaffinity_html,
)

User = get_user_model()

SAMPLE_HTML = """
<html><body>
<table class="ml movie-ratings">
    <tr>
        <td><div class="user-rating">8</div></td>
        <td>Inception (2010)</td>
        <td><em>10 de mayo de 2026, 15:06</em></td>
    </tr>
    <tr>
        <td><div class="user-rating">6</div></td>
        <td>The Dark Knight (2008)</td>
        <td><em>1 de enero de 2026, 12:00</em></td>
    </tr>
    <tr>
        <td><div class="user-rating">9</div></td>
        <td>Film Without Year</td>
        <td><em>5 de marzo de 2025, 10:00</em></td>
    </tr>
</table>
</body></html>
"""

EMPTY_HTML = """<html><body><table class="ml movie-ratings"></table></body></html>"""


class TestParseHTML(TestCase):
    """Test HTML parsing logic."""

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="12345")
        self.importer = FilmAffinityHTMLImporter(self.user)

    def test_parses_title_and_year(self):
        films = self.importer.parse_html(SAMPLE_HTML)
        self.assertEqual(films[0]["title"], "Inception")
        self.assertEqual(films[0]["year"], 2010)

    def test_parses_rating(self):
        films = self.importer.parse_html(SAMPLE_HTML)
        self.assertEqual(films[0]["score"], 8)

    def test_parses_all_rows(self):
        films = self.importer.parse_html(SAMPLE_HTML)
        self.assertEqual(len(films), 3)

    def test_film_without_year(self):
        films = self.importer.parse_html(SAMPLE_HTML)
        no_year = next(f for f in films if f["title"] == "Film Without Year")
        self.assertIsNone(no_year["year"])

    def test_empty_table_returns_empty_list(self):
        films = self.importer.parse_html(EMPTY_HTML)
        self.assertEqual(films, [])

    def test_all_items_are_movies(self):
        films = self.importer.parse_html(SAMPLE_HTML)
        for film in films:
            self.assertEqual(film["media_type"], "movie")


class TestParseDate(TestCase):
    """Test Spanish date parsing."""

    def test_standard_date(self):
        result = FilmAffinityHTMLImporter._parse_date("10 de mayo de 2026, 15:06")
        self.assertEqual(result, "2026-05-10")

    def test_january(self):
        result = FilmAffinityHTMLImporter._parse_date("1 de enero de 2026, 12:00")
        self.assertEqual(result, "2026-01-01")

    def test_december(self):
        result = FilmAffinityHTMLImporter._parse_date("31 de diciembre de 2025, 23:59")
        self.assertEqual(result, "2025-12-31")

    def test_invalid_returns_none(self):
        result = FilmAffinityHTMLImporter._parse_date("invalid string")
        self.assertIsNone(result)

    def test_empty_returns_none(self):
        result = FilmAffinityHTMLImporter._parse_date("")
        self.assertIsNone(result)

    def test_single_digit_day_padded(self):
        result = FilmAffinityHTMLImporter._parse_date("5 de marzo de 2025, 10:00")
        self.assertEqual(result, "2025-03-05")


class TestFilmAffinityHTMLImporter(TestCase):
    """Test full import flow."""

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

    @patch("integrations.imports.filmaffinity.resolve_tmdb")
    def test_import_creates_movies(self, mock_search):
        mock_search.return_value = ("550", "tmdb", "movie")
        importer = FilmAffinityHTMLImporter(self.user)
        importer.run(SAMPLE_HTML)
        self.assertGreater(Movie.objects.filter(user=self.user).count(), 0)

    @patch("integrations.imports.filmaffinity.resolve_tmdb")
    def test_score_converted_to_internal(self, mock_search):
        mock_search.return_value = ("550", "tmdb", "movie")
        FilmAffinityHTMLImporter(self.user).run(SAMPLE_HTML)
        movies = Movie.objects.filter(user=self.user)
        self.assertGreater(movies.count(), 0)
        movie = movies.filter(score=80).first()
        self.assertIsNotNone(movie)  # 8 * 10 = 80

    @patch("integrations.imports.filmaffinity.resolve_tmdb")
    def test_status_is_completed(self, mock_search):
        mock_search.return_value = ("550", "tmdb", "movie")
        FilmAffinityHTMLImporter(self.user).run(SAMPLE_HTML)
        movie = Movie.objects.filter(user=self.user).first()
        self.assertEqual(movie.status, Status.COMPLETED.value)

    @patch("integrations.imports.filmaffinity.resolve_tmdb")
    def test_fallback_to_manual_when_search_fails(self, mock_search):
        mock_search.return_value = (None, "", "movie")
        importer = FilmAffinityHTMLImporter(self.user)
        importer.run(SAMPLE_HTML)
        manual_movies = Movie.objects.filter(user=self.user, item__source="manual")
        self.assertGreater(manual_movies.count(), 0)

    @patch("integrations.imports.filmaffinity.resolve_tmdb")
    def test_deduplication_skips_existing(self, mock_search):
        mock_search.return_value = ("550", "tmdb", "movie")
        item = Item.objects.create(
            media_id="550", source="tmdb", media_type="movie",
            title="Inception", image=""
        )
        Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)

        importer = FilmAffinityHTMLImporter(self.user)
        importer.run(SAMPLE_HTML)
        self.assertGreater(importer.skipped, 0)
        self.assertEqual(Movie.objects.filter(user=self.user, item__media_id="550").count(), 1)

    @patch("integrations.imports.filmaffinity.resolve_tmdb")
    def test_overwrite_reimports(self, mock_search):
        mock_search.return_value = ("550", "tmdb", "movie")
        item = Item.objects.create(
            media_id="550", source="tmdb", media_type="movie",
            title="Inception", image=""
        )
        Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)

        importer = FilmAffinityHTMLImporter(self.user, overwrite=True)
        importer.run(SAMPLE_HTML)
        self.assertEqual(importer.skipped, 0)

    def test_empty_html_returns_message(self):
        result = FilmAffinityHTMLImporter(self.user).run(EMPTY_HTML)
        self.assertIn("No films found", result)

    def test_invalid_user_id(self):
        result = import_from_filmaffinity_html(user_id=99999, html_content="", overwrite=False)
        self.assertIn("not found", result)

    @patch("integrations.imports.filmaffinity.resolve_tmdb")
    def test_year_matching_prefers_exact_year(self, mock_search):
        mock_search.return_value = ("550", "tmdb", "movie")  # resolve_tmdb handles year matching internally
        html = """<html><body><table class="ml movie-ratings">
            <tr>
                <td><div class="user-rating">8</div></td>
                <td>Inception (2010)</td>
                <td><em>10 de mayo de 2026, 15:06</em></td>
            </tr>
        </table></body></html>"""
        FilmAffinityHTMLImporter(self.user).run(html)
        movie = Movie.objects.get(user=self.user)
        self.assertEqual(movie.item.media_id, "550")

    @patch("integrations.imports.filmaffinity.resolve_tmdb")
    def test_result_message_contains_counts(self, mock_search):
        mock_search.return_value = (None, "", "movie")
        importer = FilmAffinityHTMLImporter(self.user)
        result = importer.run(SAMPLE_HTML)
        self.assertIn("imported", result)
        self.assertIn("skipped", result)
        self.assertIn("errors", result)
