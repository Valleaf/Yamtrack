from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("media_collections", "0005_alter_collection_source_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="collectionitem",
            name="series_position",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
