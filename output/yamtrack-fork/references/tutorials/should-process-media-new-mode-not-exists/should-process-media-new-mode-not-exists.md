# How To: Should Process Media New Mode Not Exists

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test should_process_media in new mode when media doesn't exist.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `collections`
- `django.contrib.auth`
- `django.test`
- `app.models`
- `integrations.imports.helpers`


## Step-by-Step Guide

### Step 1: "Test should_process_media in new mode when media doesn't exist."

```python
"Test should_process_media in new mode when media doesn't exist."
```

### Step 2: Assign existing_media = defaultdict(...)

```python
existing_media = defaultdict(lambda: defaultdict(dict))
```

### Step 3: Assign to_delete = defaultdict(...)

```python
to_delete = defaultdict(lambda: defaultdict(set))
```

### Step 4: Assign result = should_process_media(...)

```python
result = should_process_media(existing_media, to_delete, media_type=MediaTypes.MOVIE.value, source=Sources.TMDB.value, media_id='238', mode='new')
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(result)
```


## Complete Example

```python
# Workflow
"Test should_process_media in new mode when media doesn't exist."
existing_media = defaultdict(lambda: defaultdict(dict))
to_delete = defaultdict(lambda: defaultdict(set))
result = should_process_media(existing_media, to_delete, media_type=MediaTypes.MOVIE.value, source=Sources.TMDB.value, media_id='238', mode='new')
self.assertTrue(result)
```

## Next Steps


---

*Source: test_import_helpers.py:116 | Complexity: Intermediate | Last updated: 2026-05-22*