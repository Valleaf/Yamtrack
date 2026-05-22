from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.db.models import Count, Sum
from .models import Collection, CollectionItem
from app.providers import collections_providers
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from .forms import CollectionForm

# --- View Functions ---

@login_required
def collections(request):
    """Displays the grid of all user collections."""
    # Fetch collections for the current user and calculate stats
    collections_list = Collection.objects.filter(owner=request.user).all()

    # Global aggregate stats for all collections owned by the user
    total_items = CollectionItem.objects.filter(collection__owner=request.user).count()
    source_stats = CollectionItem.objects.filter(collection__owner=request.user).values('item__source').annotate(count=Count('item__source')).order_by('-count')
    media_type_stats = CollectionItem.objects.filter(collection__owner=request.user).values('item__media_type').annotate(count=Count('item__media_type')).order_by('-count')

    context = {
        'collections': collections_list,
        'user': request.user,
        'stats': {
            'total_items': total_items,
            'sources': source_stats,
            'media_types': media_type_stats
        }
    }
    return render(request, 'media_collections/collections.html', context)

@login_required
def collection_detail(request, collection_id):
    """Displays details, stats, and items for a specific collection."""
    collection = get_object_or_404(Collection, pk=collection_id, owner=request.user)

    if request.method == 'GET':
        # Calculate stats specific to this collection
        stats = {
            'total_items': collection.collectionitem_set.count(),
            'sources': CollectionItem.objects.filter(collection=collection).values('item__source').annotate(count=Count('item__source')).order_by('-count'),
            'media_types': CollectionItem.objects.filter(collection=collection).values('item__media_type').annotate(count=Count('item__media_type')).order_by('-count')
        }
        
        # Fetch the items and general context
        items = collection.items.select_related('item').all()
        context = {
            'collection': collection,
            'items': items,
            'user': request.user,
            'stats': stats
        }
        return render(request, 'media_collections/collection_detail.html', context)

    elif request.method == 'POST':
        # Handle potential 'sync' or 'update' actions if needed, though sync is usually AJAX
        return redirect('media_collections:collection_detail', collection_id=collection.pk)

@login_required
def create(request):
    """Handles creation of a new collection."""
    if request.method == 'POST':
        # Use a formset or a simple model form for initial creation
        # Implementation detail: needs a basic form structure for name and description
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(owner=request.user)
            # Logic to set initial stats/sources
            return redirect('media_collections:collection_detail', collection_id=collection.pk)
    else:
        form = CollectionForm()
    
    context = {
        'form': form,
        'title': 'Create New Collection'
    }
    return render(request, 'media_collections/create.html', context)


@require_http_methods(["GET", "POST"])
@login_required
def sync_from_source(request, collection_id, source_key, source_id):
    """
    Endpoint to sync items from a specific source and source ID into the collection.
    GET: Displays an overview/status.
    POST: Executes the sync logic.
    """
    collection = get_object_or_404(Collection, pk=collection_id, owner=request.user)

    if request.method == 'POST':
        try:
            # 1. Call the source specific function defined in providers
            source_provider = collections_providers.get_source(source_key)
            if not source_provider:
                return JsonResponse({'success': False, 'error': f'Unknown source provider: {source_key}'}, status=400)

            # 2. Fetch the item data using the source ID
            item_data = source_provider.fetch_item(source_id)
            if not item_data:
                 return JsonResponse({'success': False, 'error': 'Could not fetch item data.'}, status=400)

            # 3. Sync the item into the collection
            from .utils import _sync_source_items
            _sync_source_items(collection, item_data, source_key)
            
            return JsonResponse({'success': True, 'message': 'Item synced successfully.'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    # GET method can handle listing source options for the modal
    return JsonResponse({'success': True, 'message': 'Ready to sync.'})

@login_required
def search_source(request, source_key, query):
    """Endpoint for searching a source (e.g., search_movie, search_person)."""
    if request.method == 'GET':
        try:
            source_provider = collections_providers.get_source(source_key)
            if not source_provider:
                return JsonResponse({'success': False, 'error': f'Unknown source provider: {source_key}'})

            # Call the search method implemented in the provider
            results = source_provider.search_source(query)
            return JsonResponse({'success': True, 'results': results})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@login_required
def search_source_items(request):
    """Handles searching for items across all sources."""
    if request.method == 'GET':
        query = request.GET.get('q')
        if not query:
            return JsonResponse({'success': False, 'error': 'Query parameter required.'})

        # TODO: Implement complex search logic traversing all source providers
        # and aggregating results. Placeholder response.
        return JsonResponse({'success': True, 'results': [{'name': 'Example Search Result'}]})


# --- Modal/Toggle View (for UI interactions) ---

@login_required
@require_http_methods(["GET"])
def collections_modal(request):
    """Populates the modal with source options/search results."""
    # Logic to fetch all sources and pre-populate searchable results
    available_sources = collections_providers.get_all_source_keys()
    context = {
        'sources': available_sources
    }
    return render(request, 'media_collections/collections_modal.html', context)

@login_required
def collection_item_toggle(request):
    """Handles adding/removing an item from a collection."""
    if request.method == 'POST':
        # Expecting POST data: collection_id, item_pk, action ('add' or 'remove')
        try:
            from django.views.decorators.csrf import csrf_exempt
            
            # Assuming this view needs to be wrapped in csrf_exempt for AJAX POSTs
            # (though it's better practice to pass CSRF token)
            # For simplicity in the view, we assume necessary data is available.
            collection_id = request.POST.get('collection_id')
            item_pk = request.POST.get('item_pk')
            action = request.POST.get('action')

            if not all([collection_id, item_pk, action]):
                return JsonResponse({'success': False, 'error': 'Missing data.'}, status=400)
            
            collection = get_object_or_404(Collection, pk=collection_id)
            item = get_object_or_404(Item, pk=item_pk) # Assuming 'Item' model exists
            
            if action == 'add':
                if not CollectionItem.objects.filter(collection=collection, item=item).exists():
                    CollectionItem.objects.create(collection=collection, item=item)
                    message = 'Item added to collection.'
                else:
                    message = 'Item already in collection.'
            elif action == 'remove':
                # Use get_object_or_isnull to safely delete
                try:
                    CollectionItem.objects.get(collection=collection, item=item).delete()
                    message = 'Item removed from collection.'
                except CollectionItem.DoesNotExist:
                    message = 'Item was not found in this collection.'

            return JsonResponse({'success': True, 'message': message})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

# TODO: Implement other necessary utility functions like utility functions used in the app