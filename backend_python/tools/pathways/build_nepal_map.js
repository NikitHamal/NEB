#!/usr/bin/env node
/* Builds nepal_map.json: the official (chuche, May 2020) boundary of Nepal, 77 districts, 7 provinces.
   Source: MoFAGA district boundaries via github.com/l3lackcurtains/nepali-geo-pro-max (MIT),
   file scripts/source-districts-chuche.geojson.
   Usage (needs `npm i mapshaper polylabel@1` in a scratch folder, not in the repo):
     curl -O .../source-districts-chuche.geojson   (save as d.geojson)
     npx mapshaper d.geojson -simplify visvalingam 28% keep-shapes -o simp.json format=geojson
     npx mapshaper simp.json -dissolve PROVINCE -o prov.json format=geojson
     npx mapshaper simp.json -dissolve -o nat.json format=geojson
     node build_nepal_map.js <scratch folder> <out.json>
   Output: integer grid, x to the right, y down, width W. Rings are delta encoded: [x0, y0, dx1, dy1, ...].
   Same file is read by the web map (static/web/data/nepal_map.json) and Android (res/raw/nepal_map.json). */
const fs = require('fs');
const dir = process.argv[2], out = process.argv[3];
const polylabel = require(dir + '/node_modules/polylabel');
const read = (f) => JSON.parse(fs.readFileSync(dir + '/' + f, 'utf8'));
const simp = read('simp.json'), prov = read('prov.json'), nat = read('nat.json');
const NAMES = { 'TEHRATHUM': 'Terhathum', 'DHANUSA': 'Dhanusha', 'KAVREPALANCHOWK': 'Kavrepalanchok', 'NAWALPUR': 'Nawalparasi East',
  'PARASI': 'Nawalparasi West', 'EASTERN RUKUM': 'Rukum East', 'WESTERN RUKUM': 'Rukum West' };
const title = (s) => s.toLowerCase().replace(/\b[a-z]/g, (m) => m.toUpperCase());
const polys = (g) => g.type === 'Polygon' ? [g.coordinates] : g.type === 'MultiPolygon' ? g.coordinates : [];
let minX = 1e9, maxX = -1e9, minY = 1e9, maxY = -1e9;
simp.features.forEach((f) => polys(f.geometry).forEach((p) => p[0].forEach(([x, y]) => {
  minX = Math.min(minX, x); maxX = Math.max(maxX, x); minY = Math.min(minY, y); maxY = Math.max(maxY, y);
})));
const k = Math.cos(((minY + maxY) / 2) * Math.PI / 180);
const W = 4000, S = W / ((maxX - minX) * k), H = Math.round((maxY - minY) * S);
const px = (lon) => Math.round((lon - minX) * k * S), py = (lat) => Math.round((maxY - lat) * S);
const ring = (r) => {
  const pts = []; r.forEach(([x, y]) => { const a = [px(x), py(y)]; const l = pts[pts.length - 1]; if (!l || l[0] !== a[0] || l[1] !== a[1]) pts.push(a); });
  if (pts.length > 1 && pts[0][0] === pts[pts.length - 1][0] && pts[0][1] === pts[pts.length - 1][1]) pts.pop();
  if (pts.length < 3) return null;
  const o = [pts[0][0], pts[0][1]];
  for (let i = 1; i < pts.length; i++) o.push(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
  return o;
};
const rings = (g) => polys(g).flatMap((p) => p.map(ring).filter(Boolean));
const d = simp.features.map((f) => {
  const raw = f.properties.DISTRICT; const n = NAMES[raw] || title(raw);
  let best = null, area = -1;
  polys(f.geometry).forEach((p) => { const a = Math.abs(p[0].reduce((s, c, i, r) => { const q = r[(i + 1) % r.length]; return s + c[0] * q[1] - q[0] * c[1]; }, 0)); if (a > area) { area = a; best = p; } });
  const pl = polylabel(best.map((r) => r.map(([x, y]) => [px(x), py(y)])), 4);
  return { n, p: f.properties.PROVINCE - 1, hq: title(f.properties.HQ || ''), c: [Math.round(pl[0]), Math.round(pl[1])], r: rings(f.geometry) };
});
const pv = []; prov.features.forEach((f) => { pv[f.properties.PROVINCE - 1] = rings(f.geometry); });
const natGeoms = nat.type === 'GeometryCollection' ? nat.geometries : nat.features.map((f) => f.geometry);
const o = natGeoms.flatMap(rings);
fs.writeFileSync(out, JSON.stringify({ v: 1, w: W, h: H, d, pv, o }));
console.log('districts', d.length, 'size', W + 'x' + H, 'bytes', fs.statSync(out).size);
