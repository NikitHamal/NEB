/* v7 compositions, set C. Same flat language as v1: expressive shapes, quarter circles, pills. */
(function (g) {
  var N = g.NebArt, L = N.layouts, sh = N.shape, ci = N.circle, rc = N.rect, f1 = N.f1;
  var SH = function (c) { return c.pick(N.shapeNames); };

  L.pinwheel = function (c) {
    var T = c.T, o = '', cx = c.rr(0.5, 0.85) * c.W, cy = c.rr(0.35, 0.65) * c.H, R = c.u * c.rr(0.7, 0.95), n = c.pick([4, 6, 8]), i;
    for (i = 0; i < n; i++) o += N.rot('<path d="M' + f1(cx) + ' ' + f1(cy) + 'L' + f1(cx + R) + ' ' + f1(cy) + 'A' + f1(R) + ' ' + f1(R) + ' 0 0 1 ' + f1(cx + R * Math.cos(6.283 / n)) + ' ' + f1(cy + R * Math.sin(6.283 / n)) + 'Z" fill="' + T[1 + (i % 4)] + '"/>', i * 360 / n, cx, cy);
    return o + ci(cx, cy, R * 0.16, T[5]) + sh(SH(c), c.rr(0.05, 0.3) * c.W, c.rr(0.6, 1) * c.H, c.u * 0.22, c.r() * 6, T[3]);
  };
  L.mondrian = function (c) {
    var T = c.T, o = '', gp = c.u * 0.02, cells = [[0, 0, c.W, c.H]], i, k = 0;
    for (i = 0; i < 7 + Math.floor(c.r() * 4); i++) {
      var j = Math.floor(c.r() * cells.length), a = cells[j], v = a[2] > a[3] * c.rr(0.8, 1.4), t = c.rr(0.35, 0.65);
      if (a[2] < c.u * 0.3 || a[3] < c.u * 0.3) continue;
      cells.splice(j, 1, v ? [a[0], a[1], a[2] * t, a[3]] : [a[0], a[1], a[2], a[3] * t], v ? [a[0] + a[2] * t, a[1], a[2] * (1 - t), a[3]] : [a[0], a[1] + a[3] * t, a[2], a[3] * (1 - t)]);
    }
    cells.forEach(function (a, n) { k = c.r(); o += rc(a[0] + gp, a[1] + gp, a[2] - gp * 2, a[3] - gp * 2, c.u * 0.07, k < 0.12 ? T[5] : k < 0.3 ? T[3] : T[1 + (n % 3)]); });
    return o;
  };
  L.halftone = function (c) {
    var T = c.T, o = '', s = c.u / c.pick([7, 9, 11]), fx = c.rr(0.2, 0.9) * c.W, fy = c.rr(0.1, 0.9) * c.H, R = Math.hypot(c.W, c.H) * 0.62, x, y, d, k = c.pick(['squircle', 'cookie', 'flower', 'pebble']);
    for (y = s / 2; y < c.H + s; y += s) for (x = s / 2; x < c.W + s; x += s) {
      d = Math.hypot(x - fx, y - fy) / R; if (d > 1) continue;
      o += sh(k, x, y, s * 0.5 * (1 - d * 0.82), (x + y) * 0.01, T[d < 0.35 ? 3 : d < 0.7 ? 2 : 1]);
    }
    return o + ci(fx, fy, s * 0.4, T[5]);
  };
  L.capsules = function (c) {
    var T = c.T, o = '', n = 9 + Math.floor(c.r() * 5), th = c.u * 0.15, i, a = c.pick([-38, -28, 32, 42]), W = c.W, H = c.H;
    for (i = 0; i < n; i++) {
      var cx = c.r() * W, cy = c.r() * H, len = c.u * c.rr(0.5, 1.4);
      o += N.rot(N.pill(cx, cy, len, th * c.rr(0.7, 1.1), T[1 + (i % 4)]), a, cx, cy);
    }
    var x = c.rr(0.2, 0.85) * W, y = c.rr(0.25, 0.75) * H;
    return o + N.rot(N.pill(x, y, c.u * 0.5, th * 0.9, T[5]), a, x, y);
  };
  L.cascade = function (c) {
    var T = c.T, o = '', n = 6 + Math.floor(c.r() * 3), s = c.u * 0.52, i, dx = (c.W - s * 0.4) / n, dy = (c.H - s * 0.5) / n, flip = c.r() > 0.5;
    for (i = 0; i < n; i++) {
      var x = (flip ? c.W - s - i * dx : i * dx), y = i * dy;
      o += rc(x, y, s, s * 0.8, s * 0.28, T[1 + (i % 4)]) + (i === n - 2 ? sh(SH(c), x + s * 0.5, y + s * 0.4, s * 0.2, c.r() * 6, T[5]) : '');
    }
    return o;
  };
  L.swirl = function (c) {
    var T = c.T, o = '', cx = c.rr(0.45, 0.8) * c.W, cy = c.rr(0.35, 0.65) * c.H, n = 22, i, k = SH(c), R = c.u * 0.95, a;
    for (i = n; i >= 0; i--) {
      a = i * 0.62; var d = R * Math.pow(i / n, 0.8) * 0.9;
      o += sh(k, cx + Math.cos(a) * d * 0.55, cy + Math.sin(a) * d * 0.55, R * (0.06 + 0.14 * (i / n)), a, T[i === 0 ? 5 : 1 + (i % 4)]);
    }
    return o;
  };
  L.ripple = function (c) {
    var T = c.T, o = '', cx = c.pick([0.1, 0.9, 0.5]) * c.W, cy = c.pick([0, 1, 0.5]) * c.H, n = 7, R = Math.hypot(c.W, c.H) * 0.85, i;
    for (i = n; i >= 1; i--) o += ci(cx, cy, R * i / n, T[1 + (i % 4)]);
    return o + ci(cx, cy, R * 0.07, T[5]) + sh(SH(c), c.rr(0.3, 0.8) * c.W, c.rr(0.3, 0.7) * c.H, c.u * 0.14, c.r() * 6, T[3]);
  };
  L.venn = function (c) {
    var T = c.T, o = '', cx = c.rr(0.45, 0.75) * c.W, cy = c.H * 0.5, R = c.u * c.rr(0.34, 0.46), n = c.pick([3, 4]), i, a0 = c.r() * 6;
    for (i = 0; i < n; i++) o += ci(cx + Math.cos(a0 + i * 6.283 / n) * R * 0.62, cy + Math.sin(a0 + i * 6.283 / n) * R * 0.62, R, T[1 + (i % 3) * 1], ' opacity="0.78"');
    return o + ci(cx, cy, R * 0.22, T[5]) + sh(SH(c), c.rr(0.05, 0.25) * c.W, c.rr(0.6, 1) * c.H, c.u * 0.2, c.r() * 6, T[3]);
  };
})(typeof window !== 'undefined' ? window : globalThis);
