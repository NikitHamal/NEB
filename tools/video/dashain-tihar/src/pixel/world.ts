// The festival world in pixels: Kathmandu valley under a sky that runs from dawn to night, and
// the things Dashain and Tihar are made of. Every function draws into a Px for one moment in time.
import { P } from '../brand/tokens';
import { bayer, Col, mix, Px, rnd, stampScaled } from './canvas';

export { P };


const lerpStops = (a: Col[], b: Col[], t: number) => a.map((c, i) => mix(c, b[i], t));

/** The sky: [phase] 0 = dawn, 1 = day, 2 = night (fractions blend). Stars come out after dusk. */
export const sky = (px: Px, phase: number, horizon: number, t: number) => {
  const stops = phase <= 1 ? lerpStops(P.dawn, P.day, phase) : lerpStops(P.day, P.night, phase - 1);
  px.vgrad(0, horizon, stops);
  if (phase > 1.55) {
    const r = rnd(7);
    const a = Math.min(1, (phase - 1.55) / 0.4);
    for (let i = 0; i < 70; i++) {
      const x = Math.floor(r() * px.w), y = Math.floor(r() * horizon * 0.8);
      const tw = Math.sin(t * 0.08 + i * 1.7) * 0.5 + 0.5;
      if (a * (0.4 + 0.6 * tw) > bayer(x, y)) px.set(x, y, P.star);
    }
  }
};

export const sun = (px: Px, x: number, y: number, r: number) => {
  for (let k = 3; k >= 1; k--) for (let yy = -r * 2; yy <= r * 2; yy++) for (let xx = -r * 2; xx <= r * 2; xx++) {
    const d = Math.hypot(xx, yy) / r;
    if (d > 1 && d < 1 + k * 0.35) px.dither(x + xx, y + yy, P.sun, 0.18 * (4 - k));
  }
  px.disc(x, y, r, P.sun);
  px.disc(x - r * 0.2, y - r * 0.2, r * 0.6, P.sunCore);
};

export const moon = (px: Px, x: number, y: number, r: number) => {
  // a crescent: the lit disc minus a shifted disc, worked out per pixel (nothing is erased)
  for (let yy = -r - 1; yy <= r + 1; yy++) for (let xx = -r - 1; xx <= r + 1; xx++) {
    const inLit = Math.hypot(xx + 0.5, yy + 0.5) <= r;
    const inShade = Math.hypot(xx + 0.5 - r * 0.5, yy + 0.5 + r * 0.25) <= r * 0.88;
    if (inLit && !inShade) px.set(x + xx, y + yy, P.moon);
  }
};

/** The Himalaya far off, then green hills: the valley's rim. [glow] warms them at dawn, darkens at night. */
export const hills = (px: Px, horizon: number, night: number) => {
  const r = rnd(3);
  const ridge: number[] = [];
  let y = horizon - px.h * 0.16;
  for (let x = 0; x < px.w; x++) {
    if (x % 6 === 0) y += (r() - 0.5) * px.h * 0.05;
    y = Math.min(horizon - px.h * 0.06, Math.max(horizon - px.h * 0.24, y));
    ridge.push(y);
  }
  const far = mix(P.ridgeFar, P.night[3], night);
  const snow = mix(P.snow, P.ridgeMid, night * 0.7);
  for (let x = 0; x < px.w; x++) {
    for (let yy = Math.floor(ridge[x]); yy < horizon; yy++) px.set(x, yy, yy < ridge[x] + 3 ? snow : far);
  }
  const mid = mix(P.hill, P.night[1], night * 0.85);
  const midLo = mix(P.hillLo, P.night[0], night * 0.85);
  for (let x = 0; x < px.w; x++) {
    const hy = horizon - px.h * 0.06 + Math.sin(x / 22) * px.h * 0.025 + Math.sin(x / 9 + 2) * px.h * 0.01;
    for (let yy = Math.floor(hy); yy < horizon + 2; yy++) px.set(x, yy, yy > hy + 4 ? midLo : mid);
  }
};

/** A Newari house: brick, a dark tiled roof, carved windows (lit at night). */
export const house = (px: Px, x: number, base: number, w: number, h: number, night: number, lit: number, seed: number) => {
  const brick = mix(P.brick, P.night[2], night * 0.75), brickLo = mix(P.brickLo, P.night[1], night * 0.75);
  px.rect(x, base - h, w, h, brick);
  for (let yy = base - h + 3; yy < base; yy += 3) px.hline(x, x + w - 1, yy, brickLo);
  const roof = mix(P.roof, P.night[0], night * 0.6);
  px.polygon([x - 3, base - h + 1, x + w + 2, base - h + 1, x + w - 2, base - h - 5, x + 2, base - h - 5], roof);
  px.hline(x - 3, x + w + 2, base - h + 1, mix(P.roofLo, P.night[0], night * 0.6));
  const r = rnd(seed);
  for (let wx = x + 3; wx + 4 < x + w - 1; wx += 7) for (let wy = base - h + 5; wy + 5 < base - 2; wy += 9) {
    const on = lit > r();
    px.rect(wx, wy, 4, 5, on ? P.windowLit : mix(P.window, P.night[0], night * 0.5));
    px.hline(wx - 1, wx + 4, wy - 1, mix(P.wood, P.night[0], night * 0.6));
  }
};

/** A pagoda: three tiers of roof, a golden finial. */
export const temple = (px: Px, cx: number, base: number, s: number, night: number) => {
  const roof = mix(P.roof, P.night[0], night * 0.6), wall = mix(P.brick, P.night[2], night * 0.75), gold = mix(P.yellow, P.night[2], night * 0.4);
  px.rect(cx - 6 * s, base - 8 * s, 12 * s, 8 * s, wall);
  for (let k = 0; k < 3; k++) {
    const y = base - 8 * s - k * 6 * s, hw = (11 - k * 2.5) * s;
    px.polygon([cx - hw, y, cx + hw, y, cx + hw * 0.45, y - 4 * s, cx - hw * 0.45, y - 4 * s], roof);
    if (k < 2) px.rect(cx - (5 - k * 1.5) * s, y - 6 * s, (10 - k * 3) * s, 2 * s, wall);
  }
  px.rect(cx - 0.5 * s, base - 28 * s, Math.max(1, s), 3 * s, gold);
};

/** A town row along the ground: houses and a temple, deterministic from [seed]. */
export const town = (px: Px, base: number, night: number, lit: number, seed = 11, k = 1) => {
  const r = rnd(seed);
  let x = -4;
  let i = 0;
  while (x < px.w + 4) {
    if (i === 3) { temple(px, x + 14 * k, base, Math.max(1, Math.round(px.h / 180)) * k, night); x += 30 * k; i++; continue; }
    const w = (16 + Math.floor(r() * 10)) * k, h = (14 + Math.floor(r() * 12)) * k;
    house(px, x, base, w, h, night, lit, seed * 7 + i);
    x += w + (2 + Math.floor(r() * 3)) * k;
    i++;
  }
  px.rect(0, base, px.w, px.h - base, mix(P.road, P.night[0], night * 0.8));
  // brick paving, rows offset like a Newari courtyard
  const joint = mix(P.brickLo, P.night[0], night * 0.8);
  for (let y = base + 3; y < px.h; y += 4) {
    px.hline(0, px.w, y, joint);
    for (let x = ((y / 4) % 2) * 4; x < px.w; x += 8) px.set(x, y + 1, joint), px.set(x, y + 2, joint);
  }
};

/** A kite (changa): a diamond with a cross-spar, tail flicking. */
export const kite = (px: Px, x: number, y: number, size: number, tilt: number, body: Col, accent: Col, t: number) => {
  const c = Math.cos(tilt), s = Math.sin(tilt);
  const pt = (dx: number, dy: number) => [x + dx * c - dy * s, y + dx * s + dy * c];
  const top = pt(0, -size), right = pt(size * 0.8, 0), bot = pt(0, size * 1.1), left = pt(-size * 0.8, 0);
  px.polygon([...top, ...right, ...bot, ...left], body);
  px.polygon([...top, ...right, x, y], accent);
  px.line(top[0], top[1], bot[0], bot[1], P.line);
  px.line(left[0], left[1], right[0], right[1], P.line);
  for (let i = 1; i <= 5; i++) {
    const tx = bot[0] + Math.sin(t * 0.25 + i) * 1.5, ty = bot[1] + i * 1.6;
    px.set(tx, ty, i % 2 ? P.red : P.yellow);
  }
};

/** The kite string, a catenary from the kite down to a hand or roof. */
export const string = (px: Px, x0: number, y0: number, x1: number, y1: number, sag: number, c: Col, lights = 0, t = 0) => {
  const n = Math.ceil(Math.hypot(x1 - x0, y1 - y0));
  for (let i = 0; i <= n; i++) {
    const u = i / n;
    const x = x0 + (x1 - x0) * u, y = y0 + (y1 - y0) * u + Math.sin(u * Math.PI) * sag;
    px.set(x, y, c);
    // Tihar: the same string, beaded with lights
    if (lights > 0 && i % 6 === 3 && u < lights) {
      const on = Math.sin(t * 0.18 + i) > -0.6;
      px.set(x, y + 1, on ? P.windowLit : P.marigold);
      px.set(x, y + 2, P.flameHi);
    }
  }
};

/** Jamara: barley shoots growing from a clay pot. [g] 0..1 growth. */
export const jamaraPot = (px: Px, x: number, base: number, g: number, t: number, k = 1) => {
  if (k > 1) { const lay = new Px(24, 34); jamaraPot(lay, 12, 33, g, t, 1); lay.outline(P.line); stampScaled(px, lay, x - 12 * k, base - 33 * k, k); return; }
  px.polygon([x - 7, base - 7, x + 7, base - 7, x + 5, base, x - 5, base], P.clay);
  px.hline(x - 8, x + 8, base - 7, P.clayLo);
  for (let i = -6; i <= 6; i += 1) {
    // each shoot on its own schedule, so the pot grows a pixel here and there every frame
    const gi = Math.max(0, Math.min(1, g * 1.25 - ((i * 5 + 6) % 13) * 0.02));
    const h = Math.max(0, gi * (10 + ((i * 7 + 13) % 5)));
    const sway = Math.sin(t * 0.06 + i * 0.7) * 0.6 * g;
    for (let k = 0; k < h; k++) px.set(x + i + sway * (k / 10), base - 8 - k, k > h - 3 ? P.jamara : i % 2 ? P.green : P.jamara);
  }
};

/** The ping: four bamboo poles leaning together and a swing on ropes. [a] swing angle. */
export const ping = (px: Px, x: number, base: number, h: number, a: number, child: boolean) => {
  const top = [x, base - h];
  for (const dx of [-0.45, -0.2, 0.2, 0.45]) px.line(x + dx * h, base, top[0], top[1], P.wood);
  const len = h * 0.85;
  const sx = top[0] + Math.sin(a) * len, sy = top[1] + Math.cos(a) * len;
  px.line(top[0], top[1], sx - 2, sy, P.line);
  px.line(top[0], top[1], sx + 2, sy, P.line);
  px.hline(sx - 3, sx + 3, sy, P.wood);
  if (child) {
    px.rect(sx - 1, sy - 6, 3, 5, P.red);
    px.disc(sx + 0.5, sy - 8, 1.8, P.skin);
    px.set(sx, sy - 9, P.hair); px.set(sx + 1, sy - 9, P.hair);
  }
};

/** A clay diyo; [lit] 0..1 brings the flame up. */
export const diyo = (px: Px, x: number, y: number, lit: number, t: number, s = 1) => {
  px.polygon([x - 4 * s, y - 2 * s, x + 4 * s, y - 2 * s, x + 2.5 * s, y + 1 * s, x - 2.5 * s, y + 1 * s], P.clay);
  px.hline(x - 3 * s, x + 3 * s, y - 2 * s, P.clayLo);
  if (lit <= 0) return;
  const fl = Math.sin(t * 0.5 + x) * 0.5 + Math.sin(t * 0.83 + y) * 0.4;
  const h = Math.max(1, (3 + fl) * s * Math.min(1, lit));
  for (let k = 0; k < h; k++) {
    const w = k < h * 0.4 ? 1 : 0;
    px.hline(x - w, x + w - (k === Math.floor(h) - 1 ? 1 : 0), y - 3 * s - k, k > h * 0.5 ? P.flameHi : P.flame);
  }
  // the pool of light it throws
  for (let yy = -6 * s; yy <= 4 * s; yy++) for (let xx = -9 * s; xx <= 9 * s; xx++) {
    const d = Math.hypot(xx, yy * 1.4) / (9 * s);
    if (d < 1 && px.get(x + xx, y + yy) !== P.flame && px.get(x + xx, y + yy) !== P.flameHi)
      px.dither(x + xx, y + yy, mix(px.get(x + xx, y + yy) | 0xff000000, P.flame, 0.35), (1 - d) * 0.5 * lit);
  }
};

/** A sayapatri (marigold) garland between two points. */
export const garland = (px: Px, x0: number, y0: number, x1: number, y1: number, sag: number, upto = 1) => {
  const n = Math.ceil(Math.abs(x1 - x0) / 3);
  for (let i = 0; i <= n * upto; i++) {
    const u = i / n;
    const x = x0 + (x1 - x0) * u, y = y0 + (y1 - y0) * u + Math.sin(u * Math.PI) * sag;
    px.disc(x, y, 1.6, i % 3 === 0 ? P.yellow : P.marigold);
    px.set(x, y, P.marigoldLo);
  }
};

/** A rangoli on the courtyard floor, petals appearing ring by ring with [p] 0..1. */
export const rangoli = (px: Px, cx: number, cy: number, r: number, p: number) => {
  const cols = [P.red, P.yellow, P.marigold, P.magenta, P.teal, P.white];
  const rings = 4;
  for (let k = rings - 1; k >= 0; k--) {
    const shown = Math.min(1, Math.max(0, p * rings - (rings - 1 - k)));
    if (shown <= 0) continue;
    const rr = r * (k + 1) / rings;
    const petals = 6 + k * 4;
    for (let i = 0; i < petals * shown; i++) {
      const a = (i / petals) * Math.PI * 2;
      px.ellipse(cx + Math.cos(a) * rr * 0.8, cy + Math.sin(a) * rr * 0.4, rr / 4.2, rr / 9, cols[(k + i) % cols.length]);
    }
  }
  if (p > 0.15) px.ellipse(cx, cy, r * 0.16, r * 0.08, P.yellow);
};

/** Kukur Tihar: a dog sitting, marigold garland round its neck, red tika, tail wagging. */
export const dog = (px: Px, x: number, base: number, t: number, look: number, k = 1) => {
  const layer = new Px(28, 26);
  const tail = Math.round(Math.sin(t * 0.35) * 2);
  layer.ellipse(15, 18, 7, 6, P.dog);
  layer.rect(9, 19, 3, 6, P.dog); layer.rect(17, 19, 3, 6, P.dog);
  layer.line(21, 18, 25, 13 + tail, P.dog); layer.line(21, 17, 25, 12 + tail, P.dog);
  layer.ellipse(9 + look, 10, 5.5, 5, P.dog);
  layer.ellipse(5 + look, 12, 3, 2.2, P.dogLo);
  layer.polygon([10 + look, 5, 13 + look, 3, 13 + look, 8], P.dogLo);
  layer.outline(P.line);
  layer.set(3 + look, 12, P.line);
  layer.set(9 + look, 9, P.line);
  layer.set(8 + look, 6, P.red);
  for (let i = 0; i < 7; i++) layer.disc(8 + i * 1.3, 15 + Math.sin(i / 2) * 1.2, 1.3, i % 2 ? P.marigold : P.yellow);
  stampScaled(px, layer, x - 14 * k, base - 25 * k, k);
};

/** Close-up for tika: a face in profile, the elder's hand, the red tika, jamara behind the ear. */
export const tikaCloseUp = (px: Px, cx: number, cy: number, s: number, hand: number, tika: number, jamara: number) => {
  // background warmth
  px.vgrad(0, px.h, P.warm);
  // shoulders in a shawl, the neck
  px.ellipse(cx - 2 * s, cy + 36 * s, 26 * s, 16 * s, P.cloth);
  px.ellipse(cx - 6 * s, cy + 30 * s, 14 * s, 8 * s, P.clothHi);
  px.rect(cx - 6 * s, cy + 14 * s, 12 * s, 12 * s, P.skinLo);
  // the face, in profile looking right, eyes closed to receive the blessing
  px.ellipse(cx, cy, 17 * s, 21 * s, P.skin);
  px.polygon([cx + 13 * s, cy - 7 * s, cx + 21 * s, cy + 3 * s, cx + 14 * s, cy + 6 * s], P.skin);
  px.ellipse(cx + 12 * s, cy + 13 * s, 5 * s, 4 * s, P.skin);
  px.ellipse(cx - 3 * s, cy - 13 * s, 19 * s, 12 * s, P.hair);
  px.rect(cx - 21 * s, cy - 14 * s, 8 * s, 22 * s, P.hair);
  px.ellipse(cx - 11 * s, cy + 3 * s, 3.6 * s, 5.5 * s, P.skinLo);
  px.line(cx + 6 * s, cy - 2 * s, cx + 11 * s, cy - 1 * s, P.line);
  px.line(cx + 11 * s, cy - 1 * s, cx + 12 * s, cy - 2 * s, P.line);
  px.line(cx + 13 * s, cy + 11 * s, cx + 17 * s, cy + 10 * s, P.skinLo);
  px.ellipse(cx + 7 * s, cy + 5 * s, 3 * s, 2 * s, P.magentaHi);
  // jamara tucked behind the ear
  if (jamara > 0) for (let i = 0; i < 7; i++) {
    const len = (12 + i * 2.2) * s * jamara;
    px.line(cx - 11 * s, cy - 1 * s, cx - 11 * s - Math.sin(0.25 + i * 0.13) * len * 0.55, cy - 1 * s - len, i % 2 ? P.jamara : P.green);
  }
  // the tika on the forehead, rice grains in the red
  if (tika > 0) {
    const r = 4 * s * Math.min(1, tika);
    px.ellipse(cx + 12 * s, cy - 11 * s, r * 0.75, r * 1.1, P.red);
    px.ellipse(cx + 12.5 * s, cy - 10 * s, r * 0.35, r * 0.5, P.redLo);
    if (tika > 0.6) { px.set(cx + 11 * s, cy - 13 * s, P.rice); px.set(cx + 13 * s, cy - 10 * s, P.rice); px.set(cx + 11.5 * s, cy - 8 * s, P.rice); }
  }
  // the elder's hand from the right: a red sleeve, the palm, three fingers, the ring finger
  // pressing the tika
  if (hand > 0) {
    const hx = cx + 66 * s - hand * 36 * s, hy = cy - 13 * s;
    px.rect(hx + 14 * s, hy - 5 * s, 60 * s, 14 * s, P.red);
    px.hline(hx + 14 * s, hx + 74 * s, hy - 5 * s, P.yellow);
    px.ellipse(hx + 8 * s, hy + 2 * s, 9 * s, 7 * s, P.skinLo);
    for (let i = 0; i < 3; i++) px.ellipse(hx - 2 * s, hy - 3 * s + i * 3.4 * s, 6 * s, 1.6 * s, P.skin);
    px.ellipse(hx - 6 * s, hy + 6 * s, 3 * s, 2.2 * s, P.skin);
    px.ellipse(hx - 8 * s, hy - 3 * s, 1.6 * s, 1.6 * s, P.red);
  }
};

/** The student at home, phone in hand, a diyo beside: the screen glows NEBians blue. */
export const student = (px: Px, x: number, base: number, s: number, t: number, screen: number) => {
  px.rect(x - 14 * s, base - 4 * s, 28 * s, 4 * s, P.wood);
  px.ellipse(x, base - 16 * s, 9 * s, 12 * s, P.cloth);
  px.disc(x - 2 * s, base - 32 * s, 6.5 * s, P.skin);
  px.ellipse(x - 3 * s, base - 36 * s, 7 * s, 4 * s, P.hair);
  px.rect(x + 3 * s, base - 22 * s, 7 * s, 10 * s, P.phone);
  px.rect(x + 4 * s, base - 21 * s, 5 * s, 8 * s, mix(P.phone, P.screen, screen));
  if (screen > 0.6) px.rect(x + 5 * s, base - 20 * s, 3 * s, 2 * s, P.screenHi);
  // the screen's blue light on the face and hands
  const gx = x + 6 * s, gy = base - 22 * s, gr = 15 * s;
  for (let yy = -gr; yy <= gr; yy++) for (let xx = -gr; xx <= gr; xx++) {
    const d = Math.hypot(xx, yy) / gr;
    const c = px.get(gx + xx, gy + yy);
    if (d < 1 && c >>> 24) px.dither(gx + xx, gy + yy, mix(c | 0xff000000, P.screenHi, 0.3), (1 - d) * 0.4 * screen);
  }
  diyo(px, x - 22 * s, base - 3 * s, 1, t, s);
};
