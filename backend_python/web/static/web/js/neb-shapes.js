/* Avatar shapes. One shape per person, everywhere: the username (from the nearest profile link, or
   data-avatar-seed) is hashed into the expressive set defined in m3x/app-shapes.css. Runs on load
   and on every DOM change, so feeds that load more posts, reply refreshes and popups all get it. */
(function () {
  'use strict';

  var SHAPES = ['cookie', 'sunny', 'flower', 'clover', 'burst', 'pebble', 'squircle'];
  var SEL = [
    '.post-card-avatar', '.fp-avatar', '.fp-reply-avatar', '.fp-thread-avatar', '.rcard-avatar',
    '.resource-card-avatar', '.forum-contributor-avatar', '.user-search-avatar', '.leaderboard-avatar',
    '.suggest-post-avatar', '.pf-reply-card-avatar', '.hf-peer-avatar', '.hf-side-avatar',
    '.mkt-hero-avatar', '.mkt-member-avatar', '.study-join-avatar', '.behalf-avatar',
    '.profile-dropdown-avatar', '.fp-identity-option-avatar', '.hf-option-avatar',
    '.notif-avatar-real', '.who-avatar-wrap', '.pf-avatar-overlap-wrap', '[data-avatar-seed]'
  ].join(',');

  function hash(s) {
    var h = 2166136261;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  }

  function userFromHref(a) {
    var m = a && a.getAttribute('href') && a.getAttribute('href').match(/\/profile\/([^\/?#]+)/);
    return m ? decodeURIComponent(m[1]).toLowerCase() : '';
  }

  function seedOf(el) {
    var s = el.getAttribute('data-avatar-seed');
    if (s) return s.toLowerCase();
    var a = el.closest('a[href*="/profile/"]') || el.querySelector('a[href*="/profile/"]');
    var u = userFromHref(a);
    if (u) return u;
    var node = el.parentElement;
    for (var d = 0; node && d < 3; d++, node = node.parentElement) {
      var links = node.querySelectorAll('a[href*="/profile/"]');
      if (links.length) return userFromHref(links[0]);
    }
    var img = el.querySelector('img[alt]');
    if (img && img.alt) return img.alt.toLowerCase();
    return (el.textContent || '').trim().toLowerCase();
  }

  function apply(root) {
    var list = [];
    if (root.nodeType === 1 && root.matches(SEL)) list.push(root);
    if (root.querySelectorAll) list.push.apply(list, root.querySelectorAll(SEL));
    list.forEach(function (el) {
      if (el.hasAttribute('data-shape')) return;
      var seed = seedOf(el);
      if (!seed) return;
      var h = hash(seed);
      el.setAttribute('data-shape', SHAPES[h % SHAPES.length]);
      el.setAttribute('data-tone', String((h >>> 8) % 3));
    });
  }

  var queued = false, pending = [];
  function flush() {
    queued = false;
    var nodes = pending; pending = [];
    nodes.forEach(function (n) { if (n.isConnected) apply(n); });
  }
  function schedule(n) {
    pending.push(n);
    if (!queued) { queued = true; requestAnimationFrame(flush); }
  }

  function start() {
    apply(document);
    new MutationObserver(function (muts) {
      muts.forEach(function (m) {
        m.addedNodes.forEach(function (n) { if (n.nodeType === 1) schedule(n); });
      });
    }).observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
  window.NebShapes = { apply: apply, shapes: SHAPES };
})();
