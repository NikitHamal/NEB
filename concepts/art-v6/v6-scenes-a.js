/* v6 scenes A: truchet, bauhaus, voronoi (stained glass), lowpoly (facets), silk (ribbons), vortex (twisted echoes). Size agnostic, flat. */
(function (g) {
  'use strict';
  var A = g.NebArtV6, E = A.engines, f = A.f, sin = Math.sin, cos = Math.cos, PI = Math.PI;
  function up(c, p) { return A.scheme(c.P, c.r, A.pickDeep(c, p)); }

  E.truchet = function (c) {
    var w = c.w, h = c.h, r = c.r, S = up(c, 0.35), cell = Math.max(w, h) / (w > h ? r.int(9, 14) : r.int(5, 8)), cols = Math.ceil(w / cell) + 1, rows = Math.ceil(h / cell) + 1, s = A.rect(0, 0, w, h, 0, S.bg), i, j, x, y, o, rr = cell / 2, sw = cell * r.range(0.3, 0.42);
    var cs = [S.ramp[2], S.ramp[4], S.acc[0], S.ramp[3]], fills = [S.ramp[0], S.ramp[1]], bold = r.chance(0.5);
    for (j = 0; j < rows; j++) for (i = 0; i < cols; i++) {
      x = i * cell; y = j * cell; o = r() < 0.5 ? 1 : 0;
      if (bold && r() < 0.5) s += A.rect(x, y, cell, cell, 0, r.pick(fills));
      var a = o ? 'M' + f(x + rr) + ' ' + f(y) + 'A' + f(rr) + ' ' + f(rr) + ' 0 0 0 ' + f(x + cell) + ' ' + f(y + rr) + 'M' + f(x + rr) + ' ' + f(y + cell) + 'A' + f(rr) + ' ' + f(rr) + ' 0 0 0 ' + f(x) + ' ' + f(y + rr)
        : 'M' + f(x + rr) + ' ' + f(y) + 'A' + f(rr) + ' ' + f(rr) + ' 0 0 1 ' + f(x) + ' ' + f(y + rr) + 'M' + f(x + rr) + ' ' + f(y + cell) + 'A' + f(rr) + ' ' + f(rr) + ' 0 0 1 ' + f(x + cell) + ' ' + f(y + rr);
      s += A.stroke(a, sw, r() < 0.12 ? S.acc[0] : cs[(i + j + (r() < 0.3 ? 1 : 0)) % 3 === 0 ? 0 : (i * 7 + j * 3) % 2 ? 1 : 3]);
    }
    return s;
  };

  E.bauhaus = function (c) {
    var w = c.w, h = c.h, r = c.r, S = up(c, 0.3), rowsN = w / h > 1.4 ? r.int(3, 4) : r.int(3, 5), cell = h / rowsN, cols = Math.ceil(w / cell), s = A.rect(0, 0, w, h, 0, S.bg), i, j, x, y, m, k, col, bgc, cx, cy, q = cell;
    var pool = S.ramp.concat([S.acc[0], S.acc[0], S.acc[1]]);
    for (j = 0; j < rowsN; j++) for (i = 0; i < cols; i++) {
      x = i * cell; y = j * cell; cx = x + q / 2; cy = y + q / 2; m = r.int(0, 8); bgc = r.chance(0.55) ? r.pick(S.ramp.slice(0, 3)) : null; col = r.pick(pool);
      if (bgc) s += A.rect(x, y, q, q, 0, bgc);
      var inner = '';
      if (m === 0) inner = A.path('M' + f(x) + ' ' + f(y) + 'H' + f(x + q) + 'A' + f(q) + ' ' + f(q) + ' 0 0 1 ' + f(x) + ' ' + f(y + q) + 'Z', col);
      else if (m === 1) inner = A.path('M' + f(x) + ' ' + f(y + q / 2) + 'A' + f(q / 2) + ' ' + f(q / 2) + ' 0 0 1 ' + f(x + q) + ' ' + f(y + q / 2) + 'Z', col);
      else if (m === 2) inner = A.circle(cx, cy, q * 0.42, col);
      else if (m === 3) inner = A.circle(cx, cy, q * 0.32, 'none', 'stroke="' + col + '" stroke-width="' + f(q * 0.16) + '"') + A.circle(cx, cy, q * 0.1, col);
      else if (m === 4) for (k = 0; k < 3; k++) inner += A.rect(x + q * 0.12, y + q * (0.14 + k * 0.28), q * 0.76, q * 0.16, q * 0.08, col);
      else if (m === 5) inner = A.rect(x + q * 0.14, y + q * 0.14, q * 0.72, q * 0.72, q * 0.22, col);
      else if (m === 6) inner = A.path('M' + f(x + q * 0.06) + ' ' + f(y + q * 0.94) + 'L' + f(x + q * 0.94) + ' ' + f(y + q * 0.94) + 'L' + f(x + q * 0.94) + ' ' + f(y + q * 0.06) + 'Z', col);
      else if (m === 8) inner = A.path('M' + f(x) + ' ' + f(y) + 'A' + f(q) + ' ' + f(q) + ' 0 0 1 ' + f(x + q) + ' ' + f(y + q) + 'L' + f(x) + ' ' + f(y + q) + 'Z', col, 'opacity=".9"');
      s += A.rot(90 * r.int(0, 3), cx, cy, inner);
    }
    return s;
  };

  E.voronoi = function (c) {
    var w = c.w, h = c.h, r = c.r, S = up(c, 0.25), nx = Math.max(4, Math.round(w / h * 3.6)), ny = 4, i, j, sites = [], polys, fl = A.field(c.uid, 1 / w * 3, 1 / h * 3), s = A.rect(0, 0, w, h, 0, S.bg), cw = w / nx, ch = h / ny;
    for (j = 0; j < ny; j++) for (i = 0; i < nx; i++) sites.push([(i + 0.5 + r.range(-0.36, 0.36)) * cw, (j + 0.5 + r.range(-0.36, 0.36)) * ch]);
    polys = A.voronoi(sites, w, h);
    polys.forEach(function (p) {
      if (p.length < 3) return; var ce = A.centroid(p), t = fl(ce[0], ce[1]), idx = Math.min(5, Math.max(0, Math.floor(t * 6 + r.range(-0.6, 0.6)))), fill = r.chance(0.1) ? r.pick(S.acc) : S.ramp[idx];
      s += A.path(A.rpoly(p, Math.min(w, h) * 0.018), fill, 'stroke="' + S.bg + '" stroke-width="' + f(Math.min(w, h) * 0.012) + '" stroke-linejoin="round"');
      if (r.chance(0.18)) s += A.circle(ce[0], ce[1], Math.min(cw, ch) * r.range(0.07, 0.15), S.card);
    });
    return s;
  };

  E.lowpoly = function (c) {
    var w = c.w, h = c.h, r = c.r, S = up(c, 0.25), cn = Math.max(5, Math.round(w / h * 5)), rn = 5, cw = w / cn, ch = h / rn, pts = [], i, j, s = A.rect(0, 0, w, h, 0, S.bg), fl = A.field(c.uid, 2 / w, 2 / h);
    for (j = 0; j <= rn; j++) { pts[j] = []; for (i = 0; i <= cn; i++) pts[j][i] = [i * cw + (i > 0 && i < cn ? r.range(-0.3, 0.3) * cw : 0), j * ch + (j > 0 && j < rn ? r.range(-0.3, 0.3) * ch : 0)]; }
    function tri(a, b, d) {
      var m = [(a[0] + b[0] + d[0]) / 3, (a[1] + b[1] + d[1]) / 3], t = (fl(m[0], m[1]) - 0.22) * 1.9 + (m[0] / w) * 0.2 + r.range(-0.07, 0.07), idx = Math.min(5, Math.max(0, Math.floor(t * 6))), fill = r.chance(0.035) ? S.acc[0] : S.ramp[idx];
      s += A.poly([a, b, d], fill, 'stroke="' + fill + '" stroke-width="1.6" stroke-linejoin="round"');
    }
    for (j = 0; j < rn; j++) for (i = 0; i < cn; i++) {
      var a = pts[j][i], b = pts[j][i + 1], d = pts[j + 1][i + 1], e = pts[j + 1][i];
      if (r() < 0.5) { tri(a, b, d); tri(a, d, e); } else { tri(a, b, e); tri(b, d, e); }
    }
    return s;
  };

  E.silk = function (c) {
    var w = c.w, h = c.h, r = c.r, S = up(c, 0.3), L = Math.hypot(w, h), n = r.int(8, 13), bh = L / n, step = L / 36, ang = r.pick([-62, -34, -18, 24, 66, 112]), s = '', i, x, k, a1 = bh * r.range(0.9, 1.7), l1 = L * r.range(0.28, 0.5), l2 = L * r.range(0.12, 0.24), p1 = r() * 6, p2 = r() * 6, curves = [];
    for (i = 0; i <= n; i++) {
      var pts = [], amp = a1 * (0.55 + 0.9 * sin(i * 0.55 + p1));
      for (x = -step * 2; x <= L + step * 2; x += step) pts.push([x - (L - w) / 2, -(L - h) / 2 + i * bh - bh + amp * sin(x / l1 * PI * 2 + p1 + i * 0.22) + a1 * 0.35 * sin(x / l2 * PI * 2 + p2 - i * 0.3)]);
      curves.push(pts);
    }
    var rc = (i0) => i0; s = A.rect(-L, -L, L * 3, L * 3, 0, S.bg);
    var body = '';
    for (i = 0; i < n; i++) body += A.band(curves[i], curves[i + 1], r.chance(0.12) ? S.acc[i % 3] : S.ramp[(i * (r.chance(0.5) ? 1 : 2) + r.int(0, 1)) % 6]);
    return s + A.rot(ang, w / 2, h / 2, body);
  };

  /* twisted echoes: one expressive petal outline repeated, scaled and turned, so it reads as a vortex of paper */
  E.vortex = function (c) {
    var w = c.w, h = c.h, r = c.r, S = up(c, 0.4), m = Math.min(w, h), cx = c.o.side === 'left' ? w * 0.25 : c.o.side === 'center' ? w / 2 : w * (w / h > 1.5 ? 0.72 : 0.5), cy = h / 2, s = A.rect(0, 0, w, h, 0, S.bg), np = r.int(4, 8), N = r.int(12, 19), amp = r.range(0.14, 0.3), twist = r.range(0.25, 0.7), big = m * (w / h > 1.5 ? 0.78 : 0.62), k, t;
    for (k = N; k >= 1; k--) {
      var u = k / N, pts = [], col = k % 6 === 0 ? S.acc[k % 3] : S.ramp[Math.min(5, Math.floor((1 - u) * 5.99))];
      for (t = 0; t < 72; t++) { var q = t / 72 * PI * 2, rd = big * u * (1 + amp * cos(np * q + u * twist * 6)); pts.push([cx + rd * cos(q), cy + rd * sin(q)]); }
      s += A.path(A.smooth(pts, true), col);
    }
    return s + A.circle(cx, cy, m * 0.035, S.card);
  };
})(typeof window !== 'undefined' ? window : globalThis);
