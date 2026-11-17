/* v3 make(): spec -> SVG string. spec = { engine, palette, seed, w, h, mode, subj, id } */
(function (g) {
  'use strict';
  var A = g.NebArtV3;
  A.make = function (s) {
    var w = s.w, h = s.h, mode = s.mode || 'light', P = A.palette(s.palette || 'brand', mode), key = (s.id || s.engine) + ':' + (s.seed || 0), r = A.rng(key);
    var uid = 'v' + (A.hash(key) % 100000), fn = A.engines[s.engine];
    if (!fn) throw new Error('unknown engine ' + s.engine);
    var body = fn({ w: w, h: h, P: P, r: r, uid: uid, subj: s.subj, o: s.o || {}, mode: mode, kind: s.kind });
    return A.svg(w, h, body, P.sky);
  };
})(typeof window !== 'undefined' ? window : globalThis);
