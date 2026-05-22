# How To: End Date Only Filtering

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test filtering for media with only end date.

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
self.movie1_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with start and end dates')
self.movie2_item = Item.objects.create(media_id='239', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only start date')
self.movie3_item = Item.objects.create(media_id='240', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only end date')
self.movie4_item = Item.objects.create(media_id='241', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with no dates')
self.movie5_item = Item.objects.create(media_id='242', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (before)')
self.movie6_item = Item.objects.create(media_id='243', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (after)')
self.movie7_item = Item.objects.create(media_id='244', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts before, ends in range)')
self.movie8_item = Item.objects.create(media_id='245', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts in range, ends after)')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value, score=8.0)
self.episode1 = Episode.objects.create(item=self.episode1_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC))
self.episode2 = Episode.objects.create(item=self.episode2_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie1 = Movie.objects.create(user=self.user, item=self.movie1_item, status=Status.COMPLETED.value, score=7.5, start_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC))
self.movie2 = Movie.objects.create(user=self.user, item=self.movie2_item, status=Status.IN_PROGRESS.value, score=8.0, start_date=datetime.datetime(2025, 2, 15, 0, 0, tzinfo=datetime.UTC), end_date=None)
self.movie3 = Movie.objects.create(user=self.user, item=self.movie3_item, status=Status.COMPLETED.value, score=6.5, start_date=None, end_date=datetime.datetime(2025, 2, 20, 0, 0, tzinfo=datetime.UTC))
self.movie4 = Movie.objects.create(user=self.user, item=self.movie4_item, status=Status.PLANNING.value, score=None, start_date=None, end_date=None)
self.movie5 = Movie.objects.create(user=self.user, item=self.movie5_item, status=Status.COMPLETED.value, score=9.0, start_date=datetime.datetime(2025, 1, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie6 = Movie.objects.create(user=self.user, item=self.movie6_item, status=Status.PLANNING.value, score=None, start_date=datetime.datetime(2025, 3, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 15, 0, 0, tzinfo=datetime.UTC))
self.movie7 = Movie.objects.create(user=self.user, item=self.movie7_item, status=Status.COMPLETED.value, score=7.0, start_date=datetime.datetime(2025, 1, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 5, 0, 0, tzinfo=datetime.UTC))
self.movie8 = Movie.objects.create(user=self.user, item=self.movie8_item, status=Status.COMPLETED.value, score=8.5, start_date=datetime.datetime(2025, 2, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 5, 0, 0, tzinfo=datetime.UTC))
```

## Step-by-Step Guide

### Step 1: 'Test filtering for media with only end date.'

```python
'Test filtering for media with only end date.'
```

### Step 2: Assign start_date = datetime.datetime(...)

```python
start_date = datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC)
```

### Step 3: Assign end_date = datetime.datetime(...)

```python
end_date = datetime.datetime(2025, 2, 20, 0, 0, tzinfo=datetime.UTC)
```

### Step 4: Assign unknown = statistics.get_user_media(...)

```python
user_media, _ = statistics.get_user_media(self.user, start_date, end_date)
```

### Step 5: Assign movie_ids = value

```python
movie_ids = [m.item.id for m in user_media[MediaTypes.MOVIE.value]]
```

### Step 6: Call self.assertIn()

```python
self.assertIn(self.movie3_item.id, movie_ids)
```

### Step 7: Assign outside_item = Item.objects.create(...)

```python
outside_item = Item.objects.create(media_id='247', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with end date outside range')
```

### Step 8: Call Movie.objects.create()

```python
Movie.objects.create(user=self.user, item=outside_item, status=Status.COMPLETED.value, start_date=None, end_date=datetime.datetime(2025, 3, 1, 0, 0, tzinfo=datetime.UTC))
```

### Step 9: Assign unknown = statistics.get_user_media(...)

```python
user_media, _ = statistics.get_user_media(self.user, start_date, end_date)
```

### Step 10: Assign movie_ids = value

```python
movie_ids = [m.item.id for m in user_media[MediaTypes.MOVIE.value]]
```

### Step 11: Call self.assertNotIn()

```python
self.assertNotIn(outside_item.id, movie_ids)
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
self.movie1_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with start and end dates')
self.movie2_item = Item.objects.create(media_id='239', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only start date')
self.movie3_item = Item.objects.create(media_id='240', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only end date')
self.movie4_item = Item.objects.create(media_id='241', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with no dates')
self.movie5_item = Item.objects.create(media_id='242', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (before)')
self.movie6_item = Item.objects.create(media_id='243', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (after)')
self.movie7_item = Item.objects.create(media_id='244', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts before, ends in range)')
self.movie8_item = Item.objects.create(media_id='245', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts in range, ends after)')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value, score=8.0)
self.episode1 = Episode.objects.create(item=self.episode1_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC))
self.episode2 = Episode.objects.create(item=self.episode2_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie1 = Movie.objects.create(user=self.user, item=self.movie1_item, status=Status.COMPLETED.value, score=7.5, start_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC))
self.movie2 = Movie.objects.create(user=self.user, item=self.movie2_item, status=Status.IN_PROGRESS.value, score=8.0, start_date=datetime.datetime(2025, 2, 15, 0, 0, tzinfo=datetime.UTC), end_date=None)
self.movie3 = Movie.objects.create(user=self.user, item=self.movie3_item, status=Status.COMPLETED.value, score=6.5, start_date=None, end_date=datetime.datetime(2025, 2, 20, 0, 0, tzinfo=datetime.UTC))
self.movie4 = Movie.objects.create(user=self.user, item=self.movie4_item, status=Status.PLANNING.value, score=None, start_date=None, end_date=None)
self.movie5 = Movie.objects.create(user=self.user, item=self.movie5_item, status=Status.COMPLETED.value, score=9.0, start_date=datetime.datetime(2025, 1, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie6 = Movie.objects.create(user=self.user, item=self.movie6_item, status=Status.PLANNING.value, score=None, start_date=datetime.datetime(2025, 3, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 15, 0, 0, tzinfo=datetime.UTC))
self.movie7 = Movie.objects.create(user=self.user, item=self.movie7_item, status=Status.COMPLETED.value, score=7.0, start_date=datetime.datetime(2025, 1, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 5, 0, 0, tzinfo=datetime.UTC))
self.movie8 = Movie.objects.create(user=self.user, item=self.movie8_item, status=Status.COMPLETED.value, score=8.5, start_date=datetime.datetime(2025, 2, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 5, 0, 0, tzinfo=datetime.UTC))

# Workflow
'Test filtering for media with only end date.'
start_date = datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC)
end_date = datetime.datetime(2025, 2, 20, 0, 0, tzinfo=datetime.UTC)
user_media, _ = statistics.get_user_media(self.user, start_date, end_date)
movie_ids = [m.item.id for m in user_media[MediaTypes.MOVIE.value]]
self.assertIn(self.movie3_item.id, movie_ids)
outside_item = Item.objects.create(media_id='247', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with end date outside range')
Movie.objects.create(user=self.user, item=outside_item, status=Status.COMPLETED.value, start_date=None, end_date=datetime.datetime(2025, 3, 1, 0, 0, tzinfo=datetime.UTC))
user_media, _ = statistics.get_user_media(self.user, start_date, end_date)
movie_ids = [m.item.id for m in user_media[MediaTypes.MOVIE.value]]
self.assertNotIn(outside_item.id, movie_ids)
```

## Next Steps


---

*Source: test_statistics.py:338 | Complexity: Advanced | Last updated: 2026-05-22*