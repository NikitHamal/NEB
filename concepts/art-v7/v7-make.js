/* v7 kinds, subjects, motifs and make(). Book covers have no text card and no bubble shapes: spine, medallion, bookmark ribbon. */
(function (g) {
  var N = g.NebArt, f1 = N.f1, ALL = N.layoutNames.slice();
  var CALM = ['orbit', 'waves', 'petals', 'stack', 'ribbons', 'folds', 'pinwheel', 'ripple', 'venn', 'contour', 'blobs', 'rings', 'bands', 'swirl', 'capsules', 'cascade', 'bento', 'segments', 'arches'];
  var WIDE = ['waves', 'contour', 'ribbons', 'capsules', 'bands', 'dots', 'folds', 'bauhaus', 'diamonds', 'truchet', 'mosaic', 'stack', 'halftone', 'petalfield'];
  var pick = function (a, b) { return a.filter(function (x) { return ALL.indexOf(x) > -1; }); };
  N.kinds = {
    cover:   { w: 1200, h: 400, label: 'Profile cover', layouts: ALL, motif: 'none' },
    school:  { w: 1200, h: 400, label: 'School banner', layouts: ['arches', 'tiles', 'folds', 'bauhaus', 'mosaic', 'petals', 'bento', 'diamonds', 'mondrian', 'bands', 'truchet', 'pinwheel'], motif: 'none' },
    thumb:   { w: 640, h: 256, label: 'Resource thumbnail', layouts: ALL, motif: 'tile' },
    book:    { w: 400, h: 560, label: 'Book cover', layouts: ['stack', 'arches', 'petals', 'orbit', 'tiles', 'folds', 'ribbons', 'mosaic', 'bars', 'pinwheel', 'bands', 'rings', 'segments', 'bento', 'ripple', 'venn'], motif: 'book' },
    note:    { w: 720, h: 320, label: 'Note cover', layouts: CALM, motif: 'none' },
    empty:   { w: 480, h: 360, label: 'Empty state', layouts: [], motif: 'empty' },
    avatar:  { w: 512, h: 512, label: 'Profile picture', layouts: [], motif: 'avatar' },
    post:    { w: 1200, h: 630, label: 'Post header', layouts: ALL, motif: 'none' },
    bg:      { w: 1600, h: 900, label: 'Background', layouts: ['waves', 'dots', 'scatter', 'ribbons', 'folds', 'mosaic', 'arches', 'contour', 'blobs', 'halftone', 'petalfield', 'bands', 'ripple', 'diamonds', 'truchet'], motif: 'none' },
    wall:    { w: 540, h: 1170, label: 'Phone wallpaper', layouts: ['waves', 'contour', 'ribbons', 'blobs', 'bands', 'folds', 'ripple', 'rings', 'capsules', 'petalfield', 'halftone', 'swirl', 'cascade', 'orbit'], motif: 'none' },
    story:   { w: 540, h: 960, label: 'Story', layouts: CALM, motif: 'none' },
    strip:   { w: 1200, h: 180, label: 'Divider strip', layouts: WIDE, motif: 'none' },
    tile:    { w: 512, h: 512, label: 'Collection tile', layouts: ALL, motif: 'center' },
    icon:    { w: 256, h: 256, label: 'Subject icon', layouts: [], motif: 'icon' },
    sticker: { w: 256, h: 256, label: 'Achievement', layouts: [], motif: 'sticker' }
  };
  var S1 = N.subjects, SUB = {}, BAN = { hills: 1, sunset: 1, rays: 1 }, k;
  for (k in S1) SUB[k] = [S1[k][0], S1[k][1], S1[k][2].filter(function (x) { return !BAN[x]; }).concat(['contour', 'blobs', 'rings'].slice(0, 2))];
  SUB['Agriculture'][0] = 'agriculture';
  var ADD = { 'Nursing': ['stethoscope', 'rose'], 'Design': ['brush', 'coral'], 'Philosophy': ['self_improvement', 'slate'], 'Languages': ['translate', 'sky'], 'Data Science': ['query_stats', 'ocean'], 'Public Policy': ['policy', 'clay'], 'Public Speaking': ['record_voice_over', 'citrine'], 'Robotics': ['memory', 'cherry'] };
  for (k in ADD) SUB[k] = [ADD[k][0], ADD[k][1], ['pinwheel', 'capsules', 'bento', 'segments', 'ripple', 'contour']];
  N.subjects = SUB; N.subjectNames = Object.keys(SUB);
  N.glyphFor = function (name) { var s = SUB[name]; return s ? s[0] : 'school'; };

  function glyph(name, x, y, s, fill) {
    var d = (g.NebGlyphs || {})[name]; if (!d) return '';
    return '<path transform="translate(' + f1(x) + ' ' + f1(y + s) + ') scale(' + (s / 960).toFixed(4) + ')" d="' + d + '" fill="' + fill + '"/>';
  }
  N.glyph = glyph;
  var P4 = ['squircle', 'cookie', 'sunny', 'flower'];
  function plate(c, cx, cy, r, T, gl, fillA, fillG, k) {
    return N.shape(k || c.pick(P4), cx, cy, r, c.r() * 6, fillA) + glyph(gl, cx - r * 0.52, cy - r * 0.52, r * 1.04, fillG);
  }

  function motif(o, c, T) {
    var W = c.W, H = c.H, gl = o.glyph || N.glyphFor(o.subject), m = o.motif || N.kinds[o.kind].motif, r, out = '', k = c.pick(P4);
    if (m === 'tile') { r = H * 0.3; out = plate(c, W * 0.8, H * 0.5, r, T, gl, T[4], T[0], k); }
    else if (m === 'center') { r = W * 0.24; out = plate(c, W / 2, H / 2, r, T, gl, T[4], T[0], k); }
    else if (m === 'icon') {
      r = W * 0.34; out = N.shape(c.pick(['cookie', 'flower', 'burst', 'sunny']), W / 2, H / 2, r * 1.28, c.r() * 6, T[1]) + plate(c, W / 2, H / 2, r, T, gl, T[4], T[0], k) + N.circle(W * 0.84, H * 0.2, W * 0.05, T[5]);
    } else if (m === 'book') {
      r = W * 0.19; var cy = H * 0.42, bx = W * 0.82;
      out = N.rect(0, 0, W * 0.07, H, 0, T[4]) + N.rect(W * 0.07, 0, W * 0.012, H, 0, T[2]);
      out += N.shape(c.pick(['cookie', 'flower', 'sunny', 'burst']), W * 0.54, cy, r * 1.34, c.r() * 6, T[1]) + plate(c, W * 0.54, cy, r, T, gl, T[4], T[0], k);
      out += '<path d="M' + f1(bx) + ' 0V' + f1(H * 0.2) + 'L' + f1(bx + W * 0.05) + ' ' + f1(H * 0.16) + 'L' + f1(bx + W * 0.1) + ' ' + f1(H * 0.2) + 'V0Z" fill="' + T[5] + '"/>';
    } else if (m === 'empty') out = N.empty(o, c, T, gl);
    else if (m === 'avatar') out = N.avatar(o, c, T, gl);
    return out;
  }

  function sticker(c, T, o) {
    var k1 = c.pick(['burst', 'flower', 'cookie', 'sunny', 'clover']), k2 = c.pick(['squircle', 'cookie', 'pebble']), gl = o.glyph || N.glyphFor(o.subject), out = '';
    out += N.shape(k1, 128, 128, 120, c.r() * 6, T[2]) + N.shape(k2, 128, 128, 84, c.r() * 6, T[4]) + glyph(gl, 128 - 44, 128 - 44, 88, T[0]);
    return out + N.circle(206, 52, 14, T[5]) + N.circle(46, 206, 8, T[3]);
  }

  /* make({kind, seed, mode, layout, palette, subject, glyph, variant}) -> SVG string. Same input, same drawing. */
  N.make = function (o) {
    o = o || {}; o.kind = o.kind || 'cover'; o.mode = o.mode || 'light'; o.seed = o.seed === undefined ? 1 : o.seed;
    var K = N.kinds[o.kind], sub = SUB[o.subject], r = N.rng(o.kind + '|' + o.seed + '|' + (o.subject || '') + '|' + (o.layout || '') + '|' + (o.variant || ''));
    var pal = o.palette || (sub ? sub[1] : N.palettes[Math.floor(r() * N.palettes.length)]);
    var T = N.palette(pal, o.mode), pool = (sub && K.layouts.length > 4) ? sub[2].filter(function (x) { return K.layouts.indexOf(x) > -1; }) : K.layouts;
    if (!pool.length) pool = K.layouts;
    var layout = o.layout || (pool.length ? pool[Math.floor(r() * pool.length)] : '');
    var c = { W: K.w, H: K.h, u: Math.min(K.w, K.h), r: r, T: T, rr: function (a, b) { return a + (b - a) * r(); }, pick: function (a) { return a[Math.floor(r() * a.length)]; }, o: o };
    var body = o.kind === 'sticker' ? sticker(c, T, o) : (layout ? N.layouts[layout](c) : '') + motif(o, c, T);
    o.resolved = { layout: layout, palette: pal };
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + K.w + ' ' + K.h + '" width="' + K.w + '" height="' + K.h + '" preserveAspectRatio="xMidYMid slice" role="img"><title>' + (o.title || K.label) + '</title><rect width="' + K.w + '" height="' + K.h + '" fill="' + T[0] + '"/>' + body + '</svg>';
  };
  N.uri = function (o) { return 'data:image/svg+xml;utf8,' + encodeURIComponent(N.make(o)); };
})(typeof window !== 'undefined' ? window : globalThis);
