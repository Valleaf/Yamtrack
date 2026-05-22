# How To: Anime Episode Anidb Guid Mark Played

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test webhook handles anime episode with anidb guid.

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

### Step 1: 'Test webhook handles anime episode with anidb guid.'

```python
'Test webhook handles anime episode with anidb guid.'
```

### Step 2: Assign mock_fetch_mapping_data.return_value = value

```python
mock_fetch_mapping_data.return_value = {'3651': {'mal_id': 849}}
```

### Step 3: Assign payload = value

```python
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'episode', 'index': 1, 'parentIndex': 1, 'guid': 'com.plexapp.agents.hama://anidb-3651/1/1?lang=en'}}
```

### Step 4: Assign data = value

```python
data = {'payload': json.dumps(payload)}
```

### Step 5: Assign response = self.client.post(...)

```python
response = self.client.post(self.url, data=data, format='multipart')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 7: Call mock_handle_anime.assert_called_once_with()

```python
mock_handle_anime.assert_called_once_with(849, 1, payload, self.user)
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
'Test webhook handles anime episode with anidb guid.'
mock_fetch_mapping_data.return_value = {'3651': {'mal_id': 849}}
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'episode', 'index': 1, 'parentIndex': 1, 'guid': 'com.plexapp.agents.hama://anidb-3651/1/1?lang=en'}}
data = {'payload': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
mock_handle_anime.assert_called_once_with(849, 1, payload, self.user)
```

## Next Steps


---

*Source: test_webhooks_plex.py:384 | Complexity: Intermediate | Last updated: 2026-05-22*