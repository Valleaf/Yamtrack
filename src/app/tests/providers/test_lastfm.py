from unittest.mock import Mock, patch

from django.test import SimpleTestCase, override_settings

from app.providers.lastfm import user_stats


class LastFMProviderTests(SimpleTestCase):
    @override_settings(LASTFM_API_KEY="test-key")
    @patch("app.providers.lastfm.requests.get")
    def test_user_stats_normalizes_api_responses(self, mock_get):
        responses = [
            {"recenttracks": {"track": [{"name": "Recent"}]}},
            {"topartists": {"artist": [{"name": "Artist"}]}},
            {"topalbums": {"album": [{"name": "Album"}]}},
            {"toptracks": {"track": [{"name": "Track"}]}},
        ]
        mock_get.side_effect = [Mock(json=lambda payload=payload: payload) for payload in responses]

        result = user_stats("listener")

        self.assertEqual(result["username"], "listener")
        self.assertEqual(result["recent_tracks"][0]["name"], "Recent")
        self.assertEqual(result["top_artists"][0]["name"], "Artist")
        self.assertEqual(mock_get.call_count, 4)

    @override_settings(LASTFM_API_KEY="")
    def test_unconfigured_integration_is_empty(self):
        self.assertEqual(user_stats("listener"), {})
