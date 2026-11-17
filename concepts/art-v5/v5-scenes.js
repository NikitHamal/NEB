/* v5 scenes: 14 calm abstract compositions made of a few large shapes. Tonal ramp of one hue (optional analogous alt). No scattered dots. */
(function (g) {
  'use strict';
  var A = g.NebArtV5, E = A.engines, f = A.f, sin = Math.sin, cos = Math.cos, PI = Math.PI;
  function T(c) { var P = c.P, o = c.o; if (o.soft) return [P.bg, P.s1, P.s2, P.s2, P.hi]; var a = o.alt ? P.alt : P; return [P.s1, P.s2, P.hi, a.m, a.d]; }
  function shuffle(r, a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(r() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  E.ribbons = function (c) {
    var t = T(c), w = c.w, h = c.h, r = c.r, n = 5, s = A.rect(0, 0, w, h, 0, t[0]), i, pts, x;
    for (i = 0; i < n; i++) { pts = []; var y = h * (0.18 + i * 0.17), am = h * r.range(0.05, 0.11), len = w * r.range(0.55, 1.1), ph = r() * 6.28;
      for (x = -w * 0.3; x <= w * 1.3; x += w / 8) pts.push([x, y + am * sin(x / len * PI * 2 + ph)]);
      s += A.path(A.smooth(pts, false) + 'L' + f(w * 1.4) + ' ' + f(h + 20) + 'L' + f(-w * 0.4) + ' ' + f(h + 20) + 'Z', t[Math.min(i + 1, 4)]); }
    return s;
  };
  E.rings = function (c) {
    var t = T(c), w = c.w, h = c.h, cx = w * (c.o.bias || 0.7), cy = h * 0.52, s = A.rect(0, 0, w, h, 0, t[0]), i;
    for (i = 0; i < 5; i++) s += A.circle(cx - i * h * 0.03, cy, h * (0.98 - i * 0.17), t[i === 0 ? 1 : i]);
    return s;
  };
  E.pills = function (c) {
    var t = T(c), w = c.w, h = c.h, r = c.r, n = 9, hh = h * 0.17, s = '', i, len, x, col, cols = [t[1], t[2], t[3], t[4]];
    for (i = 0; i < n; i++) { len = w * r.range(0.4, 1.0); x = r() * (w * 1.4 - len) - w * 0.2; col = cols[(i + r.int(0, 1)) % 4]; s += A.rect(x, i * hh * 1.28 - h * 0.45, len, hh, hh / 2, col); }
    return A.rect(0, 0, w, h, 0, t[0]) + A.clipRect(c.uid + 'p', 0, 0, w, h, 0, A.rot(-26, w / 2, h / 2, s));
  };
  E.arches = function (c) {
    var t = T(c), w = c.w, h = c.h, r = c.r, n = Math.max(5, Math.round(w / (h * 0.3))), cw = w / n, s = A.rect(0, 0, w, h, 0, t[0]), i, ah, ph = r() * 6;
    for (i = 0; i < n; i++) { ah = h * (0.5 + 0.4 * (0.5 + 0.5 * sin(i * 0.9 + ph))); s += A.arch(i * cw + cw * 0.04, h - ah, cw * 0.92, ah + 2, t[1 + i % 3]); }
    return s;
  };
  E.blobs = function (c) {
    var t = T(c), w = c.w, h = c.h, r = c.r, s = A.rect(0, 0, w, h, 0, t[0]), i, cx = w * (c.o.bias || 0.55);
    for (i = 0; i < 3; i++) s += A.path(A.blob(r, cx + (i - 1) * w * 0.26, h * (0.5 + (i % 2 ? 0.12 : -0.1)), h * (0.62 - i * 0.07), 0.2), t[i + 1]);
    return s;
  };
  E.petals = function (c) {
    var t = T(c), w = c.w, h = c.h, r = c.r, cx = w * (c.o.bias || 0.68), cy = h * 0.5, R = h * 0.7, a0 = r() * 3;
    return A.rect(0, 0, w, h, 0, t[0]) + A.path(A.cookie(w * 0.12, h * 0.95, R * 0.9, 7, 0.14, a0), t[1]) + A.path(A.cookie(cx, cy, R, 8, 0.15, a0), t[2]) + A.path(A.cookie(cx, cy, R * 0.68, 8, 0.15, a0 + 0.39), t[3]) + A.circle(cx, cy, R * 0.3, t[4]);
  };
  E.quarters = function (c) {
    var t = T(c), w = c.w, h = c.h, r = c.r, rows = r.int(3, 4), ts = h / rows, cols = Math.ceil(w / ts), s = A.rect(0, 0, w, h, 0, t[0]), i, j, x, y, k, col;
    for (j = 0; j < rows; j++) for (i = 0; i < cols; i++) { x = i * ts; y = j * ts; k = r.int(0, 4); col = r() < 0.5 ? t[2] : t[4]; if (k === 4) continue;
      s += A.rot(k * 90, x + ts / 2, y + ts / 2, A.path('M' + f(x) + ' ' + f(y) + 'H' + f(x + ts) + 'A' + f(ts) + ' ' + f(ts) + ' 0 0 1 ' + f(x) + ' ' + f(y + ts) + 'Z', col)); }
    return A.clipRect(c.uid + 'q', 0, 0, w, h, 0, s);
  };
  E.capsules = function (c) {
    var t = T(c), w = c.w, h = c.h, n = Math.max(6, Math.round(w / (h * 0.16))), cw = w / n, s = A.rect(0, 0, w, h, 0, t[0]), i, ch;
    for (i = 0; i < n; i++) { ch = h * (0.3 + 0.62 * i / (n - 1)); s += A.rect(i * cw + cw * 0.12, h - ch, cw * 0.76, ch + cw, cw * 0.38, t[1 + i % 4]); }
    return s;
  };
  E.scallop = function (c) {
    var t = T(c), w = c.w, h = c.h, rr = h / 5, s = A.rect(0, 0, w, h, 0, t[0]), i, j;
    for (j = 0; j < 8; j++) for (i = -1; i < w / rr + 1; i++) s += A.circle(i * rr * 1.2 + (j % 2) * rr * 0.6, j * rr * 0.55, rr * 0.62, t[1 + (j % 4)]);
    return A.clipRect(c.uid + 's', 0, 0, w, h, 0, s);
  };
  E.fold = function (c) {
    var t = T(c), w = c.w, h = c.h, r = c.r, s = A.rect(0, 0, w, h, 0, t[0]), i, sz = h * 0.82;
    for (i = 0; i < 4; i++) s += A.rot(r.range(-24, 24), w * (0.3 + i * 0.2), h * 0.5, A.rect(w * (0.3 + i * 0.2) - sz / 2, h * 0.5 - sz / 2, sz, sz, sz * 0.2, t[i + 1]));
    return A.clipRect(c.uid + 'f', 0, 0, w, h, 0, s);
  };
  E.graph = function (c) {
    var t = T(c), w = c.w, h = c.h, sp = h / 10, s = A.rect(0, 0, w, h, 0, t[0]), x, y, cx = w * (c.o.bias || 0.66);
    for (x = 0; x < w; x += sp) s += A.line(x, 0, x, h, 1.6, t[1]);
    for (y = 0; y < h; y += sp) s += A.line(0, y, w, y, 1.6, t[1]);
    return s + A.path(A.cookie(cx, h * 0.5, h * 0.4, 8, 0.14, 0.2), t[3]) + A.circle(cx, h * 0.5, h * 0.2, t[0]) + A.circle(cx, h * 0.5, h * 0.1, t[4]);
  };
  E.halves = function (c) {
    var t = T(c), w = c.w, h = c.h, r = c.r, ts = h / r.int(3, 4), cols = Math.ceil(w / ts), rows = Math.ceil(h / ts), s = A.rect(0, 0, w, h, 0, t[0]), i, j, k, x, y;
    for (j = 0; j < rows; j++) for (i = 0; i < cols; i++) { x = i * ts; y = j * ts; k = r.int(0, 3); s += A.rot(k * 90, x + ts / 2, y + ts / 2, A.path('M' + f(x) + ' ' + f(y + ts) + 'A' + f(ts / 2) + ' ' + f(ts / 2) + ' 0 0 1 ' + f(x + ts) + ' ' + f(y + ts) + 'Z', t[(i + j) % 2 ? 2 : 4])); }
    return A.clipRect(c.uid + 'h', 0, 0, w, h, 0, s);
  };
  E.sweep = function (c) {
    var t = T(c), w = c.w, h = c.h, s = A.rect(0, 0, w, h, 0, t[0]), i, R = Math.max(w, h) * 0.9, cx = c.o.flip ? w : 0, cy = h;
    for (i = 0; i < 6; i++) s += A.circle(cx, cy, R * (1 - i * 0.16), t[1 + (i % 4)]);
    return s;
  };
  E.swirl = function (c) {
    var t = T(c), w = c.w, h = c.h, r = c.r, s = A.rect(0, 0, w, h, 0, t[0]), i, cx = w * (c.o.bias || 0.6);
    for (i = 0; i < 4; i++) s += A.rot(i * 22 + r() * 8, cx, h / 2, A.rect(cx - h * (0.72 - i * 0.12), h / 2 - h * (0.72 - i * 0.12), h * (1.44 - i * 0.24), h * (1.44 - i * 0.24), h * (0.4 - i * 0.04), t[1 + i]));
    return s;
  };
  A.SCENES = ['ribbons', 'rings', 'pills', 'arches', 'blobs', 'petals', 'quarters', 'capsules', 'scallop', 'fold', 'graph', 'halves', 'sweep', 'swirl'];
})(typeof window !== 'undefined' ? window : globalThis);
