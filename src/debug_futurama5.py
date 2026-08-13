import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app.models import Item, MediaTypes, Sources
from app.providers import tmdb
from events.calendar.tv import get_tvmaze_episode_map, get_tvmaze_response
from django.core.cache import cache

futurama = Item.objects.get(media_id=615, source=Sources.TMDB.value, media_type=MediaTypes.TV.value)

tv_metadata = tmdb.tv(futurama.media_id)
print(f"tvdb_id from TMDB: {tv_metadata.get('tvdb_id')}")

# clear cache to force fresh fetch
tvdb_id = tv_metadata.get("tvdb_id")
cache.delete(f"tvmaze_map_{tvdb_id}")

show_response = get_tvmaze_response(tvdb_id)
if show_response:
    print(f"TVMaze show id: {show_response.get('id')}, name: {show_response.get('name')}")
    episodes = show_response.get("_embedded", {}).get("episodes", [])
    print(f"Total TVMaze episodes: {len(episodes)}")
    # find episodes tagged season 11 by tvmaze
    s11 = [ep for ep in episodes if ep.get("season") == 11]
    print(f"\nTVMaze season=11 episodes ({len(s11)}):")
    for ep in s11[:12]:
        print(f"  ep {ep.get('number')}: {ep.get('name')} airstamp={ep.get('airstamp')}")

    # also show what the actual Aug 2026 episodes are tagged as in TVMaze
    print("\nTVMaze episodes with airstamp in 2026:")
    for ep in episodes:
        stamp = ep.get("airstamp") or ""
        if stamp.startswith("2026"):
            print(f"  season={ep.get('season')} ep={ep.get('number')}: {ep.get('name')} airstamp={stamp}")
else:
    print("No TVMaze response")
