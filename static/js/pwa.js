const staticivipop = "wivivi-v1"
const assets = [
  '/',
  '/?source=pwa',
  '/static/css/style.css',
  '/static/js/custom.js',
  '/static/img/maskable-pwa-150.png',
  '/static/img/pwa-150.png',
  '/static/img/pwa-300.png',
  '/static/img/pwa-500.png',
  "/static/img/pwa-800.png",
  '/favicon.ico'
]

self.addEventListener("install", installEvent => {
  installEvent.waitUntil(
    caches.open(staticivipop).then(cache => {
      cache.addAll(assets)
    })
  )
})

self.addEventListener("fetch", fetchEvent => {
    fetchEvent.respondWith(
      caches.match(fetchEvent.request).then(res => {
        return res || fetch(fetchEvent.request)
      })
    )
  })


