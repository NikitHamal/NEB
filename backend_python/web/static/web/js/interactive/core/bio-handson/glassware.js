// Test tubes, a wooden rack, a water bath and a spot tile for the biochemical tests. A tube's
// liquid can be filled, recoloured gradually (a reagent mixing in), cloud over, throw down a
// precipitate, or fizz.
import { THREE } from '../engine.js';
import { MAT, mesh, canvasTexture, roundedSlab } from './kit.js';

const TUBE_R = 0.075; const TUBE_H = 1.25;
const tubeGeo = (() => { let g = null; return () => { if (!g) { const pts = [[0.001, 0], [0.04, 0.008], [0.065, 0.04], [TUBE_R, 0.09], [TUBE_R, TUBE_H], [TUBE_R + 0.012, TUBE_H + 0.02]].map(([r, y]) => new THREE.Vector2(r, y)); g = new THREE.LatheGeometry(pts, 28); g.userData.shared = true; } return g; }; })();

function tagTexture(text) {
  return canvasTexture(`tag:${text}`, 256, 64, (g, w, h) => { g.fillStyle = '#fefce8'; g.fillRect(0, 0, w, h); g.fillStyle = '#111827'; g.font = '700 32px system-ui, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(text, w / 2, h / 2 + 1); });
}

export function makeTube(label, opts = {}) {
  const g = new THREE.Group();
  const glass = mesh(tubeGeo(), MAT.glass(), null, { cast: false }); glass.renderOrder = 3; g.add(glass);
  const liqMat = new THREE.MeshPhysicalMaterial({ color: opts.color ?? 0xdbeafe, roughness: 0.1, transparent: true, opacity: 0.8, clearcoat: 0.8, depthWrite: false });
  const liquid = new THREE.Group();
  const body = mesh(new THREE.CylinderGeometry(TUBE_R - 0.008, TUBE_R - 0.008, 1, 22), liqMat, [0, 0.5, 0], { cast: false });
  const bottom = mesh(new THREE.SphereGeometry(TUBE_R - 0.008, 16, 8, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), liqMat, null, { cast: false });
  liquid.add(body, bottom); liquid.position.y = 0.075; body.renderOrder = 2; bottom.renderOrder = 2;
  g.add(liquid);
  const ppt = mesh(new THREE.SphereGeometry(TUBE_R - 0.01, 14, 8, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.9 }), [0, 0.075, 0], { cast: false });
  ppt.visible = false; g.add(ppt);
  if (label) { const tag = mesh(new THREE.PlaneGeometry(0.2, 0.05), new THREE.MeshBasicMaterial({ map: tagTexture(label) }), [0, 1.05, TUBE_R + 0.004]); g.add(tag); }
  let fill = 0; const c0 = new THREE.Color(); const c1 = new THREE.Color();
  function setFill(f) { fill = f; liquid.visible = f > 0.001; body.scale.y = Math.max(0.001, f * (TUBE_H - 0.12)); body.position.y = body.scale.y / 2; }
  setFill(opts.fill || 0);
  return {
    group: g, liquid, material: liqMat, glass,
    get fill() { return fill; },
    setFill,
    /** Animates fill and/or colour over dur seconds using the practical's animator. */
    to(anim, { fill: f, color, dur = 0.8, opacity }) {
      const f0 = fill; c0.copy(liqMat.color); if (color !== undefined) c1.set(color); else c1.copy(c0);
      const o0 = liqMat.opacity; const o1 = opacity ?? o0;
      anim.add(dur, (k) => { if (f !== undefined) setFill(f0 + (f - f0) * k); liqMat.color.copy(c0).lerp(c1, k); liqMat.opacity = o0 + (o1 - o0) * k; });
    },
    precipitate(anim, color, amount = 1) { ppt.visible = true; ppt.material.color.set(color); ppt.scale.set(1, 0.01, 1); anim.add(1.6, (k) => ppt.scale.set(1, 0.1 + k * 0.9 * amount, 1)); },
    top(out) { return out.set(0, 0.075 + body.scale.y + 0.02, 0).applyMatrix4(g.matrixWorld); },
  };
}

export function makeRack(n = 4) {
  const g = new THREE.Group(); const wood = MAT.gloss(0x9a6a3c);
  const w = n * 0.32 + 0.2;
  g.add(mesh(new THREE.BoxGeometry(w, 0.05, 0.4), wood, [0, 0.025, 0]));
  g.add(mesh(new THREE.BoxGeometry(w, 0.04, 0.36), wood, [0, 0.62, 0]));
  [-1, 1].forEach((s) => g.add(mesh(new THREE.BoxGeometry(0.05, 0.62, 0.4), wood, [s * (w / 2 - 0.025), 0.31, 0])));
  const slots = []; for (let i = 0; i < n; i++) slots.push(new THREE.Vector3(-w / 2 + 0.26 + i * 0.32, 0.05, 0));
  return { group: g, slots };
}

export function makeWaterBath() {
  const g = new THREE.Group();
  const prof = [[0.001, 0], [0.42, 0], [0.44, 0.02], [0.44, 0.6], [0.47, 0.63]].map(([r, y]) => new THREE.Vector2(r, y));
  g.add(mesh(new THREE.LatheGeometry(prof, 36), MAT.glass(), [0, 0.32, 0], { cast: false }));
  const water = mesh(new THREE.CylinderGeometry(0.425, 0.425, 0.48, 32), MAT.liquid(0xcfe8f5, 0.35), [0, 0.32 + 0.25, 0], { cast: false }); g.add(water);
  [[0.4, 0, 0.4], [-0.4, 0, 0.4], [0, 0, -0.5]].forEach(([x, , z]) => { const leg = mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.34, 8), MAT.steel(), [x * 0.9, 0.16, z * 0.9]); g.add(leg); });
  g.add(mesh(new THREE.TorusGeometry(0.46, 0.015, 6, 36), MAT.steel(), [0, 0.32, 0]).rotateX(Math.PI / 2));
  const flame = mesh(new THREE.ConeGeometry(0.06, 0.2, 14), new THREE.MeshBasicMaterial({ color: 0x60a5fa, transparent: true, opacity: 0.75, depthWrite: false }), [0, 0.12, 0], { cast: false });
  flame.visible = false; g.add(flame);
  g.userData.flame = flame; g.userData.waterTop = 0.32 + 0.49;
  return g;
}

export function makeSpotTile(wells = 12) {
  const g = new THREE.Group();
  g.add(mesh(roundedSlab(1.0, 0.7, 0.05, 0.05, 0.01), MAT.gloss(0xfbfbf7)));
  const spots = [];
  for (let i = 0; i < wells; i++) {
    const x = -0.36 + (i % 4) * 0.24; const z = -0.2 + Math.floor(i / 4) * 0.2;
    const well = mesh(new THREE.CircleGeometry(0.07, 24), new THREE.MeshStandardMaterial({ color: 0xe9e9e2, roughness: 0.4 }), [x, 0.061, z]); well.rotation.x = -Math.PI / 2; g.add(well);
    const drop = mesh(new THREE.CircleGeometry(0.055, 24), new THREE.MeshPhysicalMaterial({ color: 0x8b5a2b, roughness: 0.1, clearcoat: 1, transparent: true, opacity: 0.85 }), [x, 0.063, z]); drop.rotation.x = -Math.PI / 2; drop.visible = false; g.add(drop);
    spots.push({ well, drop });
  }
  return { group: g, spots };
}
