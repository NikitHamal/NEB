/* Profile overview: the latest post and the first resources are copies of the cards the other tabs already render,
   so the server does no extra work. "See all" jumps to the tab that holds the rest. */
(function () {
  'use strict';
  function fill(sectionId, bodyId, sourceId, count) {
    var sec = document.getElementById(sectionId), body = document.getElementById(bodyId), src = document.getElementById(sourceId);
    if (!sec || !body || !src) return 0;
    var cards = src.querySelectorAll(':scope > .post-card');
    for (var i = 0; i < cards.length && i < count; i++) {
      var c = cards[i].cloneNode(true);
      c.removeAttribute('id');
      c.querySelectorAll('[id]').forEach(function (n) { n.removeAttribute('id'); });
      body.appendChild(c);
    }
    sec.hidden = !body.children.length;
    return body.children.length;
  }
  function init() {
    if (!document.getElementById('tabOverview')) return;
    var n = fill('ovPost', 'ovPostBody', 'activityFeed', 1) + fill('ovRes', 'ovResBody', 'resourcesFeed', 3);
    var tiles = document.querySelector('#tabOverview .pv3-glance, #tabOverview .pv3-study');
    var none = document.getElementById('ovNone');
    if (none) none.hidden = !!(n || tiles);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
