# How To: Get Items To Process Includes Changed Movie With Existing Event

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Changed TMDB movies should be selected even with past events.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `django.utils`
- `app.models`
- `app.providers`
- `events.calendar.selectors`
- `events.models`
- `events.tests.calendar.utils`


## Step-by-Step Guide

### Step 1: 'Changed TMDB movies should be selected even with past events.'

```python
'Changed TMDB movies should be selected even with past events.'
```

### Step 2: Assign mock_tv_changes.return_value = set(...)

```python
mock_tv_changes.return_value = set()
```

### Step 3: Assign mock_movie_changes.return_value = value

```python
mock_movie_changes.return_value = {self.movie_item.media_id}
```

### Step 4: Call Event.objects.create()

```python
Event.objects.create(item=self.movie_item, content_number=None, datetime=timezone.now() - timezone.timedelta(days=30))
```

### Step 5: Assign items = get_items_to_process(...)

```python
items = get_items_to_process(self.user)
```

### Step 6: Call self.assertIn()

```python
self.assertIn(self.movie_item, items)
```


## Complete Example

```python
# Workflow
'Changed TMDB movies should be selected even with past events.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = {self.movie_item.media_id}
Event.objects.create(item=self.movie_item, content_number=None, datetime=timezone.now() - timezone.timedelta(days=30))
items = get_items_to_process(self.user)
self.assertIn(self.movie_item, items)
```

## Next Steps


---

*Source: test_selectors.py:189 | Complexity: Intermediate | Last updated: 2026-05-22*