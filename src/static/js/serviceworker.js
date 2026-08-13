// Yamtrack service worker.
//
// Strategy:
//  - App shell / library assets (css, fonts, js libraries, icons): cache-first,
//    refreshed in the background (stale-while-revalidate). Fine to go stale
//    for a request or two since CACHE_NAME gets bumped on real changes.
//  - Page navigations: network-first, so logged-in users always see fresh,
//    per-user data when online. Falls back to a static offline page when the
//    network request fails outright.
//  - Everything else (HTMX fragment GETs, API calls, non-GET requests): left
//    untouched, straight to the network. Never cache mutations or partials.
//
// Bump CACHE_NAME whenever PRECACHE_URLS changes so stale entries get purged
// on the next activate.
const CACHE_NAME = 'yamtrack-v4';
const OFFLINE_URL = '/static/offline.html';

const PRECACHE_URLS = [
  '/static/css/main.css',
  '/static/favicon/android-chrome-192x192.png',
  '/static/favicon/android-chrome-512x512.png',
  '/static/fonts/roboto-flex.woff2',
  '/static/js/libraries/htmx-2.0.4.min.js',
  '/static/js/libraries/alpinejs-3.14.9.min.js',
  '/static/js/libraries/lazysizes-5.3.2.min.js',
  OFFLINE_URL,
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name)),
      ))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;

  // Only ever intercept same-origin GET requests. POST/PUT/DELETE (HTMX
  // mutations, forms) and cross-origin requests (provider APIs) go straight
  // to the network untouched.
  if (request.method !== 'GET' || new URL(request.url).origin !== self.location.origin) {
    return;
  }

  // Full page navigations: network-first with an offline fallback. Never
  // serve a cached HTML page here, since content is per-user and dynamic.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() => caches.match(OFFLINE_URL)),
    );
    return;
  }

  // Static assets: stale-while-revalidate.
  if (request.url.includes('/static/')) {
    event.respondWith(
      caches.open(CACHE_NAME).then((cache) => cache.match(request).then((cached) => {
        const fetchPromise = fetch(request)
          .then((response) => {
            if (response.ok) {
              cache.put(request, response.clone());
            }
            return response;
          })
          .catch(() => cached);
        return cached || fetchPromise;
      })),
    );
  }

  // Anything else (e.g. HTMX fragment GETs, htmx-driven partial reloads):
  // leave untouched so it always hits the network.
});

// Web Push: display a notification when a push message arrives, even if no
// Yamtrack tab is open. Payload is the JSON built by users/webpush.py
// (title, body, url, icon).
self.addEventListener('push', (event) => {
  let payload = {};
  try {
    payload = event.data ? event.data.json() : {};
  } catch {
    payload = { title: 'YamTrack', body: event.data ? event.data.text() : '' };
  }

  const title = payload.title || 'YamTrack';
  const options = {
    body: payload.body || '',
    icon: payload.icon || '/static/favicon/android-chrome-192x192.png',
    badge: '/static/favicon/android-chrome-192x192.png',
    data: { url: payload.url || '/' },
  };

  event.waitUntil(self.registration.showNotification(title, options));
});

// Clicking the notification focuses an existing Yamtrack tab if one is
// already open at the target URL's origin, otherwise opens a new one.
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const targetUrl = (event.notification.data && event.notification.data.url) || '/';

  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
      for (const client of clientList) {
        if (client.url.includes(self.location.origin) && 'focus' in client) {
          client.navigate(targetUrl);
          return client.focus();
        }
      }
      if (self.clients.openWindow) {
        return self.clients.openWindow(targetUrl);
      }
      return undefined;
    }),
  );
});
