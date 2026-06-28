"""Tests for app.image_proxy -- the lazy local cache/proxy for hot-linked covers.

See the module docstring in app/image_proxy.py for why this exists: BnF's
cover fallback chain (Open Library/Hardcover/ComicVine) doesn't reliably
set long-lived Cache-Control headers, so without this every page view
re-fetches the same cover from scratch.
"""

from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from app import image_proxy


def fake_image_response(
    content_type="image/jpeg", content=b"fake-image-bytes",
):
    resp = MagicMock()
    resp.headers = {"Content-Type": content_type}
    resp.content = content
    resp.raise_for_status = MagicMock()
    return resp


class ProxyUrlTests(TestCase):
    """Test the digest-mapping half of the proxy -- no HTTP involved."""

    def setUp(self):
        cache.clear()

    def test_returns_short_stable_path(self):
        """The same source URL always maps to the same short path.

        Short and stable matter: Item.image is a URLField(200), and the
        path must round-trip to the same browser-cacheable URL on every
        resolve_cover() call for the same identifier.
        """
        source = "https://covers.openlibrary.org/b/isbn/9782205000075-L.jpg"

        first = image_proxy.proxy_url(source)
        second = image_proxy.proxy_url(source)

        self.assertEqual(first, second)
        self.assertTrue(first.startswith("/covers/"))
        self.assertLess(len(first), 50)

    def test_records_the_source_mapping(self):
        """proxy_url() registers digest -> source so serve() can resolve it later."""
        source = "https://covers.openlibrary.org/b/isbn/9782205000075-L.jpg"

        public_url = image_proxy.proxy_url(source)
        digest = public_url.rsplit("/", 1)[-1]

        self.assertEqual(cache.get(f"imgproxy_src_{digest}"), source)


class ServeTests(TestCase):
    """Test the view: fetch-once, cache, and serve with a long Cache-Control."""

    def setUp(self):
        cache.clear()
        credentials = {"username": "test", "password": "12345"}
        get_user_model().objects.create_user(**credentials)
        self.client.login(**credentials)

    def test_unknown_digest_is_404(self):
        response = self.client.get(reverse("cover_proxy", args=["doesnotexist"]))

        self.assertEqual(response.status_code, 404)

    @patch("app.image_proxy.requests.get")
    def test_fetches_caches_and_serves_on_first_request(self, mock_get):
        mock_get.return_value = fake_image_response()
        source = "https://covers.openlibrary.org/b/isbn/9782205000075-L.jpg"
        public_url = image_proxy.proxy_url(source)

        response = self.client.get(public_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"fake-image-bytes")
        self.assertEqual(response["Content-Type"], "image/jpeg")
        self.assertIn("immutable", response["Cache-Control"])
        mock_get.assert_called_once()

    @patch("app.image_proxy.requests.get")
    def test_second_request_is_served_from_cache(self, mock_get):
        """The whole point: a repeat view doesn't re-fetch from upstream."""
        mock_get.return_value = fake_image_response()
        source = "https://covers.openlibrary.org/b/isbn/9782205000075-L.jpg"
        public_url = image_proxy.proxy_url(source)

        self.client.get(public_url)
        self.client.get(public_url)

        mock_get.assert_called_once()

    def test_disallowed_host_is_rejected(self):
        """Only the BnF fallback-chain hosts may be proxied -- not an open relay."""
        digest = image_proxy._digest("https://evil.example.com/x.jpg")  # noqa: SLF001
        cache.set(f"imgproxy_src_{digest}", "https://evil.example.com/x.jpg")

        response = self.client.get(reverse("cover_proxy", args=[digest]))

        self.assertEqual(response.status_code, 400)

    def test_non_https_source_is_rejected(self):
        digest = image_proxy._digest("http://covers.openlibrary.org/x.jpg")  # noqa: SLF001
        cache.set(f"imgproxy_src_{digest}", "http://covers.openlibrary.org/x.jpg")

        response = self.client.get(reverse("cover_proxy", args=[digest]))

        self.assertEqual(response.status_code, 400)

    @patch("app.image_proxy.requests.get")
    def test_non_image_response_is_404(self, mock_get):
        mock_get.return_value = fake_image_response(content_type="text/html")
        source = "https://covers.openlibrary.org/b/isbn/9782205000075-L.jpg"
        public_url = image_proxy.proxy_url(source)

        response = self.client.get(public_url)

        self.assertEqual(response.status_code, 404)
