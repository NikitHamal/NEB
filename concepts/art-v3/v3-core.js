/* NEBians M3X Art Library v3 - core.
   OKLCH tonal engine (perceptual ramps, light + graphite dark), depth ramp for layered scenes,
   expressive shapes, seeded noise and smooth ridge geometry.
   Flat fills only: no gradients, no shadows, no purple, no emoji, no pixels, no rings on avatars. */
(function (g) {
  'use strict';
  var A = g.NebArtV3 = { engines: {}, kinds: {}, subjects: {}, objects: {}, faces: {} };
  var abs = Math.abs, sin = Math.sin, cos = Math.cos, PI = Math.PI;

  A.hash = function (s) { var h = 2166136261; s = String(s); for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; };
  A.rng = function (seed) {
    var a = typeof seed === 'number' ? seed >>> 0 : A.hash(seed);
    var r = function () { a = (a + 0x6D2B79F5) | 0; var t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
    r.range = function (a, b) { return a + (b - a) * r(); };
    r.int = function (a, b) { return Math.floor(a + (b - a + 1) * r()); };
    r.pick = function (l) { return l[Math.floor(r() * l.length)]; };
    r.chance = function (p) { return r() < p; };
    return r;
  };
  var f = A.f = function (v) { return Math.round(v * 10) / 10; };

  /* ---------- OKLCH -> hex with gamut squeeze ---------- */
  function lin(L, C, H) {
    var h = H * PI / 180, a = C * cos(h), b = C * sin(h);
    var l = Math.pow(L + 0.3963377774 * a + 0.2158037573 * b, 3), m = Math.pow(L - 0.1055613458 * a - 0.0638541728 * b, 3), s = Math.pow(L - 0.0894841775 * a - 1.291485548 * b, 3);
    return [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s, -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s];
  }
  var hx = A.oklch = function (L, C, H) {
    var c = lin(L, C, H), n = 0;
    while (n++ < 14 && (Math.min(c[0], c[1], c[2]) < -0.002 || Math.max(c[0], c[1], c[2]) > 1.002)) { C *= 0.93; c = lin(L, C, H); }
    return '#' + c.map(function (x) { x = Math.max(0, Math.min(1, x)); x = x <= 0.0031308 ? 12.92 * x : 1.055 * Math.pow(x, 1 / 2.4) - 0.055; return ('0' + Math.round(x * 255).toString(16)).slice(-2); }).join('');
  };

  /* name, hue, chroma, spark hue, neutral hue. 20 families, nothing between 285 and 335 (no purple). */
  var FAM = [['brand', 262, 0.20, 75, 262], ['cobalt', 255, 0.19, 55, 255], ['sky', 232, 0.15, 40, 232], ['aqua', 205, 0.13, 30, 205],
    ['teal', 188, 0.12, 40, 188], ['emerald', 160, 0.14, 70, 160], ['mint', 150, 0.12, 20, 150], ['moss', 128, 0.13, 55, 128],
    ['lime', 112, 0.16, 28, 112], ['sun', 92, 0.16, 250, 92], ['amber', 72, 0.16, 235, 72], ['marigold', 60, 0.17, 225, 60],
    ['terracotta', 42, 0.14, 215, 42], ['coral', 28, 0.17, 205, 28], ['rose', 8, 0.15, 190, 8], ['crimson', 20, 0.19, 175, 20],
    ['slate', 250, 0.045, 60, 250], ['sand', 85, 0.05, 235, 85], ['pine', 168, 0.09, 55, 168], ['denim', 245, 0.12, 70, 245]];
  A.palettes = FAM.map(function (x) { return x[0]; });
  A.palette = function (name, mode) {
    var F = FAM.filter(function (x) { return x[0] === name; })[0] || FAM[0], H = F[1], C = F[2], SH = F[3], NH = F[4], d = mode === 'dark';
    function ch(k) { return C * Math.max(0.3, 1 - abs(k - 0.58) * 1.25); }
    var P = { name: F[0], dark: d, h: H };
    P.t = function (k) { k = Math.max(0, Math.min(1, k)); return d ? hx(0.17 + 0.71 * k, ch(k) * 0.62, H) : hx(0.972 - 0.7 * k, ch(k), H); };
    P.depth = function (k) { k = Math.max(0, Math.min(1, k)); return d ? hx(0.31 - 0.215 * k, ch(0.45 + k * 0.2) * 0.5, H) : hx(0.935 - 0.58 * k, ch(0.25 + k * 0.6), H); };
    P.sp = function (k) { k = Math.max(0, Math.min(1, k)); return d ? hx(0.25 + 0.62 * k, Math.max(0.05, 0.15 * Math.max(0.4, 1 - abs(k - 0.7))), SH) : hx(0.95 - 0.55 * k, Math.max(0.06, 0.16 * Math.max(0.4, 1 - abs(k - 0.5) * 1.2)), SH); };
    P.n = function (k) { k = Math.max(0, Math.min(1, k)); return d ? hx(0.16 + 0.75 * k, 0.012, NH) : hx(0.975 - 0.75 * k, 0.012, NH); };
    P.sky = d ? hx(0.2, C * 0.22, H) : hx(0.965, C * 0.18, H);
    P.bg = P.t(0); P.ink = d ? hx(0.95, 0.02, H) : hx(0.22, 0.06, H);
    P.paper = d ? hx(0.26, ch(0.2) * 0.3, H) : '#ffffff';
    P.snow = d ? hx(0.84, 0.03, H) : '#ffffff';
    P.sun = d ? hx(0.93, 0.03, 90) : hx(0.86, 0.16, 82);
    P.glow = d ? hx(0.3, 0.025, H) : hx(0.94, 0.07, 82);
    return P;
  };

  /* ---------- shapes ---------- */
  var POL = {
    cookie: [function (t) { return 1 + 0.07 * cos(9 * t); }, 36], cookie12: [function (t) { return 1 + 0.05 * cos(12 * t); }, 48],
    sunny: [function (t) { return 1 + 0.13 * cos(8 * t); }, 32], burst: [function (t) { return 0.82 + 0.18 * Math.pow(abs(cos(6 * t)), 0.6); }, 48],
    flower: [function (t) { return 0.76 + 0.24 * cos(6 * t); }, 36], clover: [function (t) { return 0.68 + 0.32 * abs(cos(2 * t)); }, 24],
    puffy: [function (t) { return 0.8 + 0.2 * cos(5 * t) + 0.03 * cos(10 * t); }, 30], pebble: [function (t) { return 1 + 0.1 * cos(2 * t - 0.6) + 0.05 * cos(3 * t + 0.4); }, 20],
    squircle: [function (t) { return Math.pow(Math.pow(abs(cos(t)), 4) + Math.pow(abs(sin(t)), 4), -0.25); }, 24], circle: [function () { return 1; }, 12],
    gem: [function (t) { return Math.pow(Math.pow(abs(cos(t)), 1.6) + Math.pow(abs(sin(t)), 1.6), -0.625); }, 24], lotus: [function (t) { return 0.78 + 0.22 * cos(7 * t) + 0.04 * cos(14 * t); }, 42]
  };
  A.shapeNames = Object.keys(POL);
  A.smooth = function (p, closed) {
    var n = p.length, d = 'M' + f(p[0][0]) + ' ' + f(p[0][1]), i, a, b, c, e, t = 1;
    for (i = 0; i < (closed ? n : n - 1); i++) {
      a = p[(i - 1 + n) % n]; b = p[i]; c = p[(i + 1) % n]; e = p[(i + 2) % n];
      if (!closed) { a = p[Math.max(0, i - 1)]; e = p[Math.min(n - 1, i + 2)]; }
      d += 'C' + f(b[0] + (c[0] - a[0]) / 6 * t) + ' ' + f(b[1] + (c[1] - a[1]) / 6 * t) + ' ' + f(c[0] - (e[0] - b[0]) / 6 * t) + ' ' + f(c[1] - (e[1] - b[1]) / 6 * t) + ' ' + f(c[0]) + ' ' + f(c[1]);
    }
    return d + (closed ? 'Z' : '');
  };
  A.shapeD = function (k, cx, cy, r, rot) {
    var s = POL[k] || POL.cookie, n = Math.max(10, Math.round(s[1] * Math.min(1, 0.4 + r / 80))), p = [], i, t, q;
    for (i = 0; i < n; i++) { t = i / n * PI * 2; q = s[0](t) * r; p.push([cx + q * cos(t + (rot || 0)), cy + q * sin(t + (rot || 0))]); }
    return A.smooth(p, true);
  };
  A.rpoly = function (pts, rad) { /* polygon with rounded corners */
    var n = pts.length, d = '', i, a, b, c, v1, v2, l1, l2, r, p, q;
    for (i = 0; i < n; i++) {
      a = pts[(i + n - 1) % n]; b = pts[i]; c = pts[(i + 1) % n];
      l1 = Math.hypot(a[0] - b[0], a[1] - b[1]); l2 = Math.hypot(c[0] - b[0], c[1] - b[1]); r = Math.min(rad, l1 / 2.2, l2 / 2.2);
      p = [b[0] + (a[0] - b[0]) / l1 * r, b[1] + (a[1] - b[1]) / l1 * r]; q = [b[0] + (c[0] - b[0]) / l2 * r, b[1] + (c[1] - b[1]) / l2 * r];
      d += (i ? 'L' : 'M') + f(p[0]) + ' ' + f(p[1]) + 'Q' + f(b[0]) + ' ' + f(b[1]) + ' ' + f(q[0]) + ' ' + f(q[1]);
    }
    return d + 'Z';
  };
  A.ngon = function (n, cx, cy, r, rot, rad) { var p = [], i; for (i = 0; i < n; i++) p.push([cx + r * cos(rot + i / n * PI * 2), cy + r * sin(rot + i / n * PI * 2)]); return A.rpoly(p, rad == null ? r * 0.22 : rad); };
  var at = function (x) { return x ? ' ' + x : ''; };
  A.path = function (d, fill, ex) { return '<path d="' + d + '" fill="' + fill + '"' + at(ex) + '/>'; };
  A.shape = function (k, cx, cy, r, rot, fill, ex) { return A.path(A.shapeD(k, cx, cy, r, rot), fill, ex); };
  A.circle = function (cx, cy, r, fill, ex) { return '<circle cx="' + f(cx) + '" cy="' + f(cy) + '" r="' + f(r) + '" fill="' + fill + '"' + at(ex) + '/>'; };
  A.rect = function (x, y, w, h, rx, fill, ex) { return '<rect x="' + f(x) + '" y="' + f(y) + '" width="' + f(w) + '" height="' + f(h) + '" rx="' + f(rx || 0) + '" fill="' + fill + '"' + at(ex) + '/>'; };
  A.line = function (x1, y1, x2, y2, sw, stroke, ex) { return '<path d="M' + f(x1) + ' ' + f(y1) + 'L' + f(x2) + ' ' + f(y2) + '" stroke="' + stroke + '" stroke-width="' + f(sw) + '" stroke-linecap="round" fill="none"' + at(ex) + '/>'; };
  A.stroke = function (d, sw, stroke, ex) { return '<path d="' + d + '" stroke="' + stroke + '" stroke-width="' + f(sw) + '" stroke-linecap="round" stroke-linejoin="round" fill="none"' + at(ex) + '/>'; };
  A.poly = function (pts, fill, ex) { return '<path d="M' + pts.map(function (p) { return f(p[0]) + ' ' + f(p[1]); }).join('L') + 'Z" fill="' + fill + '"' + at(ex) + '/>'; };
  A.arch = function (x, y, w, h, fill, ex) { var r = w / 2; return A.path('M' + f(x) + ' ' + f(y + h) + 'V' + f(y + r) + 'A' + f(r) + ' ' + f(r) + ' 0 0 1 ' + f(x + w) + ' ' + f(y + r) + 'V' + f(y + h) + 'Z', fill, ex); };
  A.star4 = function (cx, cy, r, fill) { var k = r * 0.22; return A.path('M' + f(cx) + ' ' + f(cy - r) + 'Q' + f(cx + k) + ' ' + f(cy - k) + ' ' + f(cx + r) + ' ' + f(cy) + 'Q' + f(cx + k) + ' ' + f(cy + k) + ' ' + f(cx) + ' ' + f(cy + r) + 'Q' + f(cx - k) + ' ' + f(cy + k) + ' ' + f(cx - r) + ' ' + f(cy) + 'Q' + f(cx - k) + ' ' + f(cy - k) + ' ' + f(cx) + ' ' + f(cy - r) + 'Z', fill); };
  A.glyph = function (name, x, y, s, fill) { var d = (g.NebGlyphs || {})[name]; return d ? '<path transform="translate(' + f(x) + ' ' + f(y + s) + ') scale(' + (s / 960).toFixed(4) + ')" d="' + d + '" fill="' + fill + '"/>' : ''; };

  /* ---------- seeded value noise + ridges ---------- */
  A.noise = function (seed) {
    var r = A.rng(seed), T = [], i; for (i = 0; i < 256; i++) T.push(r());
    return function (x) { var i = Math.floor(x), t = x - i, u = t * t * (3 - 2 * t); return T[i & 255] * (1 - u) + T[(i + 1) & 255] * u; };
  };
  A.ridge = function (r, x0, x1, y, amp, freq, oct, step) {
    var n = A.noise(r.int(1, 99999)), pts = [], x, v, o, a, fr; step = step || 34;
    for (x = x0; x <= x1 + step; x += step) { v = 0; a = 1; fr = freq; for (o = 0; o < (oct || 3); o++) { v += (n(x * fr + o * 31.7) - 0.5) * a; a *= 0.5; fr *= 2.1; } pts.push([x, y + v * amp * 1.6]); }
    return pts;
  };
  A.fillTo = function (pts, bottom, fill, ex) { var q = pts.slice(); q.push([pts[pts.length - 1][0], bottom], [pts[0][0], bottom]); var d = A.smooth(pts, false) + 'L' + f(pts[pts.length - 1][0]) + ' ' + f(bottom) + 'L' + f(pts[0][0]) + ' ' + f(bottom) + 'Z'; return A.path(d, fill, ex); };
  A.svg = function (w, h, body, bg) { return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + w + ' ' + h + '" width="' + w + '" height="' + h + '" role="img">' + (bg ? '<rect width="' + w + '" height="' + h + '" fill="' + bg + '"/>' : '') + body + '</svg>'; };
})(typeof window !== 'undefined' ? window : globalThis);
