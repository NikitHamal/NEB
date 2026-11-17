/* v3 catalog: 32 subjects, 14 kinds, 1,500+ deterministic named pieces (each rendered in Light and Dark). */
(function (g) {
  'use strict';
  var A = g.NebArtV3;
  /* subject -> [palette, glyph, [objects], [scenes]] */
  var SUB = {
    'Physics': ['brand', 'bolt', ['atom', 'magnet', 'telescope'], ['twilight', 'himal', 'lake']], 'Chemistry': ['aqua', 'science', ['flask', 'atom', 'leaf'], ['lake', 'contour', 'monsoon']],
    'Biology': ['emerald', 'genetics', ['dna', 'sprout', 'leaf'], ['forest', 'meadow', 'orchard']], 'Mathematics': ['cobalt', 'functions', ['compass', 'abacus', 'chart'], ['contour', 'dunes', 'skyline']],
    'Computer Science': ['sky', 'terminal', ['laptop', 'gear', 'bulb'], ['skyline', 'twilight', 'river']], 'English': ['coral', 'menu_book', ['books', 'pencil', 'notebook'], ['meadow', 'campus', 'dunes']],
    'Nepali': ['rose', 'draw', ['pencil', 'notebook', 'pagoda'], ['valley', 'himal', 'terraces']], 'Accountancy': ['teal', 'calculate', ['calculator', 'chart', 'abacus'], ['skyline', 'campus', 'river']],
    'Economics': ['amber', 'monitoring', ['chart', 'scales', 'calculator'], ['skyline', 'terraces', 'dunes']], 'Business Studies': ['marigold', 'payments', ['chart', 'backpack', 'bulb'], ['skyline', 'campus', 'dunes']],
    'Social Studies': ['sky', 'groups', ['globe', 'books', 'pagoda'], ['valley', 'campus', 'meadow']], 'Geography': ['moss', 'public', ['globe', 'compass', 'summit'], ['himal', 'terraces', 'river']],
    'History': ['terracotta', 'history', ['stupa', 'pagoda', 'doc'], ['valley', 'dunes', 'twilight']], 'Environment': ['mint', 'eco', ['leaf', 'sprout', 'plant'], ['forest', 'meadow', 'monsoon']],
    'Hotel Management': ['marigold', 'nutrition', ['bell', 'notebook', 'plant'], ['campus', 'orchard', 'lake']], 'Law': ['slate', 'gavel', ['scales', 'shield', 'doc'], ['skyline', 'campus', 'twilight']],
    'Political Science': ['brand', 'account_balance', ['scales', 'doc', 'globe'], ['campus', 'skyline', 'valley']], 'Sociology': ['sky', 'hub', ['globe', 'backpack', 'books'], ['valley', 'river', 'meadow']],
    'Psychology': ['rose', 'psychology', ['bulb', 'pulse', 'notebook'], ['twilight', 'contour', 'lake']], 'Education': ['denim', 'school', ['cap', 'books', 'backpack'], ['campus', 'meadow', 'himal']],
    'Music': ['coral', 'music_note', ['music', 'bell', 'palette'], ['twilight', 'lake', 'meadow']], 'Health & Nursing': ['crimson', 'cardiology', ['pulse', 'flask', 'shield'], ['meadow', 'lake', 'orchard']],
    'Statistics': ['teal', 'bar_chart', ['chart', 'calculator', 'compass'], ['contour', 'skyline', 'dunes']], 'Engineering': ['terracotta', 'engineering', ['gear', 'compass', 'laptop'], ['skyline', 'river', 'himal']],
    'Agriculture': ['lime', 'forest', ['sprout', 'plant', 'leaf'], ['terraces', 'orchard', 'meadow']], 'Space & Astronomy': ['cobalt', 'rocket_launch', ['rocket', 'planet', 'telescope'], ['twilight', 'himal', 'dunes']],
    'BCA & Software': ['brand', 'code', ['laptop', 'gear', 'bulb'], ['skyline', 'twilight', 'monsoon']], 'Medicine & Entrance': ['emerald', 'medical_services', ['pulse', 'flask', 'dna'], ['lake', 'meadow', 'forest']],
    'Architecture': ['amber', 'architecture', ['pagoda', 'compass', 'gear'], ['valley', 'skyline', 'campus']], 'Nepal Heritage': ['sand', 'travel_explore', ['stupa', 'pagoda', 'summit'], ['valley', 'himal', 'terraces']],
    'Art & Design': ['coral', 'palette', ['palette', 'pencil', 'plane'], ['meadow', 'dunes', 'orchard']], 'Career Pathways': ['pine', 'travel_explore', ['plane', 'summit', 'backpack'], ['himal', 'lake', 'terraces']],
    'Study Skills': ['denim', 'school', ['clock', 'notebook', 'bulb'], ['campus', 'contour', 'meadow']], 'Exam Prep': ['marigold', 'workspace_premium', ['trophy', 'clock', 'pencil'], ['himal', 'campus', 'dunes']]
  };
  A.subjects = SUB; A.subjectNames = Object.keys(SUB);
  A.kinds = {
    cover: { w: 1200, h: 400, label: 'Profile covers', desc: 'Role-safe covers, object on the right (3:1)' }, school: { w: 1200, h: 400, label: 'School banners', desc: 'Campus, valley and Himalaya (3:1)' },
    thumb: { w: 640, h: 256, label: 'Resource thumbnails', desc: 'Notes, papers and solutions (5:2)' }, book: { w: 400, h: 560, label: 'Book covers', desc: 'Text-free plates (5:7)' },
    post: { w: 1200, h: 630, label: 'Post and OG headers', desc: 'Blog and share cards (1.9:1)' }, bg: { w: 1600, h: 900, label: 'Page backgrounds', desc: 'Calm canvases for notes (16:9)' },
    tile: { w: 512, h: 512, label: 'Collection tiles', desc: 'Subject hubs and playlists (1:1)' }, spot: { w: 480, h: 360, label: 'Empty-state spots', desc: 'Zero-state illustrations (4:3)' },
    sticker: { w: 256, h: 256, label: 'Achievements', desc: 'Medal plates (1:1)' }, avatar: { w: 256, h: 256, label: 'Profile pictures', desc: 'Frameless, clip to any shape (1:1)' },
    pathway: { w: 800, h: 320, label: 'Pathways', desc: 'Course and career banners (5:2)' }, lab: { w: 800, h: 360, label: 'Labs and chapters', desc: 'Reader and simulation heroes' },
    story: { w: 540, h: 960, label: 'Onboarding stories', desc: 'Full-screen 9:16 art' }, pattern: { w: 600, h: 600, label: 'Patterns', desc: 'Swatches for fills and tiles (1:1)' }
  };
  var SPOTS = { 'No results': 'compass', 'No notes': 'notebook', 'Offline': 'plane', 'No saved items': 'bell', 'No resources': 'books', 'No posts': 'pencil', 'No answers': 'bulb', 'No schools': 'pagoda', 'No messages': 'doc', 'No results found': 'globe', 'All caught up': 'trophy', 'Coming soon': 'rocket', 'Under review': 'clock', 'Access denied': 'shield', 'Upload ready': 'backpack', 'No history': 'stupa', 'No courses': 'cap', 'No exams': 'calculator', 'No polls': 'chart', 'No teachers': 'scales', 'No downloads': 'doc', 'Search tips': 'telescope', 'Study break': 'plant', 'Streak start': 'leaf' };
  var ACH = ['First note', 'Helpful answer', 'Seven day streak', 'Top contributor', 'Quiz master', 'Early bird', 'Verified teacher', 'Campus star', 'Resource hero', 'Poll maker', 'Exam ready', 'Bookworm', 'Explorer', 'Mentor', 'Problem solver', 'Night owl'];
  var ACHO = ['notebook', 'bulb', 'clock', 'trophy', 'calculator', 'sprout', 'cap', 'shield', 'books', 'chart', 'pencil', 'books', 'compass', 'scales', 'abacus', 'atom'];
  var PATS = ['truchet', 'dhaka', 'lattice', 'shapeField', 'stackShapes', 'scallop', 'pills', 'mandala', 'bubbles', 'waves', 'bauhaus', 'ribbons', 'arches', 'confetti', 'bars'];
  var CALM = ['waves', 'contour', 'dunes', 'orchard', 'river', 'scallop', 'arches', 'ribbons', 'bubbles', 'confetti', 'shapeField', 'lattice', 'stackShapes', 'dhaka'];
  var LAND = ['himal', 'terraces', 'valley', 'lake', 'meadow', 'forest', 'monsoon', 'twilight', 'campus', 'skyline', 'river', 'contour', 'dunes', 'orchard'];
  var PNAME = A.palettes, cache = null;
  function pal(base, k) { return k % 3 === 0 ? base : PNAME[(PNAME.indexOf(base) + (k % 3) * 7 + k) % PNAME.length]; }
  function title(s) { return s.replace(/([A-Z])/g, ' $1').replace(/^./, function (c) { return c.toUpperCase(); }); }

  A.catalog = function () {
    if (cache) return cache;
    var out = [], n = {}, S = A.subjectNames;
    function add(kind, name, engine, palette, subj, o) { n[kind] = (n[kind] || 0) + 1; out.push({ id: kind + '-' + ('00' + n[kind]).slice(-3), kind: kind, name: name, engine: engine, palette: palette, seed: n[kind] * 7 + 3, subj: subj, o: o || {}, w: A.kinds[kind].w, h: A.kinds[kind].h }); }
    function still(kind, i, styles, count) { var s = S[i % S.length], d = SUB[s], k = Math.floor(i / S.length), objs = [d[2][k % 3], d[2][(k + 1) % 3], d[2][(k + 2) % 3]]; add(kind, s + ' / ' + title(objs[0]), 'still', pal(d[0], k + 1), s, { objs: objs, style: styles[k % styles.length], glyph: d[1] }); }
    var i, s, d, k;
    for (i = 0; i < 120; i++) { s = S[i % S.length]; d = SUB[s]; k = Math.floor(i / S.length);
      if (k % 4 === 3) { var ob = [d[2][0], d[2][1], d[2][2]]; add('cover', s + ' / ' + title(ob[0]), 'still', pal(d[0], k), s, { objs: ob, side: 'right' }); } else add('cover', s + ' / ' + title(d[3][k % 3]), d[3][k % 3], pal(d[0], k), s); }
    for (i = 0; i < 80; i++) add('school', title(['campus', 'valley', 'himal', 'terraces', 'lake', 'meadow', 'skyline', 'twilight'][i % 8]) + ' ' + (Math.floor(i / 8) + 1), ['campus', 'valley', 'himal', 'terraces', 'lake', 'meadow', 'skyline', 'twilight'][i % 8], PNAME[(i * 3 + 1) % PNAME.length], 'Schools');
    for (i = 0; i < 256; i++) { if (i % 8 < 5) still('thumb', i - Math.floor(i / 8) * 3, ['disc', 'plate', 'arch', 'ground', 'pattern']); else { s = S[Math.floor(i / 8)]; d = SUB[s]; k = i % 8; add('thumb', s + ' / ' + title(d[3][k % 3]), k === 7 ? CALM[i % CALM.length] : d[3][k % 3], pal(d[0], k), s); } }
    for (i = 0; i < 128; i++) still('book', i, ['plate', 'disc', 'arch', 'pattern']);
    for (i = 0; i < 96; i++) { s = S[i % S.length]; d = SUB[s]; k = Math.floor(i / S.length); add('post', s + ' / ' + title(k === 2 ? CALM[i % CALM.length] : d[3][k % 3]), k === 2 ? CALM[i % CALM.length] : d[3][k % 3], pal(d[0], k + 1), s); }
    for (i = 0; i < 96; i++) add('bg', title(CALM[i % CALM.length]) + ' ' + (Math.floor(i / CALM.length) + 1), CALM[i % CALM.length], PNAME[(i * 7 + 2) % PNAME.length], 'Backgrounds');
    for (i = 0; i < 128; i++) still('tile', i, ['disc', 'plate', 'arch', 'ground']);
    Object.keys(SPOTS).forEach(function (nm, j) { [0, 1, 2].forEach(function (v) { add('spot', nm + ' ' + (v + 1), 'still', PNAME[(j * 5 + v * 7) % PNAME.length], 'Empty states', { objs: [SPOTS[nm]], style: ['disc', 'plate', 'arch'][v] }); }); });
    ACH.forEach(function (nm, j) { [0, 1, 2, 3].forEach(function (v) { add('sticker', nm + ' ' + (v + 1), 'still', PNAME[(j * 3 + v * 5) % PNAME.length], 'Achievements', { objs: [ACHO[j]], style: ['plate', 'disc', 'plate', 'arch'][v] }); }); });
    ['avBuddy', 'avPerson', 'avCritter', 'avGlyph'].forEach(function (e, j) { for (i = 0; i < (e === 'avGlyph' ? 60 : 60); i++) add('avatar', ({ avBuddy: 'Buddy', avPerson: 'Person', avCritter: 'Critter', avGlyph: 'Glyph' })[e] + ' ' + (i + 1), e, PNAME[(i * 3 + j) % PNAME.length], 'Profile pictures', e === 'avGlyph' ? { glyph: SUB[S[i % S.length]][1] } : {}); });
    for (i = 0; i < 64; i++) { s = S[(i * 3) % S.length]; d = SUB[s]; add('pathway', s + ' route ' + (Math.floor(i / 8) + 1), i % 4 === 3 ? 'still' : d[3][i % 3], pal(d[0], i), s, i % 4 === 3 ? { objs: d[2], side: i % 8 === 3 ? 'left' : 'right' } : {}); }
    for (i = 0; i < 48; i++) { s = S[(i * 5) % S.length]; d = SUB[s]; add('lab', s + ' lab ' + (Math.floor(i / 8) + 1), i % 3 === 2 ? 'still' : d[3][i % 3], pal(d[0], i + 1), s, i % 3 === 2 ? { objs: d[2], style: 'plate' } : {}); }
    for (i = 0; i < 48; i++) { s = S[(i * 7) % S.length]; d = SUB[s]; add('story', 'Story ' + (i + 1) + ' / ' + s, i % 2 ? 'still' : d[3][i % 3], pal(d[0], i), s, i % 2 ? { objs: d[2], style: ['disc', 'arch', 'ground'][i % 3] } : {}); }
    for (i = 0; i < 90; i++) add('pattern', title(PATS[i % 15]) + ' ' + (Math.floor(i / 15) + 1), PATS[i % 15], PNAME[(i * 7 + 3) % PNAME.length], 'Patterns');
    return (cache = out);
  };
  A.render = function (item, mode) { var c = {}; for (var k in item) c[k] = item[k]; c.mode = mode || 'light'; return A.make(c); };
})(typeof window !== 'undefined' ? window : globalThis);
