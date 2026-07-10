"""Drop ExternalList/ExternalListItem.

These were scaffolded for a TMDB-list-sync design that was never built (no
sync task/command ever populated them). Curated lists are now driven by the
static app/external_lists_data.py fixture, computed live exactly like
app/awards_data.py -- no DB table needed.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0073_persistentcacheentry"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="externallistitem",
            name="app_externallistitem_unique_list_media",
        ),
        migrations.DeleteModel(
            name="ExternalListItem",
        ),
        migrations.DeleteModel(
            name="ExternalList",
        ),
    ]
