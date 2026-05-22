# How To: Create Entry Post Duplicate Item

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test creating a duplicate item.

## Prerequisites

**Required Modules:**
- `django.contrib.auth`
- `django.db`
- `django.test`
- `django.urls`
- `django.utils`
- `app.models`


## Step-by-Step Guide

### Step 1: 'Test creating a duplicate item.'

```python
'Test creating a duplicate item.'
```

### Step 2: Assign tv_item = Item.objects.create(...)

```python
tv_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='TV Show')
```

### Step 3: Assign parent_tv = TV.objects.create(...)

```python
parent_tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
```

### Step 4: Assign season_item = Item.objects.create(...)

```python
season_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='TV Show', season_number=1)
```

### Step 5: Call Season.objects.create()

```python
Season.objects.create(item=season_item, user=self.user, related_tv=parent_tv, status=Status.IN_PROGRESS.value)
```

### Step 6: Assign initial_count = Item.objects.count(...)

```python
initial_count = Item.objects.count()
```

### Step 7: Assign form_data = value

```python
form_data = {'title': 'TV Show', 'media_type': MediaTypes.SEASON.value, 'season_number': 1, 'parent_tv': parent_tv.id, 'status': Status.IN_PROGRESS.value, 'score': 7, 'repeats': 0}
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(Item.objects.count(), initial_count)
```

### Step 9: Call self.client.post()

```python
self.client.post(reverse('create_entry'), form_data)
```


## Complete Example

```python
# Workflow
'Test creating a duplicate item.'
tv_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='TV Show')
parent_tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
season_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='TV Show', season_number=1)
Season.objects.create(item=season_item, user=self.user, related_tv=parent_tv, status=Status.IN_PROGRESS.value)
initial_count = Item.objects.count()
form_data = {'title': 'TV Show', 'media_type': MediaTypes.SEASON.value, 'season_number': 1, 'parent_tv': parent_tv.id, 'status': Status.IN_PROGRESS.value, 'score': 7, 'repeats': 0}
with transaction.atomic():
    self.client.post(reverse('create_entry'), form_data)
self.assertEqual(Item.objects.count(), initial_count)
```

## Next Steps


---

*Source: test_entry.py:188 | Complexity: Advanced | Last updated: 2026-05-22*