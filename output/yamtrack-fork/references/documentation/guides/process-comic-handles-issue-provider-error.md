# How To: Process Comic Handles Issue Provider Error

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Issue lookup failures should stop comic processing quietly.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest.mock`
- `django.test`
- `app.models`
- `app.providers`
- `events.calendar.comic`
- `events.calendar.helpers`
- `events.models`
- `events.tests.calendar.utils`

**Setup Required:**
```python
# Fixtures: mock_issue, mock_get_media_metadata
```

## Step-by-Step Guide

### Step 1: 'Issue lookup failures should stop comic processing quietly.'

```python
'Issue lookup failures should stop comic processing quietly.'
```

### Step 2: Assign response = type(...)

```python
response = type('Response', (), {'status_code': 500, 'text': 'boom'})()
```

### Step 3: Assign mock_get_media_metadata.return_value = value

```python
mock_get_media_metadata.return_value = {'max_issue_number': 10, 'last_issue_id': '4000-123456', 'last_issue': {'issue_number': '10'}}
```

### Step 4: Assign mock_issue.side_effect = services.ProviderAPIError(...)

```python
mock_issue.side_effect = services.ProviderAPIError(provider=Sources.COMICVINE.value, error=type('Error', (), {'response': response})(), details='boom')
```

### Step 5: Assign events_bulk = value

```python
events_bulk = []
```

### Step 6: Call process_comic()

```python
process_comic(self.comic_item, events_bulk)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(events_bulk, [])
```


## Complete Example

```python
# Setup
# Fixtures: mock_issue, mock_get_media_metadata

# Workflow
'Issue lookup failures should stop comic processing quietly.'
response = type('Response', (), {'status_code': 500, 'text': 'boom'})()
mock_get_media_metadata.return_value = {'max_issue_number': 10, 'last_issue_id': '4000-123456', 'last_issue': {'issue_number': '10'}}
mock_issue.side_effect = services.ProviderAPIError(provider=Sources.COMICVINE.value, error=type('Error', (), {'response': response})(), details='boom')
events_bulk = []
process_comic(self.comic_item, events_bulk)
self.assertEqual(events_bulk, [])
```

## Next Steps


---

*Source: test_comic.py:135 | Complexity: Intermediate | Last updated: 2026-05-22*