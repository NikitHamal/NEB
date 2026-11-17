/* v5 catalog: deterministic named pieces (each rendered in Light and Dark). Same id gives the same art in the browser, export-svg.js and later ports. */
(function (g) {
  'use strict';
  var A = g.NebArtV5, SUB = A.SUB, S = A.SUBJECTS, cache = null;
  A.kinds = {
    avatar: { w: 256, h: 256, label: 'Profile pictures', desc: 'Frameless, clip to any shape (1:1)' }, cover: { w: 1200, h: 400, label: 'Profile covers', desc: '3:1' }, school: { w: 1200, h: 400, label: 'School banners', desc: '3:1' },
    thumb: { w: 640, h: 256, label: 'Resource thumbnails', desc: '5:2' }, book: { w: 400, h: 560, label: 'Book covers', desc: '5:7' }, post: { w: 1200, h: 630, label: 'Post headers', desc: '1.9:1' },
    bg: { w: 1600, h: 900, label: 'Page backgrounds', desc: '16:9' }, tile: { w: 512, h: 512, label: 'Collection tiles', desc: '1:1' }, spot: { w: 480, h: 360, label: 'Empty states', desc: '4:3' },
    sticker: { w: 256, h: 256, label: 'Achievement badges', desc: '1:1' }, pathway: { w: 800, h: 320, label: 'Pathways', desc: '5:2' }, lab: { w: 800, h: 360, label: 'Labs and chapters', desc: '20:9' },
    story: { w: 540, h: 960, label: 'Onboarding stories', desc: '9:16' }, pattern: { w: 600, h: 600, label: 'Patterns', desc: '1:1' }, wide: { w: 1600, h: 560, label: 'Hero banners', desc: '20:7' }
  };
  function title(s) { return s.replace(/^./, function (c) { return c.toUpperCase(); }); }
  var PAL = A.palettes.filter(function (p) { return p !== 'ink' && p !== 'stone'; }), PLATES = ['disc', 'arch', 'tile', 'cookie', 'bloom'];
  A.catalog = function () {
    if (cache) return cache;
    var out = [], n = {}, i, k, s, d, r;
    function add(kind, name, engine, palette, subj, o) { n[kind] = (n[kind] || 0) + 1; out.push({ id: kind + '-' + ('000' + n[kind]).slice(-4), kind: kind, name: name, engine: engine, palette: palette, seed: n[kind] * 7 + 3, subj: subj, o: o || {}, w: A.kinds[kind].w, h: A.kinds[kind].h }); }
    function sub(i) { s = S[i % S.length]; d = SUB[s]; k = Math.floor(i / S.length); return d; }
    function pal(base, k) { return k % 3 === 0 ? base : PAL[(PAL.indexOf(base) + 5 * (k % 4) + k) % PAL.length]; }
    function scene(kind, i, o) { sub(i); var nm = d[2][k % 3]; add(kind, s + ' / ' + title(nm), nm, pal(d[0], k), s, o); }
    function hero(kind, i, o) { sub(i); var ob = d[1][k % 3]; var oo = { obj: ob, scene: d[2][(k + 1) % 3], soft: true, plate: 'tile', side: 'right', alt: k % 2 === 1 }; for (var q in o) oo[q] = o[q]; add(kind, s + ' / ' + title(ob), 'stage', pal(d[0], k), s, oo); }
    /* profile pictures: people */
    for (i = 0; i < 480; i++) {
      r = A.rng('av' + i); var fem = i % 2 === 0, P5 = A.people, hair = r.pick(fem ? P5.HAIR_F : P5.HAIR_M), skin = r.int(0, 7), outfit = r.pick(P5.OUTFITS), acc = r.pick(P5.ACCS), hc = r.pick([0, 0, 1, 2, 2, 3, 4, 7]);
      if (hair === 'elder') hc = r.pick([5, 6]); if (hair === 'scarf') acc = r.pick(['none', 'round', 'rect']); if (outfit === 'labcoat' && acc === 'headphones') acc = 'rect';
      if (acc === 'grad' && ['long', 'wavy', 'bob', 'bun', 'braid', 'scarf', 'curly', 'elder', 'pixie'].indexOf(hair) > -1) acc = 'none';
      if (acc === 'topi') { if (fem) acc = 'none'; else hair = 'buzz'; }
      if (acc === 'bindi' && (!fem || hair === 'scarf')) acc = 'none'; if (acc === 'earring' && (!fem || hair === 'scarf')) acc = 'none';
      if (acc === 'headphones' && (hair === 'bun' || hair === 'scarf' || hair === 'curly' || hair === 'elder')) acc = 'none';
      add('avatar', A.NAMES[i % 24] + ' ' + (Math.floor(i / 24) + 1), 'person', PAL[(i * 7 + 3) % PAL.length], 'People', { skin: skin, hair: hair, hc: hc, outfit: outfit, acc: acc, expr: r.pick(['smile', 'smile', 'grin', 'calm', 'joy']), bg: P5.BGS[(i * 3 + 1) % 7], fem: fem, flip: r.chance(0.5), beard: !fem && hair !== 'buzz' && acc !== 'topi' ? r.chance(0.28) : (!fem && r.chance(0.2)), jaw: fem ? r.range(0.82, 0.98) : r.range(1, 1.18), oc: r.pick(['m', 'm', 'alt']) });
    }
    var OBJ = Object.keys(A.objects).filter(function (x) { return x !== 'search'; });
    for (i = 0; i < 72; i++) add('avatar', title(OBJ[i % OBJ.length]) + ' ' + (Math.floor(i / OBJ.length) + 1), 'stage', PAL[(i * 5 + 2) % PAL.length], 'Objects', { obj: OBJ[i % OBJ.length], plate: PLATES[i % 5], bg: i % 2 ? 's1' : 's2', platec: i % 2 ? 's2' : 'bg', scale: 0.54 });
    for (i = 0; i < 42; i++) add('avatar', 'Abstract ' + (i + 1), A.SCENES[i % 14], PAL[(i * 3 + 1) % PAL.length], 'Abstract', { alt: i % 3 === 0 });
    for (i = 0; i < 240; i++) { if (i % 3 === 0) hero('cover', i, { scale: 0.4, plate: PLATES[i % 5] }); else scene('cover', i, { bias: 0.72, alt: i % 4 === 1 }); }
    for (i = 0; i < 96; i++) { if (i % 2) hero('school', i, { plate: 'disc', scale: 0.4 }); else scene('school', i, { bias: 0.72 }); }
    for (i = 0; i < 300; i++) { if (i % 5 < 3) hero('thumb', i, { plate: PLATES[i % 5], scale: 0.46, side: i % 2 ? 'right' : 'center' }); else scene('thumb', i, { alt: i % 2 === 0 }); }
    for (i = 0; i < 160; i++) { if (i % 3) hero('book', i, { plate: 'arch', scale: 0.46, side: 'center', soft: i % 2 === 0, dy: 0.54 }); else scene('book', i, {}); }
    for (i = 0; i < 120; i++) { if (i % 2) hero('post', i, { plate: 'tile', scale: 0.4 }); else scene('post', i, { alt: i % 3 === 0 }); }
    for (i = 0; i < 140; i++) add('bg', title(A.SCENES[i % 14]) + ' ' + (Math.floor(i / 14) + 1), A.SCENES[i % 14], PAL[(i * 7 + 2) % PAL.length], 'Backgrounds', { soft: true, bias: 0.6 });
    for (i = 0; i < 150; i++) { sub(i); add('tile', s + ' / ' + title(d[1][k % 3]), 'stage', pal(d[0], k), s, { obj: d[1][k % 3], plate: PLATES[(i + k) % 5], bg: 's1', scale: 0.6 }); }
    A.SPOTS.forEach(function (sp, j) { for (var v = 0; v < 4; v++) add('spot', sp[0] + ' ' + (v + 1), 'stage', A.CALM[(j * 3 + v * 4) % A.CALM.length], 'Empty states', { obj: sp[1], mark: sp[2], plate: ['disc', 'arch', 'cookie', 'tile'][v], bg: 's1', scale: 0.52, dy: v === 1 ? 0.54 : 0.5 }); });
    A.ACH.forEach(function (a, j) { var shapes = ['seal', 'shield', 'hex', 'round', 'bloom']; for (var v = 0; v < 5; v++) add('sticker', a[0] + ' / ' + A.TIERS[v][0], 'badge', A.TIERS[v][1], 'Achievements', { obj: a[1], shape: shapes[(j + v) % 5], k: shapes[(j + v) % 5] === 'shield' ? 0.8 : 0.9 }); });
    for (i = 0; i < 80; i++) hero('pathway', i, { plate: 'disc', scale: 0.44 }); for (i = 0; i < 60; i++) hero('lab', i, { plate: PLATES[i % 5], scale: 0.44 });
    for (i = 0; i < 60; i++) { sub(i); add('story', s + ' / Story', 'stage', pal(d[0], k), s, { obj: d[1][k % 3], scene: ['ribbons', 'arches', 'rings', 'swirl'][i % 4], soft: i % 2 === 0, plate: 'cookie', scale: 0.5, dy: 0.42 }); }
    for (i = 0; i < 84; i++) add('pattern', title(A.SCENES[i % 14]) + ' ' + (Math.floor(i / 14) + 1), A.SCENES[i % 14], PAL[(i * 5 + 4) % PAL.length], 'Patterns', {});
    for (i = 0; i < 80; i++) hero('wide', i, { plate: PLATES[i % 5], scale: 0.42 });
    return (cache = out);
  };
  A.render = function (it, mode) { return A.make({ id: it.id, engine: it.engine, seed: it.seed, palette: it.palette, w: it.w, h: it.h, subj: it.subj, o: it.o, mode: mode || 'light', kind: it.kind }); };
})(typeof window !== 'undefined' ? window : globalThis);
