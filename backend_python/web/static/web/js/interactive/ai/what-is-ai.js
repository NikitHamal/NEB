import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { roundRect, labelText } from '../biology/bio-utils.js';

// Items to sort. ring = where it belongs: 'ai', 'ml', or 'dl'.
const ITEMS = [
  { label: 'Chess engine (searches millions of moves)', ring: 'ai' },
  { label: 'Spam filter learning from emails', ring: 'ml' },
  { label: 'ChatGPT writing an essay', ring: 'dl' },
  { label: 'Face unlock on your phone', ring: 'dl' },
  { label: 'Calculator doing 2+2', ring: null },
  { label: 'Route planner (Dijkstra shortest path)', ring: 'ai' },
  { label: 'YouTube video recommender', ring: 'ml' },
  { label: 'Self-driving car vision system', ring: 'dl' },
  { label: 'Thermostat switching on at 7am', ring: null },
  { label: 'Image generator (DALL·E / Midjourney)', ring: 'dl' },
  { label: 'Weather forecast from past data', ring: 'ml' },
  { label: 'A digital clock', ring: null },
];

const RINGS = [
  { id: 'ai', label: 'AI', color: '#6366F1', desc: 'Any technique that makes a machine seem to think — including rule-based systems.' },
  { id: 'ml', label: 'Machine Learning', color: '#8B5CF6', desc: 'Systems that learn patterns from data instead of following hand-written rules.' },
  { id: 'dl', label: 'Deep Learning', color: '#EC4899', desc: 'Machine learning using many-layered neural networks — the engine of modern AI.' },
];

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const scoreBadge = hud.badge('Sorted: 0', '#a3e635');

  // Shuffle items, pick 6
  const deck = ITEMS.slice().sort(() => Math.random() - 0.5).slice(0, 6).map((it, i) => ({
    ...it, x: 0, y: 0, w: 0, h: 0, placed: null, id: i,
  }));

  // Card layout: left stack of cards, three ring dropzones on the right
  const cardW = 250; const cardH = 52;
  function layout(w, h) {
    // rings on the right
    const ringCx = w * 0.68;
    const ringCy = h * 0.5;
    const radii = [h * 0.42, h * 0.30, h * 0.18];
    // card stack on the left
    const stackX = w * 0.13;
    const stackY = h * 0.18;
    deck.forEach((c, i) => {
      if (!c.placed) {
        c.x = stackX; c.y = stackY + i * (cardH + 8); c.w = cardW; c.h = cardH;
      }
    });
    return { ringCx, ringCy, radii };
  }

  let dragging = null; let dragOff = { x: 0, y: 0 };
  let mouseX = 0; let mouseY = 0;

  function onDown(e) {
    const p = pointerPos(sim.canvas, e);
    mouseX = p.x; mouseY = p.y;
    // topmost card under pointer (from top of stack)
    for (let i = deck.length - 1; i >= 0; i--) {
      const c = deck[i];
      if (c.placed) continue;
      if (p.x >= c.x && p.x <= c.x + c.w && p.y >= c.y && p.y <= c.y + c.h) {
        dragging = c; dragOff = { x: p.x - c.x, y: p.y - c.y };
        if (sim.canvas.setPointerCapture) sim.canvas.setPointerCapture(e.pointerId);
        break;
      }
    }
  }
  function onMove(e) {
    const p = pointerPos(sim.canvas, e);
    mouseX = p.x; mouseY = p.y;
    if (dragging) { dragging.x = p.x - dragOff.x; dragging.y = p.y - dragOff.y; }
  }
  function onUp(e) {
    if (!dragging) return;
    const { ringCx, ringCy, radii } = layout(sim.width, sim.height);
    const dx = (dragging.x + dragging.w / 2) - ringCx;
    const dy = (dragging.y + dragging.h / 2) - ringCy;
    const dist = Math.hypot(dx, dy);
    // which ring? inside outer ring required; pick innermost that contains it
    let ring = null;
    if (dist <= radii[0]) {
      ring = 'dl';
      if (dist <= radii[2]) ring = 'dl';
      else if (dist <= radii[1]) ring = 'ml';
      else ring = 'ai';
    }
    if (ring) {
      dragging.placed = ring;
      const correct = dragging.ring === ring;
      showInfoCard(stage, {
        title: correct ? 'Correct! ✓' : 'Not quite',
        body: correct
          ? `${dragging.label} — belongs in ${RINGS.find((r) => r.id === ring).label}. ${RINGS.find((r) => r.id === ring).desc}`
          : `${dragging.label} is actually ${dragging.ring ? RINGS.find((r) => r.id === dragging.ring).label : 'not AI at all'} — it was dragged into ${RINGS.find((r) => r.id === ring).label}.`,
        color: correct ? '#a3e635' : '#f87171',
      });
      const placed = deck.filter((c) => c.placed).length;
      scoreBadge.set(`Sorted: ${placed}/${deck.length}`);
    } else {
      // return to stack
    }
    dragging = null;
  }
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);

  const panel = createPanel(stage, { title: 'What Is AI?' });
  panel.info('Drag each card into the ring where it belongs. AI is the big umbrella; ML learns from data; deep learning uses neural networks. Some cards are not AI at all — drag those off the rings.');
  panel.button({ label: 'New round', icon: 'refresh', onClick: () => {
    const shuffled = ITEMS.slice().sort(() => Math.random() - 0.5).slice(0, 6);
    deck.forEach((c, i) => { Object.assign(c, shuffled[i]); c.placed = null; });
    scoreBadge.set('Sorted: 0');
  } });
  panel.divider();
  panel.readout({ label: 'AI', value: 'Machines that seem to think' });
  panel.readout({ label: 'ML', value: 'Learns from data' });
  panel.readout({ label: 'DL', value: 'Deep neural networks' });
  panel.button({ label: 'Reveal the nesting', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'The three nested circles',
      body: 'AI is the broadest field. Inside AI sits machine learning (systems that learn from data). Inside ML sits deep learning (learning with many-layered neural networks). So all deep learning is ML, and all ML is AI — but not the other way round.',
      color: '#6366F1',
    });
  } });

  sim.setUpdate((ctx) => {
    const { width: w, height: h } = sim;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#070a14'; ctx.fillRect(0, 0, w, h);
    const { ringCx, ringCy, radii } = layout(w, h);

    // Draw the three nested rings (concentric, AI outer, ML mid, DL inner)
    const colors = { ai: '#6366F1', ml: '#8B5CF6', dl: '#EC4899' };
    [['ai', 0], ['ml', 1], ['dl', 2]].forEach(([id, idx]) => {
      ctx.fillStyle = hexA(colors[id], 0.10 + idx * 0.05);
      ctx.strokeStyle = colors[id]; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(ringCx, ringCy, radii[idx], 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      labelText(ctx, RINGS[idx].label, ringCx - radii[idx] + 14, ringCy - radii[idx] + 18,
        { color: colors[id], size: 13 });
    });
    // center label
    labelText(ctx, 'DEEP', ringCx, ringCy - 4, { color: '#fff', size: 14, align: 'center' });
    labelText(ctx, 'LEARNING', ringCx, ringCy + 12, { color: '#fff', size: 14, align: 'center' });

    // Drop hint at cursor when dragging
    if (dragging) {
      const dx = (dragging.x + dragging.w / 2) - ringCx;
      const dy = (dragging.y + dragging.h / 2) - ringCy;
      const dist = Math.hypot(dx, dy);
      if (dist <= radii[0]) {
        ctx.strokeStyle = '#a3e635'; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.arc(ringCx, ringCy, radii[0], 0, Math.PI * 2); ctx.stroke();
      }
    }

    // Draw cards (placed ones shrink into the ring)
    deck.forEach((c) => {
      if (c.placed) {
        // small chip inside its ring
        const ringIdx = RINGS.findIndex((r) => r.id === c.placed);
        const placed = deck.filter((x) => x.placed === c.placed);
        const myIdx = placed.indexOf(c);
        const ang = (myIdx / Math.max(1, placed.length)) * Math.PI * 2 - Math.PI / 2;
        const rr = radii[ringIdx] * 0.55;
        c.x = ringCx + Math.cos(ang) * rr - 60;
        c.y = ringCy + Math.sin(ang) * rr - 12;
        c.w = 120; c.h = 24;
        drawCard(ctx, c, c.placed === c.ring);
      } else {
        c.w = cardW; c.h = cardH;
        drawCard(ctx, c, null);
      }
    });
  });

  function drawCard(ctx, c, correct) {
    const border = correct === true ? '#a3e635' : correct === false ? '#f87171' : '#3b4252';
    ctx.fillStyle = correct === false ? 'rgba(248,113,113,0.12)' : 'rgba(99,102,241,0.14)';
    ctx.strokeStyle = border; ctx.lineWidth = dragging === c ? 2.5 : 1.5;
    roundRect(ctx, c.x, c.y, c.w, c.h, 8); ctx.fill(); ctx.stroke();
    labelText(ctx, c.label, c.x + 10, c.y + c.h / 2 + 4, { color: '#e2e8f0', size: c.h > 30 ? 12 : 10 });
  }

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onDown);
      sim.canvas.removeEventListener('pointermove', onMove);
      sim.canvas.removeEventListener('pointerup', onUp);
      panel.dispose(); hud.dispose(); sim.dispose();
    },
  };
}

function hexA(hex, a) {
  const n = parseInt(hex.slice(1), 16);
  const r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
  return `rgba(${r},${g},${b},${a})`;
}
