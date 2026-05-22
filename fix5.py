from pathlib import Path

stats = Path(r"C:\yamtrack-fork\src\app\statistics.py")
text = stats.read_text(encoding="utf-8")

to_append = '''

def get_progress_distribution(user_media):
    """Get distribution of media by completion percentage."""
    progress_buckets = {
        "Not Started": 0,
        "1-25%": 0,
        "26-50%": 0,
        "51-75%": 0,
        "76-99%": 0,
        "100%": 0,
    }

    for media_type, media_list in user_media.items():
        for media in media_list:
            max_progress = getattr(media, "max_progress", None)
            progress = getattr(media, "progress", 0) or 0

            if max_progress and max_progress > 0:
                percentage = (progress / max_progress) * 100
            elif progress > 0:
                percentage = 100
            else:
                percentage = 0

            if percentage == 0:
                progress_buckets["Not Started"] += 1
            elif percentage < 26:
                progress_buckets["1-25%"] += 1
            elif percentage < 51:
                progress_buckets["26-50%"] += 1
            elif percentage < 76:
                progress_buckets["51-75%"] += 1
            elif percentage < 100:
                progress_buckets["76-99%"] += 1
            else:
                progress_buckets["100%"] += 1

    return progress_buckets


def get_media_by_type_country_data(user_media):
    """Format country data per media type for world map display.

    Returns the same shape as get_country_distribution — kept as a separate
    function so the view can pass both independently to the template.
    """
    return get_country_distribution(user_media)
'''

if "def get_progress_distribution" not in text:
    stats.write_text(text + to_append, encoding="utf-8")
    print("  OK   appended get_progress_distribution + get_media_by_type_country_data")
else:
    print("  SKIP already present")

# Clean up temp files
for f in ["statistics_append.py", "views_country_patch.py", "statistics_patch.py"]:
    p = Path(r"C:\yamtrack-fork\src\app") / f
    if p.exists():
        p.unlink()
        print(f"  OK   deleted {f}")

print()
print("Done. Commit and rebuild:")
print("  git add src/app/statistics.py")
print("  git commit -m 'fix: restore get_progress_distribution and get_media_by_type_country_data'")
print("  docker compose down; docker compose up -d --build")
