# How To: Process Other Book

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test process_other for a book.

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

### Step 1: 'Test process_other for a book.'

```python
'Test process_other for a book.'
```

### Step 2: Assign mock_get_media_metadata.return_value = value

```python
mock_get_media_metadata.return_value = {'max_progress': 328, 'details': {'publish_date': '1949-06-08'}}
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
self.assertEqual(events_bulk[0].item, self.book_item)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].content_number, 328)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].datetime, date_parser('1949-06-08'))
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_media_metadata

# Workflow
'Test process_other for a book.'
mock_get_media_metadata.return_value = {'max_progress': 328, 'details': {'publish_date': '1949-06-08'}}
events_bulk = []
process_other(self.book_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, self.book_item)
self.assertEqual(events_bulk[0].content_number, 328)
self.assertEqual(events_bulk[0].datetime, date_parser('1949-06-08'))
```

## Next Steps


---

*Source: test_other.py:36 | Complexity: Advanced | Last updated: 2026-05-22*