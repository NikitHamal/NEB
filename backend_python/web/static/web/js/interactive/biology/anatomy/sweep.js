import { THREE } from '../../core/engine.js';

export function sweepTube(points, radius, opts = {}) {
  const curve = new THREE.CatmullRomCurve3(points.map((p) => (p.isVector3 ? p : new THREE.Vector3(...p))), false, 'centripetal');
  const segs = opts.segments ?? Math.max(24, points.length * 10);
  const radial = opts.radial ?? 14;
  const frames = curve.computeFrenetFrames(segs, false);
  const rf = typeof radius === 'function' ? radius : () => radius;
  const pos = []; const nor = []; const tt = []; const idx = [];
  const P = new THREE.Vector3(); const N = new THREE.Vector3();
  for (let i = 0; i <= segs; i++) {
    const t = i / segs;
    curve.getPointAt(t, P);
    for (let j = 0; j <= radial; j++) {
      const a = j / radial * Math.PI * 2;
      const r = rf(t, a);
      N.copy(frames.normals[i]).multiplyScalar(Math.cos(a)).addScaledVector(frames.binormals[i], Math.sin(a)).normalize();
      pos.push(P.x + N.x * r, P.y + N.y * r, P.z + N.z * r);
      nor.push(N.x, N.y, N.z);
      tt.push(t);
    }
  }
  for (let i = 0; i < segs; i++) {
    for (let j = 0; j < radial; j++) {
      const a = i * (radial + 1) + j; const b = a + radial + 1;
      idx.push(a, b, a + 1, b, b + 1, a + 1);
    }
  }
  if (opts.caps !== false) {
    for (const end of [0, 1]) {
      const i = end ? segs : 0;
      curve.getPointAt(end, P);
      const T = frames.tangents[i].clone().multiplyScalar(end ? 1 : -1);
      const center = pos.length / 3;
      pos.push(P.x, P.y, P.z); nor.push(T.x, T.y, T.z); tt.push(end);
      const ring = i * (radial + 1);
      for (let j = 0; j < radial; j++) {
        if (end) idx.push(center, ring + j, ring + j + 1);
        else idx.push(center, ring + j + 1, ring + j);
      }
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  geo.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
  geo.setAttribute('along', new THREE.Float32BufferAttribute(tt, 1));
  geo.setIndex(idx);
  if (opts.recompute) geo.computeVertexNormals();
  return geo;
}

export function mergeGeometries(geos) {
  let v = 0; let ic = 0;
  geos.forEach((g) => { v += g.attributes.position.count; ic += g.index.count; });
  const names = Object.keys(geos[0].attributes);
  const out = {};
  names.forEach((n) => { out[n] = new Float32Array(v * geos[0].attributes[n].itemSize); });
  const idx = new Uint32Array(ic);
  let vo = 0; let io = 0;
  geos.forEach((g) => {
    names.forEach((n) => out[n].set(g.attributes[n].array, vo * g.attributes[n].itemSize));
    for (let i = 0; i < g.index.count; i++) idx[io + i] = g.index.array[i] + vo;
    vo += g.attributes.position.count; io += g.index.count;
    g.dispose();
  });
  const geo = new THREE.BufferGeometry();
  names.forEach((n) => geo.setAttribute(n, new THREE.BufferAttribute(out[n], geos[0].attributes[n].itemSize)));
  geo.setIndex(new THREE.BufferAttribute(idx, 1));
  return geo;
}
