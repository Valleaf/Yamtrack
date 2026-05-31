from django.db import migrations, models


class Migration(migrations.Migration):
    """Add BnF (Bibliothèque nationale de France) as a supported source."""

    dependencies = [
        ("app", "0067_fix_historicalmusic_created_at"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="item",
            name="app_item_source_valid",
        ),
        migrations.AddConstraint(
            model_name="item",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    source__in=[
                        "tmdb",
                        "mal",
                        "mangaupdates",
                        "igdb",
                        "openlibrary",
                        "hardcover",
                        "comicvine",
                        "bgg",
                        "manual",
                        "senscritique",
                        "musicbrainz",
                        "bnf",
                    ]
                ),
                name="app_item_source_valid",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="source",
            field=models.CharField(
                choices=[
                    ("tmdb", "The Movie Database"),
                    ("mal", "MyAnimeList"),
                    ("mangaupdates", "MangaUpdates"),
                    ("igdb", "Internet Game Database"),
                    ("openlibrary", "Open Library"),
                    ("hardcover", "Hardcover"),
                    ("comicvine", "Comic Vine"),
                    ("bgg", "BoardGameGeek"),
                    ("manual", "Manual"),
                    ("senscritique", "SensCritique"),
                    ("musicbrainz", "MusicBrainz"),
                    ("bnf", "Bibliothèque nationale de France"),
                ],
                max_length=20,
            ),
        ),
    ]
