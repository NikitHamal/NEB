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

const SODA_MOLAR = 84;
const ACID_MOL_PER_ML = 0.05 / 60;
const GAS_L_PER_MOL = 24;

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const badge = hud.badge('Mix baking soda + vinegar!', '#10B981');

  const tier = detectTier();
  const MAXB = tier === 'low' ? 50 : tier === 'medium' ? 80 : 120;
  const bx = new Float32Array(MAXB);
  const by = new Float32Array(MAXB);
  const bv = new Float32Array(MAXB);
  const br = new Float32Array(MAXB);
  let bubbles = 0;

  let sodaG = 8;
  let vinegarMl = 100;
  let balloonMode = false;
  let reacting = false;
  let progress = 0;
  let gasLiters = 0;
  let limiting = '';
  let emitTimer = 0;

  function react() {
    const molSoda = sodaG / SODA_MOLAR;
    const molAcid = vinegarMl * ACID_MOL_PER_ML;
    if (molSoda <= 0 || molAcid <= 0) {
      badge.set('You need BOTH ingredients!');
      badge.el.style.setProperty('--ix-hud-color', '#ef4444');
      return;
    }
    const molGas = Math.min(molSoda, molAcid);
    gasLiters = molGas * GAS_L_PER_MOL;
    limiting = Math.abs(molSoda - molAcid) < 1e-4 ? 'perfect' : molSoda < molAcid ? 'soda' : 'vinegar';
    reacting = true;
    progress = 0;
    badge.set('Fizzzz! CO₂ bubbles everywhere!');
    badge.el.style.setProperty('--ix-hud-color', '#22d3ee');
  }

  function reset() {
    reacting = false;
    progress = 0;
    gasLiters = 0;
    limiting = '';
    bubbles = 0;
    badge.set('Mix baking soda + vinegar!');
    badge.el.style.setProperty('--ix-hud-color', '#10B981');
  }

  const panel = createPanel(stage, { title: 'Fizz Controls' });
  panel.slider({
    label: 'Baking soda',
    min: 0, max: 20, step: 1, value: sodaG,
    format: (v) => `${v} g`,
    onChange: (v) => { sodaG = v; },
  });
  panel.slider({
    label: 'Vinegar',
    min: 0, max: 200, step: 10, value: vinegarMl,
    format: (v) => `${v} mL`,
    onChange: (v) => { vinegarMl = v; },
  });
  panel.toggle({
    label: 'Balloon on bottle',
    value: balloonMode,
    onChange: (v) => { balloonMode = v; },
  });
  panel.buttonRow([
    { label: 'Pour & react!', icon: 'science', onClick: react },
    { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: reset },
  ]);
  panel.divider();
  const gasOut = panel.readout({ label: 'CO₂ made', value: '0.0 L' });
  const limOut = panel.readout({ label: 'Ran out first', value: '—' });
  panel.info('Baking soda + vinegar make carbon dioxide gas — totally safe kitchen science! Whichever ingredient runs out first stops the fizz. Try the balloon mode to trap the gas.');

  function layout(w, h) {
    const bw = Math.min(w * 0.3, 150);
    const bh = h * 0.46;
    const x = w * 0.5 - bw / 2;
    const y = h - 50 - bh;
    return { x, y, w: bw, h: bh, neckW: bw * 0.34, neckH: h * 0.1 };
  }

  function spawnBubble(ly) {
    if (bubbles >= MAXB) return;
    const k = bubbles++;
    bx[k] = ly.x + 10 + Math.random() * (ly.w - 20);
    by[k] = ly.y + ly.h - 14 - Math.random() * 10;
    bv[k] = 40 + Math.random() * 60;
    br[k] = 2 + Math.random() * 3.5;
  }

  let elapsed = 0;
  sim.setUpdate((ctx, dt, w, h) => {
    dt = Math.min(dt, 0.05);
    elapsed += dt;
    const ly = layout(w, h);
    const gasMax = 20 / SODA_MOLAR * GAS_L_PER_MOL;
    const gasNow = gasLiters * progress;

    if (reacting && progress < 1) {
      progress = Math.min(1, progress + dt / 4);
      emitTimer += dt;
      const interval = 0.03 + 0.1 * (1 - gasLiters / gasMax);
      while (emitTimer > interval) {
        emitTimer -= interval;
        spawnBubble(ly);
      }
      if (progress >= 1) {
        badge.set(limiting === 'perfect' ? 'Perfect match — both ran out together!' : `The ${limiting === 'soda' ? 'baking soda' : 'vinegar'} ran out — fizz over!`);
        badge.el.style.setProperty('--ix-hud-color', '#fbbf24');
      }
    }

    ctx.clearRect(0, 0, w, h);

    const liqH = ly.h * (0.2 + 0.5 * (vinegarMl / 200));
    const liqY = ly.y + ly.h - liqH;
    ctx.fillStyle = 'rgba(254,243,199,0.45)';
    ctx.fillRect(ly.x + 3, liqY, ly.w - 6, liqH - 3);

    if (reacting) {
      const foamH = Math.min(ly.h - liqH - 6, (ly.h * 0.55) * (gasNow / gasMax) * (balloonMode ? 0.35 : 1));
      if (foamH > 1) {
        ctx.fillStyle = 'rgba(248,250,252,0.85)';
        ctx.fillRect(ly.x + 3, liqY - foamH, ly.w - 6, foamH);
        ctx.fillStyle = 'rgba(255,255,255,0.9)';
        for (let i = 0; i < 8; i++) {
          const fx = ly.x + 8 + ((i * 53 + 17) % (ly.w - 16));
          ctx.beginPath();
          ctx.arc(fx, liqY - foamH + 2 + Math.sin(elapsed * 3 + i) * 2, 4, 0, Math.PI * 2);
          ctx.fill();
        }
      }
      const pileLeft = 1 - progress;
      if (pileLeft > 0.02) {
        ctx.fillStyle = `rgba(248,250,252,${0.9 * pileLeft})`;
        ctx.beginPath();
        ctx.moveTo(ly.x + ly.w * 0.25, ly.y + ly.h - 3);
        ctx.quadraticCurveTo(ly.x + ly.w * 0.5, ly.y + ly.h - 3 - 20 * pileLeft * (sodaG / 20), ly.x + ly.w * 0.75, ly.y + ly.h - 3);
        ctx.fill();
      }
    }

    ctx.fillStyle = 'rgba(125,211,252,0.85)';
    for (let i = bubbles - 1; i >= 0; i--) {
      by[i] -= bv[i] * dt;
      bx[i] += Math.sin(elapsed * 5 + i) * 12 * dt;
      if (by[i] < liqY - (balloonMode ? 0 : ly.h * 0.2)) {
        bubbles--;
        bx[i] = bx[bubbles]; by[i] = by[bubbles]; bv[i] = bv[bubbles]; br[i] = br[bubbles];
        continue;
      }
      ctx.beginPath();
      ctx.arc(bx[i], by[i], br[i], 0, Math.PI * 2);
      ctx.fill();
    }

    const nx = ly.x + ly.w / 2;
    ctx.strokeStyle = 'rgba(199,212,234,0.9)';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(nx - ly.neckW / 2, ly.y - ly.neckH);
    ctx.lineTo(nx - ly.neckW / 2, ly.y);
    ctx.lineTo(ly.x, ly.y + 14);
    ctx.lineTo(ly.x, ly.y + ly.h);
    ctx.lineTo(ly.x + ly.w, ly.y + ly.h);
    ctx.lineTo(ly.x + ly.w, ly.y + 14);
    ctx.lineTo(nx + ly.neckW / 2, ly.y);
    ctx.lineTo(nx + ly.neckW / 2, ly.y - ly.neckH);
    ctx.stroke();

    if (balloonMode) {
      const rMax = Math.min(w, h) * 0.13;
      const r = 8 + rMax * Math.cbrt(gasNow / gasMax);
      const byc = ly.y - ly.neckH - r + 4;
      ctx.fillStyle = 'rgba(236,72,153,0.75)';
      ctx.beginPath();
      ctx.ellipse(nx, byc, r * 0.85, r, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,0.9)';
      ctx.font = '600 10px Poppins, sans-serif';
      ctx.textAlign = 'center';
      if (gasNow > 0.05) ctx.fillText(`${gasNow.toFixed(1)} L CO₂`, nx, byc + 4);
    }

    ctx.fillStyle = 'rgba(199,212,234,0.7)';
    ctx.font = '600 11px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('baking soda + vinegar → fizzy CO₂', ly.x + ly.w / 2, ly.y + ly.h + 22);

    gasOut.set(`${gasNow.toFixed(1)} L`);
    limOut.set(!reacting ? '—' : progress < 1 ? 'reacting…' : limiting === 'perfect' ? 'both at once!' : limiting === 'soda' ? 'baking soda' : 'vinegar');
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
