// Functional group tests on four unlabelled organic liquids (an alcohol, an aldehyde, a
// carboxylic acid and phenol), in any order the student likes: a little of a sample in a clean
// tube, a reagent from the shelf, and a warm water bath where the test needs heat. Tollens' and
// Fehling's do nothing in the cold; the ester test needs warming and is positive for both the
// alcohol and the acid; bromine water is decolourised slowly by the aldehyde but with a white
// precipitate only by phenol. The student names each sample from the pattern of results.
import { createHud } from '../hud.js';
import { createTubeBench } from '../tube-bench.js';

const BY = 0.8;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });
const GROUPS = { alcohol: 'Alcohol (–OH)', aldehyde: 'Aldehyde (–CHO)', acid: 'Carboxylic acid (–COOH)', phenol: 'Phenol (Ar–OH)' };
const REAG = {
  A: { short: 'A', color: 0xf5f8fb, sub: 'unknown' }, B: { short: 'B', color: 0xf5f8fb, sub: 'unknown' }, C: { short: 'C', color: 0xf5f8fb, sub: 'unknown' }, D: { short: 'D', color: 0xf8f4ea, sub: 'unknown' },
  na: { short: 'Na', color: 0xd9d4b8, sub: 'under oil' }, nahco3: { short: 'NaHCO₃', color: 0xf1f6fa, sub: 'sat.' }, fecl3: { short: 'FeCl₃', color: 0xe6b04a, sub: 'neutral' }, br2: { short: 'Br₂ water', color: 0xe0902a },
  tollens: { short: 'Tollens', color: 0xf1f5f9, amber: true }, fehling: { short: 'Fehling', color: 0x1e5bb8, sub: 'A + B' }, dnp: { short: '2,4-DNP', color: 0xf0a030 }, ester: { short: 'EtOH/AcOH', color: 0xf6f3e8, sub: '+ conc. H₂SO₄' },
};
const NAMES = { na: 'sodium', nahco3: 'NaHCO₃', fecl3: 'neutral FeCl₃', br2: 'bromine water', tollens: 'Tollens\' reagent', fehling: 'Fehling\'s solution', dnp: '2,4-DNP', ester: 'ester test' };
const WARM = new Set(['tollens', 'fehling', 'ester']);

/** What a reagent does to a compound (warmed or not): the look of the tube and what is seen. */
function react(comp, r, warm) {
  switch (r) {
    case 'na': return comp === 'aldehyde' ? { look: {}, text: 'The sodium sits there: no effervescence.' } : { look: { fizz: 3 }, text: 'Sodium fizzes: a colourless gas that burns with a pop (H₂). An acidic O–H is present.' };
    case 'nahco3': return comp === 'acid' ? { look: { fizz: 3.5 }, text: 'Brisk effervescence; the gas turns lime water milky (CO₂).' } : { look: {}, text: 'No effervescence.' };
    case 'fecl3': return comp === 'phenol' ? { look: { color: 0x5b2a86, opacity: 0.85 }, text: 'An intense violet colour.' } : { look: { color: 0xead08a, opacity: 0.6 }, text: comp === 'acid' ? 'Pale buff-yellow; no violet.' : 'Stays the yellow of the reagent.' };
    case 'br2':
      if (comp === 'phenol') return { look: { color: 0xf3f5f7, opacity: 0.55, ppt: { color: 0xffffff, amount: 0.8 } }, text: 'The orange colour vanishes at once and a white precipitate forms (2,4,6-tribromophenol).' };
      if (comp === 'aldehyde') return { look: { color: 0xf3e3b8, opacity: 0.5, dur: 4 }, text: 'The orange colour fades slowly; no precipitate.' };
      return { look: { color: 0xe0902a, opacity: 0.6 }, text: 'Stays orange.' };
    case 'tollens':
      if (!warm) return { look: { color: 0xeef3f7 }, text: 'No change in the cold. This test needs a warm water bath.', needWarm: true };
      return comp === 'aldehyde' ? { look: { color: 0x9aa1a8, opacity: 0.6, mirror: true }, text: 'A bright silver mirror forms on the inside of the tube.' } : { look: {}, text: 'No silver mirror.' };
    case 'fehling':
      if (!warm) return { look: { color: 0x1e5bb8, opacity: 0.7 }, text: 'Deep blue. Nothing happens until it is heated.', needWarm: true };
      return comp === 'aldehyde' ? { look: { color: 0x4f7a4a, opacity: 0.7, ppt: { color: 0xb5442a, amount: 0.7 } }, text: 'A brick-red precipitate of Cu₂O.' } : { look: {}, text: 'Stays deep blue: no red precipitate.' };
    case 'dnp': return comp === 'aldehyde' ? { look: { color: 0xf3b04a, ppt: { color: 0xf08a12, amount: 0.9 } }, text: 'A yellow-orange precipitate (a 2,4-dinitrophenylhydrazone): a C=O group.' } : { look: { color: 0xf3b04a }, text: 'Orange solution; no precipitate.' };
    case 'ester':
      if (!warm) return { look: {}, text: 'Nothing to smell yet: warm it, then pour into water.', needWarm: true };
      return comp === 'alcohol' || comp === 'acid' ? { look: { layer: 0xf6f1d6 }, text: 'A sweet, fruity smell, and an oily layer floats on the water: an ester (ethyl ethanoate).' } : { look: {}, text: comp === 'phenol' ? 'Only the smell of phenol; no fruity ester.' : 'No fruity smell.' };
    default: return { look: {}, text: '' };
  }
}

export function create(ctx) {
  const { anim, ui } = ctx;
  const hud = createHud(ctx);
  const comps = Object.keys(GROUPS).sort(() => Math.random() - 0.5);
  const label = { A: comps[0], B: comps[1], C: comps[2], D: comps[3] };
  const order = ['tollens', 'fehling', 'dnp', 'ester', 'na', 'nahco3', 'fecl3', 'br2', 'A', 'B', 'C', 'D'];
  const bench = createTubeBench(ctx, { hud, reagents: REAG, order, tubes: 4, labels: ['1', '2', '3', '4'], bath: true, bottleScale: 0.85, bottlesAt: [-0.35, -0.95], burnerAt: [2.1, -0.35] });
  const st = { sample: null, reagent: null, warm: false, tests: [], seen: {} };

  function fresh() { if (bench.tube) { bench.putBack(); ctx.rig.go(SHOT, 0.9); } st.sample = null; st.reagent = null; st.warm = false; }
  function bar() {
    hud.actions([
      { id: 'warm', label: 'Warm in water bath', disabled: !st.reagent || st.warm || !WARM.has(st.reagent), onClick: warm },
      { id: 'clean', label: 'New tube', disabled: !st.sample, onClick: () => { fresh(); bar(); } },
      { id: 'done', label: `Name them (${st.tests.length})`, primary: true, disabled: st.tests.length < 6, onClick: () => { hud.actions([]); fresh(); ctx.next(); } },
    ]);
  }
  function show(res) { bench.look(res.look); ui.say(`<b>${st.sample} + ${NAMES[st.reagent]}</b>${st.warm ? ' (warmed)' : ''}: ${res.text}`, 'info', 4600); }
  function record(res) {
    const k = `${st.sample} + ${NAMES[st.reagent]}`; if (res.needWarm) return;
    st.tests.push(k); st.seen[k] = res.text; ui.observe(k, res.text.length > 60 ? `${res.text.slice(0, 58)}…` : res.text);
  }
  function warm() {
    if (!bench.heat(3.5, () => { st.warm = true; const res = react(label[st.sample], st.reagent, true); show(res); record(res); bar(); })) return;
    hud.enable('warm', false);
  }

  const SHOT = shot({ pos: [0.4, 3.3, 3.1], target: [0.4, 0.3, -0.3], fit: 4.4, fitH: 2.4 });
  const SHOT_TUBE = shot({ pos: [1.5, 1.45, 2.1], target: [1.2, 0.6, 0.2], fit: 1.9, fitH: 1.6 });
  const steps = [
    {
      title: 'Test the four liquids', text: 'Tap a sample bottle (<b>A–D</b>) to put a little in a clean tube, then tap a <b>reagent</b>. Some tests only work when <b>warmed</b> in the water bath. Use <b>New tube</b> for every test. Run enough tests to tell all four apart (at least six).', hint: 'Na fizzes with any –OH; NaHCO₃ only with an acid; FeCl₃ turns violet only with phenol; Tollens\' and Fehling\'s only with an aldehyde, and only when warm.', shot: SHOT, hideBelt: true,
      enter() { bar(); },
      exit() { hud.actions([]); },
      skip() { ['A', 'B', 'C', 'D'].forEach((s) => ['na', 'nahco3', 'fecl3', 'tollens'].forEach((r) => { const res = react(label[s], r, true); st.tests.push(`${s} + ${NAMES[r]}`); st.seen[`${s} + ${NAMES[r]}`] = res.text; })); },
      handler: { down(p) {
        if (bench.busy) return true;
        const k = bench.bottleAt(p, order); if (!k) return false;
        if ('ABCD'.includes(k)) {
          if (st.sample && st.sample !== k) { ctx.mistake('Never add a second sample to a used tube: start a new tube for each test.', 2); return true; }
          if (st.sample) return true;
          st.sample = k; bench.bring(0); anim.wait(0.85, () => { bench.pour(k, 3, () => bench.look({ fill: 0.14, color: k === 'D' && label.D === 'phenol' ? 0xf8f0e0 : 0xf3f7fb, opacity: 0.5, dur: 0.5 })); }); bar(); return true;
        }
        if (!st.sample) { ctx.say('Put a sample in the tube first.', 'hint', 1600); return true; }
        if (st.reagent) { ctx.mistake('One reagent per tube: mixing reagents in the same tube makes the result meaningless. Take a new tube.', 2); return true; }
        st.reagent = k; anim.wait(1.2, () => ctx.rig.go(SHOT_TUBE, 1.0)); bench.pour(k, k === 'na' ? 1 : 4, () => { const res = react(label[st.sample], k, false); show(res); record(res); bar(); }, k === 'na' ? 0xd9d4b8 : undefined);
        return true;
      } },
    },
    {
      title: 'Name the functional groups', text: 'Put the positive and the negative results together.', shot: SHOT, hideBelt: true,
      enter() {
        const left = ['A', 'B', 'C', 'D']; const ask = () => {
          const s = left[0]; if (!s) { ctx.next('All four identified.', 1.2); return; }
          ui.choose(ctx.stage.clientWidth / 2, 40, `Sample ${s} is…`, Object.keys(GROUPS).map((g) => ({ label: GROUPS[g], value: g })), (v) => {
            if (v !== label[s]) { ctx.mistake(`Not ${GROUPS[v].toLowerCase()}. ${hintFor(label[s])}`, 4); anim.wait(0.4, ask); return; }
            ui.observe(`Sample ${s}`, `<b>${GROUPS[v]}</b>`); left.shift(); anim.wait(0.3, ask);
          });
        };
        anim.wait(0.6, ask);
      },
      exit() { ui.clearChooser(); },
    },
  ];
  function hintFor(c) {
    return { alcohol: 'Look again: it fizzes with sodium but not with NaHCO₃, gives no violet with FeCl₃, and the ester test is fruity.', aldehyde: 'Look again: no fizz with sodium, but a silver mirror with warm Tollens\' and a red precipitate with Fehling\'s.', acid: 'Look again: it is the one that fizzes with NaHCO₃.', phenol: 'Look again: violet with FeCl₃, and a white precipitate with bromine water.' }[c];
  }

  ctx.debug = { st, label, bench, react };
  return {
    tools: [], steps,
    update(dt, t) { bench.update(dt, t); hud.update(); },
    result() {
      return {
        title: 'Functional groups',
        rows: [['Tests run', String(st.tests.length)]].concat(['A', 'B', 'C', 'D'].map((s) => [`Sample ${s}`, GROUPS[label[s]]])),
        conclusion: 'Sodium shows an acidic O–H (alcohol, phenol, acid); NaHCO₃ picks out the carboxylic acid, the only one stronger than carbonic acid; neutral FeCl₃ (violet) and bromine water (white precipitate) name phenol; the aldehyde is the reducing agent that gives Tollens\' silver mirror and Fehling\'s red Cu₂O, but only when warm. One positive test is never enough: the negatives matter as much.',
      };
    },
    dispose() { hud.dispose(); bench.dispose(); },
  };
}
