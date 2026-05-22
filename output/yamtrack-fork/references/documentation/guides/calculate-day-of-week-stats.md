# How To: Calculate Day Of Week Stats

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the calculate_day_of_week_stats function.

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

### Step 1: 'Test the calculate_day_of_week_stats function.'

```python
'Test the calculate_day_of_week_stats function.'
```

### Step 2: Assign date_counts = value

```python
date_counts = {datetime.date(2025, 1, 1): 2, datetime.date(2025, 1, 2): 1, datetime.date(2025, 1, 3): 3, datetime.date(2025, 1, 4): 0, datetime.date(2025, 1, 5): 5, datetime.date(2025, 1, 6): 2, datetime.date(2025, 1, 7): 1, datetime.date(2025, 1, 8): 4, datetime.date(2025, 1, 9): 0, datetime.date(2025, 1, 10): 0, datetime.date(2025, 1, 12): 5, datetime.date(2025, 1, 19): 3}
```

### Step 3: Assign start_date = datetime.date(...)

```python
start_date = datetime.date(2025, 1, 1)
```

### Step 4: Assign unknown = statistics.calculate_day_of_week_stats(...)

```python
most_active_day, percentage = statistics.calculate_day_of_week_stats(date_counts, start_date)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(most_active_day, 'Sunday')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(percentage, 33)
```

### Step 7: Assign empty_counts = value

```python
empty_counts = {}
```

### Step 8: Assign unknown = statistics.calculate_day_of_week_stats(...)

```python
most_active_day, percentage = statistics.calculate_day_of_week_stats(empty_counts, start_date)
```

### Step 9: Call self.assertIsNone()

```python
self.assertIsNone(most_active_day)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(percentage, 0)
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
'Test the calculate_day_of_week_stats function.'
date_counts = {datetime.date(2025, 1, 1): 2, datetime.date(2025, 1, 2): 1, datetime.date(2025, 1, 3): 3, datetime.date(2025, 1, 4): 0, datetime.date(2025, 1, 5): 5, datetime.date(2025, 1, 6): 2, datetime.date(2025, 1, 7): 1, datetime.date(2025, 1, 8): 4, datetime.date(2025, 1, 9): 0, datetime.date(2025, 1, 10): 0, datetime.date(2025, 1, 12): 5, datetime.date(2025, 1, 19): 3}
start_date = datetime.date(2025, 1, 1)
most_active_day, percentage = statistics.calculate_day_of_week_stats(date_counts, start_date)
self.assertEqual(most_active_day, 'Sunday')
self.assertEqual(percentage, 33)
empty_counts = {}
most_active_day, percentage = statistics.calculate_day_of_week_stats(empty_counts, start_date)
self.assertIsNone(most_active_day)
self.assertEqual(percentage, 0)
```

## Next Steps


---

*Source: test_statistics.py:919 | Complexity: Advanced | Last updated: 2026-05-22*