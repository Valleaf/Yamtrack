from django.db import migrations, models


class Migration(migrations.Migration):
    """Update check constraints to allow music media type and musicbrainz/senscritique sources."""

    dependencies = [
        ("app", "0064_merge_country_migrations"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="item",
            name="app_item_media_type_valid",
        ),
        migrations.AddConstraint(
            model_name="item",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    media_type__in=[
                        "tv",
                        "season",
                        "episode",
                        "movie",
                        "anime",
                        "manga",
                        "game",
                        "book",
                        "comic",
                        "boardgame",
                        "music",
                    ]
                ),
                name="app_item_media_type_valid",
            ),
        ),
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
                    ]
                ),
                name="app_item_source_valid",
            ),
        ),
    ]
