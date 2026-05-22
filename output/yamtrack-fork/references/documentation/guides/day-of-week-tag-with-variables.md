# How To: Day Of Week Tag With Variables

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the day_of_week tag with variables.

## Prerequisites

**Required Modules:**
- `django.template`
- `django.test`


## Step-by-Step Guide

### Step 1: 'Test the day_of_week tag with variables.'

```python
'Test the day_of_week tag with variables.'
```

### Step 2: Assign template_str = '\n            {% load events_tags %}\n            {% day_of_week day month year %}\n        '

```python
template_str = '\n            {% load events_tags %}\n            {% day_of_week day month year %}\n        '
```

### Step 3: Assign template = Template(...)

```python
template = Template(template_str)
```

### Step 4: Assign test_dates = value

```python
test_dates = [{'day': 1, 'month': 1, 'year': 2023, 'expected': 'Sunday'}, {'day': 4, 'month': 7, 'year': 2023, 'expected': 'Tuesday'}, {'day': 25, 'month': 12, 'year': 2023, 'expected': 'Monday'}, {'day': '31', 'month': '10', 'year': '2023', 'expected': 'Tuesday'}]
```

### Step 5: Assign context = Context(...)

```python
context = Context({'day': date_data['day'], 'month': date_data['month'], 'year': date_data['year']})
```

### Step 6: Assign rendered = template.render(...)

```python
rendered = template.render(context)
```

### Step 7: Call self.assertIn()

```python
self.assertIn(date_data['expected'], rendered)
```


## Complete Example

```python
# Workflow
'Test the day_of_week tag with variables.'
template_str = '\n            {% load events_tags %}\n            {% day_of_week day month year %}\n        '
template = Template(template_str)
test_dates = [{'day': 1, 'month': 1, 'year': 2023, 'expected': 'Sunday'}, {'day': 4, 'month': 7, 'year': 2023, 'expected': 'Tuesday'}, {'day': 25, 'month': 12, 'year': 2023, 'expected': 'Monday'}, {'day': '31', 'month': '10', 'year': '2023', 'expected': 'Tuesday'}]
for date_data in test_dates:
    context = Context({'day': date_data['day'], 'month': date_data['month'], 'year': date_data['year']})
    rendered = template.render(context)
    self.assertIn(date_data['expected'], rendered)
```

## Next Steps


---

*Source: test_templatetags.py:74 | Complexity: Intermediate | Last updated: 2026-05-22*