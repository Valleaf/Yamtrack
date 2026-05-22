# How To: User Exclusion

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test that user exclusions are respected.

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

### Step 1: 'Test that user exclusions are respected.'

```python
'Test that user exclusions are respected.'
```

### Step 2: Assign users_with_notifications = get_user_model.objects.filter.prefetch_related(...)

```python
users_with_notifications = get_user_model().objects.filter(~models.Q(notification_urls='')).prefetch_related('notification_excluded_items')
```

### Step 3: Assign target_events = value

```python
target_events = {(self.anime_event.item.id, self.anime_event.content_number): self.anime_event, (self.manga_event.item.id, self.manga_event.content_number): self.manga_event}
```

### Step 4: Assign user_releases = get_user_releases(...)

```python
user_releases = get_user_releases(users_with_notifications, target_events)
```

### Step 5: Assign user1_events = value

```python
user1_events = user_releases[self.user1.id]
```

### Step 6: Assign manga_event_found = any(...)

```python
manga_event_found = any((event.id == self.manga_event.id for event in user1_events))
```

### Step 7: Call self.assertFalse()

```python
self.assertFalse(manga_event_found)
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
'Test that user exclusions are respected.'
users_with_notifications = get_user_model().objects.filter(~models.Q(notification_urls='')).prefetch_related('notification_excluded_items')
target_events = {(self.anime_event.item.id, self.anime_event.content_number): self.anime_event, (self.manga_event.item.id, self.manga_event.content_number): self.manga_event}
user_releases = get_user_releases(users_with_notifications, target_events)
user1_events = user_releases[self.user1.id]
manga_event_found = any((event.id == self.manga_event.id for event in user1_events))
self.assertFalse(manga_event_found)
```

## Next Steps


---

*Source: test_notification.py:750 | Complexity: Intermediate | Last updated: 2026-05-22*