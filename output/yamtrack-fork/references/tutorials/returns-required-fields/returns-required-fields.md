# How To: Returns Required Fields

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test returns required fields

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest.mock`
- `django.test`
- `app.models`
- `django.core.cache`
- `app.providers.musicbrainz`

**Setup Required:**
```python
# Fixtures: mock_get, mock_artist_albums
```

## Step-by-Step Guide

### Step 1: Assign mock_get.return_value = _mock_release_group(...)

```python
mock_get.return_value = _mock_release_group()
```

### Step 2: Assign mock_artist_albums.return_value = value

```python
mock_artist_albums.return_value = []
```

### Step 3: Assign result = album(...)

```python
result = album('abc-123')
```

### Step 4: Assign required = value

```python
required = ['media_id', 'title', 'source', 'media_type', 'image', 'synopsis', 'genres', 'details', 'tracklist', 'artist_links', 'related']
```

### Step 5: Call self.assertIn()

```python
self.assertIn(field, result)
```


## Complete Example

```python
# Setup
# Fixtures: mock_get, mock_artist_albums

# Workflow
mock_get.return_value = _mock_release_group()
mock_artist_albums.return_value = []
result = album('abc-123')
required = ['media_id', 'title', 'source', 'media_type', 'image', 'synopsis', 'genres', 'details', 'tracklist', 'artist_links', 'related']
for field in required:
    self.assertIn(field, result)
```

## Next Steps


---

*Source: test_musicbrainz.py:206 | Complexity: Intermediate | Last updated: 2026-05-22*