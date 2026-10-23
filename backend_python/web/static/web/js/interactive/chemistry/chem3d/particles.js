import { THREE } from '../../core/engine.js';

// The particle picture of a substance in a sealed glass box, in 3D. The thermal model decides how much
// is solid, liquid and gas (fm, fb); the particles act it out. Solid ones sit on a cubic lattice at the
// bottom and vibrate more as it warms; the lattice gives way from its outside in. Liquid ones pool
// under gravity, held together by a short-range attraction and kept apart by a soft core. Gas ones fly
// ballistically at speeds that grow as √T and bounce off the walls. One instanced draw call.
export function createParticleBox(n, { size = 1, radius = 0.045, color = 0x60a5fa } = {}) {
  const side = Math.round(Math.cbrt(n));
  n = side * side * side;
  const half = size / 2;
  const group = new THREE.Group();
  const glass = new THREE.MeshPhysicalMaterial({ color: 0xeaf6ff, roughness: 0.05, transparent: true, opacity: 0.16, clearcoat: 1, depthWrite: false, side: THREE.DoubleSide });
  const box = new THREE.Mesh(new THREE.BoxGeometry(size, size, size), glass); box.renderOrder = 6;
  const edges = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(size, size, size)), new THREE.LineBasicMaterial({ color: 0xcfe3f3, transparent: true, opacity: 0.6 }));
  group.add(box, edges);
  const mat = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.25, clearcoat: 0.8, clearcoatRoughness: 0.2 });
  const inst = new THREE.InstancedMesh(new THREE.SphereGeometry(radius, 16, 12), mat, n);
  inst.castShadow = true;
  group.add(inst);

  const x = new Float32Array(n * 3); const v = new Float32Array(n * 3); const site = new Float32Array(n * 3); const st = new Uint8Array(n);
  const d = radius * 2.25;
  const off = -(side - 1) * d / 2;
  const order = [];
  for (let k = 0; k < side; k++) for (let j = 0; j < side; j++) for (let i = 0; i < side; i++) {
    const q = order.length;
    site[q * 3] = off + i * d; site[q * 3 + 1] = -half + radius + j * d; site[q * 3 + 2] = off + k * d;
    const cx = (i - (side - 1) / 2); const cz = (k - (side - 1) / 2);
    order.push({ q, out: Math.max(Math.abs(cx), Math.abs(cz)) + j * 0.9 });
  }
  order.sort((a, b) => b.out - a.out);
  const meltRank = new Int32Array(n);
  order.forEach((o, r) => { meltRank[o.q] = r; });
  for (let q = 0; q < n; q++) { x[q * 3] = site[q * 3]; x[q * 3 + 1] = site[q * 3 + 1]; x[q * 3 + 2] = site[q * 3 + 2]; }

  const colors = [new THREE.Color(color), new THREE.Color(color), new THREE.Color(color)];
  const tmpC = new THREE.Color(); const m4 = new THREE.Matrix4();
  const lim = half - radius;
  let gasRank = new Int32Array(n);
  for (let q = 0; q < n; q++) gasRank[q] = q;
  function rand() { return Math.random() * 2 - 1; }

  return {
    group, n,
    setColors(sol, liq, gas) { colors[0].set(sol); colors[1].set(liq); colors[2].set(gas); },
    reset(fm, fb) {
      for (let q = 0; q < n; q++) { x[q * 3] = site[q * 3]; x[q * 3 + 1] = site[q * 3 + 1]; x[q * 3 + 2] = site[q * 3 + 2]; v[q * 3] = v[q * 3 + 1] = v[q * 3 + 2] = 0; st[q] = 0; }
      gasRank = Int32Array.from(meltRank);
      this.step(0, fm, fb, 0.2);
    },
    /** fm, fb: fractions melted and boiled; heat 0..1.3 sets vibration and speeds. */
    step(dt, fm, fb, heat) {
      const nLiquidOrGas = Math.round(fm * n); const nGas = Math.round(fb * n);
      for (let q = 0; q < n; q++) {
        const r = meltRank[q];
        const want = r < nGas ? 2 : r < nLiquidOrGas ? 1 : 0;
        if (want !== st[q]) {
          if (want === 2) { const s = 0.6 + heat; v[q * 3] = rand() * s; v[q * 3 + 1] = Math.random() * s; v[q * 3 + 2] = rand() * s; }
          st[q] = want;
        }
      }
      const h = Math.min(dt, 1 / 30); const steps = h > 0 ? 2 : 0; const hs = h / Math.max(1, steps);
      const jig = 0.004 + 0.02 * heat;
      const gasV = 0.5 + 1.6 * Math.sqrt(Math.max(heat, 0.02));
      for (let s = 0; s < steps; s++) {
        for (let q = 0; q < n; q++) {
          const i = q * 3;
          if (st[q] === 0) {
            x[i] = site[i] + rand() * jig * 0.3 + (x[i] - site[i]) * 0.6;
            x[i + 1] = site[i + 1] + rand() * jig * 0.3 + (x[i + 1] - site[i + 1]) * 0.6;
            x[i + 2] = site[i + 2] + rand() * jig * 0.3 + (x[i + 2] - site[i + 2]) * 0.6;
            continue;
          }
          if (st[q] === 1) {
            v[i + 1] -= 3.0 * hs;
            for (let p = 0; p < n; p++) {
              if (p === q || st[p] === 2) continue;
              const j = p * 3; const dx = x[i] - x[j]; const dy = x[i + 1] - x[j + 1]; const dz = x[i + 2] - x[j + 2];
              const r2 = dx * dx + dy * dy + dz * dz;
              if (r2 > d * d * 2.6 || r2 < 1e-10) continue;
              const r = Math.sqrt(r2);
              const f = r < d ? (d - r) / d * 40 : st[p] === 0 ? 0 : -(r - d) / d * 1.6;
              v[i] += dx / r * f * hs; v[i + 1] += dy / r * f * hs; v[i + 2] += dz / r * f * hs;
            }
            const damp = Math.exp(-hs * 4);
            v[i] = v[i] * damp + rand() * jig * 4; v[i + 1] = v[i + 1] * damp + rand() * jig * 4; v[i + 2] = v[i + 2] * damp + rand() * jig * 4;
          } else {
            const sp = Math.hypot(v[i], v[i + 1], v[i + 2]) || 1;
            const k = 1 + (gasV / sp - 1) * Math.min(1, hs * 3);
            v[i] *= k; v[i + 1] *= k; v[i + 2] *= k;
            v[i + 1] -= 0.3 * hs;
          }
          for (let c = 0; c < 3; c++) {
            x[i + c] += v[i + c] * hs;
            if (x[i + c] > lim) { x[i + c] = lim; v[i + c] = -Math.abs(v[i + c]) * (st[q] === 2 ? 1 : 0.3); }
            if (x[i + c] < -lim) { x[i + c] = -lim; v[i + c] = Math.abs(v[i + c]) * (st[q] === 2 ? 1 : 0.3); }
          }
        }
      }
      for (let q = 0; q < n; q++) {
        m4.makeTranslation(x[q * 3], x[q * 3 + 1], x[q * 3 + 2]);
        inst.setMatrixAt(q, m4);
        inst.setColorAt(q, tmpC.copy(colors[st[q]]));
      }
      inst.instanceMatrix.needsUpdate = true;
      if (inst.instanceColor) inst.instanceColor.needsUpdate = true;
    },
    dispose() { inst.geometry.dispose(); mat.dispose(); box.geometry.dispose(); glass.dispose(); edges.geometry.dispose(); edges.material.dispose(); },
  };
}

// A hot plate that glows as it heats and frosts over as it cools: a steel housing, a ceramic top
// with a coil whose emissive colour follows the dial.
export function createHotPlate() {
  const g = new THREE.Group();
  const housing = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.32, 1.4), new THREE.MeshStandardMaterial({ color: 0xd8dde3, metalness: 0.6, roughness: 0.35 }));
  housing.position.y = 0.16; housing.castShadow = true; housing.receiveShadow = true;
  const top = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.6, 0.03, 48), new THREE.MeshStandardMaterial({ color: 0x1f2328, roughness: 0.5 }));
  top.position.y = 0.335;
  const coilMat = new THREE.MeshStandardMaterial({ color: 0x2a2a2a, emissive: 0x000000, roughness: 0.6 });
  const pts = []; for (let t = 0; t <= 1; t += 0.01) { const a = t * Math.PI * 9; const r = 0.08 + t * 0.42; pts.push(new THREE.Vector3(Math.cos(a) * r, 0.355, Math.sin(a) * r)); }
  const coil = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 300, 0.012, 6), coilMat);
  const knob = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.06, 24), new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.5 }));
  knob.rotation.x = Math.PI / 2; knob.position.set(0.55, 0.16, 0.72);
  const frost = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.6, 0.004, 48), new THREE.MeshStandardMaterial({ color: 0xe0f2fe, roughness: 0.9, transparent: true, opacity: 0 }));
  frost.position.y = 0.355;
  g.add(housing, top, coil, knob, frost);
  const hot = new THREE.Color(); const warm = new THREE.Color(0xff3b0a); const white = new THREE.Color(0xffc56b);
  return {
    group: g,
    set(dial) {
      const h = Math.max(0, dial);
      coilMat.emissive.copy(hot.copy(warm).lerp(white, h * h)).multiplyScalar(h * 2.2);
      frost.material.opacity = Math.max(0, -dial) * 0.85;
      knob.rotation.z = -dial * 2.4;
    },
  };
}
