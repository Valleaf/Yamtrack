# How To: Process Tv Does Not Reopen Completed Show For Past Only Season

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Past-only seasons should not reopen a completed TV entry.

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
# Fixtures: mock_tv, mock_tv_with_seasons, mock_get_tvmaze_episode_map
```

## Step-by-Step Guide

### Step 1: 'Past-only seasons should not reopen a completed TV entry.'

```python
'Past-only seasons should not reopen a completed TV entry.'
```

### Step 2: Call TV.objects.filter.update()

```python
TV.objects.filter(item=self.tv_item, user=self.user).update(status=Status.COMPLETED.value)
```

### Step 3: Call Season.objects.filter.update()

```python
Season.objects.filter(item=self.season_item, user=self.user).update(status=Status.COMPLETED.value)
```

### Step 4: Call Event.objects.create()

```python
Event.objects.create(item=self.season_item, content_number=1, datetime=date_parser('2008-01-20'))
```

### Step 5: Assign mock_tv.return_value = value

```python
mock_tv.return_value = {'related': {'seasons': [{'season_number': 1, 'episodes': [1]}, {'season_number': 2, 'episodes': [1]}]}, 'next_episode_season': 2}
```

### Step 6: Assign mock_tv_with_seasons.return_value = value

```python
mock_tv_with_seasons.return_value = {'season/2': {'image': 'http://example.com/season2.jpg', 'season_number': 2, 'episodes': [{'episode_number': 1, 'air_date': '2010-01-20'}], 'tvdb_id': '81189'}}
```

### Step 7: Assign mock_get_tvmaze_episode_map.return_value = value

```python
mock_get_tvmaze_episode_map.return_value = {}
```

### Step 8: Assign events_bulk = value

```python
events_bulk = []
```

### Step 9: Call process_tv()

```python
process_tv(self.tv_item, events_bulk)
```

### Step 10: Assign tv = TV.objects.get(...)

```python
tv = TV.objects.get(item=self.tv_item, user=self.user)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(tv.status, Status.COMPLETED.value)
```

### Step 12: Call self.assertFalse()

```python
self.assertFalse(Season.objects.filter(item__media_id=self.tv_item.media_id, item__source=self.tv_item.source, item__season_number=2, user=self.user).exists())
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(len(events_bulk), 1)
```


## Complete Example

```python
# Setup
# Fixtures: mock_tv, mock_tv_with_seasons, mock_get_tvmaze_episode_map

# Workflow
'Past-only seasons should not reopen a completed TV entry.'
TV.objects.filter(item=self.tv_item, user=self.user).update(status=Status.COMPLETED.value)
Season.objects.filter(item=self.season_item, user=self.user).update(status=Status.COMPLETED.value)
Event.objects.create(item=self.season_item, content_number=1, datetime=date_parser('2008-01-20'))
mock_tv.return_value = {'related': {'seasons': [{'season_number': 1, 'episodes': [1]}, {'season_number': 2, 'episodes': [1]}]}, 'next_episode_season': 2}
mock_tv_with_seasons.return_value = {'season/2': {'image': 'http://example.com/season2.jpg', 'season_number': 2, 'episodes': [{'episode_number': 1, 'air_date': '2010-01-20'}], 'tvdb_id': '81189'}}
mock_get_tvmaze_episode_map.return_value = {}
events_bulk = []
process_tv(self.tv_item, events_bulk)
tv = TV.objects.get(item=self.tv_item, user=self.user)
self.assertEqual(tv.status, Status.COMPLETED.value)
self.assertFalse(Season.objects.filter(item__media_id=self.tv_item.media_id, item__source=self.tv_item.source, item__season_number=2, user=self.user).exists())
self.assertEqual(len(events_bulk), 1)
```

## Next Steps


---

*Source: test_tv.py:155 | Complexity: Advanced | Last updated: 2026-05-22*