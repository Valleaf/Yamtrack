# How To: Process Other Manga

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test process_other for manga.

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

### Step 1: 'Test process_other for manga.'

```python
'Test process_other for manga.'
```

### Step 2: Assign mock_get_media_metadata.return_value = value

```python
mock_get_media_metadata.return_value = {'details': {'end_date': '2023-12-22'}, 'max_progress': 375}
```

### Step 3: Assign events_bulk = value

```python
events_bulk = []
```

### Step 4: Call process_other()

```python
process_other(self.manga_item, events_bulk)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(events_bulk), 1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].item, self.manga_item)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].content_number, 375)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].datetime, date_parser('2023-12-22'))
```


## Complete Example

```python
# Workflow
'Test process_other for manga.'
mock_get_media_metadata.return_value = {'details': {'end_date': '2023-12-22'}, 'max_progress': 375}
events_bulk = []
process_other(self.manga_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, self.manga_item)
self.assertEqual(events_bulk[0].content_number, 375)
self.assertEqual(events_bulk[0].datetime, date_parser('2023-12-22'))
```

## Next Steps


---

*Source: test_other.py:54 | Complexity: Advanced | Last updated: 2026-05-22*