/**
 * Life cycle of stars — choose a starting mass and scrub (or play) through the star's life. The
 * star is drawn with the colour of its surface temperature (blackbody) and a size on a log scale,
 * and its path is traced on a Hertzsprung–Russell diagram. Main-sequence numbers follow the
 * mass–luminosity relation L ≈ M^3.5, T ≈ 5772 K·M^0.5 and lifetime ≈ 10 billion years × M^−2.5;
 * the ending follows the mass: white dwarf below about 8 M☉, neutron star, or black hole above ~25 M☉.
 */
import { createKit, T, Spring, fmt, clamp, text, withAlpha, card, knob, sphere } from '../core/kit2d.js';
import { starfield, glow, starColor, npill } from '../core/space2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const L10 = Math.log10;

function lifeTxt(y) { return y >= 1e9 ? `${fmt(y / 1e9, y < 1e10 ? 1 : 0)} billion years` : y >= 1e6 ? `${fmt(y / 1e6, 0)} million years` : `${fmt(y, 0)} years`; }

function stages(M) {
  const Lms = M < 0.43 ? 0.23 * Math.pow(M, 2.3) : Math.pow(M, 3.5);
  const Tms = 5772 * Math.pow(M, 0.505), Rms = Math.pow(M, M < 1 ? 0.8 : 0.57);
  const tms = 1e10 * Math.pow(M, -2.5);
  const S = [
    { key: 'nebula', name: 'Nebula', T: 30, L: Lms * 1e-3, R: 2000, dur: 'millions of years', w: 0.08, info: 'A cold cloud of hydrogen and dust, light-years wide. Gravity pulls a clump of it together.' },
    { key: 'proto', name: 'Protostar', T: 3500, L: Lms * 6, R: Rms * 5, dur: lifeTxt(5e7 / Math.pow(M, 2.5)), w: 0.08, info: 'The collapsing clump heats as gravity squeezes it. At about 10 million °C in the core, hydrogen fusion ignites.' },
    { key: 'ms', name: 'Main sequence', T: Tms, L: Lms, R: Rms, dur: lifeTxt(tms), w: 0.46, info: `Hydrogen fuses into helium and the outward push of that energy balances gravity. At ${fmt(M, 1)} M☉ this lasts about ${lifeTxt(tms)}.` },
  ];
  if (M < 0.5) {
    S.push({ key: 'wd', name: 'White dwarf (in the far future)', T: 6000, L: 1e-3, R: 0.013, dur: 'longer than the age of the Universe', w: 0.38, info: `A red dwarf burns so slowly (about ${lifeTxt(tms)}) that none has yet died: the Universe is only 13.8 billion years old. It will fade to a white dwarf.` });
  } else if (M < 8) {
    S.push({ key: 'giant', name: 'Red giant', T: 3800, L: 1000 * Math.pow(M, 1.2), R: 100 * Math.pow(M, 0.6), dur: lifeTxt(tms * 0.1), w: 0.12, info: 'Core hydrogen runs out: the core shrinks and heats, the outer layers swell to a hundred times the size. The Sun will do this in about 5 billion years.' });
    S.push({ key: 'pneb', name: 'Planetary nebula', T: 100000, L: 3000, R: 0.05, dur: 'about 10 000 years', w: 0.08, info: 'The outer layers drift away as a glowing shell, leaving the hot bare core. (Nothing to do with planets.)' });
    S.push({ key: 'wd', name: 'White dwarf', T: 12000, L: 1e-3, R: 0.012, dur: 'cools for billions of years', w: 0.18, info: 'The leftover core: about the size of Earth but with half the Sun\'s mass. A teaspoon of it weighs about five tonnes.' });
  } else {
    S.push({ key: 'giant', name: 'Red supergiant', T: 3600, L: 1e5 * Math.min(3, M / 15), R: 800, dur: lifeTxt(tms * 0.1), w: 0.14, info: 'Hundreds of times wider than the Sun, fusing heavier and heavier elements in shells, until the core is iron, which fusion cannot burn.' });
    S.push({ key: 'sn', name: 'Supernova', T: 20000, L: 1e9, R: 2000, dur: 'weeks', w: 0.06, info: 'The iron core collapses in under a second and the star explodes, briefly outshining its whole galaxy. Gold, silver and uranium are forged in such explosions.' });
    S.push(M < 25
      ? { key: 'ns', name: 'Neutron star', T: 600000, L: 1e-1, R: 1.5e-5, dur: 'forever (it cools)', w: 0.18, info: 'A ball of neutrons about 20 km across, spinning many times a second. A teaspoon would weigh a billion tonnes.' }
      : { key: 'bh', name: 'Black hole', T: 0, L: 0, R: 4e-5, dur: 'forever', w: 0.18, info: 'The core collapses without limit. Its gravity is so strong that not even light escapes from inside the event horizon.' });
  }
  const tot = S.reduce((s, x) => s + x.w, 0); let acc = 0;
  for (const s of S) { s.a = acc / tot; acc += s.w; s.b = acc / tot; }
  return S;
}

export default function init(stage) {
  const k = createKit(stage, { night: true, label: 'A star whose life you can scrub through, with an HR diagram' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag along the timeline, or press Play', '#60a5fa');

  let M = 1, S = stages(M), s = 0.3, playing = false;
  const show = new Spring(0, 80, 14);
  const panel = createPanel(stage, { title: 'Life of a star' });
  const mS = panel.slider({ label: 'Starting mass', min: -1, max: 1.6, step: 0.01, value: 0, format: (v) => `${fmt(Math.pow(10, v), Math.pow(10, v) < 2 ? 2 : 1)} M☉`, onChange: (v) => { M = Math.pow(10, v); S = stages(M); } });
  panel.chips({ label: 'Examples', options: [{ value: '0.2', label: 'Red dwarf' }, { value: '1', label: 'The Sun' }, { value: '5', label: '5 Suns' }, { value: '15', label: '15 Suns' }, { value: '40', label: '40 Suns' }], value: '1', onChange: (v) => { M = +v; mS.set(L10(M)); S = stages(M); } });
  const [playB] = panel.buttonRow([{ label: 'Play', icon: 'play_arrow', onClick: () => { playing = !playing; if (playing && s > 0.995) s = 0; playB.setLabel(playing ? 'Pause' : 'Play'); k.animate(true); } }]);
  const st = panel.stats([{ key: 'stage', label: 'Stage' }, { key: 'dur', label: 'Lasts' }, { key: 'T', label: 'Surface temperature' }, { key: 'L', label: 'Luminosity' }]);
  const info = panel.info('');

  function cur() { for (const x of S) if (s <= x.b) return x; return S[S.length - 1]; }
  function lerpStage(out) {
    const c = cur(), i = S.indexOf(c), f = clamp((s - c.a) / (c.b - c.a), 0, 1), n = S[Math.min(S.length - 1, i + 1)];
    const ease = f < 0.9 ? 0 : (f - 0.9) / 0.1;
    const lt = (v) => L10(Math.max(v, 1e-6));
    out.T = Math.pow(10, lt(c.T) + (lt(n.T) - lt(c.T)) * ease);
    out.L = Math.pow(10, lt(c.L) + (lt(n.L) - lt(c.L)) * ease);
    out.R = Math.pow(10, lt(c.R) + (lt(n.R) - lt(c.R)) * ease);
    out.f = f; out.c = c;
    return out;
  }
  const O = { T: 0, L: 0, R: 0, f: 0, c: null };

  let sx = 0, sy = 0, hx = 0, hy = 0, hw = 0, hh = 0, tlX = 0, tlY = 0, tlW = 0;
  k.onResize((w, h) => {
    if (k.small) { sx = w * 0.3; sy = h * 0.3; hx = w * 0.56; hy = 40; hw = w * 0.42; hh = h * 0.5; }
    else { sx = w * 0.27; sy = h * 0.42; hx = w * 0.56; hy = 40; hw = w * 0.41; hh = h * 0.68; }
    tlX = 20; tlW = w - 40; tlY = h - 46;
  });
  const HX = (T0) => hx + 30 + (L10(40000) - L10(clamp(T0, 2500, 40000))) / (L10(40000) - L10(2500)) * (hw - 40);
  const HY = (L0) => hy + 20 + (6 - clamp(L10(Math.max(L0, 1e-5)), -4.5, 6)) / 10.5 * (hh - 44);

  const tl = k.drag({
    hit: (x, y, s2) => (y > tlY - 22 - s2 && y < tlY + 24 + s2 && x > tlX - 10 && x < tlX + tlW + 10 ? 1 : false),
    move: (x) => { s = clamp((x - tlX) / tlW, 0, 1); playing = false; playB.setLabel('Play'); },
    down: (x) => { s = clamp((x - tlX) / tlW, 0, 1); },
    cursor: 'ew-resize',
  });

  k.frame((ctx, dt, w, h) => {
    if (playing) { s += dt / 14; if (s >= 1) { s = 1; playing = false; playB.setLabel('Play'); } }
    lerpStage(O);
    const c = O.c;
    starfield(k, ctx, w, h, { seed: 21 });
    // the star itself
    const rpx = clamp(14 + 18 * L10(Math.max(O.R, 1e-5)), 3, Math.min(w, h) * 0.24);
    if (c.key === 'nebula' || c.key === 'proto') {
      for (let i = 0; i < 9; i++) { const a = i * 0.7 + k.t * 0.05, rr = (c.key === 'nebula' ? 90 : 60) * (0.5 + 0.5 * Math.sin(i * 1.7)); glow(ctx, sx + Math.cos(a) * rr * 0.6, sy + Math.sin(a * 1.3) * rr * 0.4, rr * 1.4, i % 2 ? '#8d7bd4' : '#d4709b', 0.35); }
      if (c.key === 'proto') { glow(ctx, sx, sy, 60, '#ff9d5c', 0.9); sphere(ctx, sx, sy, 14, '#ffb37a'); }
    } else if (c.key === 'bh') {
      glow(ctx, sx, sy, 120, '#f97316', 0.35);
      ctx.save(); ctx.translate(sx, sy); ctx.scale(1, 0.32); ctx.strokeStyle = 'rgba(255,170,90,0.85)'; ctx.lineWidth = 10; ctx.beginPath(); ctx.arc(0, 0, 64, 0, Math.PI * 2); ctx.stroke(); ctx.restore();
      ctx.beginPath(); ctx.arc(sx, sy, 26, 0, Math.PI * 2); ctx.fillStyle = '#000'; ctx.fill(); ctx.strokeStyle = 'rgba(255,200,140,0.8)'; ctx.lineWidth = 2; ctx.stroke();
    } else if (c.key === 'sn') {
      const p = O.f; glow(ctx, sx, sy, 60 + 260 * p, '#ffffff', 1 - p * 0.6); glow(ctx, sx, sy, 40 + 200 * p, '#93c5fd', 0.8);
    } else if (c.key === 'ns') {
      const ang = k.t * 6;
      for (let d = -1; d <= 1; d += 2) { ctx.fillStyle = 'rgba(147,197,253,0.25)'; ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(sx + Math.cos(ang) * 220 * d - Math.sin(ang) * 16, sy + Math.sin(ang) * 220 * d + Math.cos(ang) * 16); ctx.lineTo(sx + Math.cos(ang) * 220 * d + Math.sin(ang) * 16, sy + Math.sin(ang) * 220 * d - Math.cos(ang) * 16); ctx.fill(); }
      glow(ctx, sx, sy, 30, '#cfe4ff', 1); sphere(ctx, sx, sy, 5, '#dbeafe');
    } else {
      const col = starColor(O.T);
      if (c.key === 'pneb') { for (let i = 0; i < 3; i++) { ctx.strokeStyle = withAlpha(i % 2 ? '#6fd8c9' : '#a78bfa', 0.45); ctx.lineWidth = 10 - i * 3; ctx.beginPath(); ctx.ellipse(sx, sy, 60 + O.f * 80 + i * 10, 46 + O.f * 60 + i * 8, 0.3, 0, Math.PI * 2); ctx.stroke(); } }
      glow(ctx, sx, sy, rpx * 3.2, col, 0.85);
      sphere(ctx, sx, sy, rpx, col);
    }
    npill(ctx, c.name, sx, sy + Math.max(rpx, 40) + 24, '#e8eefb', 12);
    if (!k.small) { ctx.strokeStyle = 'rgba(255,255,255,0.18)'; ctx.setLineDash([3, 4]); ctx.beginPath(); ctx.arc(sx, sy, 14, 0, Math.PI * 2); ctx.stroke(); ctx.setLineDash([]); text(ctx, 'dotted ring: size of the Sun (log scale)', sx, sy - Math.max(rpx, 30) - 18, 'rgba(200,215,255,0.55)', 9.5, 600, 'center'); }
    // HR diagram
    card(ctx, hx, hy, hw, hh, 12, 'rgba(12,20,40,0.9)', 'rgba(160,190,255,0.18)');
    ctx.strokeStyle = 'rgba(160,190,255,0.25)'; ctx.lineWidth = 14; ctx.beginPath();
    for (let m = 0.1; m <= 40; m *= 1.25) { const L = m < 0.43 ? 0.23 * Math.pow(m, 2.3) : Math.pow(m, 3.5), T0 = 5772 * Math.pow(m, 0.505); if (m === 0.1) ctx.moveTo(HX(T0), HY(L)); else ctx.lineTo(HX(T0), HY(L)); }
    ctx.stroke();
    text(ctx, 'main sequence', HX(9000) + 10, HY(30) + 22, 'rgba(200,215,255,0.6)', 9.5, 700);
    for (const T0 of [30000, 10000, 6000, 3000]) { text(ctx, `${T0 / 1000}k K`, HX(T0), hy + hh - 10, '#8ea0c2', 9, 600, 'center'); }
    for (const e of [-4, -2, 0, 2, 4, 6]) text(ctx, e === 0 ? '1 L☉' : `10${e < 0 ? '⁻' : ''}${'⁰¹²³⁴⁵⁶'[Math.abs(e)]}`, hx + 6, HY(Math.pow(10, e)) + 3, '#8ea0c2', 9, 600);
    text(ctx, 'hot ← surface temperature → cool', hx + hw / 2, hy + 14, '#aab8d3', 9.5, 700, 'center');
    // the track through stages so far
    ctx.strokeStyle = 'rgba(251,191,36,0.85)'; ctx.lineWidth = 2; ctx.beginPath(); let started = false;
    for (const x of S) { if (x.a > s) break; if (x.L <= 0 || x.L > 1e7 || x.T > 60000 || x.T < 2000) continue; const X = HX(x.T), Y = HY(x.L); if (!started) { ctx.moveTo(X, Y); started = true; } else ctx.lineTo(X, Y); }
    if (started && O.L > 0 && O.L < 1e7 && O.T < 60000 && O.T > 2000) ctx.lineTo(HX(O.T), HY(O.L));
    ctx.stroke();
    if (O.L > 0 && O.T < 60000 && O.T > 2000) { glow(ctx, HX(O.T), HY(O.L), 16, starColor(O.T), 0.9); ctx.beginPath(); ctx.arc(HX(O.T), HY(O.L), 4.5, 0, Math.PI * 2); ctx.fillStyle = '#fff'; ctx.fill(); }
    else text(ctx, c.key === 'bh' ? 'no light: off the diagram' : 'off the diagram', hx + hw / 2, hy + hh / 2, '#aab8d3', 11, 700, 'center');
    // timeline
    for (const x of S) {
      const a = tlX + x.a * tlW, b = tlX + x.b * tlW;
      ctx.fillStyle = x === c ? 'rgba(96,165,250,0.55)' : 'rgba(160,190,255,0.16)'; ctx.beginPath(); ctx.roundRect(a + 1, tlY - 8, b - a - 2, 16, 6); ctx.fill();
      if (b - a > 54 || !k.small) text(ctx, x.name.split(' (')[0], (a + b) / 2, tlY + 24, x === c ? '#e8eefb' : '#8ea0c2', k.small ? 8 : 10, 600, 'center');
    }
    knob(ctx, tlX + s * tlW, tlY, 9, '#60a5fa', k.isHot(tl) ? 1 : 0);
    text(ctx, 'timeline (not to scale)', tlX, tlY - 16, '#8ea0c2', 9.5, 600);
    st.stage.set(c.name); st.dur.set(c.dur); st.T.set(c.key === 'bh' ? '—' : c.key === 'nebula' ? '≈ 10–30 K' : `${fmt(O.T, 0)} K`); st.L.set(O.L > 0 ? (O.L >= 100 ? `${fmt(O.L, 0)} L☉` : `${fmt(O.L, 3)} L☉`) : '0 (no light escapes)');
    info.set(c.info);
    badge.set(`${fmt(M, M < 2 ? 2 : 1)} M☉ star: ${c.name}`);
    k.animate(true);
  });

  k.debug = { set: (v) => { s = v; }, stage: () => cur().key, mass: (m) => { M = m; S = stages(M); } };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
