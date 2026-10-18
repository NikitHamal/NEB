// The simple pendulum. A brass bob on a thread through a split cork, clamped beyond the bench
// edge. The student pulls the thread to set the length, pulls the bob aside and lets go, and times
// 20 oscillations with a stopwatch on their own reflexes. The motion is the full nonlinear
// equation θ'' = -(g/L) sin θ - γθ', integrated with RK4, so a wide swing really is slower
// (T ≈ T0(1 + θ0²/16)). Several lengths give an L-T² graph whose slope gives g = 4π² L/T².
import { THREE } from '../../engine.js';
import { MAT, mesh, clamp, canvasTexture } from '../../bio-handson/kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, screenDist } from '../hud.js';
import { createStopwatch, createGraph, fitLine } from '../stopwatch.js';

const BY = 0.8;
const G = 9.787;
const PIVOT = new THREE.Vector3(0, 6.1, 3.75);
const BOB_R = 0.1;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

function scaleTex() {
  return canvasTexture('ho-metre-v', 128, 4096, (g, w, h) => {
    g.fillStyle = '#f4e3b5'; g.fillRect(0, 0, w, h);
    g.fillStyle = '#1f2937'; g.strokeStyle = '#1f2937';
    for (let mm = 0; mm <= 1000; mm += 2) {
      const y = 20 + (h - 40) * mm / 1000; const cm = mm % 10 === 0; const five = mm % 50 === 0;
      g.lineWidth = cm ? 2 : 1; g.beginPath(); g.moveTo(0, y); g.lineTo(five ? 54 : cm ? 38 : 22, y); g.stroke();
      if (cm && (mm / 10) % 5 === 0) { g.font = '700 26px system-ui, sans-serif'; g.textBaseline = 'middle'; g.fillText(String(mm / 10), 60, y); }
    }
  });
}

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const watch = createStopwatch(hud, { onStart, onStop });
  const graph = createGraph(hud, { title: 'L against T²', xLabel: 'T² (s²)', yLabel: 'L (cm)' });

  // ---- apparatus ----
  const stand = new THREE.Group(); world.add(stand);
  stand.add(mesh(new THREE.BoxGeometry(1.6, 0.1, 1.0), MAT.matte(0x2b3138), [0, 0.05, 2.5]));
  stand.add(mesh(new THREE.CylinderGeometry(0.05, 0.05, 6.6, 16), MAT.steel(), [0, 3.4, 2.3]));
  stand.add(mesh(new THREE.BoxGeometry(0.15, 0.15, 0.15), MAT.matte(0x30363d), [0, PIVOT.y, 2.3]));
  const arm = mesh(new THREE.CylinderGeometry(0.025, 0.025, 1.5, 10), MAT.steel(), [0, PIVOT.y, 3.05]); arm.rotation.x = Math.PI / 2; stand.add(arm);
  const corkMat = new THREE.MeshStandardMaterial({ color: 0xb98b5a, roughness: 0.9 });
  [-1, 1].forEach((s) => stand.add(mesh(new THREE.CylinderGeometry(0.07, 0.055, 0.22, 14, 1, false, s > 0 ? 0 : Math.PI, Math.PI), corkMat, [0, PIVOT.y - 0.05, PIVOT.z])));
  stand.add(mesh(new THREE.BoxGeometry(0.06, 0.1, 0.22), MAT.steel(), [0, PIVOT.y + 0.05, PIVOT.z - 0.12]));
  const rule = mesh(new THREE.BoxGeometry(0.16, 10.2, 0.03), new THREE.MeshStandardMaterial({ map: scaleTex(), roughness: 0.6 }), [-0.3, PIVOT.y - 0.1 - 5.0, PIVOT.z - 0.12]);
  world.add(rule);
  const bobMat = new THREE.MeshStandardMaterial({ color: 0xd4a94a, metalness: 1, roughness: 0.22 });
  const bob = new THREE.Group(); world.add(bob);
  bob.add(mesh(new THREE.SphereGeometry(BOB_R, 32, 20), bobMat));
  bob.add(mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.04, 8), MAT.steel(), [0, BOB_R + 0.01, 0]));
  const thread = mesh(new THREE.CylinderGeometry(0.004, 0.004, 1, 6), MAT.matte(0xf5f5f4), null); world.add(thread);
  const fid = mesh(new THREE.BoxGeometry(0.008, 0.6, 0.008), MAT.matte(0x111827), [0, 0, PIVOT.z - 0.25]); world.add(fid);
  const card = mesh(new THREE.BoxGeometry(0.9, 0.6, 0.01), MAT.matte(0xfafaf9), [0, 0, PIVOT.z - 0.26]); world.add(card);

  // ---- physics ----
  const p = { L: 0.65, th: 0, w: 0, held: true, swinging: false, phase: 0, prevPhase: 0, gamma: 0.0035, amp: 0, t0: 0, count0: 0 };
  const lenCm = () => Math.round(p.L * 1000) / 10;
  const thread0 = () => p.L * 10 - BOB_R;
  function deriv(th, w) { return -(G / p.L) * Math.sin(th) - p.gamma * w; }
  function integrate(dt) {
    const n = Math.max(1, Math.ceil(dt / 0.002)); const h = dt / n;
    for (let i = 0; i < n; i++) {
      const k1t = p.w, k1w = deriv(p.th, p.w);
      const k2t = p.w + 0.5 * h * k1w, k2w = deriv(p.th + 0.5 * h * k1t, p.w + 0.5 * h * k1w);
      const k3t = p.w + 0.5 * h * k2w, k3w = deriv(p.th + 0.5 * h * k2t, p.w + 0.5 * h * k2w);
      const k4t = p.w + h * k3w, k4w = deriv(p.th + h * k3t, p.w + h * k3w);
      p.th += h / 6 * (k1t + 2 * k2t + 2 * k3t + k4t); p.w += h / 6 * (k1w + 2 * k2w + 2 * k3w + k4w);
    }
    const w0 = Math.sqrt(G / p.L);
    let ph = Math.atan2(-p.w / w0, p.th); let d = ph - p.prevPhase; if (d < -Math.PI) d += Math.PI * 2; if (d > Math.PI) d -= Math.PI * 2;
    p.phase += d; p.prevPhase = ph; p.amp = Math.max(Math.abs(p.th), Math.hypot(p.th, p.w / w0) * 0.98);
  }
  const bobPos = new THREE.Vector3(); const up = new THREE.Vector3(0, 1, 0); const dir = new THREE.Vector3();
  function pose() {
    const r = p.L * 10;
    bobPos.set(PIVOT.x + Math.sin(p.th) * r, PIVOT.y - Math.cos(p.th) * r, PIVOT.z);
    bob.position.copy(bobPos); bob.rotation.z = p.th;
    dir.copy(bobPos).sub(PIVOT); const len = dir.length() - BOB_R;
    thread.scale.y = len; thread.position.copy(PIVOT).addScaledVector(dir.normalize(), len / 2);
    thread.quaternion.setFromUnitVectors(up, dir);
    fid.position.y = card.position.y = PIVOT.y - r - 0.05;
  }
  function onStart() { if (!p.swinging) return; p.count0 = p.phase / (Math.PI * 2); p.t0 = performance.now(); sfx.play('click'); }
  function onStop(t) {
    if (!p.swinging) return;
    sfx.play('click');
    const n = Math.abs(p.phase / (Math.PI * 2) - p.count0);
    const s = ctx.step; if (s && s.onTimed) s.onTimed(t, n);
  }

  const trials = [];
  const SHOT_ALL = shot({ pos: [4.2, PIVOT.y - 1.2, 16], target: [0, PIVOT.y - 4.2, 3.4], fitH: 10.8 });
  const SHOT_TOP = shot({ pos: [1.6, PIVOT.y - 0.3, 6.6], target: [0, PIVOT.y - 1.6, 3.6], fov: 34 });
  const SHOT_SWING = (L) => shot({ pos: [1.2, PIVOT.y - L * 4, PIVOT.z + 4 + L * 9], target: [0, PIVOT.y - L * 5 - 0.2, PIVOT.z], fitH: L * 10 + 1.6 });

  const steps = [];
  const IDX = {};
  IDX.len = steps.length;
  steps.push({
    title: 'Set the length', text: 'Drag the <b>bob</b> up or down to slide the thread through the split cork. Choose a length between <b>40 and 100 cm</b> (different from your earlier trials), then press <b>Length set</b>.', hint: 'Effective length L = thread length from the cork + radius of the bob, read on the metre rule.', shot: SHOT_ALL,
    enter() {
      p.held = true; p.swinging = false; p.th = 0; p.w = 0; pose();
      hud.actions([{ id: 'set', label: 'Length set', primary: true, onClick: () => {
        if (p.L < 0.395 || p.L > 1.005) { ctx.say('Between 40 and 100 cm.', 'hint', 1800); return; }
        if (trials.some((t) => Math.abs(t.L - lenCm()) < 8)) { ctx.say('Pick a length at least 8 cm away from your earlier trials so the graph spreads out.', 'hint', 2600); return; }
        hud.actions([]);
        if (!trials.length) {
          const l = thread0() * 10; const r = BOB_R * 10;
          ui.choose(ctx.stage.clientWidth / 2, 60, `Thread from cork to the top of the bob: ${l.toFixed(1)} cm. Bob diameter (vernier): ${(2 * r).toFixed(2)} cm. Effective length?`, [
            { label: `${(l + r).toFixed(1)} cm  (thread + radius)`, value: 1 }, { label: `${l.toFixed(1)} cm  (thread only)`, value: 0 }, { label: `${(l + 2 * r).toFixed(1)} cm  (thread + diameter)`, value: 2 },
          ].sort(() => Math.random() - 0.5), (v) => { if (v !== 1) ctx.mistake('L is measured to the centre of mass of the bob: thread + radius.', 3); ctx.next(`L = ${lenCm().toFixed(1)} cm.`); });
        } else ctx.next(`L = ${lenCm().toFixed(1)} cm.`);
      } }]);
    },
    exit() { hud.actions([]); ui.clearChooser(); },
    skip() { p.L = [0.5, 0.65, 0.8, 0.95][trials.length % 4]; pose(); },
    update() { hud.update(); },
    handler: {
      down(pt) { if (screenDist(ctx, bob, pt) > (pt.touch ? 70 : 50)) return false; this.drag = { y: pt.y, L: p.L }; return true; },
      move(pt) {
        if (!this.drag) return;
        const pxPerUnit = ctx.stage.clientHeight / 13;
        p.L = clamp(Math.round((this.drag.L + (pt.y - this.drag.y) / pxPerUnit / 10) * 200) / 200, 0.3, 1.05); pose();
        lenChip.set(`L = <b>${lenCm().toFixed(1)}</b> cm`); sfx.play('knob');
      },
      up() { this.drag = null; },
    },
  });
  const lenChip = hud.chip('ho-chip-read'); lenChip.dx = 18; lenChip.dy = -10;

  steps.push({
    title: 'Pull the bob aside and let go', text: 'Drag the bob <b>sideways</b> to a small angle — <b>under 10°</b> — and release it. It must swing in a plane, not in a circle.', hint: 'A small angle keeps sin θ ≈ θ, which the formula T = 2π√(L/g) assumes.', shot: null,
    enter() { ctx.rig.go(SHOT_SWING(p.L), 1.3); p.held = true; lenChip.show(false); },
    skip() { p.th = 0.1; p.w = 0; p.held = false; p.swinging = true; },
    handler: {
      down(pt) { if (screenDist(ctx, bob, pt) > (pt.touch ? 80 : 60)) return false; this.drag = true; p.held = true; p.swinging = false; return true; },
      move(pt) {
        if (!this.drag) return;
        const pl = new THREE.Plane(new THREE.Vector3(0, 0, 1), -(PIVOT.z + ctx.world.position.z)); const h = new THREE.Vector3();
        if (!ctx.input.ptr.ray.intersectPlane(pl, h)) return; ctx.world.worldToLocal(h);
        p.th = clamp(Math.atan2(h.x - PIVOT.x, PIVOT.y - h.y), -0.7, 0.7); p.w = 0; pose();
        angChip.set(`<b>${(Math.abs(p.th) * 180 / Math.PI).toFixed(0)}°</b>`); angChip.show(true);
      },
      up() {
        if (!this.drag) return; this.drag = false; angChip.show(false);
        if (Math.abs(p.th) < 0.03) { ctx.say('Pull it a little further aside.', 'hint', 1600); return; }
        p.held = false; p.swinging = true; p.prevPhase = Math.atan2(0, p.th); p.phase = 0;
        const deg = Math.abs(p.th) * 180 / Math.PI;
        if (deg > 10.5) ctx.mistake(`${deg.toFixed(0)}° is too wide: the period grows with amplitude (by about ${((deg * Math.PI / 180) ** 2 / 16 * 100).toFixed(1)} % here), so g will come out low.`, 3);
        ctx.next('Swinging. Let a few swings settle before you time.', 0.6);
      },
    },
  });
  const angChip = hud.chip('ho-chip-read'); angChip.at.copy(PIVOT); angChip.at.y += BY; angChip.dx = 16;

  steps.push({
    title: 'Time 20 oscillations', text: 'Start the stopwatch as the bob passes the <b>black mark</b> (the mean position), count 20 full oscillations — back to the mark moving the same way — and stop. <b>Space</b> works too.', hint: 'Start and stop as the bob crosses the mark, where it moves fastest and the timing is sharpest.', shot: null,
    enter() { watch.reset(); watch.show(true); },
    exit() { watch.show(false); },
    skip() { const T = 2 * Math.PI * Math.sqrt(p.L / G) * (1 + 0.1 * 0.1 / 16); this.onTimed(T * 20 + (Math.random() - 0.5) * 0.2, 20); },
    update() {
      if (watch.running) { const n = Math.abs(p.phase / (Math.PI * 2) - p.count0); watch.sub(`counting… <b>${Math.floor(n + 0.02)}</b>`); } else watch.sub('');
    },
    onTimed(t, n) {
      if (Math.abs(n - 20) > 0.25) { ctx.mistake(`You stopped after ${n.toFixed(2)} oscillations, not 20. One oscillation is a full swing there and back.`, 3); watch.reset(); return; }
      const T = t / 20; const L = lenCm();
      trials.push({ L, t, T });
      ui.observe(`L = ${L.toFixed(1)} cm`, `t₂₀ = ${t.toFixed(2)} s · T = ${T.toFixed(3)} s · T² = ${(T * T).toFixed(3)} s²`);
      ctx.next(`T = ${t.toFixed(2)} / 20 = ${T.toFixed(3)} s.`);
    },
  });

  steps.push({
    title: 'More lengths', text: 'Repeat for at least <b>four different lengths</b>, then plot the graph.', hideBelt: true, shot: null,
    enter() {
      const b = [{ id: 'again', label: 'Another length', primary: trials.length < 4, onClick: () => { hud.actions([]); p.swinging = false; p.held = true; anim.add(1.0, (k) => { p.th *= 1 - k; pose(); }); ctx.goTo(IDX.len); } }];
      if (trials.length >= 3) b.push({ id: 'plot', label: 'Plot the graph', primary: trials.length >= 4, onClick: () => { hud.actions([]); ctx.next(); } });
      hud.actions(b);
    },
    exit() { hud.actions([]); },
    skip() { while (trials.length < 4) { p.L = [0.5, 0.65, 0.8, 0.95][trials.length]; const T = 2 * Math.PI * Math.sqrt(p.L / G); trials.push({ L: lenCm(), t: 20 * T, T }); } },
  });

  steps.push({
    title: 'L–T² graph and g', text: 'The points lie on a straight line through the origin: L ∝ T². Read the slope and find g.', hideBelt: true, shot: SHOT_ALL,
    enter() {
      const pts = trials.map((t) => [t.T * t.T, t.L]);
      const fit = fitLine(pts); this.fit = fit;
      graph.draw(pts, fit, { xMax: 4.5, yMax: 110 }); graph.show(true);
      const slope = fit.b / 100; const g = 4 * Math.PI * Math.PI * slope; this.g = g;
      const opts = [[g, '4π² × slope'], [slope * 2 * Math.PI, '2π × slope'], [4 * Math.PI * Math.PI / slope / 10, '4π² / slope'], [Math.PI * Math.PI * slope, 'π² × slope']]
        .map(([v, why]) => ({ label: `${v.toFixed(2)} m/s²  (${why})`, value: v })).sort(() => Math.random() - 0.5);
      const ask = () => ui.choose(ctx.stage.clientWidth / 2, 50, `Slope = ${fit.b.toFixed(1)} cm/s² = ${slope.toFixed(4)} m/s². g = ?`, opts, (v) => {
        if (Math.abs(v - g) > 1e-9) { ctx.mistake('From T = 2π√(L/g): L/T² = g/4π², so g = 4π² × slope.', 3); anim.wait(0.4, ask); return; }
        ui.observe('g', `<b>${g.toFixed(2)} m/s²</b>`); ctx.next(`g = 4π² × ${slope.toFixed(4)} = ${g.toFixed(2)} m/s².`, 1.2);
      });
      anim.wait(1.0, ask);
    },
    exit() { ui.clearChooser(); graph.show(false); },
  });

  pose();
  ctx.debug = { p, trials, watch };
  return {
    tools: [], steps,
    update(dt, t) {
      if (!p.held) { integrate(dt); pose(); }
      watch.update(dt);
      lenChip.at.set(bob.position.x, bob.position.y + BY, bob.position.z);
      if (ctx.stepIndex === IDX.len) lenChip.show(true).set(`L = <b>${lenCm().toFixed(1)}</b> cm`);
      angChip.at.copy(bob.position); angChip.at.y += BY;
      hud.update();
    },
    result() {
      const s = steps[steps.length - 1]; const g = s.g || 0; const err = (g - G) / G * 100;
      return {
        title: 'Simple pendulum',
        rows: trials.map((t) => [`L = ${t.L.toFixed(1)} cm`, `T = ${t.T.toFixed(3)} s`]).concat([['g (your graph)', `${g.toFixed(2)} m/s²`], ['g in Kathmandu', `${G.toFixed(3)} m/s²`], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(1)} %`]]),
        conclusion: `The acceleration due to gravity is ${g.toFixed(2)} m/s². ${Math.abs(err) < 1 ? 'Excellent timing.' : 'Errors come from reaction time at start and stop (timing 20 swings divides it by 20), from wide amplitudes, and from measuring L to the wrong point of the bob.'}`,
      };
    },
    dispose() { hud.dispose(); watch.dispose(); graph.dispose(); },
  };
}
