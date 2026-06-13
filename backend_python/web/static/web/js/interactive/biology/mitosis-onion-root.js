import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Mitosis stages: accurate chromosome behaviour through all stages
// Onion root tip context — 2n = 16 for Allium cepa (simplified to 8 for clarity)

const STAGES = [
  {
    name: 'Interphase',
    color: '#3b5bdb',
    description: 'DNA replication occurs (S phase). Chromosomes are not yet visible as they are uncoiled (chromatin). Cell is metabolically active. Centrioles duplicate (in animal cells). Nucleus prominent with nucleolus.',
  },
  {
    name: 'Prophase',
    color: '#7c3aed',
    description: 'Chromatin condenses into visible chromosomes (each consisting of 2 sister chromatids joined at centromere). Nuclear envelope begins to break down. Spindle fibres form from centrioles/MTOCs. Nucleolus disappears.',
  },
  {
    name: 'Metaphase',
    color: '#db2777',
    description: 'Chromosomes align at the cell equator (metaphase plate). Each chromosome attached to spindle fibres from both poles via kinetochores. This is the best stage to count chromosomes. Maximum condensation.',
  },
  {
    name: 'Anaphase',
    color: '#dc2626',
    description: 'Sister chromatids are pulled apart to opposite poles by shortening spindle fibres. Centromere splits. Cell elongates. Each pole now has a complete set of chromosomes (chromatids become daughter chromosomes).',
  },
  {
    name: 'Telophase',
    color: '#d97706',
    description: 'Chromosomes reach the poles and begin to decondense. Nuclear envelopes reform around each set. Spindle fibres disassemble. Nucleolus reappears in each new nucleus.',
  },
  {
    name: 'Cytokinesis',
    color: '#16a34a',
    description: 'In plants: a cell plate forms at the equator from Golgi vesicles containing pectin/cellulose, building a new cell wall. In animals: a cleavage furrow pinches the cell. Result: 2 genetically identical daughter cells.',
  },
];

const N_CHROMOSOMES = 4; // simplified — 4 pairs = 8 chromosomes (2n=8)

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const stageBadge = hud.badge('Interphase', '#3b5bdb');

  let stageIdx = 0;
  let animProgress = 0; // 0..1 within stage
  let autoPlay = false;
  let autoTimer = 0;
  const AUTO_DURATION = 3.5; // seconds per stage

  const panel = createPanel(stage, { title: 'Mitosis Controls' });

  panel.section('Stage');
  const stageButtons = STAGES.map((s, i) =>
    panel.button({
      label: s.name,
      onClick: () => { stageIdx = i; animProgress = 0; autoPlay = false; autoToggle.set(false); },
    })
  );

  panel.divider();
  const autoToggle = panel.toggle({
    label: 'Auto-advance',
    value: false,
    onChange: (v) => { autoPlay = v; autoTimer = 0; },
  });
  const progressBar = panel.readout({ label: 'Stage progress', value: '0%' });
  panel.info('Step through all stages of mitosis. Toggle Auto-advance to watch the cycle automatically. Each stage shows accurate chromosome behaviour.');

  function drawInterphase(ctx, cx, cy, r, p) {
    // Nucleus with chromatin (diffuse)
    const nr = r * 0.48;
    ctx.fillStyle = 'rgba(60,91,219,0.15)';
    ctx.beginPath();
    ctx.arc(cx, cy, nr, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = 'rgba(60,91,219,0.6)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(cx, cy, nr, 0, Math.PI * 2);
    ctx.stroke();
    // Nucleolus
    ctx.fillStyle = 'rgba(100,130,255,0.5)';
    ctx.beginPath();
    ctx.arc(cx + nr * 0.2, cy - nr * 0.2, nr * 0.22, 0, Math.PI * 2);
    ctx.fill();
    // Chromatin threads
    ctx.strokeStyle = 'rgba(60,91,219,0.35)';
    ctx.lineWidth = 1.2;
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * Math.PI * 2;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.bezierCurveTo(
        cx + Math.cos(a) * nr * 0.6, cy + Math.sin(a) * nr * 0.6,
        cx + Math.cos(a + 0.8) * nr * 0.5, cy + Math.sin(a + 0.8) * nr * 0.5,
        cx + Math.cos(a + 1.2) * nr * 0.35, cy + Math.sin(a + 1.2) * nr * 0.35
      );
      ctx.stroke();
    }
  }

  function drawChromosome(ctx, x, y, angle, size, color, showSister) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    const arm = size * 0.7;
    const centromereR = size * 0.12;
    if (showSister) {
      // Two sister chromatids joined at centromere
      for (let side = -1; side <= 1; side += 2) {
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.roundRect
          ? ctx.roundRect(side * centromereR * 1.1, -arm, centromereR * 1.2, arm, centromereR * 0.6)
          : ctx.rect(side * centromereR * 1.1, -arm, centromereR * 1.2, arm);
        ctx.fill();
        ctx.beginPath();
        ctx.roundRect
          ? ctx.roundRect(side * centromereR * 1.1, centromereR * 0.5, centromereR * 1.2, arm, centromereR * 0.6)
          : ctx.rect(side * centromereR * 1.1, centromereR * 0.5, centromereR * 1.2, arm);
        ctx.fill();
      }
    } else {
      // Single chromatid
      ctx.fillStyle = color;
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(-centromereR, -arm, centromereR * 2, arm * 2, centromereR * 0.6);
      else ctx.rect(-centromereR, -arm, centromereR * 2, arm * 2);
      ctx.fill();
    }
    // Centromere
    ctx.fillStyle = 'rgba(255,255,255,0.85)';
    ctx.beginPath();
    ctx.arc(0, 0, centromereR * 0.85, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  function drawSpindle(ctx, cx, cy, r, alpha) {
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.strokeStyle = '#a78bfa';
    ctx.lineWidth = 1.2;
    for (let i = 0; i < N_CHROMOSOMES * 2 + 2; i++) {
      const xOff = (i / (N_CHROMOSOMES * 2 + 1) - 0.5) * r * 1.2;
      ctx.beginPath();
      ctx.moveTo(cx + xOff, cy - r * 0.85);
      ctx.lineTo(cx, cy);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(cx + xOff, cy + r * 0.85);
      ctx.lineTo(cx, cy);
      ctx.stroke();
    }
    ctx.restore();
  }

  const CHROM_COLORS = ['#ef4444', '#f97316', '#eab308', '#22c55e'];

  sim.setUpdate((ctx, dt, w, h) => {
    if (autoPlay) {
      autoTimer += dt;
      animProgress = Math.min(1, autoTimer / AUTO_DURATION);
      if (autoTimer >= AUTO_DURATION) {
        stageIdx = (stageIdx + 1) % STAGES.length;
        autoTimer = 0;
        animProgress = 0;
      }
    }

    const stage_data = STAGES[stageIdx];
    stageBadge.set(stage_data.name);
    progressBar.set(`${Math.round(animProgress * 100)}%`);

    ctx.clearRect(0, 0, w, h);

    // Background gradient
    const bg = ctx.createLinearGradient(0, 0, 0, h);
    bg.addColorStop(0, '#0a1628');
    bg.addColorStop(1, '#060e1a');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);

    const cx = w * 0.5;
    const cy = h * 0.44;
    const cellR = Math.min(w, h) * 0.32;

    // Onion root tip context label
    ctx.fillStyle = 'rgba(180,200,255,0.6)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('Onion root tip (Allium cepa) — 2n = 8 simplified', 10, 16);

    // Cell boundary
    ctx.strokeStyle = stage_data.color;
    ctx.lineWidth = 2.5;
    ctx.fillStyle = 'rgba(20,40,70,0.6)';
    ctx.beginPath();
    // Plant cell = rectangle
    const cellX = cx - cellR;
    const cellY = cy - cellR * 1.1;
    if (ctx.roundRect) ctx.roundRect(cellX, cellY, cellR * 2, cellR * 2.2, 8);
    else ctx.rect(cellX, cellY, cellR * 2, cellR * 2.2);
    ctx.fill();
    ctx.stroke();

    const p = animProgress;

    if (stageIdx === 0) {
      // Interphase
      drawInterphase(ctx, cx, cy, cellR, p);
      // Cell wall
      ctx.strokeStyle = 'rgba(180,140,50,0.6)';
      ctx.lineWidth = 5;
      ctx.strokeRect(cellX, cellY, cellR * 2, cellR * 2.2);

    } else if (stageIdx === 1) {
      // Prophase — chromosomes condense
      const condense = p;
      drawSpindle(ctx, cx, cy, cellR, p * 0.5);
      for (let i = 0; i < N_CHROMOSOMES; i++) {
        const angle = (i / N_CHROMOSOMES) * Math.PI * 2;
        const dist = cellR * 0.35 * (1 - condense * 0.2);
        const chromX = cx + Math.cos(angle) * dist;
        const chromY = cy + Math.sin(angle) * dist;
        const size = 8 + condense * 8;
        ctx.globalAlpha = condense;
        drawChromosome(ctx, chromX, chromY, angle + Math.PI / 4, size, CHROM_COLORS[i % CHROM_COLORS.length], true);
        ctx.globalAlpha = 1;
      }
      // Nuclear envelope fades
      const envAlpha = 1 - p;
      ctx.strokeStyle = `rgba(60,91,219,${envAlpha * 0.6})`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(cx, cy, cellR * 0.48, 0, Math.PI * 2);
      ctx.stroke();

    } else if (stageIdx === 2) {
      // Metaphase — chromosomes at equator
      drawSpindle(ctx, cx, cy, cellR, 0.85);
      for (let i = 0; i < N_CHROMOSOMES; i++) {
        const xPos = cx + (i - (N_CHROMOSOMES - 1) / 2) * cellR * 0.38;
        drawChromosome(ctx, xPos, cy, 0, 16, CHROM_COLORS[i % CHROM_COLORS.length], true);
      }
      // Metaphase plate line
      ctx.strokeStyle = 'rgba(255,255,255,0.2)';
      ctx.lineWidth = 1;
      ctx.setLineDash([5, 5]);
      ctx.beginPath();
      ctx.moveTo(cx - cellR * 0.8, cy);
      ctx.lineTo(cx + cellR * 0.8, cy);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = 'rgba(255,255,255,0.4)';
      ctx.font = '600 9px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Metaphase plate', cx, cy - 6);

    } else if (stageIdx === 3) {
      // Anaphase — chromatids pulled to poles
      drawSpindle(ctx, cx, cy, cellR, 0.6);
      const sep = p * cellR * 0.55;
      for (let i = 0; i < N_CHROMOSOMES; i++) {
        const xPos = cx + (i - (N_CHROMOSOMES - 1) / 2) * cellR * 0.36;
        // Top set
        drawChromosome(ctx, xPos, cy - sep, 0, 13, CHROM_COLORS[i % CHROM_COLORS.length], false);
        // Bottom set
        drawChromosome(ctx, xPos, cy + sep, 0, 13, CHROM_COLORS[i % CHROM_COLORS.length], false);
      }

    } else if (stageIdx === 4) {
      // Telophase — nuclei re-form
      const decondense = p;
      for (let pole = -1; pole <= 1; pole += 2) {
        const poleY = cy + pole * cellR * 0.5;
        // New nucleus
        ctx.strokeStyle = `rgba(60,91,219,${decondense * 0.7})`;
        ctx.lineWidth = 2;
        ctx.fillStyle = `rgba(60,91,219,${decondense * 0.08})`;
        ctx.beginPath();
        ctx.arc(cx, poleY, cellR * 0.3, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        // Chromosomes decondensing
        for (let i = 0; i < N_CHROMOSOMES; i++) {
          const a = (i / N_CHROMOSOMES) * Math.PI * 2;
          const dist = cellR * 0.18;
          ctx.globalAlpha = 1 - decondense * 0.7;
          drawChromosome(ctx, cx + Math.cos(a) * dist, poleY + Math.sin(a) * dist, a, 10, CHROM_COLORS[i % CHROM_COLORS.length], false);
          ctx.globalAlpha = 1;
        }
      }

    } else if (stageIdx === 5) {
      // Cytokinesis — cell plate forms
      // Two daughter nuclei
      for (let pole = -1; pole <= 1; pole += 2) {
        const poleY = cy + pole * cellR * 0.5;
        ctx.strokeStyle = 'rgba(60,91,219,0.6)';
        ctx.lineWidth = 2;
        ctx.fillStyle = 'rgba(60,91,219,0.1)';
        ctx.beginPath();
        ctx.arc(cx, poleY, cellR * 0.28, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
      }
      // Cell plate growing from centre outward
      const plateW = p * cellR * 1.9;
      ctx.strokeStyle = '#84CC16';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(cx - plateW / 2, cy);
      ctx.lineTo(cx + plateW / 2, cy);
      ctx.stroke();
      ctx.fillStyle = '#84CC16';
      ctx.font = '600 9px Poppins, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Cell plate (new cell wall)', cx, cy - 8);
      // Cell wall
      ctx.strokeStyle = 'rgba(180,140,50,0.6)';
      ctx.lineWidth = 5;
      ctx.strokeRect(cellX, cellY, cellR * 2, cellR * 2.2);
    }

    // Stage description box
    const descY = h * 0.82;
    ctx.fillStyle = 'rgba(8,16,30,0.75)';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(8, descY, w - 16, h - descY - 8, 6);
    else ctx.rect(8, descY, w - 16, h - descY - 8);
    ctx.fill();

    ctx.fillStyle = stage_data.color;
    ctx.font = '700 12px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(stage_data.name, 16, descY + 16);

    ctx.fillStyle = 'rgba(200,215,240,0.85)';
    ctx.font = '600 9.5px Poppins, sans-serif';
    // Wrap text
    const words = stage_data.description.split(' ');
    let line = '';
    let lineY = descY + 30;
    for (const word of words) {
      const test = line + word + ' ';
      if (ctx.measureText(test).width > w - 32 && line) {
        ctx.fillText(line.trim(), 16, lineY);
        line = word + ' ';
        lineY += 13;
        if (lineY > h - 10) break;
      } else {
        line = test;
      }
    }
    if (lineY <= h - 10) ctx.fillText(line.trim(), 16, lineY);
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
