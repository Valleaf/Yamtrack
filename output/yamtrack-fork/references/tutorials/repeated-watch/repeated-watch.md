# How To: Repeated Watch

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test webhook handles repeated watches.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `django.urls`
- `app.models`
- `integrations.webhooks.plex`

**Setup Required:**
```python
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token', 'plex_usernames': 'testuser'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('plex_webhook', kwargs={'token': 'test-token'})
```

## Step-by-Step Guide

### Step 1: 'Test webhook handles repeated watches.'

```python
'Test webhook handles repeated watches.'
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

### Step 5: Assign response = self.client.post(...)

```python
response = self.client.post(self.url, data=data, format='multipart')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 7: Assign movie = Movie.objects.filter(...)

```python
movie = Movie.objects.filter(item__media_id='603')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(movie.count(), 2)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(movie[0].status, Status.COMPLETED.value)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(movie[1].status, Status.COMPLETED.value)
```


## Complete Example

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token', 'plex_usernames': 'testuser'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('plex_webhook', kwargs={'token': 'test-token'})

# Workflow
'Test webhook handles repeated watches.'
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'movie', 'title': 'The Matrix', 'Guid': [{'id': 'imdb://tt0133093'}, {'id': 'tmdb://603'}, {'id': 'tvdb://169'}]}}
data = {'payload': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
movie = Movie.objects.filter(item__media_id='603')
self.assertEqual(movie.count(), 2)
self.assertEqual(movie[0].status, Status.COMPLETED.value)
self.assertEqual(movie[1].status, Status.COMPLETED.value)
```

## Next Steps


---

*Source: test_webhooks_plex.py:287 | Complexity: Advanced | Last updated: 2026-05-22*