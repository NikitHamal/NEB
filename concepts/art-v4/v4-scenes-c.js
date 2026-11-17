/* v4 scenes C: terrazzo, memphis, glyphField, weave, bloomField, scallop, ribbonStack, pennants-free bunting dots. */
(function (g) {
  'use strict';
  var A = g.NebArtV4, E = A.engines, f = A.f, sin = Math.sin, cos = Math.cos, PI = Math.PI;
  var SH = ['cookie', 'flower', 'clover', 'burst', 'sunny', 'puffy', 'pebble', 'squircle', 'lotus', 'gem'];

  E.terrazzo = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), N = Math.round(60 + w * h / (m * m) * 60), i, s = '', n, a, rad, pts, j, col, kit = P.kit.concat([P.snow, P.t(0.02)]);
    s += A.rect(0, 0, w, h, 0, P.t(r.range(0.04, 0.16)));
    for (i = 0; i < N; i++) {
      rad = m * r.range(0.012, 0.075) * (r.chance(0.12) ? 1.7 : 1); n = r.int(4, 6); pts = []; a = r() * 6;
      for (j = 0; j < n; j++) pts.push([r.range(0, 1) * 0 + Math.cos(a + j / n * 6.28) * rad * r.range(0.55, 1), Math.sin(a + j / n * 6.28) * rad * r.range(0.55, 1)]);
      col = r.chance(0.09) ? P.pop : r.pick(kit);
      s += '<g transform="translate(' + f(r() * w) + ' ' + f(r() * h) + ')">' + A.path(A.rpoly(pts, rad * 0.25), col) + '</g>';
    }
    return s;
  };

  E.memphis = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), N = Math.round(14 + w * h / (m * m) * 12), i, s = '', x, y, t, col, z;
    s += A.rect(0, 0, w, h, 0, P.t(0.06));
    for (i = 0; i < N; i++) {
      x = r() * w; y = r() * h; z = m * r.range(0.04, 0.1); t = r.int(0, 7); col = r.chance(0.2) ? P.pop : P.t(r.range(0.25, 0.85));
      if (t === 0) s += A.shape(r.pick(SH), x, y, z, r() * 3, col);
      else if (t === 1) s += A.circle(x, y, z * 0.7, 'none', 'stroke="' + col + '" stroke-width="' + f(z * 0.28) + '"');
      else if (t === 2) s += A.zig(x, y, z * 1.8, z * 0.5, 5, z * 0.2, col);
      else if (t === 3) s += A.squig(x, y, z * 2, z * 0.6, 2, z * 0.22, col);
      else if (t === 4) s += A.plus(x, y, z * 0.5, z * 0.22, col);
      else if (t === 5) s += A.pill(x, y, z * 2, z * 0.5, col, 'transform="rotate(' + r.int(-40, 40) + ' ' + f(x) + ' ' + f(y) + ')"');
      else if (t === 6) s += A.sparkle(x, y, z * 0.7, col);
      else s += A.path(A.ngon(3, x, y, z * 0.7, r() * 3, z * 0.15), col);
    }
    return s;
  };

  E.glyphField = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), names = c.o.glyphs || ['functions', 'science', 'bolt', 'menu_book', 'public', 'code'], gs = m / r.range(3.2, 4.6), s = '', x, y, k = 0, j = 0, tile, col;
    s += A.rect(0, 0, w, h, 0, P.t(0.08));
    for (y = -gs * 0.2; y < h; y += gs, j++) for (x = -gs * 0.2 + (j % 2) * gs * 0.5; x < w; x += gs, k++) {
      tile = (k + j) % 3; col = (k % 7 === 3) ? P.pop : P.t(0.28 + 0.14 * (k % 5));
      s += A.shape(['cookie', 'squircle', 'flower', 'pebble'][(k + j) % 4], x + gs * 0.5, y + gs * 0.5, gs * 0.42, k, A.mix(P.t(0.14 + 0.1 * (tile)), P.sky, 0.1)) + A.glyph(names[(k + j * 2) % names.length], x + gs * 0.5 - gs * 0.2, y + gs * 0.5 - gs * 0.2, gs * 0.4, col === P.pop ? P.pop : P.t(0.7));
    }
    return s;
  };

  E.weave = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), bw = m / r.int(6, 9), s = '', i, j, x, y, cols = Math.ceil(w / bw) + 1, rows = Math.ceil(h / bw) + 1, tc = [], rc = [];
    for (i = 0; i < cols; i++) tc.push(r.chance(0.12) ? P.pop : P.t(0.12 + 0.12 * (i % 4)));
    for (j = 0; j < rows; j++) rc.push(P.t(0.4 + 0.12 * (j % 4)));
    s += A.rect(0, 0, w, h, 0, P.t(0.04));
    for (j = 0; j < rows; j++) s += A.pill(-bw, j * bw + bw * 0.1, w + 2 * bw, bw * 0.8, rc[j]);
    for (i = 0; i < cols; i++) for (j = 0; j < rows; j++) if ((i + j) % 2) s += A.pill(i * bw + bw * 0.1, j * bw - bw * 0.05, bw * 0.8, bw * 1.1, tc[i]);
    return s;
  };

  E.bloomField = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), s = '', N = Math.round(5 + w * h / (m * m) * 3), i, x, y, R, sh, k;
    s += A.rect(0, 0, w, h, 0, P.t(0.06));
    for (i = 0; i < N; i++) {
      x = r() * w; y = r() * h; R = m * r.range(0.14, 0.34); sh = r.pick(SH);
      s += A.shape(sh, x, y, R, r() * 3, P.t(r.range(0.12, 0.6))) + A.shape(sh, x, y, R * 0.62, r() * 3, r.chance(0.2) ? P.pop : P.t(r.range(0.3, 0.85))) + A.shape(r.pick(SH), x, y, R * 0.26, r() * 3, P.snow);
    }
    return s;
  };

  E.scallop = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), R = m / r.int(5, 8), s = '', rows = Math.ceil(h / (R * 0.5)) + 2, j, i, x, y, k, t;
    s += A.rect(0, 0, w, h, 0, P.t(0.05));
    for (j = rows; j >= 0; j--) for (i = -1; i < w / (R * 2) + 1; i++) {
      x = i * R * 2 + (j % 2 ? R : 0); y = j * R * 0.5;
      for (k = 4; k >= 1; k--) s += A.circle(x, y, R * k / 4, (k === 1 && r.chance(0.06)) ? P.pop : P.t(0.08 + 0.1 * (4 - k) + 0.1 * (j % 3) * 0.5), 'stroke="' + P.sky + '" stroke-width="' + f(R * 0.03) + '"');
    }
    return s;
  };

  E.ribbonStack = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), n = r.int(5, 8), i, s = '', y, th = h / n, ph = r() * 5, col, a;
    for (i = 0; i < n; i++) {
      y = th * (i + 0.5); a = th * r.range(0.4, 1.1); col = i === r.int(1, n - 2) ? P.pop : P.t(0.1 + 0.8 * i / n);
      s += A.stroke(A.smooth(A.wave(-60, w + 60, y, a, w * r.range(0.6, 1.2), ph + i * 0.8, 30, 0.3), false), th * 0.78, col);
    }
    return s;
  };
})(typeof window !== 'undefined' ? window : globalThis);
