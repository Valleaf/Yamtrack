# How To: Genres Fallback To Tags

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test genres fallback to tags

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

### Step 1: Assign rg = _mock_release_group(...)

```python
rg = _mock_release_group(mb_id='tags-fallback-unique-id')
```

### Step 2: Assign unknown = value

```python
rg['genres'] = []
```

### Step 3: Assign unknown = value

```python
rg['tags'] = [{'name': 'jazz'}, {'name': 'soul'}]
```

### Step 4: Assign mock_get.return_value = rg

```python
mock_get.return_value = rg
```

### Step 5: Assign mock_artist_albums.return_value = value

```python
mock_artist_albums.return_value = []
```

### Step 6: Assign result = album(...)

```python
result = album('tags-fallback-unique-id')
```

### Step 7: Call self.assertIn()

```python
self.assertIn('jazz', result['genres'])
```


## Complete Example

```python
# Setup
# Fixtures: mock_get, mock_artist_albums

# Workflow
rg = _mock_release_group(mb_id='tags-fallback-unique-id')
rg['genres'] = []
rg['tags'] = [{'name': 'jazz'}, {'name': 'soul'}]
mock_get.return_value = rg
mock_artist_albums.return_value = []
result = album('tags-fallback-unique-id')
self.assertIn('jazz', result['genres'])
```

## Next Steps


---

*Source: test_musicbrainz.py:244 | Complexity: Intermediate | Last updated: 2026-05-22*