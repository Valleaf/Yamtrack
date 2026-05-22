# Building New Importers for Yamtrack

This guide explains how to build new importers for Yamtrack to support importing data from external services.

## Importer Class Interface

All importers follow a consistent pattern using a class-based architecture:

```python
class YourImporter:
    """Import media from YourService."""

    def __init__(self, user, mode, **kwargs):
        """
        Initialize the importer.

        Parameters
        ----------
        user : User
            The user object performing the import
        mode : str
            Import mode - "new" to skip existing media, "overwrite" to replace existing
        **kwargs
            Service-specific credentials (username, token, api_key, etc.)
        """
        self.user = user
        self.mode = mode
        self.bulk_media = defaultdict(list)
        self.to_delete = defaultdict(lambda: defaultdict(set))
        self.existing_media = helpers.get_existing_media(user)

    def import_data(self):
        """
        Orchestrate the import process.

        Returns
        -------
        str
            Result message summarizing imported/skipped/errored items
        """
        # 1. Fetch data from external service
        # 2. Process each item
        # 3. Validate and prepare for database
        # 4. Perform bulk operations
        # 5. Return formatted result

        # Clean up items marked for deletion
        helpers.cleanup_existing_media(self.to_delete, self.user)

        # Bulk create new media
        helpers.bulk_create_media(self.bulk_media, self.user)

        # Return formatted result
        return self._format_result()

    def _format_result(self):
        """Format import result as user-facing message."""
        return f"Imported X, Skipped Y, Errors: Z"
```

## Error Handling Pattern

Use two exception types to distinguish errors:

### `MediaImportError` (User-Facing)

Raise for expected errors that should be shown to the user:
- Invalid credentials
- User/account not found
- Service down or API changes
- Rate limiting

```python
from integrations.imports.helpers import MediaImportError

if not username or not token:
    raise MediaImportError("Username and token are required")

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        raise MediaImportError("Invalid credentials")
```

### `MediaImportUnexpectedError` (Internal)

Raise for unexpected errors in processing:
- Data structure mismatches
- Database errors
- Unexpected state

```python
from integrations.imports.helpers import MediaImportUnexpectedError

try:
    episode_data = data["episodes"][0]
except (KeyError, IndexError, TypeError) as e:
    raise MediaImportUnexpectedError(f"Unexpected data structure: {e}")
```

The Celery task wrapper will:
- Display `MediaImportError` messages to the user
- Log `MediaImportUnexpectedError` with full traceback for debugging

## Media Source Mapping

Each importer must map external service media types to Yamtrack types and source identifiers:

```python
MEDIA_TYPE_MAP = {
    "movie": MediaTypes.MOVIE,
    "tv_show": MediaTypes.TV,
    "anime": MediaTypes.ANIME,
    "manga": MediaTypes.MANGA,
    "game": MediaTypes.GAME,
    "book": MediaTypes.BOOK,
}

SOURCE_MAP = {
    "movie": Sources.TMDB,
    "tv_show": Sources.TMDB,
    "anime": Sources.MAL,
    "manga": Sources.MAL,
    "game": Sources.IGDB,
    "book": Sources.OPENLIBRARY,
}
```

If external media doesn't map to a known source:
1. Try searching external provider APIs (TMDB, MAL, etc.)
2. If not found, create manual entry with service identifier: `{service}_{id}`

## Using Helper Functions

### `get_existing_media(user)`

Cache of all user's existing media to check for duplicates:

```python
existing_media = helpers.get_existing_media(user)

# Check if media exists
if media_id in existing_media[media_type][source]:
    existing = existing_media[media_type][source][media_id]
```

### `should_process_media(...)`

Determines if media should be processed based on import mode:

```python
should_process = helpers.should_process_media(
    existing_media,
    to_delete,
    media_type=MediaTypes.MOVIE.value,
    source=Sources.TMDB.value,
    media_id="238",
    mode="new",  # or "overwrite"
)

if should_process:
    # Process this media
    self.bulk_media[media_type].append(media_object)
```

### `bulk_create_media(bulk_media_list, user)`

Bulk create all media with history tracking:

```python
helpers.bulk_create_media(self.bulk_media, self.user)
```

### Encryption for Tokens

Store sensitive credentials encrypted:

```python
from integrations.imports.helpers import encrypt, decrypt

# Store encrypted token
encrypted_token = encrypt(user_token)

# Retrieve and decrypt when needed
token = decrypt(encrypted_token)
```

## Celery Task Registration

Register your importer as a Celery task:

```python
from celery import shared_task
from integrations.imports.helpers import MediaImportError, MediaImportUnexpectedError

@shared_task(name="Import from YourService")
def import_from_yourservice(user_id, username, token, mode="new"):
    """
    Celery task for importing from YourService.

    Parameters
    ----------
    user_id : int
        User ID to import for
    username : str
        Service username
    token : str
        Encrypted service token
    mode : str
        "new" or "overwrite"
    """
    user = User.objects.get(pk=user_id)

    try:
        importer = YourServiceImporter(user, mode, username=username, token=token)
        result = importer.import_data()
        return result
    except MediaImportError as e:
        return f"ERROR_TITLE: {str(e)}"
    except Exception as e:
        logger.exception("Import failed for user %s", user.username)
        return f"ERROR_TITLE: Unexpected error during import"
```

## Example: Simple CSV Importer

Here's a minimal CSV import implementation:

```python
import csv
from collections import defaultdict
from integrations.imports import helpers
from app.models import MediaTypes, Sources

class CSVImporter:
    """Import media from CSV file."""

    def __init__(self, user, mode, csv_content):
        self.user = user
        self.mode = mode
        self.csv_content = csv_content
        self.bulk_media = defaultdict(list)
        self.to_delete = defaultdict(lambda: defaultdict(set))
        self.existing_media = helpers.get_existing_media(user)
        self.imported = 0
        self.skipped = 0
        self.errors = 0

    def import_data(self):
        """Import media from CSV content."""
        reader = csv.DictReader(self.csv_content)

        for row in reader:
            try:
                self._process_row(row)
            except Exception as e:
                logger.warning("Error processing CSV row: %s", e)
                self.errors += 1

        # Bulk operations
        helpers.cleanup_existing_media(self.to_delete, self.user)
        helpers.bulk_create_media(self.bulk_media, self.user)

        return f"Imported {self.imported}, Skipped {self.skipped}, Errors {self.errors}"

    def _process_row(self, row):
        """Process single CSV row."""
        title = row.get("title")
        media_type = row.get("type", "movie")
        external_id = row.get("external_id")

        if not title or not external_id:
            self.errors += 1
            return

        # Check if should process
        if not helpers.should_process_media(
            self.existing_media,
            self.to_delete,
            media_type=media_type,
            source=Sources.MANUAL.value,
            media_id=external_id,
            mode=self.mode,
        ):
            self.skipped += 1
            return

        # Create media object (simplified)
        media_obj = {
            "title": title,
            "media_type": media_type,
            "external_id": external_id,
        }

        self.bulk_media[media_type].append(media_obj)
        self.imported += 1
```

## Testing Your Importer

Create tests that verify:

1. **Credential validation**: Test invalid credentials raise `MediaImportError`
2. **Data parsing**: Test correct parsing of external service responses
3. **Duplicate handling**: Test "new" vs "overwrite" modes
4. **Error handling**: Test both error types are raised appropriately
5. **Result formatting**: Test result message is correct

Example test structure:

```python
class CSVImporterTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="test", password="pass")

    def test_import_new_mode(self):
        """Test importing new media in new mode."""
        csv_content = [...]
        importer = CSVImporter(self.user, "new", csv_content)
        result = importer.import_data()
        self.assertIn("Imported", result)

    def test_import_invalid_csv(self):
        """Test importing invalid CSV raises error."""
        with self.assertRaises(MediaImportError):
            importer = CSVImporter(self.user, "new", "invalid content")
```

## File Structure

Place your importer in:
- File: `src/integrations/imports/{service_name}.py`
- Class: `{ServiceName}Importer`
- Celery task: `import_from_{service_name}(...)`
- Tests: `src/integrations/tests/imports/test_{service_name}.py`

Example structure:
```
src/integrations/imports/
├── trakt.py           # TraktImporter class
├── mal.py             # MALImporter class
├── helpers.py         # Shared utilities
└── ...

src/integrations/tests/imports/
├── test_trakt.py
├── test_mal.py
├── test_helpers.py
└── ...
```

## Periodic Import Scheduling

To support scheduled/periodic imports, use the `create_import_schedule` helper:

```python
from integrations.imports.helpers import create_import_schedule

# User schedules import to run every day
create_import_schedule(
    username=user.username,
    request=request,
    mode="new",
    frequency="daily",
    import_time="03:00",  # 3 AM
    source="trakt",
    token=encrypted_token,
    task_kwargs={"username": trakt_username},
)
```

This creates a Celery Beat task that runs on the specified schedule.

## See Also

- `src/integrations/imports/helpers.py` - Shared helper functions
- `src/integrations/imports/trakt.py` - Full-featured importer example
- `src/app/models.py` - Media model definitions
- `src/integrations/tests/imports/` - Existing importer tests
