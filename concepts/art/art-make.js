/* NEBians M3X art engine: kinds, subjects, motifs and the make() entry point. */
(function (g) {
  var N = g.NebArt, f1 = N.f1;
  var ALL = ['orbit', 'bauhaus', 'waves', 'hills', 'rays', 'scatter', 'dots', 'petals', 'stack', 'net', 'graph', 'arches', 'mosaic', 'ribbons', 'bars', 'sunset', 'folds', 'tiles'];

  N.kinds = {
    cover:   { w: 1200, h: 400, label: 'Profile cover', layouts: ALL, motif: 'none' },
    school:  { w: 1200, h: 400, label: 'School banner', layouts: ['arches', 'hills', 'tiles', 'sunset', 'folds', 'bauhaus', 'mosaic', 'petals'], motif: 'none' },
    thumb:   { w: 640, h: 256, label: 'Resource thumbnail', layouts: ALL, motif: 'tile' },
    book:    { w: 400, h: 560, label: 'Book cover', layouts: ['stack', 'arches', 'petals', 'orbit', 'tiles', 'folds', 'ribbons', 'mosaic', 'scatter', 'bars'], motif: 'book' },
    post:    { w: 1200, h: 630, label: 'Post header', layouts: ALL, motif: 'none' },
    bg:      { w: 1600, h: 900, label: 'Background', layouts: ['waves', 'hills', 'dots', 'scatter', 'ribbons', 'folds', 'mosaic', 'rays', 'sunset', 'arches'], motif: 'none' },
    tile:    { w: 512, h: 512, label: 'Collection tile', layouts: ALL, motif: 'center' },
    sticker: { w: 256, h: 256, label: 'Achievement', layouts: [], motif: 'sticker' }
  };

  /* name: [glyph, palette, preferred layouts] */
  var SUB = {
    'Physics': ['bolt', 'azure', ['orbit', 'rays', 'graph', 'net']],
    'Chemistry': ['science', 'aqua', ['scatter', 'dots', 'bauhaus', 'mosaic']],
    'Biology': ['genetics', 'mint', ['petals', 'mosaic', 'net', 'scatter']],
    'Mathematics': ['functions', 'periwinkle', ['graph', 'tiles', 'bauhaus', 'dots']],
    'English': ['menu_book', 'coral', ['stack', 'ribbons', 'waves', 'folds']],
    'Nepali': ['draw', 'rose', ['petals', 'arches', 'hills', 'ribbons']],
    'Computer Science': ['terminal', 'slate', ['net', 'tiles', 'dots', 'graph']],
    'Accountancy': ['calculate', 'teal', ['bars', 'stack', 'graph', 'tiles']],
    'Economics': ['monitoring', 'amber', ['bars', 'graph', 'waves', 'dots']],
    'Business Studies': ['payments', 'orange', ['bars', 'ribbons', 'stack', 'folds']],
    'Social Studies': ['groups', 'sky', ['mosaic', 'hills', 'scatter', 'waves']],
    'Geography': ['public', 'moss', ['hills', 'waves', 'sunset', 'rays']],
    'History': ['history', 'amber', ['arches', 'folds', 'sunset', 'stack']],
    'Environment': ['eco', 'moss', ['petals', 'hills', 'waves', 'sunset']],
    'Hotel Management': ['nutrition', 'orange', ['scatter', 'mosaic', 'petals', 'ribbons']],
    'Law': ['gavel', 'slate', ['arches', 'tiles', 'stack', 'folds']],
    'Political Science': ['account_balance', 'azure', ['arches', 'folds', 'bauhaus', 'bars']],
    'Sociology': ['hub', 'sky', ['net', 'scatter', 'mosaic', 'orbit']],
    'Psychology': ['psychology', 'rose', ['petals', 'orbit', 'scatter', 'waves']],
    'Education': ['school', 'periwinkle', ['stack', 'bauhaus', 'ribbons', 'tiles']],
    'Music': ['music_note', 'coral', ['waves', 'ribbons', 'dots', 'petals']],
    'Health': ['cardiology', 'rose', ['petals', 'scatter', 'orbit', 'mosaic']],
    'Statistics': ['bar_chart', 'teal', ['bars', 'dots', 'graph', 'net']],
    'Engineering': ['engineering', 'orange', ['tiles', 'folds', 'bauhaus', 'graph']],
    'Agriculture': ['forest', 'moss', ['hills', 'sunset', 'waves', 'petals']],
    'Space Science': ['rocket_launch', 'sky', ['orbit', 'rays', 'sunset', 'net']]
  };
  N.subjects = SUB; N.subjectNames = Object.keys(SUB);
  N.glyphFor = function (name) { var s = SUB[name]; return s ? s[0] : 'school'; };

  function glyph(name, x, y, s, fill) {
    var d = (g.NebGlyphs || {})[name]; if (!d) return '';
    return '<path transform="translate(' + f1(x) + ' ' + f1(y + s) + ') scale(' + (s / 960).toFixed(4) + ')" d="' + d + '" fill="' + fill + '"/>';
  }
  N.glyph = glyph;

  function motif(o, c, T) {
    var W = c.W, H = c.H, gl = o.glyph || N.glyphFor(o.subject), k = c.pick(['squircle', 'cookie', 'sunny', 'flower']), m = o.motif || N.kinds[o.kind].motif, r, s, out = '';
    if (m === 'tile') { r = H * 0.3; out = N.shape(k, W * 0.8, H * 0.5, r, c.r() * 6, T[4]) + glyph(gl, W * 0.8 - r * 0.5, H * 0.5 - r * 0.5, r, T[0]); }
    else if (m === 'center') { r = W * 0.24; out = N.shape(k, W / 2, H / 2, r, c.r() * 6, T[4]) + glyph(gl, W / 2 - r * 0.52, H / 2 - r * 0.52, r * 1.04, T[0]); }
    else if (m === 'book') {
      r = W * 0.17; out = N.rect(0, 0, W * 0.07, H, 0, T[4]) + N.shape(k, W * 0.5, H * 0.3, r, c.r() * 6, T[4]) + glyph(gl, W * 0.5 - r * 0.55, H * 0.3 - r * 0.55, r * 1.1, T[0]);
      out += N.rect(W * 0.14, H * 0.64, W * 0.72, H * 0.27, 28, T[0]) + N.rect(W * 0.2, H * 0.7, W * 0.6, 16, 8, T[4]) + N.rect(W * 0.2, H * 0.77, W * 0.42, 12, 6, T[3]) + N.rect(W * 0.2, H * 0.83, W * 0.3, 10, 5, T[2]);
    }
    return out;
  }

  function sticker(c, T, o) {
    var W = c.W, k1 = c.pick(['burst', 'flower', 'cookie', 'sunny', 'clover']), k2 = c.pick(['squircle', 'cookie', 'pebble']), gl = o.glyph || N.glyphFor(o.subject), out = '';
    out += N.shape(k1, 128, 128, 120, c.r() * 6, T[2]) + N.shape(k2, 128, 128, 84, c.r() * 6, T[4]) + glyph(gl, 128 - 44, 128 - 44, 88, T[0]);
    out += N.circle(206, 52, 14, T[5]) + N.circle(46, 206, 8, T[3]);
    return out;
  }

  /* make({kind, seed, mode, layout, palette, subject, glyph, motif}) -> SVG string */
  N.make = function (o) {
    o = o || {}; o.kind = o.kind || 'cover'; o.mode = o.mode || 'light'; o.seed = o.seed === undefined ? 1 : o.seed;
    var K = N.kinds[o.kind], sub = SUB[o.subject], r = N.rng(o.kind + '|' + o.seed + '|' + (o.subject || '') + '|' + (o.layout || ''));
    var pal = o.palette || (sub ? sub[1] : N.palettes[Math.floor(r() * N.palettes.length)]);
    var T = N.palette(pal, o.mode), pool = (sub && K.layouts.length > 4) ? sub[2] : K.layouts, layout = o.layout || pool[Math.floor(r() * pool.length)];
    var c = { W: K.w, H: K.h, u: Math.min(K.w, K.h), r: r, T: T, rr: function (a, b) { return a + (b - a) * r(); }, pick: function (a) { return a[Math.floor(r() * a.length)]; } };
    var body = o.kind === 'sticker' ? sticker(c, T, o) : N.layouts[layout](c) + motif(o, c, T);
    o.resolved = { layout: layout, palette: pal };
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + K.w + ' ' + K.h + '" width="' + K.w + '" height="' + K.h + '" preserveAspectRatio="xMidYMid slice" role="img"><title>' + (o.title || K.label) + '</title><rect width="' + K.w + '" height="' + K.h + '" fill="' + T[0] + '"/>' + body + '</svg>';
  };
  N.uri = function (o) { return 'data:image/svg+xml;utf8,' + encodeURIComponent(N.make(o)); };
})(typeof window !== 'undefined' ? window : globalThis);
