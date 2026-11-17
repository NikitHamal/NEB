/* Node exporter. Usage: node export-svg.js [--svg] [--check] [--android OUT_DIR]
   Always writes catalog.json (ids, kinds, seeds). --svg writes svg/{light,dark}/<kind>/<id>.svg (large, not committed).
   --android writes note covers as WebP (needs sharp: npm i sharp in a scratch dir and set NODE_PATH). */
var fs = require('fs'), path = require('path'), here = __dirname, args = process.argv.slice(2);
global.window = global;
['../art/glyphs.js', 'v7-glyphs.js', '../art/art-core.js', 'v7-core.js', '../art/art-layouts-a.js', '../art/art-layouts-b.js', 'v7-lay-c.js', 'v7-lay-d.js', '../art/art-make.js', 'v7-make.js', 'v7-scenes.js', 'v7-catalog.js']
  .forEach(function (f) { require(path.join(here, f)); });
var N = global.NebArt, cat = N.catalog(), bad = 0, n = 0;
function mk(p) { fs.mkdirSync(p, { recursive: true }); }
function ok(svg) { return svg.indexOf('NaN') < 0 && svg.indexOf('undefined') < 0 && /^<svg[\s\S]*<\/svg>$/.test(svg); }
cat.forEach(function (o) { ['light', 'dark'].forEach(function (m) { var s = N.render(o, m); n++; if (!ok(s)) { bad++; if (bad < 6) console.log('BAD', o.id, m); } }); });
var by = {}; cat.forEach(function (o) { by[o.kind] = (by[o.kind] || 0) + 1; });
fs.writeFileSync(path.join(here, 'catalog.json'), JSON.stringify(cat.map(function (o) { return { id: o.id, kind: o.kind, seed: o.seed, layout: o.layout, palette: o.palette, subject: o.subject, glyph: o.glyph, variant: o.variant, tag: o.tag }; })));
console.log(cat.length + ' pieces, ' + n + ' renders, ' + bad + ' bad', JSON.stringify(by));
if (args.indexOf('--svg') > -1) cat.forEach(function (o) { ['light', 'dark'].forEach(function (m) { var d = path.join(here, 'svg', m, o.kind); mk(d); fs.writeFileSync(path.join(d, o.id + '.svg'), N.render(o, m)); }); });
var ai = args.indexOf('--android');
if (ai > -1) {
  var sharp = require('sharp'), out = args[ai + 1], list = cat.filter(function (o) { return o.kind === 'note' && o.android; });
  Promise.all(list.map(function (o, i) {
    var name = 'nc_' + ('00' + (i + 1)).slice(-3);
    return Promise.all(['light', 'dark'].map(function (m) {
      mk(path.join(out, m));
      return sharp(Buffer.from(N.render(o, m)), { density: 96 }).resize(720, 320).webp({ quality: 82 }).toFile(path.join(out, m, name + '.webp'));
    }));
  })).then(function () { console.log('android note covers: ' + list.length); });
}
process.exitCode = bad ? 1 : 0;
