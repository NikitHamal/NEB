/**
 * Projectile motion in 3D, on the school field. Aim the cannon with the sliders (angle and speed),
 * fire, and watch a stroboscopic trail (a ball every 0.2 s) split the motion into steady horizontal
 * spacing and vertical free fall. Flight is integrated with RK4, with optional quadratic air drag for
 * a football (½ρC_dAv²); the no-air theory R = v² sin 2θ / g is shown alongside. Previous shots stay
 * as coloured ghosts; drag the flag along the field to set a target.
 */
import { makeRK4 } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { createField, label, THREE } from './physics3d/field.js';

const DEG = Math.PI / 180;
const KDRAG = 0.5 * 1.2 * 0.25 * Math.PI * 0.11 * 0.11 / 0.43;
const GHOSTS = [0x7c3aed, 0x0d9488, 0xdb2777, 0x0ea5e9, 0x64748b, 0x16a34a];
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

function cannon() {
  const g = new THREE.Group();
  const iron = new THREE.MeshStandardMaterial({ color: 0x2b2f36, metalness: 0.75, roughness: 0.35 });
  const wood = new THREE.MeshStandardMaterial({ color: 0x7a4f2a, roughness: 0.8 });
  const brass = new THREE.MeshStandardMaterial({ color: 0xc9a14a, metalness: 0.9, roughness: 0.3 });
  const carriage = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.35, 0.7), wood); carriage.position.set(-0.3, 0.45, 0); g.add(carriage);
  for (const z of [-0.45, 0.45]) {
    const w = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.06, 10, 28), wood); w.position.set(-0.1, 0.45, z); g.add(w);
    for (let k = 0; k < 6; k++) { const sp = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.8, 0.04), wood); sp.rotation.z = k * Math.PI / 6; sp.position.copy(w.position); g.add(sp); }
    const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.12, 14), brass); hub.rotation.x = Math.PI / 2; hub.position.copy(w.position); g.add(hub);
  }
  const pivot = new THREE.Group(); pivot.position.set(0, 0.85, 0); g.add(pivot);
  const barrel = new THREE.Mesh(new THREE.LatheGeometry([[0, -0.35], [0.2, -0.35], [0.24, -0.25], [0.2, 0], [0.16, 1.5], [0.19, 1.56], [0.19, 1.62], [0.13, 1.62], [0.13, 0.2]].map(([r, y]) => new THREE.Vector2(r, y)), 32), iron);
  barrel.rotation.z = -Math.PI / 2; pivot.add(barrel);
  const trun = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.62, 12), brass); trun.rotation.x = Math.PI / 2; pivot.add(trun);
  g.traverse((o) => { if (o.isMesh) o.castShadow = true; });
  return { group: g, pivot, barrel };
}

export default function init(stage) {
  const F = createField(stage, { camera: [14, 7, 34], target: [14, 5, 0] });
  if (!F) return null;
  const { engine, scene, camera, controls } = F;
  const hud = createHud(stage);
  const badge = hud.badge('Set the angle and speed, then fire', '#2563eb');

  let v0 = 22; let ang = 45 * DEG; let g = 9.81; let air = false;
  const s = new Float64Array(4);
  let launchA = ang; let launchV = v0; let launchAir = false;
  let flying = false; let tFly = 0; let apexH = 0; let result = null; let targetX = 40; let hit = 0; let recoil = 0;
  const pts = []; const ghosts = [];
  const rk = makeRK4(4, (t, y, o) => {
    o[0] = y[2]; o[1] = y[3];
    if (air) { const sp = Math.hypot(y[2], y[3]); o[2] = -KDRAG * sp * y[2]; o[3] = -g - KDRAG * sp * y[3]; } else { o[2] = 0; o[3] = -g; }
  });

  const C = cannon(); C.group.scale.setScalar(1.5); scene.add(C.group);
  const MUZ = 1.62 * 1.5;
  const ballMat = new THREE.MeshStandardMaterial({ color: 0x1f2328, metalness: 0.6, roughness: 0.35 });
  const footMat = new THREE.MeshStandardMaterial({ color: 0xf5f5f0, roughness: 0.5 });
  const ball = new THREE.Mesh(new THREE.SphereGeometry(0.11, 24, 16), ballMat); ball.castShadow = true; scene.add(ball);
  const STROBE = 60;
  const strobe = new THREE.InstancedMesh(new THREE.SphereGeometry(0.2, 16, 10), new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.4, transparent: true, opacity: 0.85 }), STROBE);
  strobe.count = 0; strobe.castShadow = true; scene.add(strobe);
  const pathGeo = new THREE.BufferGeometry(); const pathPos = new Float32Array(2400 * 3); pathGeo.setAttribute('position', new THREE.BufferAttribute(pathPos, 3));
  const path = new THREE.Line(pathGeo, new THREE.LineBasicMaterial({ color: 0xf59e0b })); path.frustumCulled = false; scene.add(path);
  const ghostGroup = new THREE.Group(); scene.add(ghostGroup);
  const theoryGeo = new THREE.BufferGeometry(); const thPos = new Float32Array(121 * 3); theoryGeo.setAttribute('position', new THREE.BufferAttribute(thPos, 3));
  const theory = new THREE.Line(theoryGeo, new THREE.LineDashedMaterial({ color: 0xffffff, dashSize: 0.5, gapSize: 0.4, transparent: true, opacity: 0.6 })); theory.frustumCulled = false; scene.add(theory);
  const flag = new THREE.Group();
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 2.2, 8), new THREE.MeshStandardMaterial({ color: 0xe5e7eb, metalness: 0.5 })); pole.position.y = 1.1;
  const cloth = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 0.6, 8, 4), new THREE.MeshStandardMaterial({ color: 0xdc2626, side: THREE.DoubleSide, roughness: 0.7 })); cloth.position.set(0.45, 1.85, 0);
  const ringM = new THREE.Mesh(new THREE.RingGeometry(0.8, 1.0, 40), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.7, side: THREE.DoubleSide })); ringM.rotation.x = -Math.PI / 2; ringM.position.y = 0.02;
  flag.add(pole, cloth, ringM); pole.castShadow = cloth.castShadow = true; scene.add(flag);
  const rangeLbl = label(stage, camera); const hLbl = label(stage, camera); const flagLbl = label(stage, camera);

  const panel = createPanel(stage, { title: 'Launch' });
  const vS = panel.slider({ label: 'Launch speed v₀', min: 5, max: 40, step: 0.5, value: v0, format: (v) => `${v.toFixed(1)} m/s`, onChange: (v) => { v0 = v; } });
  const aS = panel.slider({ label: 'Launch angle θ', min: 0, max: 90, step: 1, value: 45, format: (v) => `${v}°`, onChange: (v) => { ang = v * DEG; } });
  panel.chips({ label: 'Gravity', options: [{ value: '1.62', label: 'Moon' }, { value: '3.71', label: 'Mars' }, { value: '9.81', label: 'Earth' }], value: '9.81', onChange: (v) => { g = parseFloat(v); } });
  panel.toggle({ label: 'Air resistance (football)', value: false, onChange: (v) => { air = v; } });
  panel.buttonRow([{ label: 'Fire', icon: 'rocket_launch', onClick: fire }, { label: 'Clear', icon: 'mop', variant: 'ghost', onClick: () => { ghosts.forEach((x) => ghostGroup.remove(x)); ghosts.length = 0; pts.length = 0; result = null; flying = false; } }]);
  const tS = panel.slider({ label: 'Target flag', min: 3, max: 160, step: 0.5, value: targetX, format: (v) => `${v.toFixed(1)} m`, onChange: (v) => { targetX = v; } });
  const st = panel.stats([{ key: 'R', label: 'Range' }, { key: 'H', label: 'Max height' }, { key: 'T', label: 'Flight time' }, { key: 'th', label: 'Theory (no air)' }]);
  panel.info('Each orange ball is 0.2 s apart: sideways they are evenly spaced (no horizontal force), upwards they bunch near the top. Try 30° and 60°: the same range without air.');

  function fire() {
    if (!flying && result && pts.length > 6) archive();
    launchA = ang; launchV = v0; launchAir = air;
    s[0] = 0; s[1] = 0; s[2] = v0 * Math.cos(ang); s[3] = v0 * Math.sin(ang);
    tFly = 0; apexH = 0; pts.length = 0; flying = true; result = null; hit = 0; recoil = 1;
    ball.material = air ? footMat : ballMat;
  }
  function archive() {
    const geo = new THREE.BufferGeometry().setFromPoints(pts.map((p) => new THREE.Vector3(p[0], p[1], 0)));
    const line = new THREE.Line(geo, new THREE.LineBasicMaterial({ color: GHOSTS[ghosts.length % GHOSTS.length], transparent: true, opacity: 0.75 }));
    ghosts.unshift(line); ghostGroup.add(line);
    if (ghosts.length > 6) { const old = ghosts.pop(); ghostGroup.remove(old); old.geometry.dispose(); }
  }
  const muzzle = () => [Math.cos(ang) * MUZ - recoil * 0.25, 0.85 * 1.5 + Math.sin(ang) * MUZ];
  const v3 = new THREE.Vector3(); const m4 = new THREE.Matrix4();
  let camR = 34;

  engine.setUpdate((dt, time) => {
    if (flying) {
      let rem = dt * 1.0; const hstep = 1 / 240;
      while (rem > 1e-9 && flying) {
        const hh = Math.min(hstep, rem); const prevX = s[0]; const prevY = s[1];
        rk(s, tFly, hh); tFly += hh; rem -= hh;
        if (s[1] > apexH) apexH = s[1];
        if (s[1] < 0 && s[3] < 0) { const f = prevY / (prevY - s[1]); s[0] = prevX + (s[0] - prevX) * f; s[1] = 0; tFly -= hh * (1 - f); flying = false; result = { R: s[0], T: tFly, H: apexH }; if (Math.abs(s[0] - targetX) < Math.max(1, targetX * 0.03)) hit = 1; }
        pts.push([s[0], s[1], tFly]);
      }
    }
    recoil = Math.max(0, recoil - dt * 4);
    C.pivot.rotation.z = ang; C.group.position.x = -recoil * 0.25;
    const [mx, my] = muzzle();
    const ox = mx; const oy = my;
    // flight drawn from the muzzle, theory dashed for the current settings
    const n = Math.min(pts.length, 2400);
    for (let i = 0; i < n; i++) { pathPos[i * 3] = ox + pts[i][0]; pathPos[i * 3 + 1] = oy + pts[i][1]; pathPos[i * 3 + 2] = 0; }
    pathGeo.setDrawRange(0, n); pathGeo.attributes.position.needsUpdate = true;
    ghostGroup.position.set(ox, oy, 0);
    let si = 0;
    for (let i = 0, next = 0; i < n && si < STROBE; i++) { if (pts[i][2] >= next) { m4.makeTranslation(ox + pts[i][0], oy + pts[i][1], 0); strobe.setMatrixAt(si++, m4); next += 0.2; } }
    strobe.count = si; strobe.instanceMatrix.needsUpdate = true;
    const last = n ? pts[n - 1] : [0, 0];
    ball.visible = n > 0 || !flying; ball.position.set(ox + last[0], oy + last[1], 0); ball.rotation.z -= dt * 6;
    const R0 = v0 * v0 * Math.sin(2 * ang) / g;
    for (let i = 0; i <= 120; i++) { const x = R0 * i / 120; const t = x / Math.max(1e-6, v0 * Math.cos(ang)); thPos[i * 3] = ox + x; thPos[i * 3 + 1] = oy + v0 * Math.sin(ang) * t - 0.5 * g * t * t; thPos[i * 3 + 2] = 0; }
    theoryGeo.attributes.position.needsUpdate = true; theory.computeLineDistances(); theory.visible = !flying && !result;
    flag.position.set(ox + targetX, 0, 0); cloth.rotation.y = Math.sin(time * 2) * 0.25;
    ringM.material.color.setHex(hit > 0 ? 0x22c55e : 0xffffff); hit = Math.max(0, hit - dt * 0.4);
    // frame the whole shot
    const span = Math.max(R0 * 1.15, targetX + 6, result ? result.R + 6 : 0, 18);
    const hgt = Math.max(v0 * v0 * Math.sin(ang) ** 2 / (2 * g), result ? result.H : 0, 4);
    const want = Math.max(span * 0.95, hgt * 2.2) + 8;
    camR += (want - camR) * (1 - Math.exp(-dt * 1.6));
    controls.setTarget(v3.set(span * 0.45, Math.min(hgt * 0.5 + 1, span * 0.3), 0));
    if (Math.abs(want - camR) > 0.3) controls.setDistance(camR);
    controls.update(dt);
    if (result) { rangeLbl.el.textContent = `${fmt(result.R, 1)} m`; rangeLbl.at(v3.set(ox + result.R, 0.6, 0), -14); hLbl.el.textContent = `${fmt(result.H, 1)} m high`; const ia = pts.findIndex((p) => p[1] >= result.H - 1e-3); if (ia >= 0) hLbl.at(v3.set(ox + pts[ia][0], oy + result.H + 1.2, 0)); }
    else { rangeLbl.el.style.opacity = '0'; hLbl.el.style.opacity = '0'; }
    flagLbl.el.textContent = `target ${fmt(targetX, 1)} m`; flagLbl.at(v3.set(ox + targetX, 2.6, 0));
    const r = result || { R: s[0], H: apexH, T: tFly };
    st.R.set(`${fmt(r.R, 1)} m`); st.H.set(`${fmt(r.H, 1)} m`); st.T.set(`${fmt(r.T, 2)} s`); st.th.set(`R = ${fmt(R0, 1)} m`);
    badge.set(flying ? 'In flight…' : result ? (hit > 0 ? 'On target!' : launchAir ? `Air drag cut the range to ${fmt(result.R / Math.max(1e-6, launchV * launchV * Math.sin(2 * launchA) / g) * 100, 0)} % of the no-air theory` : `Range ${fmt(result.R, 1)} m, ${fmt(Math.abs(result.R - targetX), 1)} m from the flag`) : 'Set the angle and speed, then fire');
  });
  engine.start();

  stage.__projectile = { fire, set: (v, a) => { v0 = v; ang = a * DEG; vS.set(v); aS.set(a); }, result: () => result };
  return { dispose() { panel.dispose(); hud.dispose(); rangeLbl.remove(); hLbl.remove(); flagLbl.remove(); controls.dispose(); engine.dispose(); } };
}
