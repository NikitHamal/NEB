import { makeCanvas, rng } from './kit.js';

// Calotropis leaf: broad obovate blade, short cordate base, acute tip. Half-width as a fraction of length.
export function leafHalfWidth(u) {
  const s = Math.sin(Math.PI * Math.pow(Math.min(1, Math.max(0, u)), 1.15));
  return 0.29 * (0.1 + 0.9 * Math.pow(Math.max(0, s), 0.7)) * (1 - Math.pow(u, 8));
}
const LEAF_TX = 0.6;

function noiseFill(g, w, h, rand, n, colors, rMin, rMax, alpha) {
  for (let i = 0; i < n; i++) {
    g.globalAlpha = alpha * (0.4 + rand() * 0.6);
    g.fillStyle = colors[(rand() * colors.length) | 0];
    const r = rMin + rand() * (rMax - rMin);
    g.beginPath(); g.arc(rand() * w, rand() * h, r, 0, Math.PI * 2); g.fill();
  }
  g.globalAlpha = 1;
}

function leafPath(g, S) {
  g.beginPath();
  for (let i = 0; i <= 80; i++) { const u = i / 80; g.lineTo(S * (0.5 + leafHalfWidth(u) / LEAF_TX), S * (1 - u)); }
  for (let i = 80; i >= 0; i--) { const u = i / 80; g.lineTo(S * (0.5 - leafHalfWidth(u) / LEAF_TX), S * (1 - u)); }
  g.closePath();
}

function leafVeins(g, S, colMid, colSec, colTer, under, rand) {
  const px = (x, u) => [S * (0.5 + x / LEAF_TX), S * (1 - u)];
  g.lineCap = 'round'; g.lineJoin = 'round';
  const sec = [];
  for (let side = -1; side <= 1; side += 2) {
    for (let k = 0; k < 11; k++) {
      const u0 = 0.04 + k * 0.083 + (rand() - 0.5) * 0.02;
      if (u0 > 0.9) continue;
      const pts = [];
      for (let i = 0; i <= 16; i++) {
        const t = i / 16;
        const u = u0 + 0.1 * t + 0.07 * t * t;
        const reach = leafHalfWidth(Math.min(1, u)) * (0.9 - 0.05 * t);
        const x = side * reach * t;
        pts.push(px(x, Math.min(0.99, u)));
      }
      sec.push({ pts, w: (1 - k * 0.06) });
    }
  }
  for (let k = 0; k < 2200 * (S / 1024); k++) {
    const u = 0.02 + rand() * 0.95; const v = rand() * 1.9 - 0.95; const hw = leafHalfWidth(u);
    const [x, y] = px(v * hw, u);
    g.strokeStyle = colTer; g.globalAlpha = 0.12 + rand() * 0.18; g.lineWidth = S / 1024 * (0.6 + rand() * 0.8);
    g.beginPath(); g.moveTo(x, y);
    let cx = x; let cy = y;
    for (let j = 0; j < 3; j++) { const a = rand() * Math.PI * 2; const l = S * (0.004 + rand() * 0.008); cx += Math.cos(a) * l; cy += Math.sin(a) * l; g.lineTo(cx, cy); }
    g.stroke();
  }
  g.globalAlpha = 1;
  sec.forEach(({ pts, w }) => {
    for (let i = 0; i < pts.length - 1; i++) {
      const t = i / (pts.length - 1);
      g.strokeStyle = colSec; g.globalAlpha = 0.95 - t * 0.6;
      g.lineWidth = S * (under ? 0.008 : 0.0062) * w * (1 - t * 0.75) + 0.6;
      g.beginPath(); g.moveTo(pts[i][0], pts[i][1]); g.lineTo(pts[i + 1][0], pts[i + 1][1]); g.stroke();
    }
  });
  g.globalAlpha = 1;
  g.strokeStyle = colMid;
  for (let i = 0; i < 40; i++) {
    const u = i / 40; const [x, y] = px(0, u); const [x2, y2] = px(0, Math.min(0.985, u + 1 / 40 + 0.001));
    g.lineWidth = S * (under ? 0.024 : 0.017) * (1 - u * 0.85) + 1;
    g.beginPath(); g.moveTo(x, y); g.lineTo(x2, y2); g.stroke();
  }
}

export function leafTextures(size, seed = 3) {
  const rand = rng(seed);
  const make = (under) => {
    const c = makeCanvas(size); const g = c.getContext('2d');
    g.fillStyle = under ? '#9fb592' : '#557d4b'; g.fillRect(0, 0, size, size);
    leafPath(g, size); g.save(); g.clip();
    const grad = g.createLinearGradient(0, size, 0, 0);
    if (under) { grad.addColorStop(0, '#b2c4a4'); grad.addColorStop(1, '#a0b694'); } else { grad.addColorStop(0, '#5a8c45'); grad.addColorStop(0.5, '#4d803c'); grad.addColorStop(1, '#426f36'); }
    g.fillStyle = grad; g.fillRect(0, 0, size, size);
    noiseFill(g, size, size, rand, 900 * size / 1024, under ? ['#bccbb0', '#9db08f', '#b0c2a2'] : ['#5f9048', '#457638', '#6c9a50', '#548740'], size * 0.004, size * 0.03, 0.22);
    noiseFill(g, size, size, rand, 1400 * size / 1024, under ? ['#d6e0cf'] : ['#8fae84', '#a3bd96'], size * 0.0015, size * 0.004, 0.25);
    leafVeins(g, size, under ? '#dfe8d3' : '#d2dfba', under ? '#d2ddc5' : '#a9c58f', under ? '#c8d5bd' : '#7a9c68', under, rand);
    g.restore();
    leafPath(g, size); g.strokeStyle = under ? '#9fb196' : '#4a6e40'; g.lineWidth = size * 0.006; g.stroke();
    return c;
  };
  const bump = makeCanvas(size); const b = bump.getContext('2d');
  b.fillStyle = '#9a9a9a'; b.fillRect(0, 0, size, size);
  noiseFill(b, size, size, rand, 1200 * size / 1024, ['#a8a8a8', '#8c8c8c'], size * 0.003, size * 0.012, 0.35);
  leafVeins(b, size, '#5a5a5a', '#6e6e6e', '#868686', false, rand);
  return { front: make(false), back: make(true), bump };
}

export function detailCanvas(size = 256, seed = 4) {
  const rand = rng(seed);
  const c = makeCanvas(size); const g = c.getContext('2d');
  g.fillStyle = '#808080'; g.fillRect(0, 0, size, size);
  for (let i = 0; i < size * 6; i++) {
    const v = 90 + rand() * 90 | 0;
    g.fillStyle = `rgba(${v},${v},${v},0.5)`;
    const x = rand() * size; const y = rand() * size; const r = 0.5 + rand() * 2.5;
    for (const dx of [-size, 0, size]) for (const dy of [-size, 0, size]) { g.beginPath(); g.arc(x + dx, y + dy, r, 0, Math.PI * 2); g.fill(); }
  }
  for (let i = 0; i < size * 0.8; i++) {
    g.strokeStyle = 'rgba(70,70,70,0.35)'; g.lineWidth = 0.7;
    const x = rand() * size; const y = rand() * size; const a = rand() * 6.28; const l = 4 + rand() * 10;
    g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke();
  }
  return c;
}

export function leafAlphaMask(size) {
  const c = makeCanvas(size); const g = c.getContext('2d');
  g.fillStyle = '#fff'; g.fillRect(0, 0, size, size);
  return c;
}
export function leafUvToCanvas(x, u, size) { return [size * (0.5 + x / LEAF_TX), size * (1 - u)]; }
export const LEAF_TEX_SPAN = LEAF_TX;

export function barkTexture(size, seed = 5) {
  const rand = rng(seed);
  const c = makeCanvas(size / 2, size); const g = c.getContext('2d');
  const w = size / 2; const h = size;
  const grad = g.createLinearGradient(0, 0, w, 0);
  grad.addColorStop(0, '#8f9a80'); grad.addColorStop(0.5, '#a3ab92'); grad.addColorStop(1, '#8f9a80');
  g.fillStyle = grad; g.fillRect(0, 0, w, h);
  noiseFill(g, w, h, rand, 700, ['#b8bea8', '#7f8a70', '#9aa386', '#c9cbbb'], 1, 5, 0.35);
  g.lineCap = 'round';
  for (let i = 0; i < 70; i++) {
    let x = rand() * w; let y = rand() * h;
    g.strokeStyle = rand() < 0.5 ? 'rgba(70,72,55,0.55)' : 'rgba(220,222,210,0.35)';
    g.lineWidth = 0.6 + rand() * 1.6;
    g.beginPath(); g.moveTo(x, y);
    const len = 20 + rand() * 90;
    for (let s = 0; s < 6; s++) { x += (rand() - 0.5) * 6; y += len / 6; g.lineTo(x, y); }
    g.stroke();
  }
  for (let i = 0; i < 26; i++) {
    g.fillStyle = 'rgba(90,85,65,0.5)';
    const x = rand() * w; const y = rand() * h;
    g.beginPath(); g.ellipse(x, y, 1.5 + rand() * 2, 0.8 + rand(), 0, 0, Math.PI * 2); g.fill();
  }
  return c;
}

// Plain tiger (Danaus chrysippus) wings. Wing space: x out from the body, y forward along it.
export const FORE = {
  box: [0, 1.08, -0.5, 0.36],
  outline: [[0.0, 0.05], [0.18, 0.13], [0.42, 0.22], [0.66, 0.29], [0.86, 0.31], [0.98, 0.26], [1.04, 0.16], [1.0, 0.02], [0.92, -0.14], [0.82, -0.28], [0.72, -0.39], [0.62, -0.44], [0.46, -0.38], [0.28, -0.26], [0.12, -0.14], [0.02, -0.05]],
};
export const HIND = {
  box: [0, 0.86, -0.82, 0.06],
  outline: [[0.0, 0.0], [0.2, 0.02], [0.42, 0.0], [0.6, -0.06], [0.74, -0.16], [0.81, -0.3], [0.8, -0.45], [0.73, -0.6], [0.61, -0.71], [0.45, -0.78], [0.3, -0.77], [0.18, -0.68], [0.1, -0.52], [0.05, -0.34], [0.01, -0.15]],
};

function wingCtx(spec, W) {
  const [x0, x1, y0, y1] = spec.box;
  const H = Math.round(W * (y1 - y0) / (x1 - x0));
  const c = makeCanvas(W, H); const g = c.getContext('2d');
  const P = (x, y) => [((x - x0) / (x1 - x0)) * W, ((y1 - y) / (y1 - y0)) * H];
  const k = W / (x1 - x0);
  return { c, g, P, k, W, H };
}

function smoothPath(g, P, pts) {
  const q = pts.map(([x, y]) => P(x, y));
  g.beginPath();
  const n = q.length;
  const mid = (a, b) => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
  let m = mid(q[n - 1], q[0]); g.moveTo(m[0], m[1]);
  for (let i = 0; i < n; i++) { const nx = q[(i + 1) % n]; m = mid(q[i], nx); g.quadraticCurveTo(q[i][0], q[i][1], m[0], m[1]); }
  g.closePath();
}

function scales(g, W, H, rand, dark, light, n) {
  for (let i = 0; i < n; i++) {
    g.globalAlpha = 0.05 + rand() * 0.08;
    g.fillStyle = rand() < 0.5 ? dark : light;
    const x = rand() * W; const y = rand() * H;
    g.fillRect(x, y, 1 + rand() * 2.2, 0.7 + rand() * 1.2);
  }
  g.globalAlpha = 1;
}

function veins(g, P, k, list, color, width) {
  g.strokeStyle = color; g.lineCap = 'round'; g.lineJoin = 'round';
  list.forEach((pts) => {
    g.lineWidth = width * k;
    g.beginPath();
    pts.forEach(([x, y], i) => { const [a, b] = P(x, y); if (i) g.lineTo(a, b); else g.moveTo(a, b); });
    g.stroke();
  });
}

const FORE_VEINS = [
  [[0.02, 0.04], [0.3, 0.15], [0.6, 0.25], [0.84, 0.3]],
  [[0.02, 0.0], [0.25, 0.06], [0.46, 0.1]],
  [[0.02, -0.06], [0.22, -0.08], [0.46, -0.06]],
  [[0.46, 0.1], [0.46, -0.06]],
  [[0.46, 0.1], [0.66, 0.2], [0.9, 0.27]], [[0.46, 0.1], [0.7, 0.16], [0.98, 0.2]],
  [[0.46, 0.08], [0.74, 0.1], [1.02, 0.1]], [[0.46, 0.04], [0.74, 0.0], [1.0, -0.02]],
  [[0.46, -0.02], [0.72, -0.12], [0.92, -0.16]], [[0.4, -0.07], [0.62, -0.2], [0.82, -0.3]],
  [[0.3, -0.08], [0.52, -0.25], [0.7, -0.4]], [[0.05, -0.08], [0.3, -0.22], [0.56, -0.42]],
];
const HIND_VEINS = [
  [[0.02, -0.01], [0.3, -0.02], [0.6, -0.08]],
  [[0.03, -0.04], [0.2, -0.1], [0.34, -0.2]], [[0.03, -0.08], [0.16, -0.24], [0.3, -0.3]],
  [[0.34, -0.2], [0.3, -0.3]],
  [[0.34, -0.2], [0.58, -0.22], [0.78, -0.26]], [[0.34, -0.22], [0.6, -0.36], [0.8, -0.42]],
  [[0.33, -0.26], [0.56, -0.48], [0.72, -0.6]], [[0.31, -0.29], [0.48, -0.56], [0.6, -0.7]],
  [[0.3, -0.3], [0.38, -0.56], [0.44, -0.77]], [[0.05, -0.12], [0.2, -0.5], [0.28, -0.76]],
  [[0.03, -0.18], [0.1, -0.45], [0.16, -0.66]],
];

function marginBand(g, P, k, spec, width, color) {
  g.save(); smoothPath(g, P, spec.outline); g.clip();
  g.beginPath(); spec.wedge.forEach(([x, y], i) => { const [a, b] = P(x, y); if (i) g.lineTo(a, b); else g.moveTo(a, b); }); g.closePath(); g.clip();
  smoothPath(g, P, spec.outline);
  g.strokeStyle = color; g.lineWidth = width * k * 2; g.lineJoin = 'round'; g.stroke();
  g.restore();
}

function marginDots(g, P, k, spec, inset, r, color, rows = 1) {
  g.fillStyle = color;
  const pts = spec.outer;
  const cx = spec.center[0]; const cy = spec.center[1];
  for (let row = 0; row < rows; row++) {
    for (let i = 0; i < pts.length - 1; i++) {
      const [ax, ay] = pts[i]; const [bx, by] = pts[i + 1];
      for (let s = 0; s < 2; s++) {
        const t = (s + 0.5) / 2;
        const mx = ax + (bx - ax) * t; const my = ay + (by - ay) * t;
        const dx = cx - mx; const dy = cy - my; const l = Math.hypot(dx, dy) || 1;
        const d = inset + row * inset * 1.3;
        const [px, py] = P(mx + (dx / l) * d, my + (dy / l) * d);
        const rr = r * k * (1 - row * 0.3);
        g.beginPath(); g.ellipse(px, py, rr, rr * 0.75, Math.atan2(-dy, dx) + Math.PI / 2, 0, Math.PI * 2); g.fill();
      }
    }
  }
}

FORE.wedge = [[0.5, -0.7], [0.8, 0.45], [1.3, 0.45], [1.3, -0.7]];
FORE.center = [0.55, -0.02];
HIND.wedge = [[0.3, 0.06], [1.2, -0.4], [1.2, -1.2], [0.42, -1.0]];
HIND.center = [0.38, -0.36];
FORE.outer = [[0.86, 0.31], [0.98, 0.26], [1.04, 0.16], [1.0, 0.02], [0.92, -0.14], [0.82, -0.28], [0.72, -0.39], [0.62, -0.44]];
HIND.outer = [[0.6, -0.06], [0.74, -0.16], [0.81, -0.3], [0.8, -0.45], [0.73, -0.6], [0.61, -0.71], [0.45, -0.78], [0.3, -0.77], [0.18, -0.68]];

export function wingCanvases(W, seed = 11) {
  const out = {};
  ['fore', 'hind'].forEach((which) => {
    const spec = which === 'fore' ? FORE : HIND;
    ['upper', 'under'].forEach((side) => {
      const rand = rng(seed + (which === 'fore' ? 0 : 7) + (side === 'upper' ? 0 : 3));
      const { c, g, P, k, H } = wingCtx(spec, W);
      g.save(); smoothPath(g, P, spec.outline); g.clip();
      const under = side === 'under';
      const [bx, by] = P(0, 0);
      const rg = g.createRadialGradient(bx, by, 0, bx, by, W * 1.05);
      if (under) { rg.addColorStop(0, '#c9874a'); rg.addColorStop(0.35, '#e6a65a'); rg.addColorStop(1, '#efbb70'); } else { rg.addColorStop(0, '#6e3416'); rg.addColorStop(0.18, '#b85a1f'); rg.addColorStop(0.5, '#d9772a'); rg.addColorStop(1, '#e38b34'); }
      g.fillStyle = rg; g.fillRect(0, 0, W, H);
      scales(g, W, H, rand, '#5a2a10', '#ffd9a0', W * 40);
      if (which === 'fore') {
        g.fillStyle = under ? '#7a4a28' : '#1b1310';
        g.beginPath();
        const ap = [[0.5, 0.36], [1.1, 0.36], [1.1, -0.2], [0.94, -0.16], [0.82, -0.08], [0.72, 0.02], [0.62, 0.14], [0.54, 0.24]];
        ap.forEach(([x, y], i) => { const [a, b] = P(x, y); if (i) g.lineTo(a, b); else g.moveTo(a, b); });
        g.closePath(); g.fill();
        if (under) {
          g.fillStyle = 'rgba(214,150,80,0.55)';
          g.beginPath(); [[0.78, 0.3], [1.1, 0.3], [1.1, -0.1], [0.9, 0.0]].forEach(([x, y], i) => { const [a, b] = P(x, y); if (i) g.lineTo(a, b); else g.moveTo(a, b); }); g.closePath(); g.fill();
        }
        g.strokeStyle = under ? '#3a2416' : '#1b1310'; g.lineWidth = 0.025 * k;
        g.beginPath(); [[0.0, 0.05], [0.42, 0.22], [0.86, 0.31]].forEach(([x, y], i) => { const [a, b] = P(x, y); if (i) g.lineTo(a, b); else g.moveTo(a, b); }); g.stroke();
        g.fillStyle = '#fbf8f0';
        [[0.6, 0.23, 0.05, 0.03, -0.5], [0.67, 0.18, 0.055, 0.032, -0.5], [0.73, 0.12, 0.05, 0.03, -0.6], [0.79, 0.06, 0.042, 0.026, -0.7], [0.85, 0.0, 0.03, 0.02, -0.8], [0.7, 0.25, 0.022, 0.016, -0.4], [0.88, 0.2, 0.018, 0.014, 0], [0.93, 0.13, 0.016, 0.012, 0]].forEach(([x, y, rx, ry, rot]) => {
          const [a, b] = P(x, y); g.beginPath(); g.ellipse(a, b, rx * k, ry * k, rot, 0, Math.PI * 2); g.fill();
        });
      } else {
        g.fillStyle = under ? '#1d1512' : '#1b1310';
        [[0.36, -0.17, 0.028], [0.3, -0.27, 0.026], [0.4, -0.3, 0.022]].forEach(([x, y, r]) => {
          const [a, b] = P(x, y);
          if (under) { g.fillStyle = '#f6efe2'; g.beginPath(); g.arc(a, b, (r + 0.012) * k, 0, Math.PI * 2); g.fill(); g.fillStyle = '#1d1512'; }
          g.beginPath(); g.arc(a, b, r * k, 0, Math.PI * 2); g.fill();
        });
        if (under) {
          g.fillStyle = 'rgba(250,240,225,0.5)';
          [[0.16, -0.1, 0.018], [0.22, -0.06, 0.014]].forEach(([x, y, r]) => { const [a, b] = P(x, y); g.beginPath(); g.arc(a, b, r * k, 0, Math.PI * 2); g.fill(); });
        }
      }
      marginBand(g, P, k, spec, which === 'fore' ? 0.07 : 0.085, '#1b1310');
      veins(g, P, k, which === 'fore' ? FORE_VEINS : HIND_VEINS, under ? 'rgba(80,45,22,0.75)' : 'rgba(40,20,10,0.72)', 0.0055);
      marginDots(g, P, k, spec, 0.03, which === 'fore' ? 0.011 : 0.013, '#f4efe4', which === 'fore' ? 1 : 2);
      g.restore();
      g.save(); smoothPath(g, P, spec.outline); g.lineWidth = 0.006 * k; g.setLineDash([0.006 * k, 0.012 * k]); g.strokeStyle = 'rgba(235,228,215,0.55)'; g.stroke(); g.restore();
      out[`${which}_${side}`] = c;
    });
  });
  return out;
}

export function caterpillarCanvas(W = 512, H = 128) {
  const c = makeCanvas(W, H); const g = c.getContext('2d');
  g.fillStyle = '#ece9de'; g.fillRect(0, 0, W, H);
  const segs = 13;
  for (let s = 0; s < segs; s++) {
    const x0 = (s / segs) * W; const sw = W / segs;
    g.fillStyle = '#121212';
    g.fillRect(x0 + sw * 0.1, 0, sw * 0.5, H);
    g.fillRect(x0 + sw * 0.66, 0, sw * 0.22, H);
    g.fillStyle = '#f4f1e8';
    g.fillRect(x0 + sw * 0.3, 0, sw * 0.045, H);
    g.fillRect(x0 + sw * 0.43, 0, sw * 0.03, H);
    g.fillStyle = '#f2c21a';
    [0.32, 0.68].forEach((v) => { g.beginPath(); g.ellipse(x0 + sw * 0.62, v * H, sw * 0.12, H * 0.07, 0, 0, Math.PI * 2); g.fill(); });
    g.fillStyle = '#e8b414';
    [0.1, 0.9].forEach((v) => { g.fillRect(x0 + sw * 0.56, v * H - H * 0.03, sw * 0.2, H * 0.06); });
    g.fillStyle = '#111';
    [0.18, 0.82].forEach((v) => { g.beginPath(); g.arc(x0 + sw * 0.6, v * H, H * 0.015, 0, Math.PI * 2); g.fill(); });
  }
  g.fillStyle = 'rgba(40,40,40,0.35)'; g.fillRect(0, H * 0.94, W, H * 0.06); g.fillRect(0, 0, W, H * 0.06);
  return c;
}

export function chrysalisCanvases(W = 512) {
  const H = W;
  const make = (mature) => {
    const c = makeCanvas(W, H); const g = c.getContext('2d');
    const grad = g.createLinearGradient(0, H, 0, 0);
    if (mature) { grad.addColorStop(0, '#2b2a1c'); grad.addColorStop(0.5, '#3b3220'); grad.addColorStop(1, '#3a3a26'); } else { grad.addColorStop(0, '#8fd19a'); grad.addColorStop(0.5, '#6fc184'); grad.addColorStop(1, '#5fb377'); }
    g.fillStyle = grad; g.fillRect(0, 0, W, H);
    if (mature) {
      [0.25, 0.75].forEach((u) => {
        const x = u * W;
        g.fillStyle = '#b25a1c'; g.beginPath(); g.ellipse(x, H * 0.48, W * 0.13, H * 0.2, 0, 0, Math.PI * 2); g.fill();
        g.fillStyle = '#16100c'; g.beginPath(); g.ellipse(x + W * 0.03, H * 0.34, W * 0.1, H * 0.08, 0.3, 0, Math.PI * 2); g.fill();
        g.fillStyle = '#efe7da'; [[0.02, 0.33], [0.06, 0.36], [0.0, 0.38]].forEach(([dx, v]) => { g.beginPath(); g.arc(x + dx * W, v * H, W * 0.01, 0, Math.PI * 2); g.fill(); });
      });
    } else {
      g.strokeStyle = 'rgba(40,110,60,0.25)'; g.lineWidth = W * 0.004;
      [0.25, 0.75].forEach((u) => { g.beginPath(); g.ellipse(u * W, H * 0.5, W * 0.12, H * 0.2, 0, 0, Math.PI * 2); g.stroke(); });
    }
    g.fillStyle = '#121008'; g.fillRect(0, H * 0.27, W, H * 0.022);
    g.fillStyle = '#e7b93a';
    for (let i = 0; i < 16; i++) { g.beginPath(); g.arc((i + 0.5) / 16 * W, H * 0.285, H * 0.011, 0, Math.PI * 2); g.fill(); }
    g.fillRect(0, H * 0.255, W, H * 0.012);
    [[0.12, 0.84], [0.38, 0.84], [0.62, 0.84], [0.88, 0.84], [0.2, 0.62], [0.8, 0.62], [0.5, 0.92], [0.0, 0.92], [0.5, 0.7]].forEach(([u, v]) => {
      g.beginPath(); g.arc(u * W, v * H, H * 0.012, 0, Math.PI * 2); g.fill();
    });
    return c;
  };
  const metal = makeCanvas(W, H); const m = metal.getContext('2d');
  m.fillStyle = '#000'; m.fillRect(0, 0, W, H);
  m.fillStyle = '#fff'; m.fillRect(0, H * 0.255, W, H * 0.012);
  for (let i = 0; i < 16; i++) { m.beginPath(); m.arc((i + 0.5) / 16 * W, H * 0.285, H * 0.013, 0, Math.PI * 2); m.fill(); }
  [[0.12, 0.84], [0.38, 0.84], [0.62, 0.84], [0.88, 0.84], [0.2, 0.62], [0.8, 0.62], [0.5, 0.92], [0.0, 0.92], [0.5, 0.7]].forEach(([u, v]) => {
    m.beginPath(); m.arc(u * W, v * H, H * 0.014, 0, Math.PI * 2); m.fill();
  });
  return { young: make(false), mature: make(true), metal };
}

export function groundCanvas(size, seed = 9) {
  const rand = rng(seed);
  const c = makeCanvas(size); const g = c.getContext('2d');
  g.fillStyle = '#8b7a5c'; g.fillRect(0, 0, size, size);
  noiseFill(g, size, size, rand, 600, ['#9a8866', '#7a6a4e', '#a69474', '#6e6046'], size * 0.01, size * 0.05, 0.35);
  noiseFill(g, size, size, rand, 2500, ['#b3a283', '#5e5240', '#c8b996'], 0.6, 2.2, 0.6);
  noiseFill(g, size, size, rand, 140, ['#6f7a45', '#7d8650', '#5f6a3a'], size * 0.01, size * 0.04, 0.3);
  for (let i = 0; i < 900; i++) {
    const x = rand() * size; const y = rand() * size;
    g.strokeStyle = rand() < 0.6 ? `rgba(${110 + rand() * 40 | 0},${130 + rand() * 40 | 0},${60 + rand() * 30 | 0},0.7)` : 'rgba(170,150,95,0.7)';
    g.lineWidth = 0.8 + rand();
    g.beginPath(); g.moveTo(x, y); g.lineTo(x + (rand() - 0.5) * 14, y - 6 - rand() * 14); g.stroke();
  }
  return c;
}

export function bokehCanvas(W, H, seed = 21, opts = {}) {
  const rand = rng(seed);
  const c = makeCanvas(W, H); const g = c.getContext('2d');
  const top = opts.top ?? 0.35;
  const blob = (x, y, r, col, a) => {
    const rg = g.createRadialGradient(x, y, 0, x, y, r);
    rg.addColorStop(0, col.replace('A', a)); rg.addColorStop(0.6, col.replace('A', a * 0.7)); rg.addColorStop(1, col.replace('A', 0));
    g.fillStyle = rg; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
  };
  const greens = opts.greens || ['rgba(62,92,48,A)', 'rgba(84,112,58,A)', 'rgba(48,74,40,A)', 'rgba(104,128,70,A)'];
  for (let i = 0; i < 160; i++) {
    const x = rand() * W;
    const crown = top + Math.sin(x / W * Math.PI * (3 + seed % 3)) * 0.08 + rand() * 0.1;
    const y = H * (crown + rand() * (1 - crown));
    blob(x, y, H * (0.08 + rand() * 0.2), greens[(rand() * greens.length) | 0], 0.55 + rand() * 0.35);
  }
  for (let i = 0; i < (opts.highlights ?? 40); i++) {
    const x = rand() * W; const y = H * (top + 0.05 + rand() * 0.6);
    blob(x, y, H * (0.015 + rand() * 0.035), 'rgba(235,240,190,A)', 0.25 + rand() * 0.3);
  }
  const fade = g.createLinearGradient(0, H * 0.75, 0, H);
  fade.addColorStop(0, 'rgba(0,0,0,0)'); fade.addColorStop(1, 'rgba(0,0,0,1)');
  g.globalCompositeOperation = 'destination-out';
  if (opts.fadeBottom) { g.fillStyle = fade; g.fillRect(0, 0, W, H); }
  if (opts.fadeSides) {
    const sf = g.createLinearGradient(0, 0, W, 0);
    sf.addColorStop(0, 'rgba(0,0,0,1)'); sf.addColorStop(0.22, 'rgba(0,0,0,0)'); sf.addColorStop(0.78, 'rgba(0,0,0,0)'); sf.addColorStop(1, 'rgba(0,0,0,1)');
    g.fillStyle = sf; g.fillRect(0, 0, W, H);
  }
  g.globalCompositeOperation = 'source-over';
  return c;
}
