import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const PERIOD = 14;
const SWEEP_COUNT = 8;

export default function init(stage) {
  const sim = createCanvas2D(stage);

  let ecc = 0.5;
  let speedMul = 1;
  let showSweep = true;
  let showMarkers = true;
  let M = 0;
  let sweeps = [];
  let sweepStartM = 0;
  let bgStars = [];
  let viewMode = '2d';

  sim.onResize((w, h) => {
    bgStars = [];
    const n = Math.round((w * h) / 6000);
    for (let i = 0; i < n; i++) {
      bgStars.push({ x: Math.random() * w, y: Math.random() * h, r: Math.random() * 1.2 + 0.3, a: Math.random() * 0.5 + 0.2 });
    }
  });

  function solveE(m, e) {
    let E = m;
    for (let i = 0; i < 6; i++) {
      E = E - (E - e * Math.sin(E) - m) / (1 - e * Math.cos(E));
    }
    return E;
  }

  function posAt(m, a, e) {
    const E = solveE(m, e);
    const b = a * Math.sqrt(1 - e * e);
    return { x: a * (Math.cos(E) - e), y: b * Math.sin(E) };
  }

  function resetSweeps() {
    sweeps = [];
    sweepStartM = M;
  }

  const hud = createHud(stage);
  const lawBadge = hud.badge('Equal areas in equal times', '#c4b5fd');

  const panel = createPanel(stage, { title: 'Kepler\u2019s Laws' });
  panel.select({
    label: 'View',
    options: [
      { value: '2d', label: '2D' },
      { value: '3d', label: '3D' },
    ],
    value: viewMode,
    onChange: (v) => { viewMode = v; },
  });
  panel.slider({
    label: 'Eccentricity',
    min: 0, max: 0.85, step: 0.05, value: ecc,
    format: (v) => v.toFixed(2),
    onChange: (v) => { ecc = v; resetSweeps(); },
  });
  panel.slider({
    label: 'Speed',
    min: 0, max: 3, step: 0.25, value: 1,
    format: (v) => (v === 0 ? 'Paused' : `${v}\u00d7`),
    onChange: (v) => { speedMul = v; },
  });
  panel.toggle({ label: 'Show swept areas', value: true, onChange: (v) => { showSweep = v; resetSweeps(); } });
  panel.toggle({ label: 'Perihelion / aphelion', value: true, onChange: (v) => { showMarkers = v; } });
  const distReadout = panel.readout({ label: 'Distance', value: '1.00 AU' });
  const speedReadout = panel.readout({ label: 'Speed', value: '\u2014' });
  panel.info('The Sun sits at one focus, not the centre. Each shaded slice is swept in the same amount of time \u2014 and every slice has the same area. Watch the planet sprint at perihelion!');

  sim.setUpdate((ctx, dt, w, h) => {
    const n = (Math.PI * 2) / PERIOD;
    M += n * dt * speedMul;
    if (M > Math.PI * 4) { M -= Math.PI * 2; sweepStartM -= Math.PI * 2; sweeps.forEach((s) => { s.m0 -= Math.PI * 2; s.m1 -= Math.PI * 2; }); }

    const sweepInterval = (Math.PI * 2) / SWEEP_COUNT;
    if (showSweep && speedMul > 0) {
      while (M - sweepStartM >= sweepInterval) {
        sweeps.push({ m0: sweepStartM, m1: sweepStartM + sweepInterval });
        sweepStartM += sweepInterval;
        if (sweeps.length > SWEEP_COUNT) sweeps.shift();
      }
    }

    const a = Math.min(w, h) * 0.34;
    const e = ecc;
    const cx = w / 2 + a * e * 0.5;
    const cy = h / 2;

    ctx.fillStyle = '#0a1322';
    ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#cdd9ec';
    for (let i = 0; i < bgStars.length; i++) {
      ctx.globalAlpha = bgStars[i].a;
      ctx.fillRect(bgStars[i].x, bgStars[i].y, bgStars[i].r, bgStars[i].r);
    }
    ctx.globalAlpha = 1;

    function toScreen(p) {
      return { x: cx + p.x, y: cy - p.y * (viewMode === '3d' ? 0.48 : 1) };
    }

    if (showSweep) {
      const colors = ['rgba(196,181,253,0.28)', 'rgba(125,211,252,0.28)'];
      const drawWedge = (m0, m1, fill) => {
        ctx.fillStyle = fill;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        const steps = 20;
        for (let i = 0; i <= steps; i++) {
          const p = toScreen(posAt(m0 + ((m1 - m0) * i) / steps, a, e));
          ctx.lineTo(p.x, p.y);
        }
        ctx.closePath();
        ctx.fill();
      };
      for (let i = 0; i < sweeps.length; i++) {
        drawWedge(sweeps[i].m0, sweeps[i].m1, colors[i % 2]);
      }
      if (speedMul > 0) drawWedge(sweepStartM, M, 'rgba(139,233,168,0.34)');
    }

    ctx.strokeStyle = 'rgba(158,193,255,0.5)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    const bb = a * Math.sqrt(1 - e * e);
    if (viewMode === '3d') {
      const steps = 96;
      for (let i = 0; i <= steps; i++) {
        const th = (i / steps) * Math.PI * 2;
        const p = toScreen({ x: Math.cos(th) * a - a * e, y: Math.sin(th) * bb });
        if (i === 0) ctx.moveTo(p.x, p.y);
        else ctx.lineTo(p.x, p.y);
      }
    } else {
      ctx.ellipse(cx - a * e, cy, a, bb, 0, 0, Math.PI * 2);
    }
    ctx.stroke();

    const sunR = 13;
    const grad = ctx.createRadialGradient(cx, cy, 3, cx, cy, sunR * 2.6);
    grad.addColorStop(0, 'rgba(255,210,120,0.95)');
    grad.addColorStop(0.4, 'rgba(255,170,60,0.32)');
    grad.addColorStop(1, 'rgba(255,150,40,0)');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(cx, cy, sunR * 2.6, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#ffd27a';
    ctx.beginPath();
    ctx.arc(cx, cy, sunR, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = 'rgba(232,238,251,0.85)';
    ctx.font = '600 11px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Sun (focus)', cx, cy + sunR + 16);

    ctx.fillStyle = 'rgba(232,238,251,0.45)';
    ctx.beginPath();
    ctx.arc(cx - 2 * a * e, cy, 3, 0, Math.PI * 2);
    ctx.fill();
    if (e > 0.05) ctx.fillText('empty focus', cx - 2 * a * e, cy + 18);

    if (showMarkers) {
      const peri = toScreen(posAt(0, a, e));
      const aph = toScreen(posAt(Math.PI, a, e));
      ctx.fillStyle = '#8be9a8';
      ctx.beginPath();
      ctx.arc(peri.x, peri.y, 3.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillText('perihelion (fastest)', peri.x, peri.y - 12);
      ctx.fillStyle = '#fda4af';
      ctx.beginPath();
      ctx.arc(aph.x, aph.y, 3.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillText('aphelion (slowest)', aph.x, aph.y - 12);
    }

    const p = toScreen(posAt(M, a, e));
    ctx.strokeStyle = 'rgba(139,233,168,0.6)';
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(p.x, p.y);
    ctx.stroke();
    ctx.fillStyle = '#7dd3fc';
    ctx.beginPath();
    ctx.arc(p.x, p.y, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = 'rgba(125,211,252,0.25)';
    ctx.beginPath();
    ctx.arc(p.x, p.y, 14, 0, Math.PI * 2);
    ctx.fill();
    ctx.textAlign = 'left';

    const rPx = Math.hypot(p.x - cx, p.y - cy);
    const rAU = rPx / a;
    const vRel = Math.sqrt(Math.max(0.01, 2 / rAU - 1));
    distReadout.set(`${rAU.toFixed(2)} AU`);
    speedReadout.set(`${(vRel * 29.8).toFixed(1)} km/s`);
    lawBadge.set(e < 0.03 ? 'e = 0: a perfect circle' : 'Equal areas in equal times');
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
