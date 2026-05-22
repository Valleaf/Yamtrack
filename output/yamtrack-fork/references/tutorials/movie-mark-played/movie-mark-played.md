# How To: Movie Mark Played

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test webhook handles movie mark played event.

## Prerequisites

**Required Modules:**
- `json`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `django.urls`
- `app.models`
- `integrations.webhooks.plex`


## Step-by-Step Guide

### Step 1: 'Test webhook handles movie mark played event.'

```python
'Test webhook handles movie mark played event.'
```

### Step 2: Assign payload = value

```python
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'movie', 'title': 'The Matrix', 'Guid': [{'id': 'imdb://tt0133093'}, {'id': 'tmdb://603'}, {'id': 'tvdb://169'}]}}
```

### Step 3: Assign data = value

```python
data = {'payload': json.dumps(payload)}
```

### Step 4: Assign response = self.client.post(...)

```python
response = self.client.post(self.url, data=data, format='multipart')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 6: Assign movie = Movie.objects.get(...)

```python
movie = Movie.objects.get(item__media_id='603', user=self.user)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(movie.status, Status.COMPLETED.value)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(movie.progress, 1)
```


## Complete Example

```python
# Workflow
'Test webhook handles movie mark played event.'
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'movie', 'title': 'The Matrix', 'Guid': [{'id': 'imdb://tt0133093'}, {'id': 'tmdb://603'}, {'id': 'tvdb://169'}]}}
data = {'payload': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
movie = Movie.objects.get(item__media_id='603', user=self.user)
self.assertEqual(movie.status, Status.COMPLETED.value)
self.assertEqual(movie.progress, 1)
```

## Next Steps


---

*Source: test_webhooks_plex.py:90 | Complexity: Advanced | Last updated: 2026-05-22*