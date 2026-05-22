# How To: Process Anime Bulk

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test process_anime_bulk function.

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
# Fixtures: mock_api_request
```

## Step-by-Step Guide

### Step 1: 'Test process_anime_bulk function.'

```python
'Test process_anime_bulk function.'
```

### Step 2: Assign mock_api_request.return_value = value

```python
mock_api_request.return_value = {'data': {'Page': {'pageInfo': {'hasNextPage': False}, 'media': [{'idMal': 437, 'endDate': {'year': 1997, 'month': 8, 'day': 5}, 'episodes': 1, 'airingSchedule': {'nodes': [{'episode': 1, 'airingAt': 870739200}]}}]}}}
```

### Step 3: Assign events_bulk = value

```python
events_bulk = []
```

### Step 4: Call process_anime_bulk()

```python
process_anime_bulk([self.anime_item], events_bulk)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(events_bulk), 1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].item, self.anime_item)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].content_number, 1)
```

### Step 8: Assign expected_date = datetime.datetime.fromtimestamp(...)

```python
expected_date = datetime.datetime.fromtimestamp(870739200, tz=ZoneInfo('UTC'))
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(events_bulk[0].datetime, expected_date)
```


## Complete Example

```python
# Setup
# Fixtures: mock_api_request

# Workflow
'Test process_anime_bulk function.'
mock_api_request.return_value = {'data': {'Page': {'pageInfo': {'hasNextPage': False}, 'media': [{'idMal': 437, 'endDate': {'year': 1997, 'month': 8, 'day': 5}, 'episodes': 1, 'airingSchedule': {'nodes': [{'episode': 1, 'airingAt': 870739200}]}}]}}}
events_bulk = []
process_anime_bulk([self.anime_item], events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, self.anime_item)
self.assertEqual(events_bulk[0].content_number, 1)
expected_date = datetime.datetime.fromtimestamp(870739200, tz=ZoneInfo('UTC'))
self.assertEqual(events_bulk[0].datetime, expected_date)
```

## Next Steps


---

*Source: test_anime.py:153 | Complexity: Advanced | Last updated: 2026-05-22*