/* v3 scenes B: monsoon, twilight, campus, skyline, river valley, contour, dunes, orchard. */
(function (g) {
  'use strict';
  var A = g.NebArtV3, E = A.engines, R = A.rect, C = A.circle, f = A.f, H = A.helpers;

  E.monsoon = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = R(0, 0, w, h, 0, P.t(0.18)), i, n = Math.round(w / h * 9);
    for (i = 0; i < 3; i++) o += R(0, h * i * 0.12, w, h * 0.12, 0, P.t(0.2 + i * 0.07));
    for (i = 0; i < n; i++) o += H.cloud(r.range(0, 1) * w, h * r.range(0.05, 0.4), h * r.range(0.14, 0.26), P.dark ? P.t(0.3 + r.range(0, 0.15)) : P.t(r.range(0.02, 0.16)));
    for (i = 0; i < n * 7; i++) { var x = r.range(0, 1) * w, y = h * r.range(0.3, 0.85), l = h * r.range(0.04, 0.08); o += A.line(x, y, x - l * 0.25, y + l, 2.2, P.t(0.55), ''); }
    o += H.peaks(c, h * 0.8, h * 0.1, h * 0.2, Math.round(w / h * 3), P.depth(0.5)) + A.fillTo(A.ridge(r, -20, w + 20, h * 0.9, h * 0.06, 0.012, 3), h, P.depth(0.9));
    var ux = w * r.range(0.3, 0.7), uy = h * 0.78, s = h * 0.2;
    return o + A.path('M' + f(ux - s * 0.6) + ' ' + f(uy - s * 0.5) + 'Q' + f(ux) + ' ' + f(uy - s * 1.2) + ' ' + f(ux + s * 0.6) + ' ' + f(uy - s * 0.5) + 'Q' + f(ux + s * 0.3) + ' ' + f(uy - s * 0.4) + ' ' + f(ux) + ' ' + f(uy - s * 0.5) + 'Q' + f(ux - s * 0.3) + ' ' + f(uy - s * 0.4) + ' ' + f(ux - s * 0.6) + ' ' + f(uy - s * 0.5) + 'Z', P.sp(0.55)) + A.line(ux, uy - s * 0.5, ux, uy + s * 0.2, 2.5, P.ink);
  };
  E.twilight = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = '', i, bands = 5;
    for (i = 0; i < bands; i++) o += R(0, h * i * 0.2, w, h * 0.22, 0, P.dark ? P.t(0.05 + i * 0.05) : P.t(0.55 - i * 0.1));
    for (i = 0; i < Math.round(w * h / 9000); i++) o += r.chance(0.3) ? A.star4(r.range(0, 1) * w, r.range(0, 0.6) * h, r.range(3, 7), P.snow) : C(r.range(0, 1) * w, r.range(0, 0.65) * h, r.range(0.8, 1.8), P.snow);
    var mx = w * r.range(0.65, 0.85), my = h * 0.24, mr = h * 0.1;
    o += C(mx, my, mr * 1.8, P.dark ? P.t(0.18) : P.t(0.62)) + C(mx, my, mr, P.dark ? P.snow : P.sun) + C(mx + mr * 0.4, my - mr * 0.2, mr * 0.85, P.dark ? P.t(0.12) : P.t(0.5));
    o += H.peaks(c, h * 0.78, h * 0.15, h * 0.32, Math.round(w / h * 2.4), P.dark ? P.t(0.3) : P.t(0.72), P.dark ? P.t(0.5) : P.t(0.55)) + A.fillTo(A.ridge(r, -20, w + 20, h * 0.84, h * 0.06, 0.01, 3), h, P.dark ? P.t(0.12) : P.t(0.88));
    for (i = 0; i < Math.round(w / h * 5); i++) o += H.tree(r.range(0, 1) * w, h * 0.99, h * r.range(0.16, 0.3), P.dark ? P.t(0.06) : P.t(0.96), P.dark ? P.t(0.06) : P.t(0.96), 'pine');
    return o;
  };
  E.campus = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = R(0, 0, w, h, 0, P.sky), cx = w * r.range(0.4, 0.6), gy = h * 0.8, bw = Math.min(w * 0.5, h * 1.3), bh = h * 0.38, i;
    o += H.sun(c, w * r.range(0.1, 0.9), h * 0.2, h * 0.06) + H.cloud(w * 0.2, h * 0.22, h * 0.09, P.dark ? P.depth(0.2) : '#fff') + H.peaks(c, gy, h * 0.12, h * 0.28, Math.round(w / h * 3), P.depth(0.2), P.snow) + R(0, gy, w, h - gy, 0, P.t(0.3));
    o += R(cx - bw / 2, gy - bh, bw, bh, 4, P.paper) + R(cx - bw / 2 - bw * 0.14, gy - bh * 0.7, bw * 0.16, bh * 0.7, 4, P.t(0.08)) + R(cx + bw / 2 - bw * 0.02, gy - bh * 0.7, bw * 0.16, bh * 0.7, 4, P.t(0.08));
    o += A.poly([[cx - bw * 0.3, gy - bh], [cx + bw * 0.3, gy - bh], [cx, gy - bh * 1.38]], P.t(0.58)) + R(cx - bw * 0.3, gy - bh * 1.02, bw * 0.6, bh * 0.05, 2, P.t(0.78));
    o += A.rect(cx - 1.5, gy - bh * 1.38 - h * 0.14, 3, h * 0.14, 1, P.ink) + A.poly([[cx + 2, gy - bh * 1.38 - h * 0.14], [cx + h * 0.1, gy - bh * 1.38 - h * 0.11], [cx + 2, gy - bh * 1.38 - h * 0.08]], P.sp(0.55));
    o += A.arch(cx - bw * 0.07, gy - bh * 0.42, bw * 0.14, bh * 0.42, P.t(0.7));
    for (i = 0; i < 4; i++) { var wx = cx - bw * 0.42 + i * bw * 0.2 + (i > 1 ? bw * 0.12 : 0); o += A.arch(wx, gy - bh * 0.78, bw * 0.07, bh * 0.3, P.t(0.3)) + A.arch(wx, gy - bh * 0.4, bw * 0.07, bh * 0.3, P.t(0.3)); }
    for (i = 0; i < 4; i++) o += R(cx - bw * (0.14 - i * 0.014), gy - h * 0.008 * (4 - i) - h * 0.01, bw * (0.28 - i * 0.028), h * 0.014, 2, P.t(0.45 - i * 0.07));
    o += A.poly([[cx - bw * 0.06, gy], [cx + bw * 0.06, gy], [cx + bw * 0.25, h], [cx - bw * 0.25, h]], P.t(0.1));
    o += H.tree(cx - bw * 0.78, gy + h * 0.1, h * 0.36, P.depth(0.8), P.depth(0.95), 'puff') + H.tree(cx + bw * 0.78, gy + h * 0.1, h * 0.4, P.depth(0.8), P.depth(0.95), 'puff');
    for (i = 0; i < 6; i++) o += A.shape('flower', r.range(0, 1) * w, h * r.range(0.9, 0.98), h * 0.018, 0, P.sp(0.4 + r.range(0, 0.3)));
    return o;
  };
  E.skyline = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = R(0, 0, w, h, 0, P.sky), L, x, bw, bh, i, j, base;
    o += H.sun(c, w * r.range(0.15, 0.85), h * 0.22, h * 0.06);
    for (L = 0; L < 3; L++) {
      base = h * (0.62 + L * 0.14); x = -10; var col = P.depth(0.2 + L * 0.35);
      while (x < w) {
        bw = h * r.range(0.1, 0.2); bh = h * r.range(0.16, 0.42 - L * 0.07);
        o += R(x, base - bh, bw, bh + h, r.chance(0.3) ? bw * 0.4 : 3, col);
        if (r.chance(0.35)) o += R(x + bw * 0.4, base - bh - h * 0.05, 3, h * 0.05, 1, col);
        if (L > 0) for (i = 0; i < Math.floor(bw / 16); i++) for (j = 0; j < Math.floor(bh / 24); j++) if (r.chance(0.38)) o += R(x + 8 + i * 16, base - bh + 10 + j * 24, 8, 11, 2, L === 2 ? P.sun : P.t(P.dark ? 0.6 : 0.15));
        x += bw + h * r.range(0.005, 0.03);
      }
    }
    return o;
  };
  E.river = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = R(0, 0, w, h, 0, P.t(0.12)), n = r.int(5, 8), i, x, pts, ph = r.range(0, 6), fr = r.range(1.5, 2.6) / w * 3.14;
    for (i = 0; i < n; i++) { pts = []; for (x = -30; x <= w + 40; x += 26) pts.push([x, h * (i / n) + Math.sin(x * fr + ph + i * 0.6) * h * 0.14 + Math.sin(x * fr * 2.7 + i) * h * 0.04]); o += A.fillTo(pts, h * 2, i % 2 ? P.t(0.18 + i / n * 0.28) : P.depth(0.2 + i / n * 0.3)); }
    pts = []; for (x = -30; x <= w + 40; x += 22) pts.push([x, h * 0.55 + Math.sin(x * fr * 1.4 + ph) * h * 0.2]);
    o += A.stroke(A.smooth(pts, false), h * 0.12, P.dark ? P.t(0.3) : P.sky.replace('#', '#')) + A.stroke(A.smooth(pts, false), h * 0.075, P.dark ? P.t(0.42) : P.t(0.36));
    for (i = 0; i < Math.round(w * h / 5000); i++) { x = r.range(0, 1) * w; var yy = r.range(0, 1) * h; o += C(x, yy, r.range(3, 7), P.depth(0.6 + r.range(0, 0.4))); }
    return o;
  };
  E.contour = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = R(0, 0, w, h, 0, P.t(0.04)), cs = r.int(1, 2), s, i, N = r.int(8, 12), k, a, pts, nz;
    for (s = 0; s < cs; s++) {
      var cx = w * r.range(0.2, 0.8), cy = h * r.range(0.3, 0.7), R0 = Math.max(w, h) * r.range(0.45, 0.7), n1 = A.noise(r.int(1, 9999));
      for (i = 0; i < N; i++) { k = 1 - i / N; pts = []; for (a = 0; a < 30; a++) { var t = a / 30 * Math.PI * 2; nz = n1(3 + Math.cos(t) * 1.6 + s * 9) + n1(5 + Math.sin(t) * 1.6 + s * 9); pts.push([cx + Math.cos(t) * R0 * k * (0.6 + nz * 0.5), cy + Math.sin(t) * R0 * k * (0.6 + nz * 0.5) * 0.8]); } o += A.path(A.smooth(pts, true), P.t(0.08 + (1 - k) * 0.6)); }
    }
    return o;
  };
  E.dunes = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = R(0, 0, w, h, 0, P.sky), i;
    o += H.sun(c, w * r.range(0.2, 0.8), h * 0.28, h * 0.09);
    for (i = 0; i < 6; i++) o += A.fillTo(A.ridge(r, -20, w + 20, h * (0.4 + i * 0.1), h * 0.1, 0.5 / w * 6, 2), h, i % 2 ? P.depth(0.15 + i * 0.14) : P.t(0.12 + i * 0.1));
    return o;
  };
  E.orchard = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = R(0, 0, w, h, 0, P.t(0.1)), rows = 6, i, j, n;
    for (i = 0; i < rows; i++) { var y = h * (0.15 + i * 0.16); o += R(0, y, w, h * 0.16, 0, i % 2 ? P.t(0.14) : P.t(0.22)); n = Math.round(w / h * (2.4 + i * 0.7)); for (j = 0; j < n; j++) { var x = (j + 0.5) / n * w; o += A.shape(r.pick(['puffy', 'circle', 'pebble']), x, y + h * 0.1, h * (0.045 + i * 0.01), r.range(0, 3), P.depth(0.55 + i * 0.07)) + C(x + h * 0.01, y + h * 0.09, h * 0.01, P.sp(0.4)); } }
    return o;
  };
})(typeof window !== 'undefined' ? window : globalThis);
