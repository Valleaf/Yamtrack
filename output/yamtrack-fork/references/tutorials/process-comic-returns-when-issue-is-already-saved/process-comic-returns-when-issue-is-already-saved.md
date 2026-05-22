# How To: Process Comic Returns When Issue Is Already Saved

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: No new event should be added if the latest issue is already stored.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest.mock`
- `django.test`
- `app.models`
- `app.providers`
- `events.calendar.comic`
- `events.calendar.helpers`
- `events.models`
- `events.tests.calendar.utils`

**Setup Required:**
```python
# Fixtures: mock_get_media_metadata
```

## Step-by-Step Guide

### Step 1: 'No new event should be added if the latest issue is already stored.'

```python
'No new event should be added if the latest issue is already stored.'
```

### Step 2: Call Event.objects.create()

```python
Event.objects.create(item=self.comic_item, content_number=10, datetime=date_parser('2023-04-15'))
```

### Step 3: Assign mock_get_media_metadata.return_value = value

```python
mock_get_media_metadata.return_value = {'max_issue_number': 10, 'last_issue_id': '4000-123456', 'last_issue': {'issue_number': '10'}}
```

### Step 4: Assign events_bulk = value

```python
events_bulk = []
```

### Step 5: Call process_comic()

```python
process_comic(self.comic_item, events_bulk)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(events_bulk, [])
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_media_metadata

# Workflow
'No new event should be added if the latest issue is already stored.'
Event.objects.create(item=self.comic_item, content_number=10, datetime=date_parser('2023-04-15'))
mock_get_media_metadata.return_value = {'max_issue_number': 10, 'last_issue_id': '4000-123456', 'last_issue': {'issue_number': '10'}}
events_bulk = []
process_comic(self.comic_item, events_bulk)
self.assertEqual(events_bulk, [])
```

## Next Steps


---

*Source: test_comic.py:112 | Complexity: Intermediate | Last updated: 2026-05-22*