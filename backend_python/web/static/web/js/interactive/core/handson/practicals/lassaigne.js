// Lassaigne's test on an unknown organic compound. Sodium fusion: a piece of sodium and a little
// compound go into an ignition tube, which the student holds in the flame (press and hold) until
// it glows red (the glow follows the tube's temperature) and keeps it there; plunged red-hot into
// water in a china dish, it shatters, and the boiled, filtered sodium extract is shared between
// three tubes. A short fusion gives a weak extract, and weak tests. Then the tests, in the
// student's own order: FeSO4, boil, FeCl3, acidify (Prussian blue; blood red if S is there too);
// sodium nitroprusside (violet) or lead acetate (black); and boiling with HNO3 before AgNO3, whose
// precipitate colour and solubility in ammonia name the halogen. Skip the boiling and cyanide or
// sulphide give their own silver precipitates.
import { THREE } from '../../engine.js';
import { MAT, mesh } from '../../bio-handson/kit.js';
import { reagentBottle } from '../../bio-handson/props.js';
import { sfx, noise } from '../../bio-handson/sound.js';
import { createHud, hits } from '../hud.js';
import { createTubeBench } from '../tube-bench.js';
import { glowColour } from '../flame.js';
import { steamPuffs } from '../thermo.js';

const BY = 0.8;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });
sfx.register('hiss', () => noise(0.9, { freq: 3500, q: 0.6, gain: 0.12, sweep: 0.4 }));
const COMPOUNDS = [
  { name: 'aniline', el: ['N'] }, { name: 'thiourea', el: ['N', 'S'] }, { name: 'chlorobenzene', el: ['Cl'] }, { name: 'p-bromoaniline', el: ['N', 'Br'] },
  { name: 'sulphanilic acid', el: ['N', 'S'] }, { name: 'p-chloroaniline', el: ['N', 'Cl'] }, { name: 'iodoform', el: ['I'] }, { name: 'thiophene', el: ['S'] }, { name: 'bromobenzene', el: ['Br'] },
];
const REAG = {
  feso4: { short: 'FeSO₄', color: 0xcfe8c6, sub: 'fresh' }, fecl3: { short: 'FeCl₃', color: 0xe6b04a }, hcl: { short: 'conc. HCl', color: 0xf3f7fb }, np: { short: 'Na nitroprusside', tag: 'nitroprusside', color: 0xc9583a },
  pbac: { short: 'Pb acetate', tag: 'lead acetate', color: 0xf3f5f7, sub: '+ AcOH' }, hno3: { short: 'dil. HNO₃', color: 0xf3f7fb }, agno3: { short: 'AgNO₃', color: 0xf3f5f7, amber: true }, nh4oh: { short: 'NH₄OH', color: 0xf2f8ff },
};
const NAMES = { feso4: 'FeSO₄', fecl3: 'FeCl₃', hcl: 'conc. HCl', np: 'sodium nitroprusside', pbac: 'lead acetate', hno3: 'dil. HNO₃', agno3: 'AgNO₃', nh4oh: 'ammonia' };

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const C = COMPOUNDS[Math.floor(Math.random() * COMPOUNDS.length)]; const has = (e) => C.el.includes(e);
  const order = ['feso4', 'fecl3', 'hcl', 'np', 'pbac', 'hno3', 'agno3', 'nh4oh'];
  const bench = createTubeBench(ctx, { hud, reagents: REAG, order, tubes: 3, labels: ['N', 'S', 'X'], burner: true, bottleScale: 0.8, bottlesAt: [-0.35, -0.85], burnerAt: [2.2, -0.45] });

  const fus = new THREE.Group(); world.add(fus);
  const ftube = mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.5, 14, 1, true), MAT.glass(), [0, 0.25, 0], { cast: false }); fus.add(ftube);
  const glowMat = new THREE.MeshStandardMaterial({ color: 0x777777, emissive: 0x000000, emissiveIntensity: 1.6, roughness: 0.5 });
  const charge = mesh(new THREE.SphereGeometry(0.033, 14, 10), glowMat, [0, 0.03, 0]); charge.renderOrder = 12; charge.scale.set(1, 0.8, 1); charge.visible = false; fus.add(charge);
  const tongs = new THREE.Group(); fus.add(tongs);
  [-1, 1].forEach((s) => { const b = mesh(new THREE.BoxGeometry(0.9, 0.02, 0.02), MAT.steel(), [0.47, 0.42, s * 0.03]); b.rotation.z = -0.08; tongs.add(b); });
  const FHOME = new THREE.Vector3(1.3, 0.38, 0.65); fus.position.copy(FHOME);
  const fstand = mesh(new THREE.BoxGeometry(0.2, 0.4, 0.2), MAT.matte(0x30363d), [1.95, 0.2, 0.65]); world.add(fstand);
  const naJar = reagentBottle('Na', 0xe8dfb0, 'in kerosene'); naJar.scale.setScalar(0.8); naJar.position.set(-1.9, 0, 0.75); world.add(naJar);
  const cmp = reagentBottle('X', 0xf1ede2, 'compound'); cmp.scale.setScalar(0.8); cmp.position.set(-1.45, 0, 0.75); world.add(cmp);
  const dishPts = []; for (let i = 0; i <= 12; i++) { const a = i / 12 * 1.1; dishPts.push(new THREE.Vector2(Math.sin(a) * 0.38 + 0.001, (1 - Math.cos(a)) * 0.38)); }
  const dish = new THREE.Group(); dish.position.set(0.2, 0.02, 0.85); world.add(dish);
  dish.add(mesh(new THREE.LatheGeometry(dishPts, 36), new THREE.MeshPhysicalMaterial({ color: 0xf6f4ef, roughness: 0.25, clearcoat: 0.8, side: THREE.DoubleSide })));
  const dwater = mesh(new THREE.CircleGeometry(0.3, 32), MAT.liquid(0xdbe9f3, 0.6), [0, 0.1, 0], { cast: false }); dwater.rotation.x = -Math.PI / 2; dish.add(dwater);
  const shards = new THREE.Group(); shards.visible = false; dish.add(shards);
  for (let i = 0; i < 7; i++) { const s = mesh(new THREE.BoxGeometry(0.06, 0.004, 0.03), MAT.glassEdge(), [(Math.random() - 0.5) * 0.3, 0.1, (Math.random() - 0.5) * 0.3], { cast: false }); s.rotation.y = Math.random() * 3; shards.add(s); }
  const steam = steamPuffs(world, 20);

  const st = { na: false, cmp: false, heating: false, T: 25, hot: 0, fused: false, strength: 0, plunged: false, extract: false, tubes: [[], [], []], boiled: [false, false, false], cur: -1, verdict: null, notes: {} };
  function fusionUpdate(dt) {
    const target = st.heating ? 1050 : 25; st.T += (target - st.T) * (1 - Math.exp(-dt / (st.heating ? 6 : 4)));
    if (st.T > 650 && st.na && st.cmp) st.hot += dt;
    glowColour(st.T, glowMat.emissive);
    if (st.heating && Math.random() < dt * 8) { const p = fus.position.clone(); p.y += 0.1; steam.emit(p, 4, dt, 0.03, 0.4); }
    steam.update(dt);
  }
  const FLAME = () => new THREE.Vector3(bench.flame.group.position.x - 0.03, bench.flame.top + 0.22, bench.flame.group.position.z);
  function toFlame(on) { const from = fus.position.clone(); const to = on ? FLAME() : FHOME; anim.add(0.5, (k) => fus.position.lerpVectors(from, to, k), { id: 'fus' }); const f = FLAME(); ctx.rig.go(on ? shot({ pos: [f.x - 0.25, f.y + 0.15, f.z + 1.3], target: [f.x, f.y + 0.05, f.z], fit: 0.9, fitH: 0.8 }) : SHOT_F, 0.6); }

  const SHOT_F = shot({ pos: [1.0, 1.9, 3.4], target: [1.2, 0.9, 0.1], fit: 3.4, fitH: 2.8 });
  const SHOT_T = shot({ pos: [0.4, 3.0, 3.0], target: [0.4, 0.35, -0.2], fit: 4.6, fitH: 2.4 });
  const SHOT_TUBE = shot({ pos: [1.5, 1.45, 2.1], target: [1.2, 0.6, 0.2], fit: 1.9, fitH: 1.6 });

  // ---- the extract tests ----
  function reactExtract(i, k) {
    const added = st.tubes[i]; const w = st.strength; const weak = w < 0.5;
    const seen = (r) => added.includes(r); added.push(k);
    if (k === 'feso4') return { look: { color: 0xa9b98a, opacity: 0.6, ppt: { color: 0x58663e, amount: 0.5 } }, text: 'A dirty green precipitate of Fe(OH)₂ (the extract is alkaline).' };
    if (k === 'fecl3') {
      if (!seen('feso4')) return { look: { color: has('N') && has('S') && !weak ? 0x9b1b1b : 0xd7b56a, opacity: 0.6 }, text: has('N') && has('S') && !weak ? 'A blood-red colour: thiocyanate, Fe(SCN)²⁺ — both N and S are present.' : 'A yellow-brown colour.' };
      if (has('N') && has('S') && !weak) return { look: { color: 0x8a1c1c, opacity: 0.75 }, text: 'A blood-red colour (thiocyanate): N and S together.' };
      return { look: { color: 0x7a6a3a, opacity: 0.7 }, text: 'The precipitate darkens to a brownish mass. Acidify to see what colour lies under it.' };
    }
    if (k === 'hcl') {
      if (seen('feso4') && !st.boiled[i]) return { look: { color: 0xd6c48a, opacity: 0.6, ppt: null }, text: 'The precipitate dissolves, but you acidified before boiling with FeSO₄: the cyanide was never turned into ferrocyanide.', mistake: 'Boil the extract with FeSO₄ before acidifying. Acid on unreacted cyanide releases poisonous HCN.' };
      if (seen('feso4') && st.boiled[i] && seen('fecl3')) {
        if (has('N') && !weak && !has('S')) return { look: { color: 0x123d9c, opacity: 0.85, ppt: { color: 0x0b2f86, amount: 0.6 } }, text: 'Prussian blue! A deep blue precipitate of Fe₄[Fe(CN)₆]₃: nitrogen is present.' };
        if (has('N') && has('S') && !weak) return { look: { color: 0x8a1c1c, opacity: 0.75, ppt: null }, text: 'A blood-red solution remains: thiocyanate, so nitrogen (with sulphur) is present.' };
        if (has('N') && weak) return { look: { color: 0x5d7a8a, opacity: 0.6, ppt: null }, text: 'Only a faint greenish-blue tinge… doubtful. Was the fusion complete?' };
        return { look: { color: 0xd7c27a, opacity: 0.55, ppt: null }, text: 'A clear yellow solution, no blue: no nitrogen.' };
      }
      return { look: {}, text: 'No visible change.' };
    }
    if (k === 'np') return has('S') && !weak ? { look: { color: 0x5a1f7a, opacity: 0.85 }, text: 'A deep violet colour that slowly fades: sulphide, so sulphur is present.' } : { look: { color: 0xd57a5a, opacity: 0.45 }, text: 'Only the pale red-brown of the reagent: no violet.' };
    if (k === 'pbac') return has('S') && !weak ? { look: { color: 0x2b2b2b, opacity: 0.8, ppt: { color: 0x111111, amount: 0.8 } }, text: 'A black precipitate of PbS: sulphur is present.' } : { look: { color: 0xf3f5f7 }, text: 'No black precipitate.' };
    if (k === 'hno3') return { look: { color: 0xf3f6f8 }, text: 'Acidified with dilute nitric acid. Boil it to drive off any HCN or H₂S before adding AgNO₃.' };
    if (k === 'agno3') {
      const acid = seen('hno3'); const clean = acid && st.boiled[i];
      if (!clean && (has('N') || has('S')) && !weak) return { look: { color: has('S') ? 0x2a2a2a : 0xf4f4f4, opacity: 0.85, ppt: { color: has('S') ? 0x1a1a1a : 0xfafafa, amount: 0.8 } }, text: has('S') ? 'A black precipitate (Ag₂S) — the sulphide was not boiled off.' : 'A white precipitate — but it could be AgCN: the cyanide was not boiled off with HNO₃.', trap: true };
      const hal = ['Cl', 'Br', 'I'].find(has);
      if (!hal || weak) return { look: {}, text: 'No precipitate: no halogen.' };
      const L = { Cl: [0xfafafa, 'A curdy white precipitate (AgCl).'], Br: [0xf2edc0, 'A pale yellow precipitate (AgBr).'], I: [0xf2d65a, 'A yellow precipitate (AgI).'] }[hal];
      return { look: { color: L[0], opacity: 0.85, ppt: { color: L[0], amount: 0.9 } }, text: L[1] };
    }
    if (k === 'nh4oh') {
      const hal = ['Cl', 'Br', 'I'].find(has);
      if (!seen('agno3')) return { look: {}, text: 'No visible change.' };
      if (hal === 'Cl') return { look: { color: 0xf3f6f8, opacity: 0.5, ppt: null }, text: 'The white precipitate dissolves readily in ammonia: chloride.' };
      if (hal === 'Br') return { look: { color: 0xf3f1d8, opacity: 0.6 }, text: 'The pale yellow precipitate dissolves only partly (sparingly): bromide.' };
      if (hal === 'I') return { look: {}, text: 'The yellow precipitate does not dissolve: iodide.' };
      return { look: {}, text: 'No change.' };
    }
    return { look: {}, text: '' };
  }
  function testBar() {
    hud.actions([
      { id: 't0', label: 'Tube N', onClick: () => pickTube(0) }, { id: 't1', label: 'Tube S', onClick: () => pickTube(1) }, { id: 't2', label: 'Tube X', onClick: () => pickTube(2) },
      { id: 'boil', label: 'Boil', disabled: st.cur < 0, onClick: boil },
      { id: 'done', label: 'Conclude', primary: true, onClick: () => { hud.actions([]); if (bench.tube) bench.putBack(); ctx.next(); } },
    ]);
  }
  function pickTube(i) { if (bench.busy) return; if (bench.tube) bench.putBack(); st.cur = i; anim.wait(0.5, () => { bench.bring(i, true); ctx.rig.go(SHOT_TUBE, 0.9); }); testBar(); }
  function boil() { if (st.cur < 0 || bench.busy) return; const i = st.cur; bench.heat(2.5, () => { st.boiled[i] = true; const t = st.tubes[i]; const msg = t.includes('feso4') ? 'Boiled with FeSO₄: cyanide → ferrocyanide.' : t.includes('hno3') ? 'Boiled with nitric acid: HCN and H₂S are driven off.' : 'Boiled.'; ui.say(msg, 'info', 2400); ctx.rig.go(SHOT_TUBE, 0.6); }); ctx.rig.go(SHOT_T, 0.8); }

  const steps = [
    {
      title: 'Charge the fusion tube', text: 'Tap the <b>sodium</b> jar for a pea-sized piece (cut, pressed dry on filter paper), then tap the <b>compound</b> to add a little of it to the ignition tube.', hint: 'Sodium first. Never touch sodium with wet hands, and keep it away from water until the end.', shot: SHOT_F, hideBelt: true,
      skip() { st.na = st.cmp = true; charge.visible = true; },
      handler: { down(p) {
        if (hits(ctx, naJar, p, 50, 0.3)) { if (st.na) return true; st.na = true; charge.visible = true; sfx.play('place'); ui.say('A piece of sodium, cut and pressed dry, drops into the tube.', 'info', 2200); return true; }
        if (hits(ctx, cmp, p, 50, 0.3)) { if (!st.na) { ctx.say('Sodium first, then the compound.', 'hint', 1800); return true; } st.cmp = true; glowMat.color.set(0x8a8478); sfx.play('drip'); ui.observe('Compound', 'unknown X'); ctx.next('Charged.', 0.6); return true; }
        return false;
      } },
    },
    {
      title: 'Fuse to red heat', text: 'Press and <b>hold</b> on the <b>burner</b> to hold the tube in the flame: gently at first, then strongly until the bottom <b>glows red</b>. Keep it red-hot for a while, then tap the <b>china dish</b> to plunge it into the water.', hint: 'Incomplete fusion is the commonest cause of false negatives: keep it glowing red for several seconds.', shot: SHOT_F, hideBelt: true,
      enter() { if (!bench.flame.lit) { bench.flame.setGas(1); bench.flame.light(); } },
      skip() { st.hot = 6; st.T = 900; },
      update(dt) { if (st.heating && st.T > 650 && !st.saidRed) { st.saidRed = true; ui.say('The bottom of the tube glows red.', 'info', 2000); } },
      handler: {
        down(p) {
          if (hits(ctx, dish, p, 70, 0.1)) { plunge(); return true; }
          if (hits(ctx, bench.flame.group, p, 80, 0.9) || hits(ctx, fus, p, 60, 0.2)) { st.heating = true; toFlame(true); return true; }
          return false;
        },
        up() { if (st.heating) { st.heating = false; toFlame(false); } }, cancel() { if (st.heating) { st.heating = false; toFlame(false); } },
      },
    },
    {
      title: 'Boil and filter', text: 'The broken tube and its contents are boiled with the water for a few minutes and filtered: the clear filtrate is the <b>sodium extract</b>, shared between three tubes.', shot: SHOT_T, hideBelt: true,
      enter() { anim.wait(1.0, () => { bench.tubes.forEach((t) => t.to(anim, { fill: 0.22, color: st.strength < 0.5 ? 0xf3f3f0 : 0xf4f2e6, dur: 1.2, opacity: 0.5 })); st.extract = true; ui.observe('Sodium extract', st.strength < 0.5 ? 'clear, colourless' : 'clear, faintly yellow'); ctx.next(null, 1.2); }); },
      skip() { bench.tubes.forEach((t) => { t.setFill(0.22); }); },
    },
    {
      title: 'Test the extract', text: 'Choose a tube (N, S or X) and tap reagents in the order you think right; <b>Boil</b> heats the tube in the flame. N: FeSO₄, boil, FeCl₃, then conc. HCl. S: sodium nitroprusside (or lead acetate). X: dil. HNO₃, boil, then AgNO₃ (and ammonia).', hint: 'Order matters: boil with FeSO₄ before acidifying; boil with HNO₃ before AgNO₃ if N or S might be present.', shot: SHOT_T, hideBelt: true,
      enter() { testBar(); },
      exit() { hud.actions([]); },
      skip() { st.notes = { N: has('N') ? 'positive' : 'negative', S: has('S') ? 'positive' : 'negative', X: ['Cl', 'Br', 'I'].find(has) || 'none' }; },
      handler: { down(p) {
        if (bench.busy) return true;
        const k = bench.bottleAt(p, order); if (!k) return false;
        if (st.cur < 0) { ctx.say('Choose a tube first (Tube N, S or X).', 'hint', 1800); return true; }
        const i = st.cur;
        bench.pour(k, 3, () => {
          const r = reactExtract(i, k); bench.look(r.look); ui.say(`<b>Tube ${'NSX'[i]} + ${NAMES[k]}</b>: ${r.text}`, 'info', 4800);
          ui.observe(`${'NSX'[i]}: + ${NAMES[k]}`, r.text.length > 54 ? `${r.text.slice(0, 52)}…` : r.text);
          if (r.mistake) ctx.mistake(r.mistake, 3);
          if (r.trap) ctx.say('Careful: is that precipitate really a silver halide?', 'hint', 3000);
          if (r.trap) st.trapped = true;
        });
        return true;
      } },
    },
    {
      title: 'Which elements?', text: 'From your observations, which elements does compound X contain?', shot: SHOT_T, hideBelt: true,
      enter() {
        const ask = () => ui.chooseMany(ctx.stage.clientWidth / 2, 40, 'Compound X contains…', ['N', 'S', 'Cl', 'Br', 'I'].map((e) => ({ label: { N: 'Nitrogen', S: 'Sulphur', Cl: 'Chlorine', Br: 'Bromine', I: 'Iodine' }[e], value: e })), (v) => {
          const right = v.length === C.el.length && v.every(has);
          if (!right) { ctx.mistake(`Not quite. Check each test again: ${st.strength < 0.5 ? 'and remember your fusion was short, so weak tests are not reliable negatives. ' : ''}a precipitate with AgNO₃ is only a halogen if the extract was boiled with HNO₃ first.`, 4); anim.wait(0.5, ask); return; }
          st.verdict = v; ui.observe('Elements', `<b>${C.el.join(', ')}</b>`); ctx.next(`Compound X is ${C.name}.`, 1.4);
        });
        anim.wait(0.6, ask);
      },
      exit() { ui.clearChooser(); },
    },
  ];
  function plunge() {
    if (!st.na || st.plunged) return;
    if (st.T < 600) { ctx.mistake('The tube must be red-hot when it goes into the water, or the fusion is incomplete and the sodium has not finished reacting.', 3); return; }
    st.plunged = true; st.strength = Math.min(1, st.hot / 4);
    if (st.strength < 0.5) ctx.mistake(`The tube was red-hot for only ${st.hot.toFixed(1)} s: fusion is incomplete, so the extract will be weak.`, 3);
    const from = fus.position.clone(); const to = new THREE.Vector3(dish.position.x - 0.1, 0.2, dish.position.z);
    anim.add(0.6, (k) => { fus.position.lerpVectors(from, to, k); }, { done: () => { sfx.play('hiss'); sfx.play('glass'); ftube.visible = false; charge.visible = false; shards.visible = true; dwater.material = MAT.liquid(0xd9d2bd, 0.7); const p = dish.position.clone(); p.y += 0.15; for (let i = 0; i < 20; i++) steam.emit(p, 60, 0.05, 0.2, 0.5); ui.observe('Fusion', `red-hot ${st.hot.toFixed(1)} s`); ctx.next('It cracks with a hiss: the excess sodium is destroyed and the salts dissolve.', 1.2); } });
  }

  ctx.debug = { st, C, bench, reactExtract, toFlame, dish };
  return {
    tools: [], steps,
    update(dt, t) { fusionUpdate(dt); bench.update(dt, t); hud.update(); },
    result() {
      return {
        title: "Lassaigne's test",
        rows: [['Compound X', C.name], ['Contains', C.el.join(', ')], ['Fusion (red-hot)', `${st.hot.toFixed(1)} s`], ['Extract', st.strength < 0.5 ? 'weak' : 'good']],
        conclusion: 'Fusion with sodium turns covalently bound N, S and halogens into NaCN, Na₂S (or NaSCN) and NaX, which ionic tests can see: Prussian blue for cyanide, violet nitroprusside for sulphide, and silver halides — but only after boiling with nitric acid, or AgCN and Ag₂S masquerade as halides.',
      };
    },
    dispose() { hud.dispose(); bench.dispose(); steam.dispose(); },
  };
}
