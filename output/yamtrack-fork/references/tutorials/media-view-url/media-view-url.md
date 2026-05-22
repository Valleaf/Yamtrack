# How To: Media View Url

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the media_view_url tag.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `django.test`
- `django.urls`
- `django.utils`
- `app.models`
- `app.templatetags`


## Step-by-Step Guide

### Step 1: 'Test the media_view_url tag.'

```python
'Test the media_view_url tag.'
```

### Step 2: Assign tv_modal = app_tags.media_view_url(...)

```python
tv_modal = app_tags.media_view_url('track_modal', self.tv_item)
```

### Step 3: Assign expected_tv_modal = reverse(...)

```python
expected_tv_modal = reverse('track_modal', kwargs={'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'media_id': '1668'})
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(tv_modal, expected_tv_modal)
```

### Step 5: Assign tv_dict_modal = app_tags.media_view_url(...)

```python
tv_dict_modal = app_tags.media_view_url('track_modal', self.tv_dict)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(tv_dict_modal, expected_tv_modal)
```

### Step 7: Assign episode_modal = app_tags.media_view_url(...)

```python
episode_modal = app_tags.media_view_url('history_modal', self.episode_item)
```

### Step 8: Assign expected_episode_modal = reverse(...)

```python
expected_episode_modal = reverse('history_modal', kwargs={'source': Sources.TMDB.value, 'media_type': MediaTypes.EPISODE.value, 'media_id': '1668', 'season_number': 1, 'episode_number': 1})
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(episode_modal, expected_episode_modal)
```

### Step 10: Assign episode_dict_modal = app_tags.media_view_url(...)

```python
episode_dict_modal = app_tags.media_view_url('history_modal', self.episode_dict)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(episode_dict_modal, expected_episode_modal)
```


## Complete Example

```python
# Workflow
'Test the media_view_url tag.'
tv_modal = app_tags.media_view_url('track_modal', self.tv_item)
expected_tv_modal = reverse('track_modal', kwargs={'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'media_id': '1668'})
self.assertEqual(tv_modal, expected_tv_modal)
tv_dict_modal = app_tags.media_view_url('track_modal', self.tv_dict)
self.assertEqual(tv_dict_modal, expected_tv_modal)
episode_modal = app_tags.media_view_url('history_modal', self.episode_item)
expected_episode_modal = reverse('history_modal', kwargs={'source': Sources.TMDB.value, 'media_type': MediaTypes.EPISODE.value, 'media_id': '1668', 'season_number': 1, 'episode_number': 1})
self.assertEqual(episode_modal, expected_episode_modal)
episode_dict_modal = app_tags.media_view_url('history_modal', self.episode_dict)
self.assertEqual(episode_dict_modal, expected_episode_modal)
```

## Next Steps


---

*Source: test_templatetags.py:347 | Complexity: Advanced | Last updated: 2026-05-22*