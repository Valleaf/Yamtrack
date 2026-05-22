# How To: Watch Method

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test the watch method of the Season model.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `pathlib`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `django.utils`
- `app.models`
- `users.models`

**Setup Required:**
```python
'Create a user and a season with episodes.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=item_season, user=self.user, status=Status.IN_PROGRESS.value)
item_ep1 = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
Episode.objects.create(item=item_ep1, related_season=self.season, end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_ep2 = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=2)
Episode.objects.create(item=item_ep2, related_season=self.season, end_date=datetime(2023, 6, 2, 0, 0, tzinfo=UTC))
```

## Step-by-Step Guide

### Step 1: 'Test the watch method of the Season model.'

```python
'Test the watch method of the Season model.'
```

### Step 2: Assign episode_item = Item.objects.create(...)

```python
episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=3)
```

### Step 3: Assign mock_get_episode_item.return_value = episode_item

```python
mock_get_episode_item.return_value = episode_item
```

### Step 4: Call self.season.watch()

```python
self.season.watch(3, datetime(2023, 6, 3, 0, 0, tzinfo=UTC))
```

### Step 5: Assign episode = Episode.objects.get(...)

```python
episode = Episode.objects.get(related_season=self.season, item=episode_item)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(episode.end_date, datetime(2023, 6, 3, 0, 0, tzinfo=UTC))
```

### Step 7: Call self.season.watch()

```python
self.season.watch(3, datetime(2023, 6, 4, 0, 0, tzinfo=UTC))
```

### Step 8: Assign episodes = Episode.objects.filter(...)

```python
episodes = Episode.objects.filter(related_season=self.season, item=episode_item)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(episodes.first().end_date, datetime(2023, 6, 4, 0, 0, tzinfo=UTC))
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(episodes.count(), 2)
```


## Complete Example

```python
# Setup
'Create a user and a season with episodes.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=item_season, user=self.user, status=Status.IN_PROGRESS.value)
item_ep1 = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
Episode.objects.create(item=item_ep1, related_season=self.season, end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_ep2 = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=2)
Episode.objects.create(item=item_ep2, related_season=self.season, end_date=datetime(2023, 6, 2, 0, 0, tzinfo=UTC))

# Workflow
'Test the watch method of the Season model.'
episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=3)
mock_get_episode_item.return_value = episode_item
self.season.watch(3, datetime(2023, 6, 3, 0, 0, tzinfo=UTC))
episode = Episode.objects.get(related_season=self.season, item=episode_item)
self.assertEqual(episode.end_date, datetime(2023, 6, 3, 0, 0, tzinfo=UTC))
self.season.watch(3, datetime(2023, 6, 4, 0, 0, tzinfo=UTC))
episodes = Episode.objects.filter(related_season=self.season, item=episode_item)
self.assertEqual(episodes.first().end_date, datetime(2023, 6, 4, 0, 0, tzinfo=UTC))
self.assertEqual(episodes.count(), 2)
```

## Next Steps


---

*Source: test_season.py:104 | Complexity: Advanced | Last updated: 2026-05-22*