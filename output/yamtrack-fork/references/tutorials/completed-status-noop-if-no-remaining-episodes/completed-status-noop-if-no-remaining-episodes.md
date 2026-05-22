# How To: Completed Status Noop If No Remaining Episodes

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test COMPLETED status does nothing if no remaining episodes.

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

### Step 1: 'Test COMPLETED status does nothing if no remaining episodes.'

```python
'Test COMPLETED status does nothing if no remaining episodes.'
```

### Step 2: Assign mock_metadata = value

```python
mock_metadata = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg'}], 'image': 'season_img.jpg'}
```

### Step 3: Assign mock_get_metadata.return_value = mock_metadata

```python
mock_get_metadata.return_value = mock_metadata
```

### Step 4: Assign ep_item = Item.objects.create(...)

```python
ep_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Episode', image='http://example.com/image.jpg', season_number=1, episode_number=1)
```

### Step 5: Call Episode.objects.bulk_create()

```python
Episode.objects.bulk_create([Episode(item=ep_item, related_season=self.season, end_date=timezone.now())])
```

### Step 6: Assign self.season.status = value

```python
self.season.status = Status.COMPLETED.value
```

### Step 7: Call self.season.save()

```python
self.season.save()
```

### Step 8: Call mock_bulk_create.assert_not_called()

```python
mock_bulk_create.assert_not_called()
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
'Test COMPLETED status does nothing if no remaining episodes.'
mock_metadata = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg'}], 'image': 'season_img.jpg'}
mock_get_metadata.return_value = mock_metadata
ep_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Episode', image='http://example.com/image.jpg', season_number=1, episode_number=1)
Episode.objects.bulk_create([Episode(item=ep_item, related_season=self.season, end_date=timezone.now())])
with patch('app.models.bulk_create_with_history') as mock_bulk_create:
    self.season.status = Status.COMPLETED.value
    self.season.save()
    mock_bulk_create.assert_not_called()
```

## Next Steps


---

*Source: test_season.py:553 | Complexity: Advanced | Last updated: 2026-05-22*