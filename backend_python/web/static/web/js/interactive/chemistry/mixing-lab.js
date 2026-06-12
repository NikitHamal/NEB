import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

function detectTier() {
  const mobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent) || (navigator.maxTouchPoints || 0) > 1;
  const mem = navigator.deviceMemory || 4;
  const cores = navigator.hardwareConcurrency || 4;
  if (mobile && (mem <= 2 || cores <= 4)) return 'low';
  if (mobile || mem <= 4) return 'medium';
  return 'high';
}

const T_SALT = 0;
const T_SAND = 1;
const T_DYE = 2;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Tap an ingredient!', '#10B981');

  const tier = detectTier();
  const MAX = tier === 'low' ? 100 : tier === 'medium' ? 160 : 220;
  const px = new Float32Array(MAX);
  const py = new Float32Array(MAX);
  const vx = new Float32Array(MAX);
  const vy = new Float32Array(MAX);
  const life = new Float32Array(MAX);
  const type = new Uint8Array(MAX);
  let count = 0;

  let water = 0;
  let oil = 0;
  let dye = 0;
  let sandPile = 0;
  let saltPile = 0;
  let stir = 0;

  function beakerRect(w, h) {
    const bw = Math.min(w * 0.5, 260);
    const bh = h * 0.62;
    return { x: w * 0.5 - bw / 2, y: h * 0.5 - bh / 2 + 14, w: bw, h: bh };
  }

  function levels(bk) {
    const waterH = bk.h * 0.5 * water;
    const oilH = bk.h * 0.3 * oil;
    const waterY = bk.y + bk.h - waterH;
    return { waterH, waterY, oilH, oilY: waterY - oilH };
  }

  function spawn(t, n, bk) {
    for (let i = 0; i < n && count < MAX; i++) {
      const k = count++;
      px[k] = bk.x + bk.w * (0.3 + Math.random() * 0.4);
      py[k] = bk.y - 14 - Math.random() * 18;
      vx[k] = (Math.random() - 0.5) * 24;
      vy[k] = 20 + Math.random() * 30;
      life[k] = 1;
      type[k] = t;
    }
  }

  function kill(i) {
    count--;
    px[i] = px[count]; py[i] = py[count];
    vx[i] = vx[count]; vy[i] = vy[count];
    life[i] = life[count]; type[i] = type[count];
  }

  const panel = createPanel(stage, { title: 'Kitchen Shelf' });
  const what = panel.readout({ label: 'What happened?', value: '—' });
  panel.divider();
  panel.section('Add ingredients');
  function say(msg, color) {
    what.set(msg);
    badge.set(msg);
    badge.el.style.setProperty('--ix-hud-color', color || '#10B981');
  }
  panel.buttonRow([
    { label: 'Water', icon: 'water_drop', onClick: () => { water = Math.min(1, water + 0.5); say('Water poured in!', '#3b82f6'); } },
    { label: 'Oil', icon: 'opacity', onClick: () => {
      oil = Math.min(1, oil + 0.5);
      say(water > 0 ? 'Oil FLOATS on water — less dense!' : 'Oil poured in.', '#facc15');
    } },
  ]);
  panel.buttonRow([
    { label: 'Salt', icon: 'grain', onClick: (e) => {
      spawn(T_SALT, 22, beakerRect(sim.width, sim.height));
      say(water > 0 ? 'Salt DISSOLVES — it vanishes!' : 'No water — salt just sits there.', '#e2e8f0');
    } },
    { label: 'Sand', icon: 'landscape', onClick: () => {
      spawn(T_SAND, 22, beakerRect(sim.width, sim.height));
      say('Sand SINKS — it never dissolves.', '#d97706');
    } },
  ]);
  panel.button({ label: 'Food colouring', icon: 'palette', onClick: () => {
    spawn(T_DYE, 26, beakerRect(sim.width, sim.height));
    say(water > 0 ? 'Colour spreads out — DIFFUSION!' : 'Add water first to see it spread!', '#ec4899');
  } });
  panel.divider();
  panel.buttonRow([
    { label: 'Stir!', icon: 'cyclone', onClick: () => { stir = 1; say('Stirring mixes things faster!', '#8b5cf6'); } },
    { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: () => {
      water = 0; oil = 0; dye = 0; sandPile = 0; saltPile = 0; stir = 0; count = 0;
      say('Squeaky clean beaker. Try again!', '#10B981');
    } },
  ]);
  panel.info('Add each ingredient and watch: does it float, sink, dissolve or spread out? Stirring speeds up dissolving and diffusion but never makes sand dissolve!');

  let elapsed = 0;
  sim.setUpdate((ctx, dt, w, h) => {
    dt = Math.min(dt, 0.05);
    elapsed += dt;
    const bk = beakerRect(w, h);
    const lv = levels(bk);
    stir = Math.max(0, stir - dt * 0.25);
    const cx = bk.x + bk.w / 2;
    const cy = bk.y + bk.h - lv.waterH / 2;

    for (let i = count - 1; i >= 0; i--) {
      const inWater = water > 0 && py[i] > lv.waterY;
      const t = type[i];
      if (t === T_SAND || (t === T_SALT && !inWater)) {
        vy[i] += (inWater ? 90 : 240) * dt;
        vx[i] *= 1 - Math.min(1, dt * 2);
      } else {
        vx[i] += (Math.random() - 0.5) * (inWater ? 160 : 30) * dt;
        vy[i] += inWater ? (Math.random() - 0.5) * 160 * dt : 200 * dt;
        vx[i] *= 1 - Math.min(1, dt * 1.6);
        vy[i] *= 1 - Math.min(1, dt * (inWater ? 1.6 : 0.1));
      }
      if (stir > 0 && inWater) {
        const dx = px[i] - cx;
        const dy = py[i] - cy;
        vx[i] += -dy * stir * 6 * dt * 10;
        vy[i] += dx * stir * 6 * dt * 10;
      }
      px[i] += vx[i] * dt;
      py[i] += vy[i] * dt;
      if (px[i] < bk.x + 6) { px[i] = bk.x + 6; vx[i] *= -0.4; }
      if (px[i] > bk.x + bk.w - 6) { px[i] = bk.x + bk.w - 6; vx[i] *= -0.4; }
      const floorY = bk.y + bk.h - 6;
      if (py[i] > floorY) { py[i] = floorY; vy[i] *= -0.2; }
      if (water > 0 && py[i] > lv.waterY) {
        if (t === T_SALT) life[i] -= dt * (0.35 + stir * 1.4);
        if (t === T_DYE) { life[i] -= dt * (0.2 + stir * 1.0); dye = Math.min(1, dye + dt * 0.02); }
      }
      if (t === T_SAND && py[i] >= floorY - 1 && Math.abs(vy[i]) < 12) {
        sandPile = Math.min(1, sandPile + 0.04);
        kill(i);
        continue;
      }
      if (t === T_SALT && water <= 0 && py[i] >= floorY - 1 && Math.abs(vy[i]) < 12) {
        saltPile = Math.min(1, saltPile + 0.04);
        kill(i);
        continue;
      }
      if (life[i] <= 0) kill(i);
    }
    if (saltPile > 0 && water > 0) {
      saltPile = Math.max(0, saltPile - dt * (0.1 + stir * 0.5));
      if (saltPile === 0) say('The salt pile dissolved into the water!', '#e2e8f0');
    }

    ctx.clearRect(0, 0, w, h);

    if (water > 0) {
      const r = Math.round(59 + dye * 177);
      const g = Math.round(130 - dye * 58);
      const b = Math.round(246 - dye * 93);
      ctx.fillStyle = `rgba(${r},${g},${b},0.65)`;
      ctx.fillRect(bk.x + 3, lv.waterY, bk.w - 6, lv.waterH - 3);
      const wob = Math.sin(elapsed * 3) * 2 * stir * 4;
      ctx.strokeStyle = 'rgba(255,255,255,0.35)';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(bk.x + 3, lv.waterY + wob);
      ctx.lineTo(bk.x + bk.w - 3, lv.waterY - wob);
      ctx.stroke();
    }
    if (oil > 0) {
      ctx.fillStyle = 'rgba(250,204,21,0.6)';
      ctx.fillRect(bk.x + 3, lv.oilY, bk.w - 6, lv.oilH);
    }
    if (sandPile > 0 || saltPile > 0) {
      const baseY = bk.y + bk.h - 3;
      if (sandPile > 0) {
        ctx.fillStyle = 'rgba(217,119,6,0.9)';
        ctx.beginPath();
        ctx.moveTo(bk.x + 4, baseY);
        ctx.quadraticCurveTo(bk.x + bk.w * 0.35, baseY - 26 * sandPile, bk.x + bk.w * 0.6, baseY);
        ctx.fill();
      }
      if (saltPile > 0) {
        ctx.fillStyle = 'rgba(241,245,249,0.9)';
        ctx.beginPath();
        ctx.moveTo(bk.x + bk.w * 0.4, baseY);
        ctx.quadraticCurveTo(bk.x + bk.w * 0.65, baseY - 22 * saltPile, bk.x + bk.w - 4, baseY);
        ctx.fill();
      }
    }

    for (let i = 0; i < count; i++) {
      const t = type[i];
      if (t === T_SALT) ctx.fillStyle = `rgba(248,250,252,${0.95 * life[i]})`;
      else if (t === T_SAND) ctx.fillStyle = 'rgba(217,119,6,0.95)';
      else ctx.fillStyle = `rgba(236,72,153,${0.85 * life[i]})`;
      ctx.beginPath();
      ctx.arc(px[i], py[i], t === T_DYE ? 4 : 3, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.strokeStyle = 'rgba(199,212,234,0.9)';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(bk.x - 8, bk.y - 10);
    ctx.lineTo(bk.x, bk.y);
    ctx.lineTo(bk.x, bk.y + bk.h);
    ctx.lineTo(bk.x + bk.w, bk.y + bk.h);
    ctx.lineTo(bk.x + bk.w, bk.y);
    ctx.lineTo(bk.x + bk.w + 8, bk.y - 10);
    ctx.stroke();
    ctx.fillStyle = 'rgba(199,212,234,0.7)';
    ctx.font = '600 11px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('the mixing beaker', bk.x + bk.w / 2, bk.y + bk.h + 20);
    if (oil > 0 && water > 0) {
      ctx.textAlign = 'left';
      ctx.fillText('oil (floats!)', bk.x + bk.w + 12, lv.oilY + lv.oilH / 2 + 4);
      ctx.fillText('water', bk.x + bk.w + 12, lv.waterY + lv.waterH / 2 + 4);
    }
    if (stir > 0) {
      ctx.strokeStyle = `rgba(139,92,246,${stir})`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(cx, cy, 18 + Math.sin(elapsed * 6) * 4, elapsed * 4, elapsed * 4 + 4);
      ctx.stroke();
    }
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
