"""Tests for MusicBrainz provider."""

from unittest.mock import patch, MagicMock

from django.test import TestCase

from app.models import MediaTypes, Sources
from django.core.cache import cache
from app.providers.musicbrainz import (
    search_music,
    album,
    _format_artists,
    _artist_id,
    _cover_url,
    _get_artist_albums,
    RESULTS_PER_PAGE,
)


def _mock_release_group(
    mb_id="abc-123",
    title="Abbey Road",
    artist_name="The Beatles",
    artist_id="b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d",
    primary_type="Album",
    first_release="1969-09-26",
):
    return {
        "id": mb_id,
        "title": title,
        "primary-type": primary_type,
        "secondary-types": [],
        "first-release-date": first_release,
        "artist-credit": [
            {
                "name": artist_name,
                "artist": {"id": artist_id, "name": artist_name},
            }
        ],
        "genres": [{"name": "rock"}, {"name": "pop"}],
        "tags": [],
    }


class TestCoverUrl(TestCase):
    """Test _cover_url helper."""

    def test_returns_caa_url(self):
        url = _cover_url("abc-123")
        self.assertIn("abc-123", url)
        self.assertIn("coverartarchive.org", url)
        self.assertIn("front-250", url)


class TestFormatArtists(TestCase):
    """Test _format_artists helper."""

    def test_single_artist(self):
        rg = {
            "artist-credit": [
                {"name": "The Beatles", "artist": {"id": "x", "name": "The Beatles"}}
            ]
        }
        self.assertEqual(_format_artists(rg), ["The Beatles"])

    def test_multiple_artists(self):
        rg = {
            "artist-credit": [
                {"name": "Artist A", "artist": {"id": "1", "name": "Artist A"}},
                " & ",  # join string, not a dict
                {"name": "Artist B", "artist": {"id": "2", "name": "Artist B"}},
            ]
        }
        self.assertEqual(_format_artists(rg), ["Artist A", "Artist B"])

    def test_empty_credits(self):
        self.assertEqual(_format_artists({"artist-credit": []}), [])

    def test_missing_credits(self):
        self.assertEqual(_format_artists({}), [])

    def test_prefers_credit_name_over_artist_name(self):
        """Credit name (localised) should be preferred."""
        rg = {
            "artist-credit": [
                {"name": "Credit Name", "artist": {"id": "1", "name": "Artist Name"}}
            ]
        }
        self.assertEqual(_format_artists(rg), ["Credit Name"])


class TestArtistId(TestCase):
    """Test _artist_id helper."""

    def test_returns_artist_id(self):
        rg = {
            "artist-credit": [
                {"name": "The Beatles", "artist": {"id": "beatles-uuid", "name": "The Beatles"}}
            ]
        }
        self.assertEqual(_artist_id(rg), "beatles-uuid")

    def test_returns_none_when_empty(self):
        self.assertIsNone(_artist_id({"artist-credit": []}))

    def test_returns_none_when_no_artist_key(self):
        rg = {"artist-credit": [{"name": "Join string"}]}  # no "artist" key
        self.assertIsNone(_artist_id(rg))


class TestSearchMusic(TestCase):
    """Test search_music function."""

    def setUp(self):
        cache.clear()

    @patch("app.providers.musicbrainz._get")
    def test_returns_paginated_response(self, mock_get):
        mock_get.return_value = {
            "release-group-count": 1,
            "release-groups": [_mock_release_group()],
        }
        result = search_music("Beatles", page=1)
        self.assertIn("results", result)
        self.assertEqual(len(result["results"]), 1)

    @patch("app.providers.musicbrainz._get")
    def test_result_has_required_fields(self, mock_get):
        mock_get.return_value = {
            "release-group-count": 1,
            "release-groups": [_mock_release_group()],
        }
        result = search_music("Beatles")
        item = result["results"][0]
        self.assertIn("media_id", item)
        self.assertIn("title", item)
        self.assertIn("media_type", item)
        self.assertIn("source", item)
        self.assertIn("image", item)

    @patch("app.providers.musicbrainz._get")
    def test_media_type_is_music(self, mock_get):
        mock_get.return_value = {
            "release-group-count": 1,
            "release-groups": [_mock_release_group()],
        }
        result = search_music("Beatles")
        self.assertEqual(result["results"][0]["media_type"], MediaTypes.MUSIC.value)

    @patch("app.providers.musicbrainz._get")
    def test_source_is_musicbrainz(self, mock_get):
        mock_get.return_value = {
            "release-group-count": 1,
            "release-groups": [_mock_release_group()],
        }
        result = search_music("Beatles")
        self.assertEqual(result["results"][0]["source"], Sources.MUSICBRAINZ.value)

    @patch("app.providers.musicbrainz._get")
    def test_year_extracted_from_release_date(self, mock_get):
        mock_get.return_value = {
            "release-group-count": 1,
            "release-groups": [_mock_release_group(first_release="1969-09-26")],
        }
        result = search_music("Beatles")
        self.assertEqual(result["results"][0]["year"], "1969")

    @patch("app.providers.musicbrainz._get")
    def test_empty_results(self, mock_get):
        mock_get.return_value = {"release-group-count": 0, "release-groups": []}
        result = search_music("nonexistent xyz")
        self.assertEqual(result["results"], [])

    @patch("app.providers.musicbrainz._get")
    def test_type_label_with_secondary_types(self, mock_get):
        rg = _mock_release_group(mb_id="compilation-unique-id")
        rg["secondary-types"] = ["Compilation"]
        mock_get.return_value = {"release-group-count": 1, "release-groups": [rg]}
        result = search_music("Beatles secondary types unique query xyz")
        self.assertIn("Compilation", result["results"][0]["type"])

    @patch("app.providers.musicbrainz._get")
    def test_pagination_offset(self, mock_get):
        mock_get.return_value = {"release-group-count": 0, "release-groups": []}
        search_music("Beatles", page=3)
        call_params = mock_get.call_args[0][1]
        self.assertEqual(call_params["offset"], 2 * RESULTS_PER_PAGE)

    @patch("app.providers.musicbrainz._get")
    def test_uses_cache(self, mock_get):
        mock_get.return_value = {"release-group-count": 0, "release-groups": []}
        search_music("Beatles cached query xyz")
        search_music("Beatles cached query xyz")
        # Second call should hit cache, not _get again
        self.assertEqual(mock_get.call_count, 1)


class TestAlbum(TestCase):
    """Test album() metadata fetch."""

    def setUp(self):
        cache.clear()

    @patch("app.providers.musicbrainz._get_artist_albums")
    @patch("app.providers.musicbrainz._get")
    def test_returns_required_fields(self, mock_get, mock_artist_albums):
        mock_get.return_value = _mock_release_group()
        mock_artist_albums.return_value = []
        result = album("abc-123")

        required = ["media_id", "title", "source", "media_type", "image",
                    "synopsis", "genres", "details", "tracklist", "artist_links", "related"]
        for field in required:
            self.assertIn(field, result)

    @patch("app.providers.musicbrainz._get_artist_albums")
    @patch("app.providers.musicbrainz._get")
    def test_media_type_is_music(self, mock_get, mock_artist_albums):
        mock_get.return_value = _mock_release_group()
        mock_artist_albums.return_value = []
        result = album("abc-123")
        self.assertEqual(result["media_type"], MediaTypes.MUSIC.value)

    @patch("app.providers.musicbrainz._get_artist_albums")
    @patch("app.providers.musicbrainz._get")
    def test_artist_in_synopsis(self, mock_get, mock_artist_albums):
        mock_get.return_value = _mock_release_group(artist_name="The Beatles")
        mock_artist_albums.return_value = []
        result = album("abc-123")
        self.assertIn("The Beatles", result["synopsis"])

    @patch("app.providers.musicbrainz._get_artist_albums")
    @patch("app.providers.musicbrainz._get")
    def test_genres_from_genres_field(self, mock_get, mock_artist_albums):
        rg = _mock_release_group()
        rg["genres"] = [{"name": "rock"}, {"name": "pop"}]
        mock_get.return_value = rg
        mock_artist_albums.return_value = []
        result = album("abc-123")
        self.assertIn("rock", result["genres"])

    @patch("app.providers.musicbrainz._get_artist_albums")
    @patch("app.providers.musicbrainz._get")
    def test_genres_fallback_to_tags(self, mock_get, mock_artist_albums):
        rg = _mock_release_group(mb_id="tags-fallback-unique-id")
        rg["genres"] = []
        rg["tags"] = [{"name": "jazz"}, {"name": "soul"}]
        mock_get.return_value = rg
        mock_artist_albums.return_value = []
        result = album("tags-fallback-unique-id")
        self.assertIn("jazz", result["genres"])

    @patch("app.providers.musicbrainz._get_artist_albums")
    @patch("app.providers.musicbrainz._get")
    def test_artist_links_populated(self, mock_get, mock_artist_albums):
        mock_get.return_value = _mock_release_group(
            artist_name="The Beatles",
            artist_id="beatles-uuid",
        )
        mock_artist_albums.return_value = []
        result = album("abc-123")
        self.assertEqual(len(result["artist_links"]), 1)
        self.assertEqual(result["artist_links"][0]["id"], "beatles-uuid")
        self.assertEqual(result["artist_links"][0]["name"], "The Beatles")

    @patch("app.providers.musicbrainz._get_artist_albums")
    @patch("app.providers.musicbrainz._get")
    def test_recommendations_from_artist_albums(self, mock_get, mock_artist_albums):
        mock_get.return_value = _mock_release_group(mb_id="recs-unique-id", artist_id="beatles-uuid")
        mock_artist_albums.return_value = [
            {"media_id": "other-uuid", "title": "Let It Be", "media_type": "music"}
        ]
        result = album("recs-unique-id")
        # related is a dict - find the artist recommendations key
        related_flat = []
        for v in result["related"].values():
            related_flat.extend(v)
        self.assertEqual(len(related_flat), 1)
        self.assertEqual(related_flat[0]["title"], "Let It Be")

    @patch("app.providers.musicbrainz._get_artist_albums")
    @patch("app.providers.musicbrainz._get")
    def test_uses_cache(self, mock_get, mock_artist_albums):
        mock_get.return_value = _mock_release_group(mb_id="cache-test-uuid-unique")
        mock_artist_albums.return_value = []
        album("cache-test-uuid-unique")
        album("cache-test-uuid-unique")
        self.assertEqual(mock_get.call_count, 1)


class TestGetArtistAlbums(TestCase):
    """Test _get_artist_albums helper."""

    def setUp(self):
        cache.clear()

    @patch("app.providers.musicbrainz._get")
    def test_excludes_current_album(self, mock_get):
        mock_get.return_value = {
            "release-groups": [
                _mock_release_group(mb_id="current-id"),
                _mock_release_group(mb_id="other-id", title="Other Album"),
            ]
        }
        results = _get_artist_albums("artist-uuid", exclude_id="current-id")
        ids = [r["media_id"] for r in results]
        self.assertNotIn("current-id", ids)
        self.assertIn("other-id", ids)

    @patch("app.providers.musicbrainz._get")
    def test_respects_limit(self, mock_get):
        mock_get.return_value = {
            "release-groups": [
                _mock_release_group(mb_id=f"id-{i}", title=f"Album {i}")
                for i in range(20)
            ]
        }
        results = _get_artist_albums("artist-uuid", limit=5)
        self.assertLessEqual(len(results), 5)

    @patch("app.providers.musicbrainz._get")
    def test_returns_empty_on_error(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        results = _get_artist_albums("error-test-unique-artist-uuid")
        self.assertEqual(results, [])

    @patch("app.providers.musicbrainz._get")
    def test_result_has_media_type(self, mock_get):
        mock_get.return_value = {
            "release-groups": [_mock_release_group(mb_id="x")]
        }
        results = _get_artist_albums("artist-uuid")
        self.assertEqual(results[0]["media_type"], MediaTypes.MUSIC.value)
