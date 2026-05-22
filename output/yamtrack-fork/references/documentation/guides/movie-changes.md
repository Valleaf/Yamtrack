# How To: Movie Changes

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test fetching changed movie ids from TMDB.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `datetime`
- `pathlib`
- `unittest.mock`
- `requests`
- `django.conf`
- `django.test`
- `app.models`
- `app.providers`

**Required Fixtures:**
- `api_client` fixture

**Setup Required:**
```python
# Fixtures: mock_api_request, mock_localdate
```

## Step-by-Step Guide

### Step 1: 'Test fetching changed movie ids from TMDB.'

```python
'Test fetching changed movie ids from TMDB.'
```

### Step 2: Assign mock_localdate.return_value = date(...)

```python
mock_localdate.return_value = date(2026, 4, 5)
```

### Step 3: Assign mock_api_request.return_value = value

```python
mock_api_request.return_value = {'results': [{'id': 10}, {'id': 20}], 'total_pages': 1}
```

### Step 4: Assign result = tmdb.movie_changes(...)

```python
result = tmdb.movie_changes()
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(result, {'10', '20'})
```

### Step 6: Assign unknown = value

```python
_, kwargs = mock_api_request.call_args
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(kwargs['params']['start_date'], '2026-04-02')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(kwargs['params']['end_date'], '2026-04-05')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(kwargs['params']['page'], 1)
```


## Complete Example

```python
# Setup
# Fixtures: mock_api_request, mock_localdate

# Workflow
'Test fetching changed movie ids from TMDB.'
mock_localdate.return_value = date(2026, 4, 5)
mock_api_request.return_value = {'results': [{'id': 10}, {'id': 20}], 'total_pages': 1}
result = tmdb.movie_changes()
self.assertEqual(result, {'10', '20'})
_, kwargs = mock_api_request.call_args
self.assertEqual(kwargs['params']['start_date'], '2026-04-02')
self.assertEqual(kwargs['params']['end_date'], '2026-04-05')
self.assertEqual(kwargs['params']['page'], 1)
```

## Next Steps


---

*Source: test_metadata.py:117 | Complexity: Advanced | Last updated: 2026-05-22*