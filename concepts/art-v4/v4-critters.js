/* v4 buddies, critters and glyph tiles: frameless 256 squares. */
(function (g) {
  'use strict';
  var A = g.NebArtV4, E = A.engines, f = A.f, C = A.circle, Pa = A.path, S = A.stroke, R = A.rect, mix = A.mix;
  function el(cx, cy, rx, ry, fill, ex) { return '<ellipse cx="' + cx + '" cy="' + cy + '" rx="' + rx + '" ry="' + ry + '" fill="' + fill + '"' + (ex ? ' ' + ex : '') + '/>'; }
  var FACE_SH = ['cookie', 'flower', 'clover', 'burst', 'sunny', 'puffy', 'pebble', 'squircle', 'lotus'];
  function back(c) {
    var P = c.P, r = c.r;
    return A.rect(0, 0, 256, 256, 0, P.t(r.range(0.1, 0.24))) + A.shape(r.pick(['cookie', 'pebble', 'flower', 'puffy', 'sunny']), r.range(110, 150), r.range(116, 146), r.range(108, 128), r() * 3, P.t(r.range(0.26, 0.4))) + A.sparkle(r.range(28, 62), r.range(34, 84), r.range(8, 13), P.pop) + C(r.range(204, 230), r.range(40, 86), r.range(4, 7), P.t(0.6));
  }
  function eyes(r, P, y, dx, ink) {
    var t = r.pick(['dot', 'wide', 'happy', 'sleepy']), s = '';
    [-1, 1].forEach(function (d) { var x = 128 + d * dx;
      if (t === 'dot') s += el(x, y, 7, 9, ink) + C(x + 2.5, y - 3, 2.6, '#fff');
      else if (t === 'wide') s += C(x, y, 13, '#fff') + C(x + d * 2, y + 1, 7.5, ink) + C(x + d * 2 + 2.5, y - 2, 2.4, '#fff');
      else if (t === 'happy') s += S('M' + (x - 9) + ' ' + (y + 4) + 'Q' + x + ' ' + (y - 11) + ' ' + (x + 9) + ' ' + (y + 4), 5, ink);
      else s += S('M' + (x - 9) + ' ' + (y - 2) + 'Q' + x + ' ' + (y + 9) + ' ' + (x + 9) + ' ' + (y - 2), 5, ink); });
    return s;
  }
  function mouth(r, y, ink) {
    var t = r.pick(['smile', 'open', 'cat', 'o']);
    return t === 'smile' ? S('M110 ' + y + 'Q128 ' + (y + 18) + ' 146 ' + y, 5, ink) : t === 'open' ? Pa('M108 ' + y + 'Q128 ' + (y + 34) + ' 148 ' + y + 'Z', '#6e2430') + Pa('M118 ' + (y + 15) + 'Q128 ' + (y + 6) + ' 138 ' + (y + 15) + 'Q128 ' + (y + 24) + ' 118 ' + (y + 15) + 'Z', '#f0808c') : t === 'cat' ? S('M112 ' + (y + 2) + 'Q120 ' + (y + 12) + ' 128 ' + (y + 2) + 'Q136 ' + (y + 12) + ' 144 ' + (y + 2), 4.5, ink) : el(128, y + 8, 7, 9, '#6e2430');
  }
  var INK = '#241615';
  E.buddy = function (c) {
    var P = c.P, r = c.r, s = back(c), R0 = r.range(78, 92), body = r.chance(0.3) ? P.pop : P.t(r.range(0.4, 0.72)), sh = r.pick(FACE_SH), ac = r.int(0, 4);
    s += A.shape(sh, 128, 140, R0, r() * 0.8, body) + A.shape(sh, 128, 140, R0 * 0.78, 0.4, mix(body, '#ffffff', 0.12));
    s += eyes(r, P, 128, 28, INK) + mouth(r, 160, INK) + C(88, 152, 9, '#ff6b6b', 'opacity=".25"') + C(168, 152, 9, '#ff6b6b', 'opacity=".25"');
    if (ac === 0) s += S('M128 62V38', 5, P.t(0.8)) + A.shape('flower', 128, 32, 14, 0, P.pop);
    else if (ac === 1) s += Pa('M128 64Q104 50 108 28Q130 30 128 64Z', P.t(0.8)) + Pa('M128 64Q152 50 148 28Q126 30 128 64Z', P.t(0.55));
    else if (ac === 2) s += S('M100 62L90 36M156 62L166 36', 5, P.t(0.85)) + C(90, 34, 8, P.pop) + C(166, 34, 8, P.pop);
    else if (ac === 3) s += A.sparkle(128, 50, 16, P.snow);
    return s;
  };
  var CR = {
    cat: function (P, r, fur, lt, dk) { return Pa('M62 112L70 52Q74 44 82 50L112 82Z', fur) + Pa('M194 112L186 52Q182 44 174 50L144 82Z', fur) + Pa('M76 100L78 66L100 86Z', P.popSoft) + Pa('M180 100L178 66L156 86Z', P.popSoft) + el(128, 138, 70, 62, fur) + Pa('M122 144H134L128 152Z', P.pop) + S('M60 140L92 144M60 156L92 152M196 140L164 144M196 156L164 152', 3, lt); },
    bear: function (P, r, fur, lt, dk) { return C(78, 74, 24, fur) + C(178, 74, 24, fur) + C(78, 74, 12, lt) + C(178, 74, 12, lt) + el(128, 138, 70, 64, fur) + el(128, 156, 28, 22, lt) + el(128, 148, 9, 6.5, dk); },
    bunny: function (P, r, fur, lt, dk) { return el(98, 54, 17, 52, fur) + el(158, 54, 17, 52, fur) + el(98, 58, 8, 38, P.popSoft) + el(158, 58, 8, 38, P.popSoft) + el(128, 144, 66, 58, fur) + el(128, 160, 22, 16, lt) + el(128, 150, 8, 6, P.pop); },
    fox: function (P, r, fur, lt, dk) { return Pa('M64 118L66 48L112 86Z', fur) + Pa('M192 118L190 48L144 86Z', fur) + Pa('M70 76L68 52L88 66Z', dk) + Pa('M186 76L188 52L168 66Z', dk) + Pa('M60 122Q128 70 196 122Q196 190 128 206Q60 190 60 122Z', fur) + Pa('M60 128Q100 134 128 176Q156 134 196 128Q196 190 128 206Q60 190 60 128Z', lt) + el(128, 168, 9, 7, dk); },
    owl: function (P, r, fur, lt, dk) { return Pa('M70 104L62 56L106 78Z', fur) + Pa('M186 104L194 56L150 78Z', fur) + el(128, 140, 68, 72, fur) + el(128, 168, 40, 36, lt) + C(100, 126, 24, lt) + C(156, 126, 24, lt) + Pa('M120 138H136L128 154Z', P.pop); },
    panda: function (P, r, fur, lt, dk) { return C(76, 74, 22, dk) + C(180, 74, 22, dk) + el(128, 138, 70, 64, '#ffffff') + el(98, 130, 17, 22, dk, 'transform="rotate(20 98 130)"') + el(158, 130, 17, 22, dk, 'transform="rotate(-20 158 130)"') + el(128, 154, 9, 7, dk); }
  };
  A.critterNames = Object.keys(CR);
  E.critter = function (c) {
    var P = c.P, r = c.r, k = c.o.critter || r.pick(A.critterNames), fur = k === 'panda' ? '#ffffff' : r.chance(0.3) ? P.popSoft : P.t(r.range(0.45, 0.7)), lt = P.t(0.08), dk = P.t(0.9), s = back(c), y = k === 'owl' ? 126 : 130, dx = 26;
    s += CR[k](P, r, k === 'owl' ? P.t(0.55) : fur, lt, dk);
    if (k === 'owl') s += C(100, 126, 11, INK) + C(156, 126, 11, INK) + C(103, 122, 3.5, '#fff') + C(159, 122, 3.5, '#fff');
    else s += eyes(r, P, y, dx, k === 'panda' ? '#ffffff' : INK) + (k === 'bear' || k === 'bunny' || k === 'fox' || k === 'panda' ? '' : mouth(r, 164, INK));
    if (k === 'bear' || k === 'bunny') s += S('M128 154V162Q120 172 112 166M128 162Q136 172 144 166', 4, INK);
    if (k === 'fox' || k === 'panda') s += S('M128 176Q118 186 110 178M128 176Q138 186 146 178', 4, INK);
    s += C(88, 152, 8, '#ff6b6b', 'opacity=".22"') + C(168, 152, 8, '#ff6b6b', 'opacity=".22"');
    return s;
  };
  E.glyphTile = function (c) {
    var P = c.P, r = c.r, o = c.o, s = A.rect(0, 0, 256, 256, 0, P.t(r.range(0.1, 0.22)));
    s += A.shape(r.pick(FACE_SH), 128, 128, 112, r() * 3, P.t(r.range(0.28, 0.45))) + A.shape(r.pick(['cookie', 'flower', 'squircle', 'pebble']), 128, 128, 80, r() * 3, r.chance(0.3) ? P.pop : P.t(0.62));
    return s + A.glyph(o.glyph || 'school', 78, 78, 100, P.card) + A.sparkle(r.range(30, 60), r.range(36, 70), 11, P.pop) + C(r.range(200, 226), r.range(190, 220), 5, P.t(0.6));
  };
})(typeof window !== 'undefined' ? window : globalThis);
