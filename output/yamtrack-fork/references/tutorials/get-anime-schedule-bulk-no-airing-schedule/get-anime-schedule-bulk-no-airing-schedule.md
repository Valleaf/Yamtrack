# How To: Get Anime Schedule Bulk No Airing Schedule

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test get_anime_schedule_bulk with no airing schedule.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `unittest.mock`
- `zoneinfo`
- `django.test`
- `events.calendar.anime`
- `events.tests.calendar.utils`

**Required Fixtures:**
- `api_client` fixture

**Setup Required:**
```python
# Fixtures: mock_api_request, mock_get_media_metadata
```

## Step-by-Step Guide

### Step 1: 'Test get_anime_schedule_bulk with no airing schedule.'

```python
'Test get_anime_schedule_bulk with no airing schedule.'
```

### Step 2: Assign mock_api_request.return_value = value

```python
mock_api_request.return_value = {'data': {'Page': {'pageInfo': {'hasNextPage': False}, 'media': [{'idMal': 437, 'endDate': {'year': 1997, 'month': 8, 'day': 12}, 'episodes': 2, 'airingSchedule': {'nodes': []}}]}}}
```

### Step 3: Assign mock_get_media_metadata.return_value = value

```python
mock_get_media_metadata.return_value = {'max_progress': 2, 'details': {'end_date': '1997-08-12'}}
```

### Step 4: Assign result = get_anime_schedule_bulk(...)

```python
result = get_anime_schedule_bulk(['437'])
```

### Step 5: Call self.assertIn()

```python
self.assertIn('437', result)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(result['437']), 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(result['437'][0]['episode'], 2)
```

### Step 8: Assign start_date = datetime.datetime.fromtimestamp(...)

```python
start_date = datetime.datetime.fromtimestamp(result['437'][0]['airingAt'], tz=ZoneInfo('UTC'))
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(start_date.year, 1997)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(start_date.month, 8)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(start_date.day, 12)
```


## Complete Example

```python
# Setup
# Fixtures: mock_api_request, mock_get_media_metadata

# Workflow
'Test get_anime_schedule_bulk with no airing schedule.'
mock_api_request.return_value = {'data': {'Page': {'pageInfo': {'hasNextPage': False}, 'media': [{'idMal': 437, 'endDate': {'year': 1997, 'month': 8, 'day': 12}, 'episodes': 2, 'airingSchedule': {'nodes': []}}]}}}
mock_get_media_metadata.return_value = {'max_progress': 2, 'details': {'end_date': '1997-08-12'}}
result = get_anime_schedule_bulk(['437'])
self.assertIn('437', result)
self.assertEqual(len(result['437']), 1)
self.assertEqual(result['437'][0]['episode'], 2)
start_date = datetime.datetime.fromtimestamp(result['437'][0]['airingAt'], tz=ZoneInfo('UTC'))
self.assertEqual(start_date.year, 1997)
self.assertEqual(start_date.month, 8)
self.assertEqual(start_date.day, 12)
```

## Next Steps


---

*Source: test_anime.py:51 | Complexity: Advanced | Last updated: 2026-05-22*