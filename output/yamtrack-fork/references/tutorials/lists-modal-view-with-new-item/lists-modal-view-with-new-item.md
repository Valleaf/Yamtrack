# How To: Lists Modal View With New Item

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test the lists_modal view with a new item.

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
# Fixtures: mock_get_lists, mock_get_metadata
```

## Step-by-Step Guide

### Step 1: 'Test the lists_modal view with a new item.'

```python
'Test the lists_modal view with a new item.'
```

### Step 2: Assign mock_get_lists.return_value = value

```python
mock_get_lists.return_value = [self.list1, self.list2]
```

### Step 3: Assign mock_get_metadata.return_value = value

```python
mock_get_metadata.return_value = {'title': 'New Movie', 'image': 'http://example.com/new_image.jpg'}
```

### Step 4: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('lists_modal', args=[Sources.TMDB.value, MediaTypes.MOVIE.value, '999']))
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(Item.objects.filter(media_id='999', source=Sources.TMDB.value).exists())
```

### Step 7: Assign new_item = Item.objects.get(...)

```python
new_item = Item.objects.get(media_id='999', source=Sources.TMDB.value)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(new_item.title, 'New Movie')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(new_item.image, 'http://example.com/new_image.jpg')
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_lists, mock_get_metadata

# Workflow
'Test the lists_modal view with a new item.'
mock_get_lists.return_value = [self.list1, self.list2]
mock_get_metadata.return_value = {'title': 'New Movie', 'image': 'http://example.com/new_image.jpg'}
response = self.client.get(reverse('lists_modal', args=[Sources.TMDB.value, MediaTypes.MOVIE.value, '999']))
self.assertEqual(response.status_code, 200)
self.assertTrue(Item.objects.filter(media_id='999', source=Sources.TMDB.value).exists())
new_item = Item.objects.get(media_id='999', source=Sources.TMDB.value)
self.assertEqual(new_item.title, 'New Movie')
self.assertEqual(new_item.image, 'http://example.com/new_image.jpg')
```

## Next Steps


---

*Source: test_views.py:684 | Complexity: Advanced | Last updated: 2026-05-22*