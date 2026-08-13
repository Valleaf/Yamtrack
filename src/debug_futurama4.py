import os
import django
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

logging.basicConfig(level=logging.INFO)

from app.models import Item, MediaTypes, Sources
from events.calendar.main import fetch_releases
from events.models import Event

futurama = Item.objects.get(media_id=615, source=Sources.TMDB.value, media_type=MediaTypes.TV.value)
print(f"Running fetch_releases for: {futurama}")

result = fetch_releases(items_to_process=[futurama])
print(f"\n=== RESULT ===\n{result}")

print("\n=== Season 11 events AFTER sync ===")
season11 = Item.objects.get(media_id=615, source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, season_number=11)
for e in Event.objects.filter(item=season11).order_by("content_number"):
    print(f"  ep{e.content_number}: {e.datetime}")
