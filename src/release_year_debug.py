"""Debug script: diagnose why release-year stats are empty.

Run inside the container:
    docker compose exec yamtrack python release_year_debug.py
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from django.core.cache import cache  # noqa: E402

from app import statistics as stats  # noqa: E402
from app.date_utils import get_release_year_from_metadata  # noqa: E402

User = get_user_model()

for user in User.objects.all():
    user_media, media_count = stats.get_user_media(user, None, None)
    print(f"\n=== user: {user} (total={media_count['total']}) ===")

    total = 0
    cache_hit = 0
    cache_miss = 0
    year_found = 0
    by_type = {}
    shown = 0

    for media_type, media_list in user_media.items():
        if media_type in stats._RELEASE_YEAR_SKIP:
            continue
        entry = by_type.setdefault(
            media_type, {"total": 0, "hit": 0, "miss": 0, "year": 0},
        )
        for media in media_list:
            total += 1
            entry["total"] += 1
            cache_key = (
                f"{media.item.source}_{media.item.media_type}_{media.item.media_id}"
            )
            metadata = cache.get(cache_key)
            if metadata is None:
                cache_miss += 1
                entry["miss"] += 1
                continue
            cache_hit += 1
            entry["hit"] += 1
            year = get_release_year_from_metadata(metadata)
            if year is not None:
                year_found += 1
                entry["year"] += 1
            elif shown < 15:  # noqa: SIM102
                shown += 1
                print(
                    f"  NO YEAR  {media.item.source}/{media.item.media_type}/"
                    f"{media.item.media_id}  details={metadata.get('details')!r}",
                )

    print(
        f"  total={total} cache_hit={cache_hit} cache_miss={cache_miss} "
        f"year_found={year_found}",
    )
    for mt, e in sorted(by_type.items()):
        print(
            f"    {mt:10s} total={e['total']:4d} hit={e['hit']:4d} "
            f"miss={e['miss']:4d} year={e['year']:4d}",
        )
