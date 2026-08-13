import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app.models import Item, MediaTypes, Sources
from app.providers import services, tmdb
from events.calendar.selectors import (
    get_changed_tmdb_tv_ids,
    _tv_item_has_missing_seasons,
)

futurama = Item.objects.get(media_id=615, source=Sources.TMDB.value, media_type=MediaTypes.TV.value)
print(f"Futurama item: {futurama}")

try:
    tv_metadata = tmdb.tv(futurama.media_id)
    seasons = tv_metadata.get("related", {}).get("seasons", [])
    print(f"TMDB reports {len(seasons)} seasons:")
    for s in seasons:
        print(f"  season_number={s.get('season_number')}")
    print(f"next_episode_season: {tv_metadata.get('next_episode_season')}")
except services.ProviderAPIError as e:
    print(f"TMDB fetch FAILED: {e}")

try:
    changed_ids = get_changed_tmdb_tv_ids()
    print(f"\nchanged_tv_ids count: {len(changed_ids)}")
    print(f"Futurama (615) in changed_tv_ids: {615 in changed_ids}")
except Exception as e:
    print(f"get_changed_tmdb_tv_ids FAILED: {e}")

try:
    missing = _tv_item_has_missing_seasons(futurama)
    print(f"\n_tv_item_has_missing_seasons(futurama): {missing}")
except Exception as e:
    print(f"_tv_item_has_missing_seasons FAILED: {e}")
