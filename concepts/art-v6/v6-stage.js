/* v6 stage: `show` (a v6 scene behind a hero object on a plate) and `empty` (pal + prop empty states, four compositions).
   o for show = { scene, objs:[main, chip, chip], plate: card|shape|ring, side: left|center|right, calm:bool, deep }.
   o for empty = { prop, chip, scene, look: 0..3, spec }. */
(function (g) {
  'use strict';
  var A = g.NebArtV6, E = A.engines, f = A.f, sin = Math.sin, cos = Math.cos, PI = Math.PI;
  var SH = ['cookie', 'flower', 'clover', 'burst', 'sunny', 'puffy', 'pebble', 'squircle', 'lotus', 'gem'];
  A.SCENES = ['truchet', 'bauhaus', 'voronoi', 'lowpoly', 'silk', 'vortex', 'bento', 'dotwave', 'packing', 'morphGrid', 'doodle'];
  function inner(c, scene, o) { return E[scene]({ w: c.w, h: c.h, P: c.P, r: c.r, uid: c.uid + 's', o: o || {}, mode: c.mode, kind: c.kind }); }
  function sparks() { return ''; } /* owner: no scattered dots or sparkles */
  function chip(P, name, x, y, d, c) { return A.shape(c.r.pick(['cookie', 'squircle', 'flower']), x, y, d, c.r() * 3, P.card) + A.obj(name, P, x, y, d * 1.3, c.r.int(-8, 8)); }

  E.show = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = c.o, m = Math.min(w, h), wide = w / h > 1.5, tall = h / w > 1.3, objs = o.objs || ['book'], side = o.side || (wide ? 'right' : 'center'), plate = o.plate || r.pick(['card', 'shape', 'ring']), s, k;
    var cx = side === 'right' ? w * 0.77 : side === 'left' ? w * 0.23 : w / 2, cy = tall ? h * 0.44 : h * 0.5, pl = m * (wide ? 0.9 : tall ? 0.8 : 0.78), big = pl * 0.6;
    s = inner(c, o.scene || 'bauhaus', { deep: o.deep });
    if (o.calm) s += A.calm(w, h, P, r, 0.36, P.t(0.04));
    if (plate === 'card') {
      s += A.rect(cx - pl * 0.4, cy - pl * 0.4, pl * 0.8, pl * 0.8, pl * 0.2, P.q.t(0.42), 'transform="rotate(9 ' + f(cx) + ' ' + f(cy) + ')"') + A.rect(cx - pl * 0.4, cy - pl * 0.4, pl * 0.8, pl * 0.8, pl * 0.2, P.card, 'transform="rotate(-3 ' + f(cx) + ' ' + f(cy) + ')"') + A.shape(r.pick(SH), cx, cy, pl * 0.3, r() * 3, P.t(0.12));
    } else if (plate === 'shape') {
      s += A.shape(r.pick(SH), cx, cy, pl * 0.5, r() * 3, P.card) + A.shape('cookie', cx, cy, pl * 0.4, r() * 3, P.t(0.14));
    } else s += A.shape(r.pick(SH), cx, cy, pl * 0.52, r() * 3, P.q.t(0.4)) + A.circle(cx, cy, pl * 0.38, P.card) + A.circle(cx, cy, pl * 0.3, P.t(0.1));
    s += sparks(c, cx, cy, pl * 0.6, 6, m, [P.q.t(0.5), P.card, P.q.t(0.3)]);
    s += A.obj(objs[0], P, cx, cy, big, o.tilt == null ? r.int(-8, 8) : o.tilt);
    for (k = 1; k < objs.length; k++) { var a = (k === 1 ? -0.75 : 2.5) + r.range(-0.2, 0.2); s += chip(P, objs[k], cx + cos(a) * pl * 0.46, cy + sin(a) * pl * 0.43, pl * 0.15, c); }
    return s;
  };

  E.empty = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = c.o, m = Math.min(w, h), look = o.look || 0, spec = A.palSpec(r), prop = o.prop || 'magnifier', s, cx = w / 2, cy = h * 0.52, k;
    spec.arms = look === 2 ? 'hold' : look === 3 ? 'wave' : r.pick(['up', 'wave', 'down']);
    var pickSc = o.scene || A.SCENES[(A.hash(c.uid) % 7)] , bg = P.t(0.05);
    s = A.rect(0, 0, w, h, 0, bg);
    if (look === 1) {
      var sh = r.pick(['pebble', 'cookie', 'squircle', 'puffy']);
      s += A.clip(c.uid + 'k', A.shapeD(sh, cx, cy, m * 0.46, r() * 3), inner(c, pickSc, { deep: r.chance(0.4) }));
      s += A.rect(cx - m * 0.2, cy - m * 0.3, m * 0.4, m * 0.38, m * 0.1, P.card, 'transform="rotate(-6 ' + f(cx) + ' ' + f(cy) + ')"') + A.obj(prop, P, cx, cy - m * 0.1, m * 0.34, -6);
      s += A.pal(P, r, cx + m * 0.3, cy + m * 0.2, m * 0.34, spec) + sparks(c, cx, cy, m * 0.5, 5, m, [P.q.t(0.5), P.card]);
    } else if (look === 2) {
      s += A.shape(r.pick(['flower', 'cookie', 'clover']), cx, cy + m * 0.02, m * 0.46, r() * 3, P.t(0.13)) + A.shape('pebble', cx, cy + m * 0.1, m * 0.36, r() * 3, P.t(0.21));
      s += '<ellipse cx="' + f(cx) + '" cy="' + f(cy + m * 0.42) + '" rx="' + f(m * 0.3) + '" ry="' + f(m * 0.05) + '" fill="' + P.t(0.24) + '"/>';
      s += A.pal(P, r, cx - m * 0.06, cy + m * 0.04, m * 0.5, spec) + A.obj(prop, P, cx + m * 0.28, cy + m * 0.12, m * 0.3, 8);
      s += sparks(c, cx, cy, m * 0.55, 6, m, [P.q.t(0.5), P.t(0.5)]);
    } else if (look === 3) {
      s += A.rect(cx - m * 0.4, cy - m * 0.33, m * 0.8, m * 0.6, m * 0.09, P.card, 'transform="rotate(-4 ' + f(cx) + ' ' + f(cy) + ')"') + A.rect(cx - m * 0.4, cy - m * 0.33, m * 0.8, m * 0.6, m * 0.09, 'none', 'stroke="' + P.line + '" stroke-width="2" transform="rotate(-4 ' + f(cx) + ' ' + f(cy) + ')"');
      var row = ''; for (k = 0; k < 3; k++) row += A.pill(cx - m * 0.3, cy - m * 0.22 + k * m * 0.11, m * (0.5 - k * 0.1), m * 0.05, P.t(0.16 + k * 0.04)) + A.circle(cx + m * 0.28, cy - m * 0.195 + k * m * 0.11, m * 0.026, P.q.t(0.45));
      s += A.rot(-4, cx, cy, row);
      s += A.pal(P, r, cx + m * 0.34, cy + m * 0.2, m * 0.36, spec) + A.shape(r.pick(['cookie', 'flower', 'squircle']), cx - m * 0.28, cy - m * 0.28, m * 0.15, r() * 3, P.q.t(0.4)) + A.obj(prop, P, cx - m * 0.28, cy - m * 0.28, m * 0.2, -8);
      s += sparks(c, cx, cy, m * 0.55, 5, m, [P.q.t(0.5), P.t(0.4)]);
    } else {
      s += A.shape(r.pick(['cookie', 'flower', 'puffy']), cx, cy, m * 0.47, r() * 3, P.t(0.12)) + A.shape('pebble', cx, cy + m * 0.04, m * 0.37, r() * 3, P.t(0.2));
      s += A.obj(prop, P, cx + m * 0.2, cy - m * 0.04, m * 0.36, 8) + A.pal(P, r, cx - m * 0.18, cy + m * 0.1, m * 0.4, spec);
      
      s += sparks(c, cx, cy, m * 0.55, 7, m, [P.q.t(0.5), P.t(0.5), P.card]);
    }
    return s;
  };
})(typeof window !== 'undefined' ? window : globalThis);
