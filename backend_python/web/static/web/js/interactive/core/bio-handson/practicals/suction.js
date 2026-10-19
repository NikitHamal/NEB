// Suction due to transpiration. A leafy twig is cut under water (a cut in air lets air into the
// xylem and breaks the water column), fitted airtight with rubber tubing and vaseline to the top
// of a long glass tube filled with water, and the open lower end stood in a beaker of mercury. As
// the leaves transpire, water is drawn up into the twig and the mercury rises in the tube. The
// student marks the level and reads the scale every 15 minutes; a lamp and a fan speed it up.
import { THREE } from '../../engine.js';
import { glassBeaker, timelapse, ask, sheet, table, tag } from '../bench.js';
import { leaf, stem } from '../specimens/plants.js';
import { mesh, MAT, canvasTexture, rng, clamp, ease } from '../kit.js';
import { createHud } from '../../handson/hud.js';
import { createGraph, fitLine } from '../../handson/stopwatch.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });
const TX = 0.0; const TZ = 0.0; const HG_Y = 0.3; const TOP_Y = 3.9; const PER_MM = 0.01;

function scaleTex() {
  return canvasTexture('suction-scale', 128, 2048, (g, w, h) => {
    g.fillStyle = '#fbfaf3'; g.fillRect(0, 0, w, h); g.fillStyle = '#111827';
    for (let mm = 0; mm <= 150; mm++) { const y = h - 20 - mm * (h - 40) / 150; const t = mm % 10 === 0 ? 60 : mm % 5 === 0 ? 40 : 24; g.fillRect(0, y - 2, t, 4); if (mm % 10 === 0) { g.font = '700 34px system-ui'; g.fillText(String(mm), 66, y + 12); } }
  });
}

export function create(ctx) {
  const { world, input, anim, sfx, ui, tools, fx } = ctx;
  const R = rng((Date.now() & 0xffff) || 13);
  const hud = createHud(ctx);
  const graph = createGraph(hud, { title: 'Rise of mercury', xLabel: 'time (min)', yLabel: 'rise (mm)' }); graph.el.classList.add('ho-side', 'bh-under-clock');
  const base = 0.32 + R() * 0.08; // mm min⁻¹ in still room air, diffuse light
  let lampOn = false; let fanOn = false;
  const rateNow = () => base * (1 + (lampOn ? 0.7 : 0) + (fanOn ? 0.5 : 0));

  // retort stand and the long tube
  const stand = new THREE.Group(); stand.position.set(TX - 0.55, 0, TZ - 0.1); world.add(stand);
  stand.add(mesh(new THREE.BoxGeometry(0.9, 0.05, 0.6), MAT.matte(0x1f2937), [0.25, 0.025, 0]));
  stand.add(mesh(new THREE.CylinderGeometry(0.025, 0.025, 4.4, 10), MAT.steel(), [0, 2.2, -0.15]));
  [1.6, 3.3].forEach((y) => { stand.add(mesh(new THREE.BoxGeometry(0.6, 0.04, 0.04), MAT.steel(), [0.28, y, -0.15])); stand.add(mesh(new THREE.BoxGeometry(0.08, 0.1, 0.12), MAT.gloss(0x334155), [0.55, y, -0.05])); });
  const tube = mesh(new THREE.CylinderGeometry(0.035, 0.035, TOP_Y - 0.15, 18, 1, true), MAT.glass(), [TX, (TOP_Y + 0.15) / 2, TZ], { cast: false }); tube.renderOrder = 5; world.add(tube);
  const water = mesh(new THREE.CylinderGeometry(0.027, 0.027, 1, 14), MAT.liquid(0xcfe8f5, 0.55), null, { cast: false }); water.renderOrder = 4; world.add(water);
  const hg = mesh(new THREE.CylinderGeometry(0.027, 0.027, 1, 14), new THREE.MeshStandardMaterial({ color: 0xc8ccd2, metalness: 1, roughness: 0.15 }), null); world.add(hg);
  const strip = mesh(new THREE.PlaneGeometry(0.09, 1.5 * 1.0 * (2048 / (2048 - 40))), new THREE.MeshStandardMaterial({ map: scaleTex(), roughness: 0.7 }), [TX + 0.085, HG_Y + 0.75, TZ - 0.02]); world.add(strip);
  const beaker = glassBeaker(0.32, 0.4, 0xc8ccd2, 0); beaker.group.position.set(TX, 0, TZ); world.add(beaker.group);
  const pool = mesh(new THREE.CylinderGeometry(0.31, 0.31, HG_Y - 0.02, 28), new THREE.MeshStandardMaterial({ color: 0xc8ccd2, metalness: 1, roughness: 0.12 }), [TX, (HG_Y - 0.02) / 2 + 0.01, TZ]); pool.visible = false; world.add(pool);
  const hgTag = tag('mercury', { h: 0.07 }); hgTag.position.set(TX, 0.55, TZ + 0.38); hgTag.visible = false; world.add(hgTag);
  const rubber = mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.22, 14), MAT.gloss(0x111827), [TX, TOP_Y + 0.05, TZ]); rubber.visible = false; world.add(rubber);
  const seal = mesh(new THREE.TorusGeometry(0.055, 0.02, 8, 18), new THREE.MeshPhysicalMaterial({ color: 0xfff7d6, roughness: 0.2, clearcoat: 1, transparent: true, opacity: 0.85 }), [TX, TOP_Y + 0.16, TZ]); seal.rotation.x = Math.PI / 2; seal.visible = false; world.add(seal);
  // the twig, first held in a trough of water for cutting
  const trough = glassBeaker(0.5, 0.35, 0xbfe3f2, 0.8); trough.group.position.set(1.6, 0, 0.35); world.add(trough.group);
  const twig = new THREE.Group(); world.add(twig);
  const twStem = stem([[0, -0.15, 0], [0, 0.6, 0], [0.04, 1.4, 0.02]], 0.03, 0x5b4a2a, 0.012); twig.add(twStem);
  for (let i = 0; i < 7; i++) { const l = leaf({ len: 0.5, wid: 0.28, upper: '#226b2c', lower: '#7fb069' }); l.position.set(0.02, 0.55 + i * 0.13, 0); l.rotation.set(-0.35, i * 2.4, 0, 'YXZ'); twig.add(l); }
  const stub = mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.12, 10), MAT.matte(0x5b4a2a), [0, -0.21, 0]); twig.add(stub);
  twig.position.set(1.6, 0.25, 0.35); twig.rotation.z = 0.35;
  const lamp = new THREE.Group(); lamp.position.set(-1.6, 0, -0.4); world.add(lamp);
  lamp.add(mesh(new THREE.CylinderGeometry(0.22, 0.26, 0.06, 24), MAT.gloss(0x1f2937), [0, 0.03, 0]));
  lamp.add(mesh(new THREE.CylinderGeometry(0.025, 0.025, 4.2, 10), MAT.steel(), [0, 2.1, 0]));
  const shade = mesh(new THREE.ConeGeometry(0.3, 0.38, 24, 1, true), MAT.gloss(0x0f766e), [0.15, 4.25, 0]); shade.rotation.z = -Math.PI / 2 - 0.5; lamp.add(shade);
  const bulb = mesh(new THREE.SphereGeometry(0.1, 14, 10), new THREE.MeshBasicMaterial({ color: 0x9ca3af }), [0.28, 4.18, 0]); lamp.add(bulb);
  const light = new THREE.PointLight(0xfff1c1, 0, 8, 1.4); light.position.set(0.4, 4.1, 0); lamp.add(light);
  const fan = new THREE.Group(); fan.position.set(1.7, 0, -0.5); fan.rotation.y = -0.9; world.add(fan);
  fan.add(mesh(new THREE.CylinderGeometry(0.25, 0.3, 0.06, 20), MAT.gloss(0xe5e7eb), [0, 0.03, 0]));
  fan.add(mesh(new THREE.CylinderGeometry(0.03, 0.03, 3.6, 10), MAT.gloss(0xe5e7eb), [0, 1.8, 0]));
  const blades = new THREE.Group(); blades.position.set(0, 3.75, 0.08); fan.add(blades);
  for (let i = 0; i < 3; i++) { const b = mesh(new THREE.BoxGeometry(0.1, 0.42, 0.01), MAT.gloss(0x93c5fd), [0, 0.22, 0]); const p = new THREE.Group(); p.rotation.z = i * 2.094; p.add(b); blades.add(p); }
  fan.add(mesh(new THREE.TorusGeometry(0.48, 0.012, 6, 32), MAT.steel(), [0, 3.75, 0.1]));
  fan.add(mesh(new THREE.SphereGeometry(0.09, 12, 10), MAT.gloss(0x1f2937), [0, 3.75, 0]));

  const st = { filled: 0, cut: false, fixed: false, sealed: false, inHg: false, rise: 0, t: 0, reads: [] };
  function setLevels() {
    const top = TOP_Y - 0.1; const hgTop = st.inHg ? HG_Y + st.rise * PER_MM : 0.15;
    hg.visible = st.inHg; hg.scale.y = Math.max(0.001, hgTop - 0.17); hg.position.set(TX, 0.17 + hg.scale.y / 2, TZ);
    const wBot = st.inHg ? hgTop : 0.15; const wTop = 0.15 + (top - 0.15) * st.filled;
    water.visible = st.filled > 0.01; water.scale.y = Math.max(0.001, wTop - wBot); water.position.set(TX, wBot + water.scale.y / 2, TZ);
  }
  setLevels();
  const tmp = new THREE.Vector3();
  const ALL = S([0.3, 3.2, 6.8], [0.05, 2.6, 0], 4.2, 5.7);
  const TOPV = S([0.6, 4.3, 1.5], [0.05, 3.85, 0], 1.3);
  const CUT = S([2.1, 1.3, 1.6], [1.6, 0.4, 0.35], 1.2);
  const BOT = S([0.35, 0.9, 1.4], [0.05, 0.6, 0], 1.0);
  const READ = () => S([TX + 0.25, HG_Y + st.rise * PER_MM + 0.12, 0.85], [TX + 0.05, HG_Y + st.rise * PER_MM + 0.05, 0], 0.5);
  let clock = null; let sh = null;
  const cutAt = [new THREE.Vector3(0, -0.04, 0), new THREE.Vector3(0, 0.42, 0)];
  let marks = [];

  const stepFill = {
    title: 'Fill the tube with water', text: 'The long glass tube must be completely full of (boiled, air-free) water. Press and <b>hold</b> on the tube to fill it from the wash bottle.',
    tool: null, autoTool: 'hand', shot: ALL,
    skip() { st.filled = 1; setLevels(); },
    handler: { down() { if (!input.pick([tube, water], true)) return false; this.on = true; sfx.play('pour'); return true; }, up() { this.on = false; } },
    update(dt) { if (!this.handler.on) return; st.filled = clamp(st.filled + dt / 3); setLevels(); ctx.progress(st.filled); if (st.filled >= 1 && !this.done) { this.done = true; this.handler.on = false; ctx.next('Full to the brim, no air bubbles.'); } },
  };
  const stepCut = {
    title: 'Cut the twig under water', text: 'The twig\'s cut end stands in the trough. With the <b>scalpel</b>, cut through the stem at the right place: drag across one of the marked points.',
    hint: 'A cut made in air lets air into the xylem vessels and the water column breaks.', tool: 'scalpel', shot: CUT,
    enter() { marks = cutAt.map((p) => { tmp.copy(p); twStem.localToWorld(tmp); return fx.mark(tmp, 0.04, 0xfacc15); }); },
    exit() { marks.forEach((m) => fx.unmark(m)); marks = []; },
    skip() { cutTwig(true); },
    handler: {
      down(p) { if (!input.pick([twig, trough.group], true)) return false; if (!ctx.requireTool('scalpel')) return true; this.last = [p.x, p.y]; return true; },
      move(p) {
        if (!this.last) return;
        marks.forEach((m, i) => { input.project(m.position, tmp, ctx.stage.clientWidth, ctx.stage.clientHeight); if (Math.abs(tmp.y - p.y) < 26 && (this.last[0] - tmp.x) * (p.x - tmp.x) < 0) {
          this.last = null;
          if (i === 1) { ctx.mistake('That cut was in air: air is sucked into the xylem and blocks it (embolism). Cut under the water surface.', 4); sfx.play('cut'); return; }
          cutTwig(false);
        } });
        if (this.last) this.last = [p.x, p.y];
      },
      up() { this.last = null; },
    },
  };
  function cutTwig(instant) { st.cut = true; stub.visible = false; if (!instant) { sfx.play('cut'); tmp.copy(cutAt[0]); twStem.localToWorld(tmp); fx.burst(tmp, 0xbfe3f2, 6, 0.1, tmp.y - 0.05); ctx.next('Cut under water: the xylem stays full of water.'); } }
  const stepFix = {
    title: 'Fit the twig to the tube', text: 'Tap the twig to carry its cut end (still wet) into the rubber tubing on top of the full tube.', tool: null, autoTool: 'hand', shot: ALL,
    skip() { fix(true); },
    handler: { down() { if (!input.pick([twig], true)) return false; fix(false); return true; } },
  };
  function fix(instant) {
    st.fixed = true; rubber.visible = true; const to = new THREE.Vector3(TX, TOP_Y + 0.12, TZ);
    if (instant) { twig.position.copy(to); twig.rotation.z = 0; return; }
    const from = twig.position.clone(); const r0 = twig.rotation.z; sfx.play('pick');
    anim.add(1.3, (k) => { twig.position.lerpVectors(from, to, k); twig.position.y += Math.sin(Math.PI * k) * 0.8; twig.rotation.z = r0 * (1 - k); }, { ease: ease.inOut, done: () => { sfx.play('squish'); ctx.next(); } });
  }
  const stepSeal = {
    title: 'Make the joint airtight', text: 'With the <b>brush</b>, paint vaseline round the joint between the twig and the rubber tubing.', tool: 'brush', shot: TOPV,
    skip() { seal.visible = true; st.sealed = true; },
    handler: { down() { if (!input.pick([rubber, twig], true)) return false; if (!ctx.requireTool('brush')) return true; this.n = (this.n || 0) + 1; sfx.play('squish'); seal.visible = true; seal.scale.setScalar(0.5 + this.n * 0.17); ctx.progress(this.n / 3); if (this.n >= 3) { st.sealed = true; ctx.next('Sealed: any leak would let air in instead of pulling mercury up.'); } return true; } },
  };
  const stepHg = {
    title: 'Stand the lower end in mercury', text: 'Tap the beaker of mercury to raise it under the tube until the open lower end dips well into the mercury.', tool: null, autoTool: 'hand', shot: BOT,
    enter() { pool.visible = true; hgTag.visible = true; beaker.group.position.y = -0.0; },
    skip() { st.inHg = true; setLevels(); },
    handler: { down() { if (!input.pick([beaker.group, pool], true)) return false; st.inHg = true; setLevels(); sfx.play('glass'); ctx.next('The column of water is now held between the twig and the mercury.'); return true; } },
  };
  function readHandler(onRead) {
    return { down() {
      const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), -(TZ - 0.02) * 1); const n = new THREE.Vector3(); strip.getWorldPosition(n);
      plane.setFromNormalAndCoplanarPoint(new THREE.Vector3(0, 0, 1), n);
      const hit = input.ptr.ray.intersectPlane(plane, new THREE.Vector3()); if (!hit) return false; world.worldToLocal(hit);
      if (Math.abs(hit.x - TX) > 0.18) return false; const mm = Math.round((hit.y - HG_Y) / PER_MM * 2) / 2; if (mm < -5 || mm > 155) return false;
      onRead(mm); return true;
    } };
  }
  function take(mm, done) {
    const err = Math.abs(mm - st.rise); if (err > 1.5) { ctx.mistake(`Read again at the top of the mercury column (the convex meniscus); your tap was ${err.toFixed(1)} mm off.`, 2); return; }
    st.reads.push([Math.round(st.t), mm]); sfx.play('ok'); ui.observe(`${Math.round(st.t)} min`, `${mm.toFixed(1)} mm`); done();
  }
  const stepMark = {
    title: 'Read the starting level', text: 'Tap the scale at the top of the mercury in the tube.', tool: null, autoTool: 'hand', hideBelt: true, shot: READ(),
    skip() { st.reads.push([0, 0]); },
    handler: readHandler((mm) => take(mm, () => ctx.next('Starting level recorded.'))),
  };
  const stepRun = {
    title: 'Read every 15 minutes', text: 'Run the clock 15 minutes, then tap the scale at the mercury. For the second half hour, switch on the <b>lamp</b> and the <b>fan</b> and see what happens.',
    tool: null, autoTool: 'hand', hideBelt: true, shot: ALL,
    enter() {
      graph.show(ctx.stage.clientWidth > 640); draw();
      hud.actions([{ id: 'lamp', label: 'Lamp: off', onClick() { lampOn = !lampOn; light.intensity = lampOn ? 4 : 0; bulb.material.color.setHex(lampOn ? 0xfff7d6 : 0x9ca3af); hud.relabel('lamp', `Lamp: ${lampOn ? 'on' : 'off'}`); sfx.play('switch'); } },
        { id: 'fan', label: 'Fan: off', onClick() { fanOn = !fanOn; hud.relabel('fan', `Fan: ${fanOn ? 'on' : 'off'}`); sfx.play('switch'); } }]);
      clock = timelapse(ctx, { step: 15, unit: 'min', onTick: (m, done) => { const d = m - st.t; st.t = m; st.rise += rateNow() * d * (1 + (R() - 0.5) * 0.06); setLevels(); if (done) { clock.enable(false); this.waiting = true; ctx.rig.go(READ(), 0.8); hud.root.querySelector('.ho-actions').style.visibility = 'hidden'; } } });
    },
    skip() { for (let m = 15; m <= 60; m += 15) { if (m > 30) { lampOn = fanOn = true; } st.t = m; st.rise += rateNow() * 15; st.reads.push([m, Math.round(st.rise * 2) / 2]); } setLevels(); },
    exit() { if (clock) clock.remove(); clock = null; graph.show(false); hud.actions([]); },
    handler: readHandler((mm) => { const s = stepRun; if (!s.waiting) return; take(mm, () => {
      s.waiting = false; draw(); hud.root.querySelector('.ho-actions').style.visibility = ''; ctx.rig.go(ALL, 0.8); ctx.progress(st.t / 60);
      if (st.t >= 60) ctx.next(); else { clock.enable(true); if (st.t === 30 && !(lampOn && fanOn)) ctx.say('Now switch on the lamp and the fan for the next half hour.', 'hint', 3500); }
    }); }),
  };
  function draw() { const pts = st.reads.map(([t, mm]) => [t, mm, t > 30 ? '#ea580c' : '#2563eb']); graph.draw(pts.length ? pts : [[0, 0]], null, { xMax: 60, yMax: Math.max(40, Math.ceil(base * 2.4 * 60 / 10) * 10) }); }
  const stepResult = {
    title: 'Work out the rates', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: ALL,
    enter() {
      const a = st.reads.filter(([t]) => t <= 30); const b = st.reads.filter(([t]) => t >= 30);
      const ra = fitLine(a).b * 60; const rb = fitLine(b).b * 60; res.ra = ra; res.rb = rb;
      sh = sheet(ctx, { title: 'Mercury level (mm)' });
      sh.set(table(['t (min)', 'level', 'condition'], st.reads.map(([t, mm]) => [t, mm.toFixed(1), t <= 30 ? 'room' : 'lamp + fan'])) + `<p>Rate, room air: <b>${ra.toFixed(0)} mm h⁻¹</b><br>Rate, lamp + fan: <b>${rb.toFixed(0)} mm h⁻¹</b></p>`);
      ask(ctx, 'What pulled the mercury up the tube?', [{ label: 'Transpiration pull: water lost from the leaves is replaced from the tube', value: 'ok' }, { label: 'Root pressure', value: 'rp' }, { label: 'Capillarity of the glass tube', value: 'cap' }], 'ok', {
        ok: 'Water evaporating from the mesophyll and escaping through stomata creates a tension that is passed down the unbroken, cohesive water column in the xylem; it sucks water out of the tube, and the mercury rises to replace it. More light (stomata open, warmer) and moving air (steeper diffusion gradient) raise the rate.',
        wrong: (v) => (v === 'rp' ? 'This twig has no roots at all.' : 'Mercury is depressed, not raised, by capillarity in glass; and the rise kept going as long as the leaves lost water.'),
      });
    },
    exit() { ui.clearChooser(); },
  };
  const res = {};
  const steps = [stepFill, stepCut, stepFix, stepSeal, stepHg, stepMark, stepRun, stepResult];
  ctx.debug = { st, hg, strip, READ };
  void tools;
  return {
    tools: ['hand', 'scalpel', 'brush'],
    steps,
    update(dt) { if (fanOn) blades.rotation.z -= dt * 18; if (fanOn && st.fixed) twig.rotation.x = Math.sin(performance.now() / 160) * 0.02; hud.update(); },
    result() {
      return { title: 'Suction due to transpiration', rows: [['Rise in 1 h', `${st.rise.toFixed(1)} mm of mercury`], ['Rate, still air', `${(res.ra ?? base * 60).toFixed(0)} mm h⁻¹ (true ${(base * 60).toFixed(0)})`], ['Rate, lamp + fan', `${(res.rb ?? base * 2.2 * 60).toFixed(0)} mm h⁻¹ (true ${(base * 2.2 * 60).toFixed(0)})`]], conclusion: 'The mercury rose steadily because the transpiring leaves pulled water out of the tube: transpiration creates a suction (tension) that lifts the water column in the xylem — the cohesion-tension mechanism of the ascent of sap. Light and wind increased transpiration and the rate of rise.' };
    },
    dispose() { if (clock) clock.remove(); if (sh) sh.remove(); hud.dispose(); ui.clearChooser(); },
  };
}
