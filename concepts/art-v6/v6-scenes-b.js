/* v6 scenes B: bento (M3 shape tiles), dotwave, packing (bubbles), morphGrid, doodle (study scribbles). */
(function (g) {
  'use strict';
  var A = g.NebArtV6, E = A.engines, f = A.f, sin = Math.sin, cos = Math.cos, PI = Math.PI;
  var SH = ['cookie', 'flower', 'clover', 'burst', 'sunny', 'puffy', 'pebble', 'squircle', 'lotus', 'gem'];
  var GL = ['bolt', 'science', 'genetics', 'functions', 'terminal', 'menu_book', 'draw', 'calculate', 'monitoring', 'public', 'history', 'school', 'music_note', 'code', 'gavel', 'psychology', 'rocket_launch', 'workspace_premium'];
  function up(c, p) { return A.scheme(c.P, c.r, A.pickDeep(c, p)); }

  E.bento = function (c) {
    var w = c.w, h = c.h, r = c.r, S = up(c, 0.3), m = Math.min(w, h), gap = m * 0.026, rad = m * 0.07, cells = [{ x: gap, y: gap, w: w - gap * 2, h: h - gap * 2 }], n = Math.max(5, Math.round(w * h / (m * m) * 4.2)), s = A.rect(0, 0, w, h, 0, S.bg), gl = c.o.glyph ? [c.o.glyph].concat(r.pick(GL)) : GL;
    while (cells.length < n) { cells.sort(function (a, b) { return b.w * b.h - a.w * a.h; }); var q = cells.shift(), t = r.range(0.38, 0.62); if (q.w >= q.h) { cells.push({ x: q.x, y: q.y, w: q.w * t - gap / 2, h: q.h }, { x: q.x + q.w * t + gap / 2, y: q.y, w: q.w * (1 - t) - gap / 2, h: q.h }); } else cells.push({ x: q.x, y: q.y, w: q.w, h: q.h * t - gap / 2 }, { x: q.x, y: q.y + q.h * t + gap / 2, w: q.w, h: q.h * (1 - t) - gap / 2 }); }
    cells.forEach(function (q, i) {
      var cx = q.x + q.w / 2, cy = q.y + q.h / 2, d = Math.min(q.w, q.h), fill = r.chance(0.2) ? S.acc[i % 3] : r.pick(S.ramp.slice(0, 4)), k = r.int(0, 4), id = c.uid + 'c' + i;
      var body = '';
      if (k <= 1) { var sh = r.pick(SH), dark = S.ramp[r.int(3, 5)]; body = A.shape(sh, cx, cy, d * 0.36, r() * 3, dark) + (k === 0 ? A.glyph(r.pick(gl), cx - d * 0.17, cy - d * 0.17, d * 0.34, S.card) : A.circle(cx, cy, d * 0.1, S.card)); }
      else if (k === 2) { for (var a = 0; a < 4; a++) body += A.pill(q.x + q.w * 0.14, q.y + q.h * (0.2 + a * 0.2), q.w * (a % 2 ? 0.5 : 0.72), q.h * 0.09, S.ramp[3 + (a % 3)]); }
      else if (k === 3) { for (var yy = 0; yy < 3; yy++) for (var xx = 0; xx < 3; xx++) body += A.circle(cx + (xx - 1) * d * 0.24, cy + (yy - 1) * d * 0.24, d * 0.07, S.ramp[2 + (xx + yy) % 4]); }
      else body = A.rot(r.int(-20, 20), cx, cy, A.rect(cx - d * 0.3, cy - d * 0.3, d * 0.6, d * 0.6, d * 0.22, S.ramp[4])) + A.star4(cx + d * 0.12, cy - d * 0.12, d * 0.17, S.acc[0]);
      s += A.clipRect(id, q.x, q.y, q.w, q.h, rad, A.rect(q.x, q.y, q.w, q.h, rad, fill) + body);
    });
    return s;
  };

  E.dotwave = function (c) {
    var w = c.w, h = c.h, r = c.r, S = up(c, 0.45), sp = Math.max(w, h) / r.int(26, 38), s = A.rect(0, 0, w, h, 0, S.bg), cols = Math.ceil(w / sp) + 1, rows = Math.ceil(h / sp) + 1, i, j, l1 = r.range(5, 9), l2 = r.range(4, 8), ph = r() * 6, tilt = r.range(-0.6, 0.6);
    for (j = 0; j < rows; j++) for (i = 0; i < cols; i++) {
      var u = 0.5 + 0.5 * sin(i / l1 * PI * 2 / 2 + j * tilt * 0.5 + ph) * cos(j / l2 * PI + i * 0.05), rad = sp * 0.5 * Math.pow(Math.max(0.04, u), 1.3), band = Math.floor(((j + sin(i / 7 + ph) * 2) / rows) * 3.4 + 0.5);
      s += A.circle(i * sp, j * sp, rad, band % 4 === 3 ? S.acc[0] : S.ramp[Math.min(5, 1 + (band % 4) + 1)]);
    }
    return s;
  };

  E.packing = function (c) {
    var w = c.w, h = c.h, r = c.r, S = up(c, 0.3), m = Math.min(w, h), s = A.rect(0, 0, w, h, 0, S.bg), cs = [], t, k, ok, x, y, rad, rr = m * 0.19, gap = m * 0.012;
    for (; rr > m * 0.028; rr *= 0.88) for (t = 0; t < 70; t++) {
      x = r() * w; y = r() * h; ok = true; for (k = 0; k < cs.length; k++) if (Math.hypot(cs[k][0] - x, cs[k][1] - y) < cs[k][2] + rr + gap) { ok = false; break; }
      if (ok) cs.push([x, y, rr]);
    }
    cs.forEach(function (q, i) {
      var col = r.chance(0.12) ? r.pick(S.acc) : r.pick(S.ramp), k2 = r.int(0, 3);
      s += (r.chance(0.25) && q[2] > m * 0.05 ? A.shape(r.pick(SH), q[0], q[1], q[2], r() * 3, col) : A.circle(q[0], q[1], q[2], col));
      if (k2 === 0 && q[2] > m * 0.04) s += A.circle(q[0], q[1], q[2] * 0.5, S.card, 'opacity=".9"');
      else if (k2 === 1) s += A.circle(q[0], q[1], q[2] * 0.3, S.bg);
    });
    return s;
  };

  E.morphGrid = function (c) {
    var w = c.w, h = c.h, r = c.r, S = up(c, 0.35), sp = Math.max(w, h) / r.int(12, 18), s = A.rect(0, 0, w, h, 0, S.bg), cols = Math.ceil(w / sp), rows = Math.ceil(h / sp), i, j, fl = A.field(c.uid, 0.9 / (sp * 5), 0.9 / (sp * 5)), ox = (w - cols * sp) / 2, oy = (h - rows * sp) / 2;
    for (j = 0; j < rows; j++) for (i = 0; i < cols; i++) {
      var u = fl(i * sp, j * sp), x = ox + i * sp + sp / 2, y = oy + j * sp + sp / 2, sz = sp * (0.4 + 0.52 * u), rd = sz * (0.5 - 0.34 * Math.abs(sin(u * 5.2))), col = S.ramp[Math.min(5, Math.floor(u * 6))];
      s += A.rot(u * 70 - 20, x, y, A.rect(x - sz / 2, y - sz / 2, sz, sz, rd, r.chance(0.06) ? S.acc[0] : col));
    }
    return s;
  };

  E.doodle = function (c) {
    var w = c.w, h = c.h, r = c.r, S = up(c, 0.2), m = Math.min(w, h), s = A.rect(0, 0, w, h, 0, S.bg), nx = Math.max(3, Math.round(w / m * 2.5)), ny = 3, cw = w / nx, ch = h / ny, i, j, sw = m * 0.02, bl;
    for (j = 0; j < ny; j++) for (i = 0; i < nx; i++) {
      var x = (i + 0.5) * cw + r.range(-0.15, 0.15) * cw, y = (j + 0.5) * ch + r.range(-0.15, 0.15) * ch, d = Math.min(cw, ch) * 0.4, col = r.chance(0.3) ? r.pick(S.acc) : S.ramp[r.int(2, 5)], k = r.int(0, 8), pts = [], t;
      if (r.chance(0.55)) s += A.shape(r.pick(SH), x, y, d * 1.15, r() * 3, S.ramp[r.int(0, 1)]);
      if (k === 0) s += A.squig(x - d, y, d * 2, d * 0.7, 3, sw, col);
      else if (k === 1) s += A.zig(x - d, y - d * 0.3, d * 2, d * 0.6, 6, sw, col);
      else if (k === 2) { for (t = 0; t < 90; t++) pts.push([x + d * (t / 90) * cos(t / 90 * PI * 5), y + d * (t / 90) * sin(t / 90 * PI * 5)]); s += A.stroke(A.smooth(pts, false), sw, col); }
      else if (k === 3) s += A.circle(x, y, d * 0.7, 'none', 'stroke="' + col + '" stroke-width="' + f(sw) + '"');
      else if (k === 4) s += A.star4(x, y, d * 0.8, col);
      else if (k === 5) s += A.plus(x, y, d * 0.5, sw, col);
      else if (k === 6) s += A.stroke('M' + f(x - d) + ' ' + f(y) + 'Q' + f(x) + ' ' + f(y - d * 1.1) + ' ' + f(x + d) + ' ' + f(y) + 'M' + f(x + d * 0.5) + ' ' + f(y - d * 0.4) + 'L' + f(x + d) + ' ' + f(y) + 'L' + f(x + d * 0.4) + ' ' + f(y + d * 0.3), sw, col);
      else if (k === 7) { for (t = 0; t < 3; t++) s += A.circle(x + (t - 1) * d * 0.5, y, d * 0.12, col); }
      else s += A.rect(x - d * 0.6, y - d * 0.4, d * 1.2, d * 0.8, d * 0.3, 'none', 'stroke="' + col + '" stroke-width="' + f(sw) + '" transform="rotate(' + r.int(-14, 14) + ' ' + f(x) + ' ' + f(y) + ')"');
    }
    return s;
  };

})(typeof window !== 'undefined' ? window : globalThis);
