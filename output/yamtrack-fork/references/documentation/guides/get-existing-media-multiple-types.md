# How To: Get Existing Media Multiple Types

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test get_existing_media with different media types.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `collections`
- `django.contrib.auth`
- `django.test`
- `app.models`
- `integrations.imports.helpers`


## Step-by-Step Guide

### Step 1: 'Test get_existing_media with different media types.'

```python
'Test get_existing_media with different media types.'
```

### Step 2: Assign movie_item = Item.objects.create(...)

```python
movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie')
```

### Step 3: Assign movie = Movie.objects.create(...)

```python
movie = Movie.objects.create(item=movie_item, user=self.user)
```

### Step 4: Assign tv_item = Item.objects.create(...)

```python
tv_item = Item.objects.create(media_id='1399', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='TV Show')
```

### Step 5: Assign tv = TV.objects.create(...)

```python
tv = TV.objects.create(item=tv_item, user=self.user)
```

### Step 6: Assign existing = get_existing_media(...)

```python
existing = get_existing_media(self.user)
```

### Step 7: Call self.assertIn()

```python
self.assertIn(MediaTypes.MOVIE.value, existing)
```

### Step 8: Call self.assertIn()

```python
self.assertIn(MediaTypes.TV.value, existing)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(existing[MediaTypes.MOVIE.value][Sources.TMDB.value]), 1)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(existing[MediaTypes.TV.value][Sources.TMDB.value]), 1)
```


## Complete Example

```python
# Workflow
'Test get_existing_media with different media types.'
movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie')
movie = Movie.objects.create(item=movie_item, user=self.user)
tv_item = Item.objects.create(media_id='1399', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='TV Show')
tv = TV.objects.create(item=tv_item, user=self.user)
existing = get_existing_media(self.user)
self.assertIn(MediaTypes.MOVIE.value, existing)
self.assertIn(MediaTypes.TV.value, existing)
self.assertEqual(len(existing[MediaTypes.MOVIE.value][Sources.TMDB.value]), 1)
self.assertEqual(len(existing[MediaTypes.TV.value][Sources.TMDB.value]), 1)
```

## Next Steps


---

*Source: test_import_helpers.py:70 | Complexity: Advanced | Last updated: 2026-05-22*