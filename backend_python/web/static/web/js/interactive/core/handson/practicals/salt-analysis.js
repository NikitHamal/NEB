// Full systematic analysis of an unknown simple salt: look at it, heat a little dry in a tube and
// do a flame test; test for NH₄⁺ with NaOH and warming; run the group reagents on the salt solution
// in order (dil. HCl, H₂S, NH₄Cl + NH₄OH, H₂S again, (NH₄)₂CO₃) until a precipitate names the group,
// with every real trap of doing it out of order (salt-chem.js); confirm the cation; then the anion
// tests (wet-tests.js); then the salt. Every observation comes from what is actually in the tube.
import { THREE } from '../../engine.js';
import { MAT, mesh } from '../../bio-handson/kit.js';
import { watchGlass } from '../../bio-handson/props.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud } from '../hud.js';
import { createTubeBench } from '../tube-bench.js';
import { emissionColour } from '../flame.js';
import { SALTS, CATIONS, CREAG, RNAME, createCationTube } from '../salt-chem.js';
import { ANIONS, REAGENTS, createTubeChem } from '../wet-tests.js';

const BY = 0.8;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });
const GROUP_KEYS = ['soln', 'hcl', 'h2s', 'nh4cl', 'nh4oh', 'nh42co3'];
const CONF_KEYS = ['soln', 'naoh', 'nh4oh', 'ki', 'k4fe', 'kcns', 'c2o4', 'hpo4', 'nessler'];
const AN_KEYS = ['soln', 'hno3', 'agno3', 'nh4oh', 'hcl', 'bacl2', 'feso4', 'h2so4'];

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const salt = SALTS[Math.floor(Math.random() * SALTS.length)]; const cat = salt.cat; const C = CATIONS[cat];
  const reagents = Object.assign({}, REAGENTS, CREAG);
  const order = [...new Set([...GROUP_KEYS, ...CONF_KEYS, ...AN_KEYS])];
  const bench = createTubeBench(ctx, { hud, reagents, order, tubes: 4, labels: ['dry', 'NH₄⁺', 'group', 'test'], burner: true, bottleScale: 0.72, cols: 5, bottlesAt: [-0.45, -0.95], burnerAt: [2.2, -0.5] });
  const wg = watchGlass(null); wg.position.set(-1.9, 0.02, 0.75); world.add(wg);
  const solidCol = cat === 'Cu' ? 0x3d7fd6 : cat === 'Fe' ? 0xb8742a : 0xf5f5ef;
  const heap = mesh(new THREE.SphereGeometry(0.12, 16, 8, 0, Math.PI * 2, 0, Math.PI / 2), MAT.matte(solidCol), [0, 0.02, 0]); heap.scale.set(1, 0.45, 1); wg.add(heap);
  const st = { chem: null, kind: null, dry: false, flame: false, flameT: 0, nh3: false, group: null, cation: null, anion: null };
  const col = new THREE.Color();

  const SHOT = shot({ pos: [0.3, 3.2, 3.2], target: [0.3, 0.3, -0.25], fit: 4.6, fitH: 2.6 });
  const SHOT_TUBE = shot({ pos: [1.5, 1.45, 2.1], target: [1.2, 0.6, 0.2], fit: 1.9, fitH: 1.6 });

  function newTube(i, kind) {
    if (bench.tube) bench.putBack();
    st.kind = kind; st.chem = kind === 'anion' ? createTubeChem(salt.an) : createCationTube(cat);
    anim.wait(0.5, () => bench.bring(i));
  }
  function apply(k, how) {
    if (!bench.tube || bench.busy) return;
    bench.pour(k, k === 'soln' ? 4 : 3, () => {
      let text; let look = {};
      if (st.kind === 'anion') {
        const s = st.chem.state; const before = s.ppt; text = st.chem.apply(k, how);
        look = { color: s.color, opacity: 0.45 + s.cloudy * 0.5, fill: k === 'soln' ? 0.2 : undefined };
        if (s.ppt && s.ppt !== before) look.ppt = { color: s.color, amount: s.pptAmount }; if (!s.ppt && before) look.ppt = null;
        if (s.gas && (k === 'hcl' || k === 'hno3')) look.fizz = 2.5; if (s.layered) look.layer = 0xf3eee0; if (s.ring) look.ring = 0x5b3214;
      } else { const r = st.chem.apply(k); text = r.text; look = r.look; }
      bench.look(look); ui.say(`<b>+ ${RNAME[k] || reagents[k].name || k}</b>: ${text}`, 'info', 4800); ctx.rig.go(SHOT_TUBE, 0.8);
      if (ctx.step && ctx.step.onAdd) ctx.step.onAdd(k, text);
    });
  }
  function reagentHandler(keys) {
    return { down(p) {
      if (bench.busy) return true;
      const k = bench.bottleAt(p, keys); if (!k) return false;
      if (!bench.tube) { ctx.say('Take a clean tube first.', 'hint', 1600); return true; }
      if (k === 'h2so4' && st.kind === 'anion') {
        ui.choose(p.x, p.y, 'Concentrated H₂SO₄: how do you add it?', [{ label: 'Tilt the tube, run it slowly down the side', value: 'side' }, { label: 'Pour it straight in', value: 'straight' }], (how) => { if (how === 'straight') ctx.mistake('Run concentrated acid slowly down the side so it sinks under the solution; poured in, it spits and mixes.', 3); apply(k, how); });
        return true;
      }
      apply(k); return true;
    } };
  }

  const steps = [
    {
      title: 'Preliminary tests', text: `Look at the salt on the watch glass. Then <b>heat a little dry</b> in a tube, and do a <b>flame test</b>.`, hint: 'Colour, dry heating and the flame cost nothing and narrow the possibilities.', shot: SHOT, hideBelt: true,
      enter() { bench.showOnly([]); ui.observe('Appearance', salt.look); bar0(); },
      exit() { hud.actions([]); bench.showTags(false); },
      skip() { ui.observe('Dry heating', salt.dry); ui.observe('Flame', C.flameText); },
    },
    {
      title: 'Zero group: ammonium', text: 'In a clean tube: <b>salt solution</b>, then <b>NaOH</b>; then <b>warm</b> it and test the vapour with moist red litmus.', hint: 'NH₄⁺ + OH⁻ → NH₃ + H₂O on warming. Ammonia turns red litmus blue.', shot: SHOT, hideBelt: true,
      enter() { bench.showOnly(['soln', 'naoh']); newTube(1, 'cation'); hud.actions([{ id: 'warm', label: 'Warm + litmus', onClick: () => { if (!st.chem.state.added.includes('naoh')) { ctx.say('Add the solution and NaOH first.', 'hint', 1800); return; } bench.heat(2.5, () => { const r = st.chem.warm(); st.nh3 = !!st.chem.state.gas; ui.say(r.text, 'info', 4200); ui.observe('NaOH, warm', st.nh3 ? 'NH₃ smell, litmus blue' : 'no NH₃'); hud.enable('next', true); }); } }, { id: 'next', label: 'Next', primary: true, disabled: true, onClick: () => { hud.actions([]); ctx.next(null, 0.3); } }]); },
      exit() { hud.actions([]); },
      skip() { st.nh3 = cat === 'NH4'; },
      handler: reagentHandler(['soln', 'naoh']),
    },
    {
      title: 'Group analysis', text: 'To the <b>salt solution</b> add the group reagents <b>in order</b>: dil. HCl (I); H₂S in that acid solution (II); then NH₄Cl and NH₄OH (III); H₂S again in the ammoniacal solution (IV); (NH₄)₂CO₃ (V). Stop at the first group that gives a precipitate.', hint: 'The order and the medium matter: H₂S without acid also precipitates zinc; NH₄OH without NH₄Cl also precipitates magnesium.', shot: SHOT, hideBelt: true,
      enter() { bench.showOnly(GROUP_KEYS); newTube(2, 'cation'); hud.actions([{ id: 'ppt', label: 'Precipitate: which group?', primary: true, onClick: askGroup }, { id: 'none', label: 'No precipitate at all', onClick: () => claimGroup('VI') }, { id: 'new', label: 'New tube', onClick: () => newTube(2, 'cation') }]); },
      exit() { hud.actions([]); ui.clearChooser(); },
      skip() { st.group = C.group === '0' ? 'VI' : C.group; },
      handler: reagentHandler(GROUP_KEYS),
    },
    {
      title: 'Confirm the cation', text: 'Take fresh salt solution in a clean tube and run the confirmatory test(s) for the cation you suspect; use <b>New tube</b> for each test. Then name it.', hint: 'Pb²⁺: KI (yellow). Cu²⁺: K₄[Fe(CN)₆] (chocolate brown), NH₄OH (deep blue). Fe³⁺: K₄[Fe(CN)₆] (Prussian blue), KCNS (blood red). Zn²⁺: NaOH (white, soluble in excess). Ca²⁺: ammonium oxalate. Mg²⁺: Na₂HPO₄. NH₄⁺: Nessler (brown).', shot: SHOT, hideBelt: true,
      enter() { bench.showOnly(CONF_KEYS); newTube(3, 'cation'); hud.actions([{ id: 'new', label: 'New tube', onClick: () => newTube(3, 'cation') }, { id: 'name', label: 'Name the cation', primary: true, onClick: () => askIon('cation') }]); },
      exit() { hud.actions([]); ui.clearChooser(); },
      skip() { st.cation = cat; },
      handler: reagentHandler(CONF_KEYS),
    },
    {
      title: 'Test for the anion', text: 'Salt solution in a clean tube each time: acidify with <b>dil. HNO₃</b> then <b>AgNO₃</b> (Cl⁻); acidify with <b>dil. HCl</b> then <b>BaCl₂</b> (SO₄²⁻); <b>FeSO₄</b> then conc. <b>H₂SO₄</b> down the side (NO₃⁻, brown ring).', hint: 'Acidify before AgNO₃ and BaCl₂, or carbonate gives false precipitates.', shot: SHOT, hideBelt: true,
      enter() { bench.showOnly(AN_KEYS); newTube(3, 'anion'); hud.actions([{ id: 'new', label: 'New tube', onClick: () => newTube(3, 'anion') }, { id: 'name', label: 'Name the anion', primary: true, onClick: () => askIon('anion') }]); },
      exit() { hud.actions([]); ui.clearChooser(); },
      skip() { st.anion = salt.an; },
      handler: reagentHandler(AN_KEYS),
    },
    {
      title: 'The salt', text: 'Put the cation and the anion together.', shot: SHOT, hideBelt: true,
      enter() {
        if (bench.tube) bench.putBack(); bench.showOnly([]);
        const ask = () => ui.choose(ctx.stage.clientWidth / 2, 40, 'The salt is…', SALTS.map((x) => ({ label: x.f, value: x.f })), (v) => {
          if (v !== salt.f) { ctx.mistake(`Not ${v}. Your tests showed ${C.ion} and ${ANIONS[salt.an].ion}.`, 3); anim.wait(0.4, ask); return; }
          ui.observe('Salt', `<b>${salt.f}</b>`); ctx.next(`${salt.f}.`, 1.2);
        });
        anim.wait(0.6, ask);
      },
      exit() { ui.clearChooser(); },
    },
  ];
  function bar0() {
    hud.actions([
      { id: 'dry', label: 'Dry heat', onClick: () => { if (st.dry || bench.busy) return; newTube(0, 'cation'); anim.wait(1.4, () => { bench.look({ fill: 0.05, color: solidCol, opacity: 0.9, dur: 0.4 }); bench.heat(3, () => { st.dry = true; ui.say(salt.dry, 'info', 4600); ui.observe('Dry heating', salt.dry); if (cat === 'Cu') bench.look({ color: 0xf2f2ee, dur: 2 }); check0(); }); }); } },
      { id: 'flame', label: 'Flame test', onClick: () => { if (st.flame) return; const fl = bench.flame; if (!fl.lit) { fl.setGas(1); fl.light(); } ctx.rig.go(shot({ pos: [2.0, 2.3, 2.0], target: [2.2, 1.6, -0.5], fit: 1.6, fitH: 1.6 }), 0.8); st.flameT = 4; sfx.play('whoosh'); anim.wait(1.6, () => { st.flame = true; ui.say(`Flame test: ${C.flameText}`, 'info', 4200); ui.observe('Flame', C.flameText); check0(); }); } },
      { id: 'next', label: 'Next', primary: true, disabled: true, onClick: () => { hud.actions([]); if (bench.tube) bench.putBack(); ctx.next(null, 0.3); } },
    ]);
  }
  function check0() { if (st.dry && st.flame) hud.enable('next', true); }
  function askGroup() {
    if (!st.chem || !st.chem.state.ppt) { ctx.say('There is no precipitate in the tube yet.', 'hint', 1800); return; }
    ui.choose(ctx.stage.clientWidth / 2, 40, 'The precipitate places the cation in group…', ['I', 'II', 'III', 'IV', 'V'].map((g) => ({ label: `Group ${g}`, value: g })), claimGroup);
  }
  function claimGroup(g) {
    const truth = C.group === '0' ? 'VI' : C.group;
    if (g !== truth) {
      const added = st.chem ? st.chem.state.added : [];
      const why = g === 'VI' ? 'A precipitate did form with one of the group reagents.' : (!added.includes('hcl') && added.includes('h2s')) ? 'The H₂S went into a solution that had not been acidified, so a later group came down early.' : (added.includes('nh4oh') && !added.includes('nh4cl')) ? 'NH₄OH without NH₄Cl lets a later group precipitate early.' : 'Look at which reagent first gave the precipitate.';
      ctx.mistake(`Not Group ${g}. ${why} Start a new tube and follow the order.`, 4); return;
    }
    st.group = g; ui.observe('Group', `<b>${g === 'VI' ? 'VI (or zero)' : g}</b>`); hud.actions([]); ctx.next(`Group ${g === 'VI' ? 'VI' : g}.`, 0.8);
  }
  function askIon(kind) {
    const opts = kind === 'cation' ? Object.keys(CATIONS).map((k) => ({ label: `${CATIONS[k].ion}  ${CATIONS[k].name}`, value: k })) : ['chloride', 'sulfate', 'nitrate'].map((k) => ({ label: `${ANIONS[k].ion}  ${ANIONS[k].name}`, value: k }));
    ui.choose(ctx.stage.clientWidth / 2, 40, kind === 'cation' ? 'The cation is…' : 'The anion is…', opts, (v) => {
      const truth = kind === 'cation' ? cat : salt.an;
      if (v !== truth) { ctx.mistake(kind === 'cation' ? `Not ${CATIONS[v].ion}. Which confirmatory test gave its characteristic result?` : `Not ${ANIONS[v].ion}. Which test gave a positive result after acidifying?`, 4); return; }
      st[kind] = v; ui.observe(kind === 'cation' ? 'Cation' : 'Anion', `<b>${kind === 'cation' ? C.ion : ANIONS[v].ion}</b>`); hud.actions([]); ctx.next(null, 0.6);
    });
  }

  ctx.debug = { st, salt, bench, apply, newTube };
  return {
    tools: [], steps,
    update(dt, t) {
      if (st.flameT > 0) { st.flameT -= dt; const k = C.flame ? emissionColour(C.flame, col) : 0; bench.flame.setEmission(col, st.flameT > 0 && k ? Math.min(1, st.flameT) * 0.85 : 0); }
      bench.update(dt, t); hud.update();
    },
    result() {
      return {
        title: `Salt: ${salt.f}`,
        rows: [['Appearance', salt.look], ['Flame', C.flameText], ['Ammonium test', cat === 'NH4' ? 'positive' : 'negative'], ['Group', C.group === '0' ? 'zero' : C.group], ['Cation', `${C.ion} (${C.name})`], ['Anion', `${ANIONS[salt.an].ion} (${ANIONS[salt.an].name})`]],
        conclusion: `The salt is ${salt.f}. Each group reagent removes one group and leaves the next in solution, so the first group to precipitate names the cation's group; the confirmatory test then names the ion. Skipping the acid before H₂S, or the NH₄Cl before NH₄OH, drags later cations into earlier groups.`,
      };
    },
    dispose() { hud.dispose(); bench.dispose(); },
  };
}
