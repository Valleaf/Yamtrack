from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase

from app.models import Item, MediaTypes, Music, Sources, Status
from events.models import MusicReleaseDiscovery
from events.music_discovery import sync_music_release_discoveries


class MusicReleaseDiscoveryTests(TestCase):
    """Test artist-wide release discovery without changing tracking state."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="music-discovery",
            password="password",
        )
        self.tracked_item = Item.objects.create(
            media_id="tracked-album",
            source=Sources.MUSICBRAINZ.value,
            media_type=MediaTypes.MUSIC.value,
            title="Tracked Album",
            image="https://example.com/tracked.jpg",
        )
        with patch(
            "app.providers.services.get_media_metadata",
            return_value={"max_progress": 1},
        ):
            Music.objects.create(
                item=self.tracked_item,
                user=self.user,
                status=Status.COMPLETED.value,
            )
        cache.set(
            "musicbrainz_music_tracked-album",
            {"artist_links": [{"id": "artist-1", "name": "Test Band"}]},
        )

    @patch("events.music_discovery.musicbrainz.artist_release_groups")
    def test_discovers_artist_releases_without_tracking_them(self, mock_groups):
        mock_groups.return_value = [
            {
                "media_id": "tracked-album",
                "title": "Tracked Album",
                "release_date": "2026-01-01",
                "year": "2026",
                "image": "https://example.com/tracked.jpg",
            },
            {
                "media_id": "new-album",
                "title": "New Album",
                "release_date": "2026-09-25",
                "year": "2026",
                "image": "https://example.com/new.jpg",
            },
        ]

        result = sync_music_release_discoveries()

        self.assertEqual(result, {"artists": 1, "releases": 1})
        discovery = MusicReleaseDiscovery.objects.get(user=self.user)
        self.assertEqual(discovery.item.media_id, "new-album")
        self.assertEqual(discovery.artist_names, "Test Band")
        self.assertFalse(
            Music.objects.filter(item__media_id="new-album", user=self.user).exists(),
        )
