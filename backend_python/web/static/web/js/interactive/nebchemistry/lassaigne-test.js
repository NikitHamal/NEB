import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { drawTestTube, drawBurner, makeBubbles, text } from './chem-utils.js';

const COMPOUNDS = [
  { id: 'urea', name: 'Urea', has: ['n'], formula: 'NH₂CONH₂' },
  { id: 'thiourea', name: 'Thiourea', has: ['n', 's'], formula: 'NH₂CSNH₂' },
  { id: 'chloroform', name: 'Chloroform', has: ['cl'], formula: 'CHCl₃' },
  { id: 'sulphanilic', name: 'Sulphanilic acid', has: ['n', 's'], formula: 'C₆H₇NO₃S' },
  { id: 'glucose', name: 'Glucose', has: [], formula: 'C₆H₁₂O₆' },
  { id: 'bromobenzene', name: 'Bromobenzene', has: ['br'], formula: 'C₆H₅Br' },
];

const TESTS = {
  n: {
    label: 'Nitrogen: FeSO₄ + FeCl₃, boil, acidify',
    pos: 'PRUSSIAN BLUE colour appears! Na + C + N → NaCN; 6CN⁻ + Fe²⁺ → [Fe(CN)₆]⁴⁻; then Fe⁴[Fe(CN)₆]₃ = Prussian blue.',
    neg: 'No blue colour — nitrogen absent.',
    fx: { color: 'rgba(30,58,138,0.85)', label: 'Prussian blue' },
  },
  s: {
    label: 'Sulphur: sodium nitroprusside',
    pos: 'Deep VIOLET colouration! Na + S → Na₂S; S²⁻ + [Fe(CN)₅NO]²⁻ → [Fe(CN)₅NOS]⁴⁻ (violet).',
    neg: 'No violet colour — sulphur absent.',
    fx: { color: 'rgba(124,58,237,0.8)', label: 'violet' },
  },
  hal: {
    label: 'Halogens: boil with HNO₃, add AgNO₃',
    posCl: 'WHITE curdy precipitate, soluble in NH₄OH → chlorine present. NaCl + AgNO₃ → AgCl↓ + NaNO₃.',
    posBr: 'PALE YELLOW precipitate, sparingly soluble in NH₄OH → bromine present. NaBr + AgNO₃ → AgBr↓ + NaNO₃.',
    neg: 'No precipitate — halogens absent.',
  },
};

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Step 1: fuse the compound with sodium', '#047857');
  const bubbles = makeBubbles(18);

  let unknown = COMPOUNDS[Math.floor(Math.random() * COMPOUNDS.length)];
  let stagePhase = 'fuse';
  let fuseT = 0;
  let fusing = false;
  let effect = null;
  let effectT = 0;
  let log = [];
  let solved = 0;
  let t = 0;

  const panel = createPanel(stage, { title: "Lassaigne's Test" });
  const phaseOut = panel.readout({ label: 'Stage', value: 'fusion' });
  panel.button({ label: 'Fuse with sodium (red hot)', icon: 'local_fire_department', onClick: () => {
    if (stagePhase !== 'fuse') return;
    fusing = true;
    badge.set('Heating the ignition tube to red heat…');
    badge.el.style.setProperty('--ix-hud-color', '#ef4444');
  } });
  panel.button({ label: 'Plunge into water, boil & filter', icon: 'water_drop', onClick: () => {
    if (stagePhase !== 'extract') {
      badge.set(stagePhase === 'fuse' ? 'Fuse with sodium first!' : 'Extract already prepared');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      return;
    }
    stagePhase = 'test';
    phaseOut.set('sodium extract ready');
    badge.set('Clear sodium extract (fusion filtrate) ready — run the tests');
    badge.el.style.setProperty('--ix-hud-color', '#10b981');
    showInfoCard(stage, { title: 'Sodium extract prepared', body: 'The red-hot tube is plunged into distilled water and the mixture boiled and filtered. Covalent N, S and halogens are now ionic: NaCN, Na₂S, NaX — testable in solution.', color: '#10b981' });
  } });
  panel.divider();
  panel.section('Test the extract');
  panel.button({ label: TESTS.n.label, icon: 'science', onClick: () => runTest('n') });
  panel.button({ label: TESTS.s.label, icon: 'science', onClick: () => runTest('s') });
  panel.button({ label: TESTS.hal.label, icon: 'science', onClick: () => runTest('hal') });
  panel.divider();
  panel.select({
    label: 'Elements present…',
    options: [{ value: '', label: '— conclude —' }].concat([
      { value: 'n', label: 'N only' },
      { value: 'n,s', label: 'N and S' },
      { value: 'cl', label: 'Cl only' },
      { value: 'br', label: 'Br only' },
      { value: 'none', label: 'None of N, S, X' },
    ]),
    value: '',
    onChange: (v) => {
      if (!v) return;
      const key = unknown.has.length ? unknown.has.join(',') : 'none';
      if (v === key) {
        solved++;
        scoreOut.set(String(solved));
        showInfoCard(stage, { title: 'Correct!', body: `${unknown.name} (${unknown.formula}) contains ${key === 'none' ? 'no N, S or halogens — only C, H, O' : key.toUpperCase().replace(',', ' and ')}. New compound issued.`, color: '#10b981' });
        newCompound();
      } else {
        showInfoCard(stage, { title: 'Check again', body: 'Your conclusion does not match the test results. Re-run each test on the extract and note exactly which colours appeared.', color: '#ef4444' });
      }
    },
  });
  const scoreOut = panel.readout({ label: 'Compounds solved', value: '0' });
  panel.button({ label: 'New unknown compound', icon: 'replay', variant: 'ghost', onClick: newCompound });
  panel.info('Sodium fusion converts covalently-bound N, S and halogens into water-soluble ionic salts. CAUTION in the real lab: sodium reacts violently with water — use tongs and safety screens!');

  function newCompound() {
    unknown = COMPOUNDS[Math.floor(Math.random() * COMPOUNDS.length)];
    stagePhase = 'fuse';
    fuseT = 0;
    fusing = false;
    effect = null;
    log = [];
    phaseOut.set('fusion');
    badge.set('Step 1: fuse the new compound with sodium');
    badge.el.style.setProperty('--ix-hud-color', '#047857');
  }

  function runTest(key) {
    if (stagePhase !== 'test') {
      badge.set('Prepare the sodium extract first!');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      return;
    }
    let obs, hit, fx;
    if (key === 'hal') {
      if (unknown.has.includes('cl')) { obs = TESTS.hal.posCl; hit = true; fx = { color: 'rgba(248,250,252,0.9)', label: 'white ppt', ppt: true }; }
      else if (unknown.has.includes('br')) { obs = TESTS.hal.posBr; hit = true; fx = { color: 'rgba(254,240,138,0.9)', label: 'pale yellow ppt', ppt: true }; }
      else if (unknown.has.includes('n') || unknown.has.includes('s')) { obs = 'No true halide ppt (extract boiled with HNO₃ first to expel HCN/H₂S — otherwise false positives!).'; hit = false; }
      else { obs = TESTS.hal.neg; hit = false; }
    } else {
      hit = unknown.has.includes(key);
      obs = hit ? TESTS[key].pos : TESTS[key].neg;
      if (hit) fx = TESTS[key].fx;
    }
    effect = fx || null;
    effectT = 1;
    log.unshift({ test: key === 'hal' ? 'AgNO₃ test' : key === 'n' ? 'Prussian blue test' : 'Nitroprusside test', obs, hit });
    if (log.length > 4) log.pop();
    badge.set(hit ? 'Positive!' : 'Negative');
    badge.el.style.setProperty('--ix-hud-color', hit ? '#10b981' : '#64748b');
    showInfoCard(stage, { title: key === 'hal' ? TESTS.hal.label : TESTS[key].label, body: obs, color: hit ? '#10b981' : '#64748b' });
  }

  sim.setUpdate((ctx, dt, w, h) => {
    t += dt;
    if (fusing) {
      fuseT += dt;
      if (fuseT > 3) {
        fusing = false;
        stagePhase = 'extract';
        phaseOut.set('red-hot — plunge into water');
        badge.set('Tube is red hot! Plunge it into distilled water');
        badge.el.style.setProperty('--ix-hud-color', '#f59e0b');
      }
    }
    if (effectT > 0) effectT = Math.max(0, effectT - dt * 0.15);

    ctx.clearRect(0, 0, w, h);
    const benchY = h * 0.88;
    ctx.fillStyle = '#3f3428';
    ctx.fillRect(0, benchY, w, h - benchY);

    if (stagePhase === 'fuse' || stagePhase === 'extract') {
      const cx = w * 0.32;
      drawBurner(ctx, cx, benchY, t, fusing, '#60a5fa', 36);
      const glow = stagePhase === 'extract' ? 1 : Math.min(1, fuseT / 3);
      ctx.save();
      ctx.translate(cx, benchY - 64);
      ctx.rotate(-0.5);
      drawTestTube(ctx, 0, -34, 13, 50, 0.3, `rgba(${Math.round(120 + glow * 135)},${Math.round(60 + glow * 20)},40,${0.4 + glow * 0.5})`);
      ctx.restore();
      text(ctx, 'ignition tube: sample + Na', cx + 10, benchY - 120);
      text(ctx, `unknown: "${unknown.name}"`, cx, benchY + 16, { color: '#c084fc' });
      if (glow > 0.8) text(ctx, 'RED HOT', cx + 36, benchY - 86, { align: 'left', color: '#f87171', font: '700 11px Poppins, sans-serif' });
      if (stagePhase === 'extract') {
        const bx = w * 0.68;
        ctx.fillStyle = 'rgba(96,165,250,0.3)';
        ctx.fillRect(bx - 38, benchY - 44, 76, 42);
        ctx.strokeStyle = 'rgba(199,212,234,0.85)';
        ctx.strokeRect(bx - 40, benchY - 48, 80, 46);
        text(ctx, 'distilled water — plunge here!', bx, benchY + 16, { color: '#fbbf24' });
      }
    } else {
      const cx = w * 0.24;
      const tubeTop = h * 0.26;
      const tubeH = benchY - tubeTop - 16;
      let liquid = 'rgba(203,213,225,0.2)';
      if (effect && effectT > 0 && !effect.ppt) liquid = effect.color;
      drawTestTube(ctx, cx, tubeTop, 34, tubeH, 0.55, liquid, 'sodium extract');
      if (effect && effectT > 0) {
        if (effect.ppt) {
          ctx.fillStyle = effect.color;
          for (let i = 0; i < 12; i++) {
            ctx.fillRect(cx - 11 + (i % 4) * 7, benchY - 26 - Math.floor(i / 4) * 5 - effectT * 24 * Math.abs(Math.sin(i * 2.1)), 3.5, 3.5);
          }
        }
        text(ctx, effect.label, cx + 38, tubeTop + tubeH * 0.5, { align: 'left', color: '#e2e8f0', font: '700 11px Poppins, sans-serif' });
      }
      const lx = w * 0.5;
      text(ctx, 'Test record', lx, h * 0.1, { align: 'left', font: '700 11px Poppins, sans-serif', color: '#e2e8f0' });
      if (!log.length) text(ctx, 'no tests yet', lx, h * 0.1 + 18, { align: 'left' });
      log.forEach((e, i) => {
        const y = h * 0.1 + 20 + i * 32;
        text(ctx, e.test, lx, y, { align: 'left', color: e.hit ? '#34d399' : '#94a3b8' });
        const obs = e.obs.length > 46 ? e.obs.slice(0, 46) + '…' : e.obs;
        text(ctx, obs, lx, y + 12, { align: 'left', font: '500 8.5px Poppins, sans-serif' });
      });
    }

    bubbles.step(dt);
    bubbles.draw(ctx);
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
