# How To: Create Entry Post Episode

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test creating an episode entry with parent season.

## Prerequisites

**Required Modules:**
- `django.contrib.auth`
- `django.db`
- `django.test`
- `django.urls`
- `django.utils`
- `app.models`


## Step-by-Step Guide

### Step 1: 'Test creating an episode entry with parent season.'

```python
'Test creating an episode entry with parent season.'
```

### Step 2: Assign tv_item = Item.objects.create(...)

```python
tv_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='TV Show')
```

### Step 3: Assign parent_tv = TV.objects.create(...)

```python
parent_tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
```

### Step 4: Assign season_item = Item.objects.create(...)

```python
season_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='TV Show', season_number=1)
```

### Step 5: Assign parent_season = Season.objects.create(...)

```python
parent_season = Season.objects.create(item=season_item, user=self.user, related_tv=parent_tv, status=Status.IN_PROGRESS.value)
```

### Step 6: Assign form_data = value

```python
form_data = {'title': 'TV Show', 'media_type': MediaTypes.EPISODE.value, 'season_number': 1, 'episode_number': 1, 'parent_season': parent_season.id, 'end_date': '2023-01-02T00:00'}
```

### Step 7: Assign response = self.client.post(...)

```python
response = self.client.post(reverse('create_entry'), form_data, follow=True)
```

### Step 8: Call self.assertRedirects()

```python
self.assertRedirects(response, reverse('create_entry'))
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(Item.objects.filter(title='TV Show', media_type=MediaTypes.EPISODE.value, season_number=1, episode_number=1).exists())
```

### Step 10: Assign episode = Episode.objects.get(...)

```python
episode = Episode.objects.get(item__title='TV Show')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(episode.related_season, parent_season)
```

### Step 12: Assign end_date_local = timezone.localtime(...)

```python
end_date_local = timezone.localtime(episode.end_date)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(end_date_local.strftime('%Y-%m-%d %H:%M'), '2023-01-02 00:00')
```


## Complete Example

```python
# Workflow
'Test creating an episode entry with parent season.'
tv_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='TV Show')
parent_tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
season_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='TV Show', season_number=1)
parent_season = Season.objects.create(item=season_item, user=self.user, related_tv=parent_tv, status=Status.IN_PROGRESS.value)
form_data = {'title': 'TV Show', 'media_type': MediaTypes.EPISODE.value, 'season_number': 1, 'episode_number': 1, 'parent_season': parent_season.id, 'end_date': '2023-01-02T00:00'}
response = self.client.post(reverse('create_entry'), form_data, follow=True)
self.assertRedirects(response, reverse('create_entry'))
self.assertTrue(Item.objects.filter(title='TV Show', media_type=MediaTypes.EPISODE.value, season_number=1, episode_number=1).exists())
episode = Episode.objects.get(item__title='TV Show')
self.assertEqual(episode.related_season, parent_season)
end_date_local = timezone.localtime(episode.end_date)
self.assertEqual(end_date_local.strftime('%Y-%m-%d %H:%M'), '2023-01-02 00:00')
```

## Next Steps


---

*Source: test_entry.py:133 | Complexity: Advanced | Last updated: 2026-05-22*