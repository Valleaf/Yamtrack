from django.db import migrations, models


class Migration(migrations.Migration):
    """Add music to last_search_type choices."""

    dependencies = [
        ("users", "0053_add_music_user_prefs"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="last_search_type",
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
                default="tv",
                max_length=10,
            ),
        ),
    ]
