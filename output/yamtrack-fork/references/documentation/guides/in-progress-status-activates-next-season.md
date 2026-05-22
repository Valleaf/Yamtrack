# How To: In Progress Status Activates Next Season

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test setting status to IN_PROGRESS activates next available season.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `pathlib`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `app.models`

**Setup Required:**
```python
# Fixtures: mock_get_metadata
```

## Step-by-Step Guide

### Step 1: 'Test setting status to IN_PROGRESS activates next available season.'

```python
'Test setting status to IN_PROGRESS activates next available season.'
```

### Step 2: Assign self.season1.status = value

```python
self.season1.status = Status.COMPLETED.value
```

### Step 3: Call self.season1.save()

```python
self.season1.save()
```

### Step 4: Assign mock_get_metadata.return_value = value

```python
mock_get_metadata.return_value = {'related': {'seasons': [{'season_number': 1, 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 2, 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}}
```

### Step 5: Assign self.tv.status = value

```python
self.tv.status = Status.IN_PROGRESS.value
```

### Step 6: Call self.tv.save()

```python
self.tv.save()
```

### Step 7: Assign season2 = Season.objects.get(...)

```python
season2 = Season.objects.get(pk=self.season2.pk)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(season2.status, Status.IN_PROGRESS.value)
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_metadata

# Workflow
'Test setting status to IN_PROGRESS activates next available season.'
self.season1.status = Status.COMPLETED.value
self.season1.save()
mock_get_metadata.return_value = {'related': {'seasons': [{'season_number': 1, 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 2, 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}}
self.tv.status = Status.IN_PROGRESS.value
self.tv.save()
season2 = Season.objects.get(pk=self.season2.pk)
self.assertEqual(season2.status, Status.IN_PROGRESS.value)
```

## Next Steps


---

*Source: test_tv.py:362 | Complexity: Advanced | Last updated: 2026-05-22*