# How To: Get Extended Statistics

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test extended report-style statistics.

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

### Step 1: 'Test extended report-style statistics.'

```python
'Test extended report-style statistics.'
```

### Step 2: Call TV.objects.filter.update()

```python
TV.objects.filter(user=self.user).update(score=8.5)
```

### Step 3: Assign user_media = value

```python
user_media = {MediaTypes.TV.value: TV.objects.filter(user=self.user), MediaTypes.MOVIE.value: Movie.objects.filter(user=self.user), MediaTypes.ANIME.value: Anime.objects.filter(user=self.user)}
```

### Step 4: Assign report = statistics.get_extended_statistics(...)

```python
report = statistics.get_extended_statistics(user_media)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(report['summary']['total_items'], 3)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(report['summary']['completed_items'], 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(report['summary']['completion_percentage'], 33)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(report['summary']['scored_items'], 2)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(report['summary']['unrated_items'], 1)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(report['summary']['median_score'], 8.0)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(report['summary']['highest_rated'].score, 8.5)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(report['summary']['lowest_rated'].score, 7.5)
```

### Step 13: Assign movie_row = next(...)

```python
movie_row = next((row for row in report['media_type_rows'] if row['media_type'] == MediaTypes.MOVIE.value))
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(movie_row['total'], 1)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(movie_row['scored'], 1)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(movie_row['average_score'], 7.5)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(movie_row['best_media'], self.movie)
```

### Step 18: Assign score_8 = next(...)

```python
score_8 = next((bucket for bucket in report['score_buckets'] if bucket['score'] == 8))
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(score_8['count'], 1)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(score_8['percentage'], 50)
```

### Step 21: Assign favorites = next(...)

```python
favorites = next((band for band in report['rating_bands'] if band['label'] == 'Favorites'))
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(favorites['count'], 1)
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(favorites['percentage'], 50)
```

### Step 24: Assign tmdb_row = next(...)

```python
tmdb_row = next((row for row in report['source_rows'] if row['source'] == Sources.TMDB.label))
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(tmdb_row['count'], 2)
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(tmdb_row['scored'], 2)
```

### Step 27: Call self.assertEqual()

```python
self.assertEqual(tmdb_row['average_score'], 8.0)
```

### Step 28: Assign year_2025 = next(...)

```python
year_2025 = next((row for row in report['year_rows'] if row['year'] == 2025))
```

### Step 29: Call self.assertEqual()

```python
self.assertEqual(year_2025['started'], 3)
```

### Step 30: Call self.assertEqual()

```python
self.assertEqual(year_2025['completed'], 3)
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
'Test extended report-style statistics.'
TV.objects.filter(user=self.user).update(score=8.5)
user_media = {MediaTypes.TV.value: TV.objects.filter(user=self.user), MediaTypes.MOVIE.value: Movie.objects.filter(user=self.user), MediaTypes.ANIME.value: Anime.objects.filter(user=self.user)}
report = statistics.get_extended_statistics(user_media)
self.assertEqual(report['summary']['total_items'], 3)
self.assertEqual(report['summary']['completed_items'], 1)
self.assertEqual(report['summary']['completion_percentage'], 33)
self.assertEqual(report['summary']['scored_items'], 2)
self.assertEqual(report['summary']['unrated_items'], 1)
self.assertEqual(report['summary']['median_score'], 8.0)
self.assertEqual(report['summary']['highest_rated'].score, 8.5)
self.assertEqual(report['summary']['lowest_rated'].score, 7.5)
movie_row = next((row for row in report['media_type_rows'] if row['media_type'] == MediaTypes.MOVIE.value))
self.assertEqual(movie_row['total'], 1)
self.assertEqual(movie_row['scored'], 1)
self.assertEqual(movie_row['average_score'], 7.5)
self.assertEqual(movie_row['best_media'], self.movie)
score_8 = next((bucket for bucket in report['score_buckets'] if bucket['score'] == 8))
self.assertEqual(score_8['count'], 1)
self.assertEqual(score_8['percentage'], 50)
favorites = next((band for band in report['rating_bands'] if band['label'] == 'Favorites'))
self.assertEqual(favorites['count'], 1)
self.assertEqual(favorites['percentage'], 50)
tmdb_row = next((row for row in report['source_rows'] if row['source'] == Sources.TMDB.label))
self.assertEqual(tmdb_row['count'], 2)
self.assertEqual(tmdb_row['scored'], 2)
self.assertEqual(tmdb_row['average_score'], 8.0)
year_2025 = next((row for row in report['year_rows'] if row['year'] == 2025))
self.assertEqual(year_2025['started'], 3)
self.assertEqual(year_2025['completed'], 3)
```

## Next Steps


---

*Source: test_statistics.py:718 | Complexity: Advanced | Last updated: 2026-05-22*