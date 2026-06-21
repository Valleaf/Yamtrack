import logging
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from app.models import UserMessage

logger = logging.getLogger(__name__)


@shared_task(name="Sync external lists")
def sync_external_lists():
    """Sync all configured ExternalLists from TMDB."""
    from app.models import ExternalList, ExternalListItem  # noqa: PLC0415
    from app.providers.tmdb import fetch_list  # noqa: PLC0415

    lists = list(ExternalList.objects.all())
    synced = 0

    for ext_list in lists:
        try:
            raw_items = fetch_list(ext_list.tmdb_list_id)

            # Filter to only items that match this list's media_type.
            # TMDB v3 list items carry a 'media_type' field ("movie" / "tv").
            # Fall back to the list's own media_type when the field is absent.
            matching = [
                item for item in raw_items
                if item.get("media_type", ext_list.media_type) == ext_list.media_type
            ]

            ExternalListItem.objects.filter(external_list=ext_list).delete()
            batch = [
                ExternalListItem(
                    external_list=ext_list,
                    media_id=str(item["id"]),
                    rank=rank,
                )
                for rank, item in enumerate(matching, start=1)
            ]
            ExternalListItem.objects.bulk_create(batch)

            ext_list.item_count = len(batch)
            ext_list.last_synced = timezone.now()
            ext_list.save(update_fields=["item_count", "last_synced"])
            synced += 1
            logger.info("Synced %s (%d items)", ext_list.name, len(batch))

        except Exception:
            logger.exception("Failed to sync external list '%s'", ext_list.name)

    return synced


@shared_task(name="Cleanup user messages")
def cleanup_user_messages():
    """Delete shown user messages older than the configured retention window."""
    cutoff = timezone.now() - timedelta(days=settings.USER_MESSAGE_RETENTION_DAYS)
    deleted_count, _ = UserMessage.objects.filter(
        shown_at__isnull=False,
        shown_at__lt=cutoff,
    ).delete()

    logger.info("Deleted %s old shown user messages.", deleted_count)

    return deleted_count


@shared_task(name="Backfill release years")
def backfill_release_years(progress_every=200):
    """One-time backfill: populate Item.release_year for items tracked
    before that field existed.

    Walks every Item missing release_year (skipping seasons/episodes, which
    don't carry their own release year, and manual entries, which have no
    provider metadata to fetch), fetches metadata through the normal
    provider dispatch -- so already-cached items resolve instantly and
    everything else goes through each source's existing rate limiter --
    and stores the extracted year directly on the row.

    Safe to re-run: only items still missing release_year are touched.
    Trigger manually with:
        docker compose exec yamtrack python manage.py shell -c \\
            "from app.tasks import backfill_release_years; backfill_release_years.delay()"
    """
    from app.date_utils import get_release_year_from_metadata  # noqa: PLC0415
    from app.models import Item, MediaTypes, Sources  # noqa: PLC0415
    from app.providers import services  # noqa: PLC0415

    queryset = (
        Item.objects.filter(release_year__isnull=True)
        .exclude(media_type__in=(MediaTypes.SEASON.value, MediaTypes.EPISODE.value))
        .exclude(source=Sources.MANUAL.value)
    )

    total = queryset.count()
    updated = 0
    no_year = 0
    failed = 0

    logger.info("Release year backfill: %s items to process", total)

    for index, item in enumerate(queryset.iterator(chunk_size=progress_every), start=1):
        try:
            metadata = services.get_media_metadata(
                item.media_type,
                item.media_id,
                item.source,
            )
            year = get_release_year_from_metadata(metadata)
        except Exception:
            failed += 1
            logger.exception(
                "Release year backfill failed for %s/%s/%s",
                item.source,
                item.media_type,
                item.media_id,
            )
            continue

        if year is None:
            no_year += 1
            continue

        item.release_year = year
        item.save(update_fields=["release_year"])
        updated += 1

        if index % progress_every == 0:
            logger.info(
                "Release year backfill: %s/%s processed "
                "(updated=%s, no_year=%s, failed=%s)",
                index, total, updated, no_year, failed,
            )

    logger.info(
        "Release year backfill complete: %s processed, updated=%s, no_year=%s, failed=%s",
        total, updated, no_year, failed,
    )
    return {"total": total, "updated": updated, "no_year": no_year, "failed": failed}
