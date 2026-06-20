"""Run inside the container:
  docker compose exec yamtrack python /yamtrack/bnf_series_debug.py "<title>" "<series guess>"

Diagnoses BnF series/collection lookup for a single BD album:
  1. Finds the album by title, dumps every raw DC field (looking
     specifically at dc:relation, dc:title, dc:source -- candidates
     for where BnF puts the series statement).
  2. Runs the raw bib.serie CQL query directly (bypassing
     search_by_series()) so we can see numberOfRecords even if our
     own parsing has a bug.
  3. Runs search_by_series() itself and prints what it returns.

Bypasses Redis cache entirely -- always reflects current code/network
state.
"""
import os, sys
sys.path.insert(0, '/yamtrack')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(name)s: %(message)s")

import django
django.setup()

from app.providers.bnf import (
    _sru_search, _iter_dc_elements, _get_all, _extract_ark, _get_first, _srw,
    search_by_series,
)

title_query = sys.argv[1] if len(sys.argv) > 1 else "Lucky Luke contre Pat Poker"
series_query = sys.argv[2] if len(sys.argv) > 2 else "Lucky Luke"

print(f"=== STEP 1: find album by title: {title_query!r} ===\n")
try:
    root = _sru_search(f'bib.title all "{title_query}"', max_records=3)
except Exception as exc:
    print(f"SRU title search FAILED: {exc!r}")
    sys.exit(1)

num_el = root.find(_srw("numberOfRecords"))
print(f"numberOfRecords: {num_el.text if num_el is not None else '???'}")

dc_els = list(_iter_dc_elements(root))
if not dc_els:
    print("No DC records returned for this title search.")
    sys.exit(1)

for i, dc_el in enumerate(dc_els):
    ark = _extract_ark(dc_el)
    title = _get_first(dc_el, "title")
    print(f"\n--- record {i}: {title!r} (ark={ark}) ---")
    for tag in ("title", "relation", "source", "description", "identifier"):
        vals = _get_all(dc_el, tag)
        if vals:
            print(f"  dc:{tag}:")
            for v in vals:
                print(f"    {v!r}")

print(f"\n\n=== STEP 2: raw CQL bib.serie query for {series_query!r} ===\n")
cql = f'bib.serie all "{series_query}"'
print(f"CQL: {cql}")
try:
    root2 = _sru_search(cql, max_records=5)
    num_el2 = root2.find(_srw("numberOfRecords"))
    print(f"numberOfRecords: {num_el2.text if num_el2 is not None else '???'}")
    dc_els2 = list(_iter_dc_elements(root2))
    print(f"Parsed DC records: {len(dc_els2)}")
    for dc_el in dc_els2[:5]:
        print(f"  - {_get_first(dc_el, 'title')!r}")
except Exception as exc:
    print(f"bib.serie CQL query FAILED: {exc!r}")

print(f"\n\n=== STEP 3: search_by_series({series_query!r}) ===\n")
try:
    results = search_by_series(series_query)
    print(f"Returned {len(results)} results:")
    for r in results[:15]:
        print(f"  - {r['title']!r}  (media_id={r['media_id']})")
except Exception as exc:
    print(f"search_by_series FAILED: {exc!r}")
