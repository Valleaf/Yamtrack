#!/usr/bin/env python
"""Debug script - run with: docker compose exec yamtrack python /yamtrack/debug_igdb.py"""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.core.cache import cache
from app.models import Sources, MediaTypes
from app.providers import igdb, services

# GTA V IGDB ID
GAME_ID = "1020"

print(f"\n=== Checking cache for igdb_game_{GAME_ID} ===")
cache_key = f"{Sources.IGDB.value}_{MediaTypes.GAME.value}_{GAME_ID}"
cached = cache.get(cache_key)
if cached:
    print(f"Cache HIT. igdb_collection in cache: {cached.get('igdb_collection')}")
    print(f"Keys in cached data: {list(cached.keys())}")
else:
    print("Cache MISS - will fetch fresh")

print(f"\n=== Deleting cache and fetching fresh from IGDB ===")
cache.delete(cache_key)

try:
    data = igdb.game(GAME_ID)
    print(f"Title: {data.get('title')}")
    print(f"igdb_collection: {data.get('igdb_collection')}")
    col = data.get('igdb_collection')
    if col:
        print(f"  Collection name: {col.get('name')}")
        print(f"  Collection id: {col.get('id')}")
        print(f"  Parts count: {len(col.get('parts', []))}")
        for p in col.get('parts', [])[:5]:
            print(f"    - {p.get('title')} ({p.get('media_id')})")
    else:
        print("  NO collection data returned from IGDB API")
except Exception as e:
    print(f"ERROR: {e}")

print(f"\n=== Checking DB for tracked games ===")
from app.models import Game
games = Game.objects.select_related('item').all()
for g in games:
    print(f"  {g.item.title} | media_id={g.item.media_id} | user={g.user}")

print(f"\n=== Checking Collections DB ===")
from media_collections.models import Collection
cols = Collection.objects.all()
for c in cols:
    print(f"  Collection: {c.name} | source={c.source} | source_id={c.source_id} | owner={c.owner}")
