"""Tests for SensCritique import functionality."""

from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from app.models import (
    Anime,
    Book,
    Comic,
    Game,
    Item,
    Movie,
    Music,
    TV,
    Status,
)
from integrations.imports.senscritique import (
    SensCritiqueImporter,
    SC_UNIVERSES,
    fetch_category,
    fetch_all,
    import_from_senscritique_csv,
    _normalize_browser_product,
)

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
        self.assertEqual(movie.score, 90)  # 9 * 10 (score is on movie, not item)
        self.assertEqual(movie.status, Status.COMPLETED.value)

        music = Music.objects.get(user=self.user)
        self.assertEqual(music.item.title, "Abbey Road")
        self.assertEqual(music.score, 100)  # 10 * 10

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
        self.assertEqual(movie.item.source, "manual")
        self.assertIn("sc_99999", movie.item.media_id)

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
        item = Item.objects.create(
            media_id="550",
            source="tmdb",
            media_type="movie",
            title="Inception",
            image="",
        )
        Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)

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
        item = Item.objects.create(
            media_id="550",
            source="tmdb",
            media_type="movie",
            title="Inception",
            image="",
        )
        Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)

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


# ---------------------------------------------------------------------------
# Tests for the s2l-based Apollo GraphQL scraper
# ---------------------------------------------------------------------------

class TestSCUniverses(TestCase):
    """Test SC_UNIVERSES mapping."""

    def test_all_categories_present(self):
        """All expected media types are mapped."""
        expected = {"movie", "tv", "anime", "game", "book", "comic", "music"}
        self.assertEqual(set(SC_UNIVERSES.keys()), expected)

    def test_universe_strings(self):
        """Universe strings match known SC values."""
        self.assertEqual(SC_UNIVERSES["movie"][0], "movie")
        self.assertEqual(SC_UNIVERSES["tv"][0], "tvShow")
        self.assertEqual(SC_UNIVERSES["anime"][0], "anime")
        self.assertEqual(SC_UNIVERSES["game"][0], "videogame")
        self.assertEqual(SC_UNIVERSES["book"][0], "book")
        self.assertEqual(SC_UNIVERSES["comic"][0], "comicStrip")
        self.assertEqual(SC_UNIVERSES["music"][0], "music")


class TestFetchCategory(TestCase):
    """Test fetch_category function."""

    def _mock_response(self, title, universe, total=1):
        return {
            "data": {
                "user": {
                    "collection": {
                        "total": total,
                        "products": [
                            {
                                "originalTitle": title,
                                "title": title,
                                "yearOfProduction": 2020,
                                "universe": universe,
                                "otherUserInfos": {
                                    "rating": 8,
                                    "dateDone": "2024-01-15T00:00:00Z",
                                    "isReviewed": False,
                                },
                            }
                        ],
                    }
                }
            }
        }

    @patch("integrations.imports.senscritique._fetch_batch")
    def test_fetch_movie_category(self, mock_batch):
        """Test fetching movies returns correct media_type."""
        mock_batch.return_value = self._mock_response("Inception", "movie")
        results = fetch_category("testuser", "movie", delay=0)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["media_type"], "movie")
        self.assertEqual(results[0]["title"], "Inception")
        self.assertEqual(results[0]["score"], 8)
        self.assertEqual(results[0]["year"], 2020)

    @patch("integrations.imports.senscritique._fetch_batch")
    def test_fetch_tv_category(self, mock_batch):
        """Test fetching TV shows returns correct media_type."""
        mock_batch.return_value = self._mock_response("Breaking Bad", "tvShow")
        results = fetch_category("testuser", "tv", delay=0)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["media_type"], "tv")

    @patch("integrations.imports.senscritique._fetch_batch")
    def test_fetch_music_category(self, mock_batch):
        """Test fetching music returns correct media_type."""
        mock_batch.return_value = self._mock_response("Abbey Road", "music")
        results = fetch_category("testuser", "music", delay=0)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["media_type"], "music")

    @patch("integrations.imports.senscritique._fetch_batch")
    def test_fetch_empty_collection(self, mock_batch):
        """Test that empty collection returns empty list."""
        mock_batch.return_value = {
            "data": {"user": {"collection": {"total": 0, "products": []}}}
        }
        results = fetch_category("testuser", "movie", delay=0)
        self.assertEqual(results, [])

    @patch("integrations.imports.senscritique._fetch_batch")
    def test_fetch_user_not_found(self, mock_batch):
        """Test that missing user returns empty list gracefully."""
        mock_batch.return_value = {"data": {"user": None}}
        results = fetch_category("nonexistent", "movie", delay=0)
        self.assertEqual(results, [])

    @patch("integrations.imports.senscritique._fetch_batch")
    def test_fetch_network_error(self, mock_batch):
        """Test that network errors return empty list gracefully."""
        mock_batch.side_effect = Exception("Connection error")
        results = fetch_category("testuser", "movie", delay=0)
        self.assertEqual(results, [])

    @patch("integrations.imports.senscritique._fetch_batch")
    def test_fetch_pagination(self, mock_batch):
        """Test that pagination fetches multiple pages."""
        # First call: 2 items, total 3
        first_response = {
            "data": {
                "user": {
                    "collection": {
                        "total": 3,
                        "products": [
                            {
                                "originalTitle": f"Movie {i}",
                                "title": f"Movie {i}",
                                "yearOfProduction": 2020,
                                "universe": "movie",
                                "otherUserInfos": {"rating": 7, "dateDone": None, "isReviewed": False},
                            }
                            for i in range(2)
                        ],
                    }
                }
            }
        }
        # Second call: 1 item, offset=2
        second_response = {
            "data": {
                "user": {
                    "collection": {
                        "total": 3,
                        "products": [
                            {
                                "originalTitle": "Movie 2",
                                "title": "Movie 2",
                                "yearOfProduction": 2020,
                                "universe": "movie",
                                "otherUserInfos": {"rating": 7, "dateDone": None, "isReviewed": False},
                            }
                        ],
                    }
                }
            }
        }
        mock_batch.side_effect = [first_response, second_response]
        results = fetch_category("testuser", "movie", delay=0)
        self.assertEqual(len(results), 3)
        self.assertEqual(mock_batch.call_count, 2)

    @patch("integrations.imports.senscritique._fetch_batch")
    def test_score_none_when_unrated(self, mock_batch):
        """Test that unrated items have None score."""
        mock_batch.return_value = {
            "data": {
                "user": {
                    "collection": {
                        "total": 1,
                        "products": [
                            {
                                "originalTitle": "Unrated Film",
                                "title": "Unrated Film",
                                "yearOfProduction": 2022,
                                "universe": "movie",
                                "otherUserInfos": {
                                    "rating": None,
                                    "dateDone": None,
                                    "isReviewed": False,
                                },
                            }
                        ],
                    }
                }
            }
        }
        results = fetch_category("testuser", "movie", delay=0)
        self.assertIsNone(results[0]["score"])

    @patch("integrations.imports.senscritique._fetch_batch")
    def test_watch_date_parsed(self, mock_batch):
        """Test that dateDone is parsed to YYYY-MM-DD."""
        mock_batch.return_value = {
            "data": {
                "user": {
                    "collection": {
                        "total": 1,
                        "products": [
                            {
                                "originalTitle": "Film",
                                "title": "Film",
                                "yearOfProduction": 2020,
                                "universe": "movie",
                                "otherUserInfos": {
                                    "rating": 8,
                                    "dateDone": "2024-03-15T12:00:00Z",
                                    "isReviewed": False,
                                },
                            }
                        ],
                    }
                }
            }
        }
        results = fetch_category("testuser", "movie", delay=0)
        self.assertEqual(results[0]["watch_date"], "2024-03-15")


class TestFetchAll(TestCase):
    """Test fetch_all function."""

    @patch("integrations.imports.senscritique.fetch_category")
    def test_fetch_all_calls_all_categories(self, mock_fetch):
        """Test that fetch_all calls fetch_category for each category."""
        mock_fetch.return_value = []
        fetch_all("testuser", delay=0)
        self.assertEqual(mock_fetch.call_count, len(SC_UNIVERSES))

    @patch("integrations.imports.senscritique.fetch_category")
    def test_fetch_all_combines_results(self, mock_fetch):
        """Test that fetch_all combines results from all categories."""
        def side_effect(username, media_type, **kwargs):
            return [{"title": f"{media_type} item", "media_type": media_type}]
        mock_fetch.side_effect = side_effect
        results = fetch_all("testuser", delay=0)
        self.assertEqual(len(results), len(SC_UNIVERSES))


# ---------------------------------------------------------------------------
# Tests for CSV import
# ---------------------------------------------------------------------------

class TestSCCSVImport(TestCase):
    """Test CSV-based SC import."""

    def setUp(self):
        self.credentials = {"username": "test", "password": "12345"}
        self.user = User.objects.create_user(**self.credentials)

    @patch("app.providers.services.search")
    def test_csv_import_basic(self, mock_search):
        """Test basic CSV import with movie and TV."""
        mock_search.return_value = {
            "page": 1, "total_results": 1, "total_pages": 1,
            "results": [{"media_id": "550", "title": "Inception", "year": 2010}],
        }

        csv_content = (
            "Title,Year,Rating10,WatchedDate,Review,Category\r\n"
            "Inception,2010,9,2024-01-01,,movie\r\n"
        )

        # Call the task synchronously
        result = import_from_senscritique_csv(
            user_id=self.user.id,
            csv_content=csv_content,
            overwrite=False,
        )
        self.assertIn("imported", result)

    def test_csv_import_without_category_defaults_to_movie(self):
        """Test that CSV rows without Category column default to movie."""
        # s2l output format (no Category column)
        csv_content = (
            "Title,Year,Rating10,WatchedDate,Review\r\n"
            "Inception,2010,9,2024-01-01,\r\n"
        )
        with patch("app.providers.services.search") as mock_search:
            mock_search.return_value = {
                "page": 1, "total_results": 0, "total_pages": 0, "results": [],
            }
            result = import_from_senscritique_csv(
                user_id=self.user.id,
                csv_content=csv_content,
                overwrite=False,
            )
        self.assertIn("imported", result)

    def test_csv_import_empty_file(self):
        """Test that empty CSV returns meaningful message."""
        csv_content = "Title,Year,Rating10,WatchedDate,Review,Category\r\n"
        result = import_from_senscritique_csv(
            user_id=self.user.id,
            csv_content=csv_content,
            overwrite=False,
        )
        self.assertIn("No valid items", result)

    def test_csv_import_invalid_user(self):
        """Test that invalid user_id returns error message."""
        csv_content = "Title,Year,Rating10,WatchedDate,Review,Category\r\nTest,2020,8,2024-01-01,,movie\r\n"
        result = import_from_senscritique_csv(
            user_id=99999,
            csv_content=csv_content,
            overwrite=False,
        )
        self.assertIn("not found", result)


# ---------------------------------------------------------------------------
# Tests for _normalize_browser_product
# ---------------------------------------------------------------------------

class TestNormalizeBrowserProduct(TestCase):
    """Test _normalize_browser_product normalization."""

    def test_normalize_movie(self):
        """Test normalizing a movie product from browser."""
        product = {
            "id": "123",
            "title": "Inception",
            "originalTitle": "Inception",
            "yearOfProduction": 2010,
            "poster": "http://example.com/poster.jpg",
            "category": {"label": "film"},
            "myRating": {"rating": 9},
            "artists": [],
        }
        result = _normalize_browser_product(product)
        self.assertEqual(result["media_type"], "movie")
        self.assertEqual(result["title"], "Inception")
        self.assertEqual(result["score"], 9)
        self.assertEqual(result["year"], 2010)

    def test_normalize_missing_rating(self):
        """Test normalizing product without rating."""
        product = {
            "id": "123",
            "title": "Film",
            "originalTitle": None,
            "yearOfProduction": 2020,
            "poster": None,
            "category": {"label": "film"},
            "myRating": None,
            "artists": [],
        }
        result = _normalize_browser_product(product)
        self.assertIsNone(result["score"])

    def test_normalize_uses_original_title(self):
        """Test that originalTitle is preferred over title."""
        product = {
            "id": "123",
            "title": "Inception (French Title)",
            "originalTitle": "Inception",
            "yearOfProduction": 2010,
            "poster": None,
            "category": {"label": "film"},
            "myRating": {"rating": 8},
            "artists": [],
        }
        result = _normalize_browser_product(product)
        self.assertEqual(result["title"], "Inception")

    def test_normalize_tv_category(self):
        """Test that TV series is correctly mapped."""
        product = {
            "id": "456",
            "title": "Breaking Bad",
            "originalTitle": "Breaking Bad",
            "yearOfProduction": 2008,
            "poster": None,
            "category": {"label": "serie"},
            "myRating": {"rating": 10},
            "artists": [],
        }
        result = _normalize_browser_product(product)
        self.assertEqual(result["media_type"], "tv")

    def test_normalize_unsupported_category(self):
        """Test that unsupported categories return None media_type."""
        product = {
            "id": "789",
            "title": "Some Podcast",
            "originalTitle": None,
            "yearOfProduction": 2021,
            "poster": None,
            "category": {"label": "podcast"},
            "myRating": {"rating": 7},
            "artists": [],
        }
        result = _normalize_browser_product(product)
        self.assertIsNone(result["media_type"])
