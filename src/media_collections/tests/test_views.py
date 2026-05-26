from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app.models import Item, MediaTypes, Sources
from media_collections.models import Collection, CollectionItem


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
