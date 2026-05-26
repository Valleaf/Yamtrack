"""Add country field to store media production country."""
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration to add country field to Media model."""

    dependencies = [
        ('app', '0062_add_music_model'),
    ]

    operations = [
        # Add country field to all concrete Media subclasses
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
            model_name='season',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='manga',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='movie',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='game',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='book',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='comic',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='boardgame',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        # Add country field to all historical models
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
            model_name='historicalseason',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='historicalmanga',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='historicalmovie',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='historicalgame',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='historicalbook',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='historicalcomic',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
        migrations.AddField(
            model_name='historicalboardgame',
            name='country',
            field=models.CharField(
                max_length=100,
                null=True,
                blank=True,
                help_text='Country of origin/production',
            ),
        ),
    ]
