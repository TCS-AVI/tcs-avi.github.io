// Service worker: lets the site open offline and installs as an app.
// data.js is fetched network-first so the daily updates show up; everything else is cache-first.
var V = "tcs-v1";
var CORE = ["./", "index.html", "data.js", "logo.png", "icon-192.png", "manifest.webmanifest"];
self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(V).then(function (c) { return c.addAll(CORE); }));
  self.skipWaiting();
});
self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    return Promise.all(ks.filter(function (k) { return k !== V; }).map(function (k) { return caches.delete(k); }));
  }));
  self.clients.claim();
});
self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;
  var fresh = /data\.js$|index\.html$|\/$/.test(new URL(req.url).pathname);
  if (fresh) {
    e.respondWith(fetch(req).then(function (r) {
      var copy = r.clone(); caches.open(V).then(function (c) { c.put(req, copy); }); return r;
    }).catch(function () { return caches.match(req).then(function (m) { return m || caches.match("index.html"); }); }));
  } else {
    e.respondWith(caches.match(req).then(function (m) { return m || fetch(req); }));
  }
});
