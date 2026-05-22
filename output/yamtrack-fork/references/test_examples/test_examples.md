# Test Example Extraction Report

**Total Examples**: 736  
**High Value Examples** (confidence > 0.7): 736  
**Average Complexity**: 0.54  

## Examples by Category

- **instantiation**: 26
- **method_call**: 424
- **workflow**: 286

## Examples by Language

- **Python**: 736

## Extracted Examples

### test_overwrite_steam_game_completed_status

**Category**: workflow  
**Description**: Workflow: Test overwrite mode does not downgrade completed games.  
**Expected**: self.assertEqual(game.status, Status.COMPLETED.value)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create user and common data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Counter-Strike 2', image='http://example.com/cs2.jpg')

'Test overwrite mode does not downgrade completed games.'
self._setup_mocks(mock_get_metadata, mock_external_game, mock_api_request, playtime=1100)
game = self._create_game(status=Status.COMPLETED.value, progress=1000)
imported_counts, _ = steam.importer('76561198000000000', self.user, 'overwrite')
game.refresh_from_db()
self.assertEqual(imported_counts[MediaTypes.GAME.value], 1)
self.assertEqual(game.progress, 1100)
self.assertEqual(game.status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_steam_update.py:90*

### test_overwrite_steam_game_completed_status

**Category**: workflow  
**Description**: Workflow: Test overwrite mode does not downgrade completed games.  
**Expected**: self.assertEqual(game.status, Status.COMPLETED.value)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_metadata, mock_external_game, mock_api_request

'Test overwrite mode does not downgrade completed games.'
self._setup_mocks(mock_get_metadata, mock_external_game, mock_api_request, playtime=1100)
game = self._create_game(status=Status.COMPLETED.value, progress=1000)
imported_counts, _ = steam.importer('76561198000000000', self.user, 'overwrite')
game.refresh_from_db()
self.assertEqual(imported_counts[MediaTypes.GAME.value], 1)
self.assertEqual(game.progress, 1100)
self.assertEqual(game.status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_steam_update.py:90*

### test_anime_unknown

**Category**: workflow  
**Description**: Workflow: Test the metadata method for anime with mostly unknown data.  
**Expected**: self.assertEqual(response['details']['runtime'], None)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test the metadata method for anime with mostly unknown data.'
with Path(mock_path / 'metadata_anime_unknown.json').open() as file:
    anime_response = json.load(file)
mock_data.return_value.json.return_value = anime_response
mock_data.return_value.status_code = 200
response = mal.anime('0')
self.assertEqual(response['title'], 'Unknown Example')
self.assertEqual(response['image'], settings.IMG_NONE)
self.assertEqual(response['synopsis'], 'No synopsis available.')
self.assertEqual(response['details']['episodes'], None)
self.assertEqual(response['details']['runtime'], None)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_metadata.py:38*

### test_tv_changes

**Category**: workflow  
**Description**: Workflow: Test fetching changed TV ids from TMDB.  
**Expected**: self.assertEqual(kwargs['params']['page'], 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test fetching changed TV ids from TMDB.'
mock_localdate.return_value = date(2026, 4, 5)
mock_api_request.return_value = {'results': [{'id': 1}, {'id': 2}], 'total_pages': 1}
result = tmdb.tv_changes()
self.assertEqual(result, {'1', '2'})
_, kwargs = mock_api_request.call_args
self.assertEqual(kwargs['params']['start_date'], '2026-04-02')
self.assertEqual(kwargs['params']['end_date'], '2026-04-05')
self.assertEqual(kwargs['params']['page'], 1)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_metadata.py:78*

### test_movie_changes

**Category**: workflow  
**Description**: Workflow: Test fetching changed movie ids from TMDB.  
**Expected**: self.assertEqual(kwargs['params']['page'], 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test fetching changed movie ids from TMDB.'
mock_localdate.return_value = date(2026, 4, 5)
mock_api_request.return_value = {'results': [{'id': 10}, {'id': 20}], 'total_pages': 1}
result = tmdb.movie_changes()
self.assertEqual(result, {'10', '20'})
_, kwargs = mock_api_request.call_args
self.assertEqual(kwargs['params']['start_date'], '2026-04-02')
self.assertEqual(kwargs['params']['end_date'], '2026-04-05')
self.assertEqual(kwargs['params']['page'], 1)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_metadata.py:117*

### test_tmdb_find_next_episode

**Category**: workflow  
**Description**: Workflow: Test the find_next_episode function.  
**Expected**: self.assertIsNone(next_episode)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the find_next_episode function.'
episodes_metadata = [{'episode_number': 1, 'title': 'Episode 1'}, {'episode_number': 2, 'title': 'Episode 2'}, {'episode_number': 3, 'title': 'Episode 3'}]
next_episode = tmdb.find_next_episode(1, episodes_metadata)
self.assertEqual(next_episode, 2)
next_episode = tmdb.find_next_episode(3, episodes_metadata)
self.assertIsNone(next_episode)
next_episode = tmdb.find_next_episode(5, episodes_metadata)
self.assertIsNone(next_episode)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_metadata.py:296*

### test_movie_unknown

**Category**: workflow  
**Description**: Workflow: Test the metadata method for movies with mostly unknown data.  
**Expected**: self.assertEqual(response['details']['languages'], None)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test the metadata method for movies with mostly unknown data.'
with Path(mock_path / 'metadata_movie_unknown.json').open() as file:
    movie_response = json.load(file)
mock_data.return_value.json.return_value = movie_response
mock_data.return_value.status_code = 200
response = tmdb.movie('0')
self.assertEqual(response['title'], 'Unknown Movie')
self.assertEqual(response['image'], settings.IMG_NONE)
self.assertEqual(response['synopsis'], 'No synopsis available.')
self.assertEqual(response['details']['release_date'], None)
self.assertEqual(response['details']['runtime'], None)
self.assertEqual(response['genres'], None)
self.assertEqual(response['details']['studios'], None)
self.assertEqual(response['details']['country'], None)
self.assertEqual(response['details']['languages'], None)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_metadata.py:321*

### test_manual_process_episodes

**Category**: workflow  
**Description**: Workflow: Test the process_episodes function for manual episodes.  
**Expected**: self.assertFalse(result[2]['history'], [])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the process_episodes function for manual episodes.'
Item.objects.create(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Process Episodes Test', image='http://example.com/process.jpg')
Item.objects.create(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Process Episodes Test', image='http://example.com/process_s1.jpg', season_number=1)
for i in range(1, 4):
    Item.objects.create(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.EPISODE.value, title=f'Process Episode {i}', image=f'http://example.com/process_s1e{i}.jpg', season_number=1, episode_number=i)
season_metadata = {'season_number': 1, 'episodes': [{'media_id': '5', 'episode_number': 1, 'air_date': '2025-01-01', 'image': 'http://example.com/process_s1e1.jpg', 'title': 'Process Episode 1'}, {'media_id': '5', 'episode_number': 2, 'air_date': '2025-01-08', 'image': 'http://example.com/process_s1e2.jpg', 'title': 'Process Episode 2'}, {'media_id': '5', 'episode_number': 3, 'air_date': '2025-01-15', 'image': 'http://example.com/process_s1e3.jpg', 'title': 'Process Episode 3'}]}
ep_item1 = Item.objects.get(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.EPISODE.value, season_number=1, episode_number=1)
ep_item2 = Item.objects.get(media_id='5', source=Sources.MANUAL.value, media_type=MediaTypes.EPISODE.value, season_number=1, episode_number=2)
episode_1 = Episode(item=ep_item1)
episode_2 = Episode(item=ep_item2)
episodes_in_db = [episode_1, episode_2]
result = manual.process_episodes(season_metadata, episodes_in_db)
self.assertEqual(len(result), 3)
self.assertEqual(result[0]['episode_number'], 1)
self.assertEqual(result[0]['title'], 'Process Episode 1')
self.assertEqual(result[0]['air_date'], '2025-01-01')
self.assertTrue(result[0]['history'], [episode_1])
self.assertEqual(result[1]['episode_number'], 2)
self.assertEqual(result[1]['title'], 'Process Episode 2')
self.assertEqual(result[1]['air_date'], '2025-01-08')
self.assertTrue(result[0]['history'], [episode_2])
self.assertEqual(result[2]['episode_number'], 3)
self.assertEqual(result[2]['title'], 'Process Episode 3')
self.assertEqual(result[2]['air_date'], '2025-01-15')
self.assertFalse(result[2]['history'], [])
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_metadata.py:538*

### test_hardcover_get_edition_details

**Category**: workflow  
**Description**: Workflow: Test the get_edition_details function from Hardcover provider.  
**Expected**: self.assertEqual(result['publisher'], None)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the get_edition_details function from Hardcover provider.'
edition_data = {'edition_format': 'Paperback', 'isbn_13': '9781234567890', 'isbn_10': '1234567890', 'publisher': {'name': 'Test Publisher'}}
result = hardcover.get_edition_details(edition_data)
self.assertEqual(result['format'], 'Paperback')
self.assertEqual(result['publisher'], 'Test Publisher')
self.assertEqual(result['isbn'], ['1234567890', '9781234567890'])
self.assertEqual(hardcover.get_edition_details(None), {})
no_publisher = {'edition_format': 'Paperback', 'isbn_13': '9781234567890'}
result = hardcover.get_edition_details(no_publisher)
self.assertEqual(result['publisher'], None)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_metadata.py:649*

### test_anime_unknown

**Category**: workflow  
**Description**: Workflow: Test the metadata method for anime with mostly unknown data.  
**Expected**: self.assertEqual(response['details']['runtime'], None)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_data

'Test the metadata method for anime with mostly unknown data.'
with Path(mock_path / 'metadata_anime_unknown.json').open() as file:
    anime_response = json.load(file)
mock_data.return_value.json.return_value = anime_response
mock_data.return_value.status_code = 200
response = mal.anime('0')
self.assertEqual(response['title'], 'Unknown Example')
self.assertEqual(response['image'], settings.IMG_NONE)
self.assertEqual(response['synopsis'], 'No synopsis available.')
self.assertEqual(response['details']['episodes'], None)
self.assertEqual(response['details']['runtime'], None)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_metadata.py:38*

### test_tv_changes

**Category**: workflow  
**Description**: Workflow: Test fetching changed TV ids from TMDB.  
**Expected**: self.assertEqual(kwargs['params']['page'], 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_api_request, mock_localdate

'Test fetching changed TV ids from TMDB.'
mock_localdate.return_value = date(2026, 4, 5)
mock_api_request.return_value = {'results': [{'id': 1}, {'id': 2}], 'total_pages': 1}
result = tmdb.tv_changes()
self.assertEqual(result, {'1', '2'})
_, kwargs = mock_api_request.call_args
self.assertEqual(kwargs['params']['start_date'], '2026-04-02')
self.assertEqual(kwargs['params']['end_date'], '2026-04-05')
self.assertEqual(kwargs['params']['page'], 1)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_metadata.py:78*

### test_movie_changes

**Category**: workflow  
**Description**: Workflow: Test fetching changed movie ids from TMDB.  
**Expected**: self.assertEqual(kwargs['params']['page'], 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_api_request, mock_localdate

'Test fetching changed movie ids from TMDB.'
mock_localdate.return_value = date(2026, 4, 5)
mock_api_request.return_value = {'results': [{'id': 10}, {'id': 20}], 'total_pages': 1}
result = tmdb.movie_changes()
self.assertEqual(result, {'10', '20'})
_, kwargs = mock_api_request.call_args
self.assertEqual(kwargs['params']['start_date'], '2026-04-02')
self.assertEqual(kwargs['params']['end_date'], '2026-04-05')
self.assertEqual(kwargs['params']['page'], 1)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_metadata.py:117*

### test_get_items_to_process_includes_completed_changed_tv

**Category**: workflow  
**Description**: Workflow: Changed completed TV shows should still be selected.  
**Expected**: self.assertIn(self.tv_item, items)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Changed completed TV shows should still be selected.'
mock_tv_changes.return_value = {self.tv_item.media_id}
mock_movie_changes.return_value = set()
TV.objects.filter(item=self.tv_item, user=self.user).update(status=Status.COMPLETED.value)
Event.objects.create(item=self.season_item, content_number=1, datetime=timezone.now() - timezone.timedelta(days=30))
items = get_items_to_process(self.user)
self.assertIn(self.tv_item, items)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_selectors.py:93*

### test_get_items_to_process_excludes_unchanged_tv_with_events

**Category**: workflow  
**Description**: Workflow: Tracked TV with existing season events should be skipped when unchanged.  
**Expected**: self.assertNotIn(self.tv_item, items)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Tracked TV with existing season events should be skipped when unchanged.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = set()
Event.objects.create(item=self.season_item, content_number=1, datetime=timezone.now() - timezone.timedelta(days=30))
items = get_items_to_process(self.user)
self.assertNotIn(self.tv_item, items)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_selectors.py:117*

### test_get_items_to_process_includes_tv_without_season_events

**Category**: workflow  
**Description**: Workflow: Tracked TMDB TV should bootstrap even when no season events exist yet.  
**Expected**: self.assertIn(self.tv_item, items)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Tracked TMDB TV should bootstrap even when no season events exist yet.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = set()
items = get_items_to_process(self.user)
self.assertIn(self.tv_item, items)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_selectors.py:137*

### test_get_items_to_process_excludes_unchanged_movie_with_events

**Category**: workflow  
**Description**: Workflow: Tracked TMDB movies with events should be skipped when unchanged.  
**Expected**: self.assertNotIn(self.movie_item, items)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Tracked TMDB movies with events should be skipped when unchanged.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = set()
Event.objects.create(item=self.movie_item, content_number=None, datetime=timezone.now() - timezone.timedelta(days=30))
items = get_items_to_process(self.user)
self.assertNotIn(self.movie_item, items)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_selectors.py:169*

### test_get_items_to_process_includes_changed_movie_with_existing_event

**Category**: workflow  
**Description**: Workflow: Changed TMDB movies should be selected even with past events.  
**Expected**: self.assertIn(self.movie_item, items)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Changed TMDB movies should be selected even with past events.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = {self.movie_item.media_id}
Event.objects.create(item=self.movie_item, content_number=None, datetime=timezone.now() - timezone.timedelta(days=30))
items = get_items_to_process(self.user)
self.assertIn(self.movie_item, items)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_selectors.py:189*

### test_get_items_to_process_includes_movie_without_events

**Category**: workflow  
**Description**: Workflow: Tracked TMDB movies should bootstrap when they do not have events yet.  
**Expected**: self.assertIn(self.movie_item, items)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Tracked TMDB movies should bootstrap when they do not have events yet.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = set()
items = get_items_to_process(self.user)
self.assertIn(self.movie_item, items)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_selectors.py:209*

### test_get_items_to_process_includes_completed_changed_tv

**Category**: workflow  
**Description**: Workflow: Changed completed TV shows should still be selected.  
**Expected**: self.assertIn(self.tv_item, items)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_tv_changes, mock_movie_changes

'Changed completed TV shows should still be selected.'
mock_tv_changes.return_value = {self.tv_item.media_id}
mock_movie_changes.return_value = set()
TV.objects.filter(item=self.tv_item, user=self.user).update(status=Status.COMPLETED.value)
Event.objects.create(item=self.season_item, content_number=1, datetime=timezone.now() - timezone.timedelta(days=30))
items = get_items_to_process(self.user)
self.assertIn(self.tv_item, items)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_selectors.py:93*

### test_get_items_to_process_excludes_unchanged_tv_with_events

**Category**: workflow  
**Description**: Workflow: Tracked TV with existing season events should be skipped when unchanged.  
**Expected**: self.assertNotIn(self.tv_item, items)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_tv_changes, mock_movie_changes

'Tracked TV with existing season events should be skipped when unchanged.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = set()
Event.objects.create(item=self.season_item, content_number=1, datetime=timezone.now() - timezone.timedelta(days=30))
items = get_items_to_process(self.user)
self.assertNotIn(self.tv_item, items)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_selectors.py:117*

### test_get_items_to_process_includes_tv_without_season_events

**Category**: workflow  
**Description**: Workflow: Tracked TMDB TV should bootstrap even when no season events exist yet.  
**Expected**: self.assertIn(self.tv_item, items)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_tv_changes, mock_movie_changes

'Tracked TMDB TV should bootstrap even when no season events exist yet.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = set()
items = get_items_to_process(self.user)
self.assertIn(self.tv_item, items)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_selectors.py:137*

### test_get_items_to_process_excludes_unchanged_movie_with_events

**Category**: workflow  
**Description**: Workflow: Tracked TMDB movies with events should be skipped when unchanged.  
**Expected**: self.assertNotIn(self.movie_item, items)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_tv_changes, mock_movie_changes

'Tracked TMDB movies with events should be skipped when unchanged.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = set()
Event.objects.create(item=self.movie_item, content_number=None, datetime=timezone.now() - timezone.timedelta(days=30))
items = get_items_to_process(self.user)
self.assertNotIn(self.movie_item, items)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_selectors.py:169*

### test_fetch_releases_all_types

**Category**: workflow  
**Description**: Workflow: Test fetch_releases with all media types.  
**Expected**: self.assertIn('1984', result)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test fetch_releases with all media types.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = set()
mock_process_tv.side_effect = lambda _, events_bulk: events_bulk.append(Event(item=self.season_item, content_number=1, datetime=timezone.now()))
mock_process_other.side_effect = lambda item, events_bulk: events_bulk.append(Event(item=item, content_number=1, datetime=timezone.now()))
mock_process_comic.side_effect = lambda item, events_bulk: events_bulk.append(Event(item=item, content_number=1, datetime=timezone.now()))
mock_process_anime_bulk.side_effect = lambda items, events_bulk: [events_bulk.append(Event(item=item, content_number=1, datetime=timezone.now())) for item in items]
result = fetch_releases(self.user.id)
mock_process_anime_bulk.assert_called_once()
anime_items = mock_process_anime_bulk.call_args[0][0]
self.assertEqual(len(anime_items), 1)
self.assertEqual(anime_items[0].id, self.anime_item.id)
self.assertTrue(Event.objects.filter(item=self.season_item).exists())
self.assertEqual(mock_process_other.call_count, 3)
self.assertTrue(Event.objects.filter(item=self.anime_item).exists())
self.assertTrue(Event.objects.filter(item=self.movie_item).exists())
self.assertTrue(Event.objects.filter(item=self.manga_item).exists())
self.assertTrue(Event.objects.filter(item=self.book_item).exists())
self.assertTrue(Event.objects.filter(item=self.comic_item).exists())
self.assertIn('Perfect Blue', result)
self.assertIn('The Godfather', result)
self.assertIn('Breaking Bad', result)
self.assertIn('Berserk', result)
self.assertIn('1984', result)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_main.py:21*

### test_fetch_releases_returns_when_no_items_to_process

**Category**: workflow  
**Description**: Workflow: The task should return early when nothing is eligible.  
**Expected**: self.assertEqual(result, 'No items to process')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'The task should return early when nothing is eligible.'
mock_get_items_to_process.return_value = []
result = fetch_releases(self.user.id)
self.assertEqual(result, 'No items to process')
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_main.py:125*

### test_fetch_releases_all_types

**Category**: workflow  
**Description**: Workflow: Test fetch_releases with all media types.  
**Expected**: self.assertIn('1984', result)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_process_anime_bulk, mock_process_other, mock_process_tv, mock_process_comic, mock_movie_changes, mock_tv_changes

'Test fetch_releases with all media types.'
mock_tv_changes.return_value = set()
mock_movie_changes.return_value = set()
mock_process_tv.side_effect = lambda _, events_bulk: events_bulk.append(Event(item=self.season_item, content_number=1, datetime=timezone.now()))
mock_process_other.side_effect = lambda item, events_bulk: events_bulk.append(Event(item=item, content_number=1, datetime=timezone.now()))
mock_process_comic.side_effect = lambda item, events_bulk: events_bulk.append(Event(item=item, content_number=1, datetime=timezone.now()))
mock_process_anime_bulk.side_effect = lambda items, events_bulk: [events_bulk.append(Event(item=item, content_number=1, datetime=timezone.now())) for item in items]
result = fetch_releases(self.user.id)
mock_process_anime_bulk.assert_called_once()
anime_items = mock_process_anime_bulk.call_args[0][0]
self.assertEqual(len(anime_items), 1)
self.assertEqual(anime_items[0].id, self.anime_item.id)
self.assertTrue(Event.objects.filter(item=self.season_item).exists())
self.assertEqual(mock_process_other.call_count, 3)
self.assertTrue(Event.objects.filter(item=self.anime_item).exists())
self.assertTrue(Event.objects.filter(item=self.movie_item).exists())
self.assertTrue(Event.objects.filter(item=self.manga_item).exists())
self.assertTrue(Event.objects.filter(item=self.book_item).exists())
self.assertTrue(Event.objects.filter(item=self.comic_item).exists())
self.assertIn('Perfect Blue', result)
self.assertIn('The Godfather', result)
self.assertIn('Breaking Bad', result)
self.assertIn('Berserk', result)
self.assertIn('1984', result)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_main.py:21*

### test_fetch_releases_returns_when_no_items_to_process

**Category**: workflow  
**Description**: Workflow: The task should return early when nothing is eligible.  
**Expected**: self.assertEqual(result, 'No items to process')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_items_to_process

'The task should return early when nothing is eligible.'
mock_get_items_to_process.return_value = []
result = fetch_releases(self.user.id)
self.assertEqual(result, 'No items to process')
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_main.py:125*

### test_get_existing_media_multiple_types

**Category**: workflow  
**Description**: Workflow: Test get_existing_media with different media types.  
**Expected**: self.assertEqual(len(existing[MediaTypes.TV.value][Sources.TMDB.value]), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

'Test get_existing_media with different media types.'
movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie')
movie = Movie.objects.create(item=movie_item, user=self.user)
tv_item = Item.objects.create(media_id='1399', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='TV Show')
tv = TV.objects.create(item=tv_item, user=self.user)
existing = get_existing_media(self.user)
self.assertIn(MediaTypes.MOVIE.value, existing)
self.assertIn(MediaTypes.TV.value, existing)
self.assertEqual(len(existing[MediaTypes.MOVIE.value][Sources.TMDB.value]), 1)
self.assertEqual(len(existing[MediaTypes.TV.value][Sources.TMDB.value]), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_import_helpers.py:70*

### test_should_process_media_new_mode_not_exists

**Category**: workflow  
**Description**: Workflow: Test should_process_media in new mode when media doesn't exist.  
**Expected**: self.assertTrue(result)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
"Test should_process_media in new mode when media doesn't exist."
existing_media = defaultdict(lambda: defaultdict(dict))
to_delete = defaultdict(lambda: defaultdict(set))
result = should_process_media(existing_media, to_delete, media_type=MediaTypes.MOVIE.value, source=Sources.TMDB.value, media_id='238', mode='new')
self.assertTrue(result)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_import_helpers.py:116*

### test_get_existing_media_multiple_types

**Category**: workflow  
**Description**: Workflow: Test get_existing_media with different media types.  
**Expected**: self.assertEqual(len(existing[MediaTypes.TV.value][Sources.TMDB.value]), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test get_existing_media with different media types.'
movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie')
movie = Movie.objects.create(item=movie_item, user=self.user)
tv_item = Item.objects.create(media_id='1399', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='TV Show')
tv = TV.objects.create(item=tv_item, user=self.user)
existing = get_existing_media(self.user)
self.assertIn(MediaTypes.MOVIE.value, existing)
self.assertIn(MediaTypes.TV.value, existing)
self.assertEqual(len(existing[MediaTypes.MOVIE.value][Sources.TMDB.value]), 1)
self.assertEqual(len(existing[MediaTypes.TV.value][Sources.TMDB.value]), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_import_helpers.py:70*

### test_should_process_media_new_mode_not_exists

**Category**: workflow  
**Description**: Workflow: Test should_process_media in new mode when media doesn't exist.  
**Expected**: self.assertTrue(result)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
"Test should_process_media in new mode when media doesn't exist."
existing_media = defaultdict(lambda: defaultdict(dict))
to_delete = defaultdict(lambda: defaultdict(set))
result = should_process_media(existing_media, to_delete, media_type=MediaTypes.MOVIE.value, source=Sources.TMDB.value, media_id='238', mode='new')
self.assertTrue(result)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_import_helpers.py:116*

### test_import_movie

**Category**: workflow  
**Description**: Workflow: test import movie  
**Expected**: self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
self.user = User.objects.create_user(username='test', password='12345')

def _bulk_create(objs, model, batch_size=500, default_user=None):
    model.objects.bulk_create(objs)
    return objs
patcher = unittest.mock.patch('integrations.imports.helpers.bulk_create_with_history', side_effect=_bulk_create)
self.mock_bulk = patcher.start()
self.addCleanup(patcher.stop)

mock_search.return_value = {'results': [{'media_id': '550', 'title': 'Inception', 'year': 2010}]}
csv = self._csv([['Inception', 2010, 9, '2024-01-01', '', 'movie']])
importer = SensCritiqueCSVImporter(self.user)
result = importer.run(csv)
self.assertEqual(importer.imported, 1)
self.assertIn('1 imported', result)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_senscritique.py:49*

### test_fallback_to_manual_when_no_results

**Category**: workflow  
**Description**: Workflow: test fallback to manual when no results  
**Expected**: self.assertEqual(movie.item.source, 'manual')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
self.user = User.objects.create_user(username='test', password='12345')

def _bulk_create(objs, model, batch_size=500, default_user=None):
    model.objects.bulk_create(objs)
    return objs
patcher = unittest.mock.patch('integrations.imports.helpers.bulk_create_with_history', side_effect=_bulk_create)
self.mock_bulk = patcher.start()
self.addCleanup(patcher.stop)

mock_search.return_value = {'results': []}
csv = self._csv([['Obscure Film XYZ', 2023, 7, '2024-01-01', '', 'movie']])
importer = SensCritiqueCSVImporter(self.user)
importer.run(csv)
self.assertEqual(importer.imported, 1)
movie = Movie.objects.get(user=self.user)
self.assertEqual(movie.item.source, 'manual')
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_senscritique.py:100*

### test_deduplication_skips_existing

**Category**: workflow  
**Description**: Workflow: test deduplication skips existing  
**Expected**: self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
self.user = User.objects.create_user(username='test', password='12345')

def _bulk_create(objs, model, batch_size=500, default_user=None):
    model.objects.bulk_create(objs)
    return objs
patcher = unittest.mock.patch('integrations.imports.helpers.bulk_create_with_history', side_effect=_bulk_create)
self.mock_bulk = patcher.start()
self.addCleanup(patcher.stop)

mock_search.return_value = {'results': [{'media_id': '550', 'title': 'Inception', 'year': 2010}]}
item = Item.objects.create(media_id='550', source='tmdb', media_type='movie', title='Inception', image='')
Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)
csv = self._csv([['Inception', 2010, 9, '2024-01-01', '', 'movie']])
importer = SensCritiqueCSVImporter(self.user)
importer.run(csv)
self.assertEqual(importer.skipped, 1)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_senscritique.py:110*

### test_overwrite_reimports_existing

**Category**: workflow  
**Description**: Workflow: test overwrite reimports existing  
**Expected**: self.assertEqual(importer.imported, 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
self.user = User.objects.create_user(username='test', password='12345')

def _bulk_create(objs, model, batch_size=500, default_user=None):
    model.objects.bulk_create(objs)
    return objs
patcher = unittest.mock.patch('integrations.imports.helpers.bulk_create_with_history', side_effect=_bulk_create)
self.mock_bulk = patcher.start()
self.addCleanup(patcher.stop)

mock_search.return_value = {'results': [{'media_id': '550', 'title': 'Inception', 'year': 2010}]}
item = Item.objects.create(media_id='550', source='tmdb', media_type='movie', title='Inception', image='')
Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)
csv = self._csv([['Inception', 2010, 9, '2024-01-01', '', 'movie']])
importer = SensCritiqueCSVImporter(self.user, overwrite=True)
importer.run(csv)
self.assertEqual(importer.skipped, 0)
self.assertEqual(importer.imported, 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_senscritique.py:127*

### test_multiple_types_in_one_csv

**Category**: workflow  
**Description**: Workflow: test multiple types in one csv  
**Expected**: self.assertEqual(Music.objects.filter(user=self.user).count(), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
self.user = User.objects.create_user(username='test', password='12345')

def _bulk_create(objs, model, batch_size=500, default_user=None):
    model.objects.bulk_create(objs)
    return objs
patcher = unittest.mock.patch('integrations.imports.helpers.bulk_create_with_history', side_effect=_bulk_create)
self.mock_bulk = patcher.start()
self.addCleanup(patcher.stop)

mock_search.return_value = {'results': [{'media_id': '1', 'title': 'X', 'year': 2020}]}
rows = [['Film A', 2020, 8, '2024-01-01', '', 'movie'], ['Show B', 2020, 7, '2024-01-01', '', 'tv'], ['Album C', 2020, 9, '2024-01-01', '', 'music']]
csv = self._csv(rows)
importer = SensCritiqueCSVImporter(self.user)
importer.run(csv)
self.assertEqual(importer.imported, 3)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
self.assertEqual(TV.objects.filter(user=self.user).count(), 1)
self.assertEqual(Music.objects.filter(user=self.user).count(), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_senscritique.py:166*

### test_import_movie

**Category**: workflow  
**Description**: Workflow: test import movie  
**Expected**: self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_search

mock_search.return_value = {'results': [{'media_id': '550', 'title': 'Inception', 'year': 2010}]}
csv = self._csv([['Inception', 2010, 9, '2024-01-01', '', 'movie']])
importer = SensCritiqueCSVImporter(self.user)
result = importer.run(csv)
self.assertEqual(importer.imported, 1)
self.assertIn('1 imported', result)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_senscritique.py:49*

### test_fallback_to_manual_when_no_results

**Category**: workflow  
**Description**: Workflow: test fallback to manual when no results  
**Expected**: self.assertEqual(movie.item.source, 'manual')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_search

mock_search.return_value = {'results': []}
csv = self._csv([['Obscure Film XYZ', 2023, 7, '2024-01-01', '', 'movie']])
importer = SensCritiqueCSVImporter(self.user)
importer.run(csv)
self.assertEqual(importer.imported, 1)
movie = Movie.objects.get(user=self.user)
self.assertEqual(movie.item.source, 'manual')
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_senscritique.py:100*

### test_deduplication_skips_existing

**Category**: workflow  
**Description**: Workflow: test deduplication skips existing  
**Expected**: self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_search

mock_search.return_value = {'results': [{'media_id': '550', 'title': 'Inception', 'year': 2010}]}
item = Item.objects.create(media_id='550', source='tmdb', media_type='movie', title='Inception', image='')
Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)
csv = self._csv([['Inception', 2010, 9, '2024-01-01', '', 'movie']])
importer = SensCritiqueCSVImporter(self.user)
importer.run(csv)
self.assertEqual(importer.skipped, 1)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_senscritique.py:110*

### test_overwrite_reimports_existing

**Category**: workflow  
**Description**: Workflow: test overwrite reimports existing  
**Expected**: self.assertEqual(importer.imported, 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_search

mock_search.return_value = {'results': [{'media_id': '550', 'title': 'Inception', 'year': 2010}]}
item = Item.objects.create(media_id='550', source='tmdb', media_type='movie', title='Inception', image='')
Movie.objects.create(item=item, user=self.user, status=Status.COMPLETED.value)
csv = self._csv([['Inception', 2010, 9, '2024-01-01', '', 'movie']])
importer = SensCritiqueCSVImporter(self.user, overwrite=True)
importer.run(csv)
self.assertEqual(importer.skipped, 0)
self.assertEqual(importer.imported, 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_senscritique.py:127*

### test_multiple_types_in_one_csv

**Category**: workflow  
**Description**: Workflow: test multiple types in one csv  
**Expected**: self.assertEqual(Music.objects.filter(user=self.user).count(), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_search

mock_search.return_value = {'results': [{'media_id': '1', 'title': 'X', 'year': 2020}]}
rows = [['Film A', 2020, 8, '2024-01-01', '', 'movie'], ['Show B', 2020, 7, '2024-01-01', '', 'tv'], ['Album C', 2020, 9, '2024-01-01', '', 'music']]
csv = self._csv(rows)
importer = SensCritiqueCSVImporter(self.user)
importer.run(csv)
self.assertEqual(importer.imported, 3)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
self.assertEqual(TV.objects.filter(user=self.user).count(), 1)
self.assertEqual(Music.objects.filter(user=self.user).count(), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_senscritique.py:166*

### test_tv_episode_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles TV episode mark played event.  
**Expected**: self.assertIsNotNone(episode.end_date)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('emby_webhook', kwargs={'token': 'test-token'})

'Test webhook handles TV episode mark played event.'
payload = {'Event': 'playback.stop', 'Item': {'Type': 'Episode', 'Name': 'The One Where Monica Gets a Roommate', 'ProductionYear': 1994, 'ProviderIds': {'Tvdb': '303821', 'Imdb': 'tt0583459'}, 'SeriesName': 'Friends', 'ParentIndexNumber': 1, 'IndexNumber': 1}, 'PlaybackInfo': {'PlayedToCompletion': True}}
data = {'data': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
tv_item = Item.objects.get(media_type=MediaTypes.TV.value, media_id='1668')
self.assertEqual(tv_item.title, 'Friends')
tv = TV.objects.get(item=tv_item, user=self.user)
self.assertEqual(tv.status, Status.IN_PROGRESS.value)
season = Season.objects.get(item__media_id='1668', item__season_number=1)
self.assertEqual(season.status, Status.IN_PROGRESS.value)
episode = Episode.objects.get(item__media_id='1668', item__season_number=1, item__episode_number=1)
self.assertIsNotNone(episode.end_date)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_emby.py:27*

### test_anime_episode_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles anime episode mark played event.  
**Expected**: self.assertEqual(anime.progress, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('emby_webhook', kwargs={'token': 'test-token'})

'Test webhook handles anime episode mark played event.'
payload = {'Event': 'playback.stop', 'Item': {'Type': 'Episode', 'Name': "The Journey's End", 'ProductionYear': 2003, 'ProviderIds': {'Tvdb': '9350138', 'Imdb': 'tt23861604'}, 'SeriesName': "Frieren: Beyond Journey's End", 'ParentIndexNumber': 1, 'IndexNumber': 1}, 'PlaybackInfo': {'PlayedToCompletion': True}}
data = {'data': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
anime = Anime.objects.get(item__media_id='52991', user=self.user)
self.assertEqual(anime.status, Status.IN_PROGRESS.value)
self.assertEqual(anime.progress, 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_emby.py:80*

### test_movie_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles movie mark played event.  
**Expected**: self.assertEqual(movie.progress, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('emby_webhook', kwargs={'token': 'test-token'})

'Test webhook handles movie mark played event.'
payload = {'Event': 'playback.stop', 'Item': {'Type': 'Movie', 'Name': 'The Matrix', 'ProductionYear': 1999, 'ProviderIds': {'Imdb': 'tt0133093', 'Tmdb': '603', 'Tvdb': '169', 'Official Website': 'http://www.warnerbros.com/matrix', 'Wikidata': 'Q83495', 'Wikipedia': 'The_Matrix'}}, 'PlaybackInfo': {'PlayedToCompletion': True}}
data = {'data': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
movie = Movie.objects.get(item__media_id='603', user=self.user)
self.assertEqual(movie.status, Status.COMPLETED.value)
self.assertEqual(movie.progress, 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_emby.py:121*

### test_anime_movie_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles movie mark played event.  
**Expected**: self.assertEqual(movie.progress, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('emby_webhook', kwargs={'token': 'test-token'})

'Test webhook handles movie mark played event.'
payload = {'Event': 'playback.stop', 'Item': {'Type': 'Movie', 'Name': 'Perfect Blue', 'ProductionYear': 1997, 'ProviderIds': {'Imdb': 'tt0156887', 'Tmdb': '10494', 'Tvdb': '3807'}}, 'PlaybackInfo': {'PlayedToCompletion': True}}
data = {'data': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
movie = Anime.objects.get(item__media_id='437', user=self.user)
self.assertEqual(movie.status, Status.COMPLETED.value)
self.assertEqual(movie.progress, 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_emby.py:162*

### test_repeated_watch

**Category**: workflow  
**Description**: Workflow: Test webhook handles repeated watches.  
**Expected**: self.assertEqual(movie[1].status, Status.COMPLETED.value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('emby_webhook', kwargs={'token': 'test-token'})

'Test webhook handles repeated watches.'
payload = {'Event': 'playback.stop', 'Item': {'Type': 'Movie', 'Name': 'The Matrix', 'ProductionYear': 1999, 'ProviderIds': {'Imdb': 'tt0133093', 'Tmdb': '603', 'Tvdb': '169', 'Official Website': 'http://www.warnerbros.com/matrix', 'Wikidata': 'Q83495', 'Wikipedia': 'The_Matrix'}}, 'PlaybackInfo': {'PlayedToCompletion': True}}
data = {'data': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
movie = Movie.objects.filter(item__media_id='603')
self.assertEqual(movie.count(), 2)
self.assertEqual(movie[0].status, Status.COMPLETED.value)
self.assertEqual(movie[1].status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_emby.py:295*

### test_extract_external_ids

**Category**: workflow  
**Description**: Workflow: Test extracting external IDs from provider payload.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('emby_webhook', kwargs={'token': 'test-token'})

'Test extracting external IDs from provider payload.'
payload = {'Event': 'playback.something_else', 'Item': {'Type': 'Movie', 'Name': 'The Matrix', 'ProductionYear': 1999, 'ProviderIds': {'Tmdb': '603', 'Tvdb': '169'}}, 'PlaybackInfo': {'PlayedToCompletion': True}}
expected = {'tmdb_id': '603', 'imdb_id': None, 'tvdb_id': '169'}
result = EmbyWebhookProcessor()._extract_external_ids(payload)
if result != expected:
    msg = f'Expected {expected}, got {result}'
    raise AssertionError(msg)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_emby.py:341*

### test_extract_external_ids_empty

**Category**: workflow  
**Description**: Workflow: Test handling empty provider payload.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('emby_webhook', kwargs={'token': 'test-token'})

'Test handling empty provider payload.'
payload = {'Event': 'playback.something_else', 'Item': {'Type': 'Movie', 'Name': 'The Matrix', 'ProductionYear': 1999, 'ProviderIds': {}}, 'PlaybackInfo': {'PlayedToCompletion': True}}
expected = {'tmdb_id': None, 'imdb_id': None, 'tvdb_id': None}
result = EmbyWebhookProcessor()._extract_external_ids(payload)
if result != expected:
    msg = f'Expected {expected}, got {result}'
    raise AssertionError(msg)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_emby.py:370*

### test_extract_external_ids_missing

**Category**: workflow  
**Description**: Workflow: Test handling missing ProviderIds.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('emby_webhook', kwargs={'token': 'test-token'})

'Test handling missing ProviderIds.'
payload = {'Event': 'playback.something_else', 'Item': {'Type': 'Movie', 'Name': 'The Matrix', 'ProductionYear': 1999}, 'PlaybackInfo': {'PlayedToCompletion': True}}
expected = {'tmdb_id': None, 'imdb_id': None, 'tvdb_id': None}
result = EmbyWebhookProcessor()._extract_external_ids(payload)
if result != expected:
    msg = f'Expected {expected}, got {result}'
    raise AssertionError(msg)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_emby.py:396*

### test_tv_episode_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles TV episode mark played event.  
**Expected**: self.assertIsNotNone(episode.end_date)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test webhook handles TV episode mark played event.'
payload = {'Event': 'playback.stop', 'Item': {'Type': 'Episode', 'Name': 'The One Where Monica Gets a Roommate', 'ProductionYear': 1994, 'ProviderIds': {'Tvdb': '303821', 'Imdb': 'tt0583459'}, 'SeriesName': 'Friends', 'ParentIndexNumber': 1, 'IndexNumber': 1}, 'PlaybackInfo': {'PlayedToCompletion': True}}
data = {'data': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
tv_item = Item.objects.get(media_type=MediaTypes.TV.value, media_id='1668')
self.assertEqual(tv_item.title, 'Friends')
tv = TV.objects.get(item=tv_item, user=self.user)
self.assertEqual(tv.status, Status.IN_PROGRESS.value)
season = Season.objects.get(item__media_id='1668', item__season_number=1)
self.assertEqual(season.status, Status.IN_PROGRESS.value)
episode = Episode.objects.get(item__media_id='1668', item__season_number=1, item__episode_number=1)
self.assertIsNotNone(episode.end_date)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_emby.py:27*

### test_anime_episode_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles anime episode mark played event.  
**Expected**: self.assertEqual(anime.progress, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test webhook handles anime episode mark played event.'
payload = {'Event': 'playback.stop', 'Item': {'Type': 'Episode', 'Name': "The Journey's End", 'ProductionYear': 2003, 'ProviderIds': {'Tvdb': '9350138', 'Imdb': 'tt23861604'}, 'SeriesName': "Frieren: Beyond Journey's End", 'ParentIndexNumber': 1, 'IndexNumber': 1}, 'PlaybackInfo': {'PlayedToCompletion': True}}
data = {'data': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
anime = Anime.objects.get(item__media_id='52991', user=self.user)
self.assertEqual(anime.status, Status.IN_PROGRESS.value)
self.assertEqual(anime.progress, 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_emby.py:80*

### test_trakt_oauth_uses_configured_public_url

**Category**: workflow  
**Description**: Workflow: Test Trakt authorization uses the configured public URL.  
**Expected**: self.assertEqual(state['redirect_uri'], 'https://yamtrack.example.com:8924/import/trakt/private')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**credentials)
self.client.login(**credentials)

'Test Trakt authorization uses the configured public URL.'
response = self.client.post(reverse('trakt_oauth'), {'mode': 'new', 'frequency': 'once', 'time': '14:30'})
self.assertEqual(response.status_code, 302)
redirect = urlparse(response['Location'])
query = parse_qs(redirect.query)
self.assertEqual(redirect.scheme, 'https')
self.assertEqual(redirect.netloc, 'trakt.tv')
self.assertEqual(query['client_id'], ['client'])
self.assertEqual(query['redirect_uri'], ['https://yamtrack.example.com:8924/import/trakt/private'])
state = self.client.session[query['state'][0]]
self.assertEqual(state['redirect_uri'], 'https://yamtrack.example.com:8924/import/trakt/private')
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_oauth_views.py:19*

### test_trakt_callback_reuses_stored_redirect_uri

**Category**: workflow  
**Description**: Workflow: Test the token exchange and import task reuse the original redirect URI.  
**Expected**: self.assertEqual(mock_import_trakt.call_args.kwargs['redirect_uri'], redirect_uri)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**credentials)
self.client.login(**credentials)

'Test the token exchange and import task reuse the original redirect URI.'
redirect_uri = 'https://yamtrack.example.com:8924/import/trakt/private'
session = self.client.session
session['state-token'] = {'mode': 'new', 'frequency': 'once', 'time': '14:30', 'redirect_uri': redirect_uri}
session.save()
mock_oauth_callback.return_value = {'refresh_token': 'refresh-token', 'username': 'trakt-user'}
response = self.client.get(reverse('import_trakt_private'), {'code': 'code', 'state': 'state-token'})
self.assertRedirects(response, reverse('import_data'))
mock_oauth_callback.assert_called_once()
self.assertEqual(mock_oauth_callback.call_args.kwargs['redirect_uri'], redirect_uri)
mock_import_trakt.assert_called_once()
self.assertEqual(mock_import_trakt.call_args.kwargs['redirect_uri'], redirect_uri)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_oauth_views.py:46*

### test_trakt_oauth_uses_configured_public_url

**Category**: workflow  
**Description**: Workflow: Test Trakt authorization uses the configured public URL.  
**Expected**: self.assertEqual(state['redirect_uri'], 'https://yamtrack.example.com:8924/import/trakt/private')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test Trakt authorization uses the configured public URL.'
response = self.client.post(reverse('trakt_oauth'), {'mode': 'new', 'frequency': 'once', 'time': '14:30'})
self.assertEqual(response.status_code, 302)
redirect = urlparse(response['Location'])
query = parse_qs(redirect.query)
self.assertEqual(redirect.scheme, 'https')
self.assertEqual(redirect.netloc, 'trakt.tv')
self.assertEqual(query['client_id'], ['client'])
self.assertEqual(query['redirect_uri'], ['https://yamtrack.example.com:8924/import/trakt/private'])
state = self.client.session[query['state'][0]]
self.assertEqual(state['redirect_uri'], 'https://yamtrack.example.com:8924/import/trakt/private')
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_oauth_views.py:19*

### test_trakt_callback_reuses_stored_redirect_uri

**Category**: workflow  
**Description**: Workflow: Test the token exchange and import task reuse the original redirect URI.  
**Expected**: self.assertEqual(mock_import_trakt.call_args.kwargs['redirect_uri'], redirect_uri)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_oauth_callback, mock_import_trakt

'Test the token exchange and import task reuse the original redirect URI.'
redirect_uri = 'https://yamtrack.example.com:8924/import/trakt/private'
session = self.client.session
session['state-token'] = {'mode': 'new', 'frequency': 'once', 'time': '14:30', 'redirect_uri': redirect_uri}
session.save()
mock_oauth_callback.return_value = {'refresh_token': 'refresh-token', 'username': 'trakt-user'}
response = self.client.get(reverse('import_trakt_private'), {'code': 'code', 'state': 'state-token'})
self.assertRedirects(response, reverse('import_data'))
mock_oauth_callback.assert_called_once()
self.assertEqual(mock_oauth_callback.call_args.kwargs['redirect_uri'], redirect_uri)
mock_import_trakt.assert_called_once()
self.assertEqual(mock_import_trakt.call_args.kwargs['redirect_uri'], redirect_uri)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_oauth_views.py:46*

### test_get_user_events

**Category**: workflow  
**Description**: Workflow: Test the get_user_events method.  
**Expected**: self.assertNotIn(self.past_event, limited_events)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.credentials_other = {'username': 'otheruser', 'password': 'testpassword'}
self.other_user = get_user_model().objects.create_user(**self.credentials_other)
self.tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.paused_movie_item = Item.objects.create(media_id='278', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Paused Movie')
self.dropped_movie_item = Item.objects.create(media_id='424', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Dropped Movie')
self.manga_item = Item.objects.create(media_id='66296374554', source=Sources.MANGAUPDATES.value, media_type=MediaTypes.MANGA.value, title='Test Manga')
self.tv = TV.objects.create(user=self.user, item=self.tv_item, status=Status.IN_PROGRESS.value)
self.other_tv = TV.objects.create(user=self.other_user, item=self.tv_item, status=Status.IN_PROGRESS.value)
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value)
self.paused_movie = Movie.objects.create(user=self.user, item=self.paused_movie_item, status=Status.PAUSED.value)
self.dropped_movie = Movie.objects.create(user=self.user, item=self.dropped_movie_item, status=Status.DROPPED.value)
self.manga = Manga.objects.create(user=self.user, item=self.manga_item, status=Status.IN_PROGRESS.value)
self.base_date = datetime.datetime(2025, 4, 15, 12, 0, 0, tzinfo=datetime.UTC)
self.yesterday = self.base_date - datetime.timedelta(days=1)
self.tomorrow = self.base_date + datetime.timedelta(days=1)
self.next_week = self.base_date + datetime.timedelta(days=7)
self.past_event = Event.objects.create(item=self.season_item, content_number=1, datetime=self.yesterday)
self.movie_event = Event.objects.create(item=self.movie_item, datetime=self.next_week)
self.paused_movie_event = Event.objects.create(item=self.paused_movie_item, datetime=self.next_week)
self.dropped_movie_event = Event.objects.create(item=self.dropped_movie_item, datetime=self.next_week)
self.season_event = Event.objects.create(item=self.season_item, content_number=2, datetime=self.tomorrow)
self.manga_event1 = Event.objects.create(item=self.manga_item, content_number=1, datetime=self.tomorrow)
self.manga_event2 = Event.objects.create(item=self.manga_item, content_number=2, datetime=self.next_week)

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

*Source: C:\yamtrack-fork\src\events\tests\test_models.py:269*

### test_get_user_events

**Category**: workflow  
**Description**: Workflow: Test the get_user_events method.  
**Expected**: self.assertNotIn(self.past_event, limited_events)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: C:\yamtrack-fork\src\events\tests\test_models.py:269*

### test_status_is_completed

**Category**: workflow  
**Description**: Workflow: test status is completed  
**Expected**: self.assertEqual(movie.status, Status.COMPLETED.value)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
self.user = User.objects.create_user(username='test', password='12345')

def _bulk_create(objs, model, batch_size=500, default_user=None):
    model.objects.bulk_create(objs)
    return objs
patcher = unittest.mock.patch('integrations.imports.helpers.bulk_create_with_history', side_effect=_bulk_create)
self.mock_bulk = patcher.start()
self.addCleanup(patcher.stop)

mock_resolve.return_value = ('550', 'tmdb', 'movie')
FilmAffinityRatingsImporter(self.user).run(RATINGS_HTML)
movie = Movie.objects.filter(user=self.user).first()
self.assertIsNotNone(movie)
self.assertEqual(movie.status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_filmaffinity.py:177*

### test_status_is_completed

**Category**: workflow  
**Description**: Workflow: test status is completed  
**Expected**: self.assertEqual(movie.status, Status.COMPLETED.value)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_resolve

mock_resolve.return_value = ('550', 'tmdb', 'movie')
FilmAffinityRatingsImporter(self.user).run(RATINGS_HTML)
movie = Movie.objects.filter(user=self.user).first()
self.assertIsNotNone(movie)
self.assertEqual(movie.status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_filmaffinity.py:177*

### test_get_anime_schedule_bulk_no_airing_schedule

**Category**: workflow  
**Description**: Workflow: Test get_anime_schedule_bulk with no airing schedule.  
**Expected**: self.assertEqual(start_date.day, 12)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test get_anime_schedule_bulk with no airing schedule.'
mock_api_request.return_value = {'data': {'Page': {'pageInfo': {'hasNextPage': False}, 'media': [{'idMal': 437, 'endDate': {'year': 1997, 'month': 8, 'day': 12}, 'episodes': 2, 'airingSchedule': {'nodes': []}}]}}}
mock_get_media_metadata.return_value = {'max_progress': 2, 'details': {'end_date': '1997-08-12'}}
result = get_anime_schedule_bulk(['437'])
self.assertIn('437', result)
self.assertEqual(len(result['437']), 1)
self.assertEqual(result['437'][0]['episode'], 2)
start_date = datetime.datetime.fromtimestamp(result['437'][0]['airingAt'], tz=ZoneInfo('UTC'))
self.assertEqual(start_date.year, 1997)
self.assertEqual(start_date.month, 8)
self.assertEqual(start_date.day, 12)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_anime.py:51*

### test_anilist_date_parser

**Category**: workflow  
**Description**: Workflow: Test anilist_date_parser function.  
**Expected**: self.assertIsNone(result)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test anilist_date_parser function.'
complete_date = {'year': 2024, 'month': 3, 'day': 28}
result = anilist_date_parser(complete_date)
dt = datetime.datetime.fromtimestamp(result, tz=ZoneInfo('UTC'))
self.assertEqual(dt.year, 2024)
self.assertEqual(dt.month, 3)
self.assertEqual(dt.day, 28)
partial_date = {'year': 2024, 'month': 3, 'day': None}
result = anilist_date_parser(partial_date)
dt = datetime.datetime.fromtimestamp(result, tz=ZoneInfo('UTC'))
self.assertEqual(dt.year, 2024)
self.assertEqual(dt.month, 3)
self.assertEqual(dt.day, 1)
year_only_date = {'year': 2024, 'month': None, 'day': None}
result = anilist_date_parser(year_only_date)
dt = datetime.datetime.fromtimestamp(result, tz=ZoneInfo('UTC'))
self.assertEqual(dt.year, 2024)
self.assertEqual(dt.month, 1)
self.assertEqual(dt.day, 1)
missing_year = {'year': None, 'month': 3, 'day': 28}
result = anilist_date_parser(missing_year)
self.assertIsNone(result)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_anime.py:122*

### test_process_anime_bulk

**Category**: workflow  
**Description**: Workflow: Test process_anime_bulk function.  
**Expected**: self.assertEqual(events_bulk[0].datetime, expected_date)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test process_anime_bulk function.'
mock_api_request.return_value = {'data': {'Page': {'pageInfo': {'hasNextPage': False}, 'media': [{'idMal': 437, 'endDate': {'year': 1997, 'month': 8, 'day': 5}, 'episodes': 1, 'airingSchedule': {'nodes': [{'episode': 1, 'airingAt': 870739200}]}}]}}}
events_bulk = []
process_anime_bulk([self.anime_item], events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, self.anime_item)
self.assertEqual(events_bulk[0].content_number, 1)
expected_date = datetime.datetime.fromtimestamp(870739200, tz=ZoneInfo('UTC'))
self.assertEqual(events_bulk[0].datetime, expected_date)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_anime.py:153*

### test_process_anime_bulk_no_matching_anime_anilist

**Category**: workflow  
**Description**: Workflow: Test process_anime_bulk with no matching anime in AniList.  
**Expected**: self.assertEqual(len(events_bulk), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test process_anime_bulk with no matching anime in AniList.'
mock_api_request.return_value = {'data': {'Page': {'pageInfo': {'hasNextPage': False}, 'media': []}}}
mock_get_media_metadata.return_value = {'max_progress': 1, 'details': {'end_date': '1997-08-05'}}
events_bulk = []
process_anime_bulk([self.anime_item], events_bulk)
self.assertEqual(len(events_bulk), 1)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_anime.py:187*

### test_get_anime_schedule_bulk_no_airing_schedule

**Category**: workflow  
**Description**: Workflow: Test get_anime_schedule_bulk with no airing schedule.  
**Expected**: self.assertEqual(start_date.day, 12)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_api_request, mock_get_media_metadata

'Test get_anime_schedule_bulk with no airing schedule.'
mock_api_request.return_value = {'data': {'Page': {'pageInfo': {'hasNextPage': False}, 'media': [{'idMal': 437, 'endDate': {'year': 1997, 'month': 8, 'day': 12}, 'episodes': 2, 'airingSchedule': {'nodes': []}}]}}}
mock_get_media_metadata.return_value = {'max_progress': 2, 'details': {'end_date': '1997-08-12'}}
result = get_anime_schedule_bulk(['437'])
self.assertIn('437', result)
self.assertEqual(len(result['437']), 1)
self.assertEqual(result['437'][0]['episode'], 2)
start_date = datetime.datetime.fromtimestamp(result['437'][0]['airingAt'], tz=ZoneInfo('UTC'))
self.assertEqual(start_date.year, 1997)
self.assertEqual(start_date.month, 8)
self.assertEqual(start_date.day, 12)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_anime.py:51*

### test_anilist_date_parser

**Category**: workflow  
**Description**: Workflow: Test anilist_date_parser function.  
**Expected**: self.assertIsNone(result)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test anilist_date_parser function.'
complete_date = {'year': 2024, 'month': 3, 'day': 28}
result = anilist_date_parser(complete_date)
dt = datetime.datetime.fromtimestamp(result, tz=ZoneInfo('UTC'))
self.assertEqual(dt.year, 2024)
self.assertEqual(dt.month, 3)
self.assertEqual(dt.day, 28)
partial_date = {'year': 2024, 'month': 3, 'day': None}
result = anilist_date_parser(partial_date)
dt = datetime.datetime.fromtimestamp(result, tz=ZoneInfo('UTC'))
self.assertEqual(dt.year, 2024)
self.assertEqual(dt.month, 3)
self.assertEqual(dt.day, 1)
year_only_date = {'year': 2024, 'month': None, 'day': None}
result = anilist_date_parser(year_only_date)
dt = datetime.datetime.fromtimestamp(result, tz=ZoneInfo('UTC'))
self.assertEqual(dt.year, 2024)
self.assertEqual(dt.month, 1)
self.assertEqual(dt.day, 1)
missing_year = {'year': None, 'month': 3, 'day': 28}
result = anilist_date_parser(missing_year)
self.assertIsNone(result)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_anime.py:122*

### test_process_anime_bulk

**Category**: workflow  
**Description**: Workflow: Test process_anime_bulk function.  
**Expected**: self.assertEqual(events_bulk[0].datetime, expected_date)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_api_request

'Test process_anime_bulk function.'
mock_api_request.return_value = {'data': {'Page': {'pageInfo': {'hasNextPage': False}, 'media': [{'idMal': 437, 'endDate': {'year': 1997, 'month': 8, 'day': 5}, 'episodes': 1, 'airingSchedule': {'nodes': [{'episode': 1, 'airingAt': 870739200}]}}]}}}
events_bulk = []
process_anime_bulk([self.anime_item], events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, self.anime_item)
self.assertEqual(events_bulk[0].content_number, 1)
expected_date = datetime.datetime.fromtimestamp(870739200, tz=ZoneInfo('UTC'))
self.assertEqual(events_bulk[0].datetime, expected_date)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_anime.py:153*

### test_process_anime_bulk_no_matching_anime_anilist

**Category**: workflow  
**Description**: Workflow: Test process_anime_bulk with no matching anime in AniList.  
**Expected**: self.assertEqual(len(events_bulk), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_api_request, mock_get_media_metadata

'Test process_anime_bulk with no matching anime in AniList.'
mock_api_request.return_value = {'data': {'Page': {'pageInfo': {'hasNextPage': False}, 'media': []}}}
mock_get_media_metadata.return_value = {'max_progress': 1, 'details': {'end_date': '1997-08-05'}}
events_bulk = []
process_anime_bulk([self.anime_item], events_bulk)
self.assertEqual(len(events_bulk), 1)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_anime.py:187*

### test_tv_episode_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles TV episode mark played event.  
**Expected**: self.assertIsNotNone(episode.end_date)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token', 'plex_usernames': 'testuser'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('plex_webhook', kwargs={'token': 'test-token'})

'Test webhook handles TV episode mark played event.'
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'episode', 'grandparentTitle': 'Friends', 'index': 1, 'parentIndex': 1, 'Guid': [{'id': 'imdb://tt0583459'}, {'id': 'tmdb://85987'}, {'id': 'tvdb://303821'}]}}
data = {'payload': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
tv_item = Item.objects.get(media_type=MediaTypes.TV.value, media_id='1668')
self.assertEqual(tv_item.title, 'Friends')
tv = TV.objects.get(item=tv_item, user=self.user)
self.assertEqual(tv.status, Status.IN_PROGRESS.value)
season = Season.objects.get(item__media_id='1668', item__season_number=1)
self.assertEqual(season.status, Status.IN_PROGRESS.value)
episode = Episode.objects.get(item__media_id='1668', item__season_number=1, item__episode_number=1)
self.assertIsNotNone(episode.end_date)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_plex.py:32*

### test_movie_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles movie mark played event.  
**Expected**: self.assertEqual(movie.progress, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token', 'plex_usernames': 'testuser'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('plex_webhook', kwargs={'token': 'test-token'})

'Test webhook handles movie mark played event.'
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'movie', 'title': 'The Matrix', 'Guid': [{'id': 'imdb://tt0133093'}, {'id': 'tmdb://603'}, {'id': 'tvdb://169'}]}}
data = {'payload': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
movie = Movie.objects.get(item__media_id='603', user=self.user)
self.assertEqual(movie.status, Status.COMPLETED.value)
self.assertEqual(movie.progress, 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_plex.py:90*

### test_anime_movie_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles movie mark played event.  
**Expected**: self.assertEqual(movie.progress, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token', 'plex_usernames': 'testuser'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('plex_webhook', kwargs={'token': 'test-token'})

'Test webhook handles movie mark played event.'
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'movie', 'title': 'Perfect Blue', 'Guid': [{'id': 'imdb://tt0156887'}, {'id': 'tmdb://10494'}, {'id': 'tvdb://3807'}]}}
data = {'payload': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
movie = Anime.objects.get(item__media_id='437', user=self.user)
self.assertEqual(movie.status, Status.COMPLETED.value)
self.assertEqual(movie.progress, 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_plex.py:134*

### test_anime_episode_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles anime episode mark played event.  
**Expected**: self.assertEqual(anime.progress, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token', 'plex_usernames': 'testuser'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('plex_webhook', kwargs={'token': 'test-token'})

'Test webhook handles anime episode mark played event.'
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'episode', 'grandparentTitle': "Frieren: Beyond Journey's End", 'index': 1, 'parentIndex': 1, 'Guid': [{'id': 'imdb://tt23861604'}, {'id': 'tmdb://3946240'}, {'id': 'tvdb://9350138'}]}}
data = {'payload': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
anime = Anime.objects.get(item__media_id='52991', user=self.user)
self.assertEqual(anime.status, Status.IN_PROGRESS.value)
self.assertEqual(anime.progress, 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_plex.py:178*

### test_repeated_watch

**Category**: workflow  
**Description**: Workflow: Test webhook handles repeated watches.  
**Expected**: self.assertEqual(movie[1].status, Status.COMPLETED.value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token', 'plex_usernames': 'testuser'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('plex_webhook', kwargs={'token': 'test-token'})

'Test webhook handles repeated watches.'
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'movie', 'title': 'The Matrix', 'Guid': [{'id': 'imdb://tt0133093'}, {'id': 'tmdb://603'}, {'id': 'tvdb://169'}]}}
data = {'payload': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
movie = Movie.objects.filter(item__media_id='603')
self.assertEqual(movie.count(), 2)
self.assertEqual(movie[0].status, Status.COMPLETED.value)
self.assertEqual(movie[1].status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_plex.py:287*

### test_username_matching

**Category**: workflow  
**Description**: Workflow: Test Plex username matching functionality.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token', 'plex_usernames': 'testuser'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('plex_webhook', kwargs={'token': 'test-token'})

'Test Plex username matching functionality.'
test_cases = [('testuser', 'testuser', True), ('testuser', 'TestUser', True), ('testuser', ' testuser ', True), ('testuser', 'testuser2', False), ('testuser1,testuser2', 'testuser1', True), ('testuser1, testuser2', 'testuser1', True), ('testuser1,testuser2', 'testuser3', False)]
base_payload = {'event': 'media.scrobble', 'Metadata': {'type': 'movie', 'title': 'Test Movie', 'Guid': [{'id': 'tmdb://123'}]}}
for i, (stored_usernames, incoming_username, should_match) in enumerate(test_cases):
    with self.subTest(f'Case {i + 1}: {stored_usernames} vs {incoming_username}'):
        self.user.plex_usernames = stored_usernames
        self.user.save()
        payload = base_payload.copy()
        payload['Account'] = {'title': incoming_username}
        response = self.client.post(self.url, data={'payload': json.dumps(payload)}, format='multipart')
        if should_match:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Movie.objects.count(), 1)
            Movie.objects.all().delete()
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Movie.objects.count(), 0)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_plex.py:335*

### test_anime_episode_anidb_guid_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles anime episode with anidb guid.  
**Expected**: mock_handle_anime.assert_called_once_with(849, 1, payload, self.user)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token', 'plex_usernames': 'testuser'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('plex_webhook', kwargs={'token': 'test-token'})

'Test webhook handles anime episode with anidb guid.'
mock_fetch_mapping_data.return_value = {'3651': {'mal_id': 849}}
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'episode', 'index': 1, 'parentIndex': 1, 'guid': 'com.plexapp.agents.hama://anidb-3651/1/1?lang=en'}}
data = {'payload': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
mock_handle_anime.assert_called_once_with(849, 1, payload, self.user)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_plex.py:384*

### test_tv_episode_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles TV episode mark played event.  
**Expected**: self.assertIsNotNone(episode.end_date)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test webhook handles TV episode mark played event.'
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'episode', 'grandparentTitle': 'Friends', 'index': 1, 'parentIndex': 1, 'Guid': [{'id': 'imdb://tt0583459'}, {'id': 'tmdb://85987'}, {'id': 'tvdb://303821'}]}}
data = {'payload': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
tv_item = Item.objects.get(media_type=MediaTypes.TV.value, media_id='1668')
self.assertEqual(tv_item.title, 'Friends')
tv = TV.objects.get(item=tv_item, user=self.user)
self.assertEqual(tv.status, Status.IN_PROGRESS.value)
season = Season.objects.get(item__media_id='1668', item__season_number=1)
self.assertEqual(season.status, Status.IN_PROGRESS.value)
episode = Episode.objects.get(item__media_id='1668', item__season_number=1, item__episode_number=1)
self.assertIsNotNone(episode.end_date)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_plex.py:32*

### test_movie_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles movie mark played event.  
**Expected**: self.assertEqual(movie.progress, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test webhook handles movie mark played event.'
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'movie', 'title': 'The Matrix', 'Guid': [{'id': 'imdb://tt0133093'}, {'id': 'tmdb://603'}, {'id': 'tvdb://169'}]}}
data = {'payload': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
movie = Movie.objects.get(item__media_id='603', user=self.user)
self.assertEqual(movie.status, Status.COMPLETED.value)
self.assertEqual(movie.progress, 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_plex.py:90*

### test_anime_movie_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles movie mark played event.  
**Expected**: self.assertEqual(movie.progress, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test webhook handles movie mark played event.'
payload = {'event': 'media.scrobble', 'Account': {'title': 'testuser'}, 'Metadata': {'type': 'movie', 'title': 'Perfect Blue', 'Guid': [{'id': 'imdb://tt0156887'}, {'id': 'tmdb://10494'}, {'id': 'tvdb://3807'}]}}
data = {'payload': json.dumps(payload)}
response = self.client.post(self.url, data=data, format='multipart')
self.assertEqual(response.status_code, 200)
movie = Anime.objects.get(item__media_id='437', user=self.user)
self.assertEqual(movie.status, Status.COMPLETED.value)
self.assertEqual(movie.progress, 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_plex.py:134*

### test_process_tv_season

**Category**: workflow  
**Description**: Workflow: Test processing for a TV season.  
**Expected**: self.assertEqual(events_bulk[0].datetime, expected_date)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test processing for a TV season.'
mock_tv.return_value = {'related': {'seasons': [{'season_number': 1, 'episodes': [1, 2, 3]}, {'season_number': 2, 'episodes': [1, 2]}, {'season_number': 3, 'episodes': [1]}]}, 'next_episode_season': 2}
mock_tv_with_seasons.return_value = {'season/1': {'image': 'http://example.com/season1.jpg', 'season_number': 1, 'episodes': [{'episode_number': 1, 'air_date': '2008-01-20'}, {'episode_number': 2, 'air_date': '2008-01-27'}, {'episode_number': 3, 'air_date': '2008-02-03'}], 'tvdb_id': '81189'}, 'season/2': {'image': 'http://example.com/season2.jpg', 'season_number': 2, 'episodes': [{'episode_number': 1, 'air_date': '2009-01-20'}, {'episode_number': 2, 'air_date': '2009-01-27'}], 'tvdb_id': '81189'}, 'season/3': {'image': 'http://example.com/season3.jpg', 'season_number': 3, 'episodes': [{'episode_number': 1, 'air_date': '2010-01-20'}], 'tvdb_id': '81189'}}
mock_get_tvmaze_episode_map.return_value = {'1_1': '2008-01-20T22:00:00+00:00', '1_2': '2008-01-27T22:00:00+00:00', '1_3': '2008-02-03T22:00:00+00:00'}
events_bulk = []
process_tv(self.tv_item, events_bulk)
self.assertEqual(len(events_bulk), 6)
self.assertEqual(events_bulk[0].item, self.season_item)
self.assertEqual(events_bulk[0].content_number, 1)
expected_date = datetime.datetime.fromisoformat('2008-01-20T22:00:00+00:00')
self.assertEqual(events_bulk[0].datetime, expected_date)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_tv.py:29*

### test_process_tv_reopens_completed_show_with_new_season_as_planning

**Category**: workflow  
**Description**: Workflow: Completed TV should reopen and create the discovered season as planning.  
**Expected**: self.assertEqual(len(events_bulk), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Completed TV should reopen and create the discovered season as planning.'
TV.objects.filter(item=self.tv_item, user=self.user).update(status=Status.COMPLETED.value)
Season.objects.filter(item=self.season_item, user=self.user).update(status=Status.COMPLETED.value)
Event.objects.create(item=self.season_item, content_number=1, datetime=date_parser('2008-01-20'))
mock_tv.return_value = {'related': {'seasons': [{'season_number': 1, 'episodes': [1]}, {'season_number': 2, 'episodes': [1]}]}, 'next_episode_season': 2}
mock_tv_with_seasons.return_value = {'season/2': {'image': 'http://example.com/season2.jpg', 'season_number': 2, 'episodes': [{'episode_number': 1, 'air_date': '2027-01-20'}], 'tvdb_id': '81189'}}
mock_get_tvmaze_episode_map.return_value = {}
events_bulk = []
process_tv(self.tv_item, events_bulk)
season_two_item = Item.objects.get(media_id=self.tv_item.media_id, source=self.tv_item.source, media_type=self.season_item.media_type, season_number=2)
season_two = Season.objects.get(item=season_two_item, user=self.user)
tv = TV.objects.get(item=self.tv_item, user=self.user)
self.assertEqual(tv.status, Status.IN_PROGRESS.value)
self.assertEqual(season_two.status, Status.PLANNING.value)
self.assertEqual(len(events_bulk), 1)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_tv.py:96*

### test_process_tv_does_not_reopen_completed_show_for_past_only_season

**Category**: workflow  
**Description**: Workflow: Past-only seasons should not reopen a completed TV entry.  
**Expected**: self.assertEqual(len(events_bulk), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Past-only seasons should not reopen a completed TV entry.'
TV.objects.filter(item=self.tv_item, user=self.user).update(status=Status.COMPLETED.value)
Season.objects.filter(item=self.season_item, user=self.user).update(status=Status.COMPLETED.value)
Event.objects.create(item=self.season_item, content_number=1, datetime=date_parser('2008-01-20'))
mock_tv.return_value = {'related': {'seasons': [{'season_number': 1, 'episodes': [1]}, {'season_number': 2, 'episodes': [1]}]}, 'next_episode_season': 2}
mock_tv_with_seasons.return_value = {'season/2': {'image': 'http://example.com/season2.jpg', 'season_number': 2, 'episodes': [{'episode_number': 1, 'air_date': '2010-01-20'}], 'tvdb_id': '81189'}}
mock_get_tvmaze_episode_map.return_value = {}
events_bulk = []
process_tv(self.tv_item, events_bulk)
tv = TV.objects.get(item=self.tv_item, user=self.user)
self.assertEqual(tv.status, Status.COMPLETED.value)
self.assertFalse(Season.objects.filter(item__media_id=self.tv_item.media_id, item__source=self.tv_item.source, item__season_number=2, user=self.user).exists())
self.assertEqual(len(events_bulk), 1)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_tv.py:155*

### test_get_seasons_to_process_returns_empty_when_no_seasons

**Category**: workflow  
**Description**: Workflow: TV metadata without seasons should short-circuit processing.  
**Expected**: self.assertEqual(get_seasons_to_process(self.tv_item), [])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'TV metadata without seasons should short-circuit processing.'
mock_tv.return_value = {'related': {'seasons': []}}
self.assertEqual(get_seasons_to_process(self.tv_item), [])
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_tv.py:296*

### test_process_tv_returns_when_no_seasons_need_processing

**Category**: workflow  
**Description**: Workflow: process_tv should stop cleanly when there is nothing new to fetch.  
**Expected**: self.assertEqual(events_bulk, [])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'process_tv should stop cleanly when there is nothing new to fetch.'
mock_get_seasons_to_process.return_value = []
events_bulk = []
process_tv(self.tv_item, events_bulk)
self.assertEqual(events_bulk, [])
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_tv.py:303*

### test_process_season_episodes_handles_missing_tvdb_and_episodes

**Category**: workflow  
**Description**: Workflow: A season without TVDB data or episodes should not add events.  
**Expected**: self.assertEqual(events_bulk, [])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'A season without TVDB data or episodes should not add events.'
events_bulk = []
process_season_episodes(self.season_item, {'season_number': 1, 'episodes': []}, events_bulk)
self.assertEqual(events_bulk, [])
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_tv.py:315*

### test_process_tv_season

**Category**: workflow  
**Description**: Workflow: Test processing for a TV season.  
**Expected**: self.assertEqual(events_bulk[0].datetime, expected_date)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_tvmaze_episode_map, mock_tv_with_seasons, mock_tv

'Test processing for a TV season.'
mock_tv.return_value = {'related': {'seasons': [{'season_number': 1, 'episodes': [1, 2, 3]}, {'season_number': 2, 'episodes': [1, 2]}, {'season_number': 3, 'episodes': [1]}]}, 'next_episode_season': 2}
mock_tv_with_seasons.return_value = {'season/1': {'image': 'http://example.com/season1.jpg', 'season_number': 1, 'episodes': [{'episode_number': 1, 'air_date': '2008-01-20'}, {'episode_number': 2, 'air_date': '2008-01-27'}, {'episode_number': 3, 'air_date': '2008-02-03'}], 'tvdb_id': '81189'}, 'season/2': {'image': 'http://example.com/season2.jpg', 'season_number': 2, 'episodes': [{'episode_number': 1, 'air_date': '2009-01-20'}, {'episode_number': 2, 'air_date': '2009-01-27'}], 'tvdb_id': '81189'}, 'season/3': {'image': 'http://example.com/season3.jpg', 'season_number': 3, 'episodes': [{'episode_number': 1, 'air_date': '2010-01-20'}], 'tvdb_id': '81189'}}
mock_get_tvmaze_episode_map.return_value = {'1_1': '2008-01-20T22:00:00+00:00', '1_2': '2008-01-27T22:00:00+00:00', '1_3': '2008-02-03T22:00:00+00:00'}
events_bulk = []
process_tv(self.tv_item, events_bulk)
self.assertEqual(len(events_bulk), 6)
self.assertEqual(events_bulk[0].item, self.season_item)
self.assertEqual(events_bulk[0].content_number, 1)
expected_date = datetime.datetime.fromisoformat('2008-01-20T22:00:00+00:00')
self.assertEqual(events_bulk[0].datetime, expected_date)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_tv.py:29*

### test_process_tv_reopens_completed_show_with_new_season_as_planning

**Category**: workflow  
**Description**: Workflow: Completed TV should reopen and create the discovered season as planning.  
**Expected**: self.assertEqual(len(events_bulk), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_tv, mock_tv_with_seasons, mock_get_tvmaze_episode_map

'Completed TV should reopen and create the discovered season as planning.'
TV.objects.filter(item=self.tv_item, user=self.user).update(status=Status.COMPLETED.value)
Season.objects.filter(item=self.season_item, user=self.user).update(status=Status.COMPLETED.value)
Event.objects.create(item=self.season_item, content_number=1, datetime=date_parser('2008-01-20'))
mock_tv.return_value = {'related': {'seasons': [{'season_number': 1, 'episodes': [1]}, {'season_number': 2, 'episodes': [1]}]}, 'next_episode_season': 2}
mock_tv_with_seasons.return_value = {'season/2': {'image': 'http://example.com/season2.jpg', 'season_number': 2, 'episodes': [{'episode_number': 1, 'air_date': '2027-01-20'}], 'tvdb_id': '81189'}}
mock_get_tvmaze_episode_map.return_value = {}
events_bulk = []
process_tv(self.tv_item, events_bulk)
season_two_item = Item.objects.get(media_id=self.tv_item.media_id, source=self.tv_item.source, media_type=self.season_item.media_type, season_number=2)
season_two = Season.objects.get(item=season_two_item, user=self.user)
tv = TV.objects.get(item=self.tv_item, user=self.user)
self.assertEqual(tv.status, Status.IN_PROGRESS.value)
self.assertEqual(season_two.status, Status.PLANNING.value)
self.assertEqual(len(events_bulk), 1)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_tv.py:96*

### test_process_tv_does_not_reopen_completed_show_for_past_only_season

**Category**: workflow  
**Description**: Workflow: Past-only seasons should not reopen a completed TV entry.  
**Expected**: self.assertEqual(len(events_bulk), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_tv, mock_tv_with_seasons, mock_get_tvmaze_episode_map

'Past-only seasons should not reopen a completed TV entry.'
TV.objects.filter(item=self.tv_item, user=self.user).update(status=Status.COMPLETED.value)
Season.objects.filter(item=self.season_item, user=self.user).update(status=Status.COMPLETED.value)
Event.objects.create(item=self.season_item, content_number=1, datetime=date_parser('2008-01-20'))
mock_tv.return_value = {'related': {'seasons': [{'season_number': 1, 'episodes': [1]}, {'season_number': 2, 'episodes': [1]}]}, 'next_episode_season': 2}
mock_tv_with_seasons.return_value = {'season/2': {'image': 'http://example.com/season2.jpg', 'season_number': 2, 'episodes': [{'episode_number': 1, 'air_date': '2010-01-20'}], 'tvdb_id': '81189'}}
mock_get_tvmaze_episode_map.return_value = {}
events_bulk = []
process_tv(self.tv_item, events_bulk)
tv = TV.objects.get(item=self.tv_item, user=self.user)
self.assertEqual(tv.status, Status.COMPLETED.value)
self.assertFalse(Season.objects.filter(item__media_id=self.tv_item.media_id, item__source=self.tv_item.source, item__season_number=2, user=self.user).exists())
self.assertEqual(len(events_bulk), 1)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_tv.py:155*

### test_get_seasons_to_process_returns_empty_when_no_seasons

**Category**: workflow  
**Description**: Workflow: TV metadata without seasons should short-circuit processing.  
**Expected**: self.assertEqual(get_seasons_to_process(self.tv_item), [])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_tv

'TV metadata without seasons should short-circuit processing.'
mock_tv.return_value = {'related': {'seasons': []}}
self.assertEqual(get_seasons_to_process(self.tv_item), [])
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_tv.py:296*

### test_process_entry

**Category**: workflow  
**Description**: Workflow: Test processing an entry from Kitsu.  
**Expected**: self.assertEqual(instance.notes, 'Great series!')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
with Path(mock_path / 'import_kitsu_anime.json').open() as file:
    self.sample_anime_response = json.load(file)
with Path(mock_path / 'import_kitsu_manga.json').open() as file:
    self.sample_manga_response = json.load(file)
self.importer = kitsu.KitsuImporter('testuser', self.user, 'new')

'Test processing an entry from Kitsu.'
entry = self.sample_anime_response['data'][0]
media_lookup = {item['id']: item for item in self.sample_anime_response['included'] if item['type'] == 'anime'}
mapping_lookup = {item['id']: item for item in self.sample_anime_response['included'] if item['type'] == 'mappings'}
self.importer._process_entry(entry, MediaTypes.ANIME.value, media_lookup, mapping_lookup)
instance = self.importer.bulk_media[MediaTypes.ANIME.value][0]
self.assertEqual(instance.item.media_id, '1')
self.assertIsInstance(instance, Anime)
self.assertEqual(instance.score, 9)
self.assertEqual(instance.progress, 26)
self.assertEqual(instance.status, Status.COMPLETED.value)
self.assertEqual(instance.notes, 'Great series!')
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_kitsu.py:88*

### test_process_entry

**Category**: workflow  
**Description**: Workflow: Test processing an entry from Kitsu.  
**Expected**: self.assertEqual(instance.notes, 'Great series!')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test processing an entry from Kitsu.'
entry = self.sample_anime_response['data'][0]
media_lookup = {item['id']: item for item in self.sample_anime_response['included'] if item['type'] == 'anime'}
mapping_lookup = {item['id']: item for item in self.sample_anime_response['included'] if item['type'] == 'mappings'}
self.importer._process_entry(entry, MediaTypes.ANIME.value, media_lookup, mapping_lookup)
instance = self.importer.bulk_media[MediaTypes.ANIME.value][0]
self.assertEqual(instance.item.media_id, '1')
self.assertIsInstance(instance, Anime)
self.assertEqual(instance.score, 9)
self.assertEqual(instance.progress, 26)
self.assertEqual(instance.status, Status.COMPLETED.value)
self.assertEqual(instance.notes, 'Great series!')
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_kitsu.py:88*

### test_mark_user_messages_shown

**Category**: workflow  
**Description**: Workflow: Posting to the mark-shown endpoint should timestamp only rendered rows.  
**Expected**: self.assertIsNone(third_message.shown_at)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

'Posting to the mark-shown endpoint should timestamp only rendered rows.'
first_message = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='First message')
second_message = UserMessage.objects.create(user=self.user, level=UserMessageLevel.SUCCESS, message='Second message')
third_message = UserMessage.objects.create(user=self.user, level=UserMessageLevel.WARNING, message='Third message')
response = self.client.post(reverse('mark_user_messages_shown'), {'message_ids': [first_message.id, second_message.id]})
self.assertEqual(response.status_code, 204)
first_message.refresh_from_db()
second_message.refresh_from_db()
third_message.refresh_from_db()
self.assertIsNotNone(first_message.shown_at)
self.assertIsNotNone(second_message.shown_at)
self.assertIsNone(third_message.shown_at)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_user_messages.py:35*

### test_mark_user_messages_shown

**Category**: workflow  
**Description**: Workflow: Posting to the mark-shown endpoint should timestamp only rendered rows.  
**Expected**: self.assertIsNone(third_message.shown_at)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Posting to the mark-shown endpoint should timestamp only rendered rows.'
first_message = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='First message')
second_message = UserMessage.objects.create(user=self.user, level=UserMessageLevel.SUCCESS, message='Second message')
third_message = UserMessage.objects.create(user=self.user, level=UserMessageLevel.WARNING, message='Third message')
response = self.client.post(reverse('mark_user_messages_shown'), {'message_ids': [first_message.id, second_message.id]})
self.assertEqual(response.status_code, 204)
first_message.refresh_from_db()
second_message.refresh_from_db()
third_message.refresh_from_db()
self.assertIsNotNone(first_message.shown_at)
self.assertIsNotNone(second_message.shown_at)
self.assertIsNone(third_message.shown_at)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_user_messages.py:35*

### test_process_watched_movie

**Category**: workflow  
**Description**: Workflow: Test processing a movie entry.  
**Expected**: self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 2)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)

'Test processing a movie entry.'
movie_entry = {'type': 'movie', 'movie': {'title': 'Test Movie', 'ids': {'tmdb': 67890}}, 'watched_at': '2023-01-02T00:00:00.000Z'}
mock_get_metadata.return_value = {'title': 'Test Movie', 'image': 'movie_image.jpg'}
trakt_importer = TraktImporter('test', self.user, 'new')
trakt_importer.process_watched_movie(movie_entry)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 1)
self.assertEqual(len(trakt_importer.media_instances[MediaTypes.MOVIE.value]), 1)
movie_obj = trakt_importer.bulk_media[MediaTypes.MOVIE.value][0]
self.assertEqual(movie_obj.progress, 1)
trakt_importer.process_watched_movie(movie_entry)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 2)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_trakt.py:32*

### test_process_watched_episode

**Category**: workflow  
**Description**: Workflow: Test processing an episode entry.  
**Expected**: self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.EPISODE.value]), 2)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)

'Test processing an episode entry.'
episode_entry = {'type': 'episode', 'episode': {'season': 1, 'number': 1, 'title': 'Pilot'}, 'show': {'title': 'Test Show', 'ids': {'tmdb': 12345}}, 'watched_at': '2023-01-01T00:00:00.000Z'}

def mock_metadata_side_effect(media_type, _, __, ___=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Test Show', 'image': 'tv_image.jpg', 'last_episode_season': 1, 'max_progress': 1}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Season 1', 'image': 'season_image.jpg', 'episodes': [{'episode_number': 1, 'still_path': '/still.jpg'}], 'max_progress': 1}
    return None
mock_get_metadata.side_effect = mock_metadata_side_effect
trakt_importer = TraktImporter('testuser', self.user, 'new')
trakt_importer.process_watched_episode(episode_entry)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.TV.value]), 1)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.SEASON.value]), 1)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.EPISODE.value]), 1)
trakt_importer.process_watched_episode(episode_entry)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.EPISODE.value]), 2)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_trakt.py:60*

### test_process_watchlist

**Category**: workflow  
**Description**: Workflow: Test processing a watchlist entry.  
**Expected**: self.assertEqual(tv_obj.status, Status.PLANNING.value)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)

'Test processing a watchlist entry.'
watchlist_entry = {'listed_at': '2023-01-01T00:00:00.000Z', 'type': 'show', 'show': {'title': 'Watchlist Show', 'ids': {'tmdb': 54321}}}
mock_make_request.return_value = [watchlist_entry]
mock_get_metadata.return_value = {'title': 'Watchlist Show', 'image': 'show_image.jpg'}
trakt_importer = TraktImporter('testuser', self.user, 'new')
trakt_importer.process_watchlist()
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.TV.value]), 1)
tv_obj = trakt_importer.bulk_media[MediaTypes.TV.value][0]
self.assertEqual(tv_obj.status, Status.PLANNING.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_trakt.py:101*

### test_process_ratings

**Category**: workflow  
**Description**: Workflow: Test processing a rating entry.  
**Expected**: self.assertEqual(movie_obj.score, 8)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)

'Test processing a rating entry.'
rating_entry = {'rated_at': '2023-01-01T00:00:00.000Z', 'type': 'movie', 'movie': {'title': 'Rated Movie', 'ids': {'tmdb': 238}}, 'rating': 8}
mock_make_request.return_value = [rating_entry]
mock_get_metadata.return_value = {'title': 'Rated Movie', 'image': 'movie_image.jpg'}
trakt_importer = TraktImporter('testuser', self.user, 'new')
trakt_importer.process_ratings()
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 1)
movie_obj = trakt_importer.bulk_media[MediaTypes.MOVIE.value][0]
self.assertEqual(movie_obj.score, 8)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_trakt.py:124*

### test_process_comments

**Category**: workflow  
**Description**: Workflow: Test processing paginated comments from Trakt.  
**Expected**: self.assertEqual(movie_obj.notes, 'Great movie!')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)

'Test processing paginated comments from Trakt.'
first_page = [{'type': 'movie', 'movie': {'title': 'Commented Movie', 'ids': {'tmdb': 123}}, 'comment': {'comment': 'Great movie!', 'updated_at': '2023-01-01T00:00:00.000Z'}}]
second_page = []
mock_make_request.side_effect = [first_page, second_page]
mock_get_metadata.return_value = {'title': 'Commented Movie', 'image': 'movie_image.jpg'}
trakt_importer = TraktImporter('testuser', self.user, 'new')
trakt_importer.process_comments()
calls = mock_make_request.call_args_list
self.assertEqual(len(calls), 2)
self.assertIn('?page=1&limit=1000', calls[0].args[0])
self.assertIn('?page=2&limit=1000', calls[1].args[0])
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 1)
movie_obj = trakt_importer.bulk_media[MediaTypes.MOVIE.value][0]
self.assertEqual(movie_obj.notes, 'Great movie!')
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_trakt.py:148*

### test_public_import_full_flow

**Category**: workflow  
**Description**: Workflow: Test full import flow with public username (no OAuth).  
**Expected**: self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)

'Test full import flow with public username (no OAuth).'
mock_get_paginated.side_effect = [[{'type': 'movie', 'movie': {'title': 'Public Movie', 'ids': {'tmdb': 999}}, 'watched_at': '2023-01-01T00:00:00.000Z'}], []]
mock_make_request.return_value = []
mock_get_metadata.return_value = {'title': 'Public Movie', 'image': 'movie.jpg'}
imported_counts, _ = importer(None, self.user, 'new', 'public_user')
self.assertEqual(imported_counts[MediaTypes.MOVIE.value], 1)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_trakt.py:186*

### test_oauth_import_full_flow

**Category**: workflow  
**Description**: Workflow: Test full import flow with OAuth token.  
**Expected**: self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)

'Test full import flow with OAuth token.'
mock_get_paginated.side_effect = [[{'type': 'movie', 'movie': {'title': 'OAuth Movie', 'ids': {'tmdb': 888}}, 'watched_at': '2023-01-01T00:00:00.000Z'}], []]
mock_make_request.return_value = []
mock_get_metadata.return_value = {'title': 'OAuth Movie', 'image': 'movie.jpg'}
encrypted_token = helpers.encrypt('test_refresh_token')
imported_counts, _ = importer(encrypted_token, self.user, 'new', 'oauth_user')
self.assertEqual(imported_counts[MediaTypes.MOVIE.value], 1)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_trakt.py:219*

### test_get_access_token_uses_redirect_uri

**Category**: workflow  
**Description**: Workflow: Test refreshing Trakt tokens sends the configured redirect URI.  
**Expected**: self.assertEqual(params['redirect_uri'], 'https://yamtrack.example.com/import/trakt/private')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)

'Test refreshing Trakt tokens sends the configured redirect URI.'
mock_api_request.return_value = {'access_token': 'access-token', 'refresh_token': 'new-refresh-token'}
encrypted_token = helpers.encrypt('refresh-token')
access_token = get_access_token(encrypted_token, redirect_uri='https://yamtrack.example.com/import/trakt/private')
self.assertEqual(access_token, 'access-token')
params = mock_api_request.call_args.kwargs['params']
self.assertEqual(params['redirect_uri'], 'https://yamtrack.example.com/import/trakt/private')
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_trakt.py:279*

### test_process_watched_movie

**Category**: workflow  
**Description**: Workflow: Test processing a movie entry.  
**Expected**: self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 2)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_metadata

'Test processing a movie entry.'
movie_entry = {'type': 'movie', 'movie': {'title': 'Test Movie', 'ids': {'tmdb': 67890}}, 'watched_at': '2023-01-02T00:00:00.000Z'}
mock_get_metadata.return_value = {'title': 'Test Movie', 'image': 'movie_image.jpg'}
trakt_importer = TraktImporter('test', self.user, 'new')
trakt_importer.process_watched_movie(movie_entry)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 1)
self.assertEqual(len(trakt_importer.media_instances[MediaTypes.MOVIE.value]), 1)
movie_obj = trakt_importer.bulk_media[MediaTypes.MOVIE.value][0]
self.assertEqual(movie_obj.progress, 1)
trakt_importer.process_watched_movie(movie_entry)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.MOVIE.value]), 2)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_trakt.py:32*

### test_process_watched_episode

**Category**: workflow  
**Description**: Workflow: Test processing an episode entry.  
**Expected**: self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.EPISODE.value]), 2)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_metadata

'Test processing an episode entry.'
episode_entry = {'type': 'episode', 'episode': {'season': 1, 'number': 1, 'title': 'Pilot'}, 'show': {'title': 'Test Show', 'ids': {'tmdb': 12345}}, 'watched_at': '2023-01-01T00:00:00.000Z'}

def mock_metadata_side_effect(media_type, _, __, ___=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Test Show', 'image': 'tv_image.jpg', 'last_episode_season': 1, 'max_progress': 1}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Season 1', 'image': 'season_image.jpg', 'episodes': [{'episode_number': 1, 'still_path': '/still.jpg'}], 'max_progress': 1}
    return None
mock_get_metadata.side_effect = mock_metadata_side_effect
trakt_importer = TraktImporter('testuser', self.user, 'new')
trakt_importer.process_watched_episode(episode_entry)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.TV.value]), 1)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.SEASON.value]), 1)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.EPISODE.value]), 1)
trakt_importer.process_watched_episode(episode_entry)
self.assertEqual(len(trakt_importer.bulk_media[MediaTypes.EPISODE.value]), 2)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_trakt.py:60*

### test_date_range_filtering

**Category**: workflow  
**Description**: Workflow: Test filtering with a specific date range.  
**Expected**: self.assertNotIn(self.movie6_item.id, movie_ids)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.episode2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=2)
self.movie1_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with start and end dates')
self.movie2_item = Item.objects.create(media_id='239', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only start date')
self.movie3_item = Item.objects.create(media_id='240', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only end date')
self.movie4_item = Item.objects.create(media_id='241', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with no dates')
self.movie5_item = Item.objects.create(media_id='242', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (before)')
self.movie6_item = Item.objects.create(media_id='243', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (after)')
self.movie7_item = Item.objects.create(media_id='244', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts before, ends in range)')
self.movie8_item = Item.objects.create(media_id='245', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts in range, ends after)')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value, score=8.0)
self.episode1 = Episode.objects.create(item=self.episode1_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC))
self.episode2 = Episode.objects.create(item=self.episode2_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie1 = Movie.objects.create(user=self.user, item=self.movie1_item, status=Status.COMPLETED.value, score=7.5, start_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC))
self.movie2 = Movie.objects.create(user=self.user, item=self.movie2_item, status=Status.IN_PROGRESS.value, score=8.0, start_date=datetime.datetime(2025, 2, 15, 0, 0, tzinfo=datetime.UTC), end_date=None)
self.movie3 = Movie.objects.create(user=self.user, item=self.movie3_item, status=Status.COMPLETED.value, score=6.5, start_date=None, end_date=datetime.datetime(2025, 2, 20, 0, 0, tzinfo=datetime.UTC))
self.movie4 = Movie.objects.create(user=self.user, item=self.movie4_item, status=Status.PLANNING.value, score=None, start_date=None, end_date=None)
self.movie5 = Movie.objects.create(user=self.user, item=self.movie5_item, status=Status.COMPLETED.value, score=9.0, start_date=datetime.datetime(2025, 1, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie6 = Movie.objects.create(user=self.user, item=self.movie6_item, status=Status.PLANNING.value, score=None, start_date=datetime.datetime(2025, 3, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 15, 0, 0, tzinfo=datetime.UTC))
self.movie7 = Movie.objects.create(user=self.user, item=self.movie7_item, status=Status.COMPLETED.value, score=7.0, start_date=datetime.datetime(2025, 1, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 5, 0, 0, tzinfo=datetime.UTC))
self.movie8 = Movie.objects.create(user=self.user, item=self.movie8_item, status=Status.COMPLETED.value, score=8.5, start_date=datetime.datetime(2025, 2, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 5, 0, 0, tzinfo=datetime.UTC))

'Test filtering with a specific date range.'
start_date = datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC)
end_date = datetime.datetime(2025, 2, 28, 0, 0, tzinfo=datetime.UTC)
user_media, media_count = statistics.get_user_media(self.user, start_date, end_date)
self.assertEqual(media_count[MediaTypes.TV.value], 0)
self.assertEqual(media_count[MediaTypes.SEASON.value], 0)
self.assertEqual(media_count[MediaTypes.MOVIE.value], 5)
self.assertEqual(media_count['total'], 5)
movie_ids = [m.item.id for m in user_media[MediaTypes.MOVIE.value]]
self.assertIn(self.movie1_item.id, movie_ids)
self.assertIn(self.movie2_item.id, movie_ids)
self.assertIn(self.movie3_item.id, movie_ids)
self.assertIn(self.movie7_item.id, movie_ids)
self.assertIn(self.movie8_item.id, movie_ids)
self.assertNotIn(self.movie4_item.id, movie_ids)
self.assertNotIn(self.movie5_item.id, movie_ids)
self.assertNotIn(self.movie6_item.id, movie_ids)
```

*Source: C:\yamtrack-fork\src\app\tests\test_statistics.py:231*

### test_both_dates_filtering

**Category**: workflow  
**Description**: Workflow: Test filtering for media with both start and end dates.  
**Expected**: self.assertNotIn(self.movie6_item.id, movie_ids)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.episode2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=2)
self.movie1_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with start and end dates')
self.movie2_item = Item.objects.create(media_id='239', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only start date')
self.movie3_item = Item.objects.create(media_id='240', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only end date')
self.movie4_item = Item.objects.create(media_id='241', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with no dates')
self.movie5_item = Item.objects.create(media_id='242', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (before)')
self.movie6_item = Item.objects.create(media_id='243', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (after)')
self.movie7_item = Item.objects.create(media_id='244', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts before, ends in range)')
self.movie8_item = Item.objects.create(media_id='245', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts in range, ends after)')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value, score=8.0)
self.episode1 = Episode.objects.create(item=self.episode1_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC))
self.episode2 = Episode.objects.create(item=self.episode2_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie1 = Movie.objects.create(user=self.user, item=self.movie1_item, status=Status.COMPLETED.value, score=7.5, start_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC))
self.movie2 = Movie.objects.create(user=self.user, item=self.movie2_item, status=Status.IN_PROGRESS.value, score=8.0, start_date=datetime.datetime(2025, 2, 15, 0, 0, tzinfo=datetime.UTC), end_date=None)
self.movie3 = Movie.objects.create(user=self.user, item=self.movie3_item, status=Status.COMPLETED.value, score=6.5, start_date=None, end_date=datetime.datetime(2025, 2, 20, 0, 0, tzinfo=datetime.UTC))
self.movie4 = Movie.objects.create(user=self.user, item=self.movie4_item, status=Status.PLANNING.value, score=None, start_date=None, end_date=None)
self.movie5 = Movie.objects.create(user=self.user, item=self.movie5_item, status=Status.COMPLETED.value, score=9.0, start_date=datetime.datetime(2025, 1, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie6 = Movie.objects.create(user=self.user, item=self.movie6_item, status=Status.PLANNING.value, score=None, start_date=datetime.datetime(2025, 3, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 15, 0, 0, tzinfo=datetime.UTC))
self.movie7 = Movie.objects.create(user=self.user, item=self.movie7_item, status=Status.COMPLETED.value, score=7.0, start_date=datetime.datetime(2025, 1, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 5, 0, 0, tzinfo=datetime.UTC))
self.movie8 = Movie.objects.create(user=self.user, item=self.movie8_item, status=Status.COMPLETED.value, score=8.5, start_date=datetime.datetime(2025, 2, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 5, 0, 0, tzinfo=datetime.UTC))

'Test filtering for media with both start and end dates.'
start_date = datetime.datetime(2025, 2, 5, 0, 0, tzinfo=datetime.UTC)
end_date = datetime.datetime(2025, 2, 15, 0, 0, tzinfo=datetime.UTC)
user_media, _ = statistics.get_user_media(self.user, start_date, end_date)
movie_ids = [m.item.id for m in user_media[MediaTypes.MOVIE.value]]
self.assertIn(self.movie1_item.id, movie_ids)
self.assertIn(self.movie7_item.id, movie_ids)
self.assertNotIn(self.movie5_item.id, movie_ids)
self.assertNotIn(self.movie6_item.id, movie_ids)
```

*Source: C:\yamtrack-fork\src\app\tests\test_statistics.py:272*

### test_start_date_only_filtering

**Category**: workflow  
**Description**: Workflow: Test filtering for media with only start date.  
**Expected**: self.assertNotIn(outside_item.id, movie_ids)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.episode2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=2)
self.movie1_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with start and end dates')
self.movie2_item = Item.objects.create(media_id='239', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only start date')
self.movie3_item = Item.objects.create(media_id='240', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only end date')
self.movie4_item = Item.objects.create(media_id='241', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with no dates')
self.movie5_item = Item.objects.create(media_id='242', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (before)')
self.movie6_item = Item.objects.create(media_id='243', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (after)')
self.movie7_item = Item.objects.create(media_id='244', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts before, ends in range)')
self.movie8_item = Item.objects.create(media_id='245', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts in range, ends after)')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value, score=8.0)
self.episode1 = Episode.objects.create(item=self.episode1_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC))
self.episode2 = Episode.objects.create(item=self.episode2_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie1 = Movie.objects.create(user=self.user, item=self.movie1_item, status=Status.COMPLETED.value, score=7.5, start_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC))
self.movie2 = Movie.objects.create(user=self.user, item=self.movie2_item, status=Status.IN_PROGRESS.value, score=8.0, start_date=datetime.datetime(2025, 2, 15, 0, 0, tzinfo=datetime.UTC), end_date=None)
self.movie3 = Movie.objects.create(user=self.user, item=self.movie3_item, status=Status.COMPLETED.value, score=6.5, start_date=None, end_date=datetime.datetime(2025, 2, 20, 0, 0, tzinfo=datetime.UTC))
self.movie4 = Movie.objects.create(user=self.user, item=self.movie4_item, status=Status.PLANNING.value, score=None, start_date=None, end_date=None)
self.movie5 = Movie.objects.create(user=self.user, item=self.movie5_item, status=Status.COMPLETED.value, score=9.0, start_date=datetime.datetime(2025, 1, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie6 = Movie.objects.create(user=self.user, item=self.movie6_item, status=Status.PLANNING.value, score=None, start_date=datetime.datetime(2025, 3, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 15, 0, 0, tzinfo=datetime.UTC))
self.movie7 = Movie.objects.create(user=self.user, item=self.movie7_item, status=Status.COMPLETED.value, score=7.0, start_date=datetime.datetime(2025, 1, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 5, 0, 0, tzinfo=datetime.UTC))
self.movie8 = Movie.objects.create(user=self.user, item=self.movie8_item, status=Status.COMPLETED.value, score=8.5, start_date=datetime.datetime(2025, 2, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 5, 0, 0, tzinfo=datetime.UTC))

'Test filtering for media with only start date.'
start_date = datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC)
end_date = datetime.datetime(2025, 2, 20, 0, 0, tzinfo=datetime.UTC)
user_media, _ = statistics.get_user_media(self.user, start_date, end_date)
movie_ids = [m.item.id for m in user_media[MediaTypes.MOVIE.value]]
self.assertIn(self.movie2_item.id, movie_ids)
outside_item = Item.objects.create(media_id='246', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with start date outside range')
Movie.objects.create(user=self.user, item=outside_item, status=Status.IN_PROGRESS.value, start_date=datetime.datetime(2025, 3, 1, 0, 0, tzinfo=datetime.UTC), end_date=None)
user_media, _ = statistics.get_user_media(self.user, start_date, end_date)
movie_ids = [m.item.id for m in user_media[MediaTypes.MOVIE.value]]
self.assertNotIn(outside_item.id, movie_ids)
```

*Source: C:\yamtrack-fork\src\app\tests\test_statistics.py:294*

### test_end_date_only_filtering

**Category**: workflow  
**Description**: Workflow: Test filtering for media with only end date.  
**Expected**: self.assertNotIn(outside_item.id, movie_ids)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.episode2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=2)
self.movie1_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with start and end dates')
self.movie2_item = Item.objects.create(media_id='239', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only start date')
self.movie3_item = Item.objects.create(media_id='240', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only end date')
self.movie4_item = Item.objects.create(media_id='241', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with no dates')
self.movie5_item = Item.objects.create(media_id='242', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (before)')
self.movie6_item = Item.objects.create(media_id='243', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (after)')
self.movie7_item = Item.objects.create(media_id='244', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts before, ends in range)')
self.movie8_item = Item.objects.create(media_id='245', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts in range, ends after)')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value, score=8.0)
self.episode1 = Episode.objects.create(item=self.episode1_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC))
self.episode2 = Episode.objects.create(item=self.episode2_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie1 = Movie.objects.create(user=self.user, item=self.movie1_item, status=Status.COMPLETED.value, score=7.5, start_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC))
self.movie2 = Movie.objects.create(user=self.user, item=self.movie2_item, status=Status.IN_PROGRESS.value, score=8.0, start_date=datetime.datetime(2025, 2, 15, 0, 0, tzinfo=datetime.UTC), end_date=None)
self.movie3 = Movie.objects.create(user=self.user, item=self.movie3_item, status=Status.COMPLETED.value, score=6.5, start_date=None, end_date=datetime.datetime(2025, 2, 20, 0, 0, tzinfo=datetime.UTC))
self.movie4 = Movie.objects.create(user=self.user, item=self.movie4_item, status=Status.PLANNING.value, score=None, start_date=None, end_date=None)
self.movie5 = Movie.objects.create(user=self.user, item=self.movie5_item, status=Status.COMPLETED.value, score=9.0, start_date=datetime.datetime(2025, 1, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie6 = Movie.objects.create(user=self.user, item=self.movie6_item, status=Status.PLANNING.value, score=None, start_date=datetime.datetime(2025, 3, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 15, 0, 0, tzinfo=datetime.UTC))
self.movie7 = Movie.objects.create(user=self.user, item=self.movie7_item, status=Status.COMPLETED.value, score=7.0, start_date=datetime.datetime(2025, 1, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 5, 0, 0, tzinfo=datetime.UTC))
self.movie8 = Movie.objects.create(user=self.user, item=self.movie8_item, status=Status.COMPLETED.value, score=8.5, start_date=datetime.datetime(2025, 2, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 5, 0, 0, tzinfo=datetime.UTC))

'Test filtering for media with only end date.'
start_date = datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC)
end_date = datetime.datetime(2025, 2, 20, 0, 0, tzinfo=datetime.UTC)
user_media, _ = statistics.get_user_media(self.user, start_date, end_date)
movie_ids = [m.item.id for m in user_media[MediaTypes.MOVIE.value]]
self.assertIn(self.movie3_item.id, movie_ids)
outside_item = Item.objects.create(media_id='247', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with end date outside range')
Movie.objects.create(user=self.user, item=outside_item, status=Status.COMPLETED.value, start_date=None, end_date=datetime.datetime(2025, 3, 1, 0, 0, tzinfo=datetime.UTC))
user_media, _ = statistics.get_user_media(self.user, start_date, end_date)
movie_ids = [m.item.id for m in user_media[MediaTypes.MOVIE.value]]
self.assertNotIn(outside_item.id, movie_ids)
```

*Source: C:\yamtrack-fork\src\app\tests\test_statistics.py:338*

### test_no_dates_filtering

**Category**: workflow  
**Description**: Workflow: Test that media with no dates is excluded from date-filtered results.  
**Expected**: self.assertIn(self.movie4_item.id, movie_ids)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.episode2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=2)
self.movie1_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with start and end dates')
self.movie2_item = Item.objects.create(media_id='239', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only start date')
self.movie3_item = Item.objects.create(media_id='240', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only end date')
self.movie4_item = Item.objects.create(media_id='241', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with no dates')
self.movie5_item = Item.objects.create(media_id='242', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (before)')
self.movie6_item = Item.objects.create(media_id='243', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (after)')
self.movie7_item = Item.objects.create(media_id='244', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts before, ends in range)')
self.movie8_item = Item.objects.create(media_id='245', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts in range, ends after)')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value, score=8.0)
self.episode1 = Episode.objects.create(item=self.episode1_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC))
self.episode2 = Episode.objects.create(item=self.episode2_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie1 = Movie.objects.create(user=self.user, item=self.movie1_item, status=Status.COMPLETED.value, score=7.5, start_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC))
self.movie2 = Movie.objects.create(user=self.user, item=self.movie2_item, status=Status.IN_PROGRESS.value, score=8.0, start_date=datetime.datetime(2025, 2, 15, 0, 0, tzinfo=datetime.UTC), end_date=None)
self.movie3 = Movie.objects.create(user=self.user, item=self.movie3_item, status=Status.COMPLETED.value, score=6.5, start_date=None, end_date=datetime.datetime(2025, 2, 20, 0, 0, tzinfo=datetime.UTC))
self.movie4 = Movie.objects.create(user=self.user, item=self.movie4_item, status=Status.PLANNING.value, score=None, start_date=None, end_date=None)
self.movie5 = Movie.objects.create(user=self.user, item=self.movie5_item, status=Status.COMPLETED.value, score=9.0, start_date=datetime.datetime(2025, 1, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie6 = Movie.objects.create(user=self.user, item=self.movie6_item, status=Status.PLANNING.value, score=None, start_date=datetime.datetime(2025, 3, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 15, 0, 0, tzinfo=datetime.UTC))
self.movie7 = Movie.objects.create(user=self.user, item=self.movie7_item, status=Status.COMPLETED.value, score=7.0, start_date=datetime.datetime(2025, 1, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 5, 0, 0, tzinfo=datetime.UTC))
self.movie8 = Movie.objects.create(user=self.user, item=self.movie8_item, status=Status.COMPLETED.value, score=8.5, start_date=datetime.datetime(2025, 2, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 5, 0, 0, tzinfo=datetime.UTC))

'Test that media with no dates is excluded from date-filtered results.'
start_date = datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC)
end_date = datetime.datetime(2025, 2, 28, 0, 0, tzinfo=datetime.UTC)
user_media, _ = statistics.get_user_media(self.user, start_date, end_date)
movie_ids = [m.item.id for m in user_media[MediaTypes.MOVIE.value]]
self.assertNotIn(self.movie4_item.id, movie_ids)
user_media, _ = statistics.get_user_media(self.user, None, None)
movie_ids = [m.item.id for m in user_media[MediaTypes.MOVIE.value]]
self.assertIn(self.movie4_item.id, movie_ids)
```

*Source: C:\yamtrack-fork\src\app\tests\test_statistics.py:382*

### test_overlapping_ranges

**Category**: workflow  
**Description**: Workflow: Test media with date ranges that overlap with the filter range.  
**Expected**: self.assertIn(spanning_item.id, movie_ids)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.episode2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=2)
self.movie1_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with start and end dates')
self.movie2_item = Item.objects.create(media_id='239', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only start date')
self.movie3_item = Item.objects.create(media_id='240', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with only end date')
self.movie4_item = Item.objects.create(media_id='241', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie with no dates')
self.movie5_item = Item.objects.create(media_id='242', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (before)')
self.movie6_item = Item.objects.create(media_id='243', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie outside date range (after)')
self.movie7_item = Item.objects.create(media_id='244', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts before, ends in range)')
self.movie8_item = Item.objects.create(media_id='245', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie partially in range (starts in range, ends after)')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value, score=8.0)
self.episode1 = Episode.objects.create(item=self.episode1_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC))
self.episode2 = Episode.objects.create(item=self.episode2_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie1 = Movie.objects.create(user=self.user, item=self.movie1_item, status=Status.COMPLETED.value, score=7.5, start_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 10, 0, 0, tzinfo=datetime.UTC))
self.movie2 = Movie.objects.create(user=self.user, item=self.movie2_item, status=Status.IN_PROGRESS.value, score=8.0, start_date=datetime.datetime(2025, 2, 15, 0, 0, tzinfo=datetime.UTC), end_date=None)
self.movie3 = Movie.objects.create(user=self.user, item=self.movie3_item, status=Status.COMPLETED.value, score=6.5, start_date=None, end_date=datetime.datetime(2025, 2, 20, 0, 0, tzinfo=datetime.UTC))
self.movie4 = Movie.objects.create(user=self.user, item=self.movie4_item, status=Status.PLANNING.value, score=None, start_date=None, end_date=None)
self.movie5 = Movie.objects.create(user=self.user, item=self.movie5_item, status=Status.COMPLETED.value, score=9.0, start_date=datetime.datetime(2025, 1, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie6 = Movie.objects.create(user=self.user, item=self.movie6_item, status=Status.PLANNING.value, score=None, start_date=datetime.datetime(2025, 3, 10, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 15, 0, 0, tzinfo=datetime.UTC))
self.movie7 = Movie.objects.create(user=self.user, item=self.movie7_item, status=Status.COMPLETED.value, score=7.0, start_date=datetime.datetime(2025, 1, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 5, 0, 0, tzinfo=datetime.UTC))
self.movie8 = Movie.objects.create(user=self.user, item=self.movie8_item, status=Status.COMPLETED.value, score=8.5, start_date=datetime.datetime(2025, 2, 25, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 5, 0, 0, tzinfo=datetime.UTC))

'Test media with date ranges that overlap with the filter range.'
start_date = datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC)
end_date = datetime.datetime(2025, 2, 28, 0, 0, tzinfo=datetime.UTC)
user_media, _ = statistics.get_user_media(self.user, start_date, end_date)
movie_ids = [m.item.id for m in user_media[MediaTypes.MOVIE.value]]
self.assertIn(self.movie7_item.id, movie_ids)
self.assertIn(self.movie8_item.id, movie_ids)
spanning_item = Item.objects.create(media_id='248', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Movie that spans the entire range')
Movie.objects.create(user=self.user, item=spanning_item, status=Status.COMPLETED.value, start_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 15, 0, 0, tzinfo=datetime.UTC))
user_media, _ = statistics.get_user_media(self.user, start_date, end_date)
movie_ids = [m.item.id for m in user_media[MediaTypes.MOVIE.value]]
self.assertIn(spanning_item.id, movie_ids)
```

*Source: C:\yamtrack-fork\src\app\tests\test_statistics.py:408*

### test_get_status_distribution

**Category**: workflow  
**Description**: Workflow: Test the get_status_distribution function.  
**Expected**: self.assertEqual(planning_dataset['total'], 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.episode2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=2)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.anime_item = Item.objects.create(media_id='437', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value, score=8.0)
self.episode1 = Episode.objects.create(item=self.episode1_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC))
self.episode2 = Episode.objects.create(item=self.episode2_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value, score=7.5, start_date=datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC))
self.anime = Anime.objects.create(user=self.user, item=self.anime_item, status=Status.COMPLETED.value, score=None, start_date=datetime.datetime(2025, 3, 1, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 31, 0, 0, tzinfo=datetime.UTC))

'Test the get_status_distribution function.'
user_media = {MediaTypes.TV.value: TV.objects.filter(user=self.user), MediaTypes.MOVIE.value: Movie.objects.filter(user=self.user), MediaTypes.ANIME.value: Anime.objects.filter(user=self.user)}
status_distribution = statistics.get_status_distribution(user_media)
self.assertIn('labels', status_distribution)
self.assertIn('datasets', status_distribution)
self.assertIn('total_completed', status_distribution)
self.assertEqual(len(status_distribution['labels']), 3)
self.assertEqual(len(status_distribution['datasets']), len(Status.values))
self.assertEqual(status_distribution['total_completed'], 1)
completed_dataset = next((d for d in status_distribution['datasets'] if d['label'] == Status.COMPLETED.value))
in_progress_dataset = next((d for d in status_distribution['datasets'] if d['label'] == Status.IN_PROGRESS.value))
planning_dataset = next((d for d in status_distribution['datasets'] if d['label'] == Status.PLANNING.value))
self.assertEqual(completed_dataset['total'], 1)
self.assertEqual(in_progress_dataset['total'], 1)
self.assertEqual(planning_dataset['total'], 1)
```

*Source: C:\yamtrack-fork\src\app\tests\test_statistics.py:573*

### test_get_extended_statistics

**Category**: workflow  
**Description**: Workflow: Test extended report-style statistics.  
**Expected**: self.assertEqual(year_2025['completed'], 3)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.episode2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=2)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.anime_item = Item.objects.create(media_id='437', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value, score=8.0)
self.episode1 = Episode.objects.create(item=self.episode1_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC))
self.episode2 = Episode.objects.create(item=self.episode2_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value, score=7.5, start_date=datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC))
self.anime = Anime.objects.create(user=self.user, item=self.anime_item, status=Status.COMPLETED.value, score=None, start_date=datetime.datetime(2025, 3, 1, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 31, 0, 0, tzinfo=datetime.UTC))

'Test extended report-style statistics.'
TV.objects.filter(user=self.user).update(score=8.5)
user_media = {MediaTypes.TV.value: TV.objects.filter(user=self.user), MediaTypes.MOVIE.value: Movie.objects.filter(user=self.user), MediaTypes.ANIME.value: Anime.objects.filter(user=self.user)}
report = statistics.get_extended_statistics(user_media)
self.assertEqual(report['summary']['total_items'], 3)
self.assertEqual(report['summary']['completed_items'], 1)
self.assertEqual(report['summary']['completion_percentage'], 33)
self.assertEqual(report['summary']['scored_items'], 2)
self.assertEqual(report['summary']['unrated_items'], 1)
self.assertEqual(report['summary']['median_score'], 8.0)
self.assertEqual(report['summary']['highest_rated'].score, 8.5)
self.assertEqual(report['summary']['lowest_rated'].score, 7.5)
movie_row = next((row for row in report['media_type_rows'] if row['media_type'] == MediaTypes.MOVIE.value))
self.assertEqual(movie_row['total'], 1)
self.assertEqual(movie_row['scored'], 1)
self.assertEqual(movie_row['average_score'], 7.5)
self.assertEqual(movie_row['best_media'], self.movie)
score_8 = next((bucket for bucket in report['score_buckets'] if bucket['score'] == 8))
self.assertEqual(score_8['count'], 1)
self.assertEqual(score_8['percentage'], 50)
favorites = next((band for band in report['rating_bands'] if band['label'] == 'Favorites'))
self.assertEqual(favorites['count'], 1)
self.assertEqual(favorites['percentage'], 50)
tmdb_row = next((row for row in report['source_rows'] if row['source'] == Sources.TMDB.label))
self.assertEqual(tmdb_row['count'], 2)
self.assertEqual(tmdb_row['scored'], 2)
self.assertEqual(tmdb_row['average_score'], 8.0)
year_2025 = next((row for row in report['year_rows'] if row['year'] == 2025))
self.assertEqual(year_2025['started'], 3)
self.assertEqual(year_2025['completed'], 3)
```

*Source: C:\yamtrack-fork\src\app\tests\test_statistics.py:718*

### test_get_activity_data

**Category**: workflow  
**Description**: Workflow: Test the get_activity_data function.  
**Expected**: self.assertIsInstance(months, list)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.episode2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=2)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.anime_item = Item.objects.create(media_id='437', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value, score=8.0)
self.episode1 = Episode.objects.create(item=self.episode1_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC))
self.episode2 = Episode.objects.create(item=self.episode2_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value, score=7.5, start_date=datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC))
self.anime = Anime.objects.create(user=self.user, item=self.anime_item, status=Status.COMPLETED.value, score=None, start_date=datetime.datetime(2025, 3, 1, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 31, 0, 0, tzinfo=datetime.UTC))

'Test the get_activity_data function.'
start_date = datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC)
end_date = datetime.datetime(2025, 3, 31, 0, 0, tzinfo=datetime.UTC)
mock_get_filtered_data.return_value = [{'date': datetime.date(2025, 1, 1), 'count': 2}, {'date': datetime.date(2025, 1, 2), 'count': 1}, {'date': datetime.date(2025, 1, 3), 'count': 3}, {'date': datetime.date(2025, 1, 4), 'count': 0}, {'date': datetime.date(2025, 1, 5), 'count': 5}, {'date': datetime.date(2025, 1, 6), 'count': 2}, {'date': datetime.date(2025, 1, 7), 'count': 1}, {'date': datetime.date(2025, 1, 8), 'count': 4}, {'date': datetime.date(2025, 1, 9), 'count': 0}, {'date': datetime.date(2025, 1, 10), 'count': 0}, {'date': datetime.date(2025, 3, 31), 'count': 3}]
result = statistics.get_activity_data(self.user, start_date, end_date)
self.assertIn('calendar_weeks', result)
self.assertIn('months', result)
self.assertIn('stats', result)
stats = result['stats']
self.assertIn('most_active_day', stats)
self.assertIn('most_active_day_percentage', stats)
self.assertIn('current_streak', stats)
self.assertIn('longest_streak', stats)
calendar_weeks = result['calendar_weeks']
self.assertIsInstance(calendar_weeks, list)
first_week = calendar_weeks[0]
self.assertEqual(len(first_week), 7)
months = result['months']
self.assertIsInstance(months, list)
```

*Source: C:\yamtrack-fork\src\app\tests\test_statistics.py:825*

### test_calculate_day_of_week_stats

**Category**: workflow  
**Description**: Workflow: Test the calculate_day_of_week_stats function.  
**Expected**: self.assertEqual(percentage, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.episode2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=2)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.anime_item = Item.objects.create(media_id='437', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value, score=8.0)
self.episode1 = Episode.objects.create(item=self.episode1_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.UTC))
self.episode2 = Episode.objects.create(item=self.episode2_item, related_season=self.season, end_date=datetime.datetime(2025, 1, 15, 0, 0, tzinfo=datetime.UTC))
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value, score=7.5, start_date=datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 2, 1, 0, 0, tzinfo=datetime.UTC))
self.anime = Anime.objects.create(user=self.user, item=self.anime_item, status=Status.COMPLETED.value, score=None, start_date=datetime.datetime(2025, 3, 1, 0, 0, tzinfo=datetime.UTC), end_date=datetime.datetime(2025, 3, 31, 0, 0, tzinfo=datetime.UTC))

'Test the calculate_day_of_week_stats function.'
date_counts = {datetime.date(2025, 1, 1): 2, datetime.date(2025, 1, 2): 1, datetime.date(2025, 1, 3): 3, datetime.date(2025, 1, 4): 0, datetime.date(2025, 1, 5): 5, datetime.date(2025, 1, 6): 2, datetime.date(2025, 1, 7): 1, datetime.date(2025, 1, 8): 4, datetime.date(2025, 1, 9): 0, datetime.date(2025, 1, 10): 0, datetime.date(2025, 1, 12): 5, datetime.date(2025, 1, 19): 3}
start_date = datetime.date(2025, 1, 1)
most_active_day, percentage = statistics.calculate_day_of_week_stats(date_counts, start_date)
self.assertEqual(most_active_day, 'Sunday')
self.assertEqual(percentage, 33)
empty_counts = {}
most_active_day, percentage = statistics.calculate_day_of_week_stats(empty_counts, start_date)
self.assertIsNone(most_active_day)
self.assertEqual(percentage, 0)
```

*Source: C:\yamtrack-fork\src\app\tests\test_statistics.py:919*

### test_tv_episode_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles TV episode mark played event.  
**Expected**: self.assertIsNotNone(episode.end_date)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('jellyfin_webhook', kwargs={'token': 'test-token'})

'Test webhook handles TV episode mark played event.'
payload = {'Event': 'Stop', 'Item': {'Type': 'Episode', 'Name': 'The One Where Monica Gets a Roommate', 'ProviderIds': {'Tvdb': '303821', 'Imdb': 'tt0583459'}, 'SeriesName': 'Friends', 'ParentIndexNumber': 1, 'IndexNumber': 1, 'UserData': {'Played': True}}}
response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
self.assertEqual(response.status_code, 200)
tv_item = Item.objects.get(media_type=MediaTypes.TV.value, media_id='1668')
self.assertEqual(tv_item.title, 'Friends')
tv = TV.objects.get(item=tv_item, user=self.user)
self.assertEqual(tv.status, Status.IN_PROGRESS.value)
season = Season.objects.get(item__media_id='1668', item__season_number=1)
self.assertEqual(season.status, Status.IN_PROGRESS.value)
episode = Episode.objects.get(item__media_id='1668', item__season_number=1, item__episode_number=1)
self.assertIsNotNone(episode.end_date)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_jellyfin.py:28*

### test_extract_external_ids

**Category**: workflow  
**Description**: Workflow: Test extracting external IDs from provider payload.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('jellyfin_webhook', kwargs={'token': 'test-token'})

'Test extracting external IDs from provider payload.'
payload = {'Event': 'Stop', 'Item': {'Type': 'Movie', 'Name': 'The Matrix', 'ProductionYear': 1999, 'ProviderIds': {'Tmdb': '603', 'Tvdb': '169'}}}
expected = {'tmdb_id': '603', 'imdb_id': None, 'tvdb_id': '169'}
result = JellyfinWebhookProcessor()._extract_external_ids(payload)
if result != expected:
    msg = f'Expected {expected}, got {result}'
    raise AssertionError(msg)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_jellyfin.py:268*

### test_extract_external_ids_empty

**Category**: workflow  
**Description**: Workflow: Test handling empty provider payload.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('jellyfin_webhook', kwargs={'token': 'test-token'})

'Test handling empty provider payload.'
payload = {'Event': 'Stop', 'Item': {'Type': 'Movie', 'Name': 'The Matrix', 'ProductionYear': 1999, 'ProviderIds': {}}}
expected = {'tmdb_id': None, 'imdb_id': None, 'tvdb_id': None}
result = JellyfinWebhookProcessor()._extract_external_ids(payload)
if result != expected:
    msg = f'Expected {expected}, got {result}'
    raise AssertionError(msg)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_jellyfin.py:294*

### test_extract_external_ids_missing

**Category**: workflow  
**Description**: Workflow: Test handling missing ProviderIds.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('jellyfin_webhook', kwargs={'token': 'test-token'})

'Test handling missing ProviderIds.'
payload = {'Event': 'Stop', 'Item': {'Type': 'Movie', 'Name': 'The Matrix', 'ProductionYear': 1999}}
expected = {'tmdb_id': None, 'imdb_id': None, 'tvdb_id': None}
result = JellyfinWebhookProcessor()._extract_external_ids(payload)
if result != expected:
    msg = f'Expected {expected}, got {result}'
    raise AssertionError(msg)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_jellyfin.py:317*

### test_process_tv_uses_tvdb_absolute_order_for_cross_season_match

**Category**: workflow  
**Description**: Workflow: Test webhook anime matching uses TVDB absolute numbering across seasons.  
**Expected**: mock_handle_anime.assert_called_once_with(269, 22, payload, self.user)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'testuser', 'token': 'test-token'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.url = reverse('jellyfin_webhook', kwargs={'token': 'test-token'})

'Test webhook anime matching uses TVDB absolute numbering across seasons.'
mock_fetch_mapping_data.return_value = {'2369': {'tvdb_id': 74796, 'tvdb_season': -1, 'tvdb_epoffset': 0, 'mal_id': 269}}
mock_find_tv_media_id.return_value = ('1668', 2, 2)
mock_tvdb_episode.return_value = {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22}
payload = {'Event': 'Stop', 'Item': {'Type': 'Episode', 'Name': 'Test Episode', 'ProviderIds': {'Tvdb': '12345'}, 'UserData': {'Played': True}, 'SeriesName': 'Bleach', 'ParentIndexNumber': 2, 'IndexNumber': 2}}
JellyfinWebhookProcessor().process_payload(payload, self.user)
mock_tvdb_episode.assert_called_once_with(12345)
mock_handle_anime.assert_called_once_with(269, 22, payload, self.user)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_jellyfin.py:466*

### test_tv_episode_mark_played

**Category**: workflow  
**Description**: Workflow: Test webhook handles TV episode mark played event.  
**Expected**: self.assertIsNotNone(episode.end_date)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test webhook handles TV episode mark played event.'
payload = {'Event': 'Stop', 'Item': {'Type': 'Episode', 'Name': 'The One Where Monica Gets a Roommate', 'ProviderIds': {'Tvdb': '303821', 'Imdb': 'tt0583459'}, 'SeriesName': 'Friends', 'ParentIndexNumber': 1, 'IndexNumber': 1, 'UserData': {'Played': True}}}
response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
self.assertEqual(response.status_code, 200)
tv_item = Item.objects.get(media_type=MediaTypes.TV.value, media_id='1668')
self.assertEqual(tv_item.title, 'Friends')
tv = TV.objects.get(item=tv_item, user=self.user)
self.assertEqual(tv.status, Status.IN_PROGRESS.value)
season = Season.objects.get(item__media_id='1668', item__season_number=1)
self.assertEqual(season.status, Status.IN_PROGRESS.value)
episode = Episode.objects.get(item__media_id='1668', item__season_number=1, item__episode_number=1)
self.assertIsNotNone(episode.end_date)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_jellyfin.py:28*

### test_extract_external_ids

**Category**: workflow  
**Description**: Workflow: Test extracting external IDs from provider payload.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test extracting external IDs from provider payload.'
payload = {'Event': 'Stop', 'Item': {'Type': 'Movie', 'Name': 'The Matrix', 'ProductionYear': 1999, 'ProviderIds': {'Tmdb': '603', 'Tvdb': '169'}}}
expected = {'tmdb_id': '603', 'imdb_id': None, 'tvdb_id': '169'}
result = JellyfinWebhookProcessor()._extract_external_ids(payload)
if result != expected:
    msg = f'Expected {expected}, got {result}'
    raise AssertionError(msg)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_jellyfin.py:268*

### test_extract_external_ids_empty

**Category**: workflow  
**Description**: Workflow: Test handling empty provider payload.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test handling empty provider payload.'
payload = {'Event': 'Stop', 'Item': {'Type': 'Movie', 'Name': 'The Matrix', 'ProductionYear': 1999, 'ProviderIds': {}}}
expected = {'tmdb_id': None, 'imdb_id': None, 'tvdb_id': None}
result = JellyfinWebhookProcessor()._extract_external_ids(payload)
if result != expected:
    msg = f'Expected {expected}, got {result}'
    raise AssertionError(msg)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_jellyfin.py:294*

### test_extract_external_ids_missing

**Category**: workflow  
**Description**: Workflow: Test handling missing ProviderIds.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test handling missing ProviderIds.'
payload = {'Event': 'Stop', 'Item': {'Type': 'Movie', 'Name': 'The Matrix', 'ProductionYear': 1999}}
expected = {'tmdb_id': None, 'imdb_id': None, 'tvdb_id': None}
result = JellyfinWebhookProcessor()._extract_external_ids(payload)
if result != expected:
    msg = f'Expected {expected}, got {result}'
    raise AssertionError(msg)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_jellyfin.py:317*

### test_process_tv_uses_tvdb_absolute_order_for_cross_season_match

**Category**: workflow  
**Description**: Workflow: Test webhook anime matching uses TVDB absolute numbering across seasons.  
**Expected**: mock_handle_anime.assert_called_once_with(269, 22, payload, self.user)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_fetch_mapping_data, mock_find_tv_media_id, mock_tvdb_episode, mock_handle_anime

'Test webhook anime matching uses TVDB absolute numbering across seasons.'
mock_fetch_mapping_data.return_value = {'2369': {'tvdb_id': 74796, 'tvdb_season': -1, 'tvdb_epoffset': 0, 'mal_id': 269}}
mock_find_tv_media_id.return_value = ('1668', 2, 2)
mock_tvdb_episode.return_value = {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22}
payload = {'Event': 'Stop', 'Item': {'Type': 'Episode', 'Name': 'Test Episode', 'ProviderIds': {'Tvdb': '12345'}, 'UserData': {'Played': True}, 'SeriesName': 'Bleach', 'ParentIndexNumber': 2, 'IndexNumber': 2}}
JellyfinWebhookProcessor().process_payload(payload, self.user)
mock_tvdb_episode.assert_called_once_with(12345)
mock_handle_anime.assert_called_once_with(269, 22, payload, self.user)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_webhooks_jellyfin.py:466*

### test_end_to_end_notification

**Category**: workflow  
**Description**: Workflow: Test the entire notification flow.  
**Expected**: mock_send_notifications.assert_called_once()  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

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

'Test the entire notification flow.'
mock_send_notifications.return_value = {'event_count': 5, 'event_ids': [self.anime_event.id, self.manga_event.id, self.season1_event.id, self.season2_event.id, self.season3_event.id]}
send_releases()
self.anime_event.refresh_from_db()
self.manga_event.refresh_from_db()
self.season1_event.refresh_from_db()
self.season2_event.refresh_from_db()
self.season3_event.refresh_from_db()
self.assertTrue(self.anime_event.notification_sent)
self.assertTrue(self.manga_event.notification_sent)
self.assertTrue(self.season1_event.notification_sent)
self.assertTrue(self.season2_event.notification_sent)
self.assertTrue(self.season3_event.notification_sent)
mock_send_notifications.assert_called_once()
```

*Source: C:\yamtrack-fork\src\events\tests\test_notification.py:198*

### test_exclude_then_notify

**Category**: workflow  
**Description**: Workflow: Test excluding an item then verifying it's not in notifications.  
**Expected**: self.assertTrue(self.manga_event.notification_sent)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

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

*Source: C:\yamtrack-fork\src\events\tests\test_notification.py:232*

### test_get_all_user_tracking_data

**Category**: workflow  
**Description**: Workflow: Test the get_all_user_tracking_data function.  
**Expected**: self.assertIn(season1_key, tracking_data)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

'Test the get_all_user_tracking_data function.'
users_with_notifications = get_user_model().objects.filter(~models.Q(notification_urls='')).prefetch_related('notification_excluded_items')
target_events = {(self.anime_event.item.id, self.anime_event.content_number): self.anime_event, (self.manga_event.item.id, self.manga_event.content_number): self.manga_event, (self.season1_event.item.id, self.season1_event.content_number): self.season1_event, (self.season2_event.item.id, self.season2_event.content_number): self.season2_event}
user_exclusions = {}
for user in users_with_notifications:
    user_exclusions[user.id] = set(user.notification_excluded_items.values_list('id', flat=True))
tracking_data = get_all_user_tracking_data(users_with_notifications, target_events, user_exclusions)
self.assertIsInstance(tracking_data, dict)
anime_key = (self.user1.id, self.anime_item.id)
self.assertIn(anime_key, tracking_data)
manga_key = (self.user1.id, self.manga_item.id)
self.assertIn(manga_key, tracking_data)
season1_key = (self.user1.id, self.season1_item.id)
self.assertIn(season1_key, tracking_data)
```

*Source: C:\yamtrack-fork\src\events\tests\test_notification.py:377*

### test_get_tv_tracking_data

**Category**: workflow  
**Description**: Workflow: Test the get_tv_tracking_data function.  
**Expected**: self.assertFalse(tracking_data[user2_season3_key])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

*Source: C:\yamtrack-fork\src\events\tests\test_notification.py:437*

### test_get_tv_tracking_data_empty_season_items

**Category**: workflow  
**Description**: Workflow: Test get_tv_tracking_data with empty season items.  
**Expected**: self.assertEqual(tracking_data, {})  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

'Test get_tv_tracking_data with empty season items.'
users = [self.user1, self.user2]
season_items = []
user_exclusions = {self.user1.id: set(), self.user2.id: set()}
tracking_data = get_tv_tracking_data(users, season_items, user_exclusions)
self.assertEqual(tracking_data, {})
```

*Source: C:\yamtrack-fork\src\events\tests\test_notification.py:533*

### test_get_user_releases

**Category**: workflow  
**Description**: Workflow: Test the get_user_releases function.  
**Expected**: self.assertFalse(season2_event_found)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

'Test the get_user_releases function.'
users_with_notifications = get_user_model().objects.filter(~models.Q(notification_urls='')).prefetch_related('notification_excluded_items')
target_events = {(self.anime_event.item.id, self.anime_event.content_number): self.anime_event, (self.manga_event.item.id, self.manga_event.content_number): self.manga_event, (self.season1_event.item.id, self.season1_event.content_number): self.season1_event, (self.season2_event.item.id, self.season2_event.content_number): self.season2_event}
user_releases = get_user_releases(users_with_notifications, target_events)
self.assertIn(self.user1.id, user_releases)
self.assertIn(self.user2.id, user_releases)
user1_events = user_releases[self.user1.id]
anime_event_found = any((event.id == self.anime_event.id for event in user1_events))
manga_event_found = any((event.id == self.manga_event.id for event in user1_events))
season1_event_found = any((event.id == self.season1_event.id for event in user1_events))
self.assertTrue(anime_event_found)
self.assertFalse(manga_event_found)
self.assertTrue(season1_event_found)
user2_events = user_releases[self.user2.id]
anime_event_found = any((event.id == self.anime_event.id for event in user2_events))
manga_event_found = any((event.id == self.manga_event.id for event in user2_events))
season1_event_found = any((event.id == self.season1_event.id for event in user2_events))
season2_event_found = any((event.id == self.season2_event.id for event in user2_events))
self.assertTrue(anime_event_found)
self.assertFalse(manga_event_found)
self.assertTrue(season1_event_found)
self.assertFalse(season2_event_found)
```

*Source: C:\yamtrack-fork\src\events\tests\test_notification.py:548*

### test_is_user_tracking_item

**Category**: workflow  
**Description**: Workflow: Test the is_user_tracking_item function.  
**Expected**: self.assertTrue(result)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

*Source: C:\yamtrack-fork\src\events\tests\test_notification.py:623*

### test_format_notification

**Category**: workflow  
**Description**: Workflow: Test the format_notification function.  
**Expected**: self.assertNotIn('Test Manga', notification_text)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

'Test the format_notification function.'
releases = [self.anime_event, self.manga_event, self.season1_event]
notification_text = format_notification(releases)
self.assertIn('ANIME', notification_text)
self.assertIn('MANGA', notification_text)
self.assertIn('TV Shows', notification_text)
self.assertIn('Test Anime', notification_text)
self.assertIn('Test Manga', notification_text)
self.assertIn('Test TV Show', notification_text)
self.assertIn('E5', notification_text)
self.assertIn('#10', notification_text)
releases = [self.anime_event]
notification_text = format_notification(releases)
self.assertIn('ANIME', notification_text)
self.assertIn('Test Anime', notification_text)
self.assertIn('E5', notification_text)
self.assertNotIn('MANGA', notification_text)
self.assertNotIn('Test Manga', notification_text)
```

*Source: C:\yamtrack-fork\src\events\tests\test_notification.py:708*

### test_user_exclusion

**Category**: workflow  
**Description**: Workflow: Test that user exclusions are respected.  
**Expected**: self.assertFalse(manga_event_found)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

'Test that user exclusions are respected.'
users_with_notifications = get_user_model().objects.filter(~models.Q(notification_urls='')).prefetch_related('notification_excluded_items')
target_events = {(self.anime_event.item.id, self.anime_event.content_number): self.anime_event, (self.manga_event.item.id, self.manga_event.content_number): self.manga_event}
user_releases = get_user_releases(users_with_notifications, target_events)
user1_events = user_releases[self.user1.id]
manga_event_found = any((event.id == self.manga_event.id for event in user1_events))
self.assertFalse(manga_event_found)
```

*Source: C:\yamtrack-fork\src\events\tests\test_notification.py:750*

### test_release_notifications_disabled

**Category**: workflow  
**Description**: Workflow: Test that users with disabled release_notifications_enabled.  
**Expected**: self.assertIn(self.user2.id, user_ids)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

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

'Test that users with disabled release_notifications_enabled.'
mock_send_notifications.return_value = {'event_count': 5, 'event_ids': [self.anime_event.id, self.manga_event.id, self.season1_event.id, self.season2_event.id, self.season3_event.id]}
self.user1.release_notifications_enabled = False
self.user1.save()
send_releases()
mock_send_notifications.assert_called_once()
users = mock_send_notifications.call_args[1]['users']
user_ids = [user.id for user in users]
self.assertNotIn(self.user1.id, user_ids)
self.assertIn(self.user2.id, user_ids)
```

*Source: C:\yamtrack-fork\src\events\tests\test_notification.py:837*

### test_manual_id_generation

**Category**: workflow  
**Description**: Workflow: Test that unique manual IDs are generated.  
**Expected**: self.assertTrue(item2.media_id)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create a user and necessary parent items.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='manual_tv_1', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Test Manual TV', image='http://example.com/tv.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.IN_PROGRESS.value)
self.season_item = Item.objects.create(media_id='manual_tv_1', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Test Manual TV', season_number=1, image='http://example.com/season.jpg')
self.season = Season.objects.create(item=self.season_item, user=self.user, status=Status.IN_PROGRESS.value)

'Test that unique manual IDs are generated.'
form1 = ManualItemForm(data={'media_type': MediaTypes.ANIME.value, 'title': 'Test Anime 1'}, user=self.user)
self.assertTrue(form1.is_valid())
item1 = form1.save()
form2 = ManualItemForm(data={'media_type': MediaTypes.ANIME.value, 'title': 'Test Anime 2'}, user=self.user)
self.assertTrue(form2.is_valid())
item2 = form2.save()
self.assertNotEqual(item1.media_id, item2.media_id)
self.assertTrue(item1.media_id)
self.assertTrue(item2.media_id)
```

*Source: C:\yamtrack-fork\src\app\tests\test_forms.py:461*

### test_manual_id_generation

**Category**: workflow  
**Description**: Workflow: Test that unique manual IDs are generated.  
**Expected**: self.assertTrue(item2.media_id)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test that unique manual IDs are generated.'
form1 = ManualItemForm(data={'media_type': MediaTypes.ANIME.value, 'title': 'Test Anime 1'}, user=self.user)
self.assertTrue(form1.is_valid())
item1 = form1.save()
form2 = ManualItemForm(data={'media_type': MediaTypes.ANIME.value, 'title': 'Test Anime 2'}, user=self.user)
self.assertTrue(form2.is_valid())
item2 = form2.save()
self.assertNotEqual(item1.media_id, item2.media_id)
self.assertTrue(item1.media_id)
self.assertTrue(item2.media_id)
```

*Source: C:\yamtrack-fork\src\app\tests\test_forms.py:461*

### test_apply_prefetch_related

**Category**: workflow  
**Description**: Workflow: Test the _apply_prefetch_related method.  
**Expected**: self.assertEqual(len(prefetch_lookups), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data for MediaManager tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_numbers = season_numbers or [1]
        return {f'season/{season_number}': {'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)], 'image': 'http://example.com/image.jpg'} for season_number in season_numbers}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)]}
    max_progress_by_type = {MediaTypes.MOVIE.value: 1, MediaTypes.ANIME.value: 24, MediaTypes.MANGA.value: 300, MediaTypes.GAME.value: 240, MediaTypes.BOOK.value: 500, MediaTypes.BOARDGAME.value: 1}
    return {'max_progress': max_progress_by_type.get(media_type)}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
for media_type in MediaTypes.values:
    setattr(self.user, f'{media_type.lower()}_enabled', True)
self.user.save()
self.movie_item = Item.objects.create(media_id='550', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Fight Club', image='http://example.com/fightclub.jpg')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/bebop.jpg')
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.book_item = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='1984', image='http://example.com/1984.jpg')
self.manga_item = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='http://example.com/berserk.jpg')
self.movie = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, score=9)
self.anime = Anime.objects.create(item=self.anime_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=13)
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, score=7, progress=120)
self.book = Book.objects.create(item=self.book_item, user=self.user, status=Status.PLANNING.value, score=0)
self.manga = Manga.objects.create(item=self.manga_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=100)
self.season1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, status=Status.IN_PROGRESS.value, score=8)
self.tv = TV.objects.get(user=self.user)
for i in range(1, 5):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Friends S1E{i}', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    watched_episodes = 3
    if i <= watched_episodes:
        Episode.objects.create(item=episode_item, related_season=self.season1, end_date=datetime(2023, 6, i, 0, 0, tzinfo=UTC))
for i in range(4, 7):
    Event.objects.create(item=self.anime_item, content_number=i + 13, datetime=timezone.now() + timedelta(days=i), notification_sent=False)

'Test the _apply_prefetch_related method.'
manager = MediaManager()
queryset = TV.objects.filter(user=self.user.id)
prefetched_queryset = manager._apply_prefetch_related(queryset, MediaTypes.TV.value)
self.assertTrue(hasattr(prefetched_queryset, '_prefetch_related_lookups'))
prefetch_lookups = prefetched_queryset._prefetch_related_lookups
self.assertEqual(len(prefetch_lookups), 3)
queryset = Season.objects.filter(user=self.user.id)
prefetched_queryset = manager._apply_prefetch_related(queryset, MediaTypes.SEASON.value)
self.assertTrue(hasattr(prefetched_queryset, '_prefetch_related_lookups'))
prefetch_lookups = prefetched_queryset._prefetch_related_lookups
self.assertEqual(len(prefetch_lookups), 2)
queryset = Movie.objects.filter(user=self.user.id)
prefetched_queryset = manager._apply_prefetch_related(queryset, MediaTypes.MOVIE.value)
self.assertTrue(hasattr(prefetched_queryset, '_prefetch_related_lookups'))
prefetch_lookups = prefetched_queryset._prefetch_related_lookups
self.assertEqual(len(prefetch_lookups), 1)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media_manager.py:294*

### test_get_media_list_with_prefetch_related

**Category**: workflow  
**Description**: Workflow: Test the get_media_list method with prefetch_related for TV and Season.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data for MediaManager tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_numbers = season_numbers or [1]
        return {f'season/{season_number}': {'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)], 'image': 'http://example.com/image.jpg'} for season_number in season_numbers}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)]}
    max_progress_by_type = {MediaTypes.MOVIE.value: 1, MediaTypes.ANIME.value: 24, MediaTypes.MANGA.value: 300, MediaTypes.GAME.value: 240, MediaTypes.BOOK.value: 500, MediaTypes.BOARDGAME.value: 1}
    return {'max_progress': max_progress_by_type.get(media_type)}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
for media_type in MediaTypes.values:
    setattr(self.user, f'{media_type.lower()}_enabled', True)
self.user.save()
self.movie_item = Item.objects.create(media_id='550', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Fight Club', image='http://example.com/fightclub.jpg')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/bebop.jpg')
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.book_item = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='1984', image='http://example.com/1984.jpg')
self.manga_item = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='http://example.com/berserk.jpg')
self.movie = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, score=9)
self.anime = Anime.objects.create(item=self.anime_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=13)
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, score=7, progress=120)
self.book = Book.objects.create(item=self.book_item, user=self.user, status=Status.PLANNING.value, score=0)
self.manga = Manga.objects.create(item=self.manga_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=100)
self.season1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, status=Status.IN_PROGRESS.value, score=8)
self.tv = TV.objects.get(user=self.user)
for i in range(1, 5):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Friends S1E{i}', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    watched_episodes = 3
    if i <= watched_episodes:
        Episode.objects.create(item=episode_item, related_season=self.season1, end_date=datetime(2023, 6, i, 0, 0, tzinfo=UTC))
for i in range(4, 7):
    Event.objects.create(item=self.anime_item, content_number=i + 13, datetime=timezone.now() + timedelta(days=i), notification_sent=False)

'Test the get_media_list method with prefetch_related for TV and Season.'
manager = MediaManager()
tv_list = manager.get_media_list(user=self.user, media_type=MediaTypes.TV.value, status_filter=MediaStatusChoices.ALL, sort_filter='score')
tv_list = list(tv_list)
for tv in tv_list:
    seasons = list(tv.seasons.all())
    for season in seasons:
        list(season.episodes.all())
with self.assertNumQueries(0):
    for tv in tv_list:
        seasons = list(tv.seasons.all())
        for season in seasons:
            list(season.episodes.all())
season_list = manager.get_media_list(user=self.user, media_type=MediaTypes.SEASON.value, status_filter=MediaStatusChoices.ALL, sort_filter='score')
season_list = list(season_list)
for season in season_list:
    list(season.episodes.all())
with self.assertNumQueries(0):
    for season in season_list:
        list(season.episodes.all())
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media_manager.py:328*

### test_get_media_list_sort_by_regular_field

**Category**: workflow  
**Description**: Workflow: Test the get_media_list method with sorting by regular field.  
**Expected**: self.assertEqual(media_list.last(), anime2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data for MediaManager tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_numbers = season_numbers or [1]
        return {f'season/{season_number}': {'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)], 'image': 'http://example.com/image.jpg'} for season_number in season_numbers}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)]}
    max_progress_by_type = {MediaTypes.MOVIE.value: 1, MediaTypes.ANIME.value: 24, MediaTypes.MANGA.value: 300, MediaTypes.GAME.value: 240, MediaTypes.BOOK.value: 500, MediaTypes.BOARDGAME.value: 1}
    return {'max_progress': max_progress_by_type.get(media_type)}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
for media_type in MediaTypes.values:
    setattr(self.user, f'{media_type.lower()}_enabled', True)
self.user.save()
self.movie_item = Item.objects.create(media_id='550', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Fight Club', image='http://example.com/fightclub.jpg')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/bebop.jpg')
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.book_item = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='1984', image='http://example.com/1984.jpg')
self.manga_item = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='http://example.com/berserk.jpg')
self.movie = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, score=9)
self.anime = Anime.objects.create(item=self.anime_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=13)
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, score=7, progress=120)
self.book = Book.objects.create(item=self.book_item, user=self.user, status=Status.PLANNING.value, score=0)
self.manga = Manga.objects.create(item=self.manga_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=100)
self.season1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, status=Status.IN_PROGRESS.value, score=8)
self.tv = TV.objects.get(user=self.user)
for i in range(1, 5):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Friends S1E{i}', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    watched_episodes = 3
    if i <= watched_episodes:
        Episode.objects.create(item=episode_item, related_season=self.season1, end_date=datetime(2023, 6, i, 0, 0, tzinfo=UTC))
for i in range(4, 7):
    Event.objects.create(item=self.anime_item, content_number=i + 13, datetime=timezone.now() + timedelta(days=i), notification_sent=False)

'Test the get_media_list method with sorting by regular field.'
manager = MediaManager()
anime_item2 = Item.objects.create(media_id='5', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Naruto', image='http://example.com/naruto.jpg')
anime2 = Anime.objects.create(item=anime_item2, user=self.user, status=Status.IN_PROGRESS.value, score=6)
media_list = manager.get_media_list(user=self.user, media_type=MediaTypes.ANIME.value, status_filter=MediaStatusChoices.ALL, sort_filter='score')
self.assertEqual(media_list.first(), self.anime)
self.assertEqual(media_list.last(), anime2)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media_manager.py:503*

### test_get_media_types_to_process

**Category**: workflow  
**Description**: Workflow: Test the _get_media_types_to_process method.  
**Expected**: self.assertIn(MediaTypes.MOVIE.value, media_types)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data for MediaManager tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_numbers = season_numbers or [1]
        return {f'season/{season_number}': {'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)], 'image': 'http://example.com/image.jpg'} for season_number in season_numbers}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)]}
    max_progress_by_type = {MediaTypes.MOVIE.value: 1, MediaTypes.ANIME.value: 24, MediaTypes.MANGA.value: 300, MediaTypes.GAME.value: 240, MediaTypes.BOOK.value: 500, MediaTypes.BOARDGAME.value: 1}
    return {'max_progress': max_progress_by_type.get(media_type)}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
for media_type in MediaTypes.values:
    setattr(self.user, f'{media_type.lower()}_enabled', True)
self.user.save()
self.movie_item = Item.objects.create(media_id='550', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Fight Club', image='http://example.com/fightclub.jpg')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/bebop.jpg')
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.book_item = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='1984', image='http://example.com/1984.jpg')
self.manga_item = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='http://example.com/berserk.jpg')
self.movie = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, score=9)
self.anime = Anime.objects.create(item=self.anime_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=13)
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, score=7, progress=120)
self.book = Book.objects.create(item=self.book_item, user=self.user, status=Status.PLANNING.value, score=0)
self.manga = Manga.objects.create(item=self.manga_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=100)
self.season1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, status=Status.IN_PROGRESS.value, score=8)
self.tv = TV.objects.get(user=self.user)
for i in range(1, 5):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Friends S1E{i}', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    watched_episodes = 3
    if i <= watched_episodes:
        Episode.objects.create(item=episode_item, related_season=self.season1, end_date=datetime(2023, 6, i, 0, 0, tzinfo=UTC))
for i in range(4, 7):
    Event.objects.create(item=self.anime_item, content_number=i + 13, datetime=timezone.now() + timedelta(days=i), notification_sent=False)

'Test the _get_media_types_to_process method.'
manager = MediaManager()
media_types = manager._get_media_types_to_process(self.user, MediaTypes.ANIME.value)
self.assertEqual(media_types, [MediaTypes.ANIME.value])
media_types = manager._get_media_types_to_process(self.user, None)
self.assertNotIn(MediaTypes.TV.value, media_types)
self.assertIn(MediaTypes.ANIME.value, media_types)
self.assertIn(MediaTypes.MOVIE.value, media_types)
self.assertIn(MediaTypes.GAME.value, media_types)
self.assertIn(MediaTypes.BOOK.value, media_types)
self.assertIn(MediaTypes.MANGA.value, media_types)
self.user.anime_enabled = False
self.user.manga_enabled = False
self.user.save()
media_types = manager._get_media_types_to_process(self.user, None)
self.assertNotIn(MediaTypes.ANIME.value, media_types)
self.assertNotIn(MediaTypes.MANGA.value, media_types)
self.assertIn(MediaTypes.MOVIE.value, media_types)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media_manager.py:532*

### test_get_media_types_to_process_includes_tv_for_in_progress

**Category**: workflow  
**Description**: Workflow: Test in-progress home processing includes TV shows.  
**Expected**: self.assertIn(MediaTypes.TV.value, media_types)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data for MediaManager tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_numbers = season_numbers or [1]
        return {f'season/{season_number}': {'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)], 'image': 'http://example.com/image.jpg'} for season_number in season_numbers}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)]}
    max_progress_by_type = {MediaTypes.MOVIE.value: 1, MediaTypes.ANIME.value: 24, MediaTypes.MANGA.value: 300, MediaTypes.GAME.value: 240, MediaTypes.BOOK.value: 500, MediaTypes.BOARDGAME.value: 1}
    return {'max_progress': max_progress_by_type.get(media_type)}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
for media_type in MediaTypes.values:
    setattr(self.user, f'{media_type.lower()}_enabled', True)
self.user.save()
self.movie_item = Item.objects.create(media_id='550', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Fight Club', image='http://example.com/fightclub.jpg')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/bebop.jpg')
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.book_item = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='1984', image='http://example.com/1984.jpg')
self.manga_item = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='http://example.com/berserk.jpg')
self.movie = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, score=9)
self.anime = Anime.objects.create(item=self.anime_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=13)
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, score=7, progress=120)
self.book = Book.objects.create(item=self.book_item, user=self.user, status=Status.PLANNING.value, score=0)
self.manga = Manga.objects.create(item=self.manga_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=100)
self.season1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, status=Status.IN_PROGRESS.value, score=8)
self.tv = TV.objects.get(user=self.user)
for i in range(1, 5):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Friends S1E{i}', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    watched_episodes = 3
    if i <= watched_episodes:
        Episode.objects.create(item=episode_item, related_season=self.season1, end_date=datetime(2023, 6, i, 0, 0, tzinfo=UTC))
for i in range(4, 7):
    Event.objects.create(item=self.anime_item, content_number=i + 13, datetime=timezone.now() + timedelta(days=i), notification_sent=False)

'Test in-progress home processing includes TV shows.'
manager = MediaManager()
media_types = manager._get_media_types_to_process(self.user, None, Status.IN_PROGRESS.value)
self.assertIn(MediaTypes.TV.value, media_types)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media_manager.py:561*

### test_get_home_status_groups_media_and_annotates_home_fields

**Category**: workflow  
**Description**: Workflow: Test get_home_status groups media and annotates max_progress/events.  
**Expected**: self.assertIsNone(movie.next_event)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data for MediaManager tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_numbers = season_numbers or [1]
        return {f'season/{season_number}': {'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)], 'image': 'http://example.com/image.jpg'} for season_number in season_numbers}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)]}
    max_progress_by_type = {MediaTypes.MOVIE.value: 1, MediaTypes.ANIME.value: 24, MediaTypes.MANGA.value: 300, MediaTypes.GAME.value: 240, MediaTypes.BOOK.value: 500, MediaTypes.BOARDGAME.value: 1}
    return {'max_progress': max_progress_by_type.get(media_type)}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
for media_type in MediaTypes.values:
    setattr(self.user, f'{media_type.lower()}_enabled', True)
self.user.save()
self.movie_item = Item.objects.create(media_id='550', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Fight Club', image='http://example.com/fightclub.jpg')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/bebop.jpg')
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.book_item = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='1984', image='http://example.com/1984.jpg')
self.manga_item = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='http://example.com/berserk.jpg')
self.movie = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, score=9)
self.anime = Anime.objects.create(item=self.anime_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=13)
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, score=7, progress=120)
self.book = Book.objects.create(item=self.book_item, user=self.user, status=Status.PLANNING.value, score=0)
self.manga = Manga.objects.create(item=self.manga_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=100)
self.season1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, status=Status.IN_PROGRESS.value, score=8)
self.tv = TV.objects.get(user=self.user)
for i in range(1, 5):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Friends S1E{i}', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    watched_episodes = 3
    if i <= watched_episodes:
        Episode.objects.create(item=episode_item, related_season=self.season1, end_date=datetime(2023, 6, i, 0, 0, tzinfo=UTC))
for i in range(4, 7):
    Event.objects.create(item=self.anime_item, content_number=i + 13, datetime=timezone.now() + timedelta(days=i), notification_sent=False)

'Test get_home_status groups media and annotates max_progress/events.'
manager = MediaManager()
movie_item = Item.objects.create(media_id='551', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Before Sunrise', image='http://example.com/before-sunrise.jpg')
Movie.objects.create(item=movie_item, user=self.user, status=Status.IN_PROGRESS.value)
Event.objects.create(item=self.anime_item, content_number=14, datetime=timezone.now() - timedelta(days=1), notification_sent=True)
home_status = manager.get_home_status(user=self.user, status=Status.IN_PROGRESS.value, sort_by=HomeSortChoices.UPCOMING, items_limit=14)
self.assertNotIn(MediaTypes.TV.value, home_status)
self.assertCountEqual(home_status.keys(), [MediaTypes.SEASON.value, MediaTypes.MOVIE.value, MediaTypes.ANIME.value, MediaTypes.MANGA.value, MediaTypes.GAME.value])
self.assertEqual(home_status[MediaTypes.ANIME.value]['total'], 1)
anime = home_status[MediaTypes.ANIME.value]['items'][0]
self.assertEqual(anime.max_progress, 14)
self.assertIsNotNone(anime.next_event)
self.assertEqual(anime.next_event.content_number, 17)
movie = home_status[MediaTypes.MOVIE.value]['items'][0]
self.assertEqual(movie.max_progress, 1)
self.assertIsNone(movie.next_event)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media_manager.py:573*

### test_get_home_status_includes_tv_with_planning_season

**Category**: workflow  
**Description**: Workflow: Test in-progress TV shows with unwatched seasons appear on home.  
**Expected**: self.assertEqual(tv.next_event.item, season2_item)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data for MediaManager tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_numbers = season_numbers or [1]
        return {f'season/{season_number}': {'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)], 'image': 'http://example.com/image.jpg'} for season_number in season_numbers}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)]}
    max_progress_by_type = {MediaTypes.MOVIE.value: 1, MediaTypes.ANIME.value: 24, MediaTypes.MANGA.value: 300, MediaTypes.GAME.value: 240, MediaTypes.BOOK.value: 500, MediaTypes.BOARDGAME.value: 1}
    return {'max_progress': max_progress_by_type.get(media_type)}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
for media_type in MediaTypes.values:
    setattr(self.user, f'{media_type.lower()}_enabled', True)
self.user.save()
self.movie_item = Item.objects.create(media_id='550', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Fight Club', image='http://example.com/fightclub.jpg')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/bebop.jpg')
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.book_item = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='1984', image='http://example.com/1984.jpg')
self.manga_item = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='http://example.com/berserk.jpg')
self.movie = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, score=9)
self.anime = Anime.objects.create(item=self.anime_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=13)
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, score=7, progress=120)
self.book = Book.objects.create(item=self.book_item, user=self.user, status=Status.PLANNING.value, score=0)
self.manga = Manga.objects.create(item=self.manga_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=100)
self.season1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, status=Status.IN_PROGRESS.value, score=8)
self.tv = TV.objects.get(user=self.user)
for i in range(1, 5):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Friends S1E{i}', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    watched_episodes = 3
    if i <= watched_episodes:
        Episode.objects.create(item=episode_item, related_season=self.season1, end_date=datetime(2023, 6, i, 0, 0, tzinfo=UTC))
for i in range(4, 7):
    Event.objects.create(item=self.anime_item, content_number=i + 13, datetime=timezone.now() + timedelta(days=i), notification_sent=False)

'Test in-progress TV shows with unwatched seasons appear on home.'
manager = MediaManager()
season2_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/friends-s2.jpg', season_number=2)
Season.objects.create(item=season2_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
Event.objects.create(item=season2_item, content_number=1, datetime=timezone.now() + timedelta(days=7), notification_sent=False)
home_status = manager.get_home_status(user=self.user, status=Status.IN_PROGRESS.value, sort_by=HomeSortChoices.UPCOMING, items_limit=14)
self.assertIn(MediaTypes.TV.value, home_status)
tv = home_status[MediaTypes.TV.value]['items'][0]
self.assertEqual(tv, self.tv)
self.assertEqual(tv.next_event.item, season2_item)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media_manager.py:626*

### test_get_home_status_specific_media_type_returns_remaining_items

**Category**: workflow  
**Description**: Workflow: Test get_home_status returns the remaining items for load-more.  
**Expected**: self.assertEqual([media.item.title for media in load_more_page[MediaTypes.BOOK.value]['items']], ['Foundation', 'Hyperion'])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data for MediaManager tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_numbers = season_numbers or [1]
        return {f'season/{season_number}': {'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)], 'image': 'http://example.com/image.jpg'} for season_number in season_numbers}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)]}
    max_progress_by_type = {MediaTypes.MOVIE.value: 1, MediaTypes.ANIME.value: 24, MediaTypes.MANGA.value: 300, MediaTypes.GAME.value: 240, MediaTypes.BOOK.value: 500, MediaTypes.BOARDGAME.value: 1}
    return {'max_progress': max_progress_by_type.get(media_type)}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
for media_type in MediaTypes.values:
    setattr(self.user, f'{media_type.lower()}_enabled', True)
self.user.save()
self.movie_item = Item.objects.create(media_id='550', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Fight Club', image='http://example.com/fightclub.jpg')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/bebop.jpg')
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.book_item = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='1984', image='http://example.com/1984.jpg')
self.manga_item = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='http://example.com/berserk.jpg')
self.movie = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, score=9)
self.anime = Anime.objects.create(item=self.anime_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=13)
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, score=7, progress=120)
self.book = Book.objects.create(item=self.book_item, user=self.user, status=Status.PLANNING.value, score=0)
self.manga = Manga.objects.create(item=self.manga_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=100)
self.season1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, status=Status.IN_PROGRESS.value, score=8)
self.tv = TV.objects.get(user=self.user)
for i in range(1, 5):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Friends S1E{i}', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    watched_episodes = 3
    if i <= watched_episodes:
        Episode.objects.create(item=episode_item, related_season=self.season1, end_date=datetime(2023, 6, i, 0, 0, tzinfo=UTC))
for i in range(4, 7):
    Event.objects.create(item=self.anime_item, content_number=i + 13, datetime=timezone.now() + timedelta(days=i), notification_sent=False)

'Test get_home_status returns the remaining items for load-more.'
manager = MediaManager()
for media_id, title in (('OL1M', 'Dune'), ('OL2M', 'Foundation'), ('OL3M', 'Hyperion')):
    item = Item.objects.create(media_id=media_id, source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title=title, image='http://example.com/book.jpg')
    Book.objects.create(item=item, user=self.user, status=Status.PLANNING.value)
initial_page = manager.get_home_status(user=self.user, status=Status.PLANNING.value, sort_by=HomeSortChoices.TITLE, items_limit=2)
load_more_page = manager.get_home_status(user=self.user, status=Status.PLANNING.value, sort_by=HomeSortChoices.TITLE, items_limit=2, specific_media_type=MediaTypes.BOOK.value)
self.assertEqual(initial_page[MediaTypes.BOOK.value]['total'], 4)
self.assertEqual([media.item.title for media in initial_page[MediaTypes.BOOK.value]['items']], ['1984', 'Dune'])
self.assertEqual(list(load_more_page), [MediaTypes.BOOK.value])
self.assertEqual(load_more_page[MediaTypes.BOOK.value]['total'], 4)
self.assertEqual([media.item.title for media in load_more_page[MediaTypes.BOOK.value]['items']], ['Foundation', 'Hyperion'])
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media_manager.py:663*

### test_annotate_next_event

**Category**: workflow  
**Description**: Workflow: Test the _annotate_next_event method.  
**Expected**: self.assertIsNone(anime_list[0].next_event)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data for MediaManager tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_numbers = season_numbers or [1]
        return {f'season/{season_number}': {'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)], 'image': 'http://example.com/image.jpg'} for season_number in season_numbers}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)]}
    max_progress_by_type = {MediaTypes.MOVIE.value: 1, MediaTypes.ANIME.value: 24, MediaTypes.MANGA.value: 300, MediaTypes.GAME.value: 240, MediaTypes.BOOK.value: 500, MediaTypes.BOARDGAME.value: 1}
    return {'max_progress': max_progress_by_type.get(media_type)}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
for media_type in MediaTypes.values:
    setattr(self.user, f'{media_type.lower()}_enabled', True)
self.user.save()
self.movie_item = Item.objects.create(media_id='550', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Fight Club', image='http://example.com/fightclub.jpg')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/bebop.jpg')
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.book_item = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='1984', image='http://example.com/1984.jpg')
self.manga_item = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='http://example.com/berserk.jpg')
self.movie = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, score=9)
self.anime = Anime.objects.create(item=self.anime_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=13)
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, score=7, progress=120)
self.book = Book.objects.create(item=self.book_item, user=self.user, status=Status.PLANNING.value, score=0)
self.manga = Manga.objects.create(item=self.manga_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=100)
self.season1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, status=Status.IN_PROGRESS.value, score=8)
self.tv = TV.objects.get(user=self.user)
for i in range(1, 5):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Friends S1E{i}', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    watched_episodes = 3
    if i <= watched_episodes:
        Episode.objects.create(item=episode_item, related_season=self.season1, end_date=datetime(2023, 6, i, 0, 0, tzinfo=UTC))
for i in range(4, 7):
    Event.objects.create(item=self.anime_item, content_number=i + 13, datetime=timezone.now() + timedelta(days=i), notification_sent=False)

'Test the _annotate_next_event method.'
manager = MediaManager()
queryset = Anime.objects.filter(user=self.user.id).select_related('item')
anime_list = list(queryset)
for anime in anime_list:
    anime.item.prefetched_events = list(Event.objects.filter(item=anime.item))
manager._annotate_next_event(anime_list)
self.assertIsNotNone(anime_list[0].next_event)
self.assertEqual(anime_list[0].next_event.item, self.anime_item)
anime_item2 = Item.objects.create(media_id='5', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Naruto', image='http://example.com/naruto.jpg')
Anime.objects.create(item=anime_item2, user=self.user, status=Status.IN_PROGRESS.value, score=6)
Event.objects.create(item=anime_item2, content_number=1, datetime=timezone.now() - timedelta(days=1), notification_sent=True)
queryset = Anime.objects.filter(user=self.user.id, item=anime_item2).select_related('item')
anime_list = list(queryset)
for anime in anime_list:
    anime.item.prefetched_events = list(Event.objects.filter(item=anime.item))
manager._annotate_next_event(anime_list)
self.assertIsNone(anime_list[0].next_event)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media_manager.py:717*

### test_sort_home_media

**Category**: workflow  
**Description**: Workflow: Test the _sort_home_media method.  
**Expected**: self.assertEqual(sorted_list, [anime3, anime2, anime1])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data for MediaManager tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_numbers = season_numbers or [1]
        return {f'season/{season_number}': {'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)], 'image': 'http://example.com/image.jpg'} for season_number in season_numbers}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Friends', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'episodes': [{'episode_number': i, 'air_date': f'2023-06-{i:02d}', 'image': 'http://example.com/image.jpg'} for i in range(1, 11)]}
    max_progress_by_type = {MediaTypes.MOVIE.value: 1, MediaTypes.ANIME.value: 24, MediaTypes.MANGA.value: 300, MediaTypes.GAME.value: 240, MediaTypes.BOOK.value: 500, MediaTypes.BOARDGAME.value: 1}
    return {'max_progress': max_progress_by_type.get(media_type)}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
for media_type in MediaTypes.values:
    setattr(self.user, f'{media_type.lower()}_enabled', True)
self.user.save()
self.movie_item = Item.objects.create(media_id='550', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Fight Club', image='http://example.com/fightclub.jpg')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/bebop.jpg')
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.book_item = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='1984', image='http://example.com/1984.jpg')
self.manga_item = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='http://example.com/berserk.jpg')
self.movie = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, score=9)
self.anime = Anime.objects.create(item=self.anime_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=13)
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, score=7, progress=120)
self.book = Book.objects.create(item=self.book_item, user=self.user, status=Status.PLANNING.value, score=0)
self.manga = Manga.objects.create(item=self.manga_item, user=self.user, status=Status.IN_PROGRESS.value, score=10, progress=100)
self.season1_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, status=Status.IN_PROGRESS.value, score=8)
self.tv = TV.objects.get(user=self.user)
for i in range(1, 5):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Friends S1E{i}', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    watched_episodes = 3
    if i <= watched_episodes:
        Episode.objects.create(item=episode_item, related_season=self.season1, end_date=datetime(2023, 6, i, 0, 0, tzinfo=UTC))
for i in range(4, 7):
    Event.objects.create(item=self.anime_item, content_number=i + 13, datetime=timezone.now() + timedelta(days=i), notification_sent=False)

'Test the _sort_home_media method.'
manager = MediaManager()
anime_list = []
anime1 = self.anime
anime1.max_progress = 20
anime1.progress = 13
anime1.next_event = Event.objects.filter(item=self.anime_item).first()
anime_list.append(anime1)
anime_item2 = Item.objects.create(media_id='5', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Naruto', image='http://example.com/naruto.jpg')
anime2 = Anime.objects.create(item=anime_item2, user=self.user, status=Status.IN_PROGRESS.value, score=6, progress=5)
anime2.max_progress = 100
anime2.next_event = None
anime_list.append(anime2)
anime_item3 = Item.objects.create(media_id='6', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Attack on Titan', image='http://example.com/aot.jpg')
anime3 = Anime.objects.create(item=anime_item3, user=self.user, status=Status.IN_PROGRESS.value, score=9, progress=30)
anime3.max_progress = 50
anime3.next_event = Event.objects.create(item=anime_item3, content_number=31, datetime=timezone.now() + timedelta(days=10), notification_sent=False)
anime_list.append(anime3)
sorted_list = manager._sort_home_media(anime_list, HomeSortChoices.UPCOMING)
self.assertEqual(sorted_list, [anime1, anime3, anime2])
sorted_list = manager._sort_home_media(anime_list, HomeSortChoices.TITLE)
self.assertEqual(sorted_list, sorted(anime_list, key=lambda x: x.item.title.lower()))
sorted_list = manager._sort_home_media(anime_list, HomeSortChoices.COMPLETION)
self.assertEqual(sorted_list, [anime1, anime3, anime2])
sorted_list = manager._sort_home_media(anime_list, HomeSortChoices.EPISODES_LEFT)
self.assertEqual(sorted_list, [anime1, anime3, anime2])
sorted_list = manager._sort_home_media(anime_list, sort_by=HomeSortChoices.RECENT)
self.assertEqual(sorted_list, [anime3, anime2, anime1])
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media_manager.py:771*

### test_type_label_with_secondary_types

**Category**: workflow  
**Description**: Workflow: test type label with secondary types  
**Expected**: self.assertIn('Compilation', result['results'][0]['type'])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
cache.clear()

rg = _mock_release_group(mb_id='compilation-unique-id')
rg['secondary-types'] = ['Compilation']
mock_get.return_value = {'release-group-count': 1, 'release-groups': [rg]}
result = search_music('Beatles secondary types unique query xyz')
self.assertIn('Compilation', result['results'][0]['type'])
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_musicbrainz.py:175*

### test_returns_required_fields

**Category**: workflow  
**Description**: Workflow: test returns required fields  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
cache.clear()

mock_get.return_value = _mock_release_group()
mock_artist_albums.return_value = []
result = album('abc-123')
required = ['media_id', 'title', 'source', 'media_type', 'image', 'synopsis', 'genres', 'details', 'tracklist', 'artist_links', 'related']
for field in required:
    self.assertIn(field, result)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_musicbrainz.py:206*

### test_genres_from_genres_field

**Category**: workflow  
**Description**: Workflow: test genres from genres field  
**Expected**: self.assertIn('rock', result['genres'])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
cache.clear()

rg = _mock_release_group()
rg['genres'] = [{'name': 'rock'}, {'name': 'pop'}]
mock_get.return_value = rg
mock_artist_albums.return_value = []
result = album('abc-123')
self.assertIn('rock', result['genres'])
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_musicbrainz.py:234*

### test_genres_fallback_to_tags

**Category**: workflow  
**Description**: Workflow: test genres fallback to tags  
**Expected**: self.assertIn('jazz', result['genres'])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
cache.clear()

rg = _mock_release_group(mb_id='tags-fallback-unique-id')
rg['genres'] = []
rg['tags'] = [{'name': 'jazz'}, {'name': 'soul'}]
mock_get.return_value = rg
mock_artist_albums.return_value = []
result = album('tags-fallback-unique-id')
self.assertIn('jazz', result['genres'])
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_musicbrainz.py:244*

### test_recommendations_from_artist_albums

**Category**: workflow  
**Description**: Workflow: test recommendations from artist albums  
**Expected**: self.assertEqual(related_flat[0]['title'], 'Let It Be')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
cache.clear()

mock_get.return_value = _mock_release_group(mb_id='recs-unique-id', artist_id='beatles-uuid')
mock_artist_albums.return_value = [{'media_id': 'other-uuid', 'title': 'Let It Be', 'media_type': 'music'}]
result = album('recs-unique-id')
related_flat = []
for v in result['related'].values():
    related_flat.extend(v)
self.assertEqual(len(related_flat), 1)
self.assertEqual(related_flat[0]['title'], 'Let It Be')
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_musicbrainz.py:268*

### test_type_label_with_secondary_types

**Category**: workflow  
**Description**: Workflow: test type label with secondary types  
**Expected**: self.assertIn('Compilation', result['results'][0]['type'])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get

rg = _mock_release_group(mb_id='compilation-unique-id')
rg['secondary-types'] = ['Compilation']
mock_get.return_value = {'release-group-count': 1, 'release-groups': [rg]}
result = search_music('Beatles secondary types unique query xyz')
self.assertIn('Compilation', result['results'][0]['type'])
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_musicbrainz.py:175*

### test_returns_required_fields

**Category**: workflow  
**Description**: Workflow: test returns required fields  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get, mock_artist_albums

mock_get.return_value = _mock_release_group()
mock_artist_albums.return_value = []
result = album('abc-123')
required = ['media_id', 'title', 'source', 'media_type', 'image', 'synopsis', 'genres', 'details', 'tracklist', 'artist_links', 'related']
for field in required:
    self.assertIn(field, result)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_musicbrainz.py:206*

### test_genres_from_genres_field

**Category**: workflow  
**Description**: Workflow: test genres from genres field  
**Expected**: self.assertIn('rock', result['genres'])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get, mock_artist_albums

rg = _mock_release_group()
rg['genres'] = [{'name': 'rock'}, {'name': 'pop'}]
mock_get.return_value = rg
mock_artist_albums.return_value = []
result = album('abc-123')
self.assertIn('rock', result['genres'])
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_musicbrainz.py:234*

### test_genres_fallback_to_tags

**Category**: workflow  
**Description**: Workflow: test genres fallback to tags  
**Expected**: self.assertIn('jazz', result['genres'])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get, mock_artist_albums

rg = _mock_release_group(mb_id='tags-fallback-unique-id')
rg['genres'] = []
rg['tags'] = [{'name': 'jazz'}, {'name': 'soul'}]
mock_get.return_value = rg
mock_artist_albums.return_value = []
result = album('tags-fallback-unique-id')
self.assertIn('jazz', result['genres'])
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_musicbrainz.py:244*

### test_recommendations_from_artist_albums

**Category**: workflow  
**Description**: Workflow: test recommendations from artist albums  
**Expected**: self.assertEqual(related_flat[0]['title'], 'Let It Be')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get, mock_artist_albums

mock_get.return_value = _mock_release_group(mb_id='recs-unique-id', artist_id='beatles-uuid')
mock_artist_albums.return_value = [{'media_id': 'other-uuid', 'title': 'Let It Be', 'media_type': 'music'}]
result = album('recs-unique-id')
related_flat = []
for v in result['related'].values():
    related_flat.extend(v)
self.assertEqual(len(related_flat), 1)
self.assertEqual(related_flat[0]['title'], 'Let It Be')
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_musicbrainz.py:268*

### test_media_url

**Category**: workflow  
**Description**: Workflow: Test the media_url filter.  
**Expected**: self.assertEqual(season_dict_url, expected_season_url)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.tv_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.season_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.tv_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'title': 'Test TV Show'}
self.season_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.SEASON.value, 'title': 'Test TV Show', 'season_number': 1}
self.episode_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.EPISODE.value, 'title': 'Test TV Show', 'season_number': 1, 'episode_number': 1}

'Test the media_url filter.'
tv_url = app_tags.media_url(self.tv_item)
expected_tv_url = reverse('media_details', kwargs={'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'media_id': '1668', 'title': 'test-tv-show'})
self.assertEqual(tv_url, expected_tv_url)
tv_dict_url = app_tags.media_url(self.tv_dict)
self.assertEqual(tv_dict_url, expected_tv_url)
season_url = app_tags.media_url(self.season_item)
expected_season_url = reverse('season_details', kwargs={'source': Sources.TMDB.value, 'media_id': '1668', 'title': 'test-tv-show', 'season_number': 1})
self.assertEqual(season_url, expected_season_url)
season_dict_url = app_tags.media_url(self.season_dict)
self.assertEqual(season_dict_url, expected_season_url)
```

*Source: C:\yamtrack-fork\src\app\tests\test_templatetags.py:285*

### test_component_id

**Category**: workflow  
**Description**: Workflow: Test the component_id tag.  
**Expected**: self.assertEqual(episode_dict_id, 'card-episode-1668-1-1')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.tv_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.season_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.tv_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'title': 'Test TV Show'}
self.season_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.SEASON.value, 'title': 'Test TV Show', 'season_number': 1}
self.episode_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.EPISODE.value, 'title': 'Test TV Show', 'season_number': 1, 'episode_number': 1}

'Test the component_id tag.'
tv_id = app_tags.component_id('card', self.tv_item)
self.assertEqual(tv_id, 'card-tv-1668')
tv_dict_id = app_tags.component_id('card', self.tv_dict)
self.assertEqual(tv_dict_id, 'card-tv-1668')
season_id = app_tags.component_id('card', self.season_item)
self.assertEqual(season_id, 'card-season-1668-1')
season_dict_id = app_tags.component_id('card', self.season_dict)
self.assertEqual(season_dict_id, 'card-season-1668-1')
episode_id = app_tags.component_id('card', self.episode_item)
self.assertEqual(episode_id, 'card-episode-1668-1-1')
episode_dict_id = app_tags.component_id('card', self.episode_dict)
self.assertEqual(episode_dict_id, 'card-episode-1668-1-1')
```

*Source: C:\yamtrack-fork\src\app\tests\test_templatetags.py:321*

### test_media_view_url

**Category**: workflow  
**Description**: Workflow: Test the media_view_url tag.  
**Expected**: self.assertEqual(episode_dict_modal, expected_episode_modal)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.tv_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.season_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.tv_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'title': 'Test TV Show'}
self.season_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.SEASON.value, 'title': 'Test TV Show', 'season_number': 1}
self.episode_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.EPISODE.value, 'title': 'Test TV Show', 'season_number': 1, 'episode_number': 1}

'Test the media_view_url tag.'
tv_modal = app_tags.media_view_url('track_modal', self.tv_item)
expected_tv_modal = reverse('track_modal', kwargs={'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'media_id': '1668'})
self.assertEqual(tv_modal, expected_tv_modal)
tv_dict_modal = app_tags.media_view_url('track_modal', self.tv_dict)
self.assertEqual(tv_dict_modal, expected_tv_modal)
episode_modal = app_tags.media_view_url('history_modal', self.episode_item)
expected_episode_modal = reverse('history_modal', kwargs={'source': Sources.TMDB.value, 'media_type': MediaTypes.EPISODE.value, 'media_id': '1668', 'season_number': 1, 'episode_number': 1})
self.assertEqual(episode_modal, expected_episode_modal)
episode_dict_modal = app_tags.media_view_url('history_modal', self.episode_dict)
self.assertEqual(episode_dict_modal, expected_episode_modal)
```

*Source: C:\yamtrack-fork\src\app\tests\test_templatetags.py:347*

### test_media_url

**Category**: workflow  
**Description**: Workflow: Test the media_url filter.  
**Expected**: self.assertEqual(season_dict_url, expected_season_url)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the media_url filter.'
tv_url = app_tags.media_url(self.tv_item)
expected_tv_url = reverse('media_details', kwargs={'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'media_id': '1668', 'title': 'test-tv-show'})
self.assertEqual(tv_url, expected_tv_url)
tv_dict_url = app_tags.media_url(self.tv_dict)
self.assertEqual(tv_dict_url, expected_tv_url)
season_url = app_tags.media_url(self.season_item)
expected_season_url = reverse('season_details', kwargs={'source': Sources.TMDB.value, 'media_id': '1668', 'title': 'test-tv-show', 'season_number': 1})
self.assertEqual(season_url, expected_season_url)
season_dict_url = app_tags.media_url(self.season_dict)
self.assertEqual(season_dict_url, expected_season_url)
```

*Source: C:\yamtrack-fork\src\app\tests\test_templatetags.py:285*

### test_component_id

**Category**: workflow  
**Description**: Workflow: Test the component_id tag.  
**Expected**: self.assertEqual(episode_dict_id, 'card-episode-1668-1-1')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the component_id tag.'
tv_id = app_tags.component_id('card', self.tv_item)
self.assertEqual(tv_id, 'card-tv-1668')
tv_dict_id = app_tags.component_id('card', self.tv_dict)
self.assertEqual(tv_dict_id, 'card-tv-1668')
season_id = app_tags.component_id('card', self.season_item)
self.assertEqual(season_id, 'card-season-1668-1')
season_dict_id = app_tags.component_id('card', self.season_dict)
self.assertEqual(season_dict_id, 'card-season-1668-1')
episode_id = app_tags.component_id('card', self.episode_item)
self.assertEqual(episode_id, 'card-episode-1668-1-1')
episode_dict_id = app_tags.component_id('card', self.episode_dict)
self.assertEqual(episode_dict_id, 'card-episode-1668-1-1')
```

*Source: C:\yamtrack-fork\src\app\tests\test_templatetags.py:321*

### test_media_view_url

**Category**: workflow  
**Description**: Workflow: Test the media_view_url tag.  
**Expected**: self.assertEqual(episode_dict_modal, expected_episode_modal)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the media_view_url tag.'
tv_modal = app_tags.media_view_url('track_modal', self.tv_item)
expected_tv_modal = reverse('track_modal', kwargs={'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'media_id': '1668'})
self.assertEqual(tv_modal, expected_tv_modal)
tv_dict_modal = app_tags.media_view_url('track_modal', self.tv_dict)
self.assertEqual(tv_dict_modal, expected_tv_modal)
episode_modal = app_tags.media_view_url('history_modal', self.episode_item)
expected_episode_modal = reverse('history_modal', kwargs={'source': Sources.TMDB.value, 'media_type': MediaTypes.EPISODE.value, 'media_id': '1668', 'season_number': 1, 'episode_number': 1})
self.assertEqual(episode_modal, expected_episode_modal)
episode_dict_modal = app_tags.media_view_url('history_modal', self.episode_dict)
self.assertEqual(episode_dict_modal, expected_episode_modal)
```

*Source: C:\yamtrack-fork\src\app\tests\test_templatetags.py:347*

### test_integrations_uses_configured_webhook_urls

**Category**: workflow  
**Description**: Workflow: Test copied webhook URLs use the configured public app URL.  
**Expected**: self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/emby/initial_token')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.user.token = 'initial_token'
self.user.save()

'Test copied webhook URLs use the configured public app URL.'
response = self.client.get(reverse('integrations'))
self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/jellyfin/initial_token')
self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/plex/initial_token')
self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/emby/initial_token')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_token.py:53*

### test_integrations_uses_configured_webhook_urls

**Category**: workflow  
**Description**: Workflow: Test copied webhook URLs use the configured public app URL.  
**Expected**: self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/emby/initial_token')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test copied webhook URLs use the configured public app URL.'
response = self.client.get(reverse('integrations'))
self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/jellyfin/initial_token')
self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/plex/initial_token')
self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/emby/initial_token')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_token.py:53*

### test_watch_method

**Category**: workflow  
**Description**: Workflow: Test the watch method of the Season model.  
**Expected**: self.assertEqual(episodes.count(), 2)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create a user and a season with episodes.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=item_season, user=self.user, status=Status.IN_PROGRESS.value)
item_ep1 = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
Episode.objects.create(item=item_ep1, related_season=self.season, end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_ep2 = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=2)
Episode.objects.create(item=item_ep2, related_season=self.season, end_date=datetime(2023, 6, 2, 0, 0, tzinfo=UTC))

'Test the watch method of the Season model.'
episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=3)
mock_get_episode_item.return_value = episode_item
self.season.watch(3, datetime(2023, 6, 3, 0, 0, tzinfo=UTC))
episode = Episode.objects.get(related_season=self.season, item=episode_item)
self.assertEqual(episode.end_date, datetime(2023, 6, 3, 0, 0, tzinfo=UTC))
self.season.watch(3, datetime(2023, 6, 4, 0, 0, tzinfo=UTC))
episodes = Episode.objects.filter(related_season=self.season, item=episode_item)
self.assertEqual(episodes.first().end_date, datetime(2023, 6, 4, 0, 0, tzinfo=UTC))
self.assertEqual(episodes.count(), 2)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_season.py:104*

### test_completed_status_creates_remaining_episodes

**Category**: workflow  
**Description**: Workflow: Test setting status to COMPLETED creates remaining episodes.  
**Expected**: self.assertEqual(episode_numbers, {1, 2, 3})  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)

'Test setting status to COMPLETED creates remaining episodes.'
mock_metadata = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': datetime(2020, 1, 2, tzinfo=UTC)}, {'episode_number': 3, 'image': 'img3.jpg', 'air_date': datetime(2020, 1, 3, tzinfo=UTC)}], 'image': 'season_img.jpg'}
mock_get_metadata.return_value = mock_metadata
self.season.status = Status.COMPLETED.value
self.season.save()
self.assertEqual(self.season.episodes.count(), 3)
episode_numbers = set(self.season.episodes.values_list('item__episode_number', flat=True))
self.assertEqual(episode_numbers, {1, 2, 3})
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_season.py:282*

### test_completed_status_starts_next_season

**Category**: workflow  
**Description**: Workflow: Test completing a season starts the next season automatically.  
**Expected**: self.assertEqual(self.tv.status, Status.IN_PROGRESS.value)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)

'Test completing a season starts the next season automatically.'
next_season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image2.jpg', season_number=2)
next_season = Season.objects.create(item=next_season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
mock_get_metadata.side_effect = [{'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}], 'image': 'season_img.jpg'}, {'related': {'seasons': [{'season_number': 1, 'image': 'season_img.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 2, 'image': 'season_img2.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}}]
self.season.status = Status.COMPLETED.value
self.season.save()
next_season.refresh_from_db()
self.assertEqual(next_season.status, Status.IN_PROGRESS.value)
self.tv.refresh_from_db()
self.assertEqual(self.tv.status, Status.IN_PROGRESS.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_season.py:316*

### test_completed_last_season_completes_tv_show

**Category**: workflow  
**Description**: Workflow: Test completing the last season completes the TV show.  
**Expected**: self.assertEqual(self.tv.status, Status.COMPLETED.value)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)

'Test completing the last season completes the TV show.'
mock_get_metadata.side_effect = [{'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}], 'image': 'season_img.jpg'}, {'related': {'seasons': [{'season_number': 1, 'image': 'season_img.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}}]
self.season.status = Status.COMPLETED.value
self.season.save()
self.tv.refresh_from_db()
self.assertEqual(self.tv.status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_season.py:372*

### test_completed_status_with_unaired_episodes_leaves_season_in_progress

**Category**: workflow  
**Description**: Workflow: Completing a season should only watch episodes that have aired.  
**Expected**: self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.season} had 1 released episode marked as watched automatically.').exists())  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)

'Completing a season should only watch episodes that have aired.'
mock_get_metadata.return_value = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': datetime(2999, 1, 1, tzinfo=UTC)}, {'episode_number': 3, 'image': 'img3.jpg', 'air_date': None}], 'image': 'season_img.jpg'}
self.season.status = Status.COMPLETED.value
self.season.save()
self.season.refresh_from_db()
self.tv.refresh_from_db()
self.assertEqual(self.season.status, Status.IN_PROGRESS.value)
self.assertEqual(self.tv.status, Status.IN_PROGRESS.value)
self.assertEqual(self.season.episodes.count(), 1)
self.assertEqual(self.season.progress, 1)
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.WARNING, message=f'{self.season} was left in progress because unreleased episodes remain.').exists())
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.season} had 1 released episode marked as watched automatically.').exists())
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_season.py:405*

### test_completed_status_with_future_next_season_keeps_tv_in_progress

**Category**: workflow  
**Description**: Workflow: Completing a season should not auto-start a future season.  
**Expected**: self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.tv} remains in progress because another season is still pending or has not aired yet.').exists())  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)

'Completing a season should not auto-start a future season.'
next_season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image2.jpg', season_number=2)
next_season = Season.objects.create(item=next_season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
mock_get_metadata.side_effect = [{'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}], 'image': 'season_img.jpg'}, {'related': {'seasons': [{'season_number': 1, 'image': 'season_img.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 2, 'image': 'season_img2.jpg', 'first_air_date': datetime(2999, 1, 1, tzinfo=UTC)}]}}]
self.season.status = Status.COMPLETED.value
self.season.save()
next_season.refresh_from_db()
self.tv.refresh_from_db()
self.assertEqual(next_season.status, Status.PLANNING.value)
self.assertEqual(self.tv.status, Status.IN_PROGRESS.value)
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.tv} remains in progress because another season is still pending or has not aired yet.').exists())
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_season.py:459*

### test_completed_status_noop_if_no_remaining_episodes

**Category**: workflow  
**Description**: Workflow: Test COMPLETED status does nothing if no remaining episodes.  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)

'Test COMPLETED status does nothing if no remaining episodes.'
mock_metadata = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg'}], 'image': 'season_img.jpg'}
mock_get_metadata.return_value = mock_metadata
ep_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Episode', image='http://example.com/image.jpg', season_number=1, episode_number=1)
Episode.objects.bulk_create([Episode(item=ep_item, related_season=self.season, end_date=timezone.now())])
with patch('app.models.bulk_create_with_history') as mock_bulk_create:
    self.season.status = Status.COMPLETED.value
    self.season.save()
    mock_bulk_create.assert_not_called()
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_season.py:553*

### test_get_remaining_eps_release_date

**Category**: workflow  
**Description**: Workflow: Test get_remaining_eps uses air_date for RELEASE_DATE preference.  
**Expected**: self.assertEqual(episodes[1].end_date, datetime(1994, 9, 22, tzinfo=UTC))  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create a user and a season for testing.'
self.QuickWatchDateChoices = QuickWatchDateChoices
self.credentials = {'username': 'test_quick', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Friends', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=tv_item, user=self.user, status=Status.PLANNING.value)
self.season = Season.objects.create(item=item_season, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
self.mock_metadata = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(1994, 9, 22, tzinfo=UTC)}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': datetime(1994, 9, 29, tzinfo=UTC)}, {'episode_number': 3, 'image': 'img3.jpg', 'air_date': None}], 'image': 'season_img.jpg'}

'Test get_remaining_eps uses air_date for RELEASE_DATE preference.'
self.user.quick_watch_date = self.QuickWatchDateChoices.RELEASE_DATE
self.user.save()
episode_items = []
for i in range(1, 3):
    item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Episode {i}', image=f'img{i}.jpg', season_number=1, episode_number=i)
    episode_items.append(item)
mock_get_episode_item.side_effect = episode_items
episodes = self.season.get_remaining_eps(self.mock_metadata, timezone.localdate())
self.assertEqual(len(episodes), 2)
self.assertEqual(episodes[0].end_date, datetime(1994, 9, 29, tzinfo=UTC))
self.assertEqual(episodes[1].end_date, datetime(1994, 9, 22, tzinfo=UTC))
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_season.py:723*

### test_season_completion_with_no_date

**Category**: workflow  
**Description**: Workflow: Integration test: completing a season with NO_DATE preference.  
**Expected**: self.assertEqual(episodes.count(), 0)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create a user and a season for testing.'
self.QuickWatchDateChoices = QuickWatchDateChoices
self.credentials = {'username': 'test_quick', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Friends', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=tv_item, user=self.user, status=Status.PLANNING.value)
self.season = Season.objects.create(item=item_season, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
self.mock_metadata = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(1994, 9, 22, tzinfo=UTC)}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': datetime(1994, 9, 29, tzinfo=UTC)}, {'episode_number': 3, 'image': 'img3.jpg', 'air_date': None}], 'image': 'season_img.jpg'}

'Integration test: completing a season with NO_DATE preference.'
self.user.quick_watch_date = self.QuickWatchDateChoices.NO_DATE
self.user.save()
mock_get_metadata.return_value = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': None}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': None}], 'image': 'season_img.jpg'}
self.season.status = Status.COMPLETED.value
self.season.save()
episodes = Episode.objects.filter(related_season=self.season)
self.assertEqual(episodes.count(), 0)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_season.py:754*

### test_season_completion_with_release_date

**Category**: workflow  
**Description**: Workflow: Integration test: completing a season with RELEASE_DATE preference.  
**Expected**: self.assertEqual(episodes[1].end_date, datetime(1994, 9, 29, tzinfo=UTC))  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create a user and a season for testing.'
self.QuickWatchDateChoices = QuickWatchDateChoices
self.credentials = {'username': 'test_quick', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Friends', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=tv_item, user=self.user, status=Status.PLANNING.value)
self.season = Season.objects.create(item=item_season, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
self.mock_metadata = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(1994, 9, 22, tzinfo=UTC)}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': datetime(1994, 9, 29, tzinfo=UTC)}, {'episode_number': 3, 'image': 'img3.jpg', 'air_date': None}], 'image': 'season_img.jpg'}

'Integration test: completing a season with RELEASE_DATE preference.'
self.user.quick_watch_date = self.QuickWatchDateChoices.RELEASE_DATE
self.user.save()
mock_get_metadata.return_value = {'episodes': [{'episode_number': 1, 'image': 'img1.jpg', 'air_date': datetime(1994, 9, 22, tzinfo=UTC)}, {'episode_number': 2, 'image': 'img2.jpg', 'air_date': datetime(1994, 9, 29, tzinfo=UTC)}], 'image': 'season_img.jpg'}
self.season.status = Status.COMPLETED.value
self.season.save()
episodes = Episode.objects.filter(related_season=self.season).order_by('item__episode_number')
self.assertEqual(episodes.count(), 2)
self.assertEqual(episodes[0].end_date, datetime(1994, 9, 22, tzinfo=UTC))
self.assertEqual(episodes[1].end_date, datetime(1994, 9, 29, tzinfo=UTC))
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_season.py:774*

### test_update_episode_references

**Category**: workflow  
**Description**: Workflow: Test updating episode references with actual Season instances.  
**Expected**: self.assertEqual(new_episode.related_season.id, season.id)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

'Test updating episode references with actual Season instances.'
tv_item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show')
tv = TV.objects.create(item=tv_item, user=self.user, status=Status.PLANNING.value)
season_item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', season_number=1)
season = Season.objects.create(item=season_item, user=self.user, related_tv=tv, status=Status.PLANNING.value)
episode_item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Show', season_number=1, episode_number=1)
new_episode = Episode(item=episode_item, related_season=Season(item=season_item, related_tv=tv, user=self.user))
helpers.update_episode_references([new_episode], self.user)
self.assertEqual(new_episode.related_season.id, season.id)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_helpers.py:59*

### test_update_episode_references

**Category**: workflow  
**Description**: Workflow: Test updating episode references with actual Season instances.  
**Expected**: self.assertEqual(new_episode.related_season.id, season.id)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test updating episode references with actual Season instances.'
tv_item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show')
tv = TV.objects.create(item=tv_item, user=self.user, status=Status.PLANNING.value)
season_item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', season_number=1)
season = Season.objects.create(item=season_item, user=self.user, related_tv=tv, status=Status.PLANNING.value)
episode_item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Show', season_number=1, episode_number=1)
new_episode = Episode(item=episode_item, related_season=Season(item=season_item, related_tv=tv, user=self.user))
helpers.update_episode_references([new_episode], self.user)
self.assertEqual(new_episode.related_season.id, season.id)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_helpers.py:59*

### test_importer

**Category**: workflow  
**Description**: Workflow: Test importing media from SIMKL.  
**Expected**: self.assertEqual(anime_obj.notes, 'Great series!')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
self.importer = simkl.SimklImporter(helpers.encrypt('token'), self.user, 'new')

'Test importing media from SIMKL.'
user_list.return_value = {'shows': [{'last_watched_at': '2023-01-02T00:00:00Z', 'show': {'title': 'Breaking Bad', 'ids': {'tmdb': 1396}}, 'status': 'watching', 'user_rating': 8, 'seasons': [{'number': 1, 'episodes': [{'number': 1}, {'number': 2, 'watched_at': '2023-01-02T00:00:00Z'}]}], 'memo': {}}], 'movies': [{'added_to_watchlist_at': '2023-01-01T00:00:00Z', 'movie': {'title': 'Perfect Blue', 'ids': {'tmdb': 10494}}, 'status': 'completed', 'user_rating': 9, 'last_watched_at': '2023-02-01T00:00:00Z', 'memo': {}}], 'anime': [{'added_to_watchlist_at': '2023-01-01T00:00:00Z', 'show': {'title': 'Example Anime', 'ids': {'mal': 1}}, 'status': 'plantowatch', 'user_rating': 7, 'watched_episodes_count': 0, 'last_watched_at': None, 'memo': {'text': 'Great series!'}}]}
imported_counts, warnings = self.importer.import_data()
self.assertEqual(imported_counts[MediaTypes.TV.value], 1)
self.assertEqual(imported_counts[MediaTypes.MOVIE.value], 1)
self.assertEqual(imported_counts[MediaTypes.ANIME.value], 1)
self.assertEqual(warnings, '')
tv_item = Item.objects.get(media_type=MediaTypes.TV.value)
self.assertEqual(tv_item.title, 'Breaking Bad')
tv_obj = TV.objects.get(item=tv_item)
self.assertEqual(tv_obj.status, Status.IN_PROGRESS.value)
self.assertEqual(tv_obj.score, 8)
movie_item = Item.objects.get(media_type=MediaTypes.MOVIE.value)
self.assertEqual(movie_item.title, 'Perfect Blue')
movie_obj = Movie.objects.get(item=movie_item)
self.assertEqual(movie_obj.status, Status.COMPLETED.value)
self.assertEqual(movie_obj.score, 9)
self.assertEqual(movie_obj.progress, 1)
anime_item = Item.objects.get(media_type=MediaTypes.ANIME.value)
self.assertEqual(anime_item.title, 'Cowboy Bebop')
anime_obj = Anime.objects.get(item=anime_item)
self.assertEqual(anime_obj.status, Status.PLANNING.value)
self.assertEqual(anime_obj.score, 7)
self.assertEqual(anime_obj.notes, 'Great series!')
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_simkl.py:43*

### test_season_status_logic_with_completed_seasons

**Category**: workflow  
**Description**: Workflow: Test that seasons are marked as completed when all episodes are watched.  
**Expected**: self.assertEqual(season1_episodes.count(), 7)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
self.importer = simkl.SimklImporter(helpers.encrypt('token'), self.user, 'new')

'Test that seasons are marked as completed when all episodes are watched.'
mock_tv_with_seasons.return_value = {'title': 'Breaking Bad', 'image': 'https://image.tmdb.org/t/p/w500/test.jpg', 'season/1': {'image': 'https://image.tmdb.org/t/p/w500/season1.jpg', 'max_progress': 7, 'episodes': [{'episode_number': 1, 'still_path': '/ep1.jpg'}, {'episode_number': 2, 'still_path': '/ep2.jpg'}, {'episode_number': 3, 'still_path': '/ep3.jpg'}, {'episode_number': 4, 'still_path': '/ep4.jpg'}, {'episode_number': 5, 'still_path': '/ep5.jpg'}, {'episode_number': 6, 'still_path': '/ep6.jpg'}, {'episode_number': 7, 'still_path': '/ep7.jpg'}]}, 'season/2': {'image': 'https://image.tmdb.org/t/p/w500/season2.jpg', 'max_progress': 13}}
mock_user_list.return_value = {'shows': [{'last_watched_at': '2023-01-15T00:00:00Z', 'show': {'title': 'Breaking Bad', 'ids': {'tmdb': 1396}}, 'status': 'watching', 'user_rating': 9, 'seasons': [{'number': 1, 'episodes': [{'number': 1, 'watched_at': '2023-01-01T00:00:00Z'}, {'number': 2, 'watched_at': '2023-01-02T00:00:00Z'}, {'number': 3, 'watched_at': '2023-01-03T00:00:00Z'}, {'number': 4, 'watched_at': '2023-01-04T00:00:00Z'}, {'number': 5, 'watched_at': '2023-01-05T00:00:00Z'}, {'number': 6, 'watched_at': '2023-01-06T00:00:00Z'}, {'number': 7, 'watched_at': '2023-01-07T00:00:00Z'}]}], 'memo': {}}], 'movies': [], 'anime': []}
imported_counts, _ = self.importer.import_data()
self.assertEqual(imported_counts[MediaTypes.TV.value], 1)
self.assertEqual(imported_counts[MediaTypes.SEASON.value], 1)
self.assertEqual(imported_counts[MediaTypes.EPISODE.value], 7)
tv_item = Item.objects.get(media_type=MediaTypes.TV.value)
tv_obj = TV.objects.get(item=tv_item)
self.assertEqual(tv_obj.status, Status.IN_PROGRESS.value)
season1_item = Item.objects.get(media_type=MediaTypes.SEASON.value, season_number=1)
season1_obj = Season.objects.get(item=season1_item)
self.assertEqual(season1_obj.status, Status.COMPLETED.value, 'Season 1 should be completed when all episodes are watched')
season1_episodes = Episode.objects.filter(item__season_number=1, item__media_type=MediaTypes.EPISODE.value)
self.assertEqual(season1_episodes.count(), 7)
for episode in season1_episodes:
    self.assertIsNotNone(episode.end_date)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_simkl.py:145*

### test_importer

**Category**: workflow  
**Description**: Workflow: Test importing media from SIMKL.  
**Expected**: self.assertEqual(anime_obj.notes, 'Great series!')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: user_list

'Test importing media from SIMKL.'
user_list.return_value = {'shows': [{'last_watched_at': '2023-01-02T00:00:00Z', 'show': {'title': 'Breaking Bad', 'ids': {'tmdb': 1396}}, 'status': 'watching', 'user_rating': 8, 'seasons': [{'number': 1, 'episodes': [{'number': 1}, {'number': 2, 'watched_at': '2023-01-02T00:00:00Z'}]}], 'memo': {}}], 'movies': [{'added_to_watchlist_at': '2023-01-01T00:00:00Z', 'movie': {'title': 'Perfect Blue', 'ids': {'tmdb': 10494}}, 'status': 'completed', 'user_rating': 9, 'last_watched_at': '2023-02-01T00:00:00Z', 'memo': {}}], 'anime': [{'added_to_watchlist_at': '2023-01-01T00:00:00Z', 'show': {'title': 'Example Anime', 'ids': {'mal': 1}}, 'status': 'plantowatch', 'user_rating': 7, 'watched_episodes_count': 0, 'last_watched_at': None, 'memo': {'text': 'Great series!'}}]}
imported_counts, warnings = self.importer.import_data()
self.assertEqual(imported_counts[MediaTypes.TV.value], 1)
self.assertEqual(imported_counts[MediaTypes.MOVIE.value], 1)
self.assertEqual(imported_counts[MediaTypes.ANIME.value], 1)
self.assertEqual(warnings, '')
tv_item = Item.objects.get(media_type=MediaTypes.TV.value)
self.assertEqual(tv_item.title, 'Breaking Bad')
tv_obj = TV.objects.get(item=tv_item)
self.assertEqual(tv_obj.status, Status.IN_PROGRESS.value)
self.assertEqual(tv_obj.score, 8)
movie_item = Item.objects.get(media_type=MediaTypes.MOVIE.value)
self.assertEqual(movie_item.title, 'Perfect Blue')
movie_obj = Movie.objects.get(item=movie_item)
self.assertEqual(movie_obj.status, Status.COMPLETED.value)
self.assertEqual(movie_obj.score, 9)
self.assertEqual(movie_obj.progress, 1)
anime_item = Item.objects.get(media_type=MediaTypes.ANIME.value)
self.assertEqual(anime_item.title, 'Cowboy Bebop')
anime_obj = Anime.objects.get(item=anime_item)
self.assertEqual(anime_obj.status, Status.PLANNING.value)
self.assertEqual(anime_obj.score, 7)
self.assertEqual(anime_obj.notes, 'Great series!')
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_simkl.py:43*

### test_season_status_logic_with_completed_seasons

**Category**: workflow  
**Description**: Workflow: Test that seasons are marked as completed when all episodes are watched.  
**Expected**: self.assertEqual(season1_episodes.count(), 7)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_tv_with_seasons, mock_user_list

'Test that seasons are marked as completed when all episodes are watched.'
mock_tv_with_seasons.return_value = {'title': 'Breaking Bad', 'image': 'https://image.tmdb.org/t/p/w500/test.jpg', 'season/1': {'image': 'https://image.tmdb.org/t/p/w500/season1.jpg', 'max_progress': 7, 'episodes': [{'episode_number': 1, 'still_path': '/ep1.jpg'}, {'episode_number': 2, 'still_path': '/ep2.jpg'}, {'episode_number': 3, 'still_path': '/ep3.jpg'}, {'episode_number': 4, 'still_path': '/ep4.jpg'}, {'episode_number': 5, 'still_path': '/ep5.jpg'}, {'episode_number': 6, 'still_path': '/ep6.jpg'}, {'episode_number': 7, 'still_path': '/ep7.jpg'}]}, 'season/2': {'image': 'https://image.tmdb.org/t/p/w500/season2.jpg', 'max_progress': 13}}
mock_user_list.return_value = {'shows': [{'last_watched_at': '2023-01-15T00:00:00Z', 'show': {'title': 'Breaking Bad', 'ids': {'tmdb': 1396}}, 'status': 'watching', 'user_rating': 9, 'seasons': [{'number': 1, 'episodes': [{'number': 1, 'watched_at': '2023-01-01T00:00:00Z'}, {'number': 2, 'watched_at': '2023-01-02T00:00:00Z'}, {'number': 3, 'watched_at': '2023-01-03T00:00:00Z'}, {'number': 4, 'watched_at': '2023-01-04T00:00:00Z'}, {'number': 5, 'watched_at': '2023-01-05T00:00:00Z'}, {'number': 6, 'watched_at': '2023-01-06T00:00:00Z'}, {'number': 7, 'watched_at': '2023-01-07T00:00:00Z'}]}], 'memo': {}}], 'movies': [], 'anime': []}
imported_counts, _ = self.importer.import_data()
self.assertEqual(imported_counts[MediaTypes.TV.value], 1)
self.assertEqual(imported_counts[MediaTypes.SEASON.value], 1)
self.assertEqual(imported_counts[MediaTypes.EPISODE.value], 7)
tv_item = Item.objects.get(media_type=MediaTypes.TV.value)
tv_obj = TV.objects.get(item=tv_item)
self.assertEqual(tv_obj.status, Status.IN_PROGRESS.value)
season1_item = Item.objects.get(media_type=MediaTypes.SEASON.value, season_number=1)
season1_obj = Season.objects.get(item=season1_item)
self.assertEqual(season1_obj.status, Status.COMPLETED.value, 'Season 1 should be completed when all episodes are watched')
season1_episodes = Episode.objects.filter(item__season_number=1, item__media_type=MediaTypes.EPISODE.value)
self.assertEqual(season1_episodes.count(), 7)
for episode in season1_episodes:
    self.assertIsNotNone(episode.end_date)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_simkl.py:145*

### test_create_entry_post_season

**Category**: workflow  
**Description**: Workflow: Test creating a season entry with parent TV.  
**Expected**: self.assertEqual(season.related_tv, parent_tv)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

'Test creating a season entry with parent TV.'
tv_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='TV Show')
parent_tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
form_data = {'title': 'TV Show', 'media_type': MediaTypes.SEASON.value, 'season_number': 1, 'parent_tv': parent_tv.id, 'status': Status.IN_PROGRESS.value, 'score': 7}
response = self.client.post(reverse('create_entry'), form_data, follow=True)
self.assertRedirects(response, reverse('create_entry'))
self.assertTrue(Item.objects.filter(title='TV Show', media_type=MediaTypes.SEASON.value, season_number=1).exists())
season = Season.objects.get(item__title='TV Show')
self.assertEqual(season.status, Status.IN_PROGRESS.value)
self.assertEqual(season.score, 7)
self.assertEqual(season.user, self.user)
self.assertEqual(season.related_tv, parent_tv)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_entry.py:92*

### test_create_entry_post_episode

**Category**: workflow  
**Description**: Workflow: Test creating an episode entry with parent season.  
**Expected**: self.assertEqual(end_date_local.strftime('%Y-%m-%d %H:%M'), '2023-01-02 00:00')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

'Test creating an episode entry with parent season.'
tv_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='TV Show')
parent_tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
season_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='TV Show', season_number=1)
parent_season = Season.objects.create(item=season_item, user=self.user, related_tv=parent_tv, status=Status.IN_PROGRESS.value)
form_data = {'title': 'TV Show', 'media_type': MediaTypes.EPISODE.value, 'season_number': 1, 'episode_number': 1, 'parent_season': parent_season.id, 'end_date': '2023-01-02T00:00'}
response = self.client.post(reverse('create_entry'), form_data, follow=True)
self.assertRedirects(response, reverse('create_entry'))
self.assertTrue(Item.objects.filter(title='TV Show', media_type=MediaTypes.EPISODE.value, season_number=1, episode_number=1).exists())
episode = Episode.objects.get(item__title='TV Show')
self.assertEqual(episode.related_season, parent_season)
end_date_local = timezone.localtime(episode.end_date)
self.assertEqual(end_date_local.strftime('%Y-%m-%d %H:%M'), '2023-01-02 00:00')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_entry.py:133*

### test_create_entry_post_duplicate_item

**Category**: workflow  
**Description**: Workflow: Test creating a duplicate item.  
**Expected**: self.assertEqual(Item.objects.count(), initial_count)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

'Test creating a duplicate item.'
tv_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='TV Show')
parent_tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
season_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='TV Show', season_number=1)
Season.objects.create(item=season_item, user=self.user, related_tv=parent_tv, status=Status.IN_PROGRESS.value)
initial_count = Item.objects.count()
form_data = {'title': 'TV Show', 'media_type': MediaTypes.SEASON.value, 'season_number': 1, 'parent_tv': parent_tv.id, 'status': Status.IN_PROGRESS.value, 'score': 7, 'repeats': 0}
with transaction.atomic():
    self.client.post(reverse('create_entry'), form_data)
self.assertEqual(Item.objects.count(), initial_count)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_entry.py:188*

### test_create_entry_post_season

**Category**: workflow  
**Description**: Workflow: Test creating a season entry with parent TV.  
**Expected**: self.assertEqual(season.related_tv, parent_tv)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test creating a season entry with parent TV.'
tv_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='TV Show')
parent_tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
form_data = {'title': 'TV Show', 'media_type': MediaTypes.SEASON.value, 'season_number': 1, 'parent_tv': parent_tv.id, 'status': Status.IN_PROGRESS.value, 'score': 7}
response = self.client.post(reverse('create_entry'), form_data, follow=True)
self.assertRedirects(response, reverse('create_entry'))
self.assertTrue(Item.objects.filter(title='TV Show', media_type=MediaTypes.SEASON.value, season_number=1).exists())
season = Season.objects.get(item__title='TV Show')
self.assertEqual(season.status, Status.IN_PROGRESS.value)
self.assertEqual(season.score, 7)
self.assertEqual(season.user, self.user)
self.assertEqual(season.related_tv, parent_tv)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_entry.py:92*

### test_create_entry_post_episode

**Category**: workflow  
**Description**: Workflow: Test creating an episode entry with parent season.  
**Expected**: self.assertEqual(end_date_local.strftime('%Y-%m-%d %H:%M'), '2023-01-02 00:00')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test creating an episode entry with parent season.'
tv_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='TV Show')
parent_tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
season_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='TV Show', season_number=1)
parent_season = Season.objects.create(item=season_item, user=self.user, related_tv=parent_tv, status=Status.IN_PROGRESS.value)
form_data = {'title': 'TV Show', 'media_type': MediaTypes.EPISODE.value, 'season_number': 1, 'episode_number': 1, 'parent_season': parent_season.id, 'end_date': '2023-01-02T00:00'}
response = self.client.post(reverse('create_entry'), form_data, follow=True)
self.assertRedirects(response, reverse('create_entry'))
self.assertTrue(Item.objects.filter(title='TV Show', media_type=MediaTypes.EPISODE.value, season_number=1, episode_number=1).exists())
episode = Episode.objects.get(item__title='TV Show')
self.assertEqual(episode.related_season, parent_season)
end_date_local = timezone.localtime(episode.end_date)
self.assertEqual(end_date_local.strftime('%Y-%m-%d %H:%M'), '2023-01-02 00:00')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_entry.py:133*

### test_create_entry_post_duplicate_item

**Category**: workflow  
**Description**: Workflow: Test creating a duplicate item.  
**Expected**: self.assertEqual(Item.objects.count(), initial_count)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test creating a duplicate item.'
tv_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='TV Show')
parent_tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
season_item = Item.objects.create(media_id='1', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='TV Show', season_number=1)
Season.objects.create(item=season_item, user=self.user, related_tv=parent_tv, status=Status.IN_PROGRESS.value)
initial_count = Item.objects.count()
form_data = {'title': 'TV Show', 'media_type': MediaTypes.SEASON.value, 'season_number': 1, 'parent_tv': parent_tv.id, 'status': Status.IN_PROGRESS.value, 'score': 7, 'repeats': 0}
with transaction.atomic():
    self.client.post(reverse('create_entry'), form_data)
self.assertEqual(Item.objects.count(), initial_count)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_entry.py:188*

### test_last_episode_sets_season_completed

**Category**: workflow  
**Description**: Workflow: Test last episode sets season to COMPLETED.  
**Expected**: self.assertEqual(self.tv.status, Status.COMPLETED.value)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
self.episode_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Episode', image='http://example.com/image.jpg', season_number=1, episode_number=1)

'Test last episode sets season to COMPLETED.'
mock_metadata = {'season/1': {'episodes': [{'episode_number': 1}]}, 'related': {'seasons': [{'season_number': 1}]}}
mock_get_metadata.return_value = mock_metadata
Episode.objects.create(item=self.episode_item, related_season=self.season, end_date=timezone.now())
self.season.refresh_from_db()
self.assertEqual(self.season.status, Status.COMPLETED.value)
self.tv.refresh_from_db()
self.assertEqual(self.tv.status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_episode.py:143*

### test_last_season_completes_tv_show

**Category**: workflow  
**Description**: Workflow: Test last season completion also completes TV show.  
**Expected**: self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.SUCCESS, message=f'{self.tv} was marked as completed automatically.').exists())  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
self.episode_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Episode', image='http://example.com/image.jpg', season_number=1, episode_number=1)

'Test last season completion also completes TV show.'
mock_metadata = {'season/1': {'episodes': [{'episode_number': 1}]}, 'related': {'seasons': [{'season_number': 1}]}}
mock_get_metadata.return_value = mock_metadata
Episode.objects.create(item=self.episode_item, related_season=self.season, end_date=timezone.now())
self.tv.refresh_from_db()
self.assertEqual(self.tv.status, Status.COMPLETED.value)
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.SUCCESS, message=f'{self.tv} was marked as completed automatically.').exists())
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_episode.py:210*

### test_non_last_season_starts_next_season

**Category**: workflow  
**Description**: Workflow: Test non-last season completion starts the next season.  
**Expected**: self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.tv} Season 2 was marked as in progress automatically.').exists())  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
self.episode_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Episode', image='http://example.com/image.jpg', season_number=1, episode_number=1)

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

*Source: C:\yamtrack-fork\src\app\tests\models\test_episode.py:239*

### test_last_episode_sets_season_completed

**Category**: workflow  
**Description**: Workflow: Test last episode sets season to COMPLETED.  
**Expected**: self.assertEqual(self.tv.status, Status.COMPLETED.value)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_metadata

'Test last episode sets season to COMPLETED.'
mock_metadata = {'season/1': {'episodes': [{'episode_number': 1}]}, 'related': {'seasons': [{'season_number': 1}]}}
mock_get_metadata.return_value = mock_metadata
Episode.objects.create(item=self.episode_item, related_season=self.season, end_date=timezone.now())
self.season.refresh_from_db()
self.assertEqual(self.season.status, Status.COMPLETED.value)
self.tv.refresh_from_db()
self.assertEqual(self.tv.status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_episode.py:143*

### test_last_season_completes_tv_show

**Category**: workflow  
**Description**: Workflow: Test last season completion also completes TV show.  
**Expected**: self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.SUCCESS, message=f'{self.tv} was marked as completed automatically.').exists())  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_metadata

'Test last season completion also completes TV show.'
mock_metadata = {'season/1': {'episodes': [{'episode_number': 1}]}, 'related': {'seasons': [{'season_number': 1}]}}
mock_get_metadata.return_value = mock_metadata
Episode.objects.create(item=self.episode_item, related_season=self.season, end_date=timezone.now())
self.tv.refresh_from_db()
self.assertEqual(self.tv.status, Status.COMPLETED.value)
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.SUCCESS, message=f'{self.tv} was marked as completed automatically.').exists())
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_episode.py:210*

### test_non_last_season_starts_next_season

**Category**: workflow  
**Description**: Workflow: Test non-last season completion starts the next season.  
**Expected**: self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.tv} Season 2 was marked as in progress automatically.').exists())  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_metadata

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

*Source: C:\yamtrack-fork\src\app\tests\models\test_episode.py:239*

### test_get_next_run_info_daily

**Category**: workflow  
**Description**: Workflow: Test getting next run info for daily task.  
**Expected**: self.assertEqual(next_run_info['frequency'], 'Every Day')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test getting next run info for daily task.'
current_time = datetime(2025, 2, 6, 12, 0, tzinfo=zoneinfo.ZoneInfo('UTC'))
mock_now.return_value = current_time
crontab = CrontabSchedule.objects.create(minute='0', hour='14', day_of_week='*', day_of_month='*', month_of_year='*', timezone='UTC')
periodic_task = PeriodicTask.objects.create(name='Daily Import', task='import_task', crontab=crontab)
next_run_info = helpers.get_next_run_info(periodic_task)
expected_next_run = datetime(2025, 2, 6, 14, 0, tzinfo=zoneinfo.ZoneInfo('UTC'))
self.assertEqual(next_run_info['next_run'], expected_next_run)
self.assertEqual(next_run_info['frequency'], 'Every Day')
```

*Source: C:\yamtrack-fork\src\users\tests\test_helpers.py:106*

### test_get_next_run_info_every_2_days

**Category**: workflow  
**Description**: Workflow: Test getting next run info for every 2 days task.  
**Expected**: self.assertEqual(next_run_info['frequency'], 'Every 2 days')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test getting next run info for every 2 days task.'
current_time = datetime(2025, 2, 6, 12, 0, tzinfo=zoneinfo.ZoneInfo('UTC'))
mock_now.return_value = current_time
crontab = CrontabSchedule.objects.create(minute='0', hour='14', day_of_week='*/2', day_of_month='*', month_of_year='*', timezone='UTC')
periodic_task = PeriodicTask.objects.create(name='Every 2 Days Import', task='import_task', crontab=crontab)
next_run_info = helpers.get_next_run_info(periodic_task)
expected_next_run = datetime(2025, 2, 6, 14, 0, tzinfo=zoneinfo.ZoneInfo('UTC'))
self.assertEqual(next_run_info['next_run'], expected_next_run)
self.assertEqual(next_run_info['frequency'], 'Every 2 days')
```

*Source: C:\yamtrack-fork\src\users\tests\test_helpers.py:133*

### test_get_next_run_info_every_2_days_after_todays_run

**Category**: workflow  
**Description**: Workflow: Test getting next run info for every 2 days.  
**Expected**: self.assertEqual(next_run_info['frequency'], 'Every 2 days')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test getting next run info for every 2 days.'
current_time = datetime(2025, 2, 6, 15, 0, tzinfo=zoneinfo.ZoneInfo('UTC'))
mock_now.return_value = current_time
crontab = CrontabSchedule.objects.create(minute='0', hour='14', day_of_week='*/2', day_of_month='*', month_of_year='*', timezone='UTC')
periodic_task = PeriodicTask.objects.create(name='Every 2 Days Import', task='import_task', crontab=crontab)
next_run_info = helpers.get_next_run_info(periodic_task)
expected_next_run = datetime(2025, 2, 8, 14, 0, tzinfo=zoneinfo.ZoneInfo('UTC'))
self.assertEqual(next_run_info['next_run'], expected_next_run)
self.assertEqual(next_run_info['frequency'], 'Every 2 days')
```

*Source: C:\yamtrack-fork\src\users\tests\test_helpers.py:162*

### test_get_next_run_info_daily

**Category**: workflow  
**Description**: Workflow: Test getting next run info for daily task.  
**Expected**: self.assertEqual(next_run_info['frequency'], 'Every Day')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_now

'Test getting next run info for daily task.'
current_time = datetime(2025, 2, 6, 12, 0, tzinfo=zoneinfo.ZoneInfo('UTC'))
mock_now.return_value = current_time
crontab = CrontabSchedule.objects.create(minute='0', hour='14', day_of_week='*', day_of_month='*', month_of_year='*', timezone='UTC')
periodic_task = PeriodicTask.objects.create(name='Daily Import', task='import_task', crontab=crontab)
next_run_info = helpers.get_next_run_info(periodic_task)
expected_next_run = datetime(2025, 2, 6, 14, 0, tzinfo=zoneinfo.ZoneInfo('UTC'))
self.assertEqual(next_run_info['next_run'], expected_next_run)
self.assertEqual(next_run_info['frequency'], 'Every Day')
```

*Source: C:\yamtrack-fork\src\users\tests\test_helpers.py:106*

### test_get_next_run_info_every_2_days

**Category**: workflow  
**Description**: Workflow: Test getting next run info for every 2 days task.  
**Expected**: self.assertEqual(next_run_info['frequency'], 'Every 2 days')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_now

'Test getting next run info for every 2 days task.'
current_time = datetime(2025, 2, 6, 12, 0, tzinfo=zoneinfo.ZoneInfo('UTC'))
mock_now.return_value = current_time
crontab = CrontabSchedule.objects.create(minute='0', hour='14', day_of_week='*/2', day_of_month='*', month_of_year='*', timezone='UTC')
periodic_task = PeriodicTask.objects.create(name='Every 2 Days Import', task='import_task', crontab=crontab)
next_run_info = helpers.get_next_run_info(periodic_task)
expected_next_run = datetime(2025, 2, 6, 14, 0, tzinfo=zoneinfo.ZoneInfo('UTC'))
self.assertEqual(next_run_info['next_run'], expected_next_run)
self.assertEqual(next_run_info['frequency'], 'Every 2 days')
```

*Source: C:\yamtrack-fork\src\users\tests\test_helpers.py:133*

### test_get_next_run_info_every_2_days_after_todays_run

**Category**: workflow  
**Description**: Workflow: Test getting next run info for every 2 days.  
**Expected**: self.assertEqual(next_run_info['frequency'], 'Every 2 days')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_now

'Test getting next run info for every 2 days.'
current_time = datetime(2025, 2, 6, 15, 0, tzinfo=zoneinfo.ZoneInfo('UTC'))
mock_now.return_value = current_time
crontab = CrontabSchedule.objects.create(minute='0', hour='14', day_of_week='*/2', day_of_month='*', month_of_year='*', timezone='UTC')
periodic_task = PeriodicTask.objects.create(name='Every 2 Days Import', task='import_task', crontab=crontab)
next_run_info = helpers.get_next_run_info(periodic_task)
expected_next_run = datetime(2025, 2, 8, 14, 0, tzinfo=zoneinfo.ZoneInfo('UTC'))
self.assertEqual(next_run_info['next_run'], expected_next_run)
self.assertEqual(next_run_info['frequency'], 'Every 2 days')
```

*Source: C:\yamtrack-fork\src\users\tests\test_helpers.py:162*

### test_home_view

**Category**: workflow  
**Description**: Workflow: Test the home view displays in-progress and planning media.  
**Expected**: self.assertEqual(planning_movies['items'][0].status, Status.PLANNING.value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_number = season_numbers[0]
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'details': {'seasons': 1}, f'season/{season_number}': {'episodes': [{'id': i} for i in range(1, 11)]}, 'related': {'seasons': [{'season_number': season_number, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'season/1': {'episodes': [{'id': i} for i in range(1, 11)]}}
    if media_type == MediaTypes.ANIME.value:
        return {'title': 'Test Anime', 'image': 'http://example.com/image.jpg', 'max_progress': 24}
    if media_type == MediaTypes.MOVIE.value:
        return {'title': 'Planned Movie', 'image': 'http://example.com/image.jpg', 'max_progress': 1}
    return {'max_progress': None}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', image='http://example.com/image.jpg', season_number=1)
season = Season.objects.create(item=season_item, user=self.user, status=Status.IN_PROGRESS.value)
for i in range(1, 6):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    Episode.objects.create(item=episode_item, related_season=season, end_date=timezone.now() - timezone.timedelta(days=i))
anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/image.jpg')
Anime.objects.create(item=anime_item, user=self.user, status=Status.IN_PROGRESS.value, progress=10)
movie_item = Item.objects.create(media_id='10', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Planned Movie', image='http://example.com/image.jpg')
Movie.objects.create(item=movie_item, user=self.user, status=Status.PLANNING.value)

'Test the home view displays in-progress and planning media.'
response = self.client.get(reverse('home'))
self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/home.html')
self.assertIn('home_sections', response.context)
sections_by_key = {section['key']: section for section in response.context['home_sections']}
self.assertIn(Status.IN_PROGRESS.value, sections_by_key)
self.assertIn(Status.PLANNING.value, sections_by_key)
in_progress_section = sections_by_key[Status.IN_PROGRESS.value]
planning_section = sections_by_key[Status.PLANNING.value]
self.assertIn(MediaTypes.SEASON.value, in_progress_section['media_types'])
self.assertIn(MediaTypes.ANIME.value, in_progress_section['media_types'])
self.assertIn(MediaTypes.MOVIE.value, planning_section['media_types'])
self.assertIn('sort_choices', response.context)
self.assertEqual(response.context['sort_choices'], HomeSortChoices.choices)
self.assertEqual(in_progress_section['count'], 2)
self.assertEqual(planning_section['count'], 1)
season = in_progress_section['media_types'][MediaTypes.SEASON.value]
self.assertEqual(len(season['items']), 1)
self.assertEqual(season['items'][0].progress, 5)
planning_movies = planning_section['media_types'][MediaTypes.MOVIE.value]
self.assertEqual(len(planning_movies['items']), 1)
self.assertEqual(planning_movies['items'][0].status, Status.PLANNING.value)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_home.py:160*

### test_home_view_includes_in_progress_tv_with_unwatched_seasons

**Category**: workflow  
**Description**: Workflow: Test in-progress TV with unwatched seasons appears on home.  
**Expected**: self.assertEqual(tv_media['items'][0].item.title, 'Returning Show')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_number = season_numbers[0]
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'details': {'seasons': 1}, f'season/{season_number}': {'episodes': [{'id': i} for i in range(1, 11)]}, 'related': {'seasons': [{'season_number': season_number, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'season/1': {'episodes': [{'id': i} for i in range(1, 11)]}}
    if media_type == MediaTypes.ANIME.value:
        return {'title': 'Test Anime', 'image': 'http://example.com/image.jpg', 'max_progress': 24}
    if media_type == MediaTypes.MOVIE.value:
        return {'title': 'Planned Movie', 'image': 'http://example.com/image.jpg', 'max_progress': 1}
    return {'max_progress': None}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', image='http://example.com/image.jpg', season_number=1)
season = Season.objects.create(item=season_item, user=self.user, status=Status.IN_PROGRESS.value)
for i in range(1, 6):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    Episode.objects.create(item=episode_item, related_season=season, end_date=timezone.now() - timezone.timedelta(days=i))
anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/image.jpg')
Anime.objects.create(item=anime_item, user=self.user, status=Status.IN_PROGRESS.value, progress=10)
movie_item = Item.objects.create(media_id='10', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Planned Movie', image='http://example.com/image.jpg')
Movie.objects.create(item=movie_item, user=self.user, status=Status.PLANNING.value)

'Test in-progress TV with unwatched seasons appears on home.'
tv_item = Item.objects.create(media_id='tv-with-new-season', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Returning Show', image='http://example.com/returning-show.jpg')
tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
unwatched_season_item = Item.objects.create(media_id='tv-with-new-season', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Returning Show', image='http://example.com/returning-show.jpg', season_number=2)
Season.objects.create(item=unwatched_season_item, user=self.user, related_tv=tv, status=Status.PLANNING.value)
response = self.client.get(reverse('home'))
sections_by_key = {section['key']: section for section in response.context['home_sections']}
in_progress_section = sections_by_key[Status.IN_PROGRESS.value]
self.assertIn(MediaTypes.TV.value, in_progress_section['media_types'])
tv_media = in_progress_section['media_types'][MediaTypes.TV.value]
self.assertEqual(tv_media['total'], 1)
self.assertEqual(tv_media['items'][0].item.title, 'Returning Show')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_home.py:195*

### test_home_view_htmx_load_more

**Category**: workflow  
**Description**: Workflow: Test the HTMX load more functionality.  
**Expected**: self.assertEqual(response.context['media_list']['total'], 15)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_number = season_numbers[0]
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'details': {'seasons': 1}, f'season/{season_number}': {'episodes': [{'id': i} for i in range(1, 11)]}, 'related': {'seasons': [{'season_number': season_number, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'season/1': {'episodes': [{'id': i} for i in range(1, 11)]}}
    if media_type == MediaTypes.ANIME.value:
        return {'title': 'Test Anime', 'image': 'http://example.com/image.jpg', 'max_progress': 24}
    if media_type == MediaTypes.MOVIE.value:
        return {'title': 'Planned Movie', 'image': 'http://example.com/image.jpg', 'max_progress': 1}
    return {'max_progress': None}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', image='http://example.com/image.jpg', season_number=1)
season = Season.objects.create(item=season_item, user=self.user, status=Status.IN_PROGRESS.value)
for i in range(1, 6):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    Episode.objects.create(item=episode_item, related_season=season, end_date=timezone.now() - timezone.timedelta(days=i))
anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/image.jpg')
Anime.objects.create(item=anime_item, user=self.user, status=Status.IN_PROGRESS.value, progress=10)
movie_item = Item.objects.create(media_id='10', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Planned Movie', image='http://example.com/image.jpg')
Movie.objects.create(item=movie_item, user=self.user, status=Status.PLANNING.value)

'Test the HTMX load more functionality.'
mock_get_media_metadata.return_value = {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'season/1': {'episodes': [{'id': 1}, {'id': 2}, {'id': 3}]}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
for i in range(6, 20):
    season_item = Item.objects.create(media_id=str(i), source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title=f'Test TV Show {i}', image='http://example.com/image.jpg', season_number=1)
    season = Season.objects.create(item=season_item, user=self.user, status=Status.IN_PROGRESS.value)
    episode_item = Item.objects.create(media_id=str(i), source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Test TV Show {i}', image='http://example.com/image.jpg', season_number=1, episode_number=1)
    Episode.objects.create(item=episode_item, related_season=season, end_date=timezone.now())
response = self.client.get(reverse('home') + '?load_media_type=season', headers={'hx-request': 'true'})
self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/components/home_grid.html')
self.assertIn('media_list', response.context)
self.assertEqual(response.context['home_status'], Status.IN_PROGRESS.value)
self.assertIn('items', response.context['media_list'])
self.assertIn('total', response.context['media_list'])
self.assertEqual(len(response.context['media_list']['items']), 1)
self.assertEqual(response.context['media_list']['total'], 15)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_home.py:248*

### test_home_view

**Category**: workflow  
**Description**: Workflow: Test the home view displays in-progress and planning media.  
**Expected**: self.assertEqual(planning_movies['items'][0].status, Status.PLANNING.value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the home view displays in-progress and planning media.'
response = self.client.get(reverse('home'))
self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/home.html')
self.assertIn('home_sections', response.context)
sections_by_key = {section['key']: section for section in response.context['home_sections']}
self.assertIn(Status.IN_PROGRESS.value, sections_by_key)
self.assertIn(Status.PLANNING.value, sections_by_key)
in_progress_section = sections_by_key[Status.IN_PROGRESS.value]
planning_section = sections_by_key[Status.PLANNING.value]
self.assertIn(MediaTypes.SEASON.value, in_progress_section['media_types'])
self.assertIn(MediaTypes.ANIME.value, in_progress_section['media_types'])
self.assertIn(MediaTypes.MOVIE.value, planning_section['media_types'])
self.assertIn('sort_choices', response.context)
self.assertEqual(response.context['sort_choices'], HomeSortChoices.choices)
self.assertEqual(in_progress_section['count'], 2)
self.assertEqual(planning_section['count'], 1)
season = in_progress_section['media_types'][MediaTypes.SEASON.value]
self.assertEqual(len(season['items']), 1)
self.assertEqual(season['items'][0].progress, 5)
planning_movies = planning_section['media_types'][MediaTypes.MOVIE.value]
self.assertEqual(len(planning_movies['items']), 1)
self.assertEqual(planning_movies['items'][0].status, Status.PLANNING.value)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_home.py:160*

### test_home_view_includes_in_progress_tv_with_unwatched_seasons

**Category**: workflow  
**Description**: Workflow: Test in-progress TV with unwatched seasons appears on home.  
**Expected**: self.assertEqual(tv_media['items'][0].item.title, 'Returning Show')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test in-progress TV with unwatched seasons appears on home.'
tv_item = Item.objects.create(media_id='tv-with-new-season', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Returning Show', image='http://example.com/returning-show.jpg')
tv = TV.objects.create(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
unwatched_season_item = Item.objects.create(media_id='tv-with-new-season', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Returning Show', image='http://example.com/returning-show.jpg', season_number=2)
Season.objects.create(item=unwatched_season_item, user=self.user, related_tv=tv, status=Status.PLANNING.value)
response = self.client.get(reverse('home'))
sections_by_key = {section['key']: section for section in response.context['home_sections']}
in_progress_section = sections_by_key[Status.IN_PROGRESS.value]
self.assertIn(MediaTypes.TV.value, in_progress_section['media_types'])
tv_media = in_progress_section['media_types'][MediaTypes.TV.value]
self.assertEqual(tv_media['total'], 1)
self.assertEqual(tv_media['items'][0].item.title, 'Returning Show')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_home.py:195*

### test_home_view_htmx_load_more

**Category**: workflow  
**Description**: Workflow: Test the HTMX load more functionality.  
**Expected**: self.assertEqual(response.context['media_list']['total'], 15)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_media_metadata

'Test the HTMX load more functionality.'
mock_get_media_metadata.return_value = {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'season/1': {'episodes': [{'id': 1}, {'id': 2}, {'id': 3}]}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
for i in range(6, 20):
    season_item = Item.objects.create(media_id=str(i), source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title=f'Test TV Show {i}', image='http://example.com/image.jpg', season_number=1)
    season = Season.objects.create(item=season_item, user=self.user, status=Status.IN_PROGRESS.value)
    episode_item = Item.objects.create(media_id=str(i), source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title=f'Test TV Show {i}', image='http://example.com/image.jpg', season_number=1, episode_number=1)
    Episode.objects.create(item=episode_item, related_season=season, end_date=timezone.now())
response = self.client.get(reverse('home') + '?load_media_type=season', headers={'hx-request': 'true'})
self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/components/home_grid.html')
self.assertIn('media_list', response.context)
self.assertEqual(response.context['home_status'], Status.IN_PROGRESS.value)
self.assertIn('items', response.context['media_list'])
self.assertIn('total', response.context['media_list'])
self.assertEqual(len(response.context['media_list']['items']), 1)
self.assertEqual(response.context['media_list']['total'], 15)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_home.py:248*

### test_calendar_default_view

**Category**: workflow  
**Description**: Workflow: Test the calendar view with default parameters.  
**Expected**: self.assertEqual(response.context['today'], today)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

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

*Source: C:\yamtrack-fork\src\events\tests\test_views.py:26*

### test_calendar_with_month_year_params

**Category**: workflow  
**Description**: Workflow: Test the calendar view with month and year parameters.  
**Expected**: self.assertEqual(response.context['next_year'], 2024)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

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

*Source: C:\yamtrack-fork\src\events\tests\test_views.py:71*

### test_calendar_with_invalid_month_year

**Category**: workflow  
**Description**: Workflow: Test the calendar view with invalid month and year parameters.  
**Expected**: self.assertEqual(response.context['year'], today.year)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

'Test the calendar view with invalid month and year parameters.'
mock_update_preference.return_value = 'month'
mock_get_user_events.return_value = []
response = self.client.get(reverse('calendar') + '?month=invalid&year=invalid')
self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'events/calendar.html')
today = timezone.localdate()
self.assertEqual(response.context['month'], today.month)
self.assertEqual(response.context['year'], today.year)
```

*Source: C:\yamtrack-fork\src\events\tests\test_views.py:132*

### test_calendar_with_events

**Category**: workflow  
**Description**: Workflow: Test the calendar with events.  
**Expected**: self.assertEqual(len(release_dict[20]), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

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

*Source: C:\yamtrack-fork\src\events\tests\test_views.py:202*

### test_download_calendar_with_events

**Category**: workflow  
**Description**: Workflow: Test downloading a calendar with events.  
**Expected**: self.assertEqual(call_args[0][2], expected_end)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.url = reverse('download_calendar', args=[self.user.token])

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

*Source: C:\yamtrack-fork\src\events\tests\test_views.py:328*

### test_calendar_default_view

**Category**: workflow  
**Description**: Workflow: Test the calendar view with default parameters.  
**Expected**: self.assertEqual(response.context['today'], today)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_update_preference, mock_get_user_events

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

*Source: C:\yamtrack-fork\src\events\tests\test_views.py:26*

### test_calendar_with_month_year_params

**Category**: workflow  
**Description**: Workflow: Test the calendar view with month and year parameters.  
**Expected**: self.assertEqual(response.context['next_year'], 2024)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_update_preference, mock_get_user_events

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

*Source: C:\yamtrack-fork\src\events\tests\test_views.py:71*

### test_calendar_with_invalid_month_year

**Category**: workflow  
**Description**: Workflow: Test the calendar view with invalid month and year parameters.  
**Expected**: self.assertEqual(response.context['year'], today.year)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_update_preference, mock_get_user_events

'Test the calendar view with invalid month and year parameters.'
mock_update_preference.return_value = 'month'
mock_get_user_events.return_value = []
response = self.client.get(reverse('calendar') + '?month=invalid&year=invalid')
self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'events/calendar.html')
today = timezone.localdate()
self.assertEqual(response.context['month'], today.month)
self.assertEqual(response.context['year'], today.year)
```

*Source: C:\yamtrack-fork\src\events\tests\test_views.py:132*

### test_calendar_with_events

**Category**: workflow  
**Description**: Workflow: Test the calendar with events.  
**Expected**: self.assertEqual(len(release_dict[20]), 1)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_update_preference, mock_get_user_events

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

*Source: C:\yamtrack-fork\src\events\tests\test_views.py:202*

### test_download_calendar_with_events

**Category**: workflow  
**Description**: Workflow: Test downloading a calendar with events.  
**Expected**: self.assertEqual(call_args[0][2], expected_end)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_user_events

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

*Source: C:\yamtrack-fork\src\events\tests\test_views.py:328*

### test_cleanup_user_messages_deletes_only_old_shown_messages

**Category**: workflow  
**Description**: Workflow: Delete only shown messages older than the retention window.  
**Expected**: self.assertTrue(UserMessage.objects.filter(id=unseen.id).exists())  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create a user for task tests.'
self.user = get_user_model().objects.create_user(username='test')

'Delete only shown messages older than the retention window.'
now = timezone.now()
old_shown = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='old shown', shown_at=now - timedelta(days=31))
recent_shown = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='recent shown', shown_at=now - timedelta(days=5))
unseen = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='unseen')
deleted_count = cleanup_user_messages()
self.assertEqual(deleted_count, 1)
self.assertFalse(UserMessage.objects.filter(id=old_shown.id).exists())
self.assertTrue(UserMessage.objects.filter(id=recent_shown.id).exists())
self.assertTrue(UserMessage.objects.filter(id=unseen.id).exists())
```

*Source: C:\yamtrack-fork\src\app\tests\test_tasks.py:21*

### test_cleanup_user_messages_deletes_only_old_shown_messages

**Category**: workflow  
**Description**: Workflow: Delete only shown messages older than the retention window.  
**Expected**: self.assertTrue(UserMessage.objects.filter(id=unseen.id).exists())  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Delete only shown messages older than the retention window.'
now = timezone.now()
old_shown = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='old shown', shown_at=now - timedelta(days=31))
recent_shown = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='recent shown', shown_at=now - timedelta(days=5))
unseen = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='unseen')
deleted_count = cleanup_user_messages()
self.assertEqual(deleted_count, 1)
self.assertFalse(UserMessage.objects.filter(id=old_shown.id).exists())
self.assertTrue(UserMessage.objects.filter(id=recent_shown.id).exists())
self.assertTrue(UserMessage.objects.filter(id=unseen.id).exists())
```

*Source: C:\yamtrack-fork\src\app\tests\test_tasks.py:21*

### test_process_comic_with_store_date

**Category**: workflow  
**Description**: Workflow: Test process_comic with store date available.  
**Expected**: mock_issue.assert_called_once_with('4000-123456')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test process_comic with store date available.'
comic_item = Item.objects.create(media_id='4050-18166', source=Sources.COMICVINE.value, media_type=MediaTypes.COMIC.value, title='Batman', image='http://example.com/batman.jpg')
mock_get_media_metadata.return_value = {'max_issue_number': 10, 'last_issue_id': '4000-123456', 'last_issue': {'issue_number': '10'}}
mock_issue.return_value = {'store_date': '2023-04-15', 'cover_date': '2023-05-01'}
events_bulk = []
process_comic(comic_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, comic_item)
self.assertEqual(events_bulk[0].content_number, 10)
self.assertEqual(events_bulk[0].datetime, date_parser('2023-04-15'))
mock_issue.assert_called_once_with('4000-123456')
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_comic.py:18*

### test_process_comic_with_cover_date_only

**Category**: workflow  
**Description**: Workflow: Test process_comic with only cover date available.  
**Expected**: self.assertEqual(events_bulk[0].datetime, date_parser('2023-05-01'))  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test process_comic with only cover date available.'
comic_item = Item.objects.create(media_id='4050-18167', source=Sources.COMICVINE.value, media_type=MediaTypes.COMIC.value, title='Superman', image='http://example.com/superman.jpg')
mock_get_media_metadata.return_value = {'max_issue_number': 5, 'last_issue_id': '4000-123457', 'last_issue': {'issue_number': '5'}}
mock_issue.return_value = {'store_date': None, 'cover_date': '2023-05-01'}
events_bulk = []
process_comic(comic_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, comic_item)
self.assertEqual(events_bulk[0].content_number, 5)
self.assertEqual(events_bulk[0].datetime, date_parser('2023-05-01'))
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_comic.py:50*

### test_process_comic_no_dates

**Category**: workflow  
**Description**: Workflow: Test process_comic with no dates available.  
**Expected**: self.assertEqual(len(events_bulk), 0)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test process_comic with no dates available.'
comic_item = Item.objects.create(media_id='4050-18168', source=Sources.COMICVINE.value, media_type=MediaTypes.COMIC.value, title='Wonder Woman', image='http://example.com/wonderwoman.jpg')
mock_get_media_metadata.return_value = {'max_issue_number': 3, 'last_issue_id': '4000-123458', 'last_issue': {'issue_number': '3'}}
mock_issue.return_value = {'store_date': None, 'cover_date': None}
events_bulk = []
process_comic(comic_item, events_bulk)
self.assertEqual(len(events_bulk), 0)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_comic.py:85*

### test_process_comic_returns_when_issue_is_already_saved

**Category**: workflow  
**Description**: Workflow: No new event should be added if the latest issue is already stored.  
**Expected**: self.assertEqual(events_bulk, [])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'No new event should be added if the latest issue is already stored.'
Event.objects.create(item=self.comic_item, content_number=10, datetime=date_parser('2023-04-15'))
mock_get_media_metadata.return_value = {'max_issue_number': 10, 'last_issue_id': '4000-123456', 'last_issue': {'issue_number': '10'}}
events_bulk = []
process_comic(self.comic_item, events_bulk)
self.assertEqual(events_bulk, [])
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_comic.py:112*

### test_process_comic_handles_issue_provider_error

**Category**: workflow  
**Description**: Workflow: Issue lookup failures should stop comic processing quietly.  
**Expected**: self.assertEqual(events_bulk, [])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Issue lookup failures should stop comic processing quietly.'
response = type('Response', (), {'status_code': 500, 'text': 'boom'})()
mock_get_media_metadata.return_value = {'max_issue_number': 10, 'last_issue_id': '4000-123456', 'last_issue': {'issue_number': '10'}}
mock_issue.side_effect = services.ProviderAPIError(provider=Sources.COMICVINE.value, error=type('Error', (), {'response': response})(), details='boom')
events_bulk = []
process_comic(self.comic_item, events_bulk)
self.assertEqual(events_bulk, [])
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_comic.py:135*

### test_process_comic_with_store_date

**Category**: workflow  
**Description**: Workflow: Test process_comic with store date available.  
**Expected**: mock_issue.assert_called_once_with('4000-123456')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_issue, mock_get_media_metadata

'Test process_comic with store date available.'
comic_item = Item.objects.create(media_id='4050-18166', source=Sources.COMICVINE.value, media_type=MediaTypes.COMIC.value, title='Batman', image='http://example.com/batman.jpg')
mock_get_media_metadata.return_value = {'max_issue_number': 10, 'last_issue_id': '4000-123456', 'last_issue': {'issue_number': '10'}}
mock_issue.return_value = {'store_date': '2023-04-15', 'cover_date': '2023-05-01'}
events_bulk = []
process_comic(comic_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, comic_item)
self.assertEqual(events_bulk[0].content_number, 10)
self.assertEqual(events_bulk[0].datetime, date_parser('2023-04-15'))
mock_issue.assert_called_once_with('4000-123456')
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_comic.py:18*

### test_process_comic_with_cover_date_only

**Category**: workflow  
**Description**: Workflow: Test process_comic with only cover date available.  
**Expected**: self.assertEqual(events_bulk[0].datetime, date_parser('2023-05-01'))  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_issue, mock_get_media_metadata

'Test process_comic with only cover date available.'
comic_item = Item.objects.create(media_id='4050-18167', source=Sources.COMICVINE.value, media_type=MediaTypes.COMIC.value, title='Superman', image='http://example.com/superman.jpg')
mock_get_media_metadata.return_value = {'max_issue_number': 5, 'last_issue_id': '4000-123457', 'last_issue': {'issue_number': '5'}}
mock_issue.return_value = {'store_date': None, 'cover_date': '2023-05-01'}
events_bulk = []
process_comic(comic_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, comic_item)
self.assertEqual(events_bulk[0].content_number, 5)
self.assertEqual(events_bulk[0].datetime, date_parser('2023-05-01'))
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_comic.py:50*

### test_process_comic_no_dates

**Category**: workflow  
**Description**: Workflow: Test process_comic with no dates available.  
**Expected**: self.assertEqual(len(events_bulk), 0)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_issue, mock_get_media_metadata

'Test process_comic with no dates available.'
comic_item = Item.objects.create(media_id='4050-18168', source=Sources.COMICVINE.value, media_type=MediaTypes.COMIC.value, title='Wonder Woman', image='http://example.com/wonderwoman.jpg')
mock_get_media_metadata.return_value = {'max_issue_number': 3, 'last_issue_id': '4000-123458', 'last_issue': {'issue_number': '3'}}
mock_issue.return_value = {'store_date': None, 'cover_date': None}
events_bulk = []
process_comic(comic_item, events_bulk)
self.assertEqual(len(events_bulk), 0)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_comic.py:85*

### test_process_comic_returns_when_issue_is_already_saved

**Category**: workflow  
**Description**: Workflow: No new event should be added if the latest issue is already stored.  
**Expected**: self.assertEqual(events_bulk, [])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_media_metadata

'No new event should be added if the latest issue is already stored.'
Event.objects.create(item=self.comic_item, content_number=10, datetime=date_parser('2023-04-15'))
mock_get_media_metadata.return_value = {'max_issue_number': 10, 'last_issue_id': '4000-123456', 'last_issue': {'issue_number': '10'}}
events_bulk = []
process_comic(self.comic_item, events_bulk)
self.assertEqual(events_bulk, [])
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_comic.py:112*

### test_process_comic_handles_issue_provider_error

**Category**: workflow  
**Description**: Workflow: Issue lookup failures should stop comic processing quietly.  
**Expected**: self.assertEqual(events_bulk, [])  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_issue, mock_get_media_metadata

'Issue lookup failures should stop comic processing quietly.'
response = type('Response', (), {'status_code': 500, 'text': 'boom'})()
mock_get_media_metadata.return_value = {'max_issue_number': 10, 'last_issue_id': '4000-123456', 'last_issue': {'issue_number': '10'}}
mock_issue.side_effect = services.ProviderAPIError(provider=Sources.COMICVINE.value, error=type('Error', (), {'response': response})(), details='boom')
events_bulk = []
process_comic(self.comic_item, events_bulk)
self.assertEqual(events_bulk, [])
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_comic.py:135*

### test_get_item_filter

**Category**: workflow  
**Description**: Workflow: Test the get_item filter.  
**Expected**: self.assertIn('[]', rendered)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the get_item filter.'
template_str = '\n            {% load events_tags %}\n            {{ my_dict|get_item:"key1" }}\n            {{ my_dict|get_item:"key2" }}\n            {{ my_dict|get_item:"nonexistent_key" }}\n        '
template = Template(template_str)
context = Context({'my_dict': {'key1': 'value1', 'key2': ['item1', 'item2']}})
rendered = template.render(context)
self.assertIn('value1', rendered)
self.assertIn('item1', rendered)
self.assertIn('item2', rendered)
self.assertIn('[]', rendered)
```

*Source: C:\yamtrack-fork\src\events\tests\test_templatetags.py:8*

### test_get_item_filter_with_empty_dict

**Category**: workflow  
**Description**: Workflow: Test the get_item filter with an empty dictionary.  
**Expected**: self.assertIn('[]', rendered)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the get_item filter with an empty dictionary.'
template_str = '\n            {% load events_tags %}\n            {{ empty_dict|get_item:"any_key" }}\n        '
template = Template(template_str)
context = Context({'empty_dict': {}})
rendered = template.render(context)
self.assertIn('[]', rendered)
```

*Source: C:\yamtrack-fork\src\events\tests\test_templatetags.py:38*

### test_day_of_week_tag_with_variables

**Category**: workflow  
**Description**: Workflow: Test the day_of_week tag with variables.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the day_of_week tag with variables.'
template_str = '\n            {% load events_tags %}\n            {% day_of_week day month year %}\n        '
template = Template(template_str)
test_dates = [{'day': 1, 'month': 1, 'year': 2023, 'expected': 'Sunday'}, {'day': 4, 'month': 7, 'year': 2023, 'expected': 'Tuesday'}, {'day': 25, 'month': 12, 'year': 2023, 'expected': 'Monday'}, {'day': '31', 'month': '10', 'year': '2023', 'expected': 'Tuesday'}]
for date_data in test_dates:
    context = Context({'day': date_data['day'], 'month': date_data['month'], 'year': date_data['year']})
    rendered = template.render(context)
    self.assertIn(date_data['expected'], rendered)
```

*Source: C:\yamtrack-fork\src\events\tests\test_templatetags.py:74*

### test_day_of_week_tag_edge_cases

**Category**: workflow  
**Description**: Workflow: Test the day_of_week tag with edge cases.  
**Expected**: self.assertIn('Tuesday', rendered)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the day_of_week tag with edge cases.'
template_str = '\n            {% load events_tags %}\n            {% day_of_week 29 2 2020 %}\n        '
template = Template(template_str)
rendered = template.render(Context({}))
self.assertIn('Saturday', rendered)
template_str = '\n            {% load events_tags %}\n            {% day_of_week 1 1 2030 %}\n        '
template = Template(template_str)
rendered = template.render(Context({}))
self.assertIn('Tuesday', rendered)
```

*Source: C:\yamtrack-fork\src\events\tests\test_templatetags.py:101*

### test_day_of_week_tag_invalid_input

**Category**: workflow  
**Description**: Workflow: Test the day_of_week tag with invalid input.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the day_of_week tag with invalid input.'
template_str = '\n            {% load events_tags %}\n            {% day_of_week 30 2 2023 %}\n        '
template = Template(template_str)
with self.assertRaises(ValueError):
    template.render(Context({}))
template_str = '\n            {% load events_tags %}\n            {% day_of_week "day" "month" "year" %}\n        '
template = Template(template_str)
with self.assertRaises(ValueError):
    template.render(Context({'day': 'day', 'month': 'month', 'year': 'year'}))
```

*Source: C:\yamtrack-fork\src\events\tests\test_templatetags.py:122*

### test_get_item_filter

**Category**: workflow  
**Description**: Workflow: Test the get_item filter.  
**Expected**: self.assertIn('[]', rendered)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the get_item filter.'
template_str = '\n            {% load events_tags %}\n            {{ my_dict|get_item:"key1" }}\n            {{ my_dict|get_item:"key2" }}\n            {{ my_dict|get_item:"nonexistent_key" }}\n        '
template = Template(template_str)
context = Context({'my_dict': {'key1': 'value1', 'key2': ['item1', 'item2']}})
rendered = template.render(context)
self.assertIn('value1', rendered)
self.assertIn('item1', rendered)
self.assertIn('item2', rendered)
self.assertIn('[]', rendered)
```

*Source: C:\yamtrack-fork\src\events\tests\test_templatetags.py:8*

### test_get_item_filter_with_empty_dict

**Category**: workflow  
**Description**: Workflow: Test the get_item filter with an empty dictionary.  
**Expected**: self.assertIn('[]', rendered)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the get_item filter with an empty dictionary.'
template_str = '\n            {% load events_tags %}\n            {{ empty_dict|get_item:"any_key" }}\n        '
template = Template(template_str)
context = Context({'empty_dict': {}})
rendered = template.render(context)
self.assertIn('[]', rendered)
```

*Source: C:\yamtrack-fork\src\events\tests\test_templatetags.py:38*

### test_day_of_week_tag_with_variables

**Category**: workflow  
**Description**: Workflow: Test the day_of_week tag with variables.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the day_of_week tag with variables.'
template_str = '\n            {% load events_tags %}\n            {% day_of_week day month year %}\n        '
template = Template(template_str)
test_dates = [{'day': 1, 'month': 1, 'year': 2023, 'expected': 'Sunday'}, {'day': 4, 'month': 7, 'year': 2023, 'expected': 'Tuesday'}, {'day': 25, 'month': 12, 'year': 2023, 'expected': 'Monday'}, {'day': '31', 'month': '10', 'year': '2023', 'expected': 'Tuesday'}]
for date_data in test_dates:
    context = Context({'day': date_data['day'], 'month': date_data['month'], 'year': date_data['year']})
    rendered = template.render(context)
    self.assertIn(date_data['expected'], rendered)
```

*Source: C:\yamtrack-fork\src\events\tests\test_templatetags.py:74*

### test_day_of_week_tag_edge_cases

**Category**: workflow  
**Description**: Workflow: Test the day_of_week tag with edge cases.  
**Expected**: self.assertIn('Tuesday', rendered)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the day_of_week tag with edge cases.'
template_str = '\n            {% load events_tags %}\n            {% day_of_week 29 2 2020 %}\n        '
template = Template(template_str)
rendered = template.render(Context({}))
self.assertIn('Saturday', rendered)
template_str = '\n            {% load events_tags %}\n            {% day_of_week 1 1 2030 %}\n        '
template = Template(template_str)
rendered = template.render(Context({}))
self.assertIn('Tuesday', rendered)
```

*Source: C:\yamtrack-fork\src\events\tests\test_templatetags.py:101*

### test_day_of_week_tag_invalid_input

**Category**: workflow  
**Description**: Workflow: Test the day_of_week tag with invalid input.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the day_of_week tag with invalid input.'
template_str = '\n            {% load events_tags %}\n            {% day_of_week 30 2 2023 %}\n        '
template = Template(template_str)
with self.assertRaises(ValueError):
    template.render(Context({}))
template_str = '\n            {% load events_tags %}\n            {% day_of_week "day" "month" "year" %}\n        '
template = Template(template_str)
with self.assertRaises(ValueError):
    template.render(Context({'day': 'day', 'month': 'month', 'year': 'year'}))
```

*Source: C:\yamtrack-fork\src\events\tests\test_templatetags.py:122*

### test_process_other_movie

**Category**: workflow  
**Description**: Workflow: Test process_other for a movie.  
**Expected**: self.assertEqual(events_bulk[0].datetime, date_parser('1999-10-15'))  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test process_other for a movie.'
mock_get_media_metadata.return_value = {'max_progress': 1, 'details': {'release_date': '1999-10-15'}}
events_bulk = []
process_other(self.movie_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, self.movie_item)
self.assertIsNone(events_bulk[0].content_number)
self.assertEqual(events_bulk[0].datetime, date_parser('1999-10-15'))
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_other.py:18*

### test_process_other_book

**Category**: workflow  
**Description**: Workflow: Test process_other for a book.  
**Expected**: self.assertEqual(events_bulk[0].datetime, date_parser('1949-06-08'))  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test process_other for a book.'
mock_get_media_metadata.return_value = {'max_progress': 328, 'details': {'publish_date': '1949-06-08'}}
events_bulk = []
process_other(self.book_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, self.book_item)
self.assertEqual(events_bulk[0].content_number, 328)
self.assertEqual(events_bulk[0].datetime, date_parser('1949-06-08'))
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_other.py:36*

### test_process_other_manga

**Category**: workflow  
**Description**: Workflow: Test process_other for manga.  
**Expected**: self.assertEqual(events_bulk[0].datetime, date_parser('2023-12-22'))  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test process_other for manga.'
mock_get_media_metadata.return_value = {'details': {'end_date': '2023-12-22'}, 'max_progress': 375}
events_bulk = []
process_other(self.manga_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, self.manga_item)
self.assertEqual(events_bulk[0].content_number, 375)
self.assertEqual(events_bulk[0].datetime, date_parser('2023-12-22'))
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_other.py:54*

### test_process_other_mangaupdates

**Category**: workflow  
**Description**: Workflow: Test process_other for MangaUpdates manga.  
**Expected**: self.assertEqual(events_bulk[0].datetime, expected_date)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test process_other for MangaUpdates manga.'
mangaupdates_item = Item.objects.create(media_id='123', source=Sources.MANGAUPDATES.value, media_type=MediaTypes.MANGA.value, title='Some Manga', image='http://example.com/manga.jpg')
mock_get_media_metadata.return_value = {'max_progress': 100, 'details': {}}
events_bulk = []
process_other(mangaupdates_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, mangaupdates_item)
self.assertEqual(events_bulk[0].content_number, 100)
expected_date = datetime.datetime.min.replace(tzinfo=ZoneInfo('UTC'))
self.assertEqual(events_bulk[0].datetime, expected_date)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_other.py:72*

### test_process_other_uses_placeholder_when_date_is_unknown

**Category**: workflow  
**Description**: Workflow: A known max progress with an empty date should use a placeholder.  
**Expected**: self.assertEqual(events_bulk[0].datetime, datetime.datetime.min.replace(tzinfo=ZoneInfo('UTC')))  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'A known max progress with an empty date should use a placeholder.'
mock_get_media_metadata.return_value = {'max_progress': 328, 'details': {'publish_date': ''}}
events_bulk = []
process_other(self.book_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].datetime, datetime.datetime.min.replace(tzinfo=ZoneInfo('UTC')))
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_other.py:97*

### test_process_other_game

**Category**: workflow  
**Description**: Workflow: Test process_other for a game.  
**Expected**: self.assertEqual(events_bulk[0].datetime, date_parser('2025-10-15'))  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test process_other for a game.'
game_item = Item.objects.create(media_id='52189', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Grand Theft Auto VI', image='http://example.com/gta6.jpg')
mock_get_media_metadata.return_value = {'max_progress': None, 'details': {'release_date': '2025-10-15'}}
events_bulk = []
process_other(game_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, game_item)
self.assertIsNone(events_bulk[0].content_number)
self.assertEqual(events_bulk[0].datetime, date_parser('2025-10-15'))
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_other.py:119*

### test_process_other_invalid_date

**Category**: workflow  
**Description**: Workflow: Test process_other with invalid date.  
**Expected**: self.assertEqual(len(events_bulk), 0)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test process_other with invalid date.'
mock_get_media_metadata.return_value = {'max_progress': None, 'details': {'release_date': 'invalid-date'}}
events_bulk = []
process_other(self.movie_item, events_bulk)
self.assertEqual(len(events_bulk), 0)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_other.py:145*

### test_process_other_no_date

**Category**: workflow  
**Description**: Workflow: Test process_other with no date.  
**Expected**: self.assertEqual(len(events_bulk), 0)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test process_other with no date.'
mock_get_media_metadata.return_value = {'max_progress': None, 'details': {}}
events_bulk = []
process_other(self.movie_item, events_bulk)
self.assertEqual(len(events_bulk), 0)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_other.py:160*

### test_process_other_movie

**Category**: workflow  
**Description**: Workflow: Test process_other for a movie.  
**Expected**: self.assertEqual(events_bulk[0].datetime, date_parser('1999-10-15'))  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_media_metadata

'Test process_other for a movie.'
mock_get_media_metadata.return_value = {'max_progress': 1, 'details': {'release_date': '1999-10-15'}}
events_bulk = []
process_other(self.movie_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, self.movie_item)
self.assertIsNone(events_bulk[0].content_number)
self.assertEqual(events_bulk[0].datetime, date_parser('1999-10-15'))
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_other.py:18*

### test_process_other_book

**Category**: workflow  
**Description**: Workflow: Test process_other for a book.  
**Expected**: self.assertEqual(events_bulk[0].datetime, date_parser('1949-06-08'))  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_media_metadata

'Test process_other for a book.'
mock_get_media_metadata.return_value = {'max_progress': 328, 'details': {'publish_date': '1949-06-08'}}
events_bulk = []
process_other(self.book_item, events_bulk)
self.assertEqual(len(events_bulk), 1)
self.assertEqual(events_bulk[0].item, self.book_item)
self.assertEqual(events_bulk[0].content_number, 328)
self.assertEqual(events_bulk[0].datetime, date_parser('1949-06-08'))
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_other.py:36*

### test_episode_queries_episode_endpoint

**Category**: workflow  
**Description**: Workflow: Test TVDB episode lookup returns normalized episode metadata.  
**Expected**: mock_cache.set.assert_called_once_with('tvdb_episode_12345', {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
'Test TVDB episode lookup returns normalized episode metadata.'
mock_cache.get.return_value = None
mock_get_access_token.return_value = 'test-token'
mock_api_request.return_value = {'data': {'id': 12345, 'seriesId': 74796, 'seasonNumber': 2, 'number': 2, 'absoluteNumber': 22}}
result = tvdb.episode(12345)
self.assertEqual(result, {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})
mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'GET', f'{tvdb.BASE_URL}/episodes/12345', headers={'Authorization': 'Bearer test-token'})
mock_cache.set.assert_called_once_with('tvdb_episode_12345', {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_tvdb.py:45*

### test_episode_queries_episode_endpoint

**Category**: workflow  
**Description**: Workflow: Test TVDB episode lookup returns normalized episode metadata.  
**Expected**: mock_cache.set.assert_called_once_with('tvdb_episode_12345', {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_api_request, mock_get_access_token, mock_cache

'Test TVDB episode lookup returns normalized episode metadata.'
mock_cache.get.return_value = None
mock_get_access_token.return_value = 'test-token'
mock_api_request.return_value = {'data': {'id': 12345, 'seriesId': 74796, 'seasonNumber': 2, 'number': 2, 'absoluteNumber': 22}}
result = tvdb.episode(12345)
self.assertEqual(result, {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})
mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'GET', f'{tvdb.BASE_URL}/episodes/12345', headers={'Authorization': 'Bearer test-token'})
mock_cache.set.assert_called_once_with('tvdb_episode_12345', {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_tvdb.py:45*

### test_completed_progress

**Category**: workflow  
**Description**: Workflow: When completed, the progress should be the total number of episodes.  
**Expected**: self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).progress, 26)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
item_anime = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/image.jpg')
self.anime = Anime.objects.create(item=item_anime, user=self.user, status=Status.PLANNING.value)

'When completed, the progress should be the total number of episodes.'
self.anime.status = Status.COMPLETED.value
self.anime.save()
self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).progress, 26)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media.py:39*

### test_completed_progress

**Category**: workflow  
**Description**: Workflow: When completed, the progress should be the total number of episodes.  
**Expected**: self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).progress, 26)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'When completed, the progress should be the total number of episodes.'
self.anime.status = Status.COMPLETED.value
self.anime.save()
self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).progress, 26)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media.py:39*

### test_completed_status_creates_all_seasons

**Category**: workflow  
**Description**: Workflow: Test setting status to COMPLETED creates all seasons.  
**Expected**: self.assertEqual(self.tv.seasons.filter(status=Status.COMPLETED.value).count(), 3)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season1_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, related_tv=self.tv, status=Status.IN_PROGRESS.value)
self.season2_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=2)
self.season2 = Season.objects.create(item=self.season2_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)

'Test setting status to COMPLETED creates all seasons.'
released_episodes = [{'episode_number': episode_number, 'air_date': datetime(2020, 1, 1, tzinfo=UTC)} for episode_number in range(1, 11)]
mock_metadata = {'max_progress': 10, 'related': {'seasons': [{'season_number': 1, 'image': 'img1.jpg'}, {'season_number': 2, 'image': 'img2.jpg'}, {'season_number': 3, 'image': 'img3.jpg'}]}, 'season/1': {'image': 'http://example.com/image.jpg', 'season_number': 1, 'episodes': released_episodes}, 'season/2': {'image': 'http://example.com/image.jpg', 'season_number': 2, 'episodes': released_episodes}, 'season/3': {'image': 'http://example.com/image.jpg', 'season_number': 3, 'episodes': released_episodes}}
mock_get_metadata.return_value = mock_metadata
self.tv.status = Status.COMPLETED.value
self.tv.save()
self.assertEqual(self.tv.seasons.count(), 3)
self.assertEqual(self.tv.seasons.filter(status=Status.COMPLETED.value).count(), 3)
for season in self.tv.seasons.all():
    self.assertTrue(season.episodes.exists())
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_tv.py:208*

### test_completed_status_skips_unaired_episodes_and_future_seasons

**Category**: workflow  
**Description**: Workflow: Completed TV should only mark already aired content as watched.  
**Expected**: self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.tv} had 2 released episodes marked as watched automatically.').exists())  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season1_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, related_tv=self.tv, status=Status.IN_PROGRESS.value)
self.season2_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=2)
self.season2 = Season.objects.create(item=self.season2_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)

'Completed TV should only mark already aired content as watched.'
mock_get_metadata.return_value = {'max_progress': 4, 'related': {'seasons': [{'season_number': 1, 'image': 'img1.jpg'}, {'season_number': 2, 'image': 'img2.jpg'}, {'season_number': 3, 'image': 'img3.jpg'}]}, 'season/1': {'image': 'http://example.com/image.jpg', 'season_number': 1, 'episodes': [{'episode_number': 1, 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}, 'season/2': {'image': 'http://example.com/image.jpg', 'season_number': 2, 'episodes': [{'episode_number': 1, 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'episode_number': 2, 'air_date': datetime(2999, 1, 1, tzinfo=UTC)}]}, 'season/3': {'image': 'http://example.com/image.jpg', 'season_number': 3, 'episodes': [{'episode_number': 1, 'air_date': None}]}}
self.tv.status = Status.COMPLETED.value
self.tv.save()
season1 = self.tv.seasons.get(item__season_number=1)
season2 = self.tv.seasons.get(item__season_number=2)
season3 = self.tv.seasons.get(item__season_number=3)
self.tv.refresh_from_db()
season1.refresh_from_db()
season2.refresh_from_db()
season3.refresh_from_db()
self.assertEqual(self.tv.status, Status.IN_PROGRESS.value)
self.assertEqual(season1.status, Status.COMPLETED.value)
self.assertEqual(season2.status, Status.IN_PROGRESS.value)
self.assertEqual(season3.status, Status.PLANNING.value)
self.assertEqual(season2.episodes.count(), 1)
self.assertEqual(season2.progress, 1)
self.assertFalse(season3.episodes.exists())
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.WARNING, message=f'{self.tv} was left in progress because unreleased episodes or seasons remain.').exists())
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.tv} had 2 released episodes marked as watched automatically.').exists())
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_tv.py:257*

### test_in_progress_status_activates_next_season

**Category**: workflow  
**Description**: Workflow: Test setting status to IN_PROGRESS activates next available season.  
**Expected**: self.assertEqual(season2.status, Status.IN_PROGRESS.value)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season1_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, related_tv=self.tv, status=Status.IN_PROGRESS.value)
self.season2_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=2)
self.season2 = Season.objects.create(item=self.season2_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)

'Test setting status to IN_PROGRESS activates next available season.'
self.season1.status = Status.COMPLETED.value
self.season1.save()
mock_get_metadata.return_value = {'related': {'seasons': [{'season_number': 1, 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 2, 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}}
self.tv.status = Status.IN_PROGRESS.value
self.tv.save()
season2 = Season.objects.get(pk=self.season2.pk)
self.assertEqual(season2.status, Status.IN_PROGRESS.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_tv.py:362*

### test_in_progress_status_creates_new_season_if_needed

**Category**: workflow  
**Description**: Workflow: Test setting status to IN_PROGRESS creates new season if needed.  
**Expected**: self.assertEqual(season3.status, Status.IN_PROGRESS.value)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season1_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, related_tv=self.tv, status=Status.IN_PROGRESS.value)
self.season2_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=2)
self.season2 = Season.objects.create(item=self.season2_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)

'Test setting status to IN_PROGRESS creates new season if needed.'
self.season1.status = Status.COMPLETED.value
self.season1.save()
self.season2.status = Status.COMPLETED.value
self.season2.save()
mock_metadata = {'related': {'seasons': [{'season_number': 1, 'image': 'img1.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 2, 'image': 'img2.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 3, 'image': 'img3.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}}
mock_get_metadata.return_value = mock_metadata
self.tv.status = Status.IN_PROGRESS.value
self.tv.save()
season3 = self.tv.seasons.get(item__season_number=3)
self.assertEqual(season3.status, Status.IN_PROGRESS.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_tv.py:389*

### test_completed_status_creates_all_seasons

**Category**: workflow  
**Description**: Workflow: Test setting status to COMPLETED creates all seasons.  
**Expected**: self.assertEqual(self.tv.seasons.filter(status=Status.COMPLETED.value).count(), 3)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_metadata

'Test setting status to COMPLETED creates all seasons.'
released_episodes = [{'episode_number': episode_number, 'air_date': datetime(2020, 1, 1, tzinfo=UTC)} for episode_number in range(1, 11)]
mock_metadata = {'max_progress': 10, 'related': {'seasons': [{'season_number': 1, 'image': 'img1.jpg'}, {'season_number': 2, 'image': 'img2.jpg'}, {'season_number': 3, 'image': 'img3.jpg'}]}, 'season/1': {'image': 'http://example.com/image.jpg', 'season_number': 1, 'episodes': released_episodes}, 'season/2': {'image': 'http://example.com/image.jpg', 'season_number': 2, 'episodes': released_episodes}, 'season/3': {'image': 'http://example.com/image.jpg', 'season_number': 3, 'episodes': released_episodes}}
mock_get_metadata.return_value = mock_metadata
self.tv.status = Status.COMPLETED.value
self.tv.save()
self.assertEqual(self.tv.seasons.count(), 3)
self.assertEqual(self.tv.seasons.filter(status=Status.COMPLETED.value).count(), 3)
for season in self.tv.seasons.all():
    self.assertTrue(season.episodes.exists())
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_tv.py:208*

### test_completed_status_skips_unaired_episodes_and_future_seasons

**Category**: workflow  
**Description**: Workflow: Completed TV should only mark already aired content as watched.  
**Expected**: self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.tv} had 2 released episodes marked as watched automatically.').exists())  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_metadata

'Completed TV should only mark already aired content as watched.'
mock_get_metadata.return_value = {'max_progress': 4, 'related': {'seasons': [{'season_number': 1, 'image': 'img1.jpg'}, {'season_number': 2, 'image': 'img2.jpg'}, {'season_number': 3, 'image': 'img3.jpg'}]}, 'season/1': {'image': 'http://example.com/image.jpg', 'season_number': 1, 'episodes': [{'episode_number': 1, 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}, 'season/2': {'image': 'http://example.com/image.jpg', 'season_number': 2, 'episodes': [{'episode_number': 1, 'air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'episode_number': 2, 'air_date': datetime(2999, 1, 1, tzinfo=UTC)}]}, 'season/3': {'image': 'http://example.com/image.jpg', 'season_number': 3, 'episodes': [{'episode_number': 1, 'air_date': None}]}}
self.tv.status = Status.COMPLETED.value
self.tv.save()
season1 = self.tv.seasons.get(item__season_number=1)
season2 = self.tv.seasons.get(item__season_number=2)
season3 = self.tv.seasons.get(item__season_number=3)
self.tv.refresh_from_db()
season1.refresh_from_db()
season2.refresh_from_db()
season3.refresh_from_db()
self.assertEqual(self.tv.status, Status.IN_PROGRESS.value)
self.assertEqual(season1.status, Status.COMPLETED.value)
self.assertEqual(season2.status, Status.IN_PROGRESS.value)
self.assertEqual(season3.status, Status.PLANNING.value)
self.assertEqual(season2.episodes.count(), 1)
self.assertEqual(season2.progress, 1)
self.assertFalse(season3.episodes.exists())
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.WARNING, message=f'{self.tv} was left in progress because unreleased episodes or seasons remain.').exists())
self.assertTrue(UserMessage.objects.filter(user=self.user, level=UserMessageLevel.INFO, message=f'{self.tv} had 2 released episodes marked as watched automatically.').exists())
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_tv.py:257*

### test_in_progress_status_activates_next_season

**Category**: workflow  
**Description**: Workflow: Test setting status to IN_PROGRESS activates next available season.  
**Expected**: self.assertEqual(season2.status, Status.IN_PROGRESS.value)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_metadata

'Test setting status to IN_PROGRESS activates next available season.'
self.season1.status = Status.COMPLETED.value
self.season1.save()
mock_get_metadata.return_value = {'related': {'seasons': [{'season_number': 1, 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 2, 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}}
self.tv.status = Status.IN_PROGRESS.value
self.tv.save()
season2 = Season.objects.get(pk=self.season2.pk)
self.assertEqual(season2.status, Status.IN_PROGRESS.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_tv.py:362*

### test_in_progress_status_creates_new_season_if_needed

**Category**: workflow  
**Description**: Workflow: Test setting status to IN_PROGRESS creates new season if needed.  
**Expected**: self.assertEqual(season3.status, Status.IN_PROGRESS.value)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_metadata

'Test setting status to IN_PROGRESS creates new season if needed.'
self.season1.status = Status.COMPLETED.value
self.season1.save()
self.season2.status = Status.COMPLETED.value
self.season2.save()
mock_metadata = {'related': {'seasons': [{'season_number': 1, 'image': 'img1.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 2, 'image': 'img2.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}, {'season_number': 3, 'image': 'img3.jpg', 'first_air_date': datetime(2020, 1, 1, tzinfo=UTC)}]}}
mock_get_metadata.return_value = mock_metadata
self.tv.status = Status.IN_PROGRESS.value
self.tv.save()
season3 = self.tv.seasons.get(item__season_number=3)
self.assertEqual(season3.status, Status.IN_PROGRESS.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_tv.py:389*

### test_enrich_items_with_user_data

**Category**: workflow  
**Description**: Workflow: Test enriching items with multiple scenarios.  
**Expected**: self.assertEqual(unknown_movie_enriched['item']['description'], "This movie doesn't exist in our database")  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': 'testpass'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.request = MagicMock()
self.request.user = self.user
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/movie.jpg')
self.season_item = Item.objects.create(media_id='67890', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', image='http://example.com/show.jpg', season_number=1)
self.movie_media = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, progress=1)

'Test enriching items with multiple scenarios.'
raw_items = [{'media_id': '238', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Test Movie', 'image': 'http://example.com/movie.jpg', 'release_date': '2023-01-01', 'rating': 8.5, 'genre': 'Action'}, {'media_id': '67890', 'source': Sources.TMDB.value, 'media_type': MediaTypes.SEASON.value, 'title': 'Test TV Show', 'season_title': 'Season 1', 'season_number': 1, 'image': 'http://example.com/show.jpg'}, {'media_id': '99999', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Unknown Movie', 'image': 'http://example.com/unknown.jpg', 'description': "This movie doesn't exist in our database"}]
enriched_items = enrich_items_with_user_data(self.request, raw_items, 'test')
self.assertEqual(len(enriched_items), 3)
movie_enriched = enriched_items[0]
self.assertEqual(movie_enriched['media'], self.movie_media)
self.assertEqual(movie_enriched['item']['title'], 'Test Movie')
self.assertEqual(movie_enriched['item']['media_id'], '238')
self.assertEqual(movie_enriched['item']['release_date'], '2023-01-01')
self.assertEqual(movie_enriched['item']['rating'], 8.5)
self.assertEqual(movie_enriched['item']['genre'], 'Action')
season_enriched = enriched_items[1]
self.assertEqual(season_enriched['media'], None)
self.assertEqual(season_enriched['item']['season_title'], 'Season 1')
self.assertEqual(season_enriched['item']['season_number'], 1)
unknown_movie_enriched = enriched_items[2]
self.assertEqual(unknown_movie_enriched['item']['media_id'], raw_items[2]['media_id'])
self.assertEqual(unknown_movie_enriched['media'], None)
self.assertEqual(unknown_movie_enriched['item']['title'], 'Unknown Movie')
self.assertEqual(unknown_movie_enriched['item']['media_id'], '99999')
self.assertEqual(unknown_movie_enriched['item']['description'], "This movie doesn't exist in our database")
```

*Source: C:\yamtrack-fork\src\app\tests\test_helpers.py:159*

### test_hide_completed_recommendations_enabled

**Category**: workflow  
**Description**: Workflow: Test that completed items are hidden when preference is enabled.  
**Expected**: self.assertEqual(enriched_items[0]['item']['media_id'], '99999')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': 'testpass'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.request = MagicMock()
self.request.user = self.user
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/movie.jpg')
self.season_item = Item.objects.create(media_id='67890', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', image='http://example.com/show.jpg', season_number=1)
self.movie_media = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, progress=1)

'Test that completed items are hidden when preference is enabled.'
self.user.hide_completed_recommendations = True
self.user.save()
raw_items = [{'media_id': '238', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Test Movie', 'image': 'http://example.com/movie.jpg'}, {'media_id': '99999', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Unknown Movie', 'image': 'http://example.com/unknown.jpg'}]
enriched_items = enrich_items_with_user_data(self.request, raw_items, 'recommendations')
self.assertEqual(len(enriched_items), 1)
self.assertEqual(enriched_items[0]['item']['media_id'], '99999')
```

*Source: C:\yamtrack-fork\src\app\tests\test_helpers.py:233*

### test_hide_completed_recommendations_disabled

**Category**: workflow  
**Description**: Workflow: Test that completed items are shown when preference is disabled.  
**Expected**: self.assertEqual(len(enriched_items), 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': 'testpass'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.request = MagicMock()
self.request.user = self.user
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/movie.jpg')
self.season_item = Item.objects.create(media_id='67890', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', image='http://example.com/show.jpg', season_number=1)
self.movie_media = Movie.objects.create(item=self.movie_item, user=self.user, status=Status.COMPLETED.value, progress=1)

'Test that completed items are shown when preference is disabled.'
self.user.hide_completed_recommendations = False
self.user.save()
raw_items = [{'media_id': '238', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Test Movie', 'image': 'http://example.com/movie.jpg'}, {'media_id': '99999', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Unknown Movie', 'image': 'http://example.com/unknown.jpg'}]
enriched_items = enrich_items_with_user_data(self.request, raw_items, 'recommendations')
self.assertEqual(len(enriched_items), 2)
```

*Source: C:\yamtrack-fork\src\app\tests\test_helpers.py:262*

### test_is_released_date_with_full_date

**Category**: workflow  
**Description**: Workflow: Test is_released_date with YYYY-MM-DD string format.  
**Expected**: self.assertFalse(is_released_date(future_date_str))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test is_released_date with YYYY-MM-DD string format.'
past_date_str = '2020-05-15'
self.assertTrue(is_released_date(past_date_str))
future_date_str = '2099-12-31'
self.assertFalse(is_released_date(future_date_str))
```

*Source: C:\yamtrack-fork\src\app\tests\test_helpers.py:334*

### test_is_released_date_with_custom_current_date

**Category**: workflow  
**Description**: Workflow: Test is_released_date with explicit current_date parameter.  
**Expected**: self.assertTrue(is_released_date(test_date, current_date))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test is_released_date with explicit current_date parameter.'
test_date = date(2020, 5, 15)
current_date = date(2020, 5, 20)
self.assertTrue(is_released_date(test_date, current_date))
current_date = date(2020, 5, 10)
self.assertFalse(is_released_date(test_date, current_date))
current_date = date(2020, 5, 15)
self.assertTrue(is_released_date(test_date, current_date))
```

*Source: C:\yamtrack-fork\src\app\tests\test_helpers.py:358*

### test_enrich_items_with_user_data

**Category**: workflow  
**Description**: Workflow: Test enriching items with multiple scenarios.  
**Expected**: self.assertEqual(unknown_movie_enriched['item']['description'], "This movie doesn't exist in our database")  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test enriching items with multiple scenarios.'
raw_items = [{'media_id': '238', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Test Movie', 'image': 'http://example.com/movie.jpg', 'release_date': '2023-01-01', 'rating': 8.5, 'genre': 'Action'}, {'media_id': '67890', 'source': Sources.TMDB.value, 'media_type': MediaTypes.SEASON.value, 'title': 'Test TV Show', 'season_title': 'Season 1', 'season_number': 1, 'image': 'http://example.com/show.jpg'}, {'media_id': '99999', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Unknown Movie', 'image': 'http://example.com/unknown.jpg', 'description': "This movie doesn't exist in our database"}]
enriched_items = enrich_items_with_user_data(self.request, raw_items, 'test')
self.assertEqual(len(enriched_items), 3)
movie_enriched = enriched_items[0]
self.assertEqual(movie_enriched['media'], self.movie_media)
self.assertEqual(movie_enriched['item']['title'], 'Test Movie')
self.assertEqual(movie_enriched['item']['media_id'], '238')
self.assertEqual(movie_enriched['item']['release_date'], '2023-01-01')
self.assertEqual(movie_enriched['item']['rating'], 8.5)
self.assertEqual(movie_enriched['item']['genre'], 'Action')
season_enriched = enriched_items[1]
self.assertEqual(season_enriched['media'], None)
self.assertEqual(season_enriched['item']['season_title'], 'Season 1')
self.assertEqual(season_enriched['item']['season_number'], 1)
unknown_movie_enriched = enriched_items[2]
self.assertEqual(unknown_movie_enriched['item']['media_id'], raw_items[2]['media_id'])
self.assertEqual(unknown_movie_enriched['media'], None)
self.assertEqual(unknown_movie_enriched['item']['title'], 'Unknown Movie')
self.assertEqual(unknown_movie_enriched['item']['media_id'], '99999')
self.assertEqual(unknown_movie_enriched['item']['description'], "This movie doesn't exist in our database")
```

*Source: C:\yamtrack-fork\src\app\tests\test_helpers.py:159*

### test_hide_completed_recommendations_enabled

**Category**: workflow  
**Description**: Workflow: Test that completed items are hidden when preference is enabled.  
**Expected**: self.assertEqual(enriched_items[0]['item']['media_id'], '99999')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test that completed items are hidden when preference is enabled.'
self.user.hide_completed_recommendations = True
self.user.save()
raw_items = [{'media_id': '238', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Test Movie', 'image': 'http://example.com/movie.jpg'}, {'media_id': '99999', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Unknown Movie', 'image': 'http://example.com/unknown.jpg'}]
enriched_items = enrich_items_with_user_data(self.request, raw_items, 'recommendations')
self.assertEqual(len(enriched_items), 1)
self.assertEqual(enriched_items[0]['item']['media_id'], '99999')
```

*Source: C:\yamtrack-fork\src\app\tests\test_helpers.py:233*

### test_hide_completed_recommendations_disabled

**Category**: workflow  
**Description**: Workflow: Test that completed items are shown when preference is disabled.  
**Expected**: self.assertEqual(len(enriched_items), 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test that completed items are shown when preference is disabled.'
self.user.hide_completed_recommendations = False
self.user.save()
raw_items = [{'media_id': '238', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Test Movie', 'image': 'http://example.com/movie.jpg'}, {'media_id': '99999', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'title': 'Unknown Movie', 'image': 'http://example.com/unknown.jpg'}]
enriched_items = enrich_items_with_user_data(self.request, raw_items, 'recommendations')
self.assertEqual(len(enriched_items), 2)
```

*Source: C:\yamtrack-fork\src\app\tests\test_helpers.py:262*

### test_is_released_date_with_full_date

**Category**: workflow  
**Description**: Workflow: Test is_released_date with YYYY-MM-DD string format.  
**Expected**: self.assertFalse(is_released_date(future_date_str))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test is_released_date with YYYY-MM-DD string format.'
past_date_str = '2020-05-15'
self.assertTrue(is_released_date(past_date_str))
future_date_str = '2099-12-31'
self.assertFalse(is_released_date(future_date_str))
```

*Source: C:\yamtrack-fork\src\app\tests\test_helpers.py:334*

### test_is_released_date_with_custom_current_date

**Category**: workflow  
**Description**: Workflow: Test is_released_date with explicit current_date parameter.  
**Expected**: self.assertTrue(is_released_date(test_date, current_date))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test is_released_date with explicit current_date parameter.'
test_date = date(2020, 5, 15)
current_date = date(2020, 5, 20)
self.assertTrue(is_released_date(test_date, current_date))
current_date = date(2020, 5, 10)
self.assertFalse(is_released_date(test_date, current_date))
current_date = date(2020, 5, 15)
self.assertTrue(is_released_date(test_date, current_date))
```

*Source: C:\yamtrack-fork\src\app\tests\test_helpers.py:358*

### test_export_csv

**Category**: workflow  
**Description**: Workflow: Basic test exporting media to CSV.  
**Expected**: self.assertEqual(response['Content-Type'], 'text/csv')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create necessary data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.client.login(**self.credentials)
item_movie = Item.objects.create(media_id='10494', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Perfect Blue', image='https://image.url')
Movie.objects.create(item=item_movie, user=self.user, score=9, status=Status.COMPLETED.value, notes='Nice', start_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC), end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='https://image.url', season_number=1)
season = Season.objects.create(item=item_season, user=self.user, score=9, status=Status.IN_PROGRESS.value, notes='Nice')
item_episode = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='https://image.url', season_number=1, episode_number=1)
Episode.objects.create(item=item_episode, related_season=season, end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_anime = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='https://image.url')
Anime.objects.create(item=item_anime, user=self.user, status=Status.IN_PROGRESS.value, progress=2, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_manga = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='https://image.url')
Manga.objects.create(item=item_manga, user=self.user, status=Status.IN_PROGRESS.value, progress=2, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_game = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Witcher 3: Wild Hunt', image='https://image.url')
Game.objects.create(item=item_game, user=self.user, status=Status.IN_PROGRESS.value, progress=120, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_book = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='Fantastic Mr. Fox', image='https://image.url')
Book.objects.create(item=item_book, user=self.user, status=Status.IN_PROGRESS.value, progress=120, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))

'Basic test exporting media to CSV.'
response = self.client.get(reverse('export_csv'))
self.assertEqual(response.status_code, 200)
self.assertEqual(response['Content-Type'], 'text/csv')
content = b''.join(response.streaming_content).decode('utf-8')
reader = csv.DictReader(StringIO(content))
db_media_ids = set(Item.objects.filter(Q(tv__user=self.user) | Q(movie__user=self.user) | Q(season__user=self.user) | Q(episode__related_season__user=self.user) | Q(anime__user=self.user) | Q(manga__user=self.user) | Q(game__user=self.user) | Q(book__user=self.user)).values_list('media_id', flat=True))
for row in reader:
    media_id = row['media_id']
    self.assertIn(media_id, db_media_ids)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_exports.py:143*

### test_export_csv

**Category**: workflow  
**Description**: Workflow: Basic test exporting media to CSV.  
**Expected**: self.assertEqual(response['Content-Type'], 'text/csv')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Basic test exporting media to CSV.'
response = self.client.get(reverse('export_csv'))
self.assertEqual(response.status_code, 200)
self.assertEqual(response['Content-Type'], 'text/csv')
content = b''.join(response.streaming_content).decode('utf-8')
reader = csv.DictReader(StringIO(content))
db_media_ids = set(Item.objects.filter(Q(tv__user=self.user) | Q(movie__user=self.user) | Q(season__user=self.user) | Q(episode__related_season__user=self.user) | Q(anime__user=self.user) | Q(manga__user=self.user) | Q(game__user=self.user) | Q(book__user=self.user)).values_list('media_id', flat=True))
for row in reader:
    media_id = row['media_id']
    self.assertIn(media_id, db_media_ids)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_exports.py:143*

### test_sidebar_post_update_preferences

**Category**: workflow  
**Description**: Workflow: Test POST request to update preferences.  
**Expected**: self.assertIn('Settings updated', str(messages[0]))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create user for the tests.'
self.watch_regions_patcher = patch('users.views.tmdb.watch_provider_regions', return_value=[('UNSET', 'Disabled'), ('US', 'United States')])
self.watch_regions_patcher.start()
self.addCleanup(self.watch_regions_patcher.stop)
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

'Test POST request to update preferences.'
self.user.tv_enabled = True
self.user.movie_enabled = True
self.user.anime_enabled = True
self.user.save()
response = self.client.post(reverse('preferences'), {'media_types_checkboxes': [MediaTypes.TV.value, MediaTypes.ANIME.value]})
self.assertRedirects(response, reverse('preferences'))
self.user.refresh_from_db()
self.assertTrue(self.user.tv_enabled)
self.assertFalse(self.user.movie_enabled)
self.assertTrue(self.user.anime_enabled)
messages = list(get_messages(response.wsgi_request))
self.assertEqual(len(messages), 1)
self.assertIn('Settings updated', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_sidebar.py:38*

### test_sidebar_post_demo_user

**Category**: workflow  
**Description**: Workflow: Test POST request from a demo user to preferences.  
**Expected**: self.assertIn('view-only for demo accounts', str(messages[0]))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create user for the tests.'
self.watch_regions_patcher = patch('users.views.tmdb.watch_provider_regions', return_value=[('UNSET', 'Disabled'), ('US', 'United States')])
self.watch_regions_patcher.start()
self.addCleanup(self.watch_regions_patcher.stop)
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

'Test POST request from a demo user to preferences.'
self.user.is_demo = True
self.user.tv_enabled = True
self.user.movie_enabled = False
self.user.save()
response = self.client.post(reverse('preferences'), {'media_types_checkboxes': [MediaTypes.TV.value, MediaTypes.MOVIE.value]})
self.assertRedirects(response, reverse('preferences'))
self.user.refresh_from_db()
self.assertTrue(self.user.tv_enabled)
self.assertFalse(self.user.movie_enabled)
messages = list(get_messages(response.wsgi_request))
self.assertEqual(len(messages), 1)
self.assertIn('view-only for demo accounts', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_sidebar.py:62*

### test_obfuscate_unseen_episodes_post_demo_user

**Category**: workflow  
**Description**: Workflow: Test that demo users cannot update obfuscate_unseen_episodes.  
**Expected**: self.assertIn('view-only for demo accounts', str(messages[0]))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create user for the tests.'
self.watch_regions_patcher = patch('users.views.tmdb.watch_provider_regions', return_value=[('UNSET', 'Disabled'), ('US', 'United States')])
self.watch_regions_patcher.start()
self.addCleanup(self.watch_regions_patcher.stop)
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

'Test that demo users cannot update obfuscate_unseen_episodes.'
self.user.is_demo = True
self.user.obfuscate_unseen_episodes = False
self.user.save()
response = self.client.post(reverse('preferences'), {'obfuscate_unseen_episodes': 'on', 'media_types_checkboxes': [MediaTypes.TV.value]})
self.assertRedirects(response, reverse('preferences'))
self.user.refresh_from_db()
self.assertFalse(self.user.obfuscate_unseen_episodes)
messages = list(get_messages(response.wsgi_request))
self.assertEqual(len(messages), 1)
self.assertIn('view-only for demo accounts', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_sidebar.py:146*

### test_sidebar_post_update_preferences

**Category**: workflow  
**Description**: Workflow: Test POST request to update preferences.  
**Expected**: self.assertIn('Settings updated', str(messages[0]))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test POST request to update preferences.'
self.user.tv_enabled = True
self.user.movie_enabled = True
self.user.anime_enabled = True
self.user.save()
response = self.client.post(reverse('preferences'), {'media_types_checkboxes': [MediaTypes.TV.value, MediaTypes.ANIME.value]})
self.assertRedirects(response, reverse('preferences'))
self.user.refresh_from_db()
self.assertTrue(self.user.tv_enabled)
self.assertFalse(self.user.movie_enabled)
self.assertTrue(self.user.anime_enabled)
messages = list(get_messages(response.wsgi_request))
self.assertEqual(len(messages), 1)
self.assertIn('Settings updated', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_sidebar.py:38*

### test_sidebar_post_demo_user

**Category**: workflow  
**Description**: Workflow: Test POST request from a demo user to preferences.  
**Expected**: self.assertIn('view-only for demo accounts', str(messages[0]))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test POST request from a demo user to preferences.'
self.user.is_demo = True
self.user.tv_enabled = True
self.user.movie_enabled = False
self.user.save()
response = self.client.post(reverse('preferences'), {'media_types_checkboxes': [MediaTypes.TV.value, MediaTypes.MOVIE.value]})
self.assertRedirects(response, reverse('preferences'))
self.user.refresh_from_db()
self.assertTrue(self.user.tv_enabled)
self.assertFalse(self.user.movie_enabled)
messages = list(get_messages(response.wsgi_request))
self.assertEqual(len(messages), 1)
self.assertIn('view-only for demo accounts', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_sidebar.py:62*

### test_obfuscate_unseen_episodes_post_demo_user

**Category**: workflow  
**Description**: Workflow: Test that demo users cannot update obfuscate_unseen_episodes.  
**Expected**: self.assertIn('view-only for demo accounts', str(messages[0]))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test that demo users cannot update obfuscate_unseen_episodes.'
self.user.is_demo = True
self.user.obfuscate_unseen_episodes = False
self.user.save()
response = self.client.post(reverse('preferences'), {'obfuscate_unseen_episodes': 'on', 'media_types_checkboxes': [MediaTypes.TV.value]})
self.assertRedirects(response, reverse('preferences'))
self.user.refresh_from_db()
self.assertFalse(self.user.obfuscate_unseen_episodes)
messages = list(get_messages(response.wsgi_request))
self.assertEqual(len(messages), 1)
self.assertIn('view-only for demo accounts', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_sidebar.py:146*

### test_get_import_tasks_schedules

**Category**: workflow  
**Description**: Workflow: Test get_import_tasks returns correct scheduled tasks.  
**Expected**: self.assertEqual(import_tasks['schedules'][1]['username'], 'testuser')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.credentials_other = {'username': 'otheruser', 'password': '12345'}
self.other_user = get_user_model().objects.create_user(**self.credentials_other)
self.crontab = CrontabSchedule.objects.create(minute='0', hour='0', day_of_week='*', day_of_month='*', month_of_year='*')

'Test get_import_tasks returns correct scheduled tasks.'
mock_get_next_run_info.return_value = {'next_run': timezone.now() + timedelta(days=1), 'frequency': 'Daily at midnight', 'mode': 'overwrite'}
periodic_task1 = PeriodicTask.objects.create(name='Import from Trakt for testuser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
periodic_task2 = PeriodicTask.objects.create(name='Import from AniList for testuser at weekly', task='Import from AniList', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
PeriodicTask.objects.create(name='Import from SIMKL for testuser at daily', task='Import from SIMKL', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=False)
PeriodicTask.objects.create(name='Import from Trakt for otheruser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.other_user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
import_tasks = self.user.get_import_tasks()
self.assertEqual(len(import_tasks['schedules']), 2)
self.assertEqual(import_tasks['schedules'][0]['task'], periodic_task1)
self.assertEqual(import_tasks['schedules'][0]['source'], 'trakt')
self.assertEqual(import_tasks['schedules'][0]['username'], 'testuser')
self.assertEqual(import_tasks['schedules'][0]['schedule'], 'Daily at midnight')
self.assertEqual(import_tasks['schedules'][1]['task'], periodic_task2)
self.assertEqual(import_tasks['schedules'][1]['source'], 'anilist')
self.assertEqual(import_tasks['schedules'][1]['username'], 'testuser')
```

*Source: C:\yamtrack-fork\src\users\tests\test_models.py:269*

### test_get_import_tasks_schedules

**Category**: workflow  
**Description**: Workflow: Test get_import_tasks returns correct scheduled tasks.  
**Expected**: self.assertEqual(import_tasks['schedules'][1]['username'], 'testuser')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_next_run_info

'Test get_import_tasks returns correct scheduled tasks.'
mock_get_next_run_info.return_value = {'next_run': timezone.now() + timedelta(days=1), 'frequency': 'Daily at midnight', 'mode': 'overwrite'}
periodic_task1 = PeriodicTask.objects.create(name='Import from Trakt for testuser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
periodic_task2 = PeriodicTask.objects.create(name='Import from AniList for testuser at weekly', task='Import from AniList', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
PeriodicTask.objects.create(name='Import from SIMKL for testuser at daily', task='Import from SIMKL', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=False)
PeriodicTask.objects.create(name='Import from Trakt for otheruser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.other_user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
import_tasks = self.user.get_import_tasks()
self.assertEqual(len(import_tasks['schedules']), 2)
self.assertEqual(import_tasks['schedules'][0]['task'], periodic_task1)
self.assertEqual(import_tasks['schedules'][0]['source'], 'trakt')
self.assertEqual(import_tasks['schedules'][0]['username'], 'testuser')
self.assertEqual(import_tasks['schedules'][0]['schedule'], 'Daily at midnight')
self.assertEqual(import_tasks['schedules'][1]['task'], periodic_task2)
self.assertEqual(import_tasks['schedules'][1]['source'], 'anilist')
self.assertEqual(import_tasks['schedules'][1]['username'], 'testuser')
```

*Source: C:\yamtrack-fork\src\users\tests\test_models.py:269*

### test_lists_view_sorting

**Category**: workflow  
**Description**: Workflow: Test the lists view with different sorting options.  
**Expected**: self.assertEqual(response.context['current_sort'], 'last_item_added')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Set up test data for lists view tests.'
self.factory = RequestFactory()
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.collaborator_credentials = {'username': 'collaborator', 'password': '12345'}
self.collaborator = get_user_model().objects.create_user(**self.collaborator_credentials)
self.list1 = CustomList.objects.create(name='Test List 1', description='Description 1', owner=self.user)
self.list2 = CustomList.objects.create(name='Test List 2', description='Description 2', owner=self.user)
self.list1.collaborators.add(self.collaborator)
self.item1 = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.item2 = Item.objects.create(media_id='2', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
CustomListItem.objects.create(custom_list=self.list1, item=self.item1)
CustomListItem.objects.create(custom_list=self.list2, item=self.item2)

'Test the lists view with different sorting options.'
self.client.login(**self.credentials)
mock_update_preference.return_value = 'name'
response = self.client.get(reverse('lists') + '?sort=name')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'name')
mock_update_preference.return_value = 'items_count'
response = self.client.get(reverse('lists') + '?sort=items_count')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'items_count')
mock_update_preference.return_value = 'newest_first'
response = self.client.get(reverse('lists') + '?sort=newest_first')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'newest_first')
mock_update_preference.return_value = 'last_item_added'
response = self.client.get(reverse('lists'))
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'last_item_added')
```

*Source: C:\yamtrack-fork\src\lists\tests\test_views.py:104*

### test_list_detail_view_sorting

**Category**: workflow  
**Description**: Workflow: Test the list_detail view with different sorting options.  
**Expected**: self.assertEqual(response.context['current_sort'], 'media_type')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Set up test data.'
self.factory = RequestFactory()
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.other_credentials = {'username': 'otheruser', 'password': 'testpassword'}
self.other_user = get_user_model().objects.create_user(**self.other_credentials)
self.client.login(**self.credentials)
self.custom_list = CustomList.objects.create(name='Test List', description='Test Description', owner=self.user)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime')
CustomListItem.objects.create(custom_list=self.custom_list, item=self.movie_item)
CustomListItem.objects.create(custom_list=self.custom_list, item=self.tv_item)
CustomListItem.objects.create(custom_list=self.custom_list, item=self.anime_item)

'Test the list_detail view with different sorting options.'
mock_user_can_view.return_value = True
Movie.objects.create(item=self.movie_item, status=Status.COMPLETED.value, user=self.user)
TV.objects.create(item=self.tv_item, status=Status.IN_PROGRESS.value, user=self.user)
Anime.objects.create(item=self.anime_item, status=Status.PLANNING.value, user=self.user)
mock_update_preference.side_effect = ['title', None]
response = self.client.get(reverse('list_detail', args=[self.custom_list.id]) + '?sort=title')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'title')
mock_update_preference.side_effect = ['media_type', None]
response = self.client.get(reverse('list_detail', args=[self.custom_list.id]) + '?sort=media_type')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'media_type')
```

*Source: C:\yamtrack-fork\src\lists\tests\test_views.py:420*

### test_lists_modal_view_with_new_item

**Category**: workflow  
**Description**: Workflow: Test the lists_modal view with a new item.  
**Expected**: self.assertEqual(new_item.image, 'http://example.com/new_image.jpg')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Set up test data.'
self.client = Client()
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.list1 = CustomList.objects.create(name='Test List 1', owner=self.user)
self.list2 = CustomList.objects.create(name='Test List 2', owner=self.user)

'Test the lists_modal view with a new item.'
mock_get_lists.return_value = [self.list1, self.list2]
mock_get_metadata.return_value = {'title': 'New Movie', 'image': 'http://example.com/new_image.jpg'}
response = self.client.get(reverse('lists_modal', args=[Sources.TMDB.value, MediaTypes.MOVIE.value, '999']))
self.assertEqual(response.status_code, 200)
self.assertTrue(Item.objects.filter(media_id='999', source=Sources.TMDB.value).exists())
new_item = Item.objects.get(media_id='999', source=Sources.TMDB.value)
self.assertEqual(new_item.title, 'New Movie')
self.assertEqual(new_item.image, 'http://example.com/new_image.jpg')
```

*Source: C:\yamtrack-fork\src\lists\tests\test_views.py:684*

### test_lists_view_sorting

**Category**: workflow  
**Description**: Workflow: Test the lists view with different sorting options.  
**Expected**: self.assertEqual(response.context['current_sort'], 'last_item_added')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_update_preference

'Test the lists view with different sorting options.'
self.client.login(**self.credentials)
mock_update_preference.return_value = 'name'
response = self.client.get(reverse('lists') + '?sort=name')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'name')
mock_update_preference.return_value = 'items_count'
response = self.client.get(reverse('lists') + '?sort=items_count')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'items_count')
mock_update_preference.return_value = 'newest_first'
response = self.client.get(reverse('lists') + '?sort=newest_first')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'newest_first')
mock_update_preference.return_value = 'last_item_added'
response = self.client.get(reverse('lists'))
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'last_item_added')
```

*Source: C:\yamtrack-fork\src\lists\tests\test_views.py:104*

### test_list_detail_view_sorting

**Category**: workflow  
**Description**: Workflow: Test the list_detail view with different sorting options.  
**Expected**: self.assertEqual(response.context['current_sort'], 'media_type')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_user_can_view, mock_update_preference

'Test the list_detail view with different sorting options.'
mock_user_can_view.return_value = True
Movie.objects.create(item=self.movie_item, status=Status.COMPLETED.value, user=self.user)
TV.objects.create(item=self.tv_item, status=Status.IN_PROGRESS.value, user=self.user)
Anime.objects.create(item=self.anime_item, status=Status.PLANNING.value, user=self.user)
mock_update_preference.side_effect = ['title', None]
response = self.client.get(reverse('list_detail', args=[self.custom_list.id]) + '?sort=title')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'title')
mock_update_preference.side_effect = ['media_type', None]
response = self.client.get(reverse('list_detail', args=[self.custom_list.id]) + '?sort=media_type')
self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_sort'], 'media_type')
```

*Source: C:\yamtrack-fork\src\lists\tests\test_views.py:420*

### test_lists_modal_view_with_new_item

**Category**: workflow  
**Description**: Workflow: Test the lists_modal view with a new item.  
**Expected**: self.assertEqual(new_item.image, 'http://example.com/new_image.jpg')  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_lists, mock_get_metadata

'Test the lists_modal view with a new item.'
mock_get_lists.return_value = [self.list1, self.list2]
mock_get_metadata.return_value = {'title': 'New Movie', 'image': 'http://example.com/new_image.jpg'}
response = self.client.get(reverse('lists_modal', args=[Sources.TMDB.value, MediaTypes.MOVIE.value, '999']))
self.assertEqual(response.status_code, 200)
self.assertTrue(Item.objects.filter(media_id='999', source=Sources.TMDB.value).exists())
new_item = Item.objects.get(media_id='999', source=Sources.TMDB.value)
self.assertEqual(new_item.title, 'New Movie')
self.assertEqual(new_item.image, 'http://example.com/new_image.jpg')
```

*Source: C:\yamtrack-fork\src\lists\tests\test_views.py:684*

### test_statistics_view_invalid_date_format

**Category**: workflow  
**Description**: Workflow: Test the statistics view with invalid date format.  
**Expected**: self.assertTrue(date_is_none)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

'Test the statistics view with invalid date format.'
start_date = '01/01/2023'
end_date = '2023/12/31'
response = self.client.get(reverse('statistics') + f'?start-date={start_date}&end-date={end_date}')
self.assertEqual(response.status_code, 200)
date_is_none = response.context['start_date'] is None and response.context['end_date'] is None
self.assertTrue(date_is_none)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_statistics.py:53*

### test_statistics_view_invalid_date_format

**Category**: workflow  
**Description**: Workflow: Test the statistics view with invalid date format.  
**Expected**: self.assertTrue(date_is_none)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the statistics view with invalid date format.'
start_date = '01/01/2023'
end_date = '2023/12/31'
response = self.client.get(reverse('statistics') + f'?start-date={start_date}&end-date={end_date}')
self.assertEqual(response.status_code, 200)
date_is_none = response.context['start_date'] is None and response.context['end_date'] is None
self.assertTrue(date_is_none)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_statistics.py:53*

### test_import_steam_games

**Category**: workflow  
**Description**: Workflow: Test importing games from Steam.  
**Expected**: self.assertEqual(tf2_game.progress, 500)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

'Test importing games from Steam.'
mock_api_request.return_value = {'response': {'games': [{'appid': 730, 'name': 'Counter-Strike 2', 'playtime_forever': 1250, 'playtime_2weeks': 120, 'rtime_last_played': 1704067200}, {'appid': 570, 'name': 'Dota 2', 'playtime_forever': 0, 'playtime_2weeks': 0}, {'appid': 440, 'name': 'Team Fortress 2', 'playtime_forever': 500, 'playtime_2weeks': 0, 'rtime_last_played': 1672531200}]}}
mock_external_game.side_effect = [1, 2, 3]
mock_get_metadata.side_effect = [{'title': 'Counter-Strike 2', 'image': 'http://example.com/cs2.jpg'}, {'title': 'Dota 2', 'image': 'http://example.com/dota2.jpg'}, {'title': 'Team Fortress 2', 'image': 'http://example.com/tf2.jpg'}]
imported_counts, _ = steam.importer('76561198000000000', self.user, 'new')
self.assertEqual(imported_counts[MediaTypes.GAME.value], 3)
games = Game.objects.filter(user=self.user)
self.assertEqual(games.count(), 3)
cs2_game = games.get(item__title='Counter-Strike 2')
self.assertEqual(cs2_game.status, Status.IN_PROGRESS.value)
self.assertEqual(cs2_game.progress, 1250)
dota_game = games.get(item__title='Dota 2')
self.assertEqual(dota_game.status, Status.PLANNING.value)
self.assertEqual(dota_game.progress, 0)
tf2_game = games.get(item__title='Team Fortress 2')
self.assertEqual(tf2_game.status, Status.PAUSED.value)
self.assertEqual(tf2_game.progress, 500)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_steam.py:38*

### test_determine_game_status_logic

**Category**: workflow  
**Description**: Workflow: Test the status determination logic.  
**Expected**: self.assertEqual(status, Status.PAUSED.value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

'Test the status determination logic.'
importer_instance = steam.SteamImporter('76561198000000000', self.user, 'new')
status = importer_instance._determine_game_status(0, 0)
self.assertEqual(status, Status.PLANNING.value)
status = importer_instance._determine_game_status(100, 50)
self.assertEqual(status, Status.IN_PROGRESS.value)
status = importer_instance._determine_game_status(100, 0)
self.assertEqual(status, Status.PAUSED.value)
status = importer_instance._determine_game_status(100, 0)
self.assertEqual(status, Status.PAUSED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_steam.py:151*

### test_import_steam_games

**Category**: workflow  
**Description**: Workflow: Test importing games from Steam.  
**Expected**: self.assertEqual(tf2_game.progress, 500)  
**Confidence**: 0.90  
**Tags**: mock, workflow, integration  

```python
# Setup
# Fixtures: mock_get_metadata, mock_external_game, mock_api_request

'Test importing games from Steam.'
mock_api_request.return_value = {'response': {'games': [{'appid': 730, 'name': 'Counter-Strike 2', 'playtime_forever': 1250, 'playtime_2weeks': 120, 'rtime_last_played': 1704067200}, {'appid': 570, 'name': 'Dota 2', 'playtime_forever': 0, 'playtime_2weeks': 0}, {'appid': 440, 'name': 'Team Fortress 2', 'playtime_forever': 500, 'playtime_2weeks': 0, 'rtime_last_played': 1672531200}]}}
mock_external_game.side_effect = [1, 2, 3]
mock_get_metadata.side_effect = [{'title': 'Counter-Strike 2', 'image': 'http://example.com/cs2.jpg'}, {'title': 'Dota 2', 'image': 'http://example.com/dota2.jpg'}, {'title': 'Team Fortress 2', 'image': 'http://example.com/tf2.jpg'}]
imported_counts, _ = steam.importer('76561198000000000', self.user, 'new')
self.assertEqual(imported_counts[MediaTypes.GAME.value], 3)
games = Game.objects.filter(user=self.user)
self.assertEqual(games.count(), 3)
cs2_game = games.get(item__title='Counter-Strike 2')
self.assertEqual(cs2_game.status, Status.IN_PROGRESS.value)
self.assertEqual(cs2_game.progress, 1250)
dota_game = games.get(item__title='Dota 2')
self.assertEqual(dota_game.status, Status.PLANNING.value)
self.assertEqual(dota_game.progress, 0)
tf2_game = games.get(item__title='Team Fortress 2')
self.assertEqual(tf2_game.status, Status.PAUSED.value)
self.assertEqual(tf2_game.progress, 500)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_steam.py:38*

### test_determine_game_status_logic

**Category**: workflow  
**Description**: Workflow: Test the status determination logic.  
**Expected**: self.assertEqual(status, Status.PAUSED.value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test the status determination logic.'
importer_instance = steam.SteamImporter('76561198000000000', self.user, 'new')
status = importer_instance._determine_game_status(0, 0)
self.assertEqual(status, Status.PLANNING.value)
status = importer_instance._determine_game_status(100, 50)
self.assertEqual(status, Status.IN_PROGRESS.value)
status = importer_instance._determine_game_status(100, 0)
self.assertEqual(status, Status.PAUSED.value)
status = importer_instance._determine_game_status(100, 0)
self.assertEqual(status, Status.PAUSED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_steam.py:151*

### test_overwrite_steam_game_updates_existing

**Category**: method_call  
**Description**: Test overwrite mode updates an existing game instead of recreating it.  
**Expected**: self.assertEqual(imported_counts[MediaTypes.GAME.value], 1)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user and common data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Counter-Strike 2', image='http://example.com/cs2.jpg')

game.refresh_from_db()
self.assertEqual(imported_counts[MediaTypes.GAME.value], 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_steam_update.py:83*

### test_overwrite_steam_game_updates_existing

**Category**: method_call  
**Description**: Test overwrite mode updates an existing game instead of recreating it.  
**Expected**: self.assertEqual(Game.objects.filter(user=self.user).count(), 1)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user and common data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Counter-Strike 2', image='http://example.com/cs2.jpg')

self.assertEqual(imported_counts[MediaTypes.GAME.value], 1)
self.assertEqual(Game.objects.filter(user=self.user).count(), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_steam_update.py:84*

### test_overwrite_steam_game_updates_existing

**Category**: method_call  
**Description**: Test overwrite mode updates an existing game instead of recreating it.  
**Expected**: self.assertEqual(game.progress, 1300)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user and common data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Counter-Strike 2', image='http://example.com/cs2.jpg')

self.assertEqual(Game.objects.filter(user=self.user).count(), 1)
self.assertEqual(game.progress, 1300)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_steam_update.py:85*

### test_overwrite_steam_game_updates_existing

**Category**: method_call  
**Description**: Test overwrite mode updates an existing game instead of recreating it.  
**Expected**: self.assertEqual(game.status, Status.IN_PROGRESS.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user and common data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Counter-Strike 2', image='http://example.com/cs2.jpg')

self.assertEqual(game.progress, 1300)
self.assertEqual(game.status, Status.IN_PROGRESS.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_steam_update.py:86*

### test_overwrite_steam_game_updates_existing

**Category**: method_call  
**Description**: Test overwrite mode updates an existing game instead of recreating it.  
**Expected**: self.assertEqual(game.history.count(), 2)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user and common data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Counter-Strike 2', image='http://example.com/cs2.jpg')

self.assertEqual(game.status, Status.IN_PROGRESS.value)
self.assertEqual(game.history.count(), 2)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_steam_update.py:87*

### test_overwrite_steam_game_completed_status

**Category**: method_call  
**Description**: Test overwrite mode does not downgrade completed games.  
**Expected**: self.assertEqual(imported_counts[MediaTypes.GAME.value], 1)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user and common data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Counter-Strike 2', image='http://example.com/cs2.jpg')

game.refresh_from_db()
self.assertEqual(imported_counts[MediaTypes.GAME.value], 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_steam_update.py:111*

### test_overwrite_steam_game_completed_status

**Category**: method_call  
**Description**: Test overwrite mode does not downgrade completed games.  
**Expected**: self.assertEqual(game.progress, 1100)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user and common data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Counter-Strike 2', image='http://example.com/cs2.jpg')

self.assertEqual(imported_counts[MediaTypes.GAME.value], 1)
self.assertEqual(game.progress, 1100)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_steam_update.py:112*

### test_overwrite_steam_game_completed_status

**Category**: method_call  
**Description**: Test overwrite mode does not downgrade completed games.  
**Expected**: self.assertEqual(game.status, Status.COMPLETED.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user and common data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Counter-Strike 2', image='http://example.com/cs2.jpg')

self.assertEqual(game.progress, 1100)
self.assertEqual(game.status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_steam_update.py:113*

### test_increase_progress

**Category**: method_call  
**Description**: Test increasing the progress of a game.  
**Expected**: self.assertEqual(self.game.progress, initial_progress + 30)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for Game model tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, progress=60)

self.game.increase_progress()
self.assertEqual(self.game.progress, initial_progress + 30)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_game.py:43*

### test_decrease_progress

**Category**: method_call  
**Description**: Test decreasing the progress of a game.  
**Expected**: self.assertEqual(self.game.progress, initial_progress - 30)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for Game model tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, progress=60)

self.game.decrease_progress()
self.assertEqual(self.game.progress, initial_progress - 30)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_game.py:50*

### test_field_tracker

**Category**: method_call  
**Description**: Test that the field tracker is tracking changes.  
**Expected**: self.assertEqual(self.game.tracker.previous('progress'), 60)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for Game model tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, progress=60)

self.assertTrue(self.game.tracker.changed())
self.assertEqual(self.game.tracker.previous('progress'), 60)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_game.py:63*

### test_multiple_progress_changes

**Category**: method_call  
**Description**: Test multiple progress changes.  
**Expected**: self.assertEqual(self.game.progress, 120)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for Game model tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, progress=60)

self.game.increase_progress()
self.assertEqual(self.game.progress, 120)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_game.py:70*

### test_multiple_progress_changes

**Category**: method_call  
**Description**: Test multiple progress changes.  
**Expected**: self.assertEqual(self.game.progress, 90)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for Game model tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.game_item = Item.objects.create(media_id='1234', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Last of Us', image='http://example.com/tlou.jpg')
self.game = Game.objects.create(item=self.game_item, user=self.user, status=Status.IN_PROGRESS.value, progress=60)

self.game.decrease_progress()
self.assertEqual(self.game.progress, 90)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_game.py:75*

### test_increase_progress

**Category**: method_call  
**Description**: Test increasing the progress of a game.  
**Expected**: self.assertEqual(self.game.progress, initial_progress + 30)  
**Confidence**: 0.85  

```python
self.game.increase_progress()
self.assertEqual(self.game.progress, initial_progress + 30)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_game.py:43*

### test_decrease_progress

**Category**: method_call  
**Description**: Test decreasing the progress of a game.  
**Expected**: self.assertEqual(self.game.progress, initial_progress - 30)  
**Confidence**: 0.85  

```python
self.game.decrease_progress()
self.assertEqual(self.game.progress, initial_progress - 30)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_game.py:50*

### test_field_tracker

**Category**: method_call  
**Description**: Test that the field tracker is tracking changes.  
**Expected**: self.assertEqual(self.game.tracker.previous('progress'), 60)  
**Confidence**: 0.85  

```python
self.assertTrue(self.game.tracker.changed())
self.assertEqual(self.game.tracker.previous('progress'), 60)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_game.py:63*

### test_multiple_progress_changes

**Category**: method_call  
**Description**: Test multiple progress changes.  
**Expected**: self.assertEqual(self.game.progress, 120)  
**Confidence**: 0.85  

```python
self.game.increase_progress()
self.assertEqual(self.game.progress, 120)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_game.py:70*

### test_multiple_progress_changes

**Category**: method_call  
**Description**: Test multiple progress changes.  
**Expected**: self.assertEqual(self.game.progress, 90)  
**Confidence**: 0.85  

```python
self.game.decrease_progress()
self.assertEqual(self.game.progress, 90)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_game.py:75*

### test_fetch_releases_all_types

**Category**: method_call  
**Description**: Test fetch_releases with all media types.  
**Expected**: self.assertEqual(anime_items[0].id, self.anime_item.id)  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(len(anime_items), 1)
self.assertEqual(anime_items[0].id, self.anime_item.id)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_main.py:70*

### test_fetch_releases_all_types

**Category**: method_call  
**Description**: Test fetch_releases with all media types.  
**Expected**: self.assertTrue(Event.objects.filter(item=self.season_item).exists())  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(anime_items[0].id, self.anime_item.id)
self.assertTrue(Event.objects.filter(item=self.season_item).exists())
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_main.py:71*

### test_fetch_releases_all_types

**Category**: method_call  
**Description**: Test fetch_releases with all media types.  
**Expected**: self.assertEqual(mock_process_other.call_count, 3)  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertTrue(Event.objects.filter(item=self.season_item).exists())
self.assertEqual(mock_process_other.call_count, 3)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_main.py:73*

### test_fetch_releases_all_types

**Category**: method_call  
**Description**: Test fetch_releases with all media types.  
**Expected**: self.assertTrue(Event.objects.filter(item=self.anime_item).exists())  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(mock_process_other.call_count, 3)
self.assertTrue(Event.objects.filter(item=self.anime_item).exists())
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_main.py:74*

### test_fetch_releases_all_types

**Category**: method_call  
**Description**: Test fetch_releases with all media types.  
**Expected**: self.assertTrue(Event.objects.filter(item=self.movie_item).exists())  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertTrue(Event.objects.filter(item=self.anime_item).exists())
self.assertTrue(Event.objects.filter(item=self.movie_item).exists())
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_main.py:76*

### test_fetch_releases_all_types

**Category**: method_call  
**Description**: Test fetch_releases with all media types.  
**Expected**: self.assertTrue(Event.objects.filter(item=self.manga_item).exists())  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertTrue(Event.objects.filter(item=self.movie_item).exists())
self.assertTrue(Event.objects.filter(item=self.manga_item).exists())
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_main.py:77*

### test_get_existing_media_single_movie

**Category**: method_call  
**Description**: Test get_existing_media with single movie tracked.  
**Expected**: self.assertIn(Sources.TMDB.value, existing[MediaTypes.MOVIE.value])  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

self.assertIn(MediaTypes.MOVIE.value, existing)
self.assertIn(Sources.TMDB.value, existing[MediaTypes.MOVIE.value])
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_import_helpers.py:63*

### test_get_existing_media_single_movie

**Category**: method_call  
**Description**: Test get_existing_media with single movie tracked.  
**Expected**: self.assertEqual(existing[MediaTypes.MOVIE.value][Sources.TMDB.value]['238'], movie)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

self.assertIn(Sources.TMDB.value, existing[MediaTypes.MOVIE.value])
self.assertEqual(existing[MediaTypes.MOVIE.value][Sources.TMDB.value]['238'], movie)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_import_helpers.py:64*

### test_get_existing_media_multiple_types

**Category**: method_call  
**Description**: Test get_existing_media with different media types.  
**Expected**: self.assertIn(MediaTypes.TV.value, existing)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

self.assertIn(MediaTypes.MOVIE.value, existing)
self.assertIn(MediaTypes.TV.value, existing)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_import_helpers.py:99*

### test_get_existing_media_multiple_types

**Category**: method_call  
**Description**: Test get_existing_media with different media types.  
**Expected**: self.assertEqual(len(existing[MediaTypes.MOVIE.value][Sources.TMDB.value]), 1)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

self.assertIn(MediaTypes.TV.value, existing)
self.assertEqual(len(existing[MediaTypes.MOVIE.value][Sources.TMDB.value]), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_import_helpers.py:100*

### test_get_existing_media_multiple_types

**Category**: method_call  
**Description**: Test get_existing_media with different media types.  
**Expected**: self.assertEqual(len(existing[MediaTypes.TV.value][Sources.TMDB.value]), 1)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

self.assertEqual(len(existing[MediaTypes.MOVIE.value][Sources.TMDB.value]), 1)
self.assertEqual(len(existing[MediaTypes.TV.value][Sources.TMDB.value]), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_import_helpers.py:101*

### test_get_existing_media_excludes_seasons_episodes

**Category**: method_call  
**Description**: Test get_existing_media excludes season and episode media types.  
**Expected**: self.assertNotIn(MediaTypes.EPISODE.value, existing)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

self.assertNotIn(MediaTypes.SEASON.value, existing)
self.assertNotIn(MediaTypes.EPISODE.value, existing)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_import_helpers.py:109*

### test_progress_increase

**Category**: method_call  
**Description**: Test the increase of progress for a season.  
**Expected**: self.assertEqual(Episode.objects.filter(item__media_id='1668').count(), 2)  
**Confidence**: 0.85  

```python
# Setup
'Prepare the database with a season and an episode.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.item_season, user=self.user, status=Status.IN_PROGRESS.value)
item_ep = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
episode = Episode(item=item_ep, related_season=self.season, end_date=datetime.datetime(2023, 6, 1, 0, 0, tzinfo=datetime.UTC))
Episode.save_base(episode)

self.client.post(reverse('progress_edit', kwargs={'media_type': MediaTypes.SEASON.value, 'instance_id': self.season.id}), {'operation': 'increase'})
self.assertEqual(Episode.objects.filter(item__media_id='1668').count(), 2)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_progress.py:63*

### test_progress_increase

**Category**: method_call  
**Description**: Test the increase of progress for a season.  
**Expected**: self.assertTrue(Episode.objects.filter(item__media_id='1668', item__episode_number=2).exists())  
**Confidence**: 0.85  

```python
# Setup
'Prepare the database with a season and an episode.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.item_season, user=self.user, status=Status.IN_PROGRESS.value)
item_ep = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
episode = Episode(item=item_ep, related_season=self.season, end_date=datetime.datetime(2023, 6, 1, 0, 0, tzinfo=datetime.UTC))
Episode.save_base(episode)

self.assertEqual(Episode.objects.filter(item__media_id='1668').count(), 2)
self.assertTrue(Episode.objects.filter(item__media_id='1668', item__episode_number=2).exists())
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_progress.py:76*

### test_progress_decrease

**Category**: method_call  
**Description**: Test the decrease of progress for a season.  
**Expected**: self.assertEqual(Episode.objects.filter(item__media_id='1668').count(), 0)  
**Confidence**: 0.85  

```python
# Setup
'Prepare the database with a season and an episode.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.item_season, user=self.user, status=Status.IN_PROGRESS.value)
item_ep = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
episode = Episode(item=item_ep, related_season=self.season, end_date=datetime.datetime(2023, 6, 1, 0, 0, tzinfo=datetime.UTC))
Episode.save_base(episode)

self.client.post(reverse('progress_edit', kwargs={'media_type': MediaTypes.SEASON.value, 'instance_id': self.season.id}), {'operation': 'decrease'})
self.assertEqual(Episode.objects.filter(item__media_id='1668').count(), 0)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_progress.py:90*

### test_progress_increase

**Category**: method_call  
**Description**: Test the increase of progress for an anime.  
**Expected**: self.assertEqual(Anime.objects.get(item__media_id='1').progress, 3)  
**Confidence**: 0.85  

```python
# Setup
'Prepare the database with an anime.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/image.jpg')
self.anime = Anime.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=2)

self.client.post(reverse('progress_edit', kwargs={'media_type': MediaTypes.ANIME.value, 'instance_id': self.anime.id}), {'operation': 'increase'})
self.assertEqual(Anime.objects.get(item__media_id='1').progress, 3)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_progress.py:134*

### test_progress_decrease

**Category**: method_call  
**Description**: Test the decrease of progress for an anime.  
**Expected**: self.assertEqual(Anime.objects.get(item__media_id='1').progress, 1)  
**Confidence**: 0.85  

```python
# Setup
'Prepare the database with an anime.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/image.jpg')
self.anime = Anime.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=2)

self.client.post(reverse('progress_edit', kwargs={'media_type': MediaTypes.ANIME.value, 'instance_id': self.anime.id}), {'operation': 'decrease'})
self.assertEqual(Anime.objects.get(item__media_id='1').progress, 1)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_progress.py:151*

### test_progress_edit_htmx_appends_persistent_messages

**Category**: method_call  
**Description**: HTMX progress edits should append newly created persistent toasts.  
**Expected**: self.assertContains(response, 'id="messages-list"')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Prepare a tracked season that completes on the next episode.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Friends', image='http://example.com/image.jpg')
self.tv = TV(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
TV.save_base(self.tv)
season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=season_item, user=self.user, related_tv=self.tv, status=Status.IN_PROGRESS.value)
item_ep = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
episode = Episode(item=item_ep, related_season=self.season, end_date=datetime.datetime(2023, 6, 1, 0, 0, tzinfo=datetime.UTC))
Episode.save_base(episode)

self.assertEqual(response.status_code, 200)
self.assertContains(response, 'id="messages-list"')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_progress.py:255*

### test_progress_edit_htmx_appends_persistent_messages

**Category**: method_call  
**Description**: HTMX progress edits should append newly created persistent toasts.  
**Expected**: self.assertContains(response, 'hx-swap-oob="beforeend"')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Prepare a tracked season that completes on the next episode.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Friends', image='http://example.com/image.jpg')
self.tv = TV(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
TV.save_base(self.tv)
season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=season_item, user=self.user, related_tv=self.tv, status=Status.IN_PROGRESS.value)
item_ep = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
episode = Episode(item=item_ep, related_season=self.season, end_date=datetime.datetime(2023, 6, 1, 0, 0, tzinfo=datetime.UTC))
Episode.save_base(episode)

self.assertContains(response, 'id="messages-list"')
self.assertContains(response, 'hx-swap-oob="beforeend"')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_progress.py:256*

### test_progress_edit_htmx_appends_persistent_messages

**Category**: method_call  
**Description**: HTMX progress edits should append newly created persistent toasts.  
**Expected**: self.assertContains(response, 'Friends S1 was marked as completed automatically.')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Prepare a tracked season that completes on the next episode.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Friends', image='http://example.com/image.jpg')
self.tv = TV(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
TV.save_base(self.tv)
season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=season_item, user=self.user, related_tv=self.tv, status=Status.IN_PROGRESS.value)
item_ep = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
episode = Episode(item=item_ep, related_season=self.season, end_date=datetime.datetime(2023, 6, 1, 0, 0, tzinfo=datetime.UTC))
Episode.save_base(episode)

self.assertContains(response, 'hx-swap-oob="beforeend"')
self.assertContains(response, 'Friends S1 was marked as completed automatically.')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_progress.py:257*

### test_progress_edit_htmx_appends_persistent_messages

**Category**: method_call  
**Description**: HTMX progress edits should append newly created persistent toasts.  
**Expected**: self.assertContains(response, 'Friends was marked as completed automatically.')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Prepare a tracked season that completes on the next episode.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Friends', image='http://example.com/image.jpg')
self.tv = TV(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
TV.save_base(self.tv)
season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=season_item, user=self.user, related_tv=self.tv, status=Status.IN_PROGRESS.value)
item_ep = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
episode = Episode(item=item_ep, related_season=self.season, end_date=datetime.datetime(2023, 6, 1, 0, 0, tzinfo=datetime.UTC))
Episode.save_base(episode)

self.assertContains(response, 'Friends S1 was marked as completed automatically.')
self.assertContains(response, 'Friends was marked as completed automatically.')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_progress.py:258*

### test_progress_edit_htmx_appends_persistent_messages

**Category**: method_call  
**Description**: HTMX progress edits should append newly created persistent toasts.  
**Expected**: self.assertContains(response, reverse('mark_user_messages_shown'))  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Prepare a tracked season that completes on the next episode.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Friends', image='http://example.com/image.jpg')
self.tv = TV(item=tv_item, user=self.user, status=Status.IN_PROGRESS.value)
TV.save_base(self.tv)
season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=season_item, user=self.user, related_tv=self.tv, status=Status.IN_PROGRESS.value)
item_ep = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
episode = Episode(item=item_ep, related_season=self.season, end_date=datetime.datetime(2023, 6, 1, 0, 0, tzinfo=datetime.UTC))
Episode.save_base(episode)

self.assertContains(response, 'Friends was marked as completed automatically.')
self.assertContains(response, reverse('mark_user_messages_shown'))
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_progress.py:262*

### test_custom_list_creation

**Category**: method_call  
**Description**: Test the creation of a CustomList instance.  
**Expected**: self.assertEqual(self.custom_list.description, 'Test Description')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.collaborator_credentials = {'username': 'collaborator', 'password': '12345'}
self.collaborator = get_user_model().objects.create_user(**self.collaborator_credentials)
self.custom_list = CustomList.objects.create(name='Test List', description='Test Description', owner=self.user)
self.custom_list.collaborators.add(self.collaborator)
self.item = Item.objects.create(title='Test Item', media_id='123', media_type=MediaTypes.TV.value, source=Sources.TMDB.value)
self.non_member_credentials = {'username': 'non_member', 'password': '12345'}
self.non_member = get_user_model().objects.create_user(**self.non_member_credentials)

self.assertEqual(self.custom_list.name, 'Test List')
self.assertEqual(self.custom_list.description, 'Test Description')
```

*Source: C:\yamtrack-fork\src\lists\tests\test_models.py:49*

### test_custom_list_creation

**Category**: method_call  
**Description**: Test the creation of a CustomList instance.  
**Expected**: self.assertEqual(self.custom_list.owner, self.user)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.collaborator_credentials = {'username': 'collaborator', 'password': '12345'}
self.collaborator = get_user_model().objects.create_user(**self.collaborator_credentials)
self.custom_list = CustomList.objects.create(name='Test List', description='Test Description', owner=self.user)
self.custom_list.collaborators.add(self.collaborator)
self.item = Item.objects.create(title='Test Item', media_id='123', media_type=MediaTypes.TV.value, source=Sources.TMDB.value)
self.non_member_credentials = {'username': 'non_member', 'password': '12345'}
self.non_member = get_user_model().objects.create_user(**self.non_member_credentials)

self.assertEqual(self.custom_list.description, 'Test Description')
self.assertEqual(self.custom_list.owner, self.user)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_models.py:50*

### test_owner_permissions

**Category**: method_call  
**Description**: Test owner permissions on custom list.  
**Expected**: self.assertTrue(self.custom_list.user_can_edit(self.user))  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.collaborator_credentials = {'username': 'collaborator', 'password': '12345'}
self.collaborator = get_user_model().objects.create_user(**self.collaborator_credentials)
self.custom_list = CustomList.objects.create(name='Test List', description='Test Description', owner=self.user)
self.custom_list.collaborators.add(self.collaborator)
self.item = Item.objects.create(title='Test Item', media_id='123', media_type=MediaTypes.TV.value, source=Sources.TMDB.value)
self.non_member_credentials = {'username': 'non_member', 'password': '12345'}
self.non_member = get_user_model().objects.create_user(**self.non_member_credentials)

self.assertTrue(self.custom_list.user_can_view(self.user))
self.assertTrue(self.custom_list.user_can_edit(self.user))
```

*Source: C:\yamtrack-fork\src\lists\tests\test_models.py:59*

### test_owner_permissions

**Category**: method_call  
**Description**: Test owner permissions on custom list.  
**Expected**: self.assertTrue(self.custom_list.user_can_delete(self.user))  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.collaborator_credentials = {'username': 'collaborator', 'password': '12345'}
self.collaborator = get_user_model().objects.create_user(**self.collaborator_credentials)
self.custom_list = CustomList.objects.create(name='Test List', description='Test Description', owner=self.user)
self.custom_list.collaborators.add(self.collaborator)
self.item = Item.objects.create(title='Test Item', media_id='123', media_type=MediaTypes.TV.value, source=Sources.TMDB.value)
self.non_member_credentials = {'username': 'non_member', 'password': '12345'}
self.non_member = get_user_model().objects.create_user(**self.non_member_credentials)

self.assertTrue(self.custom_list.user_can_edit(self.user))
self.assertTrue(self.custom_list.user_can_delete(self.user))
```

*Source: C:\yamtrack-fork\src\lists\tests\test_models.py:60*

### test_collaborator_permissions

**Category**: method_call  
**Description**: Test collaborator permissions on custom list.  
**Expected**: self.assertTrue(self.custom_list.user_can_edit(self.collaborator))  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.collaborator_credentials = {'username': 'collaborator', 'password': '12345'}
self.collaborator = get_user_model().objects.create_user(**self.collaborator_credentials)
self.custom_list = CustomList.objects.create(name='Test List', description='Test Description', owner=self.user)
self.custom_list.collaborators.add(self.collaborator)
self.item = Item.objects.create(title='Test Item', media_id='123', media_type=MediaTypes.TV.value, source=Sources.TMDB.value)
self.non_member_credentials = {'username': 'non_member', 'password': '12345'}
self.non_member = get_user_model().objects.create_user(**self.non_member_credentials)

self.assertTrue(self.custom_list.user_can_view(self.collaborator))
self.assertTrue(self.custom_list.user_can_edit(self.collaborator))
```

*Source: C:\yamtrack-fork\src\lists\tests\test_models.py:65*

### test_collaborator_permissions

**Category**: method_call  
**Description**: Test collaborator permissions on custom list.  
**Expected**: self.assertFalse(self.custom_list.user_can_delete(self.collaborator))  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.collaborator_credentials = {'username': 'collaborator', 'password': '12345'}
self.collaborator = get_user_model().objects.create_user(**self.collaborator_credentials)
self.custom_list = CustomList.objects.create(name='Test List', description='Test Description', owner=self.user)
self.custom_list.collaborators.add(self.collaborator)
self.item = Item.objects.create(title='Test Item', media_id='123', media_type=MediaTypes.TV.value, source=Sources.TMDB.value)
self.non_member_credentials = {'username': 'non_member', 'password': '12345'}
self.non_member = get_user_model().objects.create_user(**self.non_member_credentials)

self.assertTrue(self.custom_list.user_can_edit(self.collaborator))
self.assertFalse(self.custom_list.user_can_delete(self.collaborator))
```

*Source: C:\yamtrack-fork\src\lists\tests\test_models.py:66*

### test_non_member_permissions

**Category**: method_call  
**Description**: Test non-member permissions on custom list.  
**Expected**: self.assertFalse(self.custom_list.user_can_edit(self.non_member))  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.collaborator_credentials = {'username': 'collaborator', 'password': '12345'}
self.collaborator = get_user_model().objects.create_user(**self.collaborator_credentials)
self.custom_list = CustomList.objects.create(name='Test List', description='Test Description', owner=self.user)
self.custom_list.collaborators.add(self.collaborator)
self.item = Item.objects.create(title='Test Item', media_id='123', media_type=MediaTypes.TV.value, source=Sources.TMDB.value)
self.non_member_credentials = {'username': 'non_member', 'password': '12345'}
self.non_member = get_user_model().objects.create_user(**self.non_member_credentials)

self.assertFalse(self.custom_list.user_can_view(self.non_member))
self.assertFalse(self.custom_list.user_can_edit(self.non_member))
```

*Source: C:\yamtrack-fork\src\lists\tests\test_models.py:71*

### test_non_member_permissions

**Category**: method_call  
**Description**: Test non-member permissions on custom list.  
**Expected**: self.assertFalse(self.custom_list.user_can_delete(self.non_member))  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.collaborator_credentials = {'username': 'collaborator', 'password': '12345'}
self.collaborator = get_user_model().objects.create_user(**self.collaborator_credentials)
self.custom_list = CustomList.objects.create(name='Test List', description='Test Description', owner=self.user)
self.custom_list.collaborators.add(self.collaborator)
self.item = Item.objects.create(title='Test Item', media_id='123', media_type=MediaTypes.TV.value, source=Sources.TMDB.value)
self.non_member_credentials = {'username': 'non_member', 'password': '12345'}
self.non_member = get_user_model().objects.create_user(**self.non_member_credentials)

self.assertFalse(self.custom_list.user_can_edit(self.non_member))
self.assertFalse(self.custom_list.user_can_delete(self.non_member))
```

*Source: C:\yamtrack-fork\src\lists\tests\test_models.py:72*

### test_get_user_lists

**Category**: method_call  
**Description**: Test the get_user_lists method of CustomListManager.  
**Expected**: self.assertIn(self.list1, user_lists)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomListManager tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.other_credentials = {'username': 'other', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.other_user = get_user_model().objects.create_user(**self.other_credentials)
self.list1 = CustomList.objects.create(name='List 1', owner=self.user)
self.list2 = CustomList.objects.create(name='List 2', owner=self.other_user)
self.list2.collaborators.add(self.user)

self.assertEqual(user_lists.count(), 2)
self.assertIn(self.list1, user_lists)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_models.py:105*

### test_get_user_lists

**Category**: method_call  
**Description**: Test the get_user_lists method of CustomListManager.  
**Expected**: self.assertIn(self.list2, user_lists)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomListManager tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.other_credentials = {'username': 'other', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.other_user = get_user_model().objects.create_user(**self.other_credentials)
self.list1 = CustomList.objects.create(name='List 1', owner=self.user)
self.list2 = CustomList.objects.create(name='List 2', owner=self.other_user)
self.list2.collaborators.add(self.user)

self.assertIn(self.list1, user_lists)
self.assertIn(self.list2, user_lists)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_models.py:106*

### test_import_anilist_public

**Category**: method_call  
**Description**: Basic test importing anime and manga from AniList.  
**Expected**: self.assertEqual(Anime.objects.filter(user=self.user).count(), 4)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

anilist.importer(None, self.user, 'new', 'bloodthirstiness')
self.assertEqual(Anime.objects.filter(user=self.user).count(), 4)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_anilist.py:40*

### test_import_anilist_public

**Category**: method_call  
**Description**: Basic test importing anime and manga from AniList.  
**Expected**: self.assertEqual(Manga.objects.filter(user=self.user).count(), 3)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(Anime.objects.filter(user=self.user).count(), 4)
self.assertEqual(Manga.objects.filter(user=self.user).count(), 3)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_anilist.py:42*

### test_import_anilist_public

**Category**: method_call  
**Description**: Basic test importing anime and manga from AniList.  
**Expected**: self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').status, Status.PAUSED.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(Manga.objects.filter(user=self.user).count(), 3)
self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').status, Status.PAUSED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_anilist.py:43*

### test_import_anilist_public

**Category**: method_call  
**Description**: Basic test importing anime and manga from AniList.  
**Expected**: self.assertEqual(Manga.objects.filter(user=self.user, item__title='One Punch-Man').first().score, 9)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').status, Status.PAUSED.value)
self.assertEqual(Manga.objects.filter(user=self.user, item__title='One Punch-Man').first().score, 9)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_anilist.py:44*

### test_import_anilist_public

**Category**: method_call  
**Description**: Basic test importing anime and manga from AniList.  
**Expected**: self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').history.first().history_date, datetime(2025, 6, 4, 10, 11, 17, tzinfo=UTC))  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(Manga.objects.filter(user=self.user, item__title='One Punch-Man').first().score, 9)
self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').history.first().history_date, datetime(2025, 6, 4, 10, 11, 17, tzinfo=UTC))
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_anilist.py:48*

### test_import_anilist_private

**Category**: method_call  
**Description**: Basic test importing anime and manga from AniList.  
**Expected**: self.assertEqual(Anime.objects.filter(user=self.user).count(), 4)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

anilist.importer(helpers.encrypt('token'), self.user, 'new', 'username')
self.assertEqual(Anime.objects.filter(user=self.user).count(), 4)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_anilist.py:68*

### test_import_anilist_private

**Category**: method_call  
**Description**: Basic test importing anime and manga from AniList.  
**Expected**: self.assertEqual(Manga.objects.filter(user=self.user).count(), 3)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(Anime.objects.filter(user=self.user).count(), 4)
self.assertEqual(Manga.objects.filter(user=self.user).count(), 3)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_anilist.py:75*

### test_import_anilist_private

**Category**: method_call  
**Description**: Basic test importing anime and manga from AniList.  
**Expected**: self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').status, Status.PAUSED.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(Manga.objects.filter(user=self.user).count(), 3)
self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').status, Status.PAUSED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_anilist.py:76*

### test_import_anilist_private

**Category**: method_call  
**Description**: Basic test importing anime and manga from AniList.  
**Expected**: self.assertEqual(Manga.objects.filter(user=self.user, item__title='One Punch-Man').first().score, 9)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').status, Status.PAUSED.value)
self.assertEqual(Manga.objects.filter(user=self.user, item__title='One Punch-Man').first().score, 9)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_anilist.py:77*

### test_import_anilist_private

**Category**: method_call  
**Description**: Basic test importing anime and manga from AniList.  
**Expected**: self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').history.first().history_date, datetime(2025, 6, 4, 10, 11, 17, tzinfo=UTC))  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(Manga.objects.filter(user=self.user, item__title='One Punch-Man').first().score, 9)
self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').history.first().history_date, datetime(2025, 6, 4, 10, 11, 17, tzinfo=UTC))
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_anilist.py:81*

### test_trakt_oauth_uses_configured_public_url

**Category**: method_call  
**Description**: Test Trakt authorization uses the configured public URL.  
**Expected**: self.assertEqual(redirect.netloc, 'trakt.tv')  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**credentials)
self.client.login(**credentials)

self.assertEqual(redirect.scheme, 'https')
self.assertEqual(redirect.netloc, 'trakt.tv')
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_oauth_views.py:29*

### test_trakt_oauth_uses_configured_public_url

**Category**: method_call  
**Description**: Test Trakt authorization uses the configured public URL.  
**Expected**: self.assertEqual(query['client_id'], ['client'])  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**credentials)
self.client.login(**credentials)

self.assertEqual(redirect.netloc, 'trakt.tv')
self.assertEqual(query['client_id'], ['client'])
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_oauth_views.py:30*

### test_trakt_oauth_uses_configured_public_url

**Category**: method_call  
**Description**: Test Trakt authorization uses the configured public URL.  
**Expected**: self.assertEqual(query['redirect_uri'], ['https://yamtrack.example.com:8924/import/trakt/private'])  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**credentials)
self.client.login(**credentials)

self.assertEqual(query['client_id'], ['client'])
self.assertEqual(query['redirect_uri'], ['https://yamtrack.example.com:8924/import/trakt/private'])
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_oauth_views.py:31*

### test_trakt_callback_reuses_stored_redirect_uri

**Category**: method_call  
**Description**: Test the token exchange and import task reuse the original redirect URI.  
**Expected**: mock_oauth_callback.assert_called_once()  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**credentials)
self.client.login(**credentials)

self.assertRedirects(response, reverse('import_data'))
mock_oauth_callback.assert_called_once()
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_oauth_views.py:71*

### test_trakt_callback_reuses_stored_redirect_uri

**Category**: method_call  
**Description**: Test the token exchange and import task reuse the original redirect URI.  
**Expected**: self.assertEqual(mock_oauth_callback.call_args.kwargs['redirect_uri'], redirect_uri)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**credentials)
self.client.login(**credentials)

mock_oauth_callback.assert_called_once()
self.assertEqual(mock_oauth_callback.call_args.kwargs['redirect_uri'], redirect_uri)
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_oauth_views.py:72*

### test_trakt_callback_reuses_stored_redirect_uri

**Category**: method_call  
**Description**: Test the token exchange and import task reuse the original redirect URI.  
**Expected**: mock_import_trakt.assert_called_once()  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**credentials)
self.client.login(**credentials)

self.assertEqual(mock_oauth_callback.call_args.kwargs['redirect_uri'], redirect_uri)
mock_import_trakt.assert_called_once()
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_oauth_views.py:73*

### test_event_string_representation

**Category**: method_call  
**Description**: Test the string representation of events.  
**Expected**: self.assertEqual(str(self.movie_event), 'Test Movie')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime')
self.manga_item = Item.objects.create(media_id='66296374554', source=Sources.MANGAUPDATES.value, media_type=MediaTypes.MANGA.value, title='Test Manga')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value)
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value)
self.anime = Anime.objects.create(user=self.user, item=self.anime_item, status=Status.IN_PROGRESS.value)
self.manga = Manga.objects.create(user=self.user, item=self.manga_item, status=Status.IN_PROGRESS.value)
self.now = timezone.now()
self.tomorrow = self.now + datetime.timedelta(days=1)
self.next_week = self.now + datetime.timedelta(days=7)
self.season_event = Event.objects.create(item=self.season_item, content_number=1, datetime=self.tomorrow)
self.movie_event = Event.objects.create(item=self.movie_item, datetime=self.next_week)
self.anime_event = Event.objects.create(item=self.anime_item, content_number=1, datetime=self.tomorrow)
self.manga_event = Event.objects.create(item=self.manga_item, content_number=1, datetime=self.tomorrow)

self.assertEqual(str(self.season_event), 'Test TV Show S1 E1')
self.assertEqual(str(self.movie_event), 'Test Movie')
```

*Source: C:\yamtrack-fork\src\events\tests\test_models.py:114*

### test_event_string_representation

**Category**: method_call  
**Description**: Test the string representation of events.  
**Expected**: self.assertEqual(str(self.anime_event), 'Test Anime E1')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime')
self.manga_item = Item.objects.create(media_id='66296374554', source=Sources.MANGAUPDATES.value, media_type=MediaTypes.MANGA.value, title='Test Manga')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value)
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value)
self.anime = Anime.objects.create(user=self.user, item=self.anime_item, status=Status.IN_PROGRESS.value)
self.manga = Manga.objects.create(user=self.user, item=self.manga_item, status=Status.IN_PROGRESS.value)
self.now = timezone.now()
self.tomorrow = self.now + datetime.timedelta(days=1)
self.next_week = self.now + datetime.timedelta(days=7)
self.season_event = Event.objects.create(item=self.season_item, content_number=1, datetime=self.tomorrow)
self.movie_event = Event.objects.create(item=self.movie_item, datetime=self.next_week)
self.anime_event = Event.objects.create(item=self.anime_item, content_number=1, datetime=self.tomorrow)
self.manga_event = Event.objects.create(item=self.manga_item, content_number=1, datetime=self.tomorrow)

self.assertEqual(str(self.movie_event), 'Test Movie')
self.assertEqual(str(self.anime_event), 'Test Anime E1')
```

*Source: C:\yamtrack-fork\src\events\tests\test_models.py:120*

### test_event_string_representation

**Category**: method_call  
**Description**: Test the string representation of events.  
**Expected**: self.assertEqual(str(self.manga_event), 'Test Manga #1')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime')
self.manga_item = Item.objects.create(media_id='66296374554', source=Sources.MANGAUPDATES.value, media_type=MediaTypes.MANGA.value, title='Test Manga')
self.season = Season.objects.create(user=self.user, item=self.season_item, status=Status.IN_PROGRESS.value)
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value)
self.anime = Anime.objects.create(user=self.user, item=self.anime_item, status=Status.IN_PROGRESS.value)
self.manga = Manga.objects.create(user=self.user, item=self.manga_item, status=Status.IN_PROGRESS.value)
self.now = timezone.now()
self.tomorrow = self.now + datetime.timedelta(days=1)
self.next_week = self.now + datetime.timedelta(days=7)
self.season_event = Event.objects.create(item=self.season_item, content_number=1, datetime=self.tomorrow)
self.movie_event = Event.objects.create(item=self.movie_item, datetime=self.next_week)
self.anime_event = Event.objects.create(item=self.anime_item, content_number=1, datetime=self.tomorrow)
self.manga_event = Event.objects.create(item=self.manga_item, content_number=1, datetime=self.tomorrow)

self.assertEqual(str(self.anime_event), 'Test Anime E1')
self.assertEqual(str(self.manga_event), 'Test Manga #1')
```

*Source: C:\yamtrack-fork\src\events\tests\test_models.py:123*

### test_get_user_events

**Category**: method_call  
**Description**: Test the get_user_events method.  
**Expected**: self.assertIn(self.season_event, events)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.credentials_other = {'username': 'otheruser', 'password': 'testpassword'}
self.other_user = get_user_model().objects.create_user(**self.credentials_other)
self.tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.paused_movie_item = Item.objects.create(media_id='278', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Paused Movie')
self.dropped_movie_item = Item.objects.create(media_id='424', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Dropped Movie')
self.manga_item = Item.objects.create(media_id='66296374554', source=Sources.MANGAUPDATES.value, media_type=MediaTypes.MANGA.value, title='Test Manga')
self.tv = TV.objects.create(user=self.user, item=self.tv_item, status=Status.IN_PROGRESS.value)
self.other_tv = TV.objects.create(user=self.other_user, item=self.tv_item, status=Status.IN_PROGRESS.value)
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value)
self.paused_movie = Movie.objects.create(user=self.user, item=self.paused_movie_item, status=Status.PAUSED.value)
self.dropped_movie = Movie.objects.create(user=self.user, item=self.dropped_movie_item, status=Status.DROPPED.value)
self.manga = Manga.objects.create(user=self.user, item=self.manga_item, status=Status.IN_PROGRESS.value)
self.base_date = datetime.datetime(2025, 4, 15, 12, 0, 0, tzinfo=datetime.UTC)
self.yesterday = self.base_date - datetime.timedelta(days=1)
self.tomorrow = self.base_date + datetime.timedelta(days=1)
self.next_week = self.base_date + datetime.timedelta(days=7)
self.past_event = Event.objects.create(item=self.season_item, content_number=1, datetime=self.yesterday)
self.movie_event = Event.objects.create(item=self.movie_item, datetime=self.next_week)
self.paused_movie_event = Event.objects.create(item=self.paused_movie_item, datetime=self.next_week)
self.dropped_movie_event = Event.objects.create(item=self.dropped_movie_item, datetime=self.next_week)
self.season_event = Event.objects.create(item=self.season_item, content_number=2, datetime=self.tomorrow)
self.manga_event1 = Event.objects.create(item=self.manga_item, content_number=1, datetime=self.tomorrow)
self.manga_event2 = Event.objects.create(item=self.manga_item, content_number=2, datetime=self.next_week)

self.assertEqual(events.count(), 4)
self.assertIn(self.season_event, events)
```

*Source: C:\yamtrack-fork\src\events\tests\test_models.py:279*

### test_get_user_events

**Category**: method_call  
**Description**: Test the get_user_events method.  
**Expected**: self.assertIn(self.manga_event1, events)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.credentials_other = {'username': 'otheruser', 'password': 'testpassword'}
self.other_user = get_user_model().objects.create_user(**self.credentials_other)
self.tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.paused_movie_item = Item.objects.create(media_id='278', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Paused Movie')
self.dropped_movie_item = Item.objects.create(media_id='424', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Dropped Movie')
self.manga_item = Item.objects.create(media_id='66296374554', source=Sources.MANGAUPDATES.value, media_type=MediaTypes.MANGA.value, title='Test Manga')
self.tv = TV.objects.create(user=self.user, item=self.tv_item, status=Status.IN_PROGRESS.value)
self.other_tv = TV.objects.create(user=self.other_user, item=self.tv_item, status=Status.IN_PROGRESS.value)
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value)
self.paused_movie = Movie.objects.create(user=self.user, item=self.paused_movie_item, status=Status.PAUSED.value)
self.dropped_movie = Movie.objects.create(user=self.user, item=self.dropped_movie_item, status=Status.DROPPED.value)
self.manga = Manga.objects.create(user=self.user, item=self.manga_item, status=Status.IN_PROGRESS.value)
self.base_date = datetime.datetime(2025, 4, 15, 12, 0, 0, tzinfo=datetime.UTC)
self.yesterday = self.base_date - datetime.timedelta(days=1)
self.tomorrow = self.base_date + datetime.timedelta(days=1)
self.next_week = self.base_date + datetime.timedelta(days=7)
self.past_event = Event.objects.create(item=self.season_item, content_number=1, datetime=self.yesterday)
self.movie_event = Event.objects.create(item=self.movie_item, datetime=self.next_week)
self.paused_movie_event = Event.objects.create(item=self.paused_movie_item, datetime=self.next_week)
self.dropped_movie_event = Event.objects.create(item=self.dropped_movie_item, datetime=self.next_week)
self.season_event = Event.objects.create(item=self.season_item, content_number=2, datetime=self.tomorrow)
self.manga_event1 = Event.objects.create(item=self.manga_item, content_number=1, datetime=self.tomorrow)
self.manga_event2 = Event.objects.create(item=self.manga_item, content_number=2, datetime=self.next_week)

self.assertIn(self.season_event, events)
self.assertIn(self.manga_event1, events)
```

*Source: C:\yamtrack-fork\src\events\tests\test_models.py:280*

### test_get_user_events

**Category**: method_call  
**Description**: Test the get_user_events method.  
**Expected**: self.assertIn(self.movie_event, events)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.credentials_other = {'username': 'otheruser', 'password': 'testpassword'}
self.other_user = get_user_model().objects.create_user(**self.credentials_other)
self.tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.paused_movie_item = Item.objects.create(media_id='278', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Paused Movie')
self.dropped_movie_item = Item.objects.create(media_id='424', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Dropped Movie')
self.manga_item = Item.objects.create(media_id='66296374554', source=Sources.MANGAUPDATES.value, media_type=MediaTypes.MANGA.value, title='Test Manga')
self.tv = TV.objects.create(user=self.user, item=self.tv_item, status=Status.IN_PROGRESS.value)
self.other_tv = TV.objects.create(user=self.other_user, item=self.tv_item, status=Status.IN_PROGRESS.value)
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value)
self.paused_movie = Movie.objects.create(user=self.user, item=self.paused_movie_item, status=Status.PAUSED.value)
self.dropped_movie = Movie.objects.create(user=self.user, item=self.dropped_movie_item, status=Status.DROPPED.value)
self.manga = Manga.objects.create(user=self.user, item=self.manga_item, status=Status.IN_PROGRESS.value)
self.base_date = datetime.datetime(2025, 4, 15, 12, 0, 0, tzinfo=datetime.UTC)
self.yesterday = self.base_date - datetime.timedelta(days=1)
self.tomorrow = self.base_date + datetime.timedelta(days=1)
self.next_week = self.base_date + datetime.timedelta(days=7)
self.past_event = Event.objects.create(item=self.season_item, content_number=1, datetime=self.yesterday)
self.movie_event = Event.objects.create(item=self.movie_item, datetime=self.next_week)
self.paused_movie_event = Event.objects.create(item=self.paused_movie_item, datetime=self.next_week)
self.dropped_movie_event = Event.objects.create(item=self.dropped_movie_item, datetime=self.next_week)
self.season_event = Event.objects.create(item=self.season_item, content_number=2, datetime=self.tomorrow)
self.manga_event1 = Event.objects.create(item=self.manga_item, content_number=1, datetime=self.tomorrow)
self.manga_event2 = Event.objects.create(item=self.manga_item, content_number=2, datetime=self.next_week)

self.assertIn(self.manga_event1, events)
self.assertIn(self.movie_event, events)
```

*Source: C:\yamtrack-fork\src\events\tests\test_models.py:281*

### test_get_user_events

**Category**: method_call  
**Description**: Test the get_user_events method.  
**Expected**: self.assertIn(self.manga_event2, events)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.credentials_other = {'username': 'otheruser', 'password': 'testpassword'}
self.other_user = get_user_model().objects.create_user(**self.credentials_other)
self.tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.paused_movie_item = Item.objects.create(media_id='278', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Paused Movie')
self.dropped_movie_item = Item.objects.create(media_id='424', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Dropped Movie')
self.manga_item = Item.objects.create(media_id='66296374554', source=Sources.MANGAUPDATES.value, media_type=MediaTypes.MANGA.value, title='Test Manga')
self.tv = TV.objects.create(user=self.user, item=self.tv_item, status=Status.IN_PROGRESS.value)
self.other_tv = TV.objects.create(user=self.other_user, item=self.tv_item, status=Status.IN_PROGRESS.value)
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value)
self.paused_movie = Movie.objects.create(user=self.user, item=self.paused_movie_item, status=Status.PAUSED.value)
self.dropped_movie = Movie.objects.create(user=self.user, item=self.dropped_movie_item, status=Status.DROPPED.value)
self.manga = Manga.objects.create(user=self.user, item=self.manga_item, status=Status.IN_PROGRESS.value)
self.base_date = datetime.datetime(2025, 4, 15, 12, 0, 0, tzinfo=datetime.UTC)
self.yesterday = self.base_date - datetime.timedelta(days=1)
self.tomorrow = self.base_date + datetime.timedelta(days=1)
self.next_week = self.base_date + datetime.timedelta(days=7)
self.past_event = Event.objects.create(item=self.season_item, content_number=1, datetime=self.yesterday)
self.movie_event = Event.objects.create(item=self.movie_item, datetime=self.next_week)
self.paused_movie_event = Event.objects.create(item=self.paused_movie_item, datetime=self.next_week)
self.dropped_movie_event = Event.objects.create(item=self.dropped_movie_item, datetime=self.next_week)
self.season_event = Event.objects.create(item=self.season_item, content_number=2, datetime=self.tomorrow)
self.manga_event1 = Event.objects.create(item=self.manga_item, content_number=1, datetime=self.tomorrow)
self.manga_event2 = Event.objects.create(item=self.manga_item, content_number=2, datetime=self.next_week)

self.assertIn(self.movie_event, events)
self.assertIn(self.manga_event2, events)
```

*Source: C:\yamtrack-fork\src\events\tests\test_models.py:282*

### test_get_user_events

**Category**: method_call  
**Description**: Test the get_user_events method.  
**Expected**: self.assertNotIn(self.past_event, events)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'testuser', 'password': 'testpassword'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.credentials_other = {'username': 'otheruser', 'password': 'testpassword'}
self.other_user = get_user_model().objects.create_user(**self.credentials_other)
self.tv_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.movie_item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.paused_movie_item = Item.objects.create(media_id='278', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Paused Movie')
self.dropped_movie_item = Item.objects.create(media_id='424', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Dropped Movie')
self.manga_item = Item.objects.create(media_id='66296374554', source=Sources.MANGAUPDATES.value, media_type=MediaTypes.MANGA.value, title='Test Manga')
self.tv = TV.objects.create(user=self.user, item=self.tv_item, status=Status.IN_PROGRESS.value)
self.other_tv = TV.objects.create(user=self.other_user, item=self.tv_item, status=Status.IN_PROGRESS.value)
self.movie = Movie.objects.create(user=self.user, item=self.movie_item, status=Status.PLANNING.value)
self.paused_movie = Movie.objects.create(user=self.user, item=self.paused_movie_item, status=Status.PAUSED.value)
self.dropped_movie = Movie.objects.create(user=self.user, item=self.dropped_movie_item, status=Status.DROPPED.value)
self.manga = Manga.objects.create(user=self.user, item=self.manga_item, status=Status.IN_PROGRESS.value)
self.base_date = datetime.datetime(2025, 4, 15, 12, 0, 0, tzinfo=datetime.UTC)
self.yesterday = self.base_date - datetime.timedelta(days=1)
self.tomorrow = self.base_date + datetime.timedelta(days=1)
self.next_week = self.base_date + datetime.timedelta(days=7)
self.past_event = Event.objects.create(item=self.season_item, content_number=1, datetime=self.yesterday)
self.movie_event = Event.objects.create(item=self.movie_item, datetime=self.next_week)
self.paused_movie_event = Event.objects.create(item=self.paused_movie_item, datetime=self.next_week)
self.dropped_movie_event = Event.objects.create(item=self.dropped_movie_item, datetime=self.next_week)
self.season_event = Event.objects.create(item=self.season_item, content_number=2, datetime=self.tomorrow)
self.manga_event1 = Event.objects.create(item=self.manga_item, content_number=1, datetime=self.tomorrow)
self.manga_event2 = Event.objects.create(item=self.manga_item, content_number=2, datetime=self.next_week)

self.assertIn(self.manga_event2, events)
self.assertNotIn(self.past_event, events)
```

*Source: C:\yamtrack-fork\src\events\tests\test_models.py:283*

### test_extracts_title_and_year

**Category**: method_call  
**Description**: test extracts title and year  
**Expected**: self.assertEqual(year, 2010)  
**Confidence**: 0.85  

```python
self.assertEqual(title, 'Inception')
self.assertEqual(year, 2010)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_filmaffinity.py:61*

### test_title_without_year

**Category**: method_call  
**Description**: test title without year  
**Expected**: self.assertIsNone(year)  
**Confidence**: 0.85  

```python
self.assertEqual(title, 'Film Without Year')
self.assertIsNone(year)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_filmaffinity.py:66*

### test_title_with_colon

**Category**: method_call  
**Description**: test title with colon  
**Expected**: self.assertEqual(year, 2018)  
**Confidence**: 0.85  

```python
self.assertEqual(title, 'Black Mirror: Bandersnatch')
self.assertEqual(year, 2018)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_filmaffinity.py:71*

### test_title_with_parentheses_in_name

**Category**: method_call  
**Description**: test title with parentheses in name  
**Expected**: self.assertEqual(year, 2018)  
**Confidence**: 0.85  

```python
self.assertEqual(title, 'Spider-Man: Into the Spider-Verse')
self.assertEqual(year, 2018)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_filmaffinity.py:76*

### test_parses_title_and_year

**Category**: method_call  
**Description**: test parses title and year  
**Expected**: self.assertEqual(films[0]['year'], 2010)  
**Confidence**: 0.85  

```python
self.assertEqual(films[0]['title'], 'Inception')
self.assertEqual(films[0]['year'], 2010)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_filmaffinity.py:107*

### test_film_title_correct

**Category**: method_call  
**Description**: test film title correct  
**Expected**: self.assertEqual(films[0]['year'], 2010)  
**Confidence**: 0.85  

```python
self.assertEqual(films[0]['title'], 'Inception')
self.assertEqual(films[0]['year'], 2010)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_filmaffinity.py:143*

### test_import_creates_movies

**Category**: method_call  
**Description**: test import creates movies  
**Expected**: self.assertGreater(Movie.objects.filter(user=self.user).count(), 0)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
self.user = User.objects.create_user(username='test', password='12345')

def _bulk_create(objs, model, batch_size=500, default_user=None):
    model.objects.bulk_create(objs)
    return objs
patcher = unittest.mock.patch('integrations.imports.helpers.bulk_create_with_history', side_effect=_bulk_create)
self.mock_bulk = patcher.start()
self.addCleanup(patcher.stop)

importer.run(RATINGS_HTML)
self.assertGreater(Movie.objects.filter(user=self.user).count(), 0)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_filmaffinity.py:166*

### test_status_is_completed

**Category**: method_call  
**Description**: test status is completed  
**Expected**: self.assertEqual(movie.status, Status.COMPLETED.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
self.user = User.objects.create_user(username='test', password='12345')

def _bulk_create(objs, model, batch_size=500, default_user=None):
    model.objects.bulk_create(objs)
    return objs
patcher = unittest.mock.patch('integrations.imports.helpers.bulk_create_with_history', side_effect=_bulk_create)
self.mock_bulk = patcher.start()
self.addCleanup(patcher.stop)

self.assertIsNotNone(movie)
self.assertEqual(movie.status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_filmaffinity.py:181*

### test_get_anime_schedule_bulk

**Category**: method_call  
**Description**: Test get_anime_schedule_bulk function.  
**Expected**: self.assertEqual(len(result['437']), 1)  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertIn('437', result)
self.assertEqual(len(result['437']), 1)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_anime.py:44*

### test_get_anime_schedule_bulk

**Category**: method_call  
**Description**: Test get_anime_schedule_bulk function.  
**Expected**: self.assertEqual(result['437'][0]['episode'], 1)  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(len(result['437']), 1)
self.assertEqual(result['437'][0]['episode'], 1)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_anime.py:45*

### test_update_plex_usernames_success

**Category**: method_call  
**Description**: Test successful update of Plex usernames.  
**Expected**: self.assertEqual(self.user.plex_usernames, 'user1, user2, user3')  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.user.refresh_from_db()
self.assertEqual(self.user.plex_usernames, 'user1, user2, user3')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_plex.py:24*

### test_update_plex_usernames_success

**Category**: method_call  
**Description**: Test successful update of Plex usernames.  
**Expected**: self.assertIn('updated successfully', str(messages[0]))  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(len(messages), 1)
self.assertIn('updated successfully', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_plex.py:29*

### test_update_plex_usernames_deduplication

**Category**: method_call  
**Description**: Test duplicate usernames are removed.  
**Expected**: self.assertEqual(self.user.plex_usernames, 'user1, user2, user3')  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.user.refresh_from_db()
self.assertEqual(self.user.plex_usernames, 'user1, user2, user3')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_plex.py:39*

### test_update_plex_usernames_whitespace_handling

**Category**: method_call  
**Description**: Test whitespace in usernames is handled correctly.  
**Expected**: self.assertEqual(self.user.plex_usernames, 'user1, user2, user3')  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.user.refresh_from_db()
self.assertEqual(self.user.plex_usernames, 'user1, user2, user3')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_plex.py:49*

### test_update_plex_usernames_empty

**Category**: method_call  
**Description**: Test empty username list.  
**Expected**: self.assertEqual(self.user.plex_usernames, '')  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.user.refresh_from_db()
self.assertEqual(self.user.plex_usernames, '')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_plex.py:62*

### test_update_plex_usernames_empty

**Category**: method_call  
**Description**: Test empty username list.  
**Expected**: self.assertIn('updated successfully', str(messages[0]))  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(len(messages), 1)
self.assertIn('updated successfully', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_plex.py:66*

### test_update_plex_usernames_success

**Category**: method_call  
**Description**: Test successful update of Plex usernames.  
**Expected**: self.assertEqual(self.user.plex_usernames, 'user1, user2, user3')  
**Confidence**: 0.85  

```python
self.user.refresh_from_db()
self.assertEqual(self.user.plex_usernames, 'user1, user2, user3')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_plex.py:24*

### test_update_plex_usernames_success

**Category**: method_call  
**Description**: Test successful update of Plex usernames.  
**Expected**: self.assertIn('updated successfully', str(messages[0]))  
**Confidence**: 0.85  

```python
self.assertEqual(len(messages), 1)
self.assertIn('updated successfully', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_plex.py:29*

### test_update_plex_usernames_deduplication

**Category**: method_call  
**Description**: Test duplicate usernames are removed.  
**Expected**: self.assertEqual(self.user.plex_usernames, 'user1, user2, user3')  
**Confidence**: 0.85  

```python
self.user.refresh_from_db()
self.assertEqual(self.user.plex_usernames, 'user1, user2, user3')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_plex.py:39*

### test_update_plex_usernames_whitespace_handling

**Category**: method_call  
**Description**: Test whitespace in usernames is handled correctly.  
**Expected**: self.assertEqual(self.user.plex_usernames, 'user1, user2, user3')  
**Confidence**: 0.85  

```python
self.user.refresh_from_db()
self.assertEqual(self.user.plex_usernames, 'user1, user2, user3')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_plex.py:49*

### test_track_modal_view_existing_media

**Category**: method_call  
**Description**: Test the track modal view for existing media.  
**Expected**: self.assertTemplateUsed(response, 'app/components/fill_track.html')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')
self.movie = Movie.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=0)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/components/fill_track.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_track_modal.py:53*

### test_track_modal_view_existing_media

**Category**: method_call  
**Description**: Test the track modal view for existing media.  
**Expected**: self.assertIn('form', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')
self.movie = Movie.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=0)

self.assertTemplateUsed(response, 'app/components/fill_track.html')
self.assertIn('form', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_track_modal.py:54*

### test_track_modal_view_existing_media

**Category**: method_call  
**Description**: Test the track modal view for existing media.  
**Expected**: self.assertIn('media', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')
self.movie = Movie.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=0)

self.assertIn('form', response.context)
self.assertIn('media', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_track_modal.py:56*

### test_track_modal_view_existing_media

**Category**: method_call  
**Description**: Test the track modal view for existing media.  
**Expected**: self.assertEqual(response.context['media'], self.movie)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')
self.movie = Movie.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=0)

self.assertIn('media', response.context)
self.assertEqual(response.context['media'], self.movie)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_track_modal.py:57*

### test_track_modal_view_existing_media

**Category**: method_call  
**Description**: Test the track modal view for existing media.  
**Expected**: self.assertEqual(response.context['return_url'], '/home')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')
self.movie = Movie.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=0)

self.assertEqual(response.context['media'], self.movie)
self.assertEqual(response.context['return_url'], '/home')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_track_modal.py:58*

### test_track_modal_view_new_media

**Category**: method_call  
**Description**: Test the track modal view for new media.  
**Expected**: self.assertTemplateUsed(response, 'app/components/fill_track.html')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')
self.movie = Movie.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=0)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/components/fill_track.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_track_modal.py:85*

### test_track_modal_view_new_media

**Category**: method_call  
**Description**: Test the track modal view for new media.  
**Expected**: self.assertIn('form', response.context)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')
self.movie = Movie.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=0)

self.assertTemplateUsed(response, 'app/components/fill_track.html')
self.assertIn('form', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_track_modal.py:86*

### test_track_modal_view_new_media

**Category**: method_call  
**Description**: Test the track modal view for new media.  
**Expected**: self.assertEqual(response.context['form'].initial['media_id'], '278')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')
self.movie = Movie.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=0)

self.assertIn('form', response.context)
self.assertEqual(response.context['form'].initial['media_id'], '278')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_track_modal.py:88*

### test_track_modal_view_new_media

**Category**: method_call  
**Description**: Test the track modal view for new media.  
**Expected**: self.assertEqual(response.context['form'].initial['media_type'], MediaTypes.MOVIE.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')
self.movie = Movie.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=0)

self.assertEqual(response.context['form'].initial['media_id'], '278')
self.assertEqual(response.context['form'].initial['media_type'], MediaTypes.MOVIE.value)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_track_modal.py:89*

### test_track_modal_view_existing_media

**Category**: method_call  
**Description**: Test the track modal view for existing media.  
**Expected**: self.assertTemplateUsed(response, 'app/components/fill_track.html')  
**Confidence**: 0.85  

```python
self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/components/fill_track.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_track_modal.py:53*

### test_notifications_get

**Category**: method_call  
**Description**: Test GET request to notifications view.  
**Expected**: self.assertTemplateUsed(response, 'users/notifications.html')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item1 = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/anime.jpg')
self.item2 = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Test Manga', image='http://example.com/manga.jpg')

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'users/notifications.html')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_notifications.py:39*

### test_notifications_get

**Category**: method_call  
**Description**: Test GET request to notifications view.  
**Expected**: self.assertIn('form', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item1 = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/anime.jpg')
self.item2 = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Test Manga', image='http://example.com/manga.jpg')

self.assertTemplateUsed(response, 'users/notifications.html')
self.assertIn('form', response.context)
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_notifications.py:40*

### test_notifications_post_valid

**Category**: method_call  
**Description**: Test POST request with valid data.  
**Expected**: self.assertEqual(self.user.notification_urls, 'discord://webhook_id/webhook_token')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item1 = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/anime.jpg')
self.item2 = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Test Manga', image='http://example.com/manga.jpg')

self.user.refresh_from_db()
self.assertEqual(self.user.notification_urls, 'discord://webhook_id/webhook_token')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_notifications.py:53*

### test_notifications_post_valid

**Category**: method_call  
**Description**: Test POST request with valid data.  
**Expected**: self.assertIn('updated successfully', str(messages[0]))  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item1 = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/anime.jpg')
self.item2 = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Test Manga', image='http://example.com/manga.jpg')

self.assertEqual(len(messages), 1)
self.assertIn('updated successfully', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_notifications.py:60*

### test_notifications_post_invalid

**Category**: method_call  
**Description**: Test POST request with invalid data.  
**Expected**: self.assertEqual(self.user.notification_urls, '')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item1 = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/anime.jpg')
self.item2 = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Test Manga', image='http://example.com/manga.jpg')

self.user.refresh_from_db()
self.assertEqual(self.user.notification_urls, '')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_notifications.py:76*

### test_notifications_post_invalid

**Category**: method_call  
**Description**: Test POST request with invalid data.  
**Expected**: self.assertIn('not a valid Apprise URL', str(messages[0]))  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item1 = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/anime.jpg')
self.item2 = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Test Manga', image='http://example.com/manga.jpg')

self.assertEqual(len(messages), 1)
self.assertIn('not a valid Apprise URL', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_notifications.py:80*

### test_exclude_item

**Category**: method_call  
**Description**: Test excluding an item from notifications.  
**Expected**: self.assertTemplateUsed(response, 'users/components/excluded_items.html')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item1 = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/anime.jpg')
self.item2 = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Test Manga', image='http://example.com/manga.jpg')

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'users/components/excluded_items.html')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_notifications.py:91*

### test_exclude_item

**Category**: method_call  
**Description**: Test excluding an item from notifications.  
**Expected**: self.assertTrue(self.user.notification_excluded_items.filter(id=self.item1.id).exists())  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item1 = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/anime.jpg')
self.item2 = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Test Manga', image='http://example.com/manga.jpg')

self.assertTemplateUsed(response, 'users/components/excluded_items.html')
self.assertTrue(self.user.notification_excluded_items.filter(id=self.item1.id).exists())
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_notifications.py:92*

### test_include_item

**Category**: method_call  
**Description**: Test removing an item from exclusions.  
**Expected**: self.assertTemplateUsed(response, 'users/components/excluded_items.html')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item1 = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/anime.jpg')
self.item2 = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Test Manga', image='http://example.com/manga.jpg')

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'users/components/excluded_items.html')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_notifications.py:108*

### test_include_item

**Category**: method_call  
**Description**: Test removing an item from exclusions.  
**Expected**: self.assertFalse(self.user.notification_excluded_items.filter(id=self.item1.id).exists())  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item1 = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/anime.jpg')
self.item2 = Item.objects.create(media_id='2', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Test Manga', image='http://example.com/manga.jpg')

self.assertTemplateUsed(response, 'users/components/excluded_items.html')
self.assertFalse(self.user.notification_excluded_items.filter(id=self.item1.id).exists())
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_notifications.py:109*

### test_history_modal_view

**Category**: method_call  
**Description**: Test the history modal view.  
**Expected**: self.assertTemplateUsed(response, 'app/components/fill_history.html')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')
self.movie = Movie.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=0)
self.movie.status = Status.COMPLETED.value
self.movie.progress = 1
self.movie.score = 8
self.movie.save()

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/components/fill_history.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_history.py:56*

### test_history_modal_view

**Category**: method_call  
**Description**: Test the history modal view.  
**Expected**: self.assertIn('timeline', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')
self.movie = Movie.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=0)
self.movie.status = Status.COMPLETED.value
self.movie.progress = 1
self.movie.score = 8
self.movie.save()

self.assertTemplateUsed(response, 'app/components/fill_history.html')
self.assertIn('timeline', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_history.py:57*

### test_history_modal_view

**Category**: method_call  
**Description**: Test the history modal view.  
**Expected**: self.assertGreater(len(response.context['timeline']), 0)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')
self.movie = Movie.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=0)
self.movie.status = Status.COMPLETED.value
self.movie.progress = 1
self.movie.score = 8
self.movie.save()

self.assertIn('timeline', response.context)
self.assertGreater(len(response.context['timeline']), 0)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_history.py:59*

### test_history_modal_view

**Category**: method_call  
**Description**: Test the history modal view.  
**Expected**: self.assertGreater(len(first_entry['changes']), 0)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')
self.movie = Movie.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=0)
self.movie.status = Status.COMPLETED.value
self.movie.progress = 1
self.movie.score = 8
self.movie.save()

self.assertIn('changes', first_entry)
self.assertGreater(len(first_entry['changes']), 0)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_history.py:63*

### test_delete_history_record

**Category**: method_call  
**Description**: Test deleting a history record.  
**Expected**: self.assertEqual(self.movie.history.filter(history_id=self.history_id).count(), 0)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item = Item.objects.create(media_id='238', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')
self.movie = Movie.objects.create(item=self.item, user=self.user, status=Status.IN_PROGRESS.value, progress=0)
self.movie.status = Status.COMPLETED.value
self.movie.progress = 1
self.movie.score = 8
self.movie.save()
self.history = self.movie.history.first()
self.history_id = self.history.history_id
self.history.history_user = self.user
self.history.save()

self.assertEqual(response.status_code, 200)
self.assertEqual(self.movie.history.filter(history_id=self.history_id).count(), 0)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_history.py:114*

### test_history_modal_view

**Category**: method_call  
**Description**: Test the history modal view.  
**Expected**: self.assertTemplateUsed(response, 'app/components/fill_history.html')  
**Confidence**: 0.85  

```python
self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/components/fill_history.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_history.py:56*

### test_history_modal_view

**Category**: method_call  
**Description**: Test the history modal view.  
**Expected**: self.assertIn('timeline', response.context)  
**Confidence**: 0.85  

```python
self.assertTemplateUsed(response, 'app/components/fill_history.html')
self.assertIn('timeline', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_history.py:57*

### test_history_modal_view

**Category**: method_call  
**Description**: Test the history modal view.  
**Expected**: self.assertGreater(len(response.context['timeline']), 0)  
**Confidence**: 0.85  

```python
self.assertIn('timeline', response.context)
self.assertGreater(len(response.context['timeline']), 0)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_history.py:59*

### test_history_modal_view

**Category**: method_call  
**Description**: Test the history modal view.  
**Expected**: self.assertGreater(len(first_entry['changes']), 0)  
**Confidence**: 0.85  

```python
self.assertIn('changes', first_entry)
self.assertGreater(len(first_entry['changes']), 0)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_history.py:63*

### test_delete_history_record

**Category**: method_call  
**Description**: Test deleting a history record.  
**Expected**: self.assertEqual(self.movie.history.filter(history_id=self.history_id).count(), 0)  
**Confidence**: 0.85  

```python
self.assertEqual(response.status_code, 200)
self.assertEqual(self.movie.history.filter(history_id=self.history_id).count(), 0)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_history.py:114*

### test_historical_records

**Category**: method_call  
**Description**: Test historical records creation during import.  
**Expected**: self.assertEqual(game.history.first().history_date, datetime(2024, 2, 9, 15, 54, 48, tzinfo=UTC))  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_hltb_game.csv').open('rb') as file:
    self.import_results = hltb.importer(file, self.user, 'new')

self.assertEqual(game.history.count(), 1)
self.assertEqual(game.history.first().history_date, datetime(2024, 2, 9, 15, 54, 48, tzinfo=UTC))
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_hltb.py:37*

### test_historical_records

**Category**: method_call  
**Description**: Test historical records creation during import.  
**Expected**: self.assertEqual(game.history.first().history_date, datetime(2024, 2, 9, 15, 54, 48, tzinfo=UTC))  
**Confidence**: 0.85  

```python
self.assertEqual(game.history.count(), 1)
self.assertEqual(game.history.first().history_date, datetime(2024, 2, 9, 15, 54, 48, tzinfo=UTC))
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_hltb.py:37*

### test_get_media_response

**Category**: method_call  
**Description**: Test getting media response from Kitsu.  
**Expected**: self.assertEqual(imported_counts[MediaTypes.MANGA.value], 6)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
with Path(mock_path / 'import_kitsu_anime.json').open() as file:
    self.sample_anime_response = json.load(file)
with Path(mock_path / 'import_kitsu_manga.json').open() as file:
    self.sample_manga_response = json.load(file)
self.importer = kitsu.KitsuImporter('testuser', self.user, 'new')

self.assertEqual(imported_counts[MediaTypes.ANIME.value], 6)
self.assertEqual(imported_counts[MediaTypes.MANGA.value], 6)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_kitsu.py:63*

### test_get_media_response

**Category**: method_call  
**Description**: Test getting media response from Kitsu.  
**Expected**: self.assertEqual(warning_message, '')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
with Path(mock_path / 'import_kitsu_anime.json').open() as file:
    self.sample_anime_response = json.load(file)
with Path(mock_path / 'import_kitsu_manga.json').open() as file:
    self.sample_manga_response = json.load(file)
self.importer = kitsu.KitsuImporter('testuser', self.user, 'new')

self.assertEqual(imported_counts[MediaTypes.MANGA.value], 6)
self.assertEqual(warning_message, '')
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_kitsu.py:64*

### test_get_media_response

**Category**: method_call  
**Description**: Test getting media response from Kitsu.  
**Expected**: self.assertEqual(Anime.objects.count(), 6)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
with Path(mock_path / 'import_kitsu_anime.json').open() as file:
    self.sample_anime_response = json.load(file)
with Path(mock_path / 'import_kitsu_manga.json').open() as file:
    self.sample_manga_response = json.load(file)
self.importer = kitsu.KitsuImporter('testuser', self.user, 'new')

self.assertEqual(warning_message, '')
self.assertEqual(Anime.objects.count(), 6)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_kitsu.py:65*

### test_get_media_response

**Category**: method_call  
**Description**: Test getting media response from Kitsu.  
**Expected**: self.assertEqual(Manga.objects.count(), 6)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
with Path(mock_path / 'import_kitsu_anime.json').open() as file:
    self.sample_anime_response = json.load(file)
with Path(mock_path / 'import_kitsu_manga.json').open() as file:
    self.sample_manga_response = json.load(file)
self.importer = kitsu.KitsuImporter('testuser', self.user, 'new')

self.assertEqual(Anime.objects.count(), 6)
self.assertEqual(Manga.objects.count(), 6)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_kitsu.py:67*

### test_get_media_response

**Category**: method_call  
**Description**: Test getting media response from Kitsu.  
**Expected**: self.assertEqual(Anime.objects.get(item__title='Test Anime 2').history.first().history_date, datetime(2024, 4, 8, 16, 16, 59, 18000, tzinfo=UTC))  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
with Path(mock_path / 'import_kitsu_anime.json').open() as file:
    self.sample_anime_response = json.load(file)
with Path(mock_path / 'import_kitsu_manga.json').open() as file:
    self.sample_manga_response = json.load(file)
self.importer = kitsu.KitsuImporter('testuser', self.user, 'new')

self.assertEqual(Manga.objects.count(), 6)
self.assertEqual(Anime.objects.get(item__title='Test Anime 2').history.first().history_date, datetime(2024, 4, 8, 16, 16, 59, 18000, tzinfo=UTC))
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_kitsu.py:68*

### test_get_rating

**Category**: method_call  
**Description**: Test getting rating from Kitsu.  
**Expected**: self.assertEqual(self.importer._get_rating(10), 5)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
with Path(mock_path / 'import_kitsu_anime.json').open() as file:
    self.sample_anime_response = json.load(file)
with Path(mock_path / 'import_kitsu_manga.json').open() as file:
    self.sample_manga_response = json.load(file)
self.importer = kitsu.KitsuImporter('testuser', self.user, 'new')

self.assertEqual(self.importer._get_rating(20), 10)
self.assertEqual(self.importer._get_rating(10), 5)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_kitsu.py:76*

### test_get_rating

**Category**: method_call  
**Description**: Test getting rating from Kitsu.  
**Expected**: self.assertEqual(self.importer._get_rating(1), 0.5)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
with Path(mock_path / 'import_kitsu_anime.json').open() as file:
    self.sample_anime_response = json.load(file)
with Path(mock_path / 'import_kitsu_manga.json').open() as file:
    self.sample_manga_response = json.load(file)
self.importer = kitsu.KitsuImporter('testuser', self.user, 'new')

self.assertEqual(self.importer._get_rating(10), 5)
self.assertEqual(self.importer._get_rating(1), 0.5)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_kitsu.py:77*

### test_get_rating

**Category**: method_call  
**Description**: Test getting rating from Kitsu.  
**Expected**: self.assertIsNone(self.importer._get_rating(None))  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
with Path(mock_path / 'import_kitsu_anime.json').open() as file:
    self.sample_anime_response = json.load(file)
with Path(mock_path / 'import_kitsu_manga.json').open() as file:
    self.sample_manga_response = json.load(file)
self.importer = kitsu.KitsuImporter('testuser', self.user, 'new')

self.assertEqual(self.importer._get_rating(1), 0.5)
self.assertIsNone(self.importer._get_rating(None))
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_kitsu.py:78*

### test_delete_import_schedule_success

**Category**: method_call  
**Description**: Test successful deletion of an import schedule.  
**Expected**: self.assertIn('Import schedule deleted', str(messages[0]))  
**Confidence**: 0.85  

```python
# Setup
'Create user and test data for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.crontab = CrontabSchedule.objects.create(minute='0', hour='0', day_of_week='*', day_of_month='*', month_of_year='*')
self.task = PeriodicTask.objects.create(name='Import from Trakt for testuser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
self.other_credentials = {'username': 'otheruser', 'password': 'testpass123'}
self.other_user = get_user_model().objects.create_user(**self.other_credentials)
self.other_task = PeriodicTask.objects.create(name='Import from Trakt for otheruser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.other_user.id}, "username": "otheruser"}}', crontab=self.crontab, enabled=True)

self.assertEqual(len(messages), 1)
self.assertIn('Import schedule deleted', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_delete_import.py:58*

### test_delete_import_schedule_success

**Category**: method_call  
**Description**: Test successful deletion of an import schedule.  
**Expected**: self.assertTrue(PeriodicTask.objects.filter(id=self.other_task.id).exists())  
**Confidence**: 0.85  

```python
# Setup
'Create user and test data for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.crontab = CrontabSchedule.objects.create(minute='0', hour='0', day_of_week='*', day_of_month='*', month_of_year='*')
self.task = PeriodicTask.objects.create(name='Import from Trakt for testuser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
self.other_credentials = {'username': 'otheruser', 'password': 'testpass123'}
self.other_user = get_user_model().objects.create_user(**self.other_credentials)
self.other_task = PeriodicTask.objects.create(name='Import from Trakt for otheruser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.other_user.id}, "username": "otheruser"}}', crontab=self.crontab, enabled=True)

self.assertIn('Import schedule deleted', str(messages[0]))
self.assertTrue(PeriodicTask.objects.filter(id=self.other_task.id).exists())
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_delete_import.py:59*

### test_delete_import_schedule_not_found

**Category**: method_call  
**Description**: Test deletion of a non-existent import schedule.  
**Expected**: self.assertIn('Import schedule not found', str(messages[0]))  
**Confidence**: 0.85  

```python
# Setup
'Create user and test data for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.crontab = CrontabSchedule.objects.create(minute='0', hour='0', day_of_week='*', day_of_month='*', month_of_year='*')
self.task = PeriodicTask.objects.create(name='Import from Trakt for testuser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
self.other_credentials = {'username': 'otheruser', 'password': 'testpass123'}
self.other_user = get_user_model().objects.create_user(**self.other_credentials)
self.other_task = PeriodicTask.objects.create(name='Import from Trakt for otheruser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.other_user.id}, "username": "otheruser"}}', crontab=self.crontab, enabled=True)

self.assertEqual(len(messages), 1)
self.assertIn('Import schedule not found', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_delete_import.py:74*

### test_delete_import_schedule_not_found

**Category**: method_call  
**Description**: Test deletion of a non-existent import schedule.  
**Expected**: self.assertTrue(PeriodicTask.objects.filter(id=self.task.id).exists())  
**Confidence**: 0.85  

```python
# Setup
'Create user and test data for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.crontab = CrontabSchedule.objects.create(minute='0', hour='0', day_of_week='*', day_of_month='*', month_of_year='*')
self.task = PeriodicTask.objects.create(name='Import from Trakt for testuser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
self.other_credentials = {'username': 'otheruser', 'password': 'testpass123'}
self.other_user = get_user_model().objects.create_user(**self.other_credentials)
self.other_task = PeriodicTask.objects.create(name='Import from Trakt for otheruser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.other_user.id}, "username": "otheruser"}}', crontab=self.crontab, enabled=True)

self.assertIn('Import schedule not found', str(messages[0]))
self.assertTrue(PeriodicTask.objects.filter(id=self.task.id).exists())
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_delete_import.py:75*

### test_delete_import_schedule_other_user

**Category**: method_call  
**Description**: Test deletion of another user's import schedule.  
**Expected**: self.assertIn('Import schedule not found', str(messages[0]))  
**Confidence**: 0.85  

```python
# Setup
'Create user and test data for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.crontab = CrontabSchedule.objects.create(minute='0', hour='0', day_of_week='*', day_of_month='*', month_of_year='*')
self.task = PeriodicTask.objects.create(name='Import from Trakt for testuser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
self.other_credentials = {'username': 'otheruser', 'password': 'testpass123'}
self.other_user = get_user_model().objects.create_user(**self.other_credentials)
self.other_task = PeriodicTask.objects.create(name='Import from Trakt for otheruser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.other_user.id}, "username": "otheruser"}}', crontab=self.crontab, enabled=True)

self.assertEqual(len(messages), 1)
self.assertIn('Import schedule not found', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_delete_import.py:90*

### test_delete_import_schedule_other_user

**Category**: method_call  
**Description**: Test deletion of another user's import schedule.  
**Expected**: self.assertTrue(PeriodicTask.objects.filter(id=self.other_task.id).exists())  
**Confidence**: 0.85  

```python
# Setup
'Create user and test data for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.crontab = CrontabSchedule.objects.create(minute='0', hour='0', day_of_week='*', day_of_month='*', month_of_year='*')
self.task = PeriodicTask.objects.create(name='Import from Trakt for testuser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
self.other_credentials = {'username': 'otheruser', 'password': 'testpass123'}
self.other_user = get_user_model().objects.create_user(**self.other_credentials)
self.other_task = PeriodicTask.objects.create(name='Import from Trakt for otheruser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.other_user.id}, "username": "otheruser"}}', crontab=self.crontab, enabled=True)

self.assertIn('Import schedule not found', str(messages[0]))
self.assertTrue(PeriodicTask.objects.filter(id=self.other_task.id).exists())
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_delete_import.py:91*

### test_delete_import_schedule_success

**Category**: method_call  
**Description**: Test successful deletion of an import schedule.  
**Expected**: self.assertIn('Import schedule deleted', str(messages[0]))  
**Confidence**: 0.85  

```python
self.assertEqual(len(messages), 1)
self.assertIn('Import schedule deleted', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_delete_import.py:58*

### test_delete_import_schedule_success

**Category**: method_call  
**Description**: Test successful deletion of an import schedule.  
**Expected**: self.assertTrue(PeriodicTask.objects.filter(id=self.other_task.id).exists())  
**Confidence**: 0.85  

```python
self.assertIn('Import schedule deleted', str(messages[0]))
self.assertTrue(PeriodicTask.objects.filter(id=self.other_task.id).exists())
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_delete_import.py:59*

### test_delete_import_schedule_not_found

**Category**: method_call  
**Description**: Test deletion of a non-existent import schedule.  
**Expected**: self.assertIn('Import schedule not found', str(messages[0]))  
**Confidence**: 0.85  

```python
self.assertEqual(len(messages), 1)
self.assertIn('Import schedule not found', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_delete_import.py:74*

### test_delete_import_schedule_not_found

**Category**: method_call  
**Description**: Test deletion of a non-existent import schedule.  
**Expected**: self.assertTrue(PeriodicTask.objects.filter(id=self.task.id).exists())  
**Confidence**: 0.85  

```python
self.assertIn('Import schedule not found', str(messages[0]))
self.assertTrue(PeriodicTask.objects.filter(id=self.task.id).exists())
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_delete_import.py:75*

### test_unshown_messages_are_rendered

**Category**: method_call  
**Description**: Persistent messages should be available in the base toast UI.  
**Expected**: self.assertContains(response, 'Persistent warning')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(response.status_code, 200)
self.assertContains(response, 'Persistent warning')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_user_messages.py:27*

### test_unshown_messages_are_rendered

**Category**: method_call  
**Description**: Persistent messages should be available in the base toast UI.  
**Expected**: self.assertContains(response, reverse('mark_user_messages_shown'))  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertContains(response, 'Persistent warning')
self.assertContains(response, reverse('mark_user_messages_shown'))
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_user_messages.py:28*

### test_unshown_messages_are_rendered

**Category**: method_call  
**Description**: Persistent messages should be available in the base toast UI.  
**Expected**: self.assertContains(response, f'name="message_ids" value="{persistent_message.id}"')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertContains(response, reverse('mark_user_messages_shown'))
self.assertContains(response, f'name="message_ids" value="{persistent_message.id}"')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_user_messages.py:29*

### test_mark_user_messages_shown

**Category**: method_call  
**Description**: Posting to the mark-shown endpoint should timestamp only rendered rows.  
**Expected**: self.assertIsNotNone(first_message.shown_at)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

third_message.refresh_from_db()
self.assertIsNotNone(first_message.shown_at)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_user_messages.py:62*

### test_mark_user_messages_shown

**Category**: method_call  
**Description**: Posting to the mark-shown endpoint should timestamp only rendered rows.  
**Expected**: self.assertIsNotNone(second_message.shown_at)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertIsNotNone(first_message.shown_at)
self.assertIsNotNone(second_message.shown_at)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_user_messages.py:64*

### test_mark_user_messages_shown

**Category**: method_call  
**Description**: Posting to the mark-shown endpoint should timestamp only rendered rows.  
**Expected**: self.assertIsNone(third_message.shown_at)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertIsNotNone(second_message.shown_at)
self.assertIsNone(third_message.shown_at)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_user_messages.py:65*

### test_unshown_messages_are_rendered

**Category**: method_call  
**Description**: Persistent messages should be available in the base toast UI.  
**Expected**: self.assertContains(response, 'Persistent warning')  
**Confidence**: 0.85  

```python
self.assertEqual(response.status_code, 200)
self.assertContains(response, 'Persistent warning')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_user_messages.py:27*

### test_unshown_messages_are_rendered

**Category**: method_call  
**Description**: Persistent messages should be available in the base toast UI.  
**Expected**: self.assertContains(response, reverse('mark_user_messages_shown'))  
**Confidence**: 0.85  

```python
self.assertContains(response, 'Persistent warning')
self.assertContains(response, reverse('mark_user_messages_shown'))
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_user_messages.py:28*

### test_custom_list_form_invalid

**Category**: method_call  
**Description**: Test the form with invalid data.  
**Expected**: self.assertIn('name', form.errors)  
**Confidence**: 0.85  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertFalse(form.is_valid())
self.assertIn('name', form.errors)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_forms.py:31*

### test_custom_list_form_invalid

**Category**: method_call  
**Description**: Test the form with invalid data.  
**Expected**: self.assertIn('name', form.errors)  
**Confidence**: 0.85  

```python
self.assertFalse(form.is_valid())
self.assertIn('name', form.errors)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_forms.py:31*

### test_import_animelist

**Category**: method_call  
**Description**: Basic test importing anime and manga from MyAnimeList.  
**Expected**: self.assertEqual(Anime.objects.filter(user=self.user).count(), 5)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

mal.importer('bloodthirstiness', self.user, 'new')
self.assertEqual(Anime.objects.filter(user=self.user).count(), 5)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_mal.py:48*

### test_import_animelist

**Category**: method_call  
**Description**: Basic test importing anime and manga from MyAnimeList.  
**Expected**: self.assertEqual(Manga.objects.filter(user=self.user).count(), 3)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(Anime.objects.filter(user=self.user).count(), 5)
self.assertEqual(Manga.objects.filter(user=self.user).count(), 3)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_mal.py:49*

### test_import_animelist

**Category**: method_call  
**Description**: Basic test importing anime and manga from MyAnimeList.  
**Expected**: self.assertEqual(Anime.objects.filter(user=self.user, item__title='Ama Gli Animali').first().item.image, settings.IMG_NONE)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(Manga.objects.filter(user=self.user).count(), 3)
self.assertEqual(Anime.objects.filter(user=self.user, item__title='Ama Gli Animali').first().item.image, settings.IMG_NONE)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_mal.py:50*

### test_import_animelist

**Category**: method_call  
**Description**: Basic test importing anime and manga from MyAnimeList.  
**Expected**: self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').status, Status.PAUSED.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(Anime.objects.filter(user=self.user, item__title='Ama Gli Animali').first().item.image, settings.IMG_NONE)
self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').status, Status.PAUSED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_mal.py:52*

### test_import_animelist

**Category**: method_call  
**Description**: Basic test importing anime and manga from MyAnimeList.  
**Expected**: self.assertEqual(Manga.objects.get(user=self.user, item__title='Fire Punch').score, 7)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').status, Status.PAUSED.value)
self.assertEqual(Manga.objects.get(user=self.user, item__title='Fire Punch').score, 7)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_mal.py:61*

### test_import_animelist

**Category**: method_call  
**Description**: Basic test importing anime and manga from MyAnimeList.  
**Expected**: self.assertEqual(Anime.objects.filter(user=self.user, item__title='Chainsaw Man').first().history.first().history_date, datetime(2022, 12, 28, 19, 20, 54, tzinfo=UTC))  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(Manga.objects.get(user=self.user, item__title='Fire Punch').score, 7)
self.assertEqual(Anime.objects.filter(user=self.user, item__title='Chainsaw Man').first().history.first().history_date, datetime(2022, 12, 28, 19, 20, 54, tzinfo=UTC))
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_mal.py:65*

### test_import_animelist

**Category**: method_call  
**Description**: Basic test importing anime and manga from MyAnimeList.  
**Expected**: self.assertEqual(Anime.objects.filter(user=self.user).count(), 5)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
# Fixtures: mock_request

mal.importer('bloodthirstiness', self.user, 'new')
self.assertEqual(Anime.objects.filter(user=self.user).count(), 5)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_mal.py:48*

### test_import_animelist

**Category**: method_call  
**Description**: Basic test importing anime and manga from MyAnimeList.  
**Expected**: self.assertEqual(Manga.objects.filter(user=self.user).count(), 3)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
# Fixtures: mock_request

self.assertEqual(Anime.objects.filter(user=self.user).count(), 5)
self.assertEqual(Manga.objects.filter(user=self.user).count(), 3)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_mal.py:49*

### test_import_animelist

**Category**: method_call  
**Description**: Basic test importing anime and manga from MyAnimeList.  
**Expected**: self.assertEqual(Anime.objects.filter(user=self.user, item__title='Ama Gli Animali').first().item.image, settings.IMG_NONE)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
# Fixtures: mock_request

self.assertEqual(Manga.objects.filter(user=self.user).count(), 3)
self.assertEqual(Anime.objects.filter(user=self.user, item__title='Ama Gli Animali').first().item.image, settings.IMG_NONE)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_mal.py:50*

### test_import_animelist

**Category**: method_call  
**Description**: Basic test importing anime and manga from MyAnimeList.  
**Expected**: self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').status, Status.PAUSED.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
# Fixtures: mock_request

self.assertEqual(Anime.objects.filter(user=self.user, item__title='Ama Gli Animali').first().item.image, settings.IMG_NONE)
self.assertEqual(Anime.objects.get(user=self.user, item__title='FLCL').status, Status.PAUSED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_mal.py:52*

### test_media_date_fields_are_optional

**Category**: method_call  
**Description**: Start and end dates should remain optional in tracking forms.  
**Expected**: self.assertFalse(form.fields['end_date'].required)  
**Confidence**: 0.85  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/image.jpg')
Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test tv', image='http://example.com/image.jpg')

self.assertFalse(form.fields['start_date'].required)
self.assertFalse(form.fields['end_date'].required)
```

*Source: C:\yamtrack-fork\src\app\tests\test_forms.py:77*

### test_default_progress

**Category**: method_call  
**Description**: Test the game form using the default progress format.  
**Expected**: self.assertEqual(form.cleaned_data['progress'], 1500)  
**Confidence**: 0.85  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Test Game', image='http://example.com/image.jpg')

self.assertTrue(form.is_valid())
self.assertEqual(form.cleaned_data['progress'], 1500)
```

*Source: C:\yamtrack-fork\src\app\tests\test_forms.py:140*

### test_plain_number_progress

**Category**: method_call  
**Description**: Test the game form with a plain number for hours (e.g., '5').  
**Expected**: self.assertEqual(form.cleaned_data['progress'], 300)  
**Confidence**: 0.85  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Test Game', image='http://example.com/image.jpg')

self.assertTrue(form.is_valid())
self.assertEqual(form.cleaned_data['progress'], 300)
```

*Source: C:\yamtrack-fork\src\app\tests\test_forms.py:155*

### test_alternate_progress

**Category**: method_call  
**Description**: Test the game form using an alternate progress format.  
**Expected**: self.assertEqual(form.cleaned_data['progress'], 1500)  
**Confidence**: 0.85  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Test Game', image='http://example.com/image.jpg')

self.assertTrue(form.is_valid())
self.assertEqual(form.cleaned_data['progress'], 1500)
```

*Source: C:\yamtrack-fork\src\app\tests\test_forms.py:170*

### test_second_alternate_progress

**Category**: method_call  
**Description**: Test the game form using a second alternate progress format.  
**Expected**: self.assertEqual(form.cleaned_data['progress'], 30)  
**Confidence**: 0.85  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Test Game', image='http://example.com/image.jpg')

self.assertTrue(form.is_valid())
self.assertEqual(form.cleaned_data['progress'], 30)
```

*Source: C:\yamtrack-fork\src\app\tests\test_forms.py:185*

### test_third_alternate_progress

**Category**: method_call  
**Description**: Test the game form using a second alternate progress format.  
**Expected**: self.assertEqual(form.cleaned_data['progress'], 540)  
**Confidence**: 0.85  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Test Game', image='http://example.com/image.jpg')

self.assertTrue(form.is_valid())
self.assertEqual(form.cleaned_data['progress'], 540)
```

*Source: C:\yamtrack-fork\src\app\tests\test_forms.py:200*

### test_fourth_alternate_progress

**Category**: method_call  
**Description**: Test the game form using a second alternate progress format.  
**Expected**: self.assertEqual(form.cleaned_data['progress'], 570)  
**Confidence**: 0.85  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Test Game', image='http://example.com/image.jpg')

self.assertTrue(form.is_valid())
self.assertEqual(form.cleaned_data['progress'], 570)
```

*Source: C:\yamtrack-fork\src\app\tests\test_forms.py:215*

### test_float_progress

**Category**: method_call  
**Description**: Test the game form with float progress format (e.g., 1.5 hours).  
**Expected**: self.assertEqual(form.cleaned_data['progress'], 90)  
**Confidence**: 0.85  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.item = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='Test Game', image='http://example.com/image.jpg')

self.assertTrue(form.is_valid())
self.assertEqual(form.cleaned_data['progress'], 90)
```

*Source: C:\yamtrack-fork\src\app\tests\test_forms.py:230*

### test_import_imdb_csv

**Category**: method_call  
**Description**: Test importing movies and TV shows from IMDB CSV.  
**Expected**: self.assertEqual(imported_counts[MediaTypes.TV.value], 2)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_imdb.csv').open('rb') as file:
    self.import_results = imdb.importer(file, self.user, 'new')

self.assertEqual(imported_counts[MediaTypes.MOVIE.value], 5)
self.assertEqual(imported_counts[MediaTypes.TV.value], 2)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_imdb.py:39*

### test_import_imdb_csv

**Category**: method_call  
**Description**: Test importing movies and TV shows from IMDB CSV.  
**Expected**: self.assertIn("The Last of Us: Unsupported title type 'Video Game' - skipped", warnings)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_imdb.csv').open('rb') as file:
    self.import_results = imdb.importer(file, self.user, 'new')

self.assertEqual(imported_counts[MediaTypes.TV.value], 2)
self.assertIn("The Last of Us: Unsupported title type 'Video Game' - skipped", warnings)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_imdb.py:40*

### test_import_imdb_csv

**Category**: method_call  
**Description**: Test importing movies and TV shows from IMDB CSV.  
**Expected**: self.assertEqual(movie_1.status, Status.COMPLETED.value)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_imdb.csv').open('rb') as file:
    self.import_results = imdb.importer(file, self.user, 'new')

self.assertEqual(movie_1.score, 9)
self.assertEqual(movie_1.status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_imdb.py:48*

### test_import_imdb_csv

**Category**: method_call  
**Description**: Test importing movies and TV shows from IMDB CSV.  
**Expected**: self.assertEqual(movie_1.progress, 1)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_imdb.csv').open('rb') as file:
    self.import_results = imdb.importer(file, self.user, 'new')

self.assertEqual(movie_1.status, Status.COMPLETED.value)
self.assertEqual(movie_1.progress, 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_imdb.py:49*

### test_import_imdb_csv

**Category**: method_call  
**Description**: Test importing movies and TV shows from IMDB CSV.  
**Expected**: self.assertEqual(movie_1.end_date, datetime(2025, 2, 3, tzinfo=timezone.get_current_timezone()))  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_imdb.csv').open('rb') as file:
    self.import_results = imdb.importer(file, self.user, 'new')

self.assertEqual(movie_1.progress, 1)
self.assertEqual(movie_1.end_date, datetime(2025, 2, 3, tzinfo=timezone.get_current_timezone()))
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_imdb.py:50*

### test_extract_imdb_id

**Category**: method_call  
**Description**: Test IMDB ID extraction and formatting.  
**Expected**: self.assertEqual(importer_instance._extract_imdb_id({'Const': '0111161'}), 'tt0111161')  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_imdb.csv').open('rb') as file:
    self.import_results = imdb.importer(file, self.user, 'new')

self.assertEqual(importer_instance._extract_imdb_id({'Const': 'tt0111161'}), 'tt0111161')
self.assertEqual(importer_instance._extract_imdb_id({'Const': '0111161'}), 'tt0111161')
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_imdb.py:63*

### test_extract_imdb_id

**Category**: method_call  
**Description**: Test IMDB ID extraction and formatting.  
**Expected**: self.assertIsNone(importer_instance._extract_imdb_id({'Const': ''}))  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_imdb.csv').open('rb') as file:
    self.import_results = imdb.importer(file, self.user, 'new')

self.assertEqual(importer_instance._extract_imdb_id({'Const': '0111161'}), 'tt0111161')
self.assertIsNone(importer_instance._extract_imdb_id({'Const': ''}))
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_imdb.py:67*

### test_extract_imdb_id

**Category**: method_call  
**Description**: Test IMDB ID extraction and formatting.  
**Expected**: self.assertIsNone(importer_instance._extract_imdb_id({'Const': 'invalid'}))  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_imdb.csv').open('rb') as file:
    self.import_results = imdb.importer(file, self.user, 'new')

self.assertIsNone(importer_instance._extract_imdb_id({'Const': ''}))
self.assertIsNone(importer_instance._extract_imdb_id({'Const': 'invalid'}))
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_imdb.py:71*

### test_parse_rating

**Category**: method_call  
**Description**: Test rating parsing.  
**Expected**: self.assertEqual(importer_instance._parse_rating('10'), 10.0)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_imdb.csv').open('rb') as file:
    self.import_results = imdb.importer(file, self.user, 'new')

self.assertEqual(importer_instance._parse_rating('8.5'), 8.5)
self.assertEqual(importer_instance._parse_rating('10'), 10.0)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_imdb.py:79*

### test_parse_rating

**Category**: method_call  
**Description**: Test rating parsing.  
**Expected**: self.assertEqual(importer_instance._parse_rating('1'), 1.0)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_imdb.csv').open('rb') as file:
    self.import_results = imdb.importer(file, self.user, 'new')

self.assertEqual(importer_instance._parse_rating('10'), 10.0)
self.assertEqual(importer_instance._parse_rating('1'), 1.0)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_imdb.py:80*

### test_media_details_view

**Category**: method_call  
**Description**: Test the media details view.  
**Expected**: self.assertTemplateUsed(response, 'app/media_details.html')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/media_details.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_details.py:47*

### test_media_details_view

**Category**: method_call  
**Description**: Test the media details view.  
**Expected**: self.assertIn('media', response.context)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertTemplateUsed(response, 'app/media_details.html')
self.assertIn('media', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_details.py:48*

### test_media_details_view

**Category**: method_call  
**Description**: Test the media details view.  
**Expected**: self.assertEqual(response.context['media']['title'], 'Test Movie')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertIn('media', response.context)
self.assertEqual(response.context['media']['title'], 'Test Movie')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_details.py:50*

### test_media_details_view

**Category**: method_call  
**Description**: Test the media details view.  
**Expected**: mock_get_metadata.assert_called_once_with(MediaTypes.MOVIE.value, '238', Sources.TMDB.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(response.context['media']['title'], 'Test Movie')
mock_get_metadata.assert_called_once_with(MediaTypes.MOVIE.value, '238', Sources.TMDB.value)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_details.py:51*

### test_season_details_view

**Category**: method_call  
**Description**: Test the season details view.  
**Expected**: self.assertTemplateUsed(response, 'app/media_details.html')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/media_details.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_details.py:104*

### test_season_details_view

**Category**: method_call  
**Description**: Test the season details view.  
**Expected**: self.assertIn('media', response.context)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertTemplateUsed(response, 'app/media_details.html')
self.assertIn('media', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_details.py:105*

### test_season_details_view

**Category**: method_call  
**Description**: Test the season details view.  
**Expected**: self.assertEqual(response.context['media']['title'], 'Season 1')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertIn('media', response.context)
self.assertEqual(response.context['media']['title'], 'Season 1')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_details.py:107*

### test_season_details_view

**Category**: method_call  
**Description**: Test the season details view.  
**Expected**: self.assertEqual(len(response.context['media']['episodes']), 1)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(response.context['media']['title'], 'Season 1')
self.assertEqual(len(response.context['media']['episodes']), 1)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_details.py:108*

### test_season_details_view

**Category**: method_call  
**Description**: Test the season details view.  
**Expected**: mock_get_metadata.assert_called_once_with('tv_with_seasons', '1668', Sources.TMDB.value, [1])  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(len(response.context['media']['episodes']), 1)
mock_get_metadata.assert_called_once_with('tv_with_seasons', '1668', Sources.TMDB.value, [1])
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_details.py:109*

### test_media_details_view

**Category**: method_call  
**Description**: Test the media details view.  
**Expected**: self.assertTemplateUsed(response, 'app/media_details.html')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
# Fixtures: mock_get_metadata

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/media_details.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_details.py:47*

### test_blank_modal

**Category**: method_call  
**Description**: Test the blank modal for creating a list.  
**Expected**: expect(self.page.locator('#lists-anime-437')).to_contain_text("You haven't created any lists yet.")  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.locator('.absolute > .relative > button:nth-child(2)').first.click()
expect(self.page.locator('#lists-anime-437')).to_contain_text("You haven't created any lists yet.")
```

*Source: C:\yamtrack-fork\src\lists\tests\test_integration.py:50*

### test_flow

**Category**: method_call  
**Description**: Test the flow of adding an item to a list and editing the list.  
**Expected**: expect(self.page.locator('h2')).to_contain_text('Create New List')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.get_by_role('button', name='New List').click()
expect(self.page.locator('h2')).to_contain_text('Create New List')
```

*Source: C:\yamtrack-fork\src\lists\tests\test_integration.py:59*

### test_flow

**Category**: method_call  
**Description**: Test the flow of adding an item to a list and editing the list.  
**Expected**: expect(self.page.locator('#lists-grid div').filter(has_text='T 0 items').nth(1)).to_be_visible()  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.get_by_role('button', name='Create List').click()
expect(self.page.locator('#lists-grid div').filter(has_text='T 0 items').nth(1)).to_be_visible()
```

*Source: C:\yamtrack-fork\src\lists\tests\test_integration.py:63*

### test_flow

**Category**: method_call  
**Description**: Test the flow of adding an item to a list and editing the list.  
**Expected**: expect(self.page.locator('#lists-anime-437')).to_contain_text('Lists test Add')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.locator('.absolute > .relative > button:nth-child(2)').first.click()
expect(self.page.locator('#lists-anime-437')).to_contain_text('Lists test Add')
```

*Source: C:\yamtrack-fork\src\lists\tests\test_integration.py:76*

### test_flow

**Category**: method_call  
**Description**: Test the flow of adding an item to a list and editing the list.  
**Expected**: expect(self.page.locator('#lists-anime-437')).to_contain_text('Remove')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.get_by_role('button', name='Add', exact=True).click()
expect(self.page.locator('#lists-anime-437')).to_contain_text('Remove')
```

*Source: C:\yamtrack-fork\src\lists\tests\test_integration.py:78*

### test_flow

**Category**: method_call  
**Description**: Test the flow of adding an item to a list and editing the list.  
**Expected**: expect(self.page.locator('#lists-grid div').filter(has_text='T 1 item').nth(1)).to_be_visible()  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.get_by_role('link', name='Lists').click()
expect(self.page.locator('#lists-grid div').filter(has_text='T 1 item').nth(1)).to_be_visible()
```

*Source: C:\yamtrack-fork\src\lists\tests\test_integration.py:83*

### test_flow

**Category**: method_call  
**Description**: Test the flow of adding an item to a list and editing the list.  
**Expected**: expect(self.page.locator('#lists-grid')).to_contain_text('Edit List')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.get_by_role('button', name='Edit list').click()
expect(self.page.locator('#lists-grid')).to_contain_text('Edit List')
```

*Source: C:\yamtrack-fork\src\lists\tests\test_integration.py:87*

### test_blank_modal

**Category**: method_call  
**Description**: Test the blank modal for creating a list.  
**Expected**: expect(self.page.locator('#lists-anime-437')).to_contain_text("You haven't created any lists yet.")  
**Confidence**: 0.85  

```python
self.page.locator('.absolute > .relative > button:nth-child(2)').first.click()
expect(self.page.locator('#lists-anime-437')).to_contain_text("You haven't created any lists yet.")
```

*Source: C:\yamtrack-fork\src\lists\tests\test_integration.py:50*

### test_flow

**Category**: method_call  
**Description**: Test the flow of adding an item to a list and editing the list.  
**Expected**: expect(self.page.locator('h2')).to_contain_text('Create New List')  
**Confidence**: 0.85  

```python
self.page.get_by_role('button', name='New List').click()
expect(self.page.locator('h2')).to_contain_text('Create New List')
```

*Source: C:\yamtrack-fork\src\lists\tests\test_integration.py:59*

### test_flow

**Category**: method_call  
**Description**: Test the flow of adding an item to a list and editing the list.  
**Expected**: expect(self.page.locator('#lists-grid div').filter(has_text='T 0 items').nth(1)).to_be_visible()  
**Confidence**: 0.85  

```python
self.page.get_by_role('button', name='Create List').click()
expect(self.page.locator('#lists-grid div').filter(has_text='T 0 items').nth(1)).to_be_visible()
```

*Source: C:\yamtrack-fork\src\lists\tests\test_integration.py:63*

### test_api_request_get

**Category**: method_call  
**Description**: Test the api_request function with GET method.  
**Expected**: mock_get.assert_called_once()  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(result, {'data': 'test'})
mock_get.assert_called_once()
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_services.py:35*

### test_api_request_get

**Category**: method_call  
**Description**: Test the api_request function with GET method.  
**Expected**: self.assertEqual(kwargs['params'], {'param': 'value'})  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(kwargs['url'], 'https://example.com/api')
self.assertEqual(kwargs['params'], {'param': 'value'})
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_services.py:39*

### test_api_request_get

**Category**: method_call  
**Description**: Test the api_request function with GET method.  
**Expected**: self.assertIn('timeout', kwargs)  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(kwargs['params'], {'param': 'value'})
self.assertIn('timeout', kwargs)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_services.py:40*

### test_api_request_post

**Category**: method_call  
**Description**: Test the api_request function with POST method.  
**Expected**: mock_post.assert_called_once()  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(result, {'data': 'test'})
mock_post.assert_called_once()
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_services.py:58*

### test_api_request_post

**Category**: method_call  
**Description**: Test the api_request function with POST method.  
**Expected**: self.assertEqual(kwargs['json'], {'json_param': 'value'})  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(kwargs['url'], 'https://example.com/api')
self.assertEqual(kwargs['json'], {'json_param': 'value'})
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_services.py:62*

### test_api_request_post

**Category**: method_call  
**Description**: Test the api_request function with POST method.  
**Expected**: self.assertEqual(kwargs['data'], {'form_data': 'value'})  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(kwargs['json'], {'json_param': 'value'})
self.assertEqual(kwargs['data'], {'form_data': 'value'})
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_services.py:63*

### test_api_request_post

**Category**: method_call  
**Description**: Test the api_request function with POST method.  
**Expected**: self.assertIn('timeout', kwargs)  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(kwargs['data'], {'form_data': 'value'})
self.assertIn('timeout', kwargs)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_services.py:64*

### test_request_error_handling_rate_limit

**Category**: method_call  
**Description**: Test the request_error_handling function with rate limiting.  
**Expected**: self.assertEqual(result, {'data': 'retry_success'})  
**Confidence**: 0.85  
**Tags**: mock  

```python
mock_api_request.assert_called_once()
self.assertEqual(result, {'data': 'retry_success'})
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_services.py:89*

### test_handle_error_igdb_unauthorized

**Category**: method_call  
**Description**: Test the handle_error function with IGDB unauthorized error.  
**Expected**: self.assertEqual(result, {'retry': True})  
**Confidence**: 0.85  
**Tags**: mock  

```python
mock_cache_delete.assert_called_once_with('igdb_access_token')
self.assertEqual(result, {'retry': True})
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_services.py:107*

### test_get_media_metadata_anime

**Category**: method_call  
**Description**: Test the get_media_metadata function for anime.  
**Expected**: mock_anime.assert_called_once_with('1')  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(result, {'title': 'Test Anime'})
mock_anime.assert_called_once_with('1')
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_services.py:164*

### test_no_underscore

**Category**: method_call  
**Description**: Test the no_underscore filter.  
**Expected**: self.assertEqual(app_tags.no_underscore('test_string_with_underscores'), 'test string with underscores')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.tv_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.season_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.tv_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'title': 'Test TV Show'}
self.season_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.SEASON.value, 'title': 'Test TV Show', 'season_number': 1}
self.episode_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.EPISODE.value, 'title': 'Test TV Show', 'season_number': 1, 'episode_number': 1}

self.assertEqual(app_tags.no_underscore('hello_world'), 'hello world')
self.assertEqual(app_tags.no_underscore('test_string_with_underscores'), 'test string with underscores')
```

*Source: C:\yamtrack-fork\src\app\tests\test_templatetags.py:95*

### test_no_underscore

**Category**: method_call  
**Description**: Test the no_underscore filter.  
**Expected**: self.assertEqual(app_tags.no_underscore('no_underscores_here'), 'no underscores here')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.tv_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.season_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.tv_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'title': 'Test TV Show'}
self.season_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.SEASON.value, 'title': 'Test TV Show', 'season_number': 1}
self.episode_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.EPISODE.value, 'title': 'Test TV Show', 'season_number': 1, 'episode_number': 1}

self.assertEqual(app_tags.no_underscore('test_string_with_underscores'), 'test string with underscores')
self.assertEqual(app_tags.no_underscore('no_underscores_here'), 'no underscores here')
```

*Source: C:\yamtrack-fork\src\app\tests\test_templatetags.py:96*

### test_slug

**Category**: method_call  
**Description**: Test the slug filter.  
**Expected**: self.assertEqual(app_tags.slug('Anime: 31687'), 'anime-31687')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.tv_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.season_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.tv_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'title': 'Test TV Show'}
self.season_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.SEASON.value, 'title': 'Test TV Show', 'season_number': 1}
self.episode_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.EPISODE.value, 'title': 'Test TV Show', 'season_number': 1, 'episode_number': 1}

self.assertEqual(app_tags.slug('Hello World'), 'hello-world')
self.assertEqual(app_tags.slug('Anime: 31687'), 'anime-31687')
```

*Source: C:\yamtrack-fork\src\app\tests\test_templatetags.py:108*

### test_slug

**Category**: method_call  
**Description**: Test the slug filter.  
**Expected**: self.assertEqual(app_tags.slug('★★★'), '%E2%98%85%E2%98%85%E2%98%85')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.tv_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.season_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', season_number=1)
self.episode_item = Item(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', season_number=1, episode_number=1)
self.tv_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'title': 'Test TV Show'}
self.season_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.SEASON.value, 'title': 'Test TV Show', 'season_number': 1}
self.episode_dict = {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.EPISODE.value, 'title': 'Test TV Show', 'season_number': 1, 'episode_number': 1}

self.assertEqual(app_tags.slug('Anime: 31687'), 'anime-31687')
self.assertEqual(app_tags.slug('★★★'), '%E2%98%85%E2%98%85%E2%98%85')
```

*Source: C:\yamtrack-fork\src\app\tests\test_templatetags.py:111*

### test_media_list_view

**Category**: method_call  
**Description**: Test the media list view displays media items.  
**Expected**: self.assertTemplateUsed(response, 'app/media_list.html')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
movies_id = ['278', '238', '129', '424', '680']
num_completed = 3
for i in range(1, 6):
    item = Item.objects.create(media_id=movies_id[i - 1], source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title=f'Test Movie {i}', image='http://example.com/image.jpg')
    status = Status.COMPLETED.value if i < num_completed else Status.IN_PROGRESS.value
    Movie.objects.create(item=item, user=self.user, status=status, progress=1 if i < num_completed else 0, score=i)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/media_list.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_list.py:51*

### test_media_list_view

**Category**: method_call  
**Description**: Test the media list view displays media items.  
**Expected**: self.assertIn('media_list', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
movies_id = ['278', '238', '129', '424', '680']
num_completed = 3
for i in range(1, 6):
    item = Item.objects.create(media_id=movies_id[i - 1], source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title=f'Test Movie {i}', image='http://example.com/image.jpg')
    status = Status.COMPLETED.value if i < num_completed else Status.IN_PROGRESS.value
    Movie.objects.create(item=item, user=self.user, status=status, progress=1 if i < num_completed else 0, score=i)

self.assertTemplateUsed(response, 'app/media_list.html')
self.assertIn('media_list', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_list.py:52*

### test_media_list_view

**Category**: method_call  
**Description**: Test the media list view displays media items.  
**Expected**: self.assertEqual(response.context['media_list'].paginator.count, 5)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
movies_id = ['278', '238', '129', '424', '680']
num_completed = 3
for i in range(1, 6):
    item = Item.objects.create(media_id=movies_id[i - 1], source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title=f'Test Movie {i}', image='http://example.com/image.jpg')
    status = Status.COMPLETED.value if i < num_completed else Status.IN_PROGRESS.value
    Movie.objects.create(item=item, user=self.user, status=status, progress=1 if i < num_completed else 0, score=i)

self.assertIn('media_list', response.context)
self.assertEqual(response.context['media_list'].paginator.count, 5)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_list.py:54*

### test_media_list_view

**Category**: method_call  
**Description**: Test the media list view displays media items.  
**Expected**: self.assertIn('sort_choices', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
movies_id = ['278', '238', '129', '424', '680']
num_completed = 3
for i in range(1, 6):
    item = Item.objects.create(media_id=movies_id[i - 1], source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title=f'Test Movie {i}', image='http://example.com/image.jpg')
    status = Status.COMPLETED.value if i < num_completed else Status.IN_PROGRESS.value
    Movie.objects.create(item=item, user=self.user, status=status, progress=1 if i < num_completed else 0, score=i)

self.assertEqual(response.context['media_list'].paginator.count, 5)
self.assertIn('sort_choices', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_list.py:55*

### test_media_list_view

**Category**: method_call  
**Description**: Test the media list view displays media items.  
**Expected**: self.assertIn('status_choices', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
movies_id = ['278', '238', '129', '424', '680']
num_completed = 3
for i in range(1, 6):
    item = Item.objects.create(media_id=movies_id[i - 1], source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title=f'Test Movie {i}', image='http://example.com/image.jpg')
    status = Status.COMPLETED.value if i < num_completed else Status.IN_PROGRESS.value
    Movie.objects.create(item=item, user=self.user, status=status, progress=1 if i < num_completed else 0, score=i)

self.assertIn('sort_choices', response.context)
self.assertIn('status_choices', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_list.py:57*

### test_media_list_view

**Category**: method_call  
**Description**: Test the media list view displays media items.  
**Expected**: self.assertEqual(response.context['media_type'], MediaTypes.MOVIE.value)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
movies_id = ['278', '238', '129', '424', '680']
num_completed = 3
for i in range(1, 6):
    item = Item.objects.create(media_id=movies_id[i - 1], source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title=f'Test Movie {i}', image='http://example.com/image.jpg')
    status = Status.COMPLETED.value if i < num_completed else Status.IN_PROGRESS.value
    Movie.objects.create(item=item, user=self.user, status=status, progress=1 if i < num_completed else 0, score=i)

self.assertIn('status_choices', response.context)
self.assertEqual(response.context['media_type'], MediaTypes.MOVIE.value)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_list.py:58*

### test_media_list_view

**Category**: method_call  
**Description**: Test the media list view displays media items.  
**Expected**: self.assertEqual(response.context['media_type_plural'], app_tags.media_type_readable_plural(MediaTypes.MOVIE.value).lower())  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
movies_id = ['278', '238', '129', '424', '680']
num_completed = 3
for i in range(1, 6):
    item = Item.objects.create(media_id=movies_id[i - 1], source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title=f'Test Movie {i}', image='http://example.com/image.jpg')
    status = Status.COMPLETED.value if i < num_completed else Status.IN_PROGRESS.value
    Movie.objects.create(item=item, user=self.user, status=status, progress=1 if i < num_completed else 0, score=i)

self.assertEqual(response.context['media_type'], MediaTypes.MOVIE.value)
self.assertEqual(response.context['media_type_plural'], app_tags.media_type_readable_plural(MediaTypes.MOVIE.value).lower())
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_list.py:59*

### test_media_list_with_filters

**Category**: method_call  
**Description**: Test the media list view with filters.  
**Expected**: self.assertEqual(response.context['current_status'], Status.COMPLETED.value)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
movies_id = ['278', '238', '129', '424', '680']
num_completed = 3
for i in range(1, 6):
    item = Item.objects.create(media_id=movies_id[i - 1], source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title=f'Test Movie {i}', image='http://example.com/image.jpg')
    status = Status.COMPLETED.value if i < num_completed else Status.IN_PROGRESS.value
    Movie.objects.create(item=item, user=self.user, status=status, progress=1 if i < num_completed else 0, score=i)

self.assertEqual(response.status_code, 200)
self.assertEqual(response.context['current_status'], Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_list.py:72*

### test_media_list_with_filters

**Category**: method_call  
**Description**: Test the media list view with filters.  
**Expected**: self.assertEqual(response.context['current_sort'], 'score')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
movies_id = ['278', '238', '129', '424', '680']
num_completed = 3
for i in range(1, 6):
    item = Item.objects.create(media_id=movies_id[i - 1], source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title=f'Test Movie {i}', image='http://example.com/image.jpg')
    status = Status.COMPLETED.value if i < num_completed else Status.IN_PROGRESS.value
    Movie.objects.create(item=item, user=self.user, status=status, progress=1 if i < num_completed else 0, score=i)

self.assertEqual(response.context['current_status'], Status.COMPLETED.value)
self.assertEqual(response.context['current_sort'], 'score')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_list.py:74*

### test_media_list_with_filters

**Category**: method_call  
**Description**: Test the media list view with filters.  
**Expected**: self.assertEqual(response.context['current_layout'], 'table')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
movies_id = ['278', '238', '129', '424', '680']
num_completed = 3
for i in range(1, 6):
    item = Item.objects.create(media_id=movies_id[i - 1], source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title=f'Test Movie {i}', image='http://example.com/image.jpg')
    status = Status.COMPLETED.value if i < num_completed else Status.IN_PROGRESS.value
    Movie.objects.create(item=item, user=self.user, status=status, progress=1 if i < num_completed else 0, score=i)

self.assertEqual(response.context['current_sort'], 'score')
self.assertEqual(response.context['current_layout'], 'table')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_list.py:78*

### test_season_progress_edit

**Category**: method_call  
**Description**: Test the progress edit of a season.  
**Expected**: expect(self.page.locator('h2')).to_contain_text('Search Results')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.get_by_role('button').nth(1).click()
expect(self.page.locator('h2')).to_contain_text('Search Results')
```

*Source: C:\yamtrack-fork\src\app\tests\test_integration.py:46*

### test_season_progress_edit

**Category**: method_call  
**Description**: Test the progress edit of a season.  
**Expected**: expect(self.page.get_by_role('main')).to_contain_text('Breaking Bad')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.get_by_title('Breaking Bad', exact=True).click()
expect(self.page.get_by_role('main')).to_contain_text('Breaking Bad')
```

*Source: C:\yamtrack-fork\src\app\tests\test_integration.py:48*

### test_season_progress_edit

**Category**: method_call  
**Description**: Test the progress edit of a season.  
**Expected**: expect(self.page.get_by_role('main')).to_contain_text('Season 1')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.get_by_title('Season 1').click()
expect(self.page.get_by_role('main')).to_contain_text('Season 1')
```

*Source: C:\yamtrack-fork\src\app\tests\test_integration.py:50*

### test_season_progress_edit

**Category**: method_call  
**Description**: Test the progress edit of a season.  
**Expected**: expect(self.page.get_by_role('main')).to_contain_text('Track Episode')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.locator('.p-2').first.click()
expect(self.page.get_by_role('main')).to_contain_text('Track Episode')
```

*Source: C:\yamtrack-fork\src\app\tests\test_integration.py:52*

### test_season_progress_edit

**Category**: method_call  
**Description**: Test the progress edit of a season.  
**Expected**: expect(self.page.get_by_text('Breaking Bad S1')).to_be_visible()  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.get_by_role('link', name='Home').click()
expect(self.page.get_by_text('Breaking Bad S1')).to_be_visible()
```

*Source: C:\yamtrack-fork\src\app\tests\test_integration.py:66*

### test_tv_completed

**Category**: method_call  
**Description**: Test the completed status of a TV show.  
**Expected**: expect(self.page.locator('h2')).to_contain_text('Search Results')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.locator('form').filter(has_text='TV Shows TV').get_by_role('button').first.click()
expect(self.page.locator('h2')).to_contain_text('Search Results')
```

*Source: C:\yamtrack-fork\src\app\tests\test_integration.py:80*

### test_tv_completed

**Category**: method_call  
**Description**: Test the completed status of a TV show.  
**Expected**: expect(self.page.get_by_role('main')).to_contain_text('Breaking Bad')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.get_by_title('Breaking Bad', exact=True).click()
expect(self.page.get_by_role('main')).to_contain_text('Breaking Bad')
```

*Source: C:\yamtrack-fork\src\app\tests\test_integration.py:84*

### test_tv_completed

**Category**: method_call  
**Description**: Test the completed status of a TV show.  
**Expected**: expect(self.page.locator('#track-tv-1396')).to_contain_text('Score')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.locator('button').filter(has_text='Add to tracker').click()
expect(self.page.locator('#track-tv-1396')).to_contain_text('Score')
```

*Source: C:\yamtrack-fork\src\app\tests\test_integration.py:86*

### test_tv_completed

**Category**: method_call  
**Description**: Test the completed status of a TV show.  
**Expected**: expect(self.page.locator('tbody')).to_contain_text('62')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.get_by_role('link', name='Table View').click()
expect(self.page.locator('tbody')).to_contain_text('62')
```

*Source: C:\yamtrack-fork\src\app\tests\test_integration.py:91*

### test_season_completed

**Category**: method_call  
**Description**: Test the completed status of a season.  
**Expected**: expect(self.page.locator('h2')).to_contain_text('Search Results')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for CustomList model.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.page.goto(f'{self.live_server_url}/')
self.page.get_by_placeholder('Enter your username').fill(self.credentials['username'])
self.page.get_by_placeholder('Enter your password').fill(self.credentials['password'])
self.page.get_by_role('button', name='Sign in').click()

self.page.get_by_role('button').nth(1).click()
expect(self.page.locator('h2')).to_contain_text('Search Results')
```

*Source: C:\yamtrack-fork\src\app\tests\test_integration.py:97*

### test_date_parser_supports_year_only_dates

**Category**: method_call  
**Description**: Year-only dates should default to January 1st.  
**Expected**: self.assertEqual(parsed.month, 1)  
**Confidence**: 0.85  

```python
self.assertEqual(parsed.year, 2025)
self.assertEqual(parsed.month, 1)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_helpers.py:14*

### test_date_parser_supports_year_only_dates

**Category**: method_call  
**Description**: Year-only dates should default to January 1st.  
**Expected**: self.assertEqual(parsed.day, 1)  
**Confidence**: 0.85  

```python
self.assertEqual(parsed.month, 1)
self.assertEqual(parsed.day, 1)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_helpers.py:15*

### test_date_parser_supports_year_only_dates

**Category**: method_call  
**Description**: Year-only dates should default to January 1st.  
**Expected**: self.assertEqual(parsed.hour, SentinelDatetime.HOUR)  
**Confidence**: 0.85  

```python
self.assertEqual(parsed.day, 1)
self.assertEqual(parsed.hour, SentinelDatetime.HOUR)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_helpers.py:16*

### test_date_parser_supports_year_month_dates

**Category**: method_call  
**Description**: Year-month dates should default to the first day of the month.  
**Expected**: self.assertEqual(parsed.month, 3)  
**Confidence**: 0.85  

```python
self.assertEqual(parsed.year, 2025)
self.assertEqual(parsed.month, 3)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_helpers.py:23*

### test_date_parser_supports_year_month_dates

**Category**: method_call  
**Description**: Year-month dates should default to the first day of the month.  
**Expected**: self.assertEqual(parsed.day, 1)  
**Confidence**: 0.85  

```python
self.assertEqual(parsed.month, 3)
self.assertEqual(parsed.day, 1)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_helpers.py:24*

### test_date_parser_supports_year_month_dates

**Category**: method_call  
**Description**: Year-month dates should default to the first day of the month.  
**Expected**: self.assertEqual(parsed.minute, SentinelDatetime.MINUTE)  
**Confidence**: 0.85  

```python
self.assertEqual(parsed.day, 1)
self.assertEqual(parsed.minute, SentinelDatetime.MINUTE)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_helpers.py:25*

### test_date_parser_supports_year_only_dates

**Category**: method_call  
**Description**: Year-only dates should default to January 1st.  
**Expected**: self.assertEqual(parsed.month, 1)  
**Confidence**: 0.85  

```python
self.assertEqual(parsed.year, 2025)
self.assertEqual(parsed.month, 1)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_helpers.py:14*

### test_date_parser_supports_year_only_dates

**Category**: method_call  
**Description**: Year-only dates should default to January 1st.  
**Expected**: self.assertEqual(parsed.day, 1)  
**Confidence**: 0.85  

```python
self.assertEqual(parsed.month, 1)
self.assertEqual(parsed.day, 1)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_helpers.py:15*

### test_date_parser_supports_year_only_dates

**Category**: method_call  
**Description**: Year-only dates should default to January 1st.  
**Expected**: self.assertEqual(parsed.hour, SentinelDatetime.HOUR)  
**Confidence**: 0.85  

```python
self.assertEqual(parsed.day, 1)
self.assertEqual(parsed.hour, SentinelDatetime.HOUR)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_helpers.py:16*

### test_date_parser_supports_year_month_dates

**Category**: method_call  
**Description**: Year-month dates should default to the first day of the month.  
**Expected**: self.assertEqual(parsed.month, 3)  
**Confidence**: 0.85  

```python
self.assertEqual(parsed.year, 2025)
self.assertEqual(parsed.month, 3)
```

*Source: C:\yamtrack-fork\src\events\tests\calendar\test_helpers.py:23*

### test_regenerate_token

**Category**: method_call  
**Description**: Test token regeneration.  
**Expected**: self.assertNotEqual(self.user.token, 'initial_token')  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.user.token = 'initial_token'
self.user.save()

self.user.refresh_from_db()
self.assertNotEqual(self.user.token, 'initial_token')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_token.py:27*

### test_regenerate_token

**Category**: method_call  
**Description**: Test token regeneration.  
**Expected**: self.assertIsNotNone(self.user.token)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.user.token = 'initial_token'
self.user.save()

self.assertNotEqual(self.user.token, 'initial_token')
self.assertIsNotNone(self.user.token)
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_token.py:28*

### test_regenerate_token

**Category**: method_call  
**Description**: Test token regeneration.  
**Expected**: self.assertIn('Token regenerated successfully', str(messages[0]))  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.user.token = 'initial_token'
self.user.save()

self.assertEqual(len(messages), 1)
self.assertIn('Token regenerated successfully', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_token.py:32*

### test_regenerate_token_integrity_error

**Category**: method_call  
**Description**: Test token regeneration with an IntegrityError on first attempt.  
**Expected**: self.assertEqual(mock_save.call_count, 2)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.user.token = 'initial_token'
self.user.save()

self.assertRedirects(response, reverse('integrations'))
self.assertEqual(mock_save.call_count, 2)
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_token.py:44*

### test_regenerate_token_integrity_error

**Category**: method_call  
**Description**: Test token regeneration with an IntegrityError on first attempt.  
**Expected**: self.assertIn('Token regenerated successfully', str(messages[0]))  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.user.token = 'initial_token'
self.user.save()

self.assertEqual(len(messages), 1)
self.assertIn('Token regenerated successfully', str(messages[0]))
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_token.py:49*

### test_integrations_uses_configured_webhook_urls

**Category**: method_call  
**Description**: Test copied webhook URLs use the configured public app URL.  
**Expected**: self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/plex/initial_token')  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.user.token = 'initial_token'
self.user.save()

self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/jellyfin/initial_token')
self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/plex/initial_token')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_token.py:57*

### test_integrations_uses_configured_webhook_urls

**Category**: method_call  
**Description**: Test copied webhook URLs use the configured public app URL.  
**Expected**: self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/emby/initial_token')  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.user.token = 'initial_token'
self.user.save()

self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/plex/initial_token')
self.assertContains(response, 'https://yamtrack.example.com:8924/webhook/emby/initial_token')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_token.py:61*

### test_regenerate_token

**Category**: method_call  
**Description**: Test token regeneration.  
**Expected**: self.assertNotEqual(self.user.token, 'initial_token')  
**Confidence**: 0.85  

```python
self.user.refresh_from_db()
self.assertNotEqual(self.user.token, 'initial_token')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_token.py:27*

### test_update_season_references

**Category**: method_call  
**Description**: Test updating season references with actual TV instances.  
**Expected**: self.assertEqual(new_season.related_tv.id, tv.id)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

helpers.update_season_references([new_season], self.user)
self.assertEqual(new_season.related_tv.id, tv.id)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_helpers.py:55*

### test_update_episode_references

**Category**: method_call  
**Description**: Test updating episode references with actual Season instances.  
**Expected**: self.assertEqual(new_episode.related_season.id, season.id)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

helpers.update_episode_references([new_episode], self.user)
self.assertEqual(new_episode.related_season.id, season.id)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_helpers.py:101*

### test_create_import_schedule

**Category**: method_call  
**Description**: Test creating import schedule.  
**Expected**: self.assertEqual(schedule.name, 'Import from TestSource for testuser at 14:30:00 daily')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertIsNotNone(schedule)
self.assertEqual(schedule.name, 'Import from TestSource for testuser at 14:30:00 daily')
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_helpers.py:121*

### test_create_import_schedule

**Category**: method_call  
**Description**: Test creating import schedule.  
**Expected**: mock_messages.assert_called_with(request, 'The same import task is already scheduled.')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

helpers.create_import_schedule('testuser', request, 'new', 'daily', '14:30', 'TestSource')
mock_messages.assert_called_with(request, 'The same import task is already scheduled.')
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_helpers.py:127*

### test_create_import_schedule_invalid_time

**Category**: method_call  
**Description**: Test creating import schedule with invalid time.  
**Expected**: mock_messages.assert_called_with(request, 'Invalid import time.')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

helpers.create_import_schedule('testuser', request, 'new', 'daily', '25:00', 'TestSource')
mock_messages.assert_called_with(request, 'Invalid import time.')
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_helpers.py:146*

### test_create_import_schedule_invalid_time

**Category**: method_call  
**Description**: Test creating import schedule with invalid time.  
**Expected**: self.assertEqual(PeriodicTask.objects.count(), 0)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

mock_messages.assert_called_with(request, 'Invalid import time.')
self.assertEqual(PeriodicTask.objects.count(), 0)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_helpers.py:155*

### test_update_season_references

**Category**: method_call  
**Description**: Test updating season references with actual TV instances.  
**Expected**: self.assertEqual(new_season.related_tv.id, tv.id)  
**Confidence**: 0.85  

```python
helpers.update_season_references([new_season], self.user)
self.assertEqual(new_season.related_tv.id, tv.id)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_helpers.py:55*

### test_update_episode_references

**Category**: method_call  
**Description**: Test updating episode references with actual Season instances.  
**Expected**: self.assertEqual(new_episode.related_season.id, season.id)  
**Confidence**: 0.85  

```python
helpers.update_episode_references([new_episode], self.user)
self.assertEqual(new_episode.related_season.id, season.id)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_helpers.py:101*

### test_importer

**Category**: method_call  
**Description**: Test importing media from SIMKL.  
**Expected**: self.assertEqual(imported_counts[MediaTypes.MOVIE.value], 1)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
self.importer = simkl.SimklImporter(helpers.encrypt('token'), self.user, 'new')

self.assertEqual(imported_counts[MediaTypes.TV.value], 1)
self.assertEqual(imported_counts[MediaTypes.MOVIE.value], 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_simkl.py:92*

### test_importer

**Category**: method_call  
**Description**: Test importing media from SIMKL.  
**Expected**: self.assertEqual(imported_counts[MediaTypes.ANIME.value], 1)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
self.importer = simkl.SimklImporter(helpers.encrypt('token'), self.user, 'new')

self.assertEqual(imported_counts[MediaTypes.MOVIE.value], 1)
self.assertEqual(imported_counts[MediaTypes.ANIME.value], 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_simkl.py:93*

### test_importer

**Category**: method_call  
**Description**: Test importing media from SIMKL.  
**Expected**: self.assertEqual(warnings, '')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
self.importer = simkl.SimklImporter(helpers.encrypt('token'), self.user, 'new')

self.assertEqual(imported_counts[MediaTypes.ANIME.value], 1)
self.assertEqual(warnings, '')
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_simkl.py:94*

### test_importer

**Category**: method_call  
**Description**: Test importing media from SIMKL.  
**Expected**: self.assertEqual(tv_obj.score, 8)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
self.importer = simkl.SimklImporter(helpers.encrypt('token'), self.user, 'new')

self.assertEqual(tv_obj.status, Status.IN_PROGRESS.value)
self.assertEqual(tv_obj.score, 8)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_simkl.py:100*

### test_importer

**Category**: method_call  
**Description**: Test importing media from SIMKL.  
**Expected**: self.assertEqual(movie_obj.score, 9)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
self.importer = simkl.SimklImporter(helpers.encrypt('token'), self.user, 'new')

self.assertEqual(movie_obj.status, Status.COMPLETED.value)
self.assertEqual(movie_obj.score, 9)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_simkl.py:106*

### test_importer

**Category**: method_call  
**Description**: Test importing media from SIMKL.  
**Expected**: self.assertEqual(movie_obj.progress, 1)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**credentials)
self.importer = simkl.SimklImporter(helpers.encrypt('token'), self.user, 'new')

self.assertEqual(movie_obj.score, 9)
self.assertEqual(movie_obj.progress, 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_simkl.py:107*

### test_create_entry_get

**Category**: method_call  
**Description**: Test the GET method of create_entry view.  
**Expected**: self.assertTemplateUsed(response, 'app/create_entry.html')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/create_entry.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_entry.py:32*

### test_create_entry_get

**Category**: method_call  
**Description**: Test the GET method of create_entry view.  
**Expected**: self.assertIn('media_types', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertTemplateUsed(response, 'app/create_entry.html')
self.assertIn('media_types', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_entry.py:33*

### test_create_entry_get

**Category**: method_call  
**Description**: Test the GET method of create_entry view.  
**Expected**: self.assertEqual(response.context['media_types'], MediaTypes.values)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertIn('media_types', response.context)
self.assertEqual(response.context['media_types'], MediaTypes.values)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_entry.py:34*

### test_create_entry_post_movie

**Category**: method_call  
**Description**: Test creating a movie entry.  
**Expected**: self.assertTrue(Item.objects.filter(title='Test Movie', media_type=MediaTypes.MOVIE.value).exists())  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertRedirects(response, reverse('create_entry'))
self.assertTrue(Item.objects.filter(title='Test Movie', media_type=MediaTypes.MOVIE.value).exists())
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_entry.py:52*

### test_first_episode_sets_season_in_progress

**Category**: method_call  
**Description**: Test first episode sets season to IN_PROGRESS.  
**Expected**: self.assertEqual(self.season.status, Status.IN_PROGRESS.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
self.episode_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Episode', image='http://example.com/image.jpg', season_number=1, episode_number=1)

self.season.refresh_from_db()
self.assertEqual(self.season.status, Status.IN_PROGRESS.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_episode.py:136*

### test_first_episode_sets_season_in_progress

**Category**: method_call  
**Description**: Test first episode sets season to IN_PROGRESS.  
**Expected**: self.assertEqual(self.tv.status, Status.IN_PROGRESS.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
self.episode_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Episode', image='http://example.com/image.jpg', season_number=1, episode_number=1)

self.tv.refresh_from_db()
self.assertEqual(self.tv.status, Status.IN_PROGRESS.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_episode.py:139*

### test_last_episode_sets_season_completed

**Category**: method_call  
**Description**: Test last episode sets season to COMPLETED.  
**Expected**: self.assertEqual(self.season.status, Status.COMPLETED.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
self.episode_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Episode', image='http://example.com/image.jpg', season_number=1, episode_number=1)

self.season.refresh_from_db()
self.assertEqual(self.season.status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_episode.py:161*

### test_last_episode_sets_season_completed

**Category**: method_call  
**Description**: Test last episode sets season to COMPLETED.  
**Expected**: self.assertEqual(self.tv.status, Status.COMPLETED.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.season_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)
self.episode_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Episode', image='http://example.com/image.jpg', season_number=1, episode_number=1)

self.tv.refresh_from_db()
self.assertEqual(self.tv.status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_episode.py:164*

### test_demo_user_cannot_change_username

**Category**: method_call  
**Description**: Test that demo users cannot change their username.  
**Expected**: self.assertContains(response, 'not allowed for the demo account')  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(auth.get_user(self.client).username, 'testuser')
self.assertContains(response, 'not allowed for the demo account')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_demo_profile.py:27*

### test_demo_user_cannot_change_username

**Category**: method_call  
**Description**: Test that demo users cannot change their username.  
**Expected**: self.assertContains(response, 'not allowed for the demo account')  
**Confidence**: 0.85  

```python
self.assertEqual(auth.get_user(self.client).username, 'testuser')
self.assertContains(response, 'not allowed for the demo account')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_demo_profile.py:27*

### test_stored_progress

**Category**: method_call  
**Description**: Test progress of imported books.  
**Expected**: self.assertEqual(read_book.progress, 994)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_goodreads.csv').open('rb') as file:
    self.import_results = goodreads.importer(file, self.user, 'new')

self.assertEqual(read_book.status, Status.COMPLETED.value)
self.assertEqual(read_book.progress, 994)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_goodreads.py:42*

### test_stored_progress

**Category**: method_call  
**Description**: Test progress of imported books.  
**Expected**: self.assertEqual(read_book.progress, 0)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_goodreads.csv').open('rb') as file:
    self.import_results = goodreads.importer(file, self.user, 'new')

self.assertEqual(read_book.status, Status.IN_PROGRESS.value)
self.assertEqual(read_book.progress, 0)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_goodreads.py:46*

### test_stored_progress

**Category**: method_call  
**Description**: Test progress of imported books.  
**Expected**: self.assertEqual(read_book.progress, 994)  
**Confidence**: 0.85  

```python
self.assertEqual(read_book.status, Status.COMPLETED.value)
self.assertEqual(read_book.progress, 994)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_goodreads.py:42*

### test_stored_progress

**Category**: method_call  
**Description**: Test progress of imported books.  
**Expected**: self.assertEqual(read_book.progress, 0)  
**Confidence**: 0.85  

```python
self.assertEqual(read_book.status, Status.IN_PROGRESS.value)
self.assertEqual(read_book.progress, 0)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_goodreads.py:46*

### test_search_parent_tv_short_query

**Category**: method_call  
**Description**: Test search_parent_tv with a query that's too short.  
**Expected**: self.assertTemplateUsed(response, 'app/components/search_parent_tv.html')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.tv1 = TV.objects.create(item=tv_item1, user=self.user, status=Status.IN_PROGRESS.value)
tv_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Another TV Show')
self.tv2 = TV.objects.create(item=tv_item2, user=self.user, status=Status.IN_PROGRESS.value)
season_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Test Season', season_number=1)
self.season1 = Season.objects.create(item=season_item1, user=self.user, related_tv=self.tv1, status=Status.IN_PROGRESS.value)
season_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Another Season', season_number=1)
self.season2 = Season.objects.create(item=season_item2, user=self.user, related_tv=self.tv2, status=Status.IN_PROGRESS.value)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/components/search_parent_tv.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_search_parent.py:80*

### test_search_parent_tv_short_query

**Category**: method_call  
**Description**: Test search_parent_tv with a query that's too short.  
**Expected**: self.assertNotIn('results', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.tv1 = TV.objects.create(item=tv_item1, user=self.user, status=Status.IN_PROGRESS.value)
tv_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Another TV Show')
self.tv2 = TV.objects.create(item=tv_item2, user=self.user, status=Status.IN_PROGRESS.value)
season_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Test Season', season_number=1)
self.season1 = Season.objects.create(item=season_item1, user=self.user, related_tv=self.tv1, status=Status.IN_PROGRESS.value)
season_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Another Season', season_number=1)
self.season2 = Season.objects.create(item=season_item2, user=self.user, related_tv=self.tv2, status=Status.IN_PROGRESS.value)

self.assertTemplateUsed(response, 'app/components/search_parent_tv.html')
self.assertNotIn('results', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_search_parent.py:81*

### test_search_parent_tv_valid_query

**Category**: method_call  
**Description**: Test search_parent_tv with a valid query.  
**Expected**: self.assertTemplateUsed(response, 'app/components/search_parent_tv.html')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.tv1 = TV.objects.create(item=tv_item1, user=self.user, status=Status.IN_PROGRESS.value)
tv_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Another TV Show')
self.tv2 = TV.objects.create(item=tv_item2, user=self.user, status=Status.IN_PROGRESS.value)
season_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Test Season', season_number=1)
self.season1 = Season.objects.create(item=season_item1, user=self.user, related_tv=self.tv1, status=Status.IN_PROGRESS.value)
season_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Another Season', season_number=1)
self.season2 = Season.objects.create(item=season_item2, user=self.user, related_tv=self.tv2, status=Status.IN_PROGRESS.value)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/components/search_parent_tv.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_search_parent.py:88*

### test_search_parent_tv_valid_query

**Category**: method_call  
**Description**: Test search_parent_tv with a valid query.  
**Expected**: self.assertIn('results', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.tv1 = TV.objects.create(item=tv_item1, user=self.user, status=Status.IN_PROGRESS.value)
tv_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Another TV Show')
self.tv2 = TV.objects.create(item=tv_item2, user=self.user, status=Status.IN_PROGRESS.value)
season_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Test Season', season_number=1)
self.season1 = Season.objects.create(item=season_item1, user=self.user, related_tv=self.tv1, status=Status.IN_PROGRESS.value)
season_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Another Season', season_number=1)
self.season2 = Season.objects.create(item=season_item2, user=self.user, related_tv=self.tv2, status=Status.IN_PROGRESS.value)

self.assertTemplateUsed(response, 'app/components/search_parent_tv.html')
self.assertIn('results', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_search_parent.py:89*

### test_search_parent_tv_valid_query

**Category**: method_call  
**Description**: Test search_parent_tv with a valid query.  
**Expected**: self.assertIn('query', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.tv1 = TV.objects.create(item=tv_item1, user=self.user, status=Status.IN_PROGRESS.value)
tv_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Another TV Show')
self.tv2 = TV.objects.create(item=tv_item2, user=self.user, status=Status.IN_PROGRESS.value)
season_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Test Season', season_number=1)
self.season1 = Season.objects.create(item=season_item1, user=self.user, related_tv=self.tv1, status=Status.IN_PROGRESS.value)
season_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Another Season', season_number=1)
self.season2 = Season.objects.create(item=season_item2, user=self.user, related_tv=self.tv2, status=Status.IN_PROGRESS.value)

self.assertIn('results', response.context)
self.assertIn('query', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_search_parent.py:90*

### test_search_parent_tv_valid_query

**Category**: method_call  
**Description**: Test search_parent_tv with a valid query.  
**Expected**: self.assertEqual(len(response.context['results']), 1)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.tv1 = TV.objects.create(item=tv_item1, user=self.user, status=Status.IN_PROGRESS.value)
tv_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Another TV Show')
self.tv2 = TV.objects.create(item=tv_item2, user=self.user, status=Status.IN_PROGRESS.value)
season_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Test Season', season_number=1)
self.season1 = Season.objects.create(item=season_item1, user=self.user, related_tv=self.tv1, status=Status.IN_PROGRESS.value)
season_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Another Season', season_number=1)
self.season2 = Season.objects.create(item=season_item2, user=self.user, related_tv=self.tv2, status=Status.IN_PROGRESS.value)

self.assertIn('query', response.context)
self.assertEqual(len(response.context['results']), 1)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_search_parent.py:91*

### test_search_parent_tv_valid_query

**Category**: method_call  
**Description**: Test search_parent_tv with a valid query.  
**Expected**: self.assertEqual(response.context['results'][0], self.tv1)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.tv1 = TV.objects.create(item=tv_item1, user=self.user, status=Status.IN_PROGRESS.value)
tv_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Another TV Show')
self.tv2 = TV.objects.create(item=tv_item2, user=self.user, status=Status.IN_PROGRESS.value)
season_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Test Season', season_number=1)
self.season1 = Season.objects.create(item=season_item1, user=self.user, related_tv=self.tv1, status=Status.IN_PROGRESS.value)
season_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Another Season', season_number=1)
self.season2 = Season.objects.create(item=season_item2, user=self.user, related_tv=self.tv2, status=Status.IN_PROGRESS.value)

self.assertEqual(len(response.context['results']), 1)
self.assertEqual(response.context['results'][0], self.tv1)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_search_parent.py:93*

### test_search_parent_tv_valid_query

**Category**: method_call  
**Description**: Test search_parent_tv with a valid query.  
**Expected**: self.assertEqual(response.context['query'], 'Test')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.tv1 = TV.objects.create(item=tv_item1, user=self.user, status=Status.IN_PROGRESS.value)
tv_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Another TV Show')
self.tv2 = TV.objects.create(item=tv_item2, user=self.user, status=Status.IN_PROGRESS.value)
season_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Test Season', season_number=1)
self.season1 = Season.objects.create(item=season_item1, user=self.user, related_tv=self.tv1, status=Status.IN_PROGRESS.value)
season_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Another Season', season_number=1)
self.season2 = Season.objects.create(item=season_item2, user=self.user, related_tv=self.tv2, status=Status.IN_PROGRESS.value)

self.assertEqual(response.context['results'][0], self.tv1)
self.assertEqual(response.context['query'], 'Test')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_search_parent.py:94*

### test_search_parent_tv_no_results

**Category**: method_call  
**Description**: Test search_parent_tv with a query that returns no results.  
**Expected**: self.assertTemplateUsed(response, 'app/components/search_parent_tv.html')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.tv1 = TV.objects.create(item=tv_item1, user=self.user, status=Status.IN_PROGRESS.value)
tv_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Another TV Show')
self.tv2 = TV.objects.create(item=tv_item2, user=self.user, status=Status.IN_PROGRESS.value)
season_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Test Season', season_number=1)
self.season1 = Season.objects.create(item=season_item1, user=self.user, related_tv=self.tv1, status=Status.IN_PROGRESS.value)
season_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Another Season', season_number=1)
self.season2 = Season.objects.create(item=season_item2, user=self.user, related_tv=self.tv2, status=Status.IN_PROGRESS.value)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/components/search_parent_tv.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_search_parent.py:101*

### test_search_parent_tv_no_results

**Category**: method_call  
**Description**: Test search_parent_tv with a query that returns no results.  
**Expected**: self.assertIn('results', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
tv_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Test TV Show')
self.tv1 = TV.objects.create(item=tv_item1, user=self.user, status=Status.IN_PROGRESS.value)
tv_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.TV.value, title='Another TV Show')
self.tv2 = TV.objects.create(item=tv_item2, user=self.user, status=Status.IN_PROGRESS.value)
season_item1 = Item.objects.create(media_id='111', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Test Season', season_number=1)
self.season1 = Season.objects.create(item=season_item1, user=self.user, related_tv=self.tv1, status=Status.IN_PROGRESS.value)
season_item2 = Item.objects.create(media_id='222', source=Sources.MANUAL.value, media_type=MediaTypes.SEASON.value, title='Another Season', season_number=1)
self.season2 = Season.objects.create(item=season_item2, user=self.user, related_tv=self.tv2, status=Status.IN_PROGRESS.value)

self.assertTemplateUsed(response, 'app/components/search_parent_tv.html')
self.assertIn('results', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_search_parent.py:102*

### test_process_task_result_failure_media_import_error

**Category**: method_call  
**Description**: Test processing a failed task with MediaImportError.  
**Expected**: self.assertEqual(processed_task.errors, 'Traceback info')  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(processed_task.summary, 'Test error message')
self.assertEqual(processed_task.errors, 'Traceback info')
```

*Source: C:\yamtrack-fork\src\users\tests\test_helpers.py:29*

### test_process_task_result_failure_unexpected_error

**Category**: method_call  
**Description**: Test processing a failed task with unexpected error.  
**Expected**: self.assertEqual(processed_task.errors, 'Traceback info')  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(processed_task.summary, 'Unexpected error occurred while processing the task.')
self.assertEqual(processed_task.errors, 'Traceback info')
```

*Source: C:\yamtrack-fork\src\users\tests\test_helpers.py:46*

### test_process_task_result_success_with_errors

**Category**: method_call  
**Description**: Test processing a successful task with errors.  
**Expected**: self.assertEqual(processed_task.errors, 'Error details')  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(processed_task.summary, 'Summary text')
self.assertEqual(processed_task.errors, 'Error details')
```

*Source: C:\yamtrack-fork\src\users\tests\test_helpers.py:63*

### test_process_task_result_success_no_errors

**Category**: method_call  
**Description**: Test processing a successful task without errors.  
**Expected**: self.assertIsNone(processed_task.errors)  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(processed_task.summary, 'Summary text only')
self.assertIsNone(processed_task.errors)
```

*Source: C:\yamtrack-fork\src\users\tests\test_helpers.py:75*

### test_home_view

**Category**: method_call  
**Description**: Test the home view displays in-progress and planning media.  
**Expected**: self.assertTemplateUsed(response, 'app/home.html')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_number = season_numbers[0]
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'details': {'seasons': 1}, f'season/{season_number}': {'episodes': [{'id': i} for i in range(1, 11)]}, 'related': {'seasons': [{'season_number': season_number, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'season/1': {'episodes': [{'id': i} for i in range(1, 11)]}}
    if media_type == MediaTypes.ANIME.value:
        return {'title': 'Test Anime', 'image': 'http://example.com/image.jpg', 'max_progress': 24}
    if media_type == MediaTypes.MOVIE.value:
        return {'title': 'Planned Movie', 'image': 'http://example.com/image.jpg', 'max_progress': 1}
    return {'max_progress': None}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', image='http://example.com/image.jpg', season_number=1)
season = Season.objects.create(item=season_item, user=self.user, status=Status.IN_PROGRESS.value)
for i in range(1, 6):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    Episode.objects.create(item=episode_item, related_season=season, end_date=timezone.now() - timezone.timedelta(days=i))
anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/image.jpg')
Anime.objects.create(item=anime_item, user=self.user, status=Status.IN_PROGRESS.value, progress=10)
movie_item = Item.objects.create(media_id='10', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Planned Movie', image='http://example.com/image.jpg')
Movie.objects.create(item=movie_item, user=self.user, status=Status.PLANNING.value)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/home.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_home.py:164*

### test_home_view

**Category**: method_call  
**Description**: Test the home view displays in-progress and planning media.  
**Expected**: self.assertIn('home_sections', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_number = season_numbers[0]
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'details': {'seasons': 1}, f'season/{season_number}': {'episodes': [{'id': i} for i in range(1, 11)]}, 'related': {'seasons': [{'season_number': season_number, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'season/1': {'episodes': [{'id': i} for i in range(1, 11)]}}
    if media_type == MediaTypes.ANIME.value:
        return {'title': 'Test Anime', 'image': 'http://example.com/image.jpg', 'max_progress': 24}
    if media_type == MediaTypes.MOVIE.value:
        return {'title': 'Planned Movie', 'image': 'http://example.com/image.jpg', 'max_progress': 1}
    return {'max_progress': None}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', image='http://example.com/image.jpg', season_number=1)
season = Season.objects.create(item=season_item, user=self.user, status=Status.IN_PROGRESS.value)
for i in range(1, 6):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    Episode.objects.create(item=episode_item, related_season=season, end_date=timezone.now() - timezone.timedelta(days=i))
anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/image.jpg')
Anime.objects.create(item=anime_item, user=self.user, status=Status.IN_PROGRESS.value, progress=10)
movie_item = Item.objects.create(media_id='10', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Planned Movie', image='http://example.com/image.jpg')
Movie.objects.create(item=movie_item, user=self.user, status=Status.PLANNING.value)

self.assertTemplateUsed(response, 'app/home.html')
self.assertIn('home_sections', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_home.py:165*

### test_home_view

**Category**: method_call  
**Description**: Test the home view displays in-progress and planning media.  
**Expected**: self.assertIn(Status.PLANNING.value, sections_by_key)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_number = season_numbers[0]
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'details': {'seasons': 1}, f'season/{season_number}': {'episodes': [{'id': i} for i in range(1, 11)]}, 'related': {'seasons': [{'season_number': season_number, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'season/1': {'episodes': [{'id': i} for i in range(1, 11)]}}
    if media_type == MediaTypes.ANIME.value:
        return {'title': 'Test Anime', 'image': 'http://example.com/image.jpg', 'max_progress': 24}
    if media_type == MediaTypes.MOVIE.value:
        return {'title': 'Planned Movie', 'image': 'http://example.com/image.jpg', 'max_progress': 1}
    return {'max_progress': None}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', image='http://example.com/image.jpg', season_number=1)
season = Season.objects.create(item=season_item, user=self.user, status=Status.IN_PROGRESS.value)
for i in range(1, 6):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    Episode.objects.create(item=episode_item, related_season=season, end_date=timezone.now() - timezone.timedelta(days=i))
anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/image.jpg')
Anime.objects.create(item=anime_item, user=self.user, status=Status.IN_PROGRESS.value, progress=10)
movie_item = Item.objects.create(media_id='10', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Planned Movie', image='http://example.com/image.jpg')
Movie.objects.create(item=movie_item, user=self.user, status=Status.PLANNING.value)

self.assertIn(Status.IN_PROGRESS.value, sections_by_key)
self.assertIn(Status.PLANNING.value, sections_by_key)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_home.py:172*

### test_home_view

**Category**: method_call  
**Description**: Test the home view displays in-progress and planning media.  
**Expected**: self.assertIn(MediaTypes.ANIME.value, in_progress_section['media_types'])  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.metadata_patcher = patch('app.providers.services.get_media_metadata')
self.mock_get_media_metadata = self.metadata_patcher.start()
self.addCleanup(self.metadata_patcher.stop)

def mock_get_media_metadata(media_type, _media_id, _source, season_numbers=None, _episode_number=None):
    if media_type == MediaTypes.TV.value:
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'details': {'seasons': 1}, 'related': {'seasons': [{'season_number': 1, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == 'tv_with_seasons':
        season_number = season_numbers[0]
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'details': {'seasons': 1}, f'season/{season_number}': {'episodes': [{'id': i} for i in range(1, 11)]}, 'related': {'seasons': [{'season_number': season_number, 'image': 'http://example.com/image.jpg'}]}}
    if media_type == MediaTypes.SEASON.value:
        return {'title': 'Test TV Show', 'image': 'http://example.com/image.jpg', 'max_progress': 10, 'season/1': {'episodes': [{'id': i} for i in range(1, 11)]}}
    if media_type == MediaTypes.ANIME.value:
        return {'title': 'Test Anime', 'image': 'http://example.com/image.jpg', 'max_progress': 24}
    if media_type == MediaTypes.MOVIE.value:
        return {'title': 'Planned Movie', 'image': 'http://example.com/image.jpg', 'max_progress': 1}
    return {'max_progress': None}
self.mock_get_media_metadata.side_effect = mock_get_media_metadata
season_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test TV Show', image='http://example.com/image.jpg', season_number=1)
season = Season.objects.create(item=season_item, user=self.user, status=Status.IN_PROGRESS.value)
for i in range(1, 6):
    episode_item = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test TV Show', image='http://example.com/image.jpg', season_number=1, episode_number=i)
    Episode.objects.create(item=episode_item, related_season=season, end_date=timezone.now() - timezone.timedelta(days=i))
anime_item = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Test Anime', image='http://example.com/image.jpg')
Anime.objects.create(item=anime_item, user=self.user, status=Status.IN_PROGRESS.value, progress=10)
movie_item = Item.objects.create(media_id='10', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Planned Movie', image='http://example.com/image.jpg')
Movie.objects.create(item=movie_item, user=self.user, status=Status.PLANNING.value)

self.assertIn(MediaTypes.SEASON.value, in_progress_section['media_types'])
self.assertIn(MediaTypes.ANIME.value, in_progress_section['media_types'])
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_home.py:178*

### test_cleanup_user_messages_deletes_only_old_shown_messages

**Category**: method_call  
**Description**: Delete only shown messages older than the retention window.  
**Expected**: self.assertFalse(UserMessage.objects.filter(id=old_shown.id).exists())  
**Confidence**: 0.85  

```python
# Setup
'Create a user for task tests.'
self.user = get_user_model().objects.create_user(username='test')

self.assertEqual(deleted_count, 1)
self.assertFalse(UserMessage.objects.filter(id=old_shown.id).exists())
```

*Source: C:\yamtrack-fork\src\app\tests\test_tasks.py:44*

### test_cleanup_user_messages_deletes_only_old_shown_messages

**Category**: method_call  
**Description**: Delete only shown messages older than the retention window.  
**Expected**: self.assertTrue(UserMessage.objects.filter(id=recent_shown.id).exists())  
**Confidence**: 0.85  

```python
# Setup
'Create a user for task tests.'
self.user = get_user_model().objects.create_user(username='test')

self.assertFalse(UserMessage.objects.filter(id=old_shown.id).exists())
self.assertTrue(UserMessage.objects.filter(id=recent_shown.id).exists())
```

*Source: C:\yamtrack-fork\src\app\tests\test_tasks.py:45*

### test_cleanup_user_messages_deletes_only_old_shown_messages

**Category**: method_call  
**Description**: Delete only shown messages older than the retention window.  
**Expected**: self.assertTrue(UserMessage.objects.filter(id=unseen.id).exists())  
**Confidence**: 0.85  

```python
# Setup
'Create a user for task tests.'
self.user = get_user_model().objects.create_user(username='test')

self.assertTrue(UserMessage.objects.filter(id=recent_shown.id).exists())
self.assertTrue(UserMessage.objects.filter(id=unseen.id).exists())
```

*Source: C:\yamtrack-fork\src\app\tests\test_tasks.py:46*

### test_cleanup_user_messages_deletes_only_old_shown_messages

**Category**: method_call  
**Description**: Delete only shown messages older than the retention window.  
**Expected**: self.assertFalse(UserMessage.objects.filter(id=old_shown.id).exists())  
**Confidence**: 0.85  

```python
self.assertEqual(deleted_count, 1)
self.assertFalse(UserMessage.objects.filter(id=old_shown.id).exists())
```

*Source: C:\yamtrack-fork\src\app\tests\test_tasks.py:44*

### test_cleanup_user_messages_deletes_only_old_shown_messages

**Category**: method_call  
**Description**: Delete only shown messages older than the retention window.  
**Expected**: self.assertTrue(UserMessage.objects.filter(id=recent_shown.id).exists())  
**Confidence**: 0.85  

```python
self.assertFalse(UserMessage.objects.filter(id=old_shown.id).exists())
self.assertTrue(UserMessage.objects.filter(id=recent_shown.id).exists())
```

*Source: C:\yamtrack-fork\src\app\tests\test_tasks.py:45*

### test_cleanup_user_messages_deletes_only_old_shown_messages

**Category**: method_call  
**Description**: Delete only shown messages older than the retention window.  
**Expected**: self.assertTrue(UserMessage.objects.filter(id=unseen.id).exists())  
**Confidence**: 0.85  

```python
self.assertTrue(UserMessage.objects.filter(id=recent_shown.id).exists())
self.assertTrue(UserMessage.objects.filter(id=unseen.id).exists())
```

*Source: C:\yamtrack-fork\src\app\tests\test_tasks.py:46*

### test_change_username

**Category**: method_call  
**Description**: Test changing username.  
**Expected**: self.assertEqual(auth.get_user(self.client).username, 'new_test')  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.client.post(reverse('account'), {'username': 'new_test'})
self.assertEqual(auth.get_user(self.client).username, 'new_test')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_profile.py:19*

### test_change_username

**Category**: method_call  
**Description**: Test changing username.  
**Expected**: self.assertEqual(auth.get_user(self.client).username, 'new_test')  
**Confidence**: 0.85  

```python
self.client.post(reverse('account'), {'username': 'new_test'})
self.assertEqual(auth.get_user(self.client).username, 'new_test')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_profile.py:19*

### test_create_anime

**Category**: method_call  
**Description**: Test the creation of a TV object.  
**Expected**: self.assertEqual(Anime.objects.filter(item__media_id='1', user=self.user).exists(), True)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.client.post(reverse('media_save'), {'media_id': '1', 'source': Sources.MAL.value, 'media_type': MediaTypes.ANIME.value, 'status': Status.PLANNING.value, 'progress': 0, 'repeats': 0})
self.assertEqual(Anime.objects.filter(item__media_id='1', user=self.user).exists(), True)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_crud.py:39*

### test_create_tv

**Category**: method_call  
**Description**: Test the creation of a TV object through views.  
**Expected**: self.assertEqual(TV.objects.filter(item__media_id='5895', user=self.user).exists(), True)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.client.post(reverse('media_save'), {'media_id': '5895', 'source': Sources.TMDB.value, 'media_type': MediaTypes.TV.value, 'status': Status.PLANNING.value})
self.assertEqual(TV.objects.filter(item__media_id='5895', user=self.user).exists(), True)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_crud.py:65*

### test_create_season

**Category**: method_call  
**Description**: Test the creation of a Season through views.  
**Expected**: self.assertEqual(Season.objects.filter(item__media_id='1668', user=self.user).exists(), True)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.client.post(reverse('media_save'), {'media_id': '1668', 'source': Sources.TMDB.value, 'media_type': MediaTypes.SEASON.value, 'season_number': 1, 'status': Status.PLANNING.value})
self.assertEqual(Season.objects.filter(item__media_id='1668', user=self.user).exists(), True)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_crud.py:89*

### test_create_episodes

**Category**: method_call  
**Description**: Test the creation of Episode through views.  
**Expected**: self.assertEqual(Episode.objects.filter(item__media_id='1668', related_season__user=self.user, item__episode_number=1).exists(), True)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.client.post(reverse('episode_save'), {'media_id': '1668', 'season_number': 1, 'episode_number': 1, 'source': Sources.TMDB.value, 'date': '2023-06-01T00:00'})
self.assertEqual(Episode.objects.filter(item__media_id='1668', related_season__user=self.user, item__episode_number=1).exists(), True)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_crud.py:106*

### test_edit_movie_score

**Category**: method_call  
**Description**: Test the editing of a movie score.  
**Expected**: self.assertEqual(Movie.objects.get(item__media_id='10494').score, 10)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.client.post(reverse('media_save'), {'instance_id': movie.id, 'media_id': '10494', 'source': Sources.TMDB.value, 'media_type': MediaTypes.MOVIE.value, 'score': 10, 'progress': 1, 'status': Status.COMPLETED.value, 'notes': 'Nice'})
self.assertEqual(Movie.objects.get(item__media_id='10494').score, 10)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_crud.py:155*

### test_delete_tv

**Category**: method_call  
**Description**: Test the deletion of a tv through views.  
**Expected**: self.assertEqual(Movie.objects.filter(user=self.user).count(), 0)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.item_season, user=self.user, status=Status.IN_PROGRESS.value)
self.item_ep = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
self.episode = Episode.objects.create(item=self.item_ep, related_season=self.season, end_date=datetime.datetime(2023, 6, 1, 0, 0, tzinfo=datetime.UTC))

self.client.post(reverse('media_delete'), data={'instance_id': tv_obj.id, 'media_type': MediaTypes.TV.value})
self.assertEqual(Movie.objects.filter(user=self.user).count(), 0)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_crud.py:214*

### test_delete_season

**Category**: method_call  
**Description**: Test the deletion of a season through views.  
**Expected**: self.assertEqual(Season.objects.filter(user=self.user).count(), 0)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.item_season, user=self.user, status=Status.IN_PROGRESS.value)
self.item_ep = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
self.episode = Episode.objects.create(item=self.item_ep, related_season=self.season, end_date=datetime.datetime(2023, 6, 1, 0, 0, tzinfo=datetime.UTC))

self.client.post(reverse('media_delete'), data={'instance_id': self.season.id, 'media_type': MediaTypes.SEASON.value})
self.assertEqual(Season.objects.filter(user=self.user).count(), 0)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_crud.py:226*

### test_delete_season

**Category**: method_call  
**Description**: Test the deletion of a season through views.  
**Expected**: self.assertEqual(Episode.objects.filter(related_season__user=self.user).count(), 0)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.item_season, user=self.user, status=Status.IN_PROGRESS.value)
self.item_ep = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
self.episode = Episode.objects.create(item=self.item_ep, related_season=self.season, end_date=datetime.datetime(2023, 6, 1, 0, 0, tzinfo=datetime.UTC))

self.assertEqual(Season.objects.filter(user=self.user).count(), 0)
self.assertEqual(Episode.objects.filter(related_season__user=self.user).count(), 0)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_crud.py:233*

### test_unwatch_episode

**Category**: method_call  
**Description**: Test unwatching of an episode through views.  
**Expected**: self.assertEqual(Episode.objects.filter(related_season__user=self.user).count(), 0)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)
self.item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
self.season = Season.objects.create(item=self.item_season, user=self.user, status=Status.IN_PROGRESS.value)
self.item_ep = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
self.episode = Episode.objects.create(item=self.item_ep, related_season=self.season, end_date=datetime.datetime(2023, 6, 1, 0, 0, tzinfo=datetime.UTC))

self.client.post(reverse('media_delete'), data={'instance_id': self.episode.id, 'media_type': MediaTypes.EPISODE.value})
self.assertEqual(Episode.objects.filter(related_season__user=self.user).count(), 0)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_crud.py:241*

### test_create_anime

**Category**: method_call  
**Description**: Test the creation of a TV object.  
**Expected**: self.assertEqual(Anime.objects.filter(item__media_id='1', user=self.user).exists(), True)  
**Confidence**: 0.85  

```python
self.client.post(reverse('media_save'), {'media_id': '1', 'source': Sources.MAL.value, 'media_type': MediaTypes.ANIME.value, 'status': Status.PLANNING.value, 'progress': 0, 'repeats': 0})
self.assertEqual(Anime.objects.filter(item__media_id='1', user=self.user).exists(), True)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_crud.py:39*

### test_item_creation

**Category**: method_call  
**Description**: Test the creation of an Item instance.  
**Expected**: self.assertEqual(self.item.media_type, MediaTypes.MOVIE.value)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for Item model.'
self.item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')

self.assertEqual(self.item.media_id, '1')
self.assertEqual(self.item.media_type, MediaTypes.MOVIE.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_item.py:29*

### test_item_creation

**Category**: method_call  
**Description**: Test the creation of an Item instance.  
**Expected**: self.assertEqual(self.item.title, 'Test Movie')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for Item model.'
self.item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')

self.assertEqual(self.item.media_type, MediaTypes.MOVIE.value)
self.assertEqual(self.item.title, 'Test Movie')
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_item.py:30*

### test_item_creation

**Category**: method_call  
**Description**: Test the creation of an Item instance.  
**Expected**: self.assertEqual(self.item.image, 'http://example.com/image.jpg')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for Item model.'
self.item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')

self.assertEqual(self.item.title, 'Test Movie')
self.assertEqual(self.item.image, 'http://example.com/image.jpg')
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_item.py:31*

### test_item_creation

**Category**: method_call  
**Description**: Test the creation of an Item instance.  
**Expected**: self.assertEqual(self.item.media_type, MediaTypes.MOVIE.value)  
**Confidence**: 0.85  

```python
self.assertEqual(self.item.media_id, '1')
self.assertEqual(self.item.media_type, MediaTypes.MOVIE.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_item.py:29*

### test_item_creation

**Category**: method_call  
**Description**: Test the creation of an Item instance.  
**Expected**: self.assertEqual(self.item.title, 'Test Movie')  
**Confidence**: 0.85  

```python
self.assertEqual(self.item.media_type, MediaTypes.MOVIE.value)
self.assertEqual(self.item.title, 'Test Movie')
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_item.py:30*

### test_item_creation

**Category**: method_call  
**Description**: Test the creation of an Item instance.  
**Expected**: self.assertEqual(self.item.image, 'http://example.com/image.jpg')  
**Confidence**: 0.85  

```python
self.assertEqual(self.item.title, 'Test Movie')
self.assertEqual(self.item.image, 'http://example.com/image.jpg')
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_item.py:31*

### test_get_access_token_logs_in_and_caches_token

**Category**: method_call  
**Description**: Test TVDB login returns and caches a bearer token.  
**Expected**: mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'POST', f'{tvdb.BASE_URL}/login', params={'apikey': 'test-tvdb-key'})  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(result, 'test-token')
mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'POST', f'{tvdb.BASE_URL}/login', params={'apikey': 'test-tvdb-key'})
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_tvdb.py:29*

### test_get_access_token_logs_in_and_caches_token

**Category**: method_call  
**Description**: Test TVDB login returns and caches a bearer token.  
**Expected**: mock_cache.set.assert_called_once_with(tvdb.ACCESS_TOKEN_CACHE_KEY, 'test-token', tvdb.ACCESS_TOKEN_TIMEOUT)  
**Confidence**: 0.85  
**Tags**: mock  

```python
mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'POST', f'{tvdb.BASE_URL}/login', params={'apikey': 'test-tvdb-key'})
mock_cache.set.assert_called_once_with(tvdb.ACCESS_TOKEN_CACHE_KEY, 'test-token', tvdb.ACCESS_TOKEN_TIMEOUT)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_tvdb.py:30*

### test_episode_queries_episode_endpoint

**Category**: method_call  
**Description**: Test TVDB episode lookup returns normalized episode metadata.  
**Expected**: mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'GET', f'{tvdb.BASE_URL}/episodes/12345', headers={'Authorization': 'Bearer test-token'})  
**Confidence**: 0.85  
**Tags**: mock  

```python
self.assertEqual(result, {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})
mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'GET', f'{tvdb.BASE_URL}/episodes/12345', headers={'Authorization': 'Bearer test-token'})
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_tvdb.py:66*

### test_episode_queries_episode_endpoint

**Category**: method_call  
**Description**: Test TVDB episode lookup returns normalized episode metadata.  
**Expected**: mock_cache.set.assert_called_once_with('tvdb_episode_12345', {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})  
**Confidence**: 0.85  
**Tags**: mock  

```python
mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'GET', f'{tvdb.BASE_URL}/episodes/12345', headers={'Authorization': 'Bearer test-token'})
mock_cache.set.assert_called_once_with('tvdb_episode_12345', {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_tvdb.py:76*

### test_get_access_token_logs_in_and_caches_token

**Category**: method_call  
**Description**: Test TVDB login returns and caches a bearer token.  
**Expected**: mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'POST', f'{tvdb.BASE_URL}/login', params={'apikey': 'test-tvdb-key'})  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
# Fixtures: mock_api_request, mock_cache

self.assertEqual(result, 'test-token')
mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'POST', f'{tvdb.BASE_URL}/login', params={'apikey': 'test-tvdb-key'})
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_tvdb.py:29*

### test_get_access_token_logs_in_and_caches_token

**Category**: method_call  
**Description**: Test TVDB login returns and caches a bearer token.  
**Expected**: mock_cache.set.assert_called_once_with(tvdb.ACCESS_TOKEN_CACHE_KEY, 'test-token', tvdb.ACCESS_TOKEN_TIMEOUT)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
# Fixtures: mock_api_request, mock_cache

mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'POST', f'{tvdb.BASE_URL}/login', params={'apikey': 'test-tvdb-key'})
mock_cache.set.assert_called_once_with(tvdb.ACCESS_TOKEN_CACHE_KEY, 'test-token', tvdb.ACCESS_TOKEN_TIMEOUT)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_tvdb.py:30*

### test_episode_queries_episode_endpoint

**Category**: method_call  
**Description**: Test TVDB episode lookup returns normalized episode metadata.  
**Expected**: mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'GET', f'{tvdb.BASE_URL}/episodes/12345', headers={'Authorization': 'Bearer test-token'})  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
# Fixtures: mock_api_request, mock_get_access_token, mock_cache

self.assertEqual(result, {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})
mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'GET', f'{tvdb.BASE_URL}/episodes/12345', headers={'Authorization': 'Bearer test-token'})
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_tvdb.py:66*

### test_episode_queries_episode_endpoint

**Category**: method_call  
**Description**: Test TVDB episode lookup returns normalized episode metadata.  
**Expected**: mock_cache.set.assert_called_once_with('tvdb_episode_12345', {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
# Fixtures: mock_api_request, mock_get_access_token, mock_cache

mock_api_request.assert_called_once_with(tvdb.PROVIDER, 'GET', f'{tvdb.BASE_URL}/episodes/12345', headers={'Authorization': 'Bearer test-token'})
mock_cache.set.assert_called_once_with('tvdb_episode_12345', {'episode_id': 12345, 'series_id': 74796, 'season_number': 2, 'episode_number': 2, 'absolute_number': 22})
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_tvdb.py:76*

### test_format_description_status_initial

**Category**: method_call  
**Description**: Test format_description for initial status changes.  
**Expected**: self.assertEqual(format_description('status', None, Status.COMPLETED.value, MediaTypes.MANGA.value), 'Marked as finished reading')  
**Confidence**: 0.85  

```python
self.assertEqual(format_description('status', None, Status.IN_PROGRESS.value, MediaTypes.TV.value), 'Marked as currently watching')
self.assertEqual(format_description('status', None, Status.COMPLETED.value, MediaTypes.MANGA.value), 'Marked as finished reading')
```

*Source: C:\yamtrack-fork\src\app\tests\test_history_processor.py:25*

### test_format_description_status_initial

**Category**: method_call  
**Description**: Test format_description for initial status changes.  
**Expected**: self.assertEqual(format_description('status', None, Status.PLANNING.value, MediaTypes.GAME.value), 'Added to playing list')  
**Confidence**: 0.85  

```python
self.assertEqual(format_description('status', None, Status.COMPLETED.value, MediaTypes.MANGA.value), 'Marked as finished reading')
self.assertEqual(format_description('status', None, Status.PLANNING.value, MediaTypes.GAME.value), 'Added to playing list')
```

*Source: C:\yamtrack-fork\src\app\tests\test_history_processor.py:34*

### test_format_description_status_initial

**Category**: method_call  
**Description**: Test format_description for initial status changes.  
**Expected**: self.assertEqual(format_description('status', None, Status.DROPPED.value, MediaTypes.BOOK.value), 'Marked as dropped')  
**Confidence**: 0.85  

```python
self.assertEqual(format_description('status', None, Status.PLANNING.value, MediaTypes.GAME.value), 'Added to playing list')
self.assertEqual(format_description('status', None, Status.DROPPED.value, MediaTypes.BOOK.value), 'Marked as dropped')
```

*Source: C:\yamtrack-fork\src\app\tests\test_history_processor.py:43*

### test_format_description_status_initial

**Category**: method_call  
**Description**: Test format_description for initial status changes.  
**Expected**: self.assertEqual(format_description('status', None, Status.PAUSED.value, MediaTypes.ANIME.value), 'Marked as paused watching')  
**Confidence**: 0.85  

```python
self.assertEqual(format_description('status', None, Status.DROPPED.value, MediaTypes.BOOK.value), 'Marked as dropped')
self.assertEqual(format_description('status', None, Status.PAUSED.value, MediaTypes.ANIME.value), 'Marked as paused watching')
```

*Source: C:\yamtrack-fork\src\app\tests\test_history_processor.py:52*

### test_format_description_status_transitions

**Category**: method_call  
**Description**: Test format_description for status transitions.  
**Expected**: self.assertEqual(format_description('status', Status.IN_PROGRESS.value, Status.COMPLETED.value, MediaTypes.MANGA.value), 'Finished reading')  
**Confidence**: 0.85  

```python
self.assertEqual(format_description('status', Status.PLANNING.value, Status.IN_PROGRESS.value, MediaTypes.TV.value), 'Currently watching')
self.assertEqual(format_description('status', Status.IN_PROGRESS.value, Status.COMPLETED.value, MediaTypes.MANGA.value), 'Finished reading')
```

*Source: C:\yamtrack-fork\src\app\tests\test_history_processor.py:74*

### test_format_description_status_transitions

**Category**: method_call  
**Description**: Test format_description for status transitions.  
**Expected**: self.assertEqual(format_description('status', Status.IN_PROGRESS.value, Status.PAUSED.value, MediaTypes.GAME.value), 'Paused playing')  
**Confidence**: 0.85  

```python
self.assertEqual(format_description('status', Status.IN_PROGRESS.value, Status.COMPLETED.value, MediaTypes.MANGA.value), 'Finished reading')
self.assertEqual(format_description('status', Status.IN_PROGRESS.value, Status.PAUSED.value, MediaTypes.GAME.value), 'Paused playing')
```

*Source: C:\yamtrack-fork\src\app\tests\test_history_processor.py:83*

### test_format_description_status_transitions

**Category**: method_call  
**Description**: Test format_description for status transitions.  
**Expected**: self.assertEqual(format_description('status', Status.PAUSED.value, Status.IN_PROGRESS.value, MediaTypes.BOOK.value), 'Resumed reading')  
**Confidence**: 0.85  

```python
self.assertEqual(format_description('status', Status.IN_PROGRESS.value, Status.PAUSED.value, MediaTypes.GAME.value), 'Paused playing')
self.assertEqual(format_description('status', Status.PAUSED.value, Status.IN_PROGRESS.value, MediaTypes.BOOK.value), 'Resumed reading')
```

*Source: C:\yamtrack-fork\src\app\tests\test_history_processor.py:92*

### test_format_description_status_transitions

**Category**: method_call  
**Description**: Test format_description for status transitions.  
**Expected**: self.assertEqual(format_description('status', Status.IN_PROGRESS.value, Status.DROPPED.value, MediaTypes.ANIME.value), 'Stopped watching')  
**Confidence**: 0.85  

```python
self.assertEqual(format_description('status', Status.PAUSED.value, Status.IN_PROGRESS.value, MediaTypes.BOOK.value), 'Resumed reading')
self.assertEqual(format_description('status', Status.IN_PROGRESS.value, Status.DROPPED.value, MediaTypes.ANIME.value), 'Stopped watching')
```

*Source: C:\yamtrack-fork\src\app\tests\test_history_processor.py:101*

### test_format_description_status_transitions

**Category**: method_call  
**Description**: Test format_description for status transitions.  
**Expected**: self.assertEqual(format_description('status', 'Custom1', 'Custom2', MediaTypes.TV.value), 'Changed status from Custom1 to Custom2')  
**Confidence**: 0.85  

```python
self.assertEqual(format_description('status', Status.IN_PROGRESS.value, Status.DROPPED.value, MediaTypes.ANIME.value), 'Stopped watching')
self.assertEqual(format_description('status', 'Custom1', 'Custom2', MediaTypes.TV.value), 'Changed status from Custom1 to Custom2')
```

*Source: C:\yamtrack-fork\src\app\tests\test_history_processor.py:110*

### test_format_description_score

**Category**: method_call  
**Description**: Test format_description for score changes.  
**Expected**: self.assertEqual(format_description('score', 0, 7.0, MediaTypes.ANIME.value), 'Rated 7.0/10')  
**Confidence**: 0.85  

```python
self.assertEqual(format_description('score', None, 8.5, MediaTypes.TV.value), 'Rated 8.5/10')
self.assertEqual(format_description('score', 0, 7.0, MediaTypes.ANIME.value), 'Rated 7.0/10')
```

*Source: C:\yamtrack-fork\src\app\tests\test_history_processor.py:127*

### test_completed_progress

**Category**: method_call  
**Description**: When completed, the progress should be the total number of episodes.  
**Expected**: self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).progress, 26)  
**Confidence**: 0.85  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
item_anime = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/image.jpg')
self.anime = Anime.objects.create(item=item_anime, user=self.user, status=Status.PLANNING.value)

self.anime.save()
self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).progress, 26)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media.py:42*

### test_progress_is_max

**Category**: method_call  
**Description**: When progress is maximum number of episodes.

Status should be completed and end_date the current date if not specified.  
**Expected**: self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).status, Status.COMPLETED.value)  
**Confidence**: 0.85  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
item_anime = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/image.jpg')
self.anime = Anime.objects.create(item=item_anime, user=self.user, status=Status.PLANNING.value)

self.anime.save()
self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media.py:55*

### test_progress_is_max

**Category**: method_call  
**Description**: When progress is maximum number of episodes.

Status should be completed and end_date the current date if not specified.  
**Expected**: self.assertIsNotNone(Anime.objects.get(item__media_id='1', user=self.user).end_date)  
**Confidence**: 0.85  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
item_anime = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/image.jpg')
self.anime = Anime.objects.create(item=item_anime, user=self.user, status=Status.PLANNING.value)

self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).status, Status.COMPLETED.value)
self.assertIsNotNone(Anime.objects.get(item__media_id='1', user=self.user).end_date)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media.py:57*

### test_progress_bigger_than_max

**Category**: method_call  
**Description**: When progress is bigger than max, it should be set to max.  
**Expected**: self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).progress, 26)  
**Confidence**: 0.85  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
item_anime = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='http://example.com/image.jpg')
self.anime = Anime.objects.create(item=item_anime, user=self.user, status=Status.PLANNING.value)

self.anime.save()
self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).progress, 26)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media.py:69*

### test_completed_progress

**Category**: method_call  
**Description**: When completed, the progress should be the total number of episodes.  
**Expected**: self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).progress, 26)  
**Confidence**: 0.85  

```python
self.anime.save()
self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).progress, 26)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media.py:42*

### test_progress_is_max

**Category**: method_call  
**Description**: When progress is maximum number of episodes.

Status should be completed and end_date the current date if not specified.  
**Expected**: self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).status, Status.COMPLETED.value)  
**Confidence**: 0.85  

```python
self.anime.save()
self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).status, Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media.py:55*

### test_progress_is_max

**Category**: method_call  
**Description**: When progress is maximum number of episodes.

Status should be completed and end_date the current date if not specified.  
**Expected**: self.assertIsNotNone(Anime.objects.get(item__media_id='1', user=self.user).end_date)  
**Confidence**: 0.85  

```python
self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).status, Status.COMPLETED.value)
self.assertIsNotNone(Anime.objects.get(item__media_id='1', user=self.user).end_date)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media.py:57*

### test_progress_bigger_than_max

**Category**: method_call  
**Description**: When progress is bigger than max, it should be set to max.  
**Expected**: self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).progress, 26)  
**Confidence**: 0.85  

```python
self.anime.save()
self.assertEqual(Anime.objects.get(item__media_id='1', user=self.user).progress, 26)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_media.py:69*

### test_form_widget

**Category**: method_call  
**Description**: Test that the form uses the correct widget.  
**Expected**: self.assertEqual(form.fields['notification_urls'].widget.attrs['wrap'], 'off')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.valid_discord_url = 'discord://webhook_id/webhook_token'
self.valid_telegram_url = 'tgram://bot_token/chat_id'
self.invalid_url = 'invalid://not_a_real_url'

self.assertEqual(form.fields['notification_urls'].widget.attrs['rows'], 5)
self.assertEqual(form.fields['notification_urls'].widget.attrs['wrap'], 'off')
```

*Source: C:\yamtrack-fork\src\users\tests\test_forms.py:35*

### test_form_widget

**Category**: method_call  
**Description**: Test that the form uses the correct widget.  
**Expected**: self.assertIn('placeholder', form.fields['notification_urls'].widget.attrs)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.valid_discord_url = 'discord://webhook_id/webhook_token'
self.valid_telegram_url = 'tgram://bot_token/chat_id'
self.invalid_url = 'invalid://not_a_real_url'

self.assertEqual(form.fields['notification_urls'].widget.attrs['wrap'], 'off')
self.assertIn('placeholder', form.fields['notification_urls'].widget.attrs)
```

*Source: C:\yamtrack-fork\src\users\tests\test_forms.py:36*

### test_valid_single_url

**Category**: method_call  
**Description**: Test form with a single valid URL.  
**Expected**: mock_add.assert_called_once_with(self.valid_discord_url)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.valid_discord_url = 'discord://webhook_id/webhook_token'
self.valid_telegram_url = 'tgram://bot_token/chat_id'
self.invalid_url = 'invalid://not_a_real_url'

self.assertTrue(form.is_valid())
mock_add.assert_called_once_with(self.valid_discord_url)
```

*Source: C:\yamtrack-fork\src\users\tests\test_forms.py:51*

### test_valid_multiple_urls

**Category**: method_call  
**Description**: Test form with multiple valid URLs.  
**Expected**: self.assertEqual(mock_add.call_count, 2)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.valid_discord_url = 'discord://webhook_id/webhook_token'
self.valid_telegram_url = 'tgram://bot_token/chat_id'
self.invalid_url = 'invalid://not_a_real_url'

self.assertTrue(form.is_valid())
self.assertEqual(mock_add.call_count, 2)
```

*Source: C:\yamtrack-fork\src\users\tests\test_forms.py:66*

### test_valid_multiple_urls

**Category**: method_call  
**Description**: Test form with multiple valid URLs.  
**Expected**: mock_add.assert_any_call(self.valid_discord_url)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.valid_discord_url = 'discord://webhook_id/webhook_token'
self.valid_telegram_url = 'tgram://bot_token/chat_id'
self.invalid_url = 'invalid://not_a_real_url'

self.assertEqual(mock_add.call_count, 2)
mock_add.assert_any_call(self.valid_discord_url)
```

*Source: C:\yamtrack-fork\src\users\tests\test_forms.py:67*

### test_valid_multiple_urls

**Category**: method_call  
**Description**: Test form with multiple valid URLs.  
**Expected**: mock_add.assert_any_call(self.valid_telegram_url)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.valid_discord_url = 'discord://webhook_id/webhook_token'
self.valid_telegram_url = 'tgram://bot_token/chat_id'
self.invalid_url = 'invalid://not_a_real_url'

mock_add.assert_any_call(self.valid_discord_url)
mock_add.assert_any_call(self.valid_telegram_url)
```

*Source: C:\yamtrack-fork\src\users\tests\test_forms.py:68*

### test_empty_urls

**Category**: method_call  
**Description**: Test form with empty URLs.  
**Expected**: mock_add.assert_not_called()  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.valid_discord_url = 'discord://webhook_id/webhook_token'
self.valid_telegram_url = 'tgram://bot_token/chat_id'
self.invalid_url = 'invalid://not_a_real_url'

self.assertTrue(form.is_valid())
mock_add.assert_not_called()
```

*Source: C:\yamtrack-fork\src\users\tests\test_forms.py:81*

### test_whitespace_only_urls

**Category**: method_call  
**Description**: Test form with whitespace-only URLs.  
**Expected**: mock_add.assert_not_called()  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.valid_discord_url = 'discord://webhook_id/webhook_token'
self.valid_telegram_url = 'tgram://bot_token/chat_id'
self.invalid_url = 'invalid://not_a_real_url'

self.assertTrue(form.is_valid())
mock_add.assert_not_called()
```

*Source: C:\yamtrack-fork\src\users\tests\test_forms.py:94*

### test_invalid_url

**Category**: method_call  
**Description**: Test form with an invalid URL.  
**Expected**: self.assertIn('notification_urls', form.errors)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.valid_discord_url = 'discord://webhook_id/webhook_token'
self.valid_telegram_url = 'tgram://bot_token/chat_id'
self.invalid_url = 'invalid://not_a_real_url'

self.assertFalse(form.is_valid())
self.assertIn('notification_urls', form.errors)
```

*Source: C:\yamtrack-fork\src\users\tests\test_forms.py:109*

### test_invalid_url

**Category**: method_call  
**Description**: Test form with an invalid URL.  
**Expected**: self.assertIn(f"'{self.invalid_url}' is not a valid Apprise URL.", form.errors['notification_urls'])  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.valid_discord_url = 'discord://webhook_id/webhook_token'
self.valid_telegram_url = 'tgram://bot_token/chat_id'
self.invalid_url = 'invalid://not_a_real_url'

self.assertIn('notification_urls', form.errors)
self.assertIn(f"'{self.invalid_url}' is not a valid Apprise URL.", form.errors['notification_urls'])
```

*Source: C:\yamtrack-fork\src\users\tests\test_forms.py:110*

### test_tv_save

**Category**: method_call  
**Description**: Test the custom save method of the TV model.  
**Expected**: self.assertEqual(self.tv.seasons.filter(status=Status.COMPLETED.value).count(), 10)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and a season with episodes.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
item_season1 = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=1)
season1 = Season.objects.create(item=item_season1, user=self.user, status=Status.IN_PROGRESS.value)
self.tv = TV.objects.get(user=self.user)
item_ep1 = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=1)
Episode.objects.create(item=item_ep1, related_season=season1, end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_ep2 = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=1, episode_number=2)
Episode.objects.create(item=item_ep2, related_season=season1, end_date=datetime(2023, 6, 2, 0, 0, tzinfo=UTC))
item_season2 = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='http://example.com/image.jpg', season_number=2)
season2 = Season.objects.create(item=item_season2, related_tv=self.tv, user=self.user, status=Status.IN_PROGRESS.value)
item_ep3 = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=2, episode_number=1)
Episode.objects.create(item=item_ep3, related_season=season2, end_date=datetime(2023, 6, 4, 0, 0, tzinfo=UTC))
item_ep4 = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='http://example.com/image.jpg', season_number=2, episode_number=2)
Episode.objects.create(item=item_ep4, related_season=season2, end_date=datetime(2023, 6, 5, 0, 0, tzinfo=UTC))

self.tv.save(update_fields=['status'])
self.assertEqual(self.tv.seasons.filter(status=Status.COMPLETED.value).count(), 10)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_tv.py:145*

### test_completed_status_creates_all_seasons

**Category**: method_call  
**Description**: Test setting status to COMPLETED creates all seasons.  
**Expected**: self.assertEqual(self.tv.seasons.count(), 3)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.tv_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test Show', image='http://example.com/image.jpg')
self.tv = TV.objects.create(item=self.tv_item, user=self.user, status=Status.PLANNING.value)
self.season1_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=1)
self.season1 = Season.objects.create(item=self.season1_item, user=self.user, related_tv=self.tv, status=Status.IN_PROGRESS.value)
self.season2_item = Item.objects.create(media_id='123', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Test Show', image='http://example.com/image.jpg', season_number=2)
self.season2 = Season.objects.create(item=self.season2_item, user=self.user, related_tv=self.tv, status=Status.PLANNING.value)

self.tv.save()
self.assertEqual(self.tv.seasons.count(), 3)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_tv.py:245*

### test_export_csv

**Category**: method_call  
**Description**: Basic test exporting media to CSV.  
**Expected**: self.assertEqual(response['Content-Type'], 'text/csv')  
**Confidence**: 0.85  

```python
# Setup
'Create necessary data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.client.login(**self.credentials)
item_movie = Item.objects.create(media_id='10494', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Perfect Blue', image='https://image.url')
Movie.objects.create(item=item_movie, user=self.user, score=9, status=Status.COMPLETED.value, notes='Nice', start_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC), end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='https://image.url', season_number=1)
season = Season.objects.create(item=item_season, user=self.user, score=9, status=Status.IN_PROGRESS.value, notes='Nice')
item_episode = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='https://image.url', season_number=1, episode_number=1)
Episode.objects.create(item=item_episode, related_season=season, end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_anime = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='https://image.url')
Anime.objects.create(item=item_anime, user=self.user, status=Status.IN_PROGRESS.value, progress=2, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_manga = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='https://image.url')
Manga.objects.create(item=item_manga, user=self.user, status=Status.IN_PROGRESS.value, progress=2, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_game = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Witcher 3: Wild Hunt', image='https://image.url')
Game.objects.create(item=item_game, user=self.user, status=Status.IN_PROGRESS.value, progress=120, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_book = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='Fantastic Mr. Fox', image='https://image.url')
Book.objects.create(item=item_book, user=self.user, status=Status.IN_PROGRESS.value, progress=120, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))

self.assertEqual(response.status_code, 200)
self.assertEqual(response['Content-Type'], 'text/csv')
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_exports.py:149*

### test_export_csv

**Category**: method_call  
**Description**: Basic test exporting media to CSV.  
**Expected**: self.assertEqual(response['Content-Type'], 'text/csv')  
**Confidence**: 0.85  

```python
self.assertEqual(response.status_code, 200)
self.assertEqual(response['Content-Type'], 'text/csv')
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_exports.py:149*

### test_import_counts

**Category**: method_call  
**Description**: Test basic counts of imported media.  
**Expected**: self.assertEqual(Manga.objects.filter(user=self.user).count(), 1)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_yamtrack.csv').open('rb') as file:
    self.import_results = yamtrack.importer(file, self.user, 'new')

self.assertEqual(Anime.objects.filter(user=self.user).count(), 1)
self.assertEqual(Manga.objects.filter(user=self.user).count(), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_yamtrack.py:38*

### test_import_counts

**Category**: method_call  
**Description**: Test basic counts of imported media.  
**Expected**: self.assertEqual(TV.objects.filter(user=self.user).count(), 1)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_yamtrack.csv').open('rb') as file:
    self.import_results = yamtrack.importer(file, self.user, 'new')

self.assertEqual(Manga.objects.filter(user=self.user).count(), 1)
self.assertEqual(TV.objects.filter(user=self.user).count(), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_yamtrack.py:39*

### test_import_counts

**Category**: method_call  
**Description**: Test basic counts of imported media.  
**Expected**: self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_yamtrack.csv').open('rb') as file:
    self.import_results = yamtrack.importer(file, self.user, 'new')

self.assertEqual(TV.objects.filter(user=self.user).count(), 1)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_yamtrack.py:40*

### test_import_counts

**Category**: method_call  
**Description**: Test basic counts of imported media.  
**Expected**: self.assertEqual(Season.objects.filter(user=self.user).count(), 1)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_yamtrack.csv').open('rb') as file:
    self.import_results = yamtrack.importer(file, self.user, 'new')

self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
self.assertEqual(Season.objects.filter(user=self.user).count(), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_yamtrack.py:41*

### test_import_counts

**Category**: method_call  
**Description**: Test basic counts of imported media.  
**Expected**: self.assertEqual(Episode.objects.filter(related_season__user=self.user).count(), 24)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_yamtrack.csv').open('rb') as file:
    self.import_results = yamtrack.importer(file, self.user, 'new')

self.assertEqual(Season.objects.filter(user=self.user).count(), 1)
self.assertEqual(Episode.objects.filter(related_season__user=self.user).count(), 24)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_yamtrack.py:42*

### test_historical_records

**Category**: method_call  
**Description**: Test historical records creation during import.  
**Expected**: self.assertEqual(anime.history.first().history_date, datetime(2024, 2, 9, 10, 0, 0, tzinfo=UTC))  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_yamtrack.csv').open('rb') as file:
    self.import_results = yamtrack.importer(file, self.user, 'new')

self.assertEqual(anime.history.count(), 1)
self.assertEqual(anime.history.first().history_date, datetime(2024, 2, 9, 10, 0, 0, tzinfo=UTC))
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_yamtrack.py:51*

### test_historical_records

**Category**: method_call  
**Description**: Test historical records creation during import.  
**Expected**: self.assertEqual(movie.history.first().history_date, datetime(2024, 2, 9, 15, 30, 0, tzinfo=UTC))  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_yamtrack.csv').open('rb') as file:
    self.import_results = yamtrack.importer(file, self.user, 'new')

self.assertEqual(movie.history.count(), 1)
self.assertEqual(movie.history.first().history_date, datetime(2024, 2, 9, 15, 30, 0, tzinfo=UTC))
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_yamtrack.py:58*

### test_historical_records

**Category**: method_call  
**Description**: Test historical records creation during import.  
**Expected**: self.assertEqual(tv.history.first().history_date, datetime(2024, 2, 9, 12, 0, 0, tzinfo=UTC))  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_yamtrack.csv').open('rb') as file:
    self.import_results = yamtrack.importer(file, self.user, 'new')

self.assertEqual(tv.history.count(), 1)
self.assertEqual(tv.history.first().history_date, datetime(2024, 2, 9, 12, 0, 0, tzinfo=UTC))
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_yamtrack.py:65*

### test_import_counts

**Category**: method_call  
**Description**: Test basic counts of imported media.  
**Expected**: self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_yamtrack_partials.csv').open('rb') as file:
    self.import_results = yamtrack.importer(file, self.user, 'new')

self.assertEqual(Book.objects.filter(user=self.user).count(), 3)
self.assertEqual(Movie.objects.filter(user=self.user).count(), 1)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_yamtrack.py:135*

### test_end_dates

**Category**: method_call  
**Description**: Test end dates during import.  
**Expected**: self.assertEqual(books[0].end_date, datetime(2024, 5, 9, 0, 0, 0, tzinfo=UTC))  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_yamtrack_partials.csv').open('rb') as file:
    self.import_results = yamtrack.importer(file, self.user, 'new')

self.assertEqual(len(books), 3)
self.assertEqual(books[0].end_date, datetime(2024, 5, 9, 0, 0, 0, tzinfo=UTC))
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_yamtrack.py:199*

### test_preferences_get

**Category**: method_call  
**Description**: Test GET request to preferences view.  
**Expected**: self.assertTemplateUsed(response, 'users/preferences.html')  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.watch_regions_patcher = patch('users.views.tmdb.watch_provider_regions', return_value=[('UNSET', 'Disabled'), ('US', 'United States')])
self.watch_regions_patcher.start()
self.addCleanup(self.watch_regions_patcher.stop)
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'users/preferences.html')
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_sidebar.py:30*

### test_preferences_get

**Category**: method_call  
**Description**: Test GET request to preferences view.  
**Expected**: self.assertIn('media_types', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.watch_regions_patcher = patch('users.views.tmdb.watch_provider_regions', return_value=[('UNSET', 'Disabled'), ('US', 'United States')])
self.watch_regions_patcher.start()
self.addCleanup(self.watch_regions_patcher.stop)
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertTemplateUsed(response, 'users/preferences.html')
self.assertIn('media_types', response.context)
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_sidebar.py:31*

### test_preferences_get

**Category**: method_call  
**Description**: Test GET request to preferences view.  
**Expected**: self.assertIn(MediaTypes.TV.value, response.context['media_types'])  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.watch_regions_patcher = patch('users.views.tmdb.watch_provider_regions', return_value=[('UNSET', 'Disabled'), ('US', 'United States')])
self.watch_regions_patcher.start()
self.addCleanup(self.watch_regions_patcher.stop)
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertIn('media_types', response.context)
self.assertIn(MediaTypes.TV.value, response.context['media_types'])
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_sidebar.py:33*

### test_preferences_get

**Category**: method_call  
**Description**: Test GET request to preferences view.  
**Expected**: self.assertIn(MediaTypes.MOVIE.value, response.context['media_types'])  
**Confidence**: 0.85  

```python
# Setup
'Create user for the tests.'
self.watch_regions_patcher = patch('users.views.tmdb.watch_provider_regions', return_value=[('UNSET', 'Disabled'), ('US', 'United States')])
self.watch_regions_patcher.start()
self.addCleanup(self.watch_regions_patcher.stop)
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertIn(MediaTypes.TV.value, response.context['media_types'])
self.assertIn(MediaTypes.MOVIE.value, response.context['media_types'])
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_sidebar.py:34*

### test_media_search_view

**Category**: method_call  
**Description**: Test the media search view.  
**Expected**: self.assertTemplateUsed(response, 'app/search.html')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/search.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_search.py:44*

### test_media_search_view

**Category**: method_call  
**Description**: Test the media search view.  
**Expected**: self.assertEqual(self.user.last_search_type, MediaTypes.MOVIE.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.user.refresh_from_db()
self.assertEqual(self.user.last_search_type, MediaTypes.MOVIE.value)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_search.py:47*

### test_media_search_view

**Category**: method_call  
**Description**: Test the media search view.  
**Expected**: mock_search.assert_called_once_with(MediaTypes.MOVIE.value, 'test', 1, Sources.TMDB.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(self.user.last_search_type, MediaTypes.MOVIE.value)
mock_search.assert_called_once_with(MediaTypes.MOVIE.value, 'test', 1, Sources.TMDB.value)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_search.py:48*

### test_music_search_view

**Category**: method_call  
**Description**: Test the media search view for music.  
**Expected**: self.assertTemplateUsed(response, 'app/search.html')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/search.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_search.py:82*

### test_music_search_view

**Category**: method_call  
**Description**: Test the media search view for music.  
**Expected**: mock_search.assert_called_once_with(MediaTypes.MUSIC.value, 'Beatles', 1, Sources.MUSICBRAINZ.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertTemplateUsed(response, 'app/search.html')
mock_search.assert_called_once_with(MediaTypes.MUSIC.value, 'Beatles', 1, Sources.MUSICBRAINZ.value)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_search.py:83*

### test_media_search_view

**Category**: method_call  
**Description**: Test the media search view.  
**Expected**: self.assertTemplateUsed(response, 'app/search.html')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
# Fixtures: mock_search

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/search.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_search.py:44*

### test_media_search_view

**Category**: method_call  
**Description**: Test the media search view.  
**Expected**: self.assertEqual(self.user.last_search_type, MediaTypes.MOVIE.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
# Fixtures: mock_search

self.user.refresh_from_db()
self.assertEqual(self.user.last_search_type, MediaTypes.MOVIE.value)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_search.py:47*

### test_media_search_view

**Category**: method_call  
**Description**: Test the media search view.  
**Expected**: mock_search.assert_called_once_with(MediaTypes.MOVIE.value, 'test', 1, Sources.TMDB.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
# Fixtures: mock_search

self.assertEqual(self.user.last_search_type, MediaTypes.MOVIE.value)
mock_search.assert_called_once_with(MediaTypes.MOVIE.value, 'test', 1, Sources.TMDB.value)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_search.py:48*

### test_music_search_view

**Category**: method_call  
**Description**: Test the media search view for music.  
**Expected**: self.assertTemplateUsed(response, 'app/search.html')  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
# Fixtures: mock_search

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/search.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_search.py:82*

### test_music_search_view

**Category**: method_call  
**Description**: Test the media search view for music.  
**Expected**: mock_search.assert_called_once_with(MediaTypes.MUSIC.value, 'Beatles', 1, Sources.MUSICBRAINZ.value)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
# Fixtures: mock_search

self.assertTemplateUsed(response, 'app/search.html')
mock_search.assert_called_once_with(MediaTypes.MUSIC.value, 'Beatles', 1, Sources.MUSICBRAINZ.value)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_media_search.py:83*

### test_update_preference_no_new_value

**Category**: method_call  
**Description**: Test update_preference when no new value is provided.  
**Expected**: self.assertEqual(self.user.home_sort, HomeSortChoices.UPCOMING)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.user.refresh_from_db()
self.assertEqual(self.user.home_sort, HomeSortChoices.UPCOMING)
```

*Source: C:\yamtrack-fork\src\users\tests\test_models.py:37*

### test_update_preference_same_value

**Category**: method_call  
**Description**: Test update_preference when the new value is the same as current.  
**Expected**: self.assertEqual(self.user.home_sort, HomeSortChoices.UPCOMING)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.user.refresh_from_db()
self.assertEqual(self.user.home_sort, HomeSortChoices.UPCOMING)
```

*Source: C:\yamtrack-fork\src\users\tests\test_models.py:52*

### test_update_preference_valid_value

**Category**: method_call  
**Description**: Test update_preference with a valid new value.  
**Expected**: self.assertEqual(self.user.home_sort, HomeSortChoices.TITLE)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.user.refresh_from_db()
self.assertEqual(self.user.home_sort, HomeSortChoices.TITLE)
```

*Source: C:\yamtrack-fork\src\users\tests\test_models.py:67*

### test_update_preference_invalid_value

**Category**: method_call  
**Description**: Test update_preference with an invalid new value.  
**Expected**: self.assertEqual(self.user.home_sort, HomeSortChoices.UPCOMING)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.user.refresh_from_db()
self.assertEqual(self.user.home_sort, HomeSortChoices.UPCOMING)
```

*Source: C:\yamtrack-fork\src\users\tests\test_models.py:82*

### test_update_preference_boolean_field

**Category**: method_call  
**Description**: Test update_preference with a boolean field.  
**Expected**: self.assertEqual(self.user.tv_enabled, False)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.user.refresh_from_db()
self.assertEqual(self.user.tv_enabled, False)
```

*Source: C:\yamtrack-fork\src\users\tests\test_models.py:97*

### test_update_preference_last_search_type_valid

**Category**: method_call  
**Description**: Test update_preference with last_search_type and valid value.  
**Expected**: self.assertEqual(self.user.last_search_type, MediaTypes.MOVIE.value)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.user.refresh_from_db()
self.assertEqual(self.user.last_search_type, MediaTypes.MOVIE.value)
```

*Source: C:\yamtrack-fork\src\users\tests\test_models.py:112*

### test_update_preference_last_search_type_invalid

**Category**: method_call  
**Description**: Test update_preference with last_search_type and invalid value.  
**Expected**: self.assertEqual(self.user.last_search_type, MediaTypes.TV.value)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.user.refresh_from_db()
self.assertEqual(self.user.last_search_type, MediaTypes.TV.value)
```

*Source: C:\yamtrack-fork\src\users\tests\test_models.py:130*

### test_update_preference_daily_digest_enabled

**Category**: method_call  
**Description**: Test update_preference with daily_digest_enabled field.  
**Expected**: self.assertEqual(self.user.daily_digest_enabled, False)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.user.refresh_from_db()
self.assertEqual(self.user.daily_digest_enabled, False)
```

*Source: C:\yamtrack-fork\src\users\tests\test_models.py:148*

### test_lists_owner_view

**Category**: method_call  
**Description**: Test the lists view response and context for owner.  
**Expected**: self.assertTemplateUsed(response, 'lists/custom_lists.html')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for lists view tests.'
self.factory = RequestFactory()
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.collaborator_credentials = {'username': 'collaborator', 'password': '12345'}
self.collaborator = get_user_model().objects.create_user(**self.collaborator_credentials)
self.list1 = CustomList.objects.create(name='Test List 1', description='Description 1', owner=self.user)
self.list2 = CustomList.objects.create(name='Test List 2', description='Description 2', owner=self.user)
self.list1.collaborators.add(self.collaborator)
self.item1 = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.item2 = Item.objects.create(media_id='2', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
CustomListItem.objects.create(custom_list=self.list1, item=self.item1)
CustomListItem.objects.create(custom_list=self.list2, item=self.item2)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'lists/custom_lists.html')
```

*Source: C:\yamtrack-fork\src\lists\tests\test_views.py:71*

### test_lists_owner_view

**Category**: method_call  
**Description**: Test the lists view response and context for owner.  
**Expected**: self.assertIn('custom_lists', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for lists view tests.'
self.factory = RequestFactory()
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.collaborator_credentials = {'username': 'collaborator', 'password': '12345'}
self.collaborator = get_user_model().objects.create_user(**self.collaborator_credentials)
self.list1 = CustomList.objects.create(name='Test List 1', description='Description 1', owner=self.user)
self.list2 = CustomList.objects.create(name='Test List 2', description='Description 2', owner=self.user)
self.list1.collaborators.add(self.collaborator)
self.item1 = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.item2 = Item.objects.create(media_id='2', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
CustomListItem.objects.create(custom_list=self.list1, item=self.item1)
CustomListItem.objects.create(custom_list=self.list2, item=self.item2)

self.assertTemplateUsed(response, 'lists/custom_lists.html')
self.assertIn('custom_lists', response.context)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_views.py:72*

### test_lists_owner_view

**Category**: method_call  
**Description**: Test the lists view response and context for owner.  
**Expected**: self.assertIn('form', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for lists view tests.'
self.factory = RequestFactory()
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.collaborator_credentials = {'username': 'collaborator', 'password': '12345'}
self.collaborator = get_user_model().objects.create_user(**self.collaborator_credentials)
self.list1 = CustomList.objects.create(name='Test List 1', description='Description 1', owner=self.user)
self.list2 = CustomList.objects.create(name='Test List 2', description='Description 2', owner=self.user)
self.list1.collaborators.add(self.collaborator)
self.item1 = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.item2 = Item.objects.create(media_id='2', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
CustomListItem.objects.create(custom_list=self.list1, item=self.item1)
CustomListItem.objects.create(custom_list=self.list2, item=self.item2)

self.assertIn('custom_lists', response.context)
self.assertIn('form', response.context)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_views.py:73*

### test_lists_collaborator_view

**Category**: method_call  
**Description**: Test the lists view response and context for a collaborator.  
**Expected**: self.assertTemplateUsed(response, 'lists/custom_lists.html')  
**Confidence**: 0.85  

```python
# Setup
'Set up test data for lists view tests.'
self.factory = RequestFactory()
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.collaborator_credentials = {'username': 'collaborator', 'password': '12345'}
self.collaborator = get_user_model().objects.create_user(**self.collaborator_credentials)
self.list1 = CustomList.objects.create(name='Test List 1', description='Description 1', owner=self.user)
self.list2 = CustomList.objects.create(name='Test List 2', description='Description 2', owner=self.user)
self.list1.collaborators.add(self.collaborator)
self.item1 = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie')
self.item2 = Item.objects.create(media_id='2', source=Sources.TMDB.value, media_type=MediaTypes.TV.value, title='Test TV Show')
CustomListItem.objects.create(custom_list=self.list1, item=self.item1)
CustomListItem.objects.create(custom_list=self.list2, item=self.item2)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'lists/custom_lists.html')
```

*Source: C:\yamtrack-fork\src\lists\tests\test_views.py:80*

### test_music

**Category**: method_call  
**Description**: Test the search method for music.

Assert that all required keys are present in each entry and pagination fields exist.  
**Expected**: self.assertIn('total_results', response)  
**Confidence**: 0.85  

```python
self.assertIn('page', response)
self.assertIn('total_results', response)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_search.py:128*

### test_music

**Category**: method_call  
**Description**: Test the search method for music.

Assert that all required keys are present in each entry and pagination fields exist.  
**Expected**: self.assertIn('total_pages', response)  
**Confidence**: 0.85  

```python
self.assertIn('total_results', response)
self.assertIn('total_pages', response)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_search.py:129*

### test_music

**Category**: method_call  
**Description**: Test the search method for music.

Assert that all required keys are present in each entry and pagination fields exist.  
**Expected**: self.assertIn('results', response)  
**Confidence**: 0.85  

```python
self.assertIn('total_pages', response)
self.assertIn('results', response)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_search.py:130*

### test_music

**Category**: method_call  
**Description**: Test the search method for music.

Assert that all required keys are present in each entry and pagination fields exist.  
**Expected**: self.assertEqual(response['page'], 1)  
**Confidence**: 0.85  

```python
self.assertIn('results', response)
self.assertEqual(response['page'], 1)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_search.py:131*

### test_music

**Category**: method_call  
**Description**: Test the search method for music.

Assert that all required keys are present in each entry and pagination fields exist.  
**Expected**: self.assertIsInstance(response['results'], list)  
**Confidence**: 0.85  

```python
self.assertEqual(response['page'], 1)
self.assertIsInstance(response['results'], list)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_search.py:133*

### test_music_pagination

**Category**: method_call  
**Description**: Test the search method for music with pagination.  
**Expected**: self.assertIsInstance(response_page1['total_results'], int)  
**Confidence**: 0.85  

```python
self.assertEqual(response_page1['page'], 1)
self.assertIsInstance(response_page1['total_results'], int)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_search.py:148*

### test_music_pagination

**Category**: method_call  
**Description**: Test the search method for music with pagination.  
**Expected**: self.assertGreaterEqual(response_page1['total_results'], 0)  
**Confidence**: 0.85  

```python
self.assertIsInstance(response_page1['total_results'], int)
self.assertGreaterEqual(response_page1['total_results'], 0)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_search.py:149*

### test_music_pagination

**Category**: method_call  
**Description**: Test the search method for music with pagination.  
**Expected**: self.assertGreater(response_page1['total_pages'], 0)  
**Confidence**: 0.85  

```python
self.assertGreaterEqual(response_page1['total_results'], 0)
self.assertGreater(response_page1['total_pages'], 0)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_search.py:150*

### test_music_not_found

**Category**: method_call  
**Description**: Test the search method for music with no results.  
**Expected**: self.assertEqual(response['results'], [])  
**Confidence**: 0.85  

```python
self.assertIn('results', response)
self.assertEqual(response['results'], [])
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_search.py:164*

### test_senscritique_music

**Category**: method_call  
**Description**: Test the search method for music from SensCritique.

Assert that all required keys are present in each entry and pagination fields exist.  
**Expected**: self.assertIn('total_results', response)  
**Confidence**: 0.85  

```python
self.assertIn('page', response)
self.assertIn('total_results', response)
```

*Source: C:\yamtrack-fork\src\app\tests\providers\test_search.py:178*

### test_statistics_view_default_date_range

**Category**: method_call  
**Description**: Test the statistics view with default date range (last year).  
**Expected**: self.assertTemplateUsed(response, 'app/statistics.html')  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'app/statistics.html')
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_statistics.py:20*

### test_statistics_view_default_date_range

**Category**: method_call  
**Description**: Test the statistics view with default date range (last year).  
**Expected**: self.assertIn('media_count', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertTemplateUsed(response, 'app/statistics.html')
self.assertIn('media_count', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_statistics.py:21*

### test_statistics_view_default_date_range

**Category**: method_call  
**Description**: Test the statistics view with default date range (last year).  
**Expected**: self.assertIn('activity_data', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertIn('media_count', response.context)
self.assertIn('activity_data', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_statistics.py:23*

### test_statistics_view_default_date_range

**Category**: method_call  
**Description**: Test the statistics view with default date range (last year).  
**Expected**: self.assertIn('media_type_distribution', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertIn('activity_data', response.context)
self.assertIn('media_type_distribution', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_statistics.py:24*

### test_statistics_view_default_date_range

**Category**: method_call  
**Description**: Test the statistics view with default date range (last year).  
**Expected**: self.assertIn('score_distribution', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertIn('media_type_distribution', response.context)
self.assertIn('score_distribution', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_statistics.py:25*

### test_statistics_view_default_date_range

**Category**: method_call  
**Description**: Test the statistics view with default date range (last year).  
**Expected**: self.assertIn('status_distribution', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertIn('score_distribution', response.context)
self.assertIn('status_distribution', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_statistics.py:26*

### test_statistics_view_default_date_range

**Category**: method_call  
**Description**: Test the statistics view with default date range (last year).  
**Expected**: self.assertIn('status_pie_chart_data', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertIn('status_distribution', response.context)
self.assertIn('status_pie_chart_data', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_statistics.py:27*

### test_statistics_view_default_date_range

**Category**: method_call  
**Description**: Test the statistics view with default date range (last year).  
**Expected**: self.assertIn('extended_statistics', response.context)  
**Confidence**: 0.85  

```python
# Setup
'Create a user and log in.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

self.assertIn('status_pie_chart_data', response.context)
self.assertIn('extended_statistics', response.context)
```

*Source: C:\yamtrack-fork\src\app\tests\views\test_statistics.py:28*

### test_import_steam_games

**Category**: method_call  
**Description**: Test importing games from Steam.  
**Expected**: self.assertEqual(cs2_game.progress, 1250)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(cs2_game.status, Status.IN_PROGRESS.value)
self.assertEqual(cs2_game.progress, 1250)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_steam.py:92*

### test_import_steam_games

**Category**: method_call  
**Description**: Test importing games from Steam.  
**Expected**: self.assertEqual(dota_game.progress, 0)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(dota_game.status, Status.PLANNING.value)
self.assertEqual(dota_game.progress, 0)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_steam.py:96*

### test_import_steam_games

**Category**: method_call  
**Description**: Test importing games from Steam.  
**Expected**: self.assertEqual(tf2_game.progress, 500)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(tf2_game.status, Status.PAUSED.value)
self.assertEqual(tf2_game.progress, 500)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_steam.py:100*

### test_import_steam_game_not_found_in_igdb

**Category**: method_call  
**Description**: Test handling of games not found in IGDB.  
**Expected**: self.assertIn('Unknown Game (999)', warnings)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertEqual(imported_counts.get(MediaTypes.GAME.value, 0), 0)
self.assertIn('Unknown Game (999)', warnings)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_steam.py:144*

### test_import_steam_game_not_found_in_igdb

**Category**: method_call  
**Description**: Test handling of games not found in IGDB.  
**Expected**: self.assertIn(f"Couldn't find a match in {Sources.IGDB.label}", warnings)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertIn('Unknown Game (999)', warnings)
self.assertIn(f"Couldn't find a match in {Sources.IGDB.label}", warnings)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_steam.py:146*

### test_import_steam_game_not_found_in_igdb

**Category**: method_call  
**Description**: Test handling of games not found in IGDB.  
**Expected**: self.assertEqual(Game.objects.filter(user=self.user).count(), 0)  
**Confidence**: 0.85  
**Tags**: mock  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

self.assertIn(f"Couldn't find a match in {Sources.IGDB.label}", warnings)
self.assertEqual(Game.objects.filter(user=self.user).count(), 0)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_steam.py:147*

### test_custom_list_form_valid

**Category**: instantiation  
**Description**: Instantiate CustomListForm: Test the form with valid data.  
**Expected**: self.assertTrue(form.is_valid())  
**Confidence**: 0.80  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

form = CustomListForm(data=form_data)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_forms.py:21*

### test_custom_list_form_invalid

**Category**: instantiation  
**Description**: Instantiate CustomListForm: Test the form with invalid data.  
**Expected**: self.assertFalse(form.is_valid())  
**Confidence**: 0.80  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

form = CustomListForm(data=form_data)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_forms.py:30*

### test_custom_list_form_with_collaborators

**Category**: instantiation  
**Description**: Instantiate create_user: Test the form with collaborators.  
**Expected**: self.assertTrue(form.is_valid())  
**Confidence**: 0.80  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

collaborator = get_user_model().objects.create_user(**self.credentials)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_forms.py:37*

### test_custom_list_form_with_collaborators

**Category**: instantiation  
**Description**: Instantiate CustomListForm: Test the form with collaborators.  
**Expected**: self.assertTrue(form.is_valid())  
**Confidence**: 0.80  

```python
# Setup
'Create a user.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)

form = CustomListForm(data=form_data)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_forms.py:43*

### test_custom_list_form_valid

**Category**: instantiation  
**Description**: Instantiate CustomListForm: Test the form with valid data.  
**Expected**: self.assertTrue(form.is_valid())  
**Confidence**: 0.80  

```python
form = CustomListForm(data=form_data)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_forms.py:21*

### test_custom_list_form_invalid

**Category**: instantiation  
**Description**: Instantiate CustomListForm: Test the form with invalid data.  
**Expected**: self.assertFalse(form.is_valid())  
**Confidence**: 0.80  

```python
form = CustomListForm(data=form_data)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_forms.py:30*

### test_custom_list_form_with_collaborators

**Category**: instantiation  
**Description**: Instantiate create_user: Test the form with collaborators.  
**Expected**: self.assertTrue(form.is_valid())  
**Confidence**: 0.80  

```python
collaborator = get_user_model().objects.create_user(**self.credentials)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_forms.py:37*

### test_custom_list_form_with_collaborators

**Category**: instantiation  
**Description**: Instantiate CustomListForm: Test the form with collaborators.  
**Expected**: self.assertTrue(form.is_valid())  
**Confidence**: 0.80  

```python
form = CustomListForm(data=form_data)
```

*Source: C:\yamtrack-fork\src\lists\tests\test_forms.py:43*

### test_demo_user_cannot_change_username

**Category**: instantiation  
**Description**: Instantiate post: Test that demo users cannot change their username.  
**Expected**: self.assertEqual(auth.get_user(self.client).username, 'testuser')  
**Confidence**: 0.80  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'testuser', 'password': 'testpass123'}
self.user = get_user_model().objects.create_user(**self.credentials)
self.client.login(**self.credentials)

response = self.client.post(reverse('account'), {'username': 'new_username'})
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_demo_profile.py:21*

### test_demo_user_cannot_change_username

**Category**: instantiation  
**Description**: Instantiate post: Test that demo users cannot change their username.  
**Expected**: self.assertEqual(auth.get_user(self.client).username, 'testuser')  
**Confidence**: 0.80  

```python
response = self.client.post(reverse('account'), {'username': 'new_username'})
```

*Source: C:\yamtrack-fork\src\users\tests\views\test_demo_profile.py:21*

### test_stored_progress

**Category**: instantiation  
**Description**: Instantiate get: Test progress of imported books.  
**Expected**: self.assertEqual(read_book.status, Status.COMPLETED.value)  
**Confidence**: 0.80  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_goodreads.csv').open('rb') as file:
    self.import_results = goodreads.importer(file, self.user, 'new')

read_book = Book.objects.get(status=Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_goodreads.py:41*

### test_stored_progress

**Category**: instantiation  
**Description**: Instantiate get: Test progress of imported books.  
**Expected**: self.assertEqual(read_book.status, Status.IN_PROGRESS.value)  
**Confidence**: 0.80  

```python
# Setup
'Create user for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_user(**self.credentials)
with Path(mock_path / 'import_goodreads.csv').open('rb') as file:
    self.import_results = goodreads.importer(file, self.user, 'new')

read_book = Book.objects.get(status=Status.IN_PROGRESS.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_goodreads.py:45*

### test_stored_progress

**Category**: instantiation  
**Description**: Instantiate get: Test progress of imported books.  
**Expected**: self.assertEqual(read_book.status, Status.COMPLETED.value)  
**Confidence**: 0.80  

```python
read_book = Book.objects.get(status=Status.COMPLETED.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_goodreads.py:41*

### test_stored_progress

**Category**: instantiation  
**Description**: Instantiate get: Test progress of imported books.  
**Expected**: self.assertEqual(read_book.status, Status.IN_PROGRESS.value)  
**Confidence**: 0.80  

```python
read_book = Book.objects.get(status=Status.IN_PROGRESS.value)
```

*Source: C:\yamtrack-fork\src\integrations\tests\imports\test_goodreads.py:45*

### test_cleanup_user_messages_deletes_only_old_shown_messages

**Category**: instantiation  
**Description**: Instantiate create: Delete only shown messages older than the retention window.  
**Expected**: self.assertEqual(deleted_count, 1)  
**Confidence**: 0.80  

```python
# Setup
'Create a user for task tests.'
self.user = get_user_model().objects.create_user(username='test')

old_shown = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='old shown', shown_at=now - timedelta(days=31))
```

*Source: C:\yamtrack-fork\src\app\tests\test_tasks.py:24*

### test_cleanup_user_messages_deletes_only_old_shown_messages

**Category**: instantiation  
**Description**: Instantiate create: Delete only shown messages older than the retention window.  
**Expected**: self.assertEqual(deleted_count, 1)  
**Confidence**: 0.80  

```python
# Setup
'Create a user for task tests.'
self.user = get_user_model().objects.create_user(username='test')

recent_shown = UserMessage.objects.create(user=self.user, level=UserMessageLevel.INFO, message='recent shown', shown_at=now - timedelta(days=5))
```

*Source: C:\yamtrack-fork\src\app\tests\test_tasks.py:30*

### test_item_with_season_and_episode

**Category**: instantiation  
**Description**: Instantiate create: Test the string representation of an Item with season and episode.  
**Expected**: self.assertEqual(str(item), 'Test Show S1E2')  
**Confidence**: 0.80  

```python
# Setup
'Set up test data for Item model.'
self.item = Item.objects.create(media_id='1', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Test Movie', image='http://example.com/image.jpg')

item = Item.objects.create(media_id='2', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Show', image='http://example.com/image2.jpg', season_number=1, episode_number=2)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_item.py:40*

### test_item_with_season_and_episode

**Category**: instantiation  
**Description**: Instantiate create: Test the string representation of an Item with season and episode.  
**Expected**: self.assertEqual(str(item), 'Test Show S1E2')  
**Confidence**: 0.80  

```python
item = Item.objects.create(media_id='2', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Test Show', image='http://example.com/image2.jpg', season_number=1, episode_number=2)
```

*Source: C:\yamtrack-fork\src\app\tests\models\test_item.py:40*

### test_export_csv

**Category**: instantiation  
**Description**: Instantiate get: Basic test exporting media to CSV.  
**Expected**: self.assertEqual(response.status_code, 200)  
**Confidence**: 0.80  

```python
# Setup
'Create necessary data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.client.login(**self.credentials)
item_movie = Item.objects.create(media_id='10494', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Perfect Blue', image='https://image.url')
Movie.objects.create(item=item_movie, user=self.user, score=9, status=Status.COMPLETED.value, notes='Nice', start_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC), end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='https://image.url', season_number=1)
season = Season.objects.create(item=item_season, user=self.user, score=9, status=Status.IN_PROGRESS.value, notes='Nice')
item_episode = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='https://image.url', season_number=1, episode_number=1)
Episode.objects.create(item=item_episode, related_season=season, end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_anime = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='https://image.url')
Anime.objects.create(item=item_anime, user=self.user, status=Status.IN_PROGRESS.value, progress=2, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_manga = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='https://image.url')
Manga.objects.create(item=item_manga, user=self.user, status=Status.IN_PROGRESS.value, progress=2, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_game = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Witcher 3: Wild Hunt', image='https://image.url')
Game.objects.create(item=item_game, user=self.user, status=Status.IN_PROGRESS.value, progress=120, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_book = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='Fantastic Mr. Fox', image='https://image.url')
Book.objects.create(item=item_book, user=self.user, status=Status.IN_PROGRESS.value, progress=120, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))

response = self.client.get(reverse('export_csv'))
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_exports.py:146*

### test_export_csv

**Category**: instantiation  
**Description**: Instantiate decode: Basic test exporting media to CSV.  
**Confidence**: 0.80  

```python
# Setup
'Create necessary data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.client.login(**self.credentials)
item_movie = Item.objects.create(media_id='10494', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Perfect Blue', image='https://image.url')
Movie.objects.create(item=item_movie, user=self.user, score=9, status=Status.COMPLETED.value, notes='Nice', start_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC), end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='https://image.url', season_number=1)
season = Season.objects.create(item=item_season, user=self.user, score=9, status=Status.IN_PROGRESS.value, notes='Nice')
item_episode = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='https://image.url', season_number=1, episode_number=1)
Episode.objects.create(item=item_episode, related_season=season, end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_anime = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='https://image.url')
Anime.objects.create(item=item_anime, user=self.user, status=Status.IN_PROGRESS.value, progress=2, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_manga = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='https://image.url')
Manga.objects.create(item=item_manga, user=self.user, status=Status.IN_PROGRESS.value, progress=2, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_game = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Witcher 3: Wild Hunt', image='https://image.url')
Game.objects.create(item=item_game, user=self.user, status=Status.IN_PROGRESS.value, progress=120, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_book = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='Fantastic Mr. Fox', image='https://image.url')
Book.objects.create(item=item_book, user=self.user, status=Status.IN_PROGRESS.value, progress=120, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))

content = b''.join(response.streaming_content).decode('utf-8')
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_exports.py:155*

### test_export_csv

**Category**: instantiation  
**Description**: Instantiate DictReader: Basic test exporting media to CSV.  
**Confidence**: 0.80  

```python
# Setup
'Create necessary data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.client.login(**self.credentials)
item_movie = Item.objects.create(media_id='10494', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Perfect Blue', image='https://image.url')
Movie.objects.create(item=item_movie, user=self.user, score=9, status=Status.COMPLETED.value, notes='Nice', start_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC), end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='https://image.url', season_number=1)
season = Season.objects.create(item=item_season, user=self.user, score=9, status=Status.IN_PROGRESS.value, notes='Nice')
item_episode = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='https://image.url', season_number=1, episode_number=1)
Episode.objects.create(item=item_episode, related_season=season, end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_anime = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='https://image.url')
Anime.objects.create(item=item_anime, user=self.user, status=Status.IN_PROGRESS.value, progress=2, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_manga = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='https://image.url')
Manga.objects.create(item=item_manga, user=self.user, status=Status.IN_PROGRESS.value, progress=2, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_game = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Witcher 3: Wild Hunt', image='https://image.url')
Game.objects.create(item=item_game, user=self.user, status=Status.IN_PROGRESS.value, progress=120, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_book = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='Fantastic Mr. Fox', image='https://image.url')
Book.objects.create(item=item_book, user=self.user, status=Status.IN_PROGRESS.value, progress=120, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))

reader = csv.DictReader(StringIO(content))
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_exports.py:158*

### test_export_csv

**Category**: instantiation  
**Description**: Instantiate set: Basic test exporting media to CSV.  
**Confidence**: 0.80  

```python
# Setup
'Create necessary data for the tests.'
self.credentials = {'username': 'test', 'password': '12345'}
self.user = get_user_model().objects.create_superuser(**self.credentials)
self.client.login(**self.credentials)
item_movie = Item.objects.create(media_id='10494', source=Sources.TMDB.value, media_type=MediaTypes.MOVIE.value, title='Perfect Blue', image='https://image.url')
Movie.objects.create(item=item_movie, user=self.user, score=9, status=Status.COMPLETED.value, notes='Nice', start_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC), end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_season = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.SEASON.value, title='Friends', image='https://image.url', season_number=1)
season = Season.objects.create(item=item_season, user=self.user, score=9, status=Status.IN_PROGRESS.value, notes='Nice')
item_episode = Item.objects.create(media_id='1668', source=Sources.TMDB.value, media_type=MediaTypes.EPISODE.value, title='Friends', image='https://image.url', season_number=1, episode_number=1)
Episode.objects.create(item=item_episode, related_season=season, end_date=datetime(2023, 6, 1, 0, 0, tzinfo=UTC))
item_anime = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.ANIME.value, title='Cowboy Bebop', image='https://image.url')
Anime.objects.create(item=item_anime, user=self.user, status=Status.IN_PROGRESS.value, progress=2, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_manga = Item.objects.create(media_id='1', source=Sources.MAL.value, media_type=MediaTypes.MANGA.value, title='Berserk', image='https://image.url')
Manga.objects.create(item=item_manga, user=self.user, status=Status.IN_PROGRESS.value, progress=2, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_game = Item.objects.create(media_id='1', source=Sources.IGDB.value, media_type=MediaTypes.GAME.value, title='The Witcher 3: Wild Hunt', image='https://image.url')
Game.objects.create(item=item_game, user=self.user, status=Status.IN_PROGRESS.value, progress=120, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))
item_book = Item.objects.create(media_id='OL21733390M', source=Sources.OPENLIBRARY.value, media_type=MediaTypes.BOOK.value, title='Fantastic Mr. Fox', image='https://image.url')
Book.objects.create(item=item_book, user=self.user, status=Status.IN_PROGRESS.value, progress=120, start_date=datetime(2021, 6, 1, 0, 0, tzinfo=UTC))

db_media_ids = set(Item.objects.filter(Q(tv__user=self.user) | Q(movie__user=self.user) | Q(season__user=self.user) | Q(episode__related_season__user=self.user) | Q(anime__user=self.user) | Q(manga__user=self.user) | Q(game__user=self.user) | Q(book__user=self.user)).values_list('media_id', flat=True))
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_exports.py:160*

### test_export_csv

**Category**: instantiation  
**Description**: Instantiate get: Basic test exporting media to CSV.  
**Expected**: self.assertEqual(response.status_code, 200)  
**Confidence**: 0.80  

```python
response = self.client.get(reverse('export_csv'))
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_exports.py:146*

### test_export_csv

**Category**: instantiation  
**Description**: Instantiate decode: Basic test exporting media to CSV.  
**Confidence**: 0.80  

```python
content = b''.join(response.streaming_content).decode('utf-8')
```

*Source: C:\yamtrack-fork\src\integrations\tests\test_exports.py:155*

### test_config

**Category**: instantiation  
**Description**: Instantiate object: Test that the Gunicorn configuration file is valid.  
**Expected**: self.assertEqual(exit_code, 0)  
**Confidence**: 0.80  
**Tags**: mock, unittest  

```python
mock_argv = mock.patch.object(sys, 'argv', argv)
```

*Source: C:\yamtrack-fork\src\config\tests\test_gunicorn.py:24*

### test_config

**Category**: instantiation  
**Description**: Instantiate object: Test that the Gunicorn configuration file is valid.  
**Expected**: self.assertEqual(exit_code, 0)  
**Confidence**: 0.80  
**Tags**: mock, unittest  

```python
mock_argv = mock.patch.object(sys, 'argv', argv)
```

*Source: C:\yamtrack-fork\src\config\tests\test_gunicorn.py:24*

