/* v4 people avatars: frameless 256 squares (clip to any shape, never ring). 10 hairstyles, 6 skin tones, 7 outfits, eyes, brows, glasses, topi, grad cap, headphones. */
(function (g) {
  'use strict';
  var A = g.NebArtV4, E = A.engines, f = A.f, C = A.circle, Pa = A.path, S = A.stroke, R = A.rect, mix = A.mix;
  var HAIR = ['#24160f', '#3b2416', '#5a3820', '#14141a', '#7a4222', '#b98a4e', '#8b8f96', '#2a1d2e'];
  function el(cx, cy, rx, ry, fill, ex) { return '<ellipse cx="' + cx + '" cy="' + cy + '" rx="' + rx + '" ry="' + ry + '" fill="' + fill + '"' + (ex ? ' ' + ex : '') + '/>'; }
  var HAIRS = {
    crop: [0, 'M82 114Q74 58 128 56Q182 58 174 114Q168 90 150 84Q128 94 104 84Q88 92 82 114Z'],
    buzz: [0, 'M85 106Q84 68 128 66Q172 68 171 106Q160 82 128 82Q96 82 85 106Z'],
    side: [0, 'M80 116Q72 56 130 54Q184 58 176 112Q172 86 140 80Q108 92 80 116Z'],
    bob: ['M78 126Q66 46 128 46Q190 46 178 126V176Q178 190 164 190H92Q78 190 78 176Z', 'M82 106Q92 62 128 62Q164 62 174 106Q150 82 128 90Q104 82 82 106Z'],
    long: ['M76 120Q66 44 128 44Q190 44 180 120L186 222H70Z', 'M80 112Q86 58 128 58Q172 58 176 112Q160 78 134 84Q104 84 80 112Z'],
    bun: ['', 'M82 114Q74 62 128 60Q182 62 174 114Q166 88 150 84Q128 94 104 84Q90 92 82 114Z'],
    braid: ['M80 124Q68 48 128 48Q188 48 176 124V150H80Z', 'M80 110Q86 58 128 58Q170 58 176 110Q158 80 132 84Q102 82 80 110Z'],
    wrap: ['M72 124Q66 40 128 40Q190 40 184 124Q188 176 128 206Q68 176 72 124Z', 'M80 108Q88 62 128 60Q168 62 176 108Q152 80 128 82Q104 80 80 108Z']
  };
  A.hairNames = Object.keys(HAIRS).concat(['curly', 'topi']);

  E.person = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, o = c.o, s = '', skin = o.skin != null ? P.skin[o.skin] : r.pick(P.skin), sd = mix(skin, '#401a08', 0.18), hair = mix(r.pick(HAIR), P.sky, P.dark ? 0.1 : 0), hs = o.hair || r.pick(A.hairNames), ink = '#24160f', k, i, cl, eyes = r.pick(['dot', 'dot', 'smile', 'wide', 'lash']), mouth = r.pick(['smile', 'open', 'smirk', 'calm', 'smile']), out = o.outfit || r.pick(['crew', 'hoodie', 'collar', 'daura', 'vneck', 'coat', 'crew']);
    var cl1 = r.chance(0.35) ? P.pop : P.t(r.range(0.38, 0.8)), cl2 = P.t(0.9), ac = r.pick(['none', 'none', 'glasses', 'sq', 'phones', 'bindi', 'ear']);
    if (hs === 'topi') ac = ac === 'phones' ? 'none' : ac;
    /* backdrop: tonal field and one expressive shape, no ring */
    s += A.rect(0, 0, 256, 256, 0, P.t(r.range(0.1, 0.24))) + A.shape(r.pick(A.shapeNames.filter(function (n) { return n !== 'circle'; })), r.range(100, 156), r.range(110, 150), r.range(104, 128), r() * 3, P.t(r.range(0.26, 0.4)));
    s += A.sparkle(r.range(26, 60), r.range(34, 90), r.range(8, 14), P.pop) + C(r.range(200, 232), r.range(40, 90), r.range(4, 7), P.t(0.6)) + A.plus(r.range(200, 230), r.range(190, 230), 6, 3, P.t(0.5));
    /* hair back */
    if (HAIRS[hs] && HAIRS[hs][0]) s += Pa(HAIRS[hs][0], hair);
    if (hs === 'curly') for (i = 0; i < 11; i++) s += C(128 + Math.cos(i / 11 * 6.28 - 1.57) * 50, 112 + Math.sin(i / 11 * 6.28 - 1.57) * 56, 21, hair);
    if (hs === 'bun') s += C(128, 46, 21, hair) + C(128, 56, 8, mix(hair, '#ffffff', 0.12));
    if (hs === 'braid') for (i = 0; i < 6; i++) s += el(176 - i * 1.5, 150 + i * 17, 11 - i * 0.6, 12, i % 2 ? hair : mix(hair, '#ffffff', 0.1));
    /* body */
    s += Pa('M112 160H144V198Q128 210 112 198Z', sd);
    s += Pa('M44 256Q44 204 96 192Q128 202 160 192Q212 204 212 256Z', cl1);
    if (out === 'hoodie') s += Pa('M92 194Q128 220 164 194Q168 186 160 184Q128 206 96 184Q88 186 92 194Z', mix(cl1, '#000000', 0.18)) + S('M116 210V236M140 210V236', 3.5, P.card);
    else if (out === 'collar') s += Pa('M128 204L104 190L100 214Z', P.card) + Pa('M128 204L152 190L156 214Z', P.card) + Pa('M122 208H134L137 256H119Z', cl2);
    else if (out === 'daura') s += Pa('M96 192Q128 206 160 192V200Q128 216 96 200Z', P.card) + S('M128 206L168 256', 4, P.card) + C(150, 232, 3.5, P.pop) + C(160, 244, 3.5, P.pop);
    else if (out === 'vneck') s += Pa('M100 192Q128 232 156 192Q128 204 100 192Z', sd) + Pa('M96 192L128 238L160 192', 'none', 'stroke="' + P.card + '" stroke-width="5" stroke-linejoin="round"');
    else if (out === 'coat') s += Pa('M50 256Q50 206 98 194L128 256Z', P.card) + Pa('M206 256Q206 206 158 194L128 256Z', P.card) + Pa('M110 200L128 256L146 200Q128 212 110 200Z', P.t(0.3)) + R(166, 222, 14, 5, 2, P.pop);
    else s += Pa('M100 194Q128 214 156 194Q128 204 100 194Z', mix(cl1, '#000000', 0.15));
    /* ears, head */
    s += C(84, 126, 10, skin) + C(172, 126, 10, skin) + C(85, 127, 4.5, sd) + C(171, 127, 4.5, sd) + el(128, 118, 45, 52, skin);
    s += el(128, 170, 24, 6, sd, 'opacity=".0"');
    /* hair front */
    if (HAIRS[hs]) s += Pa(HAIRS[hs][1], hs === 'wrap' ? cl1 : hair);
    if (hs === 'curly') for (i = 0; i < 4; i++) s += C(100 + i * 19, 74 + (i % 2) * 5, 17, hair);
    if (hs === 'topi') s += A.clip(c.uid + 't', 'M84 84L88 52Q128 38 168 52L172 84Q128 70 84 84Z', R(80, 30, 100, 60, 0, P.pop) + [0, 1, 2, 3, 4, 5].map(function (j) { return R(88 + j * 15, 30, 7, 60, 0, j % 2 ? P.t(0.85) : P.t(0.3)); }).join('')) + Pa('M80 90Q82 80 90 80H166Q174 80 176 90Q150 78 128 80Q104 78 80 90Z', hair);
    if (hs === 'topi') s += Pa('M82 98Q80 84 88 80L92 98Z', hair) + Pa('M174 98Q176 84 168 80L164 98Z', hair);
    /* face */
    cl = (hs === 'wrap' || hs === 'bob' || hs === 'long') ? hair : hair;
    [-1, 1].forEach(function (sd2) {
      var x = 128 + sd2 * 18, y = 124;
      if (eyes === 'dot' || eyes === 'lash') s += el(x, y, 5.4, 6.4, ink) + C(x + 1.8, y - 2, 1.9, '#ffffff') + (eyes === 'lash' ? S('M' + (x + sd2 * 5) + ' ' + (y - 4) + 'L' + (x + sd2 * 10) + ' ' + (y - 8), 2.5, ink) : '');
      else if (eyes === 'smile') s += S('M' + (x - 6) + ' ' + (y + 2) + 'Q' + x + ' ' + (y - 7) + ' ' + (x + 6) + ' ' + (y + 2), 3.6, ink);
      else s += el(x, y, 7.5, 8, '#ffffff') + el(x + 1, y + 1, 4.6, 5, ink) + C(x + 2.5, y - 1, 1.6, '#ffffff');
      s += S('M' + (x - 8) + ' ' + (y - 14 + sd2 * 0) + 'Q' + x + ' ' + (y - 20) + ' ' + (x + 8) + ' ' + (y - 14 - sd2 * 2), 3.2, hs === 'wrap' || hs === 'topi' ? mix(hair, skin, 0.1) : hair);
    });
    s += S('M123 134Q119 143 127 144', 2.8, sd) + C(102, 144, 8, '#ff6b6b', 'opacity=".22"') + C(154, 144, 8, '#ff6b6b', 'opacity=".22"');
    if (mouth === 'smile') s += S('M114 150Q128 163 142 150', 4, ink);
    else if (mouth === 'open') s += Pa('M113 148Q128 172 143 148Z', '#6e2430') + Pa('M120 160Q128 154 136 160Q128 166 120 160Z', '#f0808c') + Pa('M115 149H141Q128 156 115 149Z', '#ffffff');
    else if (mouth === 'smirk') s += S('M116 152Q130 158 143 147', 4, ink);
    else s += S('M118 152Q128 156 138 152', 4, ink);
    /* accessories */
    if (ac === 'glasses') s += C(110, 124, 14, 'none', 'stroke="' + ink + '" stroke-width="3.4"') + C(146, 124, 14, 'none', 'stroke="' + ink + '" stroke-width="3.4"') + S('M124 122Q128 119 132 122', 3, ink);
    if (ac === 'sq') s += R(95, 112, 30, 24, 8, 'none', 'stroke="' + P.pop + '" stroke-width="4"') + R(131, 112, 30, 24, 8, 'none', 'stroke="' + P.pop + '" stroke-width="4"') + S('M125 122H131', 4, P.pop);
    if (ac === 'phones') s += S('M80 118Q80 54 128 54Q176 54 176 118', 7, P.t(0.9)) + R(70, 108, 16, 36, 8, P.t(0.9)) + R(170, 108, 16, 36, 8, P.t(0.9)) + R(70, 112, 7, 28, 3.5, P.pop);
    if (ac === 'bindi') s += C(128, 96, 3.6, P.pop);
    if (ac === 'ear') s += C(83, 142, 4.5, P.pop) + C(173, 142, 4.5, P.pop);
    if (hs === 'grad' || o.grad) s += Pa('M128 48L196 74L128 100L60 74Z', P.t(0.9)) + R(112, 90, 32, 12, 4, P.t(0.9)) + S('M186 78V112', 3, P.pop) + C(186, 114, 4.5, P.pop);
    return s;
  };
})(typeof window !== 'undefined' ? window : globalThis);
