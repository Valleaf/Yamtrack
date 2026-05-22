# How To: Get Tv Tracking Data

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the get_tv_tracking_data function.

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

### Step 1: 'Test the get_tv_tracking_data function.'

```python
'Test the get_tv_tracking_data function.'
```

### Step 2: Assign users = value

```python
users = [self.user1, self.user2]
```

### Step 3: Assign season_items = value

```python
season_items = [self.season1_item, self.season2_item, self.season3_item]
```

### Step 4: Assign user_exclusions = value

```python
user_exclusions = {self.user1.id: set(), self.user2.id: set()}
```

### Step 5: Assign tracking_data = get_tv_tracking_data(...)

```python
tracking_data = get_tv_tracking_data(users, season_items, user_exclusions)
```

### Step 6: Call self.assertIsInstance()

```python
self.assertIsInstance(tracking_data, dict)
```

### Step 7: Assign user1_season1_key = value

```python
user1_season1_key = (self.user1.id, self.season1_item.id)
```

### Step 8: Assign user1_season2_key = value

```python
user1_season2_key = (self.user1.id, self.season2_item.id)
```

### Step 9: Assign user1_season3_key = value

```python
user1_season3_key = (self.user1.id, self.season3_item.id)
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(tracking_data[user1_season1_key])
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(tracking_data[user1_season2_key])
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(tracking_data[user1_season3_key])
```

### Step 13: Assign user2_season1_key = value

```python
user2_season1_key = (self.user2.id, self.season1_item.id)
```

### Step 14: Assign user2_season2_key = value

```python
user2_season2_key = (self.user2.id, self.season2_item.id)
```

### Step 15: Assign user2_season3_key = value

```python
user2_season3_key = (self.user2.id, self.season3_item.id)
```

### Step 16: Call self.assertTrue()

```python
self.assertTrue(tracking_data[user2_season1_key])
```

### Step 17: Call self.assertFalse()

```python
self.assertFalse(tracking_data[user2_season2_key])
```

### Step 18: Call self.assertFalse()

```python
self.assertFalse(tracking_data[user2_season3_key])
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
'Test the get_tv_tracking_data function.'
users = [self.user1, self.user2]
season_items = [self.season1_item, self.season2_item, self.season3_item]
user_exclusions = {self.user1.id: set(), self.user2.id: set()}
tracking_data = get_tv_tracking_data(users, season_items, user_exclusions)
self.assertIsInstance(tracking_data, dict)
user1_season1_key = (self.user1.id, self.season1_item.id)
user1_season2_key = (self.user1.id, self.season2_item.id)
user1_season3_key = (self.user1.id, self.season3_item.id)
self.assertTrue(tracking_data[user1_season1_key])
self.assertTrue(tracking_data[user1_season2_key])
self.assertTrue(tracking_data[user1_season3_key])
user2_season1_key = (self.user2.id, self.season1_item.id)
user2_season2_key = (self.user2.id, self.season2_item.id)
user2_season3_key = (self.user2.id, self.season3_item.id)
self.assertTrue(tracking_data[user2_season1_key])
self.assertFalse(tracking_data[user2_season2_key])
self.assertFalse(tracking_data[user2_season3_key])
```

## Next Steps


---

*Source: test_notification.py:437 | Complexity: Advanced | Last updated: 2026-05-22*