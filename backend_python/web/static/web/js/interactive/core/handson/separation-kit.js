// Apparatus for the separation practical, at true size (1 unit = 10 cm): a filter funnel with a
// paper cone, an evaporating dish whose solution shrinks and crystallises, a china dish under an
// inverted funnel for sublimation, a distillation set (flask, still head with side arm, a
// thermometer that slides in its adapter, a sloping Liebig condenser with two water nozzles and a
// receiver), and a chromatography jar whose paper is redrawn as the solvent climbs.
import { THREE } from '../engine.js';
import { MAT, mesh } from '../bio-handson/kit.js';

const V2 = (x, y) => new THREE.Vector2(x, y);
const tube = (pts, r, mat) => mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 40, r, 10), mat, null, { cast: false });

export function filterFunnel() {
  const g = new THREE.Group();
  g.add(mesh(new THREE.LatheGeometry([V2(0.012, 0), V2(0.012, 0.32), V2(0.025, 0.36), V2(0.27, 0.62), V2(0.28, 0.64)], 32), MAT.glass(), null, { cast: false }));
  const paper = mesh(new THREE.LatheGeometry([V2(0.02, 0.38), V2(0.24, 0.6), V2(0.25, 0.62)], 32), new THREE.MeshStandardMaterial({ color: 0xfbfaf4, roughness: 0.95, side: THREE.DoubleSide }), null, { cast: false }); paper.visible = false; g.add(paper);
  const pool = mesh(new THREE.CircleGeometry(1, 28), MAT.liquid(0xb79b6b, 0.85), null, { cast: false }); pool.rotation.x = -Math.PI / 2; pool.visible = false; g.add(pool);
  const residue = mesh(new THREE.ConeGeometry(0.1, 0.06, 20), MAT.matte(0xc9a76a), [0, 0.42, 0]); residue.rotation.x = Math.PI; residue.visible = false; g.add(residue);
  return { group: g, paper, pool, residue, setPool(level) { pool.visible = level > 0.005; const y = 0.4 + level; pool.position.y = y; const r = 0.02 + (y - 0.38) * (0.23 / 0.24); pool.scale.set(r, r, 1); } };
}

export function evaporatingDish() {
  const g = new THREE.Group(); const pts = []; for (let i = 0; i <= 12; i++) { const a = i / 12 * 1.15; pts.push(V2(Math.sin(a) * 0.36 + 0.001, (1 - Math.cos(a)) * 0.36)); }
  g.add(mesh(new THREE.LatheGeometry(pts, 36), new THREE.MeshPhysicalMaterial({ color: 0xf6f4ef, roughness: 0.25, clearcoat: 0.8, side: THREE.DoubleSide })));
  const liq = mesh(new THREE.CircleGeometry(1, 30), MAT.liquid(0xdbe9f3, 0.7), null, { cast: false }); liq.rotation.x = -Math.PI / 2; g.add(liq);
  const crystals = new THREE.Group(); g.add(crystals);
  for (let i = 0; i < 40; i++) { const a = Math.random() * Math.PI * 2; const r = Math.random() * 0.2; const c = mesh(new THREE.BoxGeometry(0.02, 0.02, 0.02), MAT.gloss(0xffffff), [Math.cos(a) * r, 0.02 + r * r * 1.2, Math.sin(a) * r]); c.rotation.set(Math.random() * 3, Math.random() * 3, 0); c.visible = false; crystals.add(c); }
  return {
    group: g,
    set(level, cryst) { liq.visible = level > 0.01; const h = 0.02 + level * 0.18; const r = Math.sqrt(Math.max(0, 0.72 * h - h * h)); liq.position.y = h; liq.scale.set(r, r, 1); crystals.children.forEach((c, i) => { c.visible = i < cryst * 40; }); },
  };
}

export function distillation() {
  const g = new THREE.Group(); const glass = MAT.glass();
  const flask = mesh(new THREE.LatheGeometry([V2(0.001, 0), V2(0.2, 0.03), V2(0.3, 0.15), V2(0.32, 0.3), V2(0.28, 0.45), V2(0.1, 0.58), V2(0.07, 0.62), V2(0.07, 0.95)], 36), glass, [0, 1.47, 0], { cast: false }); g.add(flask);
  const liq = mesh(new THREE.SphereGeometry(0.29, 24, 12, 0, Math.PI * 2, Math.PI * 0.45, Math.PI * 0.55), MAT.liquid(0xdbe9f3, 0.55), [0, 1.47 + 0.3, 0], { cast: false }); g.add(liq);
  const arm = tube([new THREE.Vector3(0, 2.3, 0), new THREE.Vector3(0.12, 2.3, 0), new THREE.Vector3(0.45, 2.15, 0)], 0.025, glass); g.add(arm);
  const cond = new THREE.Group(); cond.position.set(0.45, 2.15, 0); cond.rotation.z = -0.32; g.add(cond);
  cond.add(mesh(new THREE.CylinderGeometry(0.09, 0.09, 2.0, 22, 1, true), glass, [1.0, 0, 0], { cast: false }).rotateZ(Math.PI / 2));
  cond.add(mesh(new THREE.CylinderGeometry(0.025, 0.025, 2.5, 12, 1, true), glass, [1.1, 0, 0], { cast: false }).rotateZ(Math.PI / 2));
  const jacket = mesh(new THREE.CylinderGeometry(0.085, 0.085, 1.98, 20), MAT.liquid(0x9ec9ea, 0.0), [1.0, 0, 0], { cast: false }); jacket.rotation.z = Math.PI / 2; cond.add(jacket);
  const nozzleLow = mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.18, 10), glass, [1.85, -0.16, 0], { cast: false }); const nozzleHigh = mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.18, 10), glass, [0.15, 0.16, 0], { cast: false }); cond.add(nozzleLow, nozzleHigh);
  const receiver = mesh(new THREE.LatheGeometry([V2(0.001, 0), V2(0.26, 0), V2(0.28, 0.05), V2(0.12, 0.6), V2(0.1, 0.8)], 32), glass, [2.6, 0, 0], { cast: false }); g.add(receiver);
  const dist = mesh(new THREE.CylinderGeometry(0.2, 0.25, 1, 24), MAT.liquid(0xeef6fb, 0.6), null, { cast: false }); dist.visible = false; g.add(dist);
  return {
    group: g, flask, liq, cond, jacket, nozzleLow, nozzleHigh, receiver,
    setDistillate(ml) { dist.visible = ml > 0.5; const h = ml / 1000 / (Math.PI * 0.22 * 0.22); dist.scale.y = Math.max(0.001, h); dist.position.set(2.6, h / 2 + 0.01, 0); },
    setLevel(k) { liq.scale.set(1, Math.max(0.05, k), 1); liq.position.y = 1.47 + 0.3 - 0.29 * (1 - k) * 0.6; },
  };
}

/** Chromatography paper: a canvas redrawn with the pencil line, spots, solvent front and dye bands. */
export function chromaPaper() {
  const cv = document.createElement('canvas'); cv.width = 256; cv.height = 1024; const g = cv.getContext('2d');
  const tex = new THREE.CanvasTexture(cv); if (tex.colorSpace !== undefined) tex.colorSpace = THREE.SRGBColorSpace;
  const m = mesh(new THREE.PlaneGeometry(0.4, 1.6), new THREE.MeshStandardMaterial({ map: tex, roughness: 0.95, side: THREE.DoubleSide }), null, { cast: false });
  const Y = (f) => 1024 - 1024 * f;
  return {
    mesh: m,
    draw({ line = 0.12, spot = false, front = 0, dyes = [], frontMark = false, wet = 0 }) {
      g.fillStyle = '#fbfaf3'; g.fillRect(0, 0, 256, 1024);
      if (wet > 0) { g.fillStyle = 'rgba(190,210,225,.35)'; g.fillRect(0, Y(wet), 256, 1024 - Y(wet)); }
      g.strokeStyle = '#6b7280'; g.lineWidth = 2; g.beginPath(); g.moveTo(20, Y(line)); g.lineTo(236, Y(line)); g.stroke();
      if (frontMark) { g.strokeStyle = '#111827'; g.setLineDash([8, 6]); g.beginPath(); g.moveTo(20, Y(front)); g.lineTo(236, Y(front)); g.stroke(); g.setLineDash([]); }
      if (spot && !dyes.length) { g.fillStyle = '#1f2937'; g.beginPath(); g.arc(128, Y(line), 12, 0, Math.PI * 2); g.fill(); }
      dyes.forEach((d) => { const y = Y(line + (front - line) * d.rf); const gr = g.createRadialGradient(128, y, 2, 128, y, 22); gr.addColorStop(0, d.color); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.beginPath(); g.ellipse(128, y, 24, 18, 0, 0, Math.PI * 2); g.fill(); });
      tex.needsUpdate = true;
    },
  };
}
