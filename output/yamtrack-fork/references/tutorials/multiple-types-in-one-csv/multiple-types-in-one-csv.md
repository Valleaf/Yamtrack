# How To: Multiple Types In One Csv

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test multiple types in one csv

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
mock_search.return_value = {'results': [{'media_id': '1', 'title': 'X', 'year': 2020}]}
```

### Step 2: Assign rows = value

```python
rows = [['Film A', 2020, 8, '2024-01-01', '', 'movie'], ['Show B', 2020, 7, '2024-01-01', '', 'tv'], ['Album C', 2020, 9, '2024-01-01', '', 'music']]
```

### Step 3: Assign csv = self._csv(...)

```python
csv = self._csv(rows)
```

### Step 4: Assign importer = SensCritiqueCSVImporter(...)

```python
importer = SensCritiqueCSVImporter(self.user)
```

### Step 5: Call importer.run()

```python
importer.run(csv)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(importer.imported, 3)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(TV.objects.filter(user=self.user).count(), 1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(Music.objects.filter(user=self.user).count(), 1)
```


## Complete Example

```python
# Setup
# Fixtures: mock_search

# Workflow
mock_search.return_value = {'results': [{'media_id': '1', 'title': 'X', 'year': 2020}]}
rows = [['Film A', 2020, 8, '2024-01-01', '', 'movie'], ['Show B', 2020, 7, '2024-01-01', '', 'tv'], ['Album C', 2020, 9, '2024-01-01', '', 'music']]
csv = self._csv(rows)
importer = SensCritiqueCSVImporter(self.user)
importer.run(csv)
self.assertEqual(importer.imported, 3)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
self.assertEqual(TV.objects.filter(user=self.user).count(), 1)
self.assertEqual(Music.objects.filter(user=self.user).count(), 1)
```

## Next Steps


---

*Source: test_senscritique.py:166 | Complexity: Advanced | Last updated: 2026-05-22*