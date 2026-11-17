/* v5 hero objects B. Same rules as A. */
(function (g) {
  'use strict';
  var A = g.NebArtV5, O = A.objects, R = A.rect, Ci = A.circle, Pa = A.path, S = A.stroke, L = A.line, Pl = A.poly;
  O.calendar = function (C) { var s = '', i, j; for (j = 0; j < 3; j++) for (i = 0; i < 4; i++) s += R(20 + i * 16, 44 + j * 14, 10, 8, 3, j === 1 && i === 2 ? C.m : C.s2); return R(10, 14, 80, 76, 10, C.paper) + Pa('M10 24 Q10 14 20 14 H80 Q90 14 90 24 V34 H10Z', C.m) + R(26, 6, 8, 16, 4, C.d) + R(66, 6, 8, 16, 4, C.d) + s; };
  O.shield = function (C) { return Pa('M50 6 L88 20 V46 C88 70 70 86 50 94 C30 86 12 70 12 46 V20Z', C.d) + Pa('M50 6 L88 20 V46 C88 70 70 86 50 94Z', C.ink) + Pa('M50 14 L80 25 V46 C80 64 66 78 50 86 C34 78 20 64 20 46 V25Z', C.m) + S('M35 50 L46 61 L66 38', 7, C.paper); };
  O.cloud = function (C) { return Pa('M26 74 C10 74 6 54 22 50 C20 30 44 22 54 36 C64 26 84 32 82 52 C96 54 96 74 80 74Z', C.paper) + Pa('M54 36 C64 26 84 32 82 52 C96 54 96 74 80 74 H54Z', C.pap2) + L(50, 82, 50, 46, 7, C.m) + S('M36 58 L50 44 L64 58', 7, C.m); };
  O.chart = function (C) { return R(12, 56, 18, 32, 6, C.hi) + R(41, 38, 18, 50, 6, C.m) + R(70, 14, 18, 74, 6, C.d) + L(6, 92, 94, 92, 4, C.ink); };
  O.plug = function (C) { return S('M50 64 C50 82 20 78 16 96', 6, C.d) + R(30, 36, 40, 32, 12, C.m) + R(30, 52, 40, 16, 8, C.d) + R(36, 12, 8, 26, 4, C.ink) + R(56, 12, 8, 26, 4, C.ink); };
  O.compass = function (C) { return Ci(50, 50, 42, C.m) + Ci(50, 50, 33, C.paper) + A.rot(40, 50, 50, Pl([[50, 18], [58, 50], [50, 50], [42, 50]], C.d) + Pl([[50, 82], [58, 50], [42, 50]], C.hi)) + Ci(50, 50, 4.5, C.ink); };
  O.calculator = function (C) { var s = '', i, j; for (j = 0; j < 3; j++) for (i = 0; i < 3; i++) s += R(24 + i * 17, 44 + j * 15, 12, 10, 4, i === 2 && j === 2 ? C.ink : C.paper); return R(16, 6, 68, 88, 12, C.m) + R(16, 6, 68, 88, 12, 'none', 'stroke="' + C.d + '" stroke-width="3"') + R(24, 14, 52, 22, 6, C.s1) + L(32, 25, 54, 25, 4, C.d) + s; };
  O.microscope = function (C) { return A.rot(-18, 46, 40, R(38, 6, 16, 50, 6, C.m) + R(34, 52, 24, 8, 3, C.d)) + S('M62 30 C88 36 86 76 58 80', 8, C.d) + R(22, 72, 62, 10, 5, C.ink) + R(30, 62, 28, 6, 3, C.hi); };
  O.sprout = function (C) { return Pa('M50 62 C50 42 44 34 30 30 C22 48 34 60 50 62Z', C.m) + Pa('M50 56 C50 36 58 22 76 20 C80 40 68 54 50 56Z', C.hi) + L(50, 62, 50, 74, 4, C.d) + Pa('M24 66 H76 L70 92 Q69 94 66 94 H34 Q31 94 30 92Z', C.d) + R(20, 62, 60, 8, 4, C.ink); };
  O.scales = function (C) { return L(50, 14, 50, 82, 6, C.d) + L(18, 28, 82, 28, 5, C.d) + L(18, 28, 8, 56, 2.6, C.ink) + L(18, 28, 28, 56, 2.6, C.ink) + L(82, 28, 72, 56, 2.6, C.ink) + L(82, 28, 92, 56, 2.6, C.ink) + Pa('M4 56 H32 Q30 68 18 68 Q6 68 4 56Z', C.m) + Pa('M68 56 H96 Q94 68 82 68 Q70 68 68 56Z', C.m) + R(32, 84, 36, 8, 4, C.ink) + Ci(50, 12, 6, C.m); };
  O.envelope = function (C) { return R(8, 20, 84, 60, 9, C.paper) + Pa('M8 29 Q8 20 17 20 H83 Q92 20 92 29 L56 54 Q50 58 44 54Z', C.pap2) + S('M8 74 L38 50 M92 74 L62 50', 3, C.s2) + Ci(50, 56, 9, C.m); };
  O.gear = function (C) { return Pa(A.cookie(50, 50, 42, 9, 0.16, 0.1), C.m) + Ci(50, 50, 28, C.d) + Ci(50, 50, 12, C.s1); };
  O.pulse = function (C) { return R(8, 18, 84, 64, 16, C.m) + S('M16 52 H34 L42 34 L54 70 L62 48 H84', 6, C.paper); };
  O.lock = function (C) { return S('M30 44 V32 C30 14 70 14 70 32 V44', 9, C.d) + R(16, 42, 68, 48, 12, C.m) + Ci(50, 62, 7, C.ink) + R(47, 64, 6, 14, 3, C.ink); };
  O.play = function (C) { return R(6, 18, 88, 64, 16, C.m) + Pl([[40, 34], [66, 50], [40, 66]], C.paper); };
  O.users = function (C) { return Ci(34, 34, 16, C.hi) + Pa('M6 84 C6 62 18 54 34 54 C50 54 62 62 62 84Z', C.hi) + Ci(66, 38, 18, C.m) + Pa('M34 90 C34 66 48 58 66 58 C84 58 96 66 96 90Z', C.m); };
  O.bolt = function (C) { return Pl([[58, 4], [20, 56], [46, 56], [38, 96], [80, 40], [54, 40]], C.m) + Pl([[58, 4], [54, 40], [80, 40]], C.hi); };
  O.download = function (C) { return L(50, 12, 50, 56, 9, C.m) + S('M30 40 L50 60 L70 40', 9, C.m) + Pa('M10 64 V82 Q10 90 18 90 H82 Q90 90 90 82 V64', 'none', 'stroke="' + C.d + '" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"'); };
  O.search = function (C) { return O.magnifier(C); };
  O.thumb = function (C) { return R(8, 44, 20, 46, 6, C.d) + Pa('M34 46 L50 10 Q60 8 62 20 L58 38 H80 Q92 38 90 52 L84 80 Q82 90 72 90 H34Z', C.m); };
  O.pin = function (C) { return Pa('M50 94 C30 66 20 54 20 38 C20 20 34 8 50 8 C66 8 80 20 80 38 C80 54 70 66 50 94Z', C.m) + Ci(50, 38, 13, C.paper); };
  O.flag = function (C) { return R(20, 8, 6, 86, 3, C.d) + Pa('M26 14 H82 L68 34 L82 54 H26Z', C.m); };
  O.hourglass = function (C) { return R(18, 6, 64, 8, 4, C.ink) + R(18, 86, 64, 8, 4, C.ink) + Pa('M26 14 H74 C74 40 56 44 56 50 C56 56 74 60 74 86 H26 C26 60 44 56 44 50 C44 44 26 40 26 14Z', C.paper) + Pa('M32 18 H68 C66 34 56 40 50 44 C44 40 34 34 32 18Z', C.m) + Pa('M38 86 C40 70 46 62 50 60 C54 62 60 70 62 86Z', C.m); };
})(typeof window !== 'undefined' ? window : globalThis);
