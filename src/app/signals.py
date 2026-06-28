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
    """Queue an async job to populate country from provider metadata.

    This used to fetch metadata inline, synchronously, inside the post_save
    signal -- meaning a slow/retried provider call (e.g. an IGDB token
    refresh) blocked the whole request and held its DB connection the
    entire time. With only one sync gunicorn worker, that froze the app
    for every user and starved the DB pool, taking down /health/ with it.
    Dispatching to Celery keeps the request fast and decouples provider
    latency from the request/DB-connection lifecycle entirely.
    """
    # Only populate if country is not already set
    if instance.country:
        return

    from app.tasks import populate_media_country  # noqa: PLC0415

    populate_media_country.delay(instance.pk)
