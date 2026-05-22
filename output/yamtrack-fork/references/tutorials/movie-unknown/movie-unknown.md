# How To: Movie Unknown

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test the metadata method for movies with mostly unknown data.

## Prerequisites

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


## Step-by-Step Guide

### Step 1: 'Test the metadata method for movies with mostly unknown data.'

```python
'Test the metadata method for movies with mostly unknown data.'
```

### Step 2: Assign mock_data.return_value.json.return_value = movie_response

```python
mock_data.return_value.json.return_value = movie_response
```

### Step 3: Assign mock_data.return_value.status_code = 200

```python
mock_data.return_value.status_code = 200
```

### Step 4: Assign response = tmdb.movie(...)

```python
response = tmdb.movie('0')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(response['title'], 'Unknown Movie')
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
self.assertEqual(response['details']['release_date'], None)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(response['details']['runtime'], None)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(response['genres'], None)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(response['details']['studios'], None)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(response['details']['country'], None)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(response['details']['languages'], None)
```

### Step 14: Assign movie_response = json.load(...)

```python
movie_response = json.load(file)
```


## Complete Example

```python
# Workflow
'Test the metadata method for movies with mostly unknown data.'
with Path(mock_path / 'metadata_movie_unknown.json').open() as file:
    movie_response = json.load(file)
mock_data.return_value.json.return_value = movie_response
mock_data.return_value.status_code = 200
response = tmdb.movie('0')
self.assertEqual(response['title'], 'Unknown Movie')
self.assertEqual(response['image'], settings.IMG_NONE)
self.assertEqual(response['synopsis'], 'No synopsis available.')
self.assertEqual(response['details']['release_date'], None)
self.assertEqual(response['details']['runtime'], None)
self.assertEqual(response['genres'], None)
self.assertEqual(response['details']['studios'], None)
self.assertEqual(response['details']['country'], None)
self.assertEqual(response['details']['languages'], None)
```

## Next Steps


---

*Source: test_metadata.py:321 | Complexity: Advanced | Last updated: 2026-05-22*