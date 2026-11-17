/* Export every v3 piece (Light + Dark) to concepts/art-v3/svg/{light,dark}/<kind>/<id>.svg and write catalog.json. Fails on NaN, undefined, gradients, filters. */
var fs = require('fs'), path = require('path');
global.window = global;
require('../art/glyphs.js');
['v3-core', 'v3-scenes-a', 'v3-scenes-b', 'v3-patterns', 'v3-objects-a', 'v3-objects-b', 'v3-still', 'v3-avatars', 'v3-make', 'v3-catalog'].forEach(function (f) { require('./' + f + '.js'); });
var A = global.NebArtV3, cat = A.catalog(), base = path.join(__dirname, 'svg'), bad = 0, bytes = 0;
['light', 'dark'].forEach(function (mode) {
  Object.keys(A.kinds).forEach(function (k) { fs.mkdirSync(path.join(base, mode, k), { recursive: true }); });
  cat.forEach(function (it) {
    var svg = A.render(it, mode);
    if (/NaN|undefined|Gradient|filter=|<image|<text/.test(svg)) { bad++; console.error('BAD', mode, it.id); }
    bytes += svg.length; fs.writeFileSync(path.join(base, mode, it.kind, it.id + '.svg'), svg + '\n');
  });
});
fs.writeFileSync(path.join(__dirname, 'catalog.json'), JSON.stringify(cat.map(function (i) { return { id: i.id, kind: i.kind, name: i.name, subject: i.subj, engine: i.engine, palette: i.palette, w: i.w, h: i.h }; })));
console.log('pieces', cat.length, 'svgs', cat.length * 2, 'MB', (bytes / 1e6).toFixed(1), 'bad', bad);
