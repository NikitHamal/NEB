import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { fmt, drawNeedleMeter, panelBg, labelText } from './lab-utils.js';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const statusBadge = hud.badge('Find balance for cell 1', '#9ec1ff');

  const driverE = 2.2;
  const wireR = 5;
  let rheo = 0.4;
  let cell = 1;
  let E1 = 0;
  let E2 = 0;
  let jockey = 200;
  let l1 = null;
  let l2 = null;
  let dragging = false;
  let revealed = false;

  function newCells() {
    E1 = 1.4 + Math.random() * 0.15;
    E2 = 1.02 + Math.random() * 0.12;
    l1 = null;
    l2 = null;
    revealed = false;
  }

  function gradient() {
    const I = driverE / (wireR + rheo + 0.3);
    return (I * wireR) / 400;
  }

  function cellE() { return cell === 1 ? E1 : E2; }

  function deflection() {
    return 30 * Math.tanh((gradient() * jockey - cellE()) / 0.06);
  }

  const panel = createPanel(stage, { title: 'Potentiometer Lab' });
  panel.select({
    label: 'Two-way key',
    options: [
      { value: '1', label: 'Cell 1 (Leclanché)' },
      { value: '2', label: 'Cell 2 (Daniell)' },
    ],
    value: '1',
    onChange: (v) => { cell = parseInt(v, 10); },
  });
  panel.slider({
    label: 'Driver rheostat',
    min: 0, max: 2, step: 0.05, value: rheo,
    format: (v) => `${v.toFixed(2)} Ω`,
    onChange: (v) => { rheo = v; },
  });
  panel.buttonRow([
    { label: 'Record l₁', icon: 'push_pin', onClick: () => { if (cell === 1 && Math.abs(deflection()) < 0.4) l1 = jockey; } },
    { label: 'Record l₂', icon: 'push_pin', onClick: () => { if (cell === 2 && Math.abs(deflection()) < 0.4) l2 = jockey; } },
  ]);
  panel.button({ label: 'New cells', icon: 'refresh', onClick: newCells });
  panel.divider();
  const kOut = panel.readout({ label: 'Potential gradient k', value: '—' });
  const l1Out = panel.readout({ label: 'Balance l₁ (cell 1)', value: '—' });
  const l2Out = panel.readout({ label: 'Balance l₂ (cell 2)', value: '—' });
  const ratioOut = panel.readout({ label: 'E₁/E₂ = l₁/l₂', value: '—' });
  panel.button({ label: 'Reveal EMFs', icon: 'visibility', onClick: () => { revealed = true; } });
  panel.info('The 400 cm wire carries a steady current, so potential drop ∝ length. Slide the jockey until the galvanometer is null for each cell. Keep the rheostat unchanged between l₁ and l₂!');

  newCells();

  function rowGeom(w, h) {
    const x0 = w * 0.08;
    const x1 = w * 0.92;
    const yTop = h * 0.42;
    const gap = Math.max(26, h * 0.07);
    return { x0, x1, yTop, gap };
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
    const g = rowGeom(sim.width, sim.height);
    if (p.y < g.yTop - 26) return;
    let row = Math.round((p.y - g.yTop) / g.gap);
    row = Math.max(0, Math.min(3, row));
    const frac = Math.max(0, Math.min(1, (p.x - g.x0) / (g.x1 - g.x0)));
    const along = row % 2 === 0 ? frac : 1 - frac;
    jockey = Math.round((row * 100 + along * 100) * 2) / 2;
    jockey = Math.max(1, Math.min(400, jockey));
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
    const g = rowGeom(w, h);

    drawNeedleMeter(ctx, {
      cx: w * 0.71, cy: h * 0.16, r: Math.min(w * 0.15, 60),
      value: defl, min: -30, max: 30, label: 'galvanometer', divisions: 12,
    });

    panelBg(ctx, 12, 12, w * 0.42, 64);
    labelText(ctx, `driver: ${driverE.toFixed(1)} V accumulator`, 22, 32, { size: 9.5, weight: 600 });
    labelText(ctx, `rheostat: ${rheo.toFixed(2)} Ω in series`, 22, 48, { size: 9.5, weight: 600, color: 'rgba(199,212,234,0.8)' });
    labelText(ctx, `testing: ${cell === 1 ? 'Cell 1 (Leclanché)' : 'Cell 2 (Daniell)'}`, 22, 64, { size: 9.5, weight: 700, color: '#ffd584' });

    for (let row = 0; row < 4; row++) {
      const yy = g.yTop + row * g.gap;
      ctx.strokeStyle = '#F59E0B';
      ctx.lineWidth = 2.4;
      ctx.beginPath();
      ctx.moveTo(g.x0, yy);
      ctx.lineTo(g.x1, yy);
      ctx.stroke();
      const startCm = row % 2 === 0 ? row * 100 : (row + 1) * 100;
      labelText(ctx, String(startCm), row % 2 === 0 ? g.x0 - 4 : g.x1 + 4, yy + 3, {
        size: 8.5, weight: 600, align: row % 2 === 0 ? 'right' : 'left', color: 'rgba(232,238,251,0.7)',
      });
      if (row < 3) {
        const xEnd = row % 2 === 0 ? g.x1 + 10 : g.x0 - 10;
        ctx.strokeStyle = 'rgba(199,212,234,0.5)';
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.moveTo(xEnd, yy);
        ctx.lineTo(xEnd, yy + g.gap);
        ctx.stroke();
      }
    }

    const row = Math.min(3, Math.floor(jockey / 100));
    const along = (jockey - row * 100) / 100;
    const fx = row % 2 === 0 ? g.x0 + (g.x1 - g.x0) * along : g.x1 - (g.x1 - g.x0) * along;
    const fy = g.yTop + row * g.gap;
    ctx.fillStyle = dragging ? '#ffd584' : '#9ec1ff';
    ctx.beginPath();
    ctx.moveTo(fx - 8, fy - 18);
    ctx.lineTo(fx, fy - 2);
    ctx.lineTo(fx + 8, fy - 18);
    ctx.closePath();
    ctx.fill();
    labelText(ctx, `jockey: ${fmt(jockey, 1)} cm`, w * 0.5, g.yTop + 3 * g.gap + 30, { size: 10.5, weight: 700, align: 'center', color: dragging ? '#ffd584' : '#9ec1ff' });

    kOut.set(`${fmt(gradient() * 100, 3)} V/m`);
    l1Out.set(l1 === null ? '—' : `${fmt(l1, 1)} cm`);
    l2Out.set(l2 === null ? '—' : `${fmt(l2, 1)} cm`);
    if (l1 !== null && l2 !== null) {
      const ratio = l1 / l2;
      ratioOut.set(revealed
        ? `${fmt(ratio, 3)} (true ${fmt(E1 / E2, 3)})`
        : fmt(ratio, 3));
    } else {
      ratioOut.set('—');
    }
    if (revealed) {
      statusBadge.set(`E₁ = ${fmt(E1, 3)} V · E₂ = ${fmt(E2, 3)} V`);
    } else {
      statusBadge.set(
        Math.abs(defl) < 0.4 ? `NULL at ${fmt(jockey, 1)} cm — record l${cell}`
          : defl > 0 ? 'Deflection + : move jockey back' : 'Deflection − : move jockey forward',
      );
    }
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
