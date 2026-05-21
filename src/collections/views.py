import logging

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from app import helpers
from app.models import Item, MediaTypes
from app.providers import services
from collections.forms import CollectionForm
from collections.models import Collection, CollectionItem

logger = logging.getLogger(__name__)


@require_GET
def collections(request):
    """List all collections for the current user."""
    user_collections = Collection.objects.get_user_collections(request.user)
    form = CollectionForm()
    return render(request, "collections/collections.html", {
        "collections": user_collections,
        "form": form,
    })


@require_GET
def collection_detail(request, collection_id):
    """Detail page for a single collection with franchise stats."""
    collection = get_object_or_404(
        Collection.objects.select_related("owner").prefetch_related("collaborators"),
        id=collection_id,
    )
    if not collection.user_can_edit(request.user) and collection.owner != request.user:
        raise Http404

    media_type_filter = request.GET.get("type", "all")
    items_qs = collection.collectionitem_set.select_related("item").order_by("date_added")
    if media_type_filter != "all":
        items_qs = items_qs.filter(item__media_type=media_type_filter)

    stats = collection.get_stats(request.user)
    form = CollectionForm(instance=collection)

    return render(request, "collections/collection_detail.html", {
        "collection": collection,
        "collection_items": items_qs,
        "stats": stats,
        "form": form,
        "media_type_filter": media_type_filter,
        "media_types": MediaTypes.values,
    })


@require_POST
def create(request):
    form = CollectionForm(request.POST)
    if form.is_valid():
        col = form.save(commit=False)
        col.owner = request.user
        col.save()
        form.save_m2m()
        logger.info("%s collection created.", col)
    else:
        helpers.form_error_messages(form, request)
    return helpers.redirect_back(request)


@require_POST
def edit(request):
    col_id = request.POST.get("collection_id")
    col = get_object_or_404(Collection, id=col_id)
    if col.user_can_edit(request.user):
        form = CollectionForm(request.POST, instance=col)
        if form.is_valid():
            form.save()
    else:
        messages.error(request, "You do not have permission to edit this collection.")
    return helpers.redirect_back(request)


@require_POST
def delete(request):
    col_id = request.POST.get("collection_id")
    col = get_object_or_404(Collection, id=col_id)
    if col.user_can_delete(request.user):
        col.delete()
        return redirect("collections")
    messages.error(request, "You do not have permission to delete this collection.")
    return helpers.redirect_back(request)


@require_GET
def collections_modal(request, source, media_type, media_id, season_number=None):
    """Modal showing collections the user can add an item to."""
    try:
        item = Item.objects.get(
            media_id=media_id, source=source, media_type=media_type,
            season_number=season_number,
        )
    except Item.DoesNotExist:
        metadata = services.get_media_metadata(media_type, media_id, source, [season_number])
        item = Item.objects.create(
            media_id=media_id, source=source, media_type=media_type,
            season_number=season_number,
            title=metadata["title"], image=metadata["image"],
            country=metadata.get("country") or "",
        )
    user_collections = Collection.objects.get_user_collections_with_item(request.user, item)
    return render(request, "collections/components/fill_collections.html", {
        "item": item,
        "user_collections": user_collections,
    })


@require_POST
def collection_item_toggle(request):
    """Add or remove an item from a collection."""
    item_id = request.POST["item_id"]
    collection_id = request.POST["collection_id"]
    item = get_object_or_404(Item, id=item_id)
    col = get_object_or_404(Collection, id=collection_id)
    if not col.user_can_edit(request.user):
        raise Http404

    if col.items.filter(id=item.id).exists():
        col.items.remove(item)
        has_item = False
    else:
        col.items.add(item)
        has_item = True

    return render(request, "collections/components/collection_item_button.html", {
        "collection": col, "item": item, "has_item": has_item,
    })
