/**
 * Ramps and rolling in 3D: a 3 m, three-lane ramp on the school field. Tilt it, pick the surface and
 * race a solid ball, a hoop and a sliding block side by side. Rolling without slipping, a solid ball
 * accelerates at a = (5/7)·g·(sin θ − c·cos θ), a hoop at ½·g·(…), a sliding block at g(sin θ − μ cos θ);
 * if the slope is too gentle for the surface one never starts. Each lane's stopwatch and the formula
 * t = √(2L/a) agree.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { createField, label, THREE } from './physics3d/field.js';

const DEG = Math.PI / 180; const G = 9.81; const L = 3; const LANE = 0.5;
const ROLLERS = [
  { value: 'ball', label: 'Solid ball', f: 5 / 7, color: 0xe5484d },
  { value: 'hoop', label: 'Hoop', f: 1 / 2, color: 0x7c3aed },
  { value: 'block', label: 'Sliding block', f: 1, color: 0xf08c00 },
];
const SURF = [
  { value: 'glass', label: 'Smooth', c: 0.005, mu: 0.05, color: 0xbfe3f7, rough: 0.05 },
  { value: 'wood', label: 'Wood', c: 0.02, mu: 0.3, color: 0xd9b07a, rough: 0.6 },
  { value: 'carpet', label: 'Carpet', c: 0.12, mu: 0.55, color: 0x8c6ca8, rough: 1 },
  { value: 'sand', label: 'Sand', c: 0.3, mu: 0.7, color: 0xe6cf98, rough: 1 },
];
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

export default function init(stage) {
  const F = createField(stage, { camera: [3.8, 2.4, 4.8], target: [1.3, 0.6, 0], maxDistance: 30 });
  if (!F) return null;
  const { engine, scene, camera, controls } = F;
  { const c = F.key.shadow.camera; c.left = -6; c.right = 6; c.top = 6; c.bottom = -6; c.updateProjectionMatrix(); }
  const hud = createHud(stage);
  const badge = hud.badge('Tilt the ramp, pick a surface, then Go', '#2563eb');

  let theta = 20 * DEG; let surf = SURF[1]; let racing = false; let t = 0;
  const R = ROLLERS.map((r) => ({ ...r, s: 0, v: 0, done: false, stuck: false, tEnd: 0 }));

  const ramp = new THREE.Group(); scene.add(ramp);
  const deckMat = new THREE.MeshStandardMaterial({ color: surf.color, roughness: surf.rough });
  const deck = new THREE.Mesh(new THREE.BoxGeometry(L, 0.04, LANE * 3 + 0.12), deckMat); deck.position.x = L / 2; deck.receiveShadow = true; deck.castShadow = true; ramp.add(deck);
  const railMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.5 });
  for (let i = 0; i <= 3; i++) { const rail = new THREE.Mesh(new THREE.BoxGeometry(L, 0.06, 0.02), railMat); rail.position.set(L / 2, 0.05, (i - 1.5) * LANE); rail.castShadow = true; ramp.add(rail); }
  const finish = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.005, LANE * 3), new THREE.MeshBasicMaterial({ color: 0xffffff })); finish.position.set(L - 0.05, 0.025, 0); ramp.add(finish);
  const legMat = new THREE.MeshStandardMaterial({ color: 0x6b4a2b, roughness: 0.8 });
  const leg = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1, 0.08), legMat); leg.castShadow = true; scene.add(leg);
  const leg2 = leg.clone(); scene.add(leg2);
  const meshes = R.map((r) => {
    let m;
    if (r.value === 'ball') m = new THREE.Mesh(new THREE.SphereGeometry(0.12, 32, 20), new THREE.MeshPhysicalMaterial({ color: r.color, roughness: 0.25, clearcoat: 0.6 }));
    else if (r.value === 'hoop') { m = new THREE.Mesh(new THREE.TorusGeometry(0.12, 0.018, 12, 40), new THREE.MeshStandardMaterial({ color: r.color, metalness: 0.6, roughness: 0.3 })); }
    else m = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.16, 0.2), new THREE.MeshStandardMaterial({ color: r.color, roughness: 0.6 }));
    m.castShadow = true; scene.add(m); return m;
  });
  const lbls = R.map(() => label(stage, camera));
  const angLbl = label(stage, camera);

  const panel = createPanel(stage, { title: 'Ramp race' });
  const angS = panel.slider({ label: 'Ramp angle θ', min: 3, max: 60, step: 1, value: 20, format: (x) => `${x}°`, onChange: (x) => { theta = x * DEG; reset(); } });
  panel.chips({ label: 'Ramp surface', options: SURF.map((r) => ({ value: r.value, label: r.label })), value: 'wood', onChange: (x) => { surf = SURF.find((r) => r.value === x); deckMat.color.setHex(surf.color); deckMat.roughness = surf.rough; reset(); } });
  panel.buttonRow([{ label: 'Go!', icon: 'flag', onClick: go }, { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: reset }]);
  const st = panel.stats(R.map((r, i) => ({ key: `r${i}`, label: r.label })));
  panel.info('The ramp is 3 m long. Gravity pulls along the slope with g·sin θ, so steeper is faster. A rolling ball also has to spin up, so it is slower than a frictionless slide; a hoop, with all its mass at the rim, is slower still.');

  function accel(r) { return r.value === 'block' ? G * (Math.sin(theta) - surf.mu * Math.cos(theta)) : r.f * G * (Math.sin(theta) - surf.c * Math.cos(theta)); }
  function reset() { racing = false; t = 0; R.forEach((r) => { r.s = 0; r.v = 0; r.done = false; r.stuck = false; r.tEnd = 0; }); }
  function go() { reset(); racing = true; R.forEach((r) => { if (accel(r) <= 0) r.stuck = true; }); }

  const v3 = new THREE.Vector3(); const dir = new THREE.Vector3(); const nrm = new THREE.Vector3();
  engine.setUpdate((dt) => {
    controls.update(dt);
    const H = L * Math.sin(theta);
    ramp.position.set(0, H + 0.04, 0); ramp.rotation.z = -theta;
    leg.scale.y = H; leg.position.set(0.04, H / 2, -LANE * 1.5 - 0.1); leg2.scale.y = H; leg2.position.set(0.04, H / 2, LANE * 1.5 + 0.1);
    dir.set(Math.cos(theta), -Math.sin(theta), 0); nrm.set(Math.sin(theta), Math.cos(theta), 0);
    if (racing) {
      t += dt;
      R.forEach((r) => {
        if (r.done || r.stuck) return;
        const a = accel(r); r.v += a * dt; r.s += r.v * dt;
        if (r.s >= L - 0.17) { r.s = L - 0.17; r.done = true; r.tEnd = Math.sqrt(2 * (L - 0.17) / a); }
      });
      if (R.every((r) => r.done || r.stuck)) racing = false;
    }
    R.forEach((r, i) => {
      const m = meshes[i]; const z = (i - 1) * LANE; const lift = r.value === 'block' ? 0.08 : 0.12;
      const s = 0.17 + r.s;
      m.position.set(0, H + 0.04, z).addScaledVector(dir, s).addScaledVector(nrm, 0.02 + lift);
      if (r.value === 'ball') m.rotation.z = -r.s / 0.12;
      else if (r.value === 'hoop') { m.rotation.set(0, 0, -r.s / 0.12); }
      else m.rotation.set(0, 0, -theta);
      const a = accel(r);
      lbls[i].el.textContent = r.stuck ? `${r.label}: stuck` : r.done ? `${r.label}: ${fmt(r.tEnd, 2)} s` : racing ? `${fmt(t, 2)} s` : r.label;
      lbls[i].at(v3.copy(m.position).add(nrm.clone().multiplyScalar(0.35)));
      st[`r${i}`].set(a <= 0 ? 'never starts' : `a = ${fmt(a, 2)} m/s² · t = √(2L/a) = ${fmt(Math.sqrt(2 * (L - 0.17) / a), 2)} s`);
    });
    angLbl.el.textContent = `θ = ${Math.round(theta / DEG)}°`; angLbl.at(v3.set(L * Math.cos(theta) - 0.6, 0.12, LANE * 1.5 + 0.3));
    const fin = R.filter((r) => r.done).sort((a, b) => a.tEnd - b.tEnd);
    badge.set(R.some((r) => r.stuck) && !racing ? `Too gentle for ${R.filter((r) => r.stuck).map((r) => r.label.toLowerCase()).join(' and ')} on ${surf.label.toLowerCase()}` : fin.length === 3 ? `${fin[0].label} wins: it is the only one not spending energy on spinning` : racing ? 'Racing…' : 'Tilt the ramp, pick a surface, then Go');
  });
  engine.start();

  stage.__ramp = { go, set: (deg) => { theta = deg * DEG; angS.set(deg); reset(); }, state: () => R.map((r) => ({ s: r.s, done: r.done, tEnd: r.tEnd })) };
  return { dispose() { panel.dispose(); hud.dispose(); lbls.forEach((l) => l.remove()); angLbl.remove(); controls.dispose(); engine.dispose(); } };
}
