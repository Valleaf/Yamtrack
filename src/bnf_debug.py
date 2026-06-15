"""Run: docker compose exec yamtrack python /yamtrack/bnf_debug.py <ark_short>"""
import os, sys
sys.path.insert(0, '/yamtrack')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from app.providers.bnf import (
    _sru_search, _iter_dc_elements, _get_all,
    _extract_ean_isbn, _extract_people, _clean_description, _best_cover_url
)

ark_short = sys.argv[1] if len(sys.argv) > 1 else "cb43416465x"
ark = f"ark:/12148/{ark_short}"
cql = f'bib.persistentid any "{ark}"'
print(f"Querying BnF SRU for {ark}\n")
root = _sru_search(cql, max_records=1)
dc_el = next(_iter_dc_elements(root), None)
if dc_el is None:
    print("ERROR: No DC element returned")
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

ean, isbn = _extract_ean_isbn(dc_el)
people = _extract_people(dc_el)
desc = _clean_description(dc_el)
cover = _best_cover_url(ark, ean, isbn)

print("\n=== EXTRACTED ===")
print(f"EAN:    {ean!r}")
print(f"ISBN:   {isbn!r}")
print(f"People: {people}")
print(f"Desc:   {desc!r}")
print(f"Cover:  {cover}")
