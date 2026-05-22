# How To: Hardcover Get Edition Details

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the get_edition_details function from Hardcover provider.

## Prerequisites

**Required Modules:**
- `json`
- `datetime`
- `pathlib`
- `unittest.mock`
- `requests`
- `django.conf`
- `django.test`
- `app.models`
- `app.providers`


## Step-by-Step Guide

### Step 1: 'Test the get_edition_details function from Hardcover provider.'

```python
'Test the get_edition_details function from Hardcover provider.'
```

### Step 2: Assign edition_data = value

```python
edition_data = {'edition_format': 'Paperback', 'isbn_13': '9781234567890', 'isbn_10': '1234567890', 'publisher': {'name': 'Test Publisher'}}
```

### Step 3: Assign result = hardcover.get_edition_details(...)

```python
result = hardcover.get_edition_details(edition_data)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(result['format'], 'Paperback')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(result['publisher'], 'Test Publisher')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(result['isbn'], ['1234567890', '9781234567890'])
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(hardcover.get_edition_details(None), {})
```

### Step 8: Assign no_publisher = value

```python
no_publisher = {'edition_format': 'Paperback', 'isbn_13': '9781234567890'}
```

### Step 9: Assign result = hardcover.get_edition_details(...)

```python
result = hardcover.get_edition_details(no_publisher)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(result['publisher'], None)
```


## Complete Example

```python
# Workflow
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

## Next Steps


---

*Source: test_metadata.py:649 | Complexity: Advanced | Last updated: 2026-05-22*