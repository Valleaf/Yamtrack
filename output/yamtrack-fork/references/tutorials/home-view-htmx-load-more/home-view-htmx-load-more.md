# How To: Home View Htmx Load More

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test the HTMX load more functionality.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `django.urls`
- `django.utils`
- `app.models`
- `users.models`

**Setup Required:**
```python
# Fixtures: mock_get_media_metadata
```

## Step-by-Step Guide

### Step 1: 'Test the HTMX load more functionality.'

```python
'Test the HTMX load more functionality.'
```

### Step 2: Assign mock_get_media_metadata.return_value = value

```python
mock_get_media_metadata.return_value = {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'season/1': {'episodes': [{'id': 1}, {'id': 2}, {'id': 3}]}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
```

### Step 3: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('home') + '?load_media_type=season', headers={'hx-request': 'true'})
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 5: Call self.assertTemplateUsed()

```python
self.assertTemplateUsed(response, 'app/components/home_grid.html')
```

### Step 6: Call self.assertIn()

```python
self.assertIn('media_list', response.context)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(response.context['home_status'], Status.IN_PROGRESS.value)
```

### Step 8: Call self.assertIn()

```python
self.assertIn('items', response.context['media_list'])
```

### Step 9: Call self.assertIn()

```python
self.assertIn('total', response.context['media_list'])
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(response.context['media_list']['items']), 1)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(response.context['media_list']['total'], 15)
```

### Step 12: Assign season_item = Item.objects.create(...)

```python
season_item = Item.objects.create(media_id=str(i), source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title=f'Test TV Show {i}', image='http://example.com/image.jpg', season_number=1)
```

### Step 13: Assign season = Season.objects.create(...)

```python
season = Season.objects.create(item=season_item, user=self.user, status=Status.IN_PROGRESS.value)
```

### Step 14: Assign episode_item = Item.objects.create(...)

```python
episode_item = Item.objects.create(media_id=str(i), source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Test TV Show {i}', image='http://example.com/image.jpg', season_number=1, episode_number=1)
```

### Step 15: Call Episode.objects.create()

```python
Episode.objects.create(item=episode_item, related_season=season, end_date=timezone.now())
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_media_metadata

# Workflow
'Test the HTMX load more functionality.'
mock_get_media_metadata.return_value = {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'season/1': {'episodes': [{'id': 1}, {'id': 2}, {'id': 3}]}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
for i in range(6, 20):
    season_item = Item.objects.create(media_id=str(i), source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title=f'Test TV Show {i}', image='http://example.com/image.jpg', season_number=1)
    season = Season.objects.create(item=season_item, user=self.user, status=Status.IN_PROGRESS.value)
    episode_item = Item.objects.create(media_id=str(i), source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Test TV Show {i}', image='http://example.com/image.jpg', season_number=1, episode_number=1)
    Episode.objects.create(item=episode_item, related_season=season, end_date=timezone.now())
response = self.client.get(reverse('home') + '?load_media_type=season', headers={'hx-request': 'true'})
self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/components/home_grid.html')
self.assertIn('media_list', response.context)
self.assertEqual(response.context['home_status'], Status.IN_PROGRESS.value)
self.assertIn('items', response.context['media_list'])
self.assertIn('total', response.context['media_list'])
self.assertEqual(len(response.context['media_list']['items']), 1)
self.assertEqual(response.context['media_list']['total'], 15)
```

## Next Steps


---

*Source: test_home.py:248 | Complexity: Advanced | Last updated: 2026-05-22*