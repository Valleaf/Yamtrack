"""Background discovery of releases by artists represented in user libraries."""

import logging
from collections import defaultdict

from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from app.models import Item, MediaTypes, Music, Sources
from app.providers import musicbrainz
from events.calendar.helpers import date_parser
from events.models import MusicReleaseDiscovery

logger = logging.getLogger(__name__)

LOOKBACK_DAYS = 365
LOOKAHEAD_DAYS = 90


def _tracked_artists():
    """Return artist IDs mapped to users and their already-tracked albums."""
    artist_users = defaultdict(set)
    artist_names = {}
    tracked_items = defaultdict(set)

    for music in Music.objects.select_related("item", "user"):
        tracked_items[music.user_id].add(music.item.media_id)
        metadata = cache.get(
            f"{music.item.source}_{music.item.media_type}_{music.item.media_id}",
        ) or {}
        for artist in metadata.get("artist_links", []):
            artist_id = artist.get("id")
            if not artist_id:
                continue
            artist_users[artist_id].add(music.user_id)
            artist_names[artist_id] = artist.get("name", "")

    return artist_users, artist_names, tracked_items


def sync_music_release_discoveries():
    """Discover recent/upcoming releases for all artists in tracked libraries.

    MusicBrainz release-group responses are shared globally through the cache,
    so identical artists across users only produce one provider request per
    cache week.  Full album metadata and cover art remain lazy.
    """
    artist_users, artist_names, tracked_items = _tracked_artists()
    if not artist_users:
        return {"artists": 0, "releases": 0}

    today = timezone.localdate()
    earliest = today - timezone.timedelta(days=LOOKBACK_DAYS)
    latest = today + timezone.timedelta(days=LOOKAHEAD_DAYS)
    discovered = 0

    for artist_id, user_ids in artist_users.items():
        try:
            release_groups = musicbrainz.artist_release_groups(artist_id)
        except Exception:  # provider errors must not stop other artists
            logger.exception("MusicBrainz release discovery failed for %s", artist_id)
            continue

        for group in release_groups:
            release_date = group.get("release_date")
            if not release_date:
                continue
            try:
                release_datetime = date_parser(release_date)
            except ValueError:
                continue
            release_day = release_datetime.date()
            if not earliest <= release_day <= latest:
                continue

            media_id = group.get("media_id")
            if not media_id:
                continue
            with transaction.atomic():
                item, _ = Item.objects.update_or_create(
                    media_id=media_id,
                    source=Sources.MUSICBRAINZ.value,
                    media_type=MediaTypes.MUSIC.value,
                    defaults={
                        "title": group.get("title", ""),
                        "image": group.get("image", ""),
                        "release_year": int(group["year"])
                        if str(group.get("year") or "").isdigit()
                        else None,
                    },
                )
                for user_id in user_ids:
                    if media_id in tracked_items[user_id]:
                        continue
                    _, created = MusicReleaseDiscovery.objects.update_or_create(
                        user_id=user_id,
                        item=item,
                        defaults={
                            "artist_names": artist_names.get(artist_id, ""),
                            "release_date": release_datetime,
                        },
                    )
                    discovered += int(created)

    logger.info(
        "Music release discovery checked %d artists and added %d releases",
        len(artist_users),
        discovered,
    )
    return {"artists": len(artist_users), "releases": discovered}
