from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("media_collections", "0003_collection_source_widened"),
    ]

    operations = [
        migrations.CreateModel(
            name="CollectionItemExclusion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("media_id", models.CharField(max_length=255)),
                ("source", models.CharField(max_length=50)),
                (
                    "media_type",
                    models.CharField(
                        choices=[
                            ("movie", "Movie"),
                            ("tv", "TV Show"),
                            ("season", "Season"),
                            ("episode", "Episode"),
                            ("book", "Book"),
                            ("comic", "Comic"),
                            ("manga", "Manga"),
                            ("anime", "Anime"),
                            ("game", "Game"),
                            ("boardgame", "Board Game"),
                            ("music", "Music"),
                        ],
                        max_length=10,
                    ),
                ),
                ("date_removed", models.DateTimeField(auto_now_add=True)),
                (
                    "collection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="media_collections.collection",
                    ),
                ),
            ],
            options={
                "ordering": ["date_removed"],
            },
        ),
        migrations.AddConstraint(
            model_name="collectionitemexclusion",
            constraint=models.UniqueConstraint(
                fields=("collection", "media_id", "source", "media_type"),
                name="collections_exclusion_unique_source_item",
            ),
        ),
    ]
