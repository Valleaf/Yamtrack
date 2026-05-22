# How To: Integrations Uses Configured Webhook Urls

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test copied webhook URLs use the configured public app URL.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `django.contrib.auth`
- `django.contrib.messages`
- `django.db`
- `django.test`
- `django.urls`


## Step-by-Step Guide

### Step 1: 'Test copied webhook URLs use the configured public app URL.'

```python
'Test copied webhook URLs use the configured public app URL.'
```

### Step 2: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('integrations'))
```

### Step 3: Call self.assertContains()

```python
self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/jellyfin/initial_token')
```

### Step 4: Call self.assertContains()

```python
self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/plex/initial_token')
```

### Step 5: Call self.assertContains()

```python
self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/emby/initial_token')
```


## Complete Example

```python
# Workflow
'Test copied webhook URLs use the configured public app URL.'
response = self.client.get(reverse('integrations'))
self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/jellyfin/initial_token')
self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/plex/initial_token')
self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/emby/initial_token')
```

## Next Steps


---

*Source: test_token.py:53 | Complexity: Intermediate | Last updated: 2026-05-22*