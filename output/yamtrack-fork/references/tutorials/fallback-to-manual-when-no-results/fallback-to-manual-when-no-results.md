# How To: Fallback To Manual When No Results

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test fallback to manual when no results

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
mock_search.return_value = {'results': []}
```

### Step 2: Assign csv = self._csv(...)

```python
csv = self._csv([['Obscure Film XYZ', 2023, 7, '2024-01-01', '', 'movie']])
```

### Step 3: Assign importer = SensCritiqueCSVImporter(...)

```python
importer = SensCritiqueCSVImporter(self.user)
```

### Step 4: Call importer.run()

```python
importer.run(csv)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(importer.imported, 1)
```

### Step 6: Assign movie = Movie.objects.get(...)

```python
movie = Movie.objects.get(user=self.user)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(movie.item.source, 'manual')
```


## Complete Example

```python
# Setup
# Fixtures: mock_search

# Workflow
mock_search.return_value = {'results': []}
csv = self._csv([['Obscure Film XYZ', 2023, 7, '2024-01-01', '', 'movie']])
importer = SensCritiqueCSVImporter(self.user)
importer.run(csv)
self.assertEqual(importer.imported, 1)
movie = Movie.objects.get(user=self.user)
self.assertEqual(movie.item.source, 'manual')
```

## Next Steps


---

*Source: test_senscritique.py:100 | Complexity: Intermediate | Last updated: 2026-05-22*