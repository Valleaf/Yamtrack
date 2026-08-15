from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("media_collections", "0007_collection_poster_url")]

    operations = [
        migrations.AddField(
            model_name="collection",
            name="parent_collection",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                related_name="subcollections",
                to="media_collections.collection",
            ),
        ),
    ]
