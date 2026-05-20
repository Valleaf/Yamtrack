from django.db import migrations, models


class Migration(migrations.Migration):
    """Merge both 0063 migrations and add Item.country."""

    dependencies = [
        ("app", "0063_add_media_country"),
        ("app", "0063_item_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="country",
            field=models.CharField(blank=True, default="", max_length=2),
        ),
    ]
