# How To: Last Episode Sets Season Completed

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test last episode sets season to COMPLETED.

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

**Setup Required:**
```python
# Fixtures: mock_get_metadata
```

## Step-by-Step Guide

### Step 1: 'Test last episode sets season to COMPLETED.'

```python
'Test last episode sets season to COMPLETED.'
```

### Step 2: Assign mock_metadata = value

```python
mock_metadata = {'season/1': {'episodes': [{'episode_number': 1}]}, 'related': {'seasons': [{'season_number': 1}]}}
```

### Step 3: Assign mock_get_metadata.return_value = mock_metadata

```python
mock_get_metadata.return_value = mock_metadata
```

### Step 4: Call Episode.objects.create()

```python
Episode.objects.create(item=self.episode_item, related_season=self.season, end_date=timezone.now())
```

### Step 5: Call self.season.refresh_from_db()

```python
self.season.refresh_from_db()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(self.season.status, Status.COMPLETED.value)
```

### Step 7: Call self.tv.refresh_from_db()

```python
self.tv.refresh_from_db()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(self.tv.status, Status.COMPLETED.value)
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_metadata

# Workflow
'Test last episode sets season to COMPLETED.'
mock_metadata = {'season/1': {'episodes': [{'episode_number': 1}]}, 'related': {'seasons': [{'season_number': 1}]}}
mock_get_metadata.return_value = mock_metadata
Episode.objects.create(item=self.episode_item, related_season=self.season, end_date=timezone.now())
self.season.refresh_from_db()
self.assertEqual(self.season.status, Status.COMPLETED.value)
self.tv.refresh_from_db()
self.assertEqual(self.tv.status, Status.COMPLETED.value)
```

## Next Steps


---

*Source: test_episode.py:143 | Complexity: Advanced | Last updated: 2026-05-22*