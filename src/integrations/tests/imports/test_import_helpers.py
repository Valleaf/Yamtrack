"""Tests for integrations import helpers."""

from unittest.mock import MagicMock, patch, call
from collections import defaultdict

from django.contrib.auth import get_user_model
from django.test import TestCase

from app.models import Item, MediaTypes, Movie, Sources, Status, TV
from integrations.imports.helpers import (
    MediaImportError,
    MediaImportUnexpectedError,
    encrypt,
    decrypt,
    fernet,
    get_existing_media,
    should_process_media,
    join_with_commas_and,
)


class GetExistingMediaTest(TestCase):
    """Test the get_existing_media function."""

    def setUp(self):
        """Set up test data."""
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass",
        )

    def test_get_existing_media_empty_user(self):
        """Test get_existing_media with user who has no media."""
        existing = get_existing_media(self.user)

        # Should return nested dict structure but all empty
        self.assertIsInstance(existing, defaultdict)
        # Filter for actual media types (exclude seasons/episodes)
        actual_entries = sum(
            len(source_dict) for media_dict in existing.values()
            for source_dict in media_dict.values()
        )
        self.assertEqual(actual_entries, 0)

    def test_get_existing_media_single_movie(self):
        """Test get_existing_media with single movie tracked."""
        # Create test data
        item = Item.objects.create(
            media_id="238",
            source=Sources.TMDB.value,
            media_type=MediaTypes.MOVIE.value,
            title="Test Movie",
        )
        movie = Movie.objects.create(
            item=item,
            user=self.user,
            status=Status.COMPLETED.value,
        )

        existing = get_existing_media(self.user)

        # Check movie is in existing
        self.assertIn(MediaTypes.MOVIE.value, existing)
        self.assertIn(Sources.TMDB.value, existing[MediaTypes.MOVIE.value])
        self.assertEqual(
            existing[MediaTypes.MOVIE.value][Sources.TMDB.value]["238"],
            movie,
        )

    def test_get_existing_media_multiple_types(self):
        """Test get_existing_media with different media types."""
        # Create movie
        movie_item = Item.objects.create(
            media_id="238",
            source=Sources.TMDB.value,
            media_type=MediaTypes.MOVIE.value,
            title="Movie",
        )
        movie = Movie.objects.create(
            item=movie_item,
            user=self.user,
        )

        # Create TV show
        tv_item = Item.objects.create(
            media_id="1399",
            source=Sources.TMDB.value,
            media_type=MediaTypes.TV.value,
            title="TV Show",
        )
        tv = TV.objects.create(
            item=tv_item,
            user=self.user,
        )

        existing = get_existing_media(self.user)

        # Verify both types are present
        self.assertIn(MediaTypes.MOVIE.value, existing)
        self.assertIn(MediaTypes.TV.value, existing)
        self.assertEqual(len(existing[MediaTypes.MOVIE.value][Sources.TMDB.value]), 1)
        self.assertEqual(len(existing[MediaTypes.TV.value][Sources.TMDB.value]), 1)

    def test_get_existing_media_excludes_seasons_episodes(self):
        """Test get_existing_media excludes season and episode media types."""
        existing = get_existing_media(self.user)

        # Seasons and episodes should not be in the returned dict
        self.assertNotIn(MediaTypes.SEASON.value, existing)
        self.assertNotIn(MediaTypes.EPISODE.value, existing)


class ShouldProcessMediaTest(TestCase):
    """Test the should_process_media function."""

    def test_should_process_media_new_mode_not_exists(self):
        """Test should_process_media in new mode when media doesn't exist."""
        existing_media = defaultdict(lambda: defaultdict(dict))
        to_delete = defaultdict(lambda: defaultdict(set))

        result = should_process_media(
            existing_media,
            to_delete,
            media_type=MediaTypes.MOVIE.value,
            source=Sources.TMDB.value,
            media_id="238",
            mode="new",
        )

        self.assertTrue(result)

    def test_should_process_media_new_mode_exists(self):
        """Test should_process_media in new mode when media already exists."""
        existing_media = defaultdict(lambda: defaultdict(dict))
        existing_media[MediaTypes.MOVIE.value][Sources.TMDB.value]["238"] = MagicMock()
        to_delete = defaultdict(lambda: defaultdict(set))

        result = should_process_media(
            existing_media,
            to_delete,
            media_type=MediaTypes.MOVIE.value,
            source=Sources.TMDB.value,
            media_id="238",
            mode="new",
        )

        # In new mode, skip if exists
        self.assertFalse(result)

    def test_should_process_media_overwrite_mode(self):
        """Test should_process_media in overwrite mode marks for deletion."""
        existing_media = defaultdict(lambda: defaultdict(dict))
        mock_media = MagicMock()
        existing_media[MediaTypes.MOVIE.value][Sources.TMDB.value]["238"] = mock_media
        to_delete = defaultdict(lambda: defaultdict(set))

        result = should_process_media(
            existing_media,
            to_delete,
            media_type=MediaTypes.MOVIE.value,
            source=Sources.TMDB.value,
            media_id="238",
            mode="overwrite",
        )

        # In overwrite mode, process but mark for deletion
        self.assertTrue(result)
        self.assertIn("238", to_delete[MediaTypes.MOVIE.value][Sources.TMDB.value])


class EncryptionTest(TestCase):
    """Test encryption/decryption functionality."""

    def test_fernet_key_generation(self):
        """Test that fernet generates consistent key."""
        key1 = fernet()
        key2 = fernet()

        # Keys should be equal (derived from SECRET_KEY)
        self.assertEqual(key1.encrypt(b"test"), key2.encrypt(b"test"))

    def test_encrypt_decrypt_roundtrip(self):
        """Test encrypt/decrypt roundtrip."""
        original_value = "secret_token_123"

        encrypted = encrypt(original_value)
        self.assertNotEqual(encrypted, original_value)

        decrypted = decrypt(encrypted)
        self.assertEqual(decrypted, original_value)

    def test_encrypt_produces_bytes(self):
        """Test that encrypt returns bytes."""
        encrypted = encrypt("test")
        self.assertIsInstance(encrypted, bytes)

    def test_decrypt_handles_bytes(self):
        """Test that decrypt accepts bytes."""
        original = "test_value"
        encrypted = encrypt(original)

        decrypted = decrypt(encrypted)
        self.assertEqual(decrypted, original)


class JoinWithCommasAndTest(TestCase):
    """Test the join_with_commas_and function."""

    def test_join_single_item(self):
        """Test joining single item."""
        result = join_with_commas_and(["item1"])
        self.assertEqual(result, "item1")

    def test_join_two_items(self):
        """Test joining two items."""
        result = join_with_commas_and(["item1", "item2"])
        self.assertEqual(result, "item1 and item2")

    def test_join_three_items(self):
        """Test joining three items."""
        result = join_with_commas_and(["item1", "item2", "item3"])
        self.assertEqual(result, "item1, item2 and item3")

    def test_join_many_items(self):
        """Test joining many items."""
        items = ["A", "B", "C", "D", "E"]
        result = join_with_commas_and(items)
        self.assertEqual(result, "A, B, C, D and E")

    def test_join_empty_list(self):
        """Test joining empty list."""
        result = join_with_commas_and([])
        self.assertEqual(result, "")


class MediaImportErrorTest(TestCase):
    """Test custom exception classes."""

    def test_media_import_error_raised(self):
        """Test MediaImportError can be raised and caught."""
        with self.assertRaises(MediaImportError) as context:
            raise MediaImportError("Test error message")

        self.assertEqual(str(context.exception), "Test error message")

    def test_media_import_unexpected_error_raised(self):
        """Test MediaImportUnexpectedError can be raised and caught."""
        with self.assertRaises(MediaImportUnexpectedError) as context:
            raise MediaImportUnexpectedError("Unexpected error")

        self.assertEqual(str(context.exception), "Unexpected error")
