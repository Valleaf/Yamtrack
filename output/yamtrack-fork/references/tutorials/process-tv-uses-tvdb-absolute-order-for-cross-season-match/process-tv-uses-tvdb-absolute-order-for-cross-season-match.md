# How To: Process Tv Uses Tvdb Absolute Order For Cross Season Match

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test webhook anime matching uses TVDB absolute numbering across seasons.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `django.urls`
- `app.models`
- `integrations.webhooks.jellyfin`

**Setup Required:**
```python
# Fixtures: mock_fetch_mapping_data, mock_find_tv_media_id, mock_tvdb_episode, mock_handle_anime
```

## Step-by-Step Guide

### Step 1: 'Test webhook anime matching uses TVDB absolute numbering across seasons.'

```python
'Test webhook anime matching uses TVDB absolute numbering across seasons.'
```

### Step 2: Assign mock_fetch_mapping_data.return_value = value

```python
mock_fetch_mapping_data.return_value = {'2369': {'tvdb_id': 74796, 'tvdb_season': -1, 'tvdb_epoffset': 0, 'mal_id': 269}}
```

### Step 3: Assign mock_find_tv_media_id.return_value = value

```python
mock_find_tv_media_id.return_value = ('1668', 2, 2)
```

### Step 4: Assign mock_tvdb_episode.return_value = value

```python
mock_tvdb_episode.return_value = {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22}
```

### Step 5: Assign payload = value

```python
payload = {'Event': 'Stop', 'Item': {'Type': 'Episode', 'Name': 'Test Episode', 'ProviderIds': {'Tvdb': '12345'}, 'UserData': {'Played': True}, 'SeriesName': 'Bleach', 'ParentIndexNumber': 2, 'IndexNumber': 2}}
```

### Step 6: Call JellyfinWebhookProcessor.process_payload()

```python
JellyfinWebhookProcessor().process_payload(payload, self.user)
```

### Step 7: Call mock_tvdb_episode.assert_called_once_with()

```python
mock_tvdb_episode.assert_called_once_with(12345)
```

### Step 8: Call mock_handle_anime.assert_called_once_with()

```python
mock_handle_anime.assert_called_once_with(269, 22, payload, self.user)
```


## Complete Example

```python
# Setup
# Fixtures: mock_fetch_mapping_data, mock_find_tv_media_id, mock_tvdb_episode, mock_handle_anime

# Workflow
'Test webhook anime matching uses TVDB absolute numbering across seasons.'
mock_fetch_mapping_data.return_value = {'2369': {'tvdb_id': 74796, 'tvdb_season': -1, 'tvdb_epoffset': 0, 'mal_id': 269}}
mock_find_tv_media_id.return_value = ('1668', 2, 2)
mock_tvdb_episode.return_value = {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22}
payload = {'Event': 'Stop', 'Item': {'Type': 'Episode', 'Name': 'Test Episode', 'ProviderIds': {'Tvdb': '12345'}, 'UserData': {'Played': True}, 'SeriesName': 'Bleach', 'ParentIndexNumber': 2, 'IndexNumber': 2}}
JellyfinWebhookProcessor().process_payload(payload, self.user)
mock_tvdb_episode.assert_called_once_with(12345)
mock_handle_anime.assert_called_once_with(269, 22, payload, self.user)
```

## Next Steps


---

*Source: test_webhooks_jellyfin.py:466 | Complexity: Advanced | Last updated: 2026-05-22*