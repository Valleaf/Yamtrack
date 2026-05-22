# How To: Sidebar Post Update Preferences

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test POST request to update preferences.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `django.contrib.auth`
- `django.contrib.messages`
- `django.test`
- `django.urls`
- `app.models`


## Step-by-Step Guide

### Step 1: 'Test POST request to update preferences.'

```python
'Test POST request to update preferences.'
```

### Step 2: Assign self.user.tv_enabled = True

```python
self.user.tv_enabled = True
```

### Step 3: Assign self.user.movie_enabled = True

```python
self.user.movie_enabled = True
```

### Step 4: Assign self.user.anime_enabled = True

```python
self.user.anime_enabled = True
```

### Step 5: Call self.user.save()

```python
self.user.save()
```

### Step 6: Assign response = self.client.post(...)

```python
response = self.client.post(reverse('preferences'), {'media_types_checkboxes': [MediaTypes.TV.value, MediaTypes.ANIME.value]})
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

### Step 11: Call self.assertTrue()

```python
self.assertTrue(self.user.anime_enabled)
```

### Step 12: Assign messages = list(...)

```python
messages = list(get_messages(response.wsgi_request))
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(len(messages), 1)
```

### Step 14: Call self.assertIn()

```python
self.assertIn('Settings updated', str(messages[0]))
```


## Complete Example

```python
# Workflow
'Test POST request to update preferences.'
self.user.tv_enabled = True
self.user.movie_enabled = True
self.user.anime_enabled = True
self.user.save()
response = self.client.post(reverse('preferences'), {'media_types_checkboxes': [MediaTypes.TV.value, MediaTypes.ANIME.value]})
self.assertRedirects(response, reverse('preferences'))
self.user.refresh_from_db()
self.assertTrue(self.user.tv_enabled)
self.assertFalse(self.user.movie_enabled)
self.assertTrue(self.user.anime_enabled)
messages = list(get_messages(response.wsgi_request))
self.assertEqual(len(messages), 1)
self.assertIn('Settings updated', str(messages[0]))
```

## Next Steps


---

*Source: test_sidebar.py:38 | Complexity: Advanced | Last updated: 2026-05-22*