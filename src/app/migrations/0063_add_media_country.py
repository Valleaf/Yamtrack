"""Add country field to store media production country."""
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration to add country field to Media model."""

    dependencies = [
        ('app', '0062_add_music_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='basicmedia',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='tv',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='historicalanime',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='historicalbasicmedia',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='historicaltv',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='historicalmusic',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
    ]
