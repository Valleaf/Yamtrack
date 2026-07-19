"""Web Push sending helper for mobile/PWA notifications.

Separate from events/notifications.py (which handles Apprise) since this
targets the browser's native Push API directly -- no third-party relay
service involved, just VAPID-signed requests to whatever push service
(FCM, Mozilla autopush, etc.) issued the subscription.

Kept deliberately thin: build a JSON payload, hand it to pywebpush per
subscription, and prune subscriptions the push service reports as gone
(410 Gone / 404 Not Found) so they don't get retried forever.
"""

import json
import logging

from django.conf import settings
from pywebpush import WebPushException, webpush

from users.models import PushSubscription

logger = logging.getLogger(__name__)

# Push services return these when a subscription is no longer valid
# (browser data cleared, extension uninstalled, device unenrolled, etc.).
_STALE_SUBSCRIPTION_STATUS_CODES = {404, 410}


def send_webpush_to_user(user, title, body, url=None, icon=None):
    """Send a Web Push notification to every device the user has registered.

    Args:
        user: User object
        title: Notification title
        body: Notification body text
        url: Optional URL to open when the notification is clicked
        icon: Optional icon URL for the notification

    Returns:
        Number of subscriptions the push was successfully handed off to
        (a push service accepting the request doesn't guarantee on-screen
        delivery, just that it was queued).
    """
    if not settings.WEBPUSH_ENABLED:
        return 0

    subscriptions = list(user.push_subscriptions.all())
    if not subscriptions:
        return 0

    payload = json.dumps({
        "title": title,
        "body": body,
        "url": url or "/",
        "icon": icon or "/static/favicon/android-chrome-192x192.png",
    })

    sent_count = 0
    stale_ids = []

    for subscription in subscriptions:
        subscription_info = {
            "endpoint": subscription.endpoint,
            "keys": {
                "p256dh": subscription.p256dh_key,
                "auth": subscription.auth_key,
            },
        }

        try:
            webpush(
                subscription_info=subscription_info,
                data=payload,
                vapid_private_key=settings.WEBPUSH_VAPID_PRIVATE_KEY,
                vapid_claims={
                    "sub": f"mailto:{settings.WEBPUSH_VAPID_ADMIN_EMAIL}",
                },
                timeout=10,
            )
            sent_count += 1
        except WebPushException as exc:
            status_code = getattr(exc.response, "status_code", None)
            if status_code in _STALE_SUBSCRIPTION_STATUS_CODES:
                stale_ids.append(subscription.id)
                logger.info(
                    "Pruning stale push subscription for %s (status %s)",
                    user.username,
                    status_code,
                )
            else:
                logger.warning(
                    "Web push failed for %s: %s",
                    user.username,
                    exc,
                )

    if stale_ids:
        PushSubscription.objects.filter(id__in=stale_ids).delete()

    return sent_count
