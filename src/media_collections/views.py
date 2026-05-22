from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from app.providers import collections_providers as col_providers

from .models import Collection, CollectionItem


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _user_can_access(user, collection):
    return collection.owner == user or collection.collaborators.filter(pk=user.pk).exists()


def _user_can_edit(user, collection):
    return collection.owner == user


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------

@login_required
def collections(request):
    owned = Collection.objects.filter(owner=request.user).prefetch_related("collectionitem_set__item")
    collab = Collection.objects.filter(collaborators=request.user).prefetch_related("collectionitem_set__item")
    return render(request, "media_collections/collections.html", {
        "owned_collections": owned,
        "collab_collections": collab,
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

    all_types = (
        CollectionItem.objects.filter(collection=collection)
        .values_list("item__media_type", flat=True)
        .distinct()
    )

    return render(request, "media_collections/collection_detail.html", {
        "collection": collection,
        "collection_items": collection_items,
        "stats": stats,
        "media_type_filter": media_type_filter,
        "all_types": sorted(all_types),
        "can_edit": _user_can_edit(request.user, collection),
        "source_label": col_providers.get_source_label(collection.source) if collection.source else "",
        "sources": col_providers.SOURCE_CHOICES,
    })


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------

@login_required
def create(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        source = request.POST.get("source", "manual")
        source_id = request.POST.get("source_id", "").strip()

        if not name:
            messages.error(request, "A collection name is required.")
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

        if source != "manual" and source_id:
            try:
                data = col_providers.fetch(source, source_id)
                if data:
                    added = _sync_items(collection, data["items"])
                    messages.success(request, f'Collection "{name}" created and synced ({added} items added).')
                else:
                    messages.warning(request, f'Collection created but no data returned from source.')
            except Exception as exc:
                messages.warning(request, f'Collection created but sync failed: {exc}')
        else:
            messages.success(request, f'Collection "{name}" created.')

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
        "sources": col_providers.SOURCE_CHOICES,
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
    """Create Item stubs + CollectionItems for fetched provider items. Returns count added."""
    from app.models import Item
    added = 0
    for entry in items:
        item, _ = Item.objects.get_or_create(
            media_id=entry["media_id"],
            source=entry["source"],
            media_type=entry["media_type"],
            defaults={"title": entry["title"], "image": entry.get("image", "")},
        )
        _, created = CollectionItem.objects.get_or_create(
            collection=collection,
            item=item,
            defaults={"notes": ""},
        )
        if created:
            added += 1
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
            messages.success(request, f"Sync complete: {added} new items added.")
    except Exception as exc:
        messages.error(request, f"Sync failed: {exc}")

    return redirect("collection_detail", collection_id=collection_id)


# ---------------------------------------------------------------------------
# Search source (HTMX)
# ---------------------------------------------------------------------------

@login_required
def search_source(request):
    """
    HTMX endpoint: GET /collection/search_source?source=tmdb_collection&q=marvel
    Returns a partial with result rows the user can pick from.
    """
    source = request.GET.get("source", "").strip()
    query = request.GET.get("q", "").strip()

    results = []
    error = None

    if source and query:
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
# Signature matches urls.py: source / media_type / media_id [/ season_number]
# ---------------------------------------------------------------------------

@login_required
def collections_modal(request, source, media_type, media_id, season_number=None):
    from app.models import Item
    from django.db.models import Exists, OuterRef

    item = Item.objects.filter(source=source, media_type=media_type, media_id=media_id).first()

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

    return render(request, "media_collections/components/collection_item_button.html", {
        "collection": collection,
        "source": source,
        "media_type": media_type,
        "media_id": media_id,
        "has_item": in_collection,
    })
