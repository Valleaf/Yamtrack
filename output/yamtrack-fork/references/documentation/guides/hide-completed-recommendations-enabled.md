# How To: Hide Completed Recommendations Enabled

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that completed items are hidden when preference is enabled.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `datetime`
- `django.contrib.auth`
- `django.http`
- `django.test`
- `django.utils`
- `app.helpers`
- `app.models`


## Step-by-Step Guide

### Step 1: 'Test that completed items are hidden when preference is enabled.'

```python
'Test that completed items are hidden when preference is enabled.'
```

### Step 2: Assign self.user.hide_completed_recommendations = True

```python
self.user.hide_completed_recommendations = True
```

### Step 3: Call self.user.save()

```python
self.user.save()
```

### Step 4: Assign raw_items = value

```python
raw_items = [{'media_id': '238', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Test Movie', 'image': 'http://example.com/movie.jpg'}, {'media_id': '99999', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Unknown Movie', 'image': 'http://example.com/unknown.jpg'}]
```

### Step 5: Assign enriched_items = enrich_items_with_user_data(...)

```python
enriched_items = enrich_items_with_user_data(self.request, raw_items, 'recommendations')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(enriched_items), 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(enriched_items[0]['item']['media_id'], '99999')
```


## Complete Example

```python
# Workflow
'Test that completed items are hidden when preference is enabled.'
self.user.hide_completed_recommendations = True
self.user.save()
raw_items = [{'media_id': '238', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Test Movie', 'image': 'http://example.com/movie.jpg'}, {'media_id': '99999', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Unknown Movie', 'image': 'http://example.com/unknown.jpg'}]
enriched_items = enrich_items_with_user_data(self.request, raw_items, 'recommendations')
self.assertEqual(len(enriched_items), 1)
self.assertEqual(enriched_items[0]['item']['media_id'], '99999')
```

## Next Steps


---

*Source: test_helpers.py:233 | Complexity: Intermediate | Last updated: 2026-05-22*