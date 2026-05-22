# How To: Process Tv Returns When No Seasons Need Processing

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: process_tv should stop cleanly when there is nothing new to fetch.

## Prerequisites

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


## Step-by-Step Guide

### Step 1: 'process_tv should stop cleanly when there is nothing new to fetch.'

```python
'process_tv should stop cleanly when there is nothing new to fetch.'
```

### Step 2: Assign mock_get_seasons_to_process.return_value = value

```python
mock_get_seasons_to_process.return_value = []
```

### Step 3: Assign events_bulk = value

```python
events_bulk = []
```

### Step 4: Call process_tv()

```python
process_tv(self.tv_item, events_bulk)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(events_bulk, [])
```


## Complete Example

```python
# Workflow
'process_tv should stop cleanly when there is nothing new to fetch.'
mock_get_seasons_to_process.return_value = []
events_bulk = []
process_tv(self.tv_item, events_bulk)
self.assertEqual(events_bulk, [])
```

## Next Steps


---

*Source: test_tv.py:303 | Complexity: Intermediate | Last updated: 2026-05-22*