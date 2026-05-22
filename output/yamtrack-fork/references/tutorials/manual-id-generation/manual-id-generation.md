# How To: Manual Id Generation

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that unique manual IDs are generated.

## Prerequisites

**Required Modules:**
- `django.conf`
- `django.contrib.auth`
- `django.test`
- `app.forms`
- `app.models`


## Step-by-Step Guide

### Step 1: 'Test that unique manual IDs are generated.'

```python
'Test that unique manual IDs are generated.'
```

### Step 2: Assign form1 = ManualItemForm(...)

```python
form1 = ManualItemForm(data={'media_type': MediaTypes.ANIME.value, 'title': 'Test Anime 1'}, user=self.user)
```

### Step 3: Call self.assertTrue()

```python
self.assertTrue(form1.is_valid())
```

### Step 4: Assign item1 = form1.save(...)

```python
item1 = form1.save()
```

### Step 5: Assign form2 = ManualItemForm(...)

```python
form2 = ManualItemForm(data={'media_type': MediaTypes.ANIME.value, 'title': 'Test Anime 2'}, user=self.user)
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(form2.is_valid())
```

### Step 7: Assign item2 = form2.save(...)

```python
item2 = form2.save()
```

### Step 8: Call self.assertNotEqual()

```python
self.assertNotEqual(item1.media_id, item2.media_id)
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(item1.media_id)
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(item2.media_id)
```


## Complete Example

```python
# Workflow
'Test that unique manual IDs are generated.'
form1 = ManualItemForm(data={'media_type': MediaTypes.ANIME.value, 'title': 'Test Anime 1'}, user=self.user)
self.assertTrue(form1.is_valid())
item1 = form1.save()
form2 = ManualItemForm(data={'media_type': MediaTypes.ANIME.value, 'title': 'Test Anime 2'}, user=self.user)
self.assertTrue(form2.is_valid())
item2 = form2.save()
self.assertNotEqual(item1.media_id, item2.media_id)
self.assertTrue(item1.media_id)
self.assertTrue(item2.media_id)
```

## Next Steps


---

*Source: test_forms.py:461 | Complexity: Advanced | Last updated: 2026-05-22*