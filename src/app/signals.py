import logging

from celery import states
from celery.signals import before_task_publish
from django.db.backends.signals import connection_created
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_results.models import TaskResult

logger = logging.getLogger(__name__)


@receiver(connection_created)
def setup_sqlite_pragmas(sender, connection, **kwargs):  # noqa: ARG001
    """Set up SQLite pragmas for WAL mode and busy timeout on connection creation."""
    if connection.vendor == "sqlite":
        cursor = connection.cursor()
        cursor.execute("PRAGMA journal_mode=wal;")
        cursor.execute("PRAGMA busy_timeout=5000;")
        cursor.close()


@before_task_publish.connect
def create_task_result_on_publish(sender=None, headers=None, body=None, **kwargs):  # noqa: ARG001
    """Create a TaskResult object with PENDING status on task publish.

    https://github.com/celery/django-celery-results/issues/286#issuecomment-1279161047
    """
    if "task" not in headers:
        return

    TaskResult.objects.store_result(
        content_type="application/json",
        content_encoding="utf-8",
        task_id=headers["id"],
        result=None,
        status=states.PENDING,
        task_name=headers["task"],
        task_args=headers.get("argsrepr", ""),
        task_kwargs=headers.get("kwargsrepr", ""),
    )


@receiver(post_save, sender='app.BasicMedia')
def populate_country_on_media_save(sender, instance, created, **kwargs):  # noqa: ARG001
    """Populate country field from provider metadata when media is created/updated."""
    # Only populate if country is not already set
    if instance.country:
        return
    
    try:
        from app import providers
        
        # Fetch metadata from provider to get country info
        metadata = providers.services.get_media_metadata(
            instance.item.media_type,
            instance.item.media_id,
            instance.item.source,
        )
        
        if metadata and metadata.get("details", {}).get("country"):
            instance.country = metadata["details"]["country"]
            # Save without triggering this signal again
            BasicMedia.objects.filter(pk=instance.pk).update(country=instance.country)
            logger.info("Updated country for %s: %s", instance, instance.country)
    except Exception as e:
        # Silently ignore errors - country is optional
        logger.debug("Failed to fetch country for %s: %s", instance, str(e))
