import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { drawTestTube, makeBubbles, text } from './chem-utils.js';

const SALTS = [
  {
    id: 'pb', name: 'Pb(NO₃)₂', cation: 'Pb²⁺ (Group I)', appearance: 'white crystalline solid',
    dry: 'Decrepitates (crackles); brown fumes of NO₂ on strong heating.',
    flame: { color: '#94a3b8', label: 'no characteristic colour' },
    groups: { g1: 'White ppt of PbCl₂ forms! Soluble in hot water — Group I confirmed.', g2: '—', g3: '—', g4: '—', g5: '—', g6: '—' },
    confirm: 'KI solution → brilliant YELLOW ppt of PbI₂ (golden shower).',
  },
  {
    id: 'cu', name: 'CuSO₄·5H₂O', cation: 'Cu²⁺ (Group II)', appearance: 'blue crystalline solid',
    dry: 'Blue crystals turn white (water of crystallisation lost).',
    flame: { color: '#34d399', label: 'blue-green flame' },
    groups: { g1: 'No ppt with dilute HCl.', g2: 'BLACK ppt of CuS with H₂S in acidic medium — Group II!', g3: '—', g4: '—', g5: '—', g6: '—' },
    confirm: 'Excess NH₄OH → deep ROYAL BLUE solution [Cu(NH₃)₄]²⁺.',
  },
  {
    id: 'fe', name: 'FeCl₃', cation: 'Fe³⁺ (Group III)', appearance: 'yellow-brown solid',
    dry: 'Fuses, turns darker brown.',
    flame: { color: '#fbbf24', label: 'no characteristic colour (sparks gold-brown)' },
    groups: { g1: 'No ppt.', g2: 'No ppt in acidic H₂S.', g3: 'Reddish-BROWN gelatinous ppt of Fe(OH)₃ with NH₄OH/NH₄Cl — Group III!', g4: '—', g5: '—', g6: '—' },
    confirm: 'Potassium ferrocyanide → PRUSSIAN BLUE ppt. KSCN → blood-red colour.',
  },
  {
    id: 'zn', name: 'ZnSO₄·7H₂O', cation: 'Zn²⁺ (Group IV)', appearance: 'white crystalline solid',
    dry: 'Loses water; residue yellow when hot, white when cold (ZnO).',
    flame: { color: '#94a3b8', label: 'no characteristic colour' },
    groups: { g1: 'No ppt.', g2: 'No ppt.', g3: 'No ppt.', g4: 'Dirty WHITE ppt of ZnS with H₂S in ammoniacal medium — Group IV!', g5: '—', g6: '—' },
    confirm: 'NaOH dropwise → white ppt of Zn(OH)₂, soluble in excess NaOH (amphoteric).',
  },
  {
    id: 'ca', name: 'CaCO₃', cation: 'Ca²⁺ (Group V)', appearance: 'white powder',
    dry: 'No melting; gives off CO₂ on strong heating (residue glows).',
    flame: { color: '#f97316', label: 'brick-red flame' },
    groups: { g1: 'No ppt.', g2: 'No ppt.', g3: 'No ppt.', g4: 'No ppt.', g5: 'WHITE ppt of CaCO₃ with (NH₄)₂CO₃ — Group V!', g6: '—' },
    confirm: 'Ammonium oxalate → white ppt of calcium oxalate, insoluble in acetic acid.',
  },
  {
    id: 'nh4', name: 'NH₄Cl', cation: 'NH₄⁺ (Group VI / zero)', appearance: 'white solid',
    dry: 'Sublimes completely — white ring forms on the cool tube wall.',
    flame: { color: '#94a3b8', label: 'no characteristic colour' },
    groups: { g1: 'No ppt.', g2: 'No ppt.', g3: 'No ppt.', g4: 'No ppt.', g5: 'No ppt.', g6: 'Heat with NaOH → pungent NH₃ gas turns moist red litmus BLUE — NH₄⁺!' },
    confirm: 'NH₃ gas + Nessler\'s reagent → brown colouration.',
  },
];

const GROUP_TESTS = [
  { id: 'g1', label: 'Group I: dilute HCl', reagent: 'dil. HCl' },
  { id: 'g2', label: 'Group II: H₂S (acidic)', reagent: 'H₂S + dil. HCl' },
  { id: 'g3', label: 'Group III: NH₄OH + NH₄Cl', reagent: 'NH₄OH/NH₄Cl' },
  { id: 'g4', label: 'Group IV: H₂S (ammoniacal)', reagent: 'H₂S + NH₄OH' },
  { id: 'g5', label: 'Group V: (NH₄)₂CO₃', reagent: '(NH₄)₂CO₃' },
  { id: 'g6', label: 'Group VI: NaOH + heat (NH₄⁺)', reagent: 'NaOH, warm' },
];

const PPT_COLORS = { pb: '#f1f5f9', cu: '#1e293b', fe: '#92400e', zn: '#e7e5e4', ca: '#f8fafc', nh4: null };

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Unknown salt — start with preliminary tests', '#8b5cf6');
  const bubbles = makeBubbles(20);

  let unknown = SALTS[Math.floor(Math.random() * SALTS.length)];
  let log = [];
  let lastEffect = null;
  let effectT = 0;
  let solved = 0;
  let t = 0;

  const panel = createPanel(stage, { title: 'Systematic Analysis' });
  panel.section('Preliminary tests');
  panel.buttonRow([
    { label: 'Look', icon: 'visibility', onClick: () => report('Appearance', unknown.appearance, false) },
    { label: 'Dry heat', icon: 'local_fire_department', onClick: () => report('Dry heating', unknown.dry, false) },
    { label: 'Flame', icon: 'whatshot', onClick: () => {
      report('Flame test', unknown.flame.label, false);
      lastEffect = { kind: 'flame', color: unknown.flame.color };
      effectT = 1;
    } },
  ]);
  panel.divider();
  panel.section('Group analysis (in order!)');
  GROUP_TESTS.forEach((g) => {
    panel.button({ label: g.label, icon: 'science', onClick: () => {
      const obs = unknown.groups[g.id];
      const hit = obs !== '—' && !obs.startsWith('No ppt') && !obs.startsWith('No ');
      report(g.label, obs === '—' ? 'No reaction observed.' : obs, hit);
      lastEffect = hit ? { kind: 'ppt', color: PPT_COLORS[unknown.id] } : { kind: 'none' };
      effectT = 1;
      if (hit && unknown.id === 'nh4') lastEffect = { kind: 'gas' };
      if (hit && unknown.id === 'ca' ) lastEffect = { kind: 'ppt', color: PPT_COLORS.ca };
    } });
  });
  panel.button({ label: 'Confirmatory test', icon: 'task_alt', onClick: () => report('Confirmatory test', unknown.confirm, true) });
  panel.divider();
  panel.select({
    label: 'Cation is…',
    options: [{ value: '', label: '— conclude —' }].concat(SALTS.map((s) => ({ value: s.id, label: s.cation }))),
    value: '',
    onChange: (v) => {
      if (!v) return;
      if (v === unknown.id) {
        solved++;
        scoreOut.set(String(solved));
        showInfoCard(stage, { title: 'Salt identified!', body: `The unknown was ${unknown.name} containing ${unknown.cation}. New sample issued — analyse it from the start.`, color: '#10b981' });
        newSalt();
      } else {
        showInfoCard(stage, { title: 'Evidence does not match', body: 'Re-check the group in which a precipitate actually appeared. Follow the scheme strictly in order — earlier groups must be NEGATIVE first.', color: '#ef4444' });
      }
    },
  });
  const scoreOut = panel.readout({ label: 'Salts solved', value: '0' });
  panel.button({ label: 'New unknown salt', icon: 'replay', variant: 'ghost', onClick: newSalt });
  panel.info('Real qualitative analysis is systematic: preliminary clues first, then group reagents strictly in order I → VI. The group where a precipitate appears tells you the cation family.');

  function newSalt() {
    unknown = SALTS[Math.floor(Math.random() * SALTS.length)];
    log = [];
    lastEffect = null;
    badge.set('Unknown salt — start with preliminary tests');
    badge.el.style.setProperty('--ix-hud-color', '#8b5cf6');
  }

  function report(test, obs, hit) {
    log.unshift({ test, obs, hit });
    if (log.length > 5) log.pop();
    badge.set(hit ? 'Positive — strong clue!' : 'Observation noted');
    badge.el.style.setProperty('--ix-hud-color', hit ? '#10b981' : '#64748b');
    showInfoCard(stage, { title: test, body: obs, color: hit ? '#10b981' : '#64748b' });
  }

  sim.setUpdate((ctx, dt, w, h) => {
    t += dt;
    if (effectT > 0) effectT = Math.max(0, effectT - dt * 0.2);

    ctx.clearRect(0, 0, w, h);
    const benchY = h * 0.88;
    ctx.fillStyle = '#3f3428';
    ctx.fillRect(0, benchY, w, h - benchY);

    const cx = w * 0.22;
    const tubeTop = h * 0.28;
    const tubeH = benchY - tubeTop - 16;
    const baseColor = unknown.id === 'cu' ? 'rgba(96,165,250,0.45)' : unknown.id === 'fe' ? 'rgba(202,138,4,0.4)' : 'rgba(203,213,225,0.22)';
    drawTestTube(ctx, cx, tubeTop, 34, tubeH, 0.55, baseColor, 'salt solution');

    if (lastEffect && effectT > 0) {
      if (lastEffect.kind === 'flame') {
        ctx.fillStyle = lastEffect.color;
        ctx.globalAlpha = effectT;
        ctx.beginPath();
        ctx.ellipse(cx, tubeTop - 30, 12, 22, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
        text(ctx, 'flame colour', cx, tubeTop - 60);
      } else if (lastEffect.kind === 'ppt' && lastEffect.color) {
        ctx.fillStyle = lastEffect.color;
        ctx.globalAlpha = 0.4 + 0.5 * (1 - effectT);
        for (let i = 0; i < 12; i++) {
          const px = cx - 11 + (i % 4) * 7;
          const py = benchY - 26 - Math.floor(i / 4) * 6 - effectT * 30 * Math.abs(Math.sin(i * 2.4));
          ctx.fillRect(px, py, 3.5, 3.5);
        }
        ctx.globalAlpha = 1;
        text(ctx, 'precipitate settles', cx + 40, benchY - 50, { align: 'left' });
      } else if (lastEffect.kind === 'gas') {
        bubbles.spawn(cx, benchY - 30, { spread: 18, top: tubeTop });
        text(ctx, 'pungent NH₃ ↑ (litmus → blue)', cx + 40, tubeTop + 30, { align: 'left', color: '#60a5fa' });
      } else {
        text(ctx, 'no change', cx + 40, tubeTop + tubeH / 2, { align: 'left', color: '#64748b' });
      }
    }

    bubbles.step(dt);
    bubbles.draw(ctx);

    const lx = w * 0.46;
    text(ctx, 'Lab notebook', lx, h * 0.08, { align: 'left', font: '700 11px Poppins, sans-serif', color: '#e2e8f0' });
    if (!log.length) text(ctx, 'record observations here', lx, h * 0.08 + 18, { align: 'left' });
    log.forEach((e, i) => {
      const y = h * 0.08 + 20 + i * 34;
      text(ctx, e.test, lx, y, { align: 'left', color: e.hit ? '#34d399' : '#94a3b8' });
      const obs = e.obs.length > 52 ? e.obs.slice(0, 52) + '…' : e.obs;
      text(ctx, obs, lx, y + 13, { align: 'left', font: '500 8.5px Poppins, sans-serif' });
    });

    text(ctx, 'Scheme: I HCl → II H₂S/H⁺ → III NH₄OH → IV H₂S/NH₃ → V (NH₄)₂CO₃ → VI NaOH', w / 2, h - 8, { font: '600 8.5px Poppins, sans-serif' });
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
