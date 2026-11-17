/* v7 compositions, set D: truchet, contour lines, blobs, rings, bento, diamonds, segments, bands. */
(function (g) {
  var N = g.NebArt, L = N.layouts, sh = N.shape, ci = N.circle, rc = N.rect, f1 = N.f1;
  var SH = function (c) { return c.pick(N.shapeNames); };

  L.truchet = function (c) {
    var T = c.T, o = '', s = c.u / c.pick([2, 3, 4]), x, y, q, t;
    for (y = 0; y * s < c.H; y++) for (x = 0; x * s < c.W; x++) {
      q = Math.floor(c.r() * 4); t = c.r();
      o += rc(x * s, y * s, s, s, 0, T[t < 0.5 ? 1 : 6]) + N.quarter(x * s, y * s, s, q, T[2 + Math.floor(c.r() * 2)]) + N.quarter(x * s + s * 0.5, y * s + s * 0.5, s * 0.5, q + 2, T[t > 0.85 ? 5 : 4]);
    }
    return o;
  };
  L.contour = function (c) {
    var T = c.T, o = '', n = 9 + Math.floor(c.r() * 5), i, j, sw = c.u * 0.045, ph = c.r() * 6, k = c.rr(0.8, 1.8), pts;
    for (i = 0; i < n; i++) {
      pts = [];
      for (j = 0; j <= 14; j++) pts.push([j / 14 * c.W, c.H * (i / (n - 1)) + Math.sin(j / 14 * 6.283 * k + ph + i * 0.28) * c.H * 0.2]);
      o += N.curve(pts, sw, T[i % 5 === 3 ? 5 : 1 + (i % 3)]);
    }
    return o;
  };
  L.blobs = function (c) {
    var T = c.T, o = '', n = 5 + Math.floor(c.r() * 3), i;
    for (i = 0; i < n; i++) o += sh(SH(c), c.rr(0.05, 0.95) * c.W, c.rr(0.1, 0.9) * c.H, c.u * c.rr(0.3, 0.62), c.r() * 6.28, T[1 + (i % 4)], ' opacity="0.9"');
    return o + sh(SH(c), c.rr(0.5, 0.9) * c.W, c.rr(0.25, 0.7) * c.H, c.u * 0.17, c.r() * 6, T[5]);
  };
  L.rings = function (c) {
    var T = c.T, o = '', cx = c.rr(0.55, 0.85) * c.W, cy = c.rr(0.35, 0.65) * c.H, n = 6, i, R = c.u * 0.9, sw = R / n * 0.5;
    for (i = 0; i < n; i++) { var a = c.r() * 6.28; o += N.ring(cx, cy, R * (i + 1.4) / (n + 0.6), sw, T[1 + (i % 2)], ' opacity="0.8"') + N.arc(cx, cy, R * (i + 1.4) / (n + 0.6), a, a + c.rr(1.8, 4.6), sw, T[i === n - 2 ? 5 : 3]); }
    return o + sh(SH(c), c.rr(0.05, 0.3) * c.W, c.rr(0.6, 1) * c.H, c.u * 0.2, c.r() * 6, T[2]);
  };
  L.bento = function (c) {
    var T = c.T, o = '', gp = c.u * 0.03, cw = c.W / 4, ch = c.H / 3, spans = [[0, 0, 2, 2], [2, 0, 1, 1], [3, 0, 1, 2], [2, 1, 1, 2], [0, 2, 2, 1], [3, 2, 1, 1]], i, a, f;
    spans.forEach(function (a, i) {
      var x = a[0] * cw + gp, y = a[1] * ch + gp, w = a[2] * cw - gp * 2, h = a[3] * ch - gp * 2; f = T[1 + (i % 4)];
      o += rc(x, y, w, h, Math.min(w, h) * 0.22, i === 2 ? T[3] : f);
      if (i % 2 === 0) o += sh(SH(c), x + w / 2, y + h / 2, Math.min(w, h) * 0.3, c.r() * 6, i === 4 ? T[5] : T[i === 0 ? 3 : 4]);
    });
    return o;
  };
  L.diamonds = function (c) {
    var T = c.T, o = '', s = c.u / c.pick([3, 4, 5]), x, y, ox;
    for (y = 0; y * s * 0.5 < c.H + s; y++) for (x = -1; x * s < c.W + s; x++) {
      ox = (y % 2) * s * 0.5; var t = c.r(), cx = x * s + ox + s / 2, cy = y * s * 0.5;
      o += N.rot(rc(cx - s * 0.3, cy - s * 0.3, s * 0.6, s * 0.6, s * 0.14, t < 0.1 ? T[5] : T[1 + Math.floor(t * 4.4) % 4]), 45, cx, cy);
    }
    return o;
  };
  L.segments = function (c) {
    var T = c.T, o = '', n = c.pick([3, 4, 5]), i, cx = c.rr(0.55, 0.85) * c.W, cy = c.H * 0.5, R = c.u * 0.85, a0 = c.r() * 6.28;
    for (i = 0; i < n; i++) {
      var a = a0 + i * 6.283 / n, b = a + 6.283 / n * 0.92, r = R * (0.62 + 0.38 * c.r());
      o += '<path d="M' + f1(cx) + ' ' + f1(cy) + 'L' + f1(cx + r * Math.cos(a)) + ' ' + f1(cy + r * Math.sin(a)) + 'A' + f1(r) + ' ' + f1(r) + ' 0 0 1 ' + f1(cx + r * Math.cos(b)) + ' ' + f1(cy + r * Math.sin(b)) + 'Z" fill="' + T[1 + (i % 4)] + '"/>';
    }
    return o + ci(cx, cy, R * 0.2, T[5]) + sh(SH(c), c.rr(0.05, 0.3) * c.W, c.rr(0.6, 1) * c.H, c.u * 0.2, c.r() * 6, T[3]);
  };
  L.bands = function (c) {
    var T = c.T, o = '', n = 5 + Math.floor(c.r() * 3), a = c.pick([-20, -14, 14, 20]), i, w = c.W * 1.6, h = c.H / n * 1.05;
    for (i = 0; i < n; i++) o += N.rot(rc(-c.W * 0.3 - (i % 2) * c.W * 0.1, i * (c.H / n) - h * 0.1, w * c.rr(0.5, 0.75), h, h / 2, T[1 + (i % 4)]), a, c.W / 2, c.H / 2);
    return o + sh(SH(c), c.rr(0.55, 0.9) * c.W, c.rr(0.3, 0.7) * c.H, c.u * 0.2, c.r() * 6, T[5]);
  };
  L.petalfield = function (c) {
    var T = c.T, o = '', cols = c.pick([3, 4, 5]), s = c.u / cols * 1.15, x, y, k = c.pick(['flower', 'cookie', 'clover', 'sunny']);
    for (y = 0; y * s * 0.85 < c.H + s; y++) for (x = 0; x * s < c.W + s; x++) {
      var cx = x * s + (y % 2) * s / 2, cy = y * s * 0.85, t = c.r();
      o += sh(k, cx, cy, s * 0.46, c.r() * 6, T[1 + Math.floor(t * 4)]) + (t > 0.88 ? ci(cx, cy, s * 0.1, T[5]) : '');
    }
    return o;
  };
  /* v1 waves put a round accent over the water, which reads as a sun. Same bands, the accent is a tilted squircle set inside the swell. */
  L.waves = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', n = 4 + Math.floor(c.r() * 3), i, j, y, a, ph, k, d;
    for (i = 0; i < n; i++) {
      y = H * (0.3 + (i / n) * 0.62); a = H * c.rr(0.05, 0.12); ph = c.r() * 6.28; k = c.rr(1, 2.6); d = 'M0 ' + H + 'V' + f1(y);
      for (j = 0; j <= 48; j++) d += 'L' + f1(j / 48 * W) + ' ' + f1(y + Math.sin(j / 48 * 6.28 * k + ph) * a);
      o += '<path d="' + d + 'V' + H + 'Z" fill="' + T[1 + (i % 4)] + '"/>';
      if (i === 1) o += sh(c.pick(['squircle', 'pebble', 'clover']), c.rr(0.15, 0.85) * W, y + H * 0.1, H * 0.12, c.r() * 6, T[5]);
    }
    return o;
  };
  /* Every v1 layout except hills and sunset (mountain and sun reads) and rays (sunburst read), plus the v7 sets. */
  var BAN = { hills: 1, sunset: 1, rays: 1 };
  N.layoutNames = Object.keys(L).filter(function (k) { return !BAN[k]; });
  N.layoutNew = ['pinwheel', 'mondrian', 'halftone', 'capsules', 'cascade', 'swirl', 'ripple', 'venn', 'truchet', 'contour', 'blobs', 'rings', 'bento', 'diamonds', 'segments', 'bands', 'petalfield'];
})(typeof window !== 'undefined' ? window : globalThis);
