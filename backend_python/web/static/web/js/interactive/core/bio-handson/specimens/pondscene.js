// A small village pond at true size (1 unit = 10 cm), seen from its bank: grassy margin, muddy
// shelving edge and still green water. Marginal cattails (Typha), rooted lotus with floating leaves
// and a flower, free-floating water hyacinth and a scum of duckweed, submerged Hydrilla seen through
// the water; and the animals — a frog on a lotus pad, snails on a stone, fish below the surface, a
// water strider and a dragonfly. Every organism is a pickable group named for the practical.
import { THREE } from '../../engine.js';
import { mesh, MAT, wet, canvasTexture, rng } from '../kit.js';
import { mergeGeos } from '../bench.js';

export const PC = new THREE.Vector3(0, 0, -9); export const PR = 13;

function lotusLeaf(r) { const g = new THREE.CircleGeometry(r, 24, 0.25, Math.PI * 2 - 0.25); g.rotateX(-Math.PI / 2); return mesh(g, wet(0x3f8f3a, { roughness: 0.6, clearcoat: 0.2, side: THREE.DoubleSide })); }

export function buildPond(seed = 3) {
  const R = rng(seed); const g = new THREE.Group(); const org = {};
  const grass = canvasTexture('pond-bank', 512, 512, (c, w, h) => { c.fillStyle = '#7b9a4c'; c.fillRect(0, 0, w, h); for (let i = 0; i < 7000; i++) { c.strokeStyle = Math.random() < 0.5 ? 'rgba(70,100,40,.6)' : 'rgba(150,160,80,.5)'; c.beginPath(); const x = Math.random() * w; const y = Math.random() * h; c.moveTo(x, y); c.lineTo(x + (Math.random() - 0.5) * 5, y - 6); c.stroke(); } }, { repeat: [12, 12] });
  const ground = mesh(new THREE.RingGeometry(PR + 1.5, 90, 64, 2), new THREE.MeshStandardMaterial({ map: grass, roughness: 1 })); ground.rotation.x = -Math.PI / 2; ground.position.set(PC.x, -0.02, PC.z); g.add(ground);
  const mud = mesh(new THREE.RingGeometry(PR - 0.05, PR + 1.6, 48), new THREE.MeshStandardMaterial({ color: 0x5a4632, roughness: 1 })); mud.rotation.x = -Math.PI / 2; mud.position.set(PC.x, -0.01, PC.z); g.add(mud);
  const bed = mesh(new THREE.CircleGeometry(PR, 48), new THREE.MeshStandardMaterial({ color: 0x3b3322, roughness: 1 })); bed.rotation.x = -Math.PI / 2; bed.position.set(PC.x, -5, PC.z); g.add(bed);
  const wall = mesh(new THREE.CylinderGeometry(PR, PR * 0.85, 5, 48, 1, true), new THREE.MeshStandardMaterial({ color: 0x4a3c28, roughness: 1, side: THREE.BackSide }), [PC.x, -2.5, PC.z]); g.add(wall);
  const water = mesh(new THREE.CircleGeometry(PR, 48), new THREE.MeshPhysicalMaterial({ color: 0x4f7f5a, roughness: 0.08, transparent: true, opacity: 0.72, clearcoat: 1, depthWrite: false }), [PC.x, -0.3, PC.z], { cast: false });
  water.rotation.x = -Math.PI / 2; water.renderOrder = 3; g.add(water); org.water = water;
  const at = (a, r, y = -0.28) => new THREE.Vector3(PC.x + Math.cos(a) * r, y, PC.z + Math.sin(a) * r);
  // Typha at the margin
  const typha = new THREE.Group(); typha.name = 'Typha (cattail)';
  for (let k = 0; k < 14; k++) { const p = at(-2.4 + R() * 0.9, PR - 0.6 + R() * 1.4, 0); const L = 9 + R() * 5; const b = mesh(new THREE.BoxGeometry(0.12, L, 0.03), wet(0x5f8a3a, { roughness: 0.7 }), [p.x, L / 2, p.z]); b.rotation.set((R() - 0.5) * 0.25, R() * 3, (R() - 0.5) * 0.25); typha.add(b); if (k % 3 === 0) { typha.add(mesh(new THREE.CylinderGeometry(0.03, 0.03, L + 2, 6), wet(0x6b8e23), [p.x + 0.2, (L + 2) / 2, p.z])); typha.add(mesh(new THREE.CylinderGeometry(0.22, 0.22, 2.2, 10), MAT.matte(0x5b3a1e), [p.x + 0.2, L + 0.6, p.z])); } }
  g.add(typha); org.typha = typha;
  // lotus: rooted with floating leaves and a flower
  const lotus = new THREE.Group(); lotus.name = 'Lotus (Nelumbo)';
  for (let k = 0; k < 7; k++) { const p = at(0.4 + R() * 1.1, 5 + R() * 4); const l = lotusLeaf(1.2 + R() * 0.8); l.position.copy(p); l.rotation.y = R() * 6; lotus.add(l); }
  const lp = at(0.9, 7); const fl = new THREE.Group(); fl.position.set(lp.x, 2.6, lp.z); lotus.add(mesh(new THREE.CylinderGeometry(0.05, 0.05, 2.9, 6), wet(0x4d7c0f), [lp.x, 1.2, lp.z]));
  for (let k = 0; k < 12; k++) { const pe = mesh(new THREE.SphereGeometry(0.55, 10, 8), wet(k < 6 ? 0xf9a8d4 : 0xfbcfe8, { side: THREE.DoubleSide }), [0, 0.3, 0]); pe.scale.set(0.45, 1, 0.2); const q = new THREE.Group(); q.rotation.set(0.45 + (k >= 6 ? -0.25 : 0), k * 0.52, 0, 'YXZ'); pe.position.set(0, 0.45, 0.25); q.add(pe); fl.add(q); }
  fl.add(mesh(new THREE.CylinderGeometry(0.28, 0.2, 0.2, 14), wet(0xfacc15), [0, 0.3, 0])); lotus.add(fl);
  g.add(lotus); org.lotus = lotus;
  // water hyacinth: floating rosettes with swollen petioles and lilac flower spikes
  const hy = new THREE.Group(); hy.name = 'Water hyacinth (Eichhornia)';
  for (let k = 0; k < 5; k++) {
    const p = at(2.2 + R() * 0.8, 6 + R() * 5); const ro = new THREE.Group(); ro.position.copy(p); ro.position.y = -0.2;
    for (let j = 0; j < 7; j++) { const a = j * 0.9; const pet = mesh(new THREE.SphereGeometry(0.22, 10, 8), wet(0x6aa84f), [Math.cos(a) * 0.35, 0.3, Math.sin(a) * 0.35]); pet.scale.set(1, 1.4, 1); ro.add(pet); const lf = mesh(new THREE.SphereGeometry(0.6, 12, 8), wet(0x2f7d32, { side: THREE.DoubleSide }), [Math.cos(a) * 0.75, 0.95, Math.sin(a) * 0.75]); lf.scale.set(1, 0.12, 0.85); lf.rotation.z = Math.cos(a) * 0.6; lf.rotation.x = -Math.sin(a) * 0.6; ro.add(lf); }
    if (k % 2 === 0) { ro.add(mesh(new THREE.CylinderGeometry(0.04, 0.04, 2, 6), wet(0x4d7c0f), [0, 1.6, 0])); for (let f = 0; f < 6; f++) ro.add(mesh(new THREE.SphereGeometry(0.22, 8, 6), wet(0xc4b5fd), [Math.cos(f) * 0.15, 2.2 + f * 0.18, Math.sin(f) * 0.15])); }
    hy.add(ro);
  }
  g.add(hy); org.hyacinth = hy;
  // duckweed scum: one instanced mesh of tiny fronds
  const dwN = 1400; const dw = new THREE.InstancedMesh(new THREE.CircleGeometry(0.09, 7).rotateX(-Math.PI / 2), wet(0x84cc16, { roughness: 0.4 }), dwN); const m4 = new THREE.Matrix4(); const v = new THREE.Vector3();
  for (let i = 0; i < dwN; i++) { const a = 3.6 + R() * 1.4; const r = Math.sqrt(R()) * (PR - 1); v.set(PC.x + Math.cos(a) * r, -0.27, PC.z + Math.sin(a) * r); m4.makeTranslation(v.x, v.y, v.z); dw.setMatrixAt(i, m4); }
  dw.name = 'Duckweed (Lemna)'; const dwg = new THREE.Group(); dwg.name = dw.name; dwg.add(dw); g.add(dwg); org.duckweed = dwg;
  // Hydrilla under water
  const hyd = new THREE.Group(); hyd.name = 'Hydrilla';
  for (let k = 0; k < 9; k++) { const p = at(5.0 + R() * 0.8, 3 + R() * 6, -4.6); const parts = []; let y = 0; for (let n = 0; n < 12; n++) { parts.push([new THREE.CylinderGeometry(0.025, 0.025, 0.36, 4).translate(Math.sin(n * 0.5) * 0.2, y + 0.18, 0), 0x3f7d20]); for (let w = 0; w < 4; w++) parts.push([new THREE.BoxGeometry(0.3, 0.02, 0.06).translate(0.15, 0, 0).rotateY(w * 1.57).translate(Math.sin(n * 0.5) * 0.2, y + 0.3, 0), 0x4d8f2a]); y += 0.36; }
    const m = mesh(mergeGeos(parts), new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.7 })); m.position.copy(p); hyd.add(m); }
  g.add(hyd); org.hydrilla = hyd;
  // animals
  const frog = new THREE.Group(); frog.name = 'Frog'; const fb = wet(0x5f7f3a, { roughness: 0.4 });
  const fbody = mesh(new THREE.SphereGeometry(0.5, 14, 10), fb, [0, 0.32, 0]); fbody.scale.set(1, 0.65, 1.3); frog.add(fbody);
  [-1, 1].forEach((s) => { frog.add(mesh(new THREE.SphereGeometry(0.12, 10, 8), MAT.gloss(0x1f2937), [s * 0.22, 0.6, 0.45])); const leg = mesh(new THREE.SphereGeometry(0.22, 10, 8), fb, [s * 0.45, 0.18, -0.3]); leg.scale.set(0.8, 0.6, 1.6); frog.add(leg); });
  const fp = lotus.children[0].position; frog.position.set(fp.x, -0.25, fp.z); frog.rotation.y = 2.2; g.add(frog); org.frog = frog;
  const stone = mesh(new THREE.SphereGeometry(1.0, 12, 8), MAT.matte(0x78716c), null); stone.scale.set(1.2, 0.5, 1); const sp = at(-0.6, PR - 0.8, -0.1); stone.position.copy(sp); g.add(stone);
  const snails = new THREE.Group(); snails.name = 'Snail (Pila)';
  for (let k = 0; k < 3; k++) { const s = new THREE.Group(); s.add(mesh(new THREE.TorusGeometry(0.16, 0.1, 8, 14), wet(0x7c5a3a, { roughness: 0.4 }), [0, 0.18, 0])); s.add(mesh(new THREE.ConeGeometry(0.16, 0.25, 12), wet(0x6b4a2e), [0, 0.18, 0.1]).rotateX(-1.2)); s.add(mesh(new THREE.CapsuleGeometry ? new THREE.CapsuleGeometry(0.07, 0.3, 4, 8) : new THREE.CylinderGeometry(0.07, 0.07, 0.4, 8), wet(0x9a8a72), [0.05, 0.05, 0]).rotateZ(Math.PI / 2)); s.position.set(sp.x + (k - 1) * 0.5, sp.y + 0.38, sp.z + (R() - 0.5) * 0.4); s.rotation.y = R() * 6; snails.add(s); }
  g.add(snails); org.snail = snails;
  const fish = new THREE.Group(); fish.name = 'Fish';
  for (let k = 0; k < 4; k++) { const f = new THREE.Group(); const b = mesh(new THREE.SphereGeometry(0.4, 12, 8), wet(k % 2 ? 0x94a3b8 : 0xc2410c, { roughness: 0.3 })); b.scale.set(1.8, 0.7, 0.45); f.add(b); f.add(mesh(new THREE.ConeGeometry(0.3, 0.45, 4), wet(k % 2 ? 0x94a3b8 : 0xc2410c), [-0.85, 0, 0]).rotateZ(Math.PI / 2)); f.userData.ph = R() * 6; f.userData.r = 3 + R() * 5; fish.add(f); }
  g.add(fish); org.fish = fish;
  const strider = new THREE.Group(); strider.name = 'Water strider'; strider.add(mesh(new THREE.CylinderGeometry(0.04, 0.03, 0.5, 6), MAT.gloss(0x1f2937)).rotateX(Math.PI / 2)); [-1, 1].forEach((s) => [-0.15, 0.05, 0.2].forEach((z) => { const L = mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.6, 4), MAT.gloss(0x1f2937), [s * 0.28, -0.03, z]); L.rotation.z = s * 1.35; strider.add(L); }));
  strider.position.copy(at(1.6, 3.5, -0.2)); g.add(strider); org.strider = strider;
  const dfly = new THREE.Group(); dfly.name = 'Dragonfly'; dfly.add(mesh(new THREE.CylinderGeometry(0.05, 0.03, 0.9, 6), wet(0x0e7490), null).rotateX(Math.PI / 2)); [-1, 1].forEach((s) => [0.12, -0.05].forEach((z) => { const w = mesh(new THREE.PlaneGeometry(0.7, 0.14), new THREE.MeshPhysicalMaterial({ color: 0xe0f2fe, transparent: true, opacity: 0.55, side: THREE.DoubleSide, depthWrite: false }), [s * 0.38, 0.02, z]); w.rotation.x = -Math.PI / 2; dfly.add(w); }));
  dfly.position.copy(at(-1.4, 8, 2.5)); g.add(dfly); org.dragonfly = dfly;
  const tad = new THREE.Group(); tad.name = 'Tadpoles'; for (let k = 0; k < 6; k++) { const t = new THREE.Group(); t.add(mesh(new THREE.SphereGeometry(0.12, 8, 6), wet(0x292524))); t.add(mesh(new THREE.ConeGeometry(0.06, 0.35, 5), wet(0x44403c), [-0.2, 0, 0]).rotateZ(Math.PI / 2)); t.position.copy(at(-0.2 + R() * 0.5, PR - 2.2 - R(), -0.9)); t.rotation.y = R() * 6; tad.add(t); }
  g.add(tad); org.tadpole = tad;
  return { group: g, org, at };
}

/** Swim, skate and hover. */
export function animatePond(p, t) {
  p.org.fish.children.forEach((f, i) => { const a = t * 0.3 + f.userData.ph; f.position.set(PC.x + Math.cos(a) * f.userData.r, -1.6 - (i % 2) * 0.6, PC.z + Math.sin(a) * f.userData.r); f.rotation.y = -a - Math.PI / 2 * 0; });
  p.org.dragonfly.position.y = 2.5 + Math.sin(t * 2) * 0.2; p.org.dragonfly.rotation.y = Math.sin(t * 0.7) * 0.6;
  p.org.tadpole.children.forEach((q, i) => { q.rotation.y += Math.sin(t * 3 + i) * 0.02; });
}
