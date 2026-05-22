# How To: Completed Status Creates All Seasons

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test setting status to COMPLETED creates all seasons.

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

### Step 1: 'Test setting status to COMPLETED creates all seasons.'

```python
'Test setting status to COMPLETED creates all seasons.'
```

### Step 2: Assign released_episodes = value

```python
released_episodes = [{'episode_number': episode_number, 'air_date': datetime(2020, 1, 1, tzinfo=UTC)} for episode_number in range(1, 11)]
```

### Step 3: Assign mock_metadata = value

```python
mock_metadata = {'max_progress': 10, 'related': {'seasons': [{'season_number': 1, 'image': 'img1.jpg'}, {'season_number': 2, 'image': 'img2.jpg'}, {'season_number': 3, 'image': 'img3.jpg'}]}, 'season/1': {'image': 'http://example.com/image.jpg', 'season_number': 1, 'episodes': released_episodes}, 'season/2': {'image': 'http://example.com/image.jpg', 'season_number': 2, 'episodes': released_episodes}, 'season/3': {'image': 'http://example.com/image.jpg', 'season_number': 3, 'episodes': released_episodes}}
```

### Step 4: Assign mock_get_metadata.return_value = mock_metadata

```python
mock_get_metadata.return_value = mock_metadata
```

### Step 5: Assign self.tv.status = value

```python
self.tv.status = Status.COMPLETED.value
```

### Step 6: Call self.tv.save()

```python
self.tv.save()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(self.tv.seasons.count(), 3)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(self.tv.seasons.filter(status=Status.COMPLETED.value).count(), 3)
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(season.episodes.exists())
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_metadata

# Workflow
'Test setting status to COMPLETED creates all seasons.'
released_episodes = [{'episode_number': episode_number, 'air_date': datetime(2020, 1, 1, tzinfo=UTC)} for episode_number in range(1, 11)]
mock_metadata = {'max_progress': 10, 'related': {'seasons': [{'season_number': 1, 'image': 'img1.jpg'}, {'season_number': 2, 'image': 'img2.jpg'}, {'season_number': 3, 'image': 'img3.jpg'}]}, 'season/1': {'image': 'http://example.com/image.jpg', 'season_number': 1, 'episodes': released_episodes}, 'season/2': {'image': 'http://example.com/image.jpg', 'season_number': 2, 'episodes': released_episodes}, 'season/3': {'image': 'http://example.com/image.jpg', 'season_number': 3, 'episodes': released_episodes}}
mock_get_metadata.return_value = mock_metadata
self.tv.status = Status.COMPLETED.value
self.tv.save()
self.assertEqual(self.tv.seasons.count(), 3)
self.assertEqual(self.tv.seasons.filter(status=Status.COMPLETED.value).count(), 3)
for season in self.tv.seasons.all():
    self.assertTrue(season.episodes.exists())
```

## Next Steps


---

*Source: test_tv.py:208 | Complexity: Advanced | Last updated: 2026-05-22*