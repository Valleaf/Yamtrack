"""Provider for Bibliothèque nationale de France (BnF) catalog.

Used for French bandes dessinées (BD) search and metadata retrieval.
Public SRU API — no API key required.

SRU endpoint: https://catalogue.bnf.fr/api/SRU
Record schema: Dublin Core (dublincore)
"""

import logging
import re
import ssl
from urllib.parse import quote

import requests
from defusedxml import ElementTree
from django.conf import settings
from django.core.cache import cache
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

from app import helpers
from app.models import MediaTypes, Sources
from app.providers import services

logger = logging.getLogger(__name__)

SRU_URL = "http://catalogue.bnf.fr/api/SRU"

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


def _extract_ean_isbn(dc_el) -> tuple[str | None, str | None]:
    """Return (ean, isbn) from dc:identifier and dc:description elements.

    BnF DC records typically store ISBNs with hyphens in dc:identifier, e.g.:
      ``978-2-8001-1234-5``  or  ``2-8001-1234-5``
    and commercial EAN in dc:description as:
      ``Code à barres commercial : EAN 3781507006999``
    """
    ean = None
    isbn = None

    for ident in _get_all(dc_el, "identifier"):
        # Skip URI-form identifiers (ARK, HTTP URLs)
        if "://" in ident or ident.strip().startswith("ark:"):
            continue
        # Normalise: strip hyphens/spaces to get a plain digit string
        digits_only = re.sub(r"[\-\s]", "", ident.strip())
        if re.fullmatch(r"\d{13}", digits_only):
            if digits_only.startswith(("978", "979")):
                isbn = isbn or digits_only
            else:
                ean = ean or digits_only
        elif re.fullmatch(r"\d{9}[\dX]", digits_only, re.IGNORECASE) and not isbn:
            isbn = digits_only.upper()

    for desc in _get_all(dc_el, "description"):
        m = re.search(r"EAN[\s:]*([0-9]{13})", desc, re.IGNORECASE)
        if m and not ean:
            ean = m.group(1)

    return ean, isbn


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


def _best_cover_url(
    ark: str | None,
    ean: str | None = None,
    isbn: str | None = None,
) -> str:
    """Return best available cover image URL.

    Priority: Open Library by EAN > Open Library by ISBN
    > BnF catalogue couverture > IMG_NONE.

    Open Library returns actual cover art for most commercially
    distributed albums; BnF couverture works only when BnF has
    explicitly indexed a cover scan.
    """
    if ean:
        return f"https://covers.openlibrary.org/b/ean/{ean}-L.jpg"
    if isbn:
        return f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
    if ark:
        # Keep `:` and `/` unencoded — BnF's couverture endpoint does plain
        # string matching on idArk and won't decode %3A / %2F.
        encoded = quote(ark, safe=":/")
        return (
            f"https://catalogue.bnf.fr/couverture"
            f"?appName=NE&idArk={encoded}&couverture=1"
        )
    return settings.IMG_NONE


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
    ean, isbn = _extract_ean_isbn(dc_el)
    creator = _get_first(dc_el, "creator")
    return {
        "media_id": ark_short,
        "source": Sources.BNF.value,
        "media_type": MediaTypes.COMIC.value,
        "title": title,
        "year": _extract_year(dc_el),
        "image": _best_cover_url(ark, ean, isbn),
        # Extra fields used by the import confidence scorer
        "creator": creator,
        "subtitle": creator or None,
    }


# ---------------------------------------------------------------------------
# Public provider interface
# ---------------------------------------------------------------------------

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
        ean, isbn = _extract_ean_isbn(dc_el)
        people = _extract_people(dc_el)

        # Canonical page on catalogue.bnf.fr
        ark_short = ark.split("/")[-1]  # e.g. cb12345678x
        source_url = f"https://catalogue.bnf.fr/ark:/12148/{ark_short}"

        details: dict = {
            "start_date": year or None,
            "publisher": publisher or None,
            "people": people,
            "language": language or None,
        }
        if ean:
            details["ean"] = ean
        if isbn:
            details["isbn"] = isbn

        data = {
            "media_id": media_id,
            "source": Sources.BNF.value,
            "source_url": source_url,
            "media_type": MediaTypes.COMIC.value,
            "title": title,
            "country": "FR",  # BnF is the French national library
            "max_progress": None,
            "max_issue_number": None,
            "image": _best_cover_url(ark, ean, isbn),
            "synopsis": description,
            "genres": subjects[:5] if subjects else None,
            "score": None,
            "score_count": None,
            "details": details,
            "creators": [],
            "related": {"recommendations": []},
            # No ComicVine-style issue events for BnF items
            "last_issue_id": None,
        }

        cache.set(cache_key, data)

    return data


