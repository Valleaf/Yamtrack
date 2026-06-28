# Generated manually to switch the default media list sort from Rating to End Date

from django.db import migrations, models

SORT_FIELDS = [
    "tv_sort",
    "season_sort",
    "movie_sort",
    "anime_sort",
    "manga_sort",
    "game_sort",
    "book_sort",
    "comic_sort",
    "boardgame_sort",
    "music_sort",
]


def set_existing_users_to_end_date(apps, schema_editor):
    """Move users still on the old 'score' default over to 'end_date'.

    Users who already customized a given sort field away from the old
    default are left untouched.
    """
    User = apps.get_model("users", "User")
    for field in SORT_FIELDS:
        User.objects.filter(**{field: "score"}).update(**{field: "end_date"})


class Migration(migrations.Migration):
    """Default media list sort is now End Date instead of Rating."""

    dependencies = [
        ("users", "0056_remove_user_last_search_type_valid_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="tv_sort",
            field=models.CharField(choices=[('score', 'Rating'), ('title', 'Title'), ('progress', 'Progress'), ('start_date', 'Start Date'), ('end_date', 'End Date')], default='end_date', max_length=20),
        ),
        migrations.AlterField(
            model_name="user",
            name="season_sort",
            field=models.CharField(choices=[('score', 'Rating'), ('title', 'Title'), ('progress', 'Progress'), ('start_date', 'Start Date'), ('end_date', 'End Date')], default='end_date', max_length=20),
        ),
        migrations.AlterField(
            model_name="user",
            name="movie_sort",
            field=models.CharField(choices=[('score', 'Rating'), ('title', 'Title'), ('progress', 'Progress'), ('start_date', 'Start Date'), ('end_date', 'End Date')], default='end_date', max_length=20),
        ),
        migrations.AlterField(
            model_name="user",
            name="anime_sort",
            field=models.CharField(choices=[('score', 'Rating'), ('title', 'Title'), ('progress', 'Progress'), ('start_date', 'Start Date'), ('end_date', 'End Date')], default='end_date', max_length=20),
        ),
        migrations.AlterField(
            model_name="user",
            name="manga_sort",
            field=models.CharField(choices=[('score', 'Rating'), ('title', 'Title'), ('progress', 'Progress'), ('start_date', 'Start Date'), ('end_date', 'End Date')], default='end_date', max_length=20),
        ),
        migrations.AlterField(
            model_name="user",
            name="game_sort",
            field=models.CharField(choices=[('score', 'Rating'), ('title', 'Title'), ('progress', 'Progress'), ('start_date', 'Start Date'), ('end_date', 'End Date')], default='end_date', max_length=20),
        ),
        migrations.AlterField(
            model_name="user",
            name="book_sort",
            field=models.CharField(choices=[('score', 'Rating'), ('title', 'Title'), ('progress', 'Progress'), ('start_date', 'Start Date'), ('end_date', 'End Date')], default='end_date', max_length=20),
        ),
        migrations.AlterField(
            model_name="user",
            name="comic_sort",
            field=models.CharField(choices=[('score', 'Rating'), ('title', 'Title'), ('progress', 'Progress'), ('start_date', 'Start Date'), ('end_date', 'End Date')], default='end_date', max_length=20),
        ),
        migrations.AlterField(
            model_name="user",
            name="boardgame_sort",
            field=models.CharField(choices=[('score', 'Rating'), ('title', 'Title'), ('progress', 'Progress'), ('start_date', 'Start Date'), ('end_date', 'End Date')], default='end_date', max_length=20),
        ),
        migrations.AlterField(
            model_name="user",
            name="music_sort",
            field=models.CharField(choices=[('score', 'Rating'), ('title', 'Title'), ('progress', 'Progress'), ('start_date', 'Start Date'), ('end_date', 'End Date')], default='end_date', max_length=20),
        ),
        migrations.RunPython(set_existing_users_to_end_date, migrations.RunPython.noop),
    ]
