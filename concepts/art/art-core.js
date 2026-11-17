/* NEBians M3X art engine, core: seeded random, tonal palettes, expressive shapes.
   Flat fills only. No gradients, no shadows, no purple, no emoji, no pixels. */
(function (g) {
  'use strict';
  var N = g.NebArt = { layouts: {}, kinds: {}, subjects: {} };

  N.hash = function (s) { var h = 2166136261; s = String(s); for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; };
  N.rng = function (seed) {
    var a = typeof seed === 'number' ? seed >>> 0 : N.hash(seed);
    return function () { a = (a + 0x6D2B79F5) | 0; var t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  };

  /* Palettes: a hue family plus one warm or cool accent. Six tones each, built per mode.
     Tone order: 0 page, 1 soft, 2 mid, 3 strong, 4 ink, 5 accent. */
  var FAM = [
    ['azure', 218, 44], ['sky', 200, 18], ['aqua', 180, 8], ['teal', 164, 36], ['mint', 142, 340],
    ['moss', 98, 210], ['amber', 42, 215], ['orange', 22, 205], ['coral', 6, 190], ['rose', 346, 160],
    ['periwinkle', 230, 48], ['slate', 214, 38]
  ];
  function hsl(h, s, l) { return 'hsl(' + Math.round(h) + ',' + Math.round(s) + '%,' + Math.round(l) + '%)'; }
  N.palettes = FAM.map(function (f) { return f[0]; });
  N.palette = function (name, mode) {
    var f = FAM.filter(function (x) { return x[0] === name; })[0] || FAM[0], h = f[1], ha = f[2], sl = name === 'slate' ? 0.35 : 1, d = mode === 'dark';
    return d ? [hsl(h, 50 * sl, 10), hsl(h, 52 * sl, 19), hsl(h, 58 * sl, 33), hsl(h, 80 * sl, 70), hsl(h, 90 * sl, 92), hsl(ha, 88, 62)]
             : [hsl(h, 82 * sl, 92), hsl(h, 76 * sl, 82), hsl(h, 72 * sl, 66), hsl(h, 88 * sl, 40), hsl(h, 92 * sl, 15), hsl(ha, 86, 62)];
  };

  /* Expressive silhouettes: polar functions sampled and smoothed through midpoints. */
  var S = {
    cookie: [9, function (t) { return 1 + 0.07 * Math.cos(9 * t); }],
    sunny: [8, function (t) { return 1 + 0.13 * Math.cos(8 * t); }],
    flower: [6, function (t) { return 0.74 + 0.26 * Math.cos(6 * t); }],
    clover: [4, function (t) { return 0.66 + 0.34 * Math.abs(Math.cos(2 * t)); }],
    burst: [12, function (t) { return 0.8 + 0.2 * Math.pow(Math.abs(Math.cos(6 * t)), 0.6); }],
    squircle: [5, function (t) { var c = Math.cos(t), s = Math.sin(t); return Math.pow(Math.pow(Math.abs(c), 4) + Math.pow(Math.abs(s), 4), -0.25); }],
    pebble: [4, function (t) { return 1 + 0.1 * Math.cos(2 * t + 1) + 0.06 * Math.cos(3 * t); }],
    circle: [4, function () { return 1; }]
  };
  N.shapeNames = ['cookie', 'sunny', 'flower', 'clover', 'burst', 'squircle', 'pebble'];
  var f1 = function (v) { return Math.round(v * 10) / 10; };
  N.shapeD = function (kind, cx, cy, r, rot) {
    var s = S[kind] || S.circle, n = Math.max(32, s[0] * 6), p = [], i, t, rho;
    for (i = 0; i < n; i++) { t = (i / n) * Math.PI * 2; rho = s[1](t) * r; p.push([cx + rho * Math.cos(t + (rot || 0)), cy + rho * Math.sin(t + (rot || 0))]); }
    var m = function (a, b) { return f1((a[0] + b[0]) / 2) + ' ' + f1((a[1] + b[1]) / 2); };
    var d = 'M' + m(p[0], p[1]);
    for (i = 1; i <= n; i++) { var a = p[i % n], b = p[(i + 1) % n]; d += 'Q' + f1(a[0]) + ' ' + f1(a[1]) + ' ' + m(a, b); }
    return d + 'Z';
  };
  N.shape = function (kind, cx, cy, r, rot, fill, extra) { return '<path d="' + N.shapeD(kind, cx, cy, r, rot) + '" fill="' + fill + '"' + (extra || '') + '/>'; };
  N.circle = function (cx, cy, r, fill, extra) { return '<circle cx="' + f1(cx) + '" cy="' + f1(cy) + '" r="' + f1(r) + '" fill="' + fill + '"' + (extra || '') + '/>'; };
  N.rect = function (x, y, w, h, rx, fill, extra) { return '<rect x="' + f1(x) + '" y="' + f1(y) + '" width="' + f1(w) + '" height="' + f1(h) + '" rx="' + f1(rx) + '" fill="' + fill + '"' + (extra || '') + '/>'; };
  N.arch = function (x, y, w, h, fill, extra) { var r = w / 2; return '<path d="M' + f1(x) + ' ' + f1(y + h) + 'V' + f1(y + r) + 'A' + f1(r) + ' ' + f1(r) + ' 0 0 1 ' + f1(x + w) + ' ' + f1(y + r) + 'V' + f1(y + h) + 'Z" fill="' + fill + '"' + (extra || '') + '/>'; };
  N.quarter = function (x, y, s, q, fill) { var a = ['M' + x + ' ' + y + 'H' + (x + s) + 'A' + s + ' ' + s + ' 0 0 1 ' + x + ' ' + (y + s) + 'Z', 'M' + (x + s) + ' ' + y + 'V' + (y + s) + 'A' + s + ' ' + s + ' 0 0 1 ' + x + ' ' + y + 'Z', 'M' + (x + s) + ' ' + (y + s) + 'H' + x + 'A' + s + ' ' + s + ' 0 0 1 ' + (x + s) + ' ' + y + 'Z', 'M' + x + ' ' + (y + s) + 'V' + y + 'A' + s + ' ' + s + ' 0 0 1 ' + (x + s) + ' ' + (y + s) + 'Z']; return '<path d="' + a[q % 4] + '" fill="' + fill + '"/>'; };
  N.f1 = f1;
})(typeof window !== 'undefined' ? window : globalThis);
