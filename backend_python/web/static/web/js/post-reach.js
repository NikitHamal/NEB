/* Reach beacons: feed impressions (a post card was on screen for a moment) and read time on the
   post page. Both are best effort and never block anything. Server side: api/post_reach.py. */
(function () {
  'use strict';

  function csrf() {
    if (typeof CSRF_TOKEN !== 'undefined') return CSRF_TOKEN;
    var m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? m[1] : '';
  }
  function send(url, body, beacon) {
    var payload = JSON.stringify(body);
    try {
      fetch(url, {
        method: 'POST', credentials: 'same-origin', keepalive: !!beacon,
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: payload
      }).catch(function () {});
    } catch (e) { /* ignore */ }
  }

  /* ---- feed impressions ---- */
  var seen = {};
  var queue = [];
  var timer = null;
  function flush() {
    timer = null;
    if (!queue.length) return;
    var ids = queue.splice(0, 40);
    send('/ajax/post/impressions/', { ids: ids });
    if (queue.length) timer = setTimeout(flush, 1500);
  }
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      var el = en.target;
      if (en.isIntersecting) {
        el._impT = setTimeout(function () {
          var id = el.getAttribute('data-post-id');
          if (id && !seen[id]) { seen[id] = 1; queue.push(id); if (!timer) timer = setTimeout(flush, 2000); }
          io.unobserve(el);
        }, 800);
      } else if (el._impT) { clearTimeout(el._impT); el._impT = null; }
    });
  }, { threshold: 0.6 }) : null;

  function watch(root) {
    if (!io) return;
    (root || document).querySelectorAll('article.post-card[data-post-id]').forEach(function (el) {
      if (!el._watched) { el._watched = true; io.observe(el); }
    });
  }
  document.addEventListener('DOMContentLoaded', function () { watch(); });
  document.addEventListener('htmx:afterSwap', function (e) { watch(e.target); });
  new MutationObserver(function (m) { for (var i = 0; i < m.length; i++) if (m[i].addedNodes.length) { watch(); return; } })
    .observe(document.documentElement, { childList: true, subtree: true });
  window.addEventListener('pagehide', function () { if (queue.length) { send('/ajax/post/impressions/', { ids: queue.splice(0, 40) }, true); } });

  /* ---- read time on the post page ---- */
  var page = document.querySelector('[data-reach-post]');
  if (page) {
    var id = page.getAttribute('data-reach-post');
    var visibleMs = 0, since = document.visibilityState === 'visible' ? Date.now() : 0, sent = 0;
    function tick() { if (since) { visibleMs += Date.now() - since; since = Date.now(); } }
    function report(final) {
      tick();
      if (visibleMs < 1500 || visibleMs - sent < 4000 && !final) return;
      sent = visibleMs;
      send('/ajax/post/' + encodeURIComponent(id) + '/view/', { dwell_ms: Math.round(visibleMs) }, final);
    }
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'visible') since = Date.now();
      else { report(true); since = 0; }
    });
    window.addEventListener('pagehide', function () { report(true); });
    setInterval(function () { if (since) report(false); }, 15000);
  }
})();
