# How To: Determine Game Status Logic

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the status determination logic.

## Prerequisites

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


## Step-by-Step Guide

### Step 1: 'Test the status determination logic.'

```python
'Test the status determination logic.'
```

### Step 2: Assign importer_instance = steam.SteamImporter(...)

```python
importer_instance = steam.SteamImporter('76561198000000000', self.user, 'new')
```

### Step 3: Assign status = importer_instance._determine_game_status(...)

```python
status = importer_instance._determine_game_status(0, 0)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(status, Status.PLANNING.value)
```

### Step 5: Assign status = importer_instance._determine_game_status(...)

```python
status = importer_instance._determine_game_status(100, 50)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(status, Status.IN_PROGRESS.value)
```

### Step 7: Assign status = importer_instance._determine_game_status(...)

```python
status = importer_instance._determine_game_status(100, 0)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(status, Status.PAUSED.value)
```

### Step 9: Assign status = importer_instance._determine_game_status(...)

```python
status = importer_instance._determine_game_status(100, 0)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(status, Status.PAUSED.value)
```


## Complete Example

```python
# Workflow
'Test the status determination logic.'
importer_instance = steam.SteamImporter('76561198000000000', self.user, 'new')
status = importer_instance._determine_game_status(0, 0)
self.assertEqual(status, Status.PLANNING.value)
status = importer_instance._determine_game_status(100, 50)
self.assertEqual(status, Status.IN_PROGRESS.value)
status = importer_instance._determine_game_status(100, 0)
self.assertEqual(status, Status.PAUSED.value)
status = importer_instance._determine_game_status(100, 0)
self.assertEqual(status, Status.PAUSED.value)
```

## Next Steps


---

*Source: test_steam.py:151 | Complexity: Advanced | Last updated: 2026-05-22*