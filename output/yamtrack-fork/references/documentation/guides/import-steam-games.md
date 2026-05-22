# How To: Import Steam Games

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test importing games from Steam.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `pathlib`
- `unittest.mock`
- `django.conf`
- `django.contrib.auth`
- `django.test`
- `requests`
- `requests.exceptions`
- `app.models`
- `integrations.imports`

**Required Fixtures:**
- `api_client` fixture

**Setup Required:**
```python
# Fixtures: mock_get_metadata, mock_external_game, mock_api_request
```

## Step-by-Step Guide

### Step 1: 'Test importing games from Steam.'

```python
'Test importing games from Steam.'
```

### Step 2: Assign mock_api_request.return_value = value

```python
mock_api_request.return_value = {'response': {'games': [{'appid': 730, 'name': 'Counter-Strike 2', 'playtime_forever': 1250, 'playtime_2weeks': 120, 'rtime_last_played': 1704067200}, {'appid': 570, 'name': 'Dota 2', 'playtime_forever': 0, 'playtime_2weeks': 0}, {'appid': 440, 'name': 'Team Fortress 2', 'playtime_forever': 500, 'playtime_2weeks': 0, 'rtime_last_played': 1672531200}]}}
```

### Step 3: Assign mock_external_game.side_effect = value

```python
mock_external_game.side_effect = [1, 2, 3]
```

### Step 4: Assign mock_get_metadata.side_effect = value

```python
mock_get_metadata.side_effect = [{'title': 'Counter-Strike 2', 'image': 'http://example.com/cs2.jpg'}, {'title': 'Dota 2', 'image': 'http://example.com/dota2.jpg'}, {'title': 'Team Fortress 2', 'image': 'http://example.com/tf2.jpg'}]
```

### Step 5: Assign unknown = steam.importer(...)

```python
imported_counts, _ = steam.importer('76561198000000000', self.user, 'new')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(imported_counts[MediaTypes.GAME.value], 3)
```

### Step 7: Assign games = Game.objects.filter(...)

```python
games = Game.objects.filter(user=self.user)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(games.count(), 3)
```

### Step 9: Assign cs2_game = games.get(...)

```python
cs2_game = games.get(item__title='Counter-Strike 2')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(cs2_game.status, Status.IN_PROGRESS.value)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(cs2_game.progress, 1250)
```

### Step 12: Assign dota_game = games.get(...)

```python
dota_game = games.get(item__title='Dota 2')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(dota_game.status, Status.PLANNING.value)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(dota_game.progress, 0)
```

### Step 15: Assign tf2_game = games.get(...)

```python
tf2_game = games.get(item__title='Team Fortress 2')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(tf2_game.status, Status.PAUSED.value)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(tf2_game.progress, 500)
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_metadata, mock_external_game, mock_api_request

# Workflow
'Test importing games from Steam.'
mock_api_request.return_value = {'response': {'games': [{'appid': 730, 'name': 'Counter-Strike 2', 'playtime_forever': 1250, 'playtime_2weeks': 120, 'rtime_last_played': 1704067200}, {'appid': 570, 'name': 'Dota 2', 'playtime_forever': 0, 'playtime_2weeks': 0}, {'appid': 440, 'name': 'Team Fortress 2', 'playtime_forever': 500, 'playtime_2weeks': 0, 'rtime_last_played': 1672531200}]}}
mock_external_game.side_effect = [1, 2, 3]
mock_get_metadata.side_effect = [{'title': 'Counter-Strike 2', 'image': 'http://example.com/cs2.jpg'}, {'title': 'Dota 2', 'image': 'http://example.com/dota2.jpg'}, {'title': 'Team Fortress 2', 'image': 'http://example.com/tf2.jpg'}]
imported_counts, _ = steam.importer('76561198000000000', self.user, 'new')
self.assertEqual(imported_counts[MediaTypes.GAME.value], 3)
games = Game.objects.filter(user=self.user)
self.assertEqual(games.count(), 3)
cs2_game = games.get(item__title='Counter-Strike 2')
self.assertEqual(cs2_game.status, Status.IN_PROGRESS.value)
self.assertEqual(cs2_game.progress, 1250)
dota_game = games.get(item__title='Dota 2')
self.assertEqual(dota_game.status, Status.PLANNING.value)
self.assertEqual(dota_game.progress, 0)
tf2_game = games.get(item__title='Team Fortress 2')
self.assertEqual(tf2_game.status, Status.PAUSED.value)
self.assertEqual(tf2_game.progress, 500)
```

## Next Steps


---

*Source: test_steam.py:38 | Complexity: Advanced | Last updated: 2026-05-22*