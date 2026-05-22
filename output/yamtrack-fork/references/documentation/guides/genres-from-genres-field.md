# How To: Genres From Genres Field

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test genres from genres field

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
rg = _mock_release_group()
```

### Step 2: Assign unknown = value

```python
rg['genres'] = [{'name': 'rock'}, {'name': 'pop'}]
```

### Step 3: Assign mock_get.return_value = rg

```python
mock_get.return_value = rg
```

### Step 4: Assign mock_artist_albums.return_value = value

```python
mock_artist_albums.return_value = []
```

### Step 5: Assign result = album(...)

```python
result = album('abc-123')
```

### Step 6: Call self.assertIn()

```python
self.assertIn('rock', result['genres'])
```


## Complete Example

```python
# Setup
# Fixtures: mock_get, mock_artist_albums

# Workflow
rg = _mock_release_group()
rg['genres'] = [{'name': 'rock'}, {'name': 'pop'}]
mock_get.return_value = rg
mock_artist_albums.return_value = []
result = album('abc-123')
self.assertIn('rock', result['genres'])
```

## Next Steps


---

*Source: test_musicbrainz.py:234 | Complexity: Intermediate | Last updated: 2026-05-22*