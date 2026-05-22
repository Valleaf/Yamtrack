# How To: Process Watched Episode

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test processing an episode entry.

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
# Fixtures: mock_get_metadata
```

## Step-by-Step Guide

### Step 1: 'Test processing an episode entry.'

```python
'Test processing an episode entry.'
```

### Step 2: Assign episode_entry = value

```python
episode_entry = {'type': 'episode', 'episode': {'season': 1, 'number': 1, 'title': 'Pilot'}, 'show': {'title': 'Test Show', 'ids': {'tmdb': 12345}}, 'watched_at': '2023-01-01T00:00:00.000Z'}
```

### Step 3: Assign mock_get_metadata.side_effect = mock_metadata_side_effect

```python
mock_get_metadata.side_effect = mock_metadata_side_effect
```

### Step 4: Assign trakt_importer = TraktImporter(...)

```python
trakt_importer = TraktImporter('testuser', self.user, 'new')
```

### Step 5: Call trakt_importer.process_watched_episode()

```python
trakt_importer.process_watched_episode(episode_entry)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.TV.value]), 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.SEASON.value]), 1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.EPISODE.value]), 1)
```

### Step 9: Call trakt_importer.process_watched_episode()

```python
trakt_importer.process_watched_episode(episode_entry)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.EPISODE.value]), 2)
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_metadata

# Workflow
'Test processing an episode entry.'
episode_entry = {'type': 'episode', 'episode': {'season': 1, 'number': 1, 'title': 'Pilot'}, 'show': {'title': 'Test Show', 'ids': {'tmdb': 12345}}, 'watched_at': '2023-01-01T00:00:00.000Z'}

def mock_metadata_side_effect(media_type, _, __, ___=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Test Show', 'image': 'tv_image.jpg', 'last_episode_season': 1, 'max_progress': 1}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Season 1', 'image': 'season_image.jpg', 'episodes': [{'episode_number': 1, 'still_path': '/still.jpg'}], 'max_progress': 1}
    return None
mock_get_metadata.side_effect = mock_metadata_side_effect
trakt_importer = TraktImporter('testuser', self.user, 'new')
trakt_importer.process_watched_episode(episode_entry)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.TV.value]), 1)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.SEASON.value]), 1)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.EPISODE.value]), 1)
trakt_importer.process_watched_episode(episode_entry)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.EPISODE.value]), 2)
```

## Next Steps


---

*Source: test_trakt.py:60 | Complexity: Advanced | Last updated: 2026-05-22*