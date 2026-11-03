// Service worker: opens the site offline and lets it install as an app.
// Pages and data are fetched network-first (so daily updates show up); images are cache-first.
var V = "tcs-v8";
var CORE = ["./", "index.html", "data.js", "bank.js", "reviewed.js", "thoughts.js", "feedback.js", "logo.png", "icon-192.png", "manifest.webmanifest"];
self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(V).then(function (c) {
    return Promise.all(CORE.map(function (u) { return c.add(u).catch(function () { return null; }); }));
  }));
  self.skipWaiting();
});
self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    return Promise.all(ks.filter(function (k) { return k !== V; }).map(function (k) { return caches.delete(k); }));
  }));
  self.clients.claim();
});
self.addEventListener("fetch", function (e) {
  var req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin) return;
  if (/\.(png|webmanifest)$/.test(url.pathname)) {
    e.respondWith(caches.match(req).then(function (m) { return m || fetch(req); }));
  } else {
    e.respondWith(fetch(req).then(function (r) {
      var copy = r.clone(); caches.open(V).then(function (c) { c.put(req, copy); }); return r;
    }).catch(function () { return caches.match(req).then(function (m) { return m || caches.match("index.html"); }); }));
  }
});
