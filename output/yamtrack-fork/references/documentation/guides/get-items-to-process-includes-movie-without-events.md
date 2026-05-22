# How To: Get Items To Process Includes Movie Without Events

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Tracked TMDB movies should bootstrap when they do not have events yet.

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

### Step 1: 'Tracked TMDB movies should bootstrap when they do not have events yet.'

```python
'Tracked TMDB movies should bootstrap when they do not have events yet.'
```

### Step 2: Assign mock_tv_changes.return_value = set(...)

```python
mock_tv_changes.return_value = set()
```

### Step 3: Assign mock_movie_changes.return_value = set(...)

```python
mock_movie_changes.return_value = set()
```

### Step 4: Assign items = get_items_to_process(...)

```python
items = get_items_to_process(self.user)
```

### Step 5: Call self.assertIn()

```python
self.assertIn(self.movie_item, items)
```


## Complete Example

```python
# Workflow
'Tracked TMDB movies should bootstrap when they do not have events yet.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = set()
items = get_items_to_process(self.user)
self.assertIn(self.movie_item, items)
```

## Next Steps


---

*Source: test_selectors.py:209 | Complexity: Intermediate | Last updated: 2026-05-22*