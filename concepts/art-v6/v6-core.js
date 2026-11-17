/* NEBians M3X Art Library v6 - core.
   Builds on the v3 OKLCH palettes and the v4 flat helpers and hero objects (read, never edited). Adds: partner colour per family (so a piece is a tonal
   family plus one warm or cool accent), scheme (calm or deep), Voronoi, calm panel, rounded helpers.
   Flat fills only. No gradients, shadows, filters, text, emoji, pixels, rings on avatars.
   BANNED SUBJECTS (owner): mountains, forests, trees, ships, boats, building rows, moon, sun. Nothing here draws them. */
(function (g) {
  'use strict';
  var V3 = g.NebArtV3, V4 = g.NebArtV4;
  if (!V3 || !V4) throw new Error('load v3-core.js and the v4 core, objects first');
  var A = g.NebArtV6 = { engines: {}, kinds: {}, subjects: {}, objects: V4.objects, people: {} };
  ['hash', 'rng', 'f', 'oklch', 'shapeNames', 'smooth', 'shapeD', 'rpoly', 'ngon', 'path', 'shape', 'circle', 'rect', 'line', 'stroke', 'poly', 'arch', 'star4', 'glyph', 'noise', 'svg',
    'blob', 'wave', 'band', 'clip', 'clipRect', 'g', 'rot', 'sparkle', 'plus', 'zig', 'squig', 'pill', 'mix', 'obj'].forEach(function (k) { A[k] = V4[k] || V3[k]; });
  var f = A.f, sin = Math.sin, cos = Math.cos, PI = Math.PI;
  A.palettes = V3.palettes.filter(function (n) { return n !== 'sun'; });
  var PAIR = { brand: 'marigold', cobalt: 'coral', sky: 'terracotta', aqua: 'coral', teal: 'rose', emerald: 'marigold', mint: 'coral', moss: 'rose', lime: 'terracotta', amber: 'denim',
    marigold: 'brand', terracotta: 'teal', coral: 'aqua', rose: 'pine', crimson: 'sky', slate: 'amber', sand: 'cobalt', pine: 'coral', denim: 'marigold' };
  /* palette: V4 kit plus partner family q, ordered ramp, accent list */
  A.palette = function (name, mode) {
    var P = V4.palette(name, mode), q = V4.palette(PAIR[name] || 'amber', mode);
    P.q = q; P.ramp = [0.07, 0.16, 0.27, 0.4, 0.54, 0.68, 0.82].map(function (k) { return P.t(k); });
    P.acc = [q.t(0.46), q.t(0.3), q.t(0.62)]; P.accSoft = q.t(0.2);
    return P;
  };
  /* scheme: bg plus ramp ordered by growing contrast to the bg; deep = punchy variant. */
  A.scheme = function (P, r, deep) {
    var dk = P.dark, s = { deep: !!deep };
    if (deep) {
      s.bg = dk ? P.t(0.12) : P.t(0.84);
      s.ramp = (dk ? [0.2, 0.3, 0.42, 0.55, 0.68, 0.8] : [0.72, 0.6, 0.48, 0.34, 0.2, 0.08]).map(function (k) { return P.t(k); });
      s.acc = [P.q.t(dk ? 0.62 : 0.42), P.q.t(dk ? 0.78 : 0.3), P.q.t(dk ? 0.5 : 0.56)]; s.ink = dk ? P.t(0.92) : P.t(0.04);
    } else {
      s.bg = P.t(0.05); s.ramp = [0.12, 0.2, 0.3, 0.42, 0.56, 0.7].map(function (k) { return P.t(k); });
      s.acc = P.acc; s.ink = P.ink;
    }
    s.card = deep ? (dk ? P.t(0.2) : P.t(0.94)) : P.card; s.P = P; return s;
  };
  A.pickDeep = function (c, p) { return c.o.deep != null ? c.o.deep : c.r.chance(p == null ? 0.3 : p); };
  /* Voronoi cells for sites inside a w x h box: half-plane clipping, returns polygons */
  A.voronoi = function (sites, w, h) {
    return sites.map(function (s, i) {
      var poly = [[0, 0], [w, 0], [w, h], [0, h]], j, t, out, a, b, da, db, mx, my, nx, ny, k;
      for (j = 0; j < sites.length && poly.length; j++) {
        if (j === i) continue; t = sites[j]; mx = (s[0] + t[0]) / 2; my = (s[1] + t[1]) / 2; nx = t[0] - s[0]; ny = t[1] - s[1]; out = [];
        for (k = 0; k < poly.length; k++) {
          a = poly[k]; b = poly[(k + 1) % poly.length]; da = (a[0] - mx) * nx + (a[1] - my) * ny; db = (b[0] - mx) * nx + (b[1] - my) * ny;
          if (da <= 0) out.push(a);
          if ((da < 0 && db > 0) || (da > 0 && db < 0)) { var u = da / (da - db); out.push([a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u]); }
        }
        poly = out;
      }
      return poly;
    });
  };
  A.centroid = function (p) { var x = 0, y = 0; p.forEach(function (q) { x += q[0]; y += q[1]; }); return [x / p.length, y / p.length]; };
  /* calm panel: a paper-edged wave on the left so a profile picture and a name sit on quiet colour */
  A.calm = function (w, h, P, r, frac, bg) {
    var x = w * (frac || 0.34), pts = [], i, n = 6, ph = r() * 6;
    for (i = 0; i <= n; i++) pts.push([x + w * 0.035 * sin(i * 1.3 + ph), h * i / n]);
    var d = 'M0 0L' + f(pts[0][0]) + ' 0' + A.smooth(pts, false).replace(/^M[^C]*/, '') + 'L0 ' + h + 'Z', d2 = d.replace(/(-?\d+\.?\d*) /g, function (m, a) { return m; });
    return '<g transform="translate(' + f(w * 0.014) + ' 0)">' + A.path(d, P.t(0.16)) + '</g>' + A.path(d, bg || P.t(0.04));
  };
  /* sample a smooth 2D field from two value-noise streams */
  A.field = function (seed, sx, sy) { var n1 = A.noise(seed + 'a'), n2 = A.noise(seed + 'b'); return function (x, y) { return 0.62 * n1(x * sx + n2(y * sy) * 2.2) + 0.38 * n2(y * sy + 3.1 + n1(x * sx * 0.7) * 1.4); }; };
  A.make = function (s) {
    var w = s.w, h = s.h, mode = s.mode || 'light', P = A.palette(s.palette || 'brand', mode), key = (s.id || s.engine) + ':' + (s.seed || 0), r = A.rng(key);
    var uid = 'v' + (A.hash(key) % 100000), fn = A.engines[s.engine];
    if (!fn) throw new Error('unknown engine ' + s.engine);
    return A.svg(w, h, fn({ w: w, h: h, P: P, r: r, uid: uid, subj: s.subj, o: s.o || {}, mode: mode, kind: s.kind }), P.sky);
  };
})(typeof window !== 'undefined' ? window : globalThis);
