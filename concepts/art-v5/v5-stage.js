/* v5 stage: ONE hero object on ONE plate (+ at most one small status mark), optional calm scene behind. Badges: clean single-hue seals. */
(function (g) {
  'use strict';
  var A = g.NebArtV5, E = A.engines, f = A.f;
  function place(obj, C, x, y, S) { return A.g('translate(' + f(x - S / 2) + ' ' + f(y - S / 2) + ') scale(' + f(S / 100) + ')', A.objects[obj](C)); }
  function mark(kind, x, y, r, P) {
    var s = A.circle(x, y, r, P.d), k = r * 0.42, w = r * 0.2;
    if (kind === 'check') s += A.stroke('M' + f(x - k) + ' ' + f(y) + 'L' + f(x - k * 0.25) + ' ' + f(y + k * 0.7) + 'L' + f(x + k) + ' ' + f(y - k * 0.7), w, P.paper);
    if (kind === 'cross') s += A.line(x - k * 0.8, y - k * 0.8, x + k * 0.8, y + k * 0.8, w, P.paper) + A.line(x + k * 0.8, y - k * 0.8, x - k * 0.8, y + k * 0.8, w, P.paper);
    if (kind === 'plus') s += A.line(x - k, y, x + k, y, w, P.paper) + A.line(x, y - k, x, y + k, w, P.paper);
    if (kind === 'dash') s += A.line(x - k, y, x + k, y, w, P.paper);
    return s;
  }
  E.stage = function (c) {
    var P = c.P, o = c.o, w = c.w, h = c.h, s = '', S = Math.min(w, h) * (o.scale || 0.56), x = o.side === 'right' ? w * 0.72 : o.side === 'left' ? w * 0.28 : w / 2, y = h * (o.dy || 0.5), plate = o.plate || 'disc';
    if (o.scene) s += E[o.scene](c);
    var pf = o.scene ? (c.mode === 'dark' ? P.s1 : P.paper) : (o.platec ? P[o.platec] : P.s2), pr = S * 0.82;
    if (plate === 'disc') s += A.circle(x, y, pr, pf);
    if (plate === 'arch') s += A.arch(x - pr * 0.9, y - pr * 1.05, pr * 1.8, pr * 2.4, pf);
    if (plate === 'tile') s += A.rot(-7, x, y, A.rect(x - pr, y - pr, pr * 2, pr * 2, pr * 0.55, pf));
    if (plate === 'cookie') s += A.path(A.cookie(x, y, pr * 1.12, 10, 0.07, 0.3), pf);
    if (plate === 'bloom') s += A.path(A.cookie(x, y, pr * 1.15, 6, 0.12, 0.2), pf);
    if (plate === 'ground') s += A.ell(x, y + S * 0.5, S * 0.7, S * 0.12, pf);
    s += place(o.obj, P, x, y, S);
    if (o.mark) s += mark(o.mark, x + S * 0.42, y + S * 0.4, S * 0.16, P);
    return s;
  };
  function hexPts(cx, cy, R) { var p = [], i; for (i = 0; i < 6; i++) p.push([cx + R * Math.cos(Math.PI / 6 + i * Math.PI / 3 - Math.PI / 6 + Math.PI / 6), cy + R * Math.sin(Math.PI / 6 + i * Math.PI / 3 - Math.PI / 6 + Math.PI / 6)]); return p; }
  E.badge = function (c) {
    var P = c.P, o = c.o, s = '', emb = { m: P.paper, d: P.pap2, hi: P.s2, ink: P.d, paper: P.paper, pap2: P.pap2, s1: P.m, s2: P.hi }, sh = o.shape, sc = 'translate(128 128) scale(.84) translate(-128 -128)';
    if (sh === 'seal') s = A.path(A.cookie(128, 128, 114, 12, 0.055, 0), P.d) + A.circle(128, 128, 90, P.m) + A.circle(128, 128, 78, 'none', 'stroke="' + P.hi + '" stroke-width="3"');
    if (sh === 'shield') { var d = 'M128 14 L220 50 V120 C220 178 180 220 128 242 C76 220 36 178 36 120 V50Z'; s = A.path(d, P.d) + A.g(sc, A.path(d, P.m)) + A.g('translate(128 128) scale(.74) translate(-128 -128)', A.path(d, 'none', 'stroke="' + P.hi + '" stroke-width="4"')); }
    if (sh === 'hex') { var hp = hexPts(128, 128, 100); s = A.poly(hp, P.d, 'stroke="' + P.d + '" stroke-width="22" stroke-linejoin="round"') + A.g(sc, A.poly(hp, P.m, 'stroke="' + P.m + '" stroke-width="22" stroke-linejoin="round"')); }
    if (sh === 'round') s = A.poly([[74, 190], [118, 206], [98, 252], [86, 238], [70, 248]], P.ink) + A.poly([[182, 190], [138, 206], [158, 252], [170, 238], [186, 248]], P.ink) + A.circle(128, 124, 108, P.d) + A.circle(128, 124, 94, P.m) + A.circle(128, 124, 82, 'none', 'stroke="' + P.hi + '" stroke-width="3"');
    if (sh === 'bloom') s = A.path(A.cookie(128, 128, 114, 10, 0.075, 0.1), P.d) + A.path(A.cookie(128, 128, 92, 10, 0.075, 0.1), P.m);
    var oy = sh === 'round' ? 124 : 128;
    return s + A.g('translate(' + f(128 - 50 * o.k) + ' ' + f(oy - 50 * o.k) + ') scale(' + f(o.k) + ')', A.objects[o.obj](emb));
  };
})(typeof window !== 'undefined' ? window : globalThis);
