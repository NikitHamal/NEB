/* The named set: every piece in the gallery and in the exported SVG folders comes from here.
   Same entries in, same drawings out. Ids are stable: kind-001, kind-002 ... */
(function (g) {
  var N = g.NebArt, SUBS = N.subjectNames, PAL = N.palettes, GL = Object.keys(g.NebGlyphs || {});
  var pad = function (n) { return ('00' + n).slice(-3); };
  var LAY = N.layoutNames;

  N.catalog = function () {
    var out = [], i, j, id = {};
    function add(kind, o) { id[kind] = (id[kind] || 0) + 1; o.kind = kind; o.id = kind + '-' + pad(id[kind]); o.group = o.group || N.kinds[kind].label; out.push(o); }
    for (i = 0; i < LAY.length; i++) for (j = 0; j < PAL.length; j++) add('cover', { seed: i * 31 + j, layout: LAY[i], palette: PAL[j], tag: LAY[i] });
    for (i = 0; i < 48; i++) add('school', { seed: 500 + i, palette: PAL[(i * 5) % PAL.length], tag: PAL[(i * 5) % PAL.length] });
    for (i = 0; i < SUBS.length; i++) for (j = 0; j < 8; j++) add('thumb', { seed: i * 8 + j, subject: SUBS[i], tag: SUBS[i] });
    for (i = 0; i < SUBS.length; i++) for (j = 0; j < 3; j++) add('book', { seed: 900 + i * 3 + j, subject: SUBS[i], tag: SUBS[i] });
    for (i = 0; i < 36; i++) add('post', { seed: 1300 + i, palette: PAL[i % PAL.length], tag: PAL[i % PAL.length] });
    for (i = 0; i < 48; i++) add('bg', { seed: 1700 + i, palette: PAL[(i * 7) % PAL.length], tag: PAL[(i * 7) % PAL.length] });
    for (i = 0; i < 36; i++) add('tile', { seed: 2100 + i, subject: SUBS[i % SUBS.length], palette: PAL[(i * 5 + 3) % PAL.length], tag: SUBS[i % SUBS.length] });
    for (i = 0; i < GL.length; i++) add('sticker', { seed: 2500 + i, glyph: GL[i], palette: PAL[i % PAL.length], tag: GL[i] });
    return out;
  };
  N.render = function (o, mode) { var c = {}; for (var k in o) c[k] = o[k]; c.mode = mode || 'light'; return N.make(c); };
})(typeof window !== 'undefined' ? window : globalThis);
