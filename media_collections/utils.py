from .models import Collection, Item, CollectionItem
from django.db import transaction

def _sync_source_items(collection, item_data: dict, source_key: str) -> None:
    """
    Syncs item data from an external source and creates/updates necessary records.

    Args:
        collection (Collection): The target collection object.
        item_data (dict): Dictionary containing item metadata from the source.
        source_key (str): The key identifying the source (e.g., 'imdb', 'trakt').
    """
    if not item_data:
        return

    # 1. Attempt to find or create the canonical Item record
    # Use media_id and source to uniquely identify the item
    media_id = item_data.get('id')
    if not media_id:
        print(f"Warning: Item data missing 'id' for source {source_key}. Skipping sync.")
        return

    # Using get_or_create ensures we don't duplicate item metadata
    # We use the media_id and source_key for the unique constraint check
    item_obj, created = Item.objects.get_or_create(
        media_id=media_id,
        source=source_key,
        defaults={
            'title': item_data.get('title'),
            'media_type': item_data.get('type'),
            'image': item_data.get('image'),
            'overview': item_data.get('overview'),
            'source_url': item_data.get('url')
        }
    )

    # Update item if new data is richer
    if created:
        print(f"Created new canonical Item: {item_obj.title}")
    else:
        # Simple logic: update title if needed
        item_obj.title = item_data.get('title') or item_obj.title
        item_obj.save()

    # 2. Create the CollectionItem link
    # Check if the item is already linked to this collection
    collectionitem, created = CollectionItem.objects.get_or_create(
        collection=collection,
        item=item_obj
    )
    
    if created:
        print(f"Successfully linked Item '{item_obj.title}' to Collection '{collection.name}'.")
    else:
        print(f"Item '{item_obj.title}' is already in collection '{collection.name}'.")