# How To: Anilist Date Parser

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test anilist_date_parser function.

## Prerequisites

**Required Modules:**
- `datetime`
- `unittest.mock`
- `zoneinfo`
- `django.test`
- `events.calendar.anime`
- `events.tests.calendar.utils`


## Step-by-Step Guide

### Step 1: 'Test anilist_date_parser function.'

```python
'Test anilist_date_parser function.'
```

### Step 2: Assign complete_date = value

```python
complete_date = {'year': 2024, 'month': 3, 'day': 28}
```

### Step 3: Assign result = anilist_date_parser(...)

```python
result = anilist_date_parser(complete_date)
```

### Step 4: Assign dt = datetime.datetime.fromtimestamp(...)

```python
dt = datetime.datetime.fromtimestamp(result, tz=ZoneInfo('UTC'))
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(dt.year, 2024)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(dt.month, 3)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(dt.day, 28)
```

### Step 8: Assign partial_date = value

```python
partial_date = {'year': 2024, 'month': 3, 'day': None}
```

### Step 9: Assign result = anilist_date_parser(...)

```python
result = anilist_date_parser(partial_date)
```

### Step 10: Assign dt = datetime.datetime.fromtimestamp(...)

```python
dt = datetime.datetime.fromtimestamp(result, tz=ZoneInfo('UTC'))
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(dt.year, 2024)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(dt.month, 3)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(dt.day, 1)
```

### Step 14: Assign year_only_date = value

```python
year_only_date = {'year': 2024, 'month': None, 'day': None}
```

### Step 15: Assign result = anilist_date_parser(...)

```python
result = anilist_date_parser(year_only_date)
```

### Step 16: Assign dt = datetime.datetime.fromtimestamp(...)

```python
dt = datetime.datetime.fromtimestamp(result, tz=ZoneInfo('UTC'))
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(dt.year, 2024)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(dt.month, 1)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(dt.day, 1)
```

### Step 20: Assign missing_year = value

```python
missing_year = {'year': None, 'month': 3, 'day': 28}
```

### Step 21: Assign result = anilist_date_parser(...)

```python
result = anilist_date_parser(missing_year)
```

### Step 22: Call self.assertIsNone()

```python
self.assertIsNone(result)
```


## Complete Example

```python
# Workflow
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

## Next Steps


---

*Source: test_anime.py:122 | Complexity: Advanced | Last updated: 2026-05-22*