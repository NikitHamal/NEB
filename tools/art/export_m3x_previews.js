/* Small WebP previews of the M3X art, for pickers and lists (the full piece stays a vector SVG).
   A cover tile in the picker is ~200 px wide, a resource thumbnail ~160 px: decoding a 60 KB SVG for each is the slow
   part, a 3 KB WebP is not. Previews are fetched lazily (only the tiles on screen), never bundled in the APK.
   Usage: NODE_PATH=<dir with sharp> node tools/art/export_m3x_previews.js [base dir]
   Reads  <base>/cover/<light|dark>/<id>.svg  and  <base>/thumb/<light|dark>/<family>-<n>.svg
   Writes <base>/cover/prev/<light|dark>/<id>.webp (480x160) and <base>/thumb/prev/<light|dark>/<name>.webp (480x192). */
var fs = require('fs'), path = require('path'), sharp = require('sharp');
var base = process.argv[2] || path.join(__dirname, '..', '..', 'backend_python/web/static/web/img/m3x');
var jobs = [], bytes = 0, files = 0;
function one(src, dst, w, h) {
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  return sharp(src, { density: 144 }).resize(w, h, { fit: 'cover' }).webp({ quality: 72, effort: 5, smartSubsample: true }).toBuffer()
    .then(function (b) { fs.writeFileSync(dst, b); bytes += b.length; files++; });
}
['cover', 'thumb'].forEach(function (kind) {
  var w = 480, h = kind === 'cover' ? 160 : 192;
  ['light', 'dark'].forEach(function (mode) {
    var dir = path.join(base, kind, mode);
    fs.readdirSync(dir).filter(function (f) { return /\.svg$/.test(f); }).forEach(function (f) {
      jobs.push(function () { return one(path.join(dir, f), path.join(base, kind, 'prev', mode, f.replace(/\.svg$/, '.webp')), w, h); });
    });
  });
});
var i = 0, running = 0, POOL = 4;
(function pump() {
  while (running < POOL && i < jobs.length) { running++; jobs[i++]().then(function () { running--; pump(); }); }
  if (!running && i >= jobs.length) console.log('previews ' + files + ', KB ' + Math.round(bytes / 1024) + ', avg ' + Math.round(bytes / files) + ' B');
})();
