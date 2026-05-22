# How To: Manual Process Episodes

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the process_episodes function for manual episodes.

## Prerequisites

**Required Modules:**
- `json`
- `datetime`
- `pathlib`
- `unittest.mock`
- `requests`
- `django.conf`
- `django.test`
- `app.models`
- `app.providers`


## Step-by-Step Guide

### Step 1: 'Test the process_episodes function for manual episodes.'

```python
'Test the process_episodes function for manual episodes.'
```

### Step 2: Call Item.objects.create()

```python
Item.objects.create(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Process Episodes Test', image='http://example.com/process.jpg')
```

### Step 3: Call Item.objects.create()

```python
Item.objects.create(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Process Episodes Test', image='http://example.com/process_s1.jpg', season_number=1)
```

### Step 4: Assign season_metadata = value

```python
season_metadata = {'season_number': 1, 'episodes': [{'media_id': '5', 'episode_number': 1, 'air_date': '2025-01-01', 'image': 'http://example.com/process_s1e1.jpg', 'title': 'Process Episode 1'}, {'media_id': '5', 'episode_number': 2, 'air_date': '2025-01-08', 'image': 'http://example.com/process_s1e2.jpg', 'title': 'Process Episode 2'}, {'media_id': '5', 'episode_number': 3, 'air_date': '2025-01-15', 'image': 'http://example.com/process_s1e3.jpg', 'title': 'Process Episode 3'}]}
```

### Step 5: Assign ep_item1 = Item.objects.get(...)

```python
ep_item1 = Item.objects.get(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.EPISODE.value, season_number=1, episode_number=1)
```

### Step 6: Assign ep_item2 = Item.objects.get(...)

```python
ep_item2 = Item.objects.get(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.EPISODE.value, season_number=1, episode_number=2)
```

### Step 7: Assign episode_1 = Episode(...)

```python
episode_1 = Episode(item=ep_item1)
```

### Step 8: Assign episode_2 = Episode(...)

```python
episode_2 = Episode(item=ep_item2)
```

### Step 9: Assign episodes_in_db = value

```python
episodes_in_db = [episode_1, episode_2]
```

### Step 10: Assign result = manual.process_episodes(...)

```python
result = manual.process_episodes(season_metadata, episodes_in_db)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(result), 3)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(result[0]['episode_number'], 1)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(result[0]['title'], 'Process Episode 1')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(result[0]['air_date'], '2025-01-01')
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(result[0]['history'], [episode_1])
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(result[1]['episode_number'], 2)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(result[1]['title'], 'Process Episode 2')
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(result[1]['air_date'], '2025-01-08')
```

### Step 19: Call self.assertTrue()

```python
self.assertTrue(result[0]['history'], [episode_2])
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(result[2]['episode_number'], 3)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(result[2]['title'], 'Process Episode 3')
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(result[2]['air_date'], '2025-01-15')
```

### Step 23: Call self.assertFalse()

```python
self.assertFalse(result[2]['history'], [])
```

### Step 24: Call Item.objects.create()

```python
Item.objects.create(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.EPISODE.value, title=f'Process Episode {i}', image=f'http://example.com/process_s1e{i}.jpg', season_number=1, episode_number=i)
```


## Complete Example

```python
# Workflow
'Test the process_episodes function for manual episodes.'
Item.objects.create(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Process Episodes Test', image='http://example.com/process.jpg')
Item.objects.create(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Process Episodes Test', image='http://example.com/process_s1.jpg', season_number=1)
for i in range(1, 4):
    Item.objects.create(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.EPISODE.value, title=f'Process Episode {i}', image=f'http://example.com/process_s1e{i}.jpg', season_number=1, episode_number=i)
season_metadata = {'season_number': 1, 'episodes': [{'media_id': '5', 'episode_number': 1, 'air_date': '2025-01-01', 'image': 'http://example.com/process_s1e1.jpg', 'title': 'Process Episode 1'}, {'media_id': '5', 'episode_number': 2, 'air_date': '2025-01-08', 'image': 'http://example.com/process_s1e2.jpg', 'title': 'Process Episode 2'}, {'media_id': '5', 'episode_number': 3, 'air_date': '2025-01-15', 'image': 'http://example.com/process_s1e3.jpg', 'title': 'Process Episode 3'}]}
ep_item1 = Item.objects.get(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.EPISODE.value, season_number=1, episode_number=1)
ep_item2 = Item.objects.get(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.EPISODE.value, season_number=1, episode_number=2)
episode_1 = Episode(item=ep_item1)
episode_2 = Episode(item=ep_item2)
episodes_in_db = [episode_1, episode_2]
result = manual.process_episodes(season_metadata, episodes_in_db)
self.assertEqual(len(result), 3)
self.assertEqual(result[0]['episode_number'], 1)
self.assertEqual(result[0]['title'], 'Process Episode 1')
self.assertEqual(result[0]['air_date'], '2025-01-01')
self.assertTrue(result[0]['history'], [episode_1])
self.assertEqual(result[1]['episode_number'], 2)
self.assertEqual(result[1]['title'], 'Process Episode 2')
self.assertEqual(result[1]['air_date'], '2025-01-08')
self.assertTrue(result[0]['history'], [episode_2])
self.assertEqual(result[2]['episode_number'], 3)
self.assertEqual(result[2]['title'], 'Process Episode 3')
self.assertEqual(result[2]['air_date'], '2025-01-15')
self.assertFalse(result[2]['history'], [])
```

## Next Steps


---

*Source: test_metadata.py:538 | Complexity: Advanced | Last updated: 2026-05-22*