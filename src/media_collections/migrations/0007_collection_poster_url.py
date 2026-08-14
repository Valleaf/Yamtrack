from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("media_collections", "0006_collectionitem_series_position"),
    ]

    operations = [
        migrations.AddField(
            model_name="collection",
            name="poster_url",
            field=models.URLField(blank=True, default=""),
        ),
    ]
