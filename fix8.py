from pathlib import Path

models_py = Path(r"C:\yamtrack-fork\src\app\models.py")
text = models_py.read_text(encoding="utf-8")

# Add country field to Item model after the image field
OLD = "    title = models.TextField()\n    image = models.URLField()  # if add default, custom media entry will show the value\n    season_number"
NEW = "    title = models.TextField()\n    image = models.URLField()  # if add default, custom media entry will show the value\n    country = models.CharField(max_length=2, blank=True, default=\"\")\n    season_number"

if OLD in text:
    text = text.replace(OLD, NEW, 1)
    models_py.write_text(text, encoding="utf-8")
    print("  OK   models.py — Item.country field added")
else:
    print("  SKIP models.py — pattern not found (check manually)")

print()
print("Done. Now also run this to set a DB default so the column never gets NULL:")
print()
print("  docker compose exec yamtrack python manage.py shell -c \"")
print("  from django.db import connection")
print("  with connection.cursor() as c:")
print("      c.execute(\\\"ALTER TABLE app_item ALTER COLUMN country SET DEFAULT ''\\\")") 
print("      print('DB default set')")
print("  \"")
print()
print("Then commit and rebuild:")
print("  git add src/app/models.py")
print("  git commit -m 'fix: add country field to Item model'")
print("  docker compose down; docker compose up -d --build")
