# Generated manually for the music release discovery feature.

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0074_drop_external_list_models"),
        ("events", "0014_delete_empty_content_number_comic_events"),
    ]

    operations = [
        migrations.CreateModel(
            name="MusicReleaseDiscovery",
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
                ("artist_names", models.TextField(blank=True, default="")),
                ("release_date", models.DateTimeField()),
                ("discovered_at", models.DateTimeField(auto_now=True)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.item",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="music_release_discoveries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("user", "item"),
                        name="unique_music_release_discovery_user_item",
                    ),
                ],
                "indexes": [
                    models.Index(
                        fields=["user", "release_date"],
                        name="music_discovery_user_date_idx",
                    ),
                ],
            },
        ),
    ]
