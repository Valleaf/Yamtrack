# Yamtrack Import Pipeline Architecture

This document explains how the data import system works in Yamtrack, from user initiation through database storage.

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Yamtrack Import Pipeline                 │
└─────────────────────────────────────────────────────────────────┘

User Action                                                          
   │                                                                 
   ├─→ [Import View]                                                
   │       │                                                         
   │       └─→ [Celery Task]                                        
   │             │                                                   
   │             └─→ [Importer Class]                               
   │                   │                                             
   │                   ├─→ [Fetch External Data]                    
   │                   │                                             
   │                   ├─→ [Helpers: get_existing_media()]         
   │                   │                                             
   │                   ├─→ [Process & Validate]                     
   │                   │                                             
   │                   ├─→ [Helpers: bulk_create/update]           
   │                   │                                             
   │                   └─→ [Result Message]                         
   │                                                                 
   └─→ [Database] + [History Tracking]                             
```

## Detailed Flow

### 1. User Initiates Import

User navigates to import page and provides credentials (e.g., Trakt username/token):

```
GET /import/trakt
POST /import/trakt/oauth  ─→ returns OAuth code
POST /import/trakt        ─→ (username, token, mode="new|overwrite", frequency="once|daily|weekly")
```

### 2. View Validates & Launches Celery Task

The import view (in `src/integrations/views.py`):
1. Validates user input and credentials
2. Encrypts sensitive data (tokens, API keys)
3. Launches Celery task asynchronously
4. Returns to user with "Import queued" message

```python
@login_required
def import_trakt(request):
    username = request.POST.get('username')
    token = decrypt(request.POST.get('token'))  # Decrypt token
    
    # Encrypt before passing to task
    encrypted_token = encrypt(token)
    
    # Launch async task
    import_from_trakt.delay(
        user_id=request.user.id,
        username=username,
        token=encrypted_token,
        mode=request.POST.get('mode', 'new')
    )
    
    return redirect('profile')
```

### 3. Celery Task Execution

Celery worker picks up the task:

```python
@shared_task(name="Import from Trakt")
def import_from_trakt(user_id, username, token, mode="new"):
    user = User.objects.get(pk=user_id)
    
    try:
        importer = TraktImporter(user, mode, username=username, token=decrypt(token))
        result = importer.import_data()
        return result  # "Imported 15, Skipped 3, Errors: 0"
    
    except MediaImportError as e:
        return f"ERROR_TITLE: {str(e)}"  # User-facing error
    
    except Exception as e:
        logger.exception("Import failed")
        return f"ERROR_TITLE: Unexpected error"  # Generic fallback
```

Task status is tracked in Django database for UI display.

### 4. Importer Class Orchestration

The Importer class (e.g., `TraktImporter`) manages the import workflow:

```python
class TraktImporter:
    def __init__(self, user, mode, username, token):
        self.user = user
        self.mode = mode
        self.bulk_media = defaultdict(list)           # Media to create
        self.to_delete = defaultdict(lambda: defaultdict(set))  # Media to delete (overwrite mode)
        self.existing_media = helpers.get_existing_media(user)   # Cache of user's media
        self.imported = 0
        self.skipped = 0
        self.errors = []
    
    def import_data(self):
        """Main orchestration method."""
        # Step 1: Fetch and parse external data
        data = self._fetch_from_trakt()
        
        # Step 2: Process each item
        for item in data:
            self._process_item(item)
        
        # Step 3: Bulk database operations
        helpers.cleanup_existing_media(self.to_delete, self.user)
        helpers.bulk_create_media(self.bulk_media, self.user)
        
        # Step 4: Return formatted result
        return self._format_result()
```

### 5. Helper Functions: Data Management

#### `get_existing_media(user)`

**Purpose**: Cache all user's existing media for fast duplicate detection

**Return**: Nested dict structure
```python
{
    'movie': {
        'tmdb': {'238': <Movie object>, '550': <Movie object>},
        'manual': {'custom_1': <Movie object>}
    },
    'tv': {
        'tmdb': {'1399': <TV object>}
    }
}
```

**Performance**: Single database query with `select_related('item')`

```python
def process_item(self, item):
    media_type = item['type']  # 'movie', 'tv', etc.
    source = 'tmdb'
    media_id = item['id']
    
    if media_id in self.existing_media[media_type][source]:
        # Media already tracked by this user
        if self.mode == 'new':
            self.skipped += 1
            return
```

#### `should_process_media(...)`

**Purpose**: Determine if media should be processed based on mode

**Logic**:
- **"new" mode**: Process only if media doesn't exist for user → `skip_duplicates=True`
- **"overwrite" mode**: Process and mark existing for deletion → `skip_duplicates=False, mark_for_delete=True`

```python
should_process = helpers.should_process_media(
    self.existing_media,
    self.to_delete,
    media_type=MediaTypes.MOVIE.value,
    source=Sources.TMDB.value,
    media_id='238',
    mode='new'
)

if should_process:
    self.bulk_media[media_type].append(movie_obj)
else:
    self.skipped += 1
```

#### `bulk_create_media(bulk_media_list, user)`

**Purpose**: Bulk create all media with history tracking

**Process**:
1. Group media by type (movies, TV, etc.)
2. Bulk insert using Django ORM batch operations
3. Track import history for each media item
4. Handle relationship updates (seasons → episodes)

```python
# Bulk create automatically:
# - Creates Item objects if needed
# - Creates media objects (Movie, TV, etc.)
# - Records creation in simple_history audit trail
# - Handles duplicates gracefully (skip duplicates, update references)
helpers.bulk_create_media(self.bulk_media, self.user)
```

**History Tracking**: Each imported media gets an audit entry with:
- Who: User performing import
- What: Media created via import
- When: Import timestamp
- Source: Import type (Trakt, MAL, etc.)

### 6. Error Handling Strategy

#### User-Facing Errors

Raise `MediaImportError` for expected failures:

```python
from integrations.imports.helpers import MediaImportError

def _authenticate(self):
    if not self.username or not self.token:
        raise MediaImportError("Username and token required")
    
    response = requests.post(f"{API_URL}/auth", data={...})
    if response.status_code == 401:
        raise MediaImportError("Invalid credentials")
```

**Task handling**:
```python
except MediaImportError as e:
    return f"ERROR_TITLE: {str(e)}"  # User sees this message
```

#### Internal Errors

Raise `MediaImportUnexpectedError` for processing failures:

```python
from integrations.imports.helpers import MediaImportUnexpectedError

def _parse_item(self, raw_item):
    try:
        episode_count = raw_item['metadata']['episode_count']
    except (KeyError, TypeError):
        raise MediaImportUnexpectedError(f"Unexpected data format for item {raw_item}")
```

**Task handling**:
```python
except Exception as e:
    logger.exception("Import failed for user %s", user.username)
    return f"ERROR_TITLE: Unexpected error (check logs)"  # Generic message
```

#### Result Message Format

Standard format for result messages:

```
"Imported 42, Skipped 5, Errors: 2"
```

If errors, append details:
```
"Imported 40, Skipped 5, Errors: 2 (invalid_format: 1, api_error: 1)"
```

### 7. Periodic Imports

For scheduled recurring imports:

```python
from integrations.imports.helpers import create_import_schedule

# User enables daily auto-import
create_import_schedule(
    username=user.username,
    request=request,
    mode='new',
    frequency='daily',
    import_time='03:00',
    source='trakt',
    token=encrypted_token,
    task_kwargs={'username': trakt_username}
)
```

This creates a `PeriodicTask` (Celery Beat) that:
- Runs at specified time (3:00 AM daily)
- Automatically executes the import task
- Logs results for display in user's import history

**Crontab mapping**:
- `daily` → every day at specified time
- `every_2_days` → every other day
- `weekly` → once per week on specified day
- Custom cron expression supported

### 8. Data Consistency & Atomicity

**Bulk operations ensure atomicity**:
1. All media created in single transaction
2. History tracking happens automatically
3. If any media fails to create, entire batch is rolled back
4. No partial imports leave dangling references

**Relationship integrity**:
- TV shows reference seasons
- Seasons reference episodes
- Bulk create respects these relationships
- Updates relationship references after creation

```python
# Bulk operations handle this automatically:
# 1. Create all TV objects
# 2. Create all season objects with FK to TV
# 3. Create all episode objects with FK to season
# 4. Everything in single transaction
helpers.bulk_create_media(self.bulk_media, self.user)
```

### 9. Database State After Import

**Media Types Created**:
- Primary: Movie, TV, Anime, Manga, Game, Book, Comic
- Automatically linked seasons/episodes for TV

**Data Stored**:
- Media item (title, poster, external IDs)
- User's tracking status (watch list, completed, rating, etc.)
- Import metadata (import date, source, action)
- Simple history audit trail

**Query Performance**:
- User-specific media retrieved with `select_related('item')`
- Indexed on (user, media_type, source, media_id)
- Prefetch related data for relationships

## Integration Points

### OAuth Flows

Some importers (Trakt, SIMKL) use OAuth 2.0:

```
1. User clicks "Connect Trakt"
2. Redirect to: https://trakt.tv/oauth/authorize?client_id=...
3. User authorizes Yamtrack app
4. Redirect back to: /import/trakt/oauth?code=...&state=...
5. Exchange code for access token
6. Store encrypted token
7. Launch import with token
```

### Webhook Integrations

Some sources (Jellyfin, Plex) push updates via webhooks:

```
Jellyfin → (webhook) → /webhooks/jellyfin
    ↓
Process play event
    ↓
Create/update media entry
    ↓
Update user tracking
```

### Scheduled Tasks

Celery Beat handles periodic imports:

```
Beat Scheduler (background)
    ├─ Every day at 3 AM
    └─→ Execute import_from_trakt task
```

## Monitoring & Debugging

**Task Status**: View in admin or dedicated task status API

```python
from celery.result import AsyncResult

result = AsyncResult(task_id)
print(result.status)    # "PENDING", "STARTED", "SUCCESS", "FAILURE"
print(result.result)    # "Imported 42, Skipped 5, ..."
```

**Logs**: Check application logs for details

```
logger.info("Fetching Trakt data for user %s", username)
logger.warning("Skipping duplicate media: %s", media_id)
logger.exception("Import failed")
```

**History**: View in Django admin or via API

```python
from simple_history.models import HistoricalMovie
historical_records = HistoricalMovie.objects.filter(user=user)
```

## Security Considerations

1. **Token Encryption**: All external tokens encrypted at rest using Fernet
2. **User Isolation**: Each user can only import to their own account
3. **Rate Limiting**: API calls throttled to avoid service violations
4. **Input Validation**: All external data validated before database insert
5. **Error Messages**: Avoid exposing internal system details in error messages

## Performance Optimization

1. **Bulk Operations**: 1000s of items imported in single transaction
2. **Caching**: Existing media cached in memory during import
3. **Batch Indexing**: Indexes on user + source + media_id for fast lookups
4. **Prefetch Related**: Reduce N+1 queries during enrichment

Typical import times:
- 50 items: < 2 seconds
- 500 items: < 10 seconds
- 5000 items: < 1 minute

## See Also

- `.github/IMPORTER_DEVELOPMENT.md` - How to build new importers
- `src/integrations/imports/helpers.py` - Helper function documentation
- `src/integrations/imports/trakt.py` - Reference implementation
- `src/integrations/tasks.py` - Celery task definitions
