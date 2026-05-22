# How To: Process Other Movie

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test process_other for a movie.

## Prerequisites

- [ ] Setup code must be executed first

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

**Setup Required:**
```python
# Fixtures: mock_get_media_metadata
```

## Step-by-Step Guide

### Step 1: 'Test process_other for a movie.'

```python
'Test process_other for a movie.'
```

### Step 2: Assign mock_get_media_metadata.return_value = value

```python
mock_get_media_metadata.return_value = {'max_progress': 1, 'details': {'release_date': '1999-10-15'}}
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
self.assertEqual(len(events_bulk), 1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].item, self.movie_item)
```

### Step 7: Call self.assertIsNone()

```python
self.assertIsNone(events_bulk[0].content_number)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].datetime, date_parser('1999-10-15'))
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_media_metadata

# Workflow
'Test process_other for a movie.'
mock_get_media_metadata.return_value = {'max_progress': 1, 'details': {'release_date': '1999-10-15'}}
events_bulk = []
process_other(self.movie_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, self.movie_item)
self.assertIsNone(events_bulk[0].content_number)
self.assertEqual(events_bulk[0].datetime, date_parser('1999-10-15'))
```

## Next Steps


---

*Source: test_other.py:18 | Complexity: Advanced | Last updated: 2026-05-22*