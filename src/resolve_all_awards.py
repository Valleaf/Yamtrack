"""Auto-resolve correct TMDB/MAL ids for every winner in awards_data.py by
searching the provider for the title named in that winner's `# comment`,
then picking the best candidate by name-similarity + release-year proximity
to the award year.

This is a best-effort pass -- festival winners can have release years that
differ from the festival year by 1 (sometimes 2), and some titles are
generic enough that search may return an unrelated match. Every resolved
id is printed with its similarity/year-delta score so low-confidence picks
can be spotted and hand-checked; nothing is written back to
awards_data.py automatically.

Run inside the container:
    docker compose cp src/resolve_all_awards.py yamtrack:/yamtrack/resolve_all_awards.py
    docker compose exec yamtrack python resolve_all_awards.py
"""
import difflib
import os
import re

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings  # noqa: E402
from django.utils import timezone  # noqa: E402

from app.models import Sources  # noqa: E402
from app.providers import services  # noqa: E402

AWARDS_DATA_PATH = "/yamtrack/app/awards_data.py"


def normalize(title):
    return re.sub(r"[^a-z0-9]", "", title.lower())


def extract_comment_title(comment):
    """Pull the searchable title out of a trailing '# Title — Director (notes)'
    comment. Strips director/notes after an em-dash and any parenthetical.
    Returns '' for placeholder/instructional comments (e.g. "Add TMDB IDs
    from...", "Look up at...") that aren't actually a title to search.
    """
    text = comment.strip()
    if re.match(r"^(Add|Look up|Populate)\b", text, re.IGNORECASE):
        return ""
    text = text.split("—")[0].split("(verify")[0].strip()
    text = re.sub(r"\s*\(.*?\)\s*$", "", text).strip()
    return text


def search_tmdb_movie(title):
    from app.providers import tmdb
    base_url = "https://api.themoviedb.org/3"
    params = {**tmdb.base_params, "query": title}
    response = services.api_request(
        Sources.TMDB.value, "GET", f"{base_url}/search/movie",
        params=params,
    )
    return response.get("results", [])


def search_tmdb_tv(title):
    from app.providers import tmdb
    base_url = "https://api.themoviedb.org/3"
    params = {**tmdb.base_params, "query": title}
    response = services.api_request(
        Sources.TMDB.value, "GET", f"{base_url}/search/tv",
        params=params,
    )
    return response.get("results", [])


def search_mal_manga(title):
    from app.providers import mal
    return mal.search("manga", title, 1).get("results", [])


def best_tmdb_match(results, wanted_title, award_year, is_tv=False):
    wanted_norm = normalize(wanted_title)
    scored = []
    for r in results:
        date_field = "first_air_date" if is_tv else "release_date"
        name_field = "name" if is_tv else "title"
        date_str = r.get(date_field) or ""
        year = int(date_str[:4]) if date_str[:4].isdigit() else None
        year_delta = abs(year - award_year) if year else 99
        sim = difflib.SequenceMatcher(
            None, wanted_norm, normalize(r.get(name_field, "")),
        ).ratio()
        # Prefer close title match, then closest release year, then popularity.
        scored.append((sim, -year_delta, r.get("popularity", 0), r, year))
    scored.sort(key=lambda t: (t[0], t[1], t[2]), reverse=True)
    return scored[0] if scored else None


def best_mal_match(results, wanted_title, award_year):
    """Same as best_tmdb_match but for MAL's normalized search result shape
    (media_id/title/year instead of TMDB's id/title-or-name/release_date).
    """
    wanted_norm = normalize(wanted_title)
    scored = []
    for r in results:
        year_str = r.get("year") or ""
        year = int(year_str) if str(year_str).isdigit() else None
        year_delta = abs(year - award_year) if year else 99
        sim = difflib.SequenceMatcher(
            None, wanted_norm, normalize(r.get("title", "")),
        ).ratio()
        scored.append((sim, -year_delta, 0, r, year))
    scored.sort(key=lambda t: (t[0], t[1], t[2]), reverse=True)
    return scored[0] if scored else None


def process_award(award):
    source = award["source"]
    media_type = award["media_type"]
    id_key = f"{source}_id"
    is_tv = media_type == "tv"
    print(f"\n[{award['slug']}] {award['name']}")

    for winner in award["winners"]:
        comment = winner.pop("_comment", "")
        wanted_title = extract_comment_title(comment)
        if not wanted_title:
            continue
        year = winner["year"]

        try:
            if source == "tmdb" and not is_tv:
                results = search_tmdb_movie(wanted_title)
            elif source == "tmdb" and is_tv:
                results = search_tmdb_tv(wanted_title)
            elif source == "mal":
                results = search_mal_manga(wanted_title)
            else:
                print(f"    year={year}  SKIP (source={source} not auto-searchable)")
                continue
        except Exception as e:  # noqa: BLE001
            print(f"    year={year}  wanted={wanted_title!r}  SEARCH ERROR: {e}")
            continue

        if not results:
            print(f"    year={year}  wanted={wanted_title!r}  NO RESULTS")
            continue

        match = (
            best_mal_match(results, wanted_title, year)
            if source == "mal"
            else best_tmdb_match(results, wanted_title, year, is_tv=is_tv)
        )
        if not match:
            print(f"    year={year}  wanted={wanted_title!r}  NO MATCH")
            continue

        sim, neg_delta, pop, r, match_year = match
        old_id = winner.get(id_key)
        new_id = r["media_id"] if source == "mal" else r["id"]
        flag = "" if sim > 0.85 else "  <<< LOW CONFIDENCE, CHECK BY HAND"
        print(
            f"    year={year}  wanted={wanted_title!r:<50} "
            f"old_id={old_id}  new_id={new_id}  match_year={match_year}  "
            f"sim={sim:.2f}{flag}"
        )


# --------------------------------------------------------------------------
# We need the ORIGINAL comments, which aren't in the Python data structures
# (they're stripped by the parser). Re-parse the source file directly to
# pair each winner dict with its trailing comment, using a simple per-line
# regex since the file has one winner per line.
# --------------------------------------------------------------------------
import ast  # noqa: E402


def load_awards_with_comments():
    with open(AWARDS_DATA_PATH, encoding="utf-8") as f:
        lines = f.readlines()

    line_re = re.compile(
        r'\{"year":\s*(\d+),\s*"(\w+_id)":\s*(?:"([^"]*)"|None)\}\s*,?\s*#\s*(.*)'
    )
    slug_re = re.compile(r'"slug":\s*"(\w+)"')
    name_re = re.compile(r'"name":\s*"([^"]*)"')
    media_type_re = re.compile(r'"media_type":\s*"(\w+)"')
    source_re = re.compile(r'"source":\s*"(\w+)"')

    awards = []
    current = None
    for line in lines:
        slug_m = slug_re.search(line)
        if slug_m and '"name"' not in line:
            if current:
                awards.append(current)
            current = {"slug": slug_m.group(1), "name": slug_m.group(1), "winners": []}
            continue
        if current is None:
            continue
        name_m = name_re.search(line)
        if name_m:
            current["name"] = name_m.group(1)
            continue
        mt_m = media_type_re.search(line)
        if mt_m:
            current["media_type"] = mt_m.group(1)
            continue
        src_m = source_re.search(line)
        if src_m:
            current["source"] = src_m.group(1)
            continue
        w_m = line_re.search(line)
        if w_m:
            year, id_key, id_val, comment = w_m.groups()
            current["winners"].append({
                "year": int(year),
                id_key: id_val,
                "_comment": comment,
            })
    if current:
        awards.append(current)
    return [a for a in awards if "media_type" in a and "source" in a]


AWARDS = load_awards_with_comments()
for award in AWARDS:
    process_award(award)

print("\nDone. Entries with no printed line either had no comment to search")
print("from, or belong to a source this script doesn't auto-search yet")
print("(hardcover/bnf) -- those still need manual lookup.")
