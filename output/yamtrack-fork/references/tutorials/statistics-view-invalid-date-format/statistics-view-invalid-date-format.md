# How To: Statistics View Invalid Date Format

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the statistics view with invalid date format.

## Prerequisites

**Required Modules:**
- `django.contrib.auth`
- `django.test`
- `django.urls`


## Step-by-Step Guide

### Step 1: 'Test the statistics view with invalid date format.'

```python
'Test the statistics view with invalid date format.'
```

### Step 2: Assign start_date = '01/01/2023'

```python
start_date = '01/01/2023'
```

### Step 3: Assign end_date = '2023/12/31'

```python
end_date = '2023/12/31'
```

### Step 4: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('statistics') + f'?start-date={start_date}&end-date={end_date}')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 6: Assign date_is_none = value

```python
date_is_none = response.context['start_date'] is None and response.context['end_date'] is None
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(date_is_none)
```


## Complete Example

```python
# Workflow
'Test the statistics view with invalid date format.'
start_date = '01/01/2023'
end_date = '2023/12/31'
response = self.client.get(reverse('statistics') + f'?start-date={start_date}&end-date={end_date}')
self.assertEqual(response.status_code, 200)
date_is_none = response.context['start_date'] is None and response.context['end_date'] is None
self.assertTrue(date_is_none)
```

## Next Steps


---

*Source: test_statistics.py:53 | Complexity: Intermediate | Last updated: 2026-05-22*