"""Run: docker compose exec yamtrack python /yamtrack/bnf_debug.py <ark_short_or_title>

Diagnoses the full BnF cover-resolution chain for a single record:
raw DC fields -> extracted identifiers -> BnF cover attempt -> Open
Library fallback -> final resolved URL. Mirrors what `comic()` does,
but prints every intermediate step instead of just the final dict.

Accepts either:
  - an ARK suffix, e.g. "cb43416465x"
  - a free-text title, e.g. "chariot" -- will search BnF by title,
    print the top matches with their ARKs, and run full diagnostics
    on the first match.

NOTE: this bypasses the Redis cache entirely (calls the helper
functions directly), so it always reflects the *current* code/network
state -- useful for telling a stale-cache problem apart from a real
resolution bug.
"""
import os, re, sys
sys.path.insert(0, '/yamtrack')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import logging
logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(name)s: %(message)s")

import django
django.setup()

from app.providers.bnf import (
    _sru_search, _iter_dc_elements, _get_all, _extract_ark, _extract_year,
    extract_identifiers, _extract_people, _clean_description, _get_first,
    get_bnf_cover, get_openlibrary_cover, resolve_cover,
    BNF_COVER_API_URL, _bnf_session,
)
from urllib.parse import quote
from django.conf import settings as dj_settings


def verbose_probe(label, url):
    """Hit a candidate cover URL directly and print the raw response,
    bypassing the True/False heuristic in _probe_image_url so we can see
    *why* it passed or failed."""
    print(f"\n--- probing [{label}] {url}")
    try:
        resp = _bnf_session.head(url, timeout=10, verify=dj_settings.REQUESTS_VERIFY_SSL, allow_redirects=True)
        if resp.status_code == 405:
            print("    HEAD not allowed, retrying with GET (stream)")
            resp = _bnf_session.get(url, timeout=10, verify=dj_settings.REQUESTS_VERIFY_SSL, stream=True)
    except Exception as exc:
        print(f"    REQUEST FAILED: {exc!r}")
        return
    print(f"    status:         {resp.status_code}")
    print(f"    content-type:   {resp.headers.get('Content-Type')!r}")
    print(f"    content-length: {resp.headers.get('Content-Length')!r}")
    print(f"    final url:      {resp.url}")

arg = sys.argv[1] if len(sys.argv) > 1 else "cb43416465x"

# Looks like an ARK suffix (e.g. cb43416465x) vs a bare EAN/ISBN-13
# (13 digits) vs a free-text title.
is_ark_suffix = bool(re.fullmatch(r"cb\d{8}[\dA-Za-z]", arg))
is_ean_isbn13 = bool(re.fullmatch(r"\d{13}", arg))

if is_ark_suffix:
    ark_short = arg
elif is_ean_isbn13:
    print(f"Searching BnF by EAN/ISBN-13 for {arg!r}...\n")
    root = _sru_search(f'bib.fuzzyISBN any "{arg}"', max_records=5)
    matches = []
    for dc_el in _iter_dc_elements(root):
        ark = _extract_ark(dc_el)
        title = _get_first(dc_el, "title")
        if ark and title:
            matches.append((ark.split("/")[-1], title))
    if not matches:
        print("ERROR: no record found via bib.fuzzyISBN for this EAN/ISBN.")
        print("(This itself is diagnostic: if BnF's own SRU can't find the")
        print("record by this identifier, the cover API won't either.)")
        sys.exit(1)
    print("=== MATCHES ===")
    for ark_short_m, title in matches:
        print(f"  {ark_short_m}  {title}")
    ark_short = matches[0][0]
    print(f"\nRunning full diagnostics on: {ark_short}\n")
else:
    print(f"Searching BnF by title for {arg!r}...\n")
    root = _sru_search(f'bib.title all "{arg}"', max_records=5)
    matches = []
    for dc_el in _iter_dc_elements(root):
        ark = _extract_ark(dc_el)
        title = _get_first(dc_el, "title")
        if ark and title:
            matches.append((ark.split("/")[-1], title))
    if not matches:
        print("ERROR: no title matches found via SRU.")
        sys.exit(1)
    print("=== TOP MATCHES ===")
    for ark_short_m, title in matches:
        print(f"  {ark_short_m}  {title}")
    ark_short = matches[0][0]
    print(f"\nRunning full diagnostics on first match: {ark_short}\n")

ark = f"ark:/12148/{ark_short}"
cql = f'bib.persistentid any "{ark}"'
print(f"Querying BnF SRU for {ark}\n")
root = _sru_search(cql, max_records=1)
dc_el = next(_iter_dc_elements(root), None)
if dc_el is None:
    print("ERROR: No DC element returned -- bad ARK, or record genuinely not found")
    sys.exit(1)

print("=== RAW DC FIELDS ===")
for tag in ("identifier", "description", "creator", "contributor",
            "title", "date", "publisher", "subject", "language",
            "relation", "format", "type"):
    vals = _get_all(dc_el, tag)
    if vals:
        print(f"\ndc:{tag}:")
        for v in vals:
            print(f"  {repr(v)}")

identifiers = extract_identifiers(dc_el)
people = _extract_people(dc_el)
desc = _clean_description(dc_el)
year = _extract_year(dc_el)

print("\n=== EXTRACTED ===")
print(f"ARK:         {identifiers['ark']!r}")
print(f"ISBN-10:     {identifiers['isbn10']!r}")
print(f"ISBN-13:     {identifiers['isbn13']!r}")
print(f"EAN:         {identifiers['ean']!r}")
print(f"Year:        {year!r}")
print(f"People:      {people}")
print(f"Description: {desc!r}")

print("\n=== VERBOSE PROBES (raw HTTP, every candidate) ===")
isbn = identifiers.get("isbn13") or identifiers.get("isbn10")
if isbn:
    verbose_probe("BnF/isbn", f"{BNF_COVER_API_URL}?ISBN={quote(isbn)}&couverture=1")
if identifiers.get("ean"):
    verbose_probe("BnF/ean", f"{BNF_COVER_API_URL}?EAN={identifiers['ean']}&couverture=1")
if identifiers.get("ark"):
    encoded = quote(identifiers["ark"], safe=":/")
    verbose_probe("BnF/ark", f"{BNF_COVER_API_URL}?idArk={encoded}&couverture=1")
if isbn:
    digits = re.sub(r"[\-\s]", "", isbn)
    verbose_probe("OpenLibrary/isbn", f"https://covers.openlibrary.org/b/isbn/{digits}-L.jpg")

print("\n=== COVER RESOLUTION (validate=True, bypassing cache) ===")
bnf_cover = get_bnf_cover(identifiers, validate=True)
print(f"\nBnF cover result:          {bnf_cover!r}")

ol_cover = None
if not bnf_cover:
    ol_cover = get_openlibrary_cover(identifiers, validate=True)
    print(f"Open Library cover result: {ol_cover!r}")

final = resolve_cover(identifiers, validate=True)
print(f"\n=== FINAL (resolve_cover, cache bypassed by direct calls above) ===")
print(f"Selected cover URL: {final}")
