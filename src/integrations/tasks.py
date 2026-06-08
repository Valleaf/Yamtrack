import logging

from celery import shared_task
from django.contrib.auth import get_user_model

import events
from app.mixins import disable_fetch_releases
from app.models import MediaTypes
from app.templatetags import app_tags
from integrations.imports import (
    anilist,
    goodreads,
    helpers,
    hltb,
    imdb,
    kitsu,
    mal,
    senscritique,
    simkl,
    steam,
    trakt,
    yamtrack,
)

logger = logging.getLogger(__name__)
ERROR_TITLE = "\n\n\n Couldn't import the following media: \n\n"


def format_media_type_display(count, media_type):
    """Format media type display with proper pluralization."""
    if count == 0:
        return None
    if count == 1:
        return f"{count} {dict(MediaTypes.choices).get(media_type, media_type)}"
    return f"{count} {app_tags.media_type_readable_plural(media_type)}"


def format_import_message(imported_counts, warning_messages=None):
    """Format the import result message based on counts and warnings."""
    parts = [
        format_media_type_display(count, media_type)
        for media_type, count in imported_counts.items()
    ]
    parts = [p for p in parts if p is not None]

    if not parts:
        info_message = "No media was imported."
    else:
        info_message = f"Imported {helpers.join_with_commas_and(parts)}."

    if warning_messages:
        return f"{info_message} {ERROR_TITLE} {warning_messages}"
    return info_message


def import_media(
    importer_func,
    identifier,
    user_id,
    mode,
    oauth_username=None,
    **kwargs,
):
    """Handle the import process for different media services."""
    user = get_user_model().objects.get(id=user_id)

    with disable_fetch_releases():
        if oauth_username is None:
            imported_counts, warnings = importer_func(
                identifier,
                user,
                mode,
                **kwargs,
            )
        else:
            imported_counts, warnings = importer_func(
                identifier,
                user,
                mode,
                username=oauth_username,
                **kwargs,
            )

    events.tasks.reload_calendar.delay()

    return format_import_message(imported_counts, warnings)


@shared_task(name="Import from Trakt")
def import_trakt(user_id, mode, token=None, username=None, redirect_uri=None):
    """Celery task for importing media data from Trakt.

    Can import using either OAuth (token provided) or public username.
    """
    return import_media(
        trakt.importer,
        token,
        user_id,
        mode,
        username,
        redirect_uri=redirect_uri,
    )


@shared_task(name="Import from SIMKL")
def import_simkl(token, user_id, mode, username=None):  # noqa: ARG001
    """Celery task for importing media data from SIMKL."""
    return import_media(simkl.importer, token, user_id, mode)


@shared_task(name="Import from MyAnimeList")
def import_mal(username, user_id, mode):
    """Celery task for importing anime and manga data from MyAnimeList."""
    return import_media(mal.importer, username, user_id, mode)


@shared_task(name="Import from AniList")
def import_anilist(user_id, mode, token=None, username=None):
    """Celery task for importing media data from AniList."""
    return import_media(anilist.importer, token, user_id, mode, username)


@shared_task(name="Import from Kitsu")
def import_kitsu(username, user_id, mode):
    """Celery task for importing anime and manga data from Kitsu."""
    return import_media(kitsu.importer, username, user_id, mode)


@shared_task(name="Import from Yamtrack")
def import_yamtrack(file, user_id, mode):
    """Celery task for importing media data from Yamtrack."""
    return import_media(yamtrack.importer, file, user_id, mode)


@shared_task(name="Import from HowLongToBeat")
def import_hltb(file, user_id, mode):
    """Celery task for importing media data from HowLongToBeat."""
    return import_media(hltb.importer, file, user_id, mode)


@shared_task(name="Import from Steam")
def import_steam(username, user_id, mode):
    """Celery task for importing game data from Steam."""
    return import_media(steam.importer, username, user_id, mode)


@shared_task(name="Import from IMDB")
def import_imdb(file, user_id, mode):
    """Celery task for importing media data from IMDB."""
    return import_media(imdb.importer, file, user_id, mode)


@shared_task(name="Import from GoodReads")
def import_goodreads(file, user_id, mode):
    """Celery task for importing media data from GoodReads."""
    return import_media(goodreads.importer, file, user_id, mode)


@shared_task(name="Import from SensCritique")
def import_senscritique(file, user_id, mode, allowed_sc_types=None):
    """Celery task for importing media data from SensCritique CSV export.

    ``allowed_sc_types`` is an optional list of raw SC type strings
    (e.g. ["movie", "tv show"]).  None means import all types.
    """
    result = import_media(
        senscritique.importer,
        file,
        user_id,
        mode,
        allowed_sc_types=allowed_sc_types,
    )
    # If there are pending items for review, create a UserMessage with a clickable link
    from integrations.imports.senscritique import get_pending_review
    pending = get_pending_review(user_id)
    if pending:
        from django.urls import reverse
        from django.utils.safestring import mark_safe
        from app.models import UserMessage, UserMessageLevel
        review_url = reverse("senscritique_review") + f"?mode={mode}"
        UserMessage.objects.create(
            user_id=user_id,
            level=UserMessageLevel.INFO,
            message=mark_safe(
                f'{len(pending)} SensCritique items need your review — '
                f'<a href="{review_url}" class="underline text-indigo-300 hover:text-indigo-200">'
                f'visit the review page</a> to approve or reject them.'
            ),
        )
    return result


@shared_task(name="Sync missing artwork")
def sync_missing_artwork():
    """Fetch and save cover images for all tracked Items with no/placeholder image."""
    import time
    from django.conf import settings
    from django.db.models import Q
    from app.models import Item, MediaTypes, Sources

    skip_types = {MediaTypes.SEASON.value, MediaTypes.EPISODE.value}

    items = list(
        Item.objects.filter(
            Q(image="") | Q(image=settings.IMG_NONE)
        ).exclude(
            source=Sources.MANUAL.value
        ).exclude(
            media_type__in=skip_types
        )
    )

    total = len(items)
    updated = 0
    failed = 0

    logger.info("Artwork sync: %d items need artwork", total)
    
    from app.providers.services import get_media_metadata
    for item in items:
        try:
            metadata = get_media_metadata(
                item.media_type,
                item.media_id,
                item.source,
            )
            new_image = metadata.get("image", "")
            if new_image and new_image != settings.IMG_NONE:
                item.image = new_image
                item.save(update_fields=["image"])
                updated += 1
                logger.debug("Updated artwork for %s", item)
            time.sleep(0.05)  # be gentle to external APIs
        except Exception as exc:
            failed += 1
            logger.exception("Artwork sync failed for %s", item)

    msg = f"Synced artwork: {updated} updated out of {total} items"
    if failed:
        msg += f" ({failed} failed)"
    logger.info(msg)
    return msg


@shared_task(name="Confirm SensCritique review")
def confirm_senscritique(
    user_id,
    confirmed_indices,
    mode,
    candidate_overrides=None,
    manual_overrides=None,
):
    """Celery task for importing user-confirmed SensCritique items."""
    from integrations.imports.senscritique import confirm_pending_items
    imported_counts, warnings = confirm_pending_items(
        user_id,
        confirmed_indices,
        mode,
        candidate_overrides=candidate_overrides,
        manual_overrides=manual_overrides,
    )
    return format_import_message(imported_counts, warnings)
