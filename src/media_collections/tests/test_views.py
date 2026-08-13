from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app.models import Item, MediaTypes, Sources
from media_collections.models import (
    Collection,
    CollectionItem,
    CollectionItemExclusion,
)
from media_collections.views import _sync_items


class CollectionDetailViewTests(TestCase):
    def setUp(self):
        self.credentials = {"username": "test", "password": "12345"}
        self.user = get_user_model().objects.create_user(**self.credentials)
        self.client.login(**self.credentials)
        self.collection = Collection.objects.create(
            name="Test Collection",
            owner=self.user,
        )

    def _add_items(self, count):
        items = [
            Item(
                media_id=str(index),
                source=Sources.TMDB.value,
                media_type=MediaTypes.MOVIE.value,
                title=f"Movie {index}",
                image="http://example.com/image.jpg",
            )
            for index in range(count)
        ]
        Item.objects.bulk_create(items)
        CollectionItem.objects.bulk_create(
            [
                CollectionItem(collection=self.collection, item=item)
                for item in Item.objects.order_by("id")
            ]
        )

    def test_collection_detail_uses_default_page_size(self):
        self._add_items(60)

        response = self.client.get(
            reverse("collection_detail", kwargs={"collection_id": self.collection.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items_per_page"], 6)
        self.assertEqual(len(response.context["collection_items"]), 6)
        self.assertContains(response, "Add to Planned")

    def test_collection_detail_accepts_series_position_sort(self):
        self._add_items(2)
        response = self.client.get(
            reverse("collection_detail", kwargs={"collection_id": self.collection.id})
            + "?item_sort=series_position"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["item_sort"], "series_position")

    def test_collection_detail_accepts_page_size_choice(self):
        self._add_items(60)

        response = self.client.get(
            reverse("collection_detail", kwargs={"collection_id": self.collection.id})
            + "?per_page=12&page=2"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items_per_page"], 12)
        self.assertEqual(response.context["collection_items"].number, 2)
        self.assertEqual(len(response.context["collection_items"]), 12)

    def test_collection_detail_rejects_unknown_page_size(self):
        self._add_items(60)

        response = self.client.get(
            reverse("collection_detail", kwargs={"collection_id": self.collection.id})
            + "?per_page=999"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items_per_page"], 6)

    def test_collection_detail_accepts_column_choice(self):
        self._add_items(8)

        response = self.client.get(
            reverse("collection_detail", kwargs={"collection_id": self.collection.id})
            + "?columns=4"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["columns"], 4)

    def test_collections_overview_uses_default_page_size(self):
        for index in range(8):
            Collection.objects.create(
                name=f"Auto Collection {index}",
                owner=self.user,
                source="tmdb_collection",
                source_id=str(index),
            )

        response = self.client.get(reverse("media_collections"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["items_per_page"], 6)
        self.assertEqual(response.context["columns"], 6)
        self.assertEqual(len(response.context["auto_collections"]), 6)
        self.assertTrue(response.context["auto_collections"].has_next())

    def test_removed_source_item_is_not_readded_on_sync(self):
        self.collection.source = "tmdb_collection"
        self.collection.source_id = "collection-1"
        self.collection.save(update_fields=["source", "source_id"])
        item = Item.objects.create(
            media_id="1",
            source=Sources.TMDB.value,
            media_type=MediaTypes.MOVIE.value,
            title="Movie 1",
            image="http://example.com/image.jpg",
        )
        CollectionItem.objects.create(collection=self.collection, item=item)

        response = self.client.post(
            reverse("collection_item_toggle"),
            {
                "collection_id": self.collection.id,
                "source": item.source,
                "media_type": item.media_type,
                "media_id": item.media_id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            CollectionItem.objects.filter(collection=self.collection, item=item).exists()
        )
        self.assertTrue(
            CollectionItemExclusion.objects.filter(
                collection=self.collection,
                media_id=item.media_id,
                source=item.source,
                media_type=item.media_type,
            ).exists()
        )

        added = _sync_items(
            self.collection,
            [
                {
                    "media_id": item.media_id,
                    "source": item.source,
                    "media_type": item.media_type,
                    "title": item.title,
                    "image": item.image,
                }
            ],
        )

        self.assertEqual(added, 0)
        self.assertFalse(
            CollectionItem.objects.filter(collection=self.collection, item=item).exists()
        )

    def test_manually_readding_source_item_clears_exclusion(self):
        self.collection.source = "tmdb_collection"
        self.collection.source_id = "collection-1"
        self.collection.save(update_fields=["source", "source_id"])
        item = Item.objects.create(
            media_id="1",
            source=Sources.TMDB.value,
            media_type=MediaTypes.MOVIE.value,
            title="Movie 1",
            image="http://example.com/image.jpg",
        )
        CollectionItemExclusion.objects.create(
            collection=self.collection,
            media_id=item.media_id,
            source=item.source,
            media_type=item.media_type,
        )

        response = self.client.post(
            reverse("collection_item_toggle"),
            {
                "collection_id": self.collection.id,
                "source": item.source,
                "media_type": item.media_type,
                "media_id": item.media_id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            CollectionItem.objects.filter(collection=self.collection, item=item).exists()
        )
        self.assertFalse(
            CollectionItemExclusion.objects.filter(
                collection=self.collection,
                media_id=item.media_id,
                source=item.source,
                media_type=item.media_type,
            ).exists()
        )
