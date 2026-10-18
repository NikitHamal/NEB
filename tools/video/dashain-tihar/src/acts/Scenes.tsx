import React, { useCallback } from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { Mark } from '../brand/Mark';
import { C, TYPE } from '../brand/tokens';
import { Words } from '../fx/Words';
import { E, hitPulse, mix, prog, SPR, spr } from '../lib/anim';
import { measureTracked } from '../lib/measure';
import { type Px } from '../pixel/canvas';
import { PixelLayer } from '../pixel/PixelLayer';
import { diyo, dog, garland, hills, jamaraPot, kite, moon, P, ping, rangoli, sky, string, student, sun, tikaCloseUp, town } from '../pixel/world';
import { ACT, copy, CUE, f60 } from '../timeline';

// The acts, each a pixel scene drawn fresh per frame (6x, crisp) with the Nepali lines set over it
// in Poppins. The scene adapts to the frame: 320 x 180 art pixels in 16:9, 180 x 320 in 9:16.

const SCALE = 6;
const useArt = () => {
  const { width, height } = useVideoConfig();
  const pw = Math.round(width / SCALE), ph = Math.round(height / SCALE);
  return { width, height, pw, ph, portrait: height > width * 1.2, u: Math.min(width, height) / 1080 };
};

/** Where the hero kite sits on screen from the moment the camera has followed it up. */
const kiteSpot = (pw: number, ph: number, portrait: boolean) => ({ x: pw * (portrait ? 0.66 : 0.64), y: ph * (portrait ? 0.24 : 0.3) });

/** One line of copy: words rising in, Poppins 700, centred on x at y (px), in [color]. */
const Line: React.FC<{ id: string; act: keyof typeof ACT; f: number; x: number; y: number; size: number; color: string; align?: 'center' | 'left' }> = ({ id, act, f, x, y, size, color, align = 'center' }) => {
  const c = copy(id);
  const w = measureTracked(c.text, size, TYPE.display.weight, TYPE.display.track);
  const left = align === 'center' ? x - w / 2 : x;
  return (
    <div style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${left}px, ${y}px)` }}>
      <Words id={id} text={c.text} frame={f} start={c.in - ACT[act].from} out={c.out < 99999 ? c.out - ACT[act].from : undefined} size={size}
        style={{ fontFamily: '"Poppins"', fontSize: size, fontWeight: 700, letterSpacing: '-0.01em', lineHeight: 1.25, color }} />
    </div>
  );
};

const L = (act: keyof typeof ACT) => (abs: number) => abs - ACT[act].from;

// ---------------------------------------------------------------- 1 dawn
export const Dawn: React.FC = () => {
  const f = useCurrentFrame();
  const A = useArt();
  const l = L('dawn');
  const ground = A.ph * (A.portrait ? 0.78 : 0.8);
  const spot = kiteSpot(A.pw, A.ph, A.portrait);
  const draw = useCallback((px: Px) => {
    const day = prog(f, 0, ACT.dawn.dur, E.linear) * 0.7;
    sky(px, day, ground - A.ph * 0.1, f);
    sun(px, A.pw * (A.portrait ? 0.24 : 0.3), mix(ground - A.ph * 0.12, A.ph * (A.portrait ? 0.4 : 0.28), prog(f, 0, ACT.dawn.dur, E.outSoft)), A.ph * (A.portrait ? 0.04 : 0.055));
    hills(px, ground - A.ph * 0.06, 0);
    town(px, ground, 0, 0, 11, (A.portrait ? 1 : 2));
    jamaraPot(px, A.pw * (A.portrait ? 0.3 : 0.16), A.ph * 0.99, prog(f, l(CUE.jamara), l(CUE.jamara) + f60(70), E.out), f, 2);
    const lift = prog(f, l(CUE.kiteLift), ACT.dawn.dur + f60(20), E.inOut);
    const kx = mix(A.pw * 0.78, spot.x, lift), ky = mix(ground - A.ph * 0.2, spot.y + A.ph * 0.18, lift);
    string(px, kx, ky + 4, A.pw * 0.86, ground - A.ph * 0.14, 6 * lift, P.line);
    kite(px, kx, ky, 6, Math.sin(f * 0.05) * 0.15, P.red, P.yellow, f);
  }, [f, A.pw, A.ph, A.portrait, ground, spot.x, spot.y, l]);
  return (
    <AbsoluteFill style={{ background: C.ink, overflow: 'hidden' }}>
      <PixelLayer w={A.pw} h={A.ph} scale={SCALE} draw={draw} frame={f} />
      <Line id="dashain" act="dawn" f={f} x={A.width / 2} y={A.height * (A.portrait ? 0.15 : 0.12)} size={110 * A.u} color={C.white} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- 2 kites
const KITES = [
  { x: 0.18, y: 0.22, c: P.cloth, a: P.screenHi, s: 4 }, { x: 0.32, y: 0.4, c: P.teal, a: P.tealHi, s: 3 },
  { x: 0.45, y: 0.16, c: P.magenta, a: P.magentaHi, s: 3 }, { x: 0.82, y: 0.2, c: P.yellow, a: P.flameHi, s: 4 },
  { x: 0.9, y: 0.44, c: P.cloth, a: P.yellow, s: 3 }, { x: 0.08, y: 0.48, c: P.red, a: P.yellow, s: 3 },
];
export const Kites: React.FC = () => {
  const f = useCurrentFrame();
  const A = useArt();
  const l = L('kites');
  const ground = A.ph * (A.portrait ? 0.78 : 0.8);
  const spot = kiteSpot(A.pw, A.ph, A.portrait);
  const draw = useCallback((px: Px) => {
    // the camera follows the hero kite up: the town sinks a little
    const follow = prog(f, 0, l(CUE.fragKites), E.cam);
    const dy = follow * A.ph * 0.12;
    sky(px, 0.7 + prog(f, 0, ACT.kites.dur, E.linear) * 0.3, ground + dy - A.ph * 0.1, f);
    sun(px, A.pw * (A.portrait ? 0.24 : 0.3), A.ph * (A.portrait ? 0.4 : 0.28) + dy * 0.5, A.ph * (A.portrait ? 0.04 : 0.055));
    // every other kite in the valley, bobbing
    KITES.forEach((k, i) => {
      const appear = prog(f, i * 4, i * 4 + f60(20), E.out);
      if (appear <= 0) return;
      const bob = Math.sin(f * 0.04 + i) * 2;
      kite(px, A.pw * k.x, A.ph * k.y + bob + (1 - appear) * 30, k.s + (A.portrait ? 0 : 1), Math.sin(f * 0.05 + i) * 0.2, k.c, k.a, f + i * 9);
    });
    hills(px, ground + dy - A.ph * 0.06, 0);
    town(px, ground + dy, 0, 0, 11, (A.portrait ? 1 : 2));
    // the ping on the left, a child swinging out
    const swing = prog(f, l(CUE.ping), l(CUE.ping) + f60(40), E.out);
    ping(px, A.pw * (A.portrait ? 0.24 : 0.16), ground + dy, A.ph * 0.3, Math.sin(f * 0.06) * 0.55 * swing, true);
    // the hero kite rises into its place and holds there
    const rise = prog(f, 0, f60(80), E.out);
    const kx = spot.x, ky = mix(spot.y + A.ph * 0.18, spot.y, rise) + Math.sin(f * 0.05) * 1.2;
    string(px, kx, ky + 4, A.pw * 0.92, ground + dy - A.ph * 0.12, 10, P.line);
    kite(px, kx, ky, 7, Math.sin(f * 0.05) * 0.12, P.red, P.yellow, f);
  }, [f, A.pw, A.ph, A.portrait, ground, spot.x, spot.y, l]);
  return (
    <AbsoluteFill style={{ background: C.ink, overflow: 'hidden' }}>
      <PixelLayer w={A.pw} h={A.ph} scale={SCALE} draw={draw} frame={f} />
      <Line id="kites" act="kites" f={f} x={A.width / 2} y={A.height * (A.portrait ? 0.12 : 0.1)} size={96 * A.u} color={C.ink} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- 3 tika
export const Tika: React.FC = () => {
  const f = useCurrentFrame();
  const A = useArt();
  const l = L('tika');
  const draw = useCallback((px: Px) => {
    const s = A.ph / (A.portrait ? 200 : 120);
    const hand = prog(f, l(CUE.hand), l(CUE.tikaOn), E.out) * (1 - prog(f, l(CUE.jamaraEar) + f60(20), l(CUE.jamaraEar) + f60(60), E.inOut));
    const tika = f >= l(CUE.tikaOn) ? Math.min(1.15, spr(f, l(CUE.tikaOn) - 6, SPR.land)) : 0;
    const jam = prog(f, l(CUE.jamaraEar), l(CUE.jamaraEar) + f60(40), E.out);
    tikaCloseUp(px, A.pw * (A.portrait ? 0.42 : 0.36), A.ph * (A.portrait ? 0.42 : 0.55), s, hand, tika, jam);
    // marigold petals drifting down through the blessing: the close-up is never still
    for (let i = 0; i < 9; i++) {
      const t = ((f * 0.35 + i * 41) % (A.ph + 20)) - 10;
      const x = ((i * 53) % A.pw) + Math.sin((f + i * 30) * 0.03) * 6;
      px.disc(x, t, 1.3, i % 3 ? P.marigold : P.yellow);
    }
  }, [f, A.pw, A.ph, A.portrait, l]);
  return (
    <AbsoluteFill style={{ background: C.ink, overflow: 'hidden' }}>
      <PixelLayer w={A.pw} h={A.ph} scale={SCALE} draw={draw} frame={f} />
      <Line id="tika" act="tika" f={f} x={A.portrait ? A.width / 2 : A.width * 0.72} y={A.height * (A.portrait ? 0.74 : 0.7)} size={96 * A.u} color={C.ink} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- 4 the turn
export const Turn: React.FC = () => {
  const f = useCurrentFrame();
  const A = useArt();
  const l = L('turn');
  const ground = A.ph * (A.portrait ? 0.78 : 0.8);
  const spot = kiteSpot(A.pw, A.ph, A.portrait);
  const night = prog(f, l(CUE.dusk), l(CUE.dusk) + f60(90), E.inOut);
  const draw = useCallback((px: Px) => {
    const dy = A.ph * 0.12;
    sky(px, 1 + night, ground + dy - A.ph * 0.1, f);
    if (night < 0.6) sun(px, A.pw * (A.portrait ? 0.24 : 0.3), A.ph * (A.portrait ? 0.4 : 0.28) + dy * 0.5 + night * A.ph * 0.6, A.ph * (A.portrait ? 0.04 : 0.055));
    if (night > 0.5) moon(px, A.pw * 0.2, A.ph * 0.18, A.ph * 0.04);
    hills(px, ground + dy - A.ph * 0.06, night);
    town(px, ground + dy, night, night * 0.8, 11, (A.portrait ? 1 : 2));
    const ky = spot.y + Math.sin(f * 0.05) * 1.2;
    string(px, spot.x, ky + 4, A.pw * 0.92, ground + dy - A.ph * 0.12, 10, night > 0.5 ? P.marigoldLo : P.line, prog(f, l(CUE.lights), l(CUE.lights) + f60(30), E.out), f);
    kite(px, spot.x, ky, 7, Math.sin(f * 0.05) * 0.12, P.red, P.yellow, f);
  }, [f, A.pw, A.ph, ground, spot.x, spot.y, l, night]);
  return (
    <AbsoluteFill style={{ background: C.ink, overflow: 'hidden' }}>
      <PixelLayer w={A.pw} h={A.ph} scale={SCALE} draw={draw} frame={f} />
      <Line id="swap.1" act="turn" f={f} x={A.width / 2} y={A.height * (A.portrait ? 0.56 : 0.56)} size={150 * A.u} color={C.white} />
      <Line id="swap.2" act="turn" f={f} x={A.width / 2} y={A.height * (A.portrait ? 0.56 : 0.56)} size={150 * A.u} color={C.white} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- 5 tihar
const DIYO_CUES = [CUE.diyo1, CUE.diyo2, CUE.diyo3, CUE.diyo4, CUE.diyo5, CUE.diyo6];
export const Tihar: React.FC = () => {
  const f = useCurrentFrame();
  const A = useArt();
  const l = L('tihar');
  const ground = A.ph * (A.portrait ? 0.8 : 0.82);
  const draw = useCallback((px: Px) => {
    sky(px, 2, ground - A.ph * 0.3, f);
    moon(px, A.pw * 0.18, A.ph * 0.12, A.ph * 0.035);
    // the house front: a long brick wall with a ledge, a doorway, a marigold garland above
    const wallTop = ground - A.ph * 0.34;
    px.rect(0, wallTop, A.pw, ground - wallTop, P.wall);
    for (let y = wallTop + 4; y < ground; y += 4) px.hline(0, A.pw, y, P.wallLo);
    px.rect(A.pw * 0.44, wallTop + A.ph * 0.08, A.pw * 0.12, ground - wallTop - A.ph * 0.08, P.door);
    px.rect(0, ground - 3, A.pw, 3, P.ledge);
    garland(px, A.pw * 0.04, wallTop + 3, A.pw * 0.96, wallTop + 3, A.ph * 0.06, prog(f, 0, f60(80), E.out));
    // the courtyard floor and the rangoli
    px.rect(0, ground, A.pw, A.ph - ground, P.floor);
    rangoli(px, A.pw * 0.5, ground + (A.ph - ground) * 0.55, Math.min(A.pw, A.ph) * 0.17, prog(f, l(CUE.rangoli), l(CUE.rangoli) + f60(150), E.out));
    // one diyo per beat along the ledge
    DIYO_CUES.forEach((c, i) => {
      const x = A.pw * (0.08 + i * 0.168);
      const lit = f >= l(c) ? Math.min(1, (f - l(c)) / 6) : 0;
      diyo(px, x, ground - 6, lit, f + i * 7, 2);
    });
    dog(px, A.pw * (A.portrait ? 0.86 : 0.8), A.ph * 0.99, f, f >= l(CUE.dog) ? 0 : 1, 2);
  }, [f, A.pw, A.ph, A.portrait, ground, l]);
  // pull back from the first flame to the whole lit house
  const zoom = mix(2.2, 1, prog(f, 0, l(CUE.diyo4), E.cam));
  const fx = A.width * 0.08, fy = A.height * (A.portrait ? 0.78 : 0.8);
  return (
    <AbsoluteFill style={{ background: C.ink, overflow: 'hidden' }}>
      <div style={{ position: 'absolute', inset: 0, transformOrigin: `${fx}px ${fy}px`, transform: `scale(${zoom})` }}>
        <PixelLayer w={A.pw} h={A.ph} scale={SCALE} draw={draw} frame={f} />
      </div>
      <Line id="home" act="tihar" f={f} x={A.width / 2} y={A.height * (A.portrait ? 0.14 : 0.1)} size={104 * A.u} color={C.white} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- 6 study
const BOOKS = [P.cloth, P.red, P.teal, P.yellow];
export const Study: React.FC = () => {
  const f = useCurrentFrame();
  const A = useArt();
  const l = L('study');
  const ground = A.ph * 0.86;
  const draw = useCallback((px: Px) => {
    px.vgrad(0, A.ph, P.room);
    // the window: night sky with the kite still up
    const wx = A.pw * (A.portrait ? 0.12 : 0.62), wy = A.ph * 0.12, ww = A.pw * (A.portrait ? 0.76 : 0.3), wh = A.ph * (A.portrait ? 0.24 : 0.36);
    px.rect(wx - 2, wy - 2, ww + 4, wh + 4, P.frame);
    for (let y = 0; y < wh; y++) for (let x = 0; x < ww; x++) px.set(wx + x, wy + y, y < wh * 0.5 ? P.night[0] : P.night[1]);
    for (let i = 0; i < 14; i++) px.set(wx + ((i * 37) % ww), wy + ((i * 23) % (wh * 0.7)), P.star);
    kite(px, wx + ww * 0.7, wy + wh * 0.35, 3, Math.sin(f * 0.05) * 0.15, P.red, P.yellow, f);
    garland(px, wx - 2, wy - 3, wx + ww + 2, wy - 3, 3);
    const screen = prog(f, l(CUE.phone), l(CUE.phone) + f60(30), E.out);
    student(px, A.pw * (A.portrait ? 0.5 : 0.32), ground, A.ph / (A.portrait ? 150 : 75), f, 0.35 + 0.65 * screen);
    // books fan out of the phone, then settle back into it
    const sx = A.pw * (A.portrait ? 0.5 : 0.32), sy = ground - A.ph * 0.4;
    const out = prog(f, l(CUE.books), l(CUE.books) + f60(30), E.out);
    const back = prog(f, l(CUE.phone) - f60(4), l(CUE.phone) + f60(26), E.inOut);
    BOOKS.forEach((c, i) => {
      const a = (-0.7 + i * 0.46);
      const r = A.ph * 0.22 * out * (1 - back);
      const bx = sx + Math.sin(a) * r * 1.3, by = sy - Math.cos(a) * r;
      if (out > 0 && back < 1) {
        px.rect(bx - 3, by - 4, 6, 8, c);
        px.hline(bx - 3, bx + 2, by - 4, P.white);
      }
    });
  }, [f, A.pw, A.ph, A.portrait, ground, l]);
  return (
    <AbsoluteFill style={{ background: C.ink, overflow: 'hidden' }}>
      <PixelLayer w={A.pw} h={A.ph} scale={SCALE} draw={draw} frame={f} />
      <Line id="study" act="study" f={f} x={A.portrait ? A.width / 2 : A.width * 0.72} y={A.height * (A.portrait ? 0.48 : 0.62)} size={92 * A.u} color={C.white} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- 7 card
export const Card: React.FC = () => {
  const f = useCurrentFrame();
  const A = useArt();
  const l = L('end');
  const ground = A.ph * 0.86;
  const draw = useCallback((px: Px) => {
    sky(px, 2, ground - A.ph * 0.1, f + 600);
    moon(px, A.pw * 0.84, A.ph * 0.14, A.ph * 0.03);
    hills(px, ground - A.ph * 0.06, 1);
    town(px, ground, 1, 0.9, 11, (A.portrait ? 1 : 2));
    for (let i = 0; i < 9; i++) diyo(px, A.pw * (0.06 + i * 0.11), A.ph * 0.95, 1, f + i * 5);
    const kx = A.pw * 0.12, ky = A.ph * 0.2 + Math.sin(f * 0.05) * 1.2;
    string(px, kx, ky + 4, A.pw * 0.02, ground - A.ph * 0.2, 6, P.marigoldLo, 1, f);
    kite(px, kx, ky, 5, Math.sin(f * 0.05) * 0.12, P.red, P.yellow, f);
  }, [f, A.pw, A.ph, ground]);
  const markH = (A.portrait ? 240 : 230) * A.u;
  const creep = 1 + 0.03 * prog(f, 0, ACT.end.dur, E.linear);
  const pose: Record<string, { y: number; o: number }> = {};
  (['front', 'back', 'inner', 'light', 'shade'] as const).forEach((k, i) => {
    const t = prog(f, l(CUE.mark) + i * 6, l(CUE.mark) + i * 6 + f60(40), E.out);
    pose[k] = { y: (1 - t) * (i % 2 ? -90 : 90), o: prog(f, l(CUE.mark) + i * 6, l(CUE.mark) + i * 6 + f60(14), E.smooth) };
  });
  const name = prog(f, l(CUE.name), l(CUE.name) + f60(34), E.out);
  const lock = hitPulse(f - l(CUE.name) - f60(30));
  const url = prog(f, copy('url').in - ACT.end.from, copy('url').resolved - ACT.end.from, E.out);
  const nameSize = 120 * A.u;
  const cy = A.height * (A.portrait ? 0.36 : 0.32);
  return (
    <AbsoluteFill style={{ background: C.ink, overflow: 'hidden' }}>
      <PixelLayer w={A.pw} h={A.ph} scale={SCALE} draw={draw} frame={f} />
      <div style={{ position: 'absolute', inset: 0, transformOrigin: `${A.width / 2}px ${cy}px`, transform: `scale(${creep})` }}>
        <div style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${A.width / 2 - (markH * 948) / 1361 / 2}px, ${cy - markH}px)` }}>
          <Mark size={markH} id="card" pose={pose} />
        </div>
        <div data-text="wordmark" style={{ position: 'absolute', left: 0, top: 0, width: A.width, textAlign: 'center', transform: `translateY(${cy + 20 * A.u + (1 - name) * 20 * A.u}px) scale(${1 + 0.02 * lock})`, opacity: name, fontFamily: '"Poppins"', fontWeight: 700, fontSize: nameSize, letterSpacing: '-0.045em', color: C.white }}>NEBians</div>
      </div>
      <Line id="wish" act="end" f={f} x={A.width / 2} y={cy + 20 * A.u + nameSize * 1.25} size={64 * A.u} color={C.white} />
      <div style={{ position: 'absolute', left: 0, top: 0, width: A.width, textAlign: 'center', transform: `translateY(${cy + 20 * A.u + nameSize * 1.25 + 110 * A.u}px)`, opacity: url, fontFamily: '"Poppins"', fontWeight: 600, fontSize: 34 * A.u, color: C.sky }} data-ui="">nebians.consica.com.np</div>
    </AbsoluteFill>
  );
};
