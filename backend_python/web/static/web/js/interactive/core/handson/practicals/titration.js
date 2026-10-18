// Acid-base titration, done the way the NEB practical is done: rinse and fill a 50 mL burette
// with 0.100 M HCl, run it to the mark and read it at eye level, pipette 25.0 mL of the unknown
// NaOH, add phenolphthalein, then titrate on a white tile with one hand on the stopcock and the
// other swirling, until one drop takes the last pink away. Readings are the student's own (a
// misread meniscus is carried into the answer), the pipetted volume is what the student actually
// drew up, and trials repeat until two titres agree within 0.10 mL.
import { THREE } from '../../engine.js';
import { reagentBottle, washBottle } from '../../bio-handson/props.js';
import { MAT, mesh, clamp } from '../../bio-handson/kit.js';
import { sfx, tone, noise } from '../../bio-handson/sound.js';
import { burette, BURETTE, conicalFlask, bulbPipette, createDrops, whiteTile, funnel, beaker } from '../glass.js';
import { createTitrationFlask, INDICATORS, basicFraction } from '../chem-model.js';
import { createHud, hits, screenDist } from '../hud.js';
import { createReadingTool } from '../reading.js';

sfx.register('drip', () => { tone(1250 + Math.random() * 300, 0.07, { gain: 0.06, slide: 0.55 }); });
sfx.register('stream', () => noise(0.25, { freq: 900, q: 0.8, gain: 0.05, type: 'lowpass' }));
sfx.register('glass', () => { tone(2600, 0.25, { gain: 0.04 }); tone(3900, 0.18, { gain: 0.02, delay: 0.01 }); });

const ACID_M = 0.1;
const BUR_Y = 1.42;
const BY = 0.8;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

export function create(ctx) {
  const { world, anim, ui, fx } = ctx;
  const hud = createHud(ctx);
  const baseM = Math.round((0.08 + Math.random() * 0.04) * 1000) / 1000;
  const chem = createTitrationFlask({ baseM, acidM: ACID_M, indicator: INDICATORS.phenolphthalein });

  // ---- the bench ----
  const stand = new THREE.Group(); world.add(stand);
  stand.add(mesh(new THREE.BoxGeometry(1.5, 0.06, 1.5), MAT.matte(0x2b3138), [0, 0.03, -0.2]));
  const rod = mesh(new THREE.CylinderGeometry(0.045, 0.045, 8.4, 16), MAT.steel(), [0, 4.26, -0.82]); stand.add(rod);
  const boss = mesh(new THREE.BoxGeometry(0.14, 0.14, 0.14), MAT.matte(0x30363d), [0, 5.6, -0.82]); stand.add(boss);
  const arm = mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.8, 10), MAT.steel(), [0, 5.6, -0.42]); arm.rotation.x = Math.PI / 2; stand.add(arm);
  [[-1, 0.075], [1, 0.075]].forEach(([s]) => stand.add(mesh(new THREE.BoxGeometry(0.035, 0.12, 0.09), MAT.matte(0x7f1d1d), [s * 0.08, 5.6, -0.02])));
  const tile = whiteTile(); tile.position.set(0, 0.06, 0); world.add(tile);
  const bur = burette(); bur.group.position.set(0, BUR_Y, 0); world.add(bur.group);
  const fun = funnel(); fun.position.set(-1.35, 0, 0.75); world.add(fun);
  const flask = conicalFlask(); flask.group.position.set(1.15, 0, 0.75); world.add(flask.group); flask.setVolume(0);
  const waste = beaker(0, 0xeef6ff); waste.group.position.set(0, 0.1, 0); world.add(waste.group);
  const naoh = beaker(180, 0xf2f6fa); naoh.group.scale.set(1.25, 1.1, 1.25); naoh.group.position.set(2.3, 0, -0.1); world.add(naoh.group);
  const naohTag = reagentBottle('NaOH', 0xf2f6fa, 'unknown M'); naohTag.scale.setScalar(0.75); naohTag.position.set(2.95, 0, -0.45); world.add(naohTag);
  const pip = bulbPipette(); const PIP_REST = new THREE.Vector3(2.3, 0.06, -0.1); pip.group.position.copy(PIP_REST); world.add(pip.group);
  const acid = reagentBottle('HCl', 0xeef6ff, '0.100 M'); acid.position.set(-1.9, 0, -0.3); world.add(acid);
  const php = reagentBottle('Phenolphth.', 0xf8fafc, 'indicator'); php.scale.setScalar(0.62); php.position.set(-0.95, 0, 0.95); world.add(php);
  const wash = washBottle(); wash.scale.setScalar(0.8); wash.position.set(-2.55, 0, 0.45); world.add(wash);
  ctx.surfaces.push(tile);

  // ---- live state ----
  const st = { open: 0, acc: 0, flowing: false, under: 'waste', swirl: 0, swirlPhase: 0, trial: 0, titres: [], init: null, repeat: false, funnelOn: false, lastDripT: 0, rinsed: { water: false, acid: false }, overshoot: 0 };
  const flaskHome = new THREE.Vector3(0, 0.1, 0);
  const drops = createDrops(world, 8);
  const stream = mesh(new THREE.CylinderGeometry(0.006, 0.009, 1, 8), MAT.liquid(0xe9f2ff, 0.55), null, { cast: false }); stream.visible = false; stream.renderOrder = 6; world.add(stream);
  const plume = new THREE.Mesh(new THREE.CircleGeometry(1, 28), new THREE.MeshBasicMaterial({ color: 0xf7faff, transparent: true, opacity: 0, depthWrite: false }));
  plume.rotation.x = -Math.PI / 2; plume.renderOrder = 4; flask.group.add(plume);
  const col = new THREE.Color();
  const reader = createReadingTool(ctx, hud, bur, BUR_Y);

  const SHOT_ALL = shot({ pos: [0.6, 4.6, 10.5], target: [0.2, 3.6, 0], fitH: 8.6, fit: 6.2 });
  const SHOT_TOP = shot({ pos: [-0.6, BUR_Y + 7.4, 2.4], target: [0, BUR_Y + 6.6, 0], fit: 1.6, fitH: 1.9 });
  const SHOT_TAP = shot({ pos: [0.6, 2.3, 3.4], target: [0, 1.25, 0], fit: 2.0, fitH: 3.0 });
  const SHOT_BENCH = shot({ pos: [0.4, 2.7, 5.8], target: [0.3, 0.9, 0.2], fit: 6.2, fitH: 3 });
  const SHOT_PIP = shot({ pos: [2.0, 2.6, 4.4], target: [2.3, 2.0, -0.1], fitH: 4.2 });
  const SHOT_MARK = shot({ pos: [2.3, 2.81, 0.75], target: [2.3, 2.81, -0.1], fov: 10, limits: { yaw: 0.25, pitch: 0.15, zMin: 0.7, zMax: 1.3 } });

  // ---- helpers ----
  const tmp = new THREE.Vector3();
  function vesselUnder() { return st.under === 'flask' ? 'flask' : st.under === 'waste' ? 'waste' : null; }
  function receiveAcid(ml) {
    const v = vesselUnder();
    if (v === 'flask') { chem.addAcid(ml); flask.setVolume(chem.volumeMl); }
    else if (v === 'waste') waste.setVolume(waste.volume + ml);
  }
  function surfaceWorldY() {
    if (st.under === 'flask') return flask.group.position.y + flask.surfaceY();
    if (st.under === 'waste') return waste.group.position.y + Math.max(0.03, waste.volume / 1000 * 4);
    return 0.08;
  }
  function setOpen(v) {
    const was = st.open; st.open = clamp(v, 0, 1);
    bur.key.rotation.x = (1 - st.open) * Math.PI / 2;
    if ((was === 0) !== (st.open === 0)) sfx.play('click');
  }
  function flowRate() {
    if (st.open <= 0 || bur.reading >= 50) return 0;
    const head = Math.max(0.05, bur.yOf(bur.reading) + 0.7) / (BURETTE.zeroY + 0.7);
    return 0.62 * st.open * st.open * Math.sqrt(head);
  }
  function tickFlow(dt) {
    const q = flowRate();
    st.flowing = q > 0; chem.state.flow = q;
    if (q <= 0) { stream.visible = false; st.acc = 0; return; }
    if (!bur.jetFull) { bur.setJet(true); bur.set(bur.reading + 0.35); ctx.say('The jet below the tap fills and its air bubble is flushed out.', 'info', 2600); }
    const dv = q * dt;
    bur.set(bur.reading + dv);
    bur.tipWorld(tmp); world.worldToLocal(tmp);
    const floorY = surfaceWorldY();
    if (q < 0.16) {
      stream.visible = false;
      st.acc += dv;
      while (st.acc >= 0.05) {
        st.acc -= 0.05;
        drops.spawn(tmp, floorY, (at) => { receiveAcid(0.05); sfx.play('drip'); fx.burst(world.localToWorld(at.clone()), 0xe0f2fe, 3, 0.06, at.y + 0.8); }, 0xeaf3ff);
      }
    } else {
      stream.visible = true;
      const len = Math.max(0.01, tmp.y - floorY);
      stream.scale.y = len; stream.position.set(tmp.x, tmp.y - len / 2, tmp.z);
      receiveAcid(dv);
      st.lastDripT += dt; if (st.lastDripT > 0.25) { st.lastDripT = 0; sfx.play('stream'); }
    }
  }

  // stopcock and swirling, shared by the run-down and titration steps
  const grab = { mode: null, open0: 0, x0: 0, y0: 0, ang: 0, t: 0 };
  function keyHit(p) { return screenDist(ctx, bur.handle, p) < (p.touch ? 64 : 46) || !!ctx.input.pick([bur.key]); }
  const flaskCenter = new THREE.Vector3(); const scr = new THREE.Vector3();
  function stopcockHandler(allowSwirl) {
    return {
      down(p) {
        if (keyHit(p)) { grab.mode = 'key'; grab.open0 = st.open; grab.x0 = p.x; grab.y0 = p.y; return true; }
        if (allowSwirl && st.under === 'flask' && hits(ctx, flask.group, p, 70, 0.6)) {
          grab.mode = 'swirl'; flask.group.getWorldPosition(flaskCenter); flaskCenter.y += 0.6;
          ctx.input.project(flaskCenter, scr, ctx.stage.clientWidth, ctx.stage.clientHeight);
          grab.ang = Math.atan2(p.y - scr.y, p.x - scr.x); grab.t = performance.now(); return true;
        }
        return false;
      },
      move(p) {
        if (grab.mode === 'key') setOpen(grab.open0 + ((p.x - grab.x0) - (p.y - grab.y0)) * 0.0045);
        else if (grab.mode === 'swirl') {
          const a = Math.atan2(p.y - scr.y, p.x - scr.x); let d = a - grab.ang; if (d > Math.PI) d -= Math.PI * 2; if (d < -Math.PI) d += Math.PI * 2;
          const now = performance.now(); const dt = Math.max(8, now - grab.t) / 1000; grab.t = now; grab.ang = a;
          st.swirlTarget = clamp(Math.abs(d / dt) / 9, 0, 1);
        }
      },
      up(p) {
        if (grab.mode === 'key' && p.moved < 6) setOpen(st.open > 0 ? 0 : 0.28);
        grab.mode = null; st.swirlTarget = 0;
      },
      cancel() { grab.mode = null; st.swirlTarget = 0; },
    };
  }

  function placeFlaskUnder(instant) {
    st.under = 'flask';
    const from = flask.group.position.clone();
    const wFrom = waste.group.position.clone(); const wTo = new THREE.Vector3(-0.9, 0, 0.9);
    if (instant) { flask.group.position.copy(flaskHome); waste.group.position.copy(wTo); return; }
    anim.add(0.7, (k) => waste.group.position.lerpVectors(wFrom, wTo, k).setY(wFrom.y + Math.sin(k * Math.PI) * 0.25 + (wTo.y - wFrom.y) * k));
    anim.add(0.9, (k) => { flask.group.position.lerpVectors(from, flaskHome, k); flask.group.position.y += Math.sin(k * Math.PI) * 0.35; }, { delay: 0.5, done: () => sfx.play('glass') });
  }
  function refreshFlaskColour() {
    chem.colour(col);
    const f = basicFraction(chem.state.ind, chem.bulkPh());
    flask.setColor(col, 0.45 + 0.4 * f * Math.min(1, chem.state.indicatorDrops / 2));
  }

  // ---- procedure ----
  const steps = [];
  steps.push({
    title: 'Rinse the burette', text: 'Rinse the burette with <b>distilled water</b> (tap the wash bottle), then with a little of the <b>0.100 M HCl</b> it will hold (tap the acid bottle).', hint: 'Water first, then the acid itself, so no water is left to dilute it.', shot: SHOT_ALL,
    skip() { st.rinsed.water = st.rinsed.acid = true; },
    handler: { down(p) {
      const w = hits(ctx, wash, p, 50, 0.5); const a = hits(ctx, acid, p, 50, 0.3);
      if (!w && !a) return false;
      if (anim.busy('rinse')) return true;
      rinseAnim(w ? 0xeaf6ff : 0xeef6ff);
      if (w) { if (st.rinsed.acid) { ctx.mistake('Rinsing with water <b>after</b> the acid leaves water behind that dilutes the titrant. Rinse with the acid again.', 4); st.rinsed.acid = false; } st.rinsed.water = true; ctx.say('Rinsed with distilled water.', 'info', 1800); }
      if (a) {
        if (!st.rinsed.water) ctx.say('Rinsed with acid. (Washing with water first removes old residues.)', 'info', 2400);
        st.rinsed.acid = true;
        if (st.rinsed.water) anim.wait(1.6, () => ctx.next('Rinsed: any water left inside is now acid of the same 0.100 M.'));
        else { st.rinsed.water = true; anim.wait(1.6, () => ctx.next('Rinsed with the acid.')); }
      }
      return true;
    } },
  });
  function rinseAnim() {
    sfx.play('pour');
    anim.add(1.4, (k) => { bur.set(k < 0.4 ? 50.5 - (k / 0.4) * 6 : 44.5 + ((k - 0.4) / 0.6) * 6); bur.group.rotation.z = Math.sin(k * Math.PI * 4) * 0.02 * (1 - k); }, { id: 'rinse', ease: (t) => t, done: () => { bur.set(50.5); bur.group.rotation.z = 0; waste.setVolume(waste.volume + 4); } });
  }

  steps.push({
    title: 'Fill the burette', text: 'Put the <b>funnel</b> in the top of the burette (tap it), then <b>press and hold</b> the acid bottle to pour. Fill a little <b>above the zero mark</b>.', hint: 'Hold on the HCl bottle; let go once the acid is just above 0. Overfilling spills acid.', shot: SHOT_TOP,
    enter() { st.pouring = false; },
    skip() { fun.position.set(0, BUR_Y + BURETTE.zeroY + 0.5, 0); st.funnelOn = true; bur.set(-0.6); },
    update(dt) {
      if (st.pouring) {
        bur.set(bur.reading - 7.5 * dt);
        acid.rotation.z = Math.min(1.9, acid.rotation.z + dt * 4);
        if (bur.reading < -2.5) { st.pouring = false; ctx.mistake('Overfilled: acid spills over the top of the burette. Pour slowly and stop just above zero.', 3); bur.set(-1.8); }
      } else acid.rotation.z = Math.max(0, acid.rotation.z - dt * 5);
      ctx.progress(clamp((50.5 - bur.reading) / 50.5));
    },
    handler: {
      down(p) {
        if (!st.funnelOn && hits(ctx, fun, p, 50, 0.3)) {
          st.funnelOn = true; const from = fun.position.clone(); const to = new THREE.Vector3(0, BUR_Y + BURETTE.zeroY + 0.5, 0);
          anim.add(1.0, (k) => { fun.position.lerpVectors(from, to, k); fun.position.y += Math.sin(k * Math.PI) * 0.8; }, { done: () => sfx.play('glass') });
          return true;
        }
        if (hits(ctx, acid, p, 55, 0.3)) {
          if (!st.funnelOn) { ctx.say('Put the funnel in first, or the acid runs down the outside.', 'hint', 2200); return true; }
          st.pouring = true; sfx.play('pour'); return true;
        }
        return false;
      },
      up() {
        if (!st.pouring) return; st.pouring = false;
        if (bur.reading < 0) ctx.next('Filled above zero. Now take the funnel out — a funnel left in drips acid in during the titration.');
        else ctx.say(`The level is at ${bur.reading.toFixed(1)} mL — keep pouring until it is just above the zero mark.`, 'hint', 2400);
      },
      cancel() { st.pouring = false; },
    },
  });

  steps.push({
    title: 'Remove the funnel', text: 'Lift the <b>funnel</b> out of the burette (tap it).', shot: SHOT_TOP,
    skip() { fun.position.set(-1.35, 0, 0.75); st.funnelOn = false; },
    handler: { down(p) {
      if (!hits(ctx, fun, p, 50)) return false;
      st.funnelOn = false; const from = fun.position.clone(); const to = new THREE.Vector3(-1.35, 0, 0.75);
      anim.add(1.0, (k) => { fun.position.lerpVectors(from, to, k); fun.position.y += Math.sin(k * Math.PI) * 0.8; }, { done: () => ctx.next('Funnel out.') });
      return true;
    } },
  });

  steps.push({
    title: 'Run the acid down to the mark', text: 'Open the <b>stopcock</b> (drag the white tap, or tap it) to run acid into the waste beaker. This fills the jet. Close it when the meniscus is <b>on or just below 0.00</b>.', hint: 'Drag the tap a little for drops, more for a stream. Tap it to close.', shot: SHOT_TAP,
    enter() { st.under = 'waste'; },
    skip() { bur.setJet(true); bur.set(0.2 + Math.random() * 0.6); setOpen(0); },
    update(dt) {
      tickFlow(dt);
      if (st.open > 0 && bur.reading > 0 && !this.watching) { this.watching = true; ctx.rig.go(shot({ pos: [0.6, BUR_Y + BURETTE.zeroY + 0.3, 2.2], target: [0, BUR_Y + BURETTE.zeroY - 0.2, 0], fov: 30 }), 1.2); }
      if (bur.reading > 6) { setOpen(0); ctx.mistake('Too far below zero — that wastes acid. Top it up and run it down again, slowly.', 2); bur.set(-0.4); this.watching = false; ctx.rig.go(SHOT_TAP, 1); }
      if (st.open === 0 && bur.jetFull && bur.reading >= 0 && bur.reading < 6 && !this.done) { this.done = true; ctx.next('Tap closed. Now read the burette.'); }
    },
    exit() { this.watching = false; this.done = false; setOpen(0); },
    handler: stopcockHandler(false),
  });

  const readStep = (which) => ({
    title: which === 'init' ? 'Read the initial reading' : 'Read the final reading',
    text: `Your eye is level with the meniscus. Drag the <b>red hairline</b> to the <b>bottom of the meniscus</b> and press <b>Record</b>. Read to 0.05 mL; 0 is at the top.`,
    hint: 'The scale counts downwards. Each small division is 0.1 mL; read between two lines as .x5 when the meniscus sits midway.',
    enter() { reader.start((val, truth) => onRead(which, val, truth)); },
    exit() { reader.stop(); },
    skip() { onRead(which, Math.round(bur.reading * 20) / 20, bur.reading, true); },
    handler: reader.handler,
  });
  function onRead(which, val, truth, silent) {
    const err = Math.abs(val - truth);
    if (!silent) {
      if (err > 0.16) ctx.mistake(`You read ${val.toFixed(2)} mL, but the meniscus bottom is at ${truth.toFixed(2)} mL. Read downwards from 0, at the bottom of the curve, with your eye level.`, 4);
      else if (err > 0.06) ctx.mistake(`Close: ${val.toFixed(2)} mL. The bottom of the meniscus is at ${truth.toFixed(2)} mL — read to the nearest 0.05.`, 2);
    }
    if (which === 'init') {
      st.init = val; st.trial += 1;
      ui.observe(`Trial ${st.trial} initial`, `${val.toFixed(2)} mL`);
      if (st.repeat) anim.wait(silent ? 0 : 1.0, () => ctx.goTo(IDX.titrate)); else if (!silent) ctx.next(`Initial reading ${val.toFixed(2)} mL recorded.`);
    } else {
      const titre = Math.round((val - st.init) * 100) / 100;
      st.titres.push(titre);
      ui.observe(`Trial ${st.trial} final`, `${val.toFixed(2)} mL`);
      ui.observe(`Trial ${st.trial} titre`, `<b>${titre.toFixed(2)} mL</b>`);
      if (!silent) ctx.next(`Titre = ${val.toFixed(2)} − ${st.init.toFixed(2)} = ${titre.toFixed(2)} mL.`);
    }
  }

  const IDX = {};
  IDX.readInit = steps.length; steps.push(Object.assign(readStep('init'), { shot: null }));

  let pipState = { holding: false, draining: false };
  steps.push({
    title: 'Pipette 25.0 mL of NaOH', text: '<b>Press and hold</b> the red pipette filler to draw the alkali up past the mark, then hold the <b>pipette stem</b> to let it fall slowly until the meniscus sits <b>on the etched ring</b>. Press <b>On the mark</b>.', hint: 'Draw a little above the ring, then release slowly. The bottom of the meniscus should just touch the ring.', shot: SHOT_PIP,
    enter() {
      pipState = { holding: false, draining: false, zoomed: false };
      hud.actions([{ id: 'mark', label: 'On the mark', primary: true, onClick: () => {
        const err = pip.volume - 25;
        if (pip.volume < 24.5) { ctx.say('Draw the alkali up past the mark first.', 'hint', 2000); return; }
        if (err > 0.06) { ctx.mistake(`The meniscus is still ${(err / pip.mlPerUnit * 100).toFixed(1)} mm above the ring — about ${err.toFixed(2)} mL too much.`, 3); return; }
        if (err < -0.06) { ctx.mistake(`Below the ring by ${(-err).toFixed(2)} mL. Draw up again and come down to the mark.`, 3); return; }
        hud.actions([]);
        ctx.next(err === 0 ? 'Exactly on the mark.' : `On the mark (within ${Math.abs(err).toFixed(2)} mL).`);
      } }]);
    },
    exit() { hud.actions([]); pipState.holding = pipState.draining = false; },
    skip() { pip.set(25 + (Math.random() - 0.5) * 0.04); },
    update(dt) {
      if (pipState.holding) { pip.set(pip.volume + (pip.volume < 23 ? 9 : 2.2) * dt); naoh.setVolume(naoh.volume - 9 * dt * 0.2); pip.bulb.scale.set(0.82, 0.95, 0.82); }
      else pip.bulb.scale.set(1, 1.15, 1);
      if (pipState.draining) pip.set(Math.max(0, pip.volume - 0.35 * dt));
      if (pip.volume > 28.5) { pipState.holding = false; pip.set(27); ctx.mistake('Alkali was sucked up into the filler. Draw more gently and stop a little above the mark.', 3); }
      if (pip.volume > 24.2 && !pipState.zoomed) { pipState.zoomed = true; ctx.rig.go(SHOT_MARK, 1.0); }
      ctx.progress(clamp(pip.volume / 25));
    },
    handler: {
      down(p) {
        if (hits(ctx, pip.filler, p, 60, 0.2)) { pipState.holding = true; sfx.play('squish'); return true; }
        if (pip.volume > 0 && (hits(ctx, pip.group, p, 0, 0) || screenDist(ctx, pip.group, p, pip.MARK - 0.4) < 70)) { pipState.draining = true; return true; }
        return false;
      },
      up() { pipState.holding = false; pipState.draining = false; },
      cancel() { pipState.holding = false; pipState.draining = false; },
    },
  });

  steps.push({
    title: 'Transfer to the conical flask', text: 'Tap the <b>conical flask</b> to run the 25.0 mL of alkali into it. Let it drain and touch the tip to the glass.', shot: SHOT_BENCH,
    skip() { chem.addBase(pip.volume); pip.set(0); flask.setVolume(chem.volumeMl); pip.group.position.copy(PIP_REST); },
    handler: { down(p) {
      if (!hits(ctx, flask.group, p, 70, 0.6)) return false;
      if (anim.busy('xfer')) return true;
      const from = pip.group.position.clone(); const over = flask.group.position.clone().add(new THREE.Vector3(0, 0.55, 0));
      const v0 = pip.volume;
      anim.add(1.1, (k) => { pip.group.position.lerpVectors(from, over, k); pip.group.position.y += Math.sin(k * Math.PI) * 0.6; }, { id: 'xfer', done: () => {
        sfx.play('pour');
        anim.add(3.0, (k) => { pip.set(v0 * (1 - k)); chem.state.baseMl = v0 * k; flask.setVolume(chem.volumeMl); }, { ease: (t) => 1 - Math.pow(1 - t, 1.6), done: () => {
          chem.state.baseMl = v0; pip.set(0);
          ui.choose(ctx.stage.clientWidth / 2, 60, 'A little liquid stays in the tip. What do you do?', [{ label: 'Leave it — the pipette is calibrated for it', value: 'leave' }, { label: 'Blow it out', value: 'blow' }], (v) => {
            if (v === 'blow') { chem.state.baseMl += 0.05; ctx.mistake('Never blow out a pipette marked "AS" or "Ex": it is calibrated to deliver 25.0 mL with that drop left behind.', 3); }
            anim.add(1.0, (k) => pip.group.position.lerpVectors(over, PIP_REST, k));
            ctx.next(`${chem.state.baseMl.toFixed(2)} mL of NaOH in the flask.`);
          });
        } });
      } });
      return true;
    } },
    exit() { ui.clearChooser(); },
  });

  steps.push({
    title: 'Add the indicator', text: 'Add <b>two drops</b> of phenolphthalein (tap the indicator bottle once per drop).', hint: 'Two drops are enough; the indicator is itself a weak acid.', shot: SHOT_BENCH,
    enter() { hud.actions([{ id: 'done', label: 'Done', primary: true, disabled: true, onClick: () => { hud.actions([]); ctx.next('The alkali turns pink: phenolphthalein is pink above pH 10.'); } }]); },
    exit() { hud.actions([]); },
    skip() { chem.addIndicator(2); refreshFlaskColour(); },
    handler: { down(p) {
      if (!hits(ctx, php, p, 50, 0.25)) return false;
      flask.group.getWorldPosition(tmp); tmp.y += 1.5; world.worldToLocal(tmp);
      drops.spawn(tmp, flask.surfaceY() + flask.group.position.y, () => { chem.addIndicator(1); sfx.play('drip'); refreshFlaskColour(); hud.enable('done', chem.state.indicatorDrops >= 1);
        if (chem.state.indicatorDrops === 5) ctx.mistake('Too much indicator: phenolphthalein is a weak acid and uses up some of the alkali.', 2); }, 0xffffff);
      return true;
    } },
  });

  steps.push({
    title: 'Flask onto the white tile', text: 'Move the flask onto the <b>white tile</b> under the burette (tap the tile). The waste beaker comes away.', shot: SHOT_BENCH,
    skip() { placeFlaskUnder(true); },
    handler: { down(p) {
      if (!hits(ctx, tile, p, 80) && !hits(ctx, waste.group, p, 50)) return false;
      placeFlaskUnder(false); anim.wait(1.6, () => ctx.next('The white tile shows the faintest pink.'));
      return true;
    } },
  });

  IDX.titrate = steps.length;
  steps.push({
    title: 'Titrate to the end point', text: 'Open the tap to let acid in, <b>swirl the flask</b> (drag round it in circles) all the time, and slow to <b>drop by drop</b> as the pink starts to vanish where the acid lands. Stop when one drop leaves the solution <b>colourless</b>.', hint: 'Fast at first, then drop by drop. If the pink comes back on swirling, you are not there yet.', shot: SHOT_TAP,
    enter() {
      st.swirlTarget = 0;
      hud.actions([{ id: 'stop', label: 'Colourless — end point', primary: true, onClick: endPoint }]);
    },
    exit() { hud.actions([]); setOpen(0); },
    skip() {
      const v = chem.equivalenceMl - chem.state.acidMl + 0.02;
      chem.addAcid(v); chem.state.plumeMl = 0; bur.set(bur.reading + v); flask.setVolume(chem.volumeMl); refreshFlaskColour();
    },
    update(dt) { tickFlow(dt); ctx.progress(clamp(chem.state.acidMl / Math.max(1, chem.equivalenceMl * 1.05))); },
    handler: stopcockHandler(true),
  });
  function endPoint() {
    if (st.open > 0) { setOpen(0); }
    chem.state.plumeMl = 0;
    const f = basicFraction(chem.state.ind, chem.finalPh());
    if (f > 0.04) { ctx.mistake('Swirl it: the pink comes back, so there is still alkali left. Add more, drop by drop.', 2); return; }
    const over = chem.state.acidMl - chem.equivalenceMl;
    st.overshoot = over;
    if (over > 0.12) ctx.mistake(`Overshot by about ${over.toFixed(2)} mL — the last few drops went in after the end point. That titre will be too high.`, 4);
    hud.actions([]);
    ctx.next(over <= 0.12 ? 'One drop and the pink is gone: the end point.' : 'Colourless.');
  }

  IDX.readFinal = steps.length; steps.push(Object.assign(readStep('final'), { shot: null }));

  steps.push({
    title: 'Concordant titres', text: 'Titres must agree within <b>0.10 mL</b>. Repeat, or go on if you have two that agree.', hideBelt: true, shot: SHOT_ALL,
    enter() {
      const ok = concordant();
      const btns = [{ id: 'again', label: 'Another titration', primary: !ok, onClick: () => { hud.actions([]); repeatTrial(); } }];
      if (ok || st.trial >= 4) btns.push({ id: 'calc', label: ok ? 'Calculate' : 'Calculate anyway', primary: true, onClick: () => { hud.actions([]); ctx.next(ok ? `Concordant: ${ok.map((x) => x.toFixed(2)).join(' and ')} mL.` : 'Using the closest two.'); } });
      hud.actions(btns);
      if (!ok) ctx.say(st.trial === 1 ? 'One titre is not a result: repeat for concordant values.' : 'No two titres agree within 0.10 mL yet.', 'hint', 3200);
    },
    exit() { hud.actions([]); },
  });
  function concordant() {
    const t = st.titres; let best = null; let bd = 1e9;
    for (let i = 0; i < t.length; i++) for (let j = i + 1; j < t.length; j++) { const d = Math.abs(t[i] - t[j]); if (d < bd) { bd = d; best = [t[i], t[j]]; } }
    return bd <= 0.1001 ? best : (st.trial >= 4 ? best : null);
  }
  function repeatTrial() {
    st.repeat = true;
    ctx.say('You rinse the flask, pipette a fresh 25.0 mL, add two drops of indicator and refill the burette.', 'info', 3600);
    chem.reset(); chem.addBase(25 + (Math.random() - 0.5) * 0.03); chem.addIndicator(2);
    flask.setVolume(0);
    anim.add(1.2, (k) => { flask.setVolume(chem.volumeMl * k); refreshFlaskColour(); }, { delay: 0.3 });
    const r0 = bur.reading; const r1 = Math.round((0.1 + Math.random() * 0.8) * 100) / 100;
    anim.add(1.4, (k) => bur.set(r0 + (r1 - r0) * k), { done: () => { ctx.rig.go(readShot(), 1.2); ctx.goTo(IDX.readInit); } });
  }

  steps.push({
    title: 'Calculate the molarity', text: 'Use the mean of your concordant titres. NaOH + HCl → NaCl + H₂O, a 1 : 1 reaction.', hideBelt: true, shot: SHOT_ALL,
    enter() {
      const pair = concordant() || st.titres.slice(-2);
      const mean = (pair[0] + pair[1]) / 2; st.mean = mean;
      const right = ACID_M * mean / 25;
      const opts = [[right, 'M₁V₁ = M₂V₂ ⇒ 0.100 × V / 25.0'], [ACID_M * 25 / mean, '0.100 × 25.0 / V'], [ACID_M * mean / 50, '0.100 × V / 50.0'], [2 * ACID_M * mean / 25, '2 × 0.100 × V / 25.0']]
        .map(([v, why]) => ({ label: `${v.toFixed(4)} M  (${why})`, value: v })).sort(() => Math.random() - 0.5);
      const ask = () => ui.choose(ctx.stage.clientWidth / 2, 50, `Mean titre ${mean.toFixed(2)} mL. Molarity of the NaOH?`, opts, (v) => {
        if (Math.abs(v - right) > 1e-9) { ctx.mistake('Moles of HCl = moles of NaOH (1 : 1), so M(NaOH) × 25.0 = 0.100 × V(HCl).', 3); anim.wait(0.5, ask); return; }
        st.answer = v; ui.observe('M(NaOH)', `<b>${v.toFixed(4)} M</b>`);
        ctx.next(`M(NaOH) = 0.100 × ${mean.toFixed(2)} / 25.0 = ${v.toFixed(4)} M.`, 1.2);
      });
      anim.wait(0.6, ask);
    },
    exit() { ui.clearChooser(); },
  });

  function readShot() { const y = BY + BUR_Y + bur.yOf(bur.reading); return { pos: [0, y, 0.95], target: [0, y, 0], fov: 13, limits: { yaw: 0.12, pitch: 0.06, zMin: 0.75, zMax: 1.25 } }; }
  steps[IDX.readInit].shot = null; steps[IDX.readFinal].shot = null;
  const origEnterI = steps[IDX.readInit].enter; steps[IDX.readInit].enter = (c) => { ctx.rig.go(readShot(), 1.3); origEnterI(c); };
  const origEnterF = steps[IDX.readFinal].enter; steps[IDX.readFinal].enter = (c) => { ctx.rig.go(readShot(), 1.3); origEnterF(c); };

  ctx.debug = { st, chem, bur, pip, flask, setOpen };
  return {
    tools: [], steps,
    update(dt, t) {
      drops.update(dt);
      st.swirl += ((st.swirlTarget || 0) - st.swirl) * (1 - Math.exp(-dt * 5));
      chem.state.swirl = st.swirl;
      chem.step(dt);
      if (st.under === 'flask') {
        st.swirlPhase += dt * (6 + 10 * st.swirl);
        const a = 0.035 * st.swirl;
        flask.group.position.set(flaskHome.x + Math.cos(st.swirlPhase) * a, flaskHome.y, flaskHome.z + Math.sin(st.swirlPhase) * a);
        flask.surface.rotation.set(-Math.PI / 2 + Math.sin(st.swirlPhase) * 0.18 * st.swirl, Math.cos(st.swirlPhase) * 0.18 * st.swirl, 0);
        if (chem.state.indicatorDrops > 0) {
          refreshFlaskColour();
          const s = chem.plumeStrength(); const pink = basicFraction(chem.state.ind, chem.bulkPh());
          plume.material.opacity = s * pink * 0.92;
          const r = Math.min(flask.radiusAt(flask.surfaceY()) * 0.92, 0.05 + Math.sqrt(chem.state.plumeMl) * 0.22 + st.swirl * 0.12);
          plume.scale.set(r, r, 1); plume.position.set(Math.cos(st.swirlPhase * 1.3) * st.swirl * 0.05, flask.surfaceY() + 0.002, Math.sin(st.swirlPhase * 1.3) * st.swirl * 0.05);
          plume.visible = plume.material.opacity > 0.01;
        }
      }
      hud.update();
    },
    result() {
      const err = st.answer ? (st.answer - baseM) / baseM * 100 : 0;
      return {
        title: 'Acid–base titration',
        rows: [['Titres', st.titres.map((x) => x.toFixed(2)).join(', ') + ' mL'], ['Mean concordant titre', `${(st.mean || 0).toFixed(2)} mL`], ['Your M(NaOH)', `${(st.answer || 0).toFixed(4)} M`], ['True M(NaOH)', `${baseM.toFixed(4)} M`], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(2)} %`]],
        conclusion: `The NaOH solution is ${(st.answer || 0).toFixed(3)} M. ${Math.abs(err) < 0.6 ? 'Excellent technique: within the ±0.5 % a careful student reaches with a class A burette and pipette.' : Math.abs(err) < 2 ? 'Good. The error comes from burette readings, the volume on the pipette mark and how sharply you caught the end point.' : 'The error is large: check your readings (downwards, bottom of the meniscus), stop at the first permanent colourless, and keep the pipette on its mark.'}`,
      };
    },
    dispose() { hud.dispose(); drops.dispose(); flask.dispose(); reader.dispose(); },
  };
}
