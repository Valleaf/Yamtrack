"""Tests for SensCritique import functionality."""

from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from app.models import (
    Anime,
    Book,
    Comic,
    Game,
    Movie,
    Music,
    TV,
    Status,
)
from integrations.imports.senscritique import SensCritiqueImporter

User = get_user_model()


class ImportSensCritique(TestCase):
    """Test importing media from SensCritique."""

    def setUp(self):
        """Create user for the tests."""
        self.credentials = {"username": "test", "password": "12345"}
        self.user = User.objects.create_user(**self.credentials)

    def _mock_products(self):
        """Return mock SC products for testing."""
        return [
            {
                "sc_id": "12345",
                "title": "Inception",
                "year": 2010,
                "poster": "http://example.com/poster.jpg",
                "media_type": "movie",
                "score": 9,
                "artists": [],
            },
            {
                "sc_id": "12346",
                "title": "Breaking Bad",
                "year": 2008,
                "poster": "http://example.com/tv.jpg",
                "media_type": "tv",
                "score": 10,
                "artists": [],
            },
            {
                "sc_id": "12347",
                "title": "Attack on Titan",
                "year": 2013,
                "poster": "http://example.com/anime.jpg",
                "media_type": "anime",
                "score": 8,
                "artists": ["Studio Wit"],
            },
            {
                "sc_id": "12348",
                "title": "Elden Ring",
                "year": 2022,
                "poster": "http://example.com/game.jpg",
                "media_type": "game",
                "score": 9,
                "artists": [],
            },
            {
                "sc_id": "12349",
                "title": "The Name of the Wind",
                "year": 2007,
                "poster": "http://example.com/book.jpg",
                "media_type": "book",
                "score": 8,
                "artists": ["Patrick Rothfuss"],
            },
            {
                "sc_id": "12350",
                "title": "Watchmen",
                "year": 1986,
                "poster": "http://example.com/comic.jpg",
                "media_type": "comic",
                "score": 9,
                "artists": ["Alan Moore"],
            },
            {
                "sc_id": "12351",
                "title": "Abbey Road",
                "year": 1969,
                "poster": "http://example.com/music.jpg",
                "media_type": "music",
                "score": 10,
                "artists": ["The Beatles"],
            },
            {
                "sc_id": "12352",
                "title": "Unsupported Type",
                "year": 2020,
                "poster": "http://example.com/podcast.jpg",
                "media_type": "podcast",
                "score": 5,
                "artists": [],
            },
        ]

    @patch("app.providers.senscritique.get_user_collection")
    @patch("app.providers.services.search")
    def test_import_multiple_media_types(self, mock_search, mock_get_collection):
        """Test importing multiple media types from SensCritique."""
        mock_get_collection.return_value = self._mock_products()

        def mock_search_side_effect(media_type, query, page=1):
            """Mock search results for different media types."""
            results_map = {
                "movie": [{"media_id": 550, "title": "Inception", "year": 2010}],
                "tv": [{"media_id": 1396, "title": "Breaking Bad", "year": 2008}],
                "anime": [{"media_id": 16498, "title": "Attack on Titan", "year": 2013}],
                "game": [{"media_id": "102674", "title": "Elden Ring", "year": 2022}],
                "book": [{"media_id": "OL45883W", "title": "The Name of the Wind", "year": 2007}],
                "comic": [{"media_id": "4050376", "title": "Watchmen", "year": 1986}],
                "music": [{"media_id": "12345", "title": "Abbey Road", "year": 1969}],
            }
            return {
                "page": page,
                "total_results": 1,
                "total_pages": 1,
                "results": results_map.get(media_type, []),
            }

        mock_search.side_effect = mock_search_side_effect

        importer = SensCritiqueImporter(self.user, "test_user")
        result_message = importer.run()

        # Check import stats
        self.assertEqual(importer.imported, 7)
        self.assertEqual(importer.skipped, 1)  # Podcast type not supported
        self.assertEqual(importer.errors, 0)
        self.assertIn("7 imported", result_message)

        # Check that each media type was created
        self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
        self.assertEqual(TV.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Anime.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Game.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Book.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Comic.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Music.objects.filter(user=self.user).count(), 1)

        # Check specific properties
        movie = Movie.objects.get(user=self.user)
        self.assertEqual(movie.item.title, "Inception")
        self.assertEqual(movie.item.score, 90)  # 9 * 10
        self.assertEqual(movie.status, Status.COMPLETED.value)

        music = Music.objects.get(user=self.user)
        self.assertEqual(music.item.title, "Abbey Road")
        self.assertEqual(music.item.score, 100)  # 10 * 10

    @patch("app.providers.senscritique.get_user_collection")
    @patch("app.providers.services.search")
    def test_import_fallback_to_manual(self, mock_search, mock_get_collection):
        """Test that items fall back to manual source when search fails."""
        mock_get_collection.return_value = [
            {
                "sc_id": "99999",
                "title": "Unknown Movie",
                "year": 2023,
                "poster": "http://example.com/unknown.jpg",
                "media_type": "movie",
                "score": 7,
                "artists": [],
            }
        ]

        # Return empty results from search
        mock_search.return_value = {
            "page": 1,
            "total_results": 0,
            "total_pages": 0,
            "results": [],
        }

        importer = SensCritiqueImporter(self.user, "test_user")
        result_message = importer.run()

        # Should fallback to manual source
        self.assertEqual(importer.imported, 1)
        movie = Movie.objects.get(user=self.user)
        self.assertEqual(movie.source, "manual")
        self.assertIn("sc_99999", movie.media_id)

    @patch("app.providers.senscritique.get_user_collection")
    @patch("app.providers.services.search")
    def test_import_deduplication(self, mock_search, mock_get_collection):
        """Test that duplicate items are skipped."""
        mock_get_collection.return_value = [
            {
                "sc_id": "12345",
                "title": "Inception",
                "year": 2010,
                "poster": "http://example.com/poster.jpg",
                "media_type": "movie",
                "score": 9,
                "artists": [],
            }
        ]

        mock_search.return_value = {
            "page": 1,
            "total_results": 1,
            "total_pages": 1,
            "results": [{"media_id": 550, "title": "Inception", "year": 2010}],
        }

        # Create the same movie as already existing
        Movie.objects.create(
            user=self.user,
            media_id=550,
            source="tmdb",
            title="Inception",
        )

        importer = SensCritiqueImporter(self.user, "test_user")
        result_message = importer.run()

        # Should skip the duplicate
        self.assertEqual(importer.imported, 0)
        self.assertEqual(importer.skipped, 1)
        self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)

    @patch("app.providers.senscritique.get_user_collection")
    @patch("app.providers.services.search")
    def test_import_with_overwrite(self, mock_search, mock_get_collection):
        """Test that overwrite flag replaces existing items."""
        mock_get_collection.return_value = [
            {
                "sc_id": "12345",
                "title": "Inception",
                "year": 2010,
                "poster": "http://example.com/poster.jpg",
                "media_type": "movie",
                "score": 9,
                "artists": [],
            }
        ]

        mock_search.return_value = {
            "page": 1,
            "total_results": 1,
            "total_pages": 1,
            "results": [{"media_id": 550, "title": "Inception", "year": 2010}],
        }

        # Create the same movie as already existing
        Movie.objects.create(
            user=self.user,
            media_id=550,
            source="tmdb",
            title="Inception",
        )

        importer = SensCritiqueImporter(self.user, "test_user", overwrite=True)
        result_message = importer.run()

        # Should import with overwrite
        self.assertEqual(importer.imported, 1)
        self.assertEqual(importer.skipped, 0)

    @patch("app.providers.senscritique.get_user_collection")
    def test_import_error_handling(self, mock_get_collection):
        """Test that import continues even when individual items error."""
        mock_get_collection.return_value = [
            {
                "sc_id": "12345",
                "title": None,  # This will cause an error
                "year": 2010,
                "poster": None,
                "media_type": "movie",
                "score": None,
                "artists": [],
            },
            {
                "sc_id": "12346",
                "title": "Valid Movie",
                "year": 2010,
                "poster": "http://example.com/poster.jpg",
                "media_type": "movie",
                "score": 8,
                "artists": [],
            },
        ]

        with patch("app.providers.services.search") as mock_search:
            mock_search.return_value = {
                "page": 1,
                "total_results": 1,
                "total_pages": 1,
                "results": [{"media_id": 550, "title": "Valid Movie", "year": 2010}],
            }

            importer = SensCritiqueImporter(self.user, "test_user")
            result_message = importer.run()

            # Should handle the error gracefully and continue
            self.assertGreater(importer.errors, 0)
            self.assertIn("error", result_message)
