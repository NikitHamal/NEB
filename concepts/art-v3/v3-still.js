/* v3 still engine: one study object on a calm M3X backdrop (disc, arch, plate, ground, pattern) + sparkle decor. */
(function (g) {
  'use strict';
  var A = g.NebArtV3, E = A.engines, R = A.rect, C = A.circle;
  var CALM = ['waves', 'shapeField', 'scallop', 'dhaka', 'bubbles', 'confetti', 'truchet', 'lattice', 'pills', 'arches', 'ribbons', 'bauhaus'];
  A.objectNames = function () { return Object.keys(A.objects); };
  function decor(c, cx, cy, avoid, n) {
    var r = c.r, P = c.P, o = '', i, x, y, t, tries = 0, cols = [P.sp(0.55), P.t(0.55), P.t(0.8), P.snow];
    for (i = 0; i < n && tries < 60; tries++) { x = r.range(0.05, 0.95) * c.w; y = r.range(0.08, 0.92) * c.h; if (Math.hypot(x - cx, y - cy) < avoid) continue; t = r.int(0, 3); i++;
      o += t === 0 ? A.star4(x, y, c.h * r.range(0.03, 0.06), cols[r.int(0, 1)]) : t === 1 ? C(x, y, c.h * r.range(0.008, 0.02), cols[r.int(0, 2)]) : t === 2 ? A.shape(r.pick(['flower', 'cookie', 'clover']), x, y, c.h * r.range(0.025, 0.05), r.range(0, 3), cols[r.int(0, 2)]) : A.line(x - c.h * 0.02, y, x + c.h * 0.02, y, 3, cols[1]) + A.line(x, y - c.h * 0.02, x, y + c.h * 0.02, 3, cols[1]); }
    return o;
  }
  E.still = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), wide = w / h > 1.6, objs = c.o.objs || [r.pick(A.objectNames())], main = objs[0], style = c.o.style || r.pick(['disc', 'arch', 'plate', 'ground', 'pattern', 'disc', 'plate']);
    var cx = wide ? w * (c.o.side === 'left' ? 0.28 : r.chance(0.7) ? 0.74 : 0.5) : w / 2, cy = h * (wide ? 0.5 : 0.5), sz = m * (wide ? 0.66 : 0.6), o = '', shp = r.pick(['cookie', 'sunny', 'cookie12', 'puffy', 'lotus', 'squircle', 'pebble', 'burst']);
    if (style === 'pattern') o += E[r.pick(CALM)](c).replace(/<svg[^>]*>/, ''); else o += R(0, 0, w, h, 0, style === 'plate' ? P.t(0.5) : style === 'ground' ? P.sky : P.t(0.08));
    if (style === 'disc') o += A.shape(shp, cx, cy, m * 0.44, r.range(0, 3), P.t(0.2)) + A.shape(shp, cx, cy, m * 0.33, r.range(0, 3), P.t(0.34));
    else if (style === 'arch') o += A.arch(cx - m * 0.4, cy - m * 0.5, m * 0.8, m * 1.2, P.t(0.26)) + A.arch(cx - m * 0.3, cy - m * 0.4, m * 0.6, m * 1.1, P.t(0.12));
    else if (style === 'plate') o += A.shape(shp, cx, cy, m * 0.4, r.range(0, 3), P.paper);
    else if (style === 'ground') o += R(0, h * 0.74, w, h * 0.26, 0, P.t(0.32)) + C(cx - m * 0.4, cy - m * 0.3, m * 0.28, P.glow) + C(cx - m * 0.4, cy - m * 0.3, m * 0.16, P.sun) + A.shape('puffy', cx, cy, m * 0.42, 0.2, P.t(0.12));
    else o += A.shape(shp, cx, cy, m * 0.4, r.range(0, 3), P.paper);
    o += decor(c, cx, cy, m * 0.5, wide ? 9 : 6);
    if (wide && objs.length > 1) o += A.drawObj(objs[1], P, w * (cx > w * 0.6 ? 0.22 : 0.74), h * 0.62, m * 0.36, -12 + r.int(-6, 6)) + A.drawObj(objs[2] || objs[0], P, w * (cx > w * 0.6 ? 0.4 : 0.9), h * 0.3, m * 0.24, 14);
    return o + A.drawObj(main, P, cx, cy + (style === 'ground' ? m * 0.06 : 0), sz * 1.0, 0);
  };
})(typeof window !== 'undefined' ? window : globalThis);
