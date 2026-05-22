# How To: Enrich Items With User Data

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test enriching items with multiple scenarios.

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

### Step 1: 'Test enriching items with multiple scenarios.'

```python
'Test enriching items with multiple scenarios.'
```

### Step 2: Assign raw_items = value

```python
raw_items = [{'media_id': '238', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Test Movie', 'image': 'http://example.com/movie.jpg', 'release_date': '2023-01-01', 'rating': 8.5, 'genre': 'Action'}, {'media_id': '67890', 'source': Sources.TMDB.value, 'media_type': MediaTypes.SEASON.value, 'title': 'Test TV Show', 'season_title': 'Season 1', 'season_number': 1, 'image': 'http://example.com/show.jpg'}, {'media_id': '99999', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Unknown Movie', 'image': 'http://example.com/unknown.jpg', 'description': "This movie doesn't exist in our database"}]
```

### Step 3: Assign enriched_items = enrich_items_with_user_data(...)

```python
enriched_items = enrich_items_with_user_data(self.request, raw_items, 'test')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(len(enriched_items), 3)
```

### Step 5: Assign movie_enriched = value

```python
movie_enriched = enriched_items[0]
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(movie_enriched['media'], self.movie_media)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(movie_enriched['item']['title'], 'Test Movie')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(movie_enriched['item']['media_id'], '238')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(movie_enriched['item']['release_date'], '2023-01-01')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(movie_enriched['item']['rating'], 8.5)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(movie_enriched['item']['genre'], 'Action')
```

### Step 12: Assign season_enriched = value

```python
season_enriched = enriched_items[1]
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(season_enriched['media'], None)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(season_enriched['item']['season_title'], 'Season 1')
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(season_enriched['item']['season_number'], 1)
```

### Step 16: Assign unknown_movie_enriched = value

```python
unknown_movie_enriched = enriched_items[2]
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(unknown_movie_enriched['item']['media_id'], raw_items[2]['media_id'])
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(unknown_movie_enriched['media'], None)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(unknown_movie_enriched['item']['title'], 'Unknown Movie')
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(unknown_movie_enriched['item']['media_id'], '99999')
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(unknown_movie_enriched['item']['description'], "This movie doesn't exist in our database")
```


## Complete Example

```python
# Workflow
'Test enriching items with multiple scenarios.'
raw_items = [{'media_id': '238', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Test Movie', 'image': 'http://example.com/movie.jpg', 'release_date': '2023-01-01', 'rating': 8.5, 'genre': 'Action'}, {'media_id': '67890', 'source': Sources.TMDB.value, 'media_type': MediaTypes.SEASON.value, 'title': 'Test TV Show', 'season_title': 'Season 1', 'season_number': 1, 'image': 'http://example.com/show.jpg'}, {'media_id': '99999', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Unknown Movie', 'image': 'http://example.com/unknown.jpg', 'description': "This movie doesn't exist in our database"}]
enriched_items = enrich_items_with_user_data(self.request, raw_items, 'test')
self.assertEqual(len(enriched_items), 3)
movie_enriched = enriched_items[0]
self.assertEqual(movie_enriched['media'], self.movie_media)
self.assertEqual(movie_enriched['item']['title'], 'Test Movie')
self.assertEqual(movie_enriched['item']['media_id'], '238')
self.assertEqual(movie_enriched['item']['release_date'], '2023-01-01')
self.assertEqual(movie_enriched['item']['rating'], 8.5)
self.assertEqual(movie_enriched['item']['genre'], 'Action')
season_enriched = enriched_items[1]
self.assertEqual(season_enriched['media'], None)
self.assertEqual(season_enriched['item']['season_title'], 'Season 1')
self.assertEqual(season_enriched['item']['season_number'], 1)
unknown_movie_enriched = enriched_items[2]
self.assertEqual(unknown_movie_enriched['item']['media_id'], raw_items[2]['media_id'])
self.assertEqual(unknown_movie_enriched['media'], None)
self.assertEqual(unknown_movie_enriched['item']['title'], 'Unknown Movie')
self.assertEqual(unknown_movie_enriched['item']['media_id'], '99999')
self.assertEqual(unknown_movie_enriched['item']['description'], "This movie doesn't exist in our database")
```

## Next Steps


---

*Source: test_helpers.py:159 | Complexity: Advanced | Last updated: 2026-05-22*