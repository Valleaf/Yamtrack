# How To: Process Comments

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test processing paginated comments from Trakt.

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

### Step 1: 'Test processing paginated comments from Trakt.'

```python
'Test processing paginated comments from Trakt.'
```

### Step 2: Assign first_page = value

```python
first_page = [{'type': 'movie', 'movie': {'title': 'Commented Movie', 'ids': {'tmdb': 123}}, 'comment': {'comment': 'Great movie!', 'updated_at': '2023-01-01T00:00:00.000Z'}}]
```

### Step 3: Assign second_page = value

```python
second_page = []
```

### Step 4: Assign mock_make_request.side_effect = value

```python
mock_make_request.side_effect = [first_page, second_page]
```

### Step 5: Assign mock_get_metadata.return_value = value

```python
mock_get_metadata.return_value = {'title': 'Commented Movie', 'image': 'movie_image.jpg'}
```

### Step 6: Assign trakt_importer = TraktImporter(...)

```python
trakt_importer = TraktImporter('testuser', self.user, 'new')
```

### Step 7: Call trakt_importer.process_comments()

```python
trakt_importer.process_comments()
```

### Step 8: Assign calls = value

```python
calls = mock_make_request.call_args_list
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(calls), 2)
```

### Step 10: Call self.assertIn()

```python
self.assertIn('?page=1&limit=1000', calls[0].args[0])
```

### Step 11: Call self.assertIn()

```python
self.assertIn('?page=2&limit=1000', calls[1].args[0])
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 1)
```

### Step 13: Assign movie_obj = value

```python
movie_obj = trakt_importer.bulk_media[MediaTypes.MOVIE.value][0]
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(movie_obj.notes, 'Great movie!')
```


## Complete Example

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)

# Workflow
'Test processing paginated comments from Trakt.'
first_page = [{'type': 'movie', 'movie': {'title': 'Commented Movie', 'ids': {'tmdb': 123}}, 'comment': {'comment': 'Great movie!', 'updated_at': '2023-01-01T00:00:00.000Z'}}]
second_page = []
mock_make_request.side_effect = [first_page, second_page]
mock_get_metadata.return_value = {'title': 'Commented Movie', 'image': 'movie_image.jpg'}
trakt_importer = TraktImporter('testuser', self.user, 'new')
trakt_importer.process_comments()
calls = mock_make_request.call_args_list
self.assertEqual(len(calls), 2)
self.assertIn('?page=1&limit=1000', calls[0].args[0])
self.assertIn('?page=2&limit=1000', calls[1].args[0])
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 1)
movie_obj = trakt_importer.bulk_media[MediaTypes.MOVIE.value][0]
self.assertEqual(movie_obj.notes, 'Great movie!')
```

## Next Steps


---

*Source: test_trakt.py:148 | Complexity: Advanced | Last updated: 2026-05-22*