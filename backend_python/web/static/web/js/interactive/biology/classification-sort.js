import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Classification sort game — drag living things into correct groups
// Accurate traits for each group

const ORGANISMS = [
  { id: 'dog', emoji: '🐶', name: 'Dog', group: 'mammals', trait: 'Has fur, feeds young with milk, warm-blooded' },
  { id: 'whale', emoji: '🐋', name: 'Whale', group: 'mammals', trait: 'Breathes air, warm-blooded, gives live birth' },
  { id: 'bat', emoji: '🦇', name: 'Bat', group: 'mammals', trait: 'Only flying mammal, has fur, feeds pups with milk' },
  { id: 'eagle', emoji: '🦅', name: 'Eagle', group: 'birds', trait: 'Has feathers, wings, lays eggs, warm-blooded' },
  { id: 'penguin', emoji: '🐧', name: 'Penguin', group: 'birds', trait: 'Has feathers, cannot fly, lays eggs' },
  { id: 'parrot', emoji: '🦜', name: 'Parrot', group: 'birds', trait: 'Has feathers, beak, lays eggs in nests' },
  { id: 'salmon', emoji: '🐟', name: 'Salmon', group: 'fish', trait: 'Has scales, gills, fins, cold-blooded, lives in water' },
  { id: 'shark', emoji: '🦈', name: 'Shark', group: 'fish', trait: 'Has cartilage skeleton, gills, cold-blooded' },
  { id: 'clownfish', emoji: '🐠', name: 'Clownfish', group: 'fish', trait: 'Has scales, gills, fins, cold-blooded' },
  { id: 'ant', emoji: '🐜', name: 'Ant', group: 'insects', trait: '6 legs, 3 body segments, exoskeleton, antennae' },
  { id: 'butterfly2', emoji: '🦋', name: 'Butterfly', group: 'insects', trait: '6 legs, 3 body segments, wings, complete metamorphosis' },
  { id: 'bee', emoji: '🐝', name: 'Bee', group: 'insects', trait: '6 legs, 3 body segments, wings, antennae' },
  { id: 'rose', emoji: '🌹', name: 'Rose', group: 'plants', trait: 'Makes own food (photosynthesis), has roots, stem, leaves' },
  { id: 'cactus', emoji: '🌵', name: 'Cactus', group: 'plants', trait: 'Makes food from sunlight, stores water in stem' },
  { id: 'tree', emoji: '🌳', name: 'Tree', group: 'plants', trait: 'Makes food by photosynthesis, woody stem (trunk)' },
];

const GROUPS = [
  { id: 'mammals', label: 'Mammals', emoji: '🦁', color: '#f59e0b', trait: 'Fur • Warm-blooded • Milk' },
  { id: 'birds', label: 'Birds', emoji: '🐦', color: '#7dd3fc', trait: 'Feathers • Warm-blooded • Eggs' },
  { id: 'fish', label: 'Fish', emoji: '🐟', color: '#60a5fa', trait: 'Scales • Gills • Cold-blooded' },
  { id: 'insects', label: 'Insects', emoji: '🦗', color: '#a3e635', trait: '6 legs • 3 body parts • Exoskeleton' },
  { id: 'plants', label: 'Plants', emoji: '🌿', color: '#22c55e', trait: 'Photosynthesis • Roots & leaves' },
];

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const scoreBadge = hud.badge('Score: 0 / 15', '#22c55e');

  // Shuffle organisms
  const organisms = [...ORGANISMS].sort(() => Math.random() - 0.5);
  const sorted = new Map(); // orgId → groupId (correct placements)
  const wrong = new Set();
  let dragging = null;
  let score = 0;
  let feedback = '';
  let feedbackColor = '#22c55e';
  let feedbackTimer = 0;

  const panel = createPanel(stage, { title: 'Classification Game' });
  panel.info('Drag each organism into the correct group box. Remember: mammals have fur, birds have feathers, fish have gills, insects have 6 legs, plants make their own food!');
  panel.button({
    label: 'New game',
    icon: 'shuffle',
    onClick: () => {
      organisms.sort(() => Math.random() - 0.5);
      sorted.clear();
      wrong.clear();
      score = 0;
      feedback = '';
      scoreBadge.set('Score: 0 / 15');
    },
  });

  // Layout
  function getGroupBoxes(w, h) {
    const boxW = w * 0.18;
    const boxH = h * 0.22;
    const spacing = (w - GROUPS.length * boxW) / (GROUPS.length + 1);
    return GROUPS.map((g, i) => ({
      group: g,
      x: spacing + i * (boxW + spacing),
      y: h * 0.06,
      w: boxW,
      h: boxH,
    }));
  }

  function getOrgCards(w, h) {
    const cardW = w * 0.11;
    const cardH = h * 0.1;
    const cols = Math.floor(w / (cardW + 6));
    return organisms
      .filter((o) => !sorted.has(o.id))
      .map((o, i) => ({
        org: o,
        x: 6 + (i % cols) * (cardW + 6),
        y: h * 0.35 + Math.floor(i / cols) * (cardH + 6),
        w: cardW,
        h: cardH,
      }));
  }

  function onPointerDown(e) {
    const pos = pointerPos(sim.canvas, e);
    const cards = getOrgCards(sim.width, sim.height);
    for (const card of cards) {
      if (pos.x >= card.x && pos.x <= card.x + card.w && pos.y >= card.y && pos.y <= card.y + card.h) {
        dragging = { orgId: card.org.id, currentX: pos.x, currentY: pos.y };
        sim.canvas.setPointerCapture && sim.canvas.setPointerCapture(e.pointerId);
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
    const boxes = getGroupBoxes(sim.width, sim.height);
    const org = ORGANISMS.find((o) => o.id === dragging.orgId);
    let placed = false;
    for (const box of boxes) {
      if (pos.x >= box.x && pos.x <= box.x + box.w && pos.y >= box.y && pos.y <= box.y + box.h) {
        if (org.group === box.group.id) {
          sorted.set(org.id, box.group.id);
          wrong.delete(org.id);
          score++;
          feedback = `✓ Correct! ${org.name} is a ${box.group.label}. ${org.trait}`;
          feedbackColor = '#22c55e';
          scoreBadge.set(`Score: ${score} / ${ORGANISMS.length}`);
        } else {
          wrong.add(org.id);
          feedback = `✗ Not quite! ${org.name} belongs with the ${GROUPS.find((g) => g.id === org.group).label}. Hint: ${org.trait}`;
          feedbackColor = '#ef4444';
        }
        feedbackTimer = 3.5;
        placed = true;
        break;
      }
    }
    dragging = null;
  }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onPointerDown);
  sim.canvas.addEventListener('pointermove', onPointerMove);
  sim.canvas.addEventListener('pointerup', onPointerUp);
  sim.canvas.addEventListener('pointercancel', onPointerUp);

  sim.setUpdate((ctx, dt, w, h) => {
    if (feedbackTimer > 0) feedbackTimer -= dt;

    ctx.clearRect(0, 0, w, h);

    const bg = ctx.createLinearGradient(0, 0, 0, h);
    bg.addColorStop(0, '#071510');
    bg.addColorStop(1, '#040d08');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);

    ctx.fillStyle = 'rgba(150,230,160,0.85)';
    ctx.font = '700 12px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('Classification Sort', 10, 18);

    // Group boxes
    const boxes = getGroupBoxes(w, h);
    boxes.forEach((box) => {
      const g = box.group;
      const contents = [...sorted.entries()].filter(([_, gid]) => gid === g.id);

      ctx.fillStyle = `${g.color}22`;
      ctx.strokeStyle = `${g.color}88`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(box.x, box.y, box.w, box.h, 8);
      else ctx.rect(box.x, box.y, box.w, box.h);
      ctx.fill();
      ctx.stroke();

      // Group label
      ctx.fillStyle = g.color;
      ctx.font = '700 10px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`${g.emoji} ${g.label}`, box.x + box.w / 2, box.y + 14);
      ctx.fillStyle = `${g.color}99`;
      ctx.font = '600 7.5px Poppins, sans-serif';
      ctx.fillText(g.trait, box.x + box.w / 2, box.y + 25);

      // Show sorted organisms in box
      contents.forEach(([orgId], i) => {
        const o = ORGANISMS.find((x) => x.id === orgId);
        ctx.font = '13px serif';
        ctx.textAlign = 'center';
        ctx.fillText(o.emoji, box.x + 14 + (i % 3) * 18, box.y + 40 + Math.floor(i / 3) * 18);
      });

      // Count badge
      ctx.fillStyle = g.color;
      ctx.font = '600 8px Poppins, sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText(`${contents.length}/3`, box.x + box.w - 4, box.y + box.h - 4);
    });

    // Organism cards
    const cards = getOrgCards(w, h);
    cards.forEach((card) => {
      const o = card.org;
      const isWrong = wrong.has(o.id);
      const isDragging = dragging && dragging.orgId === o.id;

      if (isDragging) return; // draw ghost instead

      ctx.fillStyle = isWrong ? 'rgba(80,20,20,0.8)' : 'rgba(20,50,20,0.8)';
      ctx.strokeStyle = isWrong ? '#ef4444' : '#22c55e';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(card.x, card.y, card.w, card.h, 6);
      else ctx.rect(card.x, card.y, card.w, card.h);
      ctx.fill();
      ctx.stroke();

      ctx.font = '18px serif';
      ctx.textAlign = 'center';
      ctx.fillText(o.emoji, card.x + card.w / 2, card.y + 24);
      ctx.fillStyle = 'rgba(200,240,200,0.9)';
      ctx.font = '600 8px Poppins, sans-serif';
      ctx.fillText(o.name, card.x + card.w / 2, card.y + card.h - 6);
    });

    // Dragging ghost
    if (dragging) {
      const o = ORGANISMS.find((x) => x.id === dragging.orgId);
      ctx.globalAlpha = 0.75;
      ctx.fillStyle = 'rgba(40,100,40,0.9)';
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth = 2;
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(dragging.currentX - 30, dragging.currentY - 28, 60, 52, 6);
      else ctx.rect(dragging.currentX - 30, dragging.currentY - 28, 60, 52);
      ctx.fill();
      ctx.stroke();
      ctx.font = '22px serif';
      ctx.textAlign = 'center';
      ctx.fillText(o.emoji, dragging.currentX, dragging.currentY + 4);
      ctx.globalAlpha = 1;
    }

    // Feedback
    if (feedbackTimer > 0 && feedback) {
      const fbY = h * 0.28;
      ctx.fillStyle = 'rgba(8,20,8,0.88)';
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(6, fbY, w - 12, 28, 6);
      else ctx.rect(6, fbY, w - 12, 28);
      ctx.fill();
      ctx.fillStyle = feedbackColor;
      ctx.font = '600 9.5px Poppins, sans-serif';
      ctx.textAlign = 'center';
      // Truncate if too long
      let fbText = feedback;
      while (ctx.measureText(fbText).width > w - 20 && fbText.length > 20) {
        fbText = fbText.slice(0, -4) + '…';
      }
      ctx.fillText(fbText, w / 2, fbY + 18);
    }

    // Win message
    if (score === ORGANISMS.length) {
      ctx.fillStyle = 'rgba(8,20,8,0.92)';
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(w * 0.2, h * 0.4, w * 0.6, 60, 10);
      else ctx.rect(w * 0.2, h * 0.4, w * 0.6, 60);
      ctx.fill();
      ctx.fillStyle = '#22c55e';
      ctx.font = '700 16px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('🎉 Amazing! All sorted correctly!', w / 2, h * 0.4 + 28);
      ctx.fillStyle = 'rgba(200,240,200,0.8)';
      ctx.font = '600 11px Poppins, sans-serif';
      ctx.fillText('Press "New game" to play again with a new shuffle!', w / 2, h * 0.4 + 48);
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
