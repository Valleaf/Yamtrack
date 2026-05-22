# How To: Download Calendar With Events

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test downloading a calendar with events.

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
# Fixtures: mock_get_user_events
```

## Step-by-Step Guide

### Step 1: 'Test downloading a calendar with events.'

```python
'Test downloading a calendar with events.'
```

### Step 2: Assign item1 = Item.objects.create(...)

```python
item1 = Item.objects.create(media_id='123', source=Sources.MANUAL.value, media_type=MediaTypes.ANIME.value, title='Test Show', image='https://example.com/image.jpg')
```

### Step 3: Assign item2 = Item.objects.create(...)

```python
item2 = Item.objects.create(media_id='456', source=Sources.MANUAL.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='https://example.com/image2.jpg')
```

### Step 4: Assign event1 = Event.objects.create(...)

```python
event1 = Event.objects.create(item=item1, content_number=5, datetime=timezone.make_aware(timezone.datetime(2024, 6, 15, 12, 0)))
```

### Step 5: Assign event2 = Event.objects.create(...)

```python
event2 = Event.objects.create(item=item2, datetime=timezone.make_aware(timezone.datetime(2024, 6, 20, 18, 0)))
```

### Step 6: Assign mock_get_user_events.return_value = value

```python
mock_get_user_events.return_value = [event1, event2]
```

### Step 7: Assign response = self.client.get(...)

```python
response = self.client.get(self.url)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(response['Content-Type'], 'text/calendar')
```

### Step 10: Assign content = response.content.decode(...)

```python
content = response.content.decode()
```

### Step 11: Call self.assertIn()

```python
self.assertIn('BEGIN:VCALENDAR', content)
```

### Step 12: Call self.assertIn()

```python
self.assertIn('BEGIN:VEVENT', content)
```

### Step 13: Call self.assertIn()

```python
self.assertIn('END:VEVENT', content)
```

### Step 14: Call self.assertIn()

```python
self.assertIn('END:VCALENDAR', content)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(content.count('BEGIN:VEVENT'), 2)
```

### Step 16: Call mock_get_user_events.assert_called_once()

```python
mock_get_user_events.assert_called_once()
```

### Step 17: Assign call_args = value

```python
call_args = mock_get_user_events.call_args
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(call_args[0][0], self.user)
```

### Step 19: Assign today = timezone.now.date(...)

```python
today = timezone.now().date()
```

### Step 20: Assign expected_start = value

```python
expected_start = today - timedelta(days=30)
```

### Step 21: Assign expected_end = value

```python
expected_end = today + timedelta(days=90)
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(call_args[0][1], expected_start)
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(call_args[0][2], expected_end)
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_user_events

# Workflow
'Test downloading a calendar with events.'
item1 = Item.objects.create(media_id='123', source=Sources.MANUAL.value, media_type=MediaTypes.ANIME.value, title='Test Show', image='https://example.com/image.jpg')
item2 = Item.objects.create(media_id='456', source=Sources.MANUAL.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='https://example.com/image2.jpg')
event1 = Event.objects.create(item=item1, content_number=5, datetime=timezone.make_aware(timezone.datetime(2024, 6, 15, 12, 0)))
event2 = Event.objects.create(item=item2, datetime=timezone.make_aware(timezone.datetime(2024, 6, 20, 18, 0)))
mock_get_user_events.return_value = [event1, event2]
response = self.client.get(self.url)
self.assertEqual(response.status_code, 200)
self.assertEqual(response['Content-Type'], 'text/calendar')
content = response.content.decode()
self.assertIn('BEGIN:VCALENDAR', content)
self.assertIn('BEGIN:VEVENT', content)
self.assertIn('END:VEVENT', content)
self.assertIn('END:VCALENDAR', content)
self.assertEqual(content.count('BEGIN:VEVENT'), 2)
mock_get_user_events.assert_called_once()
call_args = mock_get_user_events.call_args
self.assertEqual(call_args[0][0], self.user)
today = timezone.now().date()
expected_start = today - timedelta(days=30)
expected_end = today + timedelta(days=90)
self.assertEqual(call_args[0][1], expected_start)
self.assertEqual(call_args[0][2], expected_end)
```

## Next Steps


---

*Source: test_views.py:328 | Complexity: Advanced | Last updated: 2026-05-22*