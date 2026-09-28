from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0060_merge_home_sections_and_collection_preferences"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="lastfm_username",
            field=models.CharField(
                blank=True,
                help_text="Last.fm username used for personal music statistics",
                max_length=100,
            ),
        ),
    ]
