from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("media_collections", "0008_collection_parent_collection")]

    operations = [
        migrations.AddField(
            model_name="collection",
            name="group_regional_variants",
            field=models.BooleanField(
                default=False,
                help_text="Group clearly-labelled regional or platform editions in the collection view.",
            ),
        ),
    ]
