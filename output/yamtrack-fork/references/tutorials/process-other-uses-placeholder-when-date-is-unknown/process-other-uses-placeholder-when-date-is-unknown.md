# How To: Process Other Uses Placeholder When Date Is Unknown

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: A known max progress with an empty date should use a placeholder.

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

### Step 1: 'A known max progress with an empty date should use a placeholder.'

```python
'A known max progress with an empty date should use a placeholder.'
```

### Step 2: Assign mock_get_media_metadata.return_value = value

```python
mock_get_media_metadata.return_value = {'max_progress': 328, 'details': {'publish_date': ''}}
```

### Step 3: Assign events_bulk = value

```python
events_bulk = []
```

### Step 4: Call process_other()

```python
process_other(self.book_item, events_bulk)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(events_bulk), 1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].datetime, datetime.datetime.min.replace(tzinfo=ZoneInfo('UTC')))
```


## Complete Example

```python
# Workflow
'A known max progress with an empty date should use a placeholder.'
mock_get_media_metadata.return_value = {'max_progress': 328, 'details': {'publish_date': ''}}
events_bulk = []
process_other(self.book_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].datetime, datetime.datetime.min.replace(tzinfo=ZoneInfo('UTC')))
```

## Next Steps


---

*Source: test_other.py:97 | Complexity: Intermediate | Last updated: 2026-05-22*