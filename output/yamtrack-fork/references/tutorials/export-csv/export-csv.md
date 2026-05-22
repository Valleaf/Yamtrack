# How To: Export Csv

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Basic test exporting media to CSV.

## Prerequisites

**Required Modules:**
- `csv`
- `datetime`
- `io`
- `django.contrib.auth`
- `django.db.models`
- `django.test`
- `django.urls`
- `app.models`


## Step-by-Step Guide

### Step 1: 'Basic test exporting media to CSV.'

```python
'Basic test exporting media to CSV.'
```

### Step 2: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('export_csv'))
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(response['Content-Type'], 'text/csv')
```

### Step 5: Assign content = unknown.join.decode(...)

```python
content = b''.join(response.streaming_content).decode('utf-8')
```

### Step 6: Assign reader = csv.DictReader(...)

```python
reader = csv.DictReader(StringIO(content))
```

### Step 7: Assign db_media_ids = set(...)

```python
db_media_ids = set(Item.objects.filter(Q(tv__user=self.user) | Q(movie__user=self.user) | Q(season__user=self.user) | Q(episode__related_season__user=self.user) | Q(anime__user=self.user) | Q(manga__user=self.user) | Q(game__user=self.user) | Q(book__user=self.user)).values_list('media_id', flat=True))
```

### Step 8: Assign media_id = value

```python
media_id = row['media_id']
```

### Step 9: Call self.assertIn()

```python
self.assertIn(media_id, db_media_ids)
```


## Complete Example

```python
# Workflow
'Basic test exporting media to CSV.'
response = self.client.get(reverse('export_csv'))
self.assertEqual(response.status_code, 200)
self.assertEqual(response['Content-Type'], 'text/csv')
content = b''.join(response.streaming_content).decode('utf-8')
reader = csv.DictReader(StringIO(content))
db_media_ids = set(Item.objects.filter(Q(tv__user=self.user) | Q(movie__user=self.user) | Q(season__user=self.user) | Q(episode__related_season__user=self.user) | Q(anime__user=self.user) | Q(manga__user=self.user) | Q(game__user=self.user) | Q(book__user=self.user)).values_list('media_id', flat=True))
for row in reader:
    media_id = row['media_id']
    self.assertIn(media_id, db_media_ids)
```

## Next Steps


---

*Source: test_exports.py:143 | Complexity: Advanced | Last updated: 2026-05-22*