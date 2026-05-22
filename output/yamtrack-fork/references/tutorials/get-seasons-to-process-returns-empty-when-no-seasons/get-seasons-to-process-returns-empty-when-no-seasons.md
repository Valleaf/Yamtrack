# How To: Get Seasons To Process Returns Empty When No Seasons

**Difficulty**: Intermediate
**Estimated Time**: 5 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: TV metadata without seasons should short-circuit processing.

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
# Fixtures: mock_tv
```

## Step-by-Step Guide

### Step 1: 'TV metadata without seasons should short-circuit processing.'

```python
'TV metadata without seasons should short-circuit processing.'
```

### Step 2: Assign mock_tv.return_value = value

```python
mock_tv.return_value = {'related': {'seasons': []}}
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(get_seasons_to_process(self.tv_item), [])
```


## Complete Example

```python
# Setup
# Fixtures: mock_tv

# Workflow
'TV metadata without seasons should short-circuit processing.'
mock_tv.return_value = {'related': {'seasons': []}}
self.assertEqual(get_seasons_to_process(self.tv_item), [])
```

## Next Steps


---

*Source: test_tv.py:296 | Complexity: Intermediate | Last updated: 2026-05-22*