/**
 * Height and distance (NEB class 10) in 3D. An observer with a clinometer on a tripod looks at the top
 * of a tower like Kathmandu's Dharahara, across a school field. Move the observer, raise or lower the
 * tower, or snap the angle to 30°, 45° or 60°; the right-angled triangle hangs in the scene (line of
 * sight, base, perpendicular, the angle arc) and the working tan θ = perpendicular ⁄ base is written out
 * for whichever quantity is unknown. The depression figure looks down from the top: the angle of
 * depression equals the angle of elevation (alternate angles).
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { createField, label, THREE } from '../physics/physics3d/field.js';

const DEG = Math.PI / 180; const EXACT = { 30: '1/√3', 45: '1', 60: '√3' };
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

function tower() {
  const g = new THREE.Group();
  const white = new THREE.MeshStandardMaterial({ color: 0xf3efe6, roughness: 0.7 });
  const bronze = new THREE.MeshStandardMaterial({ color: 0xb08d3c, metalness: 0.8, roughness: 0.35 });
  const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 1.0, 1, 16), white); shaft.position.y = 0.5; shaft.castShadow = true; g.add(shaft);
  const base = new THREE.Mesh(new THREE.CylinderGeometry(1.7, 1.9, 0.05, 16), white); base.position.y = 0.025; g.add(base);
  const balcony = new THREE.Mesh(new THREE.CylinderGeometry(0.95, 0.75, 0.025, 20), white); g.add(balcony);
  const dome = new THREE.Mesh(new THREE.SphereGeometry(0.62, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), bronze); g.add(dome);
  const spire = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.14, 12), bronze); g.add(spire);
  const windows = new THREE.InstancedMesh(new THREE.BoxGeometry(0.12, 0.18, 0.04), new THREE.MeshStandardMaterial({ color: 0x334155 }), 40); g.add(windows);
  return {
    group: g,
    set(H) {
      const s = H - 4; shaft.scale.y = s; shaft.position.y = s / 2 + 0.05; balcony.position.y = s * 0.82; dome.position.y = s; dome.scale.set(1, 3 / 0.62 / 2, 1); spire.position.y = s + 3 + 0.07 + 0.9; spire.scale.set(1, 1, 1);
      const m4 = new THREE.Matrix4(); let n = 0;
      for (let k = 0; k < 5; k++) for (let j = 0; j < 8; j++) { const y = s * (0.15 + k * 0.17); const a = j / 8 * Math.PI * 2 + k * 0.4; const r = 1.0 - (y / s) * 0.38 + 0.01; m4.makeRotationY(-a + Math.PI / 2).setPosition(Math.cos(a) * r, y, Math.sin(a) * r); windows.setMatrixAt(n++, m4); }
      windows.instanceMatrix.needsUpdate = true;
    },
  };
}

function observer() {
  const g = new THREE.Group();
  const skin = new THREE.MeshStandardMaterial({ color: 0xc58c6a, roughness: 0.7 }); const shirt = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.8 }); const pants = new THREE.MeshStandardMaterial({ color: 0x1e3a8a, roughness: 0.8 });
  const add = (geo, mat, x, y, z) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = true; g.add(m); return m; };
  add(new THREE.CapsuleGeometry(0.07, 0.75, 4, 10), pants, 0, 0.45, -0.09); add(new THREE.CapsuleGeometry(0.07, 0.75, 4, 10), pants, 0, 0.45, 0.09);
  add(new THREE.CapsuleGeometry(0.17, 0.45, 6, 14), shirt, 0, 1.15, 0); add(new THREE.SphereGeometry(0.12, 20, 14), skin, 0.02, 1.55, 0);
  const steel = new THREE.MeshStandardMaterial({ color: 0x9aa3ad, metalness: 0.8, roughness: 0.3 });
  const tripod = new THREE.Group(); tripod.position.set(0.45, 0, 0); g.add(tripod);
  for (let i = 0; i < 3; i++) { const a = i / 3 * Math.PI * 2; const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 1.5, 6), steel); leg.position.set(Math.cos(a) * 0.18, 0.72, Math.sin(a) * 0.18); leg.rotation.set(Math.sin(a) * 0.25, 0, -Math.cos(a) * 0.25); tripod.add(leg); }
  const clino = new THREE.Group(); tripod.add(clino);
  const tube = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.32, 12), new THREE.MeshStandardMaterial({ color: 0x1f2937 })); tube.rotation.z = Math.PI / 2; clino.add(tube);
  const arc = new THREE.Mesh(new THREE.CircleGeometry(0.12, 24, Math.PI, Math.PI), new THREE.MeshStandardMaterial({ color: 0xfde68a, side: THREE.DoubleSide })); arc.position.y = -0.02; clino.add(arc);
  return { group: g, tripod, clino };
}

export default function init(stage) {
  const F = createField(stage, { camera: [-10, 14, 60], target: [-20, 18, 0], maxDistance: 400 });
  if (!F) return null;
  const { engine, scene, camera, controls } = F;
  const hud = createHud(stage);
  const badge = hud.badge('Move the observer or change the tower', '#2563eb');

  let d = 40; let H = 41.6; let hi = 1.6; let unknown = 'height'; let view = 'elevation'; let dS = d; let HS = H;
  const T = tower(); scene.add(T.group);
  const O = observer(); scene.add(O.group);
  const lineMat = (c) => new THREE.MeshBasicMaterial({ color: c, toneMapped: false });
  const seg = (c, r = 0.07) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 1, 8), lineMat(c)); scene.add(m); return m; };
  const sight = seg(0xf59e0b, 0.09); const base = seg(0x2563eb); const perp = seg(0x16a34a); const horiz = seg(0x94a3b8, 0.05);
  const arc = new THREE.Mesh(new THREE.RingGeometry(5.6, 6.0, 48, 1, 0, 1), new THREE.MeshBasicMaterial({ color: 0xf59e0b, side: THREE.DoubleSide, toneMapped: false })); scene.add(arc);
  const sq = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.6), new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide, transparent: true, opacity: 0.85 })); scene.add(sq);
  const target = new THREE.Mesh(new THREE.SphereGeometry(0.6, 16, 10), new THREE.MeshBasicMaterial({ color: 0xef4444 })); scene.add(target);
  const L = { th: label(stage, camera), d: label(stage, camera), p: label(stage, camera), H: label(stage, camera) };
  L.th.el.style.color = '#fcd34d'; L.d.el.style.color = '#93c5fd'; L.p.el.style.color = '#86efac';

  const panel = createPanel(stage, { title: 'Height and distance' });
  panel.chips({ label: 'Figure', options: [{ value: 'elevation', label: 'Angle of elevation' }, { value: 'depression', label: 'Angle of depression' }], value: 'elevation', onChange: (v) => { view = v; } });
  panel.chips({ label: 'What is unknown?', options: [{ value: 'height', label: 'Height' }, { value: 'distance', label: 'Distance' }, { value: 'angle', label: 'Angle' }], value: 'height', onChange: (v) => { unknown = v; } });
  panel.chips({ label: 'Snap the angle', options: [{ value: '30', label: '30°' }, { value: '45', label: '45°' }, { value: '60', label: '60°' }], value: '', onChange: (v) => { const t = Math.tan(+v * DEG); if (unknown === 'distance') d = Math.round((H - hi) / t * 10) / 10; else H = Math.round((d * t + hi) * 10) / 10; dSl.set(d); hSl.set(H); } });
  const dSl = panel.slider({ label: 'Distance from the tower', min: 5, max: 140, step: 0.5, value: d, format: (v) => `${v} m`, onChange: (v) => { d = v; } });
  const hSl = panel.slider({ label: 'Height of the tower', min: 8, max: 100, step: 0.5, value: H, format: (v) => `${v} m`, onChange: (v) => { H = v; } });
  panel.slider({ label: 'Height of the instrument', min: 0, max: 2, step: 0.1, value: hi, format: (v) => `${v.toFixed(1)} m`, onChange: (v) => { hi = v; } });
  const st = panel.stats([{ key: 'th', label: 'Angle θ' }, { key: 'd', label: 'Distance (base)' }, { key: 'p', label: 'Perpendicular' }, { key: 'H', label: 'Height of tower' }]);
  const work = document.createElement('div'); work.style.cssText = 'font:600 12px ui-monospace,Menlo,monospace;color:#e2e8f0;padding:10px 12px;border-radius:12px;background:rgba(255,255,255,0.05);line-height:1.6;flex-shrink:0;white-space:pre'; panel.body.appendChild(work);
  panel.info('tan θ = perpendicular ⁄ base. The perpendicular is measured from the instrument\'s eye level, so add the instrument height back to get the full height. Standard values: tan 30° = 1/√3, tan 45° = 1, tan 60° = √3.');

  const A = new THREE.Vector3(); const B = new THREE.Vector3(); const Y = new THREE.Vector3(0, 1, 0); const D = new THREE.Vector3();
  function put(m, a, b) { D.subVectors(b, a); const len = D.length(); m.position.copy(a).addScaledVector(D, 0.5); m.scale.set(1, Math.max(1e-3, len), 1); m.quaternion.setFromUnitVectors(Y, D.normalize()); }
  let camR = 70; let arcKey = '';
  function arcTo(r, ang) { const k = `${r.toFixed(2)}|${ang.toFixed(3)}`; if (k === arcKey) return; arcKey = k; arc.geometry.dispose(); arc.geometry = new THREE.RingGeometry(r, r + 0.5, 48, 1, 0, ang); }
  engine.setUpdate((dt) => {
    dS += (d - dS) * (1 - Math.exp(-dt * 6)); HS += (H - HS) * (1 - Math.exp(-dt * 6));
    const dd = dS; const HH = HS; const p = HH - hi; const th = Math.atan2(p, dd);
    T.set(HH);
    O.group.position.set(-dd - 0.45, 0, 0); O.clino.position.set(0, hi, 0); O.clino.rotation.z = th; O.tripod.visible = hi > 0.2;
    const eye = A.set(-dd, hi, 0); const top = new THREE.Vector3(0, HH, 0); const foot = new THREE.Vector3(0, hi, 0);
    if (view === 'elevation') {
      put(sight, eye, top); put(base, eye, foot); put(perp, foot, top); horiz.visible = false; target.visible = false;
      arc.position.copy(eye); arc.rotation.set(0, 0, 0); arcTo(Math.min(8, dd * 0.3), th);
      sq.position.set(-0.8, hi + 0.8, 0.05); sq.visible = true;
    } else {
      const gpt = new THREE.Vector3(-dd, 0, 0);
      put(sight, top, gpt); put(horiz, top, new THREE.Vector3(-dd, HH, 0)); horiz.visible = true; put(base, gpt, new THREE.Vector3(0, 0, 0)); put(perp, new THREE.Vector3(0, 0, 0), top);
      target.visible = true; target.position.copy(gpt);
      const thd = Math.atan2(HH, dd);
      arc.position.copy(top); arc.rotation.set(0, 0, Math.PI); arcTo(Math.min(8, dd * 0.3), thd);
      sq.position.set(-0.8, 0.8, 0.05);
    }
    const want = Math.max(dd, HH) * 1.35 + 20; camR += (want - camR) * (1 - Math.exp(-dt * 1.5));
    controls.setTarget(B.set(-dd * 0.5, HH * 0.45, 0)); if (Math.abs(want - camR) > 0.5) controls.setDistance(camR);
    controls.update(dt);
    const ang = Math.round(th / DEG * 10) / 10; const t = Math.tan(th); const ex = EXACT[Math.round(ang)] && Math.abs(ang - Math.round(ang)) < 0.05 ? EXACT[Math.round(ang)] : null;
    L.th.el.textContent = `θ = ${fmt(ang, 1)}°`; L.th.at(B.set(view === 'elevation' ? -dd + Math.min(8, dd * 0.3) + 3 : -Math.min(8, dd * 0.3) - 3, view === 'elevation' ? hi + 2 : HH - 2, 0));
    L.d.el.textContent = `d = ${fmt(dd, 1)} m`; L.d.at(B.set(-dd / 2, view === 'elevation' ? hi : 0, 0), 16);
    L.p.el.textContent = view === 'elevation' ? `p = ${fmt(p, 1)} m` : `H = ${fmt(HH, 1)} m`; L.p.at(B.set(2.5, view === 'elevation' ? (hi + HH) / 2 : HH / 2, 0));
    L.H.el.textContent = `tower ${fmt(HH, 1)} m`; L.H.at(B.set(0, HH + 5, 0));
    const lines = unknown === 'height' ? ['tan θ = p ⁄ d', `p = d × tan ${fmt(ang, 1)}°`, `  = ${fmt(dd, 1)} × ${ex || fmt(t, 3)} = ${fmt(p, 2)} m`, `H = p + ${fmt(hi, 1)} = ${fmt(HH, 2)} m`]
      : unknown === 'distance' ? ['tan θ = p ⁄ d', `d = p ⁄ tan ${fmt(ang, 1)}°`, `  = ${fmt(p, 1)} ⁄ ${ex || fmt(t, 3)} = ${fmt(dd, 2)} m`]
        : [`tan θ = p ⁄ d = ${fmt(p, 1)} ⁄ ${fmt(dd, 1)} = ${fmt(t, 3)}`, `θ = tan⁻¹ ${fmt(t, 3)} = ${fmt(ang, 1)}°`];
    work.textContent = lines.join('\n');
    st.th.set(`${fmt(ang, 1)}°`); st.d.set(`${fmt(dd, 1)} m`); st.p.set(`${fmt(p, 1)} m`); st.H.set(`${fmt(HH, 1)} m`);
    badge.set(view === 'depression' ? `Angle of depression from the top = ${fmt(Math.atan2(HH, dd) / DEG, 1)}° (alternate angles with the elevation)` : `Angle of elevation ${fmt(ang, 1)}°${ex ? `: tan ${Math.round(ang)}° = ${ex}` : ''}`);
  });
  engine.start();

  stage.__hd = { set: (dd, hh) => { d = dd; H = hh; dSl.set(dd); hSl.set(hh); }, view: (v) => { view = v; } };
  return { dispose() { panel.dispose(); hud.dispose(); Object.values(L).forEach((l) => l.remove()); controls.dispose(); engine.dispose(); } };
}
