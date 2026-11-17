/* NEBians M3X Art Library v2 — M3 Expressive Architectural, Isometric & Swiss Poster Layouts (14 compositions). */
(function (g) {
  'use strict';
  var V = g.NebArtV2, L = V.layouts, f1 = V.f1, sh = V.shape, ci = V.circle, rc = V.rect, ln = V.line, pl = V.poly, rg = V.ring;
  var SH = function (c) { return c.pick(V.shapeNames); };

  /* 1. isoMonolith: Signature NEBians 30-deg isometric architectural city & book-N monuments */
  L.isoMonolith = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = '', i;
    o += sh('sunny', W * c.rr(0.2, 0.8), H * 0.32, u * 0.44, c.r() * 4, T[1]);
    var blocks = [[0.26, 0.26, 0.24, 0.24, 0.42, 7, 3, 5], [0.48, 0.18, 0.30, 0.30, 0.52, 6, 4, 5], [0.70, 0.28, 0.26, 0.26, 0.38, 7, 2, 4], [0.38, 0.46, 0.22, 0.22, 0.28, 2, 3, 5], [0.60, 0.48, 0.22, 0.22, 0.26, 7, 4, 5]];
    for (i = 0; i < blocks.length; i++) {
      var b = blocks[i];
      o += V.isoBox(W * b[0], H * b[1], u * b[2], u * b[3], u * b[4], T[b[5]], T[b[6]], T[b[7]], T[0]);
    }
    return o;
  };

  /* 2. expressiveTotem: Stacked interlocking M3X silhouettes in Swiss poster balance */
  L.expressiveTotem = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = '', n = 4, i;
    for (i = 0; i < n; i++) {
      var cx = W * (0.18 + (i / (n - 1)) * 0.64), cy = H * c.rr(0.28, 0.72), r = u * c.rr(0.24, 0.38);
      o += sh(SH(c), cx, cy, r, c.r() * 6, T[1 + (i % 4)]) + sh(SH(c), cx, cy, r * 0.52, c.r() * 6, i === 2 ? T[6] : T[5]);
    }
    return o;
  };

  /* 3. swissGrid: Modular Josef Muller-Brockmann geometric grid with quarter-arcs, pills & M3X cutouts */
  L.swissGrid = function (c) {
    var T = c.T, W = c.W, H = c.H, s = H / (c.r() > 0.45 ? 2 : 3), cols = Math.ceil(W / s), rows = Math.ceil(H / s), o = '', x, y;
    for (y = 0; y < rows; y++) for (x = 0; x < cols; x++) {
      var t = c.r(), q = Math.floor(c.r() * 4), f = T[1 + ((x + y) % 5)], gx = x * s, gy = y * s;
      o += rc(gx + 2, gy + 2, s - 4, s - 4, s * 0.14, T[1]);
      if (t < 0.30) o += V.quarter(gx + 2, gy + 2, s - 4, q, f);
      else if (t < 0.54) o += sh(SH(c), gx + s / 2, gy + s / 2, s * 0.38, c.r() * 6, (x + y) % 4 === 0 ? T[6] : f);
      else if (t < 0.76) o += V.arch(gx + s * 0.14, gy + s * 0.1, s * 0.72, s * 0.84, f);
      else o += ci(gx + s / 2, gy + s / 2, s * 0.34, T[4]) + ci(gx + s / 2, gy + s / 2, s * 0.14, T[7]);
    }
    return o;
  };

  /* 4. contourTopography: Nested organic elevation bands using multi-harmonic polar splines */
  L.contourTopography = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cx = W * c.rr(0.32, 0.72), cy = H * c.rr(0.3, 0.7), R = Math.max(W, H) * 0.65, o = '', i;
    var k = c.pick(['pebble', 'cookie', 'flower', 'clover']), rot = c.r() * 6;
    for (i = 7; i >= 1; i--) {
      o += sh(k, cx, cy, R * (i / 7), rot + i * 0.14, T[1 + (i % 4)]);
    }
    o += sh('sunny', cx, cy, u * 0.16, rot, T[6]) + ci(cx, cy, u * 0.06, T[5]);
    return o;
  };

  /* 5. bauhausChronicle: Architectural Bauhaus blocks, half-pills, striped discs & balance beams */
  L.bauhausChronicle = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = '';
    o += rc(W * 0.06, H * 0.12, W * 0.42, H * 0.76, u * 0.08, T[1]);
    o += V.arch(W * 0.12, H * 0.22, W * 0.30, H * 0.66, T[4]) + ci(W * 0.27, H * 0.42, u * 0.12, T[6]);
    o += rc(W * 0.54, H * 0.12, W * 0.40, H * 0.34, u * 0.17, T[3]) + ci(W * 0.64, H * 0.29, u * 0.11, T[7]);
    o += rc(W * 0.54, H * 0.54, W * 0.40, H * 0.34, u * 0.08, T[5]) + sh('flower', W * 0.74, H * 0.71, u * 0.13, 0.3, T[6]);
    return o;
  };

  /* 6. kineticRibbons: Woven stadium tracks with sliding expressive medallions */
  L.kineticRibbons = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, n = 5, h = H / (n + 1), o = '', i;
    for (i = 0; i < n; i++) {
      var w = W * c.rr(0.48, 0.84), left = i % 2 === 0, x = left ? -h : W - w + h, y = h * (0.45 + i * 1.02);
      o += rc(x, y, w, h * 0.78, h * 0.39, T[1 + (i % 4)]);
      var mx = left ? x + w - h * 0.45 : x + h * 0.45;
      o += sh(SH(c), mx, y + h * 0.39, h * 0.28, i, i === 2 ? T[6] : T[5]);
    }
    return o;
  };

  /* 7. orbitalResonance: Eccentric nested orbital tracks with satellite expressive shapes */
  L.orbitalResonance = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cx = W * c.rr(0.45, 0.65), cy = H * 0.5, o = '', i;
    o += sh('burst', cx, cy, u * 0.22, c.r() * 4, T[5]) + ci(cx, cy, u * 0.09, T[6]);
    for (i = 1; i <= 4; i++) {
      var r = u * (0.24 + i * 0.16), a = c.r() * 6.28;
      o += rg(cx, cy, r, u * 0.016, T[1 + (i % 3)]);
      o += sh(SH(c), cx + Math.cos(a) * r, cy + Math.sin(a) * r, u * (0.06 + (4 - i) * 0.015), a, i === 2 ? T[6] : T[4]);
    }
    return o;
  };

  /* 8. stainedMosaic: Interlocking squircle, pebble, and clover tessellation */
  L.stainedMosaic = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, s = u / 3, gp = s * 0.08, o = '', x, y;
    for (y = 0; y * s < H; y++) for (x = 0; x * s < W; x++) {
      var cx = x * s + s / 2, cy = y * s + s / 2, idx = (x * 3 + y * 5) % 6;
      o += sh(c.pick(['squircle', 'cookie', 'pebble', 'clover']), cx, cy, s / 2 - gp, (x + y) * 0.4, idx === 4 ? T[6] : T[1 + (idx % 4)]);
    }
    return o;
  };

  /* 9. horizonTerrace: Stepped architectural terraces under a radiant M3X sunny medallion */
  L.horizonTerrace = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, sx = W * c.rr(0.28, 0.72), o = '', i;
    o += sh('sunny', sx, H * 0.34, u * 0.32, 0.2, T[6]) + ci(sx, H * 0.34, u * 0.16, T[7]);
    for (i = 0; i < 5; i++) {
      var y = H * (0.48 + i * 0.11);
      o += rc(0, y, W, H - y, u * 0.04, T[1 + (i % 4)]);
    }
    return o;
  };

  /* 10. prismFacets: Flat polygonal geometric facets (zero gradients) */
  L.prismFacets = function (c) {
    var T = c.T, W = c.W, H = c.H, nx = 5, ny = 3, pts = [], o = '', x, y;
    for (y = 0; y <= ny; y++) {
      pts[y] = [];
      for (x = 0; x <= nx; x++) {
        var jx = (x === 0 || x === nx) ? 0 : c.rr(-0.28, 0.28) * (W / nx);
        var jy = (y === 0 || y === ny) ? 0 : c.rr(-0.28, 0.28) * (H / ny);
        pts[y][x] = [x * (W / nx) + jx, y * (H / ny) + jy];
      }
    }
    for (y = 0; y < ny; y++) for (x = 0; x < nx; x++) {
      o += pl([pts[y][x], pts[y][x + 1], pts[y + 1][x + 1]], T[1 + ((x + y) % 4)]);
      o += pl([pts[y][x], pts[y + 1][x + 1], pts[y + 1][x]], (x === 2 && y === 1) ? T[6] : T[2 + ((x * 2 + y) % 4)]);
    }
    return o;
  };

  /* 11. botanicalGrove: Stylized flat-tonal canopy of clovers, flowers, and trunks */
  L.botanicalGrove = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = '', n = 5, i;
    o += rc(0, H * 0.82, W, H * 0.18, 0, T[3]);
    for (i = 0; i < n; i++) {
      var tx = W * (0.12 + (i / (n - 1)) * 0.76), ty = H * c.rr(0.32, 0.56), r = u * c.rr(0.18, 0.28);
      o += sh(c.pick(['clover', 'flower', 'cookie', 'lotus']), tx, ty, r, i * 0.5, i === 2 ? T[6] : T[1 + (i % 4)]);
      o += rc(tx - u * 0.022, ty, u * 0.044, H * 0.84 - ty, u * 0.02, T[5]);
    }
    return o;
  };

  /* 12. waveformHarmonic: Layered harmonic step-bars and phase waves */
  L.waveformHarmonic = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, n = 18, bw = W / n, o = '', i;
    for (i = 0; i < n; i++) {
      var h = H * (0.2 + 0.62 * Math.pow(Math.sin((i / n) * Math.PI), 1.4) * c.rr(0.75, 1.1));
      o += rc(i * bw + bw * 0.14, H - h, bw * 0.72, h + u * 0.05, bw * 0.36, T[1 + (i % 4)]);
      if (i % 4 === 2) o += ci(i * bw + bw / 2, H - h - bw * 0.45, bw * 0.26, T[6]);
    }
    return o;
  };

  /* 13. archwayCloister: Nested perspective colonnade arches */
  L.archwayCloister = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, n = 4, w = W / n, o = '', i, j;
    for (i = 0; i < n; i++) for (j = 0; j < 3; j++) {
      var iw = w * (0.86 - j * 0.22), ih = H * (0.9 - j * 0.18);
      o += V.arch(i * w + (w - iw) / 2, H - ih, iw, ih, (i === 1 && j === 2) ? T[6] : T[1 + ((i + j) % 4)]);
    }
    return o;
  };

  /* 14. radialMandala: Precision geometric lotus symmetry built from M3X lobed polygons */
  L.radialMandala = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cx = W * c.rr(0.45, 0.72), cy = H * 0.5, R = u * 0.48, o = '', i;
    var shapes = ['lotus', 'burst', 'flower', 'sunny', 'cookie', 'clover'];
    for (i = 0; i < 6; i++) {
      o += sh(shapes[i], cx, cy, R * (1 - i * 0.14), i * 0.28, i === 4 ? T[6] : T[1 + (i % 4)]);
    }
    return o + ci(cx, cy, R * 0.1, T[7]);
  };
})(typeof window !== 'undefined' ? window : globalThis);
