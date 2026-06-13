import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Food chain builder game — drag organisms into valid food chain
// Energy flow arrow, trophic levels, error feedback

const ORGANISMS = [
  { id: 'grass', label: 'Grass', emoji: '🌿', trophic: 1, type: 'producer', info: 'Producer — makes food from sunlight' },
  { id: 'rice', label: 'Rice plant', emoji: '🌾', trophic: 1, type: 'producer', info: 'Producer — converts CO₂ + water into starch' },
  { id: 'grasshopper', label: 'Grasshopper', emoji: '🦗', trophic: 2, type: 'primary', info: 'Primary consumer — herbivore (plant eater)' },
  { id: 'mouse', label: 'Mouse', emoji: '🐭', trophic: 2, type: 'primary', info: 'Primary consumer — herbivore' },
  { id: 'frog', label: 'Frog', emoji: '🐸', trophic: 3, type: 'secondary', info: 'Secondary consumer — eats insects' },
  { id: 'snake', label: 'Snake', emoji: '🐍', trophic: 4, type: 'tertiary', info: 'Tertiary consumer — eats frogs' },
  { id: 'hawk', label: 'Hawk', emoji: '🦅', trophic: 4, type: 'tertiary', info: 'Apex predator — top of food chain' },
  { id: 'lion', label: 'Lion', emoji: '🦁', trophic: 4, type: 'tertiary', info: 'Apex predator — top of food chain' },
  { id: 'bacteria', label: 'Bacteria', emoji: '🦠', trophic: 0, type: 'decomposer', info: 'Decomposer — breaks down dead matter, returning nutrients to soil' },
];

const VALID_CHAINS = [
  ['grass', 'grasshopper', 'frog', 'snake'],
  ['grass', 'grasshopper', 'frog', 'hawk'],
  ['grass', 'mouse', 'snake', 'hawk'],
  ['rice', 'grasshopper', 'frog', 'snake'],
  ['rice', 'mouse', 'snake', 'hawk'],
];

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const resultBadge = hud.badge('Build a food chain!', '#22c55e');

  // Chain slots (4 positions)
  const chain = [null, null, null, null];
  let dragging = null; // {orgId, startX, startY, currentX, currentY}
  let feedback = '';
  let feedbackColor = '#22c55e';
  let score = 0;
  let shake = 0;

  function validateChain() {
    if (chain.some((c) => c === null)) {
      feedback = 'Fill all 4 slots to complete the chain!';
      feedbackColor = '#94a3b8';
      return;
    }
    const ids = chain.map((c) => c.id);
    const isValid = VALID_CHAINS.some((vc) => vc.every((id, i) => ids[i] === id));
    if (isValid) {
      feedback = 'Correct food chain! Energy flows from left to right.';
      feedbackColor = '#22c55e';
      resultBadge.set('Correct chain!');
      score++;
    } else {
      // Check if each arrow direction makes sense (trophic order)
      const orgs = chain.map((c) => ORGANISMS.find((o) => o.id === c.id));
      let errorMsg = '';
      if (orgs[0] && orgs[0].trophic !== 1) {
        errorMsg = `${orgs[0].label} is not a producer! A food chain must start with a plant.`;
      } else {
        for (let i = 1; i < 4; i++) {
          if (orgs[i] && orgs[i - 1] && orgs[i].trophic <= orgs[i - 1].trophic) {
            errorMsg = `${orgs[i].label} doesn't eat ${orgs[i - 1].label}. Fix the order!`;
            break;
          }
        }
        if (!errorMsg) errorMsg = 'Almost! This specific combination isn\'t quite right. Try different organisms.';
      }
      feedback = errorMsg;
      feedbackColor = '#ef4444';
      resultBadge.set('Not quite — try again!');
      shake = 0.5;
    }
  }

  const panel = createPanel(stage, { title: 'Food Chain Builder' });
  panel.info('Drag organisms from the bank into the 4 chain slots (left to right = producer → apex predator). Check your chain when ready!');
  panel.button({
    label: 'Check my chain',
    icon: 'check_circle',
    variant: 'primary',
    onClick: validateChain,
  });
  panel.button({
    label: 'Clear chain',
    icon: 'backspace',
    onClick: () => { chain.fill(null); feedback = ''; resultBadge.set('Build a food chain!'); },
  });
  const scoreOut = panel.readout({ label: 'Correct chains', value: '0' });
  panel.divider();
  // Show organism info
  ORGANISMS.filter((o) => o.trophic !== 0).forEach((o) => {
    panel.info(`${o.emoji} ${o.label}: ${o.info}`);
  });

  // Layout helpers
  function getSlotPositions(w, h) {
    const slotY = h * 0.35;
    const slotW = w * 0.16;
    const spacing = w * 0.19;
    return chain.map((_, i) => ({
      x: w * 0.08 + i * spacing,
      y: slotY,
      w: slotW,
      h: 54,
    }));
  }

  function getOrgPositions(w, h) {
    const bankY = h * 0.65;
    const orgW = w * 0.12;
    const cols = Math.floor(w / (orgW + 8));
    const bankOrgs = ORGANISMS.filter((o) => o.trophic > 0);
    return bankOrgs.map((org, i) => ({
      org,
      x: 8 + (i % cols) * (orgW + 8),
      y: bankY + Math.floor(i / cols) * 62,
      w: orgW,
      h: 54,
    }));
  }

  function onPointerDown(e) {
    const pos = pointerPos(sim.canvas, e);
    const orgPositions = getOrgPositions(sim.width, sim.height);
    // Check if clicking on an organism in the bank
    for (const op of orgPositions) {
      if (pos.x >= op.x && pos.x <= op.x + op.w && pos.y >= op.y && pos.y <= op.y + op.h) {
        dragging = { orgId: op.org.id, startX: pos.x, startY: pos.y, currentX: pos.x, currentY: pos.y };
        sim.canvas.setPointerCapture && sim.canvas.setPointerCapture(e.pointerId);
        return;
      }
    }
    // Check if clicking on filled chain slot (to remove)
    const slots = getSlotPositions(sim.width, sim.height);
    for (let i = 0; i < slots.length; i++) {
      const s = slots[i];
      if (chain[i] && pos.x >= s.x && pos.x <= s.x + s.w && pos.y >= s.y && pos.y <= s.y + s.h) {
        dragging = { orgId: chain[i].id, startX: pos.x, startY: pos.y, currentX: pos.x, currentY: pos.y };
        chain[i] = null;
        feedback = '';
        return;
      }
    }
  }

  function onPointerMove(e) {
    if (!dragging) return;
    const pos = pointerPos(sim.canvas, e);
    dragging.currentX = pos.x;
    dragging.currentY = pos.y;
  }

  function onPointerUp(e) {
    if (!dragging) return;
    const pos = pointerPos(sim.canvas, e);
    const slots = getSlotPositions(sim.width, sim.height);
    let placed = false;
    for (let i = 0; i < slots.length; i++) {
      const s = slots[i];
      if (pos.x >= s.x - 10 && pos.x <= s.x + s.w + 10 && pos.y >= s.y - 10 && pos.y <= s.y + s.h + 10) {
        const org = ORGANISMS.find((o) => o.id === dragging.orgId);
        chain[i] = org;
        placed = true;
        feedback = '';
        break;
      }
    }
    dragging = null;
    scoreOut.set(String(score));
  }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onPointerDown);
  sim.canvas.addEventListener('pointermove', onPointerMove);
  sim.canvas.addEventListener('pointerup', onPointerUp);
  sim.canvas.addEventListener('pointercancel', onPointerUp);

  sim.setUpdate((ctx, dt, w, h) => {
    if (shake > 0) shake = Math.max(0, shake - dt * 3);

    ctx.clearRect(0, 0, w, h);

    const bg = ctx.createLinearGradient(0, 0, 0, h);
    bg.addColorStop(0, '#071510');
    bg.addColorStop(1, '#040d08');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);

    ctx.fillStyle = 'rgba(150,230,160,0.85)';
    ctx.font = '700 12px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('Food Chain Builder', 10, 18);

    // Energy flow label
    ctx.fillStyle = 'rgba(250,200,60,0.7)';
    ctx.font = '600 9px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('← Energy flows this way →', w * 0.42, h * 0.24);

    // Trophic level labels
    const tLevels = ['Producer\n(Trophic 1)', 'Primary\nConsumer', 'Secondary\nConsumer', 'Apex\nPredator'];
    const slots = getSlotPositions(w, h);
    const shakeX = shake > 0 ? Math.sin(shake * 40) * 5 : 0;

    slots.forEach((s, i) => {
      const sx = s.x + shakeX * (chain[i] ? 1 : 0);

      // Level label
      ctx.fillStyle = 'rgba(180,220,180,0.6)';
      ctx.font = '600 8px Poppins, sans-serif';
      ctx.textAlign = 'center';
      tLevels[i].split('\n').forEach((line, li) => {
        ctx.fillText(line, sx + s.w / 2, s.y - 22 + li * 11);
      });

      // Slot box
      ctx.fillStyle = chain[i] ? 'rgba(30,70,30,0.8)' : 'rgba(20,40,20,0.5)';
      ctx.strokeStyle = chain[i] ? '#22c55e' : 'rgba(100,180,100,0.4)';
      ctx.lineWidth = 2;
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(sx, s.y, s.w, s.h, 8);
      else ctx.rect(sx, s.y, s.w, s.h);
      ctx.fill();
      ctx.stroke();

      if (chain[i]) {
        const org = chain[i];
        ctx.font = '22px serif';
        ctx.textAlign = 'center';
        ctx.fillText(org.emoji, sx + s.w / 2, s.y + 26);
        ctx.fillStyle = '#ffffff';
        ctx.font = '600 9px Poppins, sans-serif';
        ctx.fillText(org.label, sx + s.w / 2, s.y + 46);
      } else {
        ctx.fillStyle = 'rgba(120,180,120,0.4)';
        ctx.font = '600 9px Poppins, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('Drop here', sx + s.w / 2, s.y + s.h / 2 + 4);
      }

      // Arrow between slots
      if (i < 3) {
        const arrowX = sx + s.w + 8;
        const arrowY = s.y + s.h / 2;
        ctx.strokeStyle = 'rgba(250,200,60,0.5)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(arrowX - 2, arrowY);
        ctx.lineTo(arrowX + spacing - s.w - 16, arrowY);
        ctx.stroke();
        ctx.fillStyle = 'rgba(250,200,60,0.5)';
        ctx.beginPath();
        ctx.moveTo(arrowX + spacing - s.w - 14, arrowY);
        ctx.lineTo(arrowX + spacing - s.w - 22, arrowY - 5);
        ctx.lineTo(arrowX + spacing - s.w - 22, arrowY + 5);
        ctx.closePath();
        ctx.fill();
      }
    });

    // spacing helper used in arrow drawing (recompute here)
    const spacing = w * 0.19;

    // Organism bank
    const bankY = h * 0.6;
    ctx.fillStyle = 'rgba(8,20,8,0.7)';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(4, bankY, w - 8, h * 0.34, 8);
    else ctx.rect(4, bankY, w - 8, h * 0.34);
    ctx.fill();
    ctx.fillStyle = 'rgba(120,200,120,0.6)';
    ctx.font = '600 9px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('Organism bank — drag to chain:', 10, bankY + 12);

    const orgPositions = getOrgPositions(w, h);
    orgPositions.forEach((op) => {
      const isDragging = dragging && dragging.orgId === op.org.id;
      ctx.fillStyle = isDragging ? 'rgba(50,100,50,0.5)' : 'rgba(20,50,20,0.7)';
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(op.x, op.y, op.w, op.h, 6);
      else ctx.rect(op.x, op.y, op.w, op.h);
      ctx.fill();
      ctx.stroke();
      ctx.font = '18px serif';
      ctx.textAlign = 'center';
      ctx.fillText(op.org.emoji, op.x + op.w / 2, op.y + 22);
      ctx.fillStyle = 'rgba(200,240,200,0.85)';
      ctx.font = '600 8px Poppins, sans-serif';
      ctx.fillText(op.org.label, op.x + op.w / 2, op.y + 36);
      // Trophic level
      ctx.fillStyle = 'rgba(150,210,150,0.55)';
      ctx.font = '600 7px Poppins, sans-serif';
      ctx.fillText(`T${op.org.trophic}`, op.x + op.w / 2, op.y + 48);
    });

    // Dragging ghost
    if (dragging) {
      const dragOrg = ORGANISMS.find((o) => o.id === dragging.orgId);
      ctx.globalAlpha = 0.7;
      ctx.fillStyle = 'rgba(50,120,50,0.8)';
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth = 2;
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(dragging.currentX - 30, dragging.currentY - 25, 60, 52, 6);
      else ctx.rect(dragging.currentX - 30, dragging.currentY - 25, 60, 52);
      ctx.fill();
      ctx.stroke();
      ctx.font = '20px serif';
      ctx.textAlign = 'center';
      ctx.fillText(dragOrg.emoji, dragging.currentX, dragging.currentY + 4);
      ctx.globalAlpha = 1;
    }

    // Feedback
    if (feedback) {
      const fbY = h * 0.52;
      ctx.fillStyle = 'rgba(8,20,8,0.8)';
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(8, fbY, w - 16, 26, 6);
      else ctx.rect(8, fbY, w - 16, 26);
      ctx.fill();
      ctx.fillStyle = feedbackColor;
      ctx.font = '600 10px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(feedback, w / 2, fbY + 17);
    }
  });

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onPointerDown);
      sim.canvas.removeEventListener('pointermove', onPointerMove);
      sim.canvas.removeEventListener('pointerup', onPointerUp);
      sim.canvas.removeEventListener('pointercancel', onPointerUp);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
