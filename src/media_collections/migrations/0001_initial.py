import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("app", "0064_merge_country_migrations"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Collection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, default="")),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ("collaborators", models.ManyToManyField(blank=True, related_name="collaborated_collections", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="CollectionItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("notes", models.CharField(blank=True, default="", max_length=255)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("collection", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="media_collections.collection")),
                ("item", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="app.item")),
            ],
            options={"ordering": ["date_added"]},
        ),
        migrations.AddField(
            model_name="collection",
            name="items",
            field=models.ManyToManyField(blank=True, related_name="media_collections", through="media_collections.CollectionItem", to="app.item"),
        ),
        migrations.AddConstraint(
            model_name="collectionitem",
            constraint=models.UniqueConstraint(
                fields=["item", "collection"],
                name="collections_collectionitem_unique_item_collection",
            ),
        ),
    ]
