# How To: Process Other Mangaupdates

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test process_other for MangaUpdates manga.

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

### Step 1: 'Test process_other for MangaUpdates manga.'

```python
'Test process_other for MangaUpdates manga.'
```

### Step 2: Assign mangaupdates_item = Item.objects.create(...)

```python
mangaupdates_item = Item.objects.create(media_id='123', source=Sources.MANGAUPDATES.value, media_type=MediaTypes.MANGA.value, title='Some Manga', image='http://example.com/manga.jpg')
```

### Step 3: Assign mock_get_media_metadata.return_value = value

```python
mock_get_media_metadata.return_value = {'max_progress': 100, 'details': {}}
```

### Step 4: Assign events_bulk = value

```python
events_bulk = []
```

### Step 5: Call process_other()

```python
process_other(mangaupdates_item, events_bulk)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(events_bulk), 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].item, mangaupdates_item)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].content_number, 100)
```

### Step 9: Assign expected_date = datetime.datetime.min.replace(...)

```python
expected_date = datetime.datetime.min.replace(tzinfo=ZoneInfo('UTC'))
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].datetime, expected_date)
```


## Complete Example

```python
# Workflow
'Test process_other for MangaUpdates manga.'
mangaupdates_item = Item.objects.create(media_id='123', source=Sources.MANGAUPDATES.value, media_type=MediaTypes.MANGA.value, title='Some Manga', image='http://example.com/manga.jpg')
mock_get_media_metadata.return_value = {'max_progress': 100, 'details': {}}
events_bulk = []
process_other(mangaupdates_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, mangaupdates_item)
self.assertEqual(events_bulk[0].content_number, 100)
expected_date = datetime.datetime.min.replace(tzinfo=ZoneInfo('UTC'))
self.assertEqual(events_bulk[0].datetime, expected_date)
```

## Next Steps


---

*Source: test_other.py:72 | Complexity: Advanced | Last updated: 2026-05-22*