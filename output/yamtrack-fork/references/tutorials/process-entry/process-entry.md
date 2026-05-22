# How To: Process Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test processing an entry from Kitsu.

## Prerequisites

**Required Modules:**
- `json`
- `datetime`
- `pathlib`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `app.models`
- `integrations.imports`


## Step-by-Step Guide

### Step 1: 'Test processing an entry from Kitsu.'

```python
'Test processing an entry from Kitsu.'
```

### Step 2: Assign entry = value

```python
entry = self.sample_anime_response['data'][0]
```

### Step 3: Assign media_lookup = value

```python
media_lookup = {item['id']: item for item in self.sample_anime_response['included'] if item['type'] == 'anime'}
```

### Step 4: Assign mapping_lookup = value

```python
mapping_lookup = {item['id']: item for item in self.sample_anime_response['included'] if item['type'] == 'mappings'}
```

### Step 5: Call self.importer._process_entry()

```python
self.importer._process_entry(entry, MediaTypes.ANIME.value, media_lookup, mapping_lookup)
```

### Step 6: Assign instance = value

```python
instance = self.importer.bulk_media[MediaTypes.ANIME.value][0]
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(instance.item.media_id, '1')
```

### Step 8: Call self.assertIsInstance()

```python
self.assertIsInstance(instance, Anime)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(instance.score, 9)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(instance.progress, 26)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(instance.status, Status.COMPLETED.value)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(instance.notes, 'Great series!')
```


## Complete Example

```python
# Workflow
'Test processing an entry from Kitsu.'
entry = self.sample_anime_response['data'][0]
media_lookup = {item['id']: item for item in self.sample_anime_response['included'] if item['type'] == 'anime'}
mapping_lookup = {item['id']: item for item in self.sample_anime_response['included'] if item['type'] == 'mappings'}
self.importer._process_entry(entry, MediaTypes.ANIME.value, media_lookup, mapping_lookup)
instance = self.importer.bulk_media[MediaTypes.ANIME.value][0]
self.assertEqual(instance.item.media_id, '1')
self.assertIsInstance(instance, Anime)
self.assertEqual(instance.score, 9)
self.assertEqual(instance.progress, 26)
self.assertEqual(instance.status, Status.COMPLETED.value)
self.assertEqual(instance.notes, 'Great series!')
```

## Next Steps


---

*Source: test_kitsu.py:88 | Complexity: Advanced | Last updated: 2026-05-22*