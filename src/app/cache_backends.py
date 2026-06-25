"""Custom Django cache backend: Redis-backed but durably persisted to Postgres.

Every value written through Django's cache API (``cache.set``) is mirrored
into the ``PersistentCacheEntry`` table. On a Redis miss -- a TTL expiry,
container restart, or a manual ``redis-cli FLUSHALL`` -- ``cache.get`` falls
back to the Postgres copy and transparently re-warms Redis so subsequent
reads stay fast. ``cache.delete`` removes both copies so cache-busting flows
(manual "Sync" button, collection auto-sync, etc.) still see fresh data on
the next fetch instead of having a stale Postgres row silently resurrected.

This fixes "most watched directors/artists" and similar cache-only stats
breaking after a Redis flush, and lets director/artist/author/etc. pages
recognize already-tracked media without requiring every item's detail page
to have been visited first.

Only get/set/delete are overridden here -- this codebase doesn't use
get_many, set_many, delete_pattern, or clear() on the Django cache, so
those keep their normal Redis-only (django_redis) behaviour. Extend this
class if that changes.
"""

import hashlib
import logging
import pickle

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django_redis.cache import RedisCache

logger = logging.getLogger(__name__)

_MAX_KEY_LENGTH = 300
_MISSING = object()


def _db_key(canonical_key):
    """Return a key safe to use as the PersistentCacheEntry primary key.

    Most cache keys are short and human-readable, so they're kept as-is for
    easy inspection -- only pathologically long keys (e.g. a cached search
    for a very long query string) get hashed down to a fixed length.
    """
    if len(canonical_key) <= _MAX_KEY_LENGTH:
        return canonical_key
    digest = hashlib.sha256(canonical_key.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


class PersistentRedisCache(RedisCache):
    """RedisCache that durably backs every write with a Postgres copy."""

    def set(
        self,
        key,
        value,
        timeout=DEFAULT_TIMEOUT,
        version=None,
        client=None,
        nx=False,
        xx=False,
    ):
        """Write to Redis as normal, then mirror the value into Postgres."""
        result = super().set(
            key,
            value,
            timeout=timeout,
            version=version,
            client=client,
            nx=nx,
            xx=xx,
        )
        if result:
            try:
                self._persist(key, value, version)
            except Exception:
                logger.exception("Failed to persist cache key %r to Postgres", key)
        return result

    def get(self, key, default=None, version=None, client=None):
        """Read from Redis; on a miss, fall back to the Postgres copy."""
        value = super().get(key, default=_MISSING, version=version, client=client)
        if value is not _MISSING:
            return value

        try:
            persisted_value, found = self._load(key, version)
        except Exception:
            logger.exception("Failed to load persisted cache key %r", key)
            return default

        if not found:
            return default

        # Self-heal: warm Redis back up so the next read is fast and this
        # fallback path isn't hit again until the next flush/expiry.
        try:
            super().set(key, persisted_value, version=version, client=client)
        except Exception:
            logger.exception("Failed to re-warm Redis for cache key %r", key)

        return persisted_value

    def delete(self, key, version=None, client=None):
        """Delete from Redis and Postgres so busted caches stay busted."""
        result = super().delete(key, version=version, client=client)
        try:
            self._delete_persisted(key, version)
        except Exception:
            logger.exception("Failed to delete persisted cache key %r", key)
        return result

    # -- Postgres-backed storage ----------------------------------------

    def _persist(self, key, value, version):
        """Upsert the value into PersistentCacheEntry."""
        from app.models import PersistentCacheEntry  # noqa: PLC0415

        db_key = _db_key(self.make_key(key, version=version))
        payload = pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
        PersistentCacheEntry.objects.update_or_create(
            key=db_key,
            defaults={"value": payload},
        )

    def _load(self, key, version):
        """Return (value, found) for a key from PersistentCacheEntry."""
        from app.models import PersistentCacheEntry  # noqa: PLC0415

        db_key = _db_key(self.make_key(key, version=version))
        try:
            entry = PersistentCacheEntry.objects.get(key=db_key)
        except PersistentCacheEntry.DoesNotExist:
            return None, False
        return pickle.loads(bytes(entry.value)), True

    def _delete_persisted(self, key, version):
        """Remove the persisted copy of a key, if any."""
        from app.models import PersistentCacheEntry  # noqa: PLC0415

        db_key = _db_key(self.make_key(key, version=version))
        PersistentCacheEntry.objects.filter(key=db_key).delete()
