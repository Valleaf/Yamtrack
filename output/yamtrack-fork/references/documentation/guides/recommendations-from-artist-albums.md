# How To: Recommendations From Artist Albums

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test recommendations from artist albums

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
mock_get.return_value = _mock_release_group(mb_id='recs-unique-id', artist_id='beatles-uuid')
```

### Step 2: Assign mock_artist_albums.return_value = value

```python
mock_artist_albums.return_value = [{'media_id': 'other-uuid', 'title': 'Let It Be', 'media_type': 'music'}]
```

### Step 3: Assign result = album(...)

```python
result = album('recs-unique-id')
```

### Step 4: Assign related_flat = value

```python
related_flat = []
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(related_flat), 1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(related_flat[0]['title'], 'Let It Be')
```

### Step 7: Call related_flat.extend()

```python
related_flat.extend(v)
```


## Complete Example

```python
# Setup
# Fixtures: mock_get, mock_artist_albums

# Workflow
mock_get.return_value = _mock_release_group(mb_id='recs-unique-id', artist_id='beatles-uuid')
mock_artist_albums.return_value = [{'media_id': 'other-uuid', 'title': 'Let It Be', 'media_type': 'music'}]
result = album('recs-unique-id')
related_flat = []
for v in result['related'].values():
    related_flat.extend(v)
self.assertEqual(len(related_flat), 1)
self.assertEqual(related_flat[0]['title'], 'Let It Be')
```

## Next Steps


---

*Source: test_musicbrainz.py:268 | Complexity: Intermediate | Last updated: 2026-05-22*