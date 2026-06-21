from django.db import migrations, models


class Migration(migrations.Migration):
    """Add Item.release_year, denormalized from provider metadata.

    Lets statistics read release year straight from the DB instead of the
    metadata Redis cache, so stats stay accurate regardless of cache TTL.
    """

    dependencies = [
        ("app", "0070_seed_external_lists"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="release_year",
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                help_text=(
                    "Release year, denormalized from provider metadata at "
                    "save/sync time so stats queries never depend on the "
                    "metadata cache being warm."
                ),
            ),
        ),
    ]
