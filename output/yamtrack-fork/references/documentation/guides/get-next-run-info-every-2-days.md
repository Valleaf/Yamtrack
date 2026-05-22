# How To: Get Next Run Info Every 2 Days

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Test getting next run info for every 2 days task.

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `zoneinfo`
- `datetime`
- `unittest.mock`
- `django.test`
- `django_celery_beat.models`
- `users`

**Setup Required:**
```python
# Fixtures: mock_now
```

## Step-by-Step Guide

### Step 1: 'Test getting next run info for every 2 days task.'

```python
'Test getting next run info for every 2 days task.'
```

### Step 2: Assign current_time = datetime(...)

```python
current_time = datetime(2025, 2, 6, 12, 0, tzinfo=zoneinfo.ZoneInfo('UTC'))
```

### Step 3: Assign mock_now.return_value = current_time

```python
mock_now.return_value = current_time
```

### Step 4: Assign crontab = CrontabSchedule.objects.create(...)

```python
crontab = CrontabSchedule.objects.create(minute='0', hour='14', day_of_week='*/2', day_of_month='*', month_of_year='*', timezone='UTC')
```

### Step 5: Assign periodic_task = PeriodicTask.objects.create(...)

```python
periodic_task = PeriodicTask.objects.create(name='Every 2 Days Import', task='import_task', crontab=crontab)
```

### Step 6: Assign next_run_info = helpers.get_next_run_info(...)

```python
next_run_info = helpers.get_next_run_info(periodic_task)
```

### Step 7: Assign expected_next_run = datetime(...)

```python
expected_next_run = datetime(2025, 2, 6, 14, 0, tzinfo=zoneinfo.ZoneInfo('UTC'))
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(next_run_info['next_run'], expected_next_run)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(next_run_info['frequency'], 'Every 2 days')
```


## Complete Example

```python
# Setup
# Fixtures: mock_now

# Workflow
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

## Next Steps


---

*Source: test_helpers.py:133 | Complexity: Advanced | Last updated: 2026-05-22*