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
