/* v5 hair: 12 styles, each returns {back, front}. Anchors: head centre (cx, cy), half width 42. Highlight band is a lighter tone of the same hair. */
(function (g) {
  'use strict';
  var A = g.NebArtV5, f = A.f, P5 = A.people;
  function N(a) { return a.map(f).join(' '); }
  function cap(cx, cy, o) { /* crown with a curved hairline */
    var lo = o.low || 0;
    return 'M' + N([cx - 45, cy - 4]) + 'C' + N([cx - 51, cy - 46, cx - 26, cy - 67, cx, cy - 67]) + 'C' + N([cx + 26, cy - 67, cx + 51, cy - 46, cx + 45, cy - 4]) + 'C' + N([cx + 42, cy - 18, cx + 37, cy - 30 + lo, cx + 30, cy - 34 + lo]) + 'C' + N([cx + 14, cy - 26 + lo, cx - 14, cy - 26 + lo, cx - 30, cy - 34 + lo]) + 'C' + N([cx - 37, cy - 30 + lo, cx - 42, cy - 18, cx - 45, cy - 4]) + 'Z';
  }
  function sweep(cx, cy, m) { /* m = 1 sweeps left to right, -1 mirrored */
    var X = function (v) { return cx + m * v; };
    return 'M' + N([X(-45), cy - 4]) + 'C' + N([X(-51), cy - 46, X(-26), cy - 67, X(0), cy - 67]) + 'C' + N([X(28), cy - 67, X(51), cy - 44, X(45), cy - 6]) + 'C' + N([X(41), cy - 22, X(35), cy - 31, X(22), cy - 33]) + 'C' + N([X(6), cy - 35, X(-18), cy - 27, X(-33), cy - 9]) + 'C' + N([X(-37), cy - 5, X(-42), cy - 2, X(-45), cy - 4]) + 'Z';
  }
  function shine(cx, cy, col, m) { return A.stroke('M' + N([cx - 25 * m, cy - 56]) + 'Q' + N([cx - 6 * m, cy - 66, cx + 16 * m, cy - 60]), 3.2, col); }
  function long(cx, cy, o) { /* hair behind shoulders */
    var wv = o.wave, p = [], i, y, x;
    for (i = 0; i <= 6; i++) { y = cy - 6 + i * 15; x = cx - 51 - (wv ? 4 * Math.sin(i * 1.5) : 0) - i * 0.8; p.push([x, y]); }
    var L = A.smooth(p, false), R = p.map(function (q) { return [2 * cx - q[0], q[1]]; }).reverse();
    return 'M' + N([cx - 46, cy - 14]) + 'C' + N([cx - 54, cy - 70, cx + 54, cy - 70, cx + 46, cy - 14]) + A.smooth(R, false).replace(/^M[^C]*/, 'L' + N(R[0])).replace(/^L/, 'L') + 'L' + N([cx + (cx - p[6][0]) - 0, cy + 84]) + 'L' + N([p[6][0], cy + 84]) + 'L' + N(p[6]) + A.smooth(p.slice().reverse(), false).replace(/^M[^C]*/, '') + 'Z';
  }
  P5.hair = function (style, o) {
    var cx = o.cx, cy = o.cy, c = o.col, hi = o.hi, b = '', fr = '', i, m = o.flip ? -1 : 1;
    switch (style) {
      case 'crop': fr = A.path(cap(cx, cy, {}), c) + shine(cx, cy, hi, 1); break;
      case 'sweep': fr = A.path(sweep(cx, cy, m), c) + shine(cx, cy, hi, 1); break;
      case 'buzz': fr = A.path('M' + N([cx - 44, cy - 10]) + 'C' + N([cx - 47, cy - 44, cx - 24, cy - 60, cx, cy - 60, cx + 24, cy - 60, cx + 47, cy - 44, cx + 44, cy - 10]) + 'C' + N([cx + 38, cy - 28, cx + 28, cy - 38, cx, cy - 38, cx - 28, cy - 38, cx - 38, cy - 28, cx - 44, cy - 10]) + 'Z', A.mix(c, o.skin, 0.5)); break;
      case 'curly':
        for (i = 0; i < 11; i++) { var a = (178 + i * 18.6) * Math.PI / 180; b += A.circle(cx + 50 * Math.cos(a), cy - 10 + 50 * Math.sin(a) * 1.02, 17.5, c); }
        b += A.ell(cx, cy - 22, 52, 46, c); fr = A.path(cap(cx, cy, { low: -2 }), c) + A.circle(cx - 20, cy - 52, 5, hi) + A.circle(cx + 4, cy - 58, 4, hi); break;
      case 'long': b = A.path(long(cx, cy, {}), c); fr = A.path(cap(cx, cy, { low: 2 }).replace(/C[^C]*C[^C]*C[^C]*Z$/, '') + 'C' + N([cx + 8, cy - 40, cx - 6, cy - 40, cx - 30, cy - 34]) + 'C' + N([cx - 37, cy - 30, cx - 42, cy - 18, cx - 45, cy - 4]) + 'Z', c) + shine(cx, cy, hi, 1); break;
      case 'wavy': b = A.path(long(cx, cy, { wave: true }), c); fr = A.path(sweep(cx, cy, m), c) + shine(cx, cy, hi, 1); break;
      case 'bob': b = A.path('M' + N([cx - 47, cy - 14]) + 'C' + N([cx - 55, cy - 70, cx + 55, cy - 70, cx + 47, cy - 14, cx + 52, cy + 30, cx + 50, cy + 42]) + 'Q' + N([cx + 46, cy + 56, cx + 32, cy + 52]) + 'L' + N([cx - 32, cy + 52]) + 'Q' + N([cx - 46, cy + 56, cx - 50, cy + 42]) + 'C' + N([cx - 52, cy + 30, cx - 55, cy + 6, cx - 47, cy - 14]) + 'Z', c); fr = A.path(sweep(cx, cy, m), c) + shine(cx, cy, hi, 1); break;
      case 'bun': b = A.circle(cx, cy - 72, 17, c) + A.stroke('M' + N([cx - 12, cy - 66]) + 'Q' + N([cx, cy - 60, cx + 12, cy - 66]), 3, hi); fr = A.path(cap(cx, cy, {}), c) + shine(cx, cy, hi, 1); break;
      case 'braid':
        for (i = 0; i < 6; i++) fr += A.rot(i % 2 ? 24 : -24, cx + 48 + i * 2.2, cy + 14 + i * 15, A.ell(cx + 48 + i * 2.2, cy + 14 + i * 15, 8.5 - i * 0.5, 11, c));
        fr = A.path(sweep(cx, cy, m), c) + shine(cx, cy, hi, 1) + fr + A.rect(cx + 51, cy + 98, 8, 6, 3, hi); break;
      case 'pixie': fr = A.path('M' + N([cx - 46, cy + 10]) + 'C' + N([cx - 53, cy - 46, cx - 26, cy - 69, cx + 2, cy - 69, cx + 34, cy - 69, cx + 54, cy - 42, cx + 45, cy - 4]) + 'C' + N([cx + 42, cy - 22, cx + 30, cy - 38, cx + 6, cy - 34]) + 'C' + N([cx - 16, cy - 38, cx - 30, cy - 26, cx - 38, cy - 6]) + 'L' + N([cx - 41, cy + 12]) + 'Z', c) + shine(cx, cy, hi, 1); break;
      case 'elder': fr = A.path('M' + N([cx - 43, cy - 22]) + 'C' + N([cx - 55, cy - 20, cx - 53, cy + 12, cx - 43, cy + 9]) + 'Z', c) + A.path('M' + N([cx + 43, cy - 22]) + 'C' + N([cx + 55, cy - 20, cx + 53, cy + 12, cx + 43, cy + 9]) + 'Z', c) + A.rot(-24, cx - 16, cy - 44, A.ell(cx - 16, cy - 44, 14, 4.5, A.mix(o.skin, '#ffffff', 0.38))); break;
      case 'scarf': b = A.path('M' + N([cx, cy - 70]) + 'C' + N([cx - 52, cy - 70, cx - 60, cy - 20, cx - 56, cy + 22, cx - 54, cy + 52, cx - 42, cy + 68, cx - 34, cy + 90]) + 'L' + N([cx + 34, cy + 90]) + 'C' + N([cx + 42, cy + 68, cx + 54, cy + 52, cx + 56, cy + 22, cx + 60, cy - 20, cx + 52, cy - 70, cx, cy - 70]) + 'Z', c); fr = A.path('M' + N([cx - 45, cy - 4]) + 'C' + N([cx - 51, cy - 46, cx - 26, cy - 64, cx, cy - 64, cx + 26, cy - 64, cx + 51, cy - 46, cx + 45, cy - 4]) + 'C' + N([cx + 42, cy - 22, cx + 32, cy - 34, cx, cy - 36, cx - 32, cy - 34, cx - 42, cy - 22, cx - 45, cy - 4]) + 'Z', c) + A.stroke('M' + N([cx - 30, cy - 52]) + 'Q' + N([cx, cy - 62, cx + 28, cy - 50]), 3, hi); break;
    }
    return { back: b, front: fr };
  };
  P5.HAIR_F = ['sweep', 'long', 'bob', 'bun', 'braid', 'wavy', 'pixie', 'curly', 'scarf'];
  P5.HAIR_M = ['crop', 'sweep', 'buzz', 'curly', 'elder'];
  P5.HAIRCOL = [['#2a1b14', '#4a342a'], ['#1b1411', '#3a2d28'], ['#4a2c1a', '#6e4a33'], ['#7a4a22', '#a06a3c'], ['#a9784a', '#c99a6c'], ['#8f9399', '#b8bcc2'], ['#c2c6cb', '#e2e4e7'], ['#6b2f22', '#934a39']];
})(typeof window !== 'undefined' ? window : globalThis);
