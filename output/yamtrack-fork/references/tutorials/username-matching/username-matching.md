# How To: Username Matching

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test Plex username matching functionality.

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

### Step 1: 'Test Plex username matching functionality.'

```python
'Test Plex username matching functionality.'
```

### Step 2: Assign test_cases = value

```python
test_cases = [('testuser', 'testuser', True), ('testuser', 'TestUser', True), ('testuser', ' testuser ', True), ('testuser', 'testuser2', False), ('testuser1,testuser2', 'testuser1', True), ('testuser1, testuser2', 'testuser1', True), ('testuser1,testuser2', 'testuser3', False)]
```

### Step 3: Assign base_payload = value

```python
base_payload = {'event': 'media.scrobble', 'Metadata': {'type': 'movie', 'title': 'Test Movie', 'Guid': [{'id': 'tmdb://123'}]}}
```

### Step 4: Assign self.user.plex_usernames = stored_usernames

```python
self.user.plex_usernames = stored_usernames
```

### Step 5: Call self.user.save()

```python
self.user.save()
```

### Step 6: Assign payload = base_payload.copy(...)

```python
payload = base_payload.copy()
```

### Step 7: Assign unknown = value

```python
payload['Account'] = {'title': incoming_username}
```

### Step 8: Assign response = self.client.post(...)

```python
response = self.client.post(self.url, data={'payload': json.dumps(payload)}, format='multipart')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(Movie.objects.count(), 1)
```

### Step 11: Call Movie.objects.all.delete()

```python
Movie.objects.all().delete()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(Movie.objects.count(), 0)
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
'Test Plex username matching functionality.'
test_cases = [('testuser', 'testuser', True), ('testuser', 'TestUser', True), ('testuser', ' testuser ', True), ('testuser', 'testuser2', False), ('testuser1,testuser2', 'testuser1', True), ('testuser1, testuser2', 'testuser1', True), ('testuser1,testuser2', 'testuser3', False)]
base_payload = {'event': 'media.scrobble', 'Metadata': {'type': 'movie', 'title': 'Test Movie', 'Guid': [{'id': 'tmdb://123'}]}}
for i, (stored_usernames, incoming_username, should_match) in enumerate(test_cases):
    with self.subTest(f'Case {i + 1}: {stored_usernames} vs {incoming_username}'):
        self.user.plex_usernames = stored_usernames
        self.user.save()
        payload = base_payload.copy()
        payload['Account'] = {'title': incoming_username}
        response = self.client.post(self.url, data={'payload': json.dumps(payload)}, format='multipart')
        if should_match:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Movie.objects.count(), 1)
            Movie.objects.all().delete()
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Movie.objects.count(), 0)
```

## Next Steps


---

*Source: test_webhooks_plex.py:335 | Complexity: Advanced | Last updated: 2026-05-22*