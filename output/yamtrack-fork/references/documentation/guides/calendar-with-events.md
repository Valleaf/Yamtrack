# How To: Calendar With Events

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test the calendar with events.

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

### Step 1: 'Test the calendar with events.'

```python
'Test the calendar with events.'
```

### Step 2: Assign mock_update_preference.return_value = 'month'

```python
mock_update_preference.return_value = 'month'
```

### Step 3: Assign item1 = Item(...)

```python
item1 = Item(id=1, media_id='123', source=Sources.MANUAL.value, media_type=MediaTypes.ANIME.value, title='Test Show 1', image='https://example.com/image1.jpg')
```

### Step 4: Assign item2 = Item(...)

```python
item2 = Item(id=2, media_id='456', source=Sources.MANUAL.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='https://example.com/image2.jpg')
```

### Step 5: Assign today = timezone.localdate(...)

```python
today = timezone.localdate()
```

### Step 6: Assign event1 = Event(...)

```python
event1 = Event(item=item1, datetime=timezone.make_aware(timezone.datetime(today.year, today.month, 15, 12, 0)))
```

### Step 7: Assign event2 = Event(...)

```python
event2 = Event(item=item1, content_number=2, datetime=timezone.make_aware(timezone.datetime(today.year, today.month, 15, 18, 0)))
```

### Step 8: Assign event3 = Event(...)

```python
event3 = Event(item=item2, datetime=timezone.make_aware(timezone.datetime(today.year, today.month, 20, 9, 0)))
```

### Step 9: Assign mock_get_user_events.return_value = value

```python
mock_get_user_events.return_value = [event1, event2, event3]
```

### Step 10: Assign response = self.client.get(...)

```python
response = self.client.get(reverse('calendar'))
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(response.status_code, 200)
```

### Step 12: Assign release_dict = value

```python
release_dict = response.context['release_dict']
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(len(release_dict), 2)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(len(release_dict[15]), 2)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(len(release_dict[20]), 1)
```


## Complete Example

```python
# Setup
# Fixtures: mock_update_preference, mock_get_user_events

# Workflow
'Test the calendar with events.'
mock_update_preference.return_value = 'month'
item1 = Item(id=1, media_id='123', source=Sources.MANUAL.value, media_type=MediaTypes.ANIME.value, title='Test Show 1', image='https://example.com/image1.jpg')
item2 = Item(id=2, media_id='456', source=Sources.MANUAL.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='https://example.com/image2.jpg')
today = timezone.localdate()
event1 = Event(item=item1, datetime=timezone.make_aware(timezone.datetime(today.year, today.month, 15, 12, 0)))
event2 = Event(item=item1, content_number=2, datetime=timezone.make_aware(timezone.datetime(today.year, today.month, 15, 18, 0)))
event3 = Event(item=item2, datetime=timezone.make_aware(timezone.datetime(today.year, today.month, 20, 9, 0)))
mock_get_user_events.return_value = [event1, event2, event3]
response = self.client.get(reverse('calendar'))
self.assertEqual(response.status_code, 200)
release_dict = response.context['release_dict']
self.assertEqual(len(release_dict), 2)
self.assertEqual(len(release_dict[15]), 2)
self.assertEqual(len(release_dict[20]), 1)
```

## Next Steps


---

*Source: test_views.py:202 | Complexity: Advanced | Last updated: 2026-05-22*