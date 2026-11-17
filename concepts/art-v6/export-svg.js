/* Export check for M3X Art Library v6.
   node concepts/art-v6/export-svg.js          validates every piece (Light + Dark), writes catalog.json
   node concepts/art-v6/export-svg.js --svg    also writes svg/{light,dark}/<kind>/<id>.svg (git-ignored, regenerate any time)
   Fails on NaN, undefined, gradients, filters, images, text, shadows. Same id gives the same art everywhere. */
var fs = require('fs'), path = require('path');
global.window = global;
var R = path.join(__dirname, '..');
require(R + '/art/glyphs.js'); require(R + '/art-v3/v3-core.js');
['core', 'objects-a', 'objects-b', 'catalog'].forEach(function (f) { require(R + '/art-v4/v4-' + f + '.js'); });
['core', 'scenes-a', 'scenes-b', 'pals', 'stage', 'people', 'avatars', 'catalog'].forEach(function (f) { require('./v6-' + f + '.js'); });
var A = global.NebArtV6, cat = A.catalog(), base = path.join(__dirname, 'svg'), bad = 0, bytes = 0, big = 0, writeSvg = process.argv.indexOf('--svg') > -1, perKind = {};
['light', 'dark'].forEach(function (mode) {
  if (writeSvg) Object.keys(A.kinds).forEach(function (k) { fs.mkdirSync(path.join(base, mode, k), { recursive: true }); });
  cat.forEach(function (it) {
    var svg;
    try { svg = A.render(it, mode); } catch (e) { bad++; console.error('THROW', mode, it.id, e.message); return; }
    if (/NaN|undefined|Gradient|filter=|<image|<text|box-shadow|drop-shadow/.test(svg)) { bad++; console.error('BAD', mode, it.id); }
    if (svg.length > 400000) big++;
    bytes += svg.length; if (mode === 'light') perKind[it.kind] = (perKind[it.kind] || 0) + 1;
    if (writeSvg) fs.writeFileSync(path.join(base, mode, it.kind, it.id + '.svg'), svg + '\n');
  });
});
fs.writeFileSync(path.join(__dirname, 'catalog.json'), JSON.stringify(cat.map(function (i) { return { id: i.id, kind: i.kind, name: i.name, subject: i.subj, engine: i.engine, palette: i.palette, w: i.w, h: i.h }; })));
console.log('pieces', cat.length, 'svgs', cat.length * 2, 'MB', (bytes / 1e6).toFixed(1), 'over400k', big, 'bad', bad, JSON.stringify(perKind));
process.exit(bad ? 1 : 0);
