from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("collections", "0002_collection_source"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="source",
            field=models.CharField(default="manual", max_length=50),
        ),
        migrations.AlterField(
            model_name="collection",
            name="source_id",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
    ]
