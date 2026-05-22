# How To: Get Access Token Uses Redirect Uri

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test refreshing Trakt tokens sends the configured redirect URI.

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

### Step 1: 'Test refreshing Trakt tokens sends the configured redirect URI.'

```python
'Test refreshing Trakt tokens sends the configured redirect URI.'
```

### Step 2: Assign mock_api_request.return_value = value

```python
mock_api_request.return_value = {'access_token': 'access-token', 'refresh_token': 'new-refresh-token'}
```

### Step 3: Assign encrypted_token = helpers.encrypt(...)

```python
encrypted_token = helpers.encrypt('refresh-token')
```

### Step 4: Assign access_token = get_access_token(...)

```python
access_token = get_access_token(encrypted_token, redirect_uri='https://yamtrack.example.com/import/trakt/private')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(access_token, 'access-token')
```

### Step 6: Assign params = value

```python
params = mock_api_request.call_args.kwargs['params']
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(params['redirect_uri'], 'https://yamtrack.example.com/import/trakt/private')
```


## Complete Example

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)

# Workflow
'Test refreshing Trakt tokens sends the configured redirect URI.'
mock_api_request.return_value = {'access_token': 'access-token', 'refresh_token': 'new-refresh-token'}
encrypted_token = helpers.encrypt('refresh-token')
access_token = get_access_token(encrypted_token, redirect_uri='https://yamtrack.example.com/import/trakt/private')
self.assertEqual(access_token, 'access-token')
params = mock_api_request.call_args.kwargs['params']
self.assertEqual(params['redirect_uri'], 'https://yamtrack.example.com/import/trakt/private')
```

## Next Steps


---

*Source: test_trakt.py:279 | Complexity: Intermediate | Last updated: 2026-05-22*