# How To: Completed Last Season Completes Tv Show

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test completing the last season completes the TV show.

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

### Step 1: 'Test completing the last season completes the TV show.'

```python
'Test completing the last season completes the TV show.'
```

### Step 2: Assign mock_get_metadata.side_effect = value

```python
mock_get_metadata.side_effect = [{'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}], 'image': 'season_img.jpg'}, {'related': {'seasons': [{'season_number': 1, 'image': 'season_img.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}}]
```

### Step 3: Assign self.season.status = value

```python
self.season.status = Status.COMPLETED.value
```

### Step 4: Call self.season.save()

```python
self.season.save()
```

### Step 5: Call self.tv.refresh_from_db()

```python
self.tv.refresh_from_db()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(self.tv.status, Status.COMPLETED.value)
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
'Test completing the last season completes the TV show.'
mock_get_metadata.side_effect = [{'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}], 'image': 'season_img.jpg'}, {'related': {'seasons': [{'season_number': 1, 'image': 'season_img.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}}]
self.season.status = Status.COMPLETED.value
self.season.save()
self.tv.refresh_from_db()
self.assertEqual(self.tv.status, Status.COMPLETED.value)
```

## Next Steps


---

*Source: test_season.py:372 | Complexity: Intermediate | Last updated: 2026-05-22*