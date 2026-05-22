# How To: Completed Status Creates Remaining Episodes

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test setting status to COMPLETED creates remaining episodes.

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
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
```

## Step-by-Step Guide

### Step 1: 'Test setting status to COMPLETED creates remaining episodes.'

```python
'Test setting status to COMPLETED creates remaining episodes.'
```

### Step 2: Assign mock_metadata = value

```python
mock_metadata = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': datetime(2020, 1, 2, tzinfo=UTC)}, {'episode_number': 3, 'image': 'img3.jpg', 'air_date': datetime(2020, 1, 3, tzinfo=UTC)}], 'image': 'season_img.jpg'}
```

### Step 3: Assign mock_get_metadata.return_value = mock_metadata

```python
mock_get_metadata.return_value = mock_metadata
```

### Step 4: Assign self.season.status = value

```python
self.season.status = Status.COMPLETED.value
```

### Step 5: Call self.season.save()

```python
self.season.save()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(self.season.episodes.count(), 3)
```

### Step 7: Assign episode_numbers = set(...)

```python
episode_numbers = set(self.season.episodes.values_list('item__episode_number', flat=True))
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(episode_numbers, {1, 2, 3})
```


## Complete Example

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)

# Workflow
'Test setting status to COMPLETED creates remaining episodes.'
mock_metadata = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': datetime(2020, 1, 2, tzinfo=UTC)}, {'episode_number': 3, 'image': 'img3.jpg', 'air_date': datetime(2020, 1, 3, tzinfo=UTC)}], 'image': 'season_img.jpg'}
mock_get_metadata.return_value = mock_metadata
self.season.status = Status.COMPLETED.value
self.season.save()
self.assertEqual(self.season.episodes.count(), 3)
episode_numbers = set(self.season.episodes.values_list('item__episode_number', flat=True))
self.assertEqual(episode_numbers, {1, 2, 3})
```

## Next Steps


---

*Source: test_season.py:282 | Complexity: Advanced | Last updated: 2026-05-22*