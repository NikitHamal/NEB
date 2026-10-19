// Microbiology bench pieces at true size (1 unit = 10 cm): a 9 cm Petri plate whose agar surface is
// a painted canvas, so colonies can grow over incubation time and be tapped and marked one by one;
// an incubator; and colony kinds as they look on the plate — smooth shiny bacteria, fuzzy spreading
// moulds, small chalky actinomycetes, gummy white Rhizobium on Congo red agar and red-stained
// contaminants.
import { THREE } from '../../engine.js';
import { mesh, MAT, smooth, rng } from '../kit.js';

const PX = 512; const RU = 0.43; const MM = PX / (RU * 2 * 100); // texture pixels per millimetre

/** Colony radius (mm) at time t (h). */
function radius(c, t) { return c.rmax * smooth(c.t0, c.t0 + c.tau, t); }

function drawColony(g, c, t) {
  const r = radius(c, t) * MM; if (r < 0.6) return;
  const x = c.u * PX; const y = c.v * PX;
  if (c.kind === 'fungus') {
    const gr = g.createRadialGradient(x, y, 0, x, y, r);
    gr.addColorStop(0, c.col || 'rgba(110,130,95,0.95)'); gr.addColorStop(0.55, 'rgba(235,238,225,0.92)'); gr.addColorStop(1, 'rgba(250,250,245,0)');
    g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
    g.strokeStyle = 'rgba(255,255,255,0.55)'; g.lineWidth = 0.8;
    for (let k = 0; k < 40; k++) { const a = k / 40 * Math.PI * 2 + c.seed; g.beginPath(); g.moveTo(x + Math.cos(a) * r * 0.5, y + Math.sin(a) * r * 0.5); g.lineTo(x + Math.cos(a + 0.1) * r * 1.05, y + Math.sin(a + 0.1) * r * 1.05); g.stroke(); }
    return;
  }
  if (c.kind === 'actino') { g.fillStyle = 'rgba(245,245,240,0.98)'; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill(); g.fillStyle = 'rgba(200,200,190,0.8)'; for (let k = 0; k < 6; k++) { g.beginPath(); g.arc(x + (Math.sin(k * 7 + c.seed) * r * 0.5), y + Math.cos(k * 5 + c.seed) * r * 0.5, r * 0.18, 0, Math.PI * 2); g.fill(); } return; }
  const base = c.kind === 'contam' ? [196, 40, 50] : c.kind === 'rhizo' ? [250, 248, 238] : c.col || [238, 226, 190];
  const gr = g.createRadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r);
  gr.addColorStop(0, `rgba(255,255,255,${c.kind === 'rhizo' ? 0.95 : 0.85})`); gr.addColorStop(0.35, `rgba(${base[0]},${base[1]},${base[2]},${c.kind === 'rhizo' ? 0.8 : 0.96})`); gr.addColorStop(1, `rgba(${base[0] * 0.85 | 0},${base[1] * 0.85 | 0},${base[2] * 0.85 | 0},0.95)`);
  g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
  g.strokeStyle = 'rgba(80,60,30,0.35)'; g.lineWidth = 1; g.stroke();
}

/** A Petri plate. agar: CSS colour of the medium. */
export function plate(agar = '#e9d9a6') {
  const g = new THREE.Group();
  const prof = [[0.001, 0], [0.45, 0], [0.46, 0.01], [0.46, 0.08], [0.455, 0.085]].map(([a, b]) => new THREE.Vector2(a, b));
  const dish = mesh(new THREE.LatheGeometry(prof, 40), MAT.glass(), null, { cast: false }); dish.renderOrder = 5; g.add(dish);
  const cv = document.createElement('canvas'); cv.width = cv.height = PX; const ctx2 = cv.getContext('2d');
  const tex = new THREE.CanvasTexture(cv); if (tex.colorSpace !== undefined) tex.colorSpace = THREE.SRGBColorSpace;
  const agarM = mesh(new THREE.CircleGeometry(RU + 0.015, 48), new THREE.MeshPhysicalMaterial({ map: tex, roughness: 0.25, clearcoat: 0.8, transparent: true, opacity: 0.96 }), [0, 0.03, 0]);
  agarM.rotation.x = -Math.PI / 2; agarM.visible = false; g.add(agarM);
  const lid = new THREE.Group(); lid.position.y = 0.09; g.add(lid);
  const lp = [[0.001, 0.0], [0.47, 0.0], [0.475, -0.012], [0.475, -0.06]].map(([a, b]) => new THREE.Vector2(a, b));
  const lm = mesh(new THREE.LatheGeometry(lp, 40), MAT.glass(), null, { cast: false }); lm.renderOrder = 6; lid.add(lm);
  const colonies = []; const marks = []; let t = 0; let wet = 0;
  function paint() {
    ctx2.clearRect(0, 0, PX, PX);
    ctx2.fillStyle = agar; ctx2.beginPath(); ctx2.arc(PX / 2, PX / 2, PX / 2 - 2, 0, Math.PI * 2); ctx2.fill();
    if (wet > 0) { ctx2.fillStyle = `rgba(150,140,110,${wet * 0.25})`; ctx2.beginPath(); ctx2.arc(PX / 2, PX / 2, PX * 0.2, 0, Math.PI * 2); ctx2.fill(); }
    ctx2.save(); ctx2.beginPath(); ctx2.arc(PX / 2, PX / 2, PX / 2 - 2, 0, Math.PI * 2); ctx2.clip();
    colonies.forEach((c) => drawColony(ctx2, c, t));
    ctx2.restore();
    marks.forEach(([u, v]) => { ctx2.fillStyle = '#111827'; ctx2.beginPath(); ctx2.arc(u * PX, v * PX, 3.2, 0, Math.PI * 2); ctx2.fill(); });
    tex.needsUpdate = true;
  }
  paint();
  return {
    group: g, agar: agarM, lid, colonies, tex,
    get time() { return t; },
    pour() { agarM.visible = true; paint(); },
    setWet(k) { wet = k; paint(); },
    setTime(h) { t = h; paint(); },
    /** Seed colonies: list of { kind, u, v, rmax (mm), t0, tau, col }. */
    seed(list) { colonies.push(...list); paint(); },
    mark(u, v) { marks.push([u, v]); paint(); },
    clearMarks() { marks.length = 0; paint(); },
    /** The colony at a uv (from a raycast on the agar), if visible at the current time. */
    colonyAt(uv) { let best = null; let bd = Infinity; colonies.forEach((c) => { const r = radius(c, t) * MM / PX; if (r <= 0) return; const d = Math.hypot(c.u - uv.x, c.v - (1 - uv.y)); if (d < r + 0.012 && d < bd) { bd = d; best = c; } }); return best; },
    visible() { return colonies.filter((c) => radius(c, t) > 0.15); },
    dispose() { tex.dispose(); },
  };
}

/** Random positions inside the plate (uv), spaced apart. */
export function scatter(n, seed, minD = 0.035, rMax = 0.43) {
  const R = rng(seed); const out = [];
  for (let k = 0; k < n * 40 && out.length < n; k++) {
    const a = R() * Math.PI * 2; const r = Math.sqrt(R()) * rMax; const u = 0.5 + Math.cos(a) * r; const v = 0.5 + Math.sin(a) * r;
    if (out.every(([x, y]) => Math.hypot(x - u, y - v) > minD)) out.push([u, v]);
  }
  return out;
}

/** A bench incubator with a glass inner door and a temperature display. */
export function incubator(label = '30 °C') {
  const g = new THREE.Group();
  const body = MAT.gloss(0xe5e7eb);
  g.add(mesh(new THREE.BoxGeometry(1.6, 1.3, 1.2), body, [0, 0.65, 0]));
  const inner = mesh(new THREE.BoxGeometry(1.4, 1.05, 0.02), MAT.matte(0x334155), [0, 0.68, 0.59]); g.add(inner);
  [0.35, 0.75].forEach((y) => g.add(mesh(new THREE.BoxGeometry(1.36, 0.02, 1.0), MAT.steel(), [0, y, 0.05])));
  const door = new THREE.Group(); door.position.set(-0.8, 0, 0.61); g.add(door);
  door.add(mesh(new THREE.BoxGeometry(1.6, 1.3, 0.05), body, [0.8, 0.65, 0]));
  door.add(mesh(new THREE.BoxGeometry(0.06, 0.4, 0.06), MAT.steel(), [1.45, 0.7, 0.05]));
  const cv = document.createElement('canvas'); cv.width = 256; cv.height = 64; const c = cv.getContext('2d'); c.fillStyle = '#0f172a'; c.fillRect(0, 0, 256, 64); c.fillStyle = '#f87171'; c.font = '700 40px monospace'; c.fillText(label, 24, 46);
  const tex = new THREE.CanvasTexture(cv); door.add(mesh(new THREE.PlaneGeometry(0.4, 0.1), new THREE.MeshBasicMaterial({ map: tex }), [0.8, 1.15, 0.03]));
  return { group: g, door, open(k) { door.rotation.y = -k * 1.9; } };
}
