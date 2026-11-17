/* NEBians M3X Art Library v5 - core. Self-contained (no v3/v4 code).
   Rules: one hue per piece (tonal ramp + paper + ink), one hero, no scattered dots/plus/sparkles, no stacked icon chips.
   Flat fills only. No gradients, shadows, filters, text, emoji, pixels, rings on avatars.
   Never drawn (owner): mountains, forests, trees, ships, building rows, moon, sun. */
(function (g) {
  'use strict';
  var A = g.NebArtV5 = { engines: {}, kinds: {}, objects: {}, people: {}, subjects: {} };
  var sin = Math.sin, cos = Math.cos, PI = Math.PI;
  var f = A.f = function (n) { return String(Math.round(n * 10) / 10); };
  A.hash = function (s) { var h = 2166136261, i; s = String(s); for (i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; };
  A.rng = function (seed) {
    var a = typeof seed === 'number' ? seed >>> 0 : A.hash(seed);
    var r = function () { a = (a + 0x6D2B79F5) | 0; var t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
    r.range = function (x, y) { return x + r() * (y - x); }; r.int = function (x, y) { return Math.floor(x + r() * (y - x + 1)); };
    r.pick = function (arr) { return arr[Math.floor(r() * arr.length)]; }; r.chance = function (p) { return r() < p; };
    return r;
  };
  /* OKLCH -> hex with chroma reduction until in gamut */
  function lin2s(c) { c = Math.max(0, Math.min(1, c)); return c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055; }
  A.oklch = function (L, C, H) {
    var h = H * PI / 180, k, a, b, l, m, s, rgb;
    for (k = 0; k < 14; k++) {
      a = C * cos(h); b = C * sin(h);
      l = Math.pow(L + 0.3963377774 * a + 0.2158037573 * b, 3); m = Math.pow(L - 0.1055613458 * a - 0.0638541728 * b, 3); s = Math.pow(L - 0.0894841775 * a - 1.2914855480 * b, 3);
      rgb = [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s, -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s];
      if (rgb.every(function (v) { return v >= -0.001 && v <= 1.001; })) break; C *= 0.92;
    }
    return '#' + rgb.map(function (v) { return ('0' + Math.round(lin2s(v) * 255).toString(16)).slice(-2); }).join('');
  };
  A.mix = function (a, b, t) { function p(h, i) { return parseInt(h.substr(1 + i * 2, 2), 16); } var o = '#', i; for (i = 0; i < 3; i++) o += ('0' + Math.round(p(a, i) * (1 - t) + p(b, i) * t).toString(16)).slice(-2); return o; };
  /* hue, chroma. No purple band (280-340). */
  A.HUES = { blue: [258, 0.19], cobalt: [264, 0.17], sky: [238, 0.12], cyan: [212, 0.1], teal: [192, 0.095], green: [158, 0.12], emerald: [150, 0.11], lime: [126, 0.13], olive: [108, 0.09], amber: [82, 0.13], marigold: [70, 0.14], orange: [54, 0.15], coral: [36, 0.14], red: [26, 0.17], rose: [8, 0.13], terracotta: [42, 0.1], sand: [85, 0.045], slate: [250, 0.03], stone: [70, 0.014], ink: [262, 0.05] };
  A.palettes = Object.keys(A.HUES);
  var LT = { bg: [0.972, 0.1], s1: [0.94, 0.26], s2: [0.895, 0.45], hi: [0.82, 0.7], m: [0.7, 1], d: [0.53, 0.95], ink: [0.34, 0.65] };
  var DK = { bg: [0.19, 0.22], s1: [0.235, 0.38], s2: [0.29, 0.5], hi: [0.8, 0.7], m: [0.67, 0.95], d: [0.5, 0.9], ink: [0.29, 0.5] };
  A.ramp = function (hue, C, mode) { var T = mode === 'dark' ? DK : LT, o = { hue: hue }, k; for (k in T) o[k] = A.oklch(T[k][0], C * T[k][1], hue); o.paper = mode === 'dark' ? A.oklch(0.9, 0.012, hue) : '#ffffff'; o.pap2 = mode === 'dark' ? A.oklch(0.76, 0.02, hue) : A.oklch(0.93, 0.012, hue); o.mode = mode; return o; };
  A.palette = function (name, mode) {
    var h = A.HUES[name] || A.HUES.blue, P = A.ramp(h[0], h[1], mode), ah = h[0] > 200 ? h[0] - 32 : h[0] + 32;
    P.name = name; P.alt = A.ramp(ah, Math.max(h[1], 0.09), mode); return P;
  };
  /* svg primitives */
  A.attr = function (ex) { return ex ? ' ' + ex : ''; };
  A.rect = function (x, y, w, h, rx, fill, ex) { return '<rect x="' + f(x) + '" y="' + f(y) + '" width="' + f(w) + '" height="' + f(h) + '"' + (rx ? ' rx="' + f(rx) + '"' : '') + ' fill="' + fill + '"' + A.attr(ex) + '/>'; };
  A.circle = function (x, y, r, fill, ex) { return '<circle cx="' + f(x) + '" cy="' + f(y) + '" r="' + f(r) + '" fill="' + fill + '"' + A.attr(ex) + '/>'; };
  A.ell = function (x, y, rx, ry, fill, ex) { return '<ellipse cx="' + f(x) + '" cy="' + f(y) + '" rx="' + f(rx) + '" ry="' + f(ry) + '" fill="' + fill + '"' + A.attr(ex) + '/>'; };
  A.path = function (d, fill, ex) { return '<path d="' + d + '" fill="' + fill + '"' + A.attr(ex) + '/>'; };
  A.stroke = function (d, sw, col, ex) { return '<path d="' + d + '" fill="none" stroke="' + col + '" stroke-width="' + f(sw) + '" stroke-linecap="round" stroke-linejoin="round"' + A.attr(ex) + '/>'; };
  A.line = function (x1, y1, x2, y2, sw, col) { return A.stroke('M' + f(x1) + ' ' + f(y1) + 'L' + f(x2) + ' ' + f(y2), sw, col); };
  A.poly = function (pts, fill, ex) { return A.path('M' + pts.map(function (p) { return f(p[0]) + ' ' + f(p[1]); }).join('L') + 'Z', fill, ex); };
  A.g = function (tf, body) { return '<g transform="' + tf + '">' + body + '</g>'; };
  A.rot = function (a, cx, cy, body) { return A.g('rotate(' + f(a) + ' ' + f(cx) + ' ' + f(cy) + ')', body); };
  /* Catmull-Rom smooth path through points */
  A.smooth = function (p, closed) {
    var n = p.length, d = 'M' + f(p[0][0]) + ' ' + f(p[0][1]), i, p0, p1, p2, p3;
    for (i = 0; i < (closed ? n : n - 1); i++) {
      p0 = p[closed ? (i - 1 + n) % n : Math.max(i - 1, 0)]; p1 = p[i]; p2 = p[(i + 1) % n]; p3 = p[closed ? (i + 2) % n : Math.min(i + 2, n - 1)];
      d += 'C' + f(p1[0] + (p2[0] - p0[0]) / 6) + ' ' + f(p1[1] + (p2[1] - p0[1]) / 6) + ' ' + f(p2[0] - (p3[0] - p1[0]) / 6) + ' ' + f(p2[1] - (p3[1] - p1[1]) / 6) + ' ' + f(p2[0]) + ' ' + f(p2[1]);
    }
    return d + (closed ? 'Z' : '');
  };
  /* M3 Expressive cookie / flower shape: n lobes, depth 0..0.4 */
  A.cookie = function (cx, cy, R, n, depth, rot) {
    var pts = [], k = n * 8, i, a, q; for (i = 0; i < k; i++) { a = i / k * PI * 2 + (rot || 0); q = R * (1 - depth + depth * cos(n * (a - (rot || 0)))); pts.push([cx + q * cos(a), cy + q * sin(a)]); }
    return A.smooth(pts, true);
  };
  A.blob = function (r, cx, cy, rad, wob) { var pts = [], n = 8, i, a, q, ph = r() * 6.28, k1 = r.int(2, 3), k2 = r.int(3, 5); for (i = 0; i < n; i++) { a = i / n * PI * 2; q = rad * (1 + wob * (0.6 * sin(k1 * a + ph) + 0.4 * sin(k2 * a + ph * 1.7))); pts.push([cx + q * cos(a), cy + q * sin(a)]); } return A.smooth(pts, true); };
  A.arch = function (x, y, w, h, fill, ex) { var r = w / 2; return A.path('M' + f(x) + ' ' + f(y + h) + 'V' + f(y + r) + 'A' + f(r) + ' ' + f(r) + ' 0 0 1 ' + f(x + w) + ' ' + f(y + r) + 'V' + f(y + h) + 'Z', fill, ex); };
  A.clip = function (id, d, body) { return '<defs><clipPath id="' + id + '"><path d="' + d + '"/></clipPath></defs><g clip-path="url(#' + id + ')">' + body + '</g>'; };
  A.clipRect = function (id, x, y, w, h, rx, body) { return '<defs><clipPath id="' + id + '"><rect x="' + f(x) + '" y="' + f(y) + '" width="' + f(w) + '" height="' + f(h) + '" rx="' + f(rx || 0) + '"/></clipPath></defs><g clip-path="url(#' + id + ')">' + body + '</g>'; };
  A.svg = function (w, h, body, bg) { return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + w + ' ' + h + '" width="' + w + '" height="' + h + '" fill="none">' + (bg ? A.rect(0, 0, w, h, 0, bg) : '') + body + '</svg>'; };
  A.make = function (s) {
    var mode = s.mode || 'light', P = A.palette(s.palette || 'blue', mode), key = (s.id || s.engine) + ':' + (s.seed || 0), r = A.rng(key), fn = A.engines[s.engine];
    if (!fn) throw new Error('unknown engine ' + s.engine);
    var body = fn({ w: s.w, h: s.h, P: P, r: r, uid: 'q' + (A.hash(key) % 100000), subj: s.subj, o: s.o || {}, mode: mode, kind: s.kind });
    return A.svg(s.w, s.h, body, s.nobg ? '' : (s.o && s.o.bg && P[s.o.bg]) || P.bg);
  };
})(typeof window !== 'undefined' ? window : globalThis);
