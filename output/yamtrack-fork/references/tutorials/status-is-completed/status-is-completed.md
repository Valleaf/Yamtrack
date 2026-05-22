# How To: Status Is Completed

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test status is completed

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest.mock`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `app.models`
- `integrations.imports.filmaffinity`
- `lists.models`
- `lists.models`
- `lists.models`

**Setup Required:**
```python
# Fixtures: mock_resolve
```

## Step-by-Step Guide

### Step 1: Assign mock_resolve.return_value = value

```python
mock_resolve.return_value = ('550', 'tmdb', 'movie')
```

### Step 2: Call FilmAffinityRatingsImporter.run()

```python
FilmAffinityRatingsImporter(self.user).run(RATINGS_HTML)
```

### Step 3: Assign movie = Movie.objects.filter.first(...)

```python
movie = Movie.objects.filter(user=self.user).first()
```

### Step 4: Call self.assertIsNotNone()

```python
self.assertIsNotNone(movie)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(movie.status, Status.COMPLETED.value)
```


## Complete Example

```python
# Setup
# Fixtures: mock_resolve

# Workflow
mock_resolve.return_value = ('550', 'tmdb', 'movie')
FilmAffinityRatingsImporter(self.user).run(RATINGS_HTML)
movie = Movie.objects.filter(user=self.user).first()
self.assertIsNotNone(movie)
self.assertEqual(movie.status, Status.COMPLETED.value)
```

## Next Steps


---

*Source: test_filmaffinity.py:177 | Complexity: Intermediate | Last updated: 2026-05-22*