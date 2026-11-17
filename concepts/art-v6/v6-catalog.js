/* v6 catalog: 17 kinds, 3,500+ deterministic named pieces, each in Light and Dark. Same id gives the same art everywhere.
   Subject data (palette, glyph, hero objects) is read from the v4 catalog table; nothing here draws mountains, forests, trees, ships, building rows, moon or sun. */
(function (g) {
  'use strict';
  var A = g.NebArtV6, V4 = g.NebArtV4, SUB = V4.subjects, S = V4.subjectNames, PN = A.palettes, SC = A.SCENES, cache = null;
  A.subjectNames = S; A.subjects = SUB;
  var SN = { truchet: 'Loops', bauhaus: 'Blocks', voronoi: 'Glass', lowpoly: 'Facets', silk: 'Silk', vortex: 'Vortex', bento: 'Bento', dotwave: 'Dot wave', packing: 'Bubbles', morphGrid: 'Morph', doodle: 'Doodles' };
  A.sceneName = SN;
  A.kinds = {
    cover: { w: 1200, h: 400, label: 'Profile covers', desc: 'Quiet paper edge on the left for the picture and name (3:1)' }, school: { w: 1200, h: 400, label: 'School banners', desc: 'Abstract school identity (3:1)' },
    thumb: { w: 640, h: 256, label: 'Resource thumbnails', desc: 'Notes, papers, solutions (5:2)' }, book: { w: 400, h: 560, label: 'Book covers', desc: 'Text-free plates (5:7)' },
    post: { w: 1200, h: 630, label: 'Post headers', desc: 'Blog and share cards (1.9:1)' }, bg: { w: 1600, h: 900, label: 'Page backgrounds', desc: 'Full-bleed canvases (16:9)' },
    tile: { w: 512, h: 512, label: 'Collection tiles', desc: 'Subject hubs and playlists (1:1)' }, spot: { w: 480, h: 360, label: 'Empty states', desc: 'A pal and a prop, four compositions (4:3)' },
    sticker: { w: 256, h: 256, label: 'Achievements', desc: 'Medal plates (1:1)' }, avatar: { w: 256, h: 256, label: 'Profile pictures', desc: 'People, pals and subject marks, frameless (1:1)' },
    pathway: { w: 800, h: 320, label: 'Pathways', desc: 'Course and career banners (5:2)' }, story: { w: 540, h: 960, label: 'Onboarding stories', desc: 'Full-screen (9:16)' },
    pattern: { w: 600, h: 600, label: 'Patterns', desc: 'Swatches for fills (1:1)' }, wide: { w: 1600, h: 560, label: 'Hero banners', desc: 'Web home and section heroes (20:7)' },
    strip: { w: 1200, h: 200, label: 'Section strips', desc: 'Thin headers for cards and sheets (6:1)' }, wall: { w: 540, h: 1170, label: 'Phone wallpapers', desc: 'Lock and home screens (9:19.5)' },
    icon: { w: 256, h: 256, label: 'Subject icons', desc: 'Glyph on a shape, four looks (1:1)' }
  };
  var SPOTS = [['No results', 'magnifier'], ['No notes', 'notebook'], ['Offline', 'plug'], ['No saved items', 'folder'], ['No resources', 'books'], ['No posts', 'pencil'], ['No answers', 'bulb'], ['No schools', 'cap'], ['No messages', 'chat'], ['No notifications', 'bell'], ['No downloads', 'cloud'], ['No bookmarks', 'book'], ['No followers', 'chat'], ['No quizzes', 'target'], ['No polls', 'chart'], ['No achievements yet', 'trophy'], ['No history', 'clock'], ['No drafts', 'pencil'], ['No uploads', 'cloud'], ['No comments', 'chat'], ['No reviews', 'medal'], ['No events', 'calendar'], ['No teachers', 'cap'], ['No pathways', 'compass'], ['No collections', 'folder'], ['All caught up', 'medal'], ['Search to begin', 'magnifier'], ['Sign in needed', 'shield'], ['Permission needed', 'shield'], ['Update needed', 'gear'], ['Maintenance', 'gear'], ['Page not found', 'compass'], ['Server error', 'plug'], ['Empty folder', 'folder'], ['No orders', 'envelope'], ['No payouts', 'calculator'], ['No classes', 'calendar'], ['No exams', 'clock'], ['No scores', 'chart'], ['No streak yet', 'rocket'], ['No labs', 'flask'], ['No subjects', 'globe'], ['No music', 'music'], ['Coming soon', 'rocket']];
  var ACH = [['First note', 'notebook'], ['Helpful answer', 'bulb'], ['Seven day streak', 'clock'], ['Top contributor', 'trophy'], ['Quiz master', 'target'], ['Early bird', 'clock'], ['Verified teacher', 'cap'], ['Campus star', 'medal'], ['Resource hero', 'books'], ['Bug hunter', 'magnifier'], ['Poll starter', 'chart'], ['Night owl', 'book'], ['Scholar', 'cap'], ['Explorer', 'compass'], ['Lab partner', 'flask'], ['Rocket start', 'rocket'], ['Mentor', 'chat'], ['Curator', 'folder'], ['Sharp mind', 'bulb'], ['Math whiz', 'calculator'], ['Bookworm', 'book'], ['Team player', 'scales'], ['Green thumb', 'sprout'], ['Musician', 'music']];
  var NAMES = ['Aarav', 'Anisha', 'Bibek', 'Chandra', 'Dipesh', 'Elina', 'Gita', 'Hari', 'Isha', 'Kiran', 'Laxmi', 'Manish', 'Nisha', 'Oja', 'Prabin', 'Rina', 'Sagar', 'Tara', 'Utsav', 'Yuna', 'Sujal', 'Ritu', 'Bimal', 'Sita'];
  var PALN = ['Biscuit', 'Moss', 'Pip', 'Dot', 'Noodle', 'Bean', 'Pixel', 'Mochi', 'Fig', 'Basil', 'Clove', 'Nori'];
  var PATS = ['truchet', 'bauhaus', 'voronoi', 'morphGrid', 'dotwave', 'packing', 'bento', 'doodle'], STRIPS = ['silk', 'truchet', 'dotwave', 'bauhaus', 'vortex', 'lowpoly', 'morphGrid', 'voronoi'];
  var WALLS = ['silk', 'vortex', 'truchet', 'dotwave', 'morphGrid', 'lowpoly', 'bauhaus', 'packing'], PLATE = ['card', 'shape', 'ring'];
  function pal(base, k) { return k % 3 === 0 ? base : PN[(PN.indexOf(base) + 1 + (k % 3) * 6 + k) % PN.length]; }

  A.catalog = function () {
    if (cache) return cache;
    var out = [], n = {}, i, k, s, d;
    function add(kind, name, engine, palette, subj, o) { n[kind] = (n[kind] || 0) + 1; out.push({ id: kind + '-' + ('0000' + n[kind]).slice(-4), kind: kind, name: name, engine: engine, palette: palette, seed: n[kind] * 13 + 5, subj: subj, o: o || {}, w: A.kinds[kind].w, h: A.kinds[kind].h }); }
    function sc(i) { return SC[(i * 5 + 3) % SC.length]; }
    function pick3(d, k) { return [d[2][k % 3], d[2][(k + 1) % 3], d[2][(k + 2) % 3]]; }
    function subj(kind, i, cfg) {
      s = S[i % S.length]; d = SUB[s]; k = Math.floor(i / S.length); var scene = SC[(i + k * 3 + S.indexOf(s)) % SC.length], o = { scene: scene, deep: (i + k) % 3 === 0 };
      if (cfg.show && (cfg.every ? i % cfg.every !== 0 : true)) { o.objs = cfg.one ? [pick3(d, k)[0]] : pick3(d, k).slice(0, 2); o.plate = PLATE[(i + k) % 3]; o.calm = !!cfg.calm; o.side = cfg.side; add(kind, s + ' / ' + SN[scene] + ' / ' + o.objs[0], 'show', pal(d[0], k), s, o); }
      else { o.calm = !!cfg.calm; add(kind, s + ' / ' + SN[scene], 'scenic', pal(d[0], k), s, o); }
    }
    for (i = 0; i < 300; i++) subj('cover', i, { show: true, every: 3, calm: true });
    for (i = 0; i < 150; i++) { var sc2 = SC[(i * 3 + 1) % SC.length]; add('school', 'Banner / ' + SN[sc2] + ' ' + (Math.floor(i / SC.length) + 1), 'scenic', PN[(i * 3 + 2) % PN.length], 'Schools', { scene: sc2, calm: i % 2 === 0, deep: i % 4 === 1 }); }
    for (i = 0; i < 360; i++) subj('thumb', i, { show: true, every: 4, one: true });
    for (i = 0; i < 200; i++) subj('book', i, { show: true, every: 5, side: 'center', one: true });
    for (i = 0; i < 150; i++) subj('post', i, { show: true, every: 3 });
    for (i = 0; i < 240; i++) { var sc3 = SC[(i * 7 + 2) % SC.length]; add('bg', SN[sc3] + ' ' + (Math.floor(i / SC.length) + 1), 'scenic', PN[(i * 7 + 2) % PN.length], 'Backgrounds', { scene: sc3, deep: i % 5 === 0 }); }
    for (i = 0; i < 180; i++) subj('tile', i, { show: true, side: 'center', one: true });
    SPOTS.forEach(function (sp, j) { for (var v = 0; v < 4; v++) add('spot', sp[0] + ' ' + (v + 1), 'empty', PN[(j * 5 + v * 7) % PN.length], 'Empty states', { prop: sp[1], chip: ['bulb', 'bell', 'clock', 'sprout', 'globe', 'calendar', 'target', 'chat'][(j + v * 3) % 8], look: v, scene: SC[(j + v * 4) % SC.length] }); });
    ACH.forEach(function (a, j) { for (var v = 0; v < 4; v++) add('sticker', a[0] + ' ' + (v + 1), 'show', PN[(j * 3 + v * 5) % PN.length], 'Achievements', { objs: [a[1]], plate: PLATE[(j + v) % 3], scene: SC[(j * 2 + v * 3) % SC.length], side: 'center', tilt: v * 4 - 6, deep: v === 3 }); });
    for (i = 0; i < 420; i++) add('avatar', NAMES[i % NAMES.length] + ' ' + (Math.floor(i / NAMES.length) + 1), 'person5', PN[(i * 7 + 3) % PN.length], 'People', {});
    for (i = 0; i < 200; i++) add('avatar', PALN[i % PALN.length] + ' the pal ' + (Math.floor(i / PALN.length) + 1), 'pal', PN[(i * 5 + 1) % PN.length], 'Pals', {});
    for (i = 0; i < 120; i++) { s = S[i % S.length]; d = SUB[s]; add('avatar', s + ' mark ' + (Math.floor(i / S.length) + 1), 'glyphAv', pal(d[0], Math.floor(i / S.length) + 1), s, { glyph: d[1], scene: PATS[(i + 1) % PATS.length], deep: i % 3 === 0 }); }
    for (i = 0; i < 120; i++) subj('pathway', i, { show: true, every: 2, one: true });
    for (i = 0; i < 120; i++) subj('story', i, { show: true, every: 2, side: 'center', one: true });
    for (i = 0; i < 120; i++) { var p = PATS[i % PATS.length]; add('pattern', SN[p] + ' ' + (Math.floor(i / PATS.length) + 1), 'scenic', PN[(i * 3 + 5) % PN.length], 'Patterns', { scene: p, deep: i % 4 === 0 }); }
    for (i = 0; i < 100; i++) subj('wide', i, { show: true, every: 2 });
    for (i = 0; i < 150; i++) { var q = STRIPS[i % STRIPS.length]; add('strip', SN[q] + ' strip ' + (Math.floor(i / STRIPS.length) + 1), 'scenic', PN[(i * 5 + 4) % PN.length], 'Strips', { scene: q, deep: i % 3 === 0, side: 'right' }); }
    for (i = 0; i < 120; i++) { var wl = WALLS[i % WALLS.length]; if (i % 4 === 3) { s = S[i % S.length]; d = SUB[s]; add('wall', s + ' / ' + SN[wl] + ' wall', 'show', pal(d[0], i), s, { scene: wl, objs: [d[2][i % 3]], plate: PLATE[i % 3], side: 'center', deep: i % 2 === 0 }); } else add('wall', SN[wl] + ' wall ' + (Math.floor(i / WALLS.length) + 1), 'scenic', PN[(i * 3 + 1) % PN.length], 'Wallpapers', { scene: wl, deep: i % 3 === 0, side: 'center' }); }
    for (i = 0; i < 120; i++) { s = S[i % S.length]; d = SUB[s]; k = Math.floor(i / S.length); add('icon', s + ' icon ' + (k + 1), 'mark', pal(d[0], k), s, { glyph: d[1], look: k % 4 }); }
    cache = out; return out;
  };
  A.render = function (it, mode) { return A.make({ engine: it.engine, palette: it.palette, seed: it.seed, w: it.w, h: it.h, mode: mode, subj: it.subj, id: it.id, o: it.o, kind: it.kind }); };
})(typeof window !== 'undefined' ? window : globalThis);
