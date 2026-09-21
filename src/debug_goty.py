"""Debug script: print the actual IGDB title for every GOTY-award igdb_id
in awards_data.py, so we can spot which one(s) are pointing at the wrong
game (transposed digit, wrong IGDB entry, etc).

Run inside the container:
    docker compose cp src/debug_goty.py yamtrack:/yamtrack/debug_goty.py
    docker compose exec yamtrack python debug_goty.py
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app.awards_data import AWARDS  # noqa: E402
from app.providers import igdb  # noqa: E402

GOTY_SLUGS = {"game_awards_goty", "dice_goty", "golden_joystick_goty"}

for award in AWARDS:
    if award["slug"] not in GOTY_SLUGS:
        continue
    print(f"\n=== {award['name']} ({award['slug']}) ===")
    for winner in award["winners"]:
        igdb_id = winner["igdb_id"]
        try:
            data = igdb.game(igdb_id)
            title = data["title"]
        except Exception as e:  # noqa: BLE001
            title = f"ERROR: {e}"
        print(f"  {winner['year']}  igdb_id={igdb_id:<8}  -> {title}")
