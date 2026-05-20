from django.db import migrations, models


class Migration(migrations.Migration):
    """Add country field to Item."""

    dependencies = [
        ("app", "0062_add_music_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="country",
            field=models.CharField(blank=True, default="", max_length=2),
        ),
    ]
