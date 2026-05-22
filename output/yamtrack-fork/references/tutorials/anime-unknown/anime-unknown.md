# How To: Anime Unknown

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test the metadata method for anime with mostly unknown data.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `datetime`
- `pathlib`
- `unittest.mock`
- `requests`
- `django.conf`
- `django.test`
- `app.models`
- `app.providers`

**Setup Required:**
```python
# Fixtures: mock_data
```

## Step-by-Step Guide

### Step 1: 'Test the metadata method for anime with mostly unknown data.'

```python
'Test the metadata method for anime with mostly unknown data.'
```

### Step 2: Assign mock_data.return_value.json.return_value = anime_response

```python
mock_data.return_value.json.return_value = anime_response
```

### Step 3: Assign mock_data.return_value.status_code = 200

```python
mock_data.return_value.status_code = 200
```

### Step 4: Assign response = mal.anime(...)

```python
response = mal.anime('0')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(response['title'], 'Unknown Example')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(response['image'], settings.IMG_NONE)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(response['synopsis'], 'No synopsis available.')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(response['details']['episodes'], None)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(response['details']['runtime'], None)
```

### Step 10: Assign anime_response = json.load(...)

```python
anime_response = json.load(file)
```


## Complete Example

```python
# Setup
# Fixtures: mock_data

# Workflow
'Test the metadata method for anime with mostly unknown data.'
with Path(mock_path / 'metadata_anime_unknown.json').open() as file:
    anime_response = json.load(file)
mock_data.return_value.json.return_value = anime_response
mock_data.return_value.status_code = 200
response = mal.anime('0')
self.assertEqual(response['title'], 'Unknown Example')
self.assertEqual(response['image'], settings.IMG_NONE)
self.assertEqual(response['synopsis'], 'No synopsis available.')
self.assertEqual(response['details']['episodes'], None)
self.assertEqual(response['details']['runtime'], None)
```

## Next Steps


---

*Source: test_metadata.py:38 | Complexity: Advanced | Last updated: 2026-05-22*