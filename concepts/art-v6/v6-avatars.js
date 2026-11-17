/* v6 avatars and marks: scenic (a scene, optional calm panel), glyphAv (scene crop plus expressive shape plus glyph), mark (flat subject icon tile). */
(function (g) {
  'use strict';
  var A = g.NebArtV6, E = A.engines, f = A.f;
  var SH = ['cookie', 'flower', 'clover', 'burst', 'sunny', 'puffy', 'pebble', 'squircle', 'lotus', 'gem'];
  E.scenic = function (c) {
    var s = E[c.o.scene || 'bauhaus']({ w: c.w, h: c.h, P: c.P, r: c.r, uid: c.uid + 's', o: c.o, mode: c.mode, kind: c.kind });
    if (c.o.calm) s += A.calm(c.w, c.h, c.P, c.r, c.o.calmW || 0.36, c.P.t(0.04));
    return s;
  };
  E.glyphAv = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), sh = r.pick(SH), d = P.dark;
    var s = E[c.o.scene || 'bauhaus']({ w: w, h: h, P: P, r: r, uid: c.uid + 's', o: { deep: c.o.deep }, mode: c.mode, kind: c.kind });
    s += A.shape(sh, w / 2, h / 2, m * 0.37, r() * 3, P.q.t(d ? 0.3 : 0.46)) + A.shape(sh, w / 2, h / 2, m * 0.32, r() * 3 + 0.2, d ? P.t(0.2) : P.card);
    return s + A.glyph(c.o.glyph || 'school', w / 2 - m * 0.15, h / 2 - m * 0.15, m * 0.3, d ? P.t(0.8) : P.t(0.55));
  };
  E.mark = function (c) {
    var w = c.w, h = c.h, P = c.P, r = c.r, m = Math.min(w, h), d = P.dark, look = c.o.look || 0, s = A.rect(0, 0, w, h, 0, look === 1 ? P.t(d ? 0.18 : 0.8) : P.t(d ? 0.14 : 0.1)), sh = r.pick(SH), k;
    var body = look === 2 ? P.q.t(0.48) : look === 1 ? P.t(d ? 0.4 : 0.3) : P.t(0.52), ink = look === 1 ? P.t(d ? 0.84 : 0.1) : '#ffffff';
    s += A.shape(sh, w / 2, h / 2 + m * 0.03, m * 0.43, r() * 3, look === 3 ? P.t(0.22) : P.q.t(0.38)) + A.shape(sh, w / 2, h / 2, m * 0.4, r() * 3 + 0.3, look === 3 ? P.card : body);
    return s + A.glyph(c.o.glyph || 'school', w / 2 - m * 0.17, h / 2 - m * 0.17, m * 0.34, look === 3 ? P.t(0.55) : ink);
  };
})(typeof window !== 'undefined' ? window : globalThis);
