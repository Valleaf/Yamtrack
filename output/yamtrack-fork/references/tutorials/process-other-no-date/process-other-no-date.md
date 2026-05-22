# How To: Process Other No Date

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test process_other with no date.

## Prerequisites

**Required Modules:**
- `datetime`
- `unittest.mock`
- `zoneinfo`
- `django.test`
- `app.models`
- `app.providers`
- `events.calendar.helpers`
- `events.calendar.other`
- `events.tests.calendar.utils`


## Step-by-Step Guide

### Step 1: 'Test process_other with no date.'

```python
'Test process_other with no date.'
```

### Step 2: Assign mock_get_media_metadata.return_value = value

```python
mock_get_media_metadata.return_value = {'max_progress': None, 'details': {}}
```

### Step 3: Assign events_bulk = value

```python
events_bulk = []
```

### Step 4: Call process_other()

```python
process_other(self.movie_item, events_bulk)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(events_bulk), 0)
```


## Complete Example

```python
# Workflow
'Test process_other with no date.'
mock_get_media_metadata.return_value = {'max_progress': None, 'details': {}}
events_bulk = []
process_other(self.movie_item, events_bulk)
self.assertEqual(len(events_bulk), 0)
```

## Next Steps


---

*Source: test_other.py:160 | Complexity: Intermediate | Last updated: 2026-05-22*