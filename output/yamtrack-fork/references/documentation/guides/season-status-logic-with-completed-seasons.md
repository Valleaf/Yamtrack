# How To: Season Status Logic With Completed Seasons

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test that seasons are marked as completed when all episodes are watched.

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
# Fixtures: mock_tv_with_seasons, mock_user_list
```

## Step-by-Step Guide

### Step 1: 'Test that seasons are marked as completed when all episodes are watched.'

```python
'Test that seasons are marked as completed when all episodes are watched.'
```

### Step 2: Assign mock_tv_with_seasons.return_value = value

```python
mock_tv_with_seasons.return_value = {'title': 'Breaking Bad', 'image': 'https://image.tmdb.org/t/p/w500/test.jpg', 'season/1': {'image': 'https://image.tmdb.org/t/p/w500/season1.jpg', 'max_progress': 7, 'episodes': [{'episode_number': 1, 'still_path': '/ep1.jpg'}, {'episode_number': 2, 'still_path': '/ep2.jpg'}, {'episode_number': 3, 'still_path': '/ep3.jpg'}, {'episode_number': 4, 'still_path': '/ep4.jpg'}, {'episode_number': 5, 'still_path': '/ep5.jpg'}, {'episode_number': 6, 'still_path': '/ep6.jpg'}, {'episode_number': 7, 'still_path': '/ep7.jpg'}]}, 'season/2': {'image': 'https://image.tmdb.org/t/p/w500/season2.jpg', 'max_progress': 13}}
```

### Step 3: Assign mock_user_list.return_value = value

```python
mock_user_list.return_value = {'shows': [{'last_watched_at': '2023-01-15T00:00:00Z', 'show': {'title': 'Breaking Bad', 'ids': {'tmdb': 1396}}, 'status': 'watching', 'user_rating': 9, 'seasons': [{'number': 1, 'episodes': [{'number': 1, 'watched_at': '2023-01-01T00:00:00Z'}, {'number': 2, 'watched_at': '2023-01-02T00:00:00Z'}, {'number': 3, 'watched_at': '2023-01-03T00:00:00Z'}, {'number': 4, 'watched_at': '2023-01-04T00:00:00Z'}, {'number': 5, 'watched_at': '2023-01-05T00:00:00Z'}, {'number': 6, 'watched_at': '2023-01-06T00:00:00Z'}, {'number': 7, 'watched_at': '2023-01-07T00:00:00Z'}]}], 'memo': {}}], 'movies': [], 'anime': []}
```

### Step 4: Assign unknown = self.importer.import_data(...)

```python
imported_counts, _ = self.importer.import_data()
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(imported_counts[MediaTypes.TV.value], 1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(imported_counts[MediaTypes.SEASON.value], 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(imported_counts[MediaTypes.EPISODE.value], 7)
```

### Step 8: Assign tv_item = Item.objects.get(...)

```python
tv_item = Item.objects.get(media_type=MediaTypes.TV.value)
```

### Step 9: Assign tv_obj = TV.objects.get(...)

```python
tv_obj = TV.objects.get(item=tv_item)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(tv_obj.status, Status.IN_PROGRESS.value)
```

### Step 11: Assign season1_item = Item.objects.get(...)

```python
season1_item = Item.objects.get(media_type=MediaTypes.SEASON.value, season_number=1)
```

### Step 12: Assign season1_obj = Season.objects.get(...)

```python
season1_obj = Season.objects.get(item=season1_item)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(season1_obj.status, Status.COMPLETED.value, 'Season 1 should be completed when all episodes are watched')
```

### Step 14: Assign season1_episodes = Episode.objects.filter(...)

```python
season1_episodes = Episode.objects.filter(item__season_number=1, item__media_type=MediaTypes.EPISODE.value)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(season1_episodes.count(), 7)
```

### Step 16: Call self.assertIsNotNone()

```python
self.assertIsNotNone(episode.end_date)
```


## Complete Example

```python
# Setup
# Fixtures: mock_tv_with_seasons, mock_user_list

# Workflow
'Test that seasons are marked as completed when all episodes are watched.'
mock_tv_with_seasons.return_value = {'title': 'Breaking Bad', 'image': 'https://image.tmdb.org/t/p/w500/test.jpg', 'season/1': {'image': 'https://image.tmdb.org/t/p/w500/season1.jpg', 'max_progress': 7, 'episodes': [{'episode_number': 1, 'still_path': '/ep1.jpg'}, {'episode_number': 2, 'still_path': '/ep2.jpg'}, {'episode_number': 3, 'still_path': '/ep3.jpg'}, {'episode_number': 4, 'still_path': '/ep4.jpg'}, {'episode_number': 5, 'still_path': '/ep5.jpg'}, {'episode_number': 6, 'still_path': '/ep6.jpg'}, {'episode_number': 7, 'still_path': '/ep7.jpg'}]}, 'season/2': {'image': 'https://image.tmdb.org/t/p/w500/season2.jpg', 'max_progress': 13}}
mock_user_list.return_value = {'shows': [{'last_watched_at': '2023-01-15T00:00:00Z', 'show': {'title': 'Breaking Bad', 'ids': {'tmdb': 1396}}, 'status': 'watching', 'user_rating': 9, 'seasons': [{'number': 1, 'episodes': [{'number': 1, 'watched_at': '2023-01-01T00:00:00Z'}, {'number': 2, 'watched_at': '2023-01-02T00:00:00Z'}, {'number': 3, 'watched_at': '2023-01-03T00:00:00Z'}, {'number': 4, 'watched_at': '2023-01-04T00:00:00Z'}, {'number': 5, 'watched_at': '2023-01-05T00:00:00Z'}, {'number': 6, 'watched_at': '2023-01-06T00:00:00Z'}, {'number': 7, 'watched_at': '2023-01-07T00:00:00Z'}]}], 'memo': {}}], 'movies': [], 'anime': []}
imported_counts, _ = self.importer.import_data()
self.assertEqual(imported_counts[MediaTypes.TV.value], 1)
self.assertEqual(imported_counts[MediaTypes.SEASON.value], 1)
self.assertEqual(imported_counts[MediaTypes.EPISODE.value], 7)
tv_item = Item.objects.get(media_type=MediaTypes.TV.value)
tv_obj = TV.objects.get(item=tv_item)
self.assertEqual(tv_obj.status, Status.IN_PROGRESS.value)
season1_item = Item.objects.get(media_type=MediaTypes.SEASON.value, season_number=1)
season1_obj = Season.objects.get(item=season1_item)
self.assertEqual(season1_obj.status, Status.COMPLETED.value, 'Season 1 should be completed when all episodes are watched')
season1_episodes = Episode.objects.filter(item__season_number=1, item__media_type=MediaTypes.EPISODE.value)
self.assertEqual(season1_episodes.count(), 7)
for episode in season1_episodes:
    self.assertIsNotNone(episode.end_date)
```

## Next Steps


---

*Source: test_simkl.py:145 | Complexity: Advanced | Last updated: 2026-05-22*