from django.db import migrations, models


class Migration(migrations.Migration):
    """Add country field to Item as well (merge of two 0063 migrations)."""

    dependencies = [
        ("app", "0063_add_media_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="country",
            field=models.CharField(blank=True, default="", max_length=2),
        ),
    ]
