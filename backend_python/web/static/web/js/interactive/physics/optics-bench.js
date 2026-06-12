import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const RAY_COLORS = ['#7dd3fc', '#f472b6', '#a3e635'];

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const natureBadge = hud.badge('Real · inverted', '#F59E0B');

  let element = 'convex-lens';
  let fMag = 40;
  let objDist = 100;
  const objH = 32;
  let dragging = false;

  const panel = createPanel(stage, { title: 'Optics Controls' });
  panel.select({
    label: 'Optical element',
    options: [
      { value: 'convex-lens', label: 'Converging (convex) lens' },
      { value: 'concave-lens', label: 'Diverging (concave) lens' },
      { value: 'concave-mirror', label: 'Concave mirror' },
      { value: 'convex-mirror', label: 'Convex mirror' },
    ],
    value: element,
    onChange: (v) => { element = v; },
  });
  panel.slider({
    label: 'Focal length |f|',
    min: 20, max: 90, step: 1, value: fMag,
    format: (v) => `${v} cm`,
    onChange: (v) => { fMag = v; },
  });
  panel.divider();
  const uOut = panel.readout({ label: 'Object distance u', value: '—' });
  const vOut = panel.readout({ label: 'Image distance v', value: '—' });
  const mOut = panel.readout({ label: 'Magnification m', value: '—' });
  const natOut = panel.readout({ label: 'Image is', value: '—' });
  panel.info('Drag the golden object arrow along the bench. Watch the three principal rays meet at the image — or only their dashed extensions for a virtual image.');

  function isMirror() { return element.endsWith('mirror'); }
  function focal() { return element === 'convex-lens' || element === 'concave-mirror' ? fMag : -fMag; }

  function geometry(w, h) {
    const cx = w * 0.56;
    const axisY = h * 0.46;
    const scale = Math.min((w * 0.52) / 200, (w * 0.4) / 130);
    return { cx, axisY, scale };
  }

  function toScreen(geo, x, y) {
    return { x: geo.cx + x * geo.scale, y: geo.axisY - y * geo.scale };
  }

  function compute() {
    const f = focal();
    const denom = objDist - f;
    if (Math.abs(denom) < 2) return { atFocus: true, f };
    const di = (f * objDist) / denom;
    const hi = (-objH * di) / objDist;
    const m = -di / objDist;
    return { atFocus: false, f, di, hi, m, real: di > 0 };
  }

  function imageWorldX(res) {
    return isMirror() ? -res.di : res.di;
  }

  function drawArrow(ctx, geo, wx, wTipY, color, alpha) {
    const base = toScreen(geo, wx, 0);
    const tip = toScreen(geo, wx, wTipY);
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(base.x, base.y);
    ctx.lineTo(tip.x, tip.y);
    ctx.stroke();
    const dir = wTipY >= 0 ? -1 : 1;
    ctx.beginPath();
    ctx.moveTo(tip.x, tip.y);
    ctx.lineTo(tip.x - 6, tip.y + dir * 10);
    ctx.lineTo(tip.x + 6, tip.y + dir * 10);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }

  function rayLine(ctx, geo, p1, p2, color, dashed) {
    const a = toScreen(geo, p1.x, p1.y);
    const b = toScreen(geo, p2.x, p2.y);
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.6;
    if (dashed) ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.stroke();
    if (dashed) ctx.setLineDash([]);
  }

  function extendFrom(p, dir, limit) {
    const len = Math.hypot(dir.x, dir.y) || 1;
    const t = limit / len;
    return { x: p.x + dir.x * t, y: p.y + dir.y * t };
  }

  function drawRays(ctx, geo, res, w) {
    const O = { x: -objDist, y: objH };
    const f = res.f;
    const mirror = isMirror();
    const forward = mirror ? -1 : 1;
    const reach = (w / geo.scale);

    const tF = objDist / (objDist - f);
    const hitPoints = [
      { x: 0, y: objH },
      { x: 0, y: 0 },
      Number.isFinite(tF) && Math.abs(objDist - f) > 2 ? { x: 0, y: objH * (1 - tF) } : null,
    ];

    hitPoints.forEach((P, i) => {
      if (!P || Math.abs(P.y) > 90) return;
      const color = RAY_COLORS[i];
      rayLine(ctx, geo, O, P, color, false);
      if (res.atFocus) {
        const d2 = { x: forward, y: -O.y / objDist };
        const end = extendFrom(P, d2, reach);
        rayLine(ctx, geo, P, end, color, false);
        return;
      }
      const I = { x: imageWorldX(res), y: res.hi };
      let dir = { x: I.x - P.x, y: I.y - P.y };
      if (dir.x * forward < 0) dir = { x: -dir.x, y: -dir.y };
      if (Math.abs(dir.x) < 0.001) dir.x = forward * 0.001;
      const end = extendFrom(P, dir, reach);
      rayLine(ctx, geo, P, end, color, false);
      if (!res.real) {
        rayLine(ctx, geo, P, I, color, true);
      }
    });
  }

  function drawElement(ctx, geo, h) {
    const halfH = Math.min(h * 0.3, 120);
    const top = { x: geo.cx, y: geo.axisY - halfH };
    const bot = { x: geo.cx, y: geo.axisY + halfH };
    ctx.lineWidth = 3;
    ctx.strokeStyle = 'rgba(199,212,234,0.9)';
    if (element === 'convex-lens' || element === 'concave-lens') {
      const bulge = element === 'convex-lens' ? 16 : -14;
      ctx.fillStyle = 'rgba(125,211,252,0.12)';
      ctx.beginPath();
      ctx.moveTo(top.x, top.y);
      ctx.quadraticCurveTo(geo.cx + bulge, geo.axisY, bot.x, bot.y);
      ctx.quadraticCurveTo(geo.cx - bulge, geo.axisY, top.x, top.y);
      ctx.fill();
      ctx.stroke();
      ctx.beginPath();
      const ah = element === 'convex-lens' ? 8 : -8;
      ctx.moveTo(top.x - 6, top.y + ah); ctx.lineTo(top.x, top.y); ctx.lineTo(top.x + 6, top.y + ah);
      ctx.moveTo(bot.x - 6, bot.y - ah); ctx.lineTo(bot.x, bot.y); ctx.lineTo(bot.x + 6, bot.y - ah);
      ctx.stroke();
    } else {
      const bend = element === 'concave-mirror' ? 22 : -22;
      ctx.beginPath();
      ctx.moveTo(top.x + (element === 'concave-mirror' ? 10 : -10), top.y);
      ctx.quadraticCurveTo(geo.cx - bend, geo.axisY, bot.x + (element === 'concave-mirror' ? 10 : -10), bot.y);
      ctx.stroke();
      ctx.strokeStyle = 'rgba(199,212,234,0.4)';
      ctx.lineWidth = 1;
      for (let y = -halfH + 10; y < halfH; y += 14) {
        const off = (element === 'concave-mirror' ? 10 : -10) - bend * (1 - (y * y) / (halfH * halfH)) * 0.5;
        ctx.beginPath();
        ctx.moveTo(geo.cx + off, geo.axisY + y);
        ctx.lineTo(geo.cx + off + 8, geo.axisY + y + 8);
        ctx.stroke();
      }
    }
  }

  function onDown(e) {
    const geo = geometry(sim.width, sim.height);
    const p = pointerPos(sim.canvas, e);
    const objScreen = toScreen(geo, -objDist, objH / 2);
    if (Math.abs(p.x - objScreen.x) < 40 && Math.abs(p.y - geo.axisY + (objH * geo.scale) / 2) < objH * geo.scale + 40) {
      dragging = true;
      sim.canvas.setPointerCapture && sim.canvas.setPointerCapture(e.pointerId);
      e.preventDefault();
    }
  }

  function onMove(e) {
    if (!dragging) return;
    const geo = geometry(sim.width, sim.height);
    const p = pointerPos(sim.canvas, e);
    const wx = (p.x - geo.cx) / geo.scale;
    objDist = Math.max(12, Math.min(190, -wx));
  }

  function onUp() { dragging = false; }

  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onDown);
  sim.canvas.addEventListener('pointermove', onMove);
  sim.canvas.addEventListener('pointerup', onUp);
  sim.canvas.addEventListener('pointercancel', onUp);

  sim.setUpdate((ctx, dt, w, h) => {
    ctx.clearRect(0, 0, w, h);
    const geo = geometry(w, h);
    const f = focal();

    ctx.strokeStyle = 'rgba(158,193,255,0.3)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(10, geo.axisY);
    ctx.lineTo(w - 10, geo.axisY);
    ctx.stroke();

    ctx.fillStyle = 'rgba(199,212,234,0.55)';
    ctx.font = '600 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    for (let x = -180; x <= 180; x += 20) {
      const s = toScreen(geo, x, 0);
      if (s.x < 14 || s.x > w - 14) continue;
      ctx.beginPath();
      ctx.moveTo(s.x, geo.axisY - 3);
      ctx.lineTo(s.x, geo.axisY + 3);
      ctx.stroke();
      if (x % 40 === 0) ctx.fillText(`${Math.abs(x)}`, s.x, geo.axisY + 16);
    }

    ctx.fillStyle = '#fbbf24';
    const fPts = isMirror()
      ? [{ x: -f, label: 'F' }]
      : [{ x: -Math.abs(f), label: 'F' }, { x: Math.abs(f), label: "F'" }];
    fPts.forEach((fp) => {
      const pt = toScreen(geo, fp.x, 0);
      ctx.beginPath();
      ctx.arc(pt.x, geo.axisY, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillText(fp.label, pt.x, geo.axisY - 10);
    });
    if (isMirror()) {
      const c = toScreen(geo, -2 * f, 0);
      ctx.fillStyle = '#fb923c';
      ctx.beginPath();
      ctx.arc(c.x, geo.axisY, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillText('C', c.x, geo.axisY - 10);
    }

    drawElement(ctx, geo, h);

    const res = compute();
    drawRays(ctx, geo, res, w);
    drawArrow(ctx, geo, -objDist, objH, '#F59E0B', 1);
    ctx.fillStyle = 'rgba(245,158,11,0.9)';
    ctx.font = '700 11px Poppins, sans-serif';
    const objS = toScreen(geo, -objDist, objH);
    ctx.fillText('object', objS.x, objS.y - 12);

    uOut.set(`${objDist.toFixed(0)} cm`);
    if (res.atFocus) {
      vOut.set('∞');
      mOut.set('—');
      natOut.set('No image (at focus)');
      natureBadge.set('Rays emerge parallel — no image');
    } else {
      const ix = imageWorldX(res);
      drawArrow(ctx, geo, ix, res.hi, res.real ? '#8be9a8' : '#c4b5fd', res.real ? 1 : 0.85);
      const imgS = toScreen(geo, ix, res.hi);
      ctx.fillStyle = res.real ? 'rgba(139,233,168,0.9)' : 'rgba(196,181,253,0.9)';
      ctx.fillText(res.real ? 'real image' : 'virtual image', imgS.x, imgS.y + (res.hi >= 0 ? -12 : 16));
      vOut.set(`${Math.abs(res.di).toFixed(1)} cm ${res.real ? '(real)' : '(virtual)'}`);
      mOut.set(`${res.m.toFixed(2)}×`);
      const upright = res.m > 0;
      const size = Math.abs(res.m) > 1.02 ? 'magnified' : Math.abs(res.m) < 0.98 ? 'reduced' : 'same size';
      natOut.set(`${res.real ? 'Real' : 'Virtual'}, ${upright ? 'upright' : 'inverted'}, ${size}`);
      natureBadge.set(`${res.real ? 'Real' : 'Virtual'} · ${upright ? 'upright' : 'inverted'} · ${size}`);
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
