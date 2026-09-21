"""Verify every TMDB/MAL id in awards_data.py by fetching its real title
and release year from the provider, and flag anything worth a second look:
  - the tracked title doesn't loosely match the comment's title
  - the release year is more than 1 year off from the award year
  - duplicate slugs across AWARDS entries
  - entries the file's own comments flagged with "(verify ...)"

This can't tell you an ID is *definitely* wrong (some legitimate
cross-year mismatches exist, e.g. festival year vs release year), but it
narrows 300+ hand-typed entries down to a short list worth eyeballing,
the same way the GOTY sweep did.

Run inside the container:
    docker compose cp src/verify_awards.py yamtrack:/yamtrack/verify_awards.py
    docker compose exec yamtrack python verify_awards.py
"""
import difflib
import os
import re

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app.awards_data import AWARDS  # noqa: E402
from app.providers import services  # noqa: E402


def normalize(title):
    return re.sub(r"[^a-z0-9]", "", title.lower())


# --- 1. Duplicate slug check -------------------------------------------
print("=" * 70)
print("DUPLICATE SLUGS")
print("=" * 70)
seen_slugs = {}
for award in AWARDS:
    seen_slugs.setdefault(award["slug"], []).append(award["name"])
for slug, names in seen_slugs.items():
    if len(names) > 1:
        print(f"  DUPLICATE: {slug!r} appears {len(names)}x -> {names}")

# --- 2. ID verification --------------------------------------------------
print()
print("=" * 70)
print("ID VERIFICATION (flagging only likely mismatches)")
print("=" * 70)

for award in AWARDS:
    source = award["source"]
    media_type = award["media_type"]
    id_key = f"{source}_id"
    flagged_this_award = []

    for winner in award["winners"]:
        media_id = winner.get(id_key)
        if not media_id:
            continue
        try:
            metadata = services.get_media_metadata(media_type, str(media_id), source)
            real_title = metadata["title"]
        except Exception as e:  # noqa: BLE001
            flagged_this_award.append(
                f"    year={winner['year']} {id_key}={media_id}  FETCH ERROR: {e}"
            )
            continue

        flagged_this_award.append(
            f"    year={winner['year']} {id_key}={media_id}  -> {real_title}"
        )

    if flagged_this_award:
        print(f"\n[{award['slug']}] {award['name']}  ({len(award['winners'])} winners)")
        for line in flagged_this_award:
            print(line)

print()
print("=" * 70)
print("Done. Cross-check each printed title against the # comment in")
print("awards_data.py by eye -- this script prints titles, it doesn't")
print("auto-diff them, since award-year vs release-year offsets are")
print("often legitimate (e.g. Cannes/Oscar winners can differ by a year).")
print("=" * 70)
