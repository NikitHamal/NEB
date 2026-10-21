// Stellar evolution by initial mass: main-sequence L ~ M^3.5 (M^2.3 below 0.43 M☉), T ~ 5772 K M^0.505,
// R ~ M^0.8 / M^0.57, lifetime ~ 10 Gyr M^-2.5; the ending follows the mass (white dwarf below ~8 M☉,
// neutron star to ~25 M☉, black hole above).
export const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: 0 }).replace(/,/g, ' ');
export function lifeTxt(y) { return y >= 1e9 ? `${fmt(y / 1e9, y < 1e10 ? 1 : 0)} billion years` : y >= 1e6 ? `${fmt(y / 1e6, 0)} million years` : `${fmt(y, 0)} years`; }

export function stages(M) {
  const Lms = M < 0.43 ? 0.23 * Math.pow(M, 2.3) : Math.pow(M, 3.5);
  const Tms = 5772 * Math.pow(M, 0.505); const Rms = Math.pow(M, M < 1 ? 0.8 : 0.57);
  const tms = 1e10 * Math.pow(M, -2.5);
  const S = [
    { key: 'nebula', name: 'Nebula', T: 30, L: Lms * 1e-3, R: 2000, dur: 'millions of years', w: 0.09, info: 'A cold cloud of hydrogen and dust, light-years wide. Gravity pulls a dense clump of it together.' },
    { key: 'proto', name: 'Protostar', T: 3500, L: Lms * 6, R: Rms * 5, dur: lifeTxt(5e7 / Math.pow(M, 2.5)), w: 0.09, info: 'The clump collapses and heats, feeding from a spinning disc and firing jets from its poles. At about 10 million °C in the core, hydrogen fusion ignites.' },
    { key: 'ms', name: 'Main sequence', T: Tms, L: Lms, R: Rms, dur: lifeTxt(tms), w: 0.42, info: `Hydrogen fuses into helium and the outward push of that energy balances gravity. At ${fmt(M, 1)} M☉ this lasts about ${lifeTxt(tms)}.` },
  ];
  if (M < 0.5) {
    S.push({ key: 'wd', name: 'White dwarf (far future)', T: 6000, L: 1e-3, R: 0.013, dur: 'longer than the age of the Universe', w: 0.4, info: `A red dwarf burns so slowly (about ${lifeTxt(tms)}) that none has died yet: the Universe is only 13.8 billion years old. It will fade to a white dwarf.` });
  } else if (M < 8) {
    S.push({ key: 'giant', name: 'Red giant', T: 3800, L: 1000 * Math.pow(M, 1.2), R: 100 * Math.pow(M, 0.6), dur: lifeTxt(tms * 0.1), w: 0.13, info: 'Core hydrogen runs out: the core shrinks and heats, and the outer layers swell to a hundred times the size, cool and red, churning in a few giant convection cells. The Sun will do this in about 5 billion years.' });
    S.push({ key: 'pneb', name: 'Planetary nebula', T: 100000, L: 3000, R: 0.05, dur: 'about 10 000 years', w: 0.1, info: 'The outer layers drift away as a glowing shell, lit by the exposed hot core: oxygen glows teal on the inside, hydrogen and nitrogen red at the edge. (Nothing to do with planets.)' });
    S.push({ key: 'wd', name: 'White dwarf', T: 12000, L: 1e-3, R: 0.012, dur: 'cools for billions of years', w: 0.16, info: 'The leftover core: about the size of Earth but with half the Sun\'s mass. A teaspoon of it weighs about five tonnes.' });
  } else {
    S.push({ key: 'giant', name: 'Red supergiant', T: 3600, L: 1e5 * Math.min(3, M / 15), R: 800, dur: lifeTxt(tms * 0.1), w: 0.14, info: 'Hundreds of times wider than the Sun, fusing heavier and heavier elements in shells, until the core is iron, which fusion cannot burn.' });
    S.push({ key: 'sn', name: 'Supernova', T: 20000, L: 1e9, R: 2000, dur: 'weeks', w: 0.1, info: 'The iron core collapses in under a second and the star explodes, briefly outshining its whole galaxy. Gold, silver and uranium are forged in such explosions.' });
    S.push(M < 25
      ? { key: 'ns', name: 'Neutron star', T: 600000, L: 1e-1, R: 1.5e-5, dur: 'forever (it cools)', w: 0.16, info: 'A ball of neutrons about 20 km across, spinning many times a second and sweeping beams of radio waves like a lighthouse: a pulsar. A teaspoon would weigh a billion tonnes.' }
      : { key: 'bh', name: 'Black hole', T: 0, L: 0, R: 4e-5, dur: 'forever', w: 0.16, info: 'The core collapses without limit. Not even light escapes the event horizon; light passing near it is bent, so the glowing disc behind it appears above and below the shadow.' });
  }
  const tot = S.reduce((s, x) => s + x.w, 0); let acc = 0;
  for (const s of S) { s.a = acc / tot; acc += s.w; s.b = acc / tot; }
  return S;
}

export function at(S, s, out = {}) {
  let c = S[S.length - 1];
  for (const x of S) if (s <= x.b) { c = x; break; }
  const i = S.indexOf(c); const n = S[Math.min(S.length - 1, i + 1)];
  const f = Math.min(1, Math.max(0, (s - c.a) / (c.b - c.a)));
  const e = f < 0.88 ? 0 : (f - 0.88) / 0.12;
  const lt = (v) => Math.log10(Math.max(v, 1e-6));
  const mix = (a, b) => Math.pow(10, lt(a) + (lt(b) - lt(a)) * e);
  out.c = c; out.n = n; out.i = i; out.f = f; out.e = e;
  out.T = mix(c.T || 1, n.T || 1); out.L = mix(c.L || 1e-6, n.L || 1e-6); out.R = mix(c.R, n.R);
  return out;
}
