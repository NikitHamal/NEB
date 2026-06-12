import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard, hideInfoCard } from '../core/sim-ui.js';
import { drawBeaker, drawFlask, drawTestTube, drawBurette, drawBurner, drawStand, text, roundRect, GLASS } from './chem-utils.js';

const ITEMS = [
  { id: 'beaker', name: 'Beaker', use: 'Holds and mixes liquids roughly. Graduations are approximate — never use a beaker for accurate volume measurement.' },
  { id: 'conical', name: 'Conical flask', use: 'Holds the solution being titrated. The narrow neck lets you swirl without splashing — essential during titration.' },
  { id: 'burette', name: 'Burette', use: 'Delivers a variable, accurately measured volume of liquid, readable to 0.1 mL. Always read at eye level from the bottom of the meniscus.' },
  { id: 'pipette', name: 'Pipette', use: 'Delivers one fixed, very accurate volume (usually 10 or 25 mL). Fill with a pipette filler — never by mouth.' },
  { id: 'testtube', name: 'Test tube', use: 'Holds small amounts of chemicals for qualitative tests. Heat by pointing the mouth away from everyone.' },
  { id: 'burner', name: 'Bunsen burner', use: 'The lab heat source. Blue cone flame (air hole open) is hottest at ~1500 °C; yellow flame is cooler, sooty and used as the safety flame.' },
  { id: 'tripod', name: 'Tripod + wire gauze', use: 'Supports a beaker or flask above the burner. The gauze spreads the flame heat evenly so the glass does not crack.' },
  { id: 'funnel', name: 'Funnel + filter paper', use: 'Used for filtration — separating an insoluble solid (residue) from a liquid (filtrate).' },
  { id: 'wash', name: 'Wash bottle', use: 'Squeezable bottle of distilled water for rinsing apparatus and washing the last drops of solution into a flask.' },
  { id: 'watchglass', name: 'Watch glass', use: 'Shallow dish for evaporating small volumes, weighing solids or covering a beaker.' },
];

const HAZARDS = [
  { id: 'h1', label: 'No goggles', desc: 'The student is heating acid with no safety goggles. Eye protection is the first rule of the lab.' },
  { id: 'h2', label: 'Reagent bottle open near flame', desc: 'An open bottle of flammable liquid is sitting right beside the burner flame. Vapours can ignite — keep flammables away and stoppered.' },
  { id: 'h3', label: 'Tube pointing at someone', desc: 'A test tube being heated points toward a neighbour. Bumping liquid can shoot out — always point the mouth away from people.' },
  { id: 'h4', label: 'Spill not cleaned', desc: 'A chemical spill is spreading on the bench. Spills must be reported and cleaned immediately to prevent burns and slips.' },
];

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Tap any apparatus', '#059669');

  let mode = 'explore';
  let quizTarget = null;
  let quizScore = 0;
  let quizAsked = 0;
  let foundHazards = new Set();
  let flash = null;
  let t = 0;
  let zones = [];

  const panel = createPanel(stage, { title: 'Lab Bench' });
  panel.buttonRow([
    { label: 'Explore', icon: 'touch_app', onClick: () => setMode('explore') },
    { label: 'Find it!', icon: 'quiz', onClick: () => setMode('quiz') },
    { label: 'Hazards', icon: 'warning', onClick: () => setMode('hazard') },
  ]);
  panel.divider();
  const scoreOut = panel.readout({ label: 'Score', value: '—' });
  const taskOut = panel.info('Tap each piece of apparatus on the bench to learn its name and what it is used for.');

  function setMode(m) {
    mode = m;
    flash = null;
    hideInfoCard(stage);
    if (m === 'explore') {
      badge.set('Tap any apparatus');
      badge.el.style.setProperty('--ix-hud-color', '#059669');
      scoreOut.set('—');
      taskOut.set('Tap each piece of apparatus on the bench to learn its name and what it is used for.');
    } else if (m === 'quiz') {
      quizScore = 0;
      quizAsked = 0;
      nextQuiz();
      taskOut.set('Read the name in the badge, then tap that apparatus on the bench. 8 rounds — how many can you get first try?');
    } else {
      foundHazards = new Set();
      badge.set('Find 4 hazards: 0/4');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      scoreOut.set('0 / 4 found');
      taskOut.set('This bench has 4 safety problems. Tap each unsafe thing you can spot. Look for missing protection, flames, spills and bad technique.');
    }
  }

  function nextQuiz() {
    if (quizAsked >= 8) {
      badge.set(`Done! Score ${quizScore}/8`);
      badge.el.style.setProperty('--ix-hud-color', quizScore >= 6 ? '#10b981' : '#f59e0b');
      quizTarget = null;
      return;
    }
    quizTarget = ITEMS[Math.floor(Math.random() * ITEMS.length)];
    quizAsked++;
    badge.set(`Find the ${quizTarget.name} (${quizAsked}/8)`);
    badge.el.style.setProperty('--ix-hud-color', '#3b82f6');
    scoreOut.set(`${quizScore} / ${quizAsked - 1}`);
  }

  function onTap(e) {
    const p = pointerPos(sim.canvas, e);
    let hit = null;
    for (const z of zones) {
      if (p.x >= z.x && p.x <= z.x + z.w && p.y >= z.y && p.y <= z.y + z.h) { hit = z; break; }
    }
    if (!hit) return;
    if (mode === 'explore' && hit.kind === 'item') {
      const it = ITEMS.find((i) => i.id === hit.id);
      flash = { id: hit.id, t: 0.8, ok: true };
      showInfoCard(stage, { title: it.name, body: it.use, color: '#059669' });
    } else if (mode === 'quiz' && hit.kind === 'item' && quizTarget) {
      if (hit.id === quizTarget.id) {
        quizScore++;
        flash = { id: hit.id, t: 0.8, ok: true };
        scoreOut.set(`${quizScore} / ${quizAsked}`);
        nextQuiz();
      } else {
        flash = { id: hit.id, t: 0.8, ok: false };
        badge.set(`That's the ${ITEMS.find((i) => i.id === hit.id).name} — try again!`);
        badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      }
    } else if (mode === 'hazard' && hit.kind === 'hazard') {
      if (!foundHazards.has(hit.id)) {
        foundHazards.add(hit.id);
        const hz = HAZARDS.find((x) => x.id === hit.id);
        showInfoCard(stage, { title: `Hazard found: ${hz.label}`, body: hz.desc, color: '#ef4444' });
        scoreOut.set(`${foundHazards.size} / 4 found`);
        badge.set(foundHazards.size === 4 ? 'All hazards found — safe bench!' : `Find 4 hazards: ${foundHazards.size}/4`);
        badge.el.style.setProperty('--ix-hud-color', foundHazards.size === 4 ? '#10b981' : '#ef4444');
      }
    }
  }
  sim.canvas.addEventListener('pointerdown', onTap);

  function zone(id, kind, x, y, w, h) {
    zones.push({ id, kind, x, y, w, h });
  }

  sim.setUpdate((ctx, dt, w, h) => {
    t += dt;
    if (flash) { flash.t -= dt; if (flash.t <= 0) flash = null; }
    zones = [];
    ctx.clearRect(0, 0, w, h);

    const benchY = h * 0.72;
    ctx.fillStyle = '#3f3428';
    ctx.fillRect(0, benchY, w, h - benchY);
    ctx.fillStyle = 'rgba(255,255,255,0.05)';
    ctx.fillRect(0, benchY, w, 4);

    const shelfY = h * 0.3;
    ctx.fillStyle = '#33291f';
    ctx.fillRect(w * 0.04, shelfY, w * 0.92, 5);

    const u = Math.min(w / 380, h / 300);
    const s = Math.max(0.75, Math.min(1.4, u));

    const bx = w * 0.1;
    drawBeaker(ctx, bx, benchY - 52 * s, 44 * s, 52 * s, 0.5, 'rgba(96,165,250,0.4)', 'beaker');
    zone('beaker', 'item', bx - 8, benchY - 60 * s, 60 * s, 64 * s);

    const fx = w * 0.27;
    drawFlask(ctx, fx, benchY, 52 * s, 62 * s, 0.4, 'rgba(244,114,182,0.35)', 'conical flask');
    zone('conical', 'item', fx - 30 * s, benchY - 66 * s, 60 * s, 70 * s);

    const stx = w * 0.42;
    drawStand(ctx, stx, benchY - 130 * s, benchY - 5);
    drawBurette(ctx, stx + 26 * s, benchY - 128 * s, benchY - 38 * s, 0.6, 'rgba(125,211,252,0.4)');
    text(ctx, 'burette', stx + 26 * s, benchY - 14);
    zone('burette', 'item', stx + 10 * s, benchY - 132 * s, 36 * s, 110 * s);

    const px2 = w * 0.62;
    ctx.strokeStyle = GLASS;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(px2, benchY - 96 * s);
    ctx.lineTo(px2, benchY - 70 * s);
    ctx.moveTo(px2 - 5 * s, benchY - 70 * s);
    ctx.lineTo(px2 - 5 * s, benchY - 46 * s);
    ctx.lineTo(px2 + 5 * s, benchY - 46 * s);
    ctx.lineTo(px2 + 5 * s, benchY - 70 * s);
    ctx.closePath();
    ctx.moveTo(px2, benchY - 46 * s);
    ctx.lineTo(px2, benchY - 8);
    ctx.stroke();
    text(ctx, 'pipette', px2, benchY + 12);
    zone('pipette', 'item', px2 - 14, benchY - 100 * s, 28, 96 * s);

    const ttx = w * 0.74;
    drawTestTube(ctx, ttx, benchY - 54 * s, 13 * s, 50 * s, 0.45, 'rgba(52,211,153,0.4)', 'test tube');
    zone('testtube', 'item', ttx - 12, benchY - 58 * s, 24, 58 * s);

    const bnx = w * 0.88;
    drawBurner(ctx, bnx, benchY, t, true, '#60a5fa', 30 * s);
    text(ctx, 'Bunsen burner', bnx, benchY + 12);
    zone('burner', 'item', bnx - 22, benchY - 66 * s, 44, 66 * s);

    const trx = w * 0.12;
    const sy = shelfY;
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(trx - 16 * s, sy - 2);
    ctx.lineTo(trx - 11 * s, sy - 30 * s);
    ctx.lineTo(trx + 11 * s, sy - 30 * s);
    ctx.lineTo(trx + 16 * s, sy - 2);
    ctx.moveTo(trx - 14 * s, sy - 30 * s);
    ctx.lineTo(trx + 14 * s, sy - 30 * s);
    ctx.stroke();
    text(ctx, 'tripod', trx, sy - 38 * s);
    zone('tripod', 'item', trx - 20, sy - 50 * s, 40, 50 * s);

    const fnx = w * 0.34;
    ctx.strokeStyle = GLASS;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(fnx - 16 * s, sy - 34 * s);
    ctx.lineTo(fnx + 16 * s, sy - 34 * s);
    ctx.lineTo(fnx + 2, sy - 16 * s);
    ctx.lineTo(fnx + 2, sy - 2);
    ctx.moveTo(fnx - 2, sy - 16 * s);
    ctx.lineTo(fnx - 2, sy - 2);
    ctx.moveTo(fnx - 16 * s, sy - 34 * s);
    ctx.lineTo(fnx - 2, sy - 16 * s);
    ctx.stroke();
    text(ctx, 'funnel', fnx, sy - 42 * s);
    zone('funnel', 'item', fnx - 20, sy - 50 * s, 40, 50 * s);

    const wbx = w * 0.56;
    ctx.strokeStyle = 'rgba(148,233,255,0.8)';
    ctx.lineWidth = 2;
    roundRect(ctx, wbx - 11 * s, sy - 34 * s, 22 * s, 32 * s, 5);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(wbx, sy - 34 * s);
    ctx.lineTo(wbx, sy - 42 * s);
    ctx.lineTo(wbx + 12 * s, sy - 46 * s);
    ctx.stroke();
    text(ctx, 'wash bottle', wbx, sy - 52 * s);
    zone('wash', 'item', wbx - 16, sy - 56 * s, 32, 56 * s);

    const wgx = w * 0.78;
    ctx.strokeStyle = GLASS;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.ellipse(wgx, sy - 8, 20 * s, 6 * s, 0, 0, Math.PI * 2);
    ctx.stroke();
    text(ctx, 'watch glass', wgx, sy - 22 * s);
    zone('watchglass', 'item', wgx - 24, sy - 26 * s, 48, 26 * s);

    if (mode === 'hazard') {
      const fy = h * 0.1;
      ctx.font = `600 ${Math.round(16 * s)}px Poppins, sans-serif`;
      ctx.textAlign = 'center';
      ctx.fillStyle = '#fbbf24';
      ctx.fillText('🙂', w * 0.2, fy + 10);
      text(ctx, 'student (look closely!)', w * 0.2, fy + 26, { font: FONTSM() });
      zone('h1', 'hazard', w * 0.2 - 22, fy - 14, 44, 40);

      const obx = bnx - 42 * s;
      ctx.strokeStyle = '#f87171';
      ctx.lineWidth = 2;
      roundRect(ctx, obx - 9, benchY - 34 * s, 18, 32 * s, 3);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(obx - 12, benchY - 40 * s);
      ctx.lineTo(obx + 2, benchY - 34 * s);
      ctx.stroke();
      text(ctx, 'ethanol', obx, benchY - 40 * s, { color: '#f87171', font: FONTSM() });
      zone('h2', 'hazard', obx - 16, benchY - 48 * s, 32, 48 * s);

      const htx = w * 0.5;
      ctx.save();
      ctx.translate(htx, h * 0.14);
      ctx.rotate(0.5);
      drawTestTube(ctx, 0, 0, 11, 40, 0.5, 'rgba(251,146,60,0.5)');
      ctx.restore();
      text(ctx, 'heating tube →', htx - 6, h * 0.14 - 8, { color: '#f87171', font: FONTSM() });
      zone('h3', 'hazard', htx - 20, h * 0.14 - 18, 56, 60);

      const spx = w * 0.66;
      ctx.fillStyle = 'rgba(163,230,53,0.35)';
      ctx.beginPath();
      ctx.ellipse(spx, benchY + 16, 30 * s, 8 * s, 0, 0, Math.PI * 2);
      ctx.fill();
      text(ctx, 'spill', spx, benchY + 34, { color: '#f87171', font: FONTSM() });
      zone('h4', 'hazard', spx - 34, benchY + 4, 68, 28);

      foundHazards.forEach((id) => {
        const z = zones.find((zz) => zz.id === id);
        if (!z) return;
        ctx.strokeStyle = '#10b981';
        ctx.lineWidth = 2.5;
        roundRect(ctx, z.x, z.y, z.w, z.h, 6);
        ctx.stroke();
      });
    }

    if (flash) {
      const z = zones.find((zz) => zz.id === flash.id);
      if (z) {
        ctx.strokeStyle = flash.ok ? `rgba(16,185,129,${flash.t})` : `rgba(239,68,68,${flash.t})`;
        ctx.lineWidth = 3;
        roundRect(ctx, z.x - 2, z.y - 2, z.w + 4, z.h + 4, 8);
        ctx.stroke();
      }
    }
  });

  function FONTSM() { return '600 9px Poppins, sans-serif'; }

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onTap);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
