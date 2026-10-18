import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

// Height-and-distance bench: stand a known distance from a tower, read the
// angle of elevation, and find the height with tan θ. Also solves the reverse:
// given the height, find the angle or the distance.

const ACCENT = '#F59E0B';
const BLUE = '#38bdf8';
const GREEN = '#34d399';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('tan θ = height ⁄ distance — measure one angle, find an unknown height', ACCENT);

  let distance = 30;   // m
  let angle = 30;      // degrees
  let eye = 1.5;       // m, height of the instrument above the ground
  let unknown = 'height'; // height | distance | angle

  const panel = createPanel(stage, { title: 'Theodolite bench' });
  const modeSel = panel.select({
    label: 'What is unknown?',
    options: [
      { value: 'height', label: 'Height of the tower' },
      { value: 'distance', label: 'Distance to the tower' },
      { value: 'angle', label: 'Angle of elevation' },
    ],
    value: unknown,
    onChange: (v) => { unknown = v; },
  });
  const distSlider = panel.slider({
    label: 'Horizontal distance d',
    min: 5, max: 120, step: 1, value: distance, unit: ' m',
    onChange: (v) => { distance = v; },
  });
  const angSlider = panel.slider({
    label: 'Angle of elevation θ',
    min: 2, max: 80, step: 1, value: angle, unit: '°',
    onChange: (v) => { angle = v; },
  });
  panel.slider({
    label: 'Height of the instrument',
    min: 0, max: 3, step: 0.1, value: eye, unit: ' m',
    onChange: (v) => { eye = v; },
  });
  const readTan = panel.readout({ label: 'tan θ', value: '—' });
  const readH = panel.readout({ label: 'Height above the instrument', value: '—' });
  const readTotal = panel.readout({ label: 'Total height of the tower', value: '—' });
  const readFormula = panel.readout({ label: 'Working', value: '—' });
  panel.info('tan θ = (height − instrument height) ⁄ distance. Add the instrument height back at the end.');

  function draw(ctx, w, h) {
    ctx.clearRect(0, 0, w, h);

    const rad = (angle * Math.PI) / 180;
    const hAbove = distance * Math.tan(rad);
    const total = hAbove + eye;

    // Layout: the tower sits fixed on the right, the ground at h*0.82
    const ground = h * 0.82;
    const towerX = w * 0.78;
    const eyeX = w * 0.16;
    // scale so that the tower always fits: world metres -> px
    const worldW = distance + 12;
    const worldH = Math.max(total + 6, 12);
    const scale = Math.min((towerX - eyeX) / worldW, (ground - h * 0.12) / worldH);
    const px = (m) => eyeX + m * scale;
    const py = (m) => ground - m * scale;

    // sky + ground
    const sky = ctx.createLinearGradient(0, 0, 0, ground);
    sky.addColorStop(0, 'rgba(56,116,203,0.28)');
    sky.addColorStop(1, 'rgba(12,24,44,0.1)');
    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, w, ground);
    ctx.fillStyle = 'rgba(120,113,88,0.32)';
    ctx.fillRect(0, ground, w, h - ground);

    // tower (a simple rectangular block tower with a mast)
    const tw = Math.max(16, scale * 3);
    ctx.fillStyle = 'rgba(226,232,240,0.9)';
    ctx.fillRect(towerX - tw / 2, py(total), tw, ground - py(total));
    ctx.strokeStyle = 'rgba(15,23,42,0.5)';
    ctx.lineWidth = 1;
    ctx.strokeRect(towerX - tw / 2, py(total), tw, ground - py(total));
    for (let i = 1; i * 3 < total; i++) {
      const y = py(i * 3);
      ctx.beginPath(); ctx.moveTo(towerX - tw / 2, y); ctx.lineTo(towerX + tw / 2, y); ctx.stroke();
    }
    ctx.strokeStyle = 'rgba(226,232,240,0.9)';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(towerX, py(total)); ctx.lineTo(towerX, py(total + 2)); ctx.stroke();

    // horizontal line at the instrument
    ctx.strokeStyle = 'rgba(199,212,234,0.5)';
    ctx.setLineDash([5, 4]);
    ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.moveTo(eyeX, py(eye)); ctx.lineTo(towerX - tw / 2, py(eye)); ctx.stroke();
    ctx.setLineDash([]);

    // sight line
    ctx.strokeStyle = ACCENT;
    ctx.lineWidth = 2.2;
    ctx.beginPath();
    ctx.moveTo(eyeX, py(eye));
    ctx.lineTo(towerX, py(total));
    ctx.stroke();

    // right angle marker
    ctx.strokeStyle = 'rgba(199,212,234,0.8)';
    ctx.lineWidth = 1.2;
    const rq = 10;
    ctx.strokeRect(towerX - tw / 2, py(eye) - rq, rq, rq);

    // angle arc
    ctx.strokeStyle = GREEN;
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    ctx.arc(eyeX, py(eye), 30, -rad, 0);
    ctx.stroke();
    ctx.fillStyle = GREEN;
    ctx.font = '700 11px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(`θ = ${angle}°`, eyeX + 36, py(eye) - 8);

    // dimensions
    ctx.strokeStyle = 'rgba(56,189,248,0.9)';
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.moveTo(eyeX, ground + 20);
    ctx.lineTo(towerX - tw / 2, ground + 20);
    ctx.stroke();
    ctx.fillStyle = BLUE;
    ctx.font = '700 10.5px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`d = ${distance} m`, (eyeX + towerX - tw / 2) / 2, ground + 36);

    ctx.strokeStyle = ACCENT;
    ctx.beginPath();
    ctx.moveTo(towerX + tw / 2 + 10, py(total));
    ctx.lineTo(towerX + tw / 2 + 10, py(eye));
    ctx.stroke();
    ctx.fillStyle = ACCENT;
    ctx.textAlign = 'left';
    ctx.fillText(`${hAbove.toFixed(2)} m`, towerX + tw / 2 + 16, (py(total) + py(eye)) / 2);

    // instrument
    ctx.fillStyle = 'rgba(226,232,240,0.95)';
    ctx.fillRect(eyeX - 8, py(eye), 16, ground - py(eye));
    ctx.beginPath(); ctx.arc(eyeX, py(eye) - 6, 6, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = 'rgba(199,212,234,0.85)';
    ctx.font = '600 9.5px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`theodolite ${eye.toFixed(1)} m`, eyeX, ground + 14);

    // working panel
    const bx = w * 0.03;
    const by = h * 0.06;
    const bw = Math.min(268, w * 0.42);
    const bh = 96;
    ctx.fillStyle = 'rgba(8,16,30,0.82)';
    ctx.strokeStyle = 'rgba(158,193,255,0.25)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(bx, by, bw, bh, 8); else ctx.rect(bx, by, bw, bh);
    ctx.fill(); ctx.stroke();
    ctx.textAlign = 'left';
    ctx.fillStyle = ACCENT;
    ctx.font = '700 11px Poppins, sans-serif';
    ctx.fillText('tan θ = height ⁄ distance', bx + 14, by + 22);

    let working = '';
    if (unknown === 'height') {
      working = [`tan ${angle}° = h ⁄ ${distance}`, `h = ${distance} × ${Math.tan(rad).toFixed(4)} = ${hAbove.toFixed(2)} m`, `total height = ${hAbove.toFixed(2)} + ${eye.toFixed(1)} = ${total.toFixed(2)} m`];
    } else if (unknown === 'distance') {
      const d = hAbove / Math.tan(rad);
      working = [`tan ${angle}° = h ⁄ d`, `d = ${hAbove.toFixed(2)} ⁄ ${Math.tan(rad).toFixed(4)} = ${d.toFixed(2)} m`, `(measured height ${hAbove.toFixed(2)} m, instrument ${eye.toFixed(1)} m)`];
    } else {
      working = [`tan θ = ${hAbove.toFixed(2)} ⁄ ${distance}`, `tan θ = ${(hAbove / distance).toFixed(4)}`, `θ = ${((Math.atan(hAbove / distance) * 180) / Math.PI).toFixed(2)}°`];
    }
    ctx.fillStyle = 'rgba(232,238,251,0.92)';
    ctx.font = '600 10.5px Poppins, sans-serif';
    working.forEach((line, i) => ctx.fillText(line, bx + 14, by + 44 + i * 17));

    readTan.set(Math.tan(rad).toFixed(4));
    readH.set(`${hAbove.toFixed(2)} m`);
    readTotal.set(`${total.toFixed(2)} m`);
    readFormula.set(working[0]);
    void modeSel; void distSlider; void angSlider;
  }

  // the canvas helper calls (ctx, dt, width, height); draw wants (ctx, width, height)
  sim.setUpdate((ctx, dt, w, h) => draw(ctx, w, h));
  sim.onResize(() => sim.renderOnce());
  sim.start();

  return { dispose() { sim.dispose(); hud.dispose(); panel.dispose(); } };
}
