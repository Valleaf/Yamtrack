from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from app.models import (
    Item,
    MediaTypes,
    Movie,
    Sources,
    Status,
)


class MediaDetailsViewTests(TestCase):
    """Test the media details views."""

    def setUp(self):
        """Create a user and log in."""
        self.credentials = {"username": "test", "password": "12345"}
        self.user = get_user_model().objects.create_user(**self.credentials)
        self.client.login(**self.credentials)

    @patch("app.providers.services.get_media_metadata")
    def test_media_details_view(self, mock_get_metadata):
        """Test the media details view."""
        mock_get_metadata.return_value = {
            "media_id": "238",
            "title": "Test Movie",
            "media_type": MediaTypes.MOVIE.value,
            "source": Sources.TMDB.value,
            "image": "http://example.com/image.jpg",
            "overview": "Test overview",
            "release_date": "2023-01-01",
            "directors": [
                {"id": 42, "name": "Jane Doe", "image": "http://example.com/jane.jpg"},
            ],
        }

        response = self.client.get(
            reverse(
                "media_details",
                kwargs={
                    "source": Sources.TMDB.value,
                    "media_type": MediaTypes.MOVIE.value,
                    "media_id": "238",
                    "title": "test-movie",
                },
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/media_details.html")

        self.assertIn("media", response.context)
        self.assertEqual(response.context["media"]["title"], "Test Movie")
        self.assertContains(response, "/movie/director/42/jane-doe")

        mock_get_metadata.assert_called_once_with(
            MediaTypes.MOVIE.value,
            "238",
            Sources.TMDB.value,
        )

    @patch("app.providers.tmdb.person_credits")
    @patch("app.providers.services.get_media_metadata")
    def test_movie_director_pages_show_tracked_director_percentages(
        self,
        mock_get_metadata,
        mock_person_credits,
    ):
        """Test the movie director list and director pages."""
        self.movie_item1 = Item.objects.create(
            media_id="100",
            source=Sources.TMDB.value,
            media_type=MediaTypes.MOVIE.value,
            title="First Test Movie",
            image="http://example.com/first.jpg",
        )
        self.movie1 = Movie.objects.create(
            item=self.movie_item1,
            user=self.user,
            status=Status.COMPLETED.value,
            progress=1,
            score=8,
        )
        self.movie_item2 = Item.objects.create(
            media_id="101",
            source=Sources.TMDB.value,
            media_type=MediaTypes.MOVIE.value,
            title="Second Test Movie",
            image="http://example.com/second.jpg",
        )
        self.movie2 = Movie.objects.create(
            item=self.movie_item2,
            user=self.user,
            status=Status.IN_PROGRESS.value,
            progress=0,
            score=7,
        )

        self.movie_item3 = Item.objects.create(
            media_id="102",
            source=Sources.TMDB.value,
            media_type=MediaTypes.MOVIE.value,
            title="Uncached Test Movie",
            image="http://example.com/uncached.jpg",
        )
        self.movie3 = Movie.objects.create(
            item=self.movie_item3,
            user=self.user,
            status=Status.PLANNING.value,
            progress=0,
            score=0,
        )

        cache.set(
            f"{Sources.TMDB.value}_{MediaTypes.MOVIE.value}_100",
            {
                "media_id": "100",
                "title": "First Test Movie",
                "media_type": MediaTypes.MOVIE.value,
                "source": Sources.TMDB.value,
                "image": "http://example.com/first.jpg",
                "directors": [
                    {"id": 42, "name": "Jane Doe", "image": "http://example.com/jane.jpg"},
                ],
            },
        )
        cache.set(
            f"{Sources.TMDB.value}_{MediaTypes.MOVIE.value}_101",
            {
                "media_id": "101",
                "title": "Second Test Movie",
                "media_type": MediaTypes.MOVIE.value,
                "source": Sources.TMDB.value,
                "image": "http://example.com/second.jpg",
                "directors": [
                    {"id": 99, "name": "John Smith", "image": "http://example.com/john.jpg"},
                ],
            },
        )

        mock_person_credits.return_value = [
            {
                "media_id": "100",
                "title": "First Test Movie",
                "image": "http://example.com/first.jpg",
                "release_date": "2022-01-01",
                "source_url": "https://www.themoviedb.org/movie/100",
            },
            {
                "media_id": "101",
                "title": "Second Test Movie",
                "image": "http://example.com/second.jpg",
                "release_date": "2023-01-01",
                "source_url": "https://www.themoviedb.org/movie/101",
            },
        ]

        response = self.client.get(reverse("movie_directors"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/movie_directors.html")
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "John Smith")
        self.assertContains(response, "50.0%")

        response = self.client.get(reverse("movie_director", kwargs={"director_id": 42, "name": "jane-doe"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/movie_director.html")
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "50.0%")
        self.assertContains(response, "First Test Movie")
        self.assertContains(response, "2 directed movies")
        self.assertContains(response, "Untracked")

    @patch("app.providers.services.get_media_metadata")
    @patch("app.providers.tmdb.process_episodes")
    def test_season_details_view(self, mock_process_episodes, mock_get_metadata):
        """Test the season details view."""
        mock_get_metadata.return_value = {
            "title": "Test TV Show",
            "media_id": "1668",
            "source": Sources.TMDB.value,
            "media_type": MediaTypes.TV.value,
            "image": "http://example.com/image.jpg",
            "season/1": {
                "title": "Season 1",
                "media_id": "1668",
                "media_type": MediaTypes.SEASON.value,
                "source": Sources.TMDB.value,
                "image": "http://example.com/season.jpg",
                "episodes": [],
            },
        }

        mock_process_episodes.return_value = [
            {
                "media_id": "1668",
                "source": Sources.TMDB.value,
                "media_type": MediaTypes.EPISODE.value,
                "season_number": 1,
                "episode_number": 1,
                "name": "Episode 1",
                "air_date": "2023-01-01",
                "watched": False,
            },
        ]

        response = self.client.get(
            reverse(
                "season_details",
                kwargs={
                    "source": Sources.TMDB.value,
                    "media_id": "1668",
                    "title": "test-tv-show",
                    "season_number": 1,
                },
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/media_details.html")

        self.assertIn("media", response.context)
        self.assertEqual(response.context["media"]["title"], "Season 1")
        self.assertEqual(len(response.context["media"]["episodes"]), 1)

        mock_get_metadata.assert_called_once_with(
            "tv_with_seasons",
            "1668",
            Sources.TMDB.value,
            [1],
        )
