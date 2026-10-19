/**
 * Height and distance (NEB class 10) — an observer with a clinometer on a tripod looks at the top
 * of a tower. Drag the observer along the ground, drag the tower top up or down, or snap the angle
 * to 30°, 45° or 60°; the right-angled triangle is drawn and labelled and the working
 * tan θ = perpendicular ⁄ base is written out for whichever quantity is unknown. A second figure
 * shows the angle of depression from the top, equal to the angle of elevation (alternate angles).
 */
import { createKit, T, Spring, fmt, clamp, background, text, pill, knob, withAlpha, card, dashed, dimension, DOTS } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const DEG = Math.PI / 180;
const EXACT = { 30: '1/√3', 45: '1', 60: '√3' };

export default function init(stage) {
  const k = createKit(stage, { label: 'An observer with a clinometer looking up at a tower, with the right triangle drawn' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag the observer or the top of the tower', T.blue);

  let d = 40, H = 41.6, hi = 1.6, unknown = 'height', view = 'elevation';
  const dS = new Spring(d, 140, 20), HS = new Spring(H, 140, 20);

  const panel = createPanel(stage, { title: 'Height and distance' });
  panel.chips({ label: 'Figure', options: [{ value: 'elevation', label: 'Angle of elevation' }, { value: 'depression', label: 'Angle of depression' }], value: 'elevation', onChange: (v) => { view = v; k.animate(true); } });
  panel.chips({ label: 'What is unknown?', options: [{ value: 'height', label: 'Height' }, { value: 'distance', label: 'Distance' }, { value: 'angle', label: 'Angle' }], value: 'height', onChange: (v) => { unknown = v; k.invalidate(); } });
  panel.chips({ label: 'Snap the angle', options: [{ value: '30', label: '30°' }, { value: '45', label: '45°' }, { value: '60', label: '60°' }], value: '', onChange: (v) => { const t = Math.tan(+v * DEG); if (unknown === 'distance') d = clamp((H - hi) / t, 5, 150); else H = clamp(hi + d * t, 5, 120); go(); } });
  const hiS = panel.slider({ label: 'Height of the instrument', min: 0, max: 2, step: 0.1, value: hi, format: (v) => `${v.toFixed(1)} m`, onChange: (v) => { hi = v; go(); } });
  const st = panel.stats([{ key: 'th', label: 'Angle θ' }, { key: 'd', label: 'Distance (base)' }, { key: 'p', label: 'Perpendicular' }, { key: 'H', label: 'Height of tower' }]);
  const work = panel.readout({ label: 'Working', value: '' });
  panel.info('tan θ = perpendicular ⁄ base. The perpendicular is measured from the instrument\'s eye level, so add the instrument height back to get the full height. Standard values: tan 30° = 1/√3, tan 45° = 1, tan 60° = √3.');
  function go() { dS.to(d); HS.to(H); k.animate(true); }

  let gy = 0, ox = 0, sc = 4, W = 0;
  k.onResize((w, h) => { W = w; gy = h - (k.small ? 46 : 64); sc = Math.min((w - 80) / 140, (gy - 50) / 105); ox = w - (k.small ? 50 : 120); });
  const TX = () => ox;
  const OX = () => ox - dS.x * sc;
  const Y = (m) => gy - m * sc;

  const obsH = k.drag({
    hit: (x, y, s) => (Math.abs(x - OX()) < 18 + s && y > Math.min(Y(hi), gy - 40) - 30 - s && y < gy + 8 ? Math.abs(x - OX()) : false),
    move: (x) => { const nd = clamp(Math.round((ox - x) / sc), 5, 140); if (unknown === 'angle' || unknown === 'height' || unknown === 'distance') d = nd; dS.set(d); k.invalidate(); },
    cursor: 'ew-resize',
  });
  const topH = k.drag({
    hit: (x, y, s) => { const dd = Math.hypot(x - TX(), y - Y(HS.x)); return dd < 14 + s ? dd : false; },
    move: (x, y) => { H = clamp(Math.round((gy - y) / sc * 2) / 2, hi + 1, 100); HS.set(H); k.invalidate(); },
    cursor: 'ns-resize',
  });

  k.frame((ctx, dt, w, h) => {
    const anim = dS.step(dt) | HS.step(dt);
    const dd = dS.x, HH = HS.x, p = HH - hi, th = Math.atan2(p, dd);
    background(k, ctx, w, h, '#e9f3ff', '#f7fbff');
    // hills and ground
    ctx.fillStyle = '#dbe9d4'; ctx.beginPath(); ctx.moveTo(0, gy); for (let x = 0; x <= w; x += 30) ctx.lineTo(x, gy - 30 - 18 * Math.sin(x * 0.008) - 10 * Math.sin(x * 0.021)); ctx.lineTo(w, gy); ctx.fill();
    ctx.fillStyle = '#a3c98a'; ctx.fillRect(0, gy, w, h - gy); ctx.fillStyle = '#8bb873'; ctx.fillRect(0, gy, w, 3);
    // tower (a pagoda-style tower drawn to scale)
    const tx = TX(), tw = Math.max(16, 7 * sc), topY = Y(HH);
    ctx.fillStyle = '#e7dccb'; ctx.fillRect(tx - tw / 2, topY, tw, gy - topY);
    ctx.fillStyle = '#c9b89c'; for (let yy = topY + 14; yy < gy; yy += Math.max(12, 5 * sc)) ctx.fillRect(tx - tw / 2, yy, tw, 2);
    ctx.fillStyle = '#9a3412'; ctx.beginPath(); ctx.moveTo(tx - tw / 2 - 6, topY + 4); ctx.lineTo(tx, topY - 10); ctx.lineTo(tx + tw / 2 + 6, topY + 4); ctx.fill();
    ctx.fillStyle = '#d4a017'; ctx.fillRect(tx - 1.5, topY - 20, 3, 10);
    knob(ctx, tx, topY - 2, 7, T.orange, k.isHot(topH) ? 1 : 0);
    // observer
    const oxp = OX(), eyeY = Y(hi);
    ctx.strokeStyle = '#475569'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(oxp, eyeY); ctx.lineTo(oxp - 8, gy); ctx.moveTo(oxp, eyeY); ctx.lineTo(oxp + 8, gy); ctx.moveTo(oxp, eyeY); ctx.lineTo(oxp, gy); ctx.stroke();
    ctx.fillStyle = '#334155'; ctx.beginPath(); ctx.roundRect(oxp - 6, eyeY - 5, 12, 8, 2); ctx.fill();
    ctx.fillStyle = '#0f766e'; ctx.beginPath(); ctx.arc(oxp - 16, eyeY - 14, 6, 0, Math.PI * 2); ctx.fill(); ctx.fillRect(oxp - 20, eyeY - 8, 8, gy - eyeY + 8 - 18); ctx.fillRect(oxp - 20, gy - 18, 3, 18); ctx.fillRect(oxp - 15, gy - 18, 3, 18);
    if (k.isHot(obsH) || k.active === obsH) { ctx.strokeStyle = withAlpha(T.blue, 0.5); ctx.lineWidth = 2; ctx.strokeRect(oxp - 26, gy - 70, 40, 74); }
    // triangle
    ctx.fillStyle = withAlpha(T.blue, 0.06); ctx.beginPath(); ctx.moveTo(oxp, eyeY); ctx.lineTo(tx, eyeY); ctx.lineTo(tx, topY); ctx.closePath(); ctx.fill();
    dashed(ctx, oxp, eyeY, tx, eyeY, T.ink2, 1.4);
    ctx.strokeStyle = T.red; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(oxp, eyeY); ctx.lineTo(tx, topY); ctx.stroke();
    ctx.strokeStyle = T.ink2; ctx.lineWidth = 1; ctx.strokeRect(tx - 10, eyeY - 10, 10, 10);
    // angle arc
    if (view === 'elevation') {
      ctx.strokeStyle = T.blue; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(oxp, eyeY, 44, -th, 0); ctx.stroke();
      text(ctx, `θ = ${fmt(th / DEG, 1)}°`, oxp + 50, eyeY - 10, T.blue, 12, 700);
    } else {
      dashed(ctx, tx, topY, oxp, topY, T.ink2, 1.2, DOTS);
      ctx.strokeStyle = T.purple; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(tx, topY, 44, Math.PI, Math.PI + th, false); ctx.stroke();
      text(ctx, `depression ${fmt(th / DEG, 1)}°`, tx - 50, topY + 22, T.purple, 11.5, 700, 'right');
      ctx.strokeStyle = T.blue; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(oxp, eyeY, 44, -th, 0); ctx.stroke();
      text(ctx, `elevation ${fmt(th / DEG, 1)}°`, oxp + 50, eyeY - 10, T.blue, 11.5, 700);
      pill(ctx, 'equal: alternate angles between parallel lines', (oxp + tx) / 2, topY - 18, { size: 10, color: T.ink2 });
    }
    // dimensions
    dimension(ctx, oxp, gy + 16, tx, gy + 16, `d = ${fmt(dd, 1)} m`, unknown === 'distance' ? T.red : T.ink2);
    dimension(ctx, tx + tw / 2 + 18, eyeY, tx + tw / 2 + 18, topY, `p = ${fmt(p, 1)} m`, T.ink2);
    if (hi > 0.05) text(ctx, `${fmt(hi, 1)} m`, oxp + 12, (eyeY + gy) / 2 + 4, T.ink2, 9.5, 600);
    pill(ctx, unknown === 'height' ? `H = ? = ${fmt(HH, 1)} m` : `H = ${fmt(HH, 1)} m`, tx - tw / 2 - 50, (topY + gy) / 2, { color: unknown === 'height' ? T.red : T.ink, size: 11 });
    // working card
    const t = Math.tan(th), ang = Math.round(th / DEG * 10) / 10, exact = EXACT[Math.round(ang)] && Math.abs(ang - Math.round(ang)) < 0.05 ? EXACT[Math.round(ang)] : null;
    const lines = unknown === 'height' ? [`tan θ = p ⁄ d`, `p = d × tan ${fmt(ang, 1)}° = ${fmt(dd, 1)} × ${exact || fmt(t, 3)}`, `p = ${fmt(p, 2)} m`, `H = p + ${fmt(hi, 1)} = ${fmt(HH, 2)} m`]
      : unknown === 'distance' ? [`tan θ = p ⁄ d`, `d = p ⁄ tan ${fmt(ang, 1)}° = ${fmt(p, 1)} ⁄ ${exact || fmt(t, 3)}`, `d = ${fmt(dd, 2)} m`, '']
        : [`tan θ = p ⁄ d = ${fmt(p, 1)} ⁄ ${fmt(dd, 1)}`, `tan θ = ${fmt(t, 3)}`, `θ = tan⁻¹ ${fmt(t, 3)} = ${fmt(ang, 1)}°`, ''];
    if (!k.small) { card(ctx, 14, 50, 300, 106, 12); lines.forEach((l, i) => text(ctx, l, 28, 74 + i * 20, i === 2 ? T.red : T.ink, 12, i === 2 ? 700 : 600)); }
    st.th.set(`${fmt(ang, 1)}°`); st.d.set(`${fmt(dd, 1)} m`); st.p.set(`${fmt(p, 1)} m`); st.H.set(`${fmt(HH, 1)} m`);
    work.set(lines.filter(Boolean).join(' · '));
    badge.set(k.active === obsH ? 'Walk closer and the angle grows' : k.active === topH ? 'A taller tower makes a steeper sight line' : 'Drag the observer or the top of the tower');
    k.animate(!!anim);
  });

  k.debug = { obs: () => [OX(), gy - 20], top: () => [TX(), Y(HS.x)], vals: () => [d, H] };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
