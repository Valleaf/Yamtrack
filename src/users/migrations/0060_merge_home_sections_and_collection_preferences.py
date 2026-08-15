from django.db import migrations


class Migration(migrations.Migration):
    """Join the home-section branch with the later preference migrations."""

    dependencies = [
        ("users", "0051_home_section_preferences"),
        ("users", "0059_user_collection_columns_and_more"),
    ]

    operations = []
