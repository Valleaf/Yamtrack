"""Provider for Bibliothèque nationale de France (BnF) catalog.

Used for French bandes dessinées (BD) search and metadata retrieval.
Public SRU API — no API key required.

SRU endpoint: https://catalogue.bnf.fr/api/SRU
Record schema: Dublin Core (dc)
"""

import logging
import re
from urllib.parse import quote

from django.conf import settings
from django.core.cache import cache

from app import helpers
from app.models import MediaTypes, Sources
from app.providers import services

logger = logging.getLogger(__name__)

SRU_URL = "https://catalogue.bnf.fr/api/SRU"

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
        "recordSchema": "dc",
        "maximumRecords": max_records,
        "startRecord": start_record,
        "query": cql_query,
    }
    return services.api_request(
        Sources.BNF.value,
        "GET",
        SRU_URL,
        params=params,
        response_format="xml",
    )


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

    Returns the full ARK string (e.g. ``ark:/12148/cb12345678x``) or None.
    """
    for ident in _get_all(dc_el, "identifier"):
        if ident.startswith("ark:/12148/"):
            return ident
    return None


def _extract_year(dc_el) -> str:
    """Extract the first 4-digit year from dc:date elements."""
    for date_str in _get_all(dc_el, "date"):
        m = re.search(r"\b(\d{4})\b", date_str)
        if m:
            return m.group(1)
    return ""


def _cover_url(ark: str | None) -> str:
    """Build the BnF catalog cover-image URL for an ARK identifier."""
    if not ark:
        return settings.IMG_NONE
    encoded = quote(ark, safe="")
    return (
        f"https://catalogue.bnf.fr/couverture"
        f"?appName=NE&idArk={encoded}&couverture=1"
    )


def _dc_to_result(dc_el) -> dict | None:
    """Convert a parsed DC element to the standard provider search-result dict.

    Returns None if the record has no usable ARK or title.
    """
    ark = _extract_ark(dc_el)
    if not ark:
        return None
    title = _get_first(dc_el, "title")
    if not title:
        return None
    return {
        "media_id": ark,
        "source": Sources.BNF.value,
        "media_type": MediaTypes.COMIC.value,
        "title": title,
        "year": _extract_year(dc_el),
        "image": _cover_url(ark),
        # Extra fields used by the import confidence scorer
        "creator": _get_first(dc_el, "creator"),
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

    ``media_id`` is the full BnF ARK string, e.g. ``ark:/12148/cb12345678x``.
    """
    cache_key = f"{Sources.BNF.value}_{MediaTypes.COMIC.value}_{media_id}"
    data = cache.get(cache_key)

    if data is None:
        # Retrieve by persistent ARK identifier
        cql = f'bib.persistentId adj "{media_id}"'
        try:
            root = _sru_search(cql, max_records=1)
        except Exception as exc:
            logger.warning("BnF metadata error for %r: %s", media_id, exc)
            services.raise_not_found_error(Sources.BNF.value, media_id, "comic")

        dc_el = next(_iter_dc_elements(root), None)
        if dc_el is None:
            services.raise_not_found_error(Sources.BNF.value, media_id, "comic")

        ark = _extract_ark(dc_el) or media_id
        title = _get_first(dc_el, "title") or media_id
        creator = _get_first(dc_el, "creator")
        year = _extract_year(dc_el)
        publisher = _get_first(dc_el, "publisher")
        description = _get_first(dc_el, "description") or "No synopsis available"
        subjects = _get_all(dc_el, "subject")
        language = _get_first(dc_el, "language")

        # Canonical page on catalogue.bnf.fr
        ark_short = ark.split("/")[-1]  # e.g. cb12345678x
        source_url = f"https://catalogue.bnf.fr/ark:/12148/{ark_short}"

        data = {
            "media_id": media_id,
            "source": Sources.BNF.value,
            "source_url": source_url,
            "media_type": MediaTypes.COMIC.value,
            "title": title,
            "max_progress": None,
            "max_issue_number": None,
            "image": _cover_url(ark),
            "synopsis": description,
            "genres": subjects[:5] if subjects else None,
            "score": None,
            "score_count": None,
            "details": {
                "start_date": year or None,
                "publisher": publisher or None,
                "issues_count": None,
                "last_issue_name": None,
                "last_issue_number": None,
                "people": [creator] if creator else [],
                "last_updated": None,
                "language": language or None,
            },
            "creators": (
                [{"id": "", "name": creator, "image": None}] if creator else []
            ),
            "related": {"recommendations": []},
            # No ComicVine-style issue events for BnF items
            "last_issue_id": None,
        }

        cache.set(cache_key, data)

    return data
