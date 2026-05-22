# How To: Type Label With Secondary Types

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test type label with secondary types

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest.mock`
- `django.test`
- `app.models`
- `django.core.cache`
- `app.providers.musicbrainz`

**Setup Required:**
```python
# Fixtures: mock_get
```

## Step-by-Step Guide

### Step 1: Assign rg = _mock_release_group(...)

```python
rg = _mock_release_group(mb_id='compilation-unique-id')
```

### Step 2: Assign unknown = value

```python
rg['secondary-types'] = ['Compilation']
```

### Step 3: Assign mock_get.return_value = value

```python
mock_get.return_value = {'release-group-count': 1, 'release-groups': [rg]}
```

### Step 4: Assign result = search_music(...)

```python
result = search_music('Beatles secondary types unique query xyz')
```

### Step 5: Call self.assertIn()

```python
self.assertIn('Compilation', result['results'][0]['type'])
```


## Complete Example

```python
# Setup
# Fixtures: mock_get

# Workflow
rg = _mock_release_group(mb_id='compilation-unique-id')
rg['secondary-types'] = ['Compilation']
mock_get.return_value = {'release-group-count': 1, 'release-groups': [rg]}
result = search_music('Beatles secondary types unique query xyz')
self.assertIn('Compilation', result['results'][0]['type'])
```

## Next Steps


---

*Source: test_musicbrainz.py:175 | Complexity: Intermediate | Last updated: 2026-05-22*