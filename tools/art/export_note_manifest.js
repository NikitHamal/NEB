/* Writes app/src/main/assets/m3x/notes.json: the 72 Android note covers (v7 kind `note`, android = true) as [layout, palette, seed].
   Cover index 41 + position. Order is fixed: ids and stored note covers depend on it. Usage: node tools/art/export_note_manifest.js */
var fs = require('fs'), path = require('path'), root = path.join(__dirname, '..', '..'), v7 = path.join(root, 'concepts', 'art-v7');
global.window = global;
['../art/glyphs.js', 'v7-glyphs.js', '../art/art-core.js', 'v7-core.js', '../art/art-layouts-a.js', '../art/art-layouts-b.js', 'v7-lay-c.js', 'v7-lay-d.js', '../art/art-make.js', 'v7-make.js', 'v7-scenes.js', 'v7-catalog.js']
  .forEach(function (f) { require(path.join(v7, f)); });
var list = global.NebArt.catalog().filter(function (o) { return o.kind === 'note' && o.android; });
var out = path.join(root, 'app', 'src', 'main', 'assets', 'm3x', 'notes.json');
fs.writeFileSync(out, JSON.stringify(list.map(function (o) { return [o.layout, o.palette, o.seed]; })));
console.log(list.length + ' note covers -> ' + out);
