from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration to add music media type user preferences."""

    dependencies = [
        ("users", "0052_alter_user_date_format"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="music_enabled",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="user",
            name="music_layout",
            field=models.CharField(
                choices=[("grid", "Grid"), ("table", "Table")],
                default="grid",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="music_sort",
            field=models.CharField(
                choices=[
                    ("score", "Rating"),
                    ("title", "Title"),
                    ("progress", "Progress"),
                    ("start_date", "Start Date"),
                    ("end_date", "End Date"),
                ],
                default="score",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="music_status",
            field=models.CharField(
                choices=[
                    ("All", "All"),
                    ("Completed", "Completed"),
                    ("In progress", "In Progress"),
                    ("Planning", "Planning"),
                    ("Paused", "Paused"),
                    ("Dropped", "Dropped"),
                ],
                default="All",
                max_length=20,
            ),
        ),
    ]
