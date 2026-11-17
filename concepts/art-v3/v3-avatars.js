/* v3 avatars: frameless 256x256 profile pictures (no ring, no border). Buddies, people, critters, glyph tiles. */
(function (g) {
  'use strict';
  var A = g.NebArtV3, E = A.engines, R = A.rect, C = A.circle, S = A.stroke, f = A.f;
  var SKIN = ['#f6d3b3', '#e9b98d', '#d29b6c', '#b87a4d', '#8d5a36', '#5f3b22'], HAIR = ['#1f1a17', '#3b2a20', '#6b4a2f', '#a8743a', '#d8a24a', '#2b3a4a'];
  function eyes(r, x, y, gap, ink, sz) {
    var t = r.int(0, 4), a = x - gap, b = x + gap;
    return t === 0 ? C(a, y, sz, ink) + C(b, y, sz, ink) : t === 1 ? '<ellipse cx="' + a + '" cy="' + y + '" rx="' + sz * 0.8 + '" ry="' + sz * 1.4 + '" fill="' + ink + '"/><ellipse cx="' + b + '" cy="' + y + '" rx="' + sz * 0.8 + '" ry="' + sz * 1.4 + '" fill="' + ink + '"/>'
      : t === 2 ? S('M' + (a - sz) + ' ' + (y + sz * 0.4) + 'Q' + a + ' ' + (y - sz * 1.4) + ' ' + (a + sz) + ' ' + (y + sz * 0.4), sz * 0.55, ink) + S('M' + (b - sz) + ' ' + (y + sz * 0.4) + 'Q' + b + ' ' + (y - sz * 1.4) + ' ' + (b + sz) + ' ' + (y + sz * 0.4), sz * 0.55, ink)
      : t === 3 ? C(a, y, sz, ink) + S('M' + (b - sz) + ' ' + y + 'H' + (b + sz), sz * 0.55, ink) : S('M' + (a - sz) + ' ' + y + 'H' + (a + sz), sz * 0.55, ink) + S('M' + (b - sz) + ' ' + y + 'H' + (b + sz), sz * 0.55, ink);
  }
  function mouth(r, x, y, w, ink, tongue) {
    var t = r.int(0, 3);
    return t === 0 ? S('M' + (x - w) + ' ' + y + 'Q' + x + ' ' + (y + w * 0.9) + ' ' + (x + w) + ' ' + y, 5, ink) : t === 1 ? A.path('M' + (x - w) + ' ' + y + 'H' + (x + w) + 'A' + w + ' ' + w * 0.95 + ' 0 0 1 ' + (x - w) + ' ' + y + 'Z', ink) + A.path('M' + (x - w * 0.5) + ' ' + (y + w * 0.7) + 'Q' + x + ' ' + (y + w * 0.35) + ' ' + (x + w * 0.5) + ' ' + (y + w * 0.7) + 'A' + w * 0.5 + ' ' + w * 0.3 + ' 0 0 1 ' + (x - w * 0.5) + ' ' + (y + w * 0.7) + 'Z', tongue)
      : t === 2 ? C(x, y + 4, w * 0.35, ink) : S('M' + (x - w * 0.7) + ' ' + y + 'H' + (x + w * 0.7), 5, ink);
  }
  function backdrop(c, o) { var P = c.P, r = c.r; o = R(0, 0, 256, 256, 0, P.t(r.range(0.1, 0.3))); if (r.chance(0.6)) o += A.shape(r.pick(['cookie', 'sunny', 'flower', 'burst', 'clover', 'lotus']), r.range(100, 156), r.range(110, 150), r.range(100, 130), r.range(0, 3), P.t(r.range(0.28, 0.42))); return o; }
  E.avBuddy = function (c) {
    var P = c.P, r = c.r, ink = P.dark ? '#14161c' : P.ink, o = backdrop(c, ''), body = r.pick(['cookie', 'sunny', 'cookie12', 'puffy', 'squircle', 'pebble', 'cookie', 'squircle']), fill = r.chance(0.3) ? P.sp(0.6) : P.t(r.range(0.55, 0.72)), ac = r.int(0, 5);
    if (ac === 0) o += S('M128 54 V28', 6, ink) + A.path('M128 34 Q96 20 90 46 Q120 52 128 34Z', P.sp(0.55)) + A.path('M128 34 Q160 14 172 40 Q140 48 128 34Z', P.t(0.5));
    if (ac === 1) o += S('M128 54 V22', 5, ink) + C(128, 20, 11, P.sp(0.6));
    o += A.shape(body, 128, 138, 88, r.range(0, 3), fill) + eyes(r, 128, 124, r.range(22, 32), ink, r.range(7, 11)) + mouth(r, 128, 156, r.range(16, 24), ink, P.sp(0.5));
    if (r.chance(0.6)) o += C(86, 148, 11, P.sp(0.3)) + C(170, 148, 11, P.sp(0.3));
    if (ac === 2) o += S('M84 124 H172', 5, ink) + C(100, 124, 20, 'none', 'stroke="' + ink + '" stroke-width="5"') + C(156, 124, 20, 'none', 'stroke="' + ink + '" stroke-width="5"');
    if (ac === 3) o += A.path(A.rpoly([[128, 36], [196, 62], [128, 88], [60, 62]], 6), ink) + S('M190 64 V104', 5, P.sp(0.6)) + C(190, 108, 7, P.sp(0.6));
    return o;
  };
  E.avPerson = function (c) {
    var P = c.P, r = c.r, ink = P.dark ? '#14161c' : P.ink, sk = r.pick(SKIN), hr = r.pick(HAIR), shirt = r.pick([P.t(0.62), P.sp(0.6), P.t(0.8), P.t(0.4)]), o = backdrop(c, ''), kind = r.int(0, 6), long = kind === 1 || kind === 4;
    if (long) o += R(72, 62, 112, 130, 50, hr);
    if (kind === 3) o += C(128, 54, 22, hr);
    o += A.path('M24 256 Q24 186 128 182 Q232 186 232 256Z', shirt) + R(110, 150, 36, 40, 10, sk) + A.path('M110 176 Q128 192 146 176 V190 H110Z', sk) + C(76, 126, 11, sk) + C(180, 126, 11, sk) + C(128, 118, 56, sk);
    if (kind === 0 || kind === 3 || kind === 5) o += A.path('M72 114 Q70 58 128 58 Q186 58 184 114 Q170 86 128 88 Q88 86 72 114Z', hr);
    if (kind === 1) o += A.path('M72 120 Q70 58 128 58 Q186 58 184 120 Q160 80 118 86 Q92 92 72 120Z', hr);
    if (kind === 2) o += C(100, 70, 22, hr) + C(128, 62, 26, hr) + C(156, 70, 22, hr) + C(78, 100, 18, hr) + C(178, 100, 18, hr) + A.path('M76 108 Q128 70 180 108 Q150 88 128 90 Q104 88 76 108Z', hr);
    if (kind === 4) o += A.path('M72 120 Q70 58 128 58 Q186 58 184 120 Q150 70 128 96 Q106 70 72 120Z', hr);
    if (kind === 5) { var tp = P.sp(0.55); o += A.path('M70 94 V70 Q128 36 186 70 V94 Q128 80 70 94Z', tp) + A.poly([[80, 86], [92, 72], [104, 84]], P.paper) + A.poly([[110, 82], [122, 68], [134, 80]], P.paper) + A.poly([[140, 82], [152, 68], [164, 82]], P.paper); }
    if (kind === 6) o += A.path('M72 112 Q70 62 128 62 Q186 62 184 112 Q160 90 128 92 Q96 90 72 112Z', hr) + A.path(A.rpoly([[128, 26], [200, 54], [128, 80], [56, 54]], 5), ink) + S('M194 56 V92', 5, P.sp(0.6)) + C(194, 96, 6, P.sp(0.6));
    o += C(108, 124, 5.5, ink) + C(148, 124, 5.5, ink) + S('M112 146 Q128 160 144 146', 5, ink) + C(94, 142, 8, P.sp(0.3)) + C(162, 142, 8, P.sp(0.3));
    if (r.chance(0.35)) o += C(108, 124, 17, 'none', 'stroke="' + ink + '" stroke-width="4.5"') + C(148, 124, 17, 'none', 'stroke="' + ink + '" stroke-width="4.5"') + S('M125 124 H131', 4.5, ink);
    return o;
  };
  E.avCritter = function (c) {
    var P = c.P, r = c.r, ink = P.dark ? '#14161c' : P.ink, o = backdrop(c, ''), k = r.int(0, 4), b = P.t(r.range(0.55, 0.7)), l = P.t(0.2), d = P.t(0.82), sp = P.sp(0.55);
    if (k === 0) o += A.poly([[70, 64], [100, 96], [66, 108]], d) + A.poly([[186, 64], [156, 96], [190, 108]], d) + A.shape('pebble', 128, 144, 82, 0.2, b) + A.path('M128 226 Q80 220 84 150 Q128 130 172 150 Q176 220 128 226Z', l) + C(98, 118, 30, P.paper) + C(158, 118, 30, P.paper) + C(98, 118, 14, ink) + C(158, 118, 14, ink) + A.poly([[116, 138], [140, 138], [128, 160]], sp);
    else if (k === 1) o += A.rpoly([[64, 70], [96, 56], [112, 100]], 6).replace(/^/, '') && (A.path(A.rpoly([[62, 130], [64, 52], [112, 84]], 8), b) + A.path(A.rpoly([[194, 130], [192, 52], [144, 84]], 8), b) + A.path(A.rpoly([[74, 100], [76, 66], [98, 86]], 4), sp) + A.path(A.rpoly([[182, 100], [180, 66], [158, 86]], 4), sp) + C(128, 142, 74, b) + C(100, 128, 8, ink) + C(156, 128, 8, ink) + A.path(A.rpoly([[118, 148], [138, 148], [128, 160]], 3), sp) + S('M128 160 V170 M116 174 Q128 182 140 174', 4, ink) + S('M70 150 H46 M72 162 L50 174 M186 150 H210 M184 162 L206 174', 4, ink));
    else if (k === 2) o += C(70, 80, 28, b) + C(186, 80, 28, b) + C(70, 80, 15, l) + C(186, 80, 15, l) + C(128, 140, 80, b) + '<ellipse cx="128" cy="164" rx="40" ry="32" fill="' + l + '"/>' + C(104, 124, 8, ink) + C(152, 124, 8, ink) + '<ellipse cx="128" cy="152" rx="14" ry="10" fill="' + ink + '"/>' + S('M128 160 V172 M114 176 Q128 186 142 176', 4, ink);
    else if (k === 3) o += '<ellipse cx="94" cy="76" rx="22" ry="56" fill="' + b + '"/><ellipse cx="162" cy="76" rx="22" ry="56" fill="' + b + '"/><ellipse cx="94" cy="80" rx="10" ry="38" fill="' + sp + '"/><ellipse cx="162" cy="80" rx="10" ry="38" fill="' + sp + '"/>' + C(128, 150, 72, b) + C(106, 140, 8, ink) + C(150, 140, 8, ink) + A.path(A.rpoly([[120, 156], [136, 156], [128, 166]], 3), sp) + S('M128 166 V174 M116 178 Q128 188 140 178', 4, ink) + C(92, 162, 10, sp) + C(164, 162, 10, sp);
    else o += A.path(A.rpoly([[56, 134], [60, 54], [112, 86]], 8), sp) + A.path(A.rpoly([[200, 134], [196, 54], [144, 86]], 8), sp) + A.path(A.rpoly([[128, 224], [52, 120], [128, 92], [204, 120]], 30), sp) + A.path(A.rpoly([[128, 224], [52, 120], [128, 150], [204, 120]], 30), P.paper) + C(100, 128, 8, ink) + C(156, 128, 8, ink) + C(128, 196, 10, ink);
    return o;
  };
  E.avGlyph = function (c) {
    var P = c.P, r = c.r, gl = c.o.glyph || r.pick(['school', 'science', 'bolt', 'functions', 'terminal', 'menu_book', 'eco', 'music_note', 'rocket_launch', 'psychology', 'calculate', 'public']), sh = r.pick(['cookie', 'sunny', 'cookie12', 'burst', 'puffy', 'pebble', 'lotus', 'squircle']);
    return R(0, 0, 256, 256, 0, P.t(0.14)) + A.shape(r.pick(['circle', 'squircle', 'puffy']), 128, 128, 126, r.range(0, 3), P.t(0.26)) + A.shape(sh, 128, 128, 96, r.range(0, 3), r.chance(0.4) ? P.sp(0.6) : P.t(0.62)) + A.glyph(gl, 78, 78, 100, P.paper);
  };
})(typeof window !== 'undefined' ? window : globalThis);
