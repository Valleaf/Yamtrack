# How To: Tmdb Find Next Episode

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the find_next_episode function.

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

### Step 1: 'Test the find_next_episode function.'

```python
'Test the find_next_episode function.'
```

### Step 2: Assign episodes_metadata = value

```python
episodes_metadata = [{'episode_number': 1, 'title': 'Episode 1'}, {'episode_number': 2, 'title': 'Episode 2'}, {'episode_number': 3, 'title': 'Episode 3'}]
```

### Step 3: Assign next_episode = tmdb.find_next_episode(...)

```python
next_episode = tmdb.find_next_episode(1, episodes_metadata)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(next_episode, 2)
```

### Step 5: Assign next_episode = tmdb.find_next_episode(...)

```python
next_episode = tmdb.find_next_episode(3, episodes_metadata)
```

### Step 6: Call self.assertIsNone()

```python
self.assertIsNone(next_episode)
```

### Step 7: Assign next_episode = tmdb.find_next_episode(...)

```python
next_episode = tmdb.find_next_episode(5, episodes_metadata)
```

### Step 8: Call self.assertIsNone()

```python
self.assertIsNone(next_episode)
```


## Complete Example

```python
# Workflow
'Test the find_next_episode function.'
episodes_metadata = [{'episode_number': 1, 'title': 'Episode 1'}, {'episode_number': 2, 'title': 'Episode 2'}, {'episode_number': 3, 'title': 'Episode 3'}]
next_episode = tmdb.find_next_episode(1, episodes_metadata)
self.assertEqual(next_episode, 2)
next_episode = tmdb.find_next_episode(3, episodes_metadata)
self.assertIsNone(next_episode)
next_episode = tmdb.find_next_episode(5, episodes_metadata)
self.assertIsNone(next_episode)
```

## Next Steps


---

*Source: test_metadata.py:296 | Complexity: Advanced | Last updated: 2026-05-22*