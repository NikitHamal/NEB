/**
 * Kepler's laws in 3D. A planet on an ellipse with the Sun at one focus, moved by Kepler's equation
 * (M = E − e sin E, solved by Newton's method), so its speed is exactly what the second law demands.
 * Drag the aphelion marker to stretch the orbit (perihelion stays put) or drag the planet to scrub
 * time. Twelve sectors swept in equal times lie in the orbital plane: long and thin far out, short
 * and wide close in, all of equal area. The third-law card plots T against a for the real planets.
 */
import { THREE } from '../core/engine.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { createSpace, makeSun, makePlanet, makeArrow, planeDrag, canvasCard } from './space3d/kit.js';

const PLANETS = [['Mercury', 0.387, 0.206], ['Venus', 0.723, 0.007], ['Earth', 1, 0.017], ['Mars', 1.524, 0.093], ['Jupiter', 5.203, 0.048], ['Saturn', 9.537, 0.054]];
const SECT = 12;
const GM = 4 * Math.PI * Math.PI;
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

function label(stage, cls) {
  const el = document.createElement('div');
  el.style.cssText = 'position:absolute;left:0;top:0;pointer-events:none;font:600 11px Poppins,system-ui,sans-serif;color:#c7d2fe;white-space:nowrap;text-shadow:0 1px 3px #000;will-change:transform;z-index:2';
  if (cls) el.style.color = cls;
  stage.appendChild(el);
  return el;
}

export default function init(stage) {
  const S = createSpace(stage, { camera: [0.6, 4.2, 6.2], minDistance: 2, maxDistance: 40, maxPolar: 1.52 });
  if (!S) return null;
  const { engine, scene, camera, quality, controls } = S;
  const hud = createHud(stage);
  const badge = hud.badge('Drag the aphelion marker to stretch the orbit', '#60a5fa');

  let a = 1; let e = 0.5; let t = 0; let rate = 0.25; let showSectors = true; let scrub = false; let k = 2.4;
  const panel = createPanel(stage, { title: "Kepler's laws" });
  const eS = panel.slider({ label: 'Eccentricity e', min: 0, max: 0.9, step: 0.01, value: e, format: (v) => v.toFixed(2), onChange: (v) => { e = v; dirty = true; } });
  const aS = panel.slider({ label: 'Semi-major axis a', min: 0.4, max: 5.2, step: 0.01, value: a, format: (v) => `${v.toFixed(2)} AU`, onChange: (v) => { a = v; dirty = true; } });
  panel.chips({ label: 'Real orbits', options: PLANETS.map((p) => ({ value: p[0], label: p[0] })).concat([{ value: 'Halley', label: "Halley's comet" }]), value: '', onChange: (v) => { const p = PLANETS.find((q) => q[0] === v); if (p) { a = p[1]; e = p[2]; } else { a = 17.8; e = 0.967; } aS.set(Math.min(a, 5.2)); eS.set(Math.min(e, 0.9)); dirty = true; } });
  panel.toggle({ label: 'Equal-time sectors', value: true, onChange: (v) => { showSectors = v; } });
  panel.slider({ label: 'Animation speed', min: 0.05, max: 1, step: 0.05, value: rate, format: (v) => `${v.toFixed(2)} orbits/s`, onChange: (v) => { rate = v; } });
  const graph = canvasCard(panel.body, 1.45);
  const st = panel.stats([{ key: 'T', label: 'Period T = a^1.5' }, { key: 'r', label: 'Distance now' }, { key: 'v', label: 'Speed now' }, { key: 'pa', label: 'Perihelion / aphelion' }]);
  panel.info('1: orbits are ellipses with the Sun at one focus. 2: the line to the Sun sweeps equal areas in equal times, so the planet speeds up near the Sun. 3: T² ∝ a³ (T in years, a in AU, T² = a³ for anything orbiting the Sun).');

  function solveE(M) { let E = e < 0.8 ? M : Math.PI; for (let i = 0; i < 30; i++) { const f = E - e * Math.sin(E) - M; E -= f / (1 - e * Math.cos(E)); if (Math.abs(f) < 1e-12) break; } return E; }
  const P = [0, 0];
  function pos(M) { const E = solveE(M); P[0] = a * (Math.cos(E) - e); P[1] = a * Math.sqrt(1 - e * e) * Math.sin(E); return P; }

  const sun = makeSun(quality, 0.22);
  scene.add(sun.group);
  const planet = makePlanet('earth', 0.085);
  scene.add(planet);
  const atm = new THREE.Mesh(new THREE.SphereGeometry(1.08, 32, 16), new THREE.MeshBasicMaterial({ color: 0x6fa8ff, transparent: true, opacity: 0.18, blending: THREE.AdditiveBlending, depthWrite: false }));
  planet.add(atm);

  const orbitGeo = new THREE.BufferGeometry();
  const orbitPos = new Float32Array(257 * 3);
  orbitGeo.setAttribute('position', new THREE.BufferAttribute(orbitPos, 3));
  const orbit = new THREE.Line(orbitGeo, new THREE.LineBasicMaterial({ color: 0xc7d2fe, transparent: true, opacity: 0.75 }));
  scene.add(orbit);
  const axisGeo = new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3));
  const axis = new THREE.Line(axisGeo, new THREE.LineDashedMaterial({ color: 0xc7d2fe, transparent: true, opacity: 0.3, dashSize: 0.08, gapSize: 0.08 }));
  scene.add(axis);
  const sectorGeo = new THREE.BufferGeometry();
  const SEG = 16;
  const secPos = new Float32Array(SECT * SEG * 9); const secCol = new Float32Array(SECT * SEG * 9);
  sectorGeo.setAttribute('position', new THREE.BufferAttribute(secPos, 3));
  sectorGeo.setAttribute('color', new THREE.BufferAttribute(secCol, 3));
  const sectors = new THREE.Mesh(sectorGeo, new THREE.MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.22, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending }));
  scene.add(sectors);
  const sweep = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({ color: 0xffd27a, transparent: true, opacity: 0.32, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending }));
  const sweepPos = new Float32Array(SEG * 9);
  sweep.geometry.setAttribute('position', new THREE.BufferAttribute(sweepPos, 3));
  scene.add(sweep);
  const radius = new THREE.Line(new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3)), new THREE.LineBasicMaterial({ color: 0xffd27a, transparent: true, opacity: 0.7 }));
  scene.add(radius);
  const knobMat = new THREE.MeshBasicMaterial({ color: 0x60a5fa, toneMapped: false });
  const apoKnob = new THREE.Mesh(new THREE.SphereGeometry(0.05, 20, 12), knobMat);
  const apoRing = new THREE.Mesh(new THREE.RingGeometry(0.08, 0.1, 40), new THREE.MeshBasicMaterial({ color: 0x60a5fa, transparent: true, opacity: 0.6, side: THREE.DoubleSide, toneMapped: false }));
  apoRing.rotation.x = -Math.PI / 2; apoKnob.add(apoRing);
  scene.add(apoKnob);
  const focus2 = new THREE.Mesh(new THREE.RingGeometry(0.035, 0.05, 32), new THREE.MeshBasicMaterial({ color: 0xc7d2fe, transparent: true, opacity: 0.7, side: THREE.DoubleSide }));
  focus2.rotation.x = -Math.PI / 2;
  scene.add(focus2);
  const vel = makeArrow(0x34d399, 0.011);
  scene.add(vel.group);
  const grid = new THREE.PolarGridHelper(6, 12, 8, 96, 0x22304d, 0x18233a);
  grid.material.transparent = true; grid.material.opacity = 0.5; grid.material.depthWrite = false;
  scene.add(grid);

  const L = { peri: label(stage, '#fbbf24'), apo: label(stage, '#93c5fd'), f2: label(stage), sun: label(stage, '#ffd27a'), v: label(stage, '#a7f3d0'), sec: label(stage, '#c7d2fe') };
  L.sec.style.left = '50%'; L.sec.style.top = 'auto'; L.sec.style.bottom = '12px'; L.sec.style.transform = 'translateX(-50%)';
  L.peri.textContent = 'perihelion'; L.apo.textContent = 'aphelion · drag'; L.f2.textContent = 'empty focus'; L.sun.textContent = 'Sun (focus)';
  const v3 = new THREE.Vector3();
  function place(el, x, y, z, dx = 0, dy = -16, show = true) {
    v3.set(x, y, z).project(camera);
    const w = stage.clientWidth; const h = stage.clientHeight;
    const vis = show && v3.z < 1 && v3.x > -1.1 && v3.x < 1.1 && v3.y > -1.1 && v3.y < 1.1;
    el.style.opacity = vis ? '1' : '0';
    if (vis) el.style.transform = `translate(${((v3.x + 1) / 2 * w + dx).toFixed(1)}px, ${((1 - v3.y) / 2 * h + dy).toFixed(1)}px) translate(-50%, -50%)`;
  }

  let dirty = true;
  const hW = (x) => x * k;
  function rebuild() {
    dirty = false;
    const b = a * Math.sqrt(1 - e * e);
    for (let i = 0; i <= 256; i++) { const E = i / 256 * Math.PI * 2; orbitPos[i * 3] = hW(a * (Math.cos(E) - e)); orbitPos[i * 3 + 1] = 0; orbitPos[i * 3 + 2] = -hW(b * Math.sin(E)); }
    orbitGeo.attributes.position.needsUpdate = true; orbitGeo.computeBoundingSphere();
    const ap = axisGeo.attributes.position.array; ap.set([hW(-a * (1 + e)), 0, 0, hW(a * (1 - e)), 0, 0]); axisGeo.attributes.position.needsUpdate = true; axis.computeLineDistances();
    const ca = new THREE.Color(0x60a5fa); const cb = new THREE.Color(0xa78bfa);
    let o = 0;
    for (let s = 0; s < SECT; s++) {
      const c = s % 2 ? ca : cb;
      for (let j = 0; j < SEG; j++) {
        pos(2 * Math.PI * (s + j / SEG) / SECT); const x1 = P[0]; const y1 = P[1];
        pos(2 * Math.PI * (s + (j + 1) / SEG) / SECT); const x2 = P[0]; const y2 = P[1];
        secPos.set([0, 0, 0, hW(x1), 0, -hW(y1), hW(x2), 0, -hW(y2)], o);
        for (let q = 0; q < 3; q++) secCol.set([c.r, c.g, c.b], o + q * 3);
        o += 9;
      }
    }
    sectorGeo.attributes.position.needsUpdate = true; sectorGeo.attributes.color.needsUpdate = true; sectorGeo.computeBoundingSphere();
    apoKnob.position.set(hW(-a * (1 + e)), 0, 0);
    focus2.position.set(hW(-2 * a * e), 0, 0);
  }

  const drag = planeDrag(engine.canvas, camera, controls, {
    handles: () => [{ id: 'apo', pos: apoKnob.position }, { id: 'planet', pos: planet.position }],
    onDown: (h) => { if (h.id === 'planet') scrub = true; },
    onMove: (h, p) => {
      if (h.id === 'apo') {
        const ra = Math.min(12, Math.max(0.3, -p.x / k)); const rp = a * (1 - e);
        const na = (ra + rp) / 2; const ne = Math.min(0.9, Math.max(0, (ra - rp) / (ra + rp)));
        a = Math.min(5.2, Math.max(0.4, na)); e = ne; aS.set(a); eS.set(e); dirty = true;
      } else {
        const px = p.x / k + a * e; const py = -p.z / k / Math.sqrt(1 - e * e);
        const E = Math.atan2(py, px); let M = E - e * Math.sin(E); if (M < 0) M += 2 * Math.PI;
        t = Math.floor(t) + M / (2 * Math.PI);
      }
    },
    onUp: (h) => { if (h.id === 'planet') scrub = false; },
  });

  function drawGraph(Tyr) {
    const { g, w, h } = graph.ctx();
    const ix = 34; const iy = 26; const iw = w - 46; const ih = h - 48;
    const Lg = Math.log10;
    const lx = (v) => ix + (Lg(v) + 0.5) / 2.0 * iw; const ly = (v) => iy + ih - (Lg(v) + 1) / 4 * ih;
    g.font = '700 11px Poppins, system-ui, sans-serif'; g.fillStyle = '#e8eefb'; g.textAlign = 'left'; g.fillText("Kepler's third law: T² = a³", 10, 15);
    g.strokeStyle = 'rgba(160,190,255,0.18)'; g.strokeRect(ix, iy, iw, ih);
    g.strokeStyle = 'rgba(96,165,250,0.7)'; g.lineWidth = 1.5; g.beginPath(); g.moveTo(lx(0.3), ly(Math.pow(0.3, 1.5))); g.lineTo(lx(31), ly(Math.pow(31, 1.5))); g.stroke();
    g.font = '600 9px Poppins, system-ui, sans-serif';
    for (const p of PLANETS) { g.beginPath(); g.arc(lx(p[1]), ly(Math.pow(p[1], 1.5)), 3, 0, Math.PI * 2); g.fillStyle = '#e2e8f0'; g.fill(); g.fillStyle = '#aab8d3'; g.fillText(p[0], lx(p[1]) + 5, ly(Math.pow(p[1], 1.5)) + 3); }
    g.beginPath(); g.arc(lx(a), ly(Tyr), 5, 0, Math.PI * 2); g.fillStyle = '#34d399'; g.fill();
    g.fillStyle = '#8ea0c2'; g.textAlign = 'right'; g.fillText('log a (AU) →', ix + iw, iy + ih + 14); g.textAlign = 'left'; g.fillText('log T (yr)', ix + 5, iy + 12);
  }

  let gKey = '';
  const vv = new THREE.Vector3(); const pp = new THREE.Vector3();
  engine.setUpdate((dt, time) => {
    const kGoal = 2.6 / (a * (1 + e) * 0.62 + 0.38);
    if (Math.abs(kGoal - k) > 1e-4) { k += (kGoal - k) * (1 - Math.exp(-dt * 4)); dirty = true; }
    if (dirty) rebuild();
    controls.update(dt);
    sun.uniforms.uTime.value = time;
    const Tyr = Math.pow(a, 1.5);
    if (!scrub) t += dt * rate;
    const M = 2 * Math.PI * (t % 1);
    pos(M);
    const r = Math.hypot(P[0], P[1]); const v = Math.sqrt(GM * (2 / r - 1 / a));
    planet.position.set(hW(P[0]), 0, -hW(P[1]));
    planet.rotation.y += dt * 2;
    const ra = radius.geometry.attributes.position.array; ra[3] = planet.position.x; ra[5] = planet.position.z; radius.geometry.attributes.position.needsUpdate = true;
    const E = solveE(M); vv.set(-a * Math.sin(E), 0, -a * Math.sqrt(1 - e * e) * Math.cos(E)).normalize().multiplyScalar(v * 0.045);
    vel.set(pp.copy(planet.position), vv);
    sectors.visible = showSectors;
    const s0 = Math.floor((t % 1) * SECT); const fs = ((t % 1) * SECT) - s0;
    for (let j = 0; j < SEG; j++) {
      pos(2 * Math.PI * (s0 + fs * j / SEG) / SECT); const x1 = P[0]; const y1 = P[1];
      pos(2 * Math.PI * (s0 + fs * (j + 1) / SEG) / SECT);
      sweepPos.set([0, 0.002, 0, hW(x1), 0.002, -hW(y1), hW(P[0]), 0.002, -hW(P[1])], j * 9);
    }
    sweep.geometry.attributes.position.needsUpdate = true; sweep.geometry.computeBoundingSphere();
    sweep.visible = showSectors;
    apoRing.scale.setScalar(1 + 0.15 * Math.sin(time * 3));

    place(L.peri, hW(a * (1 - e)), 0, 0, 0, 16);
    place(L.apo, hW(-a * (1 + e)), 0, 0, 0, -18);
    place(L.f2, hW(-2 * a * e), 0, 0, 0, 16, e > 0.05);
    place(L.sun, 0, 0.35, 0, 0, -10);
    L.v.textContent = `${fmt(v * 4.7406, 1)} km/s`;
    place(L.v, planet.position.x, 0.2, planet.position.z, 0, -14);
    L.sec.textContent = showSectors ? `each sector: ${fmt(Tyr / SECT * 365.25, 0)} days · ${fmt(Math.PI * a * a * Math.sqrt(1 - e * e) / SECT, 3)} AU²` : '';

    const key = `${a.toFixed(3)}`;
    if (key !== gKey) { gKey = key; drawGraph(Tyr); }
    st.T.set(`${fmt(Tyr, 2)} yr`); st.r.set(`${fmt(r, 2)} AU`); st.v.set(`${fmt(v * 4.7406, 1)} km/s`); st.pa.set(`${fmt(a * (1 - e), 2)} / ${fmt(a * (1 + e), 2)} AU`);
    badge.set(e < 0.02 ? 'A circle is an ellipse with e = 0: constant speed' : `Fastest at perihelion: ${fmt(Math.sqrt(GM * (2 / (a * (1 - e)) - 1 / a)) * 4.74, 1)} km/s · slowest at aphelion: ${fmt(Math.sqrt(GM * (2 / (a * (1 + e)) - 1 / a)) * 4.74, 1)} km/s`);
  });
  engine.start();

  stage.__kepler = { state: () => [a, e], set: (na, ne) => { a = na; e = ne; dirty = true; }, apo: () => apoKnob.position.clone() };
  return {
    dispose() {
      drag.dispose(); controls.dispose(); panel.dispose(); hud.dispose(); Object.values(L).forEach((el) => el.remove());
      sun.dispose(); vel.dispose(); engine.dispose();
    },
  };
}
