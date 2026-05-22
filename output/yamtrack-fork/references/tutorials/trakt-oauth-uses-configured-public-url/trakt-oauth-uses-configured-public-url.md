# How To: Trakt Oauth Uses Configured Public Url

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test Trakt authorization uses the configured public URL.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `urllib.parse`
- `django.contrib.auth`
- `django.test`
- `django.urls`


## Step-by-Step Guide

### Step 1: 'Test Trakt authorization uses the configured public URL.'

```python
'Test Trakt authorization uses the configured public URL.'
```

### Step 2: Assign response = self.client.post(...)

```python
response = self.client.post(reverse('trakt_oauth'), {'mode': 'new', 'frequency': 'once', 'time': '14:30'})
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 302)
```

### Step 4: Assign redirect = urlparse(...)

```python
redirect = urlparse(response['Location'])
```

### Step 5: Assign query = parse_qs(...)

```python
query = parse_qs(redirect.query)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(redirect.scheme, 'https')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(redirect.netloc, 'trakt.tv')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(query['client_id'], ['client'])
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(query['redirect_uri'], ['https://yamtrack.example.com:8924/import/trakt/private'])
```

### Step 10: Assign state = value

```python
state = self.client.session[query['state'][0]]
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(state['redirect_uri'], 'https://yamtrack.example.com:8924/import/trakt/private')
```


## Complete Example

```python
# Workflow
'Test Trakt authorization uses the configured public URL.'
response = self.client.post(reverse('trakt_oauth'), {'mode': 'new', 'frequency': 'once', 'time': '14:30'})
self.assertEqual(response.status_code, 302)
redirect = urlparse(response['Location'])
query = parse_qs(redirect.query)
self.assertEqual(redirect.scheme, 'https')
self.assertEqual(redirect.netloc, 'trakt.tv')
self.assertEqual(query['client_id'], ['client'])
self.assertEqual(query['redirect_uri'], ['https://yamtrack.example.com:8924/import/trakt/private'])
state = self.client.session[query['state'][0]]
self.assertEqual(state['redirect_uri'], 'https://yamtrack.example.com:8924/import/trakt/private')
```

## Next Steps


---

*Source: test_oauth_views.py:19 | Complexity: Advanced | Last updated: 2026-05-22*