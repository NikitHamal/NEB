import { THREE } from '../../core/engine.js';
import { mergeGeos, paintVertices } from '../butterfly/kit.js';

// Ball-and-stick molecules (CPK colours) as single merged geometries, drawn instanced.
const CPK = { C: 0x2b2b2b, O: 0xe23b2e, H: 0xf4f4f4, P: 0xf59e0b };

function atom(el, x, y, z, r, seg) {
  const g = new THREE.SphereGeometry(r, seg, Math.max(6, seg - 2));
  g.translate(x, y, z);
  return paintVertices(g, (px, py, pz, c) => c.setHex(CPK[el]));
}
function bond(a, b, r, seg) {
  const A = new THREE.Vector3(...a); const B = new THREE.Vector3(...b);
  const g = new THREE.CylinderGeometry(r, r, A.distanceTo(B), Math.max(5, seg - 4));
  g.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), B.clone().sub(A).normalize()));
  g.translate((A.x + B.x) / 2, (A.y + B.y) / 2, (A.z + B.z) / 2);
  return paintVertices(g, (px, py, pz, c) => c.setHex(0xcfd3d6));
}

export function moleculeGeometry(kind, seg = 10) {
  const parts = [];
  if (kind === 'co2') {
    parts.push(atom('C', 0, 0, 0, 0.34, seg), atom('O', -0.62, 0, 0, 0.3, seg), atom('O', 0.62, 0, 0, 0.3, seg));
    parts.push(bond([-0.6, 0, 0], [0.6, 0, 0], 0.07, seg));
  } else if (kind === 'o2') {
    parts.push(atom('O', -0.29, 0, 0, 0.3, seg), atom('O', 0.29, 0, 0, 0.3, seg));
  } else if (kind === 'h2o') {
    const a = 104.5 / 2 * Math.PI / 180;
    const h1 = [Math.sin(a) * 0.48, -Math.cos(a) * 0.48, 0]; const h2 = [-Math.sin(a) * 0.48, -Math.cos(a) * 0.48, 0];
    parts.push(atom('O', 0, 0, 0, 0.3, seg), atom('H', ...h1, 0.18, seg), atom('H', ...h2, 0.18, seg));
  } else if (kind === 'glucose') {
    const ring = [];
    for (let i = 0; i < 6; i++) {
      const ang = (i / 6) * Math.PI * 2;
      ring.push([Math.cos(ang) * 0.75, (i % 2 ? 0.12 : -0.12), Math.sin(ang) * 0.75]);
    }
    ring.forEach((p, i) => {
      parts.push(atom(i === 0 ? 'O' : 'C', ...p, i === 0 ? 0.24 : 0.26, seg));
      parts.push(bond(p, ring[(i + 1) % 6], 0.06, seg));
      if (i > 0) {
        const out = [p[0] * 1.6, p[1] + (i % 2 ? 0.35 : -0.35), p[2] * 1.6];
        parts.push(atom('O', ...out, 0.18, seg), bond(p, out, 0.05, seg));
      }
    });
  } else if (kind === 'atp') {
    parts.push(atom('C', 0, 0, 0, 0.36, seg));
    for (let i = 1; i <= 3; i++) parts.push(atom('P', i * 0.52, 0, 0, 0.22, seg));
  }
  parts.forEach((g) => { if (!g.attributes.uv) g.setAttribute('uv', new THREE.Float32BufferAttribute(new Float32Array(g.attributes.position.count * 2), 2)); });
  return mergeGeos(parts);
}

export function moleculeMaterial(glow = 0) {
  return new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: 0.32, clearcoat: 0.6, clearcoatRoughness: 0.2, emissive: glow ? 0xffb020 : 0x000000, emissiveIntensity: glow });
}

// A pool of instanced molecules that follow waypoint paths and fade by shrinking.
export class MoleculeSwarm {
  constructor(parent, kind, max, opts = {}) {
    this.mesh = new THREE.InstancedMesh(moleculeGeometry(kind, opts.seg || 10), moleculeMaterial(opts.glow || 0), max);
    this.mesh.count = 0;
    this.mesh.frustumCulled = false;
    parent.add(this.mesh);
    this.items = [];
    this.max = max;
    this.scale = opts.scale || 1;
    this.m = new THREE.Matrix4(); this.q = new THREE.Quaternion(); this.e = new THREE.Euler(); this.s = new THREE.Vector3(); this.p = new THREE.Vector3();
  }
  spawn(path, speed, opts = {}) {
    if (this.items.length >= this.max) return null;
    const it = { path, seg: 0, t: 0, speed, spin: new THREE.Vector3(Math.random() * 3, Math.random() * 3, Math.random() * 3), rot: new THREE.Vector3(Math.random() * 6, Math.random() * 6, Math.random() * 6), life: 0, jitter: opts.jitter ?? 0.4, onEnd: opts.onEnd };
    this.items.push(it);
    return it;
  }
  update(dt, time) {
    let n = 0;
    for (let i = this.items.length - 1; i >= 0; i--) {
      const it = this.items[i];
      it.life += dt;
      const a = it.path[it.seg]; const b = it.path[it.seg + 1];
      const len = a.distanceTo(b) || 0.001;
      it.t += (it.speed * dt) / len;
      if (it.t >= 1) {
        it.t = 0; it.seg += 1;
        if (it.seg >= it.path.length - 1) { if (it.onEnd) it.onEnd(it); this.items.splice(i, 1); continue; }
      }
    }
    for (const it of this.items) {
      const a = it.path[it.seg]; const b = it.path[it.seg + 1];
      this.p.lerpVectors(a, b, it.t);
      const j = it.jitter;
      this.p.x += Math.sin(time * 2.3 + it.rot.x * 3) * j; this.p.y += Math.sin(time * 1.9 + it.rot.y * 3) * j * 0.6; this.p.z += Math.cos(time * 2.1 + it.rot.z * 3) * j;
      const last = it.seg === it.path.length - 2;
      const fadeIn = Math.min(1, it.life * 3);
      const fadeOut = last ? 1 - it.t * it.t : 1;
      this.e.set(it.rot.x + time * it.spin.x * 0.4, it.rot.y + time * it.spin.y * 0.4, it.rot.z);
      this.q.setFromEuler(this.e);
      this.s.setScalar(this.scale * Math.max(0.001, fadeIn * fadeOut));
      this.m.compose(this.p, this.q, this.s);
      this.mesh.setMatrixAt(n++, this.m);
    }
    this.mesh.count = n;
    this.mesh.instanceMatrix.needsUpdate = true;
  }
  clear() { this.items.length = 0; this.mesh.count = 0; }
}
