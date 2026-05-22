# How To: Get User Events

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the get_user_events method.

## Prerequisites

**Required Modules:**
- `datetime`
- `django.contrib.auth`
- `django.test`
- `django.utils`
- `app.models`
- `events.models`


## Step-by-Step Guide

### Step 1: 'Test the get_user_events method.'

```python
'Test the get_user_events method.'
```

### Step 2: Assign today = self.base_date.date(...)

```python
today = self.base_date.date()
```

### Step 3: Assign next_week = value

```python
next_week = today + datetime.timedelta(days=7)
```

### Step 4: Assign events = Event.objects.get_user_events(...)

```python
events = Event.objects.get_user_events(self.user, today, next_week)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(events.count(), 4)
```

### Step 6: Call self.assertIn()

```python
self.assertIn(self.season_event, events)
```

### Step 7: Call self.assertIn()

```python
self.assertIn(self.manga_event1, events)
```

### Step 8: Call self.assertIn()

```python
self.assertIn(self.movie_event, events)
```

### Step 9: Call self.assertIn()

```python
self.assertIn(self.manga_event2, events)
```

### Step 10: Call self.assertNotIn()

```python
self.assertNotIn(self.past_event, events)
```

### Step 11: Assign other_events = Event.objects.get_user_events(...)

```python
other_events = Event.objects.get_user_events(self.other_user, today, next_week)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(other_events.count(), 1)
```

### Step 13: Assign tomorrow = value

```python
tomorrow = today + datetime.timedelta(days=1)
```

### Step 14: Assign limited_events = Event.objects.get_user_events(...)

```python
limited_events = Event.objects.get_user_events(self.user, today, tomorrow)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(limited_events.count(), 2)
```

### Step 16: Call self.assertIn()

```python
self.assertIn(self.season_event, limited_events)
```

### Step 17: Call self.assertIn()

```python
self.assertIn(self.manga_event1, limited_events)
```

### Step 18: Call self.assertNotIn()

```python
self.assertNotIn(self.movie_event, limited_events)
```

### Step 19: Call self.assertNotIn()

```python
self.assertNotIn(self.past_event, limited_events)
```


## Complete Example

```python
# Workflow
'Test the get_user_events method.'
today = self.base_date.date()
next_week = today + datetime.timedelta(days=7)
events = Event.objects.get_user_events(self.user, today, next_week)
self.assertEqual(events.count(), 4)
self.assertIn(self.season_event, events)
self.assertIn(self.manga_event1, events)
self.assertIn(self.movie_event, events)
self.assertIn(self.manga_event2, events)
self.assertNotIn(self.past_event, events)
other_events = Event.objects.get_user_events(self.other_user, today, next_week)
self.assertEqual(other_events.count(), 1)
tomorrow = today + datetime.timedelta(days=1)
limited_events = Event.objects.get_user_events(self.user, today, tomorrow)
self.assertEqual(limited_events.count(), 2)
self.assertIn(self.season_event, limited_events)
self.assertIn(self.manga_event1, limited_events)
self.assertNotIn(self.movie_event, limited_events)
self.assertNotIn(self.past_event, limited_events)
```

## Next Steps


---

*Source: test_models.py:269 | Complexity: Advanced | Last updated: 2026-05-22*