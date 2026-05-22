# How To: Exclude Then Notify

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test excluding an item then verifying it's not in notifications.

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

### Step 1: "Test excluding an item then verifying it's not in notifications."

```python
"Test excluding an item then verifying it's not in notifications."
```

### Step 2: Assign item2 = Item.objects.create(...)

```python
item2 = Item.objects.create(media_id='100', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Another Anime', image='http://example.com/anime2.jpg')
```

### Step 3: Call Anime.objects.create()

```python
Anime.objects.create(item=item2, user=self.user1, status=Status.IN_PROGRESS.value)
```

### Step 4: Assign now = timezone.now(...)

```python
now = timezone.now()
```

### Step 5: Assign ten_mins_ago = value

```python
ten_mins_ago = now - timedelta(minutes=10)
```

### Step 6: Assign event2 = Event.objects.create(...)

```python
event2 = Event.objects.create(item=item2, content_number=3, datetime=ten_mins_ago, notification_sent=False)
```

### Step 7: Assign mock_send_notifications.return_value = value

```python
mock_send_notifications.return_value = {'event_count': 6, 'event_ids': [self.anime_event.id, self.manga_event.id, self.season1_event.id, self.season2_event.id, self.season3_event.id, event2.id]}
```

### Step 8: Call self.user1.notification_excluded_items.add()

```python
self.user1.notification_excluded_items.add(self.anime_item)
```

### Step 9: Call send_releases()

```python
send_releases()
```

### Step 10: Call self.anime_event.refresh_from_db()

```python
self.anime_event.refresh_from_db()
```

### Step 11: Call event2.refresh_from_db()

```python
event2.refresh_from_db()
```

### Step 12: Call self.manga_event.refresh_from_db()

```python
self.manga_event.refresh_from_db()
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(self.anime_event.notification_sent)
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(event2.notification_sent)
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(self.manga_event.notification_sent)
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
"Test excluding an item then verifying it's not in notifications."
item2 = Item.objects.create(media_id='100', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Another Anime', image='http://example.com/anime2.jpg')
Anime.objects.create(item=item2, user=self.user1, status=Status.IN_PROGRESS.value)
now = timezone.now()
ten_mins_ago = now - timedelta(minutes=10)
event2 = Event.objects.create(item=item2, content_number=3, datetime=ten_mins_ago, notification_sent=False)
mock_send_notifications.return_value = {'event_count': 6, 'event_ids': [self.anime_event.id, self.manga_event.id, self.season1_event.id, self.season2_event.id, self.season3_event.id, event2.id]}
self.user1.notification_excluded_items.add(self.anime_item)
send_releases()
self.anime_event.refresh_from_db()
event2.refresh_from_db()
self.manga_event.refresh_from_db()
self.assertTrue(self.anime_event.notification_sent)
self.assertTrue(event2.notification_sent)
self.assertTrue(self.manga_event.notification_sent)
```

## Next Steps


---

*Source: test_notification.py:232 | Complexity: Advanced | Last updated: 2026-05-22*