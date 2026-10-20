import { THREE } from '../../core/engine.js';
import { surfaceNets, toGeometry } from '../../biology/anatomy/mesher.js';
import { getBySymbol } from '../elements-data.js';

const VDW = { H: 1.1, C: 1.7, N: 1.55, O: 1.52, F: 1.47, P: 1.8, S: 1.8, Cl: 1.75, Br: 1.85, I: 1.98, Na: 2.27, K: 2.75, Mg: 1.73, Ca: 2.31, B: 1.92, Si: 2.1 };

export function partialCharges(atoms, bonds) {
  const q = atoms.map(() => 0);
  const en = atoms.map((a) => { const e = getBySymbol(a.el); return e && e.en ? e.en : 2.0; });
  bonds.forEach((b) => {
    const i = b.a ?? b[0]; const j = b.b ?? b[1];
    const d = (en[j] - en[i]) * 0.16 * (b.order || b[2] || 1) ** 0.5;
    q[i] += d; q[j] -= d;
  });
  return q;
}

export function buildSurface(atoms, bonds, S, quality, ionic = false) {
  const pts = atoms.map((a) => new THREE.Vector3(a.p[0] * S, a.p[1] * S, a.p[2] * S));
  const rad = atoms.map((a) => (VDW[a.el] || 1.8) * S * 0.62);
  const q = ionic ? atoms.map((a) => ((getBySymbol(a.el) || {}).en || 2) > 2 ? -0.9 : 0.9) : partialCharges(atoms, bonds);
  const k = 0.7;
  const sdf = (p) => {
    let d = 1e9;
    for (let i = 0; i < pts.length; i++) {
      const dx = p[0] - pts[i].x; const dy = p[1] - pts[i].y; const dz = p[2] - pts[i].z;
      const di = Math.sqrt(dx * dx + dy * dy + dz * dz) - rad[i];
      const h = Math.max(k - Math.abs(d - di), 0) / k;
      d = Math.min(d, di) - h * h * k * 0.25;
    }
    return d;
  };
  const min = [Infinity, Infinity, Infinity]; const max = [-Infinity, -Infinity, -Infinity];
  pts.forEach((p, i) => { ['x', 'y', 'z'].forEach((c, j) => { min[j] = Math.min(min[j], p[c] - rad[i] - 0.4); max[j] = Math.max(max[j], p[c] + rad[i] + 0.4); }); });
  const span = Math.max(max[0] - min[0], max[1] - min[1], max[2] - min[2]);
  const cell = Math.max(0.05, span / (quality.tier === 'low' ? 70 : 110));
  const mesh = surfaceNets(sdf, { min, max }, cell);
  const col = new Float32Array(mesh.count * 3);
  const c = new THREE.Color(); const neg = new THREE.Color(0xd8141e); const mid = new THREE.Color(0xe8e2f0); const pos = new THREE.Color(0x1240e0);
  for (let v = 0; v < mesh.count; v++) {
    let phi = 0;
    for (let i = 0; i < pts.length; i++) {
      const dx = mesh.position[v * 3] - pts[i].x; const dy = mesh.position[v * 3 + 1] - pts[i].y; const dz = mesh.position[v * 3 + 2] - pts[i].z;
      phi += q[i] / Math.max(0.3, Math.sqrt(dx * dx + dy * dy + dz * dz));
    }
    const t = Math.max(-1, Math.min(1, phi * 12.0));
    if (t < 0) c.copy(mid).lerp(neg, -t); else c.copy(mid).lerp(pos, t);
    col[v * 3] = c.r; col[v * 3 + 1] = c.g; col[v * 3 + 2] = c.b;
  }
  const geo = toGeometry(THREE, mesh, { color: [col, 3] });
  const mat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.18, metalness: 0, transparent: true, opacity: 0.62, depthWrite: false, side: THREE.FrontSide, envMapIntensity: 1.3 });
  mat.onBeforeCompile = (sh) => {
    sh.fragmentShader = sh.fragmentShader.replace('#include <opaque_fragment>', `
      { float f = pow(1.0 - clamp(abs(dot(normal, normalize(vViewPosition))), 0.0, 1.0), 2.0);
        diffuseColor.a = clamp(0.5 + 0.45 * f, 0.0, 1.0); outgoingLight += vec3(0.25) * pow(f, 3.0); }
      #include <opaque_fragment>`);
  };
  mat.customProgramCacheKey = () => 'esp-surface';
  const surf = new THREE.Mesh(geo, mat);
  surf.renderOrder = 3;
  return { mesh: surf, charges: q, radii: rad };
}

export const VDW_RADII = VDW;
