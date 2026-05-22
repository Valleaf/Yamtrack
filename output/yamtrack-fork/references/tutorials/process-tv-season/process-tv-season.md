# How To: Process Tv Season

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test processing for a TV season.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `unittest.mock`
- `zoneinfo`
- `requests`
- `django.core.cache`
- `django.test`
- `app.models`
- `events.calendar.helpers`
- `events.calendar.tv`
- `events.models`
- `events.tests.calendar.utils`

**Setup Required:**
```python
# Fixtures: mock_get_tvmaze_episode_map, mock_tv_with_seasons, mock_tv
```

## Step-by-Step Guide

### Step 1: 'Test processing for a TV season.'

```python
'Test processing for a TV season.'
```

### Step 2: Assign mock_tv.return_value = value

```python
mock_tv.return_value = {'related': {'seasons': [{'season_number': 1, 'episodes': [1, 2, 3]}, {'season_number': 2, 'episodes': [1, 2]}, {'season_number': 3, 'episodes': [1]}]}, 'next_episode_season': 2}
```

### Step 3: Assign mock_tv_with_seasons.return_value = value

```python
mock_tv_with_seasons.return_value = {'season/1': {'image': 'http://example.com/season1.jpg', 'season_number': 1, 'episodes': [{'episode_number': 1, 'air_date': '2008-01-20'}, {'episode_number': 2, 'air_date': '2008-01-27'}, {'episode_number': 3, 'air_date': '2008-02-03'}], 'tvdb_id': '81189'}, 'season/2': {'image': 'http://example.com/season2.jpg', 'season_number': 2, 'episodes': [{'episode_number': 1, 'air_date': '2009-01-20'}, {'episode_number': 2, 'air_date': '2009-01-27'}], 'tvdb_id': '81189'}, 'season/3': {'image': 'http://example.com/season3.jpg', 'season_number': 3, 'episodes': [{'episode_number': 1, 'air_date': '2010-01-20'}], 'tvdb_id': '81189'}}
```

### Step 4: Assign mock_get_tvmaze_episode_map.return_value = value

```python
mock_get_tvmaze_episode_map.return_value = {'1_1': '2008-01-20T22:00:00+00:00', '1_2': '2008-01-27T22:00:00+00:00', '1_3': '2008-02-03T22:00:00+00:00'}
```

### Step 5: Assign events_bulk = value

```python
events_bulk = []
```

### Step 6: Call process_tv()

```python
process_tv(self.tv_item, events_bulk)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(events_bulk), 6)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].item, self.season_item)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].content_number, 1)
```

### Step 10: Assign expected_date = datetime.datetime.fromisoformat(...)

```python
expected_date = datetime.datetime.fromisoformat('2008-01-20T22:00:00+00:00')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].datetime, expected_date)
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_tvmaze_episode_map, mock_tv_with_seasons, mock_tv

# Workflow
'Test processing for a TV season.'
mock_tv.return_value = {'related': {'seasons': [{'season_number': 1, 'episodes': [1, 2, 3]}, {'season_number': 2, 'episodes': [1, 2]}, {'season_number': 3, 'episodes': [1]}]}, 'next_episode_season': 2}
mock_tv_with_seasons.return_value = {'season/1': {'image': 'http://example.com/season1.jpg', 'season_number': 1, 'episodes': [{'episode_number': 1, 'air_date': '2008-01-20'}, {'episode_number': 2, 'air_date': '2008-01-27'}, {'episode_number': 3, 'air_date': '2008-02-03'}], 'tvdb_id': '81189'}, 'season/2': {'image': 'http://example.com/season2.jpg', 'season_number': 2, 'episodes': [{'episode_number': 1, 'air_date': '2009-01-20'}, {'episode_number': 2, 'air_date': '2009-01-27'}], 'tvdb_id': '81189'}, 'season/3': {'image': 'http://example.com/season3.jpg', 'season_number': 3, 'episodes': [{'episode_number': 1, 'air_date': '2010-01-20'}], 'tvdb_id': '81189'}}
mock_get_tvmaze_episode_map.return_value = {'1_1': '2008-01-20T22:00:00+00:00', '1_2': '2008-01-27T22:00:00+00:00', '1_3': '2008-02-03T22:00:00+00:00'}
events_bulk = []
process_tv(self.tv_item, events_bulk)
self.assertEqual(len(events_bulk), 6)
self.assertEqual(events_bulk[0].item, self.season_item)
self.assertEqual(events_bulk[0].content_number, 1)
expected_date = datetime.datetime.fromisoformat('2008-01-20T22:00:00+00:00')
self.assertEqual(events_bulk[0].datetime, expected_date)
```

## Next Steps


---

*Source: test_tv.py:29 | Complexity: Advanced | Last updated: 2026-05-22*