# How To: Get Import Tasks Schedules

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test get_import_tasks returns correct scheduled tasks.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `datetime`
- `unittest.mock`
- `django.contrib.auth`
- `django.test`
- `django.utils`
- `django_celery_beat.models`
- `django_celery_results.models`
- `users.models`

**Setup Required:**
```python
# Fixtures: mock_get_next_run_info
```

## Step-by-Step Guide

### Step 1: 'Test get_import_tasks returns correct scheduled tasks.'

```python
'Test get_import_tasks returns correct scheduled tasks.'
```

### Step 2: Assign mock_get_next_run_info.return_value = value

```python
mock_get_next_run_info.return_value = {'next_run': timezone.now() + timedelta(days=1), 'frequency': 'Daily at midnight', 'mode': 'overwrite'}
```

### Step 3: Assign periodic_task1 = PeriodicTask.objects.create(...)

```python
periodic_task1 = PeriodicTask.objects.create(name='Import from Trakt for testuser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
```

### Step 4: Assign periodic_task2 = PeriodicTask.objects.create(...)

```python
periodic_task2 = PeriodicTask.objects.create(name='Import from AniList for testuser at weekly', task='Import from AniList', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
```

### Step 5: Call PeriodicTask.objects.create()

```python
PeriodicTask.objects.create(name='Import from SIMKL for testuser at daily', task='Import from SIMKL', kwargs=f'{{"user_id": {self.user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=False)
```

### Step 6: Call PeriodicTask.objects.create()

```python
PeriodicTask.objects.create(name='Import from Trakt for otheruser at daily', task='Import from Trakt', kwargs=f'{{"user_id": {self.other_user.id}, "username": "testuser"}}', crontab=self.crontab, enabled=True)
```

### Step 7: Assign import_tasks = self.user.get_import_tasks(...)

```python
import_tasks = self.user.get_import_tasks()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(import_tasks['schedules']), 2)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(import_tasks['schedules'][0]['task'], periodic_task1)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(import_tasks['schedules'][0]['source'], 'trakt')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(import_tasks['schedules'][0]['username'], 'testuser')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(import_tasks['schedules'][0]['schedule'], 'Daily at midnight')
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(import_tasks['schedules'][1]['task'], periodic_task2)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(import_tasks['schedules'][1]['source'], 'anilist')
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(import_tasks['schedules'][1]['username'], 'testuser')
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_next_run_info

# Workflow
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

## Next Steps


---

*Source: test_models.py:269 | Complexity: Advanced | Last updated: 2026-05-22*