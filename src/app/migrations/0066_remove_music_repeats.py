from django.db import migrations


class Migration(migrations.Migration):
    """Drop the spurious 'repeats' column from app_music and app_historicalmusic."""

    dependencies = [
        ("app", "0065_fix_music_media_type_constraint"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="music",
            name="repeats",
        ),
        migrations.RemoveField(
            model_name="historicalmusic",
            name="repeats",
        ),
    ]
