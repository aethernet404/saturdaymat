const CACHE = 'saturday-mat-v3';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/images/hero.jpg'
];

// Install: cache the static shell
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  // Activate immediately — take over from any stale workers
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

// Fetch: network-first for HTML, cache-first for static assets
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests and API calls
  if (event.request.method !== 'GET') return;
  if (event.request.url.includes('/api/')) return;

  const url = new URL(event.request.url);
  const isHTML = url.pathname === '/' || url.pathname === '/index.html';

  if (isHTML) {
    // Always try the network first so updated index.html is picked up right away
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // The Cache API rejects 206 (Partial Content) responses -- only
          // cache full, successful responses.
          if (response.ok && response.status !== 206) {
            const clone = response.clone();
            caches.open(CACHE).then((cache) => cache.put(event.request, clone));
          }
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Static assets: serve from cache, then refresh cache in the background
  event.respondWith(
    caches.match(event.request).then((cached) => {
      return cached || fetch(event.request).then((response) => {
        // Range requests (e.g. video seeking) return 206, which the Cache
        // API doesn't support storing -- only cache full 200 responses.
        if (response.ok && response.status !== 206) {
          const clone = response.clone();
          caches.open(CACHE).then((cache) => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => cached);
    })
  );
});
