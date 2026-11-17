/* Layouts A: orbit, bauhaus, waves, hills, rays, scatter, dots, petals. Each returns SVG markup. */
(function (g) {
  var N = g.NebArt, L = N.layouts, sh = N.shape, ci = N.circle, rc = N.rect;
  var SH = function (c) { return c.pick(N.shapeNames); };

  L.orbit = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = '', k = SH(c), cx = c.rr(0.55, 0.95) * W, cy = c.rr(0.1, 0.9) * H, R = u * c.rr(0.75, 1.05), rot = c.r() * 6.28;
    for (var i = 5; i >= 1; i--) o += sh(k, cx, cy, R * i / 5, rot + i * 0.12, T[i % 2 ? 1 : 2], i === 1 ? '' : ' opacity="' + (0.45 + i * 0.1).toFixed(2) + '"');
    o += sh(k, cx, cy, R * 0.2, rot, T[3]);
    o += ci(c.rr(0.08, 0.3) * W, c.rr(0.2, 0.8) * H, u * 0.09, T[5]);
    o += sh(SH(c), c.rr(0.05, 0.4) * W, c.rr(0.55, 1.05) * H, u * 0.34, c.r() * 6, T[2]);
    return o;
  };
  L.bauhaus = function (c) {
    var T = c.T, s = c.H / (c.r() > 0.5 ? 2 : 3), cols = Math.ceil(c.W / s) + 1, rows = Math.ceil(c.H / s), o = '', x, y, t, q, f;
    for (y = 0; y < rows; y++) for (x = 0; x < cols; x++) {
      t = c.r(); q = Math.floor(c.r() * 4); f = T[1 + Math.floor(c.r() * 5)];
      if (t < 0.28) o += N.quarter(x * s, y * s, s, q, f);
      else if (t < 0.46) o += ci(x * s + s / 2, y * s + s / 2, s * 0.42, f);
      else if (t < 0.62) o += N.arch(x * s + s * 0.1, y * s + s * 0.05, s * 0.8, s * 0.9, f);
      else if (t < 0.74) o += rc(x * s + s * 0.1, y * s + s * 0.3, s * 0.8, s * 0.4, s * 0.2, f);
      else if (t < 0.82) o += sh(SH(c), x * s + s / 2, y * s + s / 2, s * 0.42, c.r() * 6, T[5]);
    }
    return o;
  };
  L.waves = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', n = 4 + Math.floor(c.r() * 3), i, j, y, a, ph, d, k;
    o += sh(SH(c), c.rr(0.15, 0.85) * W, c.rr(0.25, 0.5) * H, H * 0.3, c.r() * 6, T[5]);
    for (i = 0; i < n; i++) {
      y = H * (0.42 + (i / n) * 0.5); a = H * c.rr(0.05, 0.12); ph = c.r() * 6.28; k = c.rr(1, 2.6); d = 'M0 ' + H + 'V' + N.f1(y);
      for (j = 0; j <= 48; j++) d += 'L' + N.f1(j / 48 * W) + ' ' + N.f1(y + Math.sin(j / 48 * 6.28 * k + ph) * a);
      o += '<path d="' + d + 'V' + H + 'Z" fill="' + T[1 + (i % 4)] + '"/>';
    }
    return o;
  };
  L.hills = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', i, n = 5;
    o += sh('burst', c.rr(0.2, 0.8) * W, H * 0.4, H * 0.3, c.r(), T[5]);
    for (i = 0; i < n; i++) {
      var y = H * (0.55 + i * 0.13), cnt = 2 + Math.floor(c.r() * 3), j;
      for (j = 0; j < cnt; j++) o += ci(c.r() * W, y + H * 0.3, H * c.rr(0.25, 0.5), T[1 + ((i + j) % 4)]);
      o += rc(0, y + H * 0.28, W, H, 0, T[1 + (i % 4)]);
    }
    return o;
  };
  L.rays = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', ax = c.pick([0, W, W / 2]), ay = c.pick([0, H, H / 2]), n = 14 + Math.floor(c.r() * 8), i, R = Math.hypot(W, H), a0 = c.r() * 6.28;
    for (i = 0; i < n; i += 2) {
      var a = a0 + (i / n) * 6.28, b = a0 + ((i + 1) / n) * 6.28;
      o += '<path d="M' + N.f1(ax) + ' ' + N.f1(ay) + 'L' + N.f1(ax + Math.cos(a) * R) + ' ' + N.f1(ay + Math.sin(a) * R) + 'L' + N.f1(ax + Math.cos(b) * R) + ' ' + N.f1(ay + Math.sin(b) * R) + 'Z" fill="' + T[1] + '"/>';
    }
    o += sh(SH(c), ax, ay, H * 0.36, a0, T[3]) + sh(SH(c), ax, ay, H * 0.2, a0 + 1, T[5]);
    return o;
  };
  L.scatter = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = '', n = 9 + Math.floor(c.r() * 5), i;
    for (i = 0; i < n; i++) o += sh(SH(c), c.r() * W, c.r() * H, u * c.rr(0.1, 0.42), c.r() * 6.28, T[1 + (i % 5)]);
    o += sh(SH(c), c.rr(0.5, 0.9) * W, c.rr(0.3, 0.7) * H, u * 0.3, c.r() * 6, T[3]) + ci(c.rr(0.1, 0.5) * W, c.rr(0.2, 0.8) * H, u * 0.08, T[4]);
    return o;
  };
  L.dots = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', s = c.u / 10, fx = c.rr(0.3, 1) * W, fy = c.rr(0, 1) * H, x, y, d, R = Math.hypot(W, H) * 0.7;
    for (y = s / 2; y < H; y += s) for (x = s / 2 + ((Math.round(y / s) % 2) * s) / 2; x < W; x += s) {
      d = Math.hypot(x - fx, y - fy) / R; o += ci(x, y, Math.max(0.6, s * 0.46 * (1 - d)), T[d < 0.5 ? 3 : 2]);
    }
    return sh(SH(c), fx, fy, c.u * 0.3, c.r() * 6, T[5]) + o.replace(/<circle/g, '<circle opacity=".9"');
  };
  L.petals = function (c) {
    var T = c.T, o = '', k = c.pick(['flower', 'cookie', 'sunny', 'clover']), cx = c.rr(0.58, 0.88) * c.W, cy = c.rr(0.3, 0.7) * c.H, R = c.u * c.rr(0.7, 0.95), i, n = 6;
    for (i = 0; i < n; i++) o += sh(k, cx, cy, R * (1 - i / n), i * 0.35, T[(i % 2) ? 2 : 1 + (i % 4)]);
    o += ci(cx, cy, R * 0.1, T[5]);
    o += sh(SH(c), c.rr(0.05, 0.3) * c.W, c.rr(0.6, 1) * c.H, c.u * 0.25, c.r() * 6, T[3]);
    return o;
  };
})(typeof window !== 'undefined' ? window : globalThis);
