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
