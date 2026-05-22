# How To: Fetch Releases All Types

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test fetch_releases with all media types.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest.mock`
- `django.test`
- `django.utils`
- `app.models`
- `events.calendar.main`
- `events.models`
- `events.tests.calendar.utils`

**Setup Required:**
```python
# Fixtures: mock_process_anime_bulk, mock_process_other, mock_process_tv, mock_process_comic, mock_movie_changes, mock_tv_changes
```

## Step-by-Step Guide

### Step 1: 'Test fetch_releases with all media types.'

```python
'Test fetch_releases with all media types.'
```

### Step 2: Assign mock_tv_changes.return_value = set(...)

```python
mock_tv_changes.return_value = set()
```

### Step 3: Assign mock_movie_changes.return_value = set(...)

```python
mock_movie_changes.return_value = set()
```

### Step 4: Assign mock_process_tv.side_effect = value

```python
mock_process_tv.side_effect = lambda _, events_bulk: events_bulk.append(Event(item=self.season_item, content_number=1, datetime=timezone.now()))
```

### Step 5: Assign mock_process_other.side_effect = value

```python
mock_process_other.side_effect = lambda item, events_bulk: events_bulk.append(Event(item=item, content_number=1, datetime=timezone.now()))
```

### Step 6: Assign mock_process_comic.side_effect = value

```python
mock_process_comic.side_effect = lambda item, events_bulk: events_bulk.append(Event(item=item, content_number=1, datetime=timezone.now()))
```

### Step 7: Assign mock_process_anime_bulk.side_effect = value

```python
mock_process_anime_bulk.side_effect = lambda items, events_bulk: [events_bulk.append(Event(item=item, content_number=1, datetime=timezone.now())) for item in items]
```

### Step 8: Assign result = fetch_releases(...)

```python
result = fetch_releases(self.user.id)
```

### Step 9: Call mock_process_anime_bulk.assert_called_once()

```python
mock_process_anime_bulk.assert_called_once()
```

### Step 10: Assign anime_items = value

```python
anime_items = mock_process_anime_bulk.call_args[0][0]
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(anime_items), 1)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(anime_items[0].id, self.anime_item.id)
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(Event.objects.filter(item=self.season_item).exists())
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(mock_process_other.call_count, 3)
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(Event.objects.filter(item=self.anime_item).exists())
```

### Step 16: Call self.assertTrue()

```python
self.assertTrue(Event.objects.filter(item=self.movie_item).exists())
```

### Step 17: Call self.assertTrue()

```python
self.assertTrue(Event.objects.filter(item=self.manga_item).exists())
```

### Step 18: Call self.assertTrue()

```python
self.assertTrue(Event.objects.filter(item=self.book_item).exists())
```

### Step 19: Call self.assertTrue()

```python
self.assertTrue(Event.objects.filter(item=self.comic_item).exists())
```

### Step 20: Call self.assertIn()

```python
self.assertIn('Perfect Blue', result)
```

### Step 21: Call self.assertIn()

```python
self.assertIn('The Godfather', result)
```

### Step 22: Call self.assertIn()

```python
self.assertIn('Breaking Bad', result)
```

### Step 23: Call self.assertIn()

```python
self.assertIn('Berserk', result)
```

### Step 24: Call self.assertIn()

```python
self.assertIn('1984', result)
```


## Complete Example

```python
# Setup
# Fixtures: mock_process_anime_bulk, mock_process_other, mock_process_tv, mock_process_comic, mock_movie_changes, mock_tv_changes

# Workflow
'Test fetch_releases with all media types.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = set()
mock_process_tv.side_effect = lambda _, events_bulk: events_bulk.append(Event(item=self.season_item, content_number=1, datetime=timezone.now()))
mock_process_other.side_effect = lambda item, events_bulk: events_bulk.append(Event(item=item, content_number=1, datetime=timezone.now()))
mock_process_comic.side_effect = lambda item, events_bulk: events_bulk.append(Event(item=item, content_number=1, datetime=timezone.now()))
mock_process_anime_bulk.side_effect = lambda items, events_bulk: [events_bulk.append(Event(item=item, content_number=1, datetime=timezone.now())) for item in items]
result = fetch_releases(self.user.id)
mock_process_anime_bulk.assert_called_once()
anime_items = mock_process_anime_bulk.call_args[0][0]
self.assertEqual(len(anime_items), 1)
self.assertEqual(anime_items[0].id, self.anime_item.id)
self.assertTrue(Event.objects.filter(item=self.season_item).exists())
self.assertEqual(mock_process_other.call_count, 3)
self.assertTrue(Event.objects.filter(item=self.anime_item).exists())
self.assertTrue(Event.objects.filter(item=self.movie_item).exists())
self.assertTrue(Event.objects.filter(item=self.manga_item).exists())
self.assertTrue(Event.objects.filter(item=self.book_item).exists())
self.assertTrue(Event.objects.filter(item=self.comic_item).exists())
self.assertIn('Perfect Blue', result)
self.assertIn('The Godfather', result)
self.assertIn('Breaking Bad', result)
self.assertIn('Berserk', result)
self.assertIn('1984', result)
```

## Next Steps


---

*Source: test_main.py:21 | Complexity: Advanced | Last updated: 2026-05-22*