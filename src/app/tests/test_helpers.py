from unittest.mock import MagicMock, patch
from datetime import date, datetime, timedelta

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase, override_settings
from django.utils import timezone

from app.helpers import (
    build_absolute_app_url,
    enrich_items_with_user_data,
    form_error_messages,
    format_search_response,
    get_configured_app_url,
    is_released_date,
    minutes_to_hhmm,
    redirect_back,
)
from app.models import Item, MediaTypes, Movie, Sources, Status


class HelpersTest(TestCase):
    """Test helper functions."""

    def test_minutes_to_hhmm(self):
        """Test conversion of minutes to HH:MM format."""
        # Test minutes only
        self.assertEqual(minutes_to_hhmm(30), "30min")

        # Test hours and minutes
        self.assertEqual(minutes_to_hhmm(90), "1h 30min")
        self.assertEqual(minutes_to_hhmm(125), "2h 05min")

        # Test zero
        self.assertEqual(minutes_to_hhmm(0), "0min")

    @override_settings(URLS=["https://yamtrack.example.com:8924"])
    def test_get_configured_app_url_from_urls(self):
        """Test configured public origin from URLS."""
        self.assertEqual(
            get_configured_app_url(),
            "https://yamtrack.example.com:8924",
        )

    @override_settings(URLS=["https://yamtrack.example.com"])
    def test_build_absolute_app_url_uses_configured_origin(self):
        """Test absolute URL construction behind reverse proxies."""
        request = MagicMock()

        result = build_absolute_app_url(request, "/import/trakt/private")

        self.assertEqual(result, "https://yamtrack.example.com/import/trakt/private")
        request.build_absolute_uri.assert_not_called()

    @override_settings(URLS=[])
    def test_build_absolute_app_url_falls_back_to_request(self):
        """Test request-based absolute URL construction without URLS."""
        request = MagicMock()
        request.build_absolute_uri.return_value = (
            "http://testserver/import/trakt/private"
        )

        result = build_absolute_app_url(request, "/import/trakt/private")

        self.assertEqual(result, "http://testserver/import/trakt/private")
        request.build_absolute_uri.assert_called_once_with("/import/trakt/private")

    @patch("app.helpers.url_has_allowed_host_and_scheme")
    @patch("app.helpers.HttpResponseRedirect")
    @patch("app.helpers.redirect")
    def test_redirect_back_with_next(self, _, mock_http_redirect, mock_url_check):
        """Test redirect_back with a 'next' parameter."""
        mock_url_check.return_value = True
        mock_http_redirect.return_value = "redirected"

        request = MagicMock()
        request.GET = {"next": "http://example.com/path?page=2&sort=name"}

        result = redirect_back(request)

        # Check that we redirected to the URL without the page parameter
        mock_http_redirect.assert_called_once()
        redirect_url = mock_http_redirect.call_args[0][0]
        self.assertEqual(redirect_url, "http://example.com/path?sort=name")
        self.assertEqual(result, "redirected")

    @patch("app.helpers.url_has_allowed_host_and_scheme")
    @patch("app.helpers.redirect")
    def test_redirect_back_without_next(self, mock_redirect, mock_url_check):
        """Test redirect_back without a 'next' parameter."""
        mock_url_check.return_value = False
        mock_redirect.return_value = "home_redirect"

        request = MagicMock()
        request.GET = {}

        result = redirect_back(request)

        mock_redirect.assert_called_once_with("home")
        self.assertEqual(result, "home_redirect")

    @patch("app.helpers.messages")
    def test_form_error_messages(self, mock_messages):
        """Test form_error_messages function."""
        form = MagicMock()
        form.errors = {
            "title": ["This field is required."],
            "release_date": ["Enter a valid date."],
        }
        request = HttpRequest()

        form_error_messages(form, request)

        # Check that error messages were added
        self.assertEqual(mock_messages.error.call_count, 2)
        mock_messages.error.assert_any_call(request, "Title: This field is required.")
        mock_messages.error.assert_any_call(
            request,
            "Release Date: Enter a valid date.",
        )


class EnrichItemsWithUserDataTest(TestCase):
    """Test the enrich_items_with_user_data function."""

    def setUp(self):
        """Set up test data."""
        self.credentials = {"username": "test", "password": "testpass"}
        self.user = get_user_model().objects.create_user(**self.credentials)
        self.request = MagicMock()
        self.request.user = self.user

        # Create test items in the database
        self.movie_item = Item.objects.create(
            media_id="238",
            source=Sources.TMDB.value,
            media_type=MediaTypes.MOVIE.value,
            title="Test Movie",
            image="http://example.com/movie.jpg",
        )

        self.season_item = Item.objects.create(
            media_id="67890",
            source=Sources.TMDB.value,
            media_type=MediaTypes.SEASON.value,
            title="Test TV Show",
            image="http://example.com/show.jpg",
            season_number=1,
        )

        # Create user tracking data for the movie
        self.movie_media = Movie.objects.create(
            item=self.movie_item,
            user=self.user,
            status=Status.COMPLETED.value,
            progress=1,
        )

    def test_enrich_items_with_user_data(self):
        """Test enriching items with multiple scenarios."""
        raw_items = [
            # Scenario 1: Existing movie with user tracking data
            {
                "media_id": "238",
                "source": Sources.TMDB.value,
                "media_type": MediaTypes.MOVIE.value,
                "title": "Test Movie",
                "image": "http://example.com/movie.jpg",
                "release_date": "2023-01-01",
                "rating": 8.5,
                "genre": "Action",
            },
            # Scenario 2: Existing season without user tracking data
            {
                "media_id": "67890",
                "source": Sources.TMDB.value,
                "media_type": MediaTypes.SEASON.value,
                "title": "Test TV Show",
                "season_title": "Season 1",
                "season_number": 1,
                "image": "http://example.com/show.jpg",
            },
            # Scenario 3: Non-existent item (raw data only)
            {
                "media_id": "99999",
                "source": Sources.TMDB.value,
                "media_type": MediaTypes.MOVIE.value,
                "title": "Unknown Movie",
                "image": "http://example.com/unknown.jpg",
                "description": "This movie doesn't exist in our database",
            },
        ]

        enriched_items = enrich_items_with_user_data(self.request, raw_items, "test")
        self.assertEqual(len(enriched_items), 3)

        # Scenario 1: Existing movie with user tracking data
        movie_enriched = enriched_items[0]
        self.assertEqual(movie_enriched["media"], self.movie_media)
        self.assertEqual(movie_enriched["item"]["title"], "Test Movie")
        self.assertEqual(movie_enriched["item"]["media_id"], "238")
        # Verify additional properties are preserved
        self.assertEqual(movie_enriched["item"]["release_date"], "2023-01-01")
        self.assertEqual(movie_enriched["item"]["rating"], 8.5)
        self.assertEqual(movie_enriched["item"]["genre"], "Action")

        # Scenario 2: Existing season without user tracking data
        season_enriched = enriched_items[1]
        self.assertEqual(
            season_enriched["media"],
            None,
        )  # No user tracking for this season
        self.assertEqual(
            season_enriched["item"]["season_title"],
            "Season 1",
        )  # Should use season_title
        self.assertEqual(season_enriched["item"]["season_number"], 1)

        # Scenario 3: Non-existent movie (raw data)
        unknown_movie_enriched = enriched_items[2]
        self.assertEqual(
            unknown_movie_enriched["item"]["media_id"],
            raw_items[2]["media_id"],
        )
        self.assertEqual(unknown_movie_enriched["media"], None)
        self.assertEqual(unknown_movie_enriched["item"]["title"], "Unknown Movie")
        self.assertEqual(unknown_movie_enriched["item"]["media_id"], "99999")
        self.assertEqual(
            unknown_movie_enriched["item"]["description"],
            "This movie doesn't exist in our database",
        )

    def test_hide_completed_recommendations_enabled(self):
        """Test that completed items are hidden when preference is enabled."""
        self.user.hide_completed_recommendations = True
        self.user.save()

        raw_items = [
            {
                "media_id": "238",  # This is our completed movie
                "source": Sources.TMDB.value,
                "media_type": MediaTypes.MOVIE.value,
                "title": "Test Movie",
                "image": "http://example.com/movie.jpg",
            },
            {
                "media_id": "99999",  # Not tracked
                "source": Sources.TMDB.value,
                "media_type": MediaTypes.MOVIE.value,
                "title": "Unknown Movie",
                "image": "http://example.com/unknown.jpg",
            },
        ]

        # When section is "recommendations", completed items should be hidden
        enriched_items = enrich_items_with_user_data(
            self.request, raw_items, "recommendations"
        )
        self.assertEqual(len(enriched_items), 1)
        self.assertEqual(enriched_items[0]["item"]["media_id"], "99999")

    def test_hide_completed_recommendations_disabled(self):
        """Test that completed items are shown when preference is disabled."""
        self.user.hide_completed_recommendations = False
        self.user.save()

        raw_items = [
            {
                "media_id": "238",  # This is our completed movie
                "source": Sources.TMDB.value,
                "media_type": MediaTypes.MOVIE.value,
                "title": "Test Movie",
                "image": "http://example.com/movie.jpg",
            },
            {
                "media_id": "99999",
                "source": Sources.TMDB.value,
                "media_type": MediaTypes.MOVIE.value,
                "title": "Unknown Movie",
                "image": "http://example.com/unknown.jpg",
            },
        ]

        # With preference disabled, all items should be returned
        enriched_items = enrich_items_with_user_data(
            self.request, raw_items, "recommendations"
        )
        self.assertEqual(len(enriched_items), 2)


class IsReleasedDateTest(TestCase):
    """Test the is_released_date function."""

    def test_is_released_date_with_datetime_naive(self):
        """Test is_released_date with naive datetime."""
        past_datetime = timezone.localtime() - timedelta(days=10)
        self.assertTrue(is_released_date(past_datetime.replace(tzinfo=None)))

        future_datetime = timezone.localtime() + timedelta(days=10)
        self.assertFalse(is_released_date(future_datetime.replace(tzinfo=None)))

    def test_is_released_date_with_datetime_aware(self):
        """Test is_released_date with timezone-aware datetime."""
        past_datetime = timezone.now() - timedelta(days=10)
        self.assertTrue(is_released_date(past_datetime))

        future_datetime = timezone.now() + timedelta(days=10)
        self.assertFalse(is_released_date(future_datetime))

    def test_is_released_date_with_date_object(self):
        """Test is_released_date with date object."""
        past_date = timezone.localdate() - timedelta(days=5)
        self.assertTrue(is_released_date(past_date))

        future_date = timezone.localdate() + timedelta(days=5)
        self.assertFalse(is_released_date(future_date))

    def test_is_released_date_with_year_only(self):
        """Test is_released_date with year-only string format."""
        past_year = str(timezone.localdate().year - 1)
        self.assertTrue(is_released_date(past_year))

        future_year = str(timezone.localdate().year + 1)
        self.assertFalse(is_released_date(future_year))

    def test_is_released_date_with_year_month(self):
        """Test is_released_date with YYYY-MM string format."""
        past_date_str = "2020-01"
        self.assertTrue(is_released_date(past_date_str))

        future_date_str = "2099-12"
        self.assertFalse(is_released_date(future_date_str))

    def test_is_released_date_with_full_date(self):
        """Test is_released_date with YYYY-MM-DD string format."""
        past_date_str = "2020-05-15"
        self.assertTrue(is_released_date(past_date_str))

        future_date_str = "2099-12-31"
        self.assertFalse(is_released_date(future_date_str))

    def test_is_released_date_with_invalid_string(self):
        """Test is_released_date with invalid date string format."""
        invalid_dates = [
            "not-a-date",
            "2020-13-01",  # Invalid month
            "2020-01-32",  # Invalid day
            "20-01-01",    # Invalid year format
            "",
        ]
        for invalid_date in invalid_dates:
            self.assertFalse(is_released_date(invalid_date))

    def test_is_released_date_with_none(self):
        """Test is_released_date with None value."""
        self.assertFalse(is_released_date(None))

    def test_is_released_date_with_custom_current_date(self):
        """Test is_released_date with explicit current_date parameter."""
        test_date = date(2020, 5, 15)
        current_date = date(2020, 5, 20)

        # Test date is before current date
        self.assertTrue(is_released_date(test_date, current_date))

        # Test date is after current date
        current_date = date(2020, 5, 10)
        self.assertFalse(is_released_date(test_date, current_date))

        # Test date equals current date
        current_date = date(2020, 5, 15)
        self.assertTrue(is_released_date(test_date, current_date))

    def test_is_released_date_with_today(self):
        """Test is_released_date with today's date."""
        today = timezone.localdate()
        self.assertTrue(is_released_date(today))


class FormatSearchResponseTest(TestCase):
    """Test the format_search_response function."""

    def test_format_search_response_single_page(self):
        """Test format_search_response with results on single page."""
        results = [{"id": 1, "title": "Result 1"}]
        response = format_search_response(page=1, per_page=10, total_results=5, results=results)

        self.assertEqual(response["page"], 1)
        self.assertEqual(response["total_results"], 5)
        self.assertEqual(response["total_pages"], 1)
        self.assertEqual(response["results"], results)

    def test_format_search_response_multiple_pages(self):
        """Test format_search_response with results spanning multiple pages."""
        results = [{"id": i, "title": f"Result {i}"} for i in range(10)]
        response = format_search_response(page=2, per_page=10, total_results=25, results=results)

        self.assertEqual(response["page"], 2)
        self.assertEqual(response["total_results"], 25)
        self.assertEqual(response["total_pages"], 3)
        self.assertEqual(len(response["results"]), 10)

    def test_format_search_response_no_results(self):
        """Test format_search_response with no results."""
        response = format_search_response(page=1, per_page=10, total_results=0, results=[])

        self.assertEqual(response["page"], 1)
        self.assertEqual(response["total_results"], 0)
        self.assertEqual(response["total_pages"], 1)
        self.assertEqual(response["results"], [])

    def test_format_search_response_exact_page_boundary(self):
        """Test format_search_response with results at exact page boundary."""
        # Exactly 2 pages of 10 results
        results = [{"id": i, "title": f"Result {i}"} for i in range(10)]
        response = format_search_response(page=2, per_page=10, total_results=20, results=results)

        self.assertEqual(response["page"], 2)
        self.assertEqual(response["total_pages"], 2)

    def test_format_search_response_partial_last_page(self):
        """Test format_search_response with partial results on last page."""
        results = [{"id": i, "title": f"Result {i}"} for i in range(5)]
        response = format_search_response(page=2, per_page=10, total_results=15, results=results)

        self.assertEqual(response["page"], 2)
        self.assertEqual(response["total_results"], 15)
        self.assertEqual(response["total_pages"], 2)
        self.assertEqual(len(response["results"]), 5)
