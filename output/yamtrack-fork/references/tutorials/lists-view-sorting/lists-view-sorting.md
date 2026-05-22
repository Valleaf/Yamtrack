# How To: Lists View Sorting

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test the lists view with different sorting options.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `django.urls`
- `app.models`
- `lists.models`

**Setup Required:**
```python
# Fixtures: mock_update_preference
```

## Step-by-Step Guide

### Step 1: 'Test the lists view with different sorting options.'

```python
'Test the lists view with different sorting options.'
```

### Step 2: Call self.client.login()

```python
self.client.login(**self.credentials)
```

### Step 3: Assign mock_update_preference.return_value = 'name'

```python
mock_update_preference.return_value = 'name'
```

### Step 4: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('lists') + '?sort=name')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(response.context['current_sort'], 'name')
```

### Step 7: Assign mock_update_preference.return_value = 'items_count'

```python
mock_update_preference.return_value = 'items_count'
```

### Step 8: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('lists') + '?sort=items_count')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(response.context['current_sort'], 'items_count')
```

### Step 11: Assign mock_update_preference.return_value = 'newest_first'

```python
mock_update_preference.return_value = 'newest_first'
```

### Step 12: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('lists') + '?sort=newest_first')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(response.context['current_sort'], 'newest_first')
```

### Step 15: Assign mock_update_preference.return_value = 'last_item_added'

```python
mock_update_preference.return_value = 'last_item_added'
```

### Step 16: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('lists'))
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(response.context['current_sort'], 'last_item_added')
```


## Complete Example

```python
# Setup
# Fixtures: mock_update_preference

# Workflow
'Test the lists view with different sorting options.'
self.client.login(**self.credentials)
mock_update_preference.return_value = 'name'
response = self.client.get(reverse('lists') + '?sort=name')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'name')
mock_update_preference.return_value = 'items_count'
response = self.client.get(reverse('lists') + '?sort=items_count')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'items_count')
mock_update_preference.return_value = 'newest_first'
response = self.client.get(reverse('lists') + '?sort=newest_first')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'newest_first')
mock_update_preference.return_value = 'last_item_added'
response = self.client.get(reverse('lists'))
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'last_item_added')
```

## Next Steps


---

*Source: test_views.py:104 | Complexity: Advanced | Last updated: 2026-05-22*