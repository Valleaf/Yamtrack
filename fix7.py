from pathlib import Path

views = Path(r"C:\yamtrack-fork\src\app\views.py")
text = views.read_text(encoding="utf-8")

fixes = [
    (
        '                "country": metadata.get("country") or "",\n            },\n        )\n        model = apps.get_model(app_label="app", model_name=media_type)\n        instance = model(item=item, user=request.user, country=metadata.get("country") or "")',
        '            },\n        )\n        model = apps.get_model(app_label="app", model_name=media_type)\n        instance = model(item=item, user=request.user, country=metadata.get("country") or "")',
        "media_save get_or_create — remove country from Item defaults",
    ),
    (
        '                "country": season_metadata.get("country") or "",\n            },\n        )\n        related_season = Season.objects.create(',
        '            },\n        )\n        related_season = Season.objects.create(',
        "episode_save get_or_create — remove country from Item defaults",
    ),
    (
        '                "country": metadata.get("country") or "",\n            },\n        )\n        title = metadata["title"]',
        '            },\n        )\n        title = metadata["title"]',
        "sync_metadata update_or_create — remove country from Item defaults",
    ),
]

for old, new, label in fixes:
    if old in text:
        text = text.replace(old, new, 1)
        print(f"  OK   {label}")
    else:
        print(f"  SKIP {label}")

views.write_text(text, encoding="utf-8")
print()
print("Done. Commit and rebuild:")
print("  git add src/app/views.py")
print("  git commit -m 'fix: remove country from Item get_or_create (not an Item field)'")
print("  docker compose down; docker compose up -d --build")
