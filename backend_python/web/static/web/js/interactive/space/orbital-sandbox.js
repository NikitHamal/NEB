/**
 * Orbital sandbox in 3D. Press on the orbital plane and drag to aim a launch (the arrow is the
 * velocity), then let go. While you aim, the path is predicted with the same leapfrog integrator,
 * green for a closed orbit, red for a crash, orange for an escape; ticks on the arrow mark circular
 * speed √(GM/r) and escape speed √(2GM/r). Units are real: GM☉ = 4π² AU³/yr², 1 AU/yr = 4.74 km/s.
 * The grid below dips as −GM/r: the gravity well every orbit is rolling around in.
 */
import { THREE } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { createSpace, makeSun, makePlanet, makeTrail, makeArrow, planeDrag } from './space3d/kit.js';

const GM1 = 4 * Math.PI * Math.PI;
const KMS = 4.7406;
const MAXP = 8; const TRAIL = 260; const PRED = 900;
const KINDS = ['earth', 'mars', 'neptune', 'venus', 'uranus', 'mercury', 'jupiter', 'saturn'];
const COLORS = [0x60a5fa, 0xf87171, 0x818cf8, 0xfbbf24, 0x5eead4, 0xd6d3d1, 0xfcd34d, 0xfde68a];
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

export default function init(stage) {
  const S = createSpace(stage, { camera: [0, 5.6, 6.4], minDistance: 2, maxDistance: 40, maxPolar: 1.5 });
  if (!S) return null;
  const { engine, scene, camera, quality, controls } = S;
  const hud = createHud(stage);
  const badge = hud.badge('Press on the plane and drag to aim, release to launch', '#60a5fa');
  const U = 1.4;

  let M = 1; let speed = 1; let showWell = true;
  const px = new Float64Array(MAXP); const pz = new Float64Array(MAXP); const vx = new Float64Array(MAXP); const vz = new Float64Array(MAXP);
  const alive = new Uint8Array(MAXP); const fate = new Uint8Array(MAXP);
  let n = 0; let last = -1; let aiming = false; let ax = 0; let az = 0; let avx = 0; let avz = 0; let predFate = 0; let pulse = 0;
  const predPts = new Float32Array(PRED * 3); let predN = 0;

  const panel = createPanel(stage, { title: 'Orbit sandbox' });
  panel.slider({ label: 'Star mass', min: 0.3, max: 3, step: 0.1, value: 1, format: (v) => `${v.toFixed(1)} M☉`, onChange: (v) => { M = v; pulse = 1; wellDirty = true; } });
  panel.chips({ label: 'Time speed', options: [{ value: '0.25', label: '¼ yr/s' }, { value: '1', label: '1 yr/s' }, { value: '3', label: '3 yr/s' }], value: '1', onChange: (v) => { speed = +v; } });
  panel.buttonRow([
    { label: 'Earth orbit', icon: 'public', onClick: () => launch(1, 0, 0, -Math.sqrt(GM1 * M)) },
    { label: 'Clear', icon: 'delete_sweep', variant: 'ghost', onClick: () => { n = 0; alive.fill(0); last = -1; bodies.forEach((b) => { b.mesh.visible = false; b.trail.clear(); }); } },
  ]);
  panel.toggle({ label: 'Gravity well', value: true, onChange: (v) => { showWell = v; } });
  const st = panel.stats([{ key: 'v', label: 'Launch speed' }, { key: 'vc', label: 'Circular speed here' }, { key: 'fate', label: 'Result' }, { key: 'T', label: 'Period (Kepler III)' }]);
  panel.info('An orbit is falling sideways forever: too slow and the planet falls into the star, too fast (above escape speed) and it leaves for good. In between it loops round on an ellipse. A heavier star needs faster planets.');

  const Rstar = () => 0.1 * Math.cbrt(M);
  const sun = makeSun(quality, Rstar() * U);
  scene.add(sun.group);

  const bodies = KINDS.map((kind, i) => {
    const mesh = makePlanet(kind, kind === 'jupiter' || kind === 'saturn' ? 0.09 : 0.065);
    mesh.visible = false;
    const trail = makeTrail(TRAIL, COLORS[i]);
    scene.add(mesh, trail.line);
    return { mesh, trail };
  });

  // rings at 1, 2, 3 AU and the gravity well
  const rings = new THREE.Group();
  for (let r = 1; r <= 3; r++) {
    const g = new THREE.RingGeometry(r * U - 0.004, r * U + 0.004, 160);
    const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: 0x8aa2d8, transparent: true, opacity: 0.25, side: THREE.DoubleSide, depthWrite: false }));
    m.rotation.x = -Math.PI / 2; rings.add(m);
  }
  scene.add(rings);
  const WN = 64; const WR = 4.6 * U;
  const wellPos = new Float32Array((WN + 1) * (WN + 1) * 3);
  const wellIdx = [];
  for (let j = 0; j <= WN; j++) for (let i = 0; i <= WN; i++) {
    const k = j * (WN + 1) + i;
    if (i < WN) wellIdx.push(k, k + 1);
    if (j < WN) wellIdx.push(k, k + WN + 1);
  }
  const wellGeo = new THREE.BufferGeometry();
  wellGeo.setAttribute('position', new THREE.BufferAttribute(wellPos, 3));
  wellGeo.setIndex(wellIdx);
  const well = new THREE.LineSegments(wellGeo, new THREE.ShaderMaterial({
    vertexShader: 'varying float vD; varying float vR; void main() { vD = -position.y; vR = length(position.xz); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: `varying float vD; varying float vR; void main() { float a = 0.22 * smoothstep(${WR.toFixed(2)}, ${(WR * 0.6).toFixed(2)}, vR); gl_FragColor = vec4(mix(vec3(0.3, 0.45, 0.85), vec3(1.0, 0.7, 0.35), clamp(vD / 2.5, 0.0, 1.0)) * a, 1.0); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  }));
  scene.add(well);
  let wellDirty = true;
  function buildWell() {
    wellDirty = false;
    for (let j = 0; j <= WN; j++) for (let i = 0; i <= WN; i++) {
      const x = (i / WN * 2 - 1) * WR; const z = (j / WN * 2 - 1) * WR; const r = Math.max(Math.hypot(x, z) / U, 0.18);
      const k = (j * (WN + 1) + i) * 3;
      wellPos[k] = x; wellPos[k + 1] = -0.3 - 0.55 * M / r; wellPos[k + 2] = z;
    }
    wellGeo.attributes.position.needsUpdate = true; wellGeo.computeBoundingSphere();
  }

  const aimArrow = makeArrow(0xe8eefb, 0.012);
  const pred = makeTrail(PRED, 0x34d399);
  const tickMat = [new THREE.MeshBasicMaterial({ color: 0x34d399, toneMapped: false }), new THREE.MeshBasicMaterial({ color: 0xfbbf24, toneMapped: false })];
  const ticks = tickMat.map((m) => new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.012, 0.16), m));
  const start = new THREE.Mesh(new THREE.SphereGeometry(0.045, 16, 10), new THREE.MeshBasicMaterial({ color: 0xe2e8f0 }));
  scene.add(aimArrow.group, pred.line, start, ...ticks);
  const aimLabel = document.createElement('div');
  aimLabel.style.cssText = 'position:absolute;left:0;top:0;pointer-events:none;font:700 12px Poppins,system-ui,sans-serif;padding:3px 9px;border-radius:999px;background:rgba(8,14,30,0.8);white-space:nowrap;z-index:3;opacity:0';
  stage.appendChild(aimLabel);

  function acc(x, z, out) { const r2 = x * x + z * z; const r = Math.sqrt(r2); const f = -GM1 * M / (r2 * r); out[0] = f * x; out[1] = f * z; }
  const A = new Float64Array(2);
  function step1(i, h) {
    acc(px[i], pz[i], A); vx[i] += A[0] * h / 2; vz[i] += A[1] * h / 2;
    px[i] += vx[i] * h; pz[i] += vz[i] * h;
    acc(px[i], pz[i], A); vx[i] += A[0] * h / 2; vz[i] += A[1] * h / 2;
  }
  function launch(x, z, ux, uz) {
    const i = n < MAXP ? n++ : (last + 1) % MAXP;
    px[i] = x; pz[i] = z; vx[i] = ux; vz[i] = uz; alive[i] = 1; fate[i] = 0; last = i;
    bodies[i].trail.clear(); bodies[i].mesh.visible = true;
  }
  function predict(x, z, ux, uz) {
    let X = x; let Z = z; let VX = ux; let VZ = uz; const h = 0.004;
    predN = 0; predFate = 0;
    const E = 0.5 * (ux * ux + uz * uz) - GM1 * M / Math.hypot(x, z);
    for (let s = 0; s < PRED * 4 && predN < PRED; s++) {
      const r = Math.hypot(X, Z);
      if (r < Rstar()) { predFate = 1; break; }
      if (r > 8) { predFate = 2; break; }
      let r3 = r * r * r; VX -= GM1 * M * X / r3 * h / 2; VZ -= GM1 * M * Z / r3 * h / 2;
      X += VX * h; Z += VZ * h;
      const r2 = Math.hypot(X, Z); r3 = r2 * r2 * r2; VX -= GM1 * M * X / r3 * h / 2; VZ -= GM1 * M * Z / r3 * h / 2;
      if (s % 4 === 0) { predPts[predN * 3] = X * U; predPts[predN * 3 + 1] = 0.01; predPts[predN * 3 + 2] = Z * U; predN++; }
    }
    if (!predFate && E >= 0) predFate = 2;
    pred.set(predPts.subarray(0, predN * 3));
    pred.mat.uniforms.uC.value.set(predFate === 1 ? 0xf87171 : predFate === 2 ? 0xfbbf24 : 0x34d399);
  }

  const drag = planeDrag(engine.canvas, camera, controls, {
    handles: () => [],
    onEmpty: (p, e) => { if (e.button === 2) return false; aiming = true; ax = p.x / U; az = p.z / U; avx = 0; avz = 0; predN = 0; pred.clear(); return true; },
    onMove: (h, p) => { avx = (p.x / U - ax) * 3; avz = (p.z / U - az) * 3; predict(ax, az, avx, avz); },
    onUp: () => { if (aiming && Math.hypot(ax, az) > Rstar() * 1.2 && Math.hypot(avx, avz) > 0.05) launch(ax, az, avx, avz); aiming = false; pred.clear(); },
  });

  const tmp = new THREE.Vector3(); const tv = new THREE.Vector3(); const v3 = new THREE.Vector3();
  engine.setUpdate((dt, time) => {
    controls.update(dt);
    if (wellDirty) buildWell();
    well.visible = showWell;
    pulse = Math.max(0, pulse - dt * 2);
    sun.group.scale.setScalar(Rstar() * U * (1 + 0.5 * pulse));
    sun.uniforms.uTime.value = time;
    const simDt = dt * speed; const sub = Math.max(1, Math.ceil(simDt / 0.0015)); const hh = simDt / sub;
    for (let i = 0; i < n; i++) {
      const b = bodies[i];
      if (!alive[i]) { b.trail.mat.uniforms.uK.value = Math.max(0.25, b.trail.mat.uniforms.uK.value - dt); continue; }
      b.trail.mat.uniforms.uK.value = 1;
      for (let s = 0; s < sub; s++) {
        step1(i, hh);
        b.acc = (b.acc || 0) + hh;
        if (b.acc >= 0.006) { b.acc = 0; b.trail.push(px[i] * U, 0, pz[i] * U); }
      }
      const r = Math.hypot(px[i], pz[i]);
      if (r < Rstar()) { alive[i] = 0; fate[i] = 1; pulse = 1; b.mesh.visible = false; }
      else if (r > 12) { alive[i] = 0; fate[i] = 2; b.mesh.visible = false; }
      b.mesh.position.set(px[i] * U, 0, pz[i] * U);
      b.mesh.rotation.y += dt * 1.5;
    }

    start.visible = aiming; aimArrow.group.visible = aiming; ticks.forEach((t) => { t.visible = aiming; }); pred.line.visible = aiming;
    if (aiming) {
      start.position.set(ax * U, 0, az * U);
      const v = Math.hypot(avx, avz);
      aimArrow.set(tmp.set(ax * U, 0, az * U), tv.set(avx / 3 * U, 0, avz / 3 * U));
      const r = Math.hypot(ax, az); const vc = Math.sqrt(GM1 * M / Math.max(r, 1e-3));
      if (v > 0.01) {
        const ux = avx / v; const uz = avz / v;
        [[1, 0], [Math.SQRT2, 1]].forEach(([mult, i]) => {
          const L = vc * mult / 3 * U;
          ticks[i].position.set(ax * U + ux * L, 0, az * U + uz * L);
          ticks[i].rotation.y = Math.atan2(ux, uz) + Math.PI / 2;
        });
      }
      const col = predFate === 1 ? '#f87171' : predFate === 2 ? '#fbbf24' : '#34d399';
      aimLabel.textContent = `${fmt(v * KMS, 1)} km/s · ticks: circular, escape`;
      aimLabel.style.color = col;
      v3.set(ax * U, 0.1, az * U).project(camera);
      aimLabel.style.opacity = '1';
      aimLabel.style.transform = `translate(${((v3.x + 1) / 2 * stage.clientWidth).toFixed(1)}px, ${((1 - v3.y) / 2 * stage.clientHeight - 26).toFixed(1)}px) translate(-50%, -50%)`;
    } else aimLabel.style.opacity = '0';

    if (aiming || last >= 0) {
      const X = aiming ? ax : px[last]; const Z = aiming ? az : pz[last]; const VX = aiming ? avx : vx[last]; const VZ = aiming ? avz : vz[last];
      const r = Math.hypot(X, Z); const v = Math.hypot(VX, VZ); const E = 0.5 * v * v - GM1 * M / r; const a = -GM1 * M / (2 * E);
      st.v.set(`${fmt(v * KMS, 1)} km/s`); st.vc.set(`${fmt(Math.sqrt(GM1 * M / r) * KMS, 1)} km/s`);
      const f = aiming ? predFate : fate[last] || (E >= 0 ? 2 : 0);
      st.fate.set(f === 1 ? 'crash into the star' : f === 2 ? 'escapes' : 'stable orbit');
      st.T.set(E < 0 ? `${fmt(2 * Math.PI * Math.sqrt(a * a * a / (GM1 * M)), 2)} yr` : '—');
      badge.set(aiming ? (predFate === 1 ? 'Too slow: it will fall into the star' : predFate === 2 ? 'Too fast: it will escape' : 'Just right: a closed orbit') : 'Press on the plane and drag to aim, release to launch');
    }
  });
  engine.start();
  launch(1, 0, 0, -Math.sqrt(GM1));

  stage.__orbit = { launch, alive: () => Array.from(alive.slice(0, n)), fate: () => Array.from(fate.slice(0, n)), aim: (x, z, ux, uz) => { aiming = true; ax = x; az = z; avx = ux; avz = uz; predict(x, z, ux, uz); } };
  return {
    dispose() {
      drag.dispose(); controls.dispose(); panel.dispose(); hud.dispose(); aimLabel.remove();
      bodies.forEach((b) => b.trail.dispose()); pred.dispose(); aimArrow.dispose(); sun.dispose(); engine.dispose();
    },
  };
}
