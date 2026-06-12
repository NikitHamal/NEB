import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, drawTable, drawNeedleMeter, labelText } from './lab-utils.js';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Find the null point', '#9ec1ff');

  let known = 5;
  let unknown = 0;
  let jockeyL = 50;
  let swapped = false;
  let dragging = false;
  let revealed = false;
  const records = [];

  function newUnknown() {
    unknown = Math.round((2 + Math.random() * 10) * 10) / 10;
    records.length = 0;
    revealed = false;
    swapped = false;
  }

  function deflection() {
    const Rl = swapped ? unknown : known;
    const Rr = swapped ? known : unknown;
    const num = Rl * (100 - jockeyL) - Rr * jockeyL;
    return 30 * Math.tanh(num / 60);
  }

  const panel = createPanel(stage, { title: 'Meter Bridge Lab' });
  panel.select({
    label: 'Known R (resistance box)',
    options: [1, 2, 3, 5, 8, 10].map((r) => ({ value: String(r), label: `${r} Ω` })),
    value: '5',
    onChange: (v) => { known = parseFloat(v); },
  });
  panel.toggle({ label: 'Interchange R and X', value: false, onChange: (v) => { swapped = v; } });
  panel.button({ label: 'New unknown X', icon: 'refresh', onClick: newUnknown });
  panel.button({
    label: 'Record balance point',
    icon: 'edit_note',
    onClick: () => {
      if (Math.abs(deflection()) > 0.45 || records.length >= 6) return;
      const l = jockeyL;
      const x = swapped ? (known * l) / (100 - l) : (known * (100 - l)) / l;
      records.push({ R: known, l, swapped, x });
    },
  });
  panel.button({ label: 'Clear table', icon: 'delete', variant: 'ghost', onClick: () => { records.length = 0; } });
  panel.divider();
  const lOut = panel.readout({ label: 'Jockey at l', value: '—' });
  const xOut = panel.readout({ label: 'Mean X', value: '—' });
  panel.button({ label: 'Reveal true X', icon: 'visibility', onClick: () => { revealed = true; } });
  panel.info('Slide the jockey until the galvanometer reads zero. Then X = R(100−l)/l. Repeat with different R values and with R, X interchanged, and average.');

  newUnknown();

  function geom(w, h) {
    return { x0: w * 0.08, x1: w * 0.92, wy: h * 0.52 };
  }

  function onDown(e) {
    dragging = true;
    if (sim.canvas.setPointerCapture) sim.canvas.setPointerCapture(e.pointerId);
    onMove(e);
    e.preventDefault();
  }

  function onMove(e) {
    if (!dragging) return;
    const p = pointerPos(sim.canvas, e);
    const g = geom(sim.width, sim.height);
    if (p.y < g.wy - 90) return;
    jockeyL = Math.max(1, Math.min(99, ((p.x - g.x0) / (g.x1 - g.x0)) * 100));
    jockeyL = Math.round(jockeyL * 10) / 10;
  }

  function onUp() { dragging = false; }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);
  sim.canvas.addEventListener('pointercancel', onUp);

  sim.setUpdate((ctx, dt, w, h) => {
    const defl = deflection();
    ctx.clearRect(0, 0, w, h);
    const g = geom(w, h);

    drawNeedleMeter(ctx, {
      cx: w * 0.5, cy: h * 0.18, r: Math.min(w * 0.17, 66),
      value: defl, min: -30, max: 30, label: 'galvanometer', divisions: 12,
    });

    const leftX = w * 0.22;
    const rightX = w * 0.78;
    const gapY = g.wy - 56;
    ctx.fillStyle = '#39496b';
    ctx.fillRect(leftX - 38, gapY - 12, 76, 24);
    ctx.fillRect(rightX - 38, gapY - 12, 76, 24);
    const leftLabel = swapped ? `X (unknown)` : `R = ${known} Ω`;
    const rightLabel = swapped ? `R = ${known} Ω` : `X (unknown)`;
    labelText(ctx, leftLabel, leftX, gapY + 4, { size: 9.5, weight: 700, align: 'center', color: '#ffd584' });
    labelText(ctx, rightLabel, rightX, gapY + 4, { size: 9.5, weight: 700, align: 'center', color: '#ffd584' });
    labelText(ctx, 'left gap', leftX, gapY - 20, { size: 8.5, weight: 600, align: 'center', color: 'rgba(199,212,234,0.65)' });
    labelText(ctx, 'right gap', rightX, gapY - 20, { size: 8.5, weight: 600, align: 'center', color: 'rgba(199,212,234,0.65)' });

    ctx.strokeStyle = '#F59E0B';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(g.x0, g.wy);
    ctx.lineTo(g.x1, g.wy);
    ctx.stroke();

    ctx.font = '600 8.5px Poppins, sans-serif';
    ctx.textAlign = 'center';
    for (let cm = 0; cm <= 100; cm += 10) {
      const xx = g.x0 + ((g.x1 - g.x0) * cm) / 100;
      ctx.strokeStyle = 'rgba(232,238,251,0.55)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(xx, g.wy + 6);
      ctx.lineTo(xx, g.wy + 14);
      ctx.stroke();
      ctx.fillStyle = 'rgba(232,238,251,0.8)';
      ctx.fillText(String(cm), xx, g.wy + 26);
    }

    const jx = g.x0 + ((g.x1 - g.x0) * jockeyL) / 100;
    ctx.strokeStyle = 'rgba(158,193,255,0.6)';
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.moveTo(w * 0.5, h * 0.18 + 30);
    ctx.lineTo(jx, g.wy - 18);
    ctx.stroke();
    ctx.fillStyle = dragging ? '#ffd584' : '#9ec1ff';
    ctx.beginPath();
    ctx.moveTo(jx - 9, g.wy - 18);
    ctx.lineTo(jx, g.wy - 2);
    ctx.lineTo(jx + 9, g.wy - 18);
    ctx.closePath();
    ctx.fill();
    labelText(ctx, `jockey: ${fmt(jockeyL, 1)} cm`, jx, g.wy - 28, { size: 9.5, weight: 700, align: 'center', color: dragging ? '#ffd584' : '#9ec1ff' });

    const rows = records.map((r) => [r.swapped ? 'X|R' : 'R|X', r.R, fmt(r.l, 1), fmt(r.x, 2)]);
    drawTable(ctx, {
      x: 12, y: h * 0.66, w: Math.min(w - 24, 290),
      title: 'Balance points', cols: ['gaps', 'R (Ω)', 'l (cm)', 'X (Ω)'], rows,
    });

    lOut.set(`${fmt(jockeyL, 1)} cm`);
    if (records.length) {
      const mean = records.reduce((s, r) => s + r.x, 0) / records.length;
      xOut.set(revealed ? `${fmt(mean, 2)} Ω (true ${fmt(unknown, 1)} Ω)` : `${fmt(mean, 2)} Ω`);
    } else {
      xOut.set('—');
    }
    statusBadge.set(
      Math.abs(defl) < 0.45 ? 'NULL — record this balance point!'
        : Math.abs(defl) < 4 ? 'Very close to balance…'
          : defl > 0 ? 'Deflection right — slide jockey right' : 'Deflection left — slide jockey left',
    );
  });

  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onDown);
      sim.canvas.removeEventListener('pointermove', onMove);
      sim.canvas.removeEventListener('pointerup', onUp);
      sim.canvas.removeEventListener('pointercancel', onUp);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
