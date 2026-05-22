# How To: Home View

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the home view displays in-progress and planning media.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `django.urls`
- `django.utils`
- `app.models`
- `users.models`


## Step-by-Step Guide

### Step 1: 'Test the home view displays in-progress and planning media.'

```python
'Test the home view displays in-progress and planning media.'
```

### Step 2: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('home'))
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 4: Call self.assertTemplateUsed()

```python
self.assertTemplateUsed(response, 'app/home.html')
```

### Step 5: Call self.assertIn()

```python
self.assertIn('home_sections', response.context)
```

### Step 6: Assign sections_by_key = value

```python
sections_by_key = {section['key']: section for section in response.context['home_sections']}
```

### Step 7: Call self.assertIn()

```python
self.assertIn(Status.IN_PROGRESS.value, sections_by_key)
```

### Step 8: Call self.assertIn()

```python
self.assertIn(Status.PLANNING.value, sections_by_key)
```

### Step 9: Assign in_progress_section = value

```python
in_progress_section = sections_by_key[Status.IN_PROGRESS.value]
```

### Step 10: Assign planning_section = value

```python
planning_section = sections_by_key[Status.PLANNING.value]
```

### Step 11: Call self.assertIn()

```python
self.assertIn(MediaTypes.SEASON.value, in_progress_section['media_types'])
```

### Step 12: Call self.assertIn()

```python
self.assertIn(MediaTypes.ANIME.value, in_progress_section['media_types'])
```

### Step 13: Call self.assertIn()

```python
self.assertIn(MediaTypes.MOVIE.value, planning_section['media_types'])
```

### Step 14: Call self.assertIn()

```python
self.assertIn('sort_choices', response.context)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(response.context['sort_choices'], HomeSortChoices.choices)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(in_progress_section['count'], 2)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(planning_section['count'], 1)
```

### Step 18: Assign season = value

```python
season = in_progress_section['media_types'][MediaTypes.SEASON.value]
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(len(season['items']), 1)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(season['items'][0].progress, 5)
```

### Step 21: Assign planning_movies = value

```python
planning_movies = planning_section['media_types'][MediaTypes.MOVIE.value]
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(len(planning_movies['items']), 1)
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(planning_movies['items'][0].status, Status.PLANNING.value)
```


## Complete Example

```python
# Workflow
'Test the home view displays in-progress and planning media.'
response = self.client.get(reverse('home'))
self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/home.html')
self.assertIn('home_sections', response.context)
sections_by_key = {section['key']: section for section in response.context['home_sections']}
self.assertIn(Status.IN_PROGRESS.value, sections_by_key)
self.assertIn(Status.PLANNING.value, sections_by_key)
in_progress_section = sections_by_key[Status.IN_PROGRESS.value]
planning_section = sections_by_key[Status.PLANNING.value]
self.assertIn(MediaTypes.SEASON.value, in_progress_section['media_types'])
self.assertIn(MediaTypes.ANIME.value, in_progress_section['media_types'])
self.assertIn(MediaTypes.MOVIE.value, planning_section['media_types'])
self.assertIn('sort_choices', response.context)
self.assertEqual(response.context['sort_choices'], HomeSortChoices.choices)
self.assertEqual(in_progress_section['count'], 2)
self.assertEqual(planning_section['count'], 1)
season = in_progress_section['media_types'][MediaTypes.SEASON.value]
self.assertEqual(len(season['items']), 1)
self.assertEqual(season['items'][0].progress, 5)
planning_movies = planning_section['media_types'][MediaTypes.MOVIE.value]
self.assertEqual(len(planning_movies['items']), 1)
self.assertEqual(planning_movies['items'][0].status, Status.PLANNING.value)
```

## Next Steps


---

*Source: test_home.py:160 | Complexity: Advanced | Last updated: 2026-05-22*