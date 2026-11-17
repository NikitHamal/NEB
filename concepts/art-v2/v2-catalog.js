/* NEBians M3X Art Library v2 — 30 Subjects, 12 Art Kinds, Deterministic make() & 1,140-Piece Catalog. */
(function (g) {
  'use strict';
  var V = g.NebArtV2, f1 = V.f1;
  var M3X_LAYS = ['isoMonolith', 'expressiveTotem', 'swissGrid', 'contourTopography', 'bauhausChronicle', 'kineticRibbons', 'orbitalResonance', 'stainedMosaic', 'horizonTerrace', 'prismFacets', 'botanicalGrove', 'waveformHarmonic', 'archwayCloister', 'radialMandala'];
  var ROLE_LAYS = ['roleStudent', 'roleTeacher', 'roleInstitution', 'roleContributor', 'roleAdmin'];

  /* 30 NEB, BCA, Nursing & Bridge Course Subjects -> [glyph, palette, primaryScene, altLayouts] */
  var SUB = {
    'Physics':             ['bolt',               'brand',      'physicsOptics',       ['physicsFields', 'quantumWave', 'orbitalResonance', 'waveformHarmonic']],
    'Chemistry':           ['science',            'aqua',       'chemistryLab',        ['organicSynthesis', 'stainedMosaic', 'orbitalResonance', 'prismFacets']],
    'Biology':             ['genetics',           'emerald',    'biologyHelix',        ['botanyCell', 'botanicalGrove', 'contourTopography', 'radialMandala']],
    'Mathematics':         ['functions',          'cobalt',     'mathFibonacci',       ['mathHarmonic', 'calculusSurface', 'swissGrid', 'isoMonolith']],
    'Computer Science':    ['terminal',           'azure',      'csArchitecture',      ['neuralNetwork', 'roboticsMechatronics', 'isoMonolith', 'swissGrid']],
    'English':             ['menu_book',          'coral',      'literatureEditorial', ['bauhausChronicle', 'kineticRibbons', 'swissGrid', 'archwayCloister']],
    'Nepali':              ['draw',               'rose',       'himalayanPagoda',     ['nepalHimalaya', 'kathmanduValley', 'literatureEditorial', 'radialMandala']],
    'Accountancy':         ['calculate',          'teal',       'accountancyBalance',  ['macroFinance', 'economicsLedger', 'swissGrid', 'isoMonolith']],
    'Economics':           ['monitoring',         'amber',      'economicsLedger',     ['macroFinance', 'accountancyBalance', 'waveformHarmonic', 'swissGrid']],
    'Business Studies':    ['payments',           'marigold',   'macroFinance',        ['economicsLedger', 'isoMonolith', 'bauhausChronicle', 'kineticRibbons']],
    'Social Studies':      ['groups',             'sky',        'kathmanduValley',     ['nepalHimalaya', 'himalayanPagoda', 'campusCourtyard', 'stainedMosaic']],
    'Geography':           ['public',             'moss',       'geographyAtlas',      ['nepalHimalaya', 'contourTopography', 'horizonTerrace', 'botanicalGrove']],
    'History':             ['history',            'terracotta', 'himalayanPagoda',     ['historyMonument', 'kathmanduValley', 'archwayCloister', 'bauhausChronicle']],
    'Environment':         ['eco',                'mint',       'agricultureBotany',   ['botanyCell', 'botanicalGrove', 'nepalHimalaya', 'contourTopography']],
    'Hotel Management':    ['nutrition',          'marigold',   'hospitalityCulinary', ['campusCourtyard', 'stainedMosaic', 'bauhausChronicle', 'radialMandala']],
    'Law':                 ['gavel',              'slate',      'lawCivic',            ['archwayCloister', 'bauhausChronicle', 'swissGrid', 'isoMonolith']],
    'Political Science':   ['account_balance',    'brand',      'lawCivic',            ['kathmanduValley', 'historyMonument', 'archwayCloister', 'swissGrid']],
    'Sociology':           ['hub',                'sky',        'campusCourtyard',     ['kathmanduValley', 'stainedMosaic', 'orbitalResonance', 'expressiveTotem']],
    'Psychology':          ['psychology',         'rose',       'neuralNetwork',       ['medicineVital', 'contourTopography', 'radialMandala', 'orbitalResonance']],
    'Education':           ['school',             'azure',      'campusCourtyard',     ['literatureEditorial', 'bauhausChronicle', 'swissGrid', 'isoMonolith']],
    'Music':               ['music_note',         'coral',      'musicAcoustics',      ['waveformHarmonic', 'kineticRibbons', 'radialMandala', 'orbitalResonance']],
    'Health & Nursing':    ['cardiology',         'rose',       'medicineVital',       ['biologyHelix', 'botanyCell', 'radialMandala', 'stainedMosaic']],
    'Statistics':          ['bar_chart',          'teal',       'calculusSurface',     ['mathFibonacci', 'macroFinance', 'economicsLedger', 'waveformHarmonic']],
    'Engineering':         ['engineering',        'terracotta', 'engineeringIso',      ['roboticsMechatronics', 'calculusSurface', 'isoMonolith', 'prismFacets']],
    'Agriculture':         ['forest',             'moss',       'agricultureBotany',   ['botanyCell', 'botanicalGrove', 'nepalHimalaya', 'horizonTerrace']],
    'Space & Astronomy':   ['rocket_launch',      'cobalt',     'astronomyCosmos',     ['quantumWave', 'orbitalResonance', 'physicsOptics', 'radialMandala']],
    'BCA & Software':      ['code',               'brand',      'neuralNetwork',       ['csArchitecture', 'roboticsMechatronics', 'isoMonolith', 'swissGrid']],
    'Medicine & Entrance': ['medical_services',   'emerald',    'medicineVital',       ['organicSynthesis', 'biologyHelix', 'chemistryLab', 'botanyCell']],
    'Architecture':        ['architecture',       'amber',      'himalayanPagoda',     ['engineeringIso', 'campusCourtyard', 'archwayCloister', 'isoMonolith']],
    'Nepal Heritage':      ['travel_explore',     'sage',       'kathmanduValley',     ['himalayanPagoda', 'nepalHimalaya', 'historyMonument', 'radialMandala']]
  };
  V.subjects = SUB; V.subjectNames = Object.keys(SUB);
  V.glyphFor = function (s) { return (SUB[s] && SUB[s][0]) || 'school'; };
  V.sceneFor = function (s) { return (SUB[s] && SUB[s][2]) || 'isoMonolith'; };
  V.allCompositions = Object.keys(V.scenes).concat(M3X_LAYS).concat(ROLE_LAYS);

  /* 12 Comprehensive Art Kinds across Web & Android */
  V.kinds = {
    cover:   { w: 1200, h: 400, label: 'Profile covers',     desc: 'Role-aware & expressive covers (3:1)' },
    school:  { w: 1200, h: 400, label: 'School banners',     desc: 'Campus, Himalayan & heritage banners (3:1)' },
    thumb:   { w: 640,  h: 256, label: 'Resource thumbs',    desc: 'Notes, papers & solutions by subject (5:2)' },
    book:    { w: 400,  h: 560, label: 'Book covers',        desc: 'Swiss/MIT-Press textbook plates (5:7)' },
    lab:     { w: 800,  h: 360, label: '3D labs & chapters', desc: 'Interactive simulation & reader heroes' },
    pathway: { w: 800,  h: 320, label: 'Pathways & careers', desc: 'Degree & career route banners (5:2)' },
    post:    { w: 1200, h: 630, label: 'Post & OG headers',  desc: 'Editorial, blog & social cards (1.9:1)' },
    bg:      { w: 1600, h: 900, label: 'Note & page BGs',    desc: 'Calm tonal canvases & study spaces (16:9)' },
    tile:    { w: 512,  h: 512, label: 'Collection tiles',   desc: 'Subject hubs & study playlists (1:1)' },
    spot:    { w: 480,  h: 360, label: 'Empty state spots',  desc: 'Zero-state & onboarding illustrations (4:3)' },
    sticker: { w: 256,  h: 256, label: 'Achievements',       desc: 'Multi-layered M3X medallions (1:1)' },
    glyph:   { w: 256,  h: 256, label: 'Expressive glyphs',  desc: 'Frameless M3X avatar & subject tiles (1:1)' }
  };

  function motif(o, c, T) {
    var W = c.W, H = c.H, u = c.u, gl = o.glyph || V.glyphFor(o.subject), m = o.motif, k = c.pick(['squircle', 'cookie', 'sunny', 'clover']);
    if (m === 'badge') {
      var r = u * 0.24, cx = W - r * 1.45, cy = H * 0.5;
      return V.shape(k, cx, cy, r, c.r() * 4, T[5]) + V.glyph(gl, cx - r * 0.52, cy - r * 0.52, r * 1.04, T[7]);
    }
    if (m === 'center') {
      var rc2 = u * 0.25;
      return V.shape(k, W / 2, H / 2, rc2, c.r() * 4, T[5]) + V.glyph(gl, W / 2 - rc2 * 0.52, H / 2 - rc2 * 0.52, rc2 * 1.04, T[7]);
    }
    return '';
  }

  /* Deterministic generator: NebArtV2.make({kind, seed, mode, subject, layout, palette, glyph, motif, title}) */
  V.make = function (o) {
    o = o || {}; var kind = o.kind || 'cover', mode = o.mode || 'light', seed = o.seed === undefined ? 1 : o.seed;
    var K = V.kinds[kind] || V.kinds.cover, sub = SUB[o.subject];
    var r = V.rng(kind + '|' + seed + '|' + (o.subject || '') + '|' + (o.layout || '') + '|' + (o.palette || ''));
    var pal = o.palette || (sub ? sub[1] : V.palettes[Math.floor(r() * V.palettes.length)]);
    var T = V.palette(pal, mode);
    var c = { W: K.w, H: K.h, u: Math.min(K.w, K.h), r: r, T: T, rr: function (a, b) { return a + (b - a) * r(); }, pick: function (a) { return a[Math.floor(r() * a.length)]; } };
    var lay = o.layout;
    if (!lay) {
      if (sub) {
        var pool = [sub[2], sub[2]].concat(sub[3]);
        lay = pool[Math.floor(r() * pool.length)];
      } else {
        lay = M3X_LAYS[Math.floor(r() * M3X_LAYS.length)];
      }
    }
    var fn = V.scenes[lay] || V.layouts[lay] || V.layouts.isoMonolith, body = '';
    if (kind === 'book') body = V.makeBook(c, T, o);
    else if (kind === 'lab') body = V.makeLab(c, T, o);
    else if (kind === 'pathway') body = V.makePathway(c, T, o);
    else if (kind === 'spot') body = V.makeSpot(c, T, o);
    else if (kind === 'sticker') body = V.makeSticker(c, T, o);
    else if (kind === 'glyph') body = V.makeGlyphTile(c, T, o);
    else {
      var defMotif = kind === 'tile' ? 'center' : (kind === 'thumb' && !V.scenes[lay] ? 'badge' : 'none');
      body = fn(c) + motif({ subject: o.subject, glyph: o.glyph, motif: o.motif || defMotif }, c, T);
    }
    o.resolved = { layout: lay, palette: pal, engine: V.scenes[lay] ? 'Domain Scene' : 'M3X Architecture' };
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + K.w + ' ' + K.h + '" width="' + K.w + '" height="' + K.h + '" preserveAspectRatio="xMidYMid slice" role="img"><title>' + (o.title || (o.id || K.label)) + '</title><rect width="' + K.w + '" height="' + K.h + '" fill="' + T[0] + '"/>' + body + '</svg>';
  };

  /* Build the 1,140-piece catalog with rich metadata */
  V.catalog = function () {
    var out = [], id = {}, i, j, pad = function (n) { return ('00' + n).slice(-3); };
    function add(k, o) { id[k] = (id[k] || 0) + 1; o.kind = k; o.id = k + '-' + pad(id[k]); out.push(o); }
    var roles = [['Student', 'roleStudent'], ['Teacher', 'roleTeacher'], ['Institution', 'roleInstitution'], ['Contributor', 'roleContributor'], ['Verified & Admin', 'roleAdmin']];
    for (i = 0; i < roles.length; i++) for (j = 0; j < 16; j++) add('cover', { seed: 100 + i * 16 + j, layout: roles[i][1], palette: V.palettes[j], tag: roles[i][0], title: roles[i][0] + ' cover (' + V.palettes[j] + ')' });
    for (i = 0; i < M3X_LAYS.length; i++) for (j = 0; j < 10; j++) add('cover', { seed: 300 + i * 10 + j, layout: M3X_LAYS[i], palette: V.palettes[(i * 3 + j) % 16], tag: M3X_LAYS[i], title: M3X_LAYS[i] + ' cover' });
    var schScenes = ['campusCourtyard', 'nepalHimalaya', 'historyMonument', 'archwayCloister', 'isoMonolith', 'horizonTerrace'];
    for (i = 0; i < schScenes.length; i++) for (j = 0; j < 16; j++) add('school', { seed: 600 + i * 16 + j, layout: schScenes[i], palette: V.palettes[j], tag: schScenes[i], title: 'Campus banner · ' + schScenes[i] });
    for (i = 0; i < V.subjectNames.length; i++) for (j = 0; j < 8; j++) {
      var s = V.subjectNames[i], sc = j < 4 ? SUB[s][2] : SUB[s][3][j % 4];
      add('thumb', { seed: 1000 + i * 8 + j, subject: s, layout: sc, tag: s, title: s + ' · ' + sc });
    }
    for (i = 0; i < V.subjectNames.length; i++) for (j = 0; j < 4; j++) add('book', { seed: 2000 + i * 4 + j, subject: V.subjectNames[i], tag: V.subjectNames[i], title: V.subjectNames[i] + ' Textbook Vol. ' + (j + 1) });
    for (i = 0; i < V.subjectNames.length; i++) for (j = 0; j < 2; j++) add('lab', { seed: 2600 + i * 2 + j, subject: V.subjectNames[i], tag: V.subjectNames[i], title: V.subjectNames[i] + ' 3D Interactive Lab ' + (j + 1) });
    for (i = 0; i < V.subjectNames.length; i++) for (j = 0; j < 2; j++) add('pathway', { seed: 3000 + i * 2 + j, subject: V.subjectNames[i], tag: V.subjectNames[i], title: V.subjectNames[i] + ' Career Pathway' });
    for (i = 0; i < 72; i++) add('post', { seed: 3400 + i, subject: V.subjectNames[i % 30], palette: V.palettes[i % 16], tag: V.subjectNames[i % 30], title: 'Editorial Header · ' + V.subjectNames[i % 30] });
    for (i = 0; i < 60; i++) add('bg', { seed: 3800 + i, layout: M3X_LAYS[i % M3X_LAYS.length], palette: V.palettes[i % 16], tag: V.palettes[i % 16], title: 'Study Canvas · ' + V.palettes[i % 16] });
    for (i = 0; i < 60; i++) add('tile', { seed: 4200 + i, subject: V.subjectNames[i % 30], palette: V.palettes[(i * 3) % 16], tag: V.subjectNames[i % 30], title: V.subjectNames[i % 30] + ' Hub Tile' });
    var spots = [['Empty Notes', 'event_note'], ['No Bookmarks', 'local_library'], ['Search Ready', 'travel_explore'], ['Offline Vault', 'memory'], ['Exam Complete', 'workspace_premium'], ['Study Streak', 'bolt'], ['First Question', 'quiz'], ['Lab Ready', 'experiment'], ['Campus Claim', 'account_balance']];
    for (i = 0; i < 36; i++) { var sp = spots[i % spots.length]; add('spot', { seed: 4600 + i, glyph: sp[1], palette: V.palettes[i % 16], tag: sp[0], title: sp[0] + ' Spot' }); }
    var gls = Object.keys(g.NebGlyphs || {});
    for (i = 0; i < 48; i++) add('sticker', { seed: 5000 + i, glyph: gls[i % gls.length], palette: V.palettes[i % 16], tag: gls[i % gls.length], title: 'Achievement · ' + gls[i % gls.length] });
    for (i = 0; i < 36; i++) add('glyph', { seed: 5400 + i, shape: V.shapeNames[i % V.shapeNames.length], glyph: gls[(i * 2) % gls.length], palette: V.palettes[i % 16], tag: V.shapeNames[i % V.shapeNames.length], title: 'M3X ' + V.shapeNames[i % V.shapeNames.length] + ' tile' });
    return out;
  };
})(typeof window !== 'undefined' ? window : globalThis);
