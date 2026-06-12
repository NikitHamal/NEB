import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, drawTable, labelText } from './lab-utils.js';

const MU = 0.00098;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Adjust length to find resonance', '#9ec1ff');

  let forkF = 256;
  let loadKg = 2;
  let lenCm = 50;
  let riderOn = true;
  let riderJump = 0;
  let dragging = false;
  const records = [];

  function wireFreq() {
    const T = loadKg * 9.8;
    return (1 / (2 * (lenCm / 100))) * Math.sqrt(T / MU);
  }

  function resAmp() {
    const d = (wireFreq() - forkF) / (forkF * 0.015);
    return 1 / (1 + d * d);
  }

  const panel = createPanel(stage, { title: 'Sonometer Lab' });
  panel.select({
    label: 'Tuning fork',
    options: [256, 288, 320, 384, 426, 480, 512].map((f) => ({ value: String(f), label: `${f} Hz` })),
    value: '256',
    onChange: (v) => { forkF = parseInt(v, 10); riderJump = 0; riderOn = true; },
  });
  panel.slider({
    label: 'Hanging load',
    min: 0.5, max: 4, step: 0.5, value: loadKg,
    format: (v) => `${v.toFixed(1)} kg`,
    onChange: (v) => { loadKg = v; riderOn = true; },
  });
  panel.slider({
    label: 'Wire length L (bridges)',
    min: 15, max: 90, step: 0.5, value: lenCm,
    format: (v) => `${v.toFixed(1)} cm`,
    onChange: (v) => { lenCm = v; },
  });
  panel.button({ label: 'Replace paper rider', icon: 'replay', onClick: () => { riderOn = true; riderJump = 0; } });
  panel.button({
    label: 'Record resonance',
    icon: 'edit_note',
    onClick: () => {
      if (resAmp() < 0.6 || records.length >= 6) return;
      records.push({ f: forkF, M: loadKg, L: lenCm });
    },
  });
  panel.button({ label: 'Clear table', icon: 'delete', variant: 'ghost', onClick: () => { records.length = 0; } });
  panel.divider();
  const ampOut = panel.readout({ label: 'Wire vibration', value: '—' });
  const lawOut = panel.readout({ label: 'f × L (law of length)', value: '—' });
  panel.info('Slide the bridge until the wire resonates with the fork — the paper rider dances and flies off. Record L for several forks at the same load and check f×L stays constant.');

  function geom(w, h) {
    return { x0: w * 0.1, x1: w * 0.9, wy: h * 0.34 };
  }

  function onDown(e) {
    const p = pointerPos(sim.canvas, e);
    const g = geom(sim.width, sim.height);
    const bx = g.x0 + ((g.x1 - g.x0) * lenCm) / 100;
    if (Math.abs(p.x - bx) < 40 && Math.abs(p.y - g.wy) < 70) {
      dragging = true;
      if (sim.canvas.setPointerCapture) sim.canvas.setPointerCapture(e.pointerId);
      e.preventDefault();
    }
  }

  function onMove(e) {
    if (!dragging) return;
    const p = pointerPos(sim.canvas, e);
    const g = geom(sim.width, sim.height);
    lenCm = Math.max(15, Math.min(90, ((p.x - g.x0) / (g.x1 - g.x0)) * 100));
    lenCm = Math.round(lenCm * 2) / 2;
  }

  function onUp() { dragging = false; }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);
  sim.canvas.addEventListener('pointercancel', onUp);

  sim.setUpdate((ctx, dt, w, h) => {
    const amp = resAmp();
    if (riderOn && amp > 0.75) {
      riderJump += dt * 3;
      if (riderJump > 1.6) riderOn = false;
    } else {
      riderJump = Math.max(0, riderJump - dt * 2);
    }

    ctx.clearRect(0, 0, w, h);
    const g = geom(w, h);
    ctx.fillStyle = '#2b3a57';
    ctx.fillRect(g.x0 - 20, g.wy + 16, g.x1 - g.x0 + 40, 26);
    const bx = g.x0 + ((g.x1 - g.x0) * lenCm) / 100;

    ctx.font = '600 8.5px Poppins, sans-serif';
    ctx.textAlign = 'center';
    for (let cm = 0; cm <= 100; cm += 10) {
      const xx = g.x0 + ((g.x1 - g.x0) * cm) / 100;
      ctx.strokeStyle = 'rgba(232,238,251,0.5)';
      ctx.beginPath();
      ctx.moveTo(xx, g.wy + 42);
      ctx.lineTo(xx, g.wy + 50);
      ctx.stroke();
      ctx.fillStyle = 'rgba(232,238,251,0.75)';
      ctx.fillText(String(cm), xx, g.wy + 62);
    }

    triangle(ctx, g.x0, g.wy + 16, '#9ec1ff');
    triangle(ctx, bx, g.wy + 16, dragging ? '#ffd584' : '#9ec1ff');
    labelText(ctx, 'drag bridge', bx, g.wy + 90, { size: 8.5, weight: 600, align: 'center', color: dragging ? '#ffd584' : 'rgba(199,212,234,0.6)' });

    const t = performance.now() / 1000;
    const vibAmp = amp * 10;
    ctx.strokeStyle = '#e8eefb';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.moveTo(g.x0 - 18, g.wy - 4);
    ctx.lineTo(g.x0, g.wy);
    for (let i = 0; i <= 30; i++) {
      const xx = g.x0 + ((bx - g.x0) * i) / 30;
      const yy = g.wy + Math.sin((Math.PI * i) / 30) * Math.sin(t * 18) * vibAmp;
      ctx.lineTo(xx, yy);
    }
    ctx.lineTo(g.x1 + 14, g.wy);
    ctx.stroke();

    ctx.strokeStyle = '#c7d4ea';
    ctx.lineWidth = 1.3;
    ctx.beginPath();
    ctx.moveTo(g.x1 + 14, g.wy);
    ctx.lineTo(g.x1 + 14, g.wy + 64);
    ctx.stroke();
    const n = Math.round(loadKg / 0.5);
    for (let i = 0; i < n; i++) {
      ctx.fillStyle = i % 2 ? '#4d5f85' : '#5b6f99';
      ctx.fillRect(g.x1 + 1, g.wy + 64 + i * 7, 26, 6);
    }
    labelText(ctx, `${loadKg.toFixed(1)} kg`, g.x1 + 14, g.wy + 78 + n * 7, { size: 9.5, align: 'center' });

    const rx = g.x0 + (bx - g.x0) * 0.5;
    if (riderOn) {
      const ry = g.wy - 6 - riderJump * 26 - (amp > 0.4 ? Math.abs(Math.sin(t * 18)) * vibAmp : 0);
      ctx.fillStyle = '#ffd584';
      ctx.beginPath();
      ctx.moveTo(rx - 7, ry);
      ctx.lineTo(rx, ry - 8);
      ctx.lineTo(rx + 7, ry);
      ctx.closePath();
      ctx.fill();
    } else {
      labelText(ctx, 'rider flew off — resonance!', rx, g.wy - 28, { size: 10, weight: 700, align: 'center', color: '#8be9a8' });
    }

    const rows = records.map((r) => [r.f, r.M.toFixed(1), fmt(r.L, 1), fmt((r.f * r.L) / 100, 1)]);
    drawTable(ctx, {
      x: 12, y: h * 0.62, w: Math.min(w - 24, 300),
      title: 'Resonance records', cols: ['f (Hz)', 'M (kg)', 'L (cm)', 'f·L /100'], rows,
    });

    ampOut.set(amp > 0.75 ? 'RESONANCE!' : amp > 0.3 ? 'beating, close…' : 'almost still');
    if (records.length >= 2) {
      const sameM = records.filter((r) => r.M === records[records.length - 1].M);
      if (sameM.length >= 2) {
        const prods = sameM.map((r) => (r.f * r.L) / 100);
        const spread = Math.max(...prods) - Math.min(...prods);
        lawOut.set(`spread ${fmt(spread, 1)} → ${spread < 4 ? 'constant ✓' : 'check readings'}`);
      } else {
        lawOut.set('record 2+ forks at same load');
      }
    } else {
      lawOut.set('—');
    }
    statusBadge.set(amp > 0.75 ? 'Resonance — record this length!' : `wire ≈ ${fmt(wireFreq(), 0)} Hz vs fork ${forkF} Hz`);
  });

  function triangle(ctx, x, y, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(x - 10, y);
    ctx.lineTo(x, y - 16);
    ctx.lineTo(x + 10, y);
    ctx.closePath();
    ctx.fill();
  }

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
