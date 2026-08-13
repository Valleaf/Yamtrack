"""Provider for Bibliothèque nationale de France (BnF) catalog.

Used for French bandes dessinées (BD) search and metadata retrieval.
Public SRU API — no API key required.

SRU endpoint: https://catalogue.bnf.fr/api/SRU
Record schema: Dublin Core (dublincore)
"""

from difflib import SequenceMatcher
import logging
import re
import ssl
import unicodedata
from urllib.parse import quote

import requests
from defusedxml import ElementTree
from django.conf import settings
from django.core.cache import cache
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

from app import helpers, image_proxy
from app.models import MediaTypes, Sources
from app.providers import comicvine, services

logger = logging.getLogger(__name__)

SRU_URL = "http://catalogue.bnf.fr/api/SRU"

# BnF "Service Couvertures" API (beta, launched Feb 2026).
# Unlike the old catalogue.bnf.fr/couverture endpoint (ARK only), this
# supports lookup by idArk, EAN, or ISBN directly.
# Docs: https://api.bnf.fr/fr/api-service-couvertures-du-catalogue-general
BNF_COVER_API_URL = "https://openapi.bnf.fr/couverture/image/image/recupererImage"

# Hardcover's GraphQL API has no REST "cover by ISBN" endpoint, so
# get_hardcover_cover() queries this directly. See its docstring.
HARDCOVER_GRAPHQL_URL = "https://api.hardcover.app/v1/graphql"

# Real cover scans/thumbnails are reliably larger than the known
# placeholder responses (Open Library's ~43-byte "no cover" GIF, and
# BnF's historical generic blank-book graphic on the old endpoint).
# Used to detect a fake-success (HTTP 200, but not a real cover) response.
_MIN_VALID_IMAGE_BYTES = 1500
_COVER_PROBE_TIMEOUT = 10  # seconds — short-lived HEAD/GET, not a full API call

# ---------------------------------------------------------------------------
# Dedicated HTTP session for catalogue.bnf.fr
# ---------------------------------------------------------------------------
# catalogue.bnf.fr drops TLS connections without a proper close_notify alert.
# Python 3.12 / OpenSSL 3.x treats this as SSLEOFError.  Setting
# OP_IGNORE_UNEXPECTED_EOF on the SSL context suppresses the error.
# We use a standalone session (not the shared LimiterSession) so the SSL
# adapter is guaranteed to be applied without interference.


class _BnFSSLAdapter(HTTPAdapter):
    """HTTPAdapter with TLS compatibility fixes for catalogue.bnf.fr."""

    def _make_ctx(self):
        ctx = create_urllib3_context()
        if hasattr(ssl, "OP_IGNORE_UNEXPECTED_EOF"):
            ctx.options |= ssl.OP_IGNORE_UNEXPECTED_EOF
        if hasattr(ssl, "OP_LEGACY_SERVER_CONNECT"):
            ctx.options |= ssl.OP_LEGACY_SERVER_CONNECT
        return ctx

    def init_poolmanager(self, *args, **kwargs):
        kwargs["ssl_context"] = self._make_ctx()
        super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, proxy, **proxy_kwargs):
        proxy_kwargs["ssl_context"] = self._make_ctx()
        return super().proxy_manager_for(proxy, **proxy_kwargs)


_bnf_session = requests.Session()
_bnf_session.mount("https://", _BnFSSLAdapter(max_retries=3))
_bnf_session.mount("http://", HTTPAdapter(max_retries=3))
# Default requests UA (python-requests/x.y) is a common bot signature and
# can get flagged/throttled by BnF's front-end. Look like a normal browser.
_bnf_session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
})

# XML namespace URIs
_SRW_NS = "http://www.loc.gov/zing/srw/"
_DC_NS = "http://purl.org/dc/elements/1.1/"


def _srw(tag: str) -> str:
    return f"{{{_SRW_NS}}}{tag}"


def _dc(tag: str) -> str:
    return f"{{{_DC_NS}}}{tag}"


# ---------------------------------------------------------------------------
# Low-level SRU helpers
# ---------------------------------------------------------------------------

def _sru_search(cql_query: str, max_records: int = 10, start_record: int = 1):
    """Call BnF SRU and return a parsed XML element tree."""
    params = {
        "version": "1.2",
        "operation": "searchRetrieve",
        "recordSchema": "dublincore",
        "maximumRecords": max_records,
        "startRecord": start_record,
        "query": cql_query,
    }
    try:
        resp = _bnf_session.get(
            SRU_URL,
            params=params,
            timeout=settings.REQUEST_TIMEOUT,
            verify=settings.REQUESTS_VERIFY_SSL,
        )
        resp.raise_for_status()
        return ElementTree.fromstring(resp.text)
    except requests.exceptions.RequestException as exc:
        raise services.ProviderAPIError(
            Sources.BNF.value, exc, details=str(exc)
        ) from None


def _iter_dc_elements(root):
    """Yield the top-level DC container element for each SRU record."""
    records_el = root.find(_srw("records"))
    if records_el is None:
        return
    for record_el in records_el.findall(_srw("record")):
        data_el = record_el.find(_srw("recordData"))
        if data_el is None:
            continue
        # The DC wrapper element is the first (and only) child of recordData.
        # Its local tag may be srw_dc:dc, oai_dc:dc, etc. — we don't care.
        for dc_el in data_el:
            yield dc_el
            break  # only one DC wrapper per record


def _get_all(dc_el, tag: str) -> list[str]:
    """Return all non-empty text values for a DC element tag."""
    return [el.text.strip() for el in dc_el.findall(_dc(tag)) if el.text]


def _get_first(dc_el, tag: str, default: str = "") -> str:
    values = _get_all(dc_el, tag)
    return values[0] if values else default


def _extract_ark(dc_el) -> str | None:
    """Find the BnF ARK from dc:identifier elements.

    BnF DC records store the ARK as a full URI, e.g.:
      ``http://catalogue.bnf.fr/ark:/12148/cb12345678x``
    but sometimes as a bare ARK:
      ``ark:/12148/cb12345678x``

    Returns the bare ARK string (e.g. ``ark:/12148/cb12345678x``) or None.
    """
    for ident in _get_all(dc_el, "identifier"):
        if "ark:/12148/" in ident:
            # Normalise to bare ARK regardless of URI prefix
            return "ark:/12148/" + ident.split("ark:/12148/")[1]
    return None


def _extract_year(dc_el) -> str:
    """Extract the first 4-digit year from dc:date elements."""
    for date_str in _get_all(dc_el, "date"):
        m = re.search(r"\b(\d{4})\b", date_str)
        if m:
            return m.group(1)
    return ""


# BnF tags the series/collection statement as a free-text dc:description
# line with a "Collection : " label, e.g. "Collection : Lucky Luke" or
# "Collection : Collection Lucky Luke ; 5" (some records redundantly
# repeat the word "Collection" inside the value itself).
_SERIES_DESC_PAT = re.compile(r"^\s*Collection\s*:\s*(.+?)\s*$", re.IGNORECASE)
_SERIES_LABEL_PAT = re.compile(r"^Collection\s+", re.IGNORECASE)
_SERIES_VOLUME_PAT = re.compile(r"^(.*?)\s*;\s*(\d+)\s*$")


def _extract_series_info(dc_el) -> tuple[str | None, str | None]:
    """Extract the BD series name (and volume number, if present).

    There is no dedicated/populated MARC series field exposed over SRU
    for BnF's BD holdings (see the note on ``search_by_series`` for why
    ``bib.serie`` can't be used) -- the series statement only exists as
    free text inside dc:description with a "Collection : " label.

    A trailing "; <n>" on the value is the album's position within the
    series.

    Returns (series_name, volume) -- either element is None when no
    Collection line is present, or no volume number is given.
    """
    for desc in _get_all(dc_el, "description"):
        match = _SERIES_DESC_PAT.match(desc)
        if not match:
            continue
        value = _SERIES_LABEL_PAT.sub("", match.group(1)).strip()
        volume_match = _SERIES_VOLUME_PAT.match(value)
        if volume_match:
            return volume_match.group(1).strip(), volume_match.group(2)
        return value, None
    return None, None


def _normalize_series_name(name: str) -> str:
    """Diacritic/case-insensitive normalisation for series-name matching."""
    normalized = unicodedata.normalize("NFKD", name)
    return normalized.encode("ascii", "ignore").decode("ascii").strip().lower()


def _normalize_title(title: str) -> str:
    """Diacritic/case/punctuation-insensitive normalisation for title matching.

    Used only to compare a BnF album title against a ComicVine issue name
    -- see ``get_comicvine_cover``'s title-matching fallback. Punctuation
    is stripped (not just diacritics) since apostrophes/quotes vary
    between sources (e.g. ``L'Evasion`` vs ``L Evasion``).
    """
    if not title:
        return ""
    normalized = unicodedata.normalize("NFKD", title)
    normalized = normalized.encode("ascii", "ignore").decode("ascii").lower()
    normalized = re.sub(r"[^a-z0-9\s]", " ", normalized)
    return " ".join(normalized.split())


def extract_identifiers(dc_el) -> dict[str, str | None]:
    """Extract every identifier needed for metadata + cover lookups.

    Returns a dict with keys ``isbn10``, ``isbn13``, ``ean``, ``ark``
    (each a string or ``None``).

    BnF DC records typically store ISBNs with hyphens in dc:identifier,
    e.g. ``978-2-8001-1234-5`` or ``2-8001-1234-5``, and commercial EAN
    in dc:description as ``Code à barres commercial : EAN 3781507006999``.

    ISBN values are kept in their original hyphenated form (not just
    digits) since BnF's cover API examples pass ISBNs with hyphens, e.g.
    ``ISBN=978-2-226-25022-3``.
    """
    ark = _extract_ark(dc_el)
    isbn10 = None
    isbn13 = None
    ean = None

    # BnF DC records sometimes prefix the bare identifier with a text
    # label, e.g. ``ISBN 2800118377`` instead of just ``2-8001-1234-5``.
    # Strip it before classifying, but keep everything else (including
    # hyphens) intact for the value we actually store.
    _label_pat = re.compile(r"^(?:isbn|ean)\b[\s:]*", re.IGNORECASE)

    for ident in _get_all(dc_el, "identifier"):
        raw = ident.strip()
        # Skip URI-form identifiers (ARK, HTTP URLs)
        if "://" in raw or raw.startswith("ark:"):
            continue
        raw = _label_pat.sub("", raw).strip()
        # Normalise: strip hyphens/spaces to get a plain digit string,
        # used only to classify the identifier (not for the API call).
        digits_only = re.sub(r"[\-\s]", "", raw)
        if re.fullmatch(r"\d{13}", digits_only):
            if digits_only.startswith(("978", "979")):
                isbn13 = isbn13 or raw
            else:
                ean = ean or digits_only
        elif re.fullmatch(r"\d{9}[\dX]", digits_only, re.IGNORECASE) and not isbn10:
            isbn10 = raw.upper()

    for desc in _get_all(dc_el, "description"):
        m = re.search(r"EAN[\s:]*([0-9]{13})", desc, re.IGNORECASE)
        if m and not ean:
            ean = m.group(1)

    return {"isbn10": isbn10, "isbn13": isbn13, "ean": ean, "ark": ark}


def _extract_people(dc_el) -> list[str]:
    """Return deduplicated list of all people from dc:creator + dc:contributor."""
    seen: set[str] = set()
    people = []
    for val in _get_all(dc_el, "creator") + _get_all(dc_el, "contributor"):
        if val and val not in seen:
            seen.add(val)
            people.append(val)
    return people


def _clean_description(dc_el) -> str:
    """Return the dc:description, filtering out lines that are only barcode/EAN metadata."""
    _barcode_pat = re.compile(
        r"^\s*(code[\s\u00e0àa]+barres|ean[\s:]+\d{13}|isbn[\s:]+[\d\-X]+)",
        re.IGNORECASE,
    )
    meaningful = [
        text
        for text in _get_all(dc_el, "description")
        if not _barcode_pat.match(text)
    ]
    return meaningful[0] if meaningful else ""


def _probe_image_url(url: str) -> bool:
    """Return True if `url` resolves to what looks like a genuine cover image.

    Guards against "fake success" responses that would otherwise render
    as a blank/placeholder image instead of failing outright:
      - Open Library serves a tiny ~43-byte placeholder GIF with HTTP 200
        when no cover exists for a given identifier.
      - BnF's cover service has historically served a generic blank-book
        graphic with HTTP 200 when no scan is indexed for a record.

    Both cases are filtered out using a minimum byte-size heuristic,
    since real cover scans/thumbnails are reliably larger than either
    placeholder. This is a heuristic, not a guarantee — if a server omits
    Content-Length we give the URL the benefit of the doubt.
    """
    try:
        resp = _bnf_session.head(
            url,
            timeout=_COVER_PROBE_TIMEOUT,
            verify=settings.REQUESTS_VERIFY_SSL,
            allow_redirects=True,
        )
        if resp.status_code == requests.codes.method_not_allowed:
            # Some endpoints don't support HEAD — fall back to a GET and
            # close immediately without reading the body.
            resp = _bnf_session.get(
                url,
                timeout=_COVER_PROBE_TIMEOUT,
                verify=settings.REQUESTS_VERIFY_SSL,
                stream=True,
            )
            resp.close()
    except requests.exceptions.RequestException as exc:
        logger.debug("Cover probe failed for %s: %s", url, exc)
        return False

    if resp.status_code != requests.codes.ok:
        logger.debug("Cover probe non-200 (%s) for %s", resp.status_code, url)
        return False

    content_type = resp.headers.get("Content-Type", "")
    if not content_type.startswith("image/"):
        logger.debug(
            "Cover probe non-image content-type (%s) for %s", content_type, url,
        )
        return False

    content_length = resp.headers.get("Content-Length")
    if content_length is not None and int(content_length) < _MIN_VALID_IMAGE_BYTES:
        logger.debug(
            "Cover probe placeholder-sized (%s bytes) for %s", content_length, url,
        )
        return False

    return True


# NOTE: currently not called from resolve_cover() — BnF's Service
# Couvertures API proved unreliable in practice (frequent false
# negatives/empty results even for records with a real scan indexed).
# Kept here in case it's worth revisiting once the upstream API
# stabilises; Open Library + Hardcover cover the bulk of cases for now.
def get_bnf_cover(
    identifiers: dict[str, str | None],
    *,
    validate: bool = True,
) -> str | None:
    """Resolve a cover URL from BnF's Service Couvertures API.

    Currently unused by resolve_cover() — see the module-level note
    above this function.

    Priority: ISBN-13 > ISBN-10 > EAN > ARK. ISBN/EAN are commercial
    identifiers that BnF indexes covers against directly; ARK is the
    fallback for records without one (only works if BnF has explicitly
    linked a cover scan to that specific record).

    When ``validate`` is False, the highest-priority candidate URL is
    returned without confirming a real image exists behind it (cheap
    path for bulk search results — see ``resolve_cover``). When True,
    each candidate is checked in priority order and the first one that
    resolves to a real image wins.
    """
    candidates: list[tuple[str, str]] = []

    isbn = identifiers.get("isbn13") or identifiers.get("isbn10")
    if isbn:
        candidates.append(
            ("isbn", f"{BNF_COVER_API_URL}?ISBN={quote(isbn)}&couverture=1"),
        )
    if identifiers.get("ean"):
        candidates.append(
            ("ean", f"{BNF_COVER_API_URL}?EAN={identifiers['ean']}&couverture=1"),
        )
    if identifiers.get("ark"):
        # Keep `:` and `/` unencoded — BnF's cover endpoint does plain
        # string matching on idArk and won't decode %3A / %2F.
        encoded = quote(identifiers["ark"], safe=":/")
        candidates.append(
            ("ark", f"{BNF_COVER_API_URL}?idArk={encoded}&couverture=1"),
        )

    if not candidates:
        return None

    if not validate:
        kind, url = candidates[0]
        logger.debug("BnF cover (unvalidated) via %s: %s", kind, url)
        return url

    for kind, url in candidates:
        logger.debug("BnF cover attempt via %s: %s", kind, url)
        if _probe_image_url(url):
            logger.debug("BnF cover confirmed via %s: %s", kind, url)
            return url

    logger.debug("No valid BnF cover found for identifiers=%s", identifiers)
    return None


def get_openlibrary_cover(
    identifiers: dict[str, str | None],
    *,
    validate: bool = True,
) -> str | None:
    """Resolve a cover URL from Open Library, using the large-size endpoint.

    Fallback for when BnF has no cover indexed. Open Library's coverage
    of French BD is sparse, so this rarely succeeds where BnF failed,
    but it's a free secondary attempt before giving up.
    """
    candidates: list[tuple[str, str]] = []

    isbn = identifiers.get("isbn13") or identifiers.get("isbn10")
    if isbn:
        digits = re.sub(r"[\-\s]", "", isbn)
        candidates.append(
            ("isbn", f"https://covers.openlibrary.org/b/isbn/{digits}-L.jpg"),
        )
    if identifiers.get("ean"):
        candidates.append(
            (
                "ean",
                f"https://covers.openlibrary.org/b/ean/{identifiers['ean']}-L.jpg",
            ),
        )

    if not candidates:
        return None

    if not validate:
        kind, url = candidates[0]
        logger.debug("Open Library cover (unvalidated) via %s: %s", kind, url)
        return url

    for kind, url in candidates:
        logger.debug("Open Library cover attempt via %s: %s", kind, url)
        if _probe_image_url(url):
            logger.debug("Open Library cover confirmed via %s: %s", kind, url)
            return url

    return None


def _hardcover_edition_lookup(isbn: str) -> dict | None:
    """Query Hardcover's GraphQL editions table for a cover by ISBN.

    Matches against both isbn_13 and isbn_10 columns with a single value
    since the two never collide (different digit counts/checksums), so
    callers don't need to know which kind of ISBN they're passing in.
    Returns the raw edition dict (with its nested book) or None.
    """
    query = """
    query GetEditionCoverByISBN($isbn: String!) {
      editions(
        where: {_or: [{isbn_13: {_eq: $isbn}}, {isbn_10: {_eq: $isbn}}]}
        limit: 1
      ) {
        cached_image(path: "url")
        book {
          cached_image(path: "url")
        }
      }
    }
    """
    try:
        response = services.api_request(
            Sources.HARDCOVER.value,
            "POST",
            HARDCOVER_GRAPHQL_URL,
            params={"query": query, "variables": {"isbn": isbn}},
            headers={"Authorization": settings.HARDCOVER_API},
        )
    except requests.exceptions.RequestException as exc:
        logger.debug("Hardcover cover lookup failed for isbn=%s: %s", isbn, exc)
        return None

    editions = (response.get("data") or {}).get("editions") or []
    return editions[0] if editions else None


def get_hardcover_cover(
    identifiers: dict[str, str | None],
    *,
    validate: bool = True,
) -> str | None:
    """Resolve a cover URL from Hardcover, looked up by ISBN.

    Hardcover has no REST "cover by ISBN" endpoint and no predictable
    cover-URL pattern derivable from an ISBN the way Open Library does
    — the only way to get a cover is a live GraphQL query against the
    editions table (falling back to the parent book's cover if the
    matched edition itself has none cached).

    Because that means every call here is a real network round-trip
    (unlike Open Library's free URL-template guess), this is skipped
    entirely when ``validate`` is False (bulk search results) to avoid
    N synchronous Hardcover API calls in a single search response.
    """
    if not validate:
        return None

    for kind, isbn in (
        ("isbn13", identifiers.get("isbn13")),
        ("isbn10", identifiers.get("isbn10")),
    ):
        if not isbn:
            continue
        logger.debug("Hardcover cover attempt via %s: %s", kind, isbn)
        edition = _hardcover_edition_lookup(isbn)
        if not edition:
            continue
        url = edition.get("cached_image") or (edition.get("book") or {}).get(
            "cached_image",
        )
        if url:
            logger.debug("Hardcover cover confirmed via %s: %s", kind, url)
            return url

    logger.debug("No Hardcover cover found for identifiers=%s", identifiers)
    return None


# ---------------------------------------------------------------------------
# ComicVine cover fallback — BD series with no ISBN/EAN at all (pre-~1970
# albums), where the identifier-based fallbacks above have nothing to try.
# ---------------------------------------------------------------------------
# ComicVine's volume resource has no language/country field, so the
# correct volume_id for *the original French edition* of a series can't
# be resolved automatically — a plain-name search for e.g. "Lucky Luke"
# returns a dozen volumes split by publisher/language (Cinebook EN,
# Egmont SE, Bastei DE, etc.), several renumbered relative to the French
# Dargaud originals and using translated titles. Each entry below was
# confirmed by hand against the French-language ComicVine volume before
# being added.
_BD_COMICVINE_VOLUMES: dict[str, str] = {
    # _normalize_series_name(series_name): comicvine volume id (bare numeric, no "4050-" prefix)
    "lucky luke": "32180",  # French Dargaud-era run, #1-72 (1949-2002)
}

# How close a BnF album title and a ComicVine issue name need to be
# (post-normalization) to accept a title-based match -- see
# get_comicvine_cover's fallback path. Deliberately strict: a same-volume
# free-text search for "Des rails sur la prairie" (issue #9) also pulled
# back issue #29 "Des barbeles sur la prairie" purely on the shared
# "sur la prairie" tail (~0.7 ratio) -- this threshold is set high enough
# to reject that kind of partial overlap while still tolerating harmless
# case/typography differences between sources.
_TITLE_MATCH_THRESHOLD = 0.92


def get_comicvine_cover(
    series_name: str | None,
    series_volume: str | None,
    title: str | None = None,
) -> str | None:
    """Resolve a cover from ComicVine by series name + album number/title.

    Unlike the identifier-based fallbacks above, this needs no ISBN/EAN
    — it's the only cover source that can work for pre-barcode-era BDs,
    which will never have one. Requires a series recognised in
    ``_BD_COMICVINE_VOLUMES``; returns None if it isn't mapped yet.

    Primary match is by album number (from the Collection statement's
    "; N" suffix, see ``_extract_series_info``). Some Collection lines
    have no volume number at all, so when that's missing this falls back
    to a same-volume title search instead — but only accepts a result
    whose name is a near-exact match (``_TITLE_MATCH_THRESHOLD``) against
    the BnF album title, since an unscoped/loose title search on
    ComicVine reliably returns plausible-looking wrong answers (other
    editions of the same series, or unrelated issues sharing a few
    words) — there's no safe "take the top result" shortcut here.

    Always a live call with no cheap fallback of its own, so callers
    should only reach this after the identifier-based fallbacks above
    have already failed.
    """
    if not series_name:
        return None

    volume_id = _BD_COMICVINE_VOLUMES.get(_normalize_series_name(series_name))
    if not volume_id:
        return None

    cv_issue = None
    if series_volume:
        logger.debug(
            "ComicVine cover attempt by number: series=%r volume=%r cv_volume_id=%s",
            series_name, series_volume, volume_id,
        )
        cv_issue = comicvine.get_issue_by_number(volume_id, series_volume)

    if cv_issue is None and title:
        logger.debug(
            "ComicVine cover attempt by title: series=%r title=%r cv_volume_id=%s",
            series_name, title, volume_id,
        )
        normalized_target = _normalize_title(title)
        for candidate in comicvine.search_issues(title, volume_id=volume_id):
            normalized_candidate = _normalize_title(candidate.get("name") or "")
            similarity = SequenceMatcher(
                None, normalized_target, normalized_candidate,
            ).ratio()
            if similarity >= _TITLE_MATCH_THRESHOLD:
                cv_issue = candidate
                break
            logger.debug(
                "Rejected ComicVine title match %r (similarity=%.2f < %.2f)",
                candidate.get("name"), similarity, _TITLE_MATCH_THRESHOLD,
            )

    if not cv_issue:
        logger.debug(
            "No ComicVine match for series=%r volume=%r title=%r in cv_volume_id=%s",
            series_name, series_volume, title, volume_id,
        )
        return None

    return comicvine.get_image(cv_issue)


def _public_cover_url(url: str | None) -> str:
    """Return the URL to actually display for a resolved (or cached) cover.

    Routes real covers through app.image_proxy: Open Library/Hardcover/
    ComicVine don't reliably set the long-lived Cache-Control headers
    TMDB/IGDB's media CDNs do, so without this every page view re-fetches
    the same cover from scratch instead of the browser caching it.
    """
    if not url:
        return settings.IMG_NONE
    return image_proxy.proxy_url(url)


def resolve_cover(
    identifiers: dict[str, str | None],
    *,
    series_name: str | None = None,
    series_volume: str | None = None,
    title: str | None = None,
    validate: bool = True,
) -> str:
    """Resolve the best available cover image URL for a BnF record.

    Order: Open Library (ISBN > EAN) > Hardcover (ISBN-13 > ISBN-10) >
    ComicVine (series + album number, or series + title) > IMG_NONE.
    BnF's own Service Couvertures API (get_bnf_cover) is intentionally
    skipped here — see the note above get_bnf_cover's definition for why.

    ComicVine is tried last, only when ``validate`` is True, and only
    does anything when ``series_name`` is passed in — currently just
    ``comic()``, since bulk search results don't extract series info
    (see ``_dc_to_result()``). It's the one fallback that doesn't need
    an ISBN/EAN at all, so it's the path that actually covers
    pre-barcode-era albums.

    When ``validate`` is True, successful *and* confirmed-empty lookups
    are cached by identifier (ISBN/EAN/ARK) so the external probe only
    ever runs once per identifier, regardless of how many BnF records
    reference it. ``validate=False`` skips both the network probe and
    the cache, since it's meant for cheap bulk listings.

    Cover lookup failures never raise — any unexpected error here
    should never break metadata import, since the cover is optional.
    """
    cache_id = (
        identifiers.get("isbn13")
        or identifiers.get("isbn10")
        or identifiers.get("ean")
        or identifiers.get("ark")
    )
    cache_key = f"{Sources.BNF.value}_cover_{cache_id}" if cache_id else None

    if validate and cache_key:
        cached = cache.get(cache_key)
        if cached is not None:
            return _public_cover_url(cached)

    logger.debug(
        "Resolving cover for identifiers=%s (validate=%s)", identifiers, validate,
    )

    try:
        url = get_openlibrary_cover(identifiers, validate=validate)
        if url is None:
            url = get_hardcover_cover(identifiers, validate=validate)
        if url is None and validate:
            url = get_comicvine_cover(series_name, series_volume, title)
    except Exception:
        # Cover lookup is strictly optional — never let it break metadata
        # import or a detail-page render.
        logger.exception("Unexpected error resolving cover for %s", identifiers)
        url = None

    logger.debug("Final cover selected for %s: %s", identifiers, url or "(none)")

    if validate and cache_key:
        # Cache "" (not None) for a confirmed-empty result so we don't
        # re-probe an identifier we already know has no cover.
        cache.set(cache_key, url or "")

    return _public_cover_url(url)


def _dc_to_result(dc_el) -> dict | None:
    """Convert a parsed DC element to the standard provider search-result dict.

    Returns None if the record has no usable ARK or title.

    ``media_id`` is stored as the short ARK suffix (e.g. ``cb12345678x``)
    so it can be safely embedded in URL path segments.
    """
    ark = _extract_ark(dc_el)
    if not ark:
        return None
    title = _get_first(dc_el, "title")
    if not title:
        return None
    ark_short = ark.split("/")[-1]  # e.g. cb12345678x — no slashes, URL-safe
    identifiers = extract_identifiers(dc_el)
    creator = _get_first(dc_el, "creator")
    _, series_position = _extract_series_info(dc_el)
    return {
        "media_id": ark_short,
        "source": Sources.BNF.value,
        "media_type": MediaTypes.COMIC.value,
        "title": title,
        "year": _extract_year(dc_el),
        # Unvalidated: no network probe per result, to avoid N synchronous
        # HTTP calls in a single search response. See resolve_cover().
        "image": resolve_cover(identifiers, validate=False),
        # Extra fields used by the import confidence scorer
        "creator": creator,
        "subtitle": creator or None,
        "series_position": series_position,
    }


# ---------------------------------------------------------------------------
# Public provider interface
# ---------------------------------------------------------------------------

def search_by_series(series_name: str, max_results: int = 100) -> list[dict]:
    """Return all BnF albums whose Collection statement matches *series_name*.

    ``bib.serie`` (the MARC 490/830 Series Statement index) returns zero
    records even for well-known series -- verified against live data, it
    simply isn't populated for BnF's BD holdings. The series name only
    exists as free text inside dc:description (see ``_extract_series_info``).

    So this casts a wide net with the documented ``bib.anywhere`` index
    (BnF's full-record keyword search -- see
    https://www.bnf.fr/fr/service-sru-catalogue-general-de-la-bnf) and
    keeps only the records whose own Collection line matches
    *series_name*, diacritic/case-insensitively.

    Note: BnF sometimes tags non-BD adaptations (audio dramas, etc.)
    under the same Collection label as the BD album itself -- a BnF
    data-quality quirk that can't be filtered out from the DC record
    alone.

    Returns a list of result dicts in the same format as ``_dc_to_result()``
    so they can be used directly as collection parts.
    """
    target = _normalize_series_name(series_name)
    cql = f'bib.anywhere all "{series_name}"'
    logger.info("BnF series lookup: cql=%r max=%d", cql, max_results)
    try:
        root = _sru_search(cql, max_records=min(max_results, 100))
    except Exception as exc:
        logger.warning("BnF series search failed for %r: %s", series_name, exc)
        return []

    results: list[dict] = []
    seen_ids: set[str] = set()
    for dc_el in _iter_dc_elements(root):
        found_series, _volume = _extract_series_info(dc_el)
        if not found_series or _normalize_series_name(found_series) != target:
            continue
        result = _dc_to_result(dc_el)
        if result and result["media_id"] not in seen_ids:
            seen_ids.add(result["media_id"])
            results.append(result)

    logger.info("BnF series %r → %d unique records", series_name, len(results))
    return results


def search(query: str, page: int) -> dict:
    """Search the BnF catalog and return results in the standard provider format."""
    cache_key = (
        f"search_{Sources.BNF.value}_{MediaTypes.COMIC.value}_{query}_{page}"
    )
    data = cache.get(cache_key)

    if data is None:
        per_page = settings.PER_PAGE
        start_record = (page - 1) * per_page + 1

        try:
            # Search by title.  BnF CQL: bib.title all "<terms>"
            cql = f'bib.title all "{query}"'
            root = _sru_search(cql, max_records=per_page, start_record=start_record)
        except Exception as exc:
            logger.warning("BnF search error for %r: %s", query, exc)
            return helpers.format_search_response(page, per_page, 0, [])

        # Total number of matching records
        num_el = root.find(_srw("numberOfRecords"))
        total = int(num_el.text) if (num_el is not None and num_el.text) else 0

        results = []
        for dc_el in _iter_dc_elements(root):
            result = _dc_to_result(dc_el)
            if result:
                results.append(result)

        data = helpers.format_search_response(page, per_page, total, results)
        cache.set(cache_key, data)

    return data


def comic(media_id: str) -> dict:
    """Return full metadata for a BnF item (used on the comic detail page).

    ``media_id`` is the short ARK suffix, e.g. ``cb12345678x``.
    The full ARK ``ark:/12148/<media_id>`` is reconstructed internally.
    """
    cache_key = f"{Sources.BNF.value}_{MediaTypes.COMIC.value}_{media_id}"
    data = cache.get(cache_key)

    if data is None:
        ark = f"ark:/12148/{media_id}"
        # Retrieve by persistent ARK identifier
        cql = f'bib.persistentid any "{ark}"'
        try:
            root = _sru_search(cql, max_records=1)
        except Exception as exc:
            logger.warning("BnF metadata error for %r: %s", media_id, exc)
            services.raise_not_found_error(Sources.BNF.value, media_id, "comic")

        dc_el = next(_iter_dc_elements(root), None)
        if dc_el is None:
            services.raise_not_found_error(Sources.BNF.value, media_id, "comic")

        ark = _extract_ark(dc_el) or ark
        title = _get_first(dc_el, "title") or media_id
        year = _extract_year(dc_el)
        publisher = _get_first(dc_el, "publisher")
        description = _clean_description(dc_el) or "No synopsis available"
        subjects = _get_all(dc_el, "subject")
        language = _get_first(dc_el, "language")
        identifiers = extract_identifiers(dc_el)
        people = _extract_people(dc_el)
        series_name, series_volume = _extract_series_info(dc_el)

        # Canonical page on catalogue.bnf.fr
        ark_short = ark.split("/")[-1]  # e.g. cb12345678x
        source_url = f"https://catalogue.bnf.fr/ark:/12148/{ark_short}"

        details: dict = {
            "start_date": year or None,
            "publisher": publisher or None,
            "people": people,
            "language": language or None,
        }
        if identifiers["ean"]:
            details["ean"] = identifiers["ean"]
        isbn_for_details = identifiers["isbn13"] or identifiers["isbn10"]
        if isbn_for_details:
            details["isbn"] = isbn_for_details
        if series_name:
            details["series"] = series_name
        if series_volume:
            details["series_position"] = series_volume

        # Mirrors tmdb_collection/igdb_collection/hardcover_series: embed
        # the full series listing now (one extra SRU search, cached
        # alongside this comic's own metadata) so the generic collection
        # auto-detect/lazy-sync logic in app/views.py can pick it up.
        bnf_series = None
        if series_name:
            series_parts = search_by_series(series_name)
            if series_parts:
                bnf_series = {
                    "id": series_name,
                    "name": series_name,
                    "image": next((p["image"] for p in series_parts if p["image"]), ""),
                    "parts": series_parts,
                }

        data = {
            "media_id": media_id,
            "source": Sources.BNF.value,
            "source_url": source_url,
            "media_type": MediaTypes.COMIC.value,
            "title": title,
            "country": "FR",  # BnF is the French national library
            "max_progress": None,
            "max_issue_number": None,
            # Validated: single item, cached afterward, so the extra
            # probe round-trip is paid once per cache period.
            "image": resolve_cover(
                identifiers,
                series_name=series_name,
                series_volume=series_volume,
                title=title,
                validate=True,
            ),
            "synopsis": description,
            "genres": subjects[:5] if subjects else None,
            "score": None,
            "score_count": None,
            "details": details,
            "creators": [],
            "related": {"recommendations": []},
            # No ComicVine-style issue events for BnF items
            "last_issue_id": None,
            "bnf_series": bnf_series,
        }

        cache.set(cache_key, data)

    return data
