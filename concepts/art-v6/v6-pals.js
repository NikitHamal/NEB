/* v6 pals: expressive-shape characters (cookie, flower, clover, burst ...) with a face. Mascots for empty states and a profile picture family.
   A.pal(P, r, cx, cy, size, o) draws one pal in a 100 unit box scaled to size. o = { shape, eyes, mouth, acc, arms, tone, flip }. */
(function (g) {
  'use strict';
  var A = g.NebArtV6, E = A.engines, f = A.f, sin = Math.sin, cos = Math.cos, PI = Math.PI;
  var INK = '#17202e', SHAPES = ['cookie', 'flower', 'clover', 'burst', 'sunny', 'puffy', 'pebble', 'squircle', 'lotus', 'gem'];
  var EYES = ['dot', 'happy', 'wide', 'sleepy', 'wink'], MOUTHS = ['smile', 'open', 'o', 'smirk', 'grin'], ACCS = ['sprout', 'antenna', 'bow', 'glasses', 'phones', 'none', 'cap', 'tuft'];
  A.palSpec = function (r) { return { shape: r.pick(SHAPES), eyes: r.pick(EYES), mouth: r.pick(MOUTHS), acc: r.pick(ACCS), tone: r.int(0, 3), arms: r.pick(['down', 'up', 'wave', 'hold']) }; };
  function eye(kind, x, y) {
    if (kind === 'happy') return A.stroke('M' + f(x - 5.5) + ' ' + f(y + 2) + 'Q' + f(x) + ' ' + f(y - 6) + ' ' + f(x + 5.5) + ' ' + f(y + 2), 3, INK);
    if (kind === 'sleepy') return A.stroke('M' + f(x - 5.5) + ' ' + f(y) + 'Q' + f(x) + ' ' + f(y + 5) + ' ' + f(x + 5.5) + ' ' + f(y), 3, INK);
    if (kind === 'wide') return A.circle(x, y, 7.5, '#ffffff') + A.circle(x + 0.8, y + 0.6, 4.6, INK) + A.circle(x + 2.4, y - 1.4, 1.7, '#ffffff');
    return A.circle(x, y, kind === 'wink' ? 4.4 : 4.6, INK) + A.circle(x + 1.4, y - 1.5, 1.4, '#ffffff');
  }
  function mouth(kind, y) {
    if (kind === 'open') return A.path('M-7 ' + f(y) + 'Q0 ' + f(y + 12) + ' 7 ' + f(y) + 'Z', INK) + A.path('M-3.5 ' + f(y + 5.5) + 'Q0 ' + f(y + 3.4) + ' 3.5 ' + f(y + 5.5) + 'Q0 ' + f(y + 9) + ' -3.5 ' + f(y + 5.5) + 'Z', '#f0808a');
    if (kind === 'o') return A.circle(0, y + 3, 3.6, INK);
    if (kind === 'smirk') return A.stroke('M-5 ' + f(y + 2) + 'Q2 ' + f(y + 6) + ' 7 ' + f(y - 1), 2.8, INK);
    if (kind === 'grin') return A.path('M-8 ' + f(y - 1) + 'H8Q8 ' + f(y + 9) + ' 0 ' + f(y + 9) + 'Q-8 ' + f(y + 9) + ' -8 ' + f(y - 1) + 'Z', INK) + A.rect(-6, y - 1, 12, 3.6, 1.5, '#ffffff');
    return A.stroke('M-6 ' + f(y) + 'Q0 ' + f(y + 7) + ' 6 ' + f(y), 2.8, INK);
  }
  A.pal = function (P, r, cx, cy, size, o) {
    o = o || {}; var sh = o.shape || 'cookie', tones = [P.t(0.5), P.q.t(0.5), P.t(0.34), P.q.t(0.38)], body = tones[o.tone == null ? 0 : o.tone], dk = P.t(0.7), lt = P.dark ? P.t(0.62) : P.t(0.3), s = '', ey = -4, k;
    var arms = o.arms || 'down', ac = o.acc || 'none';
    /* feet */
    s += A.rect(-19, 33, 15, 11, 5.5, dk) + A.rect(4, 33, 15, 11, 5.5, dk);
    /* arms behind body */
    var armC = P.dark ? body : dk;
    if (arms === 'up') s += A.line(-36, 2, -50, -22, 8, armC) + A.line(36, 2, 50, -22, 8, armC);
    else if (arms === 'wave') s += A.line(-36, 8, -48, 16, 8, armC) + A.line(36, 2, 50, -20, 8, armC) + A.circle(50, -22, 6, armC);
    else if (arms === 'hold') s += A.line(-36, 8, -22, 26, 8, armC) + A.line(36, 8, 22, 26, 8, armC);
    else s += A.line(-36, 8, -46, 26, 8, armC) + A.line(36, 8, 46, 26, 8, armC);
    /* hair-like accessories behind */
    if (ac === 'sprout') s += A.stroke('M0 -38Q0 -50 2 -54', 3.5, P.q.t(0.7)) + A.path('M2 -54Q14 -64 22 -52Q10 -46 2 -54Z', P.q.t(0.42)) + A.path('M1 -50Q-10 -62 -20 -52Q-8 -44 1 -50Z', P.q.t(0.56));
    if (ac === 'antenna') s += A.line(-10, -38, -16, -56, 3, dk) + A.circle(-16, -57, 4.6, P.q.t(0.45)) + A.line(10, -38, 16, -56, 3, dk) + A.circle(16, -57, 4.6, P.q.t(0.45));
    if (ac === 'tuft') s += A.path('M-6 -38Q-8 -52 0 -56Q2 -48 6 -52Q8 -44 6 -38Z', dk);
    s += A.shape(sh, 0, 0, 41, o.rot || 0, body);
    s += A.stroke('M-24 -16Q-18 -28 -6 -31', 4.5, lt, 'opacity=".55"');
    for (k = -1; k <= 1; k += 2) s += A.circle(k * 22, 9, 6, P.q.t(P.dark ? 0.5 : 0.3), 'opacity=".7"');
    s += eye(o.eyes || 'dot', -13, ey) + eye(o.eyes === 'wink' ? 'happy' : o.eyes || 'dot', 13, ey) + mouth(o.mouth || 'smile', 10);
    if (ac === 'bow') s += A.path('M0 -36L-15 -46Q-19 -34 -15 -29Z', P.q.t(0.48)) + A.path('M0 -36L15 -46Q19 -34 15 -29Z', P.q.t(0.48)) + A.circle(0, -36, 5, P.q.t(0.7));
    if (ac === 'glasses') s += A.circle(-13, ey, 11, 'none', 'stroke="' + INK + '" stroke-width="2.6"') + A.circle(13, ey, 11, 'none', 'stroke="' + INK + '" stroke-width="2.6"') + A.line(-2, ey, 2, ey, 2.6, INK);
    if (ac === 'phones') s += A.stroke('M-38 -2Q-38 -46 0 -46Q38 -46 38 -2', 5, dk) + A.rect(-44, -12, 11, 22, 5.5, P.q.t(0.5)) + A.rect(33, -12, 11, 22, 5.5, P.q.t(0.5));
    if (ac === 'cap') s += A.path('M-30 -26Q-28 -50 0 -50Q28 -50 30 -26Q0 -34 -30 -26Z', P.q.t(0.5)) + A.rect(-4, -34, 34, 6, 3, P.q.t(0.68));
    return '<g transform="translate(' + f(cx) + ' ' + f(cy) + ')' + (o.flip ? ' scale(-1 1)' : '') + ' scale(' + (size / 100 * (o.flip ? 1 : 1)).toFixed(4) + ')">' + s + '</g>';
  };
  /* pal profile pictures: frameless square, a big flat shape behind, sparkles */
  E.pal = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), o = c.o.spec || A.palSpec(r), deep = r.chance(0.35), bg = deep ? (P.dark ? P.t(0.16) : P.t(0.82)) : P.t(P.dark ? 0.14 : 0.12), s = A.rect(0, 0, w, h, 0, bg), k;
    s += A.shape(r.pick(['pebble', 'flower', 'cookie', 'clover', 'squircle']), w * 0.5 + r.range(-6, 6), h * 0.56, m * 0.5, r() * 3, deep ? (P.dark ? P.t(0.26) : P.t(0.7)) : P.t(0.22));
    return s + A.pal(P, r, w / 2, h * 0.56, m * 0.7, { shape: o.shape, eyes: o.eyes, mouth: o.mouth, acc: o.acc, tone: o.tone, arms: o.arms === 'up' ? 'up' : 'down', rot: r() * 3 });
  };
})(typeof window !== 'undefined' ? window : globalThis);
