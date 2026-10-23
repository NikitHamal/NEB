/**
 * Waves and sound in 3D — a real 8 m rope on the school field, from a hand-held grip to a post. In
 * "Shake it" the rope is solved with the wave equation (finite differences, y_tt = v²y_xx): grab the
 * grip and shake, or switch on the oscillator, and choose what the far end does (tied to the post:
 * pulses come back upside down; a loose ring on a rod: upright; endless: no echo). "Standing waves"
 * shows harmonic n with its nodes and antinodes, f = nv/2L; "Interference" adds two waves with a phase
 * difference. One red bead shows the rope only moves up and down while the wave travels along.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { canvasCard } from '../space/space3d/kit.js';
import { createField, label, THREE } from './physics3d/field.js';

const LEN = 8; const N = 200; const DX = LEN / N; const Y0 = 1.1;
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

export default function init(stage) {
  const F = createField(stage, { camera: [4, 1.6, 7.5], target: [4, 1.1, 0], maxDistance: 30 });
  if (!F) return null;
  const { engine, scene, camera, controls } = F;
  { const c = F.key.shadow.camera; c.left = -8; c.right = 12; c.top = 8; c.bottom = -8; c.updateProjectionMatrix(); }
  const hud = createHud(stage);
  const badge = hud.badge('Grab the grip and shake the rope', '#2563eb');

  let mode = 'shake'; let end = 'open'; let osc = true; let f = 1; let A = 0.3; let v = 4; let harmonic = 3; let phase = 0; let f2 = 1; let paused = false; let sound = false;
  let y = new Float64Array(N + 1); let yp = new Float64Array(N + 1); let yn = new Float64Array(N + 1);
  let t = 0; let handY = 0; let handHeld = false; let handSpring = 0; let handVel = 0; let simT = 0;
  const trace = [];

  // the rope: a tube displaced in the vertex shader from a 1-D texture of the solution
  const half = new Uint16Array((N + 1) * 4);
  const yTex = new THREE.DataTexture(half, N + 1, 1, THREE.RGBAFormat, THREE.HalfFloatType);
  yTex.magFilter = yTex.minFilter = THREE.LinearFilter; yTex.needsUpdate = true;
  const ropeGeo = new THREE.CylinderGeometry(0.022, 0.022, LEN, 10, N * 2, true); ropeGeo.rotateZ(-Math.PI / 2); ropeGeo.translate(LEN / 2, 0, 0);
  const ropeMat = new THREE.MeshStandardMaterial({ color: 0x2563eb, roughness: 0.7 });
  ropeMat.onBeforeCompile = (sh) => {
    sh.uniforms.uY = { value: yTex };
    sh.vertexShader = `uniform sampler2D uY;\n${sh.vertexShader}`.replace('#include <begin_vertex>', `#include <begin_vertex>
      float uu = clamp(position.x / ${LEN.toFixed(1)}, 0.0, 1.0) * ${(N / (N + 1)).toFixed(5)} + ${(0.5 / (N + 1)).toFixed(5)};
      transformed.y += texture2D(uY, vec2(uu, 0.5)).r;`);
  };
  ropeMat.customProgramCacheKey = () => 'rope-wave';
  const rope = new THREE.Mesh(ropeGeo, ropeMat); rope.position.y = Y0; rope.castShadow = true; rope.frustumCulled = false; scene.add(rope);
  const bead = new THREE.Mesh(new THREE.SphereGeometry(0.06, 20, 14), new THREE.MeshStandardMaterial({ color: 0xdc2626, roughness: 0.3 })); bead.castShadow = true; scene.add(bead);
  const steel = new THREE.MeshStandardMaterial({ color: 0x9aa3ad, metalness: 0.85, roughness: 0.3 });
  const grip = new THREE.Group();
  const gripBar = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.22, 16), new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.6 })); gripBar.rotation.x = Math.PI / 2;
  const glove = new THREE.Mesh(new THREE.SphereGeometry(0.08, 20, 14), new THREE.MeshStandardMaterial({ color: 0xc58c6a, roughness: 0.7 })); glove.scale.set(1.1, 0.9, 1.3); glove.position.x = -0.05;
  grip.add(gripBar, glove); scene.add(grip);
  const guide = new THREE.Mesh(new THREE.BoxGeometry(0.04, 1.6, 0.04), new THREE.MeshStandardMaterial({ color: 0x334155, transparent: true, opacity: 0.35 })); guide.position.set(-0.1, Y0, 0.12); scene.add(guide);
  const post = new THREE.Mesh(new THREE.BoxGeometry(0.18, 2.4, 0.18), new THREE.MeshStandardMaterial({ color: 0x7a5228, roughness: 0.8 })); post.position.set(LEN + 0.1, 1.2, 0); post.castShadow = true; scene.add(post);
  const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 1.8, 10), steel); rod.position.set(LEN, Y0, 0); scene.add(rod);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.05, 0.012, 8, 20), steel); ring.rotation.x = Math.PI / 2; scene.add(ring);
  const sink = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 6, 8, 1, true), new THREE.MeshBasicMaterial({ color: 0x2563eb, transparent: true, opacity: 0.25 })); sink.rotation.z = Math.PI / 2; sink.position.set(LEN + 3, Y0, 0); scene.add(sink);
  const nodeMat = new THREE.MeshBasicMaterial({ color: 0xffffff }); const nodes = [];
  for (let i = 0; i < 7; i++) { const m = new THREE.Mesh(new THREE.RingGeometry(0.06, 0.08, 24), nodeMat); m.visible = false; scene.add(m); nodes.push(m); }
  for (let m = 0; m <= LEN; m++) { const tk = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.002, m % 2 ? 0.25 : 0.5), new THREE.MeshBasicMaterial({ color: 0xffffff })); tk.position.set(m, 0.003, 0.9); scene.add(tk); }
  const lamLbl = label(stage, camera);

  const panel = createPanel(stage, { title: 'Waves' });
  panel.chips({ label: 'Experiment', options: [{ value: 'shake', label: 'Shake it' }, { value: 'standing', label: 'Standing waves' }, { value: 'interference', label: 'Interference' }], value: 'shake', onChange: (m) => { mode = m; resetString(); show(); } });
  const endC = panel.chips({ label: 'Far end', options: [{ value: 'fixed', label: 'Tied to the post' }, { value: 'free', label: 'Loose ring' }, { value: 'open', label: 'Endless' }], value: 'open', onChange: (e) => { end = e; resetString(); } });
  const oscT = panel.toggle({ label: 'Oscillator drives the grip', value: true, onChange: (o) => { osc = o; } });
  const fS = panel.slider({ label: 'Frequency f', min: 0.25, max: 3, step: 0.05, value: f, format: (x) => `${x.toFixed(2)} Hz`, onChange: (x) => { f = x; } });
  panel.slider({ label: 'Amplitude A', min: 0.05, max: 0.6, step: 0.05, value: A, format: (x) => `${x.toFixed(2)} m`, onChange: (x) => { A = x; } });
  panel.slider({ label: 'Wave speed v', min: 1, max: 8, step: 0.5, value: v, format: (x) => `${x.toFixed(1)} m/s`, onChange: (x) => { v = x; } });
  const hS = panel.slider({ label: 'Harmonic n', min: 1, max: 6, step: 1, value: harmonic, format: (x) => `n = ${x}`, onChange: (x) => { harmonic = x; } });
  const pS = panel.slider({ label: 'Phase difference', min: 0, max: 360, step: 15, value: 0, format: (x) => `${x}°`, onChange: (x) => { phase = x * Math.PI / 180; } });
  const f2S = panel.slider({ label: 'Wave 2 frequency', min: 0.25, max: 3, step: 0.05, value: 1, format: (x) => `${x.toFixed(2)} Hz`, onChange: (x) => { f2 = x; } });
  panel.toggle({ label: 'Hear the pitch (f × 200)', value: false, onChange: (s) => { sound = s; syncSound(); } });
  panel.buttonRow([{ label: 'Pause', icon: 'pause', variant: 'ghost', onClick: () => { paused = !paused; syncSound(); } }, { label: 'Calm the rope', icon: 'waves', variant: 'ghost', onClick: resetString }]);
  const graph = canvasCard(panel.body, 2.2);
  const st = panel.stats([{ key: 'f', label: 'Frequency f' }, { key: 'lam', label: 'Wavelength λ = v/f' }, { key: 'T', label: 'Period T = 1/f' }, { key: 'v', label: 'Speed v = fλ' }]);
  panel.info('Every bit of the rope only moves up and down; the shape is what travels. Double f and λ halves, because v = fλ stays fixed by the rope.');

  function show() {
    endC.el.style.display = mode === 'shake' ? '' : 'none'; oscT.el.style.display = mode === 'shake' ? '' : 'none';
    hS.el.style.display = mode === 'standing' ? '' : 'none'; pS.el.style.display = f2S.el.style.display = mode === 'interference' ? '' : 'none';
    fS.el.style.display = mode === 'standing' ? 'none' : '';
  }
  show();
  function resetString() { y.fill(0); yp.fill(0); yn.fill(0); handY = 0; handSpring = 0; handVel = 0; trace.length = 0; simT = 0; }
  function stepString(dt) {
    const hmax = 0.7 * DX / v; const n = Math.max(1, Math.ceil(dt / hmax)); const h = dt / n;
    const r2 = (v * h / DX) ** 2; const damp = 0.15 * h;
    for (let s = 0; s < n; s++) {
      t += h;
      const drive = handHeld ? handY : osc ? A * Math.sin(2 * Math.PI * f * t) : handSpring;
      for (let i = 1; i < N; i++) yn[i] = 2 * y[i] - yp[i] + r2 * (y[i + 1] - 2 * y[i] + y[i - 1]) - damp * (y[i] - yp[i]);
      yn[0] = drive;
      if (end === 'fixed') yn[N] = 0; else if (end === 'free') yn[N] = yn[N - 1]; else { const c = v * h; yn[N] = y[N - 1] + (c - DX) / (c + DX) * (yn[N - 1] - y[N]); }
      const tmp = yp; yp = y; y = yn; yn = tmp;
    }
  }
  function comp(xm, tt, which) {
    if (mode === 'standing') { const kn = harmonic * Math.PI / LEN; const om = 2 * Math.PI * harmonic * v / (2 * LEN); return which ? -A * 0.6 * Math.sin(om * tt + kn * xm) : A * 0.6 * Math.sin(om * tt - kn * xm); }
    if (which === 0) return A * 0.6 * Math.sin(2 * Math.PI * f * tt - 2 * Math.PI * f / v * xm);
    return A * 0.6 * Math.sin(2 * Math.PI * f2 * tt - 2 * Math.PI * f2 / v * xm + phase);
  }
  const yAt = (i) => (mode === 'shake' ? y[i] : comp(i * DX, t, 0) + comp(i * DX, t, 1));

  let audio = null;
  function syncSound() {
    const want = sound && !paused && !document.hidden;
    if (want && !audio) {
      try { const ac = new (window.AudioContext || window.webkitAudioContext)(); const o = ac.createOscillator(); const g = ac.createGain(); o.type = 'sine'; g.gain.value = 0.0001; o.connect(g); g.connect(ac.destination); o.start(); g.gain.setTargetAtTime(0.05, ac.currentTime, 0.05); audio = { ac, o, g }; } catch (e) { audio = null; }
    } else if (!want && audio) { const a = audio; audio = null; a.g.gain.setTargetAtTime(0, a.ac.currentTime, 0.04); setTimeout(() => a.ac.close(), 200); }
  }
  document.addEventListener('visibilitychange', syncSound);

  // grab the grip: drag it up and down in the rope's plane
  const ray = new THREE.Raycaster(); const ndc = new THREE.Vector2(); const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0); const hit = new THREE.Vector3();
  const toPlane = (e) => { const r = engine.canvas.getBoundingClientRect(); ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(ndc, camera); return ray.ray.intersectPlane(plane, hit); };
  engine.canvas.addEventListener('pointerdown', (e) => {
    if (mode !== 'shake') return;
    const r = engine.canvas.getBoundingClientRect(); ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(ndc, camera);
    if (!ray.intersectObject(grip, true).length && !ray.intersectObject(guide).length) return;
    handHeld = true; osc = false; oscT.set(false); controls.enabled = false; e.stopImmediatePropagation();
  }, true);
  engine.canvas.addEventListener('pointermove', (e) => { if (handHeld && toPlane(e)) handY = Math.max(-0.7, Math.min(0.7, hit.y - Y0)); });
  const up = () => { if (handHeld) { handHeld = false; handSpring = handY; handVel = 0; controls.enabled = true; } };
  engine.canvas.addEventListener('pointerup', up); engine.canvas.addEventListener('pointercancel', up);

  function drawGraph() {
    const { g, w, h } = graph.ctx();
    const ix = 32; const iy = 20; const iw = w - 42; const ih = h - 38;
    const t1 = Math.max(8, simT); const t0 = t1 - 8;
    const X = (tt) => ix + (tt - t0) / 8 * iw; const Y = (vv) => iy + ih / 2 - vv / 0.8 * ih / 2;
    g.font = '700 11px Poppins, system-ui, sans-serif'; g.fillStyle = '#e8eefb'; g.textAlign = 'left'; g.fillText('Red bead: displacement against time', 10, 13);
    g.strokeStyle = 'rgba(160,190,255,0.18)'; g.strokeRect(ix, iy, iw, ih); g.beginPath(); g.moveTo(ix, Y(0)); g.lineTo(ix + iw, Y(0)); g.stroke();
    g.strokeStyle = '#ef4444'; g.lineWidth = 2; g.beginPath(); let first = true;
    for (const [tt, vv] of trace) { if (tt < t0) continue; if (first) { g.moveTo(X(tt), Y(vv)); first = false; } else g.lineTo(X(tt), Y(vv)); }
    g.stroke();
  }

  const v3 = new THREE.Vector3(); let tick = 0;
  engine.setUpdate((dt) => {
    controls.update(dt);
    if (!paused) {
      if (mode === 'shake') { if (!handHeld && !osc) { handVel += (-handSpring * 60 - handVel * 9) * dt; handSpring += handVel * dt; } stepString(dt); } else t += dt;
      simT += dt; trace.push([simT, yAt(Math.round(2 / DX))]); if (trace.length > 800) trace.shift();
    }
    for (let i = 0; i <= N; i++) half[i * 4] = THREE.DataUtils.toHalfFloat(yAt(i));
    yTex.needsUpdate = true;
    const hy = yAt(0);
    grip.position.set(-0.06, Y0 + hy, 0);
    bead.position.set(2, Y0 + yAt(Math.round(2 / DX)), 0);
    const yN = yAt(N);
    rod.visible = ring.visible = mode === 'shake' && end === 'free'; ring.position.set(LEN, Y0 + yN, 0);
    post.visible = !(mode === 'shake' && end === 'open'); sink.visible = mode === 'shake' && end === 'open';
    const fNow = mode === 'standing' ? harmonic * v / (2 * LEN) : f;
    if (audio) audio.o.frequency.setTargetAtTime(fNow * 200, audio.ac.currentTime, 0.03);
    nodes.forEach((m, i) => { m.visible = mode === 'standing' && i <= harmonic; m.position.set(i * LEN / harmonic, Y0, 0.03); });
    const lam = v / fNow;
    lamLbl.el.textContent = `λ = ${fmt(lam, 2)} m`; lamLbl.at(v3.set(Math.min(LEN - 0.5, lam / 2), Y0 + 0.75, 0));
    if ((tick++ & 3) === 0) drawGraph();
    st.f.set(`${fmt(fNow, 2)} Hz`); st.lam.set(`${fmt(lam, 2)} m`); st.T.set(`${fmt(1 / fNow, 2)} s`); st.v.set(`${fmt(v, 1)} m/s`);
    badge.set(mode === 'standing' ? `Harmonic ${harmonic}: ${harmonic + 1} nodes, f = nv/2L = ${fmt(fNow, 2)} Hz` : mode === 'interference' ? (Math.abs(f - f2) < 0.01 ? `Phase ${Math.round(phase * 180 / Math.PI)}°: ${Math.abs(Math.cos(phase / 2)) > 0.9 ? 'they add up' : Math.abs(Math.cos(phase / 2)) < 0.1 ? 'they cancel' : 'partly add'}` : 'Different frequencies: beats') : end === 'fixed' ? 'Tied end: pulses come back upside down' : end === 'free' ? 'Loose ring: pulses come back the same way up' : 'Endless rope: the wave runs off and never returns');
  });
  engine.start();

  stage.__waves = { mode: (m) => { mode = m; resetString(); show(); }, end: (e) => { end = e; resetString(); } };
  return { dispose() { document.removeEventListener('visibilitychange', syncSound); if (audio) { audio.ac.close(); audio = null; } panel.dispose(); hud.dispose(); lamLbl.remove(); yTex.dispose(); controls.dispose(); engine.dispose(); } };
}
