// An adult American cockroach (Periplaneta americana), modelled in millimetres and scaled to the
// bench (1 unit = 10 cm), dorsal side up, head toward -Z. Hypognathous head with kidney-shaped
// compound eyes and long filiform antennae; a shield-like pronotum with a pale rim; leathery
// tegmina over folded membranous hind wings; three pairs of legs (coxa, trochanter, femur, spiny
// tibia, five-jointed tarsus); ten abdominal terga ending in a pair of jointed cerci. Males carry
// a pair of anal styles on the ninth sternum and wings longer than the abdomen; females have none
// and a boat-shaped seventh sternum (the brood pouch). The mouthparts come away one by one.
import { THREE } from '../../engine.js';
import { mesh, wet, canvasTexture } from '../kit.js';

const V = (x, y, z) => new THREE.Vector3(x, y, z);
function ell(rx, ry, rz, mat, pos, seg = 18) { const m = mesh(new THREE.SphereGeometry(1, seg, Math.max(8, seg / 2)), mat); m.scale.set(rx, ry, rz); if (pos) m.position.copy(pos); return m; }
function rod(a, b, r0, r1, mat) {
  const d = new THREE.Vector3().subVectors(b, a); const L = d.length();
  const m = mesh(new THREE.CylinderGeometry(r1, r0, L, 8), mat); m.position.copy(a).addScaledVector(d, 0.5);
  m.quaternion.setFromUnitVectors(V(0, 1, 0), d.normalize()); return m;
}
function wingTex(kind) {
  return canvasTexture(`roach-wing:${kind}`, 128, 512, (g, w, h) => {
    if (kind === 'teg') {
      const gr = g.createLinearGradient(0, 0, w, 0); gr.addColorStop(0, '#5a2410'); gr.addColorStop(0.55, '#7a3618'); gr.addColorStop(0.9, '#a2582a'); gr.addColorStop(1, '#c98a4a');
      g.fillStyle = gr; g.fillRect(0, 0, w, h);
      for (let i = 0; i < 260; i++) { g.fillStyle = `rgba(${30 + Math.random() * 40},${10 + Math.random() * 15},5,${Math.random() * 0.25})`; g.fillRect(Math.random() * w, Math.random() * h, 1 + Math.random() * 3, 2 + Math.random() * 6); }
    } else { g.fillStyle = 'rgba(205,165,110,0.5)'; g.fillRect(0, 0, w, h); }
    g.strokeStyle = kind === 'teg' ? 'rgba(40,15,5,0.65)' : 'rgba(120,80,40,0.7)'; g.lineWidth = 2;
    for (let i = 0; i < 9; i++) { g.beginPath(); g.moveTo(10 + i * 3, 0); g.quadraticCurveTo(20 + i * 12, h * 0.4, 8 + i * 13, h); g.stroke(); }
    for (let y = 30; y < h; y += 26) { g.lineWidth = 0.8; g.beginPath(); g.moveTo(0, y); g.lineTo(w, y + 8); g.stroke(); }
  });
}
function wingGeo(len, wid) {
  const s = new THREE.Shape(); s.moveTo(0, 0); s.bezierCurveTo(wid * 0.9, len * 0.08, wid, len * 0.7, wid * 0.35, len); s.quadraticCurveTo(0, len * 1.02, -wid * 0.1, len * 0.85); s.lineTo(0, 0);
  const g = new THREE.ShapeGeometry(s, 12); const p = g.attributes.position; const uv = g.attributes.uv;
  for (let i = 0; i < p.count; i++) uv.setXY(i, p.getX(i) / wid, p.getY(i) / len);
  g.rotateX(Math.PI / 2); return g; // lies flat, length along +Z
}

export function buildCockroach(sex = 'male') {
  const root = new THREE.Group(); const body = new THREE.Group(); body.scale.setScalar(0.01); root.add(body);
  const C = { detailScale: 0.55, detailBump: 0.0012, mottle: 0.22, sss: 0x5a1a08 };
  const chitin = wet(0x6e3216, { roughness: 0.3, clearcoat: 0.95, ccr: 0.12, sheen: 0.08, ...C });
  const dark = wet(0x2e1408, { roughness: 0.28, clearcoat: 0.95, sheen: 0.05, ...C });
  const pale = wet(0xc99a5c, { roughness: 0.36, clearcoat: 0.8, sheen: 0.1, ...C });
  const leg = wet(0x7c3e1c, { roughness: 0.34, clearcoat: 0.8, sheen: 0.1, ...C });
  const anchors = {};
  // head (bent down under the pronotum: hypognathous)
  const head = new THREE.Group(); head.position.set(0, 0.2, -10.5); head.rotation.x = 0.5; body.add(head);
  head.add(ell(2.8, 2.4, 2.6, chitin, V(0, 0, 0)));
  [-1, 1].forEach((s) => { const e = ell(0.9, 1.6, 1.0, dark, V(s * 2.3, 0.6, -0.3), 12); e.rotation.z = s * 0.3; head.add(e); });
  anchors['Compound eye'] = V(2.6, 0.6, -10.8);
  const antennae = [-1, 1].map((s) => {
    const pts = [V(s * 0.9, 1.0, -12.2), V(s * 5, 2.0, -20), V(s * 11, 2.2, -33), V(s * 17, 1.4, -47), V(s * 20, 0.8, -56)];
    const m = mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 60, 0.28, 6), dark); body.add(m); return m;
  });
  anchors.Antenna = V(11, 2.2, -33);
  // mouthparts under the head, front to back: labrum, mandibles, maxillae (with palps), labium (with palps), hypopharynx
  const mouth = new THREE.Group(); mouth.position.set(0, -2.6, -11.6); body.add(mouth);
  const mp = [];
  const addMP = (name, obj, order) => { obj.userData.mp = { name, order }; mouth.add(obj); mp.push(obj); return obj; };
  addMP('Labrum', ell(1.6, 0.35, 1.1, pale, V(0, 0.2, -1.6), 12), 0);
  [-1, 1].forEach((s) => { const m = ell(0.9, 0.6, 1.3, dark, V(s * 1.1, -0.1, -0.9), 10); m.rotation.y = s * 0.5; addMP('Mandible', m, 1); });
  [-1, 1].forEach((s) => { const g = new THREE.Group(); g.add(ell(0.6, 0.35, 1.6, pale, V(0, 0, 0), 10)); g.add(rod(V(0.3 * s, 0, -0.6), V(2.2 * s, -0.4, -2.2), 0.2, 0.14, leg)); g.position.set(s * 1.7, -0.3, -0.2); addMP('Maxilla', g, 2); });
  { const g = new THREE.Group(); g.add(ell(1.4, 0.35, 1.0, pale, V(0, 0, 0), 12)); [-1, 1].forEach((s) => g.add(rod(V(s * 0.8, 0, -0.4), V(s * 1.6, -0.4, -2.0), 0.18, 0.12, leg))); g.position.set(0, -0.55, 0.6); addMP('Labium', g, 3); }
  addMP('Hypopharynx', ell(0.45, 0.35, 0.9, wet(0xe9c9a0, { roughness: 0.5 }), V(0, 0.1, 0.0), 10), 4);
  // pronotum: a pale-rimmed shield over the head
  body.add(ell(5.2, 1.0, 4.4, pale, V(0, 2.4, -6.6), 24));
  body.add(ell(4.4, 0.9, 3.7, wet(0x4a220e, { roughness: 0.3, clearcoat: 0.9 }), V(0, 2.62, -6.5), 20));
  anchors.Pronotum = V(3.5, 3.2, -6.5);
  // meso and metathorax, abdomen
  body.add(ell(5.3, 1.6, 2.4, chitin, V(0, 1.4, -2.4)));
  body.add(ell(5.6, 1.6, 2.4, chitin, V(0, 1.3, 0.6)));
  const AW = [5.6, 6.0, 6.2, 6.2, 6.0, 5.5, 4.9, 4.1, 3.3, 2.4];
  const terga = AW.map((w, i) => { const t = ell(w * (sex === 'female' ? 1.06 : 1), 1.25 - i * 0.05, 1.5, i % 2 ? chitin : wet(0x6e3818, { roughness: 0.35, clearcoat: 0.9 }), V(0, 1.1 - i * 0.05, 3.2 + i * 2.05), 18); body.add(t); return t; });
  anchors['Abdominal tergum'] = V(5.5, 1.4, 9.4);
  // ventral sterna; the 7th of a female is boat-shaped (brood pouch)
  AW.forEach((w, i) => { const st = ell(w * 0.9, 0.5, 1.35, pale, V(0, 0.1, 3.2 + i * 2.05), 14); if (sex === 'female' && i === 6) { st.scale.set(w * 0.95, 1.1, 2.6); st.position.z += 1.2; } body.add(st); });
  const cerci = [-1, 1].map((s) => { const g = new THREE.Group(); for (let k = 0; k < 9; k++) { const a = V(s * (1.0 + k * 0.45), 1.0 - k * 0.04, 22.6 + k * 0.62); g.add(ell(0.42 - k * 0.025, 0.42 - k * 0.025, 0.36, dark, a, 8)); } body.add(g); return g; });
  anchors.Cercus = V(3.2, 0.8, 25.5);
  if (sex === 'male') { [-1, 1].forEach((s) => body.add(rod(V(s * 0.8, -0.2, 21.4), V(s * 1.2, -0.3, 24.0), 0.16, 0.1, dark))); anchors['Anal style'] = V(1.1, -0.2, 23.6); }
  // legs: [attach z, femur dir, tibia dir, scale]
  const LEGS = [[-5.4, V(0.6, -0.12, -0.75), V(0.35, -0.12, -0.85), 0.8], [-1.6, V(1, -0.1, 0.05), V(0.45, -0.12, 0.75), 1.0], [1.6, V(1, -0.1, 0.35), V(0.3, -0.1, 0.9), 1.3]];
  const legParts = [];
  LEGS.forEach(([z, fd, td, k], li) => [-1, 1].forEach((s) => {
    const base = V(s * 3.5, 0.0, z); const coxa = rod(base, base.clone().add(V(s * 1.5, -1.1, 0.6)), 1.0, 0.8, leg); body.add(coxa);
    const f0 = base.clone().add(V(s * 1.6, -1.2, 0.6)); const f1 = f0.clone().add(V(fd.x * s, fd.y, fd.z).multiplyScalar(8 * k));
    const t1 = f1.clone().add(V(td.x * s, td.y, td.z).multiplyScalar(10 * k)); const tar = t1.clone().add(V(td.x * s * 0.7, -0.04, td.z).multiplyScalar(7.5 * k));
    body.add(rod(f0, f1, 0.75, 0.6, leg)); body.add(rod(f1, t1, 0.5, 0.42, leg));
    for (let q = 1; q < 6; q++) { const p = f1.clone().lerp(t1, q / 6); const sp = rod(p, p.clone().add(V(s * 0.5, 0.6, 0.6)), 0.12, 0.02, dark); body.add(sp); }
    for (let q = 0; q < 5; q++) { const a = t1.clone().lerp(tar, q / 5); const b = t1.clone().lerp(tar, (q + 0.92) / 5); body.add(rod(a, b, 0.3, 0.24, leg)); }
    body.add(rod(tar, tar.clone().add(V(s * 0.6, -0.3, 0.4)), 0.12, 0.04, dark));
    if (li === 2 && s > 0) { anchors.Femur = f0.clone().lerp(f1, 0.55); anchors.Tibia = f1.clone().lerp(t1, 0.5); anchors.Tarsus = t1.clone().lerp(tar, 0.6); }
    if (li === 0 && s > 0) anchors.Coxa = base.clone().add(V(s * 0.8, -0.7, 0.3));
    legParts.push(coxa);
  }));
  // wings: tegmina over folded hind wings, hinged at the mesothorax
  const wlen = sex === 'male' ? 31 : 25.5;
  const wings = [-1, 1].map((s) => {
    const hinge = new THREE.Group(); hinge.position.set(-s * 1.4, 2.9 + (s > 0 ? 0.25 : 0), -4.0); body.add(hinge);
    const hind = new THREE.Group(); hinge.add(hind);
    const hw = mesh(wingGeo(wlen * 0.92, 9.0), new THREE.MeshPhysicalMaterial({ map: wingTex('hind'), transparent: true, side: THREE.DoubleSide, roughness: 0.25, depthWrite: false }), [0, -0.3, 0]); hw.scale.x = s * 0.45; hind.add(hw);
    const teg = mesh(wingGeo(wlen, 9.4), new THREE.MeshPhysicalMaterial({ map: wingTex('teg'), side: THREE.DoubleSide, roughness: 0.3, clearcoat: 0.9, clearcoatRoughness: 0.12 }), [0, 0, 0]); teg.scale.x = s; hinge.add(teg);
    hinge.rotation.y = -s * 0.05;
    return { hinge, teg, hind, hw, s, spread: 0, fan: 0 };
  });
  anchors['Tegmen (forewing)'] = V(-4, 3.7, 11.5);
  anchors['Hind wing'] = V(15.2, 2.8, 1.5);
  function setWing(w, spread, fan) {
    w.spread = spread; w.fan = fan;
    w.teg.rotation.y = w.s * spread * 1.75; w.teg.position.y = spread * 0.6;
    w.hind.rotation.y = w.s * spread * 0.8; w.hw.scale.x = w.s * (0.45 + fan * 1.25);
  }
  wings.forEach((w) => setWing(w, 0, 0));
  return {
    root, body, head, mouth, mouthparts: mp, wings, setWing, cerci, antennae, sex,
    anchors, legParts, terga,
    /** World-space anchor for a label. */
    anchor(name, out) { return out.copy(anchors[name]).applyMatrix4(body.matrixWorld); },
  };
}
