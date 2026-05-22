# How To: Completed Progress

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: When completed, the progress should be the total number of episodes.

## Prerequisites

**Required Modules:**
- `pathlib`
- `django.contrib.auth`
- `django.test`
- `app.models`


## Step-by-Step Guide

### Step 1: 'When completed, the progress should be the total number of episodes.'

```python
'When completed, the progress should be the total number of episodes.'
```

### Step 2: Assign self.anime.status = value

```python
self.anime.status = Status.COMPLETED.value
```

### Step 3: Call self.anime.save()

```python
self.anime.save()
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).progress, 26)
```


## Complete Example

```python
# Workflow
'When completed, the progress should be the total number of episodes.'
self.anime.status = Status.COMPLETED.value
self.anime.save()
self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).progress, 26)
```

## Next Steps


---

*Source: test_media.py:39 | Complexity: Intermediate | Last updated: 2026-05-22*