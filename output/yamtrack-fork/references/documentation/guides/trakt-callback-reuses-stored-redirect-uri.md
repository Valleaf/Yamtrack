# How To: Trakt Callback Reuses Stored Redirect Uri

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test the token exchange and import task reuse the original redirect URI.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest.mock`
- `urllib.parse`
- `django.contrib.auth`
- `django.test`
- `django.urls`

**Setup Required:**
```python
# Fixtures: mock_oauth_callback, mock_import_trakt
```

## Step-by-Step Guide

### Step 1: 'Test the token exchange and import task reuse the original redirect URI.'

```python
'Test the token exchange and import task reuse the original redirect URI.'
```

### Step 2: Assign redirect_uri = 'https://yamtrack.example.com:8924/import/trakt/private'

```python
redirect_uri = 'https://yamtrack.example.com:8924/import/trakt/private'
```

### Step 3: Assign session = value

```python
session = self.client.session
```

### Step 4: Assign unknown = value

```python
session['state-token'] = {'mode': 'new', 'frequency': 'once', 'time': '14:30', 'redirect_uri': redirect_uri}
```

### Step 5: Call session.save()

```python
session.save()
```

### Step 6: Assign mock_oauth_callback.return_value = value

```python
mock_oauth_callback.return_value = {'refresh_token': 'refresh-token', 'username': 'trakt-user'}
```

### Step 7: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('import_trakt_private'), {'code': 'code', 'state': 'state-token'})
```

### Step 8: Call self.assertRedirects()

```python
self.assertRedirects(response, reverse('import_data'))
```

### Step 9: Call mock_oauth_callback.assert_called_once()

```python
mock_oauth_callback.assert_called_once()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(mock_oauth_callback.call_args.kwargs['redirect_uri'], redirect_uri)
```

### Step 11: Call mock_import_trakt.assert_called_once()

```python
mock_import_trakt.assert_called_once()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(mock_import_trakt.call_args.kwargs['redirect_uri'], redirect_uri)
```


## Complete Example

```python
# Setup
# Fixtures: mock_oauth_callback, mock_import_trakt

# Workflow
'Test the token exchange and import task reuse the original redirect URI.'
redirect_uri = 'https://yamtrack.example.com:8924/import/trakt/private'
session = self.client.session
session['state-token'] = {'mode': 'new', 'frequency': 'once', 'time': '14:30', 'redirect_uri': redirect_uri}
session.save()
mock_oauth_callback.return_value = {'refresh_token': 'refresh-token', 'username': 'trakt-user'}
response = self.client.get(reverse('import_trakt_private'), {'code': 'code', 'state': 'state-token'})
self.assertRedirects(response, reverse('import_data'))
mock_oauth_callback.assert_called_once()
self.assertEqual(mock_oauth_callback.call_args.kwargs['redirect_uri'], redirect_uri)
mock_import_trakt.assert_called_once()
self.assertEqual(mock_import_trakt.call_args.kwargs['redirect_uri'], redirect_uri)
```

## Next Steps


---

*Source: test_oauth_views.py:46 | Complexity: Advanced | Last updated: 2026-05-22*