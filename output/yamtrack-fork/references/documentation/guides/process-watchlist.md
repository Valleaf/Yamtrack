# How To: Process Watchlist

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test processing a watchlist entry.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `pathlib`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `app.models`
- `integrations.imports`
- `integrations.imports.trakt`

**Setup Required:**
```python
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
```

## Step-by-Step Guide

### Step 1: 'Test processing a watchlist entry.'

```python
'Test processing a watchlist entry.'
```

### Step 2: Assign watchlist_entry = value

```python
watchlist_entry = {'listed_at': '2023-01-01T00:00:00.000Z', 'type': 'show', 'show': {'title': 'Watchlist Show', 'ids': {'tmdb': 54321}}}
```

### Step 3: Assign mock_make_request.return_value = value

```python
mock_make_request.return_value = [watchlist_entry]
```

### Step 4: Assign mock_get_metadata.return_value = value

```python
mock_get_metadata.return_value = {'title': 'Watchlist Show', 'image': 'show_image.jpg'}
```

### Step 5: Assign trakt_importer = TraktImporter(...)

```python
trakt_importer = TraktImporter('testuser', self.user, 'new')
```

### Step 6: Call trakt_importer.process_watchlist()

```python
trakt_importer.process_watchlist()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.TV.value]), 1)
```

### Step 8: Assign tv_obj = value

```python
tv_obj = trakt_importer.bulk_media[MediaTypes.TV.value][0]
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(tv_obj.status, Status.PLANNING.value)
```


## Complete Example

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)

# Workflow
'Test processing a watchlist entry.'
watchlist_entry = {'listed_at': '2023-01-01T00:00:00.000Z', 'type': 'show', 'show': {'title': 'Watchlist Show', 'ids': {'tmdb': 54321}}}
mock_make_request.return_value = [watchlist_entry]
mock_get_metadata.return_value = {'title': 'Watchlist Show', 'image': 'show_image.jpg'}
trakt_importer = TraktImporter('testuser', self.user, 'new')
trakt_importer.process_watchlist()
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.TV.value]), 1)
tv_obj = trakt_importer.bulk_media[MediaTypes.TV.value][0]
self.assertEqual(tv_obj.status, Status.PLANNING.value)
```

## Next Steps


---

*Source: test_trakt.py:101 | Complexity: Advanced | Last updated: 2026-05-22*