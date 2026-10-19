// Preparation of hydrogen, oxygen and carbon dioxide in one generator: a flask with a two-holed
// cork, a thistle funnel and a delivery tube. For each gas the student puts in the right solid,
// pours the liquid down the thistle funnel (held press; the stem must dip under the liquid or the
// gas escapes up it), chooses how to collect it from its solubility and density, lets the first
// bubbles (air) go before placing the jar, watches the jar fill, and identifies the gas with the
// test of their choice. Gas comes off at a rate set by the reaction and fills the jar as it would.
import { THREE } from '../../engine.js';
import { MAT, mesh } from '../../bio-handson/kit.js';
import { reagentBottle } from '../../bio-handson/props.js';
import { sfx, tone, noise } from '../../bio-handson/sound.js';
import { createHud, hits } from '../hud.js';

const BY = 0.8;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });
sfx.register('pop', () => { noise(0.12, { freq: 900, q: 0.8, gain: 0.5 }); tone(140, 0.12, { gain: 0.15, slide: 0.5 }); });
const V2 = (x, y) => new THREE.Vector2(x, y);
const GASES = {
  H2: { name: 'Hydrogen', f: 'H₂', solid: 'zn', liquid: 'hcl', rate: 9, method: 'water', eq: 'Zn + 2HCl → ZnCl₂ + H₂', test: 'burning', result: 'A squeaky pop: hydrogen burns (2H₂ + O₂ → 2H₂O).' },
  O2: { name: 'Oxygen', f: 'O₂', solid: 'mno2', liquid: 'h2o2', rate: 12, method: 'water', eq: '2H₂O₂ → 2H₂O + O₂ (MnO₂ catalyst)', test: 'glowing', result: 'The glowing splint bursts back into flame: oxygen.' },
  CO2: { name: 'Carbon dioxide', f: 'CO₂', solid: 'marble', liquid: 'hcl', rate: 12, method: 'up', eq: 'CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂', test: 'lime', result: 'Lime water turns milky (CaCO₃): carbon dioxide.' },
};
const TESTS = { burning: 'Burning splint', glowing: 'Glowing splint', lime: 'Bubble into lime water', litmus: 'Moist blue litmus' };
function testResult(g, t) {
  if (t === 'burning') return g === 'H2' ? GASES.H2.result : g === 'O2' ? 'The splint burns more brightly (but a glowing splint is the proper test).' : 'The burning splint goes out: the gas does not support burning.';
  if (t === 'glowing') return g === 'O2' ? GASES.O2.result : 'The glowing splint goes out.';
  if (t === 'lime') return g === 'CO2' ? GASES.CO2.result : 'Lime water stays clear.';
  return g === 'CO2' ? 'Moist blue litmus turns faintly red (carbonic acid).' : 'No change.';
}

export function create(ctx) {
  const { world, anim, ui, fx } = ctx;
  const hud = createHud(ctx);
  world.add(mesh(new THREE.BoxGeometry(6, 0.02, 2.6), MAT.matte(0x2f3640), [0, 0.01, 0]));
  // generator flask with cork, thistle funnel, delivery tube
  const FX = -1.5; const flask = new THREE.Group(); flask.position.set(FX, 0, 0); world.add(flask);
  flask.add(mesh(new THREE.LatheGeometry([V2(0.001, 0), V2(0.38, 0), V2(0.42, 0.05), V2(0.44, 0.25), V2(0.38, 0.55), V2(0.16, 0.85), V2(0.14, 0.9), V2(0.14, 1.15), V2(0.16, 1.18)], 40), MAT.glass(), null, { cast: false }));
  flask.add(mesh(new THREE.CylinderGeometry(0.15, 0.13, 0.16, 20), MAT.matte(0x9a6b3e), [0, 1.2, 0]));
  const liqMat = MAT.liquid(0xeef5fb, 0.5); const liq = mesh(new THREE.CylinderGeometry(0.4, 0.4, 1, 30), liqMat, null, { cast: false }); liq.visible = false; flask.add(liq);
  const solidMat = new THREE.MeshStandardMaterial({ color: 0x9aa0a6, roughness: 0.6 }); const solid = new THREE.Group(); flask.add(solid);
  for (let i = 0; i < 14; i++) { const s = mesh(new THREE.DodecahedronGeometry(0.05 + Math.random() * 0.03, 0), solidMat, [(Math.random() - 0.5) * 0.5, 0.05, (Math.random() - 0.5) * 0.5]); solid.add(s); }
  solid.visible = false;
  const thistle = new THREE.Group(); thistle.position.set(-0.05, 0, 0); flask.add(thistle);
  thistle.add(mesh(new THREE.CylinderGeometry(0.018, 0.018, 1.75, 10), MAT.glass(), [0, 1.0, 0], { cast: false }));
  thistle.add(mesh(new THREE.LatheGeometry([V2(0.02, 0), V2(0.08, 0.06), V2(0.1, 0.16), V2(0.06, 0.24), V2(0.12, 0.34)], 24), MAT.glass(), [0, 1.86, 0], { cast: false }));
  const STEM_TIP = 0.13;
  const deliv = mesh(new THREE.BufferGeometry(), MAT.glass(), null, { cast: false }); world.add(deliv);
  // trough with beehive shelf; gas jar
  const TX = 0.9;
  const trough = new THREE.Group(); trough.position.set(TX, 0, 0); world.add(trough);
  trough.add(mesh(new THREE.BoxGeometry(1.7, 0.5, 1.0), MAT.glass(), [0, 0.25, 0], { cast: false }));
  const water = mesh(new THREE.BoxGeometry(1.66, 0.4, 0.96), MAT.liquid(0xcfe6f5, 0.35), [0, 0.22, 0], { cast: false }); trough.add(water);
  trough.add(mesh(new THREE.CylinderGeometry(0.22, 0.25, 0.18, 24), MAT.matte(0xb5651d), [0, 0.11, 0]));
  const jar = new THREE.Group(); world.add(jar);
  jar.add(mesh(new THREE.CylinderGeometry(0.3, 0.3, 1.2, 30, 1, true), MAT.glass(), [0, 0.6, 0], { cast: false }));
  const jarTop = mesh(new THREE.CircleGeometry(0.3, 30), MAT.glass(), [0, 0.01, 0], { cast: false }); jarTop.rotation.x = -Math.PI / 2; jar.add(jarTop);
  const jarWater = mesh(new THREE.CylinderGeometry(0.29, 0.29, 1, 26), MAT.liquid(0xcfe6f5, 0.4), null, { cast: false }); jar.add(jarWater);
  const plate = mesh(new THREE.BoxGeometry(0.7, 0.012, 0.7), MAT.glassEdge(), [0, 0, 0], { cast: false }); world.add(plate); plate.visible = false;
  const JAR_HOME = new THREE.Vector3(TX + 1.5, 0, 0.75);
  const solids = { zn: reagentBottle('Zn', 0x9aa0a6, 'granulated'), mno2: reagentBottle('MnO₂', 0x262626, 'powder'), marble: reagentBottle('CaCO₃', 0xf0ede6, 'marble chips') };
  const liquids = { hcl: reagentBottle('dil. HCl', 0xeef5fb), h2o2: reagentBottle('H₂O₂', 0xf2f6f8, '20 vol') };
  [...Object.values(solids), ...Object.values(liquids)].forEach((b, i) => { b.scale.setScalar(0.8); b.position.set(-2.7 + (i % 3) * 0.42, 0, 0.6 + Math.floor(i / 3) * 0.45); world.add(b); });
  const lime = mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.4, 16), MAT.liquid(0xf4fbff, 0.5), [TX + 1.5, 0.2, -0.6], { cast: false }); world.add(lime);
  const splint = new THREE.Group(); splint.visible = false; world.add(splint);
  splint.add(mesh(new THREE.BoxGeometry(0.02, 0.02, 0.8), MAT.matte(0xc8a46a), [0, 0, 0.4]));
  const tipMat = new THREE.MeshBasicMaterial({ color: 0xff8a2a, transparent: true, opacity: 0.9 }); const tip = mesh(new THREE.SphereGeometry(0.035, 10, 8), tipMat, [0, 0, 0], { cast: false }); splint.add(tip);

  const st = { g: null, solid: false, ml: 0, pouring: false, bubbling: 0, method: null, jarOn: false, full: 0, early: false, tested: [], done: [] };
  function deliveryTo(end) {
    const a = new THREE.Vector3(FX + 0.06, 1.25, 0); const pts = [a, a.clone().setY(1.55), new THREE.Vector3(FX + 0.6, 1.62, 0), new THREE.Vector3(end.x - 0.25, Math.max(1.0, end.y + 0.6), end.z), new THREE.Vector3(end.x, end.y + 0.35, end.z), end.clone()];
    deliv.geometry.dispose(); deliv.geometry = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 60, 0.016, 8);
  }
  function setJarWater(f) { const h = 1.2 * Math.max(0, 1 - f); jarWater.visible = h > 0.01 && st.method === 'water'; jarWater.scale.y = Math.max(0.001, h); jarWater.position.y = 1.2 - h / 2; }
  function placeJar(method) {
    if (method === 'water') { jar.rotation.x = Math.PI; jar.position.set(TX, 1.42, 0); deliveryTo(new THREE.Vector3(TX - 0.3, 0.12, 0)); plate.visible = false; }
    else if (method === 'up') { jar.rotation.x = 0; jar.position.set(TX, 0.02, 0); deliveryTo(new THREE.Vector3(TX, 0.12, 0)); plate.visible = true; plate.position.set(TX + 0.12, 1.23, 0); }
    else { jar.rotation.x = Math.PI; jar.position.set(TX, 1.85, 0); deliveryTo(new THREE.Vector3(TX, 1.5, 0)); plate.visible = false; }
    setJarWater(st.full);
  }
  function resetFor(g) {
    st.g = g; st.leakSaid = false; st.chargedSaid = false; st.fullSaid = false; st.solid = false; st.ml = 0; st.bubbling = 0; st.method = null; st.jarOn = false; st.full = 0; st.early = false; st.tested = [];
    solid.visible = false; liq.visible = false; jar.position.copy(JAR_HOME); jar.rotation.x = 0; jarWater.visible = false; plate.visible = false; deliveryTo(new THREE.Vector3(TX - 0.3, 0.12, 0)); lime.material = MAT.liquid(0xf4fbff, 0.5);
  }
  const levelY = () => 0.02 + st.ml / 1000 / (Math.PI * 0.4 * 0.4);
  function physics(dt) {
    if (liq.visible) { const h = levelY(); liq.scale.y = h; liq.position.y = h / 2; }
    const covered = levelY() > STEM_TIP + 0.03;
    const reacting = st.solid && st.ml > 5 && GASES[st.g];
    if (reacting) st.bubbling += dt;
    if (reacting && Math.random() < dt * 25) { const p = new THREE.Vector3(FX + (Math.random() - 0.5) * 0.4, BY + 0.08, (Math.random() - 0.5) * 0.4); fx.burst(p, 0xffffff, 1, 0.05, p.y - 0.02); }
    if (reacting && !covered && !st.leakSaid) { st.leakSaid = true; ctx.mistake('The thistle funnel\'s stem is not under the liquid: the gas is escaping up the funnel. Add more liquid so the stem dips below the surface.', 3); }
    if (reacting && covered && st.method && st.bubbling > 0.5) {
      const out = st.method === 'water' ? new THREE.Vector3(TX - 0.3, BY + 0.35, 0) : st.method === 'up' ? new THREE.Vector3(TX, BY + 0.5, 0) : new THREE.Vector3(TX, BY + 1.6, 0);
      if (st.method === 'water' && Math.random() < dt * 14) fx.burst(out, 0xffffff, 1, 0.05, out.y - 0.05);
      if (st.jarOn && st.full < 1) { st.full = Math.min(1, st.full + dt * GASES[st.g].rate / 100 * (st.method === GASES[st.g].method || (st.g === 'H2' && st.method === 'down') ? 1 : st.method === 'water' && st.g === 'CO2' ? 0.4 : 0.6)); setJarWater(st.full); }
    }
  }

  const SHOT = shot({ pos: [-0.3, 2.6, 4.4], target: [-0.3, 0.9, 0], fit: 5.4, fitH: 2.8 });
  const SHOT_FLASK = shot({ pos: [-1.6, 1.8, 2.6], target: [-1.6, 0.8, 0.3], fit: 2.4, fitH: 2.6 });

  function gasSteps(g) {
    const G = GASES[g];
    return [
      {
        title: `${G.name}: charge the generator`, text: `Put the right <b>solid</b> in the flask (tap its jar), then pour the right <b>liquid</b> down the <b>thistle funnel</b> (press and hold the bottle) until the stem's end is <b>under</b> the liquid.`, hint: `${G.eq}.`, shot: SHOT_FLASK, hideBelt: true,
        enter() { resetFor(g); },
        exit() { st.pouring = false; },
        skip() { resetFor(g); st.solid = true; solid.visible = true; solidMat.color.set(g === 'O2' ? 0x262626 : g === 'H2' ? 0x9aa0a6 : 0xf0ede6); st.ml = 120; liq.visible = true; },
        update(dt) { if (st.pouring) { st.ml += 40 * dt; liq.visible = true; if (levelY() > STEM_TIP + 0.05 && !st.chargedSaid) { st.chargedSaid = true; ui.observe(G.f, G.eq); anim.wait(0.8, () => ctx.next('Effervescence in the flask.', 0.6)); } } },
        handler: {
          down(p) {
            for (const [k, b] of Object.entries(solids)) if (hits(ctx, b, p, 45, 0.3)) { if (k !== G.solid) { ctx.mistake(`${k === 'zn' ? 'Zinc' : k === 'mno2' ? 'Manganese dioxide' : 'Marble chips'} will not give ${G.name.toLowerCase()} with these reagents.`, 2); return true; } st.solid = true; solid.visible = true; solidMat.color.set(g === 'O2' ? 0x262626 : g === 'H2' ? 0x9aa0a6 : 0xf0ede6); sfx.play('drop'); return true; }
            for (const [k, b] of Object.entries(liquids)) if (hits(ctx, b, p, 45, 0.3)) { if (!st.solid) { ctx.say('The solid goes in first.', 'hint', 1600); return true; } if (k !== G.liquid) { ctx.mistake(`Not ${k === 'hcl' ? 'dilute HCl' : 'hydrogen peroxide'} for ${G.name.toLowerCase()}.`, 2); return true; } st.pouring = true; st.chargedSaid = false; sfx.play('pour'); return true; }
            return false;
          },
          up() { st.pouring = false; }, cancel() { st.pouring = false; },
        },
      },
      {
        title: `${G.name}: how to collect it`, text: 'Choose the collection method from the gas\'s <b>solubility in water</b> and its <b>density</b> compared with air.', shot: SHOT, hideBelt: true,
        enter() {
          anim.wait(0.5, () => ui.choose(ctx.stage.clientWidth / 2, 40, `Collect ${G.name.toLowerCase()} by…`, [{ label: 'Over water (in an inverted jar)', value: 'water' }, { label: 'Upward delivery (jar upright; displaces air up)', value: 'up' }, { label: 'Downward delivery (jar inverted; displaces air down)', value: 'down' }], (m) => {
            if (m !== G.method) ctx.mistake(g === 'CO2' ? 'CO₂ dissolves noticeably in water and is 1.5 times denser than air: deliver it to the bottom of an upright jar.' : `${G.name} is almost insoluble in water: collect it over water, which also shows when the jar is full.`, 3);
            st.method = G.method; placeJar(st.method); ui.observe(`${G.f} collected`, { water: 'over water', up: 'upward delivery', down: 'downward delivery' }[st.method]); ctx.next(null, 0.6);
          }));
        },
        exit() { ui.clearChooser(); },
        skip() { st.method = G.method; placeJar(st.method); },
      },
      {
        title: `${G.name}: collect a jar`, text: G.method === 'water' ? 'Bubbles come out under the water. Let the first few escape, then tap <b>Collect</b> to put the jar over the tube, and wait until the jar is full of gas.' : 'Let the gas run a moment, then tap <b>Collect</b>. The gas is invisible: when you think the jar is full, test the mouth with a <b>burning splint</b> (Check full).',
        hint: 'The first bubbles are the air that was in the flask.', shot: SHOT, hideBelt: true,
        enter() { st.bubbling = 0; hud.actions([{ id: 'col', label: 'Collect', primary: true, onClick: () => { if (st.jarOn) return; st.jarOn = true; st.early = st.bubbling < 2.5; if (st.early) ctx.mistake('Too soon: the first bubbles are air pushed out of the flask, so the jar now holds air as well.', 2); sfx.play('glass'); hud.enable('col', false); } }, ...(G.method !== 'water' ? [{ id: 'chk', label: 'Check full', onClick: () => { if (st.full > 0.92) { ui.say('The burning splint at the mouth goes out at once: the jar is full of CO₂.', 'good', 2600); ctx.next(null, 0.6); } else ui.say('The splint still burns at the mouth: not full yet.', 'info', 2000); } }] : [])]); },
        exit() { hud.actions([]); },
        skip() { st.jarOn = true; st.full = 1; setJarWater(1); },
        update() { if (G.method === 'water' && st.full >= 1 && !st.fullSaid) { st.fullSaid = true; ctx.next('The jar is full of gas: slide a glass plate under its mouth.', 0.8); } },
      },
      {
        title: `${G.name}: identify it`, text: 'Choose a test for the gas in the jar.', shot: SHOT, hideBelt: true,
        enter() { st.fullSaid = false; ask(); function ask() { ui.choose(ctx.stage.clientWidth / 2, 40, 'Test the gas with…', Object.keys(TESTS).map((t) => ({ label: TESTS[t], value: t })), (t) => { runTest(g, t, () => { if (t === G.test) { ui.observe(`${G.f} test`, testResult(g, t).split(':')[0]); st.done.push(g); ctx.next(`${G.name} confirmed.`, 1.0); } else { ui.say(`${testResult(g, t)} That does not confirm ${G.name.toLowerCase()}; try its own test.`, 'hint', 3600); ctx.bonus(-1); anim.wait(1.2, ask); } }); }); } },
        exit() { ui.clearChooser(); splint.visible = false; },
        skip() { st.done.push(g); },
      },
    ];
  }
  function runTest(g, t, done) {
    const mouth = new THREE.Vector3(TX, st.method === 'up' ? 1.3 : st.method === 'water' ? 1.5 : 1.9, 0);
    if (t === 'lime') { anim.add(1.2, (k) => { lime.material = MAT.liquid(g === 'CO2' ? new THREE.Color(0xf4fbff).lerp(new THREE.Color(0xf2f2f0), k).getHex() : 0xf4fbff, 0.5 + (g === 'CO2' ? 0.45 * k : 0)); }, { done: () => { ui.say(testResult(g, t), 'info', 4000); done(); } }); return; }
    splint.visible = true; tip.scale.setScalar(t === 'glowing' ? 0.6 : 1.4); tipMat.color.set(t === 'glowing' ? 0xd2401a : 0xffa63a);
    const from = new THREE.Vector3(TX + 1.6, 1.4, 0.8); const to = mouth.clone().add(new THREE.Vector3(0.1, 0.02, 0.05));
    splint.lookAt(new THREE.Vector3(-1, 0, -1).add(splint.position));
    anim.add(1.0, (k) => { splint.position.lerpVectors(from, to, k); }, { done: () => {
      const r = testResult(g, t);
      if (t === 'burning' && g === 'H2') { sfx.play('pop'); fx.burst(to.clone().add(new THREE.Vector3(0, BY, 0)), 0x9cc8ff, 10, 0.4, to.y + BY - 0.4); tip.scale.setScalar(0.01); }
      else if (/goes out/.test(r)) tip.scale.setScalar(0.01);
      else if (t === 'glowing' && g === 'O2') { anim.add(0.5, (k) => { tip.scale.setScalar(0.6 + k * 1.4); tipMat.color.set(0xffc04a); }); }
      ui.say(r, 'info', 4200); anim.wait(1.6, () => { splint.visible = false; done(); });
    } });
  }

  const steps = [...gasSteps('H2'), ...gasSteps('O2'), ...gasSteps('CO2')];
  ctx.debug = { st, placeJar };
  return {
    tools: [], steps,
    update(dt) { physics(dt); hud.update(); },
    result() {
      return {
        title: 'Preparation of gases',
        rows: Object.keys(GASES).map((g) => [GASES[g].name, `${GASES[g].eq}; ${{ water: 'over water', up: 'upward delivery' }[GASES[g].method]}; ${TESTS[GASES[g].test].toLowerCase()}`]),
        conclusion: 'The collection method follows from the gas: hydrogen and oxygen hardly dissolve, so they are collected over water (which also shows when the jar is full); carbon dioxide dissolves and is denser than air, so it is delivered to the bottom of an upright jar. MnO₂ only speeds up the decomposition of H₂O₂ and is left unchanged.',
      };
    },
    dispose() { hud.dispose(); },
  };
}
