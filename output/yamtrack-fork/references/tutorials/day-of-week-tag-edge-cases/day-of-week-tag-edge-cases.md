# How To: Day Of Week Tag Edge Cases

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the day_of_week tag with edge cases.

## Prerequisites

**Required Modules:**
- `django.template`
- `django.test`


## Step-by-Step Guide

### Step 1: 'Test the day_of_week tag with edge cases.'

```python
'Test the day_of_week tag with edge cases.'
```

### Step 2: Assign template_str = '\n            {% load events_tags %}\n            {% day_of_week 29 2 2020 %}\n        '

```python
template_str = '\n            {% load events_tags %}\n            {% day_of_week 29 2 2020 %}\n        '
```

### Step 3: Assign template = Template(...)

```python
template = Template(template_str)
```

### Step 4: Assign rendered = template.render(...)

```python
rendered = template.render(Context({}))
```

### Step 5: Call self.assertIn()

```python
self.assertIn('Saturday', rendered)
```

### Step 6: Assign template_str = '\n            {% load events_tags %}\n            {% day_of_week 1 1 2030 %}\n        '

```python
template_str = '\n            {% load events_tags %}\n            {% day_of_week 1 1 2030 %}\n        '
```

### Step 7: Assign template = Template(...)

```python
template = Template(template_str)
```

### Step 8: Assign rendered = template.render(...)

```python
rendered = template.render(Context({}))
```

### Step 9: Call self.assertIn()

```python
self.assertIn('Tuesday', rendered)
```


## Complete Example

```python
# Workflow
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

## Next Steps


---

*Source: test_templatetags.py:101 | Complexity: Advanced | Last updated: 2026-05-22*