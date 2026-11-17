/* NEBians M3X Art Library v2 — Core Engine
   8-tone M3X palettes (16 families, Light + Dark #121318 neutral graphite),
   12 expressive silhouettes, and 30-deg isometric book-N geometry primitives.
   Strictly flat tonal fills: zero gradients, zero shadows, zero purple, zero emoji, zero pixels. */
(function (g) {
  'use strict';
  var V = g.NebArtV2 = { layouts: {}, scenes: {}, kinds: {}, subjects: {}, roles: {} };

  V.hash = function (s) {
    var h = 2166136261; s = String(s);
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  };
  V.rng = function (seed) {
    var a = typeof seed === 'number' ? seed >>> 0 : V.hash(seed);
    return function () {
      a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  };

  /* 16 M3X Palette Families (Strictly no purple; anchored in NEBians brand blue #0058df & subject tokens).
     8 flat stops: [0:ground, 1:soft, 2:mid, 3:high, 4:strong, 5:ink, 6:accent, 7:paper/rim] */
  var FAM = [
    ['brand',      218, 1.00,  38], ['azure',      214, 0.92,  44],
    ['sky',        199, 0.90,  18], ['cobalt',     224, 0.88, 174],
    ['aqua',       182, 0.85,  12], ['teal',       168, 0.82,  36],
    ['emerald',    152, 0.80,  42], ['mint',       140, 0.78, 344],
    ['moss',        98, 0.72, 210], ['sage',       118, 0.56,  32],
    ['amber',       42, 0.92, 214], ['marigold',    32, 0.94, 198],
    ['terracotta',  16, 0.84, 188], ['coral',        6, 0.86, 194],
    ['rose',       346, 0.82, 164], ['slate',      215, 0.32,  38]
  ];
  function hsl(h, s, l) { return 'hsl(' + Math.round((h + 360) % 360) + ',' + Math.round(Math.max(0, Math.min(100, s))) + '%,' + Math.round(Math.max(0, Math.min(100, l))) + '%)'; }
  V.palettes = FAM.map(function (f) { return f[0]; });
  V.palette = function (name, mode) {
    var f = FAM.filter(function (x) { return x[0] === name; })[0] || FAM[0];
    var h = f[1], k = f[2], ha = f[3], d = mode === 'dark';
    return d ? [
      hsl(h, 28 * k,  9), hsl(h, 38 * k, 15), hsl(h, 48 * k, 23), hsl(h, 62 * k, 35),
      hsl(h, 82 * k, 64), hsl(h, 88 * k, 91), hsl(ha, 86, 64),    hsl(h, 40 * k, 96)
    ] : [
      hsl(h, 78 * k, 94), hsl(h, 76 * k, 86), hsl(h, 72 * k, 74), hsl(h, 76 * k, 56),
      hsl(h, 88 * k, 40), hsl(h, 90 * k, 14), hsl(ha, 86, 56),    '#ffffff'
    ];
  };

  /* 12 Expressive M3X silhouettes sampled as smooth quadratic closed splines */
  var S = {
    cookie:    [9,  function (t) { return 1 + 0.072 * Math.cos(9 * t); }],
    sunny:     [8,  function (t) { return 1 + 0.135 * Math.cos(8 * t); }],
    flower:    [6,  function (t) { return 0.76 + 0.24 * Math.cos(6 * t); }],
    clover:    [4,  function (t) { return 0.68 + 0.32 * Math.abs(Math.cos(2 * t)); }],
    burst:     [12, function (t) { return 0.81 + 0.19 * Math.pow(Math.abs(Math.cos(6 * t)), 0.65); }],
    squircle:  [5,  function (t) { var c = Math.cos(t), s = Math.sin(t); return Math.pow(Math.pow(Math.abs(c), 4) + Math.pow(Math.abs(s), 4), -0.25); }],
    gem:       [4,  function (t) { var c = Math.cos(t), s = Math.sin(t); return Math.pow(Math.pow(Math.abs(c), 1.6) + Math.pow(Math.abs(s), 1.6), -0.625); }],
    pebble:    [5,  function (t) { return 1 + 0.10 * Math.cos(2 * t - 0.6) + 0.05 * Math.cos(3 * t + 0.4); }],
    lotus:     [7,  function (t) { return 0.78 + 0.22 * Math.cos(7 * t) + 0.04 * Math.cos(14 * t); }],
    shield:    [5,  function (t) { return 0.88 + 0.12 * Math.sin(t) - 0.08 * Math.cos(2 * t); }],
    starburst: [10, function (t) { return 0.75 + 0.25 * Math.abs(Math.cos(5 * t)); }],
    circle:    [4,  function () { return 1; }]
  };
  V.shapeNames = ['cookie', 'sunny', 'flower', 'clover', 'burst', 'squircle', 'gem', 'pebble', 'lotus', 'shield', 'starburst'];
  var f1 = V.f1 = function (v) { return Math.round(v * 10) / 10; };

  V.shapeD = function (kind, cx, cy, r, rot) {
    var s = S[kind] || S.cookie, n = Math.max(36, s[0] * 6), p = [], i, t, rho;
    for (i = 0; i < n; i++) {
      t = (i / n) * Math.PI * 2; rho = s[1](t) * r;
      p.push([cx + rho * Math.cos(t + (rot || 0)), cy + rho * Math.sin(t + (rot || 0))]);
    }
    var m = function (a, b) { return f1((a[0] + b[0]) / 2) + ' ' + f1((a[1] + b[1]) / 2); };
    var d = 'M' + m(p[0], p[1]);
    for (i = 1; i <= n; i++) { var a = p[i % n], b = p[(i + 1) % n]; d += 'Q' + f1(a[0]) + ' ' + f1(a[1]) + ' ' + m(a, b); }
    return d + 'Z';
  };
  V.shape = function (k, cx, cy, r, rot, fill, ex) { return '<path d="' + V.shapeD(k, cx, cy, r, rot) + '" fill="' + fill + '"' + (ex || '') + '/>'; };
  V.circle = function (cx, cy, r, fill, ex) { return '<circle cx="' + f1(cx) + '" cy="' + f1(cy) + '" r="' + f1(r) + '" fill="' + fill + '"' + (ex || '') + '/>'; };
  V.ring = function (cx, cy, r, sw, stroke, ex) { return '<circle cx="' + f1(cx) + '" cy="' + f1(cy) + '" r="' + f1(r) + '" fill="none" stroke="' + stroke + '" stroke-width="' + f1(sw) + '"' + (ex || '') + '/>'; };
  V.rect = function (x, y, w, h, rx, fill, ex) { return '<rect x="' + f1(x) + '" y="' + f1(y) + '" width="' + f1(w) + '" height="' + f1(h) + '" rx="' + f1(rx || 0) + '" fill="' + fill + '"' + (ex || '') + '/>'; };
  V.line = function (x1, y1, x2, y2, sw, stroke, ex) { return '<line x1="' + f1(x1) + '" y1="' + f1(y1) + '" x2="' + f1(x2) + '" y2="' + f1(y2) + '" stroke="' + stroke + '" stroke-width="' + f1(sw) + '" stroke-linecap="round"' + (ex || '') + '/>'; };
  V.poly = function (pts, fill, ex) { return '<polygon points="' + pts.map(function (p) { return f1(p[0]) + ',' + f1(p[1]); }).join(' ') + '" fill="' + fill + '"' + (ex || '') + '/>'; };
  V.arch = function (x, y, w, h, fill, ex) { var r = w / 2; return '<path d="M' + f1(x) + ' ' + f1(y + h) + 'V' + f1(y + r) + 'A' + f1(r) + ' ' + f1(r) + ' 0 0 1 ' + f1(x + w) + ' ' + f1(y + r) + 'V' + f1(y + h) + 'Z" fill="' + fill + '"' + (ex || '') + '/>'; };
  V.quarter = function (x, y, s, q, fill) {
    var a = [
      'M' + f1(x) + ' ' + f1(y) + 'H' + f1(x + s) + 'A' + f1(s) + ' ' + f1(s) + ' 0 0 1 ' + f1(x) + ' ' + f1(y + s) + 'Z',
      'M' + f1(x + s) + ' ' + f1(y) + 'V' + f1(y + s) + 'A' + f1(s) + ' ' + f1(s) + ' 0 0 1 ' + f1(x) + ' ' + f1(y) + 'Z',
      'M' + f1(x + s) + ' ' + f1(y + s) + 'H' + f1(x) + 'A' + f1(s) + ' ' + f1(s) + ' 0 0 1 ' + f1(x + s) + ' ' + f1(y) + 'Z',
      'M' + f1(x) + ' ' + f1(y + s) + 'V' + f1(y) + 'A' + f1(s) + ' ' + f1(s) + ' 0 0 1 ' + f1(x + s) + ' ' + f1(y + s) + 'Z'
    ];
    return '<path d="' + a[q % 4] + '" fill="' + fill + '"/>';
  };

  /* 30-degree Isometric Solid Block (light top, mid left, dark right, optional rim) */
  var CX = 0.866025, SY = 0.5;
  V.isoBox = function (cx, cy, dx, dy, dz, fTop, fLeft, fRight, rim) {
    var p0 = [cx, cy], p1 = [cx + dx * CX, cy + dx * SY], p2 = [cx + (dx - dy) * CX, cy + (dx + dy) * SY], p3 = [cx - dy * CX, cy + dy * SY];
    var b1 = [p1[0], p1[1] + dz], b2 = [p2[0], p2[1] + dz], b3 = [p3[0], p3[1] + dz];
    var st = rim ? ' stroke="' + rim + '" stroke-width="1.4" stroke-linejoin="round"' : '';
    return V.poly([p3, p2, b2, b3], fLeft, st) + V.poly([p2, p1, b1, b2], fRight, st) + V.poly([p0, p1, p2, p3], fTop, st);
  };
  V.glyph = function (name, x, y, s, fill) {
    var d = (g.NebGlyphs || {})[name]; if (!d) return '';
    return '<path transform="translate(' + f1(x) + ' ' + f1(y + s) + ') scale(' + (s / 960).toFixed(4) + ')" d="' + d + '" fill="' + fill + '"/>';
  };
})(typeof window !== 'undefined' ? window : globalThis);
