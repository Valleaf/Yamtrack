# How To: Is Released Date With Custom Current Date

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test is_released_date with explicit current_date parameter.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `datetime`
- `django.contrib.auth`
- `django.http`
- `django.test`
- `django.utils`
- `app.helpers`
- `app.models`


## Step-by-Step Guide

### Step 1: 'Test is_released_date with explicit current_date parameter.'

```python
'Test is_released_date with explicit current_date parameter.'
```

### Step 2: Assign test_date = date(...)

```python
test_date = date(2020, 5, 15)
```

### Step 3: Assign current_date = date(...)

```python
current_date = date(2020, 5, 20)
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(is_released_date(test_date, current_date))
```

### Step 5: Assign current_date = date(...)

```python
current_date = date(2020, 5, 10)
```

### Step 6: Call self.assertFalse()

```python
self.assertFalse(is_released_date(test_date, current_date))
```

### Step 7: Assign current_date = date(...)

```python
current_date = date(2020, 5, 15)
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(is_released_date(test_date, current_date))
```


## Complete Example

```python
# Workflow
'Test is_released_date with explicit current_date parameter.'
test_date = date(2020, 5, 15)
current_date = date(2020, 5, 20)
self.assertTrue(is_released_date(test_date, current_date))
current_date = date(2020, 5, 10)
self.assertFalse(is_released_date(test_date, current_date))
current_date = date(2020, 5, 15)
self.assertTrue(is_released_date(test_date, current_date))
```

## Next Steps


---

*Source: test_helpers.py:358 | Complexity: Advanced | Last updated: 2026-05-22*