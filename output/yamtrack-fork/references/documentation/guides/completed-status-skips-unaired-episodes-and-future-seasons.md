# How To: Completed Status Skips Unaired Episodes And Future Seasons

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Completed TV should only mark already aired content as watched.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `pathlib`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `app.models`

**Setup Required:**
```python
# Fixtures: mock_get_metadata
```

## Step-by-Step Guide

### Step 1: 'Completed TV should only mark already aired content as watched.'

```python
'Completed TV should only mark already aired content as watched.'
```

### Step 2: Assign mock_get_metadata.return_value = value

```python
mock_get_metadata.return_value = {'max_progress': 4, 'related': {'seasons': [{'season_number': 1, 'image': 'img1.jpg'}, {'season_number': 2, 'image': 'img2.jpg'}, {'season_number': 3, 'image': 'img3.jpg'}]}, 'season/1': {'image': 'http://example.com/image.jpg', 'season_number': 1, 'episodes': [{'episode_number': 1, 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}, 'season/2': {'image': 'http://example.com/image.jpg', 'season_number': 2, 'episodes': [{'episode_number': 1, 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'episode_number': 2, 'air_date': datetime(2999, 1, 1, tzinfo=UTC)}]}, 'season/3': {'image': 'http://example.com/image.jpg', 'season_number': 3, 'episodes': [{'episode_number': 1, 'air_date': None}]}}
```

### Step 3: Assign self.tv.status = value

```python
self.tv.status = Status.COMPLETED.value
```

### Step 4: Call self.tv.save()

```python
self.tv.save()
```

### Step 5: Assign season1 = self.tv.seasons.get(...)

```python
season1 = self.tv.seasons.get(item__season_number=1)
```

### Step 6: Assign season2 = self.tv.seasons.get(...)

```python
season2 = self.tv.seasons.get(item__season_number=2)
```

### Step 7: Assign season3 = self.tv.seasons.get(...)

```python
season3 = self.tv.seasons.get(item__season_number=3)
```

### Step 8: Call self.tv.refresh_from_db()

```python
self.tv.refresh_from_db()
```

### Step 9: Call season1.refresh_from_db()

```python
season1.refresh_from_db()
```

### Step 10: Call season2.refresh_from_db()

```python
season2.refresh_from_db()
```

### Step 11: Call season3.refresh_from_db()

```python
season3.refresh_from_db()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(self.tv.status, Status.IN_PROGRESS.value)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(season1.status, Status.COMPLETED.value)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(season2.status, Status.IN_PROGRESS.value)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(season3.status, Status.PLANNING.value)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(season2.episodes.count(), 1)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(season2.progress, 1)
```

### Step 18: Call self.assertFalse()

```python
self.assertFalse(season3.episodes.exists())
```

### Step 19: Call self.assertTrue()

```python
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.WARNING, message=f'{self.tv} was left in progress because unreleased episodes or seasons remain.').exists())
```

### Step 20: Call self.assertTrue()

```python
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.tv} had 2 released episodes marked as watched automatically.').exists())
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_metadata

# Workflow
'Completed TV should only mark already aired content as watched.'
mock_get_metadata.return_value = {'max_progress': 4, 'related': {'seasons': [{'season_number': 1, 'image': 'img1.jpg'}, {'season_number': 2, 'image': 'img2.jpg'}, {'season_number': 3, 'image': 'img3.jpg'}]}, 'season/1': {'image': 'http://example.com/image.jpg', 'season_number': 1, 'episodes': [{'episode_number': 1, 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}, 'season/2': {'image': 'http://example.com/image.jpg', 'season_number': 2, 'episodes': [{'episode_number': 1, 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'episode_number': 2, 'air_date': datetime(2999, 1, 1, tzinfo=UTC)}]}, 'season/3': {'image': 'http://example.com/image.jpg', 'season_number': 3, 'episodes': [{'episode_number': 1, 'air_date': None}]}}
self.tv.status = Status.COMPLETED.value
self.tv.save()
season1 = self.tv.seasons.get(item__season_number=1)
season2 = self.tv.seasons.get(item__season_number=2)
season3 = self.tv.seasons.get(item__season_number=3)
self.tv.refresh_from_db()
season1.refresh_from_db()
season2.refresh_from_db()
season3.refresh_from_db()
self.assertEqual(self.tv.status, Status.IN_PROGRESS.value)
self.assertEqual(season1.status, Status.COMPLETED.value)
self.assertEqual(season2.status, Status.IN_PROGRESS.value)
self.assertEqual(season3.status, Status.PLANNING.value)
self.assertEqual(season2.episodes.count(), 1)
self.assertEqual(season2.progress, 1)
self.assertFalse(season3.episodes.exists())
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.WARNING, message=f'{self.tv} was left in progress because unreleased episodes or seasons remain.').exists())
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.tv} had 2 released episodes marked as watched automatically.').exists())
```

## Next Steps


---

*Source: test_tv.py:257 | Complexity: Advanced | Last updated: 2026-05-22*