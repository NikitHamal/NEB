/* v3 pattern engines: truchet, dhaka, lattice, shapeField, stackShapes, scallop, pills, mandala, bubbles, waves, bauhaus, ribbons, arches, confetti, bars. */
(function (g) {
  'use strict';
  var A = g.NebArtV3, E = A.engines, R = A.rect, C = A.circle, f = A.f;
  function tones(c) { var P = c.P; return [P.t(0.14), P.t(0.34), P.t(0.58), P.t(0.82), P.sp(0.55)]; }
  function bg(c, T) { return R(0, 0, c.w, c.h, 0, c.r.chance(0.5) ? c.P.sky : T[0]); }
  function quarter(x, y, s, q, fill) { var a = [[x, y, x + s, y, x, y + s], [x + s, y, x + s, y + s, x, y], [x + s, y + s, x, y + s, x + s, y], [x, y + s, x, y, x + s, y + s]][q % 4]; return A.path('M' + f(a[0]) + ' ' + f(a[1]) + 'L' + f(a[2]) + ' ' + f(a[3]) + 'A' + f(s) + ' ' + f(s) + ' 0 0 ' + (q % 2 ? 0 : 1) + ' ' + f(a[4]) + ' ' + f(a[5]) + 'Z', fill); }
  function cells(c, n, fn) { var s = c.h / n, cols = Math.ceil(c.w / s), o = '', i, j; for (j = 0; j < n; j++) for (i = 0; i < cols; i++) o += fn(i * s, j * s, s, i, j); return o; }

  E.truchet = function (c) { var T = tones(c), r = c.r, a = r.pick([1, 2, 3]), b = r.pick([0, 3, 4]); return bg(c, T) + cells(c, r.int(4, 8), function (x, y, s) { return R(x, y, s + 0.5, s + 0.5, 0, T[a]) + quarter(x, y, s + 0.3, r.int(0, 3), T[b]) + (r.chance(0.5) ? quarter(x + s, y + s, s * 0.5, r.int(0, 3), T[(b + 1) % 5]).replace(/A/, 'A') : ''); }); };
  E.dhaka = function (c) {
    var T = tones(c), r = c.r, w = c.w, h = c.h, n = r.int(6, 9), b = h / n, o = bg(c, T), i, x, k, m;
    for (i = 0; i < n; i++) {
      var y = i * b, t = i % 4, s = b * 0.9, cnt = Math.ceil(w / s) + 1; o += R(0, y, w, b + 0.5, 0, T[(i * 2 + 1) % 4]);
      for (k = 0; k < cnt; k++) { x = k * s; m = x + s / 2;
        if (t === 0) o += A.poly([[x, y + b], [m, y + b * 0.1], [x + s, y + b]], T[(i + 2) % 5]);
        else if (t === 1) o += A.path(A.rpoly([[m, y + b * 0.08], [x + s * 0.9, y + b / 2], [m, y + b * 0.92], [x + s * 0.1, y + b / 2]], b * 0.12), T[4]) + C(m, y + b / 2, b * 0.1, T[0]);
        else if (t === 2) o += R(x + s * 0.15, y + b * 0.2, s * 0.7, b * 0.6, b * 0.12, T[(i + 3) % 5]) + R(x + s * 0.35, y + b * 0.4, s * 0.3, b * 0.2, b * 0.05, T[0]);
        else o += A.poly([[x, y], [m, y + b * 0.9], [x + s, y]], T[(i + 1) % 5]);
      }
    }
    return o;
  };
  E.lattice = function (c) { var T = tones(c), r = c.r, n = r.int(4, 6); return R(0, 0, c.w, c.h, 0, T[1]) + cells(c, n, function (x, y, s, i, j) { var m = s / 2; return R(x + s * 0.06, y + s * 0.06, s * 0.88, s * 0.88, s * 0.2, T[0]) + A.path(A.ngon(4, x + m, y + m, s * 0.36, Math.PI / 4, s * 0.1), T[(i + j) % 2 ? 3 : 2]) + C(x + m, y + m, s * 0.12, (i + j) % 2 ? T[0] : T[4]) + quarter(x + s * 0.06, y + s * 0.06, s * 0.2, 0, T[2]) + quarter(x + s * 0.94 - s * 0.2, y + s * 0.06, s * 0.2, 1, T[2]) + quarter(x + s * 0.06, y + s * 0.94 - s * 0.2, s * 0.2, 3, T[2]) + quarter(x + s * 0.94 - s * 0.2, y + s * 0.94 - s * 0.2, s * 0.2, 2, T[2]); }); };
  E.shapeField = function (c) { var T = tones(c), r = c.r, names = r.pick([['cookie', 'sunny', 'flower', 'clover'], ['squircle', 'circle', 'gem', 'pebble'], A.shapeNames]), n = r.int(3, 7); return bg(c, T) + cells(c, n, function (x, y, s) { return r.chance(0.12) ? '' : A.shape(r.pick(names), x + s / 2, y + s / 2, s * r.range(0.3, 0.46), r.range(0, 3), T[r.int(1, 4)]); }); };
  E.stackShapes = function (c) {
    var T = tones(c), r = c.r, o = bg(c, T), i, N = r.int(5, 7), sh = r.pick(['cookie', 'sunny', 'flower', 'burst', 'puffy', 'clover', 'lotus']), cx = c.w * r.range(0.3, 0.7), cy = c.h * 0.5, R0 = c.h * r.range(0.5, 0.7), rot = r.range(0, 3);
    for (i = 0; i < N; i++) o += A.shape(i % 3 === 2 ? 'circle' : sh, cx, cy, R0 * (1 - i / N), rot + i * 0.12, c.P.t(0.12 + i / N * 0.72));
    for (i = 0; i < 4; i++) o += A.shape(r.pick(A.shapeNames), r.range(0, 1) * c.w, r.range(0, 1) * c.h, c.h * r.range(0.05, 0.13), r.range(0, 3), r.pick(T));
    return o + A.shape(sh, cx, cy, R0 / N * 0.7, rot, T[4]);
  };
  E.scallop = function (c) { var T = tones(c), r = c.r, n = r.int(5, 9), s = c.h / n, o = R(0, 0, c.w, c.h, 0, T[0]), i, j; for (i = n * 2; i >= 0; i--) for (j = -1; j * s < c.w + s; j++) { var cx = j * s + (i % 2 ? s / 2 : 0), cy = i * s * 0.5; o += A.path('M' + f(cx - s / 2) + ' ' + f(cy) + 'A' + f(s / 2) + ' ' + f(s / 2) + ' 0 0 0 ' + f(cx + s / 2) + ' ' + f(cy) + 'Z', c.P.t(0.1 + (i / (n * 2)) * 0.7)) + C(cx, cy + s * 0.1, s * 0.07, T[4]); } return o; };
  E.pills = function (c) { var T = tones(c), r = c.r, n = r.int(7, 12), b = c.h / n, o = bg(c, T), i, x; for (i = 0; i < n; i++) { x = -r.range(0, 0.3) * c.w; while (x < c.w) { var l = r.range(0.08, 0.36) * c.w; o += R(x, i * b + b * 0.12, l, b * 0.76, b * 0.38, T[r.int(1, 4)]); x += l + b * 0.3; } } return o; };
  E.mandala = function (c) {
    var T = tones(c), r = c.r, o = bg(c, T), k, i, j, n, cx = c.w * r.range(0.35, 0.65), cy = c.h * 0.5, R0 = c.h * 0.55, rings = r.int(4, 6);
    for (k = rings; k >= 1; k--) { n = 6 + (rings - k) * 2 + r.int(0, 1) * 2; var rad = R0 * k / rings; o += C(cx, cy, rad, c.P.t(0.12 + (rings - k) * 0.1)); for (j = 0; j < n; j++) { var a = j / n * Math.PI * 2 + k * 0.2, px = cx + Math.cos(a) * rad * 0.8, py = cy + Math.sin(a) * rad * 0.8, pr = rad * Math.sin(Math.PI / n) * 1.05; o += A.shape(k % 2 ? 'circle' : 'lotus', px, py, pr, a, c.P.t(0.3 + ((rings - k) / rings) * 0.55)); } }
    return o + A.shape('flower', cx, cy, R0 / rings * 0.7, 0, T[4]);
  };
  E.bubbles = function (c) { var T = tones(c), r = c.r, o = bg(c, T), pts = [], tries = 0, N = Math.round(c.w * c.h / 2600); while (pts.length < N && tries++ < 4000) { var rad = r.range(0.015, 0.15) * c.h, x = r.range(0, 1) * c.w, y = r.range(0, 1) * c.h, ok = true; for (var i = 0; i < pts.length; i++) if (Math.hypot(pts[i][0] - x, pts[i][1] - y) < pts[i][2] + rad + 3) { ok = false; break; } if (ok) { pts.push([x, y, rad]); o += C(x, y, rad, T[r.int(1, 4)]) + (rad > c.h * 0.06 ? C(x, y, rad * 0.5, T[r.int(0, 3)]) : ''); } } return o; };
  E.waves = function (c) { var r = c.r, o = '', n = r.int(7, 11), i, x, ph = r.range(0, 6), fr = r.range(1, 3) / c.w * 6.28, amp = c.h * r.range(0.03, 0.09); o += R(0, 0, c.w, c.h, 0, c.P.t(0.06)); for (i = 0; i < n; i++) { var pts = []; for (x = -20; x <= c.w + 40; x += 16) pts.push([x, c.h * (i + 0.5) / n + Math.sin(x * fr + ph + i * 0.7) * amp]); o += A.fillTo(pts, c.h * 1.1, c.P.t(0.1 + i / n * 0.72)); } return o; };
  E.bauhaus = function (c) { var T = tones(c), r = c.r, n = r.int(3, 6); return bg(c, T) + cells(c, n, function (x, y, s) { var t = r.int(0, 6), a = r.pick(T.slice(1)), m = s / 2; return t === 0 ? quarter(x, y, s, r.int(0, 3), a) : t === 1 ? C(x + m, y + m, s * 0.42, a) : t === 2 ? A.arch(x + s * 0.1, y + s * 0.1, s * 0.8, s * 0.9, a) : t === 3 ? R(x + s * 0.1, y + s * 0.1, s * 0.8, s * 0.8, s * 0.28, a) : t === 4 ? A.path(A.ngon(4, x + m, y + m, s * 0.46, 0, s * 0.1), a) : t === 5 ? C(x + m, y + m, s * 0.4, a) + C(x + m, y + m, s * 0.17, r.pick(T)) : ''; }); };
  E.ribbons = function (c) { var r = c.r, o = R(0, 0, c.w, c.h, 0, c.P.t(0.06)), n = r.int(6, 9), i, a = r.range(-0.4, 0.4); for (i = 0; i < n; i++) { var y = c.h * (i + 0.5) / n, pts = [], x; for (x = -40; x <= c.w + 60; x += c.w / 6) pts.push([x, y + Math.sin(x / c.w * 5 + i * 0.7 + a) * c.h * 0.16 + (x / c.w - 0.5) * a * c.h]); o += A.stroke(A.smooth(pts, false), c.h / n * 1.25, i === n - 2 ? c.P.sp(0.55) : c.P.t(0.14 + i / n * 0.7)); } return o; };
  E.arches = function (c) { var T = tones(c), r = c.r, n = r.int(2, 4), s = c.h / n * 0.96, cols = Math.ceil(c.w / (s * 0.9)) + 1, o = bg(c, T), i, j, k; for (j = 0; j < n + 1; j++) for (i = 0; i < cols; i++) for (k = 0; k < 4; k++) { var w = s * 0.82 * (1 - k * 0.22), x = i * s * 0.9 + s * 0.04 + (s * 0.82 - w) / 2 + (j % 2 ? s * 0.45 : 0) - s * 0.4, y = j * s * 0.96 + s * 0.2 + (s * 0.82 - w) / 2 - s * 0.2; o += A.arch(x, y, w, s * 0.9 - (s * 0.82 - w) / 2, k === 3 ? T[4] : c.P.t(0.2 + k * 0.22 + (j % 3) * 0.05)); } return o; };
  E.confetti = function (c) { var T = tones(c), r = c.r, o = bg(c, T), i, N = Math.round(c.w * c.h / 9000); for (i = 0; i < N; i++) { var x = r.range(0, 1) * c.w, y = r.range(0, 1) * c.h, s = c.h * r.range(0.015, 0.05), t = r.int(0, 4), col = r.pick(T.slice(1)); o += t === 0 ? C(x, y, s, col) : t === 1 ? A.star4(x, y, s * 1.5, col) : t === 2 ? R(x, y, s * 3, s, s / 2, col, 'transform="rotate(' + r.int(0, 170) + ' ' + f(x) + ' ' + f(y) + ')"') : t === 3 ? A.shape(r.pick(['flower', 'cookie', 'clover']), x, y, s * 1.4, r.range(0, 3), col) : A.line(x - s, y, x + s, y, s * 0.5, col) + A.line(x, y - s, x, y + s, s * 0.5, col); } return o; };
  E.bars = function (c) { var T = tones(c), r = c.r, n = Math.round(c.w / c.h * r.int(8, 12)), b = c.w / n, o = bg(c, T), i; for (i = 0; i < n; i++) { var hh = c.h * r.range(0.2, 0.9); o += R(i * b + b * 0.12, c.h - hh, b * 0.76, hh + b, b * 0.38, c.P.t(0.2 + (hh / c.h) * 0.6)) + C(i * b + b / 2, c.h - hh + b * 0.38, b * 0.14, i % 3 === 0 ? T[4] : T[0]); } return o; };
})(typeof window !== 'undefined' ? window : globalThis);
