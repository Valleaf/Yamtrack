# How To: In Progress Status Creates New Season If Needed

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test setting status to IN_PROGRESS creates new season if needed.

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

### Step 1: 'Test setting status to IN_PROGRESS creates new season if needed.'

```python
'Test setting status to IN_PROGRESS creates new season if needed.'
```

### Step 2: Assign self.season1.status = value

```python
self.season1.status = Status.COMPLETED.value
```

### Step 3: Call self.season1.save()

```python
self.season1.save()
```

### Step 4: Assign self.season2.status = value

```python
self.season2.status = Status.COMPLETED.value
```

### Step 5: Call self.season2.save()

```python
self.season2.save()
```

### Step 6: Assign mock_metadata = value

```python
mock_metadata = {'related': {'seasons': [{'season_number': 1, 'image': 'img1.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 2, 'image': 'img2.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 3, 'image': 'img3.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}}
```

### Step 7: Assign mock_get_metadata.return_value = mock_metadata

```python
mock_get_metadata.return_value = mock_metadata
```

### Step 8: Assign self.tv.status = value

```python
self.tv.status = Status.IN_PROGRESS.value
```

### Step 9: Call self.tv.save()

```python
self.tv.save()
```

### Step 10: Assign season3 = self.tv.seasons.get(...)

```python
season3 = self.tv.seasons.get(item__season_number=3)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(season3.status, Status.IN_PROGRESS.value)
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_metadata

# Workflow
'Test setting status to IN_PROGRESS creates new season if needed.'
self.season1.status = Status.COMPLETED.value
self.season1.save()
self.season2.status = Status.COMPLETED.value
self.season2.save()
mock_metadata = {'related': {'seasons': [{'season_number': 1, 'image': 'img1.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 2, 'image': 'img2.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 3, 'image': 'img3.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}}
mock_get_metadata.return_value = mock_metadata
self.tv.status = Status.IN_PROGRESS.value
self.tv.save()
season3 = self.tv.seasons.get(item__season_number=3)
self.assertEqual(season3.status, Status.IN_PROGRESS.value)
```

## Next Steps


---

*Source: test_tv.py:389 | Complexity: Advanced | Last updated: 2026-05-22*