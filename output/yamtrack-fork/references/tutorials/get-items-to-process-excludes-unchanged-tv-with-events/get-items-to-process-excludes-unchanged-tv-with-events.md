# How To: Get Items To Process Excludes Unchanged Tv With Events

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Tracked TV with existing season events should be skipped when unchanged.

## Prerequisites

- [ ] Setup code must be executed first

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

**Setup Required:**
```python
# Fixtures: mock_tv_changes, mock_movie_changes
```

## Step-by-Step Guide

### Step 1: 'Tracked TV with existing season events should be skipped when unchanged.'

```python
'Tracked TV with existing season events should be skipped when unchanged.'
```

### Step 2: Assign mock_tv_changes.return_value = set(...)

```python
mock_tv_changes.return_value = set()
```

### Step 3: Assign mock_movie_changes.return_value = set(...)

```python
mock_movie_changes.return_value = set()
```

### Step 4: Call Event.objects.create()

```python
Event.objects.create(item=self.season_item, content_number=1, datetime=timezone.now() - timezone.timedelta(days=30))
```

### Step 5: Assign items = get_items_to_process(...)

```python
items = get_items_to_process(self.user)
```

### Step 6: Call self.assertNotIn()

```python
self.assertNotIn(self.tv_item, items)
```


## Complete Example

```python
# Setup
# Fixtures: mock_tv_changes, mock_movie_changes

# Workflow
'Tracked TV with existing season events should be skipped when unchanged.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = set()
Event.objects.create(item=self.season_item, content_number=1, datetime=timezone.now() - timezone.timedelta(days=30))
items = get_items_to_process(self.user)
self.assertNotIn(self.tv_item, items)
```

## Next Steps


---

*Source: test_selectors.py:117 | Complexity: Intermediate | Last updated: 2026-05-22*