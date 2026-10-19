/**
 * tubes2d — a rack of test tubes for the spot-test labs. Each tube eases its contents towards a
 * target colour (so a reagent visibly swirls into a new colour), can hold a dipped paper strip,
 * show a precipitate band or a layer, and be lowered into a water bath. Reagents are dragged
 * from the shelf (chem2d) and dropped onto a tube; tubeAt(x, y) finds which one.
 */
import { T, Spring, clamp, text, withAlpha, rgb, softShadow } from './kit2d.js';

export function createRack(k, n) {
  const tubes = [];
  for (let i = 0; i < n; i++) tubes.push({ x: 0, y: 0, r: 0, g: 0, b: 0, tr: 0, tg: 0, tb: 0, a: 0.6, ta: 0.6, level: 0.45, paper: null, paperC: null, ppt: 0, label: '', sub: '', glow: new Spring(0, 200, 16), heat: 0, bubbles: 0 });
  let w = 30, h = 120, rackY = 0, x0 = 0, gap = 50;
  function layout(left, top, width, height) {
    gap = width / n; w = Math.min(34, gap * 0.55); h = Math.min(200, height * 0.72); rackY = top + height; x0 = left;
    for (let i = 0; i < n; i++) { tubes[i].x = left + gap * (i + 0.5); tubes[i].y = rackY - 14; }
  }
  function setColor(i, hex, a = 0.65, instant) {
    const c = rgb(hex), t = tubes[i];
    t.tr = c[0]; t.tg = c[1]; t.tb = c[2]; t.ta = a;
    if (instant) { t.r = c[0]; t.g = c[1]; t.b = c[2]; t.a = a; }
    t.glow.v = 8;
  }
  function step(dt) {
    let moving = false;
    const f = 1 - Math.exp(-dt * 2.2);
    for (const t of tubes) {
      const dr = t.tr - t.r, dg = t.tg - t.g, db = t.tb - t.b, da = t.ta - t.a;
      if (Math.abs(dr) + Math.abs(dg) + Math.abs(db) + Math.abs(da) * 255 > 1) { t.r += dr * f; t.g += dg * f; t.b += db * f; t.a += da * f; moving = true; }
      if (t.glow.step(dt)) moving = true;
      if (t.heat > 0) moving = true;
    }
    return moving;
  }
  function tubeAt(x, y) {
    for (let i = 0; i < n; i++) { const t = tubes[i]; if (Math.abs(x - t.x) < gap / 2 && y > t.y - h - 70 && y < t.y + 30) return i; }
    return -1;
  }
  function draw(ctx, opt) {
    // rack
    ctx.fillStyle = T.wood; ctx.fillRect(x0 + 4, rackY - 40, gap * n - 8, 8);
    ctx.fillStyle = T.woodDark; ctx.fillRect(x0 + 4, rackY - 2, gap * n - 8, 8);
    ctx.fillRect(x0 + 6, rackY - 40, 6, 46); ctx.fillRect(x0 + gap * n - 12, rackY - 40, 6, 46);
    for (let i = 0; i < n; i++) {
      const t = tubes[i], top = t.y - h, liq = t.y - h * t.level;
      if (t.heat > 0) { ctx.fillStyle = withAlpha('#93c5fd', 0.35); ctx.fillRect(t.x - w * 0.8, t.y - h * 0.5, w * 1.6, h * 0.5 + 6); }
      softShadow(ctx, t.x, t.y + 4, w * 0.7, 3, 0.15);
      ctx.save();
      ctx.beginPath(); ctx.moveTo(t.x - w / 2, top); ctx.lineTo(t.x - w / 2, t.y - w / 2); ctx.arc(t.x, t.y - w / 2, w / 2, Math.PI, 0, true); ctx.lineTo(t.x + w / 2, top); ctx.closePath();
      ctx.fillStyle = 'rgba(225,236,250,0.5)'; ctx.fill();
      ctx.clip();
      ctx.fillStyle = `rgba(${t.r | 0},${t.g | 0},${t.b | 0},${t.a.toFixed(2)})`;
      ctx.fillRect(t.x - w, liq, w * 2, h);
      if (t.ppt > 0.02) { ctx.fillStyle = withAlpha(t.pptC || '#f8fafc', 0.9 * t.ppt); ctx.fillRect(t.x - w, t.y - w * 0.9, w * 2, w); }
      ctx.fillStyle = 'rgba(255,255,255,0.35)'; ctx.fillRect(t.x - w / 2 + 3, top + 4, 3, h - 14);
      if (t.heat > 0 && t.bubbles) { ctx.fillStyle = 'rgba(255,255,255,0.8)'; for (let b = 0; b < 4; b++) { const by = t.y - ((k.t * 40 + b * 23) % (h * t.level)); ctx.beginPath(); ctx.arc(t.x - 6 + b * 4, by, 1.6, 0, Math.PI * 2); ctx.fill(); } }
      ctx.restore();
      ctx.strokeStyle = t.glow.x > 0.05 ? withAlpha(T.blue, 0.4 + t.glow.x * 0.05) : 'rgba(110,140,180,0.85)'; ctx.lineWidth = 1.6;
      ctx.beginPath(); ctx.moveTo(t.x - w / 2 - 2, top); ctx.lineTo(t.x - w / 2, top + 3); ctx.lineTo(t.x - w / 2, t.y - w / 2); ctx.arc(t.x, t.y - w / 2, w / 2, Math.PI, 0, true); ctx.lineTo(t.x + w / 2, top + 3); ctx.lineTo(t.x + w / 2 + 2, top); ctx.stroke();
      ctx.strokeStyle = withAlpha('#ffffff', 0.7); ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(t.x - w / 2 + 2, liq); ctx.lineTo(t.x + w / 2 - 2, liq); ctx.stroke();
      if (t.paper) {
        const px = t.x + w * 0.1, pTop = top - 34, pBot = liq + 18;
        ctx.fillStyle = t.paper; ctx.fillRect(px - 4, pTop, 8, pBot - pTop);
        ctx.fillStyle = t.paperC || t.paper; ctx.fillRect(px - 4, liq - 10, 8, pBot - liq + 10);
        ctx.strokeStyle = 'rgba(0,0,0,0.12)'; ctx.strokeRect(px - 4, pTop, 8, pBot - pTop);
      }
      if (!opt || opt.labels !== false) {
        text(ctx, t.label, t.x, t.y + 22, T.ink, gap < 40 ? 7 : k.small ? 8.5 : 10, 700, 'center');
        if (t.sub && gap >= 40) text(ctx, t.sub, t.x, t.y + (k.small ? 33 : 36), T.ink2, k.small ? 8 : 9.5, 600, 'center');
      }
    }
  }
  return { tubes, layout, setColor, step, draw, tubeAt, get h() { return h; }, get w() { return w; }, get gap() { return gap; } };
}

export function mixHex(a, b, t) {
  const A = rgb(a), B = rgb(b), tt = clamp(t, 0, 1);
  return '#' + ((1 << 24) | (Math.round(A[0] + (B[0] - A[0]) * tt) << 16) | (Math.round(A[1] + (B[1] - A[1]) * tt) << 8) | Math.round(A[2] + (B[2] - A[2]) * tt)).toString(16).slice(1);
}
