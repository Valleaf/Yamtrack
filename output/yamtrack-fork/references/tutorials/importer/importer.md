# How To: Importer

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test importing media from SIMKL.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `pathlib`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `app.models`
- `integrations.imports`

**Setup Required:**
```python
# Fixtures: user_list
```

## Step-by-Step Guide

### Step 1: 'Test importing media from SIMKL.'

```python
'Test importing media from SIMKL.'
```

### Step 2: Assign user_list.return_value = value

```python
user_list.return_value = {'shows': [{'last_watched_at': '2023-01-02T00:00:00Z', 'show': {'title': 'Breaking Bad', 'ids': {'tmdb': 1396}}, 'status': 'watching', 'user_rating': 8, 'seasons': [{'number': 1, 'episodes': [{'number': 1}, {'number': 2, 'watched_at': '2023-01-02T00:00:00Z'}]}], 'memo': {}}], 'movies': [{'added_to_watchlist_at': '2023-01-01T00:00:00Z', 'movie': {'title': 'Perfect Blue', 'ids': {'tmdb': 10494}}, 'status': 'completed', 'user_rating': 9, 'last_watched_at': '2023-02-01T00:00:00Z', 'memo': {}}], 'anime': [{'added_to_watchlist_at': '2023-01-01T00:00:00Z', 'show': {'title': 'Example Anime', 'ids': {'mal': 1}}, 'status': 'plantowatch', 'user_rating': 7, 'watched_episodes_count': 0, 'last_watched_at': None, 'memo': {'text': 'Great series!'}}]}
```

### Step 3: Assign unknown = self.importer.import_data(...)

```python
imported_counts, warnings = self.importer.import_data()
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(imported_counts[MediaTypes.TV.value], 1)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(imported_counts[MediaTypes.MOVIE.value], 1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(imported_counts[MediaTypes.ANIME.value], 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(warnings, '')
```

### Step 8: Assign tv_item = Item.objects.get(...)

```python
tv_item = Item.objects.get(media_type=MediaTypes.TV.value)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(tv_item.title, 'Breaking Bad')
```

### Step 10: Assign tv_obj = TV.objects.get(...)

```python
tv_obj = TV.objects.get(item=tv_item)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(tv_obj.status, Status.IN_PROGRESS.value)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(tv_obj.score, 8)
```

### Step 13: Assign movie_item = Item.objects.get(...)

```python
movie_item = Item.objects.get(media_type=MediaTypes.MOVIE.value)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(movie_item.title, 'Perfect Blue')
```

### Step 15: Assign movie_obj = Movie.objects.get(...)

```python
movie_obj = Movie.objects.get(item=movie_item)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(movie_obj.status, Status.COMPLETED.value)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(movie_obj.score, 9)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(movie_obj.progress, 1)
```

### Step 19: Assign anime_item = Item.objects.get(...)

```python
anime_item = Item.objects.get(media_type=MediaTypes.ANIME.value)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(anime_item.title, 'Cowboy Bebop')
```

### Step 21: Assign anime_obj = Anime.objects.get(...)

```python
anime_obj = Anime.objects.get(item=anime_item)
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(anime_obj.status, Status.PLANNING.value)
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(anime_obj.score, 7)
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(anime_obj.notes, 'Great series!')
```


## Complete Example

```python
# Setup
# Fixtures: user_list

# Workflow
'Test importing media from SIMKL.'
user_list.return_value = {'shows': [{'last_watched_at': '2023-01-02T00:00:00Z', 'show': {'title': 'Breaking Bad', 'ids': {'tmdb': 1396}}, 'status': 'watching', 'user_rating': 8, 'seasons': [{'number': 1, 'episodes': [{'number': 1}, {'number': 2, 'watched_at': '2023-01-02T00:00:00Z'}]}], 'memo': {}}], 'movies': [{'added_to_watchlist_at': '2023-01-01T00:00:00Z', 'movie': {'title': 'Perfect Blue', 'ids': {'tmdb': 10494}}, 'status': 'completed', 'user_rating': 9, 'last_watched_at': '2023-02-01T00:00:00Z', 'memo': {}}], 'anime': [{'added_to_watchlist_at': '2023-01-01T00:00:00Z', 'show': {'title': 'Example Anime', 'ids': {'mal': 1}}, 'status': 'plantowatch', 'user_rating': 7, 'watched_episodes_count': 0, 'last_watched_at': None, 'memo': {'text': 'Great series!'}}]}
imported_counts, warnings = self.importer.import_data()
self.assertEqual(imported_counts[MediaTypes.TV.value], 1)
self.assertEqual(imported_counts[MediaTypes.MOVIE.value], 1)
self.assertEqual(imported_counts[MediaTypes.ANIME.value], 1)
self.assertEqual(warnings, '')
tv_item = Item.objects.get(media_type=MediaTypes.TV.value)
self.assertEqual(tv_item.title, 'Breaking Bad')
tv_obj = TV.objects.get(item=tv_item)
self.assertEqual(tv_obj.status, Status.IN_PROGRESS.value)
self.assertEqual(tv_obj.score, 8)
movie_item = Item.objects.get(media_type=MediaTypes.MOVIE.value)
self.assertEqual(movie_item.title, 'Perfect Blue')
movie_obj = Movie.objects.get(item=movie_item)
self.assertEqual(movie_obj.status, Status.COMPLETED.value)
self.assertEqual(movie_obj.score, 9)
self.assertEqual(movie_obj.progress, 1)
anime_item = Item.objects.get(media_type=MediaTypes.ANIME.value)
self.assertEqual(anime_item.title, 'Cowboy Bebop')
anime_obj = Anime.objects.get(item=anime_item)
self.assertEqual(anime_obj.status, Status.PLANNING.value)
self.assertEqual(anime_obj.score, 7)
self.assertEqual(anime_obj.notes, 'Great series!')
```

## Next Steps


---

*Source: test_simkl.py:43 | Complexity: Advanced | Last updated: 2026-05-22*