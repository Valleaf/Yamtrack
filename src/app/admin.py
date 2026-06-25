import contextlib

from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from app.models import (
    Episode,
    ExternalList,
    ExternalListItem,
    Item,
    PersistentCacheEntry,
    UserMessage,
)


# Custom ModelAdmin classes with search functionality
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Custom admin for Item model with search and filter options."""

    search_fields = ["title", "media_id", "source"]
    list_display = [
        "title",
        "media_id",
        "season_number",
        "episode_number",
        "media_type",
        "source",
    ]
    list_filter = ["media_type", "source"]


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    """Custom admin for Episode model with search and filter options."""

    search_fields = ["item__title", "related_season__item__title"]
    list_display = ["__str__", "end_date"]


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    """Custom admin for persistent user messages."""

    search_fields = ["user__username", "message"]
    list_display = ["message", "level", "user", "created_at", "shown_at"]
    list_filter = ["level", "shown_at"]


@admin.register(ExternalList)
class ExternalListAdmin(admin.ModelAdmin):
    """Admin for curated external lists."""

    list_display = ["name", "media_type", "tmdb_list_id", "item_count", "last_synced"]
    list_filter = ["media_type"]
    search_fields = ["name", "slug", "tmdb_list_id"]
    readonly_fields = ["item_count", "last_synced"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ExternalListItem)
class ExternalListItemAdmin(admin.ModelAdmin):
    """Admin for individual entries within external lists."""

    list_display = ["external_list", "rank", "media_id"]
    list_filter = ["external_list"]
    search_fields = ["media_id", "external_list__name"]
    raw_id_fields = ["external_list"]


@admin.register(PersistentCacheEntry)
class PersistentCacheEntryAdmin(admin.ModelAdmin):
    """Admin for the durable cache backing store.

    Mostly useful for spot-checking what's persisted or manually evicting a
    stuck/stale entry without waiting on a Redis TTL.
    """

    search_fields = ["key"]
    list_display = ["key", "updated_at"]
    readonly_fields = ["key", "value", "updated_at"]


class MediaAdmin(admin.ModelAdmin):
    """Custom admin for regular media model with search and filter options."""

    search_fields = ["item__title", "user__username", "notes"]
    list_display = ["__str__", "status", "score", "user"]
    list_filter = ["status"]


# Register models with custom admin classes


# Auto-register remaining models
app_models = apps.get_app_config("app").get_models()
SpecialModels = ["Item", "Episode", "BasicMedia", "UserMessage", "PersistentCacheEntry"]
for model in app_models:
    if (
        not model.__name__.startswith("Historical")
        and model.__name__ not in SpecialModels
    ):
        with contextlib.suppress(AlreadyRegistered):
            admin.site.register(model, MediaAdmin)
