# How To: Calendar With Invalid Month Year

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test the calendar view with invalid month and year parameters.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `calendar`
- `datetime`
- `unittest.mock`
- `django.contrib.auth`
- `django.contrib.messages`
- `django.test`
- `django.urls`
- `django.utils`
- `app.models`
- `events.models`

**Setup Required:**
```python
# Fixtures: mock_update_preference, mock_get_user_events
```

## Step-by-Step Guide

### Step 1: 'Test the calendar view with invalid month and year parameters.'

```python
'Test the calendar view with invalid month and year parameters.'
```

### Step 2: Assign mock_update_preference.return_value = 'month'

```python
mock_update_preference.return_value = 'month'
```

### Step 3: Assign mock_get_user_events.return_value = value

```python
mock_get_user_events.return_value = []
```

### Step 4: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('calendar') + '?month=invalid&year=invalid')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 6: Call self.assertTemplateUsed()

```python
self.assertTemplateUsed(response, 'events/calendar.html')
```

### Step 7: Assign today = timezone.localdate(...)

```python
today = timezone.localdate()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(response.context['month'], today.month)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(response.context['year'], today.year)
```


## Complete Example

```python
# Setup
# Fixtures: mock_update_preference, mock_get_user_events

# Workflow
'Test the calendar view with invalid month and year parameters.'
mock_update_preference.return_value = 'month'
mock_get_user_events.return_value = []
response = self.client.get(reverse('calendar') + '?month=invalid&year=invalid')
self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'events/calendar.html')
today = timezone.localdate()
self.assertEqual(response.context['month'], today.month)
self.assertEqual(response.context['year'], today.year)
```

## Next Steps


---

*Source: test_views.py:132 | Complexity: Advanced | Last updated: 2026-05-22*