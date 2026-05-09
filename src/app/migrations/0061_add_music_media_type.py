"""
Migration: Add 'music' media type to Item.media_type choices.

Run after: app.0060_fix_reopened_completed_tv_seasons
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0060_fix_reopened_completed_tv_seasons"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="media_type",
            field=models.CharField(
                choices=[
                    ("movie", "Movie"),
                    ("tv", "TV"),
                    ("season", "Season"),
                    ("episode", "Episode"),
                    ("anime", "Anime"),
                    ("manga", "Manga"),
                    ("game", "Game"),
                    ("book", "Book"),
                    ("comic", "Comic"),
                    ("boardgame", "Board Game"),
                    ("music", "Music"),       # ← NEW
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="historicalitem",
            name="media_type",
            field=models.CharField(
                choices=[
                    ("movie", "Movie"),
                    ("tv", "TV"),
                    ("season", "Season"),
                    ("episode", "Episode"),
                    ("anime", "Anime"),
                    ("manga", "Manga"),
                    ("game", "Game"),
                    ("book", "Book"),
                    ("comic", "Comic"),
                    ("boardgame", "Board Game"),
                    ("music", "Music"),       # ← NEW
                ],
                max_length=20,
            ),
        ),
    ]
