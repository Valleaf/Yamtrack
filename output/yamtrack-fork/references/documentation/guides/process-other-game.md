# How To: Process Other Game

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test process_other for a game.

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

### Step 1: 'Test process_other for a game.'

```python
'Test process_other for a game.'
```

### Step 2: Assign game_item = Item.objects.create(...)

```python
game_item = Item.objects.create(media_id='52189', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Grand Theft Auto VI', image='http://example.com/gta6.jpg')
```

### Step 3: Assign mock_get_media_metadata.return_value = value

```python
mock_get_media_metadata.return_value = {'max_progress': None, 'details': {'release_date': '2025-10-15'}}
```

### Step 4: Assign events_bulk = value

```python
events_bulk = []
```

### Step 5: Call process_other()

```python
process_other(game_item, events_bulk)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(events_bulk), 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].item, game_item)
```

### Step 8: Call self.assertIsNone()

```python
self.assertIsNone(events_bulk[0].content_number)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].datetime, date_parser('2025-10-15'))
```


## Complete Example

```python
# Workflow
'Test process_other for a game.'
game_item = Item.objects.create(media_id='52189', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Grand Theft Auto VI', image='http://example.com/gta6.jpg')
mock_get_media_metadata.return_value = {'max_progress': None, 'details': {'release_date': '2025-10-15'}}
events_bulk = []
process_other(game_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, game_item)
self.assertIsNone(events_bulk[0].content_number)
self.assertEqual(events_bulk[0].datetime, date_parser('2025-10-15'))
```

## Next Steps


---

*Source: test_other.py:119 | Complexity: Advanced | Last updated: 2026-05-22*