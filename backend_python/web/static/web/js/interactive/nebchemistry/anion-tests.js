import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { drawTestTube, makeBubbles, text } from './chem-utils.js';

const ANIONS = [
  { id: 'co3', name: 'CO₃²⁻ (carbonate)', salt: 'Na₂CO₃' },
  { id: 'cl', name: 'Cl⁻ (chloride)', salt: 'NaCl' },
  { id: 'so4', name: 'SO₄²⁻ (sulphate)', salt: 'Na₂SO₄' },
  { id: 'no3', name: 'NO₃⁻ (nitrate)', salt: 'NaNO₃' },
];

const TESTS = {
  h2so4: {
    label: 'Dilute H₂SO₄ + lime water',
    results: {
      co3: { obs: 'Brisk effervescence! The gas turns lime water milky.', eqn: 'Na₂CO₃ + H₂SO₄ → Na₂SO₄ + H₂O + CO₂↑;  CO₂ + Ca(OH)₂ → CaCO₃↓ + H₂O', hit: true },
      cl: { obs: 'No effervescence with dilute acid in the cold.', eqn: '', hit: false },
      so4: { obs: 'No visible change.', eqn: '', hit: false },
      no3: { obs: 'No visible change with dilute acid.', eqn: '', hit: false },
    },
  },
  agno3: {
    label: 'AgNO₃ + dilute HNO₃',
    results: {
      co3: { obs: 'A white precipitate forms, but it dissolves on adding HNO₃ with fizzing — not a halide.', eqn: '', hit: false },
      cl: { obs: 'Curdy WHITE precipitate, insoluble in HNO₃, soluble in NH₄OH.', eqn: 'NaCl + AgNO₃ → AgCl↓ (white) + NaNO₃', hit: true },
      so4: { obs: 'No precipitate (Ag₂SO₄ is fairly soluble in dilute solution).', eqn: '', hit: false },
      no3: { obs: 'No precipitate.', eqn: '', hit: false },
    },
  },
  bacl2: {
    label: 'BaCl₂ + dilute HCl',
    results: {
      co3: { obs: 'White precipitate forms but dissolves in dilute HCl with effervescence.', eqn: '', hit: false },
      cl: { obs: 'No precipitate.', eqn: '', hit: false },
      so4: { obs: 'Heavy WHITE precipitate, insoluble in dilute HCl.', eqn: 'Na₂SO₄ + BaCl₂ → BaSO₄↓ (white) + 2NaCl', hit: true },
      no3: { obs: 'No precipitate.', eqn: '', hit: false },
    },
  },
  brownring: {
    label: 'Brown ring test (FeSO₄ + conc. H₂SO₄)',
    results: {
      co3: { obs: 'No ring; fizzing on adding acid.', eqn: '', hit: false },
      cl: { obs: 'No brown ring.', eqn: '', hit: false },
      so4: { obs: 'No brown ring.', eqn: '', hit: false },
      no3: { obs: 'A BROWN RING forms at the junction of the two layers!', eqn: 'NO₃⁻ + 3Fe²⁺ + 4H⁺ → NO + 3Fe³⁺ + 2H₂O;  [Fe(H₂O)₅NO]²⁺ = brown ring', hit: true },
    },
  },
};

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Unknown salt issued — test it!', '#8b5cf6');
  const bubbles = makeBubbles(26);

  let unknown = ANIONS[Math.floor(Math.random() * ANIONS.length)];
  let currentTest = null;
  let effect = null;
  let effectT = 0;
  let log = [];
  let solved = 0;
  let t = 0;

  const panel = createPanel(stage, { title: 'Anion Analysis' });
  const sampleOut = panel.readout({ label: 'Sample', value: 'unknown white salt' });
  panel.divider();
  panel.section('Perform a test');
  panel.button({ label: 'Dilute H₂SO₄ + lime water', icon: 'science', onClick: () => runTest('h2so4') });
  panel.button({ label: 'AgNO₃ solution + HNO₃', icon: 'science', onClick: () => runTest('agno3') });
  panel.button({ label: 'BaCl₂ solution + HCl', icon: 'science', onClick: () => runTest('bacl2') });
  panel.button({ label: 'Brown ring test', icon: 'science', onClick: () => runTest('brownring') });
  panel.divider();
  panel.section('Conclusion');
  panel.select({
    label: 'The anion is…',
    options: [{ value: '', label: '— decide —' }].concat(ANIONS.map((a) => ({ value: a.id, label: a.name }))),
    value: '',
    onChange: (v) => {
      if (!v) return;
      if (v === unknown.id) {
        solved++;
        scoreOut.set(String(solved));
        showInfoCard(stage, { title: 'Correct identification!', body: `The salt was ${unknown.salt}, containing ${unknown.name}. A new unknown has been issued.`, color: '#10b981' });
        newUnknown();
      } else {
        showInfoCard(stage, { title: 'Check your observations', body: `Your tests do not support ${ANIONS.find((a) => a.id === v).name}. Re-run the tests and match each observation to its anion.`, color: '#ef4444' });
      }
    },
  });
  const scoreOut = panel.readout({ label: 'Salts solved', value: '0' });
  panel.button({ label: 'New unknown salt', icon: 'replay', variant: 'ghost', onClick: newUnknown });
  panel.info('Work like a real analyst: dilute acid first (gases), then precipitation tests. A confirmatory test should give one clear positive.');

  function newUnknown() {
    unknown = ANIONS[Math.floor(Math.random() * ANIONS.length)];
    currentTest = null;
    effect = null;
    log = [];
    bubbles.clear();
    badge.set('Unknown salt issued — test it!');
    badge.el.style.setProperty('--ix-hud-color', '#8b5cf6');
    sampleOut.set('unknown white salt');
  }

  function runTest(key) {
    currentTest = key;
    const res = TESTS[key].results[unknown.id];
    effect = { key, hit: res.hit };
    effectT = 0;
    bubbles.clear();
    log.unshift({ test: TESTS[key].label, obs: res.obs, hit: res.hit });
    if (log.length > 4) log.pop();
    badge.set(res.hit ? 'Positive result!' : 'Negative — note it down');
    badge.el.style.setProperty('--ix-hud-color', res.hit ? '#10b981' : '#64748b');
    showInfoCard(stage, {
      title: TESTS[key].label,
      body: res.obs + (res.eqn ? `\n${res.eqn}` : ''),
      color: res.hit ? '#10b981' : '#64748b',
    });
  }

  sim.setUpdate((ctx, dt, w, h) => {
    t += dt;
    if (effect) effectT = Math.min(1, effectT + dt * 0.5);

    ctx.clearRect(0, 0, w, h);
    const benchY = h * 0.86;
    ctx.fillStyle = '#3f3428';
    ctx.fillRect(0, benchY, w, h - benchY);

    const cx = w * 0.3;
    const tubeTop = h * 0.22;
    const tubeH = benchY - tubeTop - 18;
    let liquid = 'rgba(203,213,225,0.25)';
    if (effect && effect.hit && effectT > 0.3) {
      if (effect.key === 'agno3' || effect.key === 'bacl2') liquid = `rgba(241,245,249,${0.25 + 0.55 * effectT})`;
    }
    drawTestTube(ctx, cx, tubeTop, 34, tubeH, 0.55, liquid, 'salt solution');

    if (effect && effectT > 0.15) {
      const liqTop = tubeTop + tubeH * 0.45;
      if (effect.key === 'h2so4' && effect.hit) {
        bubbles.spawn(cx, benchY - 30, { spread: 20, top: liqTop });
        text(ctx, 'CO₂ ↑', cx + 34, tubeTop + tubeH * 0.36, { align: 'left', color: '#fbbf24' });
        const lw = w * 0.62;
        drawTestTube(ctx, lw, tubeTop + 30, 30, tubeH - 30, 0.5, `rgba(241,245,249,${0.15 + 0.6 * effectT})`, 'lime water');
        text(ctx, effectT > 0.6 ? 'milky!' : 'gas bubbling through…', lw, tubeTop + 16, { color: effectT > 0.6 ? '#f8fafc' : '#94a3b8' });
        ctx.strokeStyle = 'rgba(148,163,184,0.7)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(cx, tubeTop - 8);
        ctx.lineTo(cx, tubeTop - 22);
        ctx.lineTo(lw, tubeTop - 22);
        ctx.lineTo(lw, tubeTop + 26);
        ctx.stroke();
      }
      if ((effect.key === 'agno3' || effect.key === 'bacl2') && effect.hit) {
        ctx.fillStyle = `rgba(248,250,252,${0.85 * effectT})`;
        for (let i = 0; i < 14; i++) {
          const px = cx - 12 + (i % 5) * 6;
          const py = benchY - 24 - Math.floor(i / 5) * 5 - Math.sin(i * 3.7) * 14 * (1 - effectT);
          ctx.fillRect(px, py, 3, 3);
        }
        text(ctx, effect.key === 'agno3' ? 'white curdy ppt (AgCl)' : 'white ppt (BaSO₄)', cx + 40, benchY - 40, { align: 'left', color: '#f8fafc' });
      }
      if (effect.key === 'brownring' && effect.hit) {
        const ringY = tubeTop + tubeH * 0.62;
        ctx.fillStyle = `rgba(146,64,14,${0.9 * effectT})`;
        ctx.fillRect(cx - 15, ringY - 3, 30, 6);
        text(ctx, 'brown ring at the junction', cx + 40, ringY, { align: 'left', color: '#d97706' });
        text(ctx, 'conc. H₂SO₄ layer below', cx + 40, ringY + 16, { align: 'left' });
      }
      if (!effect.hit) {
        text(ctx, 'no change', cx + 40, tubeTop + tubeH * 0.5, { align: 'left', color: '#64748b' });
      }
    }

    bubbles.step(dt);
    bubbles.draw(ctx);

    text(ctx, 'Observation log', w * 0.66, h * 0.1, { font: '700 11px Poppins, sans-serif', color: '#e2e8f0', align: 'left' });
    if (!log.length) text(ctx, 'run a test to begin', w * 0.66, h * 0.1 + 18, { align: 'left' });
    log.forEach((entry, i) => {
      const y = h * 0.1 + 20 + i * 30;
      text(ctx, entry.test, w * 0.66, y, { align: 'left', color: entry.hit ? '#34d399' : '#94a3b8' });
      const obs = entry.obs.length > 42 ? entry.obs.slice(0, 42) + '…' : entry.obs;
      text(ctx, obs, w * 0.66, y + 12, { align: 'left', font: '500 8.5px Poppins, sans-serif' });
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
