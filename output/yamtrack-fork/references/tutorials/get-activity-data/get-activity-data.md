# How To: Get Activity Data

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test the get_activity_data function.

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

### Step 1: 'Test the get_activity_data function.'

```python
'Test the get_activity_data function.'
```

### Step 2: Assign start_date = datetime.datetime(...)

```python
start_date = datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC)
```

### Step 3: Assign end_date = datetime.datetime(...)

```python
end_date = datetime.datetime(2025, 3, 31, 0, 0, tzinfo=datetime.UTC)
```

### Step 4: Assign mock_get_filtered_data.return_value = value

```python
mock_get_filtered_data.return_value = [{'date': datetime.date(2025, 1, 1), 'count': 2}, {'date': datetime.date(2025, 1, 2), 'count': 1}, {'date': datetime.date(2025, 1, 3), 'count': 3}, {'date': datetime.date(2025, 1, 4), 'count': 0}, {'date': datetime.date(2025, 1, 5), 'count': 5}, {'date': datetime.date(2025, 1, 6), 'count': 2}, {'date': datetime.date(2025, 1, 7), 'count': 1}, {'date': datetime.date(2025, 1, 8), 'count': 4}, {'date': datetime.date(2025, 1, 9), 'count': 0}, {'date': datetime.date(2025, 1, 10), 'count': 0}, {'date': datetime.date(2025, 3, 31), 'count': 3}]
```

### Step 5: Assign result = statistics.get_activity_data(...)

```python
result = statistics.get_activity_data(self.user, start_date, end_date)
```

### Step 6: Call self.assertIn()

```python
self.assertIn('calendar_weeks', result)
```

### Step 7: Call self.assertIn()

```python
self.assertIn('months', result)
```

### Step 8: Call self.assertIn()

```python
self.assertIn('stats', result)
```

### Step 9: Assign stats = value

```python
stats = result['stats']
```

### Step 10: Call self.assertIn()

```python
self.assertIn('most_active_day', stats)
```

### Step 11: Call self.assertIn()

```python
self.assertIn('most_active_day_percentage', stats)
```

### Step 12: Call self.assertIn()

```python
self.assertIn('current_streak', stats)
```

### Step 13: Call self.assertIn()

```python
self.assertIn('longest_streak', stats)
```

### Step 14: Assign calendar_weeks = value

```python
calendar_weeks = result['calendar_weeks']
```

### Step 15: Call self.assertIsInstance()

```python
self.assertIsInstance(calendar_weeks, list)
```

### Step 16: Assign first_week = value

```python
first_week = calendar_weeks[0]
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(len(first_week), 7)
```

### Step 18: Assign months = value

```python
months = result['months']
```

### Step 19: Call self.assertIsInstance()

```python
self.assertIsInstance(months, list)
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
'Test the get_activity_data function.'
start_date = datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC)
end_date = datetime.datetime(2025, 3, 31, 0, 0, tzinfo=datetime.UTC)
mock_get_filtered_data.return_value = [{'date': datetime.date(2025, 1, 1), 'count': 2}, {'date': datetime.date(2025, 1, 2), 'count': 1}, {'date': datetime.date(2025, 1, 3), 'count': 3}, {'date': datetime.date(2025, 1, 4), 'count': 0}, {'date': datetime.date(2025, 1, 5), 'count': 5}, {'date': datetime.date(2025, 1, 6), 'count': 2}, {'date': datetime.date(2025, 1, 7), 'count': 1}, {'date': datetime.date(2025, 1, 8), 'count': 4}, {'date': datetime.date(2025, 1, 9), 'count': 0}, {'date': datetime.date(2025, 1, 10), 'count': 0}, {'date': datetime.date(2025, 3, 31), 'count': 3}]
result = statistics.get_activity_data(self.user, start_date, end_date)
self.assertIn('calendar_weeks', result)
self.assertIn('months', result)
self.assertIn('stats', result)
stats = result['stats']
self.assertIn('most_active_day', stats)
self.assertIn('most_active_day_percentage', stats)
self.assertIn('current_streak', stats)
self.assertIn('longest_streak', stats)
calendar_weeks = result['calendar_weeks']
self.assertIsInstance(calendar_weeks, list)
first_week = calendar_weeks[0]
self.assertEqual(len(first_week), 7)
months = result['months']
self.assertIsInstance(months, list)
```

## Next Steps


---

*Source: test_statistics.py:825 | Complexity: Advanced | Last updated: 2026-05-22*