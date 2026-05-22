from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("media_collections", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="collection",
            name="source",
            field=models.CharField(blank=True, default="manual", max_length=50),
        ),
        migrations.AddField(
            model_name="collection",
            name="source_id",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
    ]
