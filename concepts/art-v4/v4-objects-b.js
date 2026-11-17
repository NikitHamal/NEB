/* v4 hero objects B (same 100 box). */
(function (g) {
  'use strict';
  var A = g.NebArtV4, O = A.objects, R = A.rect, C = A.circle, Pa = A.path, L = A.line, S = A.stroke;
  function K(P) { return { b: P.t(0.55), d: P.t(0.8), l: P.t(0.3), p: P.t(0.14), w: P.card, pop: P.pop, ps: P.popSoft, pd: P.popDeep, ink: P.ink }; }
  var rr = function (a, cx, cy, body) { return A.rot(a, cx, cy, body); };

  O.calendar = function (P) { var k = K(P), i, j, s = '';
    s += R(-40, -36, 80, 78, 14, k.w) + Pa('M-40 -22Q-40 -36 -26 -36H26Q40 -36 40 -22V-8H-40Z', k.pop) + R(-24, -46, 8, 20, 4, k.d) + R(16, -46, 8, 20, 4, k.d);
    for (j = 0; j < 3; j++) for (i = 0; i < 4; i++) s += R(-30 + i * 17, 2 + j * 15, 11, 9, 3, i === 2 && j === 1 ? k.pop : k.l);
    return s; };
  O.clock = function (P) { var k = K(P), i, s = '';
    s += C(0, 4, 40, k.d) + C(0, 4, 33, k.w) + R(-34, -44, 20, 10, 5, k.pd, 'transform="rotate(-30 -24 -39)"') + R(14, -44, 20, 10, 5, k.pd, 'transform="rotate(30 24 -39)"');
    for (i = 0; i < 12; i++) s += rr(i * 30, 0, 4, L(0, -29, 0, i % 3 ? -26 : -23, 2.5, k.l));
    return s + S('M0 4V-18M0 4L16 12', 5, k.d) + C(0, 4, 4.5, k.pop); };
  O.shield = function (P) { var k = K(P);
    return Pa('M0 -46L38 -32V0Q38 30 0 48Q-38 30 -38 0V-32Z', k.b) + Pa('M0 -46L38 -32V0Q38 30 0 48Z', k.d, 'opacity=".35"') + Pa('M0 -34L28 -24V0Q28 22 0 36Q-28 22 -28 0V-24Z', k.p) + S('M-12 0L-3 9L14 -9', 7, k.pop); };
  O.pulse = function (P) { var k = K(P);
    return Pa('M0 40C-60 0 -36 -40 -14 -40C-6 -40 0 -34 0 -28C0 -34 6 -40 14 -40C36 -40 60 0 0 40Z', k.pop) + S('M-38 4H-16L-8 -14L4 24L12 4H38', 5, k.w); };
  O.calculator = function (P) { var k = K(P), i, j, s = '';
    s += R(-32, -46, 64, 92, 14, k.d) + R(-24, -38, 48, 24, 7, k.p) + R(2, -32, 16, 5, 2.5, k.l);
    for (j = 0; j < 4; j++) for (i = 0; i < 3; i++) s += R(-24 + i * 17, -6 + j * 14, 14, 10, 5, i === 2 && j > 1 ? k.pop : k.w, 'opacity="' + (i === 2 && j > 1 ? 1 : 0.9) + '"');
    return s; };
  O.gear = function (P) { var k = K(P), i, s = '';
    for (i = 0; i < 8; i++) s += rr(i * 45, 0, 0, R(-8, -46, 16, 24, 5, k.b));
    return s + C(0, 0, 34, k.b) + C(0, 0, 14, k.p) + C(0, 0, 34, 'none', 'stroke="' + k.d + '" stroke-width="3" opacity=".25"') + A.shape('flower', 0, 0, 9, 0, k.pop); };
  O.compass = function (P) { var k = K(P);
    return S('M0 -34L-26 40', 8, k.b) + S('M0 -34L26 40', 8, k.d) + S('M-20 14H20', 4, k.pop) + C(0, -36, 10, k.pd) + R(-4, -52, 8, 14, 4, k.d) + Pa('M-30 44L-24 34L-20 46Z', k.ink) + C(26, 41, 5, k.pop); };
  O.plane = function (P) { var k = K(P);
    return Pa('M-48 -6L48 -40L18 44L2 12Z', k.w) + Pa('M-48 -6L48 -40L2 12Z', k.p) + Pa('M2 12L48 -40L18 44Z', k.b) + Pa('M2 12L-6 36L10 22Z', k.d) + S('M-46 30Q-30 10 -10 22', 3.5, k.pop, 'stroke-dasharray="1 8"'); };
  O.cap = function (P) { var k = K(P);
    return Pa('M-26 -2V22Q0 40 26 22V-2Z', k.d) + Pa('M0 -36L48 -14L0 8L-48 -14Z', k.b) + Pa('M0 8L48 -14V-8L0 14Z', k.d) + S('M40 -12V20', 3.5, k.pop) + C(40, 24, 6, k.pop) + C(0, -14, 4, k.p); };
  O.chart = function (P) { var k = K(P);
    return R(-42, -2, 20, 40, 8, k.l) + R(-14, -20, 20, 58, 8, k.b) + R(14, -38, 20, 76, 8, k.d) + S('M-40 -22L-12 -36L10 -20L38 -46', 5, k.pop) + C(38, -46, 7, k.pop) + C(38, -46, 3, k.w); };
  O.palette = function (P) { var k = K(P);
    return Pa('M0 -42C-44 -42 -50 4 -34 28C-24 42 -8 36 -8 24C-8 14 4 14 14 20C44 36 54 -10 40 -26C30 -38 14 -42 0 -42Z', k.p) + Pa('M0 -42C-44 -42 -50 4 -34 28C-24 42 -8 36 -8 24C-8 14 4 14 14 20C44 36 54 -10 40 -26C30 -38 14 -42 0 -42Z', 'none', 'stroke="'+k.l+'" stroke-width="6"') + C(-26, -8, 7, k.pop) + C(-12, -26, 7, k.b) + C(10, -28, 7, k.d) + C(28, -14, 7, k.ps) + C(-22, 14, 6, k.l) + A.rot(40, 20, 8, R(10, 2, 46, 8, 4, k.pd)); };
  O.music = function (P) { var k = K(P);
    return S('M-12 28V-30L28 -40V18', 6, k.d) + C(-22, 30, 13, k.b) + C(18, 22, 13, k.pop) + Pa('M-12 -30L28 -40V-24L-12 -14Z', k.d); };
  O.envelope = function (P) { var k = K(P);
    return R(-44, -28, 88, 62, 12, k.b) + Pa('M-44 -16Q-44 -28 -32 -28H32Q44 -28 44 -16L0 10Z', k.d) + Pa('M-44 30L-14 4M44 30L14 4', 'none', 'stroke="' + k.w + '" stroke-width="4" stroke-linecap="round"') + C(34, -30, 12, k.pop) + C(34, -30, 4, k.w); };
  O.plug = function (P) { var k = K(P);
    return S('M-50 30Q-28 30 -20 14Q-14 4 -4 6', 7, k.l) + A.rot(-30, 8, 0, R(-6, -14, 28, 28, 8, k.d) + R(22, -10, 10, 5, 2, k.b) + R(22, 5, 10, 5, 2, k.b)) + A.rot(-30, 8, 0, R(-6, -14, 8, 28, 4, k.pd)) + A.rot(-30, 8, 0, '') + C(38, -26, 4, k.pop) + S('M30 -38L46 -50M40 -18L56 -22', 3.5, k.pop); };
  O.scales = function (P) { var k = K(P);
    return R(-3, -36, 6, 72, 3, k.d) + R(-22, 34, 44, 8, 4, k.d) + S('M-38 -26H38', 5, k.b) + S('M-38 -26L-48 4M-38 -26L-28 4M38 -26L28 4M38 -26L48 4', 2.5, k.l) + Pa('M-52 4H-24Q-26 20 -38 20Q-50 20 -52 4Z', k.pop) + Pa('M24 4H52Q50 20 38 20Q26 20 24 4Z', k.b) + C(0, -38, 6, k.pop); };
  O.sprout = function (P) { var k = K(P);
    return Pa('M-28 14H28L22 42Q21 46 16 46H-16Q-21 46 -22 42Z', k.pop) + R(-32, 6, 64, 12, 6, k.pd) + S('M0 8V-20', 5, k.d) + Pa('M0 -8Q-34 -10 -36 -40Q-4 -42 0 -8Z', k.b) + Pa('M0 -22Q30 -22 36 -48Q6 -52 0 -22Z', k.l); };
  O.medal = function (P) { var k = K(P);
    return Pa('M-22 -50L-4 -50L8 -10L-10 -6Z', k.b) + Pa('M22 -50L4 -50L-8 -10L10 -6Z', k.d) + C(0, 14, 28, k.pop) + C(0, 14, 21, k.ps) + A.star4(0, 14, 14, k.w); };
  O.target = function (P) { var k = K(P);
    return C(0, 0, 42, k.p) + C(0, 0, 42, 'none', 'stroke="' + k.b + '" stroke-width="7"') + C(0, 0, 25, k.b) + C(0, 0, 10, k.pop) + S('M4 -4L40 -40', 4, k.d) + Pa('M34 -46L46 -50L50 -38L40 -34Z', k.pd); };
  O.microscope = function (P) { var k = K(P);
    return R(-34, 36, 68, 10, 5, k.d) + S('M-22 30Q-44 6 -20 -16', 8, k.d) + A.rot(28, 0, -8, R(-10, -46, 20, 56, 8, k.b) + R(-7, 10, 14, 10, 3, k.d) + R(-12, -50, 24, 8, 4, k.pd)) + R(-2, 14, 34, 6, 3, k.l) + R(8, 26, 22, 6, 3, k.d) + C(-22, 30, 6, k.pop) + A.star4(-34, -36, 8, k.pop); };
  O.dna = function (P) { var k = K(P), s = '', i, y, x;
    s += S('M-22 -44C-22 -16 22 -16 22 12C22 30 -10 38 -22 44', 6, k.b) + S('M22 -44C22 -16 -22 -16 -22 12C-22 30 10 38 22 44', 6, k.d);
    for (i = 0; i < 5; i++) { y = -34 + i * 17; x = 14 * Math.sin((y + 20) / 28 * 3.1); s += L(-x - 8, y, x + 8, y, 3.5, i % 2 ? k.l : k.pop); }
    return s; };
})(typeof window !== 'undefined' ? window : globalThis);
