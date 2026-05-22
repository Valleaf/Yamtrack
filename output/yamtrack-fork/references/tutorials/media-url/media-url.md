# How To: Media Url

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the media_url filter.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `django.test`
- `django.urls`
- `django.utils`
- `app.models`
- `app.templatetags`


## Step-by-Step Guide

### Step 1: 'Test the media_url filter.'

```python
'Test the media_url filter.'
```

### Step 2: Assign tv_url = app_tags.media_url(...)

```python
tv_url = app_tags.media_url(self.tv_item)
```

### Step 3: Assign expected_tv_url = reverse(...)

```python
expected_tv_url = reverse('media_details', kwargs={'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'media_id': '1668', 'title': 'test-tv-show'})
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(tv_url, expected_tv_url)
```

### Step 5: Assign tv_dict_url = app_tags.media_url(...)

```python
tv_dict_url = app_tags.media_url(self.tv_dict)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(tv_dict_url, expected_tv_url)
```

### Step 7: Assign season_url = app_tags.media_url(...)

```python
season_url = app_tags.media_url(self.season_item)
```

### Step 8: Assign expected_season_url = reverse(...)

```python
expected_season_url = reverse('season_details', kwargs={'source': Sources.TMDB.value, 'media_id': '1668', 'title': 'test-tv-show', 'season_number': 1})
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(season_url, expected_season_url)
```

### Step 10: Assign season_dict_url = app_tags.media_url(...)

```python
season_dict_url = app_tags.media_url(self.season_dict)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(season_dict_url, expected_season_url)
```


## Complete Example

```python
# Workflow
'Test the media_url filter.'
tv_url = app_tags.media_url(self.tv_item)
expected_tv_url = reverse('media_details', kwargs={'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'media_id': '1668', 'title': 'test-tv-show'})
self.assertEqual(tv_url, expected_tv_url)
tv_dict_url = app_tags.media_url(self.tv_dict)
self.assertEqual(tv_dict_url, expected_tv_url)
season_url = app_tags.media_url(self.season_item)
expected_season_url = reverse('season_details', kwargs={'source': Sources.TMDB.value, 'media_id': '1668', 'title': 'test-tv-show', 'season_number': 1})
self.assertEqual(season_url, expected_season_url)
season_dict_url = app_tags.media_url(self.season_dict)
self.assertEqual(season_dict_url, expected_season_url)
```

## Next Steps


---

*Source: test_templatetags.py:285 | Complexity: Advanced | Last updated: 2026-05-22*