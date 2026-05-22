# How To: Update Episode References

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test updating episode references with actual Season instances.

## Prerequisites

**Required Modules:**
- `pathlib`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `django_celery_beat.models`
- `app.models`
- `integrations.imports`


## Step-by-Step Guide

### Step 1: 'Test updating episode references with actual Season instances.'

```python
'Test updating episode references with actual Season instances.'
```

### Step 2: Assign tv_item = Item.objects.create(...)

```python
tv_item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show')
```

### Step 3: Assign tv = TV.objects.create(...)

```python
tv = TV.objects.create(item=tv_item, user=self.user, status=Status.PLANNING.value)
```

### Step 4: Assign season_item = Item.objects.create(...)

```python
season_item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', season_number=1)
```

### Step 5: Assign season = Season.objects.create(...)

```python
season = Season.objects.create(item=season_item, user=self.user, related_tv=tv, status=Status.PLANNING.value)
```

### Step 6: Assign episode_item = Item.objects.create(...)

```python
episode_item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Show', season_number=1, episode_number=1)
```

### Step 7: Assign new_episode = Episode(...)

```python
new_episode = Episode(item=episode_item, related_season=Season(item=season_item, related_tv=tv, user=self.user))
```

### Step 8: Call helpers.update_episode_references()

```python
helpers.update_episode_references([new_episode], self.user)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(new_episode.related_season.id, season.id)
```


## Complete Example

```python
# Workflow
'Test updating episode references with actual Season instances.'
tv_item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show')
tv = TV.objects.create(item=tv_item, user=self.user, status=Status.PLANNING.value)
season_item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', season_number=1)
season = Season.objects.create(item=season_item, user=self.user, related_tv=tv, status=Status.PLANNING.value)
episode_item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Show', season_number=1, episode_number=1)
new_episode = Episode(item=episode_item, related_season=Season(item=season_item, related_tv=tv, user=self.user))
helpers.update_episode_references([new_episode], self.user)
self.assertEqual(new_episode.related_season.id, season.id)
```

## Next Steps


---

*Source: test_helpers.py:59 | Complexity: Advanced | Last updated: 2026-05-22*