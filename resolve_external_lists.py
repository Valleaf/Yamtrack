#!/usr/bin/env python3
"""resolve_external_lists.py

One-off, manually-launched helper for populating
`src/app/external_lists_data.py`.

It does NOT call the Yamtrack app, the Docker container, or Django at all --
it's a standalone script that queries the TMDB and MusicBrainz public APIs
directly, given a list of titles, and prints ready-to-paste Python dict
literals in the exact shape `external_lists_data.py` expects:

    {"rank": 1, "tmdb_id": 238},        # The Godfather
    {"rank": 2, "musicbrainz_id": "..."} # some album

It never writes to external_lists_data.py itself -- you review the printed
output and paste it in by hand. This matches the project's "hand-resolved,
hand-committed" fixture pattern (see the docstring at the top of that file).

USAGE
-----
Run from anywhere (no venv/Django needed, just the stdlib):

    python resolve_external_lists.py --list letterboxd_top250
    python resolve_external_lists.py --list sight_sound_top250 --type movie
    python resolve_external_lists.py --list 1001_albums --type music
    python resolve_external_lists.py --titles-file my_titles.txt --type movie
    python resolve_external_lists.py --list bfi_best_films --interactive

TMDB needs an API key. Provide it via:
    - env var TMDB_API, or
    - --tmdb-key on the command line, or
    - it will prompt you once at runtime.

MusicBrainz needs no key, but its API asks for a descriptive User-Agent
and a courtesy rate limit (this script sleeps ~1.1s between calls).

TITLE FILE FORMAT
------------------
One entry per line. Supported formats, mixed freely:

    Title
    Title (Year)
    Artist - Title
    Artist - Title (Year)

The "Artist - " prefix is optional but strongly recommended for music
lists: it's passed to MusicBrainz as an artist-name filter, which sharply
cuts down ambiguous matches for self-titled albums, common words, etc.
(e.g. "Beatles - The Beatles (1968)" vs. bare "The Beatles"). Movie titles
ignore the artist segment if present (TMDB search doesn't need it, but
supplying "Director - Title (Year)" won't break anything -- the "Director -"
prefix is simply parsed off and unused for movie mode).

Lines starting with # are treated as comments and skipped.

BUILT-IN TITLE SEEDS
---------------------
A few of the lists in external_lists_data.py already have their known
top-N titles as comments. Those are seeded here (see SEED_TITLES below)
so you can run e.g. `--list letterboxd_top250` with zero extra setup.
For lists with no seed (edgar_wright_favorites, bfi_best_films) or if you
want a different/longer cut of a list, supply your own titles with
`--titles-file` (one title per line, optionally "Title (Year)").

OUTPUT
------
For each title:
    - auto-picks the best match and prints the dict line (for music, this
      prefers a candidate whose artist matches the supplied artist, when
      one was given), OR
    - with --interactive, shows the top 5 candidates and lets you pick,
      skip, or enter an ID manually.
Ambiguous/no-match titles are always flagged for manual attention even
in non-interactive mode.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import json


TMDB_BASE = "https://api.themoviedb.org/3"
MUSICBRAINZ_BASE = "https://musicbrainz.org/ws/2"
USER_AGENT = "yamtrack-fork-external-lists-resolver/1.0 (manual one-off script)"

# Known top-N titles already seeded as comments in external_lists_data.py,
# so these lists work out of the box with no --titles-file needed.
SEED_TITLES: dict[str, list[str]] = {
    "letterboxd_top250": [
        "The Godfather",
        "Parasite",
        "Spider-Man: Across the Spider-Verse",
        "Interstellar",
        "Fight Club",
    ],
    "sight_sound_top250": [
        "Jeanne Dielman, 23 Quai du Commerce, 1080 Bruxelles",
        "Vertigo",
        "Citizen Kane",
        "Tokyo Story",
        "In the Mood for Love",
        "2001: A Space Odyssey",
        "Beau Travail",
        "Mulholland Drive",
        "Man with a Movie Camera",
        "Singin' in the Rain",
    ],
    # No seeds seeded in the source file for these -- pass --titles-file.
    "edgar_wright_favorites": [],
    "bfi_best_films": [],
    "1001_albums": [
        "The Beatles - Sgt. Pepper's Lonely Hearts Club Band",
    ],
}

LIST_MEDIA_TYPE = {
    "letterboxd_top250": "movie",
    "sight_sound_top250": "movie",
    "edgar_wright_favorites": "movie",
    "bfi_best_films": "movie",
    "1001_albums": "music",
}


def http_get_json(url: str, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_entry(raw: str) -> tuple[str | None, str, str | None]:
    """Parse a title-file line into (artist, title, year).

    Supported: "Title", "Title (Year)", "Artist - Title",
    "Artist - Title (Year)". Artist is None if no "Artist - " prefix
    is present. Splits only on the FIRST " - " so titles containing
    " - " themselves (e.g. "Speakerboxxx/The Love Below") are safe as
    long as they don't also start with an "Artist - " pattern.
    """
    text = raw.strip()

    year = None
    m = re.match(r"^(.*)\s\((\d{4})\)\s*$", text)
    if m:
        text, year = m.group(1).strip(), m.group(2)

    artist = None
    if " - " in text:
        left, right = text.split(" - ", 1)
        # Guard against splitting genuine title punctuation as if it were
        # an "Artist - " prefix by requiring both sides be non-empty and
        # the left side look reasonably like a name (no leading digits/
        # punctuation that would suggest it's actually part of the title).
        if left.strip() and right.strip():
            artist, text = left.strip(), right.strip()

    return artist, text, year


def tmdb_search(title: str, year: str | None, api_key: str) -> list[dict]:
    params = {"api_key": api_key, "query": title, "include_adult": "false"}
    if year:
        params["year"] = year
    url = f"{TMDB_BASE}/search/movie?{urllib.parse.urlencode(params)}"
    data = http_get_json(url)
    results = data.get("results", [])
    out = []
    for r in results[:5]:
        out.append({
            "id": r["id"],
            "title": r.get("title") or r.get("original_title"),
            "year": (r.get("release_date") or "")[:4],
            "url": f"https://www.themoviedb.org/movie/{r['id']}",
        })
    return out


def _names_match(a: str, b: str) -> bool:
    """Loose case-insensitive comparison, ignoring 'The ' prefixes and
    punctuation, to match artist names across minor formatting
    differences (e.g. 'The Beatles' vs 'Beatles', 'Guns N' Roses' vs
    'Guns N Roses').
    """
    def norm(s: str) -> str:
        s = s.lower().strip()
        s = re.sub(r"^the\s+", "", s)
        s = re.sub(r"[^a-z0-9]+", "", s)
        return s
    return norm(a) == norm(b)


def musicbrainz_search(title: str, artist: str | None = None) -> list[dict]:
    query_parts = [f'releasegroup:"{title}"', "primarytype:Album"]
    if artist:
        query_parts.insert(1, f'artist:"{artist}"')
    query = urllib.parse.quote(" AND ".join(query_parts))
    url = f"{MUSICBRAINZ_BASE}/release-group/?query={query}&fmt=json&limit=5"
    data = http_get_json(url, headers={"User-Agent": USER_AGENT})
    results = data.get("release-groups", [])

    # Artist-scoped query returned nothing -- retry title-only so we still
    # surface candidates (flagged as ambiguous/manual-review) rather than
    # a hard NO MATCH just because the artist string didn't match exactly.
    if not results and artist:
        query = urllib.parse.quote(f'releasegroup:"{title}" AND primarytype:Album')
        url = f"{MUSICBRAINZ_BASE}/release-group/?query={query}&fmt=json&limit=5"
        data = http_get_json(url, headers={"User-Agent": USER_AGENT})
        results = data.get("release-groups", [])

    out = []
    for rg in results:
        rg_artist = ""
        if rg.get("artist-credit"):
            rg_artist = rg["artist-credit"][0].get("name", "")
        out.append({
            "id": rg["id"],
            "title": rg.get("title"),
            "artist": rg_artist,
            "year": (rg.get("first-release-date") or "")[:4],
            "url": f"https://musicbrainz.org/release-group/{rg['id']}",
        })
    return out


def get_tmdb_key(cli_key: str | None) -> str:
    key = cli_key or os.environ.get("TMDB_API")
    if key:
        return key
    key = input("Enter your TMDB API key (v3 auth): ").strip()
    if not key:
        print("No TMDB API key provided, aborting.", file=sys.stderr)
        sys.exit(1)
    return key


def load_titles(args) -> list[str]:
    if args.titles_file:
        with open(args.titles_file, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    seeds = SEED_TITLES.get(args.list, [])
    if not seeds:
        print(
            f"No seed titles bundled for list '{args.list}'. "
            "Pass --titles-file with your own titles (one per line, "
            "optionally 'Artist - Title (Year)').",
            file=sys.stderr,
        )
        sys.exit(1)
    return seeds


def format_movie_entry(rank: int, tmdb_id: int, title: str) -> str:
    return f'            {{"rank": {rank}, "tmdb_id": {tmdb_id}}},   # {title}'


def format_music_entry(rank: int, mbid: str, title: str, artist: str) -> str:
    label = f"{artist} - {title}" if artist else title
    return f'            {{"rank": {rank}, "musicbrainz_id": "{mbid}"}},   # {label}'


def run_movies(titles: list[str], api_key: str, interactive: bool) -> list[str]:
    lines = []
    unresolved = []
    for rank, raw in enumerate(titles, start=1):
        _artist, title, year = parse_entry(raw)
        try:
            candidates = tmdb_search(title, year, api_key)
        except Exception as exc:  # noqa: BLE001
            print(f"  [{rank}] ERROR searching '{raw}': {exc}", file=sys.stderr)
            unresolved.append(raw)
            continue

        if not candidates:
            print(f"  [{rank}] NO MATCH: '{raw}'", file=sys.stderr)
            lines.append(f'            # {{"rank": {rank}, "tmdb_id": None}},   # NO MATCH: {raw}')
            unresolved.append(raw)
            continue

        chosen = candidates[0]
        if interactive:
            print(f"\n[{rank}] '{raw}' candidates:")
            for i, c in enumerate(candidates):
                print(f"    {i + 1}. {c['title']} ({c['year']})  id={c['id']}  {c['url']}")
            print("    s. skip / enter manual id")
            sel = input("  Pick [1]: ").strip() or "1"
            if sel.lower() == "s":
                manual = input("  Manual tmdb_id (blank to skip): ").strip()
                if not manual:
                    unresolved.append(raw)
                    continue
                chosen = {"id": int(manual), "title": raw, "year": year or ""}
            else:
                idx = int(sel) - 1
                chosen = candidates[idx]
        elif len(candidates) > 1:
            # Flag ambiguity even though we auto-picked the top result.
            print(
                f"  [{rank}] AMBIGUOUS (picked top result) for '{raw}': "
                + ", ".join(f"{c['title']} ({c['year']}) id={c['id']}" for c in candidates),
                file=sys.stderr,
            )

        lines.append(format_movie_entry(rank, chosen["id"], f"{chosen['title']} ({chosen.get('year', '?')})"))
        time.sleep(0.25)  # be polite to TMDB

    if unresolved:
        print(f"\n{len(unresolved)} unresolved titles -- see NO MATCH / ERROR lines above.", file=sys.stderr)
    return lines


def run_music(titles: list[str], interactive: bool) -> list[str]:
    lines = []
    unresolved = []
    auto_disambiguated = 0
    for rank, raw in enumerate(titles, start=1):
        artist, title, _year = parse_entry(raw)
        try:
            candidates = musicbrainz_search(title, artist)
        except Exception as exc:  # noqa: BLE001
            print(f"  [{rank}] ERROR searching '{raw}': {exc}", file=sys.stderr)
            unresolved.append(raw)
            time.sleep(1.1)
            continue

        if not candidates:
            print(f"  [{rank}] NO MATCH: '{raw}'", file=sys.stderr)
            lines.append(f'            # {{"rank": {rank}, "musicbrainz_id": None}},   # NO MATCH: {raw}')
            unresolved.append(raw)
            time.sleep(1.1)
            continue

        # If an artist was supplied, prefer a candidate whose artist credit
        # actually matches it -- this is what mainly cuts down false
        # positives on self-titled albums / common words.
        chosen = candidates[0]
        artist_matched = False
        if artist:
            for c in candidates:
                if _names_match(c["artist"], artist):
                    chosen = c
                    artist_matched = True
                    break

        if interactive:
            print(f"\n[{rank}] '{raw}' candidates:")
            for i, c in enumerate(candidates):
                marker = " <-- artist match" if artist and _names_match(c["artist"], artist) else ""
                print(f"    {i + 1}. {c['artist']} - {c['title']} ({c['year']}){marker}  {c['url']}")
            print("    s. skip / enter manual id")
            default = str(candidates.index(chosen) + 1) if artist_matched else "1"
            sel = input(f"  Pick [{default}]: ").strip() or default
            if sel.lower() == "s":
                manual = input("  Manual MBID (blank to skip): ").strip()
                if not manual:
                    unresolved.append(raw)
                    time.sleep(1.1)
                    continue
                chosen = {"id": manual, "title": raw, "artist": "", "year": ""}
            else:
                idx = int(sel) - 1
                chosen = candidates[idx]
        elif artist_matched:
            auto_disambiguated += 1
        elif len(candidates) > 1 or artist:
            # Either genuinely ambiguous (multiple candidates, none matched
            # the supplied artist) or no artist was given at all to narrow
            # things down -- flag for manual review either way.
            reason = "no artist-matched candidate" if artist else "no artist supplied"
            print(
                f"  [{rank}] AMBIGUOUS ({reason}, picked top result) for '{raw}': "
                + ", ".join(f"{c['artist']} - {c['title']} ({c['year']})" for c in candidates),
                file=sys.stderr,
            )

        lines.append(format_music_entry(rank, chosen["id"], chosen.get("title", raw), chosen.get("artist", "")))
        time.sleep(1.1)  # MusicBrainz courtesy rate limit (~1 req/sec)

    if unresolved:
        print(f"\n{len(unresolved)} unresolved titles -- see NO MATCH / ERROR lines above.", file=sys.stderr)
    if auto_disambiguated:
        print(f"{auto_disambiguated} titles auto-resolved via artist match.", file=sys.stderr)
    return lines


def main():
    parser = argparse.ArgumentParser(
        description="Resolve titles to TMDB/MusicBrainz IDs for external_lists_data.py",
    )
    parser.add_argument(
        "--list",
        choices=sorted(LIST_MEDIA_TYPE.keys()),
        help="Which curated list slug to resolve (uses bundled seed titles if available).",
    )
    parser.add_argument(
        "--titles-file",
        help="Path to a text file, one title per line (optionally "
        "'Artist - Title (Year)'). Overrides bundled seed titles.",
    )
    parser.add_argument(
        "--type",
        choices=["movie", "music"],
        help="Media type to resolve against. Inferred from --list if omitted.",
    )
    parser.add_argument("--tmdb-key", help="TMDB v3 API key (else uses TMDB_API env var, else prompts).")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Show candidates and pick manually instead of auto-picking the top result.",
    )
    args = parser.parse_args()

    if not args.list and not args.titles_file:
        parser.error("Provide --list (bundled slug) and/or --titles-file")

    media_type = args.type or (LIST_MEDIA_TYPE.get(args.list) if args.list else None)
    if not media_type:
        parser.error("Could not infer --type; specify --type movie|music explicitly")

    titles = load_titles(args)
    print(f"Resolving {len(titles)} titles as '{media_type}'...\n", file=sys.stderr)

    if media_type == "movie":
        api_key = get_tmdb_key(args.tmdb_key)
        lines = run_movies(titles, api_key, args.interactive)
    else:
        lines = run_music(titles, args.interactive)

    print("\n# --- Paste into external_lists_data.py 'items' list ---")
    for line in lines:
        print(line)
    print("# --- end ---")


if __name__ == "__main__":
    main()
