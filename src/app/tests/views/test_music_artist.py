from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app.models import Item, Music, Sources, Status


class MusicArtistViewTests(TestCase):
    """Test artist pages and their user-rated album section."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="music-user",
            password="12345",
        )
        self.client.login(username="music-user", password="12345")

    @patch("app.providers.musicbrainz.artist")
    def test_artist_page_shows_rated_albums(self, mock_artist):
        mock_artist.return_value = {
            "artist_id": "artist-1",
            "name": "Test Artist",
            "discography": {
                "album": [
                    {
                        "media_id": "album-1",
                        "title": "Rated Album",
                        "image": "https://example.com/album.jpg",
                    },
                    {
                        "media_id": "album-2",
                        "title": "Untracked Album",
                        "image": "https://example.com/album-2.jpg",
                    },
                ],
            },
        }
        item = Item.objects.create(
            media_id="album-1",
            source=Sources.MUSICBRAINZ.value,
            media_type="music",
            title="Rated Album",
            image="https://example.com/album.jpg",
        )
        Music.objects.create(
            item=item,
            user=self.user,
            score=8.5,
            status=Status.PLANNING.value,
        )

        response = self.client.get(
            reverse("music_artist", kwargs={"artist_id": "artist-1", "name": "test-artist"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["rated_albums"]), 1)
        self.assertEqual(
            response.context["rated_albums"][0]["release"]["title"],
            "Rated Album",
        )
