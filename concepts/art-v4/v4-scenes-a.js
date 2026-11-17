/* v4 scenes A: orbits, waveform, flow, nest, tessera, hex, kaleido, rise. Abstract and tonal. */
(function (g) {
  'use strict';
  var A = g.NebArtV4, E = A.engines, f = A.f, sin = Math.sin, cos = Math.cos, PI = Math.PI;
  var SH = ['cookie', 'flower', 'clover', 'burst', 'sunny', 'puffy', 'pebble', 'squircle', 'lotus', 'gem'];

  E.orbits = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), cx = w * r.range(0.6, 0.82), cy = h * r.range(0.42, 0.58), n = r.int(4, 6), R0 = m * 0.2, i, s = '', R, a, k, sh;
    s += A.shape(r.pick(['cookie', 'flower', 'puffy']), cx, cy, m * 1.02, r() * 3, P.t(0.07));
    for (i = 0; i < n; i++) {
      R = R0 + (i + 1) * m * 0.15;
      s += A.circle(cx, cy, R, 'none', 'stroke="' + (i % 2 ? P.t(0.22) : P.t(0.34)) + '" stroke-width="' + f(m * 0.011) + '"' + (i % 3 === 1 ? ' stroke-dasharray="' + f(m * 0.018) + ' ' + f(m * 0.032) + '"' : ''));
      for (k = 0; k < (i % 2 ? 1 : 2); k++) {
        a = r() * 6.28; sh = r.pick(SH);
        s += A.shape(sh, cx + R * cos(a), cy + R * sin(a), m * r.range(0.035, 0.075), r() * 3, r.chance(0.25) ? P.pop : P.t(r.range(0.4, 0.8)));
      }
    }
    s += A.shape(r.pick(['circle', 'pebble', 'cookie']), cx, cy, R0 * 0.82, 0.3, P.t(0.62));
    s += A.clip(c.uid + 'p', A.shapeD('circle', cx, cy, R0 * 0.82, 0), [0.15, 0.32, 0.5].map(function (v, j) { return A.rect(cx - R0, cy - R0 * 0.82 + R0 * 1.64 * v, R0 * 2, R0 * 0.2 * (1 + j * 0.3), 0, j % 2 ? P.t(0.74) : P.t(0.5)); }).join(''));
    s += A.shape('flower', cx - R0 * 0.3, cy - R0 * 0.3, R0 * 0.22, 0, P.pop);
    return s + A.dots(r, w, h, P.t(0.4), 26, m * 0.004, m * 0.008) + A.sparkle(w * 0.1, h * 0.25, m * 0.04, P.pop) + A.sparkle(w * 0.2, h * 0.78, m * 0.025, P.t(0.5));
  };

  E.waveform = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), n = r.int(7, 10), i, s = '', y, th = h / (n - 1.5), ph = r() * 6, len = r.range(w * 0.45, w * 0.9), amp = th * r.range(0.5, 0.9), hr = r.range(0, 0.5);
    for (i = 0; i < n; i++) {
      y = -th * 0.5 + i * th * 0.95;
      s += A.band(A.wave(-40, w + 40, y, amp, len, ph + i * 0.5, 22, hr), A.wave(-40, w + 40, y + th * 1.1, amp, len, ph + (i + 1) * 0.5, 22, hr), i === n - 2 && r.chance(0.7) ? P.pop : P.t(0.06 + 0.9 * i / n));
    }
    for (i = 0; i < 5; i++) s += A.shape(r.pick(SH), w * r.range(0.1, 0.9), h * r.range(0.1, 0.9), m * r.range(0.03, 0.06), r() * 3, r.chance(0.5) ? P.snow : P.pop);
    return s;
  };

  E.flow = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), nz = A.noise(r.int(1, 9999)), N = Math.round(12 + (w * h) / (m * m) * 7), i, j, b, s = '', x, y, a, pts, sw = m * r.range(0.035, 0.05), col, fl = r.range(0.7, 1.3) / m, st = m * 0.09, off, bn;
    for (i = 0; i < N; i++) {
      x = r.range(-0.1, 1.1) * w; y = r.range(-0.1, 1.1) * h; pts = [[x, y]];
      for (j = 0; j < 16; j++) { a = nz(x * fl + 7) * 4.6 + 1.2 + nz(y * fl * 0.6 + 91) * 1.2; x += cos(a) * st; y += sin(a) * st; pts.push([x, y]); }
      bn = r.int(2, 3); col = r.chance(0.2) ? P.pop : P.t(r.range(0.1, 0.85));
      for (b = 0; b < bn; b++) { off = (b - (bn - 1) / 2) * sw * 1.5; s += A.stroke(A.smooth(pts.map(function (q) { return [q[0] + off * 0.6, q[1] + off]; }), false), sw, b === bn - 1 && bn > 2 ? A.mix(col, P.sky, 0.45) : col); }
    }
    return s;
  };

  E.nest = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), s = '', cl = r.int(1, 3), q, i, cx, cy, n, sh, rot, R;
    for (q = 0; q < cl; q++) {
      cx = w * (cl === 1 ? r.range(0.55, 0.8) : (q + 0.5) / cl + r.range(-0.08, 0.08)); cy = h * r.range(0.35, 0.65); R = m * (cl === 1 ? r.range(0.55, 0.75) : r.range(0.4, 0.6)); n = r.int(5, 8); sh = r.pick(SH); rot = r() * 3;
      for (i = 0; i < n; i++) s += A.shape(sh, cx, cy, R * (1 - i / n * 0.92), rot + i * 0.16, i === n - 1 && r.chance(0.7) ? P.pop : P.t(0.06 + 0.84 * (i + (q % 2) * 0.5) / n));
    }
    return s + A.dots(r, w, h, P.t(0.5), 24, m * 0.004, m * 0.009);
  };

  E.tessera = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), cs = m / r.int(3, 5), s = '', x, y, t, k, col, bg, rot, cx, cy, tp, popRate = 0.07, cols = Math.ceil(w / cs), rows = Math.ceil(h / cs), j, i;
    var kit = P.kit.concat([P.t(0.02), P.t(0.14)]);
    for (j = 0; j < rows; j++) for (i = 0; i < cols; i++) {
      x = i * cs; y = j * cs; cx = x + cs / 2; cy = y + cs / 2; tp = r.int(0, 6); bg = r.pick(kit); col = r.chance(popRate) ? P.pop : r.pick(kit);
      if (col === bg) col = P.snow; rot = r.int(0, 3) * 90;
      s += A.rect(x - 0.4, y - 0.4, cs + 0.8, cs + 0.8, 0, bg);
      if (tp === 0) s += A.rot(rot, cx, cy, A.path('M' + f(x) + ' ' + f(y) + 'H' + f(x + cs) + 'A' + f(cs) + ' ' + f(cs) + ' 0 0 1 ' + f(x) + ' ' + f(y + cs) + 'Z', col));
      else if (tp === 1) s += A.circle(cx, cy, cs * 0.36, col);
      else if (tp === 2) s += A.rot(rot, cx, cy, A.path('M' + f(x) + ' ' + f(y + cs) + 'A' + f(cs / 2) + ' ' + f(cs / 2) + ' 0 0 1 ' + f(x + cs) + ' ' + f(y + cs) + 'Z', col));
      else if (tp === 3) s += A.rot(rot, cx, cy, A.pill(x + cs * 0.22, y + cs * 0.05, cs * 0.56, cs * 0.9, col));
      else if (tp === 4) s += A.rot(rot, cx, cy, A.path('M' + f(x) + ' ' + f(y) + 'A' + f(cs) + ' ' + f(cs) + ' 0 0 1 ' + f(x + cs) + ' ' + f(y + cs) + 'A' + f(cs) + ' ' + f(cs) + ' 0 0 1 ' + f(x) + ' ' + f(y) + 'Z', col));
      else if (tp === 5) s += A.shape(r.pick(SH), cx, cy, cs * 0.4, r() * 3, col);
    }
    return s;
  };

  E.hex = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), R = m / r.range(3.4, 5), s = '', dx = R * 1.732, dy = R * 1.5, j, i, x, y, t, kit = P.kit;
    for (j = -1; j < h / dy + 1; j++) for (i = -1; i < w / dx + 1; i++) {
      x = i * dx + (j % 2 ? dx / 2 : 0); y = j * dy; t = r();
      if (t < 0.12) continue;
      if (t < 0.5) s += A.path(A.ngon(6, x, y, R * 0.93, PI / 6, R * 0.2), P.t(0.06 + r() * 0.3));
      else if (t < 0.78) s += A.path(A.ngon(6, x, y, R * 0.93, PI / 6, R * 0.2), r.pick(kit)) + A.path(A.ngon(6, x, y, R * 0.5, PI / 6, R * 0.12), P.t(0.04));
      else if (t < 0.9) s += A.path(A.ngon(6, x, y, R * 0.8, PI / 6, R * 0.18), 'none', 'stroke="' + P.t(0.4) + '" stroke-width="' + f(R * 0.09) + '"') + A.circle(x, y, R * 0.2, P.t(0.5));
      else s += A.path(A.ngon(6, x, y, R * 0.93, PI / 6, R * 0.2), P.pop) + A.circle(x, y, R * 0.28, P.snow);
    }
    return s;
  };

  E.kaleido = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), cx = w * r.range(0.5, 0.78), cy = h * r.range(0.4, 0.6), s = '', L, k, n, i, ww, a, Ls = m * r.range(0.6, 0.78), pt;
    s += A.circle(cx, cy, Ls * 1.05, P.t(0.08));
    for (k = 0; k < 4; k++) {
      n = r.int(7, 14); L = Ls * (1 - k * 0.2); ww = L * r.range(0.14, 0.24); a = r() * 6; pt = k === 2 && r.chance(0.6) ? P.pop : P.t(0.18 + k * 0.2);
      for (i = 0; i < n; i++) s += A.rot(a * 57 + i * 360 / n, cx, cy, A.path('M' + f(cx) + ' ' + f(cy) + 'C' + f(cx - ww) + ' ' + f(cy - L * 0.3) + ' ' + f(cx - ww) + ' ' + f(cy - L * 0.9) + ' ' + f(cx) + ' ' + f(cy - L) + 'C' + f(cx + ww) + ' ' + f(cy - L * 0.9) + ' ' + f(cx + ww) + ' ' + f(cy - L * 0.3) + ' ' + f(cx) + ' ' + f(cy) + 'Z', pt));
    }
    s += A.shape(r.pick(SH), cx, cy, Ls * 0.16, r() * 3, P.snow) + A.circle(cx, cy, Ls * 0.06, P.pop);
    return s + A.dots(r, w, h, P.t(0.45), 20, m * 0.004, m * 0.008);
  };

  E.rise = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), n = Math.round(w / m * 5) + 4, i, s = '', bw = w / (n * 1.45), x, bh, y, pts = [], col;
    s += A.dots(r, w, h, P.t(0.2), 90, m * 0.004, m * 0.006);
    for (i = 0; i < n; i++) {
      bh = h * (0.22 + 0.62 * (i + 1) / n) * r.range(0.8, 1.05); x = w * 0.06 + i * (w * 0.88 / n); y = h * 0.94 - bh - (i % 2) * h * 0.04; col = i === n - 2 ? P.pop : P.t(0.16 + 0.1 * (i % 4) + 0.04 * i / n * 3);
      s += A.pill(x, y, bw, bh, col) + A.circle(x + bw / 2, y + bw / 2, bw * 0.26, P.t(0.04));
      pts.push([x + bw / 2, y - bw * 0.7]);
    }
    s += A.stroke(A.smooth(pts, false), m * 0.012, P.ink, 'stroke-dasharray="' + f(m * 0.02) + ' ' + f(m * 0.03) + '"');
    s += A.shape('burst', pts[n - 1][0], pts[n - 1][1], m * 0.07, 0, P.popSoft) + A.sparkle(pts[n - 1][0], pts[n - 1][1], m * 0.04, P.pop);
    return s;
  };
})(typeof window !== 'undefined' ? window : globalThis);
