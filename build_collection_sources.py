#!/usr/bin/env python3
"""
build_collection_sources.py — Run from C:/yamtrack-fork
Adds all collection source types + provider fetch functions.
"""
from pathlib import Path

ROOT = Path(r"C:\yamtrack-fork")
SRC = ROOT / "src"
APP = SRC / "app"
COL = SRC / "collections"


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  OK   {path.relative_to(ROOT)}")


def patch(path: Path, old: str, new: str, label: str):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        print(f"  SKIP {label}")
        return False
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"  OK   {label}")
    return True


# ─────────────────────────────────────────────────────────────
# 1. New provider: collections_providers.py
#    All source-specific search + fetch logic lives here.
# ─────────────────────────────────────────────────────────────
print("\n[1] app/providers/collections_providers.py")
write(APP / "providers" / "collections_providers.py", '''\
"""
Fetch logic for every collection source type.
Each source exposes two functions:
  search_{source}(query) -> list of {id, name, overview, image, source_key}
  fetch_{source}(source_id) -> {name, overview, image, items: [...]}
Each item in items: {media_id, source, media_type, title, image}
"""
import logging
import time

import requests
from django.core.cache import cache
from django.conf import settings

from app.models import MediaTypes, Sources
from app.providers import services

logger = logging.getLogger(__name__)


# ── helpers ───────────────────────────────────────────────────────────────────

def _get(url, params=None, headers=None, timeout=10):
    resp = requests.get(url, params=params, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def _tmdb_params(**extra):
    p = {"api_key": settings.TMDB_API, "language": settings.TMDB_LANG}
    p.update(extra)
    return p


def _tmdb_img(path):
    if path:
        return f"https://image.tmdb.org/t/p/w500{path}"
    return settings.IMG_NONE


def _mb_headers():
    return {
        "User-Agent": "Yamtrack/1.0 (https://github.com/Valleaf/Yamtrack)",
        "Accept": "application/json",
    }


# ── TMDB: movie collection ─────────────────────────────────────────────────────

def search_tmdb_collection(query):
    key = f"col_search_tmdb_collection_{query}"
    cached = cache.get(key)
    if cached:
        return cached
    data = _get("https://api.themoviedb.org/3/search/collection",
                params=_tmdb_params(query=query))
    results = [{"id": str(r["id"]), "name": r.get("name", ""),
                "overview": r.get("overview", ""),
                "image": _tmdb_img(r.get("poster_path"))}
               for r in data.get("results", [])]
    cache.set(key, results, 300)
    return results


def fetch_tmdb_collection(source_id):
    key = f"col_fetch_tmdb_collection_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached

    data = _get(f"https://api.themoviedb.org/3/collection/{source_id}",
                params=_tmdb_params())

    def _date(m): return m.get("release_date") or "9999"
    parts = sorted(data.get("parts", []), key=_date)

    result = {
        "name": data.get("name", ""),
        "overview": data.get("overview", ""),
        "image": _tmdb_img(data.get("poster_path")),
        "source_url": f"https://www.themoviedb.org/collection/{source_id}",
        "items": [{"media_id": str(p["id"]), "source": Sources.TMDB.value,
                   "media_type": MediaTypes.MOVIE.value,
                   "title": p.get("title") or p.get("name", ""),
                   "image": _tmdb_img(p.get("poster_path"))}
                  for p in parts],
    }
    cache.set(key, result, 3600)
    return result


# ── TMDB: person (director / actor filmography) ───────────────────────────────

def search_tmdb_person(query):
    key = f"col_search_tmdb_person_{query}"
    cached = cache.get(key)
    if cached:
        return cached
    data = _get("https://api.themoviedb.org/3/search/person",
                params=_tmdb_params(query=query))
    results = [{"id": str(r["id"]), "name": r.get("name", ""),
                "overview": r.get("known_for_department", ""),
                "image": _tmdb_img(r.get("profile_path"))}
               for r in data.get("results", [])]
    cache.set(key, results, 300)
    return results


def fetch_tmdb_person(source_id):
    key = f"col_fetch_tmdb_person_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached

    person = _get(f"https://api.themoviedb.org/3/person/{source_id}",
                  params=_tmdb_params())
    credits = _get(f"https://api.themoviedb.org/3/person/{source_id}/combined_credits",
                   params=_tmdb_params())

    seen = set()
    items = []
    # crew first (director), then cast, sorted by popularity
    all_credits = credits.get("crew", []) + credits.get("cast", [])
    all_credits.sort(key=lambda x: x.get("popularity", 0), reverse=True)

    for c in all_credits:
        mid = str(c.get("id"))
        mt = c.get("media_type")
        if mid in seen or mt not in ("movie", "tv"):
            continue
        seen.add(mid)
        items.append({
            "media_id": mid,
            "source": Sources.TMDB.value,
            "media_type": MediaTypes.MOVIE.value if mt == "movie" else MediaTypes.TV.value,
            "title": c.get("title") or c.get("name", ""),
            "image": _tmdb_img(c.get("poster_path")),
        })

    result = {
        "name": person.get("name", ""),
        "overview": person.get("biography", ""),
        "image": _tmdb_img(person.get("profile_path")),
        "source_url": f"https://www.themoviedb.org/person/{source_id}",
        "items": items[:100],
    }
    cache.set(key, result, 3600)
    return result


# ── MAL: anime franchise (related graph) ─────────────────────────────────────

def _mal_headers():
    return {"X-MAL-CLIENT-ID": settings.MAL_API}


def search_mal_anime(query):
    key = f"col_search_mal_anime_{query}"
    cached = cache.get(key)
    if cached:
        return cached
    data = _get("https://api.myanimelist.net/v2/anime",
                params={"q": query, "limit": 10, "fields": "id,title,main_picture"},
                headers=_mal_headers())
    results = [{"id": str(r["node"]["id"]), "name": r["node"].get("title", ""),
                "overview": "", "image": (r["node"].get("main_picture") or {}).get("medium", settings.IMG_NONE)}
               for r in data.get("data", [])]
    cache.set(key, results, 300)
    return results


def fetch_mal_anime_franchise(source_id):
    """Crawl MAL related_anime to build a full franchise graph."""
    key = f"col_fetch_mal_anime_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached

    seed = _get(f"https://api.myanimelist.net/v2/anime/{source_id}",
                params={"fields": "title,main_picture,related_anime"},
                headers=_mal_headers())

    visited = set()
    queue = [source_id]
    items = []

    while queue and len(items) < 50:
        aid = queue.pop(0)
        if str(aid) in visited:
            continue
        visited.add(str(aid))
        try:
            a = _get(f"https://api.myanimelist.net/v2/anime/{aid}",
                     params={"fields": "title,main_picture,related_anime"},
                     headers=_mal_headers())
            time.sleep(0.3)
        except Exception:
            continue
        items.append({
            "media_id": str(a["id"]), "source": Sources.MAL.value,
            "media_type": MediaTypes.ANIME.value,
            "title": a.get("title", ""),
            "image": (a.get("main_picture") or {}).get("medium", settings.IMG_NONE),
        })
        for rel in a.get("related_anime", []):
            rid = str(rel.get("node", {}).get("id", ""))
            if rid and rid not in visited:
                queue.append(rid)

    result = {
        "name": seed.get("title", ""),
        "overview": "",
        "image": (seed.get("main_picture") or {}).get("medium", settings.IMG_NONE),
        "source_url": f"https://myanimelist.net/anime/{source_id}",
        "items": items,
    }
    cache.set(key, result, 3600)
    return result


def search_mal_manga(query):
    key = f"col_search_mal_manga_{query}"
    cached = cache.get(key)
    if cached:
        return cached
    data = _get("https://api.myanimelist.net/v2/manga",
                params={"q": query, "limit": 10, "fields": "id,title,main_picture"},
                headers=_mal_headers())
    results = [{"id": str(r["node"]["id"]), "name": r["node"].get("title", ""),
                "overview": "", "image": (r["node"].get("main_picture") or {}).get("medium", settings.IMG_NONE)}
               for r in data.get("data", [])]
    cache.set(key, results, 300)
    return results


def fetch_mal_manga_franchise(source_id):
    key = f"col_fetch_mal_manga_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached

    seed = _get(f"https://api.myanimelist.net/v2/manga/{source_id}",
                params={"fields": "title,main_picture,related_manga"},
                headers=_mal_headers())

    visited = set()
    queue = [source_id]
    items = []

    while queue and len(items) < 50:
        mid = queue.pop(0)
        if str(mid) in visited:
            continue
        visited.add(str(mid))
        try:
            m = _get(f"https://api.myanimelist.net/v2/manga/{mid}",
                     params={"fields": "title,main_picture,related_manga"},
                     headers=_mal_headers())
            time.sleep(0.3)
        except Exception:
            continue
        items.append({
            "media_id": str(m["id"]), "source": Sources.MAL.value,
            "media_type": MediaTypes.MANGA.value,
            "title": m.get("title", ""),
            "image": (m.get("main_picture") or {}).get("medium", settings.IMG_NONE),
        })
        for rel in m.get("related_manga", []):
            rid = str(rel.get("node", {}).get("id", ""))
            if rid and rid not in visited:
                queue.append(rid)

    result = {
        "name": seed.get("title", ""),
        "overview": "",
        "image": (seed.get("main_picture") or {}).get("medium", settings.IMG_NONE),
        "source_url": f"https://myanimelist.net/manga/{source_id}",
        "items": items,
    }
    cache.set(key, result, 3600)
    return result


# ── Hardcover: book series ─────────────────────────────────────────────────────

def search_hardcover_series(query):
    key = f"col_search_hc_series_{query}"
    cached = cache.get(key)
    if cached:
        return cached

    gql = """
    query SearchSeries($q: String!) {
      series(where: {name: {_ilike: $q}}, limit: 10) {
        id name description
        books { image { url } }
      }
    }
    """
    try:
        resp = requests.post(
            "https://api.hardcover.app/v1/graphql",
            json={"query": gql, "variables": {"q": f"%{query}%"}},
            headers={"Authorization": f"Bearer {settings.HARDCOVER_API}"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logger.warning("Hardcover series search failed: %s", e)
        return []

    results = []
    for s in data.get("data", {}).get("series", []):
        img = settings.IMG_NONE
        for b in s.get("books") or []:
            if b.get("image", {}).get("url"):
                img = b["image"]["url"]
                break
        results.append({"id": str(s["id"]), "name": s.get("name", ""),
                         "overview": s.get("description") or "", "image": img})
    cache.set(key, results, 300)
    return results


def fetch_hardcover_series(source_id):
    key = f"col_fetch_hc_series_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached

    gql = """
    query SeriesBooks($id: Int!) {
      series_by_pk(id: $id) {
        name description
        series_books(order_by: {position: asc}) {
          book {
            id title slug
            image { url }
            contributions { author { name } }
          }
        }
      }
    }
    """
    try:
        resp = requests.post(
            "https://api.hardcover.app/v1/graphql",
            json={"query": gql, "variables": {"id": int(source_id)}},
            headers={"Authorization": f"Bearer {settings.HARDCOVER_API}"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logger.warning("Hardcover series fetch failed: %s", e)
        return {"name": "", "overview": "", "image": settings.IMG_NONE, "items": []}

    series = data.get("data", {}).get("series_by_pk") or {}
    items = []
    for sb in series.get("series_books") or []:
        b = sb.get("book") or {}
        items.append({
            "media_id": str(b["id"]),
            "source": Sources.HARDCOVER.value,
            "media_type": MediaTypes.BOOK.value,
            "title": b.get("title", ""),
            "image": (b.get("image") or {}).get("url", settings.IMG_NONE),
        })

    img = items[0]["image"] if items else settings.IMG_NONE
    result = {
        "name": series.get("name", ""),
        "overview": series.get("description") or "",
        "image": img,
        "source_url": f"https://hardcover.app/series/{source_id}",
        "items": items,
    }
    cache.set(key, result, 3600)
    return result


# ── OpenLibrary: author works ──────────────────────────────────────────────────

def search_openlibrary_author(query):
    key = f"col_search_ol_author_{query}"
    cached = cache.get(key)
    if cached:
        return cached
    data = _get("https://openlibrary.org/search/authors.json",
                params={"q": query, "limit": 10})
    results = [{"id": d.get("key", "").replace("/authors/", ""),
                "name": d.get("name", ""),
                "overview": d.get("bio", ""),
                "image": f"https://covers.openlibrary.org/a/olid/{d.get('key','').replace('/authors/','')}-M.jpg"}
               for d in data.get("docs", [])]
    cache.set(key, results, 300)
    return results


def fetch_openlibrary_author(source_id):
    key = f"col_fetch_ol_author_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached

    author = _get(f"https://openlibrary.org/authors/{source_id}.json")
    works_data = _get(f"https://openlibrary.org/authors/{source_id}/works.json",
                      params={"limit": 50})

    items = []
    for w in works_data.get("entries", []):
        wid = w.get("key", "").replace("/works/", "")
        if not wid:
            continue
        covers = w.get("covers", [])
        img = f"https://covers.openlibrary.org/b/id/{covers[0]}-M.jpg" if covers and covers[0] > 0 else settings.IMG_NONE
        items.append({
            "media_id": wid,
            "source": Sources.OPENLIBRARY.value,
            "media_type": MediaTypes.BOOK.value,
            "title": w.get("title", ""),
            "image": img,
        })

    name = author.get("name", "")
    bio = author.get("bio", "")
    if isinstance(bio, dict):
        bio = bio.get("value", "")

    result = {
        "name": name,
        "overview": bio,
        "image": f"https://covers.openlibrary.org/a/olid/{source_id}-M.jpg",
        "source_url": f"https://openlibrary.org/authors/{source_id}",
        "items": items,
    }
    cache.set(key, result, 3600)
    return result


# ── IGDB: franchise ────────────────────────────────────────────────────────────

def _igdb_post(endpoint, body):
    from app.providers.igdb import get_access_token
    token = get_access_token()
    resp = requests.post(
        f"https://api.igdb.com/v4/{endpoint}",
        headers={"Client-ID": settings.IGDB_CLIENT_ID,
                 "Authorization": f"Bearer {token}"},
        data=body, timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def search_igdb_franchise(query):
    key = f"col_search_igdb_franchise_{query}"
    cached = cache.get(key)
    if cached:
        return cached
    try:
        data = _igdb_post("franchises",
                          f'search "{query}"; fields name,slug; limit 10;')
    except Exception as e:
        logger.warning("IGDB franchise search: %s", e)
        return []
    results = [{"id": str(r["id"]), "name": r.get("name", ""),
                "overview": "", "image": settings.IMG_NONE}
               for r in data]
    cache.set(key, results, 300)
    return results


def fetch_igdb_franchise(source_id):
    key = f"col_fetch_igdb_franchise_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached
    try:
        data = _igdb_post("franchises",
                          f"fields name,games.name,games.cover.image_id,games.first_release_date; where id = {source_id};")
    except Exception as e:
        logger.warning("IGDB franchise fetch: %s", e)
        return {"name": "", "overview": "", "image": settings.IMG_NONE, "items": []}

    franchise = data[0] if data else {}
    games = sorted(franchise.get("games", []),
                   key=lambda g: g.get("first_release_date") or 0)

    items = []
    for g in games:
        cover = g.get("cover") or {}
        img = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{cover['image_id']}.jpg" if cover.get("image_id") else settings.IMG_NONE
        items.append({"media_id": str(g["id"]), "source": Sources.IGDB.value,
                      "media_type": MediaTypes.GAME.value,
                      "title": g.get("name", ""), "image": img})

    first_img = items[0]["image"] if items else settings.IMG_NONE
    result = {
        "name": franchise.get("name", ""),
        "overview": "",
        "image": first_img,
        "source_url": f"https://www.igdb.com/franchises/{franchise.get('slug', source_id)}",
        "items": items,
    }
    cache.set(key, result, 3600)
    return result


def search_igdb_collection(query):
    key = f"col_search_igdb_collection_{query}"
    cached = cache.get(key)
    if cached:
        return cached
    try:
        data = _igdb_post("collections",
                          f'search "{query}"; fields name,slug; limit 10;')
    except Exception as e:
        logger.warning("IGDB collection search: %s", e)
        return []
    results = [{"id": str(r["id"]), "name": r.get("name", ""),
                "overview": "", "image": settings.IMG_NONE}
               for r in data]
    cache.set(key, results, 300)
    return results


def fetch_igdb_collection(source_id):
    key = f"col_fetch_igdb_collection_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached
    try:
        data = _igdb_post("collections",
                          f"fields name,slug,games.name,games.cover.image_id,games.first_release_date; where id = {source_id};")
    except Exception as e:
        logger.warning("IGDB collection fetch: %s", e)
        return {"name": "", "overview": "", "image": settings.IMG_NONE, "items": []}

    col = data[0] if data else {}
    games = sorted(col.get("games", []), key=lambda g: g.get("first_release_date") or 0)
    items = []
    for g in games:
        cover = g.get("cover") or {}
        img = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{cover['image_id']}.jpg" if cover.get("image_id") else settings.IMG_NONE
        items.append({"media_id": str(g["id"]), "source": Sources.IGDB.value,
                      "media_type": MediaTypes.GAME.value,
                      "title": g.get("name", ""), "image": img})

    result = {
        "name": col.get("name", ""),
        "overview": "",
        "image": items[0]["image"] if items else settings.IMG_NONE,
        "source_url": f"https://www.igdb.com/collections/{col.get('slug', source_id)}",
        "items": items,
    }
    cache.set(key, result, 3600)
    return result


def search_igdb_company(query):
    key = f"col_search_igdb_company_{query}"
    cached = cache.get(key)
    if cached:
        return cached
    try:
        data = _igdb_post("companies",
                          f'search "{query}"; fields name,slug; limit 10;')
    except Exception as e:
        logger.warning("IGDB company search: %s", e)
        return []
    results = [{"id": str(r["id"]), "name": r.get("name", ""),
                "overview": "", "image": settings.IMG_NONE}
               for r in data]
    cache.set(key, results, 300)
    return results


def fetch_igdb_company(source_id):
    key = f"col_fetch_igdb_company_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached
    try:
        data = _igdb_post("companies",
                          f"fields name,slug,description,logo.image_id,developed.name,developed.cover.image_id,developed.first_release_date; where id = {source_id};")
    except Exception as e:
        logger.warning("IGDB company fetch: %s", e)
        return {"name": "", "overview": "", "image": settings.IMG_NONE, "items": []}

    company = data[0] if data else {}
    logo = company.get("logo") or {}
    img = f"https://images.igdb.com/igdb/image/upload/t_logo_med/{logo['image_id']}.png" if logo.get("image_id") else settings.IMG_NONE

    games = sorted(company.get("developed", []), key=lambda g: g.get("first_release_date") or 0, reverse=True)
    items = []
    for g in games:
        cover = g.get("cover") or {}
        gimg = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{cover['image_id']}.jpg" if cover.get("image_id") else settings.IMG_NONE
        items.append({"media_id": str(g["id"]), "source": Sources.IGDB.value,
                      "media_type": MediaTypes.GAME.value,
                      "title": g.get("name", ""), "image": gimg})

    result = {
        "name": company.get("name", ""),
        "overview": company.get("description", ""),
        "image": img,
        "source_url": f"https://www.igdb.com/companies/{company.get('slug', source_id)}",
        "items": items[:80],
    }
    cache.set(key, result, 3600)
    return result


# ── ComicVine: story arc ───────────────────────────────────────────────────────

def _cv_params(**extra):
    p = {"api_key": settings.COMICVINE_API, "format": "json"}
    p.update(extra)
    return p


def search_comicvine_story_arc(query):
    key = f"col_search_cv_arc_{query}"
    cached = cache.get(key)
    if cached:
        return cached
    data = _get("https://comicvine.gamespot.com/api/search/",
                params=_cv_params(query=query, resources="story_arc",
                                  field_list="id,name,deck,image", limit=10))
    results = [{"id": str(r["id"]), "name": r.get("name", ""),
                "overview": r.get("deck", ""),
                "image": (r.get("image") or {}).get("medium_url", settings.IMG_NONE)}
               for r in data.get("results", [])]
    cache.set(key, results, 300)
    return results


def fetch_comicvine_story_arc(source_id):
    key = f"col_fetch_cv_arc_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached
    data = _get(f"https://comicvine.gamespot.com/api/story_arc/4045-{source_id}/",
                params=_cv_params(field_list="name,deck,description,image,issues"))
    r = data.get("results", {})
    items = []
    for issue in r.get("issues", [])[:80]:
        items.append({
            "media_id": str(issue["id"]).replace("4000-", ""),
            "source": Sources.COMICVINE.value,
            "media_type": MediaTypes.COMIC.value,
            "title": issue.get("name", f"Issue {issue.get('id')}"),
            "image": settings.IMG_NONE,
        })
    result = {
        "name": r.get("name", ""),
        "overview": r.get("deck", ""),
        "image": (r.get("image") or {}).get("medium_url", settings.IMG_NONE),
        "source_url": f"https://comicvine.gamespot.com/story-arc/4045-{source_id}/",
        "items": items,
    }
    cache.set(key, result, 3600)
    return result


def search_comicvine_publisher(query):
    key = f"col_search_cv_pub_{query}"
    cached = cache.get(key)
    if cached:
        return cached
    data = _get("https://comicvine.gamespot.com/api/search/",
                params=_cv_params(query=query, resources="publisher",
                                  field_list="id,name,deck,image", limit=10))
    results = [{"id": str(r["id"]), "name": r.get("name", ""),
                "overview": r.get("deck", ""),
                "image": (r.get("image") or {}).get("medium_url", settings.IMG_NONE)}
               for r in data.get("results", [])]
    cache.set(key, results, 300)
    return results


def fetch_comicvine_publisher(source_id):
    key = f"col_fetch_cv_pub_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached
    data = _get(f"https://comicvine.gamespot.com/api/publisher/4010-{source_id}/",
                params=_cv_params(field_list="name,deck,image,volumes"))
    r = data.get("results", {})
    # volumes are the comic series; we take up to 80
    items = [{"media_id": str(v["id"]).replace("4050-", ""),
              "source": Sources.COMICVINE.value,
              "media_type": MediaTypes.COMIC.value,
              "title": v.get("name", ""), "image": settings.IMG_NONE}
             for v in (r.get("volumes") or [])[:80]]
    result = {
        "name": r.get("name", ""),
        "overview": r.get("deck", ""),
        "image": (r.get("image") or {}).get("medium_url", settings.IMG_NONE),
        "source_url": f"https://comicvine.gamespot.com/publisher/4010-{source_id}/",
        "items": items,
    }
    cache.set(key, result, 3600)
    return result


def search_comicvine_character(query):
    key = f"col_search_cv_char_{query}"
    cached = cache.get(key)
    if cached:
        return cached
    data = _get("https://comicvine.gamespot.com/api/search/",
                params=_cv_params(query=query, resources="character",
                                  field_list="id,name,deck,image", limit=10))
    results = [{"id": str(r["id"]).replace("4005-", ""), "name": r.get("name", ""),
                "overview": r.get("deck", ""),
                "image": (r.get("image") or {}).get("medium_url", settings.IMG_NONE)}
               for r in data.get("results", [])]
    cache.set(key, results, 300)
    return results


def fetch_comicvine_character(source_id):
    key = f"col_fetch_cv_char_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached
    data = _get(f"https://comicvine.gamespot.com/api/character/4005-{source_id}/",
                params=_cv_params(field_list="name,deck,image,volume_credits"))
    r = data.get("results", {})
    items = [{"media_id": str(v["id"]).replace("4050-", ""),
              "source": Sources.COMICVINE.value,
              "media_type": MediaTypes.COMIC.value,
              "title": v.get("name", ""), "image": settings.IMG_NONE}
             for v in (r.get("volume_credits") or [])[:80]]
    result = {
        "name": r.get("name", ""),
        "overview": r.get("deck", ""),
        "image": (r.get("image") or {}).get("medium_url", settings.IMG_NONE),
        "source_url": f"https://comicvine.gamespot.com/character/4005-{source_id}/",
        "items": items,
    }
    cache.set(key, result, 3600)
    return result


# ── BGG: boardgame family ─────────────────────────────────────────────────────

import xml.etree.ElementTree as ET


def search_bgg_family(query):
    key = f"col_search_bgg_family_{query}"
    cached = cache.get(key)
    if cached:
        return cached
    resp = requests.get("https://boardgamegeek.com/xmlapi2/search",
                        params={"query": query, "type": "boardgamefamily"}, timeout=10)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    results = []
    for item in root.findall("item")[:10]:
        name_el = item.find("name")
        results.append({
            "id": item.get("id", ""),
            "name": name_el.get("value", "") if name_el is not None else "",
            "overview": "", "image": settings.IMG_NONE,
        })
    cache.set(key, results, 300)
    return results


def fetch_bgg_family(source_id):
    key = f"col_fetch_bgg_family_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached

    resp = requests.get("https://boardgamegeek.com/xmlapi2/family",
                        params={"id": source_id, "type": "boardgamefamily"}, timeout=10)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    item_el = root.find("item")
    if item_el is None:
        return {"name": "", "overview": "", "image": settings.IMG_NONE, "items": []}

    name_el = item_el.find("name[@type='primary']")
    name = name_el.get("value", "") if name_el is not None else ""
    desc_el = item_el.find("description")
    desc = desc_el.text or "" if desc_el is not None else ""
    img_el = item_el.find("thumbnail")
    img = img_el.text or settings.IMG_NONE if img_el is not None else settings.IMG_NONE

    # Get game IDs from links
    game_ids = [l.get("id") for l in item_el.findall("link[@type='boardgamefamily']")
                if l.get("id")]
    # Also grab direct inbound links
    game_ids += [l.get("id") for l in item_el.findall("link")
                 if l.get("type") == "boardgame" and l.get("id")]
    game_ids = list(dict.fromkeys(game_ids))[:50]

    # Fetch game details in batch
    items = []
    if game_ids:
        chunk = ",".join(game_ids[:20])
        try:
            gresp = requests.get("https://boardgamegeek.com/xmlapi2/thing",
                                 params={"id": chunk, "type": "boardgame"}, timeout=15)
            gresp.raise_for_status()
            groot = ET.fromstring(gresp.text)
            for gel in groot.findall("item"):
                gname = gel.find("name[@type='primary']")
                gthumb = gel.find("thumbnail")
                items.append({
                    "media_id": gel.get("id", ""),
                    "source": Sources.BGG.value,
                    "media_type": MediaTypes.BOARDGAME.value,
                    "title": gname.get("value", "") if gname is not None else "",
                    "image": (gthumb.text or settings.IMG_NONE) if gthumb is not None else settings.IMG_NONE,
                })
        except Exception as e:
            logger.warning("BGG family game fetch: %s", e)

    result = {
        "name": name, "overview": desc, "image": img,
        "source_url": f"https://boardgamegeek.com/boardgamefamily/{source_id}",
        "items": items,
    }
    cache.set(key, result, 3600)
    return result


# ── MusicBrainz: artist discography ───────────────────────────────────────────

def search_musicbrainz_artist(query):
    key = f"col_search_mb_artist_{query}"
    cached = cache.get(key)
    if cached:
        return cached
    time.sleep(1)
    data = _get("https://musicbrainz.org/ws/2/artist",
                params={"query": query, "limit": 10, "fmt": "json"},
                headers=_mb_headers())
    results = [{"id": a["id"], "name": a.get("name", ""),
                "overview": (a.get("disambiguation") or ""),
                "image": settings.IMG_NONE}
               for a in data.get("artists", [])]
    cache.set(key, results, 300)
    return results


def fetch_musicbrainz_artist(source_id):
    key = f"col_fetch_mb_artist_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached

    time.sleep(1)
    data = _get(f"https://musicbrainz.org/ws/2/release-group",
                params={"artist": source_id, "limit": 100, "fmt": "json",
                        "type": "album|ep|single"},
                headers=_mb_headers())

    artist_data = _get(f"https://musicbrainz.org/ws/2/artist/{source_id}",
                       params={"fmt": "json"}, headers=_mb_headers())

    items = []
    for rg in data.get("release-groups", []):
        items.append({
            "media_id": rg["id"],
            "source": Sources.MUSICBRAINZ.value,
            "media_type": MediaTypes.MUSIC.value,
            "title": rg.get("title", ""),
            "image": f"https://coverartarchive.org/release-group/{rg['id']}/front-250",
        })

    result = {
        "name": artist_data.get("name", ""),
        "overview": artist_data.get("disambiguation", ""),
        "image": settings.IMG_NONE,
        "source_url": f"https://musicbrainz.org/artist/{source_id}",
        "items": items,
    }
    cache.set(key, result, 3600)
    return result


def search_musicbrainz_label(query):
    key = f"col_search_mb_label_{query}"
    cached = cache.get(key)
    if cached:
        return cached
    time.sleep(1)
    data = _get("https://musicbrainz.org/ws/2/label",
                params={"query": query, "limit": 10, "fmt": "json"},
                headers=_mb_headers())
    results = [{"id": l["id"], "name": l.get("name", ""),
                "overview": (l.get("disambiguation") or ""),
                "image": settings.IMG_NONE}
               for l in data.get("labels", [])]
    cache.set(key, results, 300)
    return results


def fetch_musicbrainz_label(source_id):
    key = f"col_fetch_mb_label_{source_id}"
    cached = cache.get(key)
    if cached:
        return cached

    time.sleep(1)
    label = _get(f"https://musicbrainz.org/ws/2/label/{source_id}",
                 params={"fmt": "json"}, headers=_mb_headers())
    time.sleep(1)
    releases = _get("https://musicbrainz.org/ws/2/release-group",
                    params={"label": source_id, "limit": 100, "fmt": "json"},
                    headers=_mb_headers())

    items = [{"media_id": rg["id"], "source": Sources.MUSICBRAINZ.value,
              "media_type": MediaTypes.MUSIC.value,
              "title": rg.get("title", ""),
              "image": f"https://coverartarchive.org/release-group/{rg['id']}/front-250"}
             for rg in releases.get("release-groups", [])]

    result = {
        "name": label.get("name", ""),
        "overview": label.get("disambiguation", ""),
        "image": settings.IMG_NONE,
        "source_url": f"https://musicbrainz.org/label/{source_id}",
        "items": items,
    }
    cache.set(key, result, 3600)
    return result


# ── Dispatcher ────────────────────────────────────────────────────────────────

SOURCES = {
    "tmdb_collection":        ("TMDB Movie Collection",    search_tmdb_collection,      fetch_tmdb_collection),
    "tmdb_person":            ("TMDB Person / Director",   search_tmdb_person,          fetch_tmdb_person),
    "mal_anime_franchise":    ("MAL Anime Franchise",      search_mal_anime,            fetch_mal_anime_franchise),
    "mal_manga_franchise":    ("MAL Manga Franchise",      search_mal_manga,            fetch_mal_manga_franchise),
    "hardcover_series":       ("Hardcover Book Series",    search_hardcover_series,     fetch_hardcover_series),
    "openlibrary_author":     ("OpenLibrary Author",       search_openlibrary_author,   fetch_openlibrary_author),
    "igdb_franchise":         ("IGDB Game Franchise",      search_igdb_franchise,       fetch_igdb_franchise),
    "igdb_collection":        ("IGDB Game Series",         search_igdb_collection,      fetch_igdb_collection),
    "igdb_company":           ("IGDB Game Company",        search_igdb_company,         fetch_igdb_company),
    "comicvine_story_arc":    ("ComicVine Story Arc",      search_comicvine_story_arc,  fetch_comicvine_story_arc),
    "comicvine_publisher":    ("ComicVine Publisher",      search_comicvine_publisher,  fetch_comicvine_publisher),
    "comicvine_character":    ("ComicVine Character",      search_comicvine_character,  fetch_comicvine_character),
    "bgg_family":             ("BoardGameGeek Family",     search_bgg_family,           fetch_bgg_family),
    "musicbrainz_artist":     ("MusicBrainz Artist",       search_musicbrainz_artist,   fetch_musicbrainz_artist),
    "musicbrainz_label":      ("MusicBrainz Label",        search_musicbrainz_label,    fetch_musicbrainz_label),
    "manual":                 ("Manual",                   None,                        None),
}


def get_source_label(source_key):
    return SOURCES.get(source_key, ("Unknown", None, None))[0]


def search(source_key, query):
    entry = SOURCES.get(source_key)
    if not entry or entry[1] is None:
        return []
    return entry[1](query)


def fetch(source_key, source_id):
    entry = SOURCES.get(source_key)
    if not entry or entry[2] is None:
        return None
    return entry[2](source_id)


SOURCE_CHOICES = [(k, v[0]) for k, v in SOURCES.items()]
''')

# ─────────────────────────────────────────────────────────────
# 2. Update Collection model — replace old SOURCE_* with dynamic choices
# ─────────────────────────────────────────────────────────────
print("\n[2] collections/models.py — dynamic source choices")
patch(
    COL / "models.py",
    old='''\
    SOURCE_TMDB = "tmdb"
    SOURCE_MANUAL = "manual"
    SOURCE_CHOICES = [
        (SOURCE_TMDB, "The Movie Database"),
        (SOURCE_MANUAL, "Manual"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default=SOURCE_MANUAL)
    source_id = models.CharField(max_length=50, blank=True, default="")''',
    new='''\
    SOURCE_MANUAL = "manual"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    source = models.CharField(max_length=50, default=SOURCE_MANUAL)
    source_id = models.CharField(max_length=100, blank=True, default="")''',
    label="models.py — flexible source field",
)

patch(
    COL / "models.py",
    old='    @property\n    def source_url(self):\n        if self.source == self.SOURCE_TMDB and self.source_id:\n            return f"https://www.themoviedb.org/collection/{self.source_id}"\n        return None\n\n    @property\n    def is_tmdb(self):\n        return self.source == self.SOURCE_TMDB',
    new='''\
    @property
    def source_url(self):
        from app.providers.collections_providers import fetch
        if self.source != self.SOURCE_MANUAL and self.source_id:
            data = fetch(self.source, self.source_id)
            if data:
                return data.get("source_url")
        return None

    @property
    def is_sourced(self):
        return self.source != self.SOURCE_MANUAL and bool(self.source_id)

    @property
    def source_label(self):
        from app.providers.collections_providers import get_source_label
        return get_source_label(self.source)''',
    label="models.py — source_url + is_sourced + source_label",
)

# ─────────────────────────────────────────────────────────────
# 3. Migration for wider source field
# ─────────────────────────────────────────────────────────────
print("\n[3] collections/migrations/0003_collection_source_widened.py")
write(COL / "migrations" / "0003_collection_source_widened.py", '''\
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("collections", "0002_collection_source"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="source",
            field=models.CharField(default="manual", max_length=50),
        ),
        migrations.AlterField(
            model_name="collection",
            name="source_id",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
    ]
''')

# ─────────────────────────────────────────────────────────────
# 4. Update collections/views.py — use dispatcher + generic search endpoint
# ─────────────────────────────────────────────────────────────
print("\n[4] collections/views.py — generic source search + create")
# Patch the search endpoint and create to use the dispatcher
patch(
    COL / "views.py",
    old='from app.providers import services, tmdb as tmdb_provider',
    new='from app.providers import services\nfrom app.providers import collections_providers as col_providers',
    label="views.py — import collections_providers",
)

patch(
    COL / "views.py",
    old='''\
@require_GET
def search_tmdb_collections(request):
    """HTMX endpoint: search TMDB for collections by name."""
    query = request.GET.get("q", "").strip()
    if len(query) < 2:
        return render(request, "collections/components/tmdb_search_results.html", {"results": []})
    data = tmdb_provider.search_collection(query)
    return render(request, "collections/components/tmdb_search_results.html", {
        "results": data["results"],
    })''',
    new='''\
@require_GET
def search_source(request):
    """HTMX endpoint: search any source for collections."""
    source_key = request.GET.get("source_key", "").strip()
    query = request.GET.get("q", "").strip()
    if len(query) < 2 or not source_key:
        return render(request, "collections/components/source_search_results.html",
                      {"results": [], "source_key": source_key})
    results = col_providers.search(source_key, query)
    return render(request, "collections/components/source_search_results.html", {
        "results": results, "source_key": source_key,
    })''',
    label="views.py — generic search_source endpoint",
)

patch(
    COL / "views.py",
    old='''\
@require_POST
def create(request):
    source = request.POST.get("source", Collection.SOURCE_MANUAL)
    source_id = request.POST.get("source_id", "").strip()

    if source == Collection.SOURCE_TMDB and source_id:
        # Auto-populate from TMDB
        try:
            tmdb_data = tmdb_provider.fetch_collection_data(source_id)
        except Exception as e:
            messages.error(request, f"Could not fetch TMDB collection: {e}")
            return helpers.redirect_back(request)

        col = Collection.objects.create(
            name=request.POST.get("name") or tmdb_data["name"],
            description=request.POST.get("description") or tmdb_data["overview"],
            source=Collection.SOURCE_TMDB,
            source_id=source_id,
            owner=request.user,
        )
        _sync_tmdb_items(col, tmdb_data)
        logger.info("Created TMDB collection %s with %d items.", col, len(tmdb_data["parts"]))
    else:
        form = CollectionForm(request.POST)
        if form.is_valid():
            col = form.save(commit=False)
            col.owner = request.user
            col.source = Collection.SOURCE_MANUAL
            col.save()
            form.save_m2m()
        else:
            helpers.form_error_messages(form, request)
            return helpers.redirect_back(request)

    return redirect("collection_detail", collection_id=col.id)''',
    new='''\
@require_POST
def create(request):
    source = request.POST.get("source", Collection.SOURCE_MANUAL)
    source_id = request.POST.get("source_id", "").strip()

    if source != Collection.SOURCE_MANUAL and source_id:
        try:
            data = col_providers.fetch(source, source_id)
        except Exception as e:
            messages.error(request, f"Could not fetch collection data: {e}")
            return helpers.redirect_back(request)
        if not data:
            messages.error(request, "No data returned for that source.")
            return helpers.redirect_back(request)

        col = Collection.objects.create(
            name=request.POST.get("name") or data["name"],
            description=request.POST.get("description") or data.get("overview", ""),
            source=source,
            source_id=source_id,
            owner=request.user,
        )
        added = _sync_source_items(col, data)
        logger.info("Created %s collection %s with %d items.", source, col, added)
    else:
        form = CollectionForm(request.POST)
        if form.is_valid():
            col = form.save(commit=False)
            col.owner = request.user
            col.source = Collection.SOURCE_MANUAL
            col.save()
            form.save_m2m()
        else:
            helpers.form_error_messages(form, request)
            return helpers.redirect_back(request)

    return redirect("collection_detail", collection_id=col.id)''',
    label="views.py — generic create from any source",
)

patch(
    COL / "views.py",
    old='''\
@require_POST
def sync_from_tmdb(request, collection_id):
    """Re-fetch items from TMDB for a TMDB-sourced collection."""
    col = get_object_or_404(Collection, id=collection_id)
    if not col.is_tmdb or not col.source_id:
        messages.error(request, "This collection is not linked to TMDB.")
        return helpers.redirect_back(request)
    if not col.user_can_edit(request.user):
        raise Http404
    try:
        tmdb_data = tmdb_provider.fetch_collection_data(col.source_id)
        added = _sync_tmdb_items(col, tmdb_data)
        messages.success(request, f"Synced from TMDB — {added} new item(s) added.")
    except Exception as e:
        messages.error(request, f"Sync failed: {e}")
    return helpers.redirect_back(request)


def _sync_tmdb_items(col: Collection, tmdb_data: dict) -> int:
    """Add any missing TMDB movie parts to a collection. Returns count added."""
    added = 0
    for part in tmdb_data["parts"]:
        item, _ = Item.objects.get_or_create(
            media_id=part["media_id"],
            source=part["source"],
            media_type=part["media_type"],
            season_number=None,
            episode_number=None,
            defaults={"title": part["title"], "image": part["image"], "country": ""},
        )
        _, created = CollectionItem.objects.get_or_create(
            collection=col, item=item,
        )
        if created:
            added += 1
    return added''',
    new='''\
@require_POST
def sync_from_source(request, collection_id):
    """Re-fetch items from the external source for a sourced collection."""
    col = get_object_or_404(Collection, id=collection_id)
    if not col.is_sourced:
        messages.error(request, "This collection has no external source.")
        return helpers.redirect_back(request)
    if not col.user_can_edit(request.user):
        raise Http404
    try:
        data = col_providers.fetch(col.source, col.source_id)
        added = _sync_source_items(col, data)
        messages.success(request, f"Synced — {added} new item(s) added.")
    except Exception as e:
        messages.error(request, f"Sync failed: {e}")
    return helpers.redirect_back(request)


def _sync_source_items(col: Collection, data: dict) -> int:
    """Add any missing items from fetched source data. Returns count added."""
    added = 0
    for part in data.get("items", []):
        item, _ = Item.objects.get_or_create(
            media_id=part["media_id"],
            source=part["source"],
            media_type=part["media_type"],
            season_number=None,
            defaults={"title": part["title"], "image": part["image"], "country": ""},
        )
        _, created = CollectionItem.objects.get_or_create(collection=col, item=item)
        if created:
            added += 1
    return added''',
    label="views.py — generic sync_from_source",
)

# ─────────────────────────────────────────────────────────────
# 5. Update URLs
# ─────────────────────────────────────────────────────────────
print("\n[5] collections/urls.py")
write(COL / "urls.py", '''\
from django.urls import path
from collections import views

urlpatterns = [
    path("collections", views.collections, name="collections"),
    path("collection/<int:collection_id>", views.collection_detail, name="collection_detail"),
    path("collection/create", views.create, name="collection_create"),
    path("collection/edit", views.edit, name="collection_edit"),
    path("collection/delete", views.delete, name="collection_delete"),
    path("collection/<int:collection_id>/sync", views.sync_from_source, name="collection_sync"),
    path("collection/search_source", views.search_source, name="collection_search_source"),
    path("collection_item_toggle", views.collection_item_toggle, name="collection_item_toggle"),
    path("collections_modal/<str:source>/<str:media_type>/<str:media_id>",
         views.collections_modal, name="collections_modal"),
    path("collections_modal/<str:source>/<str:media_type>/<str:media_id>/<int:season_number>",
         views.collections_modal, name="collections_modal"),
]
''')

# ─────────────────────────────────────────────────────────────
# 6. Source search results partial
# ─────────────────────────────────────────────────────────────
print("\n[6] templates — source_search_results.html")
TMPL = SRC / "templates" / "collections"
write(TMPL / "components" / "source_search_results.html", '''\
{% if results %}
  <div class="mt-2 bg-[#1e2227] rounded-lg border border-gray-700 overflow-hidden max-h-64 overflow-y-auto">
    {% for r in results %}
      <button type="button"
              class="w-full flex items-center gap-3 px-4 py-3 hover:bg-[#2a2f35] transition-colors cursor-pointer text-left border-b border-gray-800 last:border-0"
              @click="selectSource('{{ r.id }}', '{{ r.name|escapejs }}', '{{ r.overview|default:''|escapejs|truncatechars:120 }}')">
        <img src="{{ r.image }}" alt="{{ r.name }}"
             class="w-10 h-14 object-cover rounded flex-shrink-0 bg-[#39404b]"
             onerror="this.src=''">
        <div class="min-w-0">
          <p class="font-medium text-white text-sm truncate">{{ r.name }}</p>
          {% if r.overview %}
            <p class="text-gray-400 text-xs mt-0.5 line-clamp-2">{{ r.overview }}</p>
          {% endif %}
        </div>
      </button>
    {% endfor %}
  </div>
{% elif request.GET.q %}
  <p class="text-sm text-gray-500 mt-2 px-1">No results found for "{{ request.GET.q }}".</p>
{% endif %}
''')

# ─────────────────────────────────────────────────────────────
# 7. Rewrite collection_form.html — source picker with all 15 sources
# ─────────────────────────────────────────────────────────────
print("\n[7] templates — collection_form.html with full source picker")
write(TMPL / "components" / "collection_form.html", '''\
{% load app_tags %}
<div x-show="showModal"
     x-cloak
     class="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
     @click.self="showModal = false"
     x-data="{
       source: '{% if collection %}{{ collection.source }}{% else %}manual{% endif %}',
       sourceId: '{{ collection.source_id|default:'' }}',
       selectedName: '{{ collection.name|escapejs }}',
       selectSource(id, name, desc) {
         this.sourceId = id;
         this.selectedName = name;
         document.getElementById('col-name-input').value = name;
         document.getElementById('col-desc-input').value = desc;
         document.getElementById('source-search-results').innerHTML = '';
         document.getElementById('source-search-input').value = name;
       }
     }">
  <div class="bg-[#1e2227] rounded-xl shadow-xl w-full max-w-lg mx-4 p-6 max-h-[90vh] overflow-y-auto">
    <h2 class="text-lg font-semibold mb-5">
      {% if collection %}Edit Collection{% else %}New Collection{% endif %}
    </h2>

    <form method="post"
          action="{% if collection %}{% url 'collection_edit' %}{% else %}{% url 'collection_create' %}{% endif %}">
      {% csrf_token %}
      {% if collection %}<input type="hidden" name="collection_id" value="{{ collection.id }}">{% endif %}
      <input type="hidden" name="next" value="{{ request.path }}">
      <input type="hidden" name="source" :value="source">
      <input type="hidden" name="source_id" :value="sourceId">

      {% if not collection %}
      {# Source selector #}
      <div class="mb-5">
        <label class="block text-sm text-gray-400 mb-2">Source</label>
        <div class="grid grid-cols-2 gap-1.5 max-h-52 overflow-y-auto pr-1">
          {% for key, label in source_choices %}
          <button type="button"
                  @click="source = '{{ key }}'; sourceId = ''; selectedName = ''"
                  :class="source === '{{ key }}' ? 'bg-indigo-600 text-white border-indigo-500' : 'bg-[#2a2f35] text-gray-300 hover:bg-[#39404b] border-gray-700'"
                  class="px-3 py-2 rounded-md text-xs font-medium transition-colors cursor-pointer border text-left">
            {{ label }}
          </button>
          {% endfor %}
        </div>
      </div>

      {# Search box — hidden for manual #}
      <div x-show="source !== 'manual'" class="mb-4">
        <label class="block text-sm text-gray-400 mb-1">Search</label>
        <input id="source-search-input"
               type="search"
               placeholder="Search..."
               class="w-full px-3 py-2 bg-[#2a2f35] rounded-md text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
               hx-get="{% url 'collection_search_source' %}"
               hx-trigger="keyup changed delay:400ms"
               hx-target="#source-search-results"
               hx-include="[name='source']"
               name="q">
        {# Pass current source to the search endpoint #}
        <input type="hidden" name="source_key" :value="source">
        <div id="source-search-results"></div>
        <p x-show="sourceId" class="mt-1.5 text-xs text-indigo-400">
          ✓ <span x-text="selectedName"></span>
        </p>
      </div>
      {% endif %}

      {# Name #}
      <div class="mb-4">
        <label class="block text-sm text-gray-400 mb-1">Name</label>
        <input id="col-name-input" type="text" name="name"
               value="{{ collection.name|default:'' }}"
               placeholder="e.g. Game of Thrones Universe"
               class="w-full px-3 py-2 bg-[#2a2f35] rounded-md text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
      </div>

      {# Description #}
      <div class="mb-4">
        <label class="block text-sm text-gray-400 mb-1">
          Description <span class="text-gray-600">(optional)</span>
        </label>
        <textarea id="col-desc-input" name="description" rows="3"
                  placeholder="What is this collection about?"
                  class="w-full px-3 py-2 bg-[#2a2f35] rounded-md text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none">{{ collection.description|default:'' }}</textarea>
      </div>

      <div class="flex justify-end gap-3 mt-6">
        <button type="button" @click="showModal = false"
                class="px-4 py-2 rounded-md bg-[#39404b] hover:bg-[#454d5a] text-sm transition-colors cursor-pointer">
          Cancel
        </button>
        <button type="submit"
                :disabled="source !== 'manual' && !sourceId && !{{ collection.id|default:0 }}"
                class="px-4 py-2 rounded-md bg-indigo-600 hover:bg-indigo-700 text-sm font-medium transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed">
          {% if collection %}Save{% else %}Create{% endif %}
        </button>
      </div>
    </form>

    {% if collection and collection.user_can_delete(request.user) %}
    <form method="post" action="{% url 'collection_delete' %}" class="mt-3 text-right">
      {% csrf_token %}
      <input type="hidden" name="collection_id" value="{{ collection.id }}">
      <input type="hidden" name="next" value="{% url 'collections' %}">
      <button type="submit" onclick="return confirm(\'Delete this collection?\')"
              class="text-red-400 hover:text-red-300 text-xs transition-colors cursor-pointer">
        Delete collection
      </button>
    </form>
    {% endif %}
  </div>
</div>
''')

# ─────────────────────────────────────────────────────────────
# 8. Pass source_choices to both collection views
# ─────────────────────────────────────────────────────────────
print("\n[8] views.py — pass source_choices to templates")
patch(
    COL / "views.py",
    old='    form = CollectionForm()\n    return render(request, "collections/collections.html", {\n        "collections": user_collections,\n        "form": form,\n    })',
    new='    form = CollectionForm()\n    return render(request, "collections/collections.html", {\n        "collections": user_collections,\n        "form": form,\n        "source_choices": col_providers.SOURCE_CHOICES,\n    })',
    label="views.py — source_choices in collections view",
)

patch(
    COL / "views.py",
    old='    return render(request, "collections/collection_detail.html", {\n        "collection": collection,\n        "collection_items": items_qs,\n        "stats": stats,\n        "form": form,\n        "media_type_filter": media_type_filter,\n        "media_types": MediaTypes.values,\n    })',
    new='    return render(request, "collections/collection_detail.html", {\n        "collection": collection,\n        "collection_items": items_qs,\n        "stats": stats,\n        "form": form,\n        "media_type_filter": media_type_filter,\n        "media_types": MediaTypes.values,\n        "source_choices": col_providers.SOURCE_CHOICES,\n    })',
    label="views.py — source_choices in collection_detail view",
)

# ─────────────────────────────────────────────────────────────
# 9. Update collection_detail.html — is_tmdb → is_sourced, sync URL
# ─────────────────────────────────────────────────────────────
print("\n[9] collection_detail.html — is_tmdb → is_sourced")
detail = TMPL / "collection_detail.html"
text = detail.read_text(encoding="utf-8")
text = text.replace("collection.is_tmdb", "collection.is_sourced")
text = text.replace("{% url 'collection_sync' collection.id %}", "{% url 'collection_sync' collection.id %}")
text = text.replace("Sync TMDB", "Sync Source")
text = text.replace(
    '{% if collection.is_sourced %}\n          <a href="{{ collection.source_url }}" target="_blank" rel="noopener"\n             class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-blue-600/20 text-blue-400 border border-blue-500/30 rounded-full text-xs font-medium hover:bg-blue-600/30 transition-colors">\n            <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/></svg>\n            TMDB Collection\n          </a>',
    '{% if collection.is_sourced %}\n          <a href="{{ collection.source_url }}" target="_blank" rel="noopener"\n             class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-blue-600/20 text-blue-400 border border-blue-500/30 rounded-full text-xs font-medium hover:bg-blue-600/30 transition-colors">\n            <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/></svg>\n            {{ collection.source_label }}\n          </a>',
)
detail.write_text(text, encoding="utf-8")
print("  OK   collection_detail.html — source_label badge")

# ─────────────────────────────────────────────────────────────
# 10. Fix URL name: collection_search_tmdb → collection_search_source in old template
# ─────────────────────────────────────────────────────────────
print("\n[10] templates — fix old tmdb search URL reference")
for tmpl_file in [TMPL / "components" / "collection_form.html",
                   TMPL / "collections.html"]:
    if tmpl_file.exists():
        t = tmpl_file.read_text(encoding="utf-8")
        if "collection_search_tmdb" in t:
            tmpl_file.write_text(t.replace("collection_search_tmdb", "collection_search_source"), encoding="utf-8")
            print(f"  OK   {tmpl_file.name} — URL updated")

print()
print("=" * 60)
print("Done. Commit and rebuild:")
print()
print("  git add src/app/providers/collections_providers.py")
print("  git add src/collections/")
print("  git add src/templates/collections/")
print("  git commit -m 'feat: Collection sources — 15 source types across all media'")
print("  docker compose down; docker compose up -d --build")
