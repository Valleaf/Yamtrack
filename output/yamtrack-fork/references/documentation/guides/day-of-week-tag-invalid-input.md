# How To: Day Of Week Tag Invalid Input

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the day_of_week tag with invalid input.

## Prerequisites

**Required Modules:**
- `django.template`
- `django.test`


## Step-by-Step Guide

### Step 1: 'Test the day_of_week tag with invalid input.'

```python
'Test the day_of_week tag with invalid input.'
```

### Step 2: Assign template_str = '\n            {% load events_tags %}\n            {% day_of_week 30 2 2023 %}\n        '

```python
template_str = '\n            {% load events_tags %}\n            {% day_of_week 30 2 2023 %}\n        '
```

### Step 3: Assign template = Template(...)

```python
template = Template(template_str)
```

### Step 4: Assign template_str = '\n            {% load events_tags %}\n            {% day_of_week "day" "month" "year" %}\n        '

```python
template_str = '\n            {% load events_tags %}\n            {% day_of_week "day" "month" "year" %}\n        '
```

### Step 5: Assign template = Template(...)

```python
template = Template(template_str)
```

### Step 6: Call template.render()

```python
template.render(Context({}))
```

### Step 7: Call template.render()

```python
template.render(Context({'day': 'day', 'month': 'month', 'year': 'year'}))
```


## Complete Example

```python
# Workflow
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

## Next Steps


---

*Source: test_templatetags.py:122 | Complexity: Intermediate | Last updated: 2026-05-22*