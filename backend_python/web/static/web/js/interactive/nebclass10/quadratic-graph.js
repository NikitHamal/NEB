import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Quadratic explorer for grade-10 optional / grade-10 mathematics: change a, b
// and c and watch the parabola, its vertex, its axis of symmetry and its roots.

const ACCENT = '#F59E0B';
const GREEN = '#34d399';
const BLUE = '#38bdf8';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('The graph of y = ax² + bx + c is a parabola', ACCENT);

  let a = 1;
  let b = -2;
  let c = -3;

  const panel = createPanel(stage, { title: 'y = ax² + bx + c' });
  panel.slider({ label: 'a', min: -3, max: 3, step: 0.1, value: a, format: (v) => v.toFixed(1), onChange: (v) => { a = v; if (Math.abs(a) < 0.1) a = 0.1; } });
  panel.slider({ label: 'b', min: -8, max: 8, step: 0.5, value: b, format: (v) => v.toFixed(1), onChange: (v) => { b = v; } });
  panel.slider({ label: 'c', min: -8, max: 8, step: 0.5, value: c, format: (v) => v.toFixed(1), onChange: (v) => { c = v; } });
  panel.buttonRow([
    { label: 'Roots', icon: 'functions', onClick: () => { a = 1; b = -2; c = -3; setAll(); badge.set('y = x² − 2x − 3 factorises as (x − 3)(x + 1), so the roots are 3 and −1.'); } },
    { label: 'No real roots', icon: 'block', onClick: () => { a = 1; b = 0; c = 4; setAll(); badge.set('y = x² + 4 has discriminant −16, so the parabola never meets the x-axis.'); } },
    { label: 'Perfect square', icon: 'square', onClick: () => { a = 1; b = -6; c = 9; setAll(); badge.set('y = x² − 6x + 9 = (x − 3)². The discriminant is 0, so it touches the axis at x = 3.'); } },
  ]);
  const readVertex = panel.readout({ label: 'Vertex', value: '—' });
  const readAxis = panel.readout({ label: 'Axis of symmetry', value: '—' });
  const readDisc = panel.readout({ label: 'Discriminant b² − 4ac', value: '—' });
  const readRoots = panel.readout({ label: 'Roots', value: '—' });
  panel.info('The vertex is at x = −b/2a. The number of real roots is decided by the sign of D = b² − 4ac.');

  function setAll() {
    const inputs = panel.el.querySelectorAll('input[type=range]');
    const vals = [a, b, c];
    inputs.forEach((inp, i) => {
      if (vals[i] === undefined) return;
      inp.value = vals[i];
      const val = inp.closest('.ix-ctrl-slider').querySelector('.ix-ctrl-value');
      if (val) val.textContent = vals[i].toFixed(1);
    });
  }

  function draw(ctx, w, h) {
    ctx.clearRect(0, 0, w, h);

    const pad = 26;
    const gx = pad + 26;
    const gy = pad;
    const gw = w - gx - pad - 150;
    const gh = h - gy - pad - 24;
    const xMin = -8;
    const xMax = 8;
    const yMin = -10;
    const yMax = 10;
    const X = (x) => gx + ((x - xMin) / (xMax - xMin)) * gw;
    const Y = (y) => gy + gh - ((y - yMin) / (yMax - yMin)) * gh;

    // grid
    ctx.strokeStyle = 'rgba(199,212,234,0.14)';
    ctx.lineWidth = 1;
    for (let x = xMin; x <= xMax; x++) {
      ctx.beginPath(); ctx.moveTo(X(x), gy); ctx.lineTo(X(x), gy + gh); ctx.stroke();
    }
    for (let y = yMin; y <= yMax; y++) {
      ctx.beginPath(); ctx.moveTo(gx, Y(y)); ctx.lineTo(gx + gw, Y(y)); ctx.stroke();
    }
    // axes
    ctx.strokeStyle = 'rgba(199,212,234,0.6)';
    ctx.lineWidth = 1.4;
    ctx.beginPath(); ctx.moveTo(gx, Y(0)); ctx.lineTo(gx + gw, Y(0)); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(X(0), gy); ctx.lineTo(X(0), gy + gh); ctx.stroke();
    ctx.fillStyle = 'rgba(199,212,234,0.75)';
    ctx.font = '600 9px Poppins, sans-serif';
    ctx.textAlign = 'center';
    for (let x = xMin + 1; x <= xMax - 1; x += 2) {
      if (x === 0) continue;
      ctx.fillText(String(x), X(x), Y(0) + 12);
    }

    // axis of symmetry
    const vx = -b / (2 * a);
    ctx.strokeStyle = 'rgba(96,165,250,0.7)';
    ctx.setLineDash([5, 4]);
    ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.moveTo(X(vx), gy); ctx.lineTo(X(vx), gy + gh); ctx.stroke();
    ctx.setLineDash([]);

    // parabola
    ctx.strokeStyle = ACCENT;
    ctx.lineWidth = 2.4;
    ctx.beginPath();
    let started = false;
    for (let px = 0; px <= gw; px += 2) {
      const x = xMin + (px / gw) * (xMax - xMin);
      const y = a * x * x + b * x + c;
      if (y < yMin - 4 || y > yMax + 4) { started = false; continue; }
      const sx = gx + px;
      const sy = Y(y);
      if (!started) { ctx.moveTo(sx, sy); started = true; } else ctx.lineTo(sx, sy);
    }
    ctx.stroke();

    // vertex
    const vy = a * vx * vx + b * vx + c;
    if (vy >= yMin && vy <= yMax) {
      ctx.fillStyle = GREEN;
      ctx.beginPath(); ctx.arc(X(vx), Y(vy), 4.5, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = 'rgba(232,238,251,0.9)';
      ctx.font = '700 10px Poppins, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(`(${vx.toFixed(2)}, ${vy.toFixed(2)})`, X(vx) + 8, Y(vy) - 6);
    }

    // roots
    const D = b * b - 4 * a * c;
    let rootsTxt = 'none (no real roots)';
    if (D >= 0 && Math.abs(a) > 1e-9) {
      const r1 = (-b - Math.sqrt(D)) / (2 * a);
      const r2 = (-b + Math.sqrt(D)) / (2 * a);
      rootsTxt = D === 0 ? `x = ${r1.toFixed(2)} (repeated)` : `x = ${r1.toFixed(2)} and x = ${r2.toFixed(2)}`;
      [r1, r2].forEach((r) => {
        if (r < xMin || r > xMax) return;
        ctx.fillStyle = BLUE;
        ctx.beginPath(); ctx.arc(X(r), Y(0), 4.5, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = 'rgba(2,6,23,0.6)'; ctx.lineWidth = 1; ctx.stroke();
      });
    }

    // equation panel
    const px0 = gx + gw + 14;
    ctx.fillStyle = 'rgba(8,16,30,0.8)';
    ctx.strokeStyle = 'rgba(158,193,255,0.25)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(px0, gy, 136, gh, 8); else ctx.rect(px0, gy, 136, gh);
    ctx.fill(); ctx.stroke();
    ctx.textAlign = 'left';
    ctx.fillStyle = ACCENT;
    ctx.font = '700 12px Poppins, sans-serif';
    ctx.fillText('y = ax² + bx + c', px0 + 12, gy + 24);
    ctx.fillStyle = 'rgba(232,238,251,0.92)';
    ctx.font = '600 11px Poppins, sans-serif';
    ctx.fillText(`a = ${a.toFixed(1)}`, px0 + 12, gy + 48);
    ctx.fillText(`b = ${b.toFixed(1)}`, px0 + 12, gy + 66);
    ctx.fillText(`c = ${c.toFixed(1)}`, px0 + 12, gy + 84);
    ctx.fillStyle = a > 0 ? GREEN : '#fb7185';
    ctx.font = '600 10.5px Poppins, sans-serif';
    ctx.fillText(a > 0 ? 'opens upwards (minimum)' : 'opens downwards (maximum)', px0 + 12, gy + 110);
    ctx.fillStyle = 'rgba(199,212,234,0.8)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.fillText('x-intercepts = roots', px0 + 12, gy + 134);
    ctx.fillText('y-intercept = c', px0 + 12, gy + 150);

    readVertex.set(`(${vx.toFixed(2)}, ${vy.toFixed(2)})`);
    readAxis.set(`x = ${vx.toFixed(2)}`);
    readDisc.set(`${D.toFixed(2)}`);
    readRoots.set(rootsTxt);
  }

  // the canvas helper calls (ctx, dt, width, height); draw wants (ctx, width, height)
  sim.setUpdate((ctx, dt, w, h) => draw(ctx, w, h));
  sim.onResize(() => sim.renderOnce());
  sim.start();

  return { dispose() { sim.dispose(); hud.dispose(); panel.dispose(); } };
}
