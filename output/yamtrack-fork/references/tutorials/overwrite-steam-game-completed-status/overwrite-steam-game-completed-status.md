# How To: Overwrite Steam Game Completed Status

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test overwrite mode does not downgrade completed games.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `app.models`
- `integrations.imports`

**Required Fixtures:**
- `api_client` fixture

**Setup Required:**
```python
# Fixtures: mock_get_metadata, mock_external_game, mock_api_request
```

## Step-by-Step Guide

### Step 1: 'Test overwrite mode does not downgrade completed games.'

```python
'Test overwrite mode does not downgrade completed games.'
```

### Step 2: Call self._setup_mocks()

```python
self._setup_mocks(mock_get_metadata, mock_external_game, mock_api_request, playtime=1100)
```

### Step 3: Assign game = self._create_game(...)

```python
game = self._create_game(status=Status.COMPLETED.value, progress=1000)
```

### Step 4: Assign unknown = steam.importer(...)

```python
imported_counts, _ = steam.importer('76561198000000000', self.user, 'overwrite')
```

### Step 5: Call game.refresh_from_db()

```python
game.refresh_from_db()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(imported_counts[MediaTypes.GAME.value], 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(game.progress, 1100)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(game.status, Status.COMPLETED.value)
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_metadata, mock_external_game, mock_api_request

# Workflow
'Test overwrite mode does not downgrade completed games.'
self._setup_mocks(mock_get_metadata, mock_external_game, mock_api_request, playtime=1100)
game = self._create_game(status=Status.COMPLETED.value, progress=1000)
imported_counts, _ = steam.importer('76561198000000000', self.user, 'overwrite')
game.refresh_from_db()
self.assertEqual(imported_counts[MediaTypes.GAME.value], 1)
self.assertEqual(game.progress, 1100)
self.assertEqual(game.status, Status.COMPLETED.value)
```

## Next Steps


---

*Source: test_steam_update.py:90 | Complexity: Advanced | Last updated: 2026-05-22*