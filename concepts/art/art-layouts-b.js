/* Layouts B: stack, net, graph, arches, mosaic, ribbons, bars, sunset, folds, tiles. */
(function (g) {
  var N = g.NebArt, L = N.layouts, sh = N.shape, ci = N.circle, rc = N.rect, f1 = N.f1;
  var SH = function (c) { return c.pick(N.shapeNames); };

  L.stack = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', n = 6 + Math.floor(c.r() * 4), h = H / n, i;
    for (i = 0; i < n; i++) {
      var w = W * c.rr(0.45, 0.98), x = c.r() > 0.5 ? 0 : W - w;
      o += rc(x - h, i * h + h * 0.08, w + h, h * 0.84, h * 0.42, T[1 + (i % 4)]);
      if (c.r() > 0.55) o += ci(x + (x === 0 ? w - h * 0.1 : h * 0.6), i * h + h / 2, h * 0.26, T[5]);
    }
    return o;
  };
  L.net = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', n = 16 + Math.floor(c.r() * 10), p = [], i, j;
    o += sh(SH(c), c.rr(0.2, 0.8) * W, c.rr(0.3, 0.7) * H, c.u * 0.55, c.r() * 6, T[1]);
    for (i = 0; i < n; i++) p.push([c.r() * W, c.r() * H, c.u * c.rr(0.015, 0.06)]);
    for (i = 0; i < n; i++) for (j = i + 1; j < n; j++) if (Math.hypot(p[i][0] - p[j][0], p[i][1] - p[j][1]) < c.u * 0.45)
      o += '<path d="M' + f1(p[i][0]) + ' ' + f1(p[i][1]) + 'L' + f1(p[j][0]) + ' ' + f1(p[j][1]) + '" stroke="' + T[2] + '" stroke-width="' + f1(c.u * 0.012) + '" stroke-linecap="round"/>';
    for (i = 0; i < n; i++) o += ci(p[i][0], p[i][1], p[i][2], i % 5 === 0 ? T[5] : T[i % 2 ? 3 : 4]);
    return o;
  };
  L.graph = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', s = c.u / 6, x, y, d = '', i, ph = c.r() * 6, k = c.rr(1.2, 2.4), sw = f1(c.u * 0.014);
    for (x = s; x < W; x += s) o += '<path d="M' + f1(x) + ' 0V' + H + '" stroke="' + T[1] + '" stroke-width="' + sw + '"/>';
    for (y = s; y < H; y += s) o += '<path d="M0 ' + f1(y) + 'H' + W + '" stroke="' + T[1] + '" stroke-width="' + sw + '"/>';
    for (i = 0; i <= 60; i++) d += (i ? 'L' : 'M') + f1(i / 60 * W) + ' ' + f1(H * 0.5 + Math.sin(i / 60 * 6.28 * k + ph) * H * 0.28 * (0.6 + i / 100));
    o += '<path d="' + d + '" fill="none" stroke="' + T[3] + '" stroke-width="' + f1(c.u * 0.05) + '" stroke-linecap="round" stroke-linejoin="round"/>';
    for (i = 0; i < 3; i++) o += ci(c.rr(0.15, 0.85) * W, c.rr(0.2, 0.8) * H, c.u * 0.06, T[5 - i * 1]);
    return o;
  };
  L.arches = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', n = 3 + Math.floor(c.r() * 3), w = W / n, i, j;
    for (i = 0; i < n; i++) for (j = 0; j < 3; j++) {
      var iw = w * (1 - j * 0.28) - w * 0.1;
      o += N.arch(i * w + (w - iw) / 2, H - (H * 0.95) * (1 - j * 0.2) + (H * 0.05), iw, H * 0.95 * (1 - j * 0.2), T[(i + j) % 2 ? 1 + j : 2 + (j ? 1 : 0)]);
    }
    return o + ci(c.rr(0.2, 0.8) * W, H * 0.22, c.u * 0.1, T[5]);
  };
  L.mosaic = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', s = c.u / c.pick([3, 4, 5]), gp = s * 0.08, x, y;
    for (y = 0; y * s < H; y++) for (x = 0; x * s < W; x++) {
      var t = c.r(), cx = x * s + s / 2, cy = y * s + s / 2;
      if (t < 0.55) o += sh(c.pick(['squircle', 'pebble', 'cookie']), cx, cy, s / 2 - gp, c.r() * 6, T[1 + Math.floor(c.r() * 4)]);
      else if (t < 0.7) o += sh(SH(c), cx, cy, s / 2 - gp, c.r() * 6, T[5]);
    }
    return o;
  };
  L.ribbons = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', n = 5 + Math.floor(c.r() * 3), a = c.rr(-0.6, -0.3), i, th = c.u * 0.22;
    for (i = 0; i < n; i++) {
      var cx = (i / (n - 1)) * W * 1.1, cy = H * c.rr(0.2, 0.8);
      o += '<g transform="translate(' + f1(cx) + ' ' + f1(cy) + ') rotate(' + f1(a * 57.3) + ')">' + rc(-W * 0.4, -th / 2, W * c.rr(0.5, 0.9), th, th / 2, T[1 + (i % 4)]) + '</g>';
    }
    return o + ci(c.rr(0.1, 0.9) * W, c.rr(0.15, 0.85) * H, c.u * 0.12, T[5]);
  };
  L.bars = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', n = 7 + Math.floor(c.r() * 4), w = W / n, i;
    for (i = 0; i < n; i++) {
      var h = H * (0.25 + 0.65 * (i / n) * c.rr(0.7, 1.15)), r = Math.min(w * 0.4, 40);
      o += rc(i * w + w * 0.1, H - h, w * 0.8, h + r, r, T[1 + (i % 4)]);
      if (i > n - 3) o += ci(i * w + w / 2, H - h - w * 0.35, w * 0.22, T[5]);
    }
    return o;
  };
  L.sunset = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', cx = c.rr(0.3, 0.75) * W, cy = H * 0.52, R = H * 0.34, i;
    o += ci(cx, cy, R, T[5]);
    for (i = 0; i < 6; i++) o += rc(cx - R - 4, cy + R * (0.1 + i * 0.16), R * 2 + 8, R * 0.05 * (i + 1), 0, T[0]);
    o += rc(0, H * 0.78, W, H, 0, T[3]);
    o += rc(0, H * 0.88, W, H, 0, T[4]);
    for (i = 0; i < 5; i++) o += rc(c.r() * W, c.rr(0.1, 0.4) * H, c.u * c.rr(0.2, 0.5), c.u * 0.05, c.u * 0.025, T[2]);
    return o;
  };
  L.folds = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', n = 4 + Math.floor(c.r() * 3), i, x = 0, pts;
    for (i = 0; i < n; i++) {
      var w = W * c.rr(0.25, 0.5), y1 = c.r() * H, y2 = c.r() * H;
      pts = 'M' + f1(x) + ' 0L' + f1(x + w) + ' 0L' + f1(x + w * 0.3) + ' ' + H + 'L' + f1(x - w * 0.7) + ' ' + H + 'Z';
      o += '<path d="' + pts + '" fill="' + T[1 + (i % 4)] + '"/>'; x += w * 0.7;
    }
    return o + sh(SH(c), c.rr(0.2, 0.8) * W, c.rr(0.3, 0.7) * H, c.u * 0.2, c.r() * 6, T[5]) + sh(SH(c), c.rr(0.2, 0.9) * W, c.rr(0.2, 0.9) * H, c.u * 0.12, c.r() * 6, T[3]);
  };
  L.tiles = function (c) {
    var T = c.T, W = c.W, H = c.H, o = '', s = c.u / c.pick([2, 3]), x, y, q;
    for (y = 0; y * s < H; y++) for (x = 0; x * s < W; x++) {
      q = (x + y * 2 + Math.floor(c.r() * 2)) % 4;
      o += rc(x * s, y * s, s, s, 0, T[1 + (q % 2)]) + N.quarter(x * s, y * s, s, q, T[3]) + ci(x * s + s * (q % 2 ? 0.74 : 0.26), y * s + s * (q > 1 ? 0.26 : 0.74), s * 0.1, T[5]);
    }
    return o;
  };
  N.layoutNames = Object.keys(L);
})(typeof window !== 'undefined' ? window : globalThis);
