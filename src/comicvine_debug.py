"""Debug script: inspect a Comic Vine volume's issue list / a single issue,
or search issues by name.

Use this to confirm a candidate volume's issue_number sequence actually
matches the French BnF album numbering (and that titles/covers look
right) BEFORE adding it to bnf._BD_COMICVINE_VOLUMES.

Usage (inside the container):
    docker compose cp src/comicvine_debug.py yamtrack:/yamtrack/comicvine_debug.py

    # list every issue in a volume, sorted by issue number
    docker compose exec yamtrack python comicvine_debug.py <volume_id>

    # look up one specific issue by number
    docker compose exec yamtrack python comicvine_debug.py <volume_id> <issue_number>

    # search issues by title (optionally scoped to one volume)
    docker compose exec yamtrack python comicvine_debug.py --search "<title>" [volume_id]

<volume_id> is the bare numeric Comic Vine volume id (no "4050-" prefix) --
e.g. for https://comicvine.gamespot.com/lucky-luke/4050-48134/ that's 48134.
"""

import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from app.providers import comicvine  # noqa: E402


def run_search(args):
    if not args:
        print("Usage: comicvine_debug.py --search \"<title>\" [volume_id]")
        sys.exit(1)

    query = args[0]
    volume_id = args[1] if len(args) > 1 else None

    results = comicvine.search_issues(query, volume_id=volume_id)
    scope = f" in volume {volume_id}" if volume_id else " (unscoped)"
    print(f"{len(results)} result(s) for {query!r}{scope}\n")

    for r in results:
        vol = r.get("volume") or {}
        print(f"  issue #{r.get('issue_number')}  {r.get('name')!r}")
        print(f"    volume:      {vol.get('name')!r} (id={vol.get('id')})")
        print(f"    cover_date:  {r.get('cover_date')}")
        print(f"    image:       {comicvine.get_image(r)}")
        print()


def run_volume(args):
    volume_id = args[0]

    issues = comicvine.get_volume_issues(volume_id)
    print(f"{len(issues)} issues found for volume {volume_id}\n")

    preview = issues if len(issues) <= 15 else issues[:10] + issues[-5:]
    for i, item in enumerate(preview):
        if len(issues) > 15 and i == 10:
            print("  ...")
        number = item.get("issue_number")
        name = item.get("name")
        date = item.get("cover_date")
        print(f"  #{number!s:>4}  {name!r:<40}  {date}")

    if len(args) > 1:
        number = args[1]
        print(f"\nLookup issue #{number} in volume {volume_id}:")
        match = comicvine.get_issue_by_number(volume_id, number)
        if match:
            print(f"  name:        {match.get('name')!r}")
            print(f"  cover_date:  {match.get('cover_date')}")
            print(f"  image:       {comicvine.get_image(match)}")
        else:
            print("  no match")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    if args[0] == "--search":
        run_search(args[1:])
    else:
        run_volume(args)


if __name__ == "__main__":
    main()
