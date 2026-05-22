# How To: Calendar With Month Year Params

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test the calendar view with month and year parameters.

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

### Step 1: 'Test the calendar view with month and year parameters.'

```python
'Test the calendar view with month and year parameters.'
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
response = self.client.get(reverse('calendar') + '?month=6&year=2024')
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

### Step 8: Assign first_day = date(...)

```python
first_day = date(2024, 6, 1)
```

### Step 9: Assign last_day = value

```python
last_day = date(2024, 7, 1) - timedelta(days=1)
```

### Step 10: Call mock_get_user_events.assert_called_once_with()

```python
mock_get_user_events.assert_called_once_with(self.user, first_day, last_day)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(response.context['month'], 6)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(response.context['year'], 2024)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(response.context['month_name'], 'June')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(response.context['prev_month'], 5)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(response.context['prev_year'], 2024)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(response.context['next_month'], 7)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(response.context['next_year'], 2024)
```


## Complete Example

```python
# Setup
# Fixtures: mock_update_preference, mock_get_user_events

# Workflow
'Test the calendar view with month and year parameters.'
mock_update_preference.return_value = 'month'
mock_get_user_events.return_value = []
response = self.client.get(reverse('calendar') + '?month=6&year=2024')
self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'events/calendar.html')
mock_update_preference.assert_called_once_with('calendar_layout', None)
first_day = date(2024, 6, 1)
last_day = date(2024, 7, 1) - timedelta(days=1)
mock_get_user_events.assert_called_once_with(self.user, first_day, last_day)
self.assertEqual(response.context['month'], 6)
self.assertEqual(response.context['year'], 2024)
self.assertEqual(response.context['month_name'], 'June')
self.assertEqual(response.context['prev_month'], 5)
self.assertEqual(response.context['prev_year'], 2024)
self.assertEqual(response.context['next_month'], 7)
self.assertEqual(response.context['next_year'], 2024)
```

## Next Steps


---

*Source: test_views.py:71 | Complexity: Advanced | Last updated: 2026-05-22*