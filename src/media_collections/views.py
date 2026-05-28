import logging

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from app.models import Status
from app.providers import collections_providers as col_providers

from .models import Collection, CollectionItem

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _user_can_access(user, collection):
    return collection.owner == user or collection.collaborators.filter(pk=user.pk).exists()


def _user_can_edit(user, collection):
    return collection.owner == user


COLLECTION_ITEMS_PER_PAGE_CHOICES = (6, 12, 24)
DEFAULT_COLLECTION_ITEMS_PER_PAGE = 6
COLLECTION_COLUMNS_CHOICES = (3, 4, 5, 6)
DEFAULT_COLLECTION_COLUMNS = 6


def _get_items_per_page(request):
    try:
        per_page = int(request.GET.get("per_page", DEFAULT_COLLECTION_ITEMS_PER_PAGE))
    except (TypeError, ValueError):
        return DEFAULT_COLLECTION_ITEMS_PER_PAGE

    if per_page not in COLLECTION_ITEMS_PER_PAGE_CHOICES:
        return DEFAULT_COLLECTION_ITEMS_PER_PAGE
    return per_page


def _get_columns(request):
    try:
        columns = int(request.GET.get("columns", DEFAULT_COLLECTION_COLUMNS))
    except (TypeError, ValueError):
        return DEFAULT_COLLECTION_COLUMNS

    if columns not in COLLECTION_COLUMNS_CHOICES:
        return DEFAULT_COLLECTION_COLUMNS
    return columns


def _paginate(items, request, page_param):
    paginator = Paginator(items, _get_items_per_page(request))
    return paginator.get_page(request.GET.get(page_param, 1))


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------

@login_required
def collections(request):
    """Show all collections for the user — auto-sourced and manual."""
    owned = (
        Collection.objects.filter(owner=request.user)
        .prefetch_related("collectionitem_set__item")
        .order_by("name")
    )
    collab = (
        Collection.objects.filter(collaborators=request.user)
        .prefetch_related("collectionitem_set__item")
        .order_by("name")
    )

    # Split owned into auto-sourced vs manual
    auto_collections = [c for c in owned if c.source and c.source != "manual"]
    manual_collections = [c for c in owned if not c.source or c.source == "manual"]
    per_page = _get_items_per_page(request)

    return render(request, "media_collections/collections.html", {
        "auto_collections": _paginate(auto_collections, request, "auto_page"),
        "manual_collections": _paginate(manual_collections, request, "manual_page"),
        "collab_collections": _paginate(collab, request, "collab_page"),
        "items_per_page": per_page,
        "items_per_page_choices": COLLECTION_ITEMS_PER_PAGE_CHOICES,
        "columns": _get_columns(request),
        "columns_choices": COLLECTION_COLUMNS_CHOICES,
    })


# ---------------------------------------------------------------------------
# Detail
# ---------------------------------------------------------------------------

@login_required
def collection_detail(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    if not _user_can_access(request.user, collection):
        messages.error(request, "You don't have access to this collection.")
        return redirect("media_collections")

    media_type_filter = request.GET.get("type", "all")
    stats = collection.get_stats(request.user)

    collection_items = (
        CollectionItem.objects.filter(collection=collection)
        .select_related("item")
        .order_by("date_added")
    )
    if media_type_filter != "all":
        collection_items = collection_items.filter(item__media_type=media_type_filter)

    per_page = _get_items_per_page(request)
    paginator = Paginator(collection_items, per_page)
    collection_items_page = paginator.get_page(request.GET.get("page", 1))

    page_items = list(collection_items_page)
    item_ids_by_type = {}
    for ci in page_items:
        item_ids_by_type.setdefault(ci.item.media_type, []).append(ci.item_id)

    tracked_by_item_id = {}
    for media_type, item_ids in item_ids_by_type.items():
        try:
            model = apps.get_model("app", media_type)
        except LookupError:
            continue

        for media in model.objects.filter(item_id__in=item_ids, user=request.user).select_related("item"):
            tracked_by_item_id[media.item_id] = media

    for ci in page_items:
        tracked = tracked_by_item_id.get(ci.item_id)
        ci.tracked = bool(tracked)
        ci.completed = bool(tracked and tracked.status == Status.COMPLETED.value)

    collection_items_page.object_list = page_items

    all_types = list(
        CollectionItem.objects.filter(collection=collection)
        .values_list("item__media_type", flat=True)
        .distinct()
        .order_by("item__media_type")
    )

    return render(request, "media_collections/collection_detail.html", {
        "collection": collection,
        "collection_items": collection_items_page,
        "items_per_page": per_page,
        "items_per_page_choices": COLLECTION_ITEMS_PER_PAGE_CHOICES,
        "columns": _get_columns(request),
        "columns_choices": COLLECTION_COLUMNS_CHOICES,
        "stats": stats,
        "media_type_filter": media_type_filter,
        "all_types": all_types,
        "show_type_tabs": len(all_types) > 1,
        "can_edit": _user_can_edit(request.user, collection),
        "source_label": col_providers.get_source_label(collection.source) if collection.source else "",
        "sources": col_providers.SOURCE_CHOICES,
    })


# ---------------------------------------------------------------------------
# Create (import from source — no manual entry)
# ---------------------------------------------------------------------------

@login_required
def create(request):
    """Import a collection from TMDB or another source."""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        source = request.POST.get("source", "tmdb_collection")
        source_id = request.POST.get("source_id", "").strip()

        if not name:
            messages.error(request, "A collection name is required.")
            return render(request, "media_collections/create.html", {
                "sources": col_providers.SOURCE_CHOICES,
                "post": request.POST,
            })

        if not source_id:
            messages.error(request, "Please search for and select a collection.")
            return render(request, "media_collections/create.html", {
                "sources": col_providers.SOURCE_CHOICES,
                "post": request.POST,
            })

        collection = Collection.objects.create(
            name=name,
            description=description,
            source=source,
            source_id=source_id,
            owner=request.user,
        )

        try:
            data = col_providers.fetch(source, source_id)
            if data:
                added = _sync_items(collection, data["items"])
                # Use the official name from the source
                if data.get("name"):
                    collection.name = data["name"]
                    collection.description = data.get("description", description)
                    collection.save(update_fields=["name", "description"])
                messages.success(request, f'"{collection.name}" imported with {added} items.')
            else:
                messages.warning(request, "Collection created but no data returned from source.")
        except Exception as exc:
            logger.exception("Collection sync failed")
            messages.warning(request, f"Collection created but sync failed: {exc}")

        return redirect("collection_detail", collection_id=collection.pk)

    return render(request, "media_collections/create.html", {
        "sources": col_providers.SOURCE_CHOICES,
    })


# ---------------------------------------------------------------------------
# Edit
# ---------------------------------------------------------------------------

@login_required
def edit(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    if not _user_can_edit(request.user, collection):
        messages.error(request, "Only the owner can edit this collection.")
        return redirect("collection_detail", collection_id=collection_id)

    if request.method == "POST":
        collection.name = request.POST.get("name", collection.name).strip()
        collection.description = request.POST.get("description", collection.description).strip()
        collection.save()
        messages.success(request, "Collection updated.")
        return redirect("collection_detail", collection_id=collection_id)

    return render(request, "media_collections/edit.html", {
        "collection": collection,
    })


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------

@login_required
@require_POST
def delete(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    if not _user_can_edit(request.user, collection):
        messages.error(request, "Only the owner can delete this collection.")
        return redirect("collection_detail", collection_id=collection_id)

    collection.delete()
    messages.success(request, "Collection deleted.")
    return redirect("media_collections")


# ---------------------------------------------------------------------------
# Sync from source
# ---------------------------------------------------------------------------

def _sync_items(collection, items):
    """Replace CollectionItems with the given list, deduplicating by item."""
    from app.models import Item

    # Deduplicate incoming items by media_id to avoid creating duplicate rows
    seen_ids = set()
    unique_items = []
    for entry in items:
        key = (str(entry["media_id"]), entry["source"], entry["media_type"])
        if key not in seen_ids:
            seen_ids.add(key)
            unique_items.append(entry)

    # Get existing CollectionItem ids for this collection
    existing_item_ids = set(
        CollectionItem.objects.filter(collection=collection)
        .values_list("item__media_id", flat=True)
    )

    added = 0
    for entry in unique_items:
        title = (entry["title"] or "").strip()
        image = entry.get("image", "")
        item, item_new = Item.objects.get_or_create(
            media_id=str(entry["media_id"]),
            source=entry["source"],
            media_type=entry["media_type"],
            defaults={"title": title, "image": image},
        )
        if not item_new and (not item.title or not item.image):
            update_fields = []
            if not item.title and title:
                item.title = title
                update_fields.append("title")
            if not item.image and image:
                item.image = image
                update_fields.append("image")
            if update_fields:
                item.save(update_fields=update_fields)

        _, created = CollectionItem.objects.get_or_create(
            collection=collection,
            item=item,
            defaults={"notes": ""},
        )
        if created:
            added += 1

    # Remove any CollectionItems that are no longer in the source
    valid_item_ids = {str(e["media_id"]) for e in unique_items}
    stale = CollectionItem.objects.filter(collection=collection).exclude(
        item__media_id__in=valid_item_ids
    )
    removed = stale.count()
    stale.delete()
    if removed:
        logger.info("Removed %d stale items from '%s'", removed, collection.name)

    return added


@login_required
@require_POST
def sync_from_source(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    if not _user_can_edit(request.user, collection):
        messages.error(request, "Only the owner can sync this collection.")
        return redirect("collection_detail", collection_id=collection_id)

    if not collection.source or collection.source == "manual":
        messages.warning(request, "Manual collections cannot be synced from a source.")
        return redirect("collection_detail", collection_id=collection_id)

    if not collection.source_id:
        messages.error(request, "This collection has no source ID — cannot sync.")
        return redirect("collection_detail", collection_id=collection_id)

    try:
        data = col_providers.fetch(collection.source, collection.source_id)
        if not data:
            messages.error(request, "Source returned no data.")
        else:
            added = _sync_items(collection, data["items"])
            if data.get("name"):
                collection.name = data["name"]
                collection.save(update_fields=["name"])
            messages.success(request, f"Sync complete: {added} new items added.")
    except Exception as exc:
        logger.exception("Sync failed")
        messages.error(request, f"Sync failed: {exc}")

    return redirect("collection_detail", collection_id=collection_id)


# ---------------------------------------------------------------------------
# Search source (HTMX)
# ---------------------------------------------------------------------------

@login_required
def search_source(request):
    """HTMX: search collections by name on a given source."""
    source = request.GET.get("source", "").strip()
    query = request.GET.get("q", "").strip()

    results = []
    error = None

    if source and query and len(query) >= 2:
        try:
            results = col_providers.search(source, query)
        except Exception as exc:
            error = f"Search error: {exc}"

    return render(request, "media_collections/components/source_search_results.html", {
        "results": results,
        "source": source,
        "query": query,
        "error": error,
    })


# ---------------------------------------------------------------------------
# Collections modal (HTMX — shown from item detail pages)
# ---------------------------------------------------------------------------

@login_required
def collections_modal(request, source, media_type, media_id, season_number=None):
    from app.models import Item
    from django.db.models import Exists, OuterRef

    item = Item.objects.filter(
        source=source, media_type=media_type, media_id=media_id
    ).first()

    user_collections = Collection.objects.filter(
        owner=request.user
    ).annotate(
        has_item=Exists(
            CollectionItem.objects.filter(
                collection_id=OuterRef("pk"),
                item=item,
            )
        ) if item else Exists(CollectionItem.objects.none())
    ).order_by("name")

    return render(request, "media_collections/components/fill_collections.html", {
        "source": source,
        "media_type": media_type,
        "media_id": media_id,
        "season_number": season_number,
        "user_collections": user_collections,
    })


# ---------------------------------------------------------------------------
# Toggle item in / out of a collection (HTMX)
# ---------------------------------------------------------------------------

@login_required
@require_POST
def collection_item_toggle(request):
    from app.models import Item
    collection_id = request.POST.get("collection_id")
    source = request.POST.get("source")
    media_type = request.POST.get("media_type")
    media_id = request.POST.get("media_id")

    collection = get_object_or_404(Collection, pk=collection_id)
    if not _user_can_edit(request.user, collection):
        return HttpResponse("Forbidden", status=403)

    item, _ = Item.objects.get_or_create(
        source=source,
        media_type=media_type,
        media_id=media_id,
    )

    ci = CollectionItem.objects.filter(collection=collection, item=item).first()
    if ci:
        ci.delete()
        in_collection = False
    else:
        CollectionItem.objects.create(collection=collection, item=item)
        in_collection = True

    # HTMX request: return the button partial for inline swap
    if request.headers.get("HX-Request"):
        return render(request, "media_collections/components/collection_item_button.html", {
            "collection": collection,
            "source": source,
            "media_type": media_type,
            "media_id": media_id,
            "has_item": in_collection,
        })

    # Plain form POST: redirect back to referring page
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER")
    if next_url:
        return redirect(next_url)
    return redirect("collection_detail", collection_id=collection.pk)
