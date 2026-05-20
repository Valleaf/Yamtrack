from django.db import migrations


class Migration(migrations.Migration):
    """Merge the two 0063 migrations: add_media_country and item_country."""

    dependencies = [
        ("app", "0063_add_media_country"),
        ("app", "0063_item_country"),
    ]

    operations = []
