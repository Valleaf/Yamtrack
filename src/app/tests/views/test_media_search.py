from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app.models import (
    MediaTypes,
    Sources,
)


class MediaSearchViewTests(TestCase):
    """Test the media search view."""

    def setUp(self):
        """Create a user and log in."""
        self.credentials = {"username": "test", "password": "12345"}
        self.user = get_user_model().objects.create_user(**self.credentials)
        self.client.login(**self.credentials)

    @patch("app.providers.services.search")
    def test_media_search_view(self, mock_search):
        """Test the media search view."""
        mock_search.return_value = {
            "page": 1,
            "total_results": 1,
            "total_pages": 1,
            "results": [
                {
                    "media_id": "238",
                    "title": "Test Movie",
                    "media_type": MediaTypes.MOVIE.value,
                    "source": Sources.TMDB.value,
                    "image": "http://example.com/image.jpg",
                },
            ],
        }

        response = self.client.get(
            reverse("search") + "?media_type=movie&q=test",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/search.html")

        self.user.refresh_from_db()
        self.assertEqual(self.user.last_search_type, MediaTypes.MOVIE.value)

        mock_search.assert_called_once_with(
            MediaTypes.MOVIE.value,
            "test",
            1,
            Sources.TMDB.value,
        )

    @patch("app.providers.services.search")
    def test_music_search_view(self, mock_search):
        """Test the media search view for music."""
        mock_search.return_value = {
            "page": 1,
            "total_results": 5,
            "total_pages": 1,
            "results": [
                {
                    "media_id": "12345",
                    "title": "Abbey Road",
                    "media_type": "music",
                    "source": "musicbrainz",
                    "image": "http://example.com/image.jpg",
                    "year": "1969",
                    "artists": ["The Beatles"],
                    "type": "Album",
                },
            ],
        }

        response = self.client.get(
            reverse("search") + "?media_type=music&q=Beatles",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/search.html")

        mock_search.assert_called_once_with(
            MediaTypes.MUSIC.value,
            "Beatles",
            1,
            "",
        )

    @patch("app.providers.services.search")
    def test_music_search_view_passes_musicbrainz_type_filter(self, mock_search):
        """Music search should pass the selected MusicBrainz type tab."""
        mock_search.return_value = {
            "page": 1,
            "total_results": 0,
            "total_pages": 1,
            "results": [],
        }

        response = self.client.get(
            reverse("search") + "?media_type=music&q=Beatles&mb_type=album",
        )

        self.assertEqual(response.status_code, 200)
        mock_search.assert_called_once_with(
            MediaTypes.MUSIC.value,
            "Beatles",
            1,
            "album",
        )
