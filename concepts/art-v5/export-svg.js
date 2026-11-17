/* Export check for M3X Art Library v5.
   node concepts/art-v5/export-svg.js          validates every piece (Light + Dark), writes catalog.json
   node concepts/art-v5/export-svg.js --svg    also writes svg/{light,dark}/<kind>/<id>.svg (git-ignored)
   Fails on NaN, undefined, gradients, filters, images, text, shadows. Same id gives the same art everywhere. */
var fs = require('fs'), path = require('path');
global.window = global;
['core', 'face', 'hair', 'people', 'objects-a', 'objects-b', 'scenes', 'stage', 'data', 'catalog'].forEach(function (f) { require('./v5-' + f + '.js'); });
var A = global.NebArtV5, cat = A.catalog(), base = path.join(__dirname, 'svg'), bad = 0, bytes = 0, writeSvg = process.argv.indexOf('--svg') > -1, perKind = {}, ids = {};
['light', 'dark'].forEach(function (mode) {
  if (writeSvg) Object.keys(A.kinds).forEach(function (k) { fs.mkdirSync(path.join(base, mode, k), { recursive: true }); });
  cat.forEach(function (it) {
    if (ids[it.id] && mode === 'light') { bad++; console.error('DUP', it.id); } ids[it.id] = 1;
    var svg = A.render(it, mode);
    if (/NaN|undefined|Gradient|filter=|<image|<text|box-shadow|drop-shadow/.test(svg)) { bad++; console.error('BAD', mode, it.id); }
    bytes += svg.length; perKind[it.kind] = (perKind[it.kind] || 0) + (mode === 'light' ? 1 : 0);
    if (writeSvg) fs.writeFileSync(path.join(base, mode, it.kind, it.id + '.svg'), svg + '\n');
  });
});
fs.writeFileSync(path.join(__dirname, 'catalog.json'), JSON.stringify(cat.map(function (i) { return { id: i.id, kind: i.kind, name: i.name, subject: i.subj, engine: i.engine, palette: i.palette, w: i.w, h: i.h }; })));
console.log('pieces', cat.length, 'svgs', cat.length * 2, 'MB', (bytes / 1e6).toFixed(1), 'bad', bad, JSON.stringify(perKind));
process.exit(bad ? 1 : 0);
