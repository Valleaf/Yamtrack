# Generated manually on 2026-06-22 -- adds PersistentCacheEntry,
# the durable backing store for app.cache_backends.PersistentRedisCache.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0072_alter_music_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersistentCacheEntry',
            fields=[
                ('key', models.CharField(max_length=300, primary_key=True, serialize=False)),
                ('value', models.BinaryField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
