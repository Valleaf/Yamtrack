from django.contrib.auth import get_user_model
from django.test import TestCase

from app.awards_data import AWARDS
from app.external_lists_data import LISTS
from app.models import Item
from app.statistics import get_award_winners_detail, get_list_winners_detail


class CuratedDetailArtworkTests(TestCase):
    """Artwork in detail panels comes from local Item data without API calls."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="curated-artwork",
            password="password",
        )

    def test_award_entries_include_item_artwork(self):
        award = next(a for a in AWARDS if a["winners"])
        winner = next(w for w in award["winners"] if w.get(f"{award['source']}_id"))
        source = award["source"]
        media_type = award["media_type"]
        media_id = str(winner[f"{source}_id"])
        Item.objects.create(
            media_id=media_id,
            source=source,
            media_type=media_type,
            title="Artwork Winner",
            image="https://example.com/award.jpg",
        )

        detail = get_award_winners_detail(self.user, award["slug"])

        entry = next(e for e in detail["entries"] if e["media_id"] == media_id)
        self.assertEqual(entry["image"], "https://example.com/award.jpg")

    def test_list_entries_include_item_artwork(self):
        curated_list = next(lst for lst in LISTS if lst["items"])
        entry_config = next(
            entry
            for entry in curated_list["items"]
            if entry.get(f"{curated_list['source']}_id")
        )
        source = curated_list["source"]
        media_type = curated_list["media_type"]
        media_id = str(entry_config[f"{source}_id"])
        Item.objects.create(
            media_id=media_id,
            source=source,
            media_type=media_type,
            title="Artwork List Entry",
            image="https://example.com/list.jpg",
        )

        detail = get_list_winners_detail(self.user, curated_list["slug"])

        entry = next(e for e in detail["entries"] if e["media_id"] == media_id)
        self.assertEqual(entry["image"], "https://example.com/list.jpg")
