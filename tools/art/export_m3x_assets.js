/* Ships the M3X art used by the app and the site as small WebP files.
   Usage: NODE_PATH=<dir with sharp> node tools/art/export_m3x_assets.js <out dir> [--stats]
   covers: v7 `cover` pieces (stable ids cover-NNN). Layouts that read as ribbons, arches, graph, net, stacks,
           bars, capsules, cascades and bands are left out. PALS limits the colours per layout.
   thumb:  v1 `thumb` pieces (concepts/art), 6 per subject family, no hills, sunset or rays.
   Light and Dark are separate files; ids and file names never change (append only). */
var fs = require('fs'), path = require('path'), root = path.join(__dirname, '..', '..');
var out = process.argv[2], stats = process.argv.indexOf('--stats') > -1;
var EXCL = ['ribbons', 'arches', 'graph', 'net', 'stack', 'bars', 'capsules', 'cascade', 'bands'];
var PALS = ['azure', 'sky', 'teal', 'mint', 'amber', 'coral', 'rose', 'slate'];
var FAMS = {
  HEALTH: ['Health'], EXAM: ['Education', 'Law'], COMPUTING: ['Computer Science'], PHYSICS: ['Physics'], CHEMISTRY: ['Chemistry'],
  MATH: ['Mathematics'], BIOLOGY: ['Biology'], SOCIAL: ['Social Studies', 'Geography', 'History'], COMMERCE: ['Economics', 'Accountancy', 'Business Studies'],
  LANGUAGE: ['English', 'Nepali'], SCIENCE: ['Environment', 'Physics', 'Chemistry'], GENERAL: ['Education', 'Psychology', 'Music', 'Sociology']
};
function load(files, base) { global.window = global; global.NebArt = undefined; files.forEach(function (f) { var p = path.join(base, f); delete require.cache[require.resolve(p)]; require(p); }); return global.NebArt; }
function mk(p) { fs.mkdirSync(p, { recursive: true }); }
var sharp = require('sharp'), jobs = [], manifest = { covers: [], thumbFamilies: {}, thumbVariants: 6 }, bytes = 0;
function enc(svg, w, h, q, file) { return sharp(Buffer.from(svg), { density: 96 }).resize(w, h).webp({ quality: q, effort: 6 }).toBuffer().then(function (b) { bytes += b.length; if (!stats) { mk(path.dirname(file)); fs.writeFileSync(file, b); } return b.length; }); }

var V1 = load(['glyphs.js', 'art-core.js', 'art-layouts-a.js', 'art-layouts-b.js', 'art-make.js'], path.join(root, 'concepts/art'));
var BAN1 = { hills: 1, sunset: 1, rays: 1 }, subs = V1.subjectNames || Object.keys(V1.subjects);
Object.keys(FAMS).forEach(function (fam) {
  var list = FAMS[fam], got = [], round = 0;
  while (got.length < 6 && round < 8) {
    list.forEach(function (name) {
      if (got.length >= 6) return;
      var i = subs.indexOf(name), o = { kind: 'thumb', seed: i * 8 + round, subject: name, mode: 'light' };
      V1.make(o); if (BAN1[o.resolved.layout]) return;
      got.push(o);
    });
    round++;
  }
  manifest.thumbFamilies[fam] = got.map(function (o) { return o.subject + '#' + o.seed + ':' + o.resolved.layout; });
  got.forEach(function (o, v) { ['light', 'dark'].forEach(function (m) {
    var c = { kind: 'thumb', seed: o.seed, subject: o.subject, mode: m };
    jobs.push(enc(V1.make(c), 448, 179, 64, path.join(out, 'thumb', m, fam.toLowerCase() + '-' + v + '.webp')));
  }); });
});

var N = load(['../art/glyphs.js', 'v7-glyphs.js', '../art/art-core.js', 'v7-core.js', '../art/art-layouts-a.js', '../art/art-layouts-b.js', 'v7-lay-c.js', 'v7-lay-d.js', '../art/art-make.js', 'v7-make.js', 'v7-scenes.js', 'v7-catalog.js'], path.join(root, 'concepts/art-v7'));
var covers = N.catalog().filter(function (o) { return o.kind === 'cover' && EXCL.indexOf(o.layout) < 0 && PALS.indexOf(o.palette) > -1; });
covers.forEach(function (o) {
  manifest.covers.push([o.id, o.layout, o.palette]);
  ['light', 'dark'].forEach(function (m) { jobs.push(enc(N.render(o, m), 640, 214, 60, path.join(out, 'cover', m, o.id + '.webp'))); });
});
Promise.all(jobs).then(function (s) {
  if (!stats) fs.writeFileSync(path.join(out, 'covers.json'), JSON.stringify(manifest));
  console.log('files ' + jobs.length + ', covers ' + covers.length + ', layouts ' + new Set(covers.map(function (o) { return o.layout; })).size + ', KB ' + Math.round(bytes / 1024));
});
