// Coefficient of friction, two ways, for the same wooden block on the same plank. First the
// angle of repose: the student lifts the free end of the hinged plank by hand; the block holds by
// static friction until tan θ exceeds this trial's μs (it varies a little from trial to trial, as
// dust and humidity make it do), then slides down at g(sin θ − μk cos θ). The angle is read off
// the quadrant where the plank's pointer stands. Then the plank is laid flat and the block is
// pulled through a spring balance with a maximum-reading marker; loads of 0, 100 and 200 g are
// added, and the breakaway force against the normal reaction gives μ from the slope.
import { THREE } from '../../engine.js';
import { MAT, mesh, canvasTexture, clamp } from '../../bio-handson/kit.js';
import { M as KIT } from '../../lab3d-kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, hits, screenDist } from '../hud.js';
import { createGraph } from '../stopwatch.js';

const BY = 0.8; const G = 9.8; const LEN = 6; const HX = -3; const HY = 0.45; const BLOCK_M = 0.2; const FMAX = 2.5;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });
const gauss = () => { let u = 0; for (let i = 0; i < 6; i++) u += Math.random(); return (u - 3) / Math.sqrt(0.5); };

function quadrantTex() {
  return canvasTexture('ho-fr-quad', 1024, 1024, (g, w, h) => {
    g.clearRect(0, 0, w, h); g.fillStyle = 'rgba(250,248,240,.96)'; g.beginPath(); g.moveTo(0, h); g.arc(0, h, w - 4, -Math.PI / 2, 0); g.closePath(); g.fill();
    g.fillStyle = '#0b0f14'; g.strokeStyle = '#0b0f14';
    for (let d = 0; d <= 90; d++) {
      const a = -d * Math.PI / 180; const big = d % 10 === 0; const mid = d % 5 === 0; const r1 = w - 8; const r0 = r1 - (big ? 70 : mid ? 50 : 30);
      g.lineWidth = big ? 4 : 2.4; g.beginPath(); g.moveTo(Math.cos(a) * r0, h + Math.sin(a) * r0); g.lineTo(Math.cos(a) * r1, h + Math.sin(a) * r1); g.stroke();
      if (big) { g.save(); g.translate(Math.cos(a) * (r0 - 40), h + Math.sin(a) * (r0 - 40)); g.rotate(a + Math.PI / 2); g.font = '800 40px system-ui, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(String(d), 0, 0); g.restore(); }
    }
    g.font = '700 34px system-ui, sans-serif'; g.fillText('degrees', 120, h - 40);
  }, { anisotropy: 16 });
}
function balanceTex() {
  return canvasTexture('ho-fr-bal', 2048, 160, (g, w, h) => {
    g.fillStyle = '#f8f6ee'; g.fillRect(0, 0, w, h); g.fillStyle = '#0b0f14';
    const x = (n) => w - 80 - (w - 160) * n / FMAX;
    for (let i = 0; i <= FMAX * 20; i++) { const n = i / 20; const big = i % 10 === 0; const mid = i % 2 === 0; g.fillRect(Math.round(x(n) - 2), 0, 4, big ? 70 : mid ? 50 : 32); if (big || i % 10 === 5) { g.font = `800 ${big ? 46 : 34}px system-ui, sans-serif`; g.textAlign = 'center'; g.fillText(String(n), x(n), 122); } }
    g.font = '700 30px system-ui, sans-serif'; g.textAlign = 'left'; g.fillText('N', 20, 122);
  }, { anisotropy: 16 });
}

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const graph = createGraph(hud, { title: 'Limiting friction against normal reaction', xLabel: 'N (newton)', yLabel: 'F (N)' });
  const MU = Math.round((0.32 + Math.random() * 0.18) * 1000) / 1000; const MUK = MU * 0.8;

  world.add(mesh(new THREE.BoxGeometry(7, 0.3, 1.2), MAT.matte(0x2b3138), [0, 0.15, 0]));
  const hinge = new THREE.Group(); hinge.position.set(HX, HY, 0); world.add(hinge);
  const plank = mesh(new THREE.BoxGeometry(LEN, 0.1, 1.0), KIT.wood('oak'), [LEN / 2, -0.05, 0]); hinge.add(plank);
  hinge.add(mesh(new THREE.BoxGeometry(0.08, 0.25, 1.0), MAT.matte(0x30363d), [0.04, 0.05, 0]));
  hinge.add(mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.05, 14), MAT.steel(), [0, -0.05, 0]).rotateX(Math.PI / 2));
  const quad = mesh(new THREE.PlaneGeometry(1.4, 1.4), new THREE.MeshStandardMaterial({ map: quadrantTex(), transparent: true, roughness: 0.6, side: THREE.DoubleSide }), [HX + 0.7, HY + 0.7 - 0.05, 0.56]); world.add(quad);
  world.add(mesh(new THREE.BoxGeometry(0.05, 1.5, 0.05), MAT.matte(0x30363d), [HX - 0.02, HY + 0.7, 0.54]));
  const ptr = mesh(new THREE.BoxGeometry(1.42, 0.012, 0.01), MAT.ink(0xb91c1c), [0.71, -0.05, 0.575]); hinge.add(ptr);
  const block = new THREE.Group(); hinge.add(block);
  block.add(mesh(new THREE.BoxGeometry(0.9, 0.42, 0.6), KIT.wood('teak'), [0, 0.21, 0]));
  const loads = new THREE.Group(); block.add(loads);
  const stack = new THREE.Group(); stack.position.set(2.6, 0.3, 0.9); world.add(stack);
  const slot = (y) => mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.08, 24), MAT.gloss(0x9a7b3a), [0, y, 0]);
  const stackD = [0, 1].map((i) => { const d = slot(0.04 + i * 0.085); stack.add(d); return d; });

  const bal = new THREE.Group(); world.add(bal); bal.visible = false;
  const caseM = mesh(new THREE.BoxGeometry(1.6, 0.14, 0.32), MAT.gloss(0x9aa4ae), [0.8, 0.07, 0]); bal.add(caseM);
  const face = mesh(new THREE.PlaneGeometry(1.4 * 2048 / 1888, 0.11), new THREE.MeshStandardMaterial({ map: balanceTex(), roughness: 0.5 }), [0.8, 0.142, 0.04]); face.rotation.x = -Math.PI / 2; bal.add(face);
  const handle = mesh(new THREE.TorusGeometry(0.1, 0.022, 8, 20), MAT.steel(), [1.7, 0.07, 0]); handle.rotation.x = Math.PI / 2; bal.add(handle);
  const hook = new THREE.Group(); bal.add(hook);
  hook.add(mesh(new THREE.CylinderGeometry(0.012, 0.012, 1.4, 8), MAT.steel(), [0.7, 0.1, -0.06]).rotateZ(Math.PI / 2));
  const needle = mesh(new THREE.BoxGeometry(0.014, 0.03, 0.12), MAT.ink(0x111827), [0, 0.15, 0.02]); hook.add(needle);
  const marker = mesh(new THREE.BoxGeometry(0.03, 0.04, 0.09), MAT.gloss(0xdc2626), [0, 0.16, 0.08]); bal.add(marker);
  const string = mesh(new THREE.CylinderGeometry(0.008, 0.008, 1, 6), MAT.matte(0x5b4636), null, { cast: false }); string.rotation.z = Math.PI / 2; world.add(string); string.visible = false;
  const W_S = 1.4 * 2048 / 1888; const X0 = 0.8 + (1968 / 2048 - 0.5) * W_S; const PER_N = 1.4 / FMAX; const LS = 0.3;

  const st = { theta: 0, s: LEN - 0.8, v: 0, slipping: false, locked: false, rate: 0, trials: [], muTrial: MU, read: null, mode: 'incline', bx: -1.6, bv: 0, hx: 0, F: 0, max: 0, moved: false, pull: [], extra: 0, dragging: false };
  function trialMu() { st.muTrial = MU * (1 + 0.035 * gauss()); }
  trialMu();
  function setTheta(t) { st.theta = clamp(t, 0, THREE.MathUtils.degToRad(50)); hinge.rotation.z = st.theta; }
  function placeBlock() { block.position.set(st.s, 0, 0); }
  placeBlock();

  // ---- method 1: raising the plank ----
  const endPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), -0.5); const hit = new THREE.Vector3();
  const endWorld = new THREE.Vector3();
  const liftHandler = {
    down(p) { if (st.locked || st.slipping) return false; plank.localToWorld(endWorld.set(LEN / 2 - 0.2, 0, 0)); if (screenDist(ctx, endWorld, p) > 140 && !hits(ctx, plank, p, 40)) return false; st.dragging = true; return true; },
    move() {
      if (!st.dragging || st.locked) return; if (!ctx.input.ptr.ray.intersectPlane(endPlane, hit)) return; world.worldToLocal(hit);
      const target = Math.atan2(Math.max(0, hit.y - HY), LEN); const max = THREE.MathUtils.degToRad(0.9);
      setTheta(st.theta + clamp(target - st.theta, -max, max));
    },
    up() { st.dragging = false; }, cancel() { st.dragging = false; },
  };
  let lastTheta = 0;
  function inclineUpdate(dt) {
    st.rate = st.rate * 0.85 + 0.15 * THREE.MathUtils.radToDeg(Math.abs(st.theta - lastTheta)) / Math.max(dt, 1e-3); lastTheta = st.theta;
    if (!st.slipping && !st.locked && Math.tan(st.theta) > st.muTrial && st.s > 1) {
      st.slipping = true; st.locked = true; st.dragging = false; st.slipAt = st.theta; st.slipRate = st.rate; sfx.play('squish');
    }
    if (st.slipping) {
      const a = G * 10 * (Math.sin(st.theta) - MUK * Math.cos(st.theta));
      st.v += a * dt; st.s -= st.v * dt;
      if (st.s <= 0.55) { st.s = 0.55; st.v = 0; st.slipping = false; sfx.play('drop'); onSlid(); }
      placeBlock();
    }
  }
  function onSlid() {
    if (st.slipRate > 5) { ctx.mistake(`You were lifting at about ${st.slipRate.toFixed(0)}° per second when it slipped, so the angle overshoots. Raise the plank slowly near the slipping point.`, 2); resetTrial(); return; }
    ctx.say('It slipped. Now read the angle where the red pointer crosses the quadrant: tap it.', 'info', 3200);
    ctx.rig.go(QUAD(), 1.0); hud.actions([{ id: 'rec', label: 'Record angle', primary: true, disabled: true, onClick: recordAngle }]);
  }
  const quadMark = mesh(new THREE.BoxGeometry(0.15, 0.008, 0.01), new THREE.MeshBasicMaterial({ color: 0x2563eb, depthTest: false }), null, { cast: false }); quadMark.renderOrder = 20; quadMark.visible = false; world.add(quadMark);
  const quadPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), -0.56);
  function tapQuad() {
    if (!ctx.input.ptr.ray.intersectPlane(quadPlane, hit)) return false; world.worldToLocal(hit);
    const dx = hit.x - HX; const dy = hit.y - HY + 0.05; const r = Math.hypot(dx, dy); if (r < 0.6 || r > 1.5) return false;
    const deg = Math.round(THREE.MathUtils.radToDeg(Math.atan2(dy, dx)) * 2) / 2; st.read = deg;
    const a = THREE.MathUtils.degToRad(deg); quadMark.visible = true; quadMark.position.set(HX + Math.cos(a) * 1.25, HY - 0.05 + Math.sin(a) * 1.25, 0.6); quadMark.rotation.z = a;
    hud.relabel('rec', `Record ${deg.toFixed(1)}°`); hud.enable('rec', true); sfx.play('click'); return true;
  }
  function recordAngle() {
    const t = THREE.MathUtils.radToDeg(st.theta);
    if (Math.abs(st.read - t) > 0.6) { ctx.mistake(`The pointer stands at ${t.toFixed(1)}°, not ${st.read.toFixed(1)}°. Read where the red line crosses the scale.`, 2); return; }
    st.trials.push(st.read); ui.observe(`Trial ${st.trials.length}`, `θ = <b>${st.read.toFixed(1)}°</b>`); hud.actions([]); quadMark.visible = false;
    if (st.trials.length >= 3) { ctx.next('Three trials.'); return; }
    resetTrial();
  }
  function resetTrial() {
    hud.actions([]); quadMark.visible = false; const t0 = st.theta;
    anim.add(1.2, (k) => { setTheta(t0 * (1 - k)); st.s = 0.55 + (LEN - 1.35) * k; placeBlock(); }, { done: () => { st.locked = false; trialMu(); lastTheta = 0; ctx.rig.go(SHOT_INC, 0.8); ctx.say('Block back at the top. Raise the plank again, slowly.', 'info', 2200); } });
  }

  // ---- method 2: horizontal pull ----
  const N = () => (BLOCK_M + st.extra) * G;
  function layoutPull() {
    block.position.set(st.bx - HX, 0, 0);
    const caseX = st.hx - 1.7; bal.position.set(caseX, HY, 0);
    hook.position.x = -st.F * PER_N; needle.position.x = X0;
    marker.position.x = Math.min(marker.position.x, X0 - st.max * PER_N);
    const a = st.bx + 0.45; const b = caseX - st.F * PER_N; string.scale.y = Math.max(0.01, b - a); string.position.set((a + b) / 2, HY + 0.1, -0.06);
  }
  function pullUpdate(dt) {
    const n = Math.max(1, Math.ceil(dt / 0.004)); const h = dt / n; const m = BLOCK_M + st.extra;
    for (let i = 0; i < n; i++) {
      st.F = Math.max(0, (st.hx - 1.7 - st.bx - 0.45 - LS) / PER_N);
      if (st.bv <= 0 && st.F <= st.muTrial * N()) { st.bv = 0; continue; }
      st.bv = Math.max(0, st.bv + (st.F - MUK * N()) / m * 10 * h); st.bx += st.bv * h; st.moved = true;
    }
    st.max = Math.max(st.max, st.F);
    if (st.bx > 0.6) { st.bx = 0.6; st.bv = 0; }
    layoutPull();
  }
  const pullPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), -(BY + HY + 0.1));
  const pullHandler = {
    down(p) { if (screenDist(ctx, handle, p) > 70 && !hits(ctx, caseM, p, 30)) return false; st.dragging = true; st.grab = null; return true; },
    move() { if (!st.dragging) return; if (!ctx.input.ptr.ray.intersectPlane(pullPlane, hit)) return; world.worldToLocal(hit); if (st.grab === null) st.grab = hit.x - st.hx; st.hx = clamp(hit.x - st.grab, st.hx - 0.06, st.hx + 0.06); st.hx = clamp(st.hx, st.bx + 0.45 + 1.7 + LS - 0.05, 3.6); },
    up() { st.dragging = false; if (st.moved) { ctx.say('It broke free. The red marker stayed at the largest force: tap the scale at the marker\'s edge to read it.', 'info', 3200); hud.enable('rec', false); ctx.rig.go(BAL(), 0.9); } },
    cancel() { st.dragging = false; },
  };
  const balPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0); const balMark = mesh(new THREE.BoxGeometry(0.01, 0.01, 0.16), new THREE.MeshBasicMaterial({ color: 0x2563eb, depthTest: false }), null, { cast: false }); balMark.renderOrder = 20; balMark.visible = false; world.add(balMark);
  function tapBalance() {
    balPlane.constant = -(BY + HY + 0.142); if (!ctx.input.ptr.ray.intersectPlane(balPlane, hit)) return false; world.worldToLocal(hit);
    const lx = hit.x - bal.position.x; if (Math.abs(hit.z) > 0.3 || lx < 0 || lx > 1.6) return false;
    const n = Math.round((X0 - lx) / PER_N * 20) / 20; st.read = n;
    balMark.visible = true; balMark.position.set(bal.position.x + X0 - n * PER_N, HY + 0.15, 0.04);
    hud.relabel('rec', `Record ${n.toFixed(2)} N`); hud.enable('rec', true); sfx.play('click'); return true;
  }
  function startPull() {
    st.bx = -1.6; st.bv = 0; st.hx = st.bx + 0.45 + 1.7 + LS; st.F = 0; st.max = 0; st.moved = false; trialMu(); marker.position.x = X0; balMark.visible = false; layoutPull();
    hud.actions([{ id: 'rec', label: 'Record', primary: true, disabled: true, onClick: recordPull }]);
    ctx.rig.go(SHOT_PULL, 1.0);
  }
  function recordPull() {
    const truth = st.max;
    if (Math.abs(st.read - truth) > 0.051) { ctx.mistake(`The marker is at ${truth.toFixed(2)} N, not ${st.read.toFixed(2)} N.`, 2); return; }
    st.pull.push([N(), st.read]); ui.observe(`Load +${Math.round(st.extra * 1000)} g`, `N = ${N().toFixed(2)} N, F = <b>${st.read.toFixed(2)} N</b>`);
    if (st.pull.length >= 3) { hud.actions([]); ctx.next('Three loads done.'); return; }
    stackD[st.pull.length - 1].visible = false; const d = slot(0.42 + 0.04 + (st.pull.length - 1) * 0.085); loads.add(d); st.extra = 0.1 * st.pull.length; sfx.play('place');
    ctx.say(`A 100 g mass is added on the block (now +${Math.round(st.extra * 1000)} g). Pull again.`, 'info', 2400);
    startPull();
  }

  const SHOT_INC = shot({ pos: [0.3, 2.4, 8], target: [0.3, 1.0, 0], fit: 7.8, fitH: 3.6 });
  const QUAD = () => shot({ pos: [HX + 0.75, HY + 0.85, 2.2], target: [HX + 0.75, HY + 0.6, 0.5], fit: 1.6, fitH: 1.5 });
  const SHOT_PULL = shot({ pos: [0, 2.8, 4.4], target: [-0.3, 0.4, 0], fit: 5.6, fitH: 2.4 });
  const BAL = () => shot({ pos: [bal.position.x + 0.8, HY + 1.3, 1.3], target: [bal.position.x + 0.8, HY + 0.1, 0], fit: 1.8, fitH: 1.0 });

  const steps = [
    {
      title: 'Angle of repose', text: 'Drag the <b>free end of the plank</b> upwards to tilt it, <b>slowly</b>. The moment the block starts to slide, stop and tap the <b>quadrant</b> where the red pointer crosses it. Three trials.', hint: 'Near the slipping point raise it a degree at a time. The block starts from the top each trial.', shot: SHOT_INC, hideBelt: true,
      enter() { setTheta(0); st.s = LEN - 0.8; placeBlock(); },
      exit() { hud.actions([]); quadMark.visible = false; },
      skip() { while (st.trials.length < 3) { trialMu(); st.trials.push(Math.round(THREE.MathUtils.radToDeg(Math.atan(st.muTrial)) * 2) / 2); } setTheta(0); st.locked = false; st.slipping = false; },
      update(dt) { inclineUpdate(dt); },
      handler: { down(p) { if (st.locked && !st.slipping) return tapQuad(); return liftHandler.down(p); }, move: (p) => liftHandler.move(p), up: (p) => liftHandler.up(p), cancel: (p) => liftHandler.cancel(p) },
    },
    {
      title: 'μ from the angle', text: 'At the angle of repose, mg sin θ = μ mg cos θ.', shot: SHOT_INC, hideBelt: true,
      enter() {
        const m = st.trials.reduce((a, b) => a + b, 0) / st.trials.length; st.thetaMean = m; const t = Math.tan(THREE.MathUtils.degToRad(m)); st.muAngle = t;
        const opts = [[t, 'tan θ'], [Math.sin(THREE.MathUtils.degToRad(m)), 'sin θ'], [Math.cos(THREE.MathUtils.degToRad(m)), 'cos θ'], [1 / t, '1 / tan θ']].map(([v, w]) => ({ label: `${v.toFixed(3)}  (${w})`, value: w })).sort(() => Math.random() - 0.5);
        anim.wait(0.8, () => ui.choose(ctx.stage.clientWidth / 2, 50, `Mean angle of repose θ = ${m.toFixed(1)}°. μs =`, opts, (v) => {
          if (v !== 'tan θ') ctx.mistake('Along the plane mg sin θ = μ mg cos θ, so μ = tan θ: the mass cancels.', 3);
          ui.observe('μ = tan θ', `<b>${t.toFixed(3)}</b>`); ctx.next(`μs = tan ${m.toFixed(1)}° = ${t.toFixed(3)}.`);
        }));
      },
      exit() { ui.clearChooser(); },
    },
    {
      title: 'Pull with a spring balance', text: 'The plank is flat and the block is hooked to a spring balance. Drag the balance\'s <b>ring</b> to the right <b>slowly and steadily</b> until the block breaks free, let go, then tap the scale at the <b>red marker</b> and record. A 100 g mass is added each time: three loads.', hint: 'The red marker is pushed along by the pointer and stays at the largest force: the limiting friction.', shot: SHOT_PULL, hideBelt: true,
      enter() { setTheta(0); bal.visible = true; string.visible = true; quad.visible = false; ptr.visible = false; st.mode = 'pull'; startPull(); },
      exit() { hud.actions([]); balMark.visible = false; },
      skip() { st.pull = []; [0, 0.1, 0.2].forEach((e) => { st.extra = e; trialMu(); st.pull.push([N(), Math.round(st.muTrial * N() * 20) / 20]); }); },
      update(dt) { pullUpdate(dt); },
      handler: { down(p) { if (st.moved && !st.dragging) return tapBalance(); return pullHandler.down(p); }, move: (p) => pullHandler.move(p), up: (p) => pullHandler.up(p), cancel: (p) => pullHandler.cancel(p) },
    },
    {
      title: 'F against N', text: 'Limiting friction against normal reaction: the slope is μs.', shot: SHOT_PULL, hideBelt: true,
      enter() {
        st.muPull = st.pull.reduce((a, [n, f]) => a + f * n, 0) / st.pull.reduce((a, [n]) => a + n * n, 0);
        graph.draw(st.pull, { a: 0, b: st.muPull }, { xMax: 4, yMax: 2 }); graph.show(true);
        ui.observe('μ from slope', `<b>${st.muPull.toFixed(3)}</b>`);
        hud.actions([{ id: 'ok', label: 'Compare the two methods', primary: true, onClick: () => { hud.actions([]); ctx.next(); } }]);
      },
      exit() { graph.show(false); hud.actions([]); },
    },
  ];

  ctx.debug = { st, MU, setTheta };
  return {
    tools: [], steps,
    update() { hud.update(); },
    result() {
      const a = st.muAngle || 0; const b = st.muPull || 0;
      const e = (x) => { const v = (x - MU) / MU * 100; return `${v >= 0 ? '+' : ''}${v.toFixed(1)} %`; };
      return {
        title: 'Coefficient of friction',
        rows: [['Angle of repose', `${(st.thetaMean || 0).toFixed(1)}°`], ['μ = tan θ', `${a.toFixed(3)} (${e(a)})`], ['μ from F–N slope', `${b.toFixed(3)} (${e(b)})`], ['Surfaces (wood on wood)', `μs = ${MU.toFixed(3)}`]],
        conclusion: `Both methods give μs ≈ ${((a + b) / 2).toFixed(2)} for wood on wood. Doubling the normal reaction doubled the limiting friction (a straight line through the origin), and the angle method needs no force at all because the mass cancels. The scatter between trials is real: limiting friction changes a little with dust and the exact spot on the plank, which is why the angle is taken several times.`,
      };
    },
    dispose() { hud.dispose(); graph.dispose(); },
  };
}
