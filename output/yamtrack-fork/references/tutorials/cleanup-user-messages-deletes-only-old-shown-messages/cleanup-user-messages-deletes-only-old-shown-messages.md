# How To: Cleanup User Messages Deletes Only Old Shown Messages

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Delete only shown messages older than the retention window.

## Prerequisites

**Required Modules:**
- `datetime`
- `django.contrib.auth`
- `django.test`
- `django.utils`
- `app.models`
- `app.tasks`


## Step-by-Step Guide

### Step 1: 'Delete only shown messages older than the retention window.'

```python
'Delete only shown messages older than the retention window.'
```

### Step 2: Assign now = timezone.now(...)

```python
now = timezone.now()
```

### Step 3: Assign old_shown = UserMessage.objects.create(...)

```python
old_shown = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='old shown', shown_at=now - timedelta(days=31))
```

### Step 4: Assign recent_shown = UserMessage.objects.create(...)

```python
recent_shown = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='recent shown', shown_at=now - timedelta(days=5))
```

### Step 5: Assign unseen = UserMessage.objects.create(...)

```python
unseen = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='unseen')
```

### Step 6: Assign deleted_count = cleanup_user_messages(...)

```python
deleted_count = cleanup_user_messages()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(deleted_count, 1)
```

### Step 8: Call self.assertFalse()

```python
self.assertFalse(UserMessage.objects.filter(id=old_shown.id).exists())
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(UserMessage.objects.filter(id=recent_shown.id).exists())
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(UserMessage.objects.filter(id=unseen.id).exists())
```


## Complete Example

```python
# Workflow
'Delete only shown messages older than the retention window.'
now = timezone.now()
old_shown = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='old shown', shown_at=now - timedelta(days=31))
recent_shown = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='recent shown', shown_at=now - timedelta(days=5))
unseen = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='unseen')
deleted_count = cleanup_user_messages()
self.assertEqual(deleted_count, 1)
self.assertFalse(UserMessage.objects.filter(id=old_shown.id).exists())
self.assertTrue(UserMessage.objects.filter(id=recent_shown.id).exists())
self.assertTrue(UserMessage.objects.filter(id=unseen.id).exists())
```

## Next Steps


---

*Source: test_tasks.py:21 | Complexity: Advanced | Last updated: 2026-05-22*