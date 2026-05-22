# How To: Process Comic No Dates

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test process_comic with no dates available.

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
# Fixtures: mock_issue, mock_get_media_metadata
```

## Step-by-Step Guide

### Step 1: 'Test process_comic with no dates available.'

```python
'Test process_comic with no dates available.'
```

### Step 2: Assign comic_item = Item.objects.create(...)

```python
comic_item = Item.objects.create(media_id='4050-18168', source=Sources.COMICVINE.value, media_type=MediaTypes.COMIC.value, title='Wonder Woman', image='http://example.com/wonderwoman.jpg')
```

### Step 3: Assign mock_get_media_metadata.return_value = value

```python
mock_get_media_metadata.return_value = {'max_issue_number': 3, 'last_issue_id': '4000-123458', 'last_issue': {'issue_number': '3'}}
```

### Step 4: Assign mock_issue.return_value = value

```python
mock_issue.return_value = {'store_date': None, 'cover_date': None}
```

### Step 5: Assign events_bulk = value

```python
events_bulk = []
```

### Step 6: Call process_comic()

```python
process_comic(comic_item, events_bulk)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(events_bulk), 0)
```


## Complete Example

```python
# Setup
# Fixtures: mock_issue, mock_get_media_metadata

# Workflow
'Test process_comic with no dates available.'
comic_item = Item.objects.create(media_id='4050-18168', source=Sources.COMICVINE.value, media_type=MediaTypes.COMIC.value, title='Wonder Woman', image='http://example.com/wonderwoman.jpg')
mock_get_media_metadata.return_value = {'max_issue_number': 3, 'last_issue_id': '4000-123458', 'last_issue': {'issue_number': '3'}}
mock_issue.return_value = {'store_date': None, 'cover_date': None}
events_bulk = []
process_comic(comic_item, events_bulk)
self.assertEqual(len(events_bulk), 0)
```

## Next Steps


---

*Source: test_comic.py:85 | Complexity: Intermediate | Last updated: 2026-05-22*