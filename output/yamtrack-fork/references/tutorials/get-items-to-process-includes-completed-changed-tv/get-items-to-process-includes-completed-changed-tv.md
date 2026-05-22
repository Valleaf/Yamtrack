# How To: Get Items To Process Includes Completed Changed Tv

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Changed completed TV shows should still be selected.

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

### Step 1: 'Changed completed TV shows should still be selected.'

```python
'Changed completed TV shows should still be selected.'
```

### Step 2: Assign mock_tv_changes.return_value = value

```python
mock_tv_changes.return_value = {self.tv_item.media_id}
```

### Step 3: Assign mock_movie_changes.return_value = set(...)

```python
mock_movie_changes.return_value = set()
```

### Step 4: Call TV.objects.filter.update()

```python
TV.objects.filter(item=self.tv_item, user=self.user).update(status=Status.COMPLETED.value)
```

### Step 5: Call Event.objects.create()

```python
Event.objects.create(item=self.season_item, content_number=1, datetime=timezone.now() - timezone.timedelta(days=30))
```

### Step 6: Assign items = get_items_to_process(...)

```python
items = get_items_to_process(self.user)
```

### Step 7: Call self.assertIn()

```python
self.assertIn(self.tv_item, items)
```


## Complete Example

```python
# Setup
# Fixtures: mock_tv_changes, mock_movie_changes

# Workflow
'Changed completed TV shows should still be selected.'
mock_tv_changes.return_value = {self.tv_item.media_id}
mock_movie_changes.return_value = set()
TV.objects.filter(item=self.tv_item, user=self.user).update(status=Status.COMPLETED.value)
Event.objects.create(item=self.season_item, content_number=1, datetime=timezone.now() - timezone.timedelta(days=30))
items = get_items_to_process(self.user)
self.assertIn(self.tv_item, items)
```

## Next Steps


---

*Source: test_selectors.py:93 | Complexity: Intermediate | Last updated: 2026-05-22*