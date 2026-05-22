#!/usr/bin/env python3
"""Rename the 'collections' Django app to 'media_collections' to avoid
shadowing Python's built-in collections module."""
from pathlib import Path
import shutil

ROOT = Path(r"C:\yamtrack-fork")
SRC = ROOT / "src"

OLD_APP = SRC / "collections"
NEW_APP = SRC / "media_collections"
TMPL_OLD = SRC / "templates" / "collections"
TMPL_NEW = SRC / "templates" / "media_collections"


def rwrite(path, old, new, label=""):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        print(f"  SKIP {label or path.name}")
        return
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"  OK   {label or path.name}")


# 1. Rename the app directory
if OLD_APP.exists() and not NEW_APP.exists():
    shutil.copytree(OLD_APP, NEW_APP)
    shutil.rmtree(OLD_APP)
    print("  OK   src/collections/ → src/media_collections/")
elif NEW_APP.exists():
    print("  SKIP src/media_collections/ already exists")

# 2. Rename templates directory
if TMPL_OLD.exists() and not TMPL_NEW.exists():
    shutil.copytree(TMPL_OLD, TMPL_NEW)
    shutil.rmtree(TMPL_OLD)
    print("  OK   templates/collections/ → templates/media_collections/")
elif TMPL_NEW.exists():
    print("  SKIP templates/media_collections/ already exists")

# 3. Fix every file in the new app directory
replacements = [
    ("from collections.", "from media_collections."),
    ("from collections import", "from media_collections import"),
    ('"collections"', '"media_collections"'),
    ("'collections'", "'media_collections'"),
    ("name = \"collections\"", "name = \"media_collections\""),
    ("app_label = \"collections\"", "app_label = \"media_collections\""),
    ('("collections",', '("media_collections",'),
    ('("collections")', '("media_collections")'),
    ('collections.collection', 'media_collections.collection'),
    ('collections.collectionitem', 'media_collections.collectionitem'),
    ('"collections/components/', '"media_collections/components/'),
    ("'collections/components/", "'media_collections/components/"),
    ('"collections/collections.html"', '"media_collections/collections.html"'),
    ('"collections/collection_detail.html"', '"media_collections/collection_detail.html"'),
    ("import collections\n", "import media_collections\n"),
]

for py_file in list(NEW_APP.rglob("*.py")) + list(TMPL_NEW.rglob("*.html")):
    text = py_file.read_text(encoding="utf-8")
    changed = False
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
            changed = True
    if changed:
        py_file.write_text(text, encoding="utf-8")
        print(f"  OK   {py_file.relative_to(ROOT)}")

# 4. Fix config/settings.py
settings = SRC / "config" / "settings.py"
rwrite(settings, '"collections"', '"media_collections"', "settings.py")

# 5. Fix config/urls.py
urls = SRC / "config" / "urls.py"
rwrite(urls, 'include("collections.urls")', 'include("media_collections.urls")', "config/urls.py")

# 6. Fix base.html (url tags and any references)
base = SRC / "templates" / "base.html"
text = base.read_text(encoding="utf-8")
for old, new in [
    ("{% url 'collections' %}", "{% url 'media_collections' %}"),
    ("{% url 'collection_", "{% url 'collection_"),  # these don't change
]:
    text = text.replace(old, new)
base.write_text(text, encoding="utf-8")
print("  OK   base.html")

# 7. Fix all template files that reference old URL names or paths
for tmpl in TMPL_NEW.rglob("*.html"):
    text = tmpl.read_text(encoding="utf-8")
    changed = False
    # URL name for the list view
    if "{% url 'collections' %}" in text:
        text = text.replace("{% url 'collections' %}", "{% url 'media_collections' %}")
        changed = True
    # template paths in include tags
    for old, new in [
        ('"collections/components/', '"media_collections/components/'),
        ("'collections/components/", "'media_collections/components/"),
    ]:
        if old in text:
            text = text.replace(old, new)
            changed = True
    if changed:
        tmpl.write_text(text, encoding="utf-8")
        print(f"  OK   {tmpl.relative_to(ROOT)}")

# 8. Fix views.py URL name for the collections list
views_py = NEW_APP / "views.py"
rwrite(views_py, 'return redirect("collections")', 'return redirect("media_collections")', "views.py — redirect name")

# 9. Fix urls.py — the list view URL name
urls_py = NEW_APP / "urls.py"
rwrite(urls_py,
    'path("collections", views.collections, name="collections")',
    'path("collections", views.collections, name="media_collections")',
    "media_collections/urls.py — list view name")

print()
print("Done. Commit and rebuild:")
print("  git add src/ templates/")
print("  git commit -m 'fix: rename collections app to media_collections'")
print("  docker compose down; docker compose up -d --build")
