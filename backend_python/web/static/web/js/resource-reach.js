/* Library reach beacons: resource cards that were on screen for a moment (impressions), read time on the
   resource page, and the Read / Share taps. Best effort, never blocks anything.
   Server side: api/resource_reach.py. */
(function () {
  'use strict';

  function csrf() {
    if (typeof CSRF_TOKEN !== 'undefined') return CSRF_TOKEN;
    var m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? m[1] : '';
  }
  function send(url, body, beacon) {
    try {
      fetch(url, {
        method: 'POST', credentials: 'same-origin', keepalive: !!beacon,
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify(body)
      }).catch(function () {});
    } catch (e) { /* ignore */ }
  }

  /* ---- list impressions ---- */
  var seen = {}, queue = [], timer = null;
  function flush() {
    timer = null;
    if (!queue.length) return;
    send('/ajax/resource/impressions/', { ids: queue.splice(0, 40) });
    if (queue.length) timer = setTimeout(flush, 1500);
  }
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      var el = en.target;
      if (en.isIntersecting) {
        el._impT = setTimeout(function () {
          var id = el.getAttribute('data-resource-id');
          if (id && !seen[id]) { seen[id] = 1; queue.push(id); if (!timer) timer = setTimeout(flush, 2000); }
          io.unobserve(el);
        }, 800);
      } else if (el._impT) { clearTimeout(el._impT); el._impT = null; }
    });
  }, { threshold: 0.6 }) : null;

  function watch(root) {
    if (!io) return;
    (root || document).querySelectorAll('a.rcard[data-resource-id], a.resource-card[data-resource-id]').forEach(function (el) {
      if (!el._watched) { el._watched = true; io.observe(el); }
    });
  }
  document.addEventListener('DOMContentLoaded', function () { watch(); });
  document.addEventListener('htmx:afterSwap', function (e) { watch(e.target); });
  new MutationObserver(function (m) {
    for (var i = 0; i < m.length; i++) if (m[i].addedNodes.length) { watch(); return; }
  }).observe(document.documentElement, { childList: true, subtree: true });
  window.addEventListener('pagehide', function () {
    if (queue.length) send('/ajax/resource/impressions/', { ids: queue.splice(0, 40) }, true);
  });

  /* ---- the resource page: read time, Read and Share ---- */
  var page = document.querySelector('[data-reach-resource]');
  if (!page) return;
  var id = page.getAttribute('data-reach-resource');
  var base = '/ajax/resource/' + encodeURIComponent(id);
  var visibleMs = 0, since = document.visibilityState === 'visible' ? Date.now() : 0, sent = 0, did = {};

  function tick() { if (since) { visibleMs += Date.now() - since; since = Date.now(); } }
  function report(final) {
    tick();
    if (visibleMs < 1500 || (visibleMs - sent < 4000 && !final)) return;
    sent = visibleMs;
    send(base + '/view/', { dwell_ms: Math.round(visibleMs) }, final);
  }
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'visible') since = Date.now();
    else { report(true); since = 0; }
  });
  window.addEventListener('pagehide', function () { report(true); });
  setInterval(function () { if (since) report(false); }, 15000);

  function action(name) {
    if (did[name]) return;
    did[name] = 1;
    send(base + '/action/', { action: name });
  }
  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-vw-read]')) action('read');
    else if (e.target.closest('[data-action="share-resource"]')) action('share');
  }, true);
})();
