/* Writes covers.json for the code-drawn M3X art (no images are exported any more).
   Usage: node tools/art/export_m3x_manifest.js            (writes the site copy and the app copy)
   covers : [id, layout, palette, seed]  v7 `cover` pieces, ids never change. The seed is the catalog seed, so the
            same (layout, palette, seed) draws the same picture in js/m3x-art.js and in M3xEngine.kt.
   thumbs : { FAMILY: [[layout, palette, "thumb|seed|subject|layout|"] x 6] } v1 `thumb` picks, same rules as before,
            limited to the layouts both engines draw. */
var fs = require('fs'), path = require('path'), root = path.join(__dirname, '..', '..');
var EXCL = ['ribbons', 'arches', 'graph', 'net', 'stack', 'bars', 'capsules', 'cascade', 'bands', 'halftone', 'hills', 'sunset', 'rays'];
var PALS = ['azure', 'sky', 'teal', 'mint', 'amber', 'coral', 'rose', 'slate'];
var FAMS = {
  HEALTH: ['Health'], EXAM: ['Education', 'Law'], COMPUTING: ['Computer Science'], PHYSICS: ['Physics'], CHEMISTRY: ['Chemistry'],
  MATH: ['Mathematics'], BIOLOGY: ['Biology'], SOCIAL: ['Social Studies', 'Geography', 'History'], COMMERCE: ['Economics', 'Accountancy', 'Business Studies'],
  LANGUAGE: ['English', 'Nepali'], SCIENCE: ['Environment', 'Physics', 'Chemistry'], GENERAL: ['Education', 'Psychology', 'Music', 'Sociology']
};
function load(files, base) { global.window = global; global.NebArt = undefined; files.forEach(function (f) { var p = path.join(base, f); delete require.cache[require.resolve(p)]; require(p); }); return global.NebArt; }
var V1 = load(['glyphs.js', 'art-core.js', 'art-layouts-a.js', 'art-layouts-b.js', 'art-make.js'], path.join(root, 'concepts/art'));
var subs = V1.subjectNames || Object.keys(V1.subjects), subPal = {};
subs.forEach(function (s) { subPal[s] = V1.subjects[s][1]; });
var thumbs = {};
Object.keys(FAMS).forEach(function (fam) {
  var list = FAMS[fam], got = [], round = 0;
  while (got.length < 6 && round < 80) {
    list.forEach(function (name) {
      if (got.length >= 6) return;
      var i = subs.indexOf(name), o = { kind: 'thumb', seed: i * 8 + round, subject: name, mode: 'light' };
      V1.make(o); if (EXCL.indexOf(o.resolved.layout) > -1) return;
      got.push([o.resolved.layout, o.resolved.palette, 'thumb|' + o.seed + '|' + name + '|' + o.resolved.layout + '|']);
    });
    round++;
  }
  thumbs[fam] = got;
});
var N = load(['../art/glyphs.js', 'v7-glyphs.js', '../art/art-core.js', 'v7-core.js', '../art/art-layouts-a.js', '../art/art-layouts-b.js', 'v7-lay-c.js', 'v7-lay-d.js', '../art/art-make.js', 'v7-make.js', 'v7-scenes.js', 'v7-catalog.js'], path.join(root, 'concepts/art-v7'));
var covers = N.catalog().filter(function (o) { return o.kind === 'cover' && EXCL.indexOf(o.layout) < 0 && PALS.indexOf(o.palette) > -1; })
  .map(function (o) { return [o.id, o.layout, o.palette, o.seed]; });
var old = JSON.parse(fs.readFileSync(path.join(root, 'app/src/main/assets/m3x/covers.json'), 'utf8')).covers.map(function (r) { return r[0]; });
var keep = covers.filter(function (r) { return old.indexOf(r[0]) > -1; }); // ids that already exist stay, nothing new appears
var text = JSON.stringify({ covers: keep, thumbs: thumbs });
['backend_python/web/static/web/img/m3x/covers.json', 'app/src/main/assets/m3x/covers.json'].forEach(function (p) { fs.writeFileSync(path.join(root, p), text); });
console.log('covers ' + keep.length + ' (of ' + covers.length + '), layouts ' + new Set(keep.map(function (r) { return r[1]; })).size + ', bytes ' + text.length);
console.log(Object.keys(thumbs).map(function (k) { return k + ':' + thumbs[k].map(function (t) { return t[0]; }).join(','); }).join('\n'));
