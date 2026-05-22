from pathlib import Path

ROOT = Path(r"C:\yamtrack-fork")

# ── 1. views.py: set country on new media instances ──────────────────────────
views = ROOT / "src" / "app" / "views.py"
text = views.read_text(encoding="utf-8")

OLD = "        model = apps.get_model(app_label=\"app\", model_name=media_type)\n        instance = model(item=item, user=request.user)"
NEW = "        model = apps.get_model(app_label=\"app\", model_name=media_type)\n        instance = model(item=item, user=request.user, country=metadata.get(\"country\") or \"\")"

if OLD in text:
    views.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print("  OK   views.py — media_save sets country on new instance")
else:
    print("  SKIP views.py — pattern not found (already patched?)")

# ── 2. statistics.py: fix get_country_distribution to read media.country ─────
stats = ROOT / "src" / "app" / "statistics.py"
text = stats.read_text(encoding="utf-8")

OLD2 = "        for media in media_list.select_related(\"item\"):\n            code = (getattr(media.item, \"country\", None) or \"\").strip().upper()"
NEW2 = "        for media in media_list:\n            code = (getattr(media, \"country\", None) or \"\").strip().upper()"

if OLD2 in text:
    stats.write_text(text.replace(OLD2, NEW2, 1), encoding="utf-8")
    print("  OK   statistics.py — reads media.country not media.item.country")
elif "for media in media_list:\n            code = (getattr(media, \"country\"" in text:
    print("  SKIP statistics.py — already reads media.country")
else:
    print("  WARN statistics.py — pattern not found, check get_country_distribution manually")

# ── 3. Clean up temp files ────────────────────────────────────────────────────
for f in ["views_country_patch.py", "statistics_patch.py"]:
    p = ROOT / "src" / "app" / f
    if p.exists():
        p.unlink()
        print(f"  OK   deleted {f}")

print()
print("Done. Commit and rebuild:")
print("  git add src/app/views.py src/app/statistics.py")
print("  git commit -m 'fix: set media.country on track; read media.country in stats'")
print("  docker compose down; docker compose up -d --build")
print()
print("Then backfill existing items via the shell:")
print("  docker compose exec yamtrack python manage.py shell -c \"")
print("  from app.models import *")
print("  from app.providers import services")
print("  models = [Movie, TV, Season, Anime, Manga, Game, Book, Comic, BoardGame, Music]")
print("  for M in models:")
print("      for m in M.objects.filter(country=''):")
print("          try:")
print("              meta = services.get_media_metadata(m.item.media_type, m.item.media_id, m.item.source)")
print("              c = meta.get('country') or ''")
print("              if c:")
print("                  m.country = c; m.save(update_fields=['country'])")
print("                  print('OK', m)")
print("          except Exception as e: print('SKIP', m, e)")
print("  \"")
