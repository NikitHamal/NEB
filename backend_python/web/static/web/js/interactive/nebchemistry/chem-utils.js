export const GLASS = 'rgba(199,212,234,0.85)';
export const GLASS_DIM = 'rgba(199,212,234,0.45)';
export const LABEL = 'rgba(199,212,234,0.75)';
export const FONT = '600 10px Poppins, sans-serif';
export const FONT_SM = '600 9px Poppins, sans-serif';

export function drawBeaker(ctx, x, y, w, h, fillFrac, color, label) {
  if (fillFrac > 0) {
    const lh = h * Math.min(1, fillFrac);
    ctx.fillStyle = color;
    ctx.fillRect(x + 2, y + h - lh, w - 4, lh - 2);
  }
  ctx.strokeStyle = GLASS;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(x - 5, y - 6);
  ctx.lineTo(x, y);
  ctx.lineTo(x, y + h);
  ctx.lineTo(x + w, y + h);
  ctx.lineTo(x + w, y);
  ctx.lineTo(x + w + 5, y - 6);
  ctx.stroke();
  if (label) {
    ctx.fillStyle = LABEL;
    ctx.font = FONT_SM;
    ctx.textAlign = 'center';
    ctx.fillText(label, x + w / 2, y + h + 13);
  }
}

export function drawFlask(ctx, cx, baseY, w, h, fillFrac, color, label) {
  const neckW = w * 0.26;
  const topY = baseY - h;
  if (fillFrac > 0) {
    const f = Math.min(1, fillFrac);
    const lh = h * 0.62 * f;
    ctx.save();
    flaskPath(ctx, cx, baseY, w, h, neckW);
    ctx.clip();
    ctx.fillStyle = color;
    ctx.fillRect(cx - w / 2, baseY - lh, w, lh);
    ctx.restore();
  }
  ctx.strokeStyle = GLASS;
  ctx.lineWidth = 2;
  flaskPath(ctx, cx, baseY, w, h, neckW);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(cx - neckW / 2 - 3, topY - 4);
  ctx.lineTo(cx + neckW / 2 + 3, topY - 4);
  ctx.stroke();
  if (label) {
    ctx.fillStyle = LABEL;
    ctx.font = FONT_SM;
    ctx.textAlign = 'center';
    ctx.fillText(label, cx, baseY + 14);
  }
}

function flaskPath(ctx, cx, baseY, w, h, neckW) {
  const topY = baseY - h;
  ctx.beginPath();
  ctx.moveTo(cx - neckW / 2, topY);
  ctx.lineTo(cx - neckW / 2, topY + h * 0.32);
  ctx.lineTo(cx - w / 2, baseY - 6);
  ctx.quadraticCurveTo(cx - w / 2, baseY, cx - w / 2 + 8, baseY);
  ctx.lineTo(cx + w / 2 - 8, baseY);
  ctx.quadraticCurveTo(cx + w / 2, baseY, cx + w / 2, baseY - 6);
  ctx.lineTo(cx + neckW / 2, topY + h * 0.32);
  ctx.lineTo(cx + neckW / 2, topY);
}

export function drawTestTube(ctx, cx, topY, w, h, fillFrac, color, label) {
  if (fillFrac > 0) {
    const lh = (h - w / 2) * Math.min(1, fillFrac) + w / 2;
    ctx.save();
    tubePath(ctx, cx, topY, w, h);
    ctx.clip();
    ctx.fillStyle = color;
    ctx.fillRect(cx - w / 2, topY + h - lh, w, lh);
    ctx.restore();
  }
  ctx.strokeStyle = GLASS;
  ctx.lineWidth = 2;
  tubePath(ctx, cx, topY, w, h);
  ctx.stroke();
  if (label) {
    ctx.fillStyle = LABEL;
    ctx.font = FONT_SM;
    ctx.textAlign = 'center';
    ctx.fillText(label, cx, topY + h + 14);
  }
}

function tubePath(ctx, cx, topY, w, h) {
  ctx.beginPath();
  ctx.moveTo(cx - w / 2, topY);
  ctx.lineTo(cx - w / 2, topY + h - w / 2);
  ctx.arc(cx, topY + h - w / 2, w / 2, Math.PI, 0, true);
  ctx.lineTo(cx + w / 2, topY);
}

export function drawBurette(ctx, x, topY, botY, fillFrac, color, maxMl) {
  const w = 13;
  const h = botY - topY;
  if (fillFrac > 0) {
    ctx.fillStyle = color;
    ctx.fillRect(x - w / 2 + 2, topY + h * (1 - fillFrac), w - 4, h * fillFrac);
  }
  ctx.strokeStyle = GLASS;
  ctx.lineWidth = 2;
  ctx.strokeRect(x - w / 2, topY, w, h);
  ctx.beginPath();
  ctx.moveTo(x - w / 2, botY);
  ctx.lineTo(x, botY + 11);
  ctx.lineTo(x + w / 2, botY);
  ctx.stroke();
  ctx.strokeStyle = GLASS_DIM;
  ctx.lineWidth = 1;
  ctx.fillStyle = LABEL;
  ctx.font = FONT_SM;
  ctx.textAlign = 'left';
  for (let i = 0; i <= 10; i++) {
    const gy = topY + (i / 10) * h;
    ctx.beginPath();
    ctx.moveTo(x + w / 2, gy);
    ctx.lineTo(x + w / 2 + 4, gy);
    ctx.stroke();
    if (maxMl && i % 2 === 0) ctx.fillText(String((maxMl * i) / 10), x + w / 2 + 7, gy + 3);
  }
}

export function drawFlame(ctx, cx, baseY, size, t, color) {
  const wob = Math.sin(t * 9) * size * 0.08;
  const g = ctx.createRadialGradient(cx, baseY - size * 0.4, 2, cx, baseY - size * 0.4, size);
  const outer = color || '#60a5fa';
  g.addColorStop(0, 'rgba(255,255,255,0.9)');
  g.addColorStop(0.45, outer);
  g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g;
  ctx.beginPath();
  ctx.moveTo(cx - size * 0.32, baseY);
  ctx.quadraticCurveTo(cx - size * 0.4 + wob, baseY - size * 0.55, cx + wob, baseY - size);
  ctx.quadraticCurveTo(cx + size * 0.4 + wob, baseY - size * 0.55, cx + size * 0.32, baseY);
  ctx.fill();
}

export function drawBurner(ctx, cx, baseY, t, on, flameColor, flameSize) {
  ctx.fillStyle = '#475569';
  ctx.fillRect(cx - 16, baseY - 4, 32, 4);
  ctx.fillRect(cx - 3.5, baseY - 30, 7, 26);
  if (on) drawFlame(ctx, cx, baseY - 30, flameSize || 34, t, flameColor);
}

export function makeBubbles(max) {
  const list = [];
  return {
    list,
    spawn(x, y, opts = {}) {
      if (list.length >= (max || 40)) return;
      list.push({
        x: x + (Math.random() - 0.5) * (opts.spread || 10),
        y,
        r: opts.r || 1.5 + Math.random() * 2,
        v: opts.v || 26 + Math.random() * 24,
        top: opts.top !== undefined ? opts.top : 0,
        color: opts.color || 'rgba(255,255,255,0.55)',
      });
    },
    step(dt) {
      for (let i = list.length - 1; i >= 0; i--) {
        const b = list[i];
        b.y -= b.v * dt;
        b.x += Math.sin(b.y * 0.12) * 12 * dt;
        if (b.y <= b.top) list.splice(i, 1);
      }
    },
    draw(ctx) {
      list.forEach((b) => {
        ctx.strokeStyle = b.color;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
        ctx.stroke();
      });
    },
    clear() { list.length = 0; },
  };
}

export function drawStand(ctx, x, topY, botY) {
  ctx.strokeStyle = '#64748b';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(x, topY);
  ctx.lineTo(x, botY);
  ctx.stroke();
  ctx.fillStyle = '#64748b';
  ctx.fillRect(x - 26, botY, 52, 5);
}

export function drawClamp(ctx, standX, y, toX) {
  ctx.strokeStyle = '#64748b';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(standX, y);
  ctx.lineTo(toX, y);
  ctx.stroke();
}

export function text(ctx, str, x, y, opts = {}) {
  ctx.fillStyle = opts.color || LABEL;
  ctx.font = opts.font || FONT;
  ctx.textAlign = opts.align || 'center';
  ctx.fillText(str, x, y);
}

export function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}
