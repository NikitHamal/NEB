/* v4 stage engine: hero object(s) on a backdrop. Used for empty states, thumbnails, book plates, tiles, achievements and covers.
   o = { objs: [main, chip, chip], style: disc|arch|plate|ground|pattern|burst, side: left|center|right, bg: engine for style pattern } */
(function (g) {
  'use strict';
  var A = g.NebArtV4, E = A.engines, f = A.f, sin = Math.sin, cos = Math.cos, PI = Math.PI;
  var SH = ['cookie', 'flower', 'clover', 'burst', 'sunny', 'puffy', 'pebble', 'squircle', 'lotus', 'gem'];
  A.PATTERN_BG = ['tessera', 'hex', 'halftone', 'memphis', 'terrazzo', 'bloomField', 'scallop', 'weave', 'glyphField', 'flow', 'waveform', 'nest'];

  E.stage = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = c.o, m = Math.min(w, h), wide = w / h > 1.5, tall = h / w > 1.3, objs = o.objs || ['book'], style = o.style || 'disc', side = o.side || (wide ? 'right' : 'center'), s = '';
    var cx = side === 'right' ? w * 0.76 : side === 'left' ? w * 0.24 : w / 2, cy = tall ? h * 0.42 : h * 0.5, pl = m * (wide ? 0.92 : 0.84), big = pl * 0.62, k, a, x, y, sh = r.pick(SH);
    if (style === 'pattern') s += A.engines[o.bg || 'tessera']({ w: w, h: h, P: P, r: r, uid: c.uid, o: {}, mode: c.mode, kind: c.kind });
    else s += A.rect(0, 0, w, h, 0, P.t(style === 'ground' ? 0.1 : 0.05));
    if (style === 'disc' || style === 'burst') {
      s += A.shape(style === 'burst' ? 'burst' : sh, cx, cy, pl * 0.58, r() * 3, P.t(0.12)) + A.shape(style === 'burst' ? 'sunny' : sh, cx, cy, pl * 0.46, r() * 3, P.t(0.22));
    } else if (style === 'arch') {
      s += A.arch(cx - pl * 0.34, cy - pl * 0.5, pl * 0.68, pl, P.t(0.16)) + A.arch(cx - pl * 0.26, cy - pl * 0.42, pl * 0.52, pl * 0.92, P.t(0.06));
    } else if (style === 'plate') {
      s += A.rect(cx - pl * 0.42, cy - pl * 0.42, pl * 0.84, pl * 0.84, pl * 0.2, P.t(0.26), 'transform="rotate(8 ' + f(cx) + ' ' + f(cy) + ')"') + A.rect(cx - pl * 0.42, cy - pl * 0.42, pl * 0.84, pl * 0.84, pl * 0.2, P.card, 'transform="rotate(-5 ' + f(cx) + ' ' + f(cy) + ')"');
    } else if (style === 'ground') {
      s += A.shape('pebble', cx, cy + pl * 0.36, pl * 0.5, 0, P.t(0.24)) + A.shape('pebble', cx, cy + pl * 0.32, pl * 0.42, 0.4, P.t(0.16));
    } else s += A.shape('flower', cx, cy, pl * 0.5, r() * 3, P.card) + A.shape('cookie', cx, cy, pl * 0.4, r() * 3, P.t(0.12));
    /* accents */
    for (k = 0; k < 7; k++) { a = r() * 6.28; x = cx + cos(a) * pl * r.range(0.5, 0.75); y = cy + sin(a) * pl * r.range(0.4, 0.6); if (x < 0 || x > w || y < 0 || y > h) continue; var t = r.int(0, 3); s += t === 0 ? A.sparkle(x, y, m * r.range(0.03, 0.06), k % 2 ? P.pop : P.t(0.5)) : t === 1 ? A.circle(x, y, m * r.range(0.008, 0.02), P.t(0.4)) : t === 2 ? A.plus(x, y, m * 0.022, m * 0.01, P.t(0.45)) : A.shape(r.pick(SH), x, y, m * r.range(0.025, 0.045), r() * 3, P.popSoft); }
    /* main object, then chips */
    s += A.obj(objs[0], P, cx, cy, big, o.tilt == null ? r.int(-6, 6) : o.tilt);
    for (k = 1; k < objs.length; k++) {
      a = (k === 1 ? -0.7 : 2.55) + r.range(-0.2, 0.2); x = cx + cos(a) * pl * 0.46; y = cy + sin(a) * pl * 0.42; var cs = pl * 0.17;
      s += A.shape(['cookie', 'squircle', 'flower'][k % 3], x, y, cs, r() * 3, P.card) + A.obj(objs[k], P, x, y, cs * 1.25, 0);
    }
    return s;
  };
})(typeof window !== 'undefined' ? window : globalThis);
