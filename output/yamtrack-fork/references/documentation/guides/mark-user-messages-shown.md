# How To: Mark User Messages Shown

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Posting to the mark-shown endpoint should timestamp only rendered rows.

## Prerequisites

**Required Modules:**
- `django.contrib.auth`
- `django.test`
- `django.urls`
- `app.models`


## Step-by-Step Guide

### Step 1: 'Posting to the mark-shown endpoint should timestamp only rendered rows.'

```python
'Posting to the mark-shown endpoint should timestamp only rendered rows.'
```

### Step 2: Assign first_message = UserMessage.objects.create(...)

```python
first_message = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='First message')
```

### Step 3: Assign second_message = UserMessage.objects.create(...)

```python
second_message = UserMessage.objects.create(user=self.user, level=UserMessageLevel.SUCCESS, message='Second message')
```

### Step 4: Assign third_message = UserMessage.objects.create(...)

```python
third_message = UserMessage.objects.create(user=self.user, level=UserMessageLevel.WARNING, message='Third message')
```

### Step 5: Assign response = self.client.post(...)

```python
response = self.client.post(reverse('mark_user_messages_shown'), {'message_ids': [first_message.id, second_message.id]})
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 204)
```

### Step 7: Call first_message.refresh_from_db()

```python
first_message.refresh_from_db()
```

### Step 8: Call second_message.refresh_from_db()

```python
second_message.refresh_from_db()
```

### Step 9: Call third_message.refresh_from_db()

```python
third_message.refresh_from_db()
```

### Step 10: Call self.assertIsNotNone()

```python
self.assertIsNotNone(first_message.shown_at)
```

### Step 11: Call self.assertIsNotNone()

```python
self.assertIsNotNone(second_message.shown_at)
```

### Step 12: Call self.assertIsNone()

```python
self.assertIsNone(third_message.shown_at)
```


## Complete Example

```python
# Workflow
'Posting to the mark-shown endpoint should timestamp only rendered rows.'
first_message = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='First message')
second_message = UserMessage.objects.create(user=self.user, level=UserMessageLevel.SUCCESS, message='Second message')
third_message = UserMessage.objects.create(user=self.user, level=UserMessageLevel.WARNING, message='Third message')
response = self.client.post(reverse('mark_user_messages_shown'), {'message_ids': [first_message.id, second_message.id]})
self.assertEqual(response.status_code, 204)
first_message.refresh_from_db()
second_message.refresh_from_db()
third_message.refresh_from_db()
self.assertIsNotNone(first_message.shown_at)
self.assertIsNotNone(second_message.shown_at)
self.assertIsNone(third_message.shown_at)
```

## Next Steps


---

*Source: test_user_messages.py:35 | Complexity: Advanced | Last updated: 2026-05-22*