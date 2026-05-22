# How To: List Detail View Sorting

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test the list_detail view with different sorting options.

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
# Fixtures: mock_user_can_view, mock_update_preference
```

## Step-by-Step Guide

### Step 1: 'Test the list_detail view with different sorting options.'

```python
'Test the list_detail view with different sorting options.'
```

### Step 2: Assign mock_user_can_view.return_value = True

```python
mock_user_can_view.return_value = True
```

### Step 3: Call Movie.objects.create()

```python
Movie.objects.create(item=self.movie_item, status=Status.COMPLETED.value, user=self.user)
```

### Step 4: Call TV.objects.create()

```python
TV.objects.create(item=self.tv_item, status=Status.IN_PROGRESS.value, user=self.user)
```

### Step 5: Call Anime.objects.create()

```python
Anime.objects.create(item=self.anime_item, status=Status.PLANNING.value, user=self.user)
```

### Step 6: Assign mock_update_preference.side_effect = value

```python
mock_update_preference.side_effect = ['title', None]
```

### Step 7: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('list_detail', args=[self.custom_list.id]) + '?sort=title')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(response.context['current_sort'], 'title')
```

### Step 10: Assign mock_update_preference.side_effect = value

```python
mock_update_preference.side_effect = ['media_type', None]
```

### Step 11: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('list_detail', args=[self.custom_list.id]) + '?sort=media_type')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(response.context['current_sort'], 'media_type')
```


## Complete Example

```python
# Setup
# Fixtures: mock_user_can_view, mock_update_preference

# Workflow
'Test the list_detail view with different sorting options.'
mock_user_can_view.return_value = True
Movie.objects.create(item=self.movie_item, status=Status.COMPLETED.value, user=self.user)
TV.objects.create(item=self.tv_item, status=Status.IN_PROGRESS.value, user=self.user)
Anime.objects.create(item=self.anime_item, status=Status.PLANNING.value, user=self.user)
mock_update_preference.side_effect = ['title', None]
response = self.client.get(reverse('list_detail', args=[self.custom_list.id]) + '?sort=title')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'title')
mock_update_preference.side_effect = ['media_type', None]
response = self.client.get(reverse('list_detail', args=[self.custom_list.id]) + '?sort=media_type')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'media_type')
```

## Next Steps


---

*Source: test_views.py:420 | Complexity: Advanced | Last updated: 2026-05-22*