self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Installed');
});

self.addEventListener('fetch', (event) => {
  // Can be used to cache responses
});
