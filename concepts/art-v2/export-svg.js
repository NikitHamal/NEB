/* Export all 1,108 pieces (2,216 Light + Dark SVGs) to concepts/art-v2/svg/{light,dark}/<kind>/<id>.svg */
var fs = require('fs'), path = require('path');
global.window = global;
require('../art/glyphs.js');
require('./v2-core.js');
require('./v2-scenes-sci.js');
require('./v2-scenes-hum.js');
require('./v2-scenes-extra.js');
require('./v2-layouts-m3x.js');
require('./v2-layouts-ui.js');
require('./v2-catalog.js');

var V = global.NebArtV2, cat = V.catalog(), base = path.join(__dirname, 'svg');
['light', 'dark'].forEach(function (mode) {
  Object.keys(V.kinds).forEach(function (k) {
    fs.mkdirSync(path.join(base, mode, k), { recursive: true });
  });
  cat.forEach(function (item) {
    var c = {}; for (var k in item) c[k] = item[k];
    c.mode = mode;
    var svg = V.make(c);
    fs.writeFileSync(path.join(base, mode, item.kind, item.id + '.svg'), svg + '\n');
  });
});
console.log('Exported', cat.length * 2, 'SVGs to', base);
