// Shared helpers for biology lab sims. Mirrors the nebphysics/lab-utils + nebchemistry/chem-utils pattern.

export function fmt(v, d = 2) {
  return Number(v).toFixed(d);
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

export function labelText(ctx, text, x, y, opts = {}) {
  ctx.fillStyle = opts.color || 'rgba(232,238,251,0.9)';
  ctx.font = `${opts.weight || 700} ${opts.size || 12}px Poppins, sans-serif`;
  ctx.textAlign = opts.align || 'left';
  ctx.fillText(text, x, y);
}

export function drawTable(ctx, { x, y, w, title, cols, rows, accent = '#84CC16' }) {
  const rowH = 16;
  const headH = title ? 20 : 6;
  const h = headH + rowH * (rows.length + 1) + 8;
  panelBg(ctx, x, y, w, h);
  ctx.textAlign = 'left';
  if (title) {
    ctx.fillStyle = accent;
    ctx.font = '700 11px Poppins, sans-serif';
    ctx.fillText(title, x + 8, y + 14);
  }
  const cw = (w - 14) / cols.length;
  ctx.font = '600 9px Poppins, sans-serif';
  ctx.fillStyle = 'rgba(199,212,234,0.75)';
  cols.forEach((c, i) => ctx.fillText(c, x + 8 + i * cw, y + headH + 12));
  ctx.font = '500 10px Poppins, sans-serif';
  ctx.fillStyle = 'rgba(232,238,251,0.92)';
  rows.forEach((row, ri) => {
    row.forEach((cell, ci) => ctx.fillText(String(cell), x + 8 + ci * cw, y + headH + 12 + rowH * (ri + 1)));
  });
  return h;
}

// Draw a microscope eyepiece vignette over the field of view.
export function microscopeVignette(ctx, cx, cy, r) {
  const g = ctx.createRadialGradient(cx, cy, r * 0.6, cx, cy, r);
  g.addColorStop(0, 'rgba(0,0,0,0)');
  g.addColorStop(0.85, 'rgba(0,0,0,0.55)');
  g.addColorStop(1, 'rgba(0,0,0,0.95)');
  ctx.fillStyle = g;
  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, Math.PI * 2);
  ctx.fill();
}
