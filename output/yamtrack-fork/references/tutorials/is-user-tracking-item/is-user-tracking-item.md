# How To: Is User Tracking Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the is_user_tracking_item function.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `unittest.mock`
- `django.contrib.auth`
- `django.db`
- `django.test`
- `django.utils`
- `app.models`
- `events.models`
- `events.notifications`

**Setup Required:**
```python
'Set up test data.'
self.credentials = {'username': 'user1', 'password': '12345', 'notification_urls': 'https://example.com/notify1'}
self.user1 = get_user_model().objects.create_user(**self.credentials)
self.credentials = {'username': 'user2', 'password': '12345', 'notification_urls': 'https://example.com/notify2'}
self.user2 = get_user_model().objects.create_user(**self.credentials)
self.credentials = {'username': 'user3', 'password': '12345'}
self.user3 = get_user_model().objects.create_user(**self.credentials)
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/anime.jpg')
self.manga_item = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Test Manga', image='http://example.com/manga.jpg')
self.tv_show_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show', image='http://example.com/tv.jpg')
self.season1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show - Season 1', season_number=1, image='http://example.com/tv.jpg')
self.season2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show - Season 2', season_number=2, image='http://example.com/tv.jpg')
self.season3_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show - Season 3', season_number=3, image='http://example.com/tv.jpg')
Anime.objects.create(item=self.anime_item, user=self.user1, status=Status.IN_PROGRESS.value)
Anime.objects.create(item=self.anime_item, user=self.user2, status=Status.IN_PROGRESS.value)
Anime.objects.create(item=self.anime_item, user=self.user3, status=Status.IN_PROGRESS.value)
Manga.objects.create(item=self.manga_item, user=self.user1, status=Status.IN_PROGRESS.value)
Manga.objects.create(item=self.manga_item, user=self.user2, status=Status.PAUSED.value)
TV.objects.create(item=self.tv_show_item, user=self.user1, status=Status.IN_PROGRESS.value)
user2_tv = TV.objects.create(item=self.tv_show_item, user=self.user2, status=Status.IN_PROGRESS.value)
Season.objects.bulk_create([Season(item=self.season2_item, related_tv=user2_tv, user=self.user2, status=Status.DROPPED.value)])
now = timezone.now()
ten_mins_ago = now - timedelta(minutes=10)
self.anime_event = Event.objects.create(item=self.anime_item, content_number=5, datetime=ten_mins_ago, notification_sent=False)
self.manga_event = Event.objects.create(item=self.manga_item, content_number=10, datetime=ten_mins_ago, notification_sent=False)
self.season1_event = Event.objects.create(item=self.season1_item, content_number=5, datetime=ten_mins_ago, notification_sent=False)
self.season2_event = Event.objects.create(item=self.season2_item, content_number=3, datetime=ten_mins_ago, notification_sent=False)
self.season3_event = Event.objects.create(item=self.season3_item, content_number=1, datetime=ten_mins_ago, notification_sent=False)
self.user1.notification_excluded_items.add(self.manga_item)
```

## Step-by-Step Guide

### Step 1: 'Test the is_user_tracking_item function.'

```python
'Test the is_user_tracking_item function.'
```

### Step 2: Assign users = value

```python
users = [self.user1, self.user2]
```

### Step 3: Assign target_events = value

```python
target_events = {(self.anime_event.item.id, self.anime_event.content_number): self.anime_event, (self.manga_event.item.id, self.manga_event.content_number): self.manga_event, (self.season1_event.item.id, self.season1_event.content_number): self.season1_event}
```

### Step 4: Assign user_exclusions = value

```python
user_exclusions = {self.user1.id: set(), self.user2.id: set()}
```

### Step 5: Assign tracking_data = get_all_user_tracking_data(...)

```python
tracking_data = get_all_user_tracking_data(users, target_events, user_exclusions)
```

### Step 6: Assign result = is_user_tracking_item(...)

```python
result = is_user_tracking_item(self.user1, self.anime_item, tracking_data)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(result)
```

### Step 8: Assign result = is_user_tracking_item(...)

```python
result = is_user_tracking_item(self.user1, self.manga_item, tracking_data)
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(result)
```

### Step 10: Assign result = is_user_tracking_item(...)

```python
result = is_user_tracking_item(self.user2, self.anime_item, tracking_data)
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(result)
```

### Step 12: Assign result = is_user_tracking_item(...)

```python
result = is_user_tracking_item(self.user2, self.manga_item, tracking_data)
```

### Step 13: Call self.assertFalse()

```python
self.assertFalse(result)
```

### Step 14: Assign result = is_user_tracking_item(...)

```python
result = is_user_tracking_item(self.user1, self.season1_item, tracking_data)
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(result)
```


## Complete Example

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'user1', 'password': '12345', 'notification_urls': 'https://example.com/notify1'}
self.user1 = get_user_model().objects.create_user(**self.credentials)
self.credentials = {'username': 'user2', 'password': '12345', 'notification_urls': 'https://example.com/notify2'}
self.user2 = get_user_model().objects.create_user(**self.credentials)
self.credentials = {'username': 'user3', 'password': '12345'}
self.user3 = get_user_model().objects.create_user(**self.credentials)
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/anime.jpg')
self.manga_item = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Test Manga', image='http://example.com/manga.jpg')
self.tv_show_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show', image='http://example.com/tv.jpg')
self.season1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show - Season 1', season_number=1, image='http://example.com/tv.jpg')
self.season2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show - Season 2', season_number=2, image='http://example.com/tv.jpg')
self.season3_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show - Season 3', season_number=3, image='http://example.com/tv.jpg')
Anime.objects.create(item=self.anime_item, user=self.user1, status=Status.IN_PROGRESS.value)
Anime.objects.create(item=self.anime_item, user=self.user2, status=Status.IN_PROGRESS.value)
Anime.objects.create(item=self.anime_item, user=self.user3, status=Status.IN_PROGRESS.value)
Manga.objects.create(item=self.manga_item, user=self.user1, status=Status.IN_PROGRESS.value)
Manga.objects.create(item=self.manga_item, user=self.user2, status=Status.PAUSED.value)
TV.objects.create(item=self.tv_show_item, user=self.user1, status=Status.IN_PROGRESS.value)
user2_tv = TV.objects.create(item=self.tv_show_item, user=self.user2, status=Status.IN_PROGRESS.value)
Season.objects.bulk_create([Season(item=self.season2_item, related_tv=user2_tv, user=self.user2, status=Status.DROPPED.value)])
now = timezone.now()
ten_mins_ago = now - timedelta(minutes=10)
self.anime_event = Event.objects.create(item=self.anime_item, content_number=5, datetime=ten_mins_ago, notification_sent=False)
self.manga_event = Event.objects.create(item=self.manga_item, content_number=10, datetime=ten_mins_ago, notification_sent=False)
self.season1_event = Event.objects.create(item=self.season1_item, content_number=5, datetime=ten_mins_ago, notification_sent=False)
self.season2_event = Event.objects.create(item=self.season2_item, content_number=3, datetime=ten_mins_ago, notification_sent=False)
self.season3_event = Event.objects.create(item=self.season3_item, content_number=1, datetime=ten_mins_ago, notification_sent=False)
self.user1.notification_excluded_items.add(self.manga_item)

# Workflow
'Test the is_user_tracking_item function.'
users = [self.user1, self.user2]
target_events = {(self.anime_event.item.id, self.anime_event.content_number): self.anime_event, (self.manga_event.item.id, self.manga_event.content_number): self.manga_event, (self.season1_event.item.id, self.season1_event.content_number): self.season1_event}
user_exclusions = {self.user1.id: set(), self.user2.id: set()}
tracking_data = get_all_user_tracking_data(users, target_events, user_exclusions)
result = is_user_tracking_item(self.user1, self.anime_item, tracking_data)
self.assertTrue(result)
result = is_user_tracking_item(self.user1, self.manga_item, tracking_data)
self.assertTrue(result)
result = is_user_tracking_item(self.user2, self.anime_item, tracking_data)
self.assertTrue(result)
result = is_user_tracking_item(self.user2, self.manga_item, tracking_data)
self.assertFalse(result)
result = is_user_tracking_item(self.user1, self.season1_item, tracking_data)
self.assertTrue(result)
```

## Next Steps


---

*Source: test_notification.py:623 | Complexity: Advanced | Last updated: 2026-05-22*