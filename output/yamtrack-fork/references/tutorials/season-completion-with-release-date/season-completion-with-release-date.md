# How To: Season Completion With Release Date

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Integration test: completing a season with RELEASE_DATE preference.

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

### Step 1: 'Integration test: completing a season with RELEASE_DATE preference.'

```python
'Integration test: completing a season with RELEASE_DATE preference.'
```

### Step 2: Assign self.user.quick_watch_date = value

```python
self.user.quick_watch_date = self.QuickWatchDateChoices.RELEASE_DATE
```

### Step 3: Call self.user.save()

```python
self.user.save()
```

### Step 4: Assign mock_get_metadata.return_value = value

```python
mock_get_metadata.return_value = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(1994, 9, 22, tzinfo=UTC)}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': datetime(1994, 9, 29, tzinfo=UTC)}], 'image': 'season_img.jpg'}
```

### Step 5: Assign self.season.status = value

```python
self.season.status = Status.COMPLETED.value
```

### Step 6: Call self.season.save()

```python
self.season.save()
```

### Step 7: Assign episodes = Episode.objects.filter.order_by(...)

```python
episodes = Episode.objects.filter(related_season=self.season).order_by('item__episode_number')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(episodes.count(), 2)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(episodes[0].end_date, datetime(1994, 9, 22, tzinfo=UTC))
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(episodes[1].end_date, datetime(1994, 9, 29, tzinfo=UTC))
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
'Integration test: completing a season with RELEASE_DATE preference.'
self.user.quick_watch_date = self.QuickWatchDateChoices.RELEASE_DATE
self.user.save()
mock_get_metadata.return_value = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(1994, 9, 22, tzinfo=UTC)}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': datetime(1994, 9, 29, tzinfo=UTC)}], 'image': 'season_img.jpg'}
self.season.status = Status.COMPLETED.value
self.season.save()
episodes = Episode.objects.filter(related_season=self.season).order_by('item__episode_number')
self.assertEqual(episodes.count(), 2)
self.assertEqual(episodes[0].end_date, datetime(1994, 9, 22, tzinfo=UTC))
self.assertEqual(episodes[1].end_date, datetime(1994, 9, 29, tzinfo=UTC))
```

## Next Steps


---

*Source: test_season.py:774 | Complexity: Advanced | Last updated: 2026-05-22*