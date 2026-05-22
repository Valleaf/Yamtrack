# How To: Last Season Completes Tv Show

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test last season completion also completes TV show.

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

### Step 1: 'Test last season completion also completes TV show.'

```python
'Test last season completion also completes TV show.'
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

### Step 5: Call self.tv.refresh_from_db()

```python
self.tv.refresh_from_db()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(self.tv.status, Status.COMPLETED.value)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.SUCCESS, message=f'{self.tv} was marked as completed automatically.').exists())
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_metadata

# Workflow
'Test last season completion also completes TV show.'
mock_metadata = {'season/1': {'episodes': [{'episode_number': 1}]}, 'related': {'seasons': [{'season_number': 1}]}}
mock_get_metadata.return_value = mock_metadata
Episode.objects.create(item=self.episode_item, related_season=self.season, end_date=timezone.now())
self.tv.refresh_from_db()
self.assertEqual(self.tv.status, Status.COMPLETED.value)
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.SUCCESS, message=f'{self.tv} was marked as completed automatically.').exists())
```

## Next Steps


---

*Source: test_episode.py:210 | Complexity: Intermediate | Last updated: 2026-05-22*