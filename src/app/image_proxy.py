"""Lazy local cache/proxy for hot-linked cover images.

Why this exists: every provider's "image" field is a hot-linked URL to
that provider's own host -- TMDB/IGDB/MAL's media CDNs set long-lived
Cache-Control headers, so the browser caches those covers after the
first view. BnF's cover-resolution fallbacks (Open Library, Hardcover,
ComicVine -- see app.providers.bnf.resolve_cover) don't reliably do the
same, so without this, every single page view re-fetches the same cover
from scratch (visible as a ~2s placeholder-then-image flash every time).

This proxies those URLs through Yamtrack's own origin instead:
  - The public-facing URL is a short, fixed-length `/covers/<digest>`
    path (NOT the original URL itself -- Item.image is a URLField(200),
    and some upstream URLs, e.g. Hardcover's signed CDN links, are long
    enough that embedding+percent-encoding them would blow past that).
  - `digest -> original_url` and `digest -> (content_type, bytes)` are
    both stored in the normal Django cache, so they ride on the same
    durable PersistentRedisCache (Postgres-mirrored) as everything else
    in this codebase -- no new volume/storage to manage, and it
    survives a `redis-cli FLUSHALL` the same way provider metadata does.
  - The first request for a given source URL fetches and caches it; every
    response (including that first one) gets a long, immutable
    Cache-Control header, so the browser only ever fetches it once.

Only used by app.providers.bnf for now. Scoped to a small host allowlist
matching that provider's fallback chain -- extend _ALLOWED_SUFFIXES if
another provider's cover source needs the same treatment.
"""

import hashlib
import ipaddress
import logging
import socket
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.cache import cache
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET

logger = logging.getLogger(__name__)

# Hosts allowed to be proxied -- defense in depth so this endpoint can't
# be turned into an open relay. Matches the upstream hosts used by BnF's
# cover fallback chain (see app/providers/bnf.py: Open Library, Hardcover,
# ComicVine).
_ALLOWED_SUFFIXES = (
    "openlibrary.org",
    "hardcover.app",
    "gamespot.com",
    "cbsistatic.com",
)

_CACHE_TIMEOUT = 60 * 60 * 24 * 90  # 90 days -- covers don't change once published
_FETCH_TIMEOUT = 15  # seconds -- this runs synchronously in the request/response cycle


def _digest(original_url: str) -> str:
    return hashlib.sha256(original_url.encode("utf-8")).hexdigest()[:32]


def proxy_url(original_url: str) -> str:
    """Return a short, same-origin URL that lazily caches/serves `original_url`.

    Registers the digest -> original_url mapping in the cache so the
    `serve` view can resolve it later purely from the digest in the path
    -- the original URL is never embedded in the returned path itself.
    """
    digest = _digest(original_url)
    cache.set(f"imgproxy_src_{digest}", original_url, _CACHE_TIMEOUT)
    return f"/covers/{digest}"


def _is_allowed_host(hostname: str) -> bool:
    return any(
        hostname == suffix or hostname.endswith(f".{suffix}")
        for suffix in _ALLOWED_SUFFIXES
    )


def _is_public_host(hostname: str) -> bool:
    """Reject hosts that resolve to a private/loopback/link-local address.

    Defense in depth against this endpoint being used to reach internal
    services (redis/db containers etc.) even if a hostname somehow slipped
    past the suffix allowlist.
    """
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            return False
    return True


@require_GET
def serve(request, digest):
    """Serve a proxied/cached cover image, fetching it on first request."""
    img_cache_key = f"imgproxy_img_{digest}"
    cached = cache.get(img_cache_key)

    if cached is None:
        original_url = cache.get(f"imgproxy_src_{digest}")
        if not original_url:
            raise Http404("Unknown image")

        parsed = urlparse(original_url)
        if parsed.scheme != "https" or not parsed.hostname:
            return HttpResponseBadRequest("Invalid source")
        if not _is_allowed_host(parsed.hostname) or not _is_public_host(
            parsed.hostname,
        ):
            return HttpResponseBadRequest("Host not allowed")

        try:
            resp = requests.get(
                original_url,
                timeout=_FETCH_TIMEOUT,
                verify=settings.REQUESTS_VERIFY_SSL,
                headers={"User-Agent": "Mozilla/5.0 (Yamtrack image proxy)"},
            )
            resp.raise_for_status()
        except requests.exceptions.RequestException:
            logger.warning(
                "Image proxy fetch failed for %s", original_url, exc_info=True,
            )
            raise Http404("Image not available") from None

        content_type = resp.headers.get("Content-Type", "image/jpeg")
        if not content_type.startswith("image/"):
            logger.warning(
                "Image proxy got non-image content-type %r for %s",
                content_type,
                original_url,
            )
            raise Http404("Image not available")

        cached = (content_type, resp.content)
        cache.set(img_cache_key, cached, _CACHE_TIMEOUT)

    content_type, body = cached
    response = HttpResponse(body, content_type=content_type)
    response["Cache-Control"] = f"public, max-age={_CACHE_TIMEOUT}, immutable"
    return response
