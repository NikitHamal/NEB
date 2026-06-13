import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const LIQUIDS = {
  honey: { label: 'Honey', d: 1.42, color: 'rgba(217,119,6,0.85)' },
  syrup: { label: 'Syrup', d: 1.37, color: 'rgba(139,92,246,0.8)' },
  water: { label: 'Water', d: 1.0, color: 'rgba(59,130,246,0.7)' },
  oil: { label: 'Oil', d: 0.92, color: 'rgba(250,204,21,0.7)' },
  alcohol: { label: 'Alcohol', d: 0.79, color: 'rgba(165,243,252,0.5)' },
};

const OBJECTS = {
  grape: { label: 'Grape', d: 1.1, color: '#7c3aed', r: 9 },
  ice: { label: 'Ice cube', d: 0.92, color: '#bae6fd', r: 10, square: true },
  cork: { label: 'Cork', d: 0.24, color: '#d4a373', r: 9, square: true },
  coin: { label: 'Coin', d: 8.9, color: '#fbbf24', r: 8 },
};

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Pour your first liquid!', '#10B981');

  const layers = [];
  const dropped = [];

  function glassRect(w, h) {
    const gw = Math.min(w * 0.34, 170);
    const gh = h * 0.74;
    return { x: w * 0.5 - gw / 2, y: h * 0.5 - gh / 2 + 8, w: gw, h: gh };
  }

  function retarget(gl) {
    const unit = gl.h / 5.4;
    const sorted = layers.slice().sort((a, b) => b.liq.d - a.liq.d);
    let yTop = gl.y + gl.h;
    sorted.forEach((layer) => {
      yTop -= unit;
      layer.ty = yTop;
      layer.th = unit;
    });
  }

  function objectTargetY(gl, obj) {
    if (!layers.length) return gl.y + gl.h - obj.r - 3;
    const sorted = layers.slice().sort((a, b) => a.liq.d - b.liq.d);
    for (let i = 0; i < sorted.length; i++) {
      if (sorted[i].liq.d >= obj.d) {
        return sorted[i].ty + obj.r * 0.4;
      }
    }
    return gl.y + gl.h - obj.r - 3;
  }

  function settleMessage(obj) {
    if (!layers.length) return `${obj.label} hit the empty glass!`;
    const sorted = layers.slice().sort((a, b) => a.liq.d - b.liq.d);
    for (let i = 0; i < sorted.length; i++) {
      if (sorted[i].liq.d >= obj.d) {
        return `${obj.label} (${obj.d} g/mL) floats on ${sorted[i].liq.label.toLowerCase()}!`;
      }
    }
    return `${obj.label} (${obj.d} g/mL) sank past everything!`;
  }

  const panel = createPanel(stage, { title: 'Density Tower' });
  panel.section('Pour a liquid');
  const pourBtns = {};
  function makePour(key) {
    return () => {
      if (layers.some((l) => l.key === key)) return;
      const gl = glassRect(sim.width, sim.height);
      const liq = LIQUIDS[key];
      layers.push({ key, liq, ty: gl.y - 30, th: 0, y: gl.y - 60, h: 0 });
      retarget(gl);
      pourBtns[key].setLabel(`${liq.label} ✓`);
      badge.set(`${liq.label} (${liq.d.toFixed(2)} g/mL) finds its place…`);
      badge.el.style.setProperty('--ix-hud-color', '#10B981');
    };
  }
  Object.entries(LIQUIDS).forEach(([key, liq], i) => {
    if (i % 2 === 0) {
      const next = Object.entries(LIQUIDS)[i + 1];
      const row = panel.buttonRow([
        { label: `${liq.label} ${liq.d.toFixed(2)}`, onClick: makePour(key) },
        ...(next ? [{ label: `${next[1].label} ${next[1].d.toFixed(2)}`, onClick: makePour(next[0]) }] : []),
      ]);
      pourBtns[key] = row[0];
      if (next) pourBtns[next[0]] = row[1];
    }
  });
  panel.divider();
  panel.section('Drop an object');
  const objEntries = Object.entries(OBJECTS);
  for (let i = 0; i < objEntries.length; i += 2) {
    panel.buttonRow(objEntries.slice(i, i + 2).map(([key, obj]) => ({
      label: obj.label,
      onClick: () => {
        if (dropped.some((d) => d.key === key)) return;
        const gl = glassRect(sim.width, sim.height);
        dropped.push({ key, obj, x: gl.x + gl.w * (0.3 + Math.random() * 0.4), y: gl.y - 24, vy: 0, settled: false });
        badge.set(`${obj.label}: density ${obj.d} g/mL — where will it stop?`);
        badge.el.style.setProperty('--ix-hud-color', '#fbbf24');
      },
    })));
  }
  panel.divider();
  panel.button({
    label: 'Empty the glass',
    icon: 'replay',
    variant: 'ghost',
    onClick: () => {
      layers.length = 0;
      dropped.length = 0;
      Object.entries(LIQUIDS).forEach(([key, liq]) => pourBtns[key].setLabel(`${liq.label} ${liq.d.toFixed(2)}`));
      badge.set('Pour your first liquid!');
      badge.el.style.setProperty('--ix-hud-color', '#10B981');
    },
  });
  panel.info('Denser liquids always sink below lighter ones — no matter what order you pour! Each object floats on the first liquid that is denser than itself.');

  sim.setUpdate((ctx, dt, w, h) => {
    dt = Math.min(dt, 0.05);
    const gl = glassRect(w, h);
    retarget(gl);

    ctx.clearRect(0, 0, w, h);

    for (let i = 0; i < layers.length; i++) {
      const l = layers[i];
      const k = Math.min(1, dt * 4);
      l.y += (l.ty - l.y) * k;
      l.h += (l.th - l.h) * k;
      ctx.fillStyle = l.liq.color;
      ctx.fillRect(gl.x + 3, l.y, gl.w - 6, l.h);
    }

    ctx.strokeStyle = 'rgba(199,212,234,0.9)';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(gl.x, gl.y - 6);
    ctx.lineTo(gl.x, gl.y + gl.h);
    ctx.lineTo(gl.x + gl.w, gl.y + gl.h);
    ctx.lineTo(gl.x + gl.w, gl.y - 6);
    ctx.stroke();

    ctx.font = '600 11px Poppins, sans-serif';
    for (let i = 0; i < layers.length; i++) {
      const l = layers[i];
      if (l.h < 8) continue;
      ctx.fillStyle = 'rgba(255,255,255,0.95)';
      ctx.textAlign = 'left';
      ctx.fillText(`${l.liq.label} ${l.liq.d.toFixed(2)} g/mL`, gl.x + gl.w + 10, l.y + l.h / 2 + 4);
      ctx.strokeStyle = 'rgba(199,212,234,0.35)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(gl.x + gl.w + 2, l.y + l.h / 2);
      ctx.lineTo(gl.x + gl.w + 8, l.y + l.h / 2);
      ctx.stroke();
    }

    for (let i = 0; i < dropped.length; i++) {
      const d = dropped[i];
      const targetY = objectTargetY(gl, d.obj);
      if (!d.settled) {
        d.vy += 320 * dt;
        d.y += d.vy * dt;
        if (d.y >= targetY) {
          d.y = targetY;
          d.vy = 0;
          d.settled = true;
          badge.set(settleMessage(d.obj));
          badge.el.style.setProperty('--ix-hud-color', d.obj.color);
        }
      } else {
        d.y += (targetY - d.y) * Math.min(1, dt * 3);
      }
      ctx.fillStyle = d.obj.color;
      if (d.obj.square) {
        ctx.fillRect(d.x - d.obj.r, d.y - d.obj.r, d.obj.r * 2, d.obj.r * 2);
      } else {
        ctx.beginPath();
        ctx.arc(d.x, d.y, d.obj.r, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.fillStyle = 'rgba(15,23,42,0.85)';
      ctx.textAlign = 'center';
      ctx.font = '700 8px Poppins, sans-serif';
      ctx.fillText(d.obj.d.toFixed(2), d.x, d.y + 3);
      ctx.font = '600 11px Poppins, sans-serif';
    }

    ctx.fillStyle = 'rgba(199,212,234,0.7)';
    ctx.textAlign = 'center';
    ctx.fillText('lighter floats up · denser sinks down', gl.x + gl.w / 2, gl.y + gl.h + 20);
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
