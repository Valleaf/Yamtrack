# How To: Get Media List With Prefetch Related

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the get_media_list method with prefetch_related for TV and Season.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `pathlib`
- `unittest.mock`
- `django.contrib.auth`
- `django.db.models`
- `django.test`
- `django.utils`
- `app.models`
- `events.models`
- `users.models`

**Setup Required:**
```python
'Set up test data for MediaManager tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_numbers = season_numbers or [1]
        return {f'season/{season_number}': {'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)], 'image': 'http://example.com/image.jpg'} for season_number in season_numbers}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)]}
    max_progress_by_type = {MediaTypes.MOVIE.value: 1, MediaTypes.ANIME.value: 24, MediaTypes.MANGA.value: 300, MediaTypes.GAME.value: 240, MediaTypes.BOOK.value: 500, MediaTypes.BOARDGAME.value: 1}
    return {'max_progress': max_progress_by_type.get(media_type)}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
for media_type in MediaTypes.values:
    setattr(self.user, f'{media_type.lower()}_enabled', True)
self.user.save()
self.movie_item = Item.objects.create(media_id='550', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Fight Club', image='http://example.com/fightclub.jpg')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/bebop.jpg')
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.book_item = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='1984', image='http://example.com/1984.jpg')
self.manga_item = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='http://example.com/berserk.jpg')
self.movie = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, score=9)
self.anime = Anime.objects.create(item=self.anime_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=13)
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, score=7, progress=120)
self.book = Book.objects.create(item=self.book_item, user=self.user, status=Status.PLANNING.value, score=0)
self.manga = Manga.objects.create(item=self.manga_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=100)
self.season1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, status=Status.IN_PROGRESS.value, score=8)
self.tv = TV.objects.get(user=self.user)
for i in range(1, 5):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Friends S1E{i}', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    watched_episodes = 3
    if i <= watched_episodes:
        Episode.objects.create(item=episode_item, related_season=self.season1, end_date=datetime(2023, 6, i, 0, 0, tzinfo=UTC))
for i in range(4, 7):
    Event.objects.create(item=self.anime_item, content_number=i + 13, datetime=timezone.now() + timedelta(days=i), notification_sent=False)
```

## Step-by-Step Guide

### Step 1: 'Test the get_media_list method with prefetch_related for TV and Season.'

```python
'Test the get_media_list method with prefetch_related for TV and Season.'
```

### Step 2: Assign manager = MediaManager(...)

```python
manager = MediaManager()
```

### Step 3: Assign tv_list = manager.get_media_list(...)

```python
tv_list = manager.get_media_list(user=self.user, media_type=MediaTypes.TV.value, status_filter=MediaStatusChoices.ALL, sort_filter='score')
```

### Step 4: Assign tv_list = list(...)

```python
tv_list = list(tv_list)
```

### Step 5: Assign season_list = manager.get_media_list(...)

```python
season_list = manager.get_media_list(user=self.user, media_type=MediaTypes.SEASON.value, status_filter=MediaStatusChoices.ALL, sort_filter='score')
```

### Step 6: Assign season_list = list(...)

```python
season_list = list(season_list)
```

### Step 7: Assign seasons = list(...)

```python
seasons = list(tv.seasons.all())
```

### Step 8: Call list()

```python
list(season.episodes.all())
```

### Step 9: Call list()

```python
list(season.episodes.all())
```

### Step 10: Assign seasons = list(...)

```python
seasons = list(tv.seasons.all())
```

### Step 11: Call list()

```python
list(season.episodes.all())
```

### Step 12: Call list()

```python
list(season.episodes.all())
```


## Complete Example

```python
# Setup
'Set up test data for MediaManager tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_numbers = season_numbers or [1]
        return {f'season/{season_number}': {'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)], 'image': 'http://example.com/image.jpg'} for season_number in season_numbers}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)]}
    max_progress_by_type = {MediaTypes.MOVIE.value: 1, MediaTypes.ANIME.value: 24, MediaTypes.MANGA.value: 300, MediaTypes.GAME.value: 240, MediaTypes.BOOK.value: 500, MediaTypes.BOARDGAME.value: 1}
    return {'max_progress': max_progress_by_type.get(media_type)}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
for media_type in MediaTypes.values:
    setattr(self.user, f'{media_type.lower()}_enabled', True)
self.user.save()
self.movie_item = Item.objects.create(media_id='550', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Fight Club', image='http://example.com/fightclub.jpg')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/bebop.jpg')
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.book_item = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='1984', image='http://example.com/1984.jpg')
self.manga_item = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='http://example.com/berserk.jpg')
self.movie = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, score=9)
self.anime = Anime.objects.create(item=self.anime_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=13)
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, score=7, progress=120)
self.book = Book.objects.create(item=self.book_item, user=self.user, status=Status.PLANNING.value, score=0)
self.manga = Manga.objects.create(item=self.manga_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=100)
self.season1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, status=Status.IN_PROGRESS.value, score=8)
self.tv = TV.objects.get(user=self.user)
for i in range(1, 5):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Friends S1E{i}', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    watched_episodes = 3
    if i <= watched_episodes:
        Episode.objects.create(item=episode_item, related_season=self.season1, end_date=datetime(2023, 6, i, 0, 0, tzinfo=UTC))
for i in range(4, 7):
    Event.objects.create(item=self.anime_item, content_number=i + 13, datetime=timezone.now() + timedelta(days=i), notification_sent=False)

# Workflow
'Test the get_media_list method with prefetch_related for TV and Season.'
manager = MediaManager()
tv_list = manager.get_media_list(user=self.user, media_type=MediaTypes.TV.value, status_filter=MediaStatusChoices.ALL, sort_filter='score')
tv_list = list(tv_list)
for tv in tv_list:
    seasons = list(tv.seasons.all())
    for season in seasons:
        list(season.episodes.all())
with self.assertNumQueries(0):
    for tv in tv_list:
        seasons = list(tv.seasons.all())
        for season in seasons:
            list(season.episodes.all())
season_list = manager.get_media_list(user=self.user, media_type=MediaTypes.SEASON.value, status_filter=MediaStatusChoices.ALL, sort_filter='score')
season_list = list(season_list)
for season in season_list:
    list(season.episodes.all())
with self.assertNumQueries(0):
    for season in season_list:
        list(season.episodes.all())
```

## Next Steps


---

*Source: test_media_manager.py:328 | Complexity: Advanced | Last updated: 2026-05-22*