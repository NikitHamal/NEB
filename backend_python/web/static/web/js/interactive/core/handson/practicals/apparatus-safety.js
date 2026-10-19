// Laboratory apparatus and safety at a real bench. The student picks up (taps) each piece of
// apparatus to learn its name and use, then finds the right one for each job (accurate fixed or
// variable volume, heating, filtering…), lights a Bunsen burner in the safe order (air hole shut,
// flame to the barrel, then the gas; then open the air hole for the blue flame — gas first is
// caught), spots the hazards set out on the bench, and answers how to dilute an acid.
import { THREE } from '../../engine.js';
import { MAT, mesh } from '../../bio-handson/kit.js';
import { tripodWithGauze } from '../../lab3d-kit.js';
import { reagentBottle, washBottle, watchGlass, spiritLamp } from '../../bio-handson/props.js';
import { makeTube } from '../../bio-handson/glassware.js';
import { sfx, noise } from '../../bio-handson/sound.js';
import { createHud, hits } from '../hud.js';
import { beaker, conicalFlask, burette, bulbPipette, funnel } from '../glass.js';
import { bunsen } from '../burner.js';

const BY = 0.8;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });
sfx.register('whoof', () => noise(0.5, { freq: 300, q: 0.7, gain: 0.5, type: 'lowpass', sweep: 0.4 }));
const INFO = {
  beaker: ['Beaker', 'Holding, mixing and heating liquids. Its marks are only approximate.'],
  flask: ['Conical flask', 'Swirling without spilling; the flask in a titration.'],
  burette: ['Burette', 'Delivers an accurately measured variable volume (read to 0.05 mL).'],
  pipette: ['Pipette', 'Delivers one accurate fixed volume (25.0 mL).'],
  tube: ['Test tube', 'Small-scale reactions and tests.'],
  burner: ['Bunsen burner', 'Heating: blue (air open) for heat, yellow (air shut) as a safety flame.'],
  tripod: ['Tripod and gauze', 'Supports a beaker or dish over the burner; the gauze spreads the heat.'],
  funnel: ['Funnel', 'Filtering with a paper cone, or pouring into narrow necks.'],
  wash: ['Wash bottle', 'A jet of distilled water for rinsing and making up to the mark.'],
  watch: ['Watch glass', 'Covering a beaker, weighing or evaporating a few drops.'],
};
const JOBS = [['an accurate, variable volume of liquid (titrant)', 'burette'], ['exactly 25.0 mL of a solution', 'pipette'], ['swirling during a titration', 'flask'], ['separating sand from water', 'funnel'], ['heating 100 mL of water', 'beaker'], ['rinsing the inside of a burette with distilled water', 'wash'], ['evaporating a few drops of solution', 'watch']];

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  world.add(mesh(new THREE.BoxGeometry(7, 0.02, 2.8), MAT.matte(0x2f3640), [0, 0.01, 0]));
  const items = {};
  const put = (k, obj, x, z) => { obj.position.set(x, 0, z); world.add(obj); items[k] = obj; };
  const bk = beaker(80, 0xdbeafe); put('beaker', bk.group, -2.6, 0.5);
  const fl = conicalFlask(); fl.setVolume(60); put('flask', fl.group, -1.9, 0.5);
  const bstand = new THREE.Group(); const bur = burette(); bur.set(0); bur.group.scale.setScalar(0.42); bstand.add(bur.group); bstand.add(mesh(new THREE.BoxGeometry(0.5, 0.04, 0.4), MAT.matte(0x24323a), [0.15, 0.02, 0])); bstand.add(mesh(new THREE.CylinderGeometry(0.02, 0.02, 3, 10), MAT.steel(), [0.3, 1.5, 0])); put('burette', bstand, -1.2, -0.6);
  const pip = bulbPipette(); pip.group.rotation.z = Math.PI / 2; pip.group.position.y = 0.14; const pg = new THREE.Group(); pg.add(pip.group); pip.group.scale.setScalar(0.6); put('pipette', pg, -0.5, 0.9);
  const tube = makeTube('', {}); put('tube', tube.group, -0.15, 0.45); tube.group.rotation.z = 0.0;
  const burner = bunsen(ctx.quality); burner.group.rotation.y = Math.PI / 2; put('burner', burner.group, 0.7, -0.4);
  const tri = tripodWithGauze(); tri.scale.setScalar(0.8); put('tripod', tri, 1.7, -0.4);
  const fun = funnel(); fun.scale.setScalar(1.2); put('funnel', fun, 2.4, 0.6);
  const wb = washBottle(); put('wash', wb, 2.9, -0.3);
  const wg = watchGlass(null); put('watch', wg, 1.6, 0.8);
  const matchbox = mesh(new THREE.BoxGeometry(0.3, 0.08, 0.2), MAT.gloss(0xc0392b), [1.2, 0.04, 0.35]); world.add(matchbox);
  const splint = mesh(new THREE.BoxGeometry(0.4, 0.015, 0.015), MAT.matte(0xc8a46a), null); splint.visible = false; world.add(splint);
  const sflame = mesh(new THREE.SphereGeometry(0.03, 10, 8), new THREE.MeshBasicMaterial({ color: 0xffa63a }), [0.2, 0, 0], { cast: false }); sflame.scale.set(1, 1.8, 1); splint.add(sflame);
  // hazards
  const goggles = new THREE.Group(); goggles.position.set(-2.8, 0.05, -0.6); world.add(goggles);
  [-0.09, 0.09].forEach((x) => goggles.add(mesh(new THREE.TorusGeometry(0.07, 0.018, 8, 20), MAT.plastic(0x0ea5e9), [x, 0.05, 0])));
  goggles.add(mesh(new THREE.TorusGeometry(0.16, 0.008, 6, 24, Math.PI), MAT.plastic(0x111827), [0, 0.05, -0.05]).rotateX(Math.PI / 2));
  const etoh = reagentBottle('Ethanol', 0xf7f7f2, 'FLAMMABLE'); etoh.scale.setScalar(0.9); etoh.position.set(1.05, 0, -0.7); world.add(etoh);
  const lamp = spiritLamp(); lamp.position.set(-0.2, 0, -0.8); lamp.userData.flame.visible = true; world.add(lamp);
  const htube = makeTube(''); htube.setFill(0.25); htube.group.position.set(-0.2, 0.55, -0.8); htube.group.rotation.x = 1.0; world.add(htube.group);
  const spill = mesh(new THREE.CircleGeometry(0.28, 30), MAT.liquid(0xe6f0f8, 0.6), [2.3, 0.022, -0.8], { cast: false }); spill.rotation.x = -Math.PI / 2; spill.scale.set(1, 0.6, 1); world.add(spill);
  const spillTag = reagentBottle('conc. H₂SO₄', 0xf7f3e8, 'corrosive'); spillTag.scale.setScalar(0.7); spillTag.rotation.z = Math.PI / 2; spillTag.position.set(2.65, 0.11, -0.85); world.add(spillTag);
  const HAZ = {
    goggles: { obj: goggles, text: 'Safety goggles lying on the bench: put them on before anything is heated or poured.', fix: () => { anim.add(0.6, (k) => { goggles.position.y = 0.05 + k * 1.5; goggles.scale.setScalar(1 - k); }); } },
    etoh: { obj: etoh, text: 'Ethanol (flammable) right beside the burner: move it well away from flames.', fix: () => { const f = etoh.position.clone(); anim.add(0.8, (k) => { etoh.position.lerpVectors(f, new THREE.Vector3(-3.0, 0, 0.9), k); etoh.position.y = Math.sin(k * Math.PI) * 0.4; }); } },
    tube: { obj: htube.group, text: 'A test tube heated with its mouth pointing at you: it can bump and spit. Point it away from everyone, and heat it gently near the surface.', fix: () => { anim.add(0.6, (k) => { htube.group.rotation.x = 1.0 - 2.0 * k; }); } },
    spill: { obj: spill, text: 'A spill of concentrated acid: neutralise it (sodium hydrogencarbonate), wipe it up and tell the teacher.', fix: () => { anim.add(0.8, (k) => { spill.scale.set(1 - k, 0.6 * (1 - k), 1); }); } },
  };

  const st = { seen: new Set(), q: 0, jobs: JOBS.slice().sort(() => Math.random() - 0.5).slice(0, 5), air: true, gas: false, splint: false, lit: false, blue: false, found: new Set() };
  const SHOT = shot({ pos: [0, 3.0, 4.6], target: [0, 0.4, 0], fit: 6.4, fitH: 2.6 });
  const SHOT_B = shot({ pos: [1.0, 2.0, 2.6], target: [0.8, 0.9, -0.3], fit: 2.0, fitH: 2.4 });
  const keyAt = (p) => Object.keys(items).find((k) => hits(ctx, items[k], p, 40, 0.3));

  function burnerBar() { hud.actions([{ id: 'air', label: 'Air hole: open', onClick: () => { st.air = !st.air; burner.setAir(st.air ? 0.95 : 0); hud.relabel('air', `Air hole: ${st.air ? 'open' : 'shut'}`); sfx.play('knob'); checkBlue(); } }, { id: 'gas', label: 'Gas tap: off', onClick: gasTap }]); }
  function gasTap() {
    st.gas = !st.gas; burner.setGas(st.gas ? 1 : 0); hud.relabel('gas', `Gas tap: ${st.gas ? 'on' : 'off'}`); sfx.play('knob');
    if (!st.gas) { st.lit = false; return; }
    if (st.splint) { burner.light(); st.lit = true; sfx.play('whoosh'); if (st.air) ctx.mistake('Light it with the air hole shut: a burner lit with the air open can strike back down the barrel.', 2); ui.say(st.air ? 'It lit, roaring blue.' : 'A quiet yellow, luminous flame: easy to see.', 'info', 2400); checkBlue(); return; }
    anim.wait(1.4, () => { if (st.gas && !st.lit) { if (st.splint) return; ctx.mistake('Gas first with no flame ready: unburnt gas pours out and lights with a dangerous whoof when the match comes. Have the lighted splint at the barrel BEFORE turning on the gas.', 4); sfx.play('whoof'); st.gas = false; burner.setGas(0); hud.relabel('gas', 'Gas tap: off'); } });
  }
  function checkBlue() { if (st.lit && st.air && !st.blue) { st.blue = true; ui.observe('Bunsen', 'lit safely; blue flame for heating'); anim.wait(1.2, () => ctx.next('Blue, roaring, non-luminous: the hot flame.', 0.8)); } }

  const steps = [
    {
      title: 'Know your apparatus', text: 'Tap each piece of apparatus to pick it up and see what it is called and what it is for. Get to know all ten.', shot: SHOT, hideBelt: true,
      enter() { hud.actions([{ id: 'n', label: '0 / 10', disabled: true, onClick: () => {} }]); },
      exit() { hud.actions([]); },
      skip() { Object.keys(items).forEach((k) => st.seen.add(k)); },
      handler: { down(p) {
        const k = keyAt(p); if (!k) return false; const o = items[k]; const y0 = o.position.y;
        anim.add(0.7, (e) => { o.position.y = y0 + Math.sin(e * Math.PI) * 0.35; }, { id: `lift-${k}` }); sfx.play('pick');
        ui.say(`<b>${INFO[k][0]}</b>: ${INFO[k][1]}`, 'info', 4200); st.seen.add(k); hud.relabel('n', `${st.seen.size} / 10`);
        if (st.seen.size === 10) { ui.observe('Apparatus', 'all ten named'); anim.wait(1.5, () => ctx.next(null, 0.4)); }
        return true;
      } },
    },
    {
      title: 'Find the right apparatus', text: 'Tap the apparatus for each job.', shot: SHOT, hideBelt: true,
      enter() { st.q = 0; ask(); },
      skip() { st.q = st.jobs.length; },
      handler: { down(p) {
        const k = keyAt(p); if (!k || st.q >= st.jobs.length) return false; const [job, want] = st.jobs[st.q];
        if (k !== want) { ctx.mistake(`Not the ${INFO[k][0].toLowerCase()} for ${job}: ${INFO[want][0].toLowerCase()}. ${INFO[want][1]}`, 2); }
        else sfx.play('ok');
        st.q += 1; if (st.q >= st.jobs.length) { ui.observe('Right apparatus', `${st.jobs.length} jobs`); ctx.next(null, 0.6); } else ask();
        return true;
      } },
    },
    {
      title: 'Light the Bunsen burner', text: 'Light it the safe way. Use the buttons for the air hole and the gas tap, and tap the <b>matches</b> to strike a splint and hold it at the top of the barrel. Finish with a blue flame.', hint: 'Air hole shut → lighted splint at the barrel → gas on → open the air hole.', shot: SHOT_B, hideBelt: true,
      enter() { burnerBar(); burner.setAir(0.95); },
      exit() { hud.actions([]); splint.visible = false; },
      skip() { burner.setGas(1); burner.light(); burner.setAir(0.95); st.lit = st.blue = true; },
      handler: { down(p) { if (!hits(ctx, matchbox, p, 50)) return false; st.splint = true; splint.visible = true; splint.position.set(0.5, 1.33, -0.4); sfx.play('whoosh'); ui.say('A lighted splint held at the side of the barrel top.', 'info', 2000); anim.wait(9, () => { st.splint = false; splint.visible = false; }); if (st.gas && !st.lit) { burner.light(); st.lit = true; sfx.play('whoof'); ctx.mistake('The gas was already on: it lit with a whoof. Have the flame ready before the gas.', 3); checkBlue(); } return true; } },
    },
    {
      title: 'Spot the hazards', text: 'Four things on this bench are unsafe. Tap each one to put it right.', shot: SHOT, hideBelt: true,
      enter() { hud.actions([{ id: 'n', label: '0 / 4 found', disabled: true, onClick: () => {} }]); },
      exit() { hud.actions([]); },
      skip() { Object.keys(HAZ).forEach((k) => st.found.add(k)); },
      handler: { down(p) {
        const k = Object.keys(HAZ).find((h) => !st.found.has(h) && hits(ctx, HAZ[h].obj, p, 45, 0.2));
        if (!k) { const it = keyAt(p); if (it) { ctx.say('That one is fine where it is.', 'info', 1400); return true; } return false; }
        st.found.add(k); HAZ[k].fix(); sfx.play('ok'); ui.say(HAZ[k].text, 'good', 4200); ui.observe('Hazard', HAZ[k].text.split(':')[0]); hud.relabel('n', `${st.found.size} / 4 found`);
        if (st.found.size === 4) anim.wait(2, () => ctx.next(null, 0.4));
        return true;
      } },
    },
    {
      title: 'Diluting an acid', text: 'Last question.', shot: SHOT, hideBelt: true,
      enter() { anim.wait(0.5, () => ui.choose(ctx.stage.clientWidth / 2, 40, 'To dilute concentrated sulphuric acid you…', [{ label: 'Add the acid slowly to the water, stirring', value: 1 }, { label: 'Add the water to the acid', value: 2 }, { label: 'Mix them quickly in a measuring cylinder', value: 3 }], (v) => { if (v !== 1) ctx.mistake('Always add acid to water, slowly, with stirring: water added to the acid boils on the surface and spits concentrated acid.', 4); ui.observe('Dilution', 'acid into water, slowly'); ctx.next(null, 0.8); })); },
      exit() { ui.clearChooser(); },
    },
  ];
  function ask() { const [job] = st.jobs[st.q]; ctx.ui.setText(`<b>Question ${st.q + 1} of ${st.jobs.length}.</b> Tap the apparatus you would use for <b>${job}</b>.`); }

  ctx.debug = { st, items, HAZ };
  return {
    tools: [], steps,
    update(dt, t) { burner.update(dt, t); if (splint.visible) sflame.scale.set(1 + Math.sin(t * 30) * 0.1, 1.8, 1); hud.update(); },
    result() {
      return {
        title: 'Apparatus and safety',
        rows: [['Apparatus named', `${st.seen.size} / 10`], ['Jobs matched', `${st.jobs.length}`], ['Burner', st.blue ? 'lit safely, blue flame' : '—'], ['Hazards found', `${st.found.size} / 4`]],
        conclusion: 'Measuring needs volumetric glassware (pipette for a fixed volume, burette for a variable one); beakers and flasks only hold. Light a burner with the air hole shut and the flame ready before the gas; open the air for the hot blue flame. Goggles on, flammables away from flames, tube mouths pointed away, spills cleared at once, and acid always added to water.',
      };
    },
    dispose() { hud.dispose(); },
  };
}
