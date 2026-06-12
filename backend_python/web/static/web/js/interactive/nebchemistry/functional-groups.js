import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { drawTestTube, makeBubbles, text } from './chem-utils.js';

const COMPOUNDS = [
  { id: 'alcohol', name: 'Ethanol (alcohol, −OH)', label: 'C₂H₅OH' },
  { id: 'aldehyde', name: 'Ethanal (aldehyde, −CHO)', label: 'CH₃CHO' },
  { id: 'acid', name: 'Ethanoic acid (−COOH)', label: 'CH₃COOH' },
  { id: 'phenol', name: 'Phenol (Ar−OH)', label: 'C₆H₅OH' },
];

const TESTS = {
  na: {
    label: 'Sodium metal test',
    results: {
      alcohol: { obs: 'Brisk effervescence of H₂ gas — sodium reacts with the −OH group.', eqn: '2C₂H₅OH + 2Na → 2C₂H₅ONa + H₂↑', hit: true, fx: 'fizz' },
      aldehyde: { obs: 'No effervescence — aldehydes have no acidic −OH hydrogen.', eqn: '', hit: false, fx: 'none' },
      acid: { obs: 'Effervescence of H₂ (acids also react!) — not conclusive alone.', eqn: '2CH₃COOH + 2Na → 2CH₃COONa + H₂↑', hit: true, fx: 'fizz' },
      phenol: { obs: 'Slow effervescence — phenol\'s −OH also reacts. Combine with other tests.', eqn: '2C₆H₅OH + 2Na → 2C₆H₅ONa + H₂↑', hit: true, fx: 'fizz' },
    },
  },
  tollens: {
    label: "Tollens' test (warm)",
    results: {
      alcohol: { obs: 'No silver mirror.', eqn: '', hit: false, fx: 'none' },
      aldehyde: { obs: 'A shining SILVER MIRROR coats the tube wall!', eqn: 'CH₃CHO + 2[Ag(NH₃)₂]⁺ + 3OH⁻ → CH₃COO⁻ + 2Ag↓ + 4NH₃ + 2H₂O', hit: true, fx: 'mirror' },
      acid: { obs: 'No silver mirror.', eqn: '', hit: false, fx: 'none' },
      phenol: { obs: 'No silver mirror.', eqn: '', hit: false, fx: 'none' },
    },
  },
  fehling: {
    label: "Fehling's test (boil)",
    results: {
      alcohol: { obs: 'Solution stays blue — no reaction.', eqn: '', hit: false, fx: 'none' },
      aldehyde: { obs: 'RED-BROWN precipitate of Cu₂O forms on boiling!', eqn: 'CH₃CHO + 2Cu²⁺ + 5OH⁻ → CH₃COO⁻ + Cu₂O↓ + 3H₂O', hit: true, fx: 'redppt' },
      acid: { obs: 'Stays blue.', eqn: '', hit: false, fx: 'none' },
      phenol: { obs: 'Stays blue.', eqn: '', hit: false, fx: 'none' },
    },
  },
  nahco3: {
    label: 'NaHCO₃ test',
    results: {
      alcohol: { obs: 'No effervescence — alcohols are too weakly acidic.', eqn: '', hit: false, fx: 'none' },
      aldehyde: { obs: 'No effervescence.', eqn: '', hit: false, fx: 'none' },
      acid: { obs: 'Brisk effervescence of CO₂ — the test for −COOH!', eqn: 'CH₃COOH + NaHCO₃ → CH₃COONa + H₂O + CO₂↑', hit: true, fx: 'fizz' },
      phenol: { obs: 'NO effervescence — phenol is too weak to displace CO₂. This separates phenol from carboxylic acids!', eqn: '', hit: false, fx: 'none' },
    },
  },
  fecl3: {
    label: 'Neutral FeCl₃ test',
    results: {
      alcohol: { obs: 'No colour change.', eqn: '', hit: false, fx: 'none' },
      aldehyde: { obs: 'No colour change.', eqn: '', hit: false, fx: 'none' },
      acid: { obs: 'Red colouration (ferric acetate) — note, not violet.', eqn: '3CH₃COO⁻ + Fe³⁺ → (CH₃COO)₃Fe (red)', hit: true, fx: 'red' },
      phenol: { obs: 'VIOLET / purple colouration — characteristic of phenol!', eqn: '6C₆H₅OH + Fe³⁺ → [Fe(OC₆H₅)₆]³⁻ (violet) + 6H⁺', hit: true, fx: 'violet' },
    },
  },
  ester: {
    label: 'Ester test (acid + ethanol + conc. H₂SO₄)',
    results: {
      alcohol: { obs: 'Fruity smell only if an acid is also present — alone, nothing.', eqn: '', hit: false, fx: 'none' },
      aldehyde: { obs: 'No fruity smell.', eqn: '', hit: false, fx: 'none' },
      acid: { obs: 'Sweet FRUITY smell of ethyl ethanoate after warming!', eqn: 'CH₃COOH + C₂H₅OH --H₂SO₄--> CH₃COOC₂H₅ + H₂O', hit: true, fx: 'smell' },
      phenol: { obs: 'No fruity smell under these conditions.', eqn: '', hit: false, fx: 'none' },
    },
  },
};

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Unknown liquid A — run any test', '#8b5cf6');
  const bubbles = makeBubbles(22);

  let unknown = COMPOUNDS[Math.floor(Math.random() * COMPOUNDS.length)];
  let effect = null;
  let effectT = 0;
  let log = [];
  let solved = 0;

  const panel = createPanel(stage, { title: 'Organic Analysis' });
  panel.section('Perform tests (any order)');
  Object.keys(TESTS).forEach((k) => {
    panel.button({ label: TESTS[k].label, icon: 'science', onClick: () => run(k) });
  });
  panel.divider();
  panel.select({
    label: 'Functional group is…',
    options: [{ value: '', label: '— conclude —' }].concat(COMPOUNDS.map((c) => ({ value: c.id, label: c.name }))),
    value: '',
    onChange: (v) => {
      if (!v) return;
      if (v === unknown.id) {
        solved++;
        scoreOut.set(String(solved));
        showInfoCard(stage, { title: 'Identified!', body: `The unknown was ${unknown.name} (${unknown.label}). A new unknown liquid is on the bench.`, color: '#10b981' });
        newUnknown();
      } else {
        showInfoCard(stage, { title: 'Re-examine the evidence', body: 'At least one of your observations contradicts that group. Remember: NaHCO₃ fizz = −COOH only; silver mirror = −CHO only; violet FeCl₃ = phenol.', color: '#ef4444' });
      }
    },
  });
  const scoreOut = panel.readout({ label: 'Identified', value: '0' });
  panel.button({ label: 'New unknown liquid', icon: 'replay', variant: 'ghost', onClick: newUnknown });
  panel.info('Each functional group has a signature test. Run two or three tests and cross-check — one positive plus the right negatives nails the group.');

  function newUnknown() {
    unknown = COMPOUNDS[Math.floor(Math.random() * COMPOUNDS.length)];
    effect = null;
    log = [];
    bubbles.clear();
    badge.set('Unknown liquid issued — run any test');
    badge.el.style.setProperty('--ix-hud-color', '#8b5cf6');
  }

  function run(key) {
    const res = TESTS[key].results[unknown.id];
    effect = { fx: res.fx };
    effectT = 1;
    bubbles.clear();
    log.unshift({ test: TESTS[key].label, obs: res.obs, hit: res.hit });
    if (log.length > 5) log.pop();
    badge.set(res.hit ? 'Positive!' : 'Negative — useful clue');
    badge.el.style.setProperty('--ix-hud-color', res.hit ? '#10b981' : '#64748b');
    showInfoCard(stage, { title: TESTS[key].label, body: res.obs + (res.eqn ? `\n${res.eqn}` : ''), color: res.hit ? '#10b981' : '#64748b' });
  }

  sim.setUpdate((ctx, dt, w, h) => {
    if (effectT > 0) effectT = Math.max(0, effectT - dt * 0.18);

    ctx.clearRect(0, 0, w, h);
    const benchY = h * 0.88;
    ctx.fillStyle = '#3f3428';
    ctx.fillRect(0, benchY, w, h - benchY);

    const cx = w * 0.22;
    const tubeTop = h * 0.24;
    const tubeH = benchY - tubeTop - 16;
    let liquid = 'rgba(203,213,225,0.25)';
    if (effect && effectT > 0) {
      if (effect.fx === 'violet') liquid = `rgba(139,92,246,${0.3 + 0.4 * (1 - effectT)})`;
      if (effect.fx === 'red') liquid = `rgba(220,38,38,${0.3 + 0.35 * (1 - effectT)})`;
      if (effect.fx === 'redppt') liquid = 'rgba(59,130,246,0.35)';
    }
    drawTestTube(ctx, cx, tubeTop, 34, tubeH, 0.5, liquid, 'unknown liquid');

    if (effect && effectT > 0) {
      const liqTop = tubeTop + tubeH * 0.5;
      if (effect.fx === 'fizz') {
        bubbles.spawn(cx, benchY - 28, { spread: 20, top: liqTop });
        text(ctx, 'gas evolved ↑', cx + 36, liqTop, { align: 'left', color: '#fbbf24' });
      } else if (effect.fx === 'mirror') {
        ctx.strokeStyle = `rgba(226,232,240,${0.95 * (1 - effectT * 0.5)})`;
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(cx - 15, liqTop);
        ctx.lineTo(cx - 15, benchY - 36);
        ctx.moveTo(cx + 15, liqTop);
        ctx.lineTo(cx + 15, benchY - 36);
        ctx.stroke();
        text(ctx, 'silver mirror!', cx + 36, liqTop + 20, { align: 'left', color: '#e2e8f0' });
      } else if (effect.fx === 'redppt') {
        ctx.fillStyle = `rgba(185,28,28,${0.9 * (1 - effectT * 0.4)})`;
        for (let i = 0; i < 10; i++) {
          ctx.fillRect(cx - 10 + (i % 4) * 6, benchY - 26 - Math.floor(i / 4) * 5, 3.5, 3.5);
        }
        text(ctx, 'red Cu₂O ppt', cx + 36, benchY - 36, { align: 'left', color: '#f87171' });
      } else if (effect.fx === 'smell') {
        text(ctx, '~ fruity smell ~', cx, tubeTop - 14, { color: '#f9a8d4', font: '700 11px Poppins, sans-serif' });
      } else if (effect.fx === 'none') {
        text(ctx, 'no change', cx + 36, liqTop, { align: 'left', color: '#64748b' });
      }
    }

    bubbles.step(dt);
    bubbles.draw(ctx);

    const lx = w * 0.46;
    text(ctx, 'Observations', lx, h * 0.08, { align: 'left', font: '700 11px Poppins, sans-serif', color: '#e2e8f0' });
    if (!log.length) text(ctx, 'no tests yet', lx, h * 0.08 + 18, { align: 'left' });
    log.forEach((e, i) => {
      const y = h * 0.08 + 20 + i * 32;
      text(ctx, e.test, lx, y, { align: 'left', color: e.hit ? '#34d399' : '#94a3b8' });
      const obs = e.obs.length > 50 ? e.obs.slice(0, 50) + '…' : e.obs;
      text(ctx, obs, lx, y + 12, { align: 'left', font: '500 8.5px Poppins, sans-serif' });
    });
  });

  sim.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
