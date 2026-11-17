/* v5 face: head, ears, almond eyes with iris and lid line, tapered brows, nose, four mouths. Frameless, flat fills. */
(function (g) {
  'use strict';
  var A = g.NebArtV5, f = A.f, P5 = A.people;
  P5.SKIN = ['#f8dcc8', '#f1c6a4', '#e3aa80', '#cb8c5c', '#a86d42', '#8a5332', '#6b3c24', '#4b2a1a'];
  P5.IRIS = ['#4a2e1c', '#2a1b12', '#5b3a1a', '#33493a', '#2f4258'];
  P5.skinKit = function (i) { var s = P5.SKIN[i % 8]; return { skin: s, shade: A.mix(s, '#6a2d12', 0.2), deep: A.mix(s, '#4a1e0c', 0.34), blush: A.mix(s, '#e0564e', i > 5 ? 0.12 : 0.22), lip: A.mix(s, '#b83a3a', i > 5 ? 0.42 : 0.55), lipDeep: A.mix(s, '#7a1f24', 0.62) }; };
  P5.facePath = function (cx, cy, w, jaw) {
    var j = 26 * jaw;
    return 'M' + f(cx - w) + ' ' + f(cy - 6) + 'C' + f(cx - w) + ' ' + f(cy - 42) + ' ' + f(cx - 26) + ' ' + f(cy - 56) + ' ' + f(cx) + ' ' + f(cy - 56) + 'C' + f(cx + 26) + ' ' + f(cy - 56) + ' ' + f(cx + w) + ' ' + f(cy - 42) + ' ' + f(cx + w) + ' ' + f(cy - 6) + 'C' + f(cx + w) + ' ' + f(cy + 26) + ' ' + f(cx + j) + ' ' + f(cy + 56) + ' ' + f(cx) + ' ' + f(cy + 56) + 'C' + f(cx - j) + ' ' + f(cy + 56) + ' ' + f(cx - w) + ' ' + f(cy + 26) + ' ' + f(cx - w) + ' ' + f(cy - 6) + 'Z';
  };
  P5.eye = function (x, y, side, o) {
    var s = '', lash = o.lash, ink = o.lid;
    if (o.expr === 'joy') return A.stroke('M' + f(x - 8) + ' ' + f(y + 2) + 'Q' + f(x) + ' ' + f(y - 8) + ' ' + f(x + 8) + ' ' + f(y + 2), 3, ink);
    var d = 'M' + f(x - 9) + ' ' + f(y + 0.5) + 'C' + f(x - 4) + ' ' + f(y - 6.5) + ' ' + f(x + 4) + ' ' + f(y - 6.5) + ' ' + f(x + 9) + ' ' + f(y + 0.5) + 'C' + f(x + 4) + ' ' + f(y + 5.2) + ' ' + f(x - 4) + ' ' + f(y + 5.2) + ' ' + f(x - 9) + ' ' + f(y + 0.5) + 'Z';
    s += A.clip(o.uid + 'e' + (side > 0 ? 'r' : 'l'), d, A.rect(x - 10, y - 8, 20, 16, 0, '#fbf6f1') + A.circle(x + side * 0.6, y - 0.4, 5, o.iris) + A.circle(x + side * 0.6, y - 0.4, 2.4, '#150d09') + A.circle(x + side * 0.6 + 1.7, y - 2.2, 1.3, '#ffffff'));
    s += A.stroke('M' + f(x - 9.4) + ' ' + f(y + 0.8) + 'C' + f(x - 4) + ' ' + f(y - 7.2) + ' ' + f(x + 4) + ' ' + f(y - 7.2) + ' ' + f(x + 9.4) + ' ' + f(y + 0.8), 2.4, ink);
    if (lash) s += A.stroke('M' + f(x + side * 8.6) + ' ' + f(y - 1) + 'L' + f(x + side * 12) + ' ' + f(y - 3.4), 2, ink);
    return s;
  };
  P5.brow = function (x, y, side, o) {
    var t = o.thick, up = o.expr === 'joy' ? 3 : 0;
    return A.path('M' + f(x - side * 11) + ' ' + f(y + 1.5 - up) + 'C' + f(x - side * 5) + ' ' + f(y - 4 - up) + ' ' + f(x + side * 3) + ' ' + f(y - 5.4 - up) + ' ' + f(x + side * 11) + ' ' + f(y - 1.5 - up) + 'C' + f(x + side * 4) + ' ' + f(y - 2 - up) + ' ' + f(x - side * 4) + ' ' + f(y - 1 - up) + ' ' + f(x - side * 11) + ' ' + f(y + 1.5 - up) + 'Z', o.brow, 'stroke="' + o.brow + '" stroke-width="' + f(t) + '" stroke-linejoin="round"');
  };
  P5.mouth = function (cx, y, o) {
    var k = o.k, e = o.expr;
    if (e === 'grin' || e === 'joy') {
      var d = 'M' + f(cx - 13) + ' ' + f(y - 2) + 'Q' + f(cx) + ' ' + f(y + 3) + ' ' + f(cx + 13) + ' ' + f(y - 2) + 'Q' + f(cx + 10) + ' ' + f(y + 14) + ' ' + f(cx) + ' ' + f(y + 14) + 'Q' + f(cx - 10) + ' ' + f(y + 14) + ' ' + f(cx - 13) + ' ' + f(y - 2) + 'Z';
      return A.clip(o.uid + 'm', d, A.rect(cx - 14, y - 4, 28, 20, 0, k.lipDeep) + A.rect(cx - 14, y - 4, 28, 8.5, 0, '#fffaf5') + A.ell(cx, y + 14, 8, 5, '#d8665f')) + A.stroke('M' + f(cx - 13) + ' ' + f(y - 2) + 'Q' + f(cx) + ' ' + f(y + 3) + ' ' + f(cx + 13) + ' ' + f(y - 2), 2, k.lipDeep);
    }
    if (e === 'calm') return A.path('M' + f(cx - 11) + ' ' + f(y) + 'Q' + f(cx - 5) + ' ' + f(y - 3.6) + ' ' + f(cx) + ' ' + f(y - 1.6) + 'Q' + f(cx + 5) + ' ' + f(y - 3.6) + ' ' + f(cx + 11) + ' ' + f(y) + 'Q' + f(cx) + ' ' + f(y + 7.5) + ' ' + f(cx - 11) + ' ' + f(y) + 'Z', k.lip) + A.stroke('M' + f(cx - 11) + ' ' + f(y) + 'Q' + f(cx) + ' ' + f(y + 1.8) + ' ' + f(cx + 11) + ' ' + f(y), 1.6, k.lipDeep);
    return A.stroke('M' + f(cx - 11) + ' ' + f(y - 1) + 'Q' + f(cx) + ' ' + f(y + 8) + ' ' + f(cx + 11) + ' ' + f(y - 1), 3, k.lipDeep);
  };
  /* returns {base, feat}: base = ears, face, blush; feat = brows, eyes, nose, mouth */
  P5.face = function (o) {
    var cx = o.cx, cy = o.cy, k = o.k, w = o.w || 42, jaw = o.jaw || 1, b = '', s = '', ey = cy + 2, fem = o.fem;
    b += A.ell(cx - w - 0.5, cy + 3, 7, 11.5, k.skin) + A.ell(cx + w + 0.5, cy + 3, 7, 11.5, k.skin) + A.ell(cx - w - 1.5, cy + 4, 3, 6.5, k.shade) + A.ell(cx + w + 1.5, cy + 4, 3, 6.5, k.shade);
    b += A.path(P5.facePath(cx, cy, w, jaw), k.skin);
    b += A.ell(cx - 27, cy + 21, 9.5, 6, k.blush) + A.ell(cx + 27, cy + 21, 9.5, 6, k.blush);
    var eo = { expr: o.expr, iris: o.iris, lid: o.lid, lash: fem, uid: o.uid, thick: fem ? 3 : 4.4, brow: o.brow };
    s += P5.brow(cx - 17, cy - 16, 1, eo) + P5.brow(cx + 17, cy - 16, -1, eo);
    s += P5.eye(cx - 17, ey, -1, eo) + P5.eye(cx + 17, ey, 1, eo);
    s += A.stroke('M' + f(cx + 0.5) + ' ' + f(cy + 7) + 'C' + f(cx - 4.5) + ' ' + f(cy + 17) + ' ' + f(cx - 6) + ' ' + f(cy + 22) + ' ' + f(cx - 1.5) + ' ' + f(cy + 23.5) + 'Q' + f(cx + 2) + ' ' + f(cy + 24.5) + ' ' + f(cx + 5.5) + ' ' + f(cy + 22), 2.4, k.deep);
    s += P5.mouth(cx, cy + 37, { k: k, expr: o.expr, uid: o.uid });
    return { base: b, feat: s };
  };
})(typeof window !== 'undefined' ? window : globalThis);
