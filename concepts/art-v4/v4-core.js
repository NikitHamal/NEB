/* NEBians M3X Art Library v4 - core.
   Builds on the v3 OKLCH engine (palettes, expressive shapes, noise) and adds: tonal kits, organic blobs, waves, grain, clip helpers.
   Flat fills only. No gradients, shadows, filters, text, emoji, pixels, rings on avatars.
   BANNED SUBJECTS (owner): mountains, forests, trees, ships, boats, city or building rows, moon, sun. Nothing here draws them. */
(function (g) {
  'use strict';
  var V3 = g.NebArtV3;
  if (!V3) throw new Error('load v3-core.js first');
  var A = g.NebArtV4 = { engines: {}, kinds: {}, objects: {}, subjects: {}, people: {} };
  ['hash', 'rng', 'f', 'oklch', 'palettes', 'shapeNames', 'smooth', 'shapeD', 'rpoly', 'ngon', 'path', 'shape', 'circle', 'rect', 'line', 'stroke', 'poly', 'arch', 'star4', 'glyph', 'noise', 'svg'].forEach(function (k) { A[k] = V3[k]; });
  var f = A.f, sin = Math.sin, cos = Math.cos, PI = Math.PI;
  var base = V3.palette;
  /* Palette with a tonal kit: five calm tones from pale to deep, plus a spark accent and its soft partner. No sun colour is used as a disc. */
  A.palette = function (name, mode) {
    var P = base(name, mode), d = mode === 'dark';
    P.kit = [P.t(0.1), P.t(0.28), P.t(0.46), P.t(0.66), P.t(0.86)];
    P.pop = P.sp(0.5); P.popSoft = P.sp(0.22); P.popDeep = P.sp(0.78);
    P.card = d ? P.t(0.1) : '#ffffff'; P.line = d ? P.t(0.3) : P.t(0.2);
    P.skin = ['#f6d3b8', '#eab98f', '#d49a6a', '#b97a4a', '#8d5a36', '#5f3a22'];
    return P;
  };
  A.mix = function (a, b, t) { /* hex blend, only for tiny steps between flat tones */
    function p(h, i) { return parseInt(h.substr(1 + i * 2, 2), 16); }
    var o = '#'; for (var i = 0; i < 3; i++) o += ('0' + Math.round(p(a, i) * (1 - t) + p(b, i) * t).toString(16)).slice(-2); return o;
  };
  /* organic closed blob from a seeded rng */
  A.blob = function (r, cx, cy, rad, wob, n) {
    n = n || 9; var pts = [], i, a, q, ph = r() * 6.28, k1 = r.int(2, 4), k2 = r.int(3, 6);
    for (i = 0; i < n; i++) { a = i / n * PI * 2; q = rad * (1 + wob * (0.6 * sin(k1 * a + ph) + 0.4 * sin(k2 * a + ph * 1.7))); pts.push([cx + q * cos(a), cy + q * sin(a)]); }
    return A.smooth(pts, true);
  };
  /* smooth wave polyline */
  A.wave = function (x0, x1, y, amp, len, ph, step, harm) {
    var pts = [], x; step = step || 24;
    for (x = x0; x <= x1 + step; x += step) pts.push([x, y + amp * (sin((x / len) * PI * 2 + ph) + (harm || 0) * sin((x / len) * PI * 4 + ph * 1.6))]);
    return pts;
  };
  A.band = function (top, bot, fill, ex) { /* closed ribbon between two polylines */
    var d = A.smooth(top, false), i, b = bot.slice().reverse();
    d += 'L' + f(b[0][0]) + ' ' + f(b[0][1]) + A.smooth(b, false).replace(/^M[^C]*/, '') + 'Z';
    return A.path(d, fill, ex);
  };
  A.dots = function (r, w, h, fill, n, rmin, rmax, avoid) {
    var s = '', i, x, y; for (i = 0; i < n; i++) { x = r() * w; y = r() * h; if (avoid && avoid(x, y)) continue; s += A.circle(x, y, r.range(rmin, rmax), fill); } return s;
  };
  A.clip = function (id, d, body) { return '<defs><clipPath id="' + id + '"><path d="' + d + '"/></clipPath></defs><g clip-path="url(#' + id + ')">' + body + '</g>'; };
  A.clipRect = function (id, x, y, w, h, rx, body) { return '<defs><clipPath id="' + id + '"><rect x="' + f(x) + '" y="' + f(y) + '" width="' + f(w) + '" height="' + f(h) + '" rx="' + f(rx || 0) + '"/></clipPath></defs><g clip-path="url(#' + id + ')">' + body + '</g>'; };
  A.g = function (tf, body) { return '<g transform="' + tf + '">' + body + '</g>'; };
  A.rot = function (a, cx, cy, body) { return '<g transform="rotate(' + f(a) + ' ' + f(cx) + ' ' + f(cy) + ')">' + body + '</g>'; };
  A.sparkle = function (cx, cy, r, fill) { return A.star4(cx, cy, r, fill); };
  A.plus = function (cx, cy, r, sw, col) { return A.line(cx - r, cy, cx + r, cy, sw, col) + A.line(cx, cy - r, cx, cy + r, sw, col); };
  A.zig = function (x, y, w, h, n, sw, col) { var p = [], i; for (i = 0; i <= n; i++) p.push([x + w * i / n, y + (i % 2 ? h : 0)]); return A.stroke('M' + p.map(function (q) { return f(q[0]) + ' ' + f(q[1]); }).join('L'), sw, col); };
  A.squig = function (x, y, w, h, n, sw, col) { var p = [], i; for (i = 0; i <= n * 4; i++) p.push([x + w * i / (n * 4), y + h * sin(i / 4 * PI * 2) * 0.5]); return A.stroke(A.smooth(p, false), sw, col); };
  /* rounded pill and capsule helpers */
  A.pill = function (x, y, w, h, fill, ex) { return A.rect(x, y, w, h, Math.min(w, h) / 2, fill, ex); };
  A.cap = function (x1, y1, x2, y2, sw, col) { return A.line(x1, y1, x2, y2, sw, col); };
  /* pick n distinct tones from a kit, seeded */
  A.tones = function (P, r, n) { var k = P.kit.slice(), o = []; while (n-- > 0 && k.length) o.push(k.splice(r.int(0, k.length - 1), 1)[0]); return o; };
  /* make(spec): engine renders a body, wrapped with page colour */
  A.make = function (s) {
    var w = s.w, h = s.h, mode = s.mode || 'light', P = A.palette(s.palette || 'brand', mode), key = (s.id || s.engine) + ':' + (s.seed || 0), r = A.rng(key);
    var uid = 'q' + (A.hash(key) % 100000), fn = A.engines[s.engine];
    if (!fn) throw new Error('unknown engine ' + s.engine);
    var body = fn({ w: w, h: h, P: P, r: r, uid: uid, subj: s.subj, o: s.o || {}, mode: mode, kind: s.kind });
    return A.svg(w, h, body, P.sky);
  };
})(typeof window !== 'undefined' ? window : globalThis);
