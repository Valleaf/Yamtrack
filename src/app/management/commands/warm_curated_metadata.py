"""Management command: warm the provider-metadata cache for every ID committed
in app/awards_data.py and app/external_lists_data.py.

Both fixtures are hand-curated lists of external-provider IDs (TMDB,
MusicBrainz, IGDB, Hardcover, MAL, BnF, ...) that back the "Awards & Lists"
statistics section. That section is intentionally cache-only -- no live API
calls from the stats page -- so any ID nobody has ever tracked or visited
shows up as "Unknown title (ID <n>)" instead of its real title, even though
the ID itself is valid and already committed to the fixture.

This command walks every winner/item across both fixtures, skips whatever
is already cached (or already has a shared Item row, which the stats page
reads first anyway), and fetches the rest through the normal provider
dispatch (app.providers.services.get_media_metadata), which caches the
result as a side effect -- same trick used by
app.tasks.backfill_people_metadata_cache and app.tasks.backfill_release_years.

Safe to re-run: already-cached/already-tracked IDs are skipped via a
cache.get / Item lookup, so running this after adding new fixture rows only
fetches the new ones.

Usage:
    docker compose exec yamtrack python manage.py warm_curated_metadata
    docker compose exec yamtrack python manage.py warm_curated_metadata --dry-run
"""

import logging

from django.core.cache import cache
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Warm the metadata cache for every ID in awards_data.py / external_lists_data.py."""

    help = (
        "Fetch and cache provider metadata for every award-winner / curated-list "
        "ID that isn't already cached, so the Statistics page stops showing "
        "'Unknown title' placeholders for valid, already-committed IDs."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List what would be fetched without making any provider requests.",
        )

    def handle(self, *args, **options):
        from app.awards_data import AWARDS  # noqa: PLC0415
        from app.external_lists_data import LISTS  # noqa: PLC0415
        from app.models import Item  # noqa: PLC0415
        from app.providers import services  # noqa: PLC0415

        dry_run = options["dry_run"]

        # Collect unique (source, media_type, media_id) triples across both
        # fixtures. A dict (not set) so we can report duplicates removed.
        targets = {}

        for award in AWARDS:
            source = award["source"]
            media_type = award["media_type"]
            id_key = f"{source}_id"
            for winner in award["winners"]:
                media_id = winner.get(id_key)
                if not media_id:
                    continue
                targets[(source, media_type, str(media_id))] = award["name"]

        for curated_list in LISTS:
            source = curated_list["source"]
            media_type = curated_list["media_type"]
            id_key = f"{source}_id"
            for item in curated_list["items"]:
                media_id = item.get(id_key)
                if not media_id:
                    continue
                targets[(source, media_type, str(media_id))] = curated_list["name"]

        total = len(targets)
        self.stdout.write(f"Found {total} unique IDs across AWARDS + LISTS.")

        # Anything with a shared Item row already has a title the stats page
        # can read directly (get_award_winners_detail / get_list_winners_detail
        # check Item before falling back to cache) -- no need to hit the
        # provider API for those, even if the metadata cache itself is cold.
        existing_item_keys = set(
            Item.objects.filter(
                media_id__in={mid for (_, _, mid) in targets},
            ).values_list("source", "media_type", "media_id"),
        )

        already_cached = 0
        already_tracked = 0
        to_fetch = []

        for (source, media_type, media_id), origin in targets.items():
            if (source, media_type, media_id) in existing_item_keys:
                already_tracked += 1
                continue
            cache_key = f"{source}_{media_type}_{media_id}"
            if cache.get(cache_key) is not None:
                already_cached += 1
                continue
            to_fetch.append((source, media_type, media_id, origin))

        self.stdout.write(
            f"{already_tracked} already have a tracked Item row, "
            f"{already_cached} already cache-warm, "
            f"{len(to_fetch)} need fetching.",
        )

        if dry_run:
            for source, media_type, media_id, origin in to_fetch:
                self.stdout.write(f"  would fetch: {source}/{media_type}/{media_id}  ({origin})")
            self.stdout.write(self.style.SUCCESS("Dry run complete -- no requests made."))
            return

        warmed = 0
        failed = 0

        for index, (source, media_type, media_id, origin) in enumerate(to_fetch, start=1):
            try:
                services.get_media_metadata(media_type, media_id, source)
                warmed += 1
            except Exception:
                failed += 1
                logger.exception(
                    "Failed to warm metadata for %s/%s/%s (%s)",
                    source, media_type, media_id, origin,
                )
                self.stdout.write(
                    self.style.WARNING(
                        f"  FAILED: {source}/{media_type}/{media_id}  ({origin})",
                    ),
                )

            if index % 25 == 0 or index == len(to_fetch):
                self.stdout.write(f"  {index}/{len(to_fetch)} processed...")

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. warmed={warmed} failed={failed} "
                f"(already_tracked={already_tracked} already_cached={already_cached})",
            ),
        )
        logger.info(
            "warm_curated_metadata complete: total=%s warmed=%s failed=%s "
            "already_tracked=%s already_cached=%s",
            total, warmed, failed, already_tracked, already_cached,
        )
