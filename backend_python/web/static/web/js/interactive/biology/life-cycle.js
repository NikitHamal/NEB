import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Butterfly and frog life cycle — interactive timeline
// Accurate metamorphosis stages

const CYCLES = {
  butterfly: {
    label: 'Butterfly (Complete Metamorphosis)',
    color: '#f9a8d4',
    stages: [
      {
        name: 'Egg',
        emoji: '🥚',
        duration: '3-7 days',
        info: 'The butterfly lays tiny round eggs on a leaf. The egg has a hard shell to protect the growing larva inside. The eggs are sticky so they don\'t fall off the leaf in wind or rain.',
      },
      {
        name: 'Caterpillar (Larva)',
        emoji: '🐛',
        duration: '2-4 weeks',
        info: 'A tiny caterpillar hatches from the egg and eats leaves non-stop! It grows so fast it must shed its skin (moult) several times. The caterpillar\'s only job is to eat and grow.',
      },
      {
        name: 'Pupa (Chrysalis)',
        emoji: '🫘',
        duration: '1-2 weeks',
        info: 'Inside the chrysalis, the caterpillar\'s body breaks down completely and is rebuilt as a butterfly — organs, wings and all. This amazing transformation is called metamorphosis.',
      },
      {
        name: 'Adult Butterfly',
        emoji: '🦋',
        duration: 'Days to months',
        info: 'The adult butterfly emerges with crumpled wings, which it pumps with fluid to expand. Adults drink nectar with a long tube (proboscis) and find mates to lay eggs — starting the cycle again!',
      },
    ],
  },
  frog: {
    label: 'Frog (Amphibian Metamorphosis)',
    color: '#86efac',
    stages: [
      {
        name: 'Egg (Spawn)',
        emoji: '🫧',
        duration: '1-3 weeks',
        info: 'Frogs lay hundreds of eggs in water, protected by a jelly coat. The jelly keeps eggs together (frogspawn), protects from bacteria, and acts as a lens to focus sunlight for warmth.',
      },
      {
        name: 'Tadpole',
        emoji: '🐟',
        duration: '6-9 weeks',
        info: 'Tadpoles hatch and breathe through gills like fish. They have long tails for swimming and eat algae. Over weeks they slowly change — growing legs, developing lungs, and the tail begins to shrink.',
      },
      {
        name: 'Froglet',
        emoji: '🐸',
        duration: '3-6 weeks',
        info: 'The froglet has four legs and a shrinking tail. It can breathe both in water (through skin and some gills) and in air (through lungs). It spends time near the water\'s edge.',
      },
      {
        name: 'Adult Frog',
        emoji: '🐸',
        duration: '1-5 years',
        info: 'The adult frog has no tail, breathes with lungs, and has a sticky tongue to catch insects. It lives on land but returns to water to mate and lay eggs — continuing the cycle!',
      },
    ],
  },
};

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const cycleBadge = hud.badge('Butterfly Cycle', '#f9a8d4');

  let activeAnimal = 'butterfly';
  let selectedStage = 0;
  let animT = 0;

  const panel = createPanel(stage, { title: 'Life Cycle' });
  panel.buttonRow([
    { label: '🦋 Butterfly', onClick: () => { activeAnimal = 'butterfly'; selectedStage = 0; cycleBadge.set('Butterfly Cycle'); } },
    { label: '🐸 Frog', onClick: () => { activeAnimal = 'frog'; selectedStage = 0; cycleBadge.set('Frog Cycle'); } },
  ]);
  panel.divider();
  panel.info('Click any stage on the wheel to learn about it. Use the animal buttons to switch between butterfly and frog metamorphosis.');

  // Auto-advance button
  let autoPlay = false;
  let autoTimer = 0;
  const autoToggle = panel.toggle({
    label: 'Auto-advance stages',
    value: false,
    onChange: (v) => { autoPlay = v; autoTimer = 0; },
  });

  function onCanvasClick(e) {
    const rect = sim.canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const w = sim.width;
    const h = sim.height;
    const cycle = CYCLES[activeAnimal];
    const cx = w * 0.5;
    const cy = h * 0.42;
    const radius = Math.min(w, h) * 0.3;
    cycle.stages.forEach((s, i) => {
      const angle = (i / cycle.stages.length) * Math.PI * 2 - Math.PI / 2;
      const sx = cx + Math.cos(angle) * radius;
      const sy = cy + Math.sin(angle) * radius;
      if (Math.hypot(mx - sx, my - sy) < 36) {
        selectedStage = i;
      }
    });
  }

  sim.canvas.addEventListener('click', onCanvasClick);

  sim.setUpdate((ctx, dt, w, h) => {
    animT += dt;
    if (autoPlay) {
      autoTimer += dt;
      if (autoTimer > 3.5) {
        autoTimer = 0;
        selectedStage = (selectedStage + 1) % CYCLES[activeAnimal].stages.length;
      }
    }

    ctx.clearRect(0, 0, w, h);

    const bg = ctx.createLinearGradient(0, 0, 0, h);
    bg.addColorStop(0, '#0a0f1a');
    bg.addColorStop(1, '#060a10');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);

    const cycle = CYCLES[activeAnimal];
    const n = cycle.stages.length;
    const cx = w * 0.5;
    const cy = h * 0.38;
    const radius = Math.min(w, h) * 0.28;

    ctx.fillStyle = cycle.color;
    ctx.font = '700 12px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(cycle.label, cx, h * 0.06);

    // Draw cycle arrows
    for (let i = 0; i < n; i++) {
      const a1 = (i / n) * Math.PI * 2 - Math.PI / 2;
      const a2 = ((i + 1) / n) * Math.PI * 2 - Math.PI / 2;
      const aMid = (a1 + a2) / 2;
      const arrowR = radius * 0.85;

      ctx.strokeStyle = `${cycle.color}66`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(cx, cy, radius, a1, a2);
      ctx.stroke();

      // Arrow tip
      const tipX = cx + Math.cos(a2 - 0.08) * radius;
      const tipY = cy + Math.sin(a2 - 0.08) * radius;
      const tangX = -Math.sin(a2);
      const tangY = Math.cos(a2);
      ctx.fillStyle = `${cycle.color}66`;
      ctx.beginPath();
      ctx.moveTo(tipX, tipY);
      ctx.lineTo(tipX - tangX * 8 - tangY * 5, tipY - tangY * 8 + tangX * 5);
      ctx.lineTo(tipX - tangX * 8 + tangY * 5, tipY - tangY * 8 - tangX * 5);
      ctx.closePath();
      ctx.fill();
    }

    // Draw stage circles
    cycle.stages.forEach((s, i) => {
      const angle = (i / n) * Math.PI * 2 - Math.PI / 2;
      const sx = cx + Math.cos(angle) * radius;
      const sy = cy + Math.sin(angle) * radius;
      const isSelected = i === selectedStage;
      const pulse = isSelected ? 1 + 0.08 * Math.sin(animT * 4) : 1;

      // Glow for selected
      if (isSelected) {
        ctx.fillStyle = `${cycle.color}44`;
        ctx.beginPath();
        ctx.arc(sx, sy, 40 * pulse, 0, Math.PI * 2);
        ctx.fill();
      }

      // Circle
      ctx.fillStyle = isSelected ? cycle.color : `${cycle.color}88`;
      ctx.beginPath();
      ctx.arc(sx, sy, 30 * pulse, 0, Math.PI * 2);
      ctx.fill();

      // Emoji
      ctx.font = `${20 * pulse}px serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(s.emoji, sx, sy);
      ctx.textBaseline = 'alphabetic';

      // Stage name
      ctx.fillStyle = isSelected ? '#ffffff' : 'rgba(200,220,255,0.7)';
      ctx.font = `${isSelected ? '700' : '600'} 9px Poppins, sans-serif`;
      ctx.textAlign = 'center';
      const labelOffset = 44 * pulse;
      ctx.fillText(s.name, sx, sy + labelOffset);
    });

    // Info box
    const sel = cycle.stages[selectedStage];
    const infoY = h * 0.73;
    const infoH = h * 0.24;
    ctx.fillStyle = 'rgba(8,14,24,0.85)';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(8, infoY, w - 16, infoH, 8);
    else ctx.rect(8, infoY, w - 16, infoH);
    ctx.fill();
    ctx.strokeStyle = cycle.color;
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.fillStyle = cycle.color;
    ctx.font = '700 11px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(`${sel.emoji} ${sel.name} — ${sel.duration}`, 14, infoY + 15);

    ctx.fillStyle = 'rgba(200,220,255,0.9)';
    ctx.font = '600 9px Poppins, sans-serif';
    const words = sel.info.split(' ');
    let line = '';
    let ly = infoY + 29;
    for (const word of words) {
      const test = line + word + ' ';
      if (ctx.measureText(test).width > w - 28 && line) {
        ctx.fillText(line.trim(), 14, ly);
        line = word + ' ';
        ly += 12;
        if (ly > infoY + infoH - 4) break;
      } else {
        line = test;
      }
    }
    if (ly <= infoY + infoH - 4) ctx.fillText(line.trim(), 14, ly);
  });

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('click', onCanvasClick);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
