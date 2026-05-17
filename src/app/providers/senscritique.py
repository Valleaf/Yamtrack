"""
SensCritique GraphQL API provider for Yamtrack.
Handles music (albums) and acts as metadata source for SC-imported items.

SC GraphQL endpoint: https://gql.senscritique.com/graphql
Auth: Firebase email/password → ID token → Bearer header
"""

import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

SC_GQL_URL = "https://gql.senscritique.com/graphql"
# SC's Firebase API key - configurable via SC_FIREBASE_API_KEY env var
_DEFAULT_FIREBASE_KEY = "AIzaSyCjLSEDd8GVE0HEnAMvSHHBMfy8uF0GRAL"


def _get_firebase_api_key() -> str:
    import os
    return os.environ.get("SC_FIREBASE_API_KEY", _DEFAULT_FIREBASE_KEY)


def _get_firebase_auth_url() -> str:
    return (
        "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
        f"?key={_get_firebase_api_key()}"
    )

# SC category slugs → Yamtrack media types
SC_CATEGORY_MAP = {
    "film": "movie",
    "serie": "tv",
    "jeu": "game",
    "livre": "book",
    "bd": "comic",
    "album": "music",
    "anime": "anime",
    "podcast": None,  # not supported
}


def _get_firebase_token(email: str, password: str) -> str:
    """Authenticate with Firebase and return the ID token."""
    resp = requests.post(
        _get_firebase_auth_url(),
        json={"email": email, "password": password, "returnSecureToken": True},
        timeout=10,
    )
    if not resp.ok:
        logger.error("Firebase auth failed: %s %s", resp.status_code, resp.text[:500])
        resp.raise_for_status()
    data = resp.json()
    if "idToken" not in data:
        raise ValueError(f"Firebase auth response missing idToken: {data}")
    return data["idToken"]


def _gql(query: str, variables: dict, token: str | None = None) -> dict:
    """Execute a GraphQL query against the SC API."""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    resp = requests.post(
        SC_GQL_URL,
        json={"query": query, "variables": variables},
        headers=headers,
        timeout=15,
    )
    if not resp.ok:
        logger.error("SC GQL failed: %s %s", resp.status_code, resp.text[:300])
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise ValueError(f"SC GraphQL error: {data['errors']}")
    return data["data"]


# ---------------------------------------------------------------------------
# Public collection fetch (no auth needed for public profiles)
# ---------------------------------------------------------------------------

USER_COLLECTION_QUERY = """
query UserCollection($username: String!, $categoryId: Int, $limit: Int, $offset: Int) {
  userByUsername(username: $username) {
    collection(categoryId: $categoryId, limit: $limit, offset: $offset) {
      products {
        id
        title
        originalTitle
        yearOfProduction
        poster
        category {
          label
        }
        rating
        userRating {
          score
        }
        artists {
          name
        }
      }
      totalCount
    }
  }
}
"""

# SC category IDs
SC_CATEGORY_IDS = {
    "movie": 1,
    "tv": 2,
    "game": 3,
    "book": 4,
    "comic": 5,
    "music": 6,
    "anime": 7,
}


def get_user_collection(
    username: str,
    media_type: str | None = None,
    token: str | None = None,
) -> list[dict]:
    """
    Fetch all items from a SC user's collection.
    media_type: one of SC_CATEGORY_IDS keys, or None for all.
    Returns list of normalized dicts ready for Yamtrack ingestion.
    """
    category_id = SC_CATEGORY_IDS.get(media_type) if media_type else None
    limit = 100
    offset = 0
    all_products = []

    while True:
        data = _gql(
            USER_COLLECTION_QUERY,
            {
                "username": username,
                "categoryId": category_id,
                "limit": limit,
                "offset": offset,
            },
            token=token,
        )
        user = data.get("userByUsername")
        if not user or not user.get("collection"):
            break

        products = user["collection"].get("products", [])
        total = user["collection"].get("totalCount", 0)
        all_products.extend(products)

        if offset + limit >= total:
            break
        offset += limit

    return [_normalize_product(p) for p in all_products]


def _normalize_product(p: dict) -> dict:
    """Map a SC product to a Yamtrack-compatible dict."""
    category_label = (p.get("category") or {}).get("label", "").lower()
    media_type = SC_CATEGORY_MAP.get(category_label)

    score = None
    if p.get("userRating") and p["userRating"].get("score") is not None:
        # SC scores 1–10, Yamtrack stores 0–10 as integer *10
        score = int(p["userRating"]["score"])

    artists = [a["name"] for a in (p.get("artists") or []) if a.get("name")]

    return {
        "sc_id": str(p["id"]),
        "title": p.get("title") or p.get("originalTitle", ""),
        "year": p.get("yearOfProduction"),
        "poster": p.get("poster"),
        "media_type": media_type,
        "score": score,
        "artists": artists,
    }


# ---------------------------------------------------------------------------
# Music (album) metadata — used by the music provider module
# ---------------------------------------------------------------------------

ALBUM_QUERY = """
query Album($id: Int!) {
  product(id: $id) {
    id
    title
    originalTitle
    yearOfProduction
    poster
    synopsis
    genres {
      label
    }
    artists {
      name
    }
    rating
    releasedAt
  }
}
"""

SEARCH_QUERY = """
query Search($query: String!, $categoryId: Int) {
  search(query: $query, categoryId: $categoryId, limit: 10) {
    results {
      id
      title
      originalTitle
      yearOfProduction
      poster
      category {
        label
      }
      artists {
        name
      }
    }
  }
}
"""


def album(sc_id: int | str) -> dict:
    """Fetch a single album's metadata from SC. Returns Yamtrack metadata dict."""
    data = _gql(ALBUM_QUERY, {"id": int(sc_id)})
    p = data["product"]

    genres = [g["label"] for g in (p.get("genres") or [])]
    artists = [a["name"] for a in (p.get("artists") or [])]

    return {
        "media_id": str(p["id"]),
        "title": p.get("title") or p.get("originalTitle", ""),
        "source": "senscritique",
        "image": p.get("poster", ""),
        "synopsis": p.get("synopsis", ""),
        "genres": genres,
        "release_date": p.get("releasedAt") or str(p.get("yearOfProduction", "")),
        "rating": p.get("rating"),
        "artists": artists,
        "recommendations": [],  # SC doesn't expose this easily
    }


def search_music(query: str, page: int = 1) -> dict:
    """Search SC for music albums. Returns dict with pagination fields and results list."""
    # SC API doesn't support pagination, so we fetch all and return page 1
    data = _gql(SEARCH_QUERY, {"query": query, "categoryId": SC_CATEGORY_IDS["music"]})
    results = (data.get("search") or {}).get("results", [])
    
    formatted_results = [
        {
            "media_id": str(r["id"]),
            "title": r.get("title") or r.get("originalTitle", ""),
            "source": "senscritique",
            "image": r.get("poster", ""),
            "year": r.get("yearOfProduction"),
            "artists": [a["name"] for a in (r.get("artists") or [])],
        }
        for r in results
    ]
    
    total_results = len(formatted_results)
    
    return {
        "page": page,
        "total_results": total_results,
        "total_pages": 1 if total_results > 0 else 0,
        "results": formatted_results,
    }
