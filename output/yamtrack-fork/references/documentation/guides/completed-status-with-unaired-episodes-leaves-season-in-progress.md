# How To: Completed Status With Unaired Episodes Leaves Season In Progress

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Completing a season should only watch episodes that have aired.

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

### Step 1: 'Completing a season should only watch episodes that have aired.'

```python
'Completing a season should only watch episodes that have aired.'
```

### Step 2: Assign mock_get_metadata.return_value = value

```python
mock_get_metadata.return_value = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': datetime(2999, 1, 1, tzinfo=UTC)}, {'episode_number': 3, 'image': 'img3.jpg', 'air_date': None}], 'image': 'season_img.jpg'}
```

### Step 3: Assign self.season.status = value

```python
self.season.status = Status.COMPLETED.value
```

### Step 4: Call self.season.save()

```python
self.season.save()
```

### Step 5: Call self.season.refresh_from_db()

```python
self.season.refresh_from_db()
```

### Step 6: Call self.tv.refresh_from_db()

```python
self.tv.refresh_from_db()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(self.season.status, Status.IN_PROGRESS.value)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(self.tv.status, Status.IN_PROGRESS.value)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(self.season.episodes.count(), 1)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(self.season.progress, 1)
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.WARNING, message=f'{self.season} was left in progress because unreleased episodes remain.').exists())
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.season} had 1 released episode marked as watched automatically.').exists())
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
'Completing a season should only watch episodes that have aired.'
mock_get_metadata.return_value = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': datetime(2999, 1, 1, tzinfo=UTC)}, {'episode_number': 3, 'image': 'img3.jpg', 'air_date': None}], 'image': 'season_img.jpg'}
self.season.status = Status.COMPLETED.value
self.season.save()
self.season.refresh_from_db()
self.tv.refresh_from_db()
self.assertEqual(self.season.status, Status.IN_PROGRESS.value)
self.assertEqual(self.tv.status, Status.IN_PROGRESS.value)
self.assertEqual(self.season.episodes.count(), 1)
self.assertEqual(self.season.progress, 1)
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.WARNING, message=f'{self.season} was left in progress because unreleased episodes remain.').exists())
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.season} had 1 released episode marked as watched automatically.').exists())
```

## Next Steps


---

*Source: test_season.py:405 | Complexity: Advanced | Last updated: 2026-05-22*