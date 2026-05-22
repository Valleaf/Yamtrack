# How To: Episode Queries Episode Endpoint

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test TVDB episode lookup returns normalized episode metadata.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest.mock`
- `django.test`
- `app.providers`

**Required Fixtures:**
- `api_client` fixture

**Setup Required:**
```python
# Fixtures: mock_api_request, mock_get_access_token, mock_cache
```

## Step-by-Step Guide

### Step 1: 'Test TVDB episode lookup returns normalized episode metadata.'

```python
'Test TVDB episode lookup returns normalized episode metadata.'
```

### Step 2: Assign mock_cache.get.return_value = None

```python
mock_cache.get.return_value = None
```

### Step 3: Assign mock_get_access_token.return_value = 'test-token'

```python
mock_get_access_token.return_value = 'test-token'
```

### Step 4: Assign mock_api_request.return_value = value

```python
mock_api_request.return_value = {'data': {'id': 12345, 'seriesId': 74796, 'seasonNumber': 2, 'number': 2, 'absoluteNumber': 22}}
```

### Step 5: Assign result = tvdb.episode(...)

```python
result = tvdb.episode(12345)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(result, {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})
```

### Step 7: Call mock_api_request.assert_called_once_with()

```python
mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'GET', f'{tvdb.BASE_URL}/episodes/12345', headers={'Authorization': 'Bearer test-token'})
```

### Step 8: Call mock_cache.set.assert_called_once_with()

```python
mock_cache.set.assert_called_once_with('tvdb_episode_12345', {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})
```


## Complete Example

```python
# Setup
# Fixtures: mock_api_request, mock_get_access_token, mock_cache

# Workflow
'Test TVDB episode lookup returns normalized episode metadata.'
mock_cache.get.return_value = None
mock_get_access_token.return_value = 'test-token'
mock_api_request.return_value = {'data': {'id': 12345, 'seriesId': 74796, 'seasonNumber': 2, 'number': 2, 'absoluteNumber': 22}}
result = tvdb.episode(12345)
self.assertEqual(result, {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})
mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'GET', f'{tvdb.BASE_URL}/episodes/12345', headers={'Authorization': 'Bearer test-token'})
mock_cache.set.assert_called_once_with('tvdb_episode_12345', {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})
```

## Next Steps


---

*Source: test_tvdb.py:45 | Complexity: Advanced | Last updated: 2026-05-22*