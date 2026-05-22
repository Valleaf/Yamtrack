# How To: Deduplication Skips Existing

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test deduplication skips existing

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest.mock`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `app.models`
- `integrations.imports.senscritique`

**Setup Required:**
```python
# Fixtures: mock_search
```

## Step-by-Step Guide

### Step 1: Assign mock_search.return_value = value

```python
mock_search.return_value = {'results': [{'media_id': '550', 'title': 'Inception', 'year': 2010}]}
```

### Step 2: Assign item = Item.objects.create(...)

```python
item = Item.objects.create(media_id='550', source='tmdb', media_type='movie', title='Inception', image='')
```

### Step 3: Call Movie.objects.create()

```python
Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)
```

### Step 4: Assign csv = self._csv(...)

```python
csv = self._csv([['Inception', 2010, 9, '2024-01-01', '', 'movie']])
```

### Step 5: Assign importer = SensCritiqueCSVImporter(...)

```python
importer = SensCritiqueCSVImporter(self.user)
```

### Step 6: Call importer.run()

```python
importer.run(csv)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(importer.skipped, 1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```


## Complete Example

```python
# Setup
# Fixtures: mock_search

# Workflow
mock_search.return_value = {'results': [{'media_id': '550', 'title': 'Inception', 'year': 2010}]}
item = Item.objects.create(media_id='550', source='tmdb', media_type='movie', title='Inception', image='')
Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)
csv = self._csv([['Inception', 2010, 9, '2024-01-01', '', 'movie']])
importer = SensCritiqueCSVImporter(self.user)
importer.run(csv)
self.assertEqual(importer.skipped, 1)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```

## Next Steps


---

*Source: test_senscritique.py:110 | Complexity: Advanced | Last updated: 2026-05-22*