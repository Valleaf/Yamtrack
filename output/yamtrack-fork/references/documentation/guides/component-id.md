# How To: Component Id

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the component_id tag.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `django.test`
- `django.urls`
- `django.utils`
- `app.models`
- `app.templatetags`


## Step-by-Step Guide

### Step 1: 'Test the component_id tag.'

```python
'Test the component_id tag.'
```

### Step 2: Assign tv_id = app_tags.component_id(...)

```python
tv_id = app_tags.component_id('card', self.tv_item)
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(tv_id, 'card-tv-1668')
```

### Step 4: Assign tv_dict_id = app_tags.component_id(...)

```python
tv_dict_id = app_tags.component_id('card', self.tv_dict)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(tv_dict_id, 'card-tv-1668')
```

### Step 6: Assign season_id = app_tags.component_id(...)

```python
season_id = app_tags.component_id('card', self.season_item)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(season_id, 'card-season-1668-1')
```

### Step 8: Assign season_dict_id = app_tags.component_id(...)

```python
season_dict_id = app_tags.component_id('card', self.season_dict)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(season_dict_id, 'card-season-1668-1')
```

### Step 10: Assign episode_id = app_tags.component_id(...)

```python
episode_id = app_tags.component_id('card', self.episode_item)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(episode_id, 'card-episode-1668-1-1')
```

### Step 12: Assign episode_dict_id = app_tags.component_id(...)

```python
episode_dict_id = app_tags.component_id('card', self.episode_dict)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(episode_dict_id, 'card-episode-1668-1-1')
```


## Complete Example

```python
# Workflow
'Test the component_id tag.'
tv_id = app_tags.component_id('card', self.tv_item)
self.assertEqual(tv_id, 'card-tv-1668')
tv_dict_id = app_tags.component_id('card', self.tv_dict)
self.assertEqual(tv_dict_id, 'card-tv-1668')
season_id = app_tags.component_id('card', self.season_item)
self.assertEqual(season_id, 'card-season-1668-1')
season_dict_id = app_tags.component_id('card', self.season_dict)
self.assertEqual(season_dict_id, 'card-season-1668-1')
episode_id = app_tags.component_id('card', self.episode_item)
self.assertEqual(episode_id, 'card-episode-1668-1-1')
episode_dict_id = app_tags.component_id('card', self.episode_dict)
self.assertEqual(episode_dict_id, 'card-episode-1668-1-1')
```

## Next Steps


---

*Source: test_templatetags.py:321 | Complexity: Advanced | Last updated: 2026-05-22*