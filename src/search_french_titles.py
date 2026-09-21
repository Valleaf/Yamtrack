"""Search TMDB directly for the 8 French-language César/Berlinale titles
that scored LOW CONFIDENCE in the first resolve pass (their English-search
matches were noise). Prints candidates for each so the correct id can be
picked by hand.

Run inside the container:
    docker compose cp src/search_french_titles.py yamtrack:/yamtrack/search_french_titles.py
    docker compose exec yamtrack python search_french_titles.py
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app.models import Sources  # noqa: E402
from app.providers import services, tmdb  # noqa: E402

TITLES = [
    ("cesar_best_film", 2021, "De leur vivant"),
    ("cesar_best_film", 2019, "Jusqu'à la garde"),
    ("cesar_best_film", 2018, "120 battements par minute"),
    ("cesar_best_film", 2016, "La loi du marché"),
    ("cesar_best_film", 2014, "La vie d'Adèle"),
    ("cesar_best_film", 2011, "Des hommes et des dieux"),
    ("cesar_best_film", 2010, "Un prophète"),
    ("berlinale_jury_grand_prix", 2023, "Sur l'Adamant"),
]

for slug, year, title in TITLES:
    r = services.api_request(
        Sources.TMDB.value, "GET", "https://api.themoviedb.org/3/search/movie",
        params={**tmdb.base_params, "query": title},
    )
    print(f"\n--- [{slug}] {year}: {title!r} ---")
    for x in r.get("results", [])[:5]:
        print(f"  id={x['id']:<8} {x.get('release_date')}  {x['title']}")
