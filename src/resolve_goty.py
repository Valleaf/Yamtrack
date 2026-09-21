"""Resolve correct IGDB IDs for GOTY winners by searching IGDB directly,
since debug_goty.py showed the currently-stored igdb_ids point to the
wrong games entirely (transposed/wrong IDs, never actually verified).

Run inside the container:
    docker compose cp src/resolve_goty.py yamtrack:/yamtrack/resolve_goty.py
    docker compose exec yamtrack python resolve_goty.py
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings  # noqa: E402

from app.providers import igdb  # noqa: E402
from app.providers import services  # noqa: E402
from app.models import Sources  # noqa: E402

# (year, title-to-search) for every winner across the three GOTY awards.
# Deduplicated -- Game Awards / DICE / Golden Joystick share most winners.
CANDIDATES = [
    (2024, "Astro Bot"),
    (2023, "Baldur's Gate 3"),
    (2022, "Elden Ring"),
    (2021, "It Takes Two"),
    (2020, "The Last of Us Part II"),
    (2019, "Sekiro: Shadows Die Twice"),
    (2018, "God of War"),
    (2017, "The Legend of Zelda: Breath of the Wild"),
    (2016, "Overwatch"),
    (2015, "The Witcher 3: Wild Hunt"),
    (2014, "Dragon Age: Inquisition"),
]


def search_exact(title):
    """Use the raw IGDB search endpoint (not the app's fuzzy search()) to
    list candidate id/name pairs with release year, sorted by rating count
    so the most-likely-correct (most well known) match is first.
    """
    access_token = igdb.get_access_token()
    url = f"{igdb.base_url}/games"
    query = (
        f'fields name,first_release_date,total_rating_count,game_type,version_parent;'
        f'search "{title}";'
        f"limit 10;"
    )
    headers = {
        "Client-ID": settings.IGDB_ID,
        "Authorization": f"Bearer {access_token}",
    }
    return services.api_request(
        Sources.IGDB.value, "POST", url, data=query, headers=headers,
    )


for year, title in CANDIDATES:
    print(f"\n=== {year}  searching: {title!r} ===")
    try:
        results = search_exact(title)
    except Exception as e:  # noqa: BLE001
        print(f"  ERROR: {e}")
        continue
    for r in results:
        rel = r.get("first_release_date")
        rel_year = None
        if rel:
            from django.utils import timezone
            rel_year = timezone.datetime.fromtimestamp(
                rel, tz=timezone.get_current_timezone(),
            ).year
        print(
            f"  id={r['id']:<8} rating_count={r.get('total_rating_count', 0):<6} "
            f"release_year={rel_year}  game_type={r.get('game_type')}  "
            f"name={r['name']!r}"
        )
