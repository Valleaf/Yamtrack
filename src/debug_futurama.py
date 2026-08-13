import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app.models import Item, TV, Season, MediaTypes, Status
from events.models import Event

items = Item.objects.filter(title__icontains="Futurama")
print(f"Items matching 'Futurama': {items.count()}")
for it in items:
    print(f"  Item id={it.id} media_id={it.media_id} source={it.source} media_type={it.media_type} title={it.title!r} season_number={it.season_number}")

tv_items = items.filter(media_type=MediaTypes.TV.value)
for tv_item in tv_items:
    print(f"\n--- TV item: {tv_item} (media_id={tv_item.media_id}, source={tv_item.source}) ---")
    tv_trackings = TV.objects.filter(item=tv_item)
    for tv in tv_trackings:
        print(f"  TV tracking: user={tv.user} status={tv.status}")

    seasons = Item.objects.filter(
        media_id=tv_item.media_id,
        source=tv_item.source,
        media_type=MediaTypes.SEASON.value,
    )
    print(f"  Season items for this show: {seasons.count()}")
    for s in seasons:
        season_trackings = Season.objects.filter(item=s)
        statuses = [(st.user.username, st.status) for st in season_trackings]
        events = Event.objects.filter(item=s)
        print(f"    Season {s.season_number} (item id={s.id}): season_trackings={statuses}, events={events.count()}")
        for e in events.order_by("datetime")[:10]:
            print(f"       event id={e.id} content_number={e.content_number} datetime={e.datetime}")
