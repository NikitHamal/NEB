/* Writes the M3X art the app and the site draw as small optimised SVG files (vector: sharp at any size, nothing is bundled
   in the APK, the app fetches a piece once and Coil keeps it on disk).
   Usage: node tools/art/export_m3x_assets.js <out dir> [--stats]   (no npm packages needed)
   covers: v7 `cover` pieces (stable ids cover-NNN). Layouts that read as ribbons, arches, graph, net, stacks,
           bars, capsules, cascades and bands are left out. PALS limits the colours per layout.
   thumb:  v1 `thumb` pieces (concepts/art), 6 per subject family, no hills, sunset or rays.
   Light and Dark are separate files; ids and file names never change (append only).
   Optimiser: whole-number coordinates, hsl() as hex, no title/width/height, so a cover is a few KB. */
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
var jobs = [], manifest = { covers: [], thumbFamilies: {}, thumbVariants: 6 }, bytes = 0;
function hex(h, sat, l) { h = +h; sat /= 100; l /= 100; var k = function (n) { var m = (n + h / 30) % 12, a = sat * Math.min(l, 1 - l); return Math.round(255 * (l - a * Math.max(-1, Math.min(m - 3, 9 - m, 1)))); }; return '#' + [k(0), k(8), k(4)].map(function (v) { return ('0' + v.toString(16)).slice(-2); }).join(''); }
function opt(svg) {
  return svg.replace(/hsl\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*\)/g, function (_, h, s2, l) { return hex(h, +s2, +l); })
    .replace(/<title>[^<]*<\/title>/, '').replace(/ role="img"/, '').replace(/^<svg[^>]*>/, function (t) { return t.replace(/ (width|height)="\d+"/g, ''); })
    .replace(/-?\d+\.\d+/g, function (x) { var r = Math.round(parseFloat(x) * 10) / 10; return Math.abs(r) >= 100 ? String(Math.round(r)) : String(r); })
    .replace(/(\d)\.0(?=\D)/g, '$1').replace(/-0(?=[^\d.])/g, '0');
}
function enc(svg, file) { var o = opt(svg); bytes += o.length; if (!stats) { mk(path.dirname(file)); fs.writeFileSync(file, o); } return Promise.resolve(); }

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
    jobs.push(enc(V1.make(c), path.join(out, 'thumb', m, fam.toLowerCase() + '-' + v + '.svg')));
  }); });
});

var N = load(['../art/glyphs.js', 'v7-glyphs.js', '../art/art-core.js', 'v7-core.js', '../art/art-layouts-a.js', '../art/art-layouts-b.js', 'v7-lay-c.js', 'v7-lay-d.js', '../art/art-make.js', 'v7-make.js', 'v7-scenes.js', 'v7-catalog.js'], path.join(root, 'concepts/art-v7'));
var BUDGET = 70000; /* bytes per cover after optimising: the few thousand-shape covers (halftone, petal field) cost more than a screenful of the app */
var covers = N.catalog().filter(function (o) { return o.kind === 'cover' && EXCL.indexOf(o.layout) < 0 && PALS.indexOf(o.palette) > -1 && opt(N.render(o, 'light')).length <= BUDGET; });
covers.forEach(function (o) {
  manifest.covers.push([o.id, o.layout, o.palette]);
  ['light', 'dark'].forEach(function (m) { jobs.push(enc(N.render(o, m), path.join(out, 'cover', m, o.id + '.svg'))); });
});
Promise.all(jobs).then(function (s) {
  if (!stats) fs.writeFileSync(path.join(out, 'covers.json'), JSON.stringify(manifest));
  console.log('files ' + jobs.length + ', covers ' + covers.length + ', layouts ' + new Set(covers.map(function (o) { return o.layout; })).size + ', KB ' + Math.round(bytes / 1024));
});
