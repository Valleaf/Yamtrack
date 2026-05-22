# How To: Obfuscate Unseen Episodes Post Demo User

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that demo users cannot update obfuscate_unseen_episodes.

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `django.contrib.auth`
- `django.contrib.messages`
- `django.test`
- `django.urls`
- `app.models`


## Step-by-Step Guide

### Step 1: 'Test that demo users cannot update obfuscate_unseen_episodes.'

```python
'Test that demo users cannot update obfuscate_unseen_episodes.'
```

### Step 2: Assign self.user.is_demo = True

```python
self.user.is_demo = True
```

### Step 3: Assign self.user.obfuscate_unseen_episodes = False

```python
self.user.obfuscate_unseen_episodes = False
```

### Step 4: Call self.user.save()

```python
self.user.save()
```

### Step 5: Assign response = self.client.post(...)

```python
response = self.client.post(reverse('preferences'), {'obfuscate_unseen_episodes': 'on', 'media_types_checkboxes': [MediaTypes.TV.value]})
```

### Step 6: Call self.assertRedirects()

```python
self.assertRedirects(response, reverse('preferences'))
```

### Step 7: Call self.user.refresh_from_db()

```python
self.user.refresh_from_db()
```

### Step 8: Call self.assertFalse()

```python
self.assertFalse(self.user.obfuscate_unseen_episodes)
```

### Step 9: Assign messages = list(...)

```python
messages = list(get_messages(response.wsgi_request))
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(len(messages), 1)
```

### Step 11: Call self.assertIn()

```python
self.assertIn('view-only for demo accounts', str(messages[0]))
```


## Complete Example

```python
# Workflow
'Test that demo users cannot update obfuscate_unseen_episodes.'
self.user.is_demo = True
self.user.obfuscate_unseen_episodes = False
self.user.save()
response = self.client.post(reverse('preferences'), {'obfuscate_unseen_episodes': 'on', 'media_types_checkboxes': [MediaTypes.TV.value]})
self.assertRedirects(response, reverse('preferences'))
self.user.refresh_from_db()
self.assertFalse(self.user.obfuscate_unseen_episodes)
messages = list(get_messages(response.wsgi_request))
self.assertEqual(len(messages), 1)
self.assertIn('view-only for demo accounts', str(messages[0]))
```

## Next Steps


---

*Source: test_sidebar.py:146 | Complexity: Advanced | Last updated: 2026-05-22*