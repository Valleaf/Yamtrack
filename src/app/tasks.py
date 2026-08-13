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


@shared_task(name="Populate media country")
def populate_media_country(media_pk):
    """Fetch country of origin from provider metadata for one BasicMedia row.

    Runs off the request path (queued from app.signals.populate_country_on_media_save)
    so a slow or retried provider call never blocks a web request or holds its
    DB connection open. Country is best-effort/optional, so any failure is
    logged and swallowed rather than retried.
    """
    from app.models import BasicMedia  # noqa: PLC0415
    from app.providers import services  # noqa: PLC0415

    try:
        instance = BasicMedia.objects.select_related("item").get(pk=media_pk)
    except BasicMedia.DoesNotExist:
        return

    # may already have been populated (e.g. duplicate signal fire)
    if instance.country:
        return

    try:
        metadata = services.get_media_metadata(
            instance.item.media_type,
            instance.item.media_id,
            instance.item.source,
        )
    except Exception as e:
        # Silently ignore errors - country is optional
        logger.debug("Failed to fetch country for media pk=%s: %s", media_pk, str(e))
        return

    country = metadata.get("details", {}).get("country") if metadata else None
    if country:
        BasicMedia.objects.filter(pk=media_pk).update(country=country)
        logger.info("Updated country for media pk=%s: %s", media_pk, country)


@shared_task(name="Backup database")
def backup_database():
    """Create a compressed database backup and prune old ones.

    No-ops if DB_BACKUP_ENABLED is False, so the periodic schedule entry
    can stay registered while the feature is toggled off via env var.
    """
    if not settings.DB_BACKUP_ENABLED:
        logger.info("Database backup skipped: DB_BACKUP_ENABLED is False")
        return

    from django.core.management import call_command  # noqa: PLC0415

    call_command("backup_db")


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


@shared_task(name="Sync all tracked media")
def sync_all_tracked_media(progress_every=50):
    """Refresh provider metadata for every tracked, non-manual item.

    The per-item "Sync" button on a detail page (app.views.sync_metadata)
    does this one item at a time; this task is the bulk equivalent, meant
    to run on a schedule (see CELERY_BEAT_SCHEDULE) so titles, artwork,
    and release-year data stay current without anyone having to click
    through their whole library by hand.

    Scope: TV, movie, anime, manga, game, book, comic, boardgame, and
    music Items that have at least one tracking row (BasicMedia via any
    of the per-media-type models) -- i.e. actually tracked, not just
    referenced (season/episode Items are refreshed as a side effect of
    their parent TV item's fetch_releases() call, same as the manual
    sync button). Manual entries are skipped since they have no provider
    to sync against.

    Deliberately reuses services.get_media_metadata rather than calling
    provider APIs directly, so it goes through the same rate limiters as
    everything else and benefits from any items that are already cache-warm.

    Safe to re-run; every run is a full pass, not a delta. Trigger
    manually with:
        docker compose exec yamtrack python manage.py shell -c \\
            "from app.tasks import sync_all_tracked_media; sync_all_tracked_media.delay()"
    """
    from app.date_utils import get_release_year_from_metadata  # noqa: PLC0415
    from app.models import Item, MediaTypes, Sources  # noqa: PLC0415
    from app.providers import services  # noqa: PLC0415

    # Media types with their own top-level Item + tracking model. Seasons
    # and episodes are intentionally excluded -- they're refreshed when
    # their parent TV item's fetch_releases() runs below, same as the
    # manual per-item sync button does for a TV show's seasons.
    trackable_media_types = [
        MediaTypes.TV.value,
        MediaTypes.MOVIE.value,
        MediaTypes.ANIME.value,
        MediaTypes.MANGA.value,
        MediaTypes.GAME.value,
        MediaTypes.BOOK.value,
        MediaTypes.COMIC.value,
        MediaTypes.BOARDGAME.value,
        MediaTypes.MUSIC.value,
    ]

    queryset = (
        Item.objects.filter(media_type__in=trackable_media_types)
        .exclude(source=Sources.MANUAL.value)
        .distinct()
    )

    total = queryset.count()
    updated = 0
    unchanged = 0
    failed = 0

    logger.info("Full media sync: %s items to process", total)

    for index, item in enumerate(queryset.iterator(chunk_size=progress_every), start=1):
        try:
            metadata = services.get_media_metadata(
                item.media_type,
                item.media_id,
                item.source,
            )
        except Exception:
            failed += 1
            logger.exception(
                "Full media sync failed for %s/%s/%s",
                item.source, item.media_type, item.media_id,
            )
            continue

        update_fields = []

        if metadata.get("title") and metadata["title"] != item.title:
            item.title = metadata["title"]
            update_fields.append("title")

        if metadata.get("image") and metadata["image"] != item.image:
            item.image = metadata["image"]
            update_fields.append("image")

        country = metadata.get("country", "")
        if country and country != item.country:
            item.country = country
            update_fields.append("country")

        if item.release_year is None:
            release_year = get_release_year_from_metadata(metadata)
            if release_year is not None:
                item.release_year = release_year
                update_fields.append("release_year")

        if update_fields:
            item.save(update_fields=update_fields)
            updated += 1
        else:
            unchanged += 1

        # Picks up new seasons/episodes/releases for TV shows the same way
        # the manual sync button does; cheap no-op for other media types.
        item.fetch_releases(delay=True)

        if index % progress_every == 0:
            logger.info(
                "Full media sync: %s/%s processed (updated=%s, unchanged=%s, failed=%s)",
                index, total, updated, unchanged, failed,
            )

    logger.info(
        "Full media sync complete: %s processed, updated=%s, unchanged=%s, failed=%s",
        total, updated, unchanged, failed,
    )
    return {"total": total, "updated": updated, "unchanged": unchanged, "failed": failed}


@shared_task(bind=True, name="Warm statistics cache")
def warm_statistics_cache(self, user_id):
    """Rebuild and cache the all-time statistics context for one user.

    Queued with a short countdown from app.signals whenever tracked media
    changes, so the expensive per-section computation happens in the
    background instead of on a user's next page load. Only warms the
    all-time (no date range) view, since that's what the page opens to by
    default; any other date range the user picks still computes on first
    request as before.

    Debounced by task id: app.signals stamps a "latest scheduled task"
    token in cache each time it schedules this task. A burst of saves (e.g.
    a CSV import) each schedule a run ~30s out and overwrite that token, so
    when an earlier-scheduled run finally executes it checks whether it's
    still the one the token points to -- if a later save superseded it,
    it skips, and only the last-scheduled run (which fires after the burst
    settles) actually rebuilds.
    """
    from django.contrib.auth import get_user_model  # noqa: PLC0415
    from django.core.cache import cache  # noqa: PLC0415

    from app import statistics as stats  # noqa: PLC0415

    token_key = f"statistics:warm-token:{user_id}"
    current_token = cache.get(token_key)
    if current_token is not None and current_token != self.request.id:
        logger.debug("Statistics warm-up for user %s superseded, skipping", user_id)
        return

    User = get_user_model()  # noqa: N806
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return

    stats.get_statistics_context(user, None, None)
    logger.info("Warmed statistics cache for %s", user)


@shared_task(name="Backfill people metadata cache")
def backfill_people_metadata_cache(progress_every=200):
    """One-time backfill: warm the provider-metadata cache for tracked
    movies and music albums so the Statistics page's Top People section
    (directors/actors/artists) has something to read.

    get_people_stats() is intentionally cache-only -- no live API calls
    from the stats page -- so any item whose metadata was never fetched
    silently contributes nothing to the directors/actors/artists lists.
    That's normally fine (visiting a detail page or the Movie Directors
    tab warms it), but the SensCritique and FilmAffinity importers only
    do a lightweight TMDB search match and create the Item directly --
    they never call tmdb.movie(), so imported movies stay cache-cold
    until someone happens to open them individually.

    Walks every Movie/Music Item still missing a cache entry and fetches
    it once through the normal provider dispatch, which caches as a side
    effect (same trick backfill_release_years uses).

    Safe to re-run: items already cached are skipped via a cache.get check.
    Trigger manually with:
        docker compose exec yamtrack python manage.py shell -c \\
            "from app.tasks import backfill_people_metadata_cache; backfill_people_metadata_cache.delay()"
    """
    from django.core.cache import cache  # noqa: PLC0415
    from django.db.models import Q  # noqa: PLC0415

    from app.models import Item, MediaTypes, Sources  # noqa: PLC0415
    from app.providers import services  # noqa: PLC0415

    queryset = Item.objects.filter(
        Q(media_type=MediaTypes.MOVIE.value, source=Sources.TMDB.value)
        | Q(media_type=MediaTypes.MUSIC.value, source=Sources.MUSICBRAINZ.value),
    )

    total = queryset.count()
    warmed = 0
    already_cached = 0
    failed = 0

    logger.info("People metadata cache backfill: %s items to check", total)

    for index, item in enumerate(queryset.iterator(chunk_size=progress_every), start=1):
        cache_key = f"{item.source}_{item.media_type}_{item.media_id}"
        if cache.get(cache_key) is not None:
            already_cached += 1
        else:
            try:
                services.get_media_metadata(item.media_type, item.media_id, item.source)
                warmed += 1
            except Exception:
                failed += 1
                logger.exception(
                    "People metadata backfill failed for %s/%s/%s",
                    item.source, item.media_type, item.media_id,
                )

        if index % progress_every == 0:
            logger.info(
                "People metadata cache backfill: %s/%s checked "
                "(warmed=%s, already_cached=%s, failed=%s)",
                index, total, warmed, already_cached, failed,
            )

    logger.info(
        "People metadata cache backfill complete: %s checked, "
        "warmed=%s, already_cached=%s, failed=%s",
        total, warmed, already_cached, failed,
    )
    return {
        "total": total,
        "warmed": warmed,
        "already_cached": already_cached,
        "failed": failed,
    }
