# How To: Get Item Filter With Empty Dict

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the get_item filter with an empty dictionary.

## Prerequisites

**Required Modules:**
- `django.template`
- `django.test`


## Step-by-Step Guide

### Step 1: 'Test the get_item filter with an empty dictionary.'

```python
'Test the get_item filter with an empty dictionary.'
```

### Step 2: Assign template_str = '\n            {% load events_tags %}\n            {{ empty_dict|get_item:"any_key" }}\n        '

```python
template_str = '\n            {% load events_tags %}\n            {{ empty_dict|get_item:"any_key" }}\n        '
```

### Step 3: Assign template = Template(...)

```python
template = Template(template_str)
```

### Step 4: Assign context = Context(...)

```python
context = Context({'empty_dict': {}})
```

### Step 5: Assign rendered = template.render(...)

```python
rendered = template.render(context)
```

### Step 6: Call self.assertIn()

```python
self.assertIn('[]', rendered)
```


## Complete Example

```python
# Workflow
'Test the get_item filter with an empty dictionary.'
template_str = '\n            {% load events_tags %}\n            {{ empty_dict|get_item:"any_key" }}\n        '
template = Template(template_str)
context = Context({'empty_dict': {}})
rendered = template.render(context)
self.assertIn('[]', rendered)
```

## Next Steps


---

*Source: test_templatetags.py:38 | Complexity: Intermediate | Last updated: 2026-05-22*