# How To: Create Entry Post Season

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test creating a season entry with parent TV.

## Prerequisites

**Required Modules:**
- `django.contrib.auth`
- `django.db`
- `django.test`
- `django.urls`
- `django.utils`
- `app.models`


## Step-by-Step Guide

### Step 1: 'Test creating a season entry with parent TV.'

```python
'Test creating a season entry with parent TV.'
```

### Step 2: Assign tv_item = Item.objects.create(...)

```python
tv_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='TV Show')
```

### Step 3: Assign parent_tv = TV.objects.create(...)

```python
parent_tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
```

### Step 4: Assign form_data = value

```python
form_data = {'title': 'TV Show', 'media_type': MediaTypes.SEASON.value, 'season_number': 1, 'parent_tv': parent_tv.id, 'status': Status.IN_PROGRESS.value, 'score': 7}
```

### Step 5: Assign response = self.client.post(...)

```python
response = self.client.post(reverse('create_entry'), form_data, follow=True)
```

### Step 6: Call self.assertRedirects()

```python
self.assertRedirects(response, reverse('create_entry'))
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(Item.objects.filter(title='TV Show', media_type=MediaTypes.SEASON.value, season_number=1).exists())
```

### Step 8: Assign season = Season.objects.get(...)

```python
season = Season.objects.get(item__title='TV Show')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(season.status, Status.IN_PROGRESS.value)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(season.score, 7)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(season.user, self.user)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(season.related_tv, parent_tv)
```


## Complete Example

```python
# Workflow
'Test creating a season entry with parent TV.'
tv_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='TV Show')
parent_tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
form_data = {'title': 'TV Show', 'media_type': MediaTypes.SEASON.value, 'season_number': 1, 'parent_tv': parent_tv.id, 'status': Status.IN_PROGRESS.value, 'score': 7}
response = self.client.post(reverse('create_entry'), form_data, follow=True)
self.assertRedirects(response, reverse('create_entry'))
self.assertTrue(Item.objects.filter(title='TV Show', media_type=MediaTypes.SEASON.value, season_number=1).exists())
season = Season.objects.get(item__title='TV Show')
self.assertEqual(season.status, Status.IN_PROGRESS.value)
self.assertEqual(season.score, 7)
self.assertEqual(season.user, self.user)
self.assertEqual(season.related_tv, parent_tv)
```

## Next Steps


---

*Source: test_entry.py:92 | Complexity: Advanced | Last updated: 2026-05-22*