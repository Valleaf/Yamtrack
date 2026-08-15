from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("users", "0050_user_watch_provider_region")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="show_home_in_progress",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="user",
            name="show_home_planning",
            field=models.BooleanField(default=True),
        ),
    ]
