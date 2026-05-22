# How To: Home View Includes In Progress Tv With Unwatched Seasons

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test in-progress TV with unwatched seasons appears on home.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `django.urls`
- `django.utils`
- `app.models`
- `users.models`


## Step-by-Step Guide

### Step 1: 'Test in-progress TV with unwatched seasons appears on home.'

```python
'Test in-progress TV with unwatched seasons appears on home.'
```

### Step 2: Assign tv_item = Item.objects.create(...)

```python
tv_item = Item.objects.create(media_id='tv-with-new-season', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Returning Show', image='http://example.com/returning-show.jpg')
```

### Step 3: Assign tv = TV.objects.create(...)

```python
tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
```

### Step 4: Assign unwatched_season_item = Item.objects.create(...)

```python
unwatched_season_item = Item.objects.create(media_id='tv-with-new-season', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Returning Show', image='http://example.com/returning-show.jpg', season_number=2)
```

### Step 5: Call Season.objects.create()

```python
Season.objects.create(item=unwatched_season_item, user=self.user, related_tv=tv, status=Status.PLANNING.value)
```

### Step 6: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('home'))
```

### Step 7: Assign sections_by_key = value

```python
sections_by_key = {section['key']: section for section in response.context['home_sections']}
```

### Step 8: Assign in_progress_section = value

```python
in_progress_section = sections_by_key[Status.IN_PROGRESS.value]
```

### Step 9: Call self.assertIn()

```python
self.assertIn(MediaTypes.TV.value, in_progress_section['media_types'])
```

### Step 10: Assign tv_media = value

```python
tv_media = in_progress_section['media_types'][MediaTypes.TV.value]
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(tv_media['total'], 1)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(tv_media['items'][0].item.title, 'Returning Show')
```


## Complete Example

```python
# Workflow
'Test in-progress TV with unwatched seasons appears on home.'
tv_item = Item.objects.create(media_id='tv-with-new-season', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Returning Show', image='http://example.com/returning-show.jpg')
tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
unwatched_season_item = Item.objects.create(media_id='tv-with-new-season', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Returning Show', image='http://example.com/returning-show.jpg', season_number=2)
Season.objects.create(item=unwatched_season_item, user=self.user, related_tv=tv, status=Status.PLANNING.value)
response = self.client.get(reverse('home'))
sections_by_key = {section['key']: section for section in response.context['home_sections']}
in_progress_section = sections_by_key[Status.IN_PROGRESS.value]
self.assertIn(MediaTypes.TV.value, in_progress_section['media_types'])
tv_media = in_progress_section['media_types'][MediaTypes.TV.value]
self.assertEqual(tv_media['total'], 1)
self.assertEqual(tv_media['items'][0].item.title, 'Returning Show')
```

## Next Steps


---

*Source: test_home.py:195 | Complexity: Advanced | Last updated: 2026-05-22*