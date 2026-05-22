# How To: Import Movie

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test import movie

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

### Step 2: Assign csv = self._csv(...)

```python
csv = self._csv([['Inception', 2010, 9, '2024-01-01', '', 'movie']])
```

### Step 3: Assign importer = SensCritiqueCSVImporter(...)

```python
importer = SensCritiqueCSVImporter(self.user)
```

### Step 4: Assign result = importer.run(...)

```python
result = importer.run(csv)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(importer.imported, 1)
```

### Step 6: Call self.assertIn()

```python
self.assertIn('1 imported', result)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```


## Complete Example

```python
# Setup
# Fixtures: mock_search

# Workflow
mock_search.return_value = {'results': [{'media_id': '550', 'title': 'Inception', 'year': 2010}]}
csv = self._csv([['Inception', 2010, 9, '2024-01-01', '', 'movie']])
importer = SensCritiqueCSVImporter(self.user)
result = importer.run(csv)
self.assertEqual(importer.imported, 1)
self.assertIn('1 imported', result)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```

## Next Steps


---

*Source: test_senscritique.py:49 | Complexity: Intermediate | Last updated: 2026-05-22*