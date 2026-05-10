from pathlib import Path

from django.test import TestCase

from app.models import MediaTypes
from app.providers import (
    hardcover,
    igdb,
    mal,
    mangaupdates,
    musicbrainz,
    openlibrary,
    senscritique,
    tmdb,
)

mock_path = Path(__file__).resolve().parent.parent / "mock_data"


class Search(TestCase):
    """Test the external API calls for media search."""

    def test_anime(self):
        """Test the search method for anime.

        Assert that all required keys are present in each entry.
        """
        response = mal.search(MediaTypes.ANIME.value, "Cowboy Bebop", 1)

        required_keys = {"media_id", "media_type", "title", "image"}

        for anime in response["results"]:
            self.assertTrue(all(key in anime for key in required_keys))

    def test_anime_not_found(self):
        """Test the search method for anime with no results."""
        response = mal.search(MediaTypes.ANIME.value, "q", 1)

        self.assertEqual(response["results"], [])

    def test_mangaupdates(self):
        """Test the search method for manga.

        Assert that all required keys are present in each entry.
        """
        response = mangaupdates.search("One Piece", 1)
        required_keys = {"media_id", "media_type", "title", "image"}

        for manga in response["results"]:
            self.assertTrue(all(key in manga for key in required_keys))

    def test_manga_not_found(self):
        """Test the search method for manga with no results."""
        response = mangaupdates.search("", 1)

        self.assertEqual(response["results"], [])

    def test_tv(self):
        """Test the search method for TV shows.

        Assert that all required keys are present in each entry.
        """
        response = tmdb.search(MediaTypes.TV.value, "Breaking Bad", 1)
        required_keys = {"media_id", "media_type", "title", "image"}

        for tv in response["results"]:
            self.assertTrue(all(key in tv for key in required_keys))

    def test_games(self):
        """Test the search method for games.

        Assert that all required keys are present in each entry.
        """
        response = igdb.search("Persona 5", 1)
        required_keys = {"media_id", "media_type", "title", "image"}

        for game in response["results"]:
            self.assertTrue(all(key in game for key in required_keys))

    def test_books(self):
        """Test the search method for books.

        Assert that all required keys are present in each entry.
        """
        response = openlibrary.search("The Name of the Wind", 1)
        required_keys = {"media_id", "media_type", "title", "image"}

        for book in response["results"]:
            self.assertTrue(all(key in book for key in required_keys))

    def test_comics(self):
        """Test the search method for comics.

        Assert that all required keys are present in each entry.
        """
        response = igdb.search("Batman", 1)
        required_keys = {"media_id", "media_type", "title", "image"}

        for comic in response["results"]:
            self.assertTrue(all(key in comic for key in required_keys))

    def test_hardcover(self):
        """Test the search method for books from Hardcover.

        Assert that all required keys are present in each entry.
        """
        response = hardcover.search("1984 George Orwell", 1)
        required_keys = {"media_id", "media_type", "title", "image"}

        self.assertTrue(len(response["results"]) > 0)

        for book in response["results"]:
            self.assertTrue(all(key in book for key in required_keys))

    def test_hardcover_not_found(self):
        """Test the search method for books from Hardcover with no results."""
        response = hardcover.search("xjkqzptmvnsieurytowahdbfglc", 1)
        self.assertEqual(response["results"], [])

    def test_music(self):
        """Test the search method for music.

        Assert that all required keys are present in each entry and pagination fields exist.
        """
        response = musicbrainz.search_music("The Beatles", 1)

        # Check pagination fields
        self.assertIn("page", response)
        self.assertIn("total_results", response)
        self.assertIn("total_pages", response)
        self.assertIn("results", response)

        self.assertEqual(response["page"], 1)
        self.assertIsInstance(response["results"], list)

        # Check required keys in each result
        required_keys = {"media_id", "title", "source", "image", "year", "artists", "type"}

        if response["results"]:  # If results exist
            for music in response["results"]:
                self.assertTrue(all(key in music for key in required_keys))
                self.assertEqual(music["source"], "musicbrainz")

    def test_music_pagination(self):
        """Test the search method for music with pagination."""
        # Test first page
        response_page1 = musicbrainz.search_music("Pink Floyd", 1)
        self.assertEqual(response_page1["page"], 1)
        self.assertIsInstance(response_page1["total_results"], int)
        self.assertGreaterEqual(response_page1["total_results"], 0)
        self.assertGreater(response_page1["total_pages"], 0)

        # Test second page if there are enough results
        if response_page1["total_pages"] > 1:
            response_page2 = musicbrainz.search_music("Pink Floyd", 2)
            self.assertEqual(response_page2["page"], 2)
            # Results should be different between pages or one could be empty
            self.assertIsInstance(response_page2["results"], list)

    def test_music_not_found(self):
        """Test the search method for music with no results."""
        response = musicbrainz.search_music("xjkqzptmvnsieurytowahdbfglc", 1)

        self.assertIn("results", response)
        self.assertEqual(response["results"], [])

    def test_senscritique_music(self):
        """Test the search method for music from SensCritique.

        Assert that all required keys are present in each entry and pagination fields exist.
        """
        try:
            response = senscritique.search_music("The Beatles", 1)
        except Exception as e:
            self.skipTest(f"SensCritique API unavailable or auth failed: {e}")

        # Check pagination fields
        self.assertIn("page", response)
        self.assertIn("total_results", response)
        self.assertIn("total_pages", response)
        self.assertIn("results", response)

        self.assertEqual(response["page"], 1)
        self.assertIsInstance(response["results"], list)

        # Check required keys in each result
        required_keys = {"media_id", "title", "source", "image", "year", "artists"}

        if response["results"]:  # If results exist
            for music in response["results"]:
                self.assertTrue(all(key in music for key in required_keys))
                self.assertEqual(music["source"], "senscritique")

    def test_senscritique_music_not_found(self):
        """Test the search method for music from SensCritique with no results."""
        try:
            response = senscritique.search_music("xjkqzptmvnsieurytowahdbfglc", 1)
        except Exception as e:
            self.skipTest(f"SensCritique API unavailable or auth failed: {e}")

        self.assertIn("results", response)
        self.assertEqual(response["results"], [])
