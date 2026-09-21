from django.test import SimpleTestCase

from app.external_lists_data import LISTS
from app.curated_lists import list_from_award


class CuratedListsTests(SimpleTestCase):
    """Keep static curated-list fixtures safe for statistics rendering."""

    def test_list_slugs_and_ranks_are_unique(self):
        slugs = [curated_list["slug"] for curated_list in LISTS]
        self.assertEqual(len(slugs), len(set(slugs)))

        for curated_list in LISTS:
            ranks = [entry["rank"] for entry in curated_list["items"]]
            self.assertEqual(
                len(ranks),
                len(set(ranks)),
                curated_list["slug"],
            )

    def test_entries_have_the_declared_provider_id(self):
        for curated_list in LISTS:
            id_key = f"{curated_list['source']}_id"
            for entry in curated_list["items"]:
                self.assertTrue(entry.get(id_key), f"{curated_list['slug']}: {id_key}")

    def test_snapshots_have_provenance(self):
        for curated_list in LISTS:
            self.assertTrue(curated_list.get("source_url"), curated_list["slug"])
            self.assertRegex(curated_list["snapshot_date"], r"^20\d{2}-\d{2}-\d{2}$")
            self.assertEqual(curated_list["verification_status"], "verified_provider_ids")

    def test_award_helper_preserves_verified_order_and_ids(self):
        curated_list = list_from_award(
            "game_awards_goty",
            slug="test-game-awards",
            limit=2,
        )
        self.assertEqual(curated_list["media_type"], "game")
        self.assertEqual(curated_list["items"], [
            {"rank": 1, "igdb_id": "303811"},
            {"rank": 2, "igdb_id": "119171"},
        ])
