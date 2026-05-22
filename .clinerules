---
name: djangoproject
description: Use when working with djangoproject
---

# Djangoproject Skill

Use when working with djangoproject

## When to Use This Skill

Use this skill when you need to:
- understand djangoproject features, APIs, and workflows
- find concrete code examples before implementing or debugging
- navigate the official documentation quickly through categorized references

## Quick Reference

### Key Usage Notes

**Pattern 1:** Some actions are best if they’re made available to any object in the admin site – the export action defined above would be a good candidate.

```
from django.contrib import admin

admin.site.add_action(export_selected_objects)
```

**Pattern 2:** For example, if we reverse the order of the values() and annotate() clause from our previous example

```
>>> Author.objects.annotate(average_rating=Avg("book__rating")).values(
...     "name", "average_rating"
... )
```

**Pattern 3:** Take the following example

```
>>> from django.db.models import F, Count, Greatest
>>> Book.objects.values(greatest_pages=Greatest("pages", 600)).annotate(
...     num_authors=Count("authors"),
...     pages_per_author=F("greatest_pages") / F("num_authors"),
... ).aggregate(Avg("pages_per_author"))
```

**Pattern 4:** If you want to call a part of Django that is still synchronous, you will need to wrap it in a sync_to_async() call.

```
from asgiref.sync import sync_to_async

results = await sync_to_async(sync_function, thread_sensitive=True)(pk=123)
```

**Pattern 5:** For example

```
from django.views.decorators.cache import never_cache


@never_cache
def my_sync_view(request): ...


@never_cache
async def my_async_view(request): ...
```

**Pattern 6:** Sample usage

```
{% autoescape on %}
    {{ body }}
{% endautoescape %}
```

**Pattern 7:** Sample usage

```
<p>Rendered text with {{ pub_date|date:"c" }}</p>
{% comment "Optional note" %}
    <p>Commented out text with {{ create_date|date:"c" }}</p>
{% endcomment %}
```

**Pattern 8:** By default, when you use the as keyword with the cycle tag, the usage of {% cycle %} that initiates the cycle will itself produce the first value i...

```
{% for obj in some_list %}
    {% cycle 'row1' 'row2' as rowcolors silent %}
    <tr class="{{ rowcolors }}">{% include "subtemplate.html" %}</tr>
{% endfor %}
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Api documentation
- **contrib.md** - Contrib documentation
- **howto.md** - Howto documentation
- **internals.md** - Internals documentation
- **models.md** - Models documentation
- **other.md** - Other documentation
- **ref.md** - Ref documentation
- **releases.md** - Releases documentation
- **topics.md** - Topics documentation
- **tutorials.md** - Tutorials documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### Start Here
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
Use the high-signal examples above first, then open the matching reference file for full context.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference entries are filtered to avoid low-signal placeholders and inline tokens

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
