from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class Collection(models.Model):
    """
    Represents a user-created collection of media items.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_lxs="owner")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

    def __str__(self):
        return self.name

    def get_stats(self):
        """Calculates and returns a dictionary of comprehensive statistics for the collection."""
        
        # Statistics specific to this collection instance
        stats = {
            "total_items": self.collectionitem_set.count(),
            "source_stats": CollectionItem.objects.filter(collection=self).values('item__source').annotate(count=Count('item__source')).order_by('-count'),
            "media_type_stats": CollectionItem.objects.filter(collection=self).values('item__media_type').annotate(count=Count('item__media_type')).order_by('-count')
        }
        return stats

class Item(models.Model):
    """
    A canonical representation of a single media item, regardless of its source.
    Using this model prevents duplication of item metadata across different collection entries.
    """
    media_id = models.CharField(max_length=100, unique=True, help_text="Unique ID provided by the external source (e.g., IMDB ID).")
    source = models.CharField(max_length=50)
    media_type = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=500, blank=True)
    overview = models.TextField(blank=True, null=True)
    source_url = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = "Media Item"
        verbose_name_plural = "Media Items"
        unique_together = ('media_id', 'source')

    def __str__(self):
        return self.title

class CollectionItem(models.Model):
    """
    Junction model linking a Collection to a specific Item.
    """
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_lxs="collection")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_lxs="item")
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Collection Item Link"
        verbose_name_plural = "Collection Item Links"
        unique_together = ('collection', 'item')

    def __str__(self):
        return f"{self.collection.name} contains {self.item.title}"

# Note: Since we are calculating stats in the view layer for now,
# we rely on the item_count property above.