from django.db import migrations


def create_default_users(apps, schema_editor):
    """Create Val and Imane if they don't already exist."""
    User = apps.get_model("users", "User")

    for username in ["Val", "Imane"]:
        if not User.objects.filter(username=username).exists():
            user = User(username=username)
            user.set_unusable_password()
            user.save()


class Migration(migrations.Migration):
    """Create the two default local users."""

    dependencies = [
        ("users", "0054_add_music_to_search_type"),
    ]

    operations = [
        migrations.RunPython(create_default_users, migrations.RunPython.noop),
    ]
