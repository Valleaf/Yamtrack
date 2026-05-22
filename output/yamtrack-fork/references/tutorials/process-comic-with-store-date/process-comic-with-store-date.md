# How To: Process Comic With Store Date

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test process_comic with store date available.

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

### Step 1: 'Test process_comic with store date available.'

```python
'Test process_comic with store date available.'
```

### Step 2: Assign comic_item = Item.objects.create(...)

```python
comic_item = Item.objects.create(media_id='4050-18166', source=Sources.COMICVINE.value, media_type=MediaTypes.COMIC.value, title='Batman', image='http://example.com/batman.jpg')
```

### Step 3: Assign mock_get_media_metadata.return_value = value

```python
mock_get_media_metadata.return_value = {'max_issue_number': 10, 'last_issue_id': '4000-123456', 'last_issue': {'issue_number': '10'}}
```

### Step 4: Assign mock_issue.return_value = value

```python
mock_issue.return_value = {'store_date': '2023-04-15', 'cover_date': '2023-05-01'}
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
self.assertEqual(len(events_bulk), 1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].item, comic_item)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].content_number, 10)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].datetime, date_parser('2023-04-15'))
```

### Step 11: Call mock_issue.assert_called_once_with()

```python
mock_issue.assert_called_once_with('4000-123456')
```


## Complete Example

```python
# Setup
# Fixtures: mock_issue, mock_get_media_metadata

# Workflow
'Test process_comic with store date available.'
comic_item = Item.objects.create(media_id='4050-18166', source=Sources.COMICVINE.value, media_type=MediaTypes.COMIC.value, title='Batman', image='http://example.com/batman.jpg')
mock_get_media_metadata.return_value = {'max_issue_number': 10, 'last_issue_id': '4000-123456', 'last_issue': {'issue_number': '10'}}
mock_issue.return_value = {'store_date': '2023-04-15', 'cover_date': '2023-05-01'}
events_bulk = []
process_comic(comic_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, comic_item)
self.assertEqual(events_bulk[0].content_number, 10)
self.assertEqual(events_bulk[0].datetime, date_parser('2023-04-15'))
mock_issue.assert_called_once_with('4000-123456')
```

## Next Steps


---

*Source: test_comic.py:18 | Complexity: Advanced | Last updated: 2026-05-22*