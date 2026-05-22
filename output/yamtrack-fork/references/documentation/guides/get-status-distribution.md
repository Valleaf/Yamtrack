# How To: Get Status Distribution

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the get_status_distribution function.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `app`
- `app.models`

**Setup Required:**
```python
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.episode2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=2)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.anime_item = Item.objects.create(media_id='437', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value, score=8.0)
self.episode1 = Episode.objects.create(item=self.episode1_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC))
self.episode2 = Episode.objects.create(item=self.episode2_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value, score=7.5, start_date=datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC))
self.anime = Anime.objects.create(user=self.user, item=self.anime_item, status=Status.COMPLETED.value, score=None, start_date=datetime.datetime(2025, 3, 1, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 31, 0, 0, tzinfo=datetime.UTC))
```

## Step-by-Step Guide

### Step 1: 'Test the get_status_distribution function.'

```python
'Test the get_status_distribution function.'
```

### Step 2: Assign user_media = value

```python
user_media = {MediaTypes.TV.value: TV.objects.filter(user=self.user), MediaTypes.MOVIE.value: Movie.objects.filter(user=self.user), MediaTypes.ANIME.value: Anime.objects.filter(user=self.user)}
```

### Step 3: Assign status_distribution = statistics.get_status_distribution(...)

```python
status_distribution = statistics.get_status_distribution(user_media)
```

### Step 4: Call self.assertIn()

```python
self.assertIn('labels', status_distribution)
```

### Step 5: Call self.assertIn()

```python
self.assertIn('datasets', status_distribution)
```

### Step 6: Call self.assertIn()

```python
self.assertIn('total_completed', status_distribution)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(status_distribution['labels']), 3)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(status_distribution['datasets']), len(Status.values))
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(status_distribution['total_completed'], 1)
```

### Step 10: Assign completed_dataset = next(...)

```python
completed_dataset = next((d for d in status_distribution['datasets'] if d['label'] == Status.COMPLETED.value))
```

### Step 11: Assign in_progress_dataset = next(...)

```python
in_progress_dataset = next((d for d in status_distribution['datasets'] if d['label'] == Status.IN_PROGRESS.value))
```

### Step 12: Assign planning_dataset = next(...)

```python
planning_dataset = next((d for d in status_distribution['datasets'] if d['label'] == Status.PLANNING.value))
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(completed_dataset['total'], 1)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(in_progress_dataset['total'], 1)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(planning_dataset['total'], 1)
```


## Complete Example

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.episode2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=2)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.anime_item = Item.objects.create(media_id='437', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value, score=8.0)
self.episode1 = Episode.objects.create(item=self.episode1_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC))
self.episode2 = Episode.objects.create(item=self.episode2_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value, score=7.5, start_date=datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC))
self.anime = Anime.objects.create(user=self.user, item=self.anime_item, status=Status.COMPLETED.value, score=None, start_date=datetime.datetime(2025, 3, 1, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 31, 0, 0, tzinfo=datetime.UTC))

# Workflow
'Test the get_status_distribution function.'
user_media = {MediaTypes.TV.value: TV.objects.filter(user=self.user), MediaTypes.MOVIE.value: Movie.objects.filter(user=self.user), MediaTypes.ANIME.value: Anime.objects.filter(user=self.user)}
status_distribution = statistics.get_status_distribution(user_media)
self.assertIn('labels', status_distribution)
self.assertIn('datasets', status_distribution)
self.assertIn('total_completed', status_distribution)
self.assertEqual(len(status_distribution['labels']), 3)
self.assertEqual(len(status_distribution['datasets']), len(Status.values))
self.assertEqual(status_distribution['total_completed'], 1)
completed_dataset = next((d for d in status_distribution['datasets'] if d['label'] == Status.COMPLETED.value))
in_progress_dataset = next((d for d in status_distribution['datasets'] if d['label'] == Status.IN_PROGRESS.value))
planning_dataset = next((d for d in status_distribution['datasets'] if d['label'] == Status.PLANNING.value))
self.assertEqual(completed_dataset['total'], 1)
self.assertEqual(in_progress_dataset['total'], 1)
self.assertEqual(planning_dataset['total'], 1)
```

## Next Steps


---

*Source: test_statistics.py:573 | Complexity: Advanced | Last updated: 2026-05-22*