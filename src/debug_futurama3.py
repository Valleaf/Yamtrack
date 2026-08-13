import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app.models import Item, MediaTypes, Sources
from app.providers import services, tmdb

futurama = Item.objects.get(media_id=615, source=Sources.TMDB.value, media_type=MediaTypes.TV.value)
print(f"Futurama item media_id repr: {futurama.media_id!r} (type={type(futurama.media_id)})")

print("\n=== Calling tmdb.tv_changes() ===")
try:
    changed_ids = tmdb.tv_changes()
    print(f"changed_tv_ids count: {len(changed_ids)}")
    print(f"'615' in changed_tv_ids: {'615' in changed_ids}")
    print(f"615 in changed_tv_ids: {615 in changed_ids}")
    sample = list(changed_ids)[:5]
    print(f"sample entries: {sample}")
except Exception as e:
    print(f"FAILED: {type(e).__name__}: {e}")
