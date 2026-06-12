import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const currentBadge = hud.badge('I = 0 A', '#F59E0B');

  let V = 12;
  let R1 = 6;
  let R2 = 6;
  let mode = 'single';
  let paths = [];
  let lastKey = '';

  const panel = createPanel(stage, { title: 'Circuit Controls' });
  panel.slider({
    label: 'Battery voltage',
    min: 0, max: 24, step: 0.5, value: V,
    format: (v) => `${v.toFixed(1)} V`,
    onChange: (v) => { V = v; },
  });
  panel.slider({
    label: 'Resistance R₁',
    min: 1, max: 20, step: 0.5, value: R1,
    format: (v) => `${v.toFixed(1)} Ω`,
    onChange: (v) => { R1 = v; },
  });
  panel.select({
    label: 'Circuit layout',
    options: [
      { value: 'single', label: 'R₁ only' },
      { value: 'series', label: 'Series: R₁ + R₂' },
      { value: 'parallel', label: 'Parallel: R₁ ∥ R₂' },
    ],
    value: mode,
    onChange: (v) => {
      mode = v;
      r2Slider.el.style.display = v === 'single' ? 'none' : '';
    },
  });
  const r2Slider = panel.slider({
    label: 'Resistance R₂',
    min: 1, max: 20, step: 0.5, value: R2,
    format: (v) => `${v.toFixed(1)} Ω`,
    onChange: (v) => { R2 = v; },
  });
  r2Slider.el.style.display = 'none';
  panel.divider();
  const rTotOut = panel.readout({ label: 'Total resistance', value: '—' });
  const iTotOut = panel.readout({ label: 'Current I = V/R', value: '—' });
  const v1Out = panel.readout({ label: 'V across R₁', value: '—' });
  const v2Out = panel.readout({ label: 'V across R₂', value: '—' });
  panel.info('The moving dots are electrons — their speed shows the current. Compare how adding R₂ in series slows them, while parallel speeds the battery dots up.');

  function solve() {
    let rTot, i1, i2, vr1, vr2;
    if (mode === 'single') {
      rTot = R1;
      i1 = V / R1; i2 = 0; vr1 = V; vr2 = 0;
    } else if (mode === 'series') {
      rTot = R1 + R2;
      i1 = V / rTot; i2 = i1;
      vr1 = i1 * R1; vr2 = i2 * R2;
    } else {
      rTot = (R1 * R2) / (R1 + R2);
      vr1 = V; vr2 = V;
      i1 = V / R1; i2 = V / R2;
    }
    return { rTot, iTot: V / rTot, i1, i2, vr1, vr2 };
  }

  function box(w, h) {
    const x0 = Math.max(40, w * 0.1);
    const x1 = w - Math.max(40, w * 0.1);
    const y0 = Math.max(46, h * 0.14);
    const y1 = h - Math.max(60, h * 0.2);
    return { x0, x1, y0, y1, xb: x0 + (x1 - x0) * 0.55 };
  }

  function makePath(points) {
    let len = 0;
    const segs = [];
    for (let i = 0; i < points.length - 1; i++) {
      const d = Math.hypot(points[i + 1].x - points[i].x, points[i + 1].y - points[i].y);
      segs.push({ a: points[i], b: points[i + 1], len: d, start: len });
      len += d;
    }
    const dots = [];
    const n = Math.max(6, Math.floor(len / 30));
    for (let i = 0; i < n; i++) dots.push((i / n) * len);
    return { segs, len, dots, current: 0 };
  }

  function posOnPath(path, s) {
    s = ((s % path.len) + path.len) % path.len;
    for (let i = 0; i < path.segs.length; i++) {
      const seg = path.segs[i];
      if (s <= seg.start + seg.len) {
        const t = (s - seg.start) / seg.len;
        return { x: seg.a.x + (seg.b.x - seg.a.x) * t, y: seg.a.y + (seg.b.y - seg.a.y) * t };
      }
    }
    return path.segs[0].a;
  }

  function rebuildPaths(w, h) {
    const b = box(w, h);
    if (mode === 'parallel') {
      paths = [
        makePath([
          { x: b.x0, y: b.y1 }, { x: b.x0, y: b.y0 }, { x: b.xb, y: b.y0 },
          { x: b.xb, y: b.y1 }, { x: b.x0, y: b.y1 },
        ]),
        makePath([
          { x: b.x0, y: b.y1 }, { x: b.x0, y: b.y0 }, { x: b.x1, y: b.y0 },
          { x: b.x1, y: b.y1 }, { x: b.x0, y: b.y1 },
        ]),
      ];
    } else {
      paths = [
        makePath([
          { x: b.x0, y: b.y1 }, { x: b.x0, y: b.y0 }, { x: b.x1, y: b.y0 },
          { x: b.x1, y: b.y1 }, { x: b.x0, y: b.y1 },
        ]),
      ];
    }
  }

  function drawWireRect(ctx, pts) {
    ctx.strokeStyle = 'rgba(199,212,234,0.8)';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    pts.forEach((p, i) => { if (i === 0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y); });
    ctx.stroke();
  }

  function drawBattery(ctx, x, yMid) {
    ctx.clearRect(x - 14, yMid - 22, 28, 44);
    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(x - 12, yMid - 8);
    ctx.lineTo(x + 12, yMid - 8);
    ctx.stroke();
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x - 5, yMid + 8);
    ctx.lineTo(x + 5, yMid + 8);
    ctx.stroke();
    ctx.fillStyle = '#fbbf24';
    ctx.font = '700 12px Poppins, sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText('+', x - 18, yMid - 6);
    ctx.fillText('−', x - 18, yMid + 14);
  }

  function drawResistor(ctx, x, yMid, label, vDrop, iThrough, glow) {
    const hh = 26;
    if (glow > 0.04) {
      const g = ctx.createRadialGradient(x, yMid, 4, x, yMid, 36 + glow * 18);
      g.addColorStop(0, `rgba(255,180,80,${0.45 * glow})`);
      g.addColorStop(1, 'rgba(255,180,80,0)');
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(x, yMid, 36 + glow * 18, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.strokeStyle = '#e8eefb';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x, yMid - hh);
    let y = yMid - hh + 4;
    let side = 1;
    ctx.lineTo(x, y);
    while (y < yMid + hh - 6) {
      ctx.lineTo(x + side * 7, y + 3);
      y += 6;
      side = -side;
    }
    ctx.lineTo(x, yMid + hh);
    ctx.stroke();
    ctx.fillStyle = '#9ec1ff';
    ctx.font = '700 11px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(label, x + 14, yMid - 6);
    ctx.fillStyle = 'rgba(139,233,168,0.95)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.fillText(`${vDrop.toFixed(1)} V`, x + 14, yMid + 8);
    ctx.fillText(`${iThrough.toFixed(2)} A`, x + 14, yMid + 21);
  }

  function drawMeter(ctx, x, y, letter, value) {
    ctx.fillStyle = '#16233a';
    ctx.strokeStyle = '#7dd3fc';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(x, y, 15, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#7dd3fc';
    ctx.font = '800 13px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(letter, x, y + 1);
    ctx.textBaseline = 'alphabetic';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.fillText(value, x, y - 22);
  }

  function drawBulb(ctx, x, y, brightness) {
    if (brightness > 0.02) {
      const g = ctx.createRadialGradient(x, y, 4, x, y, 30 + brightness * 34);
      g.addColorStop(0, `rgba(255,230,150,${0.75 * brightness})`);
      g.addColorStop(1, 'rgba(255,210,100,0)');
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(x, y, 30 + brightness * 34, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.fillStyle = brightness > 0.05 ? `rgba(255,225,140,${0.25 + 0.6 * brightness})` : '#1c2f4d';
    ctx.strokeStyle = '#c7d4ea';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(x, y, 13, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    const r = 13 / Math.SQRT2;
    ctx.beginPath();
    ctx.moveTo(x - r, y - r); ctx.lineTo(x + r, y + r);
    ctx.moveTo(x - r, y + r); ctx.lineTo(x + r, y - r);
    ctx.stroke();
  }

  sim.setUpdate((ctx, dt, w, h) => {
    const key = `${w}x${h}:${mode}`;
    if (key !== lastKey) {
      rebuildPaths(w, h);
      lastKey = key;
    }
    const sol = solve();
    const b = box(w, h);
    ctx.clearRect(0, 0, w, h);

    if (mode === 'parallel') {
      drawWireRect(ctx, [{ x: b.x0, y: b.y1 }, { x: b.x0, y: b.y0 }, { x: b.x1, y: b.y0 }, { x: b.x1, y: b.y1 }, { x: b.x0, y: b.y1 }]);
      drawWireRect(ctx, [{ x: b.xb, y: b.y0 }, { x: b.xb, y: b.y1 }]);
    } else {
      drawWireRect(ctx, [{ x: b.x0, y: b.y1 }, { x: b.x0, y: b.y0 }, { x: b.x1, y: b.y0 }, { x: b.x1, y: b.y1 }, { x: b.x0, y: b.y1 }]);
    }

    if (mode === 'parallel') {
      paths[0].current = sol.i1;
      paths[1].current = sol.i2;
    } else {
      paths[0].current = sol.iTot;
    }
    ctx.fillStyle = '#60a5fa';
    paths.forEach((path) => {
      const v = Math.min(150, 34 * Math.sqrt(Math.max(0, path.current)));
      for (let i = 0; i < path.dots.length; i++) {
        path.dots[i] = (path.dots[i] + v * dt) % path.len;
        const p = posOnPath(path, path.dots[i]);
        ctx.beginPath();
        ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    const midY = (b.y0 + b.y1) / 2;
    drawBattery(ctx, b.x0, midY);
    ctx.fillStyle = '#fbbf24';
    ctx.font = '700 11px Poppins, sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(`${V.toFixed(1)} V`, b.x0 - 16, midY + 34);

    drawMeter(ctx, b.x0 + (b.x1 - b.x0) * 0.3, b.y0, 'A', `${sol.iTot.toFixed(2)} A`);

    if (mode === 'single') {
      drawResistor(ctx, b.x1, midY, 'R₁', sol.vr1, sol.i1, Math.min(1, (sol.i1 * sol.i1 * R1) / 60));
      drawMeter(ctx, b.x1 - 52, midY, 'V', `${sol.vr1.toFixed(1)} V`);
    } else if (mode === 'series') {
      const yA = b.y0 + (b.y1 - b.y0) * 0.32;
      const yB = b.y0 + (b.y1 - b.y0) * 0.7;
      drawResistor(ctx, b.x1, yA, 'R₁', sol.vr1, sol.i1, Math.min(1, (sol.i1 * sol.i1 * R1) / 60));
      drawResistor(ctx, b.x1, yB, 'R₂', sol.vr2, sol.i2, Math.min(1, (sol.i2 * sol.i2 * R2) / 60));
      drawMeter(ctx, b.x1 - 52, yA, 'V', `${sol.vr1.toFixed(1)} V`);
    } else {
      drawResistor(ctx, b.xb, midY, 'R₁', sol.vr1, sol.i1, Math.min(1, (sol.i1 * sol.i1 * R1) / 60));
      drawResistor(ctx, b.x1, midY, 'R₂', sol.vr2, sol.i2, Math.min(1, (sol.i2 * sol.i2 * R2) / 60));
    }

    drawBulb(ctx, b.x0 + (b.x1 - b.x0) * 0.5, b.y1, Math.min(1, sol.iTot / 4));

    currentBadge.set(`I = ${sol.iTot.toFixed(2)} A`);
    rTotOut.set(`${sol.rTot.toFixed(2)} Ω`);
    iTotOut.set(`${sol.iTot.toFixed(2)} A`);
    v1Out.set(`${sol.vr1.toFixed(1)} V · ${sol.i1.toFixed(2)} A`);
    v2Out.set(mode === 'single' ? '—' : `${sol.vr2.toFixed(1)} V · ${sol.i2.toFixed(2)} A`);
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
