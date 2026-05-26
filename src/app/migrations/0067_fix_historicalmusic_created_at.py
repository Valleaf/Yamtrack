from django.db import migrations, models


class Migration(migrations.Migration):
    """Fix historicalmusic.created_at to allow NULL, as simple_history expects."""

    dependencies = [
        ("app", "0066_remove_music_repeats"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalmusic",
            name="created_at",
            field=models.DateTimeField(blank=True, null=True, editable=False),
        ),
    ]
