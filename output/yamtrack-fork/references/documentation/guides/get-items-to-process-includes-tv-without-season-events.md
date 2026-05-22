# How To: Get Items To Process Includes Tv Without Season Events

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Tracked TMDB TV should bootstrap even when no season events exist yet.

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

### Step 1: 'Tracked TMDB TV should bootstrap even when no season events exist yet.'

```python
'Tracked TMDB TV should bootstrap even when no season events exist yet.'
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
self.assertIn(self.tv_item, items)
```


## Complete Example

```python
# Setup
# Fixtures: mock_tv_changes, mock_movie_changes

# Workflow
'Tracked TMDB TV should bootstrap even when no season events exist yet.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = set()
items = get_items_to_process(self.user)
self.assertIn(self.tv_item, items)
```

## Next Steps


---

*Source: test_selectors.py:137 | Complexity: Intermediate | Last updated: 2026-05-22*