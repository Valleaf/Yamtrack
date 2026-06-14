import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0068_add_bnf_source"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExternalList",
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
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "media_type",
                    models.CharField(
                        choices=[
                            ("tv", "TV Show"),
                            ("season", "TV Season"),
                            ("episode", "Episode"),
                            ("movie", "Movie"),
                            ("anime", "Anime"),
                            ("manga", "Manga"),
                            ("game", "Game"),
                            ("book", "Book"),
                            ("comic", "Comic"),
                            ("boardgame", "Boardgame"),
                            ("music", "Music"),
                        ],
                        max_length=10,
                    ),
                ),
                ("tmdb_list_id", models.CharField(max_length=50)),
                ("item_count", models.PositiveIntegerField(default=0)),
                ("last_synced", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="ExternalListItem",
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
                ("media_id", models.CharField(max_length=50)),
                ("rank", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "external_list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entries",
                        to="app.externallist",
                    ),
                ),
            ],
            options={
                "ordering": ["rank", "media_id"],
            },
        ),
        migrations.AddConstraint(
            model_name="externallistitem",
            constraint=models.UniqueConstraint(
                fields=["external_list", "media_id"],
                name="app_externallistitem_unique_list_media",
            ),
        ),
    ]
