# How To: Get Item Filter

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test the get_item filter.

## Prerequisites

**Required Modules:**
- `django.template`
- `django.test`


## Step-by-Step Guide

### Step 1: 'Test the get_item filter.'

```python
'Test the get_item filter.'
```

### Step 2: Assign template_str = '\n            {% load events_tags %}\n            {{ my_dict|get_item:"key1" }}\n            {{ my_dict|get_item:"key2" }}\n            {{ my_dict|get_item:"nonexistent_key" }}\n        '

```python
template_str = '\n            {% load events_tags %}\n            {{ my_dict|get_item:"key1" }}\n            {{ my_dict|get_item:"key2" }}\n            {{ my_dict|get_item:"nonexistent_key" }}\n        '
```

### Step 3: Assign template = Template(...)

```python
template = Template(template_str)
```

### Step 4: Assign context = Context(...)

```python
context = Context({'my_dict': {'key1': 'value1', 'key2': ['item1', 'item2']}})
```

### Step 5: Assign rendered = template.render(...)

```python
rendered = template.render(context)
```

### Step 6: Call self.assertIn()

```python
self.assertIn('value1', rendered)
```

### Step 7: Call self.assertIn()

```python
self.assertIn('item1', rendered)
```

### Step 8: Call self.assertIn()

```python
self.assertIn('item2', rendered)
```

### Step 9: Call self.assertIn()

```python
self.assertIn('[]', rendered)
```


## Complete Example

```python
# Workflow
'Test the get_item filter.'
template_str = '\n            {% load events_tags %}\n            {{ my_dict|get_item:"key1" }}\n            {{ my_dict|get_item:"key2" }}\n            {{ my_dict|get_item:"nonexistent_key" }}\n        '
template = Template(template_str)
context = Context({'my_dict': {'key1': 'value1', 'key2': ['item1', 'item2']}})
rendered = template.render(context)
self.assertIn('value1', rendered)
self.assertIn('item1', rendered)
self.assertIn('item2', rendered)
self.assertIn('[]', rendered)
```

## Next Steps


---

*Source: test_templatetags.py:8 | Complexity: Advanced | Last updated: 2026-05-22*