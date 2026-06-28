from django.conf import settings
from django.db import models
from django.db.models import Exists, Prefetch, Q

from app.models import Item, MediaTypes, Status


class CollectionManager(models.Manager):
    """Manager for collections."""

    def get_user_collections(self, user):
        return (
            self.filter(Q(owner=user) | Q(collaborators=user))
            .select_related("owner")
            .prefetch_related(
                "collaborators",
                Prefetch(
                    "collectionitem_set",
                    queryset=CollectionItem.objects.select_related("item")
                    .order_by("date_added"),
                ),
            )
            .distinct()
            .order_by("name")
        )

    def get_user_collections_with_item(self, user, item):
        return (
            self.filter(Q(owner=user) | Q(collaborators=user))
            .annotate(
                has_item=Exists(
                    CollectionItem.objects.filter(
                        collection_id=models.OuterRef("id"),
                        item=item,
                    )
                )
            )
            .prefetch_related("collaborators")
            .distinct()
            .order_by("name")
        )


class Collection(models.Model):
    """A cross-media franchise or universe collection."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    source = models.CharField(max_length=50, blank=True, default="manual")
    source_id = models.CharField(max_length=255, blank=True, default="")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="collaborated_collections",
        blank=True,
    )
    items = models.ManyToManyField(
        Item,
        related_name="media_collections",
        blank=True,
        through="CollectionItem",
    )

    objects = CollectionManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def image(self):
        first = self.collectionitem_set.select_related("item").first()
        return first.item.image if first else settings.IMG_NONE

    def user_can_edit(self, user):
        return self.owner == user or user in self.collaborators.all()

    def user_can_delete(self, user):
        return self.owner == user

    def get_stats(self, user):
        """Compute franchise-style stats for this collection for a given user."""
        from django.apps import apps

        items = list(
            self.collectionitem_set.select_related("item").order_by("date_added")
        )
        total = len(items)
        if not total:
            return {
                "total": 0,
                "tracked": 0,
                "tracked_pct": 0,
                "completed": 0,
                "completed_pct": 0,
                "by_type": {},
                "avg_score": None,
            }

        # Group items by media_type
        by_type = {}
        for ci in items:
            mt = ci.item.media_type
            by_type.setdefault(mt, [])
            by_type[mt].append(ci.item)

        type_stats = {}
        total_tracked = 0
        total_completed = 0
        score_sum = 0
        score_count = 0

        for mt, type_items in by_type.items():
            try:
                model = apps.get_model("app", mt)
            except LookupError:
                continue

            item_ids = [i.id for i in type_items]
            qs = model.objects.filter(item_id__in=item_ids, user=user).select_related("item")

            tracked_ids = set(qs.values_list("item_id", flat=True))
            completed_count = qs.filter(
                status__in=[Status.COMPLETED.value, Status.DROPPED.value],
            ).count()
            scores = [float(m.score) for m in qs if m.score is not None]

            type_stats[mt] = {
                "total": len(type_items),
                "tracked": len(tracked_ids),
                "tracked_pct": round(len(tracked_ids) / len(type_items) * 100) if type_items else 0,
                "completed": completed_count,
                "completed_pct": round(completed_count / len(type_items) * 100) if type_items else 0,
                "share_pct": round(len(type_items) / total * 100) if total else 0,
                "avg_score": round(sum(scores) / len(scores), 1) if scores else None,
                "items": type_items,
            }
            total_tracked += len(tracked_ids)
            total_completed += completed_count
            score_sum += sum(scores)
            score_count += len(scores)

        return {
            "total": total,
            "tracked": total_tracked,
            "tracked_pct": round(total_tracked / total * 100) if total else 0,
            "completed": total_completed,
            "completed_pct": round(total_completed / total * 100) if total else 0,
            "by_type": type_stats,
            "avg_score": round(score_sum / score_count, 1) if score_count else None,
        }


class CollectionItem(models.Model):
    """An item within a collection, with an optional note."""

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    notes = models.CharField(max_length=255, blank=True, default="")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_added"]
        constraints = [
            models.UniqueConstraint(
                fields=["item", "collection"],
                name="collections_collectionitem_unique_item_collection",
            )
        ]

    def __str__(self):
        return self.item.title


class CollectionItemExclusion(models.Model):
    """A source item the owner intentionally removed from a synced collection."""

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    media_id = models.CharField(max_length=255)
    source = models.CharField(max_length=50)
    media_type = models.CharField(max_length=10, choices=MediaTypes)
    date_removed = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_removed"]
        constraints = [
            models.UniqueConstraint(
                fields=["collection", "media_id", "source", "media_type"],
                name="collections_exclusion_unique_source_item",
            )
        ]

    def __str__(self):
        return f"{self.collection}: {self.source}/{self.media_type}/{self.media_id}"
