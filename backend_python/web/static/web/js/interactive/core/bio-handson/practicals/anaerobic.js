// Anaerobic respiration (alcoholic fermentation) by yeast. Boil 5% glucose solution to drive out
// the dissolved oxygen (and kill other microbes), cool it in a water trough while watching the
// thermometer, stir in yeast only once it is near 35 °C (hotter kills the yeast), seal the surface
// under a layer of liquid paraffin, and lead the delivery tube into lime water. A second flask
// with boiled yeast is the control. Over an hour at 35 °C bubbles of CO2 turn the lime water milky
// (CaCO3) in the test flask only, and the flask smells of alcohol.
import { THREE } from '../../engine.js';
import { reagentBottle } from '../props.js';
import { makeTube, makeRack } from '../glassware.js';
import { glassBeaker, timelapse, ask, tag } from '../bench.js';
import { mesh, MAT, clamp, smooth, rng } from '../kit.js';
import { conicalFlask } from '../../handson/glass.js';
import { bunsen } from '../../handson/burner.js';
import { thermometer, steamPuffs } from '../../handson/thermo.js';
import { tripodWithGauze } from '../../lab3d-kit.js';
import { createHud } from '../../handson/hud.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });
const TRI = new THREE.Vector3(-1.5, 1.84, -0.3); const TROUGH = new THREE.Vector3(0.05, 0.06, -0.25);

export function create(ctx) {
  const { world, input, anim, sfx, ui } = ctx;
  const R = rng((Date.now() & 0xffff) || 11);
  const hud = createHud(ctx); const tchip = hud.chip('ho-chip-read');
  const burner = bunsen(ctx.quality); burner.group.position.set(TRI.x, 0, TRI.z); burner.group.rotation.y = Math.PI / 2; burner.group.scale.setScalar(0.85); world.add(burner.group); burner.setAir(0.85);
  const tri = tripodWithGauze(); tri.scale.y = 1.25; tri.position.set(TRI.x, 0, TRI.z); world.add(tri);
  const trough = glassBeaker(0.85, 0.75, 0xcfe8f5, 0.62); trough.group.position.set(TROUGH.x, 0, TROUGH.z); world.add(trough.group);
  const troughTag = tag('water trough', { h: 0.08 }); troughTag.position.set(TROUGH.x, 0.95, TROUGH.z + 0.75); world.add(troughTag);
  const flaskA = conicalFlask({ color: 0xfef9c3, opacity: 0.4 }); flaskA.setVolume(100); flaskA.group.position.copy(TRI); world.add(flaskA.group);
  const flaskB = conicalFlask({ color: 0xf5e7b8, opacity: 0.5 }); flaskB.setVolume(100); flaskB.group.position.set(TROUGH.x - 0.42, TROUGH.y, TROUGH.z + 0.3); flaskB.group.visible = false; world.add(flaskB.group);
  const th = thermometer({ min: 0, max: 110, div: 1, len: 2.0 }); th.group.scale.setScalar(0.8); flaskA.group.add(th.group); th.group.position.set(0.06, 0.06, 0.02); th.set(22, true);
  const steam = steamPuffs(flaskA.group, 18);
  const yeast = new THREE.Group(); yeast.position.set(0.95, 0, 0.5); world.add(yeast);
  const yb = glassBeaker(0.16, 0.36, 0xd6b98c, 0.5); yeast.add(yb.group); yb.material.opacity = 0.85;
  const yTag = tag('yeast suspension', { h: 0.06 }); yTag.position.set(0, 0.5, 0); yeast.add(yTag);
  const oil = reagentBottle('Liquid paraffin', 0xfffbeb, 'oil'); oil.position.set(1.45, 0, 0.55); world.add(oil);
  const rack = makeRack(2); rack.group.position.set(1.25, 0, -0.25); world.add(rack.group);
  const lime = [0, 1].map((i) => { const t = makeTube(i ? 'B' : 'A', { color: 0xa5d8f0, fill: 0.62 }); t.material.opacity = 0.45; t.group.position.copy(rack.slots[i]); rack.group.add(t.group); return t; });
  const limeTag = tag('lime water', { h: 0.07 }); limeTag.position.set(1.25, 1.5, -0.25); world.add(limeTag);
  const oilLayers = [flaskA, flaskB].map((f) => { const m = mesh(new THREE.CylinderGeometry(1, 1, 0.025, 32), MAT.liquid(0xfde68a, 0.75), null, { cast: false }); m.visible = false; m.renderOrder = 4; f.group.add(m); return m; });
  const bungs = [flaskA, flaskB].map((f) => { const b = mesh(new THREE.CylinderGeometry(0.19, 0.155, 0.16, 20), MAT.gloss(0x7f1d1d), [0, 1.48, 0]); b.visible = false; f.group.add(b); return b; });
  function deliveryTube(i) {
    const f = i ? flaskB : flaskA; const tube = lime[i];
    const a = new THREE.Vector3(TROUGH.x - (i ? 0.42 : 0), 1.45 + 0.06, TROUGH.z + (i ? 0.3 : 0));
    const b2 = new THREE.Vector3(); rack.group.updateMatrixWorld(); tube.group.getWorldPosition(b2); world.worldToLocal(b2);
    const pts = [a, a.clone().setY(1.95 + i * 0.08), b2.clone().setY(1.95 + i * 0.08), b2.clone().setY(1.5), b2.clone().setY(0.18)];
    const m = mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts, false, 'catmullrom', 0.05), 60, 0.018, 8, false), MAT.glassEdge(), null, { cast: false }); m.visible = false; m.renderOrder = 6; world.add(m);
    void f; return { m, end: b2.clone().setY(0.2) };
  }
  let tubesD = null;
  const bubbles = []; const bubMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.8 });
  for (let k = 0; k < 24; k++) { const b = mesh(new THREE.SphereGeometry(0.012, 8, 6), bubMat, null, { cast: false }); b.visible = false; world.add(b); bubbles.push({ m: b, life: 0, i: 0 }); }

  const st = { T: 22, heating: false, boilT: 0, inTrough: false, yeastAt: null, killed: false, oil: 0, t: 0, co2: [0, 0], warm: false };
  const tmp = new THREE.Vector3();
  const BENCH = S([0.1, 2.6, 3.6], [-0.2, 0.9, 0], 4.2);
  const HEAT = S([-0.7, 2.6, 2.9], [-1.45, 1.45, -0.3], 2.4, 3.0);
  const COOL = S([0.9, 2.2, 2.4], [0.45, 0.9, 0.2], 2.3);
  const RUN = S([0.7, 2.4, 3.0], [0.45, 0.9, -0.1], 2.9);

  const stepLight = {
    title: 'Heat the glucose solution', text: 'The flask holds 100 mL of 5% glucose solution. Tap the <b>burner</b> to light it under the tripod.',
    tool: null, autoTool: 'hand', hideBelt: true, shot: HEAT,
    skip() { burner.setGas(1); burner.light(); st.heating = true; },
    handler: { down(p) { if (!input.pick([burner.group])) return false; burner.setGas(1); burner.light(); st.heating = true; sfx.play('click'); ctx.next('Burner lit; the solution warms.'); return true; } },
  };
  const stepBoil = {
    title: 'Boil it, then turn off', text: 'Let the solution <b>boil for a few minutes</b> — boiling drives out the dissolved oxygen and kills other microbes. Then tap the burner to turn it off.',
    tool: null, autoTool: 'hand', hideBelt: true, shot: HEAT,
    skip() { st.T = 100; st.boilT = 5; burner.setGas(0); st.heating = false; },
    handler: { down() {
      if (!input.pick([burner.group])) return false;
      if (st.T < 99) { ctx.mistake(`Not boiling yet (${Math.round(st.T)} °C). Oxygen stays dissolved until it boils.`, 2); return true; }
      if (st.boilT < 3) { ctx.say('Let it boil a little longer to drive out all the oxygen.', 'hint', 2200); return true; }
      burner.setGas(0); st.heating = false; sfx.play('click'); ctx.next('Burner off. The boiled solution is free of oxygen — but far too hot for yeast.'); return true;
    } },
  };
  const stepCool = {
    title: 'Cool it in the trough', text: 'Tap the flask to stand it in the trough of cold water. Watch the thermometer.',
    tool: null, autoTool: 'hand', shot: HEAT,
    skip() { moveFlask(true); st.T = 36; },
    handler: { down() { if (!input.pick([flaskA.group], true)) return false; moveFlask(false); return true; } },
  };
  function moveFlask(instant) {
    const from = flaskA.group.position.clone(); const to = TROUGH.clone();
    st.inTrough = true;
    if (instant) { flaskA.group.position.copy(to); return; }
    sfx.play('glass'); ctx.rig.go(COOL, 1.2);
    anim.add(1.1, (k) => { flaskA.group.position.lerpVectors(from, to, k); flaskA.group.position.y += Math.sin(Math.PI * k) * 0.5; }, { done: () => { sfx.play('place'); ctx.next('Cooling. Oxygen redissolves only slowly into still water.'); } });
  }
  const stepYeast = {
    title: 'Add the yeast at about 35 °C', text: 'Watch the thermometer. When the solution has cooled to about <b>35–40 °C</b>, tap the <b>yeast suspension</b> to stir it in.',
    hint: 'Above about 45 °C the yeast cells are killed; below 25 °C they ferment slowly.', tool: null, autoTool: 'hand', shot: COOL,
    skip() { st.T = 36; st.yeastAt = 36; flaskA.setColor(new THREE.Color(0xe9d29a), 0.6); yeast.visible = false; },
    handler: { down() {
      if (!input.pick([yeast], true)) return false;
      if (st.T > 45) { st.killed = true; ctx.mistake(`At ${Math.round(st.T)} °C the heat kills the yeast: no fermentation would follow. A fresh suspension is ready — wait until the solution has cooled.`, 5); sfx.play('pour'); return true; }
      st.yeastAt = st.T; yeast.visible = false; sfx.play('pour'); flaskA.setColor(new THREE.Color(0xe9d29a), 0.6); ui.observe('Yeast added at', `${Math.round(st.T)} °C`);
      ctx.next(st.T < 27 ? 'Added — a bit cool, so it will ferment slowly, but it will work.' : 'Yeast added at a good temperature for its enzymes.'); return true;
    } },
  };
  const stepOil = {
    title: 'Seal the surface with oil', text: 'Fill the <b>dropper</b> with liquid paraffin and add it to the flask until a layer covers the whole surface (three dropperfuls). It keeps air out.',
    tool: 'dropper', shot: COOL,
    skip() { st.oil = 3; setOil(0, 1); },
    handler: { down() {
      if (input.pick([oil])) { if (!ctx.requireTool('dropper')) return true; this.loaded = true; sfx.play('pick'); return true; }
      if (!input.pick([flaskA.group], true)) return false;
      if (!ctx.requireTool('dropper')) return true;
      if (!this.loaded) { ctx.say('Fill the dropper from the paraffin bottle first.', 'hint', 1800); return true; }
      this.loaded = false; st.oil += 1; sfx.play('drip'); setOil(0, st.oil / 3); ctx.progress(st.oil / 3);
      if (st.oil >= 3) ctx.next('An unbroken film of oil: no oxygen can reach the yeast.'); return true;
    } },
  };
  function setOil(i, k) { const f = i ? flaskB : flaskA; const m = oilLayers[i]; const y = f.surfaceY(); const r = f.radiusAt(y); m.visible = k > 0; m.position.y = y + 0.012; m.scale.set(r * Math.min(1, 0.35 + k * 0.65), 1, r * Math.min(1, 0.35 + k * 0.65)); }
  const stepSeal = {
    title: 'Fit the delivery tube', text: 'Tap the flask to fit the bung with its delivery tube, which dips into the lime water in tube A. A control flask with <b>boiled yeast</b>, set up the same way, leads into tube B.',
    tool: null, autoTool: 'hand', shot: RUN,
    skip() { seal(); },
    handler: { down() { if (!input.pick([flaskA.group], true)) return false; seal(); sfx.play('squish'); ctx.next('Both flasks sealed and stood in the water bath, kept at 35 °C.'); return true; } },
  };
  function seal() {
    if (!tubesD) tubesD = [deliveryTube(0), deliveryTube(1)];
    flaskB.group.visible = true; setOil(1, 1); bungs.forEach((b) => { b.visible = true; }); tubesD.forEach((d) => { d.m.visible = true; });
    trough.material.color.setHex(0xfde2c8); st.warm = true; st.T = 35;
  }
  const stepRun = {
    title: 'Watch for an hour', text: 'Run the clock in 10-minute steps and watch the lime water in tubes A and B.', tool: null, autoTool: 'hand', hideBelt: true, shot: RUN,
    enter() { this.c = timelapse(ctx, { step: 10, unit: 'min', onTick: (m, done) => { const d = m - st.t; st.t = m; advance(d); if (done) { record(m); if (m >= 60 && !this.done) { this.done = true; this.c.show(false); ctx.next(); } } } }); },
    skip() { for (let m = 10; m <= 60; m += 10) { advance(10); st.t = m; record(m); } },
    exit() { if (this.c) this.c.remove(); },
  };
  const rate = () => { const T = st.yeastAt ?? 35; return clamp((T - 18) / 20, 0.3, 1.1); }; // relative fermentation rate of the starter culture
  function advance(dmin) { st.co2[0] += dmin * 0.9 * rate() * (st.killed && !st.yeastAt ? 0 : 1); st.co2[1] += 0; paintLime(); }
  function milk(c) { return smooth(4, 24, c) * (1 - 0.35 * smooth(70, 120, c)); }
  const CLEAR = new THREE.Color(0xa5d8f0); const MILK = new THREE.Color(0xfbfbf8);
  function paintLime() { lime.forEach((t, i) => { const k = milk(st.co2[i]); t.material.color.copy(CLEAR).lerp(MILK, k); t.material.opacity = 0.45 + k * 0.53; }); }
  const words = (k) => (k < 0.08 ? 'clear' : k < 0.35 ? 'faintly cloudy' : k < 0.7 ? 'milky' : 'very milky');
  const log = [];
  function record(m) { const a = milk(st.co2[0]); const b = milk(st.co2[1]); log.push([m, a, b]); ui.observe(`${m} min`, `A ${words(a)} · B ${words(b)}`); }
  const stepSmell = {
    title: 'Open and smell', text: 'Remove the bung of flask A and waft the air toward you with your hand. Tap the flask.', tool: null, autoTool: 'hand', shot: RUN,
    handler: { down() { if (!input.pick([flaskA.group], true)) return false; bungs[0].visible = false; ctx.next('A sweet, fruity smell of alcohol (ethanol): the other product of fermentation.'); return true; } },
  };
  const stepExplain = {
    title: 'Explain the result', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: RUN,
    enter() {
      ask(ctx, 'Why was the glucose solution boiled and covered with oil?', [{ label: 'To remove dissolved O₂ and keep air out', value: 'o' }, { label: 'To dissolve the glucose', value: 'd' }, { label: 'To feed the yeast with oil', value: 'f' }], 'o', {
        wrong: 'Think about which gas must be absent for anaerobic respiration.',
        then() {
          ask(ctx, 'Which equation shows what happened in flask A?', [{ label: 'C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂ + energy', value: 'f' }, { label: 'C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O', value: 'a' }, { label: 'C₆H₁₂O₆ → 2 C₃H₆O₃ (lactic acid)', value: 'l' }], 'f', {
            delay: 0.3, ok: 'Alcoholic fermentation: yeast converts glucose to ethanol and carbon dioxide without oxygen, releasing a little energy (2 ATP per glucose). The CO₂ turned the lime water milky: Ca(OH)₂ + CO₂ → CaCO₃ + H₂O.',
            wrong: (v) => (v === 'a' ? 'That is aerobic respiration — no oxygen was available here.' : 'Lactic acid fermentation happens in muscle and some bacteria, not yeast. Which gas turned the lime water milky?'),
          });
        },
      });
    },
    exit() { ui.clearChooser(); },
  };
  const steps = [stepLight, stepBoil, stepCool, stepYeast, stepOil, stepSeal, stepRun, stepSmell, stepExplain];
  ctx.debug = { st, flaskA, lime, burner };
  return {
    tools: ['hand', 'dropper'],
    steps,
    update(dt, t) {
      burner.update(dt, t);
      if (st.heating && burner.lit) { st.T = Math.min(100, st.T + dt * (st.T < 90 ? 7 : 3)); if (st.T >= 99.5) st.boilT += dt; }
      else if (st.inTrough && !st.warm) st.T += (19 - st.T) * (1 - Math.exp(-dt / 9));
      else if (!st.warm) st.T += (22 - st.T) * (1 - Math.exp(-dt / 60));
      th.set(st.T); th.update(dt, 0.8);
      const boiling = st.T > 99 && burner.lit;
      steam.emit(tmp.set(0, 1.42, 0), boiling ? 8 : st.T > 70 ? 2 : 0, dt); steam.update(dt);
      flaskA.group.updateMatrixWorld(); th.group.getWorldPosition(tchip.at); tchip.at.y += 0.75; tchip.dy = -20; tchip.dx = 14;
      tchip.set(`<b>${Math.round(th.reading)}</b> °C`).show(ctx.stepIndex >= 0 && ctx.stepIndex <= 3);
      hud.update();
      if (tubesD && ctx.stepIndex === 6 && st.co2[0] > 0) {
        const bp = bubbles.find((b) => b.life <= 0); if (bp && Math.random() < dt * 6 * rate()) { bp.life = 1; bp.m.visible = true; bp.m.position.copy(tubesD[0].end); bp.m.position.x += (Math.random() - 0.5) * 0.03; }
      }
      bubbles.forEach((b) => { if (b.life <= 0) return; b.life -= dt * 1.6; b.m.position.y += dt * 0.35; if (b.life <= 0 || b.m.position.y > 0.55) { b.life = 0; b.m.visible = false; } });
    },
    result() {
      const a = milk(st.co2[0]);
      return {
        title: 'Anaerobic respiration in yeast',
        rows: [['Yeast added at', `${Math.round(st.yeastAt ?? 35)} °C`], ['Lime water A (yeast) after 60 min', words(a)], ['Lime water B (boiled yeast)', 'clear'], ['Smell of flask A', 'alcohol (ethanol)']],
        conclusion: 'In the oxygen-free glucose solution (boiled, sealed under oil) living yeast respired anaerobically: CO₂ bubbled out and turned the lime water milky, and ethanol was formed. The boiled-yeast control produced no CO₂, so the gas came from the living yeast. C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂ + energy.',
      };
    },
    dispose() { hud.dispose(); ui.clearChooser(); },
  };
}
