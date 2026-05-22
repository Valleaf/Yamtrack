---
name: yamtrack-fork
description: Local codebase analysis for yamtrack-fork
doc_version: 
---

# yamtrack-fork Codebase

## Description

Local codebase analysis and documentation generated from code analysis.

**Path:** `C:\yamtrack-fork`
**Files Analyzed:** 0
**Languages:** 
**Analysis Depth:** surface

## When to Use This Skill

Use this skill when you need to:
- Understand the codebase architecture and design patterns
- Find implementation examples and usage patterns
- Review API documentation extracted from code
- Check configuration patterns and best practices
- Explore test examples and real-world usage
- Navigate the codebase structure efficiently

## ⚡ Quick Reference

### Codebase Statistics

**Languages:**

**Analysis Performed:**
- ✅ API Reference (C2.5)
- ✅ Dependency Graph (C2.6)
- ✅ Design Patterns (C3.1)
- ✅ Test Examples (C3.2)
- ✅ Configuration Patterns (C3.4)
- ✅ Architectural Analysis (C3.7)
- ✅ Project Documentation (C3.9)

### 🎨 Design Patterns Detected

*From C3.1 codebase analysis (confidence > 0.7)*

- **Adapter**: 1 instances

*Total: 1 high-confidence patterns*

*See `references/patterns/` for complete pattern analysis*

## 📝 Code Examples

*High-quality examples extracted from test files (C3.2)*

**Workflow: Test the metadata method for anime with mostly unknown data.** (complexity: 1.00)

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

**Workflow: Test the metadata method for movies with mostly unknown data.** (complexity: 1.00)

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

**Workflow: Test the process_episodes function for manual episodes.** (complexity: 1.00)

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

**Workflow: Test the get_edition_details function from Hardcover provider.** (complexity: 1.00)

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

**Workflow: Test the metadata method for anime with mostly unknown data.** (complexity: 1.00)

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

**Workflow: Test fetch_releases with all media types.** (complexity: 1.00)

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

**Workflow: Test fetch_releases with all media types.** (complexity: 1.00)

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

**Workflow: Test get_existing_media with different media types.** (complexity: 1.00)

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

**Workflow: Test get_existing_media with different media types.** (complexity: 1.00)

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

**Workflow: Test webhook handles TV episode mark played event.** (complexity: 1.00)

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

*See `references/test_examples/` for all extracted examples*

## ⚙️ Configuration Patterns

*From C3.4 configuration analysis*

**Configuration Files Analyzed:** 717
**Total Settings:** 184817
**Patterns Detected:** 0

**Configuration Types:**
- unknown: 717 files

*See `references/config_patterns/` for detailed configuration analysis*

## 📖 Project Documentation

*Extracted from markdown files in the project (C3.9)*

**Total Documentation Files:** 190
**Categories:** 6

### Overview

- **README.md** (`README.md`)

### Guides

- **anilist-date-parser.md** (`output\yamtrack-fork\tutorials\anilist-date-parser\anilist-date-parser.md`)
- **anime-episode-anidb-guid-mark-played.md** (`output\yamtrack-fork\tutorials\anime-episode-anidb-guid-mark-played\anime-episode-anidb-guid-mark-played.md`)
- **anime-episode-mark-played.md** (`output\yamtrack-fork\tutorials\anime-episode-mark-played\anime-episode-mark-played.md`)
- **anime-movie-mark-played.md** (`output\yamtrack-fork\tutorials\anime-movie-mark-played\anime-movie-mark-played.md`)
- **anime-unknown.md** (`output\yamtrack-fork\tutorials\anime-unknown\anime-unknown.md`)
- *...and 165 more*

### Api

- **api.md** (`output\djangoproject\references\api.md`)
- **contrib.md** (`output\djangoproject\references\contrib.md`)
- **howto.md** (`output\djangoproject\references\howto.md`)
- **index.md** (`output\djangoproject\references\index.md`)
- **internals.md** (`output\djangoproject\references\internals.md`)
- *...and 6 more*

### Examples

- **test_examples.md** (`output\yamtrack-fork\test_examples\test_examples.md`)

### Other

- **IMPORT_PIPELINE.md** (`.github\IMPORT_PIPELINE.md`)
- **IMPORTER_DEVELOPMENT.md** (`.github\IMPORTER_DEVELOPMENT.md`)
- **SKILL.md** (`output\djangoproject\SKILL.md`)
- **SKILL.md** (`output\SKILL.md`)
- **config_patterns.md** (`output\yamtrack-fork\config_patterns\config_patterns.md`)

### Templates

- **bug_report.md** (`.github\ISSUE_TEMPLATE\bug_report.md`)
- **feature_request.md** (`.github\ISSUE_TEMPLATE\feature_request.md`)

*See `references/documentation/` for all project documentation*

## 📚 Available References

This skill includes detailed reference documentation:

- **Dependencies**: `references/dependencies/` - Dependency graph and analysis
- **Patterns**: `references/patterns/` - Detected design patterns
- **Examples**: `references/test_examples/` - Usage examples from tests
- **Configuration**: `references/config_patterns/` - Configuration patterns
- **Documentation**: `references/documentation/` - Project documentation

---

**Generated by Skill Seeker** | Codebase Analyzer with C3.x Analysis
