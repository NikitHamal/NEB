/* v6 people: refined flat portraits in a 256 box. Frameless; clip to any expressive shape, never ring. Hair back and front layers, ears, neck shade, brows,
   nose, blush, eight outfits (hoodie, tee, shirt and tie, lab coat, daura collar, blazer, kurta trim, uniform), glasses, headphones, topi, grad cap, hijab, bindi. */
(function (g) {
  'use strict';
  var A = g.NebArtV6, E = A.engines, f = A.f, sin = Math.sin, cos = Math.cos, PI = Math.PI;
  var HAIR = ['#1b1411', '#2e1d14', '#4a2c1b', '#74482a', '#a8743a', '#cfa75e', '#8c8c94', '#a4402c'], STY = ['crop', 'side', 'curly', 'buzz', 'bob', 'long', 'bun', 'puff', 'braid', 'topknot'];
  var D = {
    crop: 'M82 118C74 66 112 46 134 50C168 54 182 90 174 120C170 100 160 88 140 86C118 84 96 92 82 118Z', side: 'M80 122C70 62 118 44 142 50C176 58 184 96 174 126C172 100 152 82 118 92C100 98 86 108 80 122Z',
    buzz: 'M86 112C84 78 106 62 128 62C150 62 172 78 170 112C160 92 148 86 128 86C108 86 96 92 86 112Z', bobB: 'M70 122C66 60 100 44 128 44C156 44 190 60 186 120L186 160Q186 172 174 172L82 172Q70 172 70 160Z',
    bobF: 'M84 104C90 78 110 68 128 68C148 68 168 78 172 104C150 90 108 90 84 104Z', longB: 'M68 122C64 56 100 42 128 42C156 42 192 56 188 122L194 204Q194 214 180 214L76 214Q62 214 62 204Z',
    longL: 'M128 52C98 56 84 86 84 124C92 98 108 86 128 86Z', longR: 'M128 52C158 56 172 86 172 124C164 98 148 86 128 86Z', hijab: 'M64 150C58 62 100 38 128 38C156 38 198 62 192 150C194 196 182 236 128 246C74 236 62 196 64 150Z'
  };
  function sc(P) { return [P.t(0.5), P.q.t(0.5), P.t(0.72), P.q.t(0.36), P.t(0.34)]; }
  E.person5 = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, dk = P.dark, s = '', k, sk = r.pick(P.skin), skd = A.mix(sk, '#4a2208', 0.2), hc = r.pick(HAIR), hl = A.mix(hc, '#ffffff', 0.18), st = r.pick(STY), oc = r.pick(sc(P)), ocd = A.mix(oc, '#0a1220', 0.22), ink = '#1a1411', fw = r.range(0.93, 1.06);
    var out = r.int(0, 7), acc = r.pick(['none', 'none', 'glasses', 'glasses', 'sq', 'phones', 'topi', 'grad', 'hijab', 'none']), bg = r.chance(0.3) ? (dk ? P.t(0.16) : P.t(0.82)) : P.t(dk ? 0.14 : 0.13), hij = acc === 'hijab', cap = acc === 'topi' || acc === 'grad';
    s += A.rect(0, 0, 256, 256, 0, bg) + A.shape(r.pick(['pebble', 'flower', 'cookie', 'clover', 'squircle', 'puffy']), 128 + r.range(-8, 8), 140, 118, r() * 3, bg === P.t(dk ? 0.14 : 0.13) ? P.t(0.22) : (dk ? P.t(0.26) : P.t(0.7)));
    /* back hair */
    if (hij) s += A.path(D.hijab, oc, '') + A.path(D.hijab, ocd, 'opacity=".25" transform="translate(6 4)"');
    else if (st === 'bob') s += A.path(D.bobB, hc); else if (st === 'long') s += A.path(D.longB, hc);
    else if (st === 'puff') s += A.circle(128, 84, 62, hc) + A.circle(88, 112, 22, hc) + A.circle(168, 112, 22, hc);
    else if (st === 'bun') s += A.circle(128, 40, 26, hc) + A.circle(120, 34, 8, hl, 'opacity=".5"');
    else if (st === 'topknot') s += A.circle(128, 46, 17, hc);
    else if (st === 'braid') for (k = -1; k <= 1; k += 2) for (var q = 0; q < 4; q++) s += A.circle(128 + k * (62 - q * 2), 150 + q * 22, 13 - q, q % 2 ? hl : hc);
    /* torso, neck */
    var tor = 'M26 256Q26 196 84 182L172 182Q230 196 230 256Z', cl = out === 3 ? (dk ? '#dfe6f1' : '#ffffff') : out === 5 ? P.t(dk ? 0.3 : 0.8) : oc;
    if (out === 1) s += A.path('M88 174Q128 152 168 174Q184 196 178 212L78 212Q72 196 88 174Z', ocd);
    s += A.path(tor, cl) + A.rect(110, 150, 36, 44, 14, skd);
    if (out === 0 || out === 6 || out === 4) s += A.path('M104 182Q128 214 152 182L146 180L110 180Z', skd) + A.path('M106 182Q128 208 150 182Z', skd);
    if (out === 0) s += A.stroke('M104 182Q128 212 152 182', 5, ocd);
    if (out === 1) s += A.path('M104 182Q128 206 152 182Z', skd) + A.line(116, 200, 114, 232, 4, '#fff') + A.line(140, 200, 142, 232, 4, '#fff');
    if (out === 2) s += A.path('M104 180L128 206L110 218L94 192Z', '#fff') + A.path('M152 180L128 206L146 218L162 192Z', '#fff') + A.path('M122 206H134L139 246L128 254L117 246Z', P.q.t(0.45));
    if (out === 3) s += A.path('M104 180L128 238L96 256L80 204Z', '#fff', 'stroke="' + P.line + '" stroke-width="2"') + A.path('M152 180L128 238L160 256L176 204Z', '#fff', 'stroke="' + P.line + '" stroke-width="2"') + A.path('M106 180L128 232L150 180Z', P.t(0.5)) + A.rect(176, 214, 22, 6, 3, P.q.t(0.45));
    if (out === 4) s += A.rect(108, 170, 40, 16, 8, ocd) + A.line(128, 196, 96, 256, 3, ocd) + [0, 1, 2].map(function (i) { return A.circle(122 - i * 8, 204 + i * 15, 3.4, '#fff'); }).join('');
    if (out === 5) s += A.path('M106 180L128 226L150 180Z', '#fff') + A.path('M104 180L128 232L92 256L76 204Z', A.mix(cl, '#ffffff', 0.12)) + A.path('M152 180L128 232L164 256L180 204Z', A.mix(cl, '#ffffff', 0.12));
    if (out === 6) s += A.stroke('M102 184Q128 218 154 184', 7, P.q.t(0.5)) + [-1, 0, 1].map(function (i) { return A.circle(128 + i * 14, 212 - Math.abs(i) * 6, 3, P.q.t(0.75)); }).join('');
    if (out === 7) s += A.rect(26, 226, 204, 10, 0, '#ffffff', 'opacity=".55"') + A.rect(26, 242, 204, 6, 0, P.q.t(0.5), 'opacity=".8"') + A.path('M104 182Q128 206 152 182Z', skd);
    /* head, ears */
    var hd = 'M128 66C160 66 172 92 172 118C172 150 152 176 128 176C104 176 84 150 84 118C84 92 96 66 128 66Z', tf = 'transform="translate(128 0) scale(' + f(fw) + ' 1) translate(-128 0)"';
    if (!hij) s += A.circle(83, 124, 11, sk, tf) + A.circle(173, 124, 11, sk, tf) + A.circle(83, 124, 5, skd, 'opacity=".5" ' + tf) + A.circle(173, 124, 5, skd, 'opacity=".5" ' + tf);
    s += A.path(hd, sk, tf) + A.path('M92 150Q128 190 164 150Q150 176 128 176Q106 176 92 150Z', skd, 'opacity=".28" ' + tf);
    /* face */
    var lip = A.mix(sk, '#7a1f2a', 0.55), ec = r.pick(['dot', 'dot', 'glad', 'wide']);
    s += A.circle(100, 144, 8, P.q.t(0.3), 'opacity=".55"') + A.circle(156, 144, 8, P.q.t(0.3), 'opacity=".55"');
    [108, 148].forEach(function (x, i) {
      s += ec === 'glad' ? A.stroke('M' + (x - 7) + ' 128Q' + x + ' 116 ' + (x + 7) + ' 128', 3.6, ink) : ec === 'wide' ? A.circle(x, 124, 8.5, '#fff') + A.circle(x + 0.8, 125, 5.4, ink) + A.circle(x + 2.6, 122.6, 1.9, '#fff') : A.circle(x, 124, 6, ink) + A.circle(x + 2, 122, 2, '#fff');
      s += A.stroke('M' + (x - 9) + ' ' + (108 + (i ? 1 : 0)) + 'Q' + x + ' ' + (102 + r.int(-2, 2)) + ' ' + (x + 9) + ' ' + (108 + (i ? 0 : 1)), 3.4, hc === '#cfa75e' ? '#7b5a2a' : hc);
    });
    s += A.stroke('M126 132Q122 142 128 144', 2.6, A.mix(sk, '#4a2208', 0.45));
    var mo = r.int(0, 3);
    s += mo === 0 ? A.stroke('M112 156Q128 168 144 156', 3.6, lip) : mo === 1 ? A.path('M110 154H146Q146 172 128 172Q110 172 110 154Z', '#5b1f27') + A.rect(114, 154, 28, 6, 3, '#fff') : mo === 2 ? A.stroke('M114 158Q130 164 144 154', 3.4, lip) : A.stroke('M116 158Q128 164 140 158', 3.6, lip);
    if (acc === 'none' && r.chance(0.5)) s += A.circle(128, 96, 3.2, '#d23b3b');
    /* front hair, caps */
    if (!hij && !cap) {
      if (st === 'crop' || st === 'bun' || st === 'braid') s += A.path(D.crop, hc, tf) + A.stroke('M100 84Q120 74 146 78', 4, hl, 'opacity=".55"');
      else if (st === 'side') s += A.path(D.side, hc, tf) + A.stroke('M104 84Q128 70 152 78', 4, hl, 'opacity=".55"');
      else if (st === 'buzz' || st === 'topknot') s += A.path(D.buzz, hc, tf);
      else if (st === 'bob') s += A.path(D.bobF, hc, tf); else if (st === 'long') s += A.path(D.longL, hc, tf) + A.path(D.longR, hc, tf);
      else if (st === 'puff') s += A.path(D.buzz, hc, tf); else if (st === 'curly') { s += A.path(D.crop, hc, tf); for (k = 0; k < 8; k++) s += A.circle(128 + 56 * cos(PI + k / 7 * PI), 98 + 50 * sin(PI + k / 7 * PI), 17, hc, tf); }
    } else if (hij) s += A.path(D.bobF, oc, tf) + A.path('M84 104C90 78 110 68 128 68C148 68 168 78 172 104C150 90 108 90 84 104Z', ocd, 'opacity=".2" ' + tf);
    if (acc === 'topi') s += A.path('M80 98L88 58Q128 36 168 58L176 98Q128 82 80 98Z', P.q.t(0.5), tf) + [0, 1, 2, 3, 4].map(function (i) { return A.poly([[92 + i * 15, 94], [100 + i * 15, 70], [108 + i * 15, 94]], P.q.t(0.78), 'opacity=".7"'); }).join('');
    if (acc === 'grad') s += A.rect(96, 62, 64, 18, 8, '#1f2937') + A.poly([[128, 38], [200, 64], [128, 86], [56, 64]], '#273449') + A.stroke('M190 68L190 100', 3, P.q.t(0.5)) + A.circle(190, 102, 5, P.q.t(0.5));
    if (acc === 'glasses') s += A.circle(108, 126, 17, 'none', 'stroke="' + ink + '" stroke-width="3.4"') + A.circle(148, 126, 17, 'none', 'stroke="' + ink + '" stroke-width="3.4"') + A.line(124, 124, 132, 124, 3.4, ink);
    if (acc === 'sq') s += A.rect(88, 112, 36, 28, 9, 'none', 'stroke="' + P.q.t(0.45) + '" stroke-width="4"') + A.rect(132, 112, 36, 28, 9, 'none', 'stroke="' + P.q.t(0.45) + '" stroke-width="4"') + A.line(124, 124, 132, 124, 4, P.q.t(0.45));
    if (acc === 'phones') s += A.stroke('M78 126Q74 56 128 54Q182 56 178 126', 8, P.t(0.78)) + A.rect(66, 112, 20, 38, 9, P.q.t(0.5)) + A.rect(170, 112, 20, 38, 9, P.q.t(0.5));
    return s;
  };
})(typeof window !== 'undefined' ? window : globalThis);
