# How To: Hide Completed Recommendations Disabled

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that completed items are shown when preference is disabled.

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

### Step 1: 'Test that completed items are shown when preference is disabled.'

```python
'Test that completed items are shown when preference is disabled.'
```

### Step 2: Assign self.user.hide_completed_recommendations = False

```python
self.user.hide_completed_recommendations = False
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
self.assertEqual(len(enriched_items), 2)
```


## Complete Example

```python
# Workflow
'Test that completed items are shown when preference is disabled.'
self.user.hide_completed_recommendations = False
self.user.save()
raw_items = [{'media_id': '238', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Test Movie', 'image': 'http://example.com/movie.jpg'}, {'media_id': '99999', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Unknown Movie', 'image': 'http://example.com/unknown.jpg'}]
enriched_items = enrich_items_with_user_data(self.request, raw_items, 'recommendations')
self.assertEqual(len(enriched_items), 2)
```

## Next Steps


---

*Source: test_helpers.py:262 | Complexity: Intermediate | Last updated: 2026-05-22*