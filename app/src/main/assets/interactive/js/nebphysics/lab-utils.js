export function fmt(v, d = 2) {
  return Number(v).toFixed(d);
}

export function linFit(pts) {
  const n = pts.length;
  if (n < 2) return null;
  let sx = 0;
  let sy = 0;
  let sxx = 0;
  let sxy = 0;
  for (const p of pts) {
    sx += p.x;
    sy += p.y;
    sxx += p.x * p.x;
    sxy += p.x * p.y;
  }
  const den = n * sxx - sx * sx;
  if (Math.abs(den) < 1e-12) return null;
  const m = (n * sxy - sx * sy) / den;
  return { m, b: (sy - m * sx) / n };
}

export function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  if (ctx.roundRect) ctx.roundRect(x, y, w, h, r);
  else ctx.rect(x, y, w, h);
}

export function panelBg(ctx, x, y, w, h) {
  ctx.fillStyle = 'rgba(8,16,30,0.78)';
  ctx.strokeStyle = 'rgba(158,193,255,0.25)';
  ctx.lineWidth = 1;
  roundRect(ctx, x, y, w, h, 8);
  ctx.fill();
  ctx.stroke();
}

export function drawTable(ctx, { x, y, w, title, cols, rows, accent = '#F59E0B' }) {
  const rowH = 15;
  const headH = title ? 18 : 6;
  const h = headH + rowH * (rows.length + 1) + 8;
  panelBg(ctx, x, y, w, h);
  ctx.textAlign = 'left';
  if (title) {
    ctx.fillStyle = accent;
    ctx.font = '700 10px Poppins, sans-serif';
    ctx.fillText(title, x + 8, y + 13);
  }
  const cw = (w - 14) / cols.length;
  ctx.font = '600 8.5px Poppins, sans-serif';
  ctx.fillStyle = 'rgba(199,212,234,0.75)';
  cols.forEach((c, i) => ctx.fillText(c, x + 8 + i * cw, y + headH + 11));
  ctx.font = '500 9.5px Poppins, sans-serif';
  ctx.fillStyle = 'rgba(232,238,251,0.92)';
  rows.forEach((row, ri) => {
    row.forEach((cell, ci) => ctx.fillText(String(cell), x + 8 + ci * cw, y + headH + 11 + rowH * (ri + 1)));
  });
  return h;
}

export function drawGraph(ctx, { x, y, w, h, pts, xLabel, yLabel, fit, xMax, yMax, accent = '#F59E0B' }) {
  panelBg(ctx, x, y, w, h);
  const padL = 14;
  const padR = 10;
  const padT = 16;
  const padB = 20;
  const gx = x + padL;
  const gy = y + padT;
  const gw = w - padL - padR;
  const gh = h - padT - padB;
  const mx = xMax || Math.max(...pts.map((p) => p.x), 1e-6) * 1.2;
  const my = yMax || Math.max(...pts.map((p) => p.y), 1e-6) * 1.2;
  ctx.strokeStyle = 'rgba(199,212,234,0.4)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(gx, gy);
  ctx.lineTo(gx, gy + gh);
  ctx.lineTo(gx + gw, gy + gh);
  ctx.stroke();
  ctx.fillStyle = 'rgba(199,212,234,0.7)';
  ctx.font = '600 9px Poppins, sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText(yLabel, x + 6, y + 11);
  ctx.textAlign = 'right';
  ctx.fillText(xLabel, x + w - 8, gy + gh + 14);
  if (fit) {
    ctx.strokeStyle = 'rgba(139,233,168,0.85)';
    ctx.beginPath();
    ctx.moveTo(gx, gy + gh - Math.max(0, Math.min(1, fit.b / my)) * gh);
    const yEnd = fit.m * mx + fit.b;
    ctx.lineTo(gx + gw, gy + gh - Math.max(0, Math.min(1, yEnd / my)) * gh);
    ctx.stroke();
  }
  pts.forEach((p) => {
    const px = gx + (p.x / mx) * gw;
    const py = gy + gh - (p.y / my) * gh;
    ctx.fillStyle = accent;
    ctx.beginPath();
    ctx.arc(px, py, 3.4, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.6)';
    ctx.lineWidth = 1;
    ctx.stroke();
  });
}

export function drawNeedleMeter(ctx, { cx, cy, r, value, min = 0, max, label, accent = '#F59E0B', divisions = 10 }) {
  panelBg(ctx, cx - r - 6, cy - r * 0.9 - 6, r * 2 + 12, r * 1.1 + 30);
  const a0 = -Math.PI * 0.8;
  const a1 = -Math.PI * 0.2;
  ctx.strokeStyle = 'rgba(232,238,251,0.6)';
  ctx.lineWidth = 1.4;
  ctx.beginPath();
  ctx.arc(cx, cy, r * 0.8, a0, a1);
  ctx.stroke();
  ctx.font = '600 8px Poppins, sans-serif';
  for (let i = 0; i <= divisions; i++) {
    const a = a0 + ((a1 - a0) * i) / divisions;
    const big = i % (divisions / 2) === 0 || i % 5 === 0;
    ctx.strokeStyle = 'rgba(199,212,234,0.8)';
    ctx.beginPath();
    ctx.moveTo(cx + Math.cos(a) * r * 0.8, cy + Math.sin(a) * r * 0.8);
    ctx.lineTo(cx + Math.cos(a) * r * (big ? 0.68 : 0.74), cy + Math.sin(a) * r * (big ? 0.68 : 0.74));
    ctx.stroke();
    if (big) {
      const v = min + ((max - min) * i) / divisions;
      ctx.fillStyle = 'rgba(199,212,234,0.85)';
      ctx.textAlign = 'center';
      ctx.fillText(fmt(v, Math.abs(max - min) >= 10 ? 0 : 1), cx + Math.cos(a) * r * 0.55, cy + Math.sin(a) * r * 0.55 + 3);
    }
  }
  const t = Math.max(0, Math.min(1, (value - min) / (max - min)));
  const na = a0 + (a1 - a0) * t;
  ctx.strokeStyle = accent;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(cx + Math.cos(na) * r * 0.76, cy + Math.sin(na) * r * 0.76);
  ctx.stroke();
  ctx.fillStyle = accent;
  ctx.beginPath();
  ctx.arc(cx, cy, 3.5, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = 'rgba(232,238,251,0.92)';
  ctx.font = '700 10px Poppins, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(label, cx, cy + 16);
}

export function labelText(ctx, text, x, y, opts = {}) {
  ctx.fillStyle = opts.color || 'rgba(232,238,251,0.9)';
  ctx.font = `${opts.weight || 700} ${opts.size || 12}px Poppins, sans-serif`;
  ctx.textAlign = opts.align || 'left';
  ctx.fillText(text, x, y);
}
