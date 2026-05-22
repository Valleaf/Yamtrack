# How To: Anime Episode Mark Played

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test webhook handles anime episode mark played event.

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

### Step 1: 'Test webhook handles anime episode mark played event.'

```python
'Test webhook handles anime episode mark played event.'
```

### Step 2: Assign payload = value

```python
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'episode', 'grandparentTitle': "Frieren: Beyond Journey's End", 'index': 1, 'parentIndex': 1, 'Guid': [{'id': 'imdb://tt23861604'}, {'id': 'tmdb://3946240'}, {'id': 'tvdb://9350138'}]}}
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

### Step 6: Assign anime = Anime.objects.get(...)

```python
anime = Anime.objects.get(item__media_id='52991', user=self.user)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(anime.status, Status.IN_PROGRESS.value)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(anime.progress, 1)
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
'Test webhook handles anime episode mark played event.'
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'episode', 'grandparentTitle': "Frieren: Beyond Journey's End", 'index': 1, 'parentIndex': 1, 'Guid': [{'id': 'imdb://tt23861604'}, {'id': 'tmdb://3946240'}, {'id': 'tvdb://9350138'}]}}
data = {'payload': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
anime = Anime.objects.get(item__media_id='52991', user=self.user)
self.assertEqual(anime.status, Status.IN_PROGRESS.value)
self.assertEqual(anime.progress, 1)
```

## Next Steps


---

*Source: test_webhooks_plex.py:178 | Complexity: Advanced | Last updated: 2026-05-22*