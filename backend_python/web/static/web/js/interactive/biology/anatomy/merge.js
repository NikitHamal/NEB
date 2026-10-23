import { THREE } from '../../core/engine.js';

export function mergeMeshes(meshes, extra = null) {
  let vcount = 0; let icount = 0;
  const geos = meshes.map((m) => {
    m.updateWorldMatrix(true, false);
    const g = m.geometry.index ? m.geometry : m.geometry.toNonIndexed();
    vcount += g.attributes.position.count;
    icount += g.index ? g.index.count : g.attributes.position.count;
    return g;
  });
  const pos = new Float32Array(vcount * 3); const nor = new Float32Array(vcount * 3);
  const part = new Float32Array(vcount);
  const idx = vcount > 65535 ? new Uint32Array(icount) : new Uint16Array(icount);
  const extras = extra ? Object.fromEntries(Object.entries(extra.attrs).map(([k, size]) => [k, new Float32Array(vcount * size)])) : {};
  const v = new THREE.Vector3(); const n = new THREE.Vector3(); const nm = new THREE.Matrix3();
  let vo = 0; let io = 0;
  geos.forEach((g, gi) => {
    const m = meshes[gi];
    nm.getNormalMatrix(m.matrixWorld);
    const P = g.attributes.position; const N = g.attributes.normal;
    const start = vo;
    for (let i = 0; i < P.count; i++) {
      v.fromBufferAttribute(P, i).applyMatrix4(m.matrixWorld);
      pos[(vo + i) * 3] = v.x; pos[(vo + i) * 3 + 1] = v.y; pos[(vo + i) * 3 + 2] = v.z;
      if (N) { n.fromBufferAttribute(N, i).applyMatrix3(nm).normalize(); nor[(vo + i) * 3] = n.x; nor[(vo + i) * 3 + 1] = n.y; nor[(vo + i) * 3 + 2] = n.z; }
      part[vo + i] = gi;
    }
    if (g.index) for (let i = 0; i < g.index.count; i++) idx[io + i] = g.index.getX(i) + vo;
    else for (let i = 0; i < P.count; i++) idx[io + i] = vo + i;
    if (extra) extra.fill(extras, m, pos, start, P.count);
    vo += P.count; io += g.index ? g.index.count : P.count;
  });
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('normal', new THREE.BufferAttribute(nor, 3));
  geo.setAttribute('part', new THREE.BufferAttribute(part, 1));
  Object.entries(extras).forEach(([k, arr]) => geo.setAttribute(k, new THREE.BufferAttribute(arr, extra.attrs[k])));
  geo.setIndex(new THREE.BufferAttribute(idx, 1));
  geo.computeBoundingSphere();
  return geo;
}

export function principalAxis(pos, start, count) {
  let cx = 0; let cy = 0; let cz = 0;
  for (let i = start; i < start + count; i++) { cx += pos[i * 3]; cy += pos[i * 3 + 1]; cz += pos[i * 3 + 2]; }
  cx /= count; cy /= count; cz /= count;
  let xx = 0; let xy = 0; let xz = 0; let yy = 0; let yz = 0; let zz = 0;
  for (let i = start; i < start + count; i++) {
    const x = pos[i * 3] - cx; const y = pos[i * 3 + 1] - cy; const z = pos[i * 3 + 2] - cz;
    xx += x * x; xy += x * y; xz += x * z; yy += y * y; yz += y * z; zz += z * z;
  }
  let a = [0.3, 1, 0.2];
  for (let it = 0; it < 24; it++) {
    const b = [xx * a[0] + xy * a[1] + xz * a[2], xy * a[0] + yy * a[1] + yz * a[2], xz * a[0] + yz * a[1] + zz * a[2]];
    const l = Math.hypot(...b) || 1;
    a = [b[0] / l, b[1] / l, b[2] / l];
  }
  return { c: [cx, cy, cz], axis: a };
}
