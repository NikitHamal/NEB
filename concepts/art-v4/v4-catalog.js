/* v4 catalog: 30 subjects, 15 kinds, 2,000+ deterministic named pieces (each in Light and Dark). Nothing here draws mountains, forests, trees, ships, building rows, moon or sun. */
(function (g) {
  'use strict';
  var A = g.NebArtV4;
  /* subject -> [palette, glyph, [3 objects], [3 abstract scenes]] */
  var SUB = {
    'Physics': ['brand', 'bolt', ['atom', 'bulb', 'magnifier'], ['orbits', 'waveform', 'halftone']], 'Chemistry': ['aqua', 'science', ['flask', 'atom', 'microscope'], ['molecules', 'hex', 'nest']],
    'Biology': ['emerald', 'genetics', ['dna', 'microscope', 'sprout'], ['cells', 'dna', 'bloomField']], 'Mathematics': ['cobalt', 'functions', ['compass', 'calculator', 'target'], ['graph', 'tessera', 'arcs']],
    'Computer Science': ['sky', 'terminal', ['laptop', 'gear', 'chat'], ['network', 'halftone', 'tessera']], 'English': ['coral', 'menu_book', ['book', 'pencil', 'chat'], ['ink', 'ribbonStack', 'memphis']],
    'Nepali': ['rose', 'draw', ['notebook', 'pencil', 'bell'], ['kaleido', 'scallop', 'weave']], 'Accountancy': ['teal', 'calculate', ['calculator', 'chart', 'folder'], ['rise', 'graph', 'weave']],
    'Economics': ['amber', 'monitoring', ['chart', 'scales', 'target'], ['rise', 'graph', 'arcs']], 'Business Studies': ['marigold', 'payments', ['chart', 'envelope', 'target'], ['rise', 'tessera', 'flow']],
    'Social Studies': ['sky', 'groups', ['globe', 'chat', 'book'], ['network', 'bloomField', 'glyphField']], 'Geography': ['moss', 'public', ['globe', 'compass', 'plane'], ['flow', 'waveform', 'nest']],
    'History': ['terracotta', 'history', ['book', 'clock', 'folder'], ['weave', 'scallop', 'kaleido']], 'Environment': ['mint', 'compost', ['sprout', 'globe', 'cloud'], ['bloomField', 'flow', 'cells']],
    'Hotel Management': ['marigold', 'nutrition', ['bell', 'calendar', 'envelope'], ['scallop', 'memphis', 'hex']], 'Law': ['slate', 'gavel', ['scales', 'shield', 'folder'], ['weave', 'tessera', 'arcs']],
    'Political Science': ['brand', 'account_balance', ['scales', 'chat', 'globe'], ['arcs', 'tessera', 'network']], 'Sociology': ['sky', 'hub', ['chat', 'globe', 'bell'], ['network', 'bloomField', 'cells']],
    'Psychology': ['rose', 'psychology', ['bulb', 'pulse', 'notebook'], ['nest', 'kaleido', 'ink']], 'Education': ['denim', 'school', ['cap', 'book', 'notebook'], ['glyphField', 'tessera', 'ribbonStack']],
    'Music': ['coral', 'music_note', ['music', 'bell', 'palette'], ['waveform', 'ribbonStack', 'halftone']], 'Health & Nursing': ['crimson', 'cardiology', ['pulse', 'shield', 'microscope'], ['cells', 'molecules', 'hex']],
    'Statistics': ['teal', 'bar_chart', ['chart', 'calculator', 'target'], ['graph', 'rise', 'halftone']], 'Engineering': ['terracotta', 'engineering', ['gear', 'compass', 'laptop'], ['hex', 'tessera', 'network']],
    'Agriculture': ['lime', 'compost', ['sprout', 'cloud', 'globe'], ['bloomField', 'flow', 'cells']], 'Space & Astronomy': ['cobalt', 'rocket_launch', ['rocket', 'atom', 'magnifier'], ['orbits', 'halftone', 'nest']],
    'BCA & Software': ['brand', 'code', ['laptop', 'cloud', 'plug'], ['network', 'tessera', 'halftone']], 'Medicine & Entrance': ['emerald', 'medical_services', ['pulse', 'microscope', 'dna'], ['cells', 'molecules', 'dna']],
    'Architecture': ['amber', 'architecture', ['compass', 'folder', 'gear'], ['tessera', 'hex', 'scallop']], 'Nepal Heritage': ['sand', 'travel_explore', ['bell', 'book', 'palette'], ['kaleido', 'scallop', 'weave']],
    'Art & Design': ['coral', 'palette', ['palette', 'pencil', 'plane'], ['ink', 'memphis', 'bloomField']], 'Career Pathways': ['pine', 'travel_explore', ['plane', 'target', 'medal'], ['flow', 'arcs', 'rise']],
    'Study Skills': ['denim', 'school', ['clock', 'notebook', 'bulb'], ['glyphField', 'ribbonStack', 'nest']], 'Exam Prep': ['marigold', 'workspace_premium', ['trophy', 'clock', 'pencil'], ['arcs', 'rise', 'tessera']]
  };
  A.subjects = SUB; A.subjectNames = Object.keys(SUB);
  A.kinds = {
    cover: { w: 1200, h: 400, label: 'Profile covers', desc: 'Calm space on the left, art on the right (3:1)' }, school: { w: 1200, h: 400, label: 'School banners', desc: 'Abstract school identity, no buildings (3:1)' },
    thumb: { w: 640, h: 256, label: 'Resource thumbnails', desc: 'Notes, papers, solutions (5:2)' }, book: { w: 400, h: 560, label: 'Book covers', desc: 'Text-free plates (5:7)' },
    post: { w: 1200, h: 630, label: 'Post and share headers', desc: 'Blog and OG cards (1.9:1)' }, bg: { w: 1600, h: 900, label: 'Page backgrounds', desc: 'Calm canvases (16:9)' },
    tile: { w: 512, h: 512, label: 'Collection tiles', desc: 'Subject hubs and playlists (1:1)' }, spot: { w: 480, h: 360, label: 'Empty states', desc: 'Zero-state illustrations (4:3)' },
    sticker: { w: 256, h: 256, label: 'Achievements', desc: 'Medal plates (1:1)' }, avatar: { w: 256, h: 256, label: 'Profile pictures', desc: 'Frameless, clip to any shape (1:1)' },
    pathway: { w: 800, h: 320, label: 'Pathways', desc: 'Course and career banners (5:2)' }, lab: { w: 800, h: 360, label: 'Labs and chapters', desc: 'Reader and simulation heroes' },
    story: { w: 540, h: 960, label: 'Onboarding stories', desc: 'Full-screen 9:16' }, pattern: { w: 600, h: 600, label: 'Patterns', desc: 'Swatches for fills (1:1)' }, wide: { w: 1600, h: 560, label: 'Hero banners', desc: 'Web home and section heroes (20:7)' }
  };
  var SPOTS = [['No results', 'magnifier'], ['No notes', 'notebook'], ['Offline', 'plug'], ['No saved items', 'folder'], ['No resources', 'books'], ['No posts', 'pencil'], ['No answers', 'bulb'], ['No schools', 'cap'], ['No messages', 'chat'], ['No notifications', 'bell'], ['All caught up', 'medal'], ['Coming soon', 'rocket'], ['Under review', 'clock'], ['Access denied', 'shield'], ['Upload ready', 'cloud'], ['No history', 'calendar'], ['No followers', 'chat'], ['No quizzes', 'target'], ['No polls', 'chart'], ['No downloads', 'folder'], ['No books', 'book'], ['No videos', 'laptop'], ['No pathways', 'plane'], ['No courses', 'cap'], ['No events', 'calendar'], ['No comments', 'chat'], ['Something broke', 'plug'], ['Sign in', 'envelope'], ['Verify email', 'envelope'], ['Maintenance', 'gear'], ['No scholarships', 'trophy'], ['No jobs', 'compass'], ['No papers', 'notebook'], ['No labs', 'flask'], ['No music', 'music'], ['No drafts', 'pencil'], ['No achievements', 'medal'], ['Search to start', 'magnifier'], ['First steps', 'sprout'], ['Saved for later', 'calendar']];
  var ACH = [['First note', 'notebook'], ['Helpful answer', 'bulb'], ['Seven day streak', 'clock'], ['Top contributor', 'trophy'], ['Quiz master', 'target'], ['Early bird', 'clock'], ['Verified teacher', 'cap'], ['Campus star', 'medal'], ['Resource hero', 'books'], ['Poll maker', 'chart'], ['Exam ready', 'pencil'], ['Bookworm', 'book'], ['Explorer', 'compass'], ['Mentor', 'scales'], ['Problem solver', 'calculator'], ['Night owl', 'atom'], ['Lab rat', 'flask'], ['Coder', 'laptop'], ['Artist', 'palette'], ['Musician', 'music'], ['Navigator', 'plane'], ['Guardian', 'shield'], ['Green thumb', 'sprout'], ['Champion', 'medal']];
  var NAMES = ['Aarav', 'Anisha', 'Bibek', 'Chandra', 'Dipesh', 'Elina', 'Gita', 'Hari', 'Isha', 'Kiran', 'Laxmi', 'Manish', 'Nisha', 'Oja', 'Prabin', 'Rina', 'Sagar', 'Tara', 'Utsav', 'Yuna', 'Sujal', 'Ritu', 'Bimal', 'Sita'];
  var CALM = ['waveform', 'flow', 'nest', 'tessera', 'hex', 'kaleido', 'halftone', 'arcs', 'scallop', 'weave', 'bloomField', 'terrazzo', 'memphis', 'ribbonStack', 'cells', 'orbits', 'rise'];
  var PNAME = A.palettes, cache = null;
  function pal(base, k) { return k % 3 === 0 ? base : PNAME[(PNAME.indexOf(base) + (k % 3) * 7 + k) % PNAME.length]; }
  function title(s) { return s.replace(/([A-Z])/g, ' $1').replace(/^./, function (c) { return c.toUpperCase(); }); }
  var STY = ['disc', 'arch', 'plate', 'ground', 'burst', 'pattern'];

  A.catalog = function () {
    if (cache) return cache;
    var out = [], n = {}, S = A.subjectNames, i, k, s, d, nm;
    function add(kind, name, engine, palette, subj, o) { n[kind] = (n[kind] || 0) + 1; out.push({ id: kind + '-' + ('000' + n[kind]).slice(-4), kind: kind, name: name, engine: engine, palette: palette, seed: n[kind] * 7 + 3, subj: subj, o: o || {}, w: A.kinds[kind].w, h: A.kinds[kind].h }); }
    function hero(kind, i, styles, side) { s = S[i % S.length]; d = SUB[s]; k = Math.floor(i / S.length); var ob = [d[2][k % 3], d[2][(k + 1) % 3], d[2][(k + 2) % 3]]; add(kind, s + ' / ' + title(ob[0]), 'stage', pal(d[0], k + 1), s, { objs: k % 2 ? [ob[0], ob[1]] : ob, style: styles[k % styles.length], bg: d[3][(k + 1) % 3], side: side }); }
    function scene(kind, i, sub) { s = S[i % S.length]; d = SUB[s]; k = Math.floor(i / S.length); nm = d[3][k % 3]; add(kind, s + ' / ' + title(nm), nm, pal(d[0], k), s); }
    for (i = 0; i < 240; i++) { if (i % 3 === 0) hero('cover', i, ['pattern', 'disc', 'arch'], 'right'); else scene('cover', i); }
    for (i = 0; i < 120; i++) { if (i % 2) hero('school', i, ['pattern', 'burst', 'plate'], 'right'); else add('school', 'Banner ' + (i + 1), CALM[i % CALM.length], PNAME[(i * 3 + 1) % PNAME.length], 'Schools'); }
    for (i = 0; i < 300; i++) { if (i % 5 < 3) hero('thumb', i - Math.floor(i / 5) * 2, STY, 'center'); else scene('thumb', i); }
    for (i = 0; i < 160; i++) { if (i % 3) hero('book', i, ['arch', 'plate', 'disc', 'pattern'], 'center'); else scene('book', i); }
    for (i = 0; i < 120; i++) { if (i % 2) hero('post', i, ['pattern', 'disc', 'plate'], 'right'); else scene('post', i); }
    for (i = 0; i < 160; i++) add('bg', title(CALM[i % CALM.length]) + ' ' + (Math.floor(i / CALM.length) + 1), CALM[i % CALM.length], PNAME[(i * 7 + 2) % PNAME.length], 'Backgrounds');
    for (i = 0; i < 150; i++) hero('tile', i, STY, 'center');
    SPOTS.forEach(function (sp, j) { var alt = ['bulb', 'chat', 'bell', 'clock', 'sprout', 'globe', 'calendar', 'target'];
      for (var v = 0; v < 4; v++) add('spot', sp[0] + ' ' + (v + 1), 'stage', PNAME[(j * 5 + v * 7) % PNAME.length], 'Empty states', { objs: v === 0 ? [sp[1]] : [sp[1], alt[(j + v) % 8], alt[(j + v * 3 + 2) % 8]].slice(0, v === 1 ? 2 : 3), style: ['disc', 'arch', 'plate', 'ground'][v], side: 'center' }); });
    ACH.forEach(function (a, j) { for (var v = 0; v < 4; v++) add('sticker', a[0] + ' ' + (v + 1), 'stage', PNAME[(j * 3 + v * 5) % PNAME.length], 'Achievements', { objs: [a[1]], style: ['burst', 'plate', 'disc', 'arch'][v], side: 'center', tilt: v * 3 - 4 }); });
    for (i = 0; i < 240; i++) add('avatar', NAMES[i % NAMES.length] + ' ' + (Math.floor(i / NAMES.length) + 1), 'person', PNAME[(i * 7 + 3) % PNAME.length], 'People', {});
    for (i = 0; i < 60; i++) add('avatar', 'Buddy ' + (i + 1), 'buddy', PNAME[(i * 5 + 1) % PNAME.length], 'Buddies', {});
    for (i = 0; i < 72; i++) { var cn = A.critterNames[i % A.critterNames.length]; add('avatar', title(cn) + ' ' + (Math.floor(i / 6) + 1), 'critter', PNAME[(i * 3 + 2) % PNAME.length], 'Critters', { critter: cn }); }
    for (i = 0; i < 60; i++) { s = S[i % S.length]; d = SUB[s]; add('avatar', s + ' tile ' + (Math.floor(i / S.length) + 1), 'glyphTile', pal(d[0], Math.floor(i / S.length) + 1), s, { glyph: d[1] }); }
    for (i = 0; i < 60; i++) { s = S[i % S.length]; d = SUB[s]; add('avatar', s + ' / ' + title(d[2][i % 3]), 'stage', pal(d[0], i), s, { objs: [d[2][i % 3]], style: ['disc', 'burst', 'ground'][i % 3], side: 'center' }); }
    for (i = 0; i < 100; i++) { if (i % 2) hero('pathway', i, ['pattern', 'disc'], 'right'); else scene('pathway', i); }
    for (i = 0; i < 80; i++) { if (i % 2) hero('lab', i, ['plate', 'pattern', 'arch'], 'right'); else scene('lab', i); }
    for (i = 0; i < 60; i++) { if (i % 2) hero('story', i, ['arch', 'plate', 'disc', 'pattern'], 'center'); else scene('story', i); }
    for (i = 0; i < 17 * 8; i++) add('pattern', title(CALM[i % CALM.length]) + ' ' + (Math.floor(i / CALM.length) + 1), CALM[i % CALM.length], PNAME[(i * 3 + Math.floor(i / 17)) % PNAME.length], 'Patterns');
    for (i = 0; i < 90; i++) { if (i % 3) hero('wide', i, ['pattern', 'disc', 'arch'], 'right'); else scene('wide', i); }
    return (cache = out);
  };
  A.render = function (it, mode) { return A.make({ engine: it.engine, palette: it.palette, seed: it.seed, w: it.w, h: it.h, mode: mode, subj: it.subj, id: it.id, o: it.o, kind: it.kind }); };
})(typeof window !== 'undefined' ? window : globalThis);
