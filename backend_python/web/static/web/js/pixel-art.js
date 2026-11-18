/* M3X art for resource thumbnails and profile covers (file name kept for the templates that load it).

   Thumbnails are the v1 M3X art library's `thumb` pieces, 6 per subject family, and covers are the v7
   `cover` pieces (concepts/art, concepts/art-v7). Both are drawn by code from js/m3x-art.js (inline SVG). A thumbnail is picked by subject family and a stable
   hash, the same as the Android app (M3xArt.kt). A cover is the id in data-neb-cover. */
(function (global) {
  'use strict';

  var BANNER_VARIANTS = 6;
  var ROLES = ['MEMBER', 'VERIFIED', 'TUTOR', 'INSTITUTION', 'MODERATOR', 'ADMIN', 'BOT'];
  // [accent, deep] for type laid over each role's cover; ink is always white
  var COVER_INK = {
    MEMBER: ['rgb(196, 201, 212)', 'rgb(14, 19, 28)'],
    VERIFIED: ['rgb(192, 211, 246)', 'rgb(11, 27, 56)'],
    TUTOR: ['rgb(210, 199, 234)', 'rgb(26, 17, 46)'],
    INSTITUTION: ['rgb(188, 212, 204)', 'rgb(8, 28, 21)'],
    MODERATOR: ['rgb(192, 206, 220)', 'rgb(12, 23, 35)'],
    ADMIN: ['rgb(201, 201, 206)', 'rgb(18, 18, 22)'],
    BOT: ['rgb(184, 213, 221)', 'rgb(5, 29, 36)']
  };

  function stableSeed(key) {
    var h = -2128831035;
    for (var i = 0; i < key.length; i++) { h = (h ^ key.charCodeAt(i)) | 0; h = Math.imul(h, 16777619); }
    return h | 0;
  }
  function variant(hash, n) { return ((hash >>> 3) & 0x7FFFFFFF) % n; }

  // The keyword table from Color.kt, so a subject lands in the same family as in the app.
  var FAM_KEYWORDS = [
    ["HEALTH", ["health", "physical education", "phy. edu", "hpe", "sport", "fitness", "nutrition", "yoga", "स्वास्थ्य"]],
    ["EXAM", ["exam tip", "exam prep", "entrance", "model paper", "model set", "past paper", "question bank", "mock test", "revision"]],
    ["COMPUTING", ["computer", "software", "programming", "informatics", "information tech", "digital", "coding", "algorithm", "database", "web dev"]],
    ["PHYSICS", ["physics", "भौतिक"]],
    ["CHEMISTRY", ["chemistry", "chemical", "रसायन"]],
    ["MATH", ["math", "algebra", "geometry", "trigonometry", "calculus", "statistic", "गणित"]],
    ["BIOLOGY", ["biology", "botany", "zoology", "microbio", "anatomy", "genetic", "जीव"]],
    ["SOCIAL", ["social", "history", "geography", "civic", "population", "culture", "सामाजिक", "अध्ययन"]],
    ["COMMERCE", ["economic", "account", "business", "finance", "commerce", "marketing", "banking", "book keeping", "bookkeeping", "अर्थ"]],
    ["LANGUAGE", ["english", "nepali", "literature", "grammar", "language", "sanskrit", "hindi", "maithili", "newari", "writing", "नेपाली", "अंग्रेजी", "साहित्य"]],
    ["SCIENCE", ["science", "environment", "astronomy", "geology", "laboratory", "विज्ञान"]]
  ];

  function subjectFamily(subject) {
    var s = (subject || '').trim().toLowerCase();
    if (!s) return 'GENERAL';
    for (var i = 0; i < FAM_KEYWORDS.length; i++) {
      var kws = FAM_KEYWORDS[i][1];
      for (var k = 0; k < kws.length; k++) if (s.indexOf(kws[k]) >= 0) return FAM_KEYWORDS[i][0];
    }
    return 'GENERAL';
  }

  function img(src, cls, eager) {
    var i = document.createElement('img');
    i.className = 'neb-pixel-art ' + cls;
    i.alt = '';
    i.decoding = 'async';
    if (!eager) i.loading = 'lazy';
    i.setAttribute('aria-hidden', 'true');
    i.src = src;
    return i;
  }

  // The art is drawn for the box it sits in (aspect read from the element, steps of 0.05), so the whole composition is
  // always visible: nothing is cropped on a phone, a tablet or a wide column. A resize that changes the aspect redraws it.
  function aspectOf(el) {
    var w = el.clientWidth, h = el.clientHeight;
    return w > 0 && h > 0 ? w / h : 0;
  }

  var ro = global.ResizeObserver ? new ResizeObserver(function (entries) {
    entries.forEach(function (e) {
      var el = e.target, M = global.NebM3x;
      if (!M || el.__nebRaf) return;
      el.__nebRaf = requestAnimationFrame(function () {
        el.__nebRaf = 0;
        var a = M.fit(aspectOf(el), 0);
        if (a && a !== el.__nebFit) draw(el);
      });
    });
  }) : null;

  function draw(el) {
    var M = global.NebM3x;
    if (!M) return;
    var old = el.querySelector(':scope > svg.m3a');
    var a = M.fit(aspectOf(el), 0);
    el.__nebFit = a;
    var kind = el.getAttribute('data-neb-art'), html;
    // drawn by code (js/m3x-art.js): inline SVG, no request, Light and Dark share one drawing
    if (kind === 'cover') {
      var cid = el.getAttribute('data-neb-cover');
      if (!cid || !M.has(cid)) cid = M.defaultCover(el.getAttribute('data-neb-user'));
      html = M.cover(cid, el.hasAttribute('data-neb-live'), a);
    } else {
      var subject = el.getAttribute('data-neb-subject') || '';
      var bv = variant(stableSeed(el.getAttribute('data-neb-seed') || subject), BANNER_VARIANTS);
      html = M.thumb(subjectFamily(subject), bv, a);
    }
    // The settle (css .m3a-live) plays when the art first shows or a cover is picked, never on a resize redraw.
    var play = !old || el.__nebPlay; el.__nebPlay = false;
    el.insertAdjacentHTML('afterbegin', html);
    if (!play) { var fresh = el.querySelector(':scope > svg.m3a'); if (fresh) fresh.classList.add('m3a-still'); }
    if (old) old.remove();
  }

  function paint(el) {
    if (el.__nebPixelArt) return;
    el.__nebPixelArt = true;
    // a copy of a drawn card (the profile overview) has its art already: watch its box so it is redrawn for its own aspect
    if (el.querySelector(':scope > svg.m3a')) { if (ro) ro.observe(el); return; }
    if (el.querySelector('svg')) return;
    draw(el);
    if (ro) ro.observe(el);
  }

  function scan(root) {
    var els = (root || document).querySelectorAll('[data-neb-art]');
    for (var i = 0; i < els.length; i++) paint(els[i]);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { scan(); });
  else scan();
  document.addEventListener('htmx:afterSwap', function (e) { scan(e.target); });

  global.NebArt = { scan: scan, repaint: function (el) { if (el) { el.__nebPlay = true; draw(el); } }, subjectFamily: subjectFamily, stableSeed: stableSeed, roles: ROLES.slice() };
})(window);
