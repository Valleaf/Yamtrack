# How To: Calendar Default View

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test the calendar view with default parameters.

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

### Step 1: 'Test the calendar view with default parameters.'

```python
'Test the calendar view with default parameters.'
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
response = self.client.get(reverse('calendar'))
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 6: Call self.assertTemplateUsed()

```python
self.assertTemplateUsed(response, 'events/calendar.html')
```

### Step 7: Call mock_update_preference.assert_called_once_with()

```python
mock_update_preference.assert_called_once_with('calendar_layout', None)
```

### Step 8: Assign today = timezone.localdate(...)

```python
today = timezone.localdate()
```

### Step 9: Assign first_day = date(...)

```python
first_day = date(today.year, today.month, 1)
```

### Step 10: Assign december = 12

```python
december = 12
```

### Step 11: Call mock_get_user_events.assert_called_once_with()

```python
mock_get_user_events.assert_called_once_with(self.user, first_day, last_day)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(response.context['month'], today.month)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(response.context['year'], today.year)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(response.context['month_name'], calendar.month_name[today.month])
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(response.context['view_type'], 'month')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(response.context['today'], today)
```

### Step 17: Assign last_day = value

```python
last_day = date(today.year + 1, 1, 1) - timedelta(days=1)
```

### Step 18: Assign last_day = value

```python
last_day = date(today.year, today.month + 1, 1) - timedelta(days=1)
```


## Complete Example

```python
# Setup
# Fixtures: mock_update_preference, mock_get_user_events

# Workflow
'Test the calendar view with default parameters.'
mock_update_preference.return_value = 'month'
mock_get_user_events.return_value = []
response = self.client.get(reverse('calendar'))
self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'events/calendar.html')
mock_update_preference.assert_called_once_with('calendar_layout', None)
today = timezone.localdate()
first_day = date(today.year, today.month, 1)
december = 12
if today.month == december:
    last_day = date(today.year + 1, 1, 1) - timedelta(days=1)
else:
    last_day = date(today.year, today.month + 1, 1) - timedelta(days=1)
mock_get_user_events.assert_called_once_with(self.user, first_day, last_day)
self.assertEqual(response.context['month'], today.month)
self.assertEqual(response.context['year'], today.year)
self.assertEqual(response.context['month_name'], calendar.month_name[today.month])
self.assertEqual(response.context['view_type'], 'month')
self.assertEqual(response.context['today'], today)
```

## Next Steps


---

*Source: test_views.py:26 | Complexity: Advanced | Last updated: 2026-05-22*