from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration to add music media type."""

    dependencies = [
        ("app", "0060_fix_reopened_completed_tv_seasons"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="media_type",
            field=models.CharField(
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
                default="movie",
                max_length=10,
            ),
        ),
    ]
