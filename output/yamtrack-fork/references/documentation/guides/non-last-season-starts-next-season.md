# How To: Non Last Season Starts Next Season

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test non-last season completion starts the next season.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `pathlib`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `django.utils`
- `app.models`

**Setup Required:**
```python
# Fixtures: mock_get_metadata
```

## Step-by-Step Guide

### Step 1: 'Test non-last season completion starts the next season.'

```python
'Test non-last season completion starts the next season.'
```

### Step 2: Assign next_season_item = Item.objects.create(...)

```python
next_season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image2.jpg', season_number=2)
```

### Step 3: Assign next_season = Season.objects.create(...)

```python
next_season = Season.objects.create(item=next_season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
```

### Step 4: Assign mock_metadata = value

```python
mock_metadata = {'season/1': {'episodes': [{'episode_number': 1}]}, 'related': {'seasons': [{'season_number': 1, 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 2, 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}}
```

### Step 5: Assign mock_get_metadata.return_value = mock_metadata

```python
mock_get_metadata.return_value = mock_metadata
```

### Step 6: Call Episode.objects.create()

```python
Episode.objects.create(item=self.episode_item, related_season=self.season, end_date=timezone.now())
```

### Step 7: Call next_season.refresh_from_db()

```python
next_season.refresh_from_db()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(next_season.status, Status.IN_PROGRESS.value)
```

### Step 9: Call self.tv.refresh_from_db()

```python
self.tv.refresh_from_db()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(self.tv.status, Status.IN_PROGRESS.value)
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.SUCCESS, message=f'{self.season} was marked as completed automatically.').exists())
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.tv} Season 2 was marked as in progress automatically.').exists())
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_metadata

# Workflow
'Test non-last season completion starts the next season.'
next_season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image2.jpg', season_number=2)
next_season = Season.objects.create(item=next_season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
mock_metadata = {'season/1': {'episodes': [{'episode_number': 1}]}, 'related': {'seasons': [{'season_number': 1, 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 2, 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}}
mock_get_metadata.return_value = mock_metadata
Episode.objects.create(item=self.episode_item, related_season=self.season, end_date=timezone.now())
next_season.refresh_from_db()
self.assertEqual(next_season.status, Status.IN_PROGRESS.value)
self.tv.refresh_from_db()
self.assertEqual(self.tv.status, Status.IN_PROGRESS.value)
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.SUCCESS, message=f'{self.season} was marked as completed automatically.').exists())
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.tv} Season 2 was marked as in progress automatically.').exists())
```

## Next Steps


---

*Source: test_episode.py:239 | Complexity: Advanced | Last updated: 2026-05-22*