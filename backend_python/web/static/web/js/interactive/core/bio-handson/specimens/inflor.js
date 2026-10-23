// Inflorescence specimens at true size (1 unit = 10 cm), each flower carrying its age (0 bud,
// 1 open flower, 2 fruit or fading) so the order of opening can be read from the specimen:
// mustard raceme and amaranth spike (acropetal), coriander umbel, candytuft corymb and marigold
// capitulum (centripetal, outermost oldest), and a jasmine dichasial cyme (the terminal flower
// first, then the laterals: basipetal).
import { THREE } from '../../engine.js';
import { mesh, wet, rng } from '../kit.js';
import { stem, flower, bud } from './plants.js';

function pod(len = 0.22) { const g = new THREE.Group(); const m = mesh(new THREE.CylinderGeometry(0.012, 0.014, len, 8), wet(0x84a33a, { roughness: 0.5 }), [0, len / 2, 0]); g.add(m); g.add(mesh(new THREE.ConeGeometry(0.01, 0.04, 6), wet(0x6b8e23), [0, len + 0.02, 0])); return g; }
function unit(age, color, r = 0.06) { if (age === 0) return bud(0x7fae3a, r * 0.8); if (age === 1) return flower(color, r); const f = flower(color, r * 0.85); f.children.forEach((c) => { if (c.material && c.material.color) { c.material = c.material.clone(); c.material.color.lerp(new THREE.Color(0x9a8a5a), 0.55); } }); return f; }
function place(g, list, obj, age, at, dir) {
  obj.position.copy(at); if (dir) obj.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.clone().normalize());
  obj.userData.age = age; obj.traverse((o) => { o.userData.unitRoot = obj; }); g.add(obj); list.push(obj);
}

export const TYPES = {
  raceme: { name: 'Raceme', group: 'racemose', eg: 'mustard (Brassica)', note: 'Raceme: an elongated main axis bearing stalked (pedicellate) flowers, the oldest at the base and buds at the tip — acropetal.' },
  spike: { name: 'Spike', group: 'racemose', eg: 'Achyranthes / amaranth', note: 'Spike: like a raceme but the flowers are sessile (no pedicels) on the long axis.' },
  umbel: { name: 'Umbel', group: 'racemose', eg: 'coriander (Coriandrum)', note: 'Umbel: the axis is condensed; flowers on equal pedicels arise from one point, outer ones open first — centripetal.' },
  corymb: { name: 'Corymb', group: 'racemose', eg: 'candytuft (Iberis)', note: 'Corymb: lower pedicels are longer, so all flowers reach about one level; outer (lower) flowers open first.' },
  capitulum: { name: 'Capitulum (head)', group: 'racemose', eg: 'marigold / sunflower', note: 'Capitulum: a flattened receptacle crowded with sessile florets — ray florets outside, disc florets inside; the outer open first.' },
  cyme: { name: 'Dichasial cyme', group: 'cymose', eg: 'jasmine (Jasminum)', note: 'Dichasial cyme: the main axis ends in a flower (the oldest); two lateral branches below it end in younger flowers — basipetal, definite growth.' },
};

export function buildInflorescence(kind, seed = 1) {
  const R = rng(seed); const g = new THREE.Group(); const units = []; const V = (x, y, z) => new THREE.Vector3(x, y, z);
  const green = 0x5f8f2f;
  if (kind === 'raceme' || kind === 'spike') {
    const H = kind === 'raceme' ? 1.25 : 1.0; g.add(stem([[0, 0, 0], [0.01, H * 0.5, 0], [0, H, 0]], 0.016, green, 0.008));
    const n = kind === 'raceme' ? 13 : 22;
    for (let i = 0; i < n; i++) {
      const t = 0.18 + (i / (n - 1)) * 0.8; const y = H * t; const a = i * 2.4; const out = V(Math.cos(a), 0, Math.sin(a));
      const age = t < 0.42 ? 2 : t < 0.7 ? 1 : 0;
      if (kind === 'raceme') { const ped = 0.11; const base = V(0, y, 0); const tip = base.clone().addScaledVector(out, ped).add(V(0, 0.05, 0)); g.add(stem([[0, y, 0], [tip.x * 0.6, y + 0.03, tip.z * 0.6], [tip.x, tip.y, tip.z]], 0.004, green)); place(g, units, age === 2 ? pod() : unit(age, 0xfacc15, 0.055), age, tip, age === 2 ? V(out.x * 0.4, 1, out.z * 0.4) : V(out.x, 0.6, out.z)); }
      else { const tip = V(out.x * 0.035, y, out.z * 0.035); place(g, units, unit(age, 0xd9f99d, 0.028), age, tip, V(out.x, 0.5, out.z)); }
    }
  } else if (kind === 'umbel') {
    const H = 0.85; g.add(stem([[0, 0, 0], [0.02, 0.4, 0], [0, H, 0]], 0.016, green, 0.01));
    const rays = 12;
    for (let i = 0; i < rays; i++) { const a = i / rays * Math.PI * 2; const outer = i % 2 === 0; const L = outer ? 0.32 : 0.2; const tip = V(Math.cos(a) * L * 0.75, H + L * 0.7, Math.sin(a) * L * 0.75); g.add(stem([[0, H, 0], [tip.x * 0.5, H + L * 0.45, tip.z * 0.5], [tip.x, tip.y, tip.z]], 0.004, green)); place(g, units, unit(outer ? 2 : 1, 0xf8fafc, 0.045), outer ? 2 : 1, tip, V(0, 1, 0)); }
    place(g, units, unit(0, 0xf8fafc, 0.04), 0, V(0, H + 0.2, 0), V(0, 1, 0));
  } else if (kind === 'corymb') {
    const H = 0.9; g.add(stem([[0, 0, 0], [0.01, 0.5, 0], [0, H, 0]], 0.016, green, 0.008)); const top = H + 0.25;
    for (let i = 0; i < 11; i++) { const y = 0.55 + i * 0.035; const a = i * 2.4; const r = 0.28 - i * 0.022; const tip = V(Math.cos(a) * r, top - Math.abs(r) * 0.15, Math.sin(a) * r); g.add(stem([[0, y, 0], [tip.x * 0.4, (y + tip.y) / 2, tip.z * 0.4], [tip.x, tip.y, tip.z]], 0.004, green)); const age = i < 4 ? 2 : i < 8 ? 1 : 0; place(g, units, unit(age, 0xf5f3ff, 0.05), age, tip, V(0, 1, 0)); }
  } else if (kind === 'capitulum') {
    const H = 0.9; g.add(stem([[0, 0, 0], [0.02, 0.45, 0], [0, H, 0]], 0.018, green, 0.014));
    const head = new THREE.Group(); head.position.y = H; g.add(head);
    head.add(mesh(new THREE.CylinderGeometry(0.2, 0.12, 0.06, 28), wet(0x6b8e23), [0, 0, 0]));
    for (let i = 0; i < 20; i++) { const a = i / 20 * Math.PI * 2; const ray = mesh(new THREE.SphereGeometry(0.12, 10, 6), wet(0xf59e0b, { side: THREE.DoubleSide }), null); ray.scale.set(0.35, 0.06, 1); const rg = new THREE.Group(); rg.add(ray); ray.position.z = 0.12; rg.rotation.y = -a + Math.PI / 2; rg.position.set(Math.cos(a) * 0.17, 0.035, Math.sin(a) * 0.17); rg.rotation.x = 0; rg.userData.age = 2; rg.traverse((o) => { o.userData.unitRoot = rg; }); head.add(rg); units.push(rg); }
    for (let i = 0; i < 70; i++) { const r = Math.sqrt(i / 70) * 0.16; const a = i * 2.4; const age = r > 0.11 ? 1 : 0; const d = mesh(new THREE.CylinderGeometry(0.012, 0.012, age ? 0.035 : 0.02, 6), wet(age ? 0xb45309 : 0x65a30d), [Math.cos(a) * r, 0.04, Math.sin(a) * r]); d.userData.age = age; d.userData.unitRoot = d; head.add(d); units.push(d); }
  } else {
    const H = 0.85; g.add(stem([[0, 0, 0], [0.01, 0.45, 0], [0, H, 0]], 0.016, green, 0.01));
    place(g, units, unit(2, 0xffffff, 0.07), 2, V(0, H + 0.02, 0), V(0, 1, 0));
    [-1, 1].forEach((s) => { const b = V(s * 0.2, H + 0.05, 0.02); g.add(stem([[0, H - 0.22, 0], [s * 0.1, H - 0.1, 0.01], [b.x, b.y, b.z]], 0.006, green)); place(g, units, unit(1, 0xffffff, 0.06), 1, b, V(s * 0.3, 1, 0));
      [-1, 1].forEach((q) => { const c = V(b.x + s * 0.12, H - 0.02, q * 0.11); g.add(stem([[b.x * 0.75, H - 0.08, 0], [c.x, c.y, c.z]], 0.004, green)); place(g, units, unit(0, 0xffffff, 0.045), 0, c, V(s * 0.5, 1, q * 0.5)); }); });
  }
  void R;
  return { group: g, units, kind };
}
