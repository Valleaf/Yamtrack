"""Tests for the BnF provider's cover-resolution pipeline.

Covers identifier extraction from real-shaped SRU/DC XML, the
placeholder-detection heuristic in ``_probe_image_url``, and the
BnF-first / Open-Library-fallback priority in ``resolve_cover``.
"""

from unittest.mock import MagicMock, patch

import requests
from django.conf import settings
from django.core.cache import cache
from django.test import TestCase

from app.providers import bnf

SRU_RESPONSE_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<srw:searchRetrieveResponse xmlns:srw="http://www.loc.gov/zing/srw/">
    <srw:version>1.2</srw:version>
    <srw:numberOfRecords>1</srw:numberOfRecords>
    <srw:records>
        <srw:record>
            <srw:recordSchema>info:srw/schema/1/dc-v1.1</srw:recordSchema>
            <srw:recordData>
                <srw_dc:dc
                    xmlns:srw_dc="info:srw/schema/1/dc-schema"
                    xmlns:dc="http://purl.org/dc/elements/1.1/">
                    <dc:title>{title}</dc:title>
                    <dc:creator>Goscinny</dc:creator>
                    <dc:date>{date}</dc:date>
                    <dc:publisher>Dargaud</dc:publisher>
                    <dc:language>fre</dc:language>
                    <dc:subject>Bande dessinée</dc:subject>
                    <dc:description>Synopsis du document.</dc:description>
                    {identifiers}
                </srw_dc:dc>
            </srw:recordData>
        </srw:record>
    </srw:records>
</srw:searchRetrieveResponse>"""


def build_sru_xml(title="Astérix le Gaulois", date="1961", identifiers=""):
    """Build a minimal but realistically-shaped BnF SRU/DC XML response."""
    return SRU_RESPONSE_TEMPLATE.format(
        title=title,
        date=date,
        identifiers=identifiers,
    )


def fake_response(status_code=200, text=""):
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    resp.raise_for_status = MagicMock()
    if status_code >= requests.codes.bad_request:
        resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=resp,
        )
    return resp


def fake_head_response(status_code=200, content_type="image/jpeg", content_length="50000"):
    resp = MagicMock()
    resp.status_code = status_code
    headers = {}
    if content_type is not None:
        headers["Content-Type"] = content_type
    if content_length is not None:
        headers["Content-Length"] = content_length
    resp.headers = headers
    return resp


class ExtractIdentifiers(TestCase):
    """Test identifier extraction from parsed DC elements."""

    def _dc_el(self, identifiers_xml):
        xml = build_sru_xml(identifiers=identifiers_xml)
        root = bnf.ElementTree.fromstring(xml)
        return next(bnf._iter_dc_elements(root))  # noqa: SLF001

    def test_ark_and_isbn13(self):
        """ARK and a hyphenated ISBN-13 are extracted correctly."""
        dc_el = self._dc_el(
            "<dc:identifier>http://catalogue.bnf.fr/ark:/12148/cb12345678x</dc:identifier>"
            "<dc:identifier>978-2-205-00007-5</dc:identifier>",
        )
        identifiers = bnf.extract_identifiers(dc_el)
        self.assertEqual(identifiers["ark"], "ark:/12148/cb12345678x")
        self.assertEqual(identifiers["isbn13"], "978-2-205-00007-5")
        self.assertIsNone(identifiers["isbn10"])
        self.assertIsNone(identifiers["ean"])

    def test_isbn10(self):
        """A bare 10-character ISBN-10 (with trailing X) is detected."""
        dc_el = self._dc_el("<dc:identifier>2-205-0000-X</dc:identifier>")
        identifiers = bnf.extract_identifiers(dc_el)
        self.assertEqual(identifiers["isbn10"], "2-205-0000-X")
        self.assertIsNone(identifiers["isbn13"])

    def test_ean_from_description(self):
        """A commercial EAN embedded in dc:description is detected."""
        xml = build_sru_xml(
            identifiers="<dc:identifier>ark:/12148/cb12345678x</dc:identifier>",
        )
        # inject an EAN-bearing description as an extra element
        xml = xml.replace(
            "<dc:description>Synopsis du document.</dc:description>",
            "<dc:description>Synopsis du document.</dc:description>"
            "<dc:description>Code à barres commercial : EAN 3781507006999</dc:description>",
        )
        root = bnf.ElementTree.fromstring(xml)
        dc_el = next(bnf._iter_dc_elements(root))  # noqa: SLF001
        identifiers = bnf.extract_identifiers(dc_el)
        self.assertEqual(identifiers["ean"], "3781507006999")

    def test_thirteen_digit_non_978_979_is_ean_not_isbn(self):
        """A 13-digit identifier not starting with 978/979 is classified as EAN."""
        dc_el = self._dc_el("<dc:identifier>3781507006999</dc:identifier>")
        identifiers = bnf.extract_identifiers(dc_el)
        self.assertEqual(identifiers["ean"], "3781507006999")
        self.assertIsNone(identifiers["isbn13"])

    def test_no_identifiers(self):
        """Missing identifiers all resolve to None without raising."""
        dc_el = self._dc_el("")
        identifiers = bnf.extract_identifiers(dc_el)
        self.assertEqual(
            identifiers,
            {"isbn10": None, "isbn13": None, "ean": None, "ark": None},
        )


class ProbeImageUrl(TestCase):
    """Test the placeholder-detection heuristic."""

    @patch("requests.Session.head")
    def test_real_image_passes(self, mock_head):
        """A normal-sized image response is accepted."""
        mock_head.return_value = fake_head_response()
        self.assertTrue(bnf._probe_image_url("https://example.com/cover.jpg"))  # noqa: SLF001

    @patch("requests.Session.head")
    def test_tiny_placeholder_rejected(self, mock_head):
        """Open Library's ~43-byte placeholder GIF is rejected."""
        mock_head.return_value = fake_head_response(
            content_type="image/gif",
            content_length="43",
        )
        self.assertFalse(bnf._probe_image_url("https://covers.openlibrary.org/b/isbn/0-L.jpg"))  # noqa: SLF001

    @patch("requests.Session.head")
    def test_html_error_page_rejected(self, mock_head):
        """An HTML error/placeholder page is rejected."""
        mock_head.return_value = fake_head_response(content_type="text/html")
        self.assertFalse(bnf._probe_image_url("https://catalogue.bnf.fr/couverture"))  # noqa: SLF001

    @patch("requests.Session.head")
    def test_non_200_rejected(self, mock_head):
        """A non-200 status is rejected."""
        mock_head.return_value = fake_head_response(status_code=404)
        self.assertFalse(bnf._probe_image_url("https://example.com/missing.jpg"))  # noqa: SLF001

    @patch("requests.Session.head")
    def test_network_error_rejected(self, mock_head):
        """A network error never raises out of the probe — it's treated as no cover."""
        mock_head.side_effect = requests.exceptions.ConnectionError("boom")
        self.assertFalse(bnf._probe_image_url("https://example.com/cover.jpg"))  # noqa: SLF001

    @patch("requests.Session.get")
    @patch("requests.Session.head")
    def test_head_not_allowed_falls_back_to_get(self, mock_head, mock_get):
        """A 405 on HEAD falls back to a streamed GET."""
        mock_head.return_value = fake_head_response(
            status_code=requests.codes.method_not_allowed,
        )
        get_resp = fake_head_response()
        get_resp.close = MagicMock()
        mock_get.return_value = get_resp
        self.assertTrue(bnf._probe_image_url("https://example.com/cover.jpg"))  # noqa: SLF001
        get_resp.close.assert_called_once()


class ResolveCover(TestCase):
    """Test the Open-Library / Hardcover / ComicVine fallback chain and caching.

    BnF's own Service Couvertures API (get_bnf_cover) is intentionally not
    part of this chain -- see the note above get_bnf_cover's definition.
    A successful lookup is wrapped behind app.image_proxy, so assertions
    resolve the returned `/covers/<digest>` path back to its source URL
    via the imgproxy_src_ cache entry rather than comparing strings directly.
    """

    def setUp(self):
        cache.clear()

    @staticmethod
    def _source_url(public_url):
        """Resolve a `/covers/<digest>` proxy path back to its source URL."""
        digest = public_url.rsplit("/", 1)[-1]
        return cache.get(f"imgproxy_src_{digest}")

    @patch("app.providers.bnf.get_openlibrary_cover")
    def test_openlibrary_tried_first(self, mock_ol_cover):
        """Open Library is the first source tried."""
        mock_ol_cover.return_value = "https://covers.openlibrary.org/b/isbn/x-L.jpg"
        identifiers = {"isbn10": None, "isbn13": "978-2-205-00007-5", "ean": None, "ark": None}

        result = bnf.resolve_cover(identifiers, validate=True)

        self.assertTrue(result.startswith("/covers/"))
        self.assertEqual(
            self._source_url(result), "https://covers.openlibrary.org/b/isbn/x-L.jpg",
        )

    @patch("app.providers.bnf.get_hardcover_cover")
    @patch("app.providers.bnf.get_openlibrary_cover")
    def test_falls_back_to_hardcover(self, mock_ol_cover, mock_hc_cover):
        """When Open Library has no cover, Hardcover is tried next."""
        mock_ol_cover.return_value = None
        mock_hc_cover.return_value = "https://assets.hardcover.app/cover.jpg"
        identifiers = {"isbn10": None, "isbn13": "978-2-205-00007-5", "ean": None, "ark": None}

        result = bnf.resolve_cover(identifiers, validate=True)

        self.assertEqual(
            self._source_url(result), "https://assets.hardcover.app/cover.jpg",
        )

    @patch("app.providers.bnf.get_comicvine_cover")
    @patch("app.providers.bnf.get_hardcover_cover")
    @patch("app.providers.bnf.get_openlibrary_cover")
    def test_falls_back_to_comicvine_when_validated(
        self, mock_ol_cover, mock_hc_cover, mock_cv_cover,
    ):
        """With nothing from Open Library/Hardcover, ComicVine is tried last
        -- but only when validate=True, since it needs a series name."""
        mock_ol_cover.return_value = None
        mock_hc_cover.return_value = None
        mock_cv_cover.return_value = "https://comicvine.gamespot.com/cover.jpg"
        identifiers = {"isbn10": None, "isbn13": None, "ean": None, "ark": "ark:/12148/cb1x"}

        result = bnf.resolve_cover(
            identifiers, series_name="Lucky Luke", series_volume="9", validate=True,
        )

        self.assertEqual(
            self._source_url(result), "https://comicvine.gamespot.com/cover.jpg",
        )
        mock_cv_cover.assert_called_once_with("Lucky Luke", "9", None)

    @patch("app.providers.bnf.get_comicvine_cover")
    @patch("app.providers.bnf.get_hardcover_cover")
    @patch("app.providers.bnf.get_openlibrary_cover")
    def test_no_cover_anywhere_returns_img_none(
        self, mock_ol_cover, mock_hc_cover, mock_cv_cover,
    ):
        """When nothing has a cover, IMG_NONE is returned instead of breaking."""
        mock_ol_cover.return_value = None
        mock_hc_cover.return_value = None
        mock_cv_cover.return_value = None
        identifiers = {"isbn10": None, "isbn13": "978-2-205-00007-5", "ean": None, "ark": None}

        result = bnf.resolve_cover(identifiers, series_name="Some Series", validate=True)

        self.assertEqual(result, settings.IMG_NONE)

    @patch("app.providers.bnf.get_hardcover_cover")
    @patch("app.providers.bnf.get_openlibrary_cover")
    def test_confirmed_empty_result_is_cached(self, mock_ol_cover, mock_hc_cover):
        """A confirmed-no-cover result is cached so the probe isn't repeated."""
        mock_ol_cover.return_value = None
        mock_hc_cover.return_value = None
        identifiers = {"isbn10": None, "isbn13": "978-2-205-00007-5", "ean": None, "ark": None}

        bnf.resolve_cover(identifiers, validate=True)
        bnf.resolve_cover(identifiers, validate=True)

        self.assertEqual(mock_ol_cover.call_count, 1)
        self.assertEqual(mock_hc_cover.call_count, 1)

    @patch("app.providers.bnf.get_openlibrary_cover")
    def test_validated_result_is_proxied_and_stable(self, mock_ol_cover):
        """A real cover is wrapped behind a stable local proxy URL, whether
        served fresh or from the per-identifier cache."""
        mock_ol_cover.return_value = "https://covers.openlibrary.org/b/isbn/x-L.jpg"
        identifiers = {"isbn10": None, "isbn13": "978-2-205-00007-5", "ean": None, "ark": None}

        first = bnf.resolve_cover(identifiers, validate=True)
        second = bnf.resolve_cover(identifiers, validate=True)  # from cache

        self.assertEqual(first, second)
        self.assertEqual(mock_ol_cover.call_count, 1)

    @patch("app.providers.bnf.get_openlibrary_cover")
    def test_unvalidated_path_skips_cache(self, mock_ol_cover):
        """validate=False never reads or writes the per-identifier cover cache."""
        mock_ol_cover.return_value = "https://covers.openlibrary.org/b/isbn/x-L.jpg"
        identifiers = {"isbn10": None, "isbn13": "978-2-205-00007-5", "ean": None, "ark": None}

        bnf.resolve_cover(identifiers, validate=False)
        bnf.resolve_cover(identifiers, validate=False)

        self.assertEqual(mock_ol_cover.call_count, 2)
        mock_ol_cover.assert_called_with(identifiers, validate=False)

    @patch("app.providers.bnf._probe_image_url")  # noqa: SLF001
    def test_get_bnf_cover_priority_order(self, mock_probe):
        """get_bnf_cover tries ISBN before EAN before ARK."""
        identifiers = {
            "isbn10": None,
            "isbn13": "978-2-205-00007-5",
            "ean": "3781507006999",
            "ark": "ark:/12148/cb1x",
        }

        # Only the ARK candidate "succeeds" — confirms ISBN and EAN were
        # tried first and rejected before falling through to ARK.
        def probe_side_effect(url):
            return "idArk=" in url

        mock_probe.side_effect = probe_side_effect

        result = bnf.get_bnf_cover(identifiers, validate=True)

        self.assertIn("idArk=", result)
        self.assertEqual(mock_probe.call_count, 3)


class DcToResultCoverIntegration(TestCase):
    """Integration test: grid search results use the cheap, unvalidated path."""

    @patch("app.providers.bnf._probe_image_url")  # noqa: SLF001
    def test_search_result_does_not_probe(self, mock_probe):
        """Search results never trigger a network probe for the cover."""
        xml = build_sru_xml(
            identifiers="<dc:identifier>ark:/12148/cb12345678x</dc:identifier>"
            "<dc:identifier>978-2-205-00007-5</dc:identifier>",
        )
        root = bnf.ElementTree.fromstring(xml)
        dc_el = next(bnf._iter_dc_elements(root))  # noqa: SLF001

        result = bnf._dc_to_result(dc_el)  # noqa: SLF001

        mock_probe.assert_not_called()
        self.assertTrue(result["image"].startswith("/covers/"))
        digest = result["image"].rsplit("/", 1)[-1]
        self.assertIn("9782205000075", cache.get(f"imgproxy_src_{digest}"))


class ComicDetailCoverIntegration(TestCase):
    """Integration test: the comic detail page uses the validated path."""

    def setUp(self):
        cache.clear()

    @patch("requests.Session.head")
    @patch("requests.Session.get")
    def test_comic_resolves_validated_cover(self, mock_get, mock_head):
        xml = build_sru_xml(
            identifiers="<dc:identifier>ark:/12148/cb12345678x</dc:identifier>"
            "<dc:identifier>978-2-205-00007-5</dc:identifier>",
        )
        mock_get.return_value = fake_response(text=xml)
        mock_head.return_value = fake_head_response()  # looks like a real image

        data = bnf.comic("cb12345678x")

        # Open Library is tried first and "succeeds" here since the HEAD
        # probe is mocked to always look like a real image -- the
        # displayed image is a local proxy URL, not the raw Open Library
        # URL itself (see app.image_proxy).
        self.assertTrue(data["image"].startswith("/covers/"))
        digest = data["image"].rsplit("/", 1)[-1]
        source_url = cache.get(f"imgproxy_src_{digest}")
        self.assertIn("covers.openlibrary.org", source_url)
        self.assertIn("9782205000075", source_url)
        self.assertEqual(data["details"]["isbn"], "978-2-205-00007-5")
