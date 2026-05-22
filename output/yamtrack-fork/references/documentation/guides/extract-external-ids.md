# How To: Extract External Ids

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test extracting external IDs from provider payload.

## Prerequisites

**Required Modules:**
- `json`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `django.urls`
- `app.models`
- `integrations.webhooks.jellyfin`


## Step-by-Step Guide

### Step 1: 'Test extracting external IDs from provider payload.'

```python
'Test extracting external IDs from provider payload.'
```

### Step 2: Assign payload = value

```python
payload = {'Event': 'Stop', 'Item': {'Type': 'Movie', 'Name': 'The Matrix', 'ProductionYear': 1999, 'ProviderIds': {'Tmdb': '603', 'Tvdb': '169'}}}
```

### Step 3: Assign expected = value

```python
expected = {'tmdb_id': '603', 'imdb_id': None, 'tvdb_id': '169'}
```

### Step 4: Assign result = JellyfinWebhookProcessor._extract_external_ids(...)

```python
result = JellyfinWebhookProcessor()._extract_external_ids(payload)
```

### Step 5: Assign msg = value

```python
msg = f'Expected {expected}, got {result}'
```


## Complete Example

```python
# Workflow
'Test extracting external IDs from provider payload.'
payload = {'Event': 'Stop', 'Item': {'Type': 'Movie', 'Name': 'The Matrix', 'ProductionYear': 1999, 'ProviderIds': {'Tmdb': '603', 'Tvdb': '169'}}}
expected = {'tmdb_id': '603', 'imdb_id': None, 'tvdb_id': '169'}
result = JellyfinWebhookProcessor()._extract_external_ids(payload)
if result != expected:
    msg = f'Expected {expected}, got {result}'
    raise AssertionError(msg)
```

## Next Steps


---

*Source: test_webhooks_jellyfin.py:268 | Complexity: Intermediate | Last updated: 2026-05-22*