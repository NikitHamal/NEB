import { THREE } from './engine.js';

// Draw-call batching for the procedural biology models.
//
// The model builders emit hundreds of individually-transformed primitives, which means
// hundreds of draw calls per frame. This module collapses them into one merged buffer per
// material without changing what is drawn: every source vertex is transformed by its own
// world matrix and written into a single geometry that keeps the same material.
//
// Opaque geometry is always merged - it is order-independent, so the result is bit-identical.
// Transparent geometry is merged only for small, plentiful pieces, so large glassware keeps
// its per-object depth sorting and cannot develop sorting artefacts.

const _pos = new THREE.Vector3();
const _quat = new THREE.Quaternion();
const _scale = new THREE.Vector3();
const _inv = new THREE.Matrix4();
const _rel = new THREE.Matrix4();
const KEEP_ATTRS = ['position', 'normal', 'uv'];

// Flat panels (boxes/planes/circles) are deliberately excluded from the organic
// displacement pass, so they must never share a merged buffer with curved geometry.
const FLAT_GEOMETRY = ['BoxGeometry', 'PlaneGeometry', 'CircleGeometry'];
function geometryClass(geo) {
  const type = (geo && geo.type) || '';
  for (const flat of FLAT_GEOMETRY) if (type.includes(flat)) return 'flat';
  return 'curved';
}

function materialSignature(m, geo) {
  if (!m) return null;
  const tex = (t) => (t && t.uuid) || '0';
  return [
    geometryClass(geo),
    m.type,
    m.vertexColors ? 'v' : '-',
    m.flatShading ? 'f' : 's',
    m.color ? m.color.getHexString() : 'x',
    tex(m.map), tex(m.normalMap), tex(m.roughnessMap), tex(m.emissiveMap), tex(m.alphaMap),
    Number(m.opacity).toFixed(3),
    m.transparent ? 1 : 0,
    m.side,
    Number(m.roughness).toFixed(3),
    Number(m.metalness).toFixed(3),
    m.emissive ? m.emissive.getHexString() : 'x',
    Number(m.emissiveIntensity).toFixed(3),
    m.depthWrite === false ? 0 : 1,
    m.alphaTest || 0,
  ].join('~');
}

function worldRadius(geo, matrix) {
  if (!geo.boundingSphere) geo.computeBoundingSphere();
  const r = geo.boundingSphere ? geo.boundingSphere.radius : 0;
  matrix.decompose(_pos, _quat, _scale);
  return r * Math.max(_scale.x, _scale.y, _scale.z);
}

function mergeGeometries(entries) {
  let totalV = 0;
  let totalI = 0;
  const prepared = [];
  const shared = new Set();
  const seen = new Set();
  for (const entry of entries) {
    if (seen.has(entry.geo.uuid)) shared.add(entry.geo.uuid);
    seen.add(entry.geo.uuid);
  }

  for (const entry of entries) {
    // Source geometries are owned by this call (they are disposed once merged), so a
    // geometry used once can be transformed in place. A geometry shared by several entries
    // must be cloned for every entry, including the first: in-place mutation would corrupt
    // the copies that follow.
    let g = entry.geo;
    if (shared.has(g.uuid)) g = g.clone();
    const count = g.attributes.position.count;
    if (!g.attributes.uv) {
      g.setAttribute('uv', new THREE.BufferAttribute(new Float32Array(count * 2), 2));
    }
    if (!g.attributes.normal) g.computeVertexNormals();
    for (const name of Object.keys(g.attributes)) {
      if (KEEP_ATTRS.indexOf(name) === -1) g.deleteAttribute(name);
    }
    g.applyMatrix4(entry.matrix);
    const iCount = g.index ? g.index.count : count;
    prepared.push({ g, count, iCount, owned: g !== entry.geo });
    totalV += count;
    totalI += iCount;
  }

  const position = new Float32Array(totalV * 3);
  const normal = new Float32Array(totalV * 3);
  const uv = new Float32Array(totalV * 2);
  const index = totalV > 65535 ? new Uint32Array(totalI) : new Uint16Array(totalI);

  let vo = 0;
  let io = 0;
  for (const p of prepared) {
    position.set(p.g.attributes.position.array, vo * 3);
    normal.set(p.g.attributes.normal.array, vo * 3);
    uv.set(p.g.attributes.uv.array, vo * 2);
    if (p.g.index) {
      const src = p.g.index.array;
      for (let i = 0; i < src.length; i++) index[io + i] = src[i] + vo;
    } else {
      for (let i = 0; i < p.iCount; i++) index[io + i] = i + vo;
    }
    vo += p.count;
    io += p.iCount;
    if (p.owned) p.g.dispose();
  }

  const out = new THREE.BufferGeometry();
  out.setAttribute('position', new THREE.BufferAttribute(position, 3));
  out.setAttribute('normal', new THREE.BufferAttribute(normal, 3));
  out.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
  out.setIndex(new THREE.BufferAttribute(index, 1));
  out.computeBoundingSphere();
  return out;
}

function mergeLines(entries) {
  let total = 0;
  const prepared = [];
  for (const entry of entries) {
    const g = entry.geo;
    const pos = g.attributes.position;
    if (!pos) continue;
    const segments = g.index ? g.index.count : pos.count;
    if (segments < 2) continue;
    prepared.push({ g, matrix: entry.matrix, count: pos.count });
    total += (pos.count - 1) * 2;
  }
  if (!prepared.length) return null;

  const out = new Float32Array(total * 3);
  let w = 0;
  for (const p of prepared) {
    const src = p.g.attributes.position;
    const idx = p.g.index;
    const n = idx ? idx.count : src.count;
    for (let i = 0; i < n - 1; i++) {
      const a = idx ? idx.getX(i) : i;
      const b = idx ? idx.getX(i + 1) : i + 1;
      _pos.set(src.getX(a), src.getY(a), src.getZ(a)).applyMatrix4(p.matrix);
      out[w] = _pos.x; out[w + 1] = _pos.y; out[w + 2] = _pos.z;
      _pos.set(src.getX(b), src.getY(b), src.getZ(b)).applyMatrix4(p.matrix);
      out[w + 3] = _pos.x; out[w + 4] = _pos.y; out[w + 5] = _pos.z;
      w += 6;
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(out.subarray(0, w), 3));
  geo.computeBoundingSphere();
  return geo;
}

/**
 * Merge every batchable mesh in `root` that shares an equivalent material.
 * @param {THREE.Object3D} root
 * @param {{ minGroup?: number, transparentMaxRadius?: number, mergeLines?: boolean, disposeSources?: boolean, pick?: boolean }} opts
 * @returns {{ mergedMeshes: number, mergedLines: number, drawCallsSaved: number, merged: THREE.Mesh[] }}
 */
export function batchStaticGeometry(root, opts = {}) {
  const merged = [];
  const minGroup = opts.minGroup ?? 2;
  const transparentMaxRadius = opts.transparentMaxRadius ?? 0.9;
  const shouldMergeLines = opts.mergeLines !== false;
  const disposeSources = opts.disposeSources !== false;

  root.updateMatrixWorld(true);
  _inv.copy(root.matrixWorld).invert();

  const meshGroups = new Map();
  const lineGroups = new Map();
  const meshSources = [];
  const lineSources = [];

  root.traverse((obj) => {
    if (obj === root) return;
    if (obj.userData && (obj.userData.noBatch || obj.userData.keepSeparate)) return;

    if (obj.isMesh && !obj.isInstancedMesh && obj.geometry && obj.geometry.attributes.position) {
      const sig = materialSignature(obj.material, obj.geometry);
      if (!sig) return;
      _rel.multiplyMatrices(_inv, obj.matrixWorld);
      const entry = { obj, geo: obj.geometry, matrix: _rel.clone(), radius: worldRadius(obj.geometry, obj.matrixWorld) };
      if (!meshGroups.has(sig)) meshGroups.set(sig, []);
      meshGroups.get(sig).push(entry);
      meshSources.push(entry);
      return;
    }
    if (shouldMergeLines && obj.isLine && !obj.isLineSegments && obj.geometry && obj.geometry.attributes.position) {
      const sig = materialSignature(obj.material);
      if (!sig) return;
      _rel.multiplyMatrices(_inv, obj.matrixWorld);
      const entry = { obj, geo: obj.geometry, matrix: _rel.clone() };
      if (!lineGroups.has(sig)) lineGroups.set(sig, []);
      lineGroups.get(sig).push(entry);
      lineSources.push(entry);
    }
  });

  let mergedMeshes = 0;
  let drawCallsSaved = 0;

  for (const [, entries] of meshGroups) {
    if (entries.length < minGroup) continue;
    const representative = entries[0].obj.material;
    const transparent = !!(representative && representative.transparent);
    if (transparent) {
      if (entries.length < 3) continue;
      if (entries.some((e) => e.radius > transparentMaxRadius)) continue;
    }
    const geo = mergeGeometries(entries);
    const mesh = new THREE.Mesh(geo, representative);
    mesh.name = 'batched';
    mesh.userData.mergedCount = entries.length;
    mesh.userData.mergeClass = geometryClass(entries[0].geo);
    mesh.castShadow = entries.some((e) => e.obj.castShadow);
    mesh.receiveShadow = entries.some((e) => e.obj.receiveShadow);
    if (transparent) mesh.renderOrder = entries[0].obj.renderOrder || 0;
    if (opts.pick) buildPickMap(mesh, entries);
    root.add(mesh);
    for (const e of entries) {
      if (e.obj.parent) e.obj.parent.remove(e.obj);
      if (disposeSources) e.obj.geometry.dispose();
    }
    merged.push(mesh);
    mergedMeshes++;
    drawCallsSaved += entries.length - 1;
  }

  let mergedLines = 0;
  for (const [, entries] of lineGroups) {
    if (entries.length < 2) continue;
    const geo = mergeLines(entries);
    if (!geo) continue;
    const line = new THREE.LineSegments(geo, entries[0].obj.material);
    line.name = 'batched-lines';
    line.userData.mergedCount = entries.length;
    root.add(line);
    for (const e of entries) {
      if (e.obj.parent) e.obj.parent.remove(e.obj);
      if (disposeSources) e.obj.geometry.dispose();
    }
    mergedLines++;
    drawCallsSaved += entries.length - 1;
  }

  return { mergedMeshes, mergedLines, drawCallsSaved, merged };
}

// Faces of a merged buffer are laid out contiguously per source object, so identity can be
// recovered from a hit's face index with a binary search over the offsets instead of keeping
// a per-face lookup array (which would add hundreds of kilobytes on a large model).
function buildPickMap(mesh, entries) {
  const offsets = new Int32Array(entries.length + 1);
  const sources = new Array(entries.length);
  let faces = 0;
  for (let i = 0; i < entries.length; i++) {
    const e = entries[i];
    const count = e.geo.index ? e.geo.index.count : e.geo.attributes.position.count;
    faces += Math.floor(count / 3);
    offsets[i + 1] = faces;
    sources[i] = e.obj;
  }
  mesh.userData.pickFaces = offsets;
  mesh.userData.pickSources = sources;
}

/**
 * Resolve which source object a raycast hit on a merged mesh belongs to.
 * @param {THREE.Mesh} mesh
 * @param {number} faceIndex
 * @returns {THREE.Object3D|null}
 */
export function pickSource(mesh, faceIndex) {
  const offsets = mesh && mesh.userData ? mesh.userData.pickFaces : null;
  if (!offsets) return null;
  let lo = 0;
  let hi = offsets.length - 2;
  while (lo < hi) {
    const mid = (lo + hi + 1) >> 1;
    if (offsets[mid] <= faceIndex) lo = mid; else hi = mid - 1;
  }
  return mesh.userData.pickSources[lo] || null;
}

/**
 * Merge like `batchStaticGeometry` but keep tap-to-identify working: every merged mesh carries
 * a face-range table so a raycast hit can be traced back to the part that produced it.
 * @param {THREE.Object3D} root
 */
export function mergeWithPickMap(root, opts = {}) {
  return batchStaticGeometry(root, { ...opts, pick: true, mergeLines: opts.mergeLines !== false });
}

/**
 * Collapse runs of repeated identical geometry into InstancedMesh.
 * Used by the scatter-heavy micro-detail passes where one primitive is cloned many times.
 */
export function instanceRepeatedGeometry(root, opts = {}) {
  const minGroup = opts.minGroup ?? 8;
  root.updateMatrixWorld(true);
  _inv.copy(root.matrixWorld).invert();

  const groups = new Map();
  root.traverse((obj) => {
    if (!obj.isMesh || obj.isInstancedMesh || !obj.geometry) return;
    if (obj.userData && obj.userData.noBatch) return;
    const key = [
      obj.geometry.uuid,
      obj.material ? obj.material.uuid : 'x',
      obj.castShadow ? 1 : 0,
      obj.receiveShadow ? 1 : 0,
    ].join('~');
    _rel.multiplyMatrices(_inv, obj.matrixWorld);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({ obj, matrix: _rel.clone() });
  });

  let created = 0;
  let saved = 0;
  for (const [, entries] of groups) {
    if (entries.length < minGroup) continue;
    const template = entries[0];
    const inst = new THREE.InstancedMesh(template.obj.geometry, template.obj.material, entries.length);
    inst.name = 'instanced';
    inst.castShadow = template.obj.castShadow;
    inst.receiveShadow = template.obj.receiveShadow;
    inst.userData.mergedCount = entries.length;
    for (let i = 0; i < entries.length; i++) inst.setMatrixAt(i, entries[i].matrix);
    inst.instanceMatrix.needsUpdate = true;
    inst.computeBoundingSphere();
    root.add(inst);
    for (const e of entries) if (e.obj.parent) e.obj.parent.remove(e.obj);
    created++;
    saved += entries.length - 1;
  }
  return { instancedMeshes: created, drawCallsSaved: saved };
}
