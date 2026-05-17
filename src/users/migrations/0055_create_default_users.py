from django.db import migrations


def create_default_users(apps, schema_editor):
    """Create Val and Imane if they don't already exist."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    for username in ["Val", "Imane"]:
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=username.lower() + "123")


class Migration(migrations.Migration):
    """Create the two default local users."""

    dependencies = [
        ("users", "0054_add_music_to_search_type"),
    ]

    operations = [
        migrations.RunPython(create_default_users, migrations.RunPython.noop),
    ]
