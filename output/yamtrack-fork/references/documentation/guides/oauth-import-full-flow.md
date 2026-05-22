# How To: Oauth Import Full Flow

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test full import flow with OAuth token.

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

### Step 1: 'Test full import flow with OAuth token.'

```python
'Test full import flow with OAuth token.'
```

### Step 2: Assign mock_get_paginated.side_effect = value

```python
mock_get_paginated.side_effect = [[{'type': 'movie', 'movie': {'title': 'OAuth Movie', 'ids': {'tmdb': 888}}, 'watched_at': '2023-01-01T00:00:00.000Z'}], []]
```

### Step 3: Assign mock_make_request.return_value = value

```python
mock_make_request.return_value = []
```

### Step 4: Assign mock_get_metadata.return_value = value

```python
mock_get_metadata.return_value = {'title': 'OAuth Movie', 'image': 'movie.jpg'}
```

### Step 5: Assign encrypted_token = helpers.encrypt(...)

```python
encrypted_token = helpers.encrypt('test_refresh_token')
```

### Step 6: Assign unknown = importer(...)

```python
imported_counts, _ = importer(encrypted_token, self.user, 'new', 'oauth_user')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(imported_counts[MediaTypes.MOVIE.value], 1)
```

### Step 8: Call self.assertEqual()

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
'Test full import flow with OAuth token.'
mock_get_paginated.side_effect = [[{'type': 'movie', 'movie': {'title': 'OAuth Movie', 'ids': {'tmdb': 888}}, 'watched_at': '2023-01-01T00:00:00.000Z'}], []]
mock_make_request.return_value = []
mock_get_metadata.return_value = {'title': 'OAuth Movie', 'image': 'movie.jpg'}
encrypted_token = helpers.encrypt('test_refresh_token')
imported_counts, _ = importer(encrypted_token, self.user, 'new', 'oauth_user')
self.assertEqual(imported_counts[MediaTypes.MOVIE.value], 1)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```

## Next Steps


---

*Source: test_trakt.py:219 | Complexity: Advanced | Last updated: 2026-05-22*