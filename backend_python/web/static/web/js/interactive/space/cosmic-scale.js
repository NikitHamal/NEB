/**
 * Scale of the universe — one continuous zoom across 27 powers of ten, from a person to the
 * observable universe. Every object is drawn at its true size relative to the view (all nested
 * about the centre), so each one shrinks to a dot as the next appears. Drag up or down (or scroll,
 * or use the slider) to zoom; the scale bar converts the view into metres, kilometres, AU and
 * light-years.
 */
import { createKit, T, Spring, fmt, clamp, text, withAlpha, sphere } from '../core/kit2d.js';
import { starfield, glow, npill } from '../core/space2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const LY = 9.4607e15, AU = 1.496e11;
const OBJ = [
  { name: 'You', size: 1.7, type: 'person', color: '#e8eefb', label: '1.7 m tall' },
  { name: 'Mt. Everest (Sagarmatha)', size: 8849, type: 'mountain', color: '#cdd9ec', label: '8 849 m high' },
  { name: 'Nepal', size: 8.85e5, type: 'country', color: '#60a5fa', label: '885 km long' },
  { name: 'Earth', size: 1.2742e7, type: 'planet', color: '#4d9fff', label: '12 742 km across' },
  { name: 'The Moon\'s orbit', size: 7.69e8, type: 'orbit', color: '#9aa7bd', label: '384 400 km from Earth' },
  { name: 'The Sun', size: 1.3927e9, type: 'star', color: '#ffd27a', label: '1.39 million km across' },
  { name: 'Earth\'s orbit', size: 2 * AU, type: 'orbit', color: '#7dd3fc', label: '1 AU = 150 million km from the Sun' },
  { name: 'The Solar System', size: 60 * AU, type: 'orbit', color: '#a5b4fc', label: 'Neptune\'s orbit, 30 AU from the Sun' },
  { name: 'The Oort cloud', size: 3.2 * LY, type: 'cloud', color: '#94a3b8', label: 'icy comets out to ~1.6 light-years' },
  { name: 'Nearest stars', size: 2 * 4.24 * LY, type: 'neighbours', color: '#f9a8d4', label: 'Proxima Centauri, 4.24 light-years away' },
  { name: 'The Milky Way', size: 1.0e5 * LY, type: 'galaxy', color: '#c4b5fd', label: '100 000 light-years across' },
  { name: 'The Local Group', size: 1.0e7 * LY, type: 'group', color: '#94a8d0', label: '~10 million light-years, with Andromeda' },
  { name: 'Laniakea Supercluster', size: 5.2e8 * LY, type: 'web', color: '#7c8db0', label: '520 million light-years' },
  { name: 'Observable Universe', size: 9.3e10 * LY, type: 'universe', color: '#f0a65a', label: '93 billion light-years across' },
];

function human(m) {
  if (m < 1e3) return `${fmt(m, m < 10 ? 1 : 0)} m`;
  if (m < 1e9) return `${fmt(m / 1e3, m < 1e4 ? 1 : 0)} km`;
  if (m < 0.05 * LY) return `${fmt(m / AU, m < 10 * AU ? 2 : 0)} AU`;
  const ly = m / LY;
  return ly < 1e3 ? `${fmt(ly, ly < 10 ? 2 : 0)} light-years` : ly < 1e6 ? `${fmt(ly / 1e3, 0)} thousand ly` : ly < 1e9 ? `${fmt(ly / 1e6, 0)} million ly` : `${fmt(ly / 1e9, 0)} billion ly`;
}
const SUP = '⁰¹²³⁴⁵⁶⁷⁸⁹';
const pow10 = (n) => '10' + String(n).split('').map((d) => (d === '-' ? '⁻' : SUP[+d])).join('');

export default function init(stage) {
  const k = createKit(stage, { night: true, captureTouch: true, label: 'A zoom through the powers of ten from a person to the observable universe' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag up to zoom out, down to zoom in', '#60a5fa');

  const z = new Spring(0.7, 40, 12);
  let target = 0.7, touring = false;
  const panel = createPanel(stage, { title: 'Powers of ten' });
  const zS = panel.slider({ label: 'View width', min: 0, max: 27.2, step: 0.01, value: target, format: (v) => `${pow10(Math.floor(v))} m · ${human(Math.pow(10, v))}`, onChange: (v) => { target = v; touring = false; k.animate(true); } });
  panel.chips({ label: 'Jump to', options: OBJ.filter((o, i) => i % 2 === 1 || i === 13).map((o) => ({ value: o.name, label: o.name.replace('The ', '').split(' (')[0] })), value: '', onChange: (v) => { const o = OBJ.find((q) => q.name === v); target = Math.log10(o.size * 1.6); zS.set(target); touring = false; k.animate(true); } });
  const [tourB] = panel.buttonRow([{ label: 'Tour', icon: 'rocket_launch', onClick: () => { touring = !touring; if (touring && target > 27) target = 0.2; k.animate(true); } }]);
  const st = panel.stats([{ key: 'w', label: 'View width' }, { key: 'p', label: 'Power of ten' }, { key: 'obj', label: 'In view' }, { key: 'light', label: 'Light takes' }]);
  panel.info('Each step to the right in the power of ten is ten times bigger. From the Sun to the nearest star is about 270 000 AU; between galaxies is mostly empty space.');

  let dragY0 = 0, z0 = 0;
  k.drag({ hit: () => 1, down: (x, y) => { dragY0 = y; z0 = target; touring = false; }, move: (x, y) => { target = clamp(z0 + (dragY0 - y) / 90, 0, 27.2); zS.set(target); k.animate(true); }, cursor: 'ns-resize', cursorActive: 'ns-resize' });
  function onWheel(e) { e.preventDefault(); target = clamp(target + e.deltaY * 0.004, 0, 27.2); zS.set(target); touring = false; k.animate(true); }
  k.canvas.addEventListener('wheel', onWheel, { passive: false });

  const galaxy = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 256;
    const g = c.getContext('2d');
    let s = 7; const r = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    for (let i = 0; i < 2600; i++) {
      const arm = i % 2, t = r() * 4.2, rad = 10 + t * 26 + (r() - 0.5) * 14, a = t * 1.25 + arm * Math.PI + (r() - 0.5) * 0.45;
      g.fillStyle = r() < 0.2 ? 'rgba(255,200,160,0.8)' : 'rgba(190,200,255,0.7)';
      g.fillRect(128 + Math.cos(a) * rad, 128 + Math.sin(a) * rad * 0.9, 1.4, 1.4);
    }
    const core = g.createRadialGradient(128, 128, 0, 128, 128, 40); core.addColorStop(0, 'rgba(255,230,190,0.95)'); core.addColorStop(1, 'rgba(255,230,190,0)');
    g.fillStyle = core; g.fillRect(0, 0, 256, 256);
    return c;
  })();
  const web = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 256;
    const g = c.getContext('2d');
    let s = 3; const r = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    const nodes = []; for (let i = 0; i < 40; i++) nodes.push([r() * 256, r() * 256]);
    g.strokeStyle = 'rgba(150,170,230,0.25)'; g.lineWidth = 1.2;
    for (const a of nodes) for (const b of nodes) if (a !== b && Math.hypot(a[0] - b[0], a[1] - b[1]) < 55) { g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.stroke(); }
    for (let i = 0; i < 1400; i++) { const n = nodes[(r() * nodes.length) | 0]; g.fillStyle = 'rgba(200,210,255,0.6)'; g.fillRect(n[0] + (r() - 0.5) * 30, n[1] + (r() - 0.5) * 30, 1.2, 1.2); }
    return c;
  })();

  k.frame((ctx, dt, w, h) => {
    if (touring) { target = Math.min(27.2, target + dt * 1.1); zS.set(target); if (target >= 27.2) { touring = false; tourB.setLabel('Tour'); } }
    z.to(target); z.step(dt);
    const view = Math.pow(10, z.x), W = Math.min(w, h) * 0.9, cx = w / 2, cy = h / 2;
    starfield(k, ctx, w, h, { seed: 9 });
    let inView = '';
    for (let i = OBJ.length - 1; i >= 0; i--) {
      const o = OBJ[i], s = o.size / view * W;
      if (s < 0.6 || s > W * 40) continue;
      const fade = clamp(Math.min((s - 0.6) / 6, (W * 40 - s) / (W * 30)), 0, 1);
      ctx.globalAlpha = fade;
      draw(ctx, o, cx, cy, s);
      ctx.globalAlpha = 1;
      if (s > W * 0.12 && s < W * 1.6 && !inView) inView = o.name;
      if (s > 26 && s < W * 1.25) npill(ctx, `${o.name} · ${o.label}`, cx, Math.max(30, cy - Math.min(s, W) / 2 - 16) + (i % 2 ? 0 : 0), withAlpha(o.color === '#e8eefb' ? '#e8eefb' : o.color, 1), k.small ? 9.5 : 11);
    }
    // scale bar
    const pw = Math.floor(z.x - 0.7), bar = Math.pow(10, pw) / view * W;
    const bx = 20, by = h - 26;
    ctx.strokeStyle = '#e8eefb'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(bx, by - 6); ctx.lineTo(bx, by); ctx.lineTo(bx + bar, by); ctx.lineTo(bx + bar, by - 6); ctx.stroke();
    text(ctx, `${pow10(pw)} m = ${human(Math.pow(10, pw))}`, bx + bar + 8, by + 3, '#e8eefb', 11, 700);
    text(ctx, pow10(Math.round(z.x)) + ' m', w - 20, 40, 'rgba(232,238,251,0.85)', k.small ? 22 : 34, 800, 'right');
    st.w.set(human(view)); st.p.set(`${pow10(Math.round(z.x))} m`); st.obj.set(inView || '—');
    const lt = view / 2.998e8;
    st.light.set(lt < 1e-3 ? `${fmt(lt * 1e9, 0)} ns to cross` : lt < 1 ? `${fmt(lt * 1000, 2)} ms to cross` : lt < 3600 ? `${fmt(lt, 1)} s to cross` : lt < 86400 * 365 ? `${fmt(lt / 3600, 1)} hours to cross` : `${human(view).replace('light-years', 'years').replace('ly', 'years')} to cross`);
    badge.set(inView ? `${inView}` : 'Drag up to zoom out, down to zoom in');
    k.animate(touring || z.moving);
  });

  function draw(ctx, o, cx, cy, s) {
    const r = s / 2;
    switch (o.type) {
      case 'person': {
        const hgt = s; ctx.strokeStyle = o.color; ctx.lineWidth = Math.max(1, hgt * 0.06); ctx.lineCap = 'round';
        ctx.beginPath(); ctx.arc(cx, cy - hgt * 0.4, hgt * 0.08, 0, Math.PI * 2); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx, cy - hgt * 0.32); ctx.lineTo(cx, cy + hgt * 0.1); ctx.lineTo(cx - hgt * 0.12, cy + hgt * 0.5); ctx.moveTo(cx, cy + hgt * 0.1); ctx.lineTo(cx + hgt * 0.12, cy + hgt * 0.5); ctx.moveTo(cx - hgt * 0.18, cy - hgt * 0.15); ctx.lineTo(cx + hgt * 0.18, cy - hgt * 0.15); ctx.stroke();
        break;
      }
      case 'mountain':
        ctx.fillStyle = '#64748b'; ctx.beginPath(); ctx.moveTo(cx - s * 1.4, cy + r); ctx.lineTo(cx - s * 0.2, cy - r); ctx.lineTo(cx + s * 0.1, cy - r * 0.7); ctx.lineTo(cx + s * 1.3, cy + r); ctx.fill();
        ctx.fillStyle = '#f1f5f9'; ctx.beginPath(); ctx.moveTo(cx - s * 0.2, cy - r); ctx.lineTo(cx - s * 0.42, cy - r * 0.55); ctx.lineTo(cx - s * 0.05, cy - r * 0.6); ctx.lineTo(cx + s * 0.1, cy - r * 0.7); ctx.closePath(); ctx.fill();
        break;
      case 'country':
        ctx.fillStyle = withAlpha('#3b82f6', 0.35); ctx.strokeStyle = '#93c5fd'; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(cx - r, cy - r * 0.05); ctx.lineTo(cx - r * 0.6, cy - r * 0.28); ctx.lineTo(cx, cy - r * 0.2); ctx.lineTo(cx + r * 0.6, cy - r * 0.08); ctx.lineTo(cx + r, cy + r * 0.05); ctx.lineTo(cx + r * 0.8, cy + r * 0.22); ctx.lineTo(cx, cy + r * 0.16); ctx.lineTo(cx - r * 0.7, cy + r * 0.18); ctx.closePath(); ctx.fill(); ctx.stroke();
        break;
      case 'planet': glow(ctx, cx, cy, r * 1.25, '#60a5fa', 0.4); sphere(ctx, cx, cy, r, o.color); break;
      case 'star': glow(ctx, cx, cy, r * 2.4, '#ffd27a', 0.9); sphere(ctx, cx, cy, r, '#ffcf5c'); break;
      case 'orbit': ctx.strokeStyle = withAlpha(o.color, 0.7); ctx.lineWidth = 1.4; ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke(); break;
      case 'cloud': ctx.strokeStyle = withAlpha(o.color, 0.35); ctx.lineWidth = Math.max(2, r * 0.25); ctx.beginPath(); ctx.arc(cx, cy, r * 0.85, 0, Math.PI * 2); ctx.stroke(); break;
      case 'neighbours':
        ctx.strokeStyle = withAlpha(o.color, 0.6); ctx.setLineDash([4, 5]); ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke(); ctx.setLineDash([]);
        glow(ctx, cx + r * 0.71, cy - r * 0.71, 10, '#f9a8d4', 0.9); glow(ctx, cx + r * 0.68, cy - r * 0.74, 7, '#fde68a', 0.9);
        break;
      case 'galaxy': ctx.drawImage(galaxy, cx - r * 1.1, cy - r * 1.1, r * 2.2, r * 2.2); break;
      case 'group':
        ctx.drawImage(galaxy, cx - r * 0.02 - r * 0.01, cy - r * 0.02, r * 0.04, r * 0.04);
        ctx.drawImage(galaxy, cx + r * 0.25 - r * 0.026, cy - r * 0.1 - r * 0.026, r * 0.052, r * 0.052);
        ctx.strokeStyle = withAlpha(o.color, 0.5); ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke();
        break;
      case 'web': ctx.drawImage(web, cx - r, cy - r, r * 2, r * 2); break;
      case 'universe': {
        ctx.strokeStyle = withAlpha('#f0a65a', 0.6); ctx.lineWidth = Math.max(2, r * 0.03); ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke();
        ctx.globalAlpha *= 0.6; ctx.drawImage(web, cx - r, cy - r, r * 2, r * 2); ctx.globalAlpha = 1;
        break;
      }
      default: break;
    }
  }

  k.debug = { zoom: (v) => { target = v; zS.set(v); k.animate(true); }, z: () => z.x };
  return { dispose() { k.canvas.removeEventListener('wheel', onWheel); k.dispose(); panel.dispose(); hud.dispose(); } };
}
