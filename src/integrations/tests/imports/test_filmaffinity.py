"""Tests for FilmAffinity import functionality."""

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from app.models import Item, Movie, TV, Status
from integrations.imports.filmaffinity import (
    FilmAffinityImporter,
    import_from_filmaffinity,
    FA_TO_YAMTRACK,
)

User = get_user_model()


def _mock_product(title="Inception", year=2010, score=8, media_type="movie", fa_id="12345"):
    return {
        "fa_id": fa_id,
        "title": title,
        "year": year,
        "score": score,
        "media_type": media_type,
        "poster": "http://example.com/poster.jpg",
    }


def _mock_search_response(media_id=550, title="Inception", year=2010):
    return {
        "page": 1,
        "total_results": 1,
        "total_pages": 1,
        "results": [{"media_id": media_id, "title": title, "year": year}],
    }


class TestFAToYamtrack(TestCase):
    """Test FA_TO_YAMTRACK mapping."""

    def test_movie_mapped(self):
        self.assertEqual(FA_TO_YAMTRACK["movie"], "movie")

    def test_tv_mapped(self):
        self.assertEqual(FA_TO_YAMTRACK["tv"], "tv")


class TestFilmAffinityImporter(TestCase):
    """Test FilmAffinityImporter class."""

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="12345")

    @patch("app.providers.filmaffinity.scrape_user_ratings")
    @patch("app.providers.services.search")
    def test_import_movie(self, mock_search, mock_scrape):
        """Test importing a movie resolves to TMDB."""
        mock_scrape.return_value = [_mock_product()]
        mock_search.return_value = _mock_search_response()

        importer = FilmAffinityImporter(self.user, "12345")
        result = importer.run()

        self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
        movie = Movie.objects.get(user=self.user)
        self.assertEqual(movie.item.title, "Inception")
        self.assertEqual(movie.score, 80)  # 8 * 10
        self.assertEqual(movie.status, Status.COMPLETED.value)
        self.assertIn("imported", result)

    @patch("app.providers.filmaffinity.scrape_user_ratings")
    @patch("app.providers.services.search")
    def test_import_tv(self, mock_search, mock_scrape):
        """Test importing a TV show."""
        mock_scrape.return_value = [_mock_product(title="Breaking Bad", year=2008, media_type="tv", fa_id="99")]
        mock_search.return_value = _mock_search_response(media_id=1396, title="Breaking Bad", year=2008)

        importer = FilmAffinityImporter(self.user, "12345")
        importer.run()

        self.assertEqual(TV.objects.filter(user=self.user).count(), 1)

    @patch("app.providers.filmaffinity.scrape_user_ratings")
    @patch("app.providers.services.search")
    def test_score_conversion(self, mock_search, mock_scrape):
        """Test FA 1-10 score converted to internal 0-100."""
        mock_scrape.return_value = [_mock_product(score=7)]
        mock_search.return_value = _mock_search_response()

        FilmAffinityImporter(self.user, "12345").run()

        movie = Movie.objects.get(user=self.user)
        self.assertEqual(movie.score, 70)

    @patch("app.providers.filmaffinity.scrape_user_ratings")
    @patch("app.providers.services.search")
    def test_none_score(self, mock_search, mock_scrape):
        """Test that None score is stored as None."""
        mock_scrape.return_value = [_mock_product(score=None)]
        mock_search.return_value = _mock_search_response()

        FilmAffinityImporter(self.user, "12345").run()

        movie = Movie.objects.get(user=self.user)
        self.assertIsNone(movie.score)

    @patch("app.providers.filmaffinity.scrape_user_ratings")
    @patch("app.providers.services.search")
    def test_fallback_to_manual_when_search_fails(self, mock_search, mock_scrape):
        """Test that items with no TMDB match fall back to manual source."""
        mock_scrape.return_value = [_mock_product(title="Obscure Film", fa_id="99999")]
        mock_search.return_value = {"page": 1, "total_results": 0, "total_pages": 0, "results": []}

        FilmAffinityImporter(self.user, "12345").run()

        movie = Movie.objects.get(user=self.user)
        self.assertEqual(movie.item.source, "manual")
        self.assertIn("fa_99999", movie.item.media_id)

    @patch("app.providers.filmaffinity.scrape_user_ratings")
    @patch("app.providers.services.search")
    def test_deduplication(self, mock_search, mock_scrape):
        """Test that existing items are skipped."""
        mock_scrape.return_value = [_mock_product()]
        mock_search.return_value = _mock_search_response()

        item = Item.objects.create(media_id="550", source="tmdb", media_type="movie", title="Inception", image="")
        Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)

        importer = FilmAffinityImporter(self.user, "12345")
        importer.run()

        self.assertEqual(importer.skipped, 1)
        self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)

    @patch("app.providers.filmaffinity.scrape_user_ratings")
    @patch("app.providers.services.search")
    def test_overwrite(self, mock_search, mock_scrape):
        """Test that overwrite=True re-imports existing items."""
        mock_scrape.return_value = [_mock_product()]
        mock_search.return_value = _mock_search_response()

        item = Item.objects.create(media_id="550", source="tmdb", media_type="movie", title="Inception", image="")
        Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)

        importer = FilmAffinityImporter(self.user, "12345", overwrite=True)
        result = importer.run()

        self.assertEqual(importer.skipped, 0)
        self.assertIn("imported", result)

    @patch("app.providers.filmaffinity.scrape_user_ratings")
    def test_empty_collection(self, mock_scrape):
        """Test importing an empty FA profile."""
        mock_scrape.return_value = []

        importer = FilmAffinityImporter(self.user, "12345")
        result = importer.run()

        self.assertEqual(Movie.objects.filter(user=self.user).count(), 0)
        self.assertIn("0 imported", result)

    @patch("app.providers.filmaffinity.scrape_user_ratings")
    @patch("app.providers.services.search")
    def test_year_matching(self, mock_search, mock_scrape):
        """Test that year matching picks exact year match over first result."""
        mock_scrape.return_value = [_mock_product(title="Batman", year=1989)]
        mock_search.return_value = {
            "page": 1, "total_results": 3, "total_pages": 1,
            "results": [
                {"media_id": 100, "title": "Batman", "year": 2022},
                {"media_id": 200, "title": "Batman", "year": 1989},
                {"media_id": 300, "title": "Batman", "year": 2005},
            ],
        }

        FilmAffinityImporter(self.user, "12345").run()

        movie = Movie.objects.get(user=self.user)
        self.assertEqual(movie.item.media_id, "200")

    def test_invalid_user(self):
        """Test task with invalid user_id returns error."""
        result = import_from_filmaffinity(user_id=99999, fa_user_id="12345")
        self.assertIn("not found", result)
