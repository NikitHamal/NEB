/* v3 layered scenes A: Himalaya, terraces, Kathmandu valley, lake, meadow, forest. Depth ramp = atmospheric perspective. */
(function (g) {
  'use strict';
  var A = g.NebArtV3, E = A.engines, R = A.rect, C = A.circle, f = A.f;

  var H = A.helpers = {};
  H.cloud = function (x, y, s, fill) { return C(x, y, s * 0.5, fill) + C(x + s * 0.55, y + s * 0.1, s * 0.4, fill) + C(x - s * 0.5, y + s * 0.15, s * 0.34, fill) + R(x - s * 0.84, y + s * 0.15, s * 1.84, s * 0.35, s * 0.17, fill); };
  H.sun = function (c, x, y, rad) { var P = c.P; return P.dark ? C(x, y, rad * 1.9, P.glow) + C(x, y, rad, P.sun) + C(x + rad * 0.42, y - rad * 0.2, rad * 0.8, P.sky) : C(x, y, rad * 2.2, P.glow) + C(x, y, rad * 1.5, P.t(0.12)) + C(x, y, rad, P.sun); };
  H.peaks = function (c, base, hMin, hMax, n, fill, snow, k) {
    var r = c.r, w = c.w, pts = [], out = '', i, px = -w * 0.1, st = w * 1.2 / n, pk = [];
    for (i = 0; i <= n; i++) { var x = px + i * st + r.range(-0.25, 0.25) * st, y = base - r.range(hMin, hMax); pk.push([x, y]); pts.push([x - st * 0.5 + r.range(-.1, .1) * st, base - r.range(0, hMin * 0.25)]); }
    pts.push([px + (n + 1) * st, base]);
    var poly = [[px - st, base + 4]]; for (i = 0; i <= n; i++) { poly.push(pts[i], pk[i]); } poly.push(pts[n + 1], [px + (n + 2) * st, base + 4]);
    out += A.poly(poly, fill) + R(0, base, w, c.h - base, 0, fill);
    if (snow) for (i = 0; i <= n; i++) {
      var L = pts[i], Rr = pts[i + 1], p = pk[i], t = r.range(0.26, 0.4), a = [p[0] + (L[0] - p[0]) * t, p[1] + (L[1] - p[1]) * t], b = [p[0] + (Rr[0] - p[0]) * t, p[1] + (Rr[1] - p[1]) * t];
      var m = [(a[0] + b[0]) / 2 + r.range(-6, 6), Math.max(a[1], b[1]) + (b[0] - a[0]) * 0.12];
      out += A.poly([p, a, [a[0] + (b[0] - a[0]) * 0.28, a[1] + (m[1] - a[1]) * 0.9], [m[0], m[1] - (b[0] - a[0]) * 0.04], [a[0] + (b[0] - a[0]) * 0.72, b[1] + (m[1] - b[1]) * 0.9], b], snow);
    }
    return out;
  };
  H.flags = function (c, x1, y1, x2, y2, s) {
    var P = c.P, cols = P.dark ? ['#5aa3ff', '#e9edf5', '#ff6b5e', '#4cc38a', '#ffc94d'] : ['#2f6fed', '#ffffff', '#e5483b', '#2faa6b', '#f4b400'], o = A.stroke('M' + f(x1) + ' ' + f(y1) + 'Q' + f((x1 + x2) / 2) + ' ' + f(Math.max(y1, y2) + s * 2) + ' ' + f(x2) + ' ' + f(y2), s * 0.12, P.ink), i, t, x, y;
    for (i = 1; i < 11; i++) { t = i / 11; x = (1 - t) * (1 - t) * x1 + 2 * t * (1 - t) * (x1 + x2) / 2 + t * t * x2; y = (1 - t) * (1 - t) * y1 + 2 * t * (1 - t) * (Math.max(y1, y2) + s * 2) + t * t * y2; o += A.poly([[x - s * 0.6, y], [x + s * 0.6, y], [x + s * 0.6, y + s * 1.1], [x - s * 0.6, y + s * 1.2]], cols[i % 5]); }
    return o;
  };
  H.tree = function (x, y, s, fill, trunk, kind) {
    if (kind === 'pine') return A.rect(x - s * 0.06, y - s * 0.2, s * 0.12, s * 0.22, 1, trunk) + A.path(A.rpoly([[x - s * 0.36, y - s * 0.14], [x + s * 0.36, y - s * 0.14], [x, y - s * 0.6]], s * 0.06), fill) + A.path(A.rpoly([[x - s * 0.28, y - s * 0.46], [x + s * 0.28, y - s * 0.46], [x, y - s * 0.95]], s * 0.05), fill);
    return A.rect(x - s * 0.05, y - s * 0.5, s * 0.1, s * 0.52, 1, trunk) + (kind === 'puff' ? C(x, y - s * 0.78, s * 0.26, fill) + C(x - s * 0.24, y - s * 0.62, s * 0.22, fill) + C(x + s * 0.24, y - s * 0.62, s * 0.22, fill) + C(x, y - s * 0.56, s * 0.26, fill) : C(x, y - s * 0.74, s * 0.3, fill) + C(x - s * 0.2, y - s * 0.62, s * 0.2, fill) + C(x + s * 0.2, y - s * 0.62, s * 0.2, fill));
  };
  H.hut = function (x, y, s, wall, roof, door) { return A.rect(x - s * 0.5, y - s * 0.5, s, s * 0.5, s * 0.04, wall) + A.poly([[x - s * 0.64, y - s * 0.48], [x + s * 0.64, y - s * 0.48], [x + s * 0.4, y - s * 0.88], [x - s * 0.4, y - s * 0.88]], roof) + A.arch(x - s * 0.1, y - s * 0.32, s * 0.2, s * 0.32, door); };
  H.pagoda = function (x, y, s, body, roof, hole) {
    var o = A.rect(x - s * 0.34, y - s * 0.08, s * 0.68, s * 0.08, 0, roof), i, w, yy;
    for (i = 0; i < 3; i++) { w = s * (0.5 - i * 0.1); yy = y - s * 0.08 - i * s * 0.3; o += A.rect(x - w / 2, yy - s * 0.2, w, s * 0.2, 0, body) + A.rect(x - w * 0.12, yy - s * 0.17, w * 0.24, s * 0.14, 2, hole) + A.poly([[x - w * 0.9, yy - s * 0.2 + s * 0.04], [x + w * 0.9, yy - s * 0.16 + s * 0.04], [x + w * 0.5, yy - s * 0.31], [x - w * 0.5, yy - s * 0.31]], roof); }
    return o + A.rect(x - s * 0.015, y - s * 1.1, s * 0.03, s * 0.2, 1, roof) + C(x, y - s * 1.1, s * 0.03, roof);
  };
  H.stupa = function (x, y, s, body, roof) { return A.rect(x - s * 0.5, y - s * 0.08, s, s * 0.08, 0, roof) + A.rect(x - s * 0.38, y - s * 0.16, s * 0.76, s * 0.08, 0, body) + A.path('M' + f(x - s * 0.34) + ' ' + f(y - s * 0.16) + 'A' + f(s * 0.34) + ' ' + f(s * 0.32) + ' 0 0 1 ' + f(x + s * 0.34) + ' ' + f(y - s * 0.16) + 'Z', body) + A.rect(x - s * 0.09, y - s * 0.52, s * 0.18, s * 0.1, 0, roof) + A.poly([[x - s * 0.07, y - s * 0.52], [x + s * 0.07, y - s * 0.52], [x, y - s * 0.9]], roof); };

  E.himal = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = R(0, 0, w, h, 0, P.sky), n = r.int(4, 5), i, k, base, sx = r.range(0.15, 0.85) * w;
    o += H.sun(c, sx, h * r.range(0.17, 0.3), h * r.range(0.06, 0.09)) + H.cloud(w * (sx > w / 2 ? r.range(0.08, 0.3) : r.range(0.62, 0.85)), h * 0.2, h * 0.1, P.dark ? P.depth(0.2) : '#fff') + H.cloud(w * (sx > w / 2 ? r.range(0.35, 0.5) : r.range(0.1, 0.25)), h * 0.3, h * 0.07, P.dark ? P.depth(0.2) : '#fff');
    o += H.peaks(c, h * 0.62, h * 0.32, h * 0.5, Math.round(w / h * 2.3), P.depth(0.14), P.snow);
    o += H.peaks(c, h * 0.72, h * 0.2, h * 0.34, Math.round(w / h * 3.2), P.depth(0.3), P.dark ? P.t(0.55) : P.t(0.02));
    for (i = 0; i < 3; i++) { k = 0.45 + i * 0.25; base = h * (0.74 + i * 0.1); o += A.fillTo(A.ridge(r, -20, w + 20, base, h * (0.13 - i * 0.03), 2.2 / w * 100, 3), h, P.depth(k)); }
    for (i = 0; i < Math.round(w / h * 6); i++) { var tx = r.range(0.02, 0.98) * w, ty = h * r.range(0.9, 0.99); o += H.tree(tx, ty, h * r.range(0.12, 0.22), P.depth(1), P.depth(0.9), 'pine'); }
    if (r.chance(0.8)) o += H.flags(c, w * 0.06, h * 0.55, w * 0.38, h * r.range(0.46, 0.58), h * 0.028);
    return o;
  };
  E.terraces = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = R(0, 0, w, h, 0, P.sky), N = r.int(9, 13), j, y0 = h * 0.38, dy = h * 0.62 / N, ph = r.range(0, 6), fr = r.range(2.4, 4) / w * 6;
    o += H.sun(c, w * r.range(0.2, 0.8), h * 0.2, h * 0.07) + H.peaks(c, h * 0.5, h * 0.18, h * 0.3, Math.round(w / h * 3), P.depth(0.15), P.snow);
    for (j = 0; j < N; j++) {
      var pts = [], x, yy = y0 + j * dy; for (x = -20; x <= w + 30; x += 44) pts.push([x, yy + Math.sin(x * fr + j * 0.9 + ph) * dy * 0.8 + Math.sin(x * fr * 2.3 + ph) * dy * 0.25 - j * 0]);
      o += A.fillTo(pts, h, j % 2 ? P.depth(0.35 + j / N * 0.5) : P.t(0.2 + j / N * 0.35)) + A.stroke(A.smooth(pts, false), 1.8, P.depth(0.6 + j / N * 0.3));
    }
    o += H.hut(w * r.range(0.25, 0.75), h * 0.7, h * 0.14, P.paper, P.sp(0.6), P.depth(0.9)) + H.tree(w * 0.12, h * 0.78, h * 0.18, P.depth(0.95), P.depth(1), 'puff') + H.tree(w * 0.9, h * 0.84, h * 0.22, P.depth(0.95), P.depth(1), 'puff');
    return o;
  };
  E.valley = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = R(0, 0, w, h, 0, P.sky), i, x;
    o += H.sun(c, w * r.range(0.15, 0.85), h * 0.22, h * 0.07) + H.peaks(c, h * 0.62, h * 0.2, h * 0.34, Math.round(w / h * 3), P.depth(0.12), P.snow) + A.fillTo(A.ridge(r, -20, w + 20, h * 0.62, h * 0.06, 0.012, 3), h, P.depth(0.28));
    for (i = 0; i < Math.round(w / h * 14); i++) { x = r.range(0, 1) * w; o += A.rect(x, h * 0.62 - r.range(0.05, 0.13) * h, r.range(0.05, 0.09) * h, h * 0.4, 2, P.depth(0.4)); }
    var cx = [0.2, 0.5, 0.8]; for (i = 0; i < 3; i++) { x = (cx[i] + r.range(-0.07, 0.07)) * w; o += (i === 1 ? H.stupa(x, h * 0.7, h * 0.34, P.paper, P.sp(0.55)) : H.pagoda(x, h * 0.7, h * 0.3 * r.range(0.9, 1.2), P.depth(0.55), P.depth(0.82), P.sky)); }
    for (i = 0; i < Math.round(w / h * 9); i++) { x = r.range(0, 1) * w; var hh = h * r.range(0.09, 0.16), ww = h * r.range(0.1, 0.17); o += A.rect(x, h * 0.84 - hh, ww, hh + h * 0.2, 2, P.depth(0.6 + r.range(0, 0.2))) + A.rect(x - 4, h * 0.84 - hh - 4, ww + 8, 10, 3, P.sp(0.55)) + A.rect(x + ww * 0.2, h * 0.84 - hh * 0.6, ww * 0.18, hh * 0.3, 2, P.sky) + A.rect(x + ww * 0.6, h * 0.84 - hh * 0.6, ww * 0.18, hh * 0.3, 2, P.sky); }
    return o + A.rect(0, h * 0.93, w, h * 0.07, 0, P.depth(1));
  };
  E.lake = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, wl = h * 0.6, o = R(0, 0, w, h, 0, P.sky), i, m;
    m = H.peaks(c, wl, h * 0.25, h * 0.42, Math.round(w / h * 2.2), P.depth(0.2), P.snow) + A.fillTo(A.ridge(r, -20, w + 20, wl - h * 0.02, h * 0.08, 0.01, 3), wl, P.depth(0.45));
    o += H.sun(c, w * r.range(0.2, 0.8), h * 0.22, h * 0.065) + m + R(0, wl, w, h - wl, 0, P.t(0.34));
    o += '<clipPath id="' + c.uid + 'c"><rect y="' + f(wl) + '" width="' + w + '" height="' + f(h - wl) + '"/></clipPath><g clip-path="url(#' + c.uid + 'c)"><g transform="translate(0 ' + f(wl * 2) + ') scale(1 -1)" opacity="1">' + m.replace(/fill="[^"]+"/g, function (s) { return s === 'fill="' + P.snow + '"' ? 'fill="' + P.t(0.2) + '"' : 'fill="' + P.t(0.46) + '"'; }) + '</g></g>';
    for (i = 0; i < 16; i++) { var yy = wl + h * (0.03 + i * 0.024); o += A.rect(r.range(0, 1) * w, yy, r.range(0.06, 0.2) * w, h * 0.008, h * 0.004, i % 2 ? P.t(0.18) : P.t(0.5)); }
    var bx = w * r.range(0.3, 0.7), by = wl + h * 0.2, s = h * 0.18;
    o += A.path('M' + f(bx - s * 0.7) + ' ' + f(by) + 'H' + f(bx + s * 0.7) + 'Q' + f(bx + s * 0.5) + ' ' + f(by + s * 0.2) + ' ' + f(bx) + ' ' + f(by + s * 0.2) + 'Q' + f(bx - s * 0.5) + ' ' + f(by + s * 0.2) + ' ' + f(bx - s * 0.7) + ' ' + f(by) + 'Z', P.sp(0.55)) + A.rect(bx - 1.5, by - s * 1.1, 3, s * 1.1, 1, P.ink) + A.poly([[bx + 5, by - s * 1.05], [bx + s * 0.6, by - s * 0.08], [bx + 5, by - s * 0.08]], P.paper) + A.poly([[bx - 5, by - s * 0.8], [bx - s * 0.42, by - s * 0.08], [bx - 5, by - s * 0.08]], P.t(0.1));
    return o + A.fillTo(A.ridge(r, -20, w + 20, h * 0.96, h * 0.05, 0.012, 2), h, P.depth(0.95));
  };
  E.meadow = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = R(0, 0, w, h, 0, P.sky), i, j, k;
    o += H.sun(c, w * r.range(0.15, 0.85), h * 0.22, h * 0.07) + H.cloud(w * 0.25, h * 0.15, h * 0.1, P.dark ? P.depth(0.2) : '#fff') + H.cloud(w * 0.7, h * 0.26, h * 0.08, P.dark ? P.depth(0.2) : '#fff');
    for (i = 0; i < 5; i++) {
      k = i / 4; var base = h * (0.5 + i * 0.12); o += A.fillTo(A.ridge(r, -20, w + 20, base, h * (0.1 - i * 0.012), 0.8 / w * 6, 2), h, P.depth(0.2 + k * 0.75));
      for (j = 0; j < Math.round(w / h * (2 + i * 1.6)); j++) { var tx = r.range(0, 1) * w; o += (i < 4 && r.chance(0.5)) ? H.tree(tx, base + h * r.range(0.04, 0.09), h * (0.1 + k * 0.12), P.depth(0.35 + k * 0.7), P.depth(0.9), r.pick(['puff', 'round'])) : C(tx, base + h * r.range(0.05, 0.1), h * 0.008 + k * 4, P.sp(0.4 + r.range(0, 0.3))); }
    }
    return o;
  };
  E.forest = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = R(0, 0, w, h, 0, P.sky), i, j, rows = 5;
    o += C(w * r.range(0.3, 0.7), h * 0.3, h * 0.2, P.glow) + C(w * 0.5, h * 0.3, h * 0.1, P.sun);
    for (i = 0; i < rows; i++) {
      var base = h * (0.55 + i * 0.1), k = i / (rows - 1), n = Math.round(w / h * (7 + i * 3)), col = P.depth(0.15 + k * 0.85);
      o += R(0, base - h * 0.02, w, h, 0, col);
      for (j = 0; j < n; j++) o += H.tree(j / n * w * 1.1 - 10 + r.range(-0.4, 0.4) * w / n, base, h * (0.2 + k * 0.28) * r.range(0.8, 1.2), col, col, 'pine');
      if (i < rows - 1) o += R(0, base + h * 0.05, w, h * 0.03, 0, P.depth(0.1 + k * 0.4));
    }
    return o;
  };
})(typeof window !== 'undefined' ? window : globalThis);
