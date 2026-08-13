"""Debug script: inspect raw IGDB behavior for London Seirei Tantei-dan.

Run inside the container:
    docker compose cp src/igdb_debug.py yamtrack:/yamtrack/igdb_debug.py
    docker compose exec yamtrack python igdb_debug.py
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings  # noqa: E402

from app.models import Sources  # noqa: E402
from app.providers import igdb, services  # noqa: E402

QUERY = "London Seirei Tantei-dan"

access_token = igdb.get_access_token()
url = f"{igdb.base_url}/multiquery"
headers = {
    "Client-ID": settings.IGDB_ID,
    "Authorization": f"Bearer {access_token}",
}

# 1. Same name-match the app uses, but WITHOUT the game_type/theme filters,
#    to see if IGDB's fuzzy name search finds the title at all.
base_conditions_unfiltered = f'where name ~ *"{QUERY}"*'
mq = (
    'query games "SearchResults" {'
    "fields name,game_type,themes,total_rating_count,first_release_date;"
    "limit 50;"
    f"{base_conditions_unfiltered};"
    "};"
)
resp = services.api_request(Sources.IGDB.value, "POST", url, data=mq, headers=headers)
print("=== UNFILTERED name search (full title) ===")
for r in resp[0]["result"]:
    print(r)
if not resp[0]["result"]:
    print("  (no results at all -- fuzzy name match failed)")

# 2. With the app's real filters (game_type whitelist + NSFW theme exclusion)
base_conditions_filtered = (
    f'where name ~ *"{QUERY}"* & game_type = (0,1,2,3,4,5,6,7,8,9,10)'
)
if not settings.IGDB_NSFW:
    base_conditions_filtered += " & themes != (42)"
mq2 = (
    'query games "SearchResults" {'
    "fields name,game_type,themes,total_rating_count,first_release_date;"
    "limit 50;"
    f"{base_conditions_filtered};"
    "};"
)
resp2 = services.api_request(Sources.IGDB.value, "POST", url, data=mq2, headers=headers)
print()
print("=== FILTERED (app's actual query, full title) ===")
for r in resp2[0]["result"]:
    print(r)
if not resp2[0]["result"]:
    print("  (present in unfiltered but dropped by game_type/theme filter!)"
          if resp[0]["result"] else "  (no results -- filters aren't the issue)")

# 3. Try shorter substrings to see how fuzzy matching behaves, and where the
#    real title lands in the "London" result set (pagination/ranking check).
for partial in ["Seirei Tantei-dan", "Seirei Tantei dan", "Tantei-dan", "London"]:
    cond = f'where name ~ *"{partial}"* & game_type = (0,1,2,3,4,5,6,7,8,9,10)'
    if not settings.IGDB_NSFW:
        cond += " & themes != (42)"
    mq3 = (
        'query games "SearchResults" {'
        "fields name,total_rating_count;"
        "sort total_rating_count desc;"
        "limit 24;"
        f"{cond};"
        "};"
        'query games/count "TotalCount" {'
        f"{cond};"
        "};"
    )
    resp3 = services.api_request(
        Sources.IGDB.value, "POST", url, data=mq3, headers=headers,
    )
    results = next((i["result"] for i in resp3 if i["name"] == "SearchResults"), [])
    total = next((i["count"] for i in resp3 if i["name"] == "TotalCount"), 0)
    names = [r["name"] for r in results]
    found = any("tantei" in n.lower() or "seirei" in n.lower() for n in names)
    print()
    print(f"=== partial='{partial}' total_results={total} found_on_page1={found} ===")
    if partial == "London":
        print(f"  (page 1 of {total} total results, PER_PAGE={settings.PER_PAGE})")
        print("  top 24 by rating count:", names)
