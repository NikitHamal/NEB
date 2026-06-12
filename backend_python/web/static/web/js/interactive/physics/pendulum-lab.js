import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const GRAVITY_PRESETS = { moon: 1.62, earth: 9.81, jupiter: 24.8 };
const MAX_SAMPLES = 600;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const phaseBadge = hud.badge('Swinging', '#F59E0B');

  let L = 1.0;
  let g = 9.81;
  let damping = false;
  let theta = (30 * Math.PI) / 180;
  let omega = 0;
  let elapsed = 0;
  let dragging = false;
  let swings = 0;
  let lastCross = -1;
  let measuredT = 0;
  let prevOmegaSign = 0;
  const samples = new Float32Array(MAX_SAMPLES);
  const sampleT = new Float32Array(MAX_SAMPLES);
  let sampleCount = 0;
  let sampleHead = 0;
  let sampleClock = 0;

  function resetMotion(angleDeg) {
    theta = (angleDeg * Math.PI) / 180;
    omega = 0;
    elapsed = 0;
    swings = 0;
    lastCross = -1;
    measuredT = 0;
    prevOmegaSign = 0;
    sampleCount = 0;
    sampleHead = 0;
    sampleClock = 0;
  }

  const panel = createPanel(stage, { title: 'Pendulum Controls' });
  const lenSlider = panel.slider({
    label: 'Length L',
    min: 0.2, max: 3, step: 0.05, value: L,
    format: (v) => `${v.toFixed(2)} m`,
    onChange: (v) => { L = v; },
  });
  const gravSelect = panel.select({
    label: 'Gravity preset',
    options: [
      { value: 'earth', label: 'Earth (9.81 m/s²)' },
      { value: 'moon', label: 'Moon (1.62 m/s²)' },
      { value: 'jupiter', label: 'Jupiter (24.8 m/s²)' },
      { value: 'custom', label: 'Custom' },
    ],
    value: 'earth',
    onChange: (v) => {
      if (v !== 'custom') {
        g = GRAVITY_PRESETS[v];
        gravSlider.set(g);
      }
    },
  });
  const gravSlider = panel.slider({
    label: 'Gravity g',
    min: 1, max: 30, step: 0.1, value: g,
    format: (v) => `${v.toFixed(2)} m/s²`,
    onChange: (v) => { g = v; gravSelect.set('custom'); },
  });
  const angleSlider = panel.slider({
    label: 'Initial angle',
    min: 5, max: 75, step: 1, value: 30,
    format: (v) => `${v}°`,
    onChange: (v) => resetMotion(v),
  });
  panel.toggle({
    label: 'Air damping',
    value: false,
    onChange: (v) => { damping = v; },
  });
  panel.divider();
  const periodOut = panel.readout({ label: 'Measured period', value: '—' });
  const theoryOut = panel.readout({ label: 'Theory 2π√(L/g)', value: '—' });
  const swingOut = panel.readout({ label: 'Completed swings', value: '0' });
  panel.button({
    label: 'Reset swing',
    icon: 'replay',
    onClick: () => resetMotion(angleSlider.get()),
  });
  panel.info('Drag the bob to set a new angle, then release. Compare big and small swings against the theory readout.');

  function layout(w, h) {
    const graphH = Math.max(110, h * 0.27);
    return {
      pivotX: w * 0.5,
      pivotY: 44,
      graphTop: h - graphH,
      graphH,
      pxPerM: (h - graphH - 44 - 60) / 3.05,
    };
  }

  function bobPos(w, h) {
    const ly = layout(w, h);
    const r = L * ly.pxPerM;
    return {
      x: ly.pivotX + Math.sin(theta) * r,
      y: ly.pivotY + Math.cos(theta) * r,
      r,
      ly,
    };
  }

  function onDown(e) {
    const p = pointerPos(sim.canvas, e);
    const b = bobPos(sim.width, sim.height);
    if (Math.hypot(p.x - b.x, p.y - b.y) < 44) {
      dragging = true;
      sim.canvas.setPointerCapture && sim.canvas.setPointerCapture(e.pointerId);
      e.preventDefault();
    }
  }

  function onMove(e) {
    if (!dragging) return;
    const p = pointerPos(sim.canvas, e);
    const ly = layout(sim.width, sim.height);
    theta = Math.atan2(p.x - ly.pivotX, p.y - ly.pivotY);
    theta = Math.max(-1.4, Math.min(1.4, theta));
    omega = 0;
  }

  function onUp() {
    if (!dragging) return;
    dragging = false;
    elapsed = 0;
    swings = 0;
    lastCross = -1;
    measuredT = 0;
    prevOmegaSign = 0;
  }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);
  sim.canvas.addEventListener('pointercancel', onUp);

  function step(dt) {
    const sub = 4;
    const h = dt / sub;
    for (let i = 0; i < sub; i++) {
      const b = damping ? 0.18 : 0;
      const alpha = -(g / L) * Math.sin(theta) - b * omega;
      omega += alpha * h;
      theta += omega * h;
      elapsed += h;
      const sign = omega > 0 ? 1 : omega < 0 ? -1 : 0;
      if (prevOmegaSign <= 0 && sign > 0 && theta < 0.001) {
        if (lastCross >= 0) {
          measuredT = elapsed - lastCross;
          swings++;
        }
        lastCross = elapsed;
      }
      if (sign !== 0) prevOmegaSign = sign;
    }
  }

  function pushSample(dt) {
    sampleClock += dt;
    if (sampleClock < 0.033) return;
    sampleClock = 0;
    samples[sampleHead] = theta;
    sampleT[sampleHead] = elapsed;
    sampleHead = (sampleHead + 1) % MAX_SAMPLES;
    if (sampleCount < MAX_SAMPLES) sampleCount++;
  }

  function drawGraph(ctx, w, ly) {
    const gx = 16;
    const gw = w - 32;
    const gy = ly.graphTop + 12;
    const gh = ly.graphH - 26;
    ctx.fillStyle = 'rgba(8,16,30,0.7)';
    ctx.strokeStyle = 'rgba(158,193,255,0.25)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(gx, gy, gw, gh, 8);
    else ctx.rect(gx, gy, gw, gh);
    ctx.fill();
    ctx.stroke();
    const midY = gy + gh / 2;
    ctx.strokeStyle = 'rgba(158,193,255,0.2)';
    ctx.beginPath();
    ctx.moveTo(gx + 8, midY);
    ctx.lineTo(gx + gw - 8, midY);
    ctx.stroke();
    ctx.fillStyle = 'rgba(199,212,234,0.55)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('angle θ vs time', gx + 10, gy + 14);
    ctx.fillText('+90°', gx + 10, gy + 26);
    ctx.fillText('−90°', gx + 10, gy + gh - 8);
    if (sampleCount < 2) return;
    const span = 10;
    const tNow = elapsed;
    ctx.strokeStyle = '#F59E0B';
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    let started = false;
    for (let i = 0; i < sampleCount; i++) {
      const idx = (sampleHead - sampleCount + i + MAX_SAMPLES) % MAX_SAMPLES;
      const age = tNow - sampleT[idx];
      if (age > span || age < 0) continue;
      const x = gx + gw - 8 - (age / span) * (gw - 16);
      const y = midY - (samples[idx] / (Math.PI / 2)) * (gh / 2 - 8);
      if (!started) { ctx.moveTo(x, y); started = true; } else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }

  sim.setUpdate((ctx, dt, w, h) => {
    if (!dragging) {
      step(dt);
      pushSample(dt);
    }
    const b = bobPos(w, h);
    const ly = b.ly;

    ctx.clearRect(0, 0, w, h);

    ctx.strokeStyle = 'rgba(158,193,255,0.15)';
    ctx.lineWidth = 1;
    ctx.setLineDash([5, 6]);
    ctx.beginPath();
    ctx.moveTo(ly.pivotX, ly.pivotY);
    ctx.lineTo(ly.pivotX, ly.pivotY + 3.05 * ly.pxPerM);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.fillStyle = 'rgba(199,212,234,0.85)';
    ctx.fillRect(ly.pivotX - 46, ly.pivotY - 12, 92, 8);
    ctx.strokeStyle = 'rgba(199,212,234,0.4)';
    for (let i = -40; i <= 40; i += 10) {
      ctx.beginPath();
      ctx.moveTo(ly.pivotX + i, ly.pivotY - 12);
      ctx.lineTo(ly.pivotX + i - 6, ly.pivotY - 20);
      ctx.stroke();
    }

    ctx.strokeStyle = '#c7d4ea';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(ly.pivotX, ly.pivotY);
    ctx.lineTo(b.x, b.y);
    ctx.stroke();

    ctx.fillStyle = '#1c2f4d';
    ctx.beginPath();
    ctx.arc(ly.pivotX, ly.pivotY, 6, 0, Math.PI * 2);
    ctx.fill();

    const grad = ctx.createRadialGradient(b.x - 5, b.y - 6, 2, b.x, b.y, 18);
    grad.addColorStop(0, '#ffd584');
    grad.addColorStop(1, '#F59E0B');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(b.x, b.y, 16, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.5)';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    if (dragging) {
      ctx.strokeStyle = 'rgba(245,158,11,0.5)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(b.x, b.y, 26, 0, Math.PI * 2);
      ctx.stroke();
    }

    const deg = (theta * 180) / Math.PI;
    ctx.fillStyle = 'rgba(232,238,251,0.9)';
    ctx.font = '700 13px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(`θ = ${deg.toFixed(1)}°`, 16, 26);
    ctx.fillText(`t = ${elapsed.toFixed(1)} s`, 16, 44);

    drawGraph(ctx, w, ly);

    const theory = 2 * Math.PI * Math.sqrt(L / g);
    theoryOut.set(`${theory.toFixed(2)} s`);
    periodOut.set(measuredT > 0 ? `${measuredT.toFixed(2)} s` : '—');
    swingOut.set(String(swings));
    phaseBadge.set(dragging ? 'Set the angle…' : damping ? 'Damped swing' : 'Swinging');
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
