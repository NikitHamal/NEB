/* v5 people: torso + 9 outfits, accessories, 7 backdrops, engine "person". One hue, one backdrop shape, nothing scattered. */
(function (g) {
  'use strict';
  var A = g.NebArtV5, f = A.f, P5 = A.people;
  function N(a) { return a.map(f).join(' '); }
  P5.OUTFITS = ['tee', 'hoodie', 'blazer', 'daura', 'labcoat', 'cardigan', 'turtle', 'kurta', 'vneck'];
  P5.ACCS = ['none', 'none', 'round', 'rect', 'headphones', 'topi', 'grad', 'bindi', 'earring'];
  P5.BGS = ['disc', 'arch', 'cookie', 'split', 'squircle', 'bloom', 'solid'];
  var LAST = {};
  function torso(cx, nw, nd, V, col) {
    LAST = { cx: cx, nw: nw, nd: nd, V: V };
    var neck = V ? 'L' + N([cx, 180 + nd]) + 'L' + N([cx + nw, 180]) : 'C' + N([cx - nw, 180 + nd * 0.9, cx - nw * 0.4, 180 + nd, cx, 180 + nd, cx + nw * 0.4, 180 + nd, cx + nw, 180 + nd * 0.9, cx + nw, 180]);
    return A.path('M' + N([cx - 100, 256]) + 'L' + N([cx - 100, 218]) + 'C' + N([cx - 100, 196, cx - 64, 192, cx - 36, 184]) + 'L' + N([cx - nw, 180]) + neck + 'L' + N([cx + 36, 184]) + 'C' + N([cx + 64, 192, cx + 100, 196, cx + 100, 218]) + 'L' + N([cx + 100, 256]) + 'Z', col);
  }
  P5.outfit = function (kind, cx, C, k) {
    var back = '', body = '', over = '', m = C.m, d = C.d, pp = C.paper;
    switch (kind) {
      case 'hoodie': back = A.ell(cx, 192, 58, 24, d); body = torso(cx, 30, 12, 0, m); over = A.stroke('M' + N([cx - 30, 182]) + 'Q' + N([cx, 206, cx + 30, 182]), 5, d) + A.line(cx - 13, 198, cx - 15, 228, 3.2, C.pap2) + A.line(cx + 13, 198, cx + 15, 228, 3.2, C.pap2); break;
      case 'blazer': body = torso(cx, 36, 62, 1, d) + A.poly([[cx - 36, 180], [cx, 242], [cx + 36, 180], [cx + 22, 180], [cx, 216], [cx - 22, 180]], pp); over = A.poly([[cx - 6, 206], [cx + 6, 206], [cx + 9, 222], [cx, 250], [cx - 9, 222]], m) + A.poly([[cx - 36, 180], [cx - 14, 218], [cx - 30, 232], [cx - 54, 190]], C.ink) + A.poly([[cx + 36, 180], [cx + 14, 218], [cx + 30, 232], [cx + 54, 190]], C.ink); break;
      case 'daura': body = torso(cx, 20, 6, 0, pp); over = A.rect(cx - 21, 172, 42, 15, 6, C.pap2) + A.line(cx, 190, cx, 256, 2, C.pap2) + A.circle(cx + 7, 204, 2.6, m) + A.circle(cx + 7, 222, 2.6, m) + A.circle(cx + 7, 240, 2.6, m) + A.line(cx - 62, 214, cx - 40, 256, 2, C.pap2); break;
      case 'labcoat': body = torso(cx, 38, 60, 1, pp) + A.poly([[cx - 26, 180], [cx, 226], [cx + 26, 180]], m); over = A.stroke('M' + N([cx - 38, 180]) + 'L' + N([cx - 6, 232]), 3, C.pap2) + A.stroke('M' + N([cx + 38, 180]) + 'L' + N([cx + 6, 232]), 3, C.pap2) + A.stroke('M' + N([cx - 30, 186, cx - 38, 238, cx + 38, 238, cx + 30, 186]).replace(/(\S+ \S+) (\S+ \S+) (\S+ \S+) (\S+ \S+)/, '$1C$2 $3 $4'), 3.2, d) + A.circle(cx + 14, 240, 6, d) + A.circle(cx + 14, 240, 2.4, m); break;
      case 'cardigan': body = torso(cx, 34, 40, 1, d) + A.path('M' + N([cx - 28, 180]) + 'L' + N([cx, 212]) + 'L' + N([cx + 28, 180]) + 'L' + N([cx + 36, 256, cx - 36, 256]) + 'Z', pp); over = A.line(cx, 214, cx, 256, 2.4, C.pap2) + A.stroke('M' + N([cx - 34, 182]) + 'L' + N([cx, 216]) + 'L' + N([cx + 34, 182]), 5, m) + A.circle(cx - 8, 232, 2.6, pp) + A.circle(cx - 8, 246, 2.6, pp); break;
      case 'turtle': body = torso(cx, 24, 10, 0, m); over = A.rect(cx - 24, 166, 48, 28, 11, d) + A.line(cx - 18, 180, cx + 18, 180, 2, m); break;
      case 'kurta': body = torso(cx, 26, 16, 0, m); over = A.stroke('M' + N([cx - 34, 182]) + 'C' + N([cx - 30, 206, cx + 30, 206, cx + 34, 182]), 3, pp) + A.line(cx, 200, cx, 238, 2.6, pp) + A.circle(cx, 238, 3.4, pp); break;
      case 'vneck': body = torso(cx, 32, 38, 1, m); over = A.stroke('M' + N([cx - 32, 181]) + 'L' + N([cx, 218]) + 'L' + N([cx + 32, 181]), 5, d); break;
      default: body = torso(cx, 27, 15, 0, m); over = A.stroke('M' + N([cx - 28, 181]) + 'C' + N([cx - 26, 192, cx - 12, 197, cx, 197, cx + 12, 197, cx + 26, 192, cx + 28, 181]), 4.4, d);
    }
    return { back: back, body: body, over: over, neckless: kind === 'turtle' };
  };
  P5.acc = function (kind, o) {
    var cx = o.cx, cy = o.cy, C = o.C, fr = o.frame, s = '', i;
    if (kind === 'round') s = A.circle(cx - 17, cy + 2, 13.5, 'none', 'stroke="' + fr + '" stroke-width="2.6"') + A.circle(cx + 17, cy + 2, 13.5, 'none', 'stroke="' + fr + '" stroke-width="2.6"') + A.stroke('M' + N([cx - 3.6, cy + 0, cx, cy - 3, cx + 3.6, cy + 0]).replace(/ (\S+) (\S+) (\S+) (\S+)$/, 'Q$1 $2 $3 $4'), 2.4, fr) + A.line(cx - 30.4, cy, cx - 43, cy - 2, 2.4, fr) + A.line(cx + 30.4, cy, cx + 43, cy - 2, 2.4, fr);
    if (kind === 'rect') s = A.rect(cx - 33, cy - 9, 31, 22, 8, 'none', 'stroke="' + fr + '" stroke-width="2.6"') + A.rect(cx + 2, cy - 9, 31, 22, 8, 'none', 'stroke="' + fr + '" stroke-width="2.6"') + A.line(cx - 2, cy - 1, cx + 2, cy - 1, 2.4, fr) + A.line(cx - 33, cy - 3, cx - 43, cy - 4, 2.4, fr) + A.line(cx + 33, cy - 3, cx + 43, cy - 4, 2.4, fr);
    if (kind === 'headphones') s = A.stroke('M' + N([cx - 49, cy - 2]) + 'C' + N([cx - 54, cy - 86, cx + 54, cy - 86, cx + 49, cy - 2]), 6.5, C.d) + A.rect(cx - 58, cy - 12, 15, 36, 7, C.m) + A.rect(cx + 43, cy - 12, 15, 36, 7, C.m) + A.rect(cx - 54, cy - 6, 7, 24, 3.5, C.d) + A.rect(cx + 47, cy - 6, 7, 24, 3.5, C.d);
    if (kind === 'topi') {
      var d = 'M' + N([cx - 43, cy - 32]) + 'L' + N([cx - 42, cy - 62]) + 'Q' + N([cx, cy - 72, cx + 42, cy - 62]) + 'L' + N([cx + 43, cy - 32]) + 'Q' + N([cx, cy - 22, cx - 43, cy - 32]) + 'Z', st = '';
      for (i = 0; i < 7; i++) st += A.rect(cx - 42 + i * 12.5, cy - 74, 5, 50, 0, i % 2 ? C.hi : C.ink);
      s = A.clip(o.uid + 'tp', d, A.rect(cx - 46, cy - 76, 92, 54, 0, C.m) + st) + A.stroke('M' + N([cx - 43, cy - 31]) + 'Q' + N([cx, cy - 21, cx + 43, cy - 31]), 3.4, C.d);
    }
    if (kind === 'grad') s = A.path('M' + N([cx - 34, cy - 50]) + 'L' + N([cx - 34, cy - 32]) + 'Q' + N([cx, cy - 16, cx + 34, cy - 32]) + 'L' + N([cx + 34, cy - 50]) + 'Z', C.d) + A.poly([[cx - 64, cy - 52], [cx, cy - 80], [cx + 64, cy - 52], [cx, cy - 28]], C.ink) + A.line(cx + 54, cy - 51, cx + 54, cy - 20, 2.6, C.hi) + A.circle(cx + 54, cy - 17, 4.4, C.hi);
    if (kind === 'bindi') s = A.circle(cx, cy - 22, 2.8, '#c63b30');
    if (kind === 'earring') s = A.circle(cx - 44, cy + 19, 3.6, '#e2b24c') + A.circle(cx + 44, cy + 19, 3.6, '#e2b24c');
    return s;
  };
  P5.backdrop = function (kind, P, r, uid) {
    switch (kind) {
      case 'disc': return A.circle(128, 124, 106, P.s2);
      case 'arch': return A.arch(26, 22, 204, 240, P.s2);
      case 'cookie': return A.path(A.cookie(128, 124, 116, 12, 0.07, r() * 3), P.s2);
      case 'bloom': return A.path(A.cookie(128, 124, 120, 6, 0.12, r() * 3), P.s2);
      case 'split': return A.poly([[0, 0], [256, 0], [256, 90], [0, 190]], P.s2);
      case 'squircle': return A.rot(-8, 128, 128, A.rect(26, 26, 204, 204, 62, P.s2));
      default: return '';
    }
  };
  /* o: skin(0-7) hair style, hc(0-7), outfit, acc, expr(smile|grin|calm|joy), bg, fem, flip, beard, jaw, oc ('m'|'d'|'alt'|'ink') */
  A.engines.person = function (c) {
    var P = c.P, o = c.o, cx = 128, cy = 108, k = P5.skinKit(o.skin), hc = P5.HAIRCOL[o.hc], base = o.oc === 'alt' ? P.alt : P, C = { m: base.m, d: base.d, hi: base.hi, ink: base.ink, paper: P.paper, pap2: P.pap2 };
    var hair = P5.hair(o.hair, { cx: cx, cy: cy, col: hc[0], hi: hc[1], skin: k.skin, flip: o.flip });
    var of = P5.outfit(o.outfit, cx, C, k), ff = P5.face({ cx: cx, cy: cy, w: o.fem ? 40 : 43, jaw: o.jaw || 1, k: k, expr: o.expr, iris: P5.IRIS[(o.skin + o.hc) % 5], lid: '#2a1710', brow: A.mix(hc[0], '#1a0f0a', 0.25), fem: o.fem, uid: c.uid });
    var s = P5.backdrop(o.bg, P, c.r, c.uid) + of.back + hair.back, bodyS = of.body;
    if (!of.neckless) {
      var L = LAST, nk = L.V ? 'L' + N([L.cx, 180 + L.nd]) + 'L' + N([L.cx + L.nw, 180]) : 'C' + N([L.cx - L.nw, 180 + L.nd * 0.9, L.cx - L.nw * 0.4, 180 + L.nd, L.cx, 180 + L.nd, L.cx + L.nw * 0.4, 180 + L.nd, L.cx + L.nw, 180 + L.nd * 0.9, L.cx + L.nw, 180]);
      s += A.rect(cx - 17, cy + 30, 34, 62, 0, k.skin) + A.path('M' + N([cx - L.nw, 180]) + nk + 'Z', k.skin) + A.path('M' + N([cx - 17, cy + 40]) + 'L' + N([cx + 17, cy + 40]) + 'L' + N([cx + 17, cy + 56]) + 'Q' + N([cx, cy + 70, cx - 17, cy + 56]) + 'Z', k.shade);
    }
    s += bodyS + of.over + ff.base;
    if (o.beard) { var bc = hc[0]; s += A.path('M' + N([cx - 43, cy + 2]) + 'C' + N([cx - 45, cy + 40, cx - 26, cy + 60, cx, cy + 60, cx + 26, cy + 60, cx + 45, cy + 40, cx + 43, cy + 2]) + 'C' + N([cx + 38, cy + 24, cx + 30, cy + 26, cx + 20, cy + 28]) + 'Q' + N([cx, cy + 30, cx - 20, cy + 28]) + 'C' + N([cx - 30, cy + 26, cx - 38, cy + 24, cx - 43, cy + 2]) + 'Z', bc); }
    s += ff.feat + hair.front + P5.acc(o.acc, { cx: cx, cy: cy, C: C, frame: o.acc === 'round' || o.acc === 'rect' ? base.ink : '', uid: c.uid });
    return s;
  };
})(typeof window !== 'undefined' ? window : globalThis);
