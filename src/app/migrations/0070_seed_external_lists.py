"""Seed initial external lists.

TMDB list IDs can be found at https://www.themoviedb.org/list/<id>
Add more lists via Django admin → App → External lists, or extend
INITIAL_LISTS below and create a new data migration.

Known stable IDs (verified community lists):
  28          IMDb Top 250 Movies
  11          Top 250 Rated Movies (TMDB staff picks)

"""
from django.db import migrations


INITIAL_LISTS = [
    {
        "slug": "imdb_top250",
        "name": "IMDb Top 250",
        "media_type": "movie",
        "tmdb_list_id": "28",
    },
]


def seed_lists(apps, schema_editor):
    ExternalList = apps.get_model("app", "ExternalList")
    for data in INITIAL_LISTS:
        ExternalList.objects.get_or_create(slug=data["slug"], defaults=data)


def remove_lists(apps, schema_editor):
    ExternalList = apps.get_model("app", "ExternalList")
    for data in INITIAL_LISTS:
        ExternalList.objects.filter(slug=data["slug"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0069_external_lists"),
    ]

    operations = [
        migrations.RunPython(seed_lists, remove_lists),
    ]
