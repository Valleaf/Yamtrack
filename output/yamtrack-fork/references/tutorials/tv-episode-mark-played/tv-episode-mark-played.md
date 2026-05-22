# How To: Tv Episode Mark Played

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test webhook handles TV episode mark played event.

## Prerequisites

**Required Modules:**
- `json`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `django.urls`
- `app.models`
- `integrations.webhooks.jellyfin`


## Step-by-Step Guide

### Step 1: 'Test webhook handles TV episode mark played event.'

```python
'Test webhook handles TV episode mark played event.'
```

### Step 2: Assign payload = value

```python
payload = {'Event': 'Stop', 'Item': {'Type': 'Episode', 'Name': 'The One Where Monica Gets a Roommate', 'ProviderIds': {'Tvdb': '303821', 'Imdb': 'tt0583459'}, 'SeriesName': 'Friends', 'ParentIndexNumber': 1, 'IndexNumber': 1, 'UserData': {'Played': True}}}
```

### Step 3: Assign response = self.client.post(...)

```python
response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 5: Assign tv_item = Item.objects.get(...)

```python
tv_item = Item.objects.get(media_type=MediaTypes.TV.value, media_id='1668')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(tv_item.title, 'Friends')
```

### Step 7: Assign tv = TV.objects.get(...)

```python
tv = TV.objects.get(item=tv_item, user=self.user)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(tv.status, Status.IN_PROGRESS.value)
```

### Step 9: Assign season = Season.objects.get(...)

```python
season = Season.objects.get(item__media_id='1668', item__season_number=1)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(season.status, Status.IN_PROGRESS.value)
```

### Step 11: Assign episode = Episode.objects.get(...)

```python
episode = Episode.objects.get(item__media_id='1668', item__season_number=1, item__episode_number=1)
```

### Step 12: Call self.assertIsNotNone()

```python
self.assertIsNotNone(episode.end_date)
```


## Complete Example

```python
# Workflow
'Test webhook handles TV episode mark played event.'
payload = {'Event': 'Stop', 'Item': {'Type': 'Episode', 'Name': 'The One Where Monica Gets a Roommate', 'ProviderIds': {'Tvdb': '303821', 'Imdb': 'tt0583459'}, 'SeriesName': 'Friends', 'ParentIndexNumber': 1, 'IndexNumber': 1, 'UserData': {'Played': True}}}
response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
self.assertEqual(response.status_code, 200)
tv_item = Item.objects.get(media_type=MediaTypes.TV.value, media_id='1668')
self.assertEqual(tv_item.title, 'Friends')
tv = TV.objects.get(item=tv_item, user=self.user)
self.assertEqual(tv.status, Status.IN_PROGRESS.value)
season = Season.objects.get(item__media_id='1668', item__season_number=1)
self.assertEqual(season.status, Status.IN_PROGRESS.value)
episode = Episode.objects.get(item__media_id='1668', item__season_number=1, item__episode_number=1)
self.assertIsNotNone(episode.end_date)
```

## Next Steps


---

*Source: test_webhooks_jellyfin.py:28 | Complexity: Advanced | Last updated: 2026-05-22*