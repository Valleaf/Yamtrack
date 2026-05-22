# How To: Get Remaining Eps Release Date

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test get_remaining_eps uses air_date for RELEASE_DATE preference.

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
'Create a user and a season for testing.'
self.QuickWatchDateChoices = QuickWatchDateChoices
self.credentials = {'username': 'test_quick', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Friends', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=tv_item, user=self.user, status=Status.PLANNING.value)
self.season = Season.objects.create(item=item_season, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
self.mock_metadata = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(1994, 9, 22, tzinfo=UTC)}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': datetime(1994, 9, 29, tzinfo=UTC)}, {'episode_number': 3, 'image': 'img3.jpg', 'air_date': None}], 'image': 'season_img.jpg'}
```

## Step-by-Step Guide

### Step 1: 'Test get_remaining_eps uses air_date for RELEASE_DATE preference.'

```python
'Test get_remaining_eps uses air_date for RELEASE_DATE preference.'
```

### Step 2: Assign self.user.quick_watch_date = value

```python
self.user.quick_watch_date = self.QuickWatchDateChoices.RELEASE_DATE
```

### Step 3: Call self.user.save()

```python
self.user.save()
```

### Step 4: Assign episode_items = value

```python
episode_items = []
```

### Step 5: Assign mock_get_episode_item.side_effect = episode_items

```python
mock_get_episode_item.side_effect = episode_items
```

### Step 6: Assign episodes = self.season.get_remaining_eps(...)

```python
episodes = self.season.get_remaining_eps(self.mock_metadata, timezone.localdate())
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(episodes), 2)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(episodes[0].end_date, datetime(1994, 9, 29, tzinfo=UTC))
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(episodes[1].end_date, datetime(1994, 9, 22, tzinfo=UTC))
```

### Step 10: Assign item = Item.objects.create(...)

```python
item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Episode {i}', image=f'img{i}.jpg', season_number=1, episode_number=i)
```

### Step 11: Call episode_items.append()

```python
episode_items.append(item)
```


## Complete Example

```python
# Setup
'Create a user and a season for testing.'
self.QuickWatchDateChoices = QuickWatchDateChoices
self.credentials = {'username': 'test_quick', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Friends', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=tv_item, user=self.user, status=Status.PLANNING.value)
self.season = Season.objects.create(item=item_season, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
self.mock_metadata = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(1994, 9, 22, tzinfo=UTC)}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': datetime(1994, 9, 29, tzinfo=UTC)}, {'episode_number': 3, 'image': 'img3.jpg', 'air_date': None}], 'image': 'season_img.jpg'}

# Workflow
'Test get_remaining_eps uses air_date for RELEASE_DATE preference.'
self.user.quick_watch_date = self.QuickWatchDateChoices.RELEASE_DATE
self.user.save()
episode_items = []
for i in range(1, 3):
    item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Episode {i}', image=f'img{i}.jpg', season_number=1, episode_number=i)
    episode_items.append(item)
mock_get_episode_item.side_effect = episode_items
episodes = self.season.get_remaining_eps(self.mock_metadata, timezone.localdate())
self.assertEqual(len(episodes), 2)
self.assertEqual(episodes[0].end_date, datetime(1994, 9, 29, tzinfo=UTC))
self.assertEqual(episodes[1].end_date, datetime(1994, 9, 22, tzinfo=UTC))
```

## Next Steps


---

*Source: test_season.py:723 | Complexity: Advanced | Last updated: 2026-05-22*