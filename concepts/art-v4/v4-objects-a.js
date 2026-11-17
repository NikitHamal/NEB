/* v4 hero objects A. Each is drawn in a 100 x 100 box centred on 0,0 (-50..50) and scaled by A.obj(). Flat, rounded, tonal. */
(function (g) {
  'use strict';
  var A = g.NebArtV4, O = A.objects, R = A.rect, C = A.circle, Pa = A.path, L = A.line, S = A.stroke;
  A.obj = function (name, P, cx, cy, size, rot) {
    var fn = O[name]; if (!fn) throw new Error('unknown object ' + name);
    return '<g transform="translate(' + A.f(cx) + ' ' + A.f(cy) + ')' + (rot ? ' rotate(' + rot + ')' : '') + ' scale(' + (size / 100).toFixed(4) + ')">' + fn(P) + '</g>';
  };
  function K(P) { return { b: P.t(0.55), d: P.t(0.8), l: P.t(0.3), p: P.t(0.14), w: P.card, pop: P.pop, ps: P.popSoft, pd: P.popDeep, ink: P.ink }; }
  function ln(x1, y1, x2, y2, w, c) { return L(x1, y1, x2, y2, w, c); }

  O.book = function (P) { var k = K(P);
    return Pa('M-50 -18Q-25 -30 0 -14Q25 -30 50 -18V32Q25 20 0 36Q-25 20 -50 32Z', k.d) + Pa('M-44 -20Q-22 -29 0 -12V30Q-22 16 -44 26Z', k.w) + Pa('M44 -20Q22 -29 0 -12V30Q22 16 44 26Z', k.p) +
      [-4, 6, 16].map(function (y, i) { return ln(-36, y - 6 + i, -10, y + 4 + i * 0.5, 3, k.l) + ln(10, y + 4 + i * 0.5, 36, y - 6 + i, 3, k.l); }).join('') + Pa('M-8 -13H8V-40L0 -32L-8 -40Z', k.pop); };
  O.books = function (P) { var k = K(P);
    return R(-44, 18, 88, 22, 8, k.d) + R(-36, -4, 76, 22, 8, k.b) + R(-40, -26, 70, 22, 8, k.l) + R(-24, 22, 8, 14, 4, k.pop) + R(-14, 0, 8, 14, 4, k.w) + R(-8, -22, 6, 14, 3, k.d) +
      Pa('M20 -28L40 -46L46 -40L34 -26Z', k.pop) + R(18, -50, 16, 8, 4, k.ps, 'transform="rotate(-30 26 -46)"'); };
  O.notebook = function (P) { var k = K(P), i, s = '';
    s += R(-34, -46, 72, 92, 12, k.b) + R(-26, -46, 64, 92, 10, k.w);
    for (i = 0; i < 5; i++) s += ln(-12, -24 + i * 14, 26, -24 + i * 14, 3.5, k.p);
    for (i = 0; i < 6; i++) s += R(-38, -40 + i * 15, 16, 7, 3.5, k.d);
    return s + Pa('M20 -46H34V-18L27 -24L20 -18Z', k.pop) + R(-12, -38, 24, 6, 3, k.l); };
  O.pencil = function (P) { var k = K(P);
    return A.rot(-45, 0, 0, R(-52, -9, 88, 18, 5, k.pop) + R(-52, -9, 14, 18, 5, k.pd) + R(-34, -9, 5, 18, 0, k.w) + Pa('M36 -9L56 0L36 9Z', k.p) + Pa('M48 -4.5L56 0L48 4.5Z', k.ink) + R(-12, -9, 3, 18, 0, k.ps)); };
  O.flask = function (P) { var k = K(P);
    return Pa('M-10 -42H10V-14L36 30Q42 44 26 44H-26Q-42 44 -36 30L-10 -14Z', k.p) + A.clip('qfl', 'M-10 -42H10V-14L36 30Q42 44 26 44H-26Q-42 44 -36 30L-10 -14Z', R(-50, 8, 100, 40, 0, k.b) + R(-50, 8, 100, 4, 0, k.l)) +
      R(-14, -46, 28, 8, 4, k.d) + C(-8, 24, 4, k.w) + C(8, 16, 3, k.w) + C(2, 30, 2.5, k.p) + C(14, -2, 4, k.pop) + C(18, -16, 2.5, k.pop); };
  O.atom = function (P) { var k = K(P), e = function (a) { return A.rot(a, 0, 0, '<ellipse cx="0" cy="0" rx="46" ry="17" fill="none" stroke="' + k.l + '" stroke-width="4"/>' + C(46, 0, 5, k.b)); };
    return e(0) + e(60) + e(120) + A.shape('flower', 0, 0, 15, 0, k.pop) + C(0, 0, 5, k.w); };
  O.globe = function (P) { var k = K(P);
    return C(0, -2, 40, k.b) + A.clip('qgl', A.shapeD('circle', 0, -2, 40, 0), Pa('M-30 -22Q-14 -34 -2 -20Q6 -8 -8 0Q-22 4 -32 -8Z', k.pd) + Pa('M10 6Q24 -4 34 8Q36 24 22 34Q10 30 12 18Z', k.pd) + Pa('M16 -32Q28 -30 32 -20Q22 -14 14 -22Z', k.pd)) +
      '<ellipse cx="0" cy="-2" rx="16" ry="40" fill="none" stroke="' + k.w + '" stroke-width="2.5" opacity=".7"/>' + S('M-40 -2H40', 2.5, k.w, 'opacity=".7"') + S('M-26 -30Q0 -22 26 -30M-26 26Q0 18 26 26', 2.5, k.w, 'opacity=".7"') + S('M-26 42Q0 52 26 42', 6, k.d) + R(-5, 38, 10, 6, 2, k.d); };
  O.laptop = function (P) { var k = K(P);
    return R(-38, -34, 76, 52, 8, k.d) + R(-33, -29, 66, 42, 5, k.p) + R(-26, -22, 28, 5, 2.5, k.b) + R(-26, -13, 40, 4, 2, k.l) + R(-26, -5, 22, 4, 2, k.l) + A.shape('cookie', 22, -4, 9, 0, k.pop) + Pa('M-46 22H46Q46 34 38 34H-38Q-46 34 -46 22Z', k.b) + R(-9, 22, 18, 4, 2, k.d); };
  O.bulb = function (P) { var k = K(P), i, s = '';
    for (i = 0; i < 5; i++) s += A.rot(-72 + i * 36, 0, -10, ln(0, -50, 0, -43, 4, k.pop));
    return s + C(0, -10, 28, k.ps) + Pa('M-12 14Q-12 22 -10 26H10Q12 22 12 14Z', k.ps) + R(-10, 26, 20, 6, 3, k.d) + R(-8, 33, 16, 6, 3, k.b) + S('M-8 12V-4Q-8 -12 0 -10Q8 -12 8 -4V12', 3.5, k.pd) + C(-12, -20, 5, k.w, 'opacity=".7"'); };
  O.trophy = function (P) { var k = K(P);
    return S('M-26 -24H-38Q-38 -2 -20 0M26 -24H38Q38 -2 20 0', 5, k.pd) + Pa('M-28 -40H28V-14Q28 12 0 14Q-28 12 -28 -14Z', k.pop) + R(-6, 12, 12, 16, 2, k.pd) + R(-20, 28, 40, 12, 6, k.d) + A.star4(0, -18, 12, k.w) + R(-22, -40, 6, 30, 3, k.ps); };
  O.rocket = function (P) { var k = K(P);
    return A.rot(45, 0, 0, Pa('M-10 36L0 56L10 36Z', k.pop) + Pa('M-16 -4Q-34 6 -28 24L-14 18Z', k.d) + Pa('M16 -4Q34 6 28 24L14 18Z', k.d) + Pa('M0 -52Q22 -30 16 26H-16Q-22 -30 0 -52Z', k.w) + Pa('M0 -52Q10 -42 14 -28H-14Q-10 -42 0 -52Z', k.b) + C(0, -10, 9, k.d) + C(0, -10, 5, k.p) + R(-16, 22, 32, 6, 3, k.l)); };
  O.magnifier = function (P) { var k = K(P);
    return A.rot(-45, 0, 0, R(-6, 12, 12, 44, 6, k.d)) + C(-6, -8, 30, k.p) + C(-6, -8, 30, 'none', 'stroke="' + k.b + '" stroke-width="9"') + Pa('M-22 -14Q-16 -26 -4 -26', 'none', 'stroke="' + k.w + '" stroke-width="4" stroke-linecap="round"') + A.star4(-2, -8, 10, k.pop); };
  O.folder = function (P) { var k = K(P);
    return Pa('M-46 -30Q-46 -38 -38 -38H-12L-4 -28H38Q46 -28 46 -20V28Q46 36 38 36H-38Q-46 36 -46 28Z', k.d) + R(-38, -22, 76, 40, 6, k.w) + R(-38, -14, 76, 40, 6, k.p) + Pa('M-46 -6Q-46 -12 -38 -12H38Q46 -12 46 -4L40 30Q39 36 32 36H-38Q-46 36 -46 28Z', k.b) + C(0, 12, 6, k.w); };
  O.cloud = function (P) { var k = K(P);
    return C(-18, 4, 20, k.b) + C(8, -8, 26, k.b) + C(28, 12, 16, k.b) + R(-36, 4, 80, 24, 12, k.b) + Pa('M0 24V2M-10 10L0 0L10 10', 'none', 'stroke="' + k.w + '" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"') + C(-34, -30, 4, k.l) + C(40, -26, 3, k.pop); };
  O.chat = function (P) { var k = K(P);
    return Pa('M-44 -34H20Q30 -34 30 -24V8Q30 18 20 18H-14L-30 34V18H-34Q-44 18 -44 8Z', k.b) + Pa('M-6 4H34V-8Q34 -14 44 -14H46Q56 -14 56 -4V26Q56 34 48 34H46V46L32 34H4Q-6 34 -6 24Z', k.pop, 'transform="translate(-6 4) scale(.9)"') + C(-28, -12, 4.5, k.w) + C(-12, -12, 4.5, k.w) + C(4, -12, 4.5, k.w); };
  O.bell = function (P) { var k = K(P);
    return Pa('M0 -42Q-26 -42 -26 -12V10L-36 24H36L26 10V-12Q26 -42 0 -42Z', k.pop) + Pa('M0 -42Q-26 -42 -26 -12V10L-36 24H-8Q-18 0 -16 -22Q-14 -40 0 -42Z', k.pd, 'opacity=".25"') + C(0, 34, 8, k.d) + R(-3, -50, 6, 10, 3, k.d) + S('M-14 -20Q-14 -30 -4 -32', 4, k.w, 'opacity=".7"'); };
})(typeof window !== 'undefined' ? window : globalThis);
