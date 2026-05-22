from pathlib import Path

views = Path(r"C:\yamtrack-fork\src\app\views.py")
text = views.read_text(encoding="utf-8")

# Fix 1: media_save — Item.objects.get_or_create defaults missing country
OLD1 = '''            defaults={
                "title": metadata["title"],
                "image": metadata["image"],
            },
        )
        model = apps.get_model(app_label="app", model_name=media_type)
        instance = model(item=item, user=request.user, country=metadata.get("country") or "")'''

NEW1 = '''            defaults={
                "title": metadata["title"],
                "image": metadata["image"],
                "country": metadata.get("country") or "",
            },
        )
        model = apps.get_model(app_label="app", model_name=media_type)
        instance = model(item=item, user=request.user, country=metadata.get("country") or "")'''

# Fix 2: episode_save — Item.objects.get_or_create for season also missing country
OLD2 = '''        item, _ = Item.objects.get_or_create(
            media_id=media_id,
            source=Sources.TMDB.value,
            media_type=MediaTypes.SEASON.value,
            season_number=season_number,
            defaults={
                "title": tv_with_seasons_metadata["title"],
                "image": season_metadata["image"],
            },
        )'''

NEW2 = '''        item, _ = Item.objects.get_or_create(
            media_id=media_id,
            source=Sources.TMDB.value,
            media_type=MediaTypes.SEASON.value,
            season_number=season_number,
            defaults={
                "title": tv_with_seasons_metadata["title"],
                "image": season_metadata["image"],
                "country": season_metadata.get("country") or "",
            },
        )'''

# Fix 3: sync_metadata — Item.objects.update_or_create also missing country
OLD3 = '''        item, _ = Item.objects.update_or_create(
            media_id=media_id,
            source=source,
            media_type=media_type,
            season_number=season_number,
            defaults={
                "title": metadata["title"],
                "image": metadata["image"],
            },
        )'''

NEW3 = '''        item, _ = Item.objects.update_or_create(
            media_id=media_id,
            source=source,
            media_type=media_type,
            season_number=season_number,
            defaults={
                "title": metadata["title"],
                "image": metadata["image"],
                "country": metadata.get("country") or "",
            },
        )'''

for old, new, label in [(OLD1, NEW1, "media_save get_or_create"),
                         (OLD2, NEW2, "episode_save get_or_create"),
                         (OLD3, NEW3, "sync_metadata update_or_create")]:
    if old in text:
        text = text.replace(old, new, 1)
        print(f"  OK   {label}")
    else:
        print(f"  SKIP {label} — already patched or not found")

views.write_text(text, encoding="utf-8")

# Also fix the Item model field to allow blank (default="") instead of null constraint
models_py = Path(r"C:\yamtrack-fork\src\app\models.py")
mtext = models_py.read_text(encoding="utf-8")
if 'country = models.CharField(max_length=2, blank=True, default="")' in mtext:
    print("  OK   models.py — Item.country already has default='' (migration may need null=False check)")
else:
    print("  WARN models.py — check Item.country field definition manually")

print()
print("Done. Commit and rebuild:")
print("  git add src/app/views.py")
print("  git commit -m 'fix: include country in all Item get_or_create defaults'")
print("  docker compose down; docker compose up -d --build")
