# How To: Process Watched Movie

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test processing a movie entry.

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
# Fixtures: mock_get_metadata
```

## Step-by-Step Guide

### Step 1: 'Test processing a movie entry.'

```python
'Test processing a movie entry.'
```

### Step 2: Assign movie_entry = value

```python
movie_entry = {'type': 'movie', 'movie': {'title': 'Test Movie', 'ids': {'tmdb': 67890}}, 'watched_at': '2023-01-02T00:00:00.000Z'}
```

### Step 3: Assign mock_get_metadata.return_value = value

```python
mock_get_metadata.return_value = {'title': 'Test Movie', 'image': 'movie_image.jpg'}
```

### Step 4: Assign trakt_importer = TraktImporter(...)

```python
trakt_importer = TraktImporter('test', self.user, 'new')
```

### Step 5: Call trakt_importer.process_watched_movie()

```python
trakt_importer.process_watched_movie(movie_entry)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(trakt_importer.media_instances[MediaTypes.MOVIE.value]), 1)
```

### Step 8: Assign movie_obj = value

```python
movie_obj = trakt_importer.bulk_media[MediaTypes.MOVIE.value][0]
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(movie_obj.progress, 1)
```

### Step 10: Call trakt_importer.process_watched_movie()

```python
trakt_importer.process_watched_movie(movie_entry)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 2)
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_metadata

# Workflow
'Test processing a movie entry.'
movie_entry = {'type': 'movie', 'movie': {'title': 'Test Movie', 'ids': {'tmdb': 67890}}, 'watched_at': '2023-01-02T00:00:00.000Z'}
mock_get_metadata.return_value = {'title': 'Test Movie', 'image': 'movie_image.jpg'}
trakt_importer = TraktImporter('test', self.user, 'new')
trakt_importer.process_watched_movie(movie_entry)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 1)
self.assertEqual(len(trakt_importer.media_instances[MediaTypes.MOVIE.value]), 1)
movie_obj = trakt_importer.bulk_media[MediaTypes.MOVIE.value][0]
self.assertEqual(movie_obj.progress, 1)
trakt_importer.process_watched_movie(movie_entry)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 2)
```

## Next Steps


---

*Source: test_trakt.py:32 | Complexity: Advanced | Last updated: 2026-05-22*