# How To: Sidebar Post Demo User

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test POST request from a demo user to preferences.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `django.contrib.auth`
- `django.contrib.messages`
- `django.test`
- `django.urls`
- `app.models`


## Step-by-Step Guide

### Step 1: 'Test POST request from a demo user to preferences.'

```python
'Test POST request from a demo user to preferences.'
```

### Step 2: Assign self.user.is_demo = True

```python
self.user.is_demo = True
```

### Step 3: Assign self.user.tv_enabled = True

```python
self.user.tv_enabled = True
```

### Step 4: Assign self.user.movie_enabled = False

```python
self.user.movie_enabled = False
```

### Step 5: Call self.user.save()

```python
self.user.save()
```

### Step 6: Assign response = self.client.post(...)

```python
response = self.client.post(reverse('preferences'), {'media_types_checkboxes': [MediaTypes.TV.value, MediaTypes.MOVIE.value]})
```

### Step 7: Call self.assertRedirects()

```python
self.assertRedirects(response, reverse('preferences'))
```

### Step 8: Call self.user.refresh_from_db()

```python
self.user.refresh_from_db()
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(self.user.tv_enabled)
```

### Step 10: Call self.assertFalse()

```python
self.assertFalse(self.user.movie_enabled)
```

### Step 11: Assign messages = list(...)

```python
messages = list(get_messages(response.wsgi_request))
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(len(messages), 1)
```

### Step 13: Call self.assertIn()

```python
self.assertIn('view-only for demo accounts', str(messages[0]))
```


## Complete Example

```python
# Workflow
'Test POST request from a demo user to preferences.'
self.user.is_demo = True
self.user.tv_enabled = True
self.user.movie_enabled = False
self.user.save()
response = self.client.post(reverse('preferences'), {'media_types_checkboxes': [MediaTypes.TV.value, MediaTypes.MOVIE.value]})
self.assertRedirects(response, reverse('preferences'))
self.user.refresh_from_db()
self.assertTrue(self.user.tv_enabled)
self.assertFalse(self.user.movie_enabled)
messages = list(get_messages(response.wsgi_request))
self.assertEqual(len(messages), 1)
self.assertIn('view-only for demo accounts', str(messages[0]))
```

## Next Steps


---

*Source: test_sidebar.py:62 | Complexity: Advanced | Last updated: 2026-05-22*