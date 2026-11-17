/* v4 scenes B: graph, network, cells, molecules, dna, ink, halftone, arcs. */
(function (g) {
  'use strict';
  var A = g.NebArtV4, E = A.engines, f = A.f, sin = Math.sin, cos = Math.cos, PI = Math.PI;
  var SH = ['cookie', 'flower', 'clover', 'burst', 'sunny', 'puffy', 'pebble', 'squircle', 'lotus', 'gem'];
  function sw(m, k, col) { return 'stroke="' + col + '" stroke-width="' + f(m * k) + '"'; }

  E.graph = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), s = '', i, x, gs = m / 6, n = r.int(2, 3), k, pts, ph, am, fr, y0, col, fn;
    for (x = gs / 2; x < w; x += gs) s += A.line(x, 0, x, h, m * 0.004, P.t(0.12));
    for (i = gs / 2; i < h; i += gs) s += A.line(0, i, w, i, m * 0.004, P.t(0.12));
    s += A.line(0, h * 0.62, w, h * 0.62, m * 0.012, P.t(0.4)) + A.line(w * 0.08, 0, w * 0.08, h, m * 0.012, P.t(0.4));
    for (k = 0; k < n; k++) {
      ph = r() * 6; am = h * r.range(0.14, 0.26); fr = w * r.range(0.35, 0.8); y0 = h * (0.4 + k * 0.1); fn = r.int(0, 2); pts = [];
      for (x = -30; x <= w + 60; x += 30) pts.push([x, y0 - am * (fn === 0 ? sin(x / fr * 6.28 + ph) : fn === 1 ? sin(x / fr * 6.28 + ph) * cos(x / fr * 3.1) : Math.pow(sin(x / fr * 3.14 + ph), 3))]);
      col = k === n - 1 ? P.pop : P.t(0.3 + k * 0.22);
      s += A.band(pts, pts.map(function (q) { return [q[0], h + 20]; }), col, 'fill-opacity="0.22"') + A.stroke(A.smooth(pts, false), m * 0.018, col);
      for (i = 2; i < pts.length - 3; i += r.int(4, 7)) s += A.circle(pts[i][0], pts[i][1], m * 0.026, P.card, sw(m, 0.012, col));
    }
    return s + A.sparkle(w * 0.88, h * 0.16, m * 0.05, P.pop);
  };

  E.network = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), N = Math.round(10 + w * h / (m * m) * 8), nd = [], i, j, t, s = '', e = '', d, q, tries, ok, rad;
    for (tries = 0; nd.length < N && tries < 800; tries++) { q = [r() * w, r() * h]; ok = nd.every(function (z) { return Math.hypot(z[0] - q[0], z[1] - q[1]) > m * 0.17; }); if (ok) nd.push(q); }
    nd.forEach(function (a, ia) {
      nd.map(function (b, ib) { return [ib, Math.hypot(a[0] - b[0], a[1] - b[1])]; }).sort(function (x, y) { return x[1] - y[1]; }).slice(1, 3).forEach(function (z) { e += A.line(a[0], a[1], nd[z[0]][0], nd[z[0]][1], m * 0.01, P.t(0.3)); });
    });
    s += e;
    nd.forEach(function (a, ia) { rad = m * (ia === 0 ? 0.1 : r.range(0.032, 0.062)); t = ia === 0 ? P.pop : P.t(r.range(0.3, 0.85));
      s += A.shape(ia === 0 ? 'flower' : r.pick(SH), a[0], a[1], rad, r() * 3, t) + A.circle(a[0], a[1], rad * 0.34, P.card); });
    return s;
  };

  E.cells = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), cs = [], i, t, s = '', R, x, y, ok, z;
    for (R = m * 0.3; R > m * 0.035; R *= 0.86) for (t = 0; t < 40; t++) { x = r() * w; y = r() * h; ok = cs.every(function (q) { return Math.hypot(q[0] - x, q[1] - y) > q[2] + R + m * 0.012; }); if (ok) { cs.push([x, y, R]); break; } }
    cs.forEach(function (q, k) {
      z = r.chance(0.12) ? P.pop : P.t(r.range(0.1, 0.5));
      s += A.path(A.blob(r, q[0], q[1], q[2], 0.07, 9), z) + A.path(A.blob(r, q[0] + q[2] * 0.1, q[1] + q[2] * 0.05, q[2] * 0.36, 0.14, 7), P.t(r.range(0.5, 0.85)));
      for (i = 0; i < 4; i++) s += A.circle(q[0] + cos(i * 1.7 + k) * q[2] * 0.62, q[1] + sin(i * 1.7 + k) * q[2] * 0.62, q[2] * 0.07, P.snow);
    });
    return s;
  };

  E.molecules = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), R = m * r.range(0.17, 0.24), n = Math.max(2, Math.round(w / (R * 3.2))), s = '', e = '', a = '', i, j, cx, cy, v, ang, k, rot = r() * 1.0, aR = m * 0.045;
    s += A.dots(r, w, h, P.t(0.22), 40, m * 0.004, m * 0.01);
    for (i = 0; i < n; i++) {
      cx = w * (i + 0.5) / n + r.range(-0.03, 0.03) * w; cy = h * (0.5 + (i % 2 ? 0.14 : -0.14)) + r.range(-0.05, 0.05) * h; v = [];
      for (j = 0; j < 6; j++) { ang = rot + j * PI / 3; v.push([cx + R * cos(ang), cy + R * sin(ang), ang]); }
      for (j = 0; j < 6; j++) { k = (j + 1) % 6; e += A.line(v[j][0], v[j][1], v[k][0], v[k][1], m * 0.016, P.t(0.45));
        if (j % 2 === 0) e += A.line(cx + (v[j][0] - cx) * 0.74 + (v[k][0] - v[j][0]) * 0.1, cy + (v[j][1] - cy) * 0.74 + (v[k][1] - v[j][1]) * 0.1, cx + (v[k][0] - cx) * 0.74 - (v[k][0] - v[j][0]) * 0.1, cy + (v[k][1] - cy) * 0.74 - (v[k][1] - v[j][1]) * 0.1, m * 0.01, P.t(0.45)); }
      a += A.path(A.ngon(6, cx, cy, R * 0.98, rot, R * 0.2), A.mix(P.t(0.12), P.sky, 0.2));
      v.forEach(function (p, q) {
        if (r.chance(0.4)) { e += A.line(p[0], p[1], p[0] + cos(p[2]) * R * 0.7, p[1] + sin(p[2]) * R * 0.7, m * 0.014, P.t(0.45)); a += A.circle(p[0] + cos(p[2]) * R * 0.7, p[1] + sin(p[2]) * R * 0.7, aR * 1.25, r.chance(0.5) ? P.pop : P.t(0.3)); }
        a += A.circle(p[0], p[1], aR, P.t(0.35 + 0.12 * (q % 3)));
      });
    }
    return s + a + e;
  };

  E.dna = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), s = '', q, n = r.int(1, 2), x, i, p1, p2, len, amp, y0, rot, rungs = '', st = m * 0.014;
    for (q = 0; q < n; q++) {
      y0 = h * (n === 1 ? 0.5 : 0.28 + q * 0.44); amp = m * r.range(0.14, 0.2) * (n === 1 ? 1.2 : 1); len = m * r.range(0.9, 1.3); rot = r.range(-14, 14); p1 = []; p2 = []; rungs = '';
      for (x = -w * 0.2; x <= w * 1.2; x += 12) { p1.push([x, y0 + amp * sin(x / len * 6.28)]); p2.push([x, y0 - amp * sin(x / len * 6.28)]); }
      for (x = -w * 0.2, i = 0; x <= w * 1.2; x += len / 10, i++) { var y1 = y0 + amp * sin(x / len * 6.28), y2 = y0 - amp * sin(x / len * 6.28); rungs += A.line(x, y1, x, y2, st * 0.8, P.t(0.28)) + A.circle(x, y1, st * 1.2, i % 3 ? P.t(0.55) : P.pop) + A.circle(x, y2, st * 1.2, i % 2 ? P.t(0.8) : P.t(0.4)); }
      s += A.rot(rot, w / 2, h / 2, A.stroke(A.smooth(p1, false), st * 2.6, P.t(0.5)) + A.stroke(A.smooth(p2, false), st * 2.6, P.t(0.78)) + rungs);
    }
    return A.dots(r, w, h, P.t(0.2), 36, m * 0.004, m * 0.01) + s;
  };

  E.ink = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), n = r.int(5, 8), i, s = '', x, y, d, col, wd;
    for (i = 0; i < n; i++) {
      x = r.range(-0.1, 0.5) * w; y = r.range(0.1, 0.95) * h; wd = m * r.range(0.1, 0.22); col = i === n - 2 ? P.pop : P.t(0.08 + 0.8 * i / n);
      d = 'M' + f(x) + ' ' + f(y) + 'C' + f(x + w * 0.25) + ' ' + f(y - h * r.range(0.2, 0.7)) + ' ' + f(x + w * 0.45) + ' ' + f(y + h * r.range(0.2, 0.7)) + ' ' + f(x + w * r.range(0.6, 1.1)) + ' ' + f(y + h * r.range(-0.3, 0.3));
      s += A.stroke(d, wd, col);
    }
    for (i = 0; i < 14; i++) s += A.circle(r() * w, r() * h, m * r.range(0.006, 0.03), r.chance(0.3) ? P.pop : P.t(0.5));
    return s;
  };

  E.halftone = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), sp = m / r.int(14, 20), s = '', x, y, v, a = r.range(1, 3) / m, b = r.range(1, 3) / m, ph = r() * 6, cx = w * r.range(0.3, 0.8), cy = h * r.range(0.3, 0.7), z, d;
    for (y = sp / 2; y < h; y += sp) for (x = sp / 2; x < w; x += sp) {
      d = Math.hypot(x - cx, (y - cy) * 1.2) / (m * 1.1); v = 0.5 + 0.5 * sin(d * 7 + ph + sin(x * a + y * b));
      z = v * sp * 0.52; if (z < sp * 0.06) continue;
      s += A.circle(x, y, z, v > 0.9 && d < 0.55 ? P.pop : P.t(0.3 + 0.5 * v));
    }
    return s;
  };

  E.arcs = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), n = Math.max(1, Math.round(w / m * 1.6)), q, i, k, cx, R, s = '', th, ang, ring;
    for (q = 0; q < n; q++) {
      cx = w * (q + 0.5) / n + r.range(-0.05, 0.05) * w; R = Math.min(w / n * 0.62, h * 0.95) * r.range(0.8, 1.1); k = r.int(4, 6); th = R / k; ang = r.chance(0.5) ? 0 : 1;
      for (i = 0; i < k; i++) { ring = R - i * th; s += A.path('M' + f(cx - ring) + ' ' + f(h * 1.02) + 'A' + f(ring) + ' ' + f(ring) + ' 0 0 1 ' + f(cx + ring) + ' ' + f(h * 1.02) + 'Z', i === k - 1 && r.chance(0.6) ? P.pop : P.t(0.1 + 0.12 * ((i + q) % 6))); }
      s += A.shape(r.pick(SH), cx + r.range(-0.3, 0.3) * R, h * 1.02 - R - m * 0.09, m * 0.05, r() * 3, P.t(0.6));
    }
    return A.dots(r, w, h, P.t(0.35), 30, m * 0.004, m * 0.009) + s;
  };
})(typeof window !== 'undefined' ? window : globalThis);
