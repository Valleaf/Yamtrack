# How To: Process Ratings

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test processing a rating entry.

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

### Step 1: 'Test processing a rating entry.'

```python
'Test processing a rating entry.'
```

### Step 2: Assign rating_entry = value

```python
rating_entry = {'rated_at': '2023-01-01T00:00:00.000Z', 'type': 'movie', 'movie': {'title': 'Rated Movie', 'ids': {'tmdb': 238}}, 'rating': 8}
```

### Step 3: Assign mock_make_request.return_value = value

```python
mock_make_request.return_value = [rating_entry]
```

### Step 4: Assign mock_get_metadata.return_value = value

```python
mock_get_metadata.return_value = {'title': 'Rated Movie', 'image': 'movie_image.jpg'}
```

### Step 5: Assign trakt_importer = TraktImporter(...)

```python
trakt_importer = TraktImporter('testuser', self.user, 'new')
```

### Step 6: Call trakt_importer.process_ratings()

```python
trakt_importer.process_ratings()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 1)
```

### Step 8: Assign movie_obj = value

```python
movie_obj = trakt_importer.bulk_media[MediaTypes.MOVIE.value][0]
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(movie_obj.score, 8)
```


## Complete Example

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)

# Workflow
'Test processing a rating entry.'
rating_entry = {'rated_at': '2023-01-01T00:00:00.000Z', 'type': 'movie', 'movie': {'title': 'Rated Movie', 'ids': {'tmdb': 238}}, 'rating': 8}
mock_make_request.return_value = [rating_entry]
mock_get_metadata.return_value = {'title': 'Rated Movie', 'image': 'movie_image.jpg'}
trakt_importer = TraktImporter('testuser', self.user, 'new')
trakt_importer.process_ratings()
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 1)
movie_obj = trakt_importer.bulk_media[MediaTypes.MOVIE.value][0]
self.assertEqual(movie_obj.score, 8)
```

## Next Steps


---

*Source: test_trakt.py:124 | Complexity: Advanced | Last updated: 2026-05-22*