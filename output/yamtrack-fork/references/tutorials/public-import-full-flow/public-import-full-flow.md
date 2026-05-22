# How To: Public Import Full Flow

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test full import flow with public username (no OAuth).

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

### Step 1: 'Test full import flow with public username (no OAuth).'

```python
'Test full import flow with public username (no OAuth).'
```

### Step 2: Assign mock_get_paginated.side_effect = value

```python
mock_get_paginated.side_effect = [[{'type': 'movie', 'movie': {'title': 'Public Movie', 'ids': {'tmdb': 999}}, 'watched_at': '2023-01-01T00:00:00.000Z'}], []]
```

### Step 3: Assign mock_make_request.return_value = value

```python
mock_make_request.return_value = []
```

### Step 4: Assign mock_get_metadata.return_value = value

```python
mock_get_metadata.return_value = {'title': 'Public Movie', 'image': 'movie.jpg'}
```

### Step 5: Assign unknown = importer(...)

```python
imported_counts, _ = importer(None, self.user, 'new', 'public_user')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(imported_counts[MediaTypes.MOVIE.value], 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```


## Complete Example

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)

# Workflow
'Test full import flow with public username (no OAuth).'
mock_get_paginated.side_effect = [[{'type': 'movie', 'movie': {'title': 'Public Movie', 'ids': {'tmdb': 999}}, 'watched_at': '2023-01-01T00:00:00.000Z'}], []]
mock_make_request.return_value = []
mock_get_metadata.return_value = {'title': 'Public Movie', 'image': 'movie.jpg'}
imported_counts, _ = importer(None, self.user, 'new', 'public_user')
self.assertEqual(imported_counts[MediaTypes.MOVIE.value], 1)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```

## Next Steps


---

*Source: test_trakt.py:186 | Complexity: Intermediate | Last updated: 2026-05-22*