/* Pixel art for resource banners and profile covers -- the web half.

   The pictures are drawn once, in Kotlin (app/.../ui/pixel/art), and exported as
   tiny palette PNGs to img/pixel-art/: banner/<family>-<variant>-<day|night>.png
   (128 x 64) and cover/<role>-<variant>.png (192 x 64). Any element with
   data-neb-art gets an <img> of the same picture the Android app draws: the
   same subject family, the same hash, the same variant. Banners switch to their
   night version in dark mode. neb-art.js (the older vector art, generated from
   the same Kotlin) stays in the repo but is no longer loaded. */
(function (global) {
  'use strict';

  var BASE = (function () {
    var s = document.currentScript && document.currentScript.src;
    return s ? s.replace(/js\/pixel-art\.js.*$/, 'img/pixel-art/') : '/static/web/img/pixel-art/';
  })();
  var BANNER_VARIANTS = 12, COVER_VARIANTS = 3;
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

  function paint(el) {
    if (el.__nebPixelArt) return;
    el.__nebPixelArt = true;
    var kind = el.getAttribute('data-neb-art');
    if (kind === 'cover') {
      var role = (el.getAttribute('data-neb-role') || 'MEMBER').toUpperCase();
      if (ROLES.indexOf(role) < 0) role = 'MEMBER';
      var v = variant(stableSeed('cover|' + (el.getAttribute('data-neb-seed') || '') + '|' + role), COVER_VARIANTS);
      el.insertBefore(img(BASE + 'cover/' + role.toLowerCase() + '-' + v + '.png', 'neb-pixel-cover', true), el.firstChild);
      el.style.setProperty('--neb-cover-ink', '#fff');
      el.style.setProperty('--neb-cover-accent', COVER_INK[role][0]);
      el.style.setProperty('--neb-cover-deep', COVER_INK[role][1]);
    } else {
      var subject = el.getAttribute('data-neb-subject') || '';
      var fam = subjectFamily(subject).toLowerCase();
      var bv = variant(stableSeed(el.getAttribute('data-neb-seed') || subject), BANNER_VARIANTS);
      var stem = BASE + 'banner/' + fam + '-' + bv + '-';
      // both are in the markup; CSS shows the one that matches the theme, and a hidden lazy image is never fetched
      el.insertBefore(img(stem + 'night.png', 'neb-pixel-night'), el.firstChild);
      el.insertBefore(img(stem + 'day.png', 'neb-pixel-day'), el.firstChild);
    }
  }

  function scan(root) {
    var els = (root || document).querySelectorAll('[data-neb-art]');
    for (var i = 0; i < els.length; i++) paint(els[i]);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { scan(); });
  else scan();
  document.addEventListener('htmx:afterSwap', function (e) { scan(e.target); });

  global.NebArt = { scan: scan, repaint: function () {}, subjectFamily: subjectFamily, stableSeed: stableSeed, roles: ROLES.slice() };
})(window);
