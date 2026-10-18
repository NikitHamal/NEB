import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C } from '../brand/tokens';
import { READER } from '../data';
import { TypeOn } from '../fx/TypeOn';
import { E, hitPulse, prog, SPR, spr } from '../lib/anim';
import { camera, lc, type Shot } from '../lib/camera';
import { ACT, copy, CUE, f60 } from '../timeline';
import { Chip, Phone, T } from '../ui/kit';
import { Neby, useNebyFrames } from '../ui/neby';
import { useStage } from '../ui/stage';

// ACT 4 - the reader. A zoom-out hop: from the page filling the frame back to the phone it is open
// in, on the ink stage. Ask Neby is pressed; the sheet rises and Neby, the product's own avatar,
// lands beside the phone (the film's second true landing) and explains while the answer types and
// the line it explains lights on the page. Then paper rises from the bottom edge into Act 5.

const L = (abs: number) => abs - ACT.reader.from;
const BARS = [0.34, 0.52, 0.86, 1]; // successive ionisation energies on the page's figure: each higher

export const Reader: React.FC = () => {
  const f = useCurrentFrame();
  const S = useStage();
  const u = S.u;
  const frames = useNebyFrames();

  const phoneW = (S.portrait ? 420 : S.square ? 330 : 440) * S.ut; // the phone scales its own screen (q)
  const phoneH = phoneW * 2.06;
  const q = phoneW / 440;
  const nebySize = (S.portrait ? 330 : S.square ? 360 : 500) * S.ut;
  const phone = S.portrait
    ? { x: S.cx - phoneW / 2, y: S.band.y + S.band.h - phoneH }
    : { x: S.cx - (S.square ? 200 : 330) * u - phoneW / 2, y: S.cy - phoneH / 2 };
  const nebyPos = S.portrait
    ? { x: S.cx - nebySize / 2, y: S.band.y - 20 * u }
    : { x: S.cx + (S.square ? 190 : 330) * u - nebySize / 2, y: S.cy - nebySize / 2 - 20 * u };

  // zoom-out hop: from the page filling the frame to the phone it is open in
  const bezel = phoneW * 0.035;
  const pageFocus = { x: phone.x + bezel + 40 * q, y: phone.y + bezel + 150 * q };
  const A: Shot = { ax: pageFocus.x, ay: pageFocus.y, sx: S.w * 0.18, sy: S.h * 0.3, k: 2.6 };
  const B: Shot = { ax: S.cx, ay: S.cy, sx: S.cx, sy: S.cy, k: 1 };
  const hop = prog(f, 0, f60(66), E.cam);
  const cam = lc(A, B, hop);

  const press = hitPulse(f - L(CUE.askNeby) - 2);
  const sheet = prog(f, L(CUE.askNeby) + f60(4), L(CUE.askNeby) + f60(40), E.out);
  const land = spr(f, L(CUE.neby) - 14, SPR.land); // true landing #2
  const nebyIn = prog(f, L(CUE.neby) - 14, L(CUE.neby) - 4, E.smooth);
  const lit = prog(f, L(CUE.highlight), L(CUE.highlight) + f60(16), E.out);
  const out = prog(f, L(CUE.readerOut), L(CUE.readerOut) + f60(36), E.contact);

  const sw = phoneW - 2 * bezel;
  const sh = phoneH - 2 * bezel;
  const sheetH = sh * 0.36;
  const lineW = [0.92, 0.84, 0.9, 0.62, 0.88, 0.8, 0.9, 0.54];

  return (
    <AbsoluteFill style={{ background: C.ink, overflow: 'hidden' }}>
      <div style={camera(cam)}>
        <div style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${phone.x}px, ${phone.y + out * 40 * u}px)` }}>
          <Phone w={phoneW}>
            <div style={{ position: 'absolute', left: 0, top: 0, width: sw, height: 74 * q, background: C.sky, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: `0 ${26 * q}px`, boxSizing: 'border-box' }}>
              <T role="ui" size={22 * q} style={{ fontWeight: 600 }}>{READER.book}</T>
              <T role="ui" size={22 * q} color={C.ink}>{`${READER.page} / ${READER.pages}`}</T>
            </div>
            <div style={{ position: 'absolute', left: 30 * q, top: 104 * q, right: 30 * q }}>
              <T role="title" size={28 * q}>{READER.heading}</T>
              <div style={{ marginTop: 22 * q, display: 'flex', flexDirection: 'column', gap: 14 * q }}>
                {lineW.map((w, i) => (
                  <div key={i} style={{ position: 'relative', width: w * (sw - 60 * q), height: 12 * q }}>
                    {i === 4 && <div style={{ position: 'absolute', left: -8 * q, top: -9 * q, width: (w * (sw - 60 * q) + 16 * q) * lit, height: 30 * q, borderRadius: 8 * q, background: C.sky }} />}
                    <div style={{ position: 'absolute', inset: 0, borderRadius: 6 * q, background: i === 4 && lit > 0.5 ? C.accent : C.line }} />
                  </div>
                ))}
              </div>
              <div style={{ marginTop: 26 * q, height: 150 * q, borderRadius: 16 * q, background: C.mist, display: 'flex', alignItems: 'flex-end', gap: 22 * q, padding: `0 ${34 * q}px ${22 * q}px`, boxSizing: 'border-box' }}>
                {BARS.map((b, i) => <div key={i} style={{ flex: 1, height: b * 100 * q, borderRadius: 6 * q, background: i === BARS.length - 1 ? C.accent : C.sky }} />)}
              </div>
            </div>
            {/* Ask Neby, then the sheet with the answer */}
            <div style={{ position: 'absolute', right: 24 * q, bottom: 28 * q, transform: `translateY(${-sheet * sheetH}px) scale(${1 - 0.06 * press})`, transformOrigin: '100% 100%', opacity: 1 - sheet }}>
              <Chip size={22 * q} tone="accent">{copy('askNeby').text}</Chip>
            </div>
            <div style={{ position: 'absolute', left: 0, top: 0, transform: `translateY(${sh - sheetH * sheet}px)`, width: sw, height: sheetH, background: C.ink, borderRadius: `${30 * q}px ${30 * q}px 0 0`, padding: 30 * q, boxSizing: 'border-box' }}>
              <T role="ui" size={22 * q} color={C.sky} style={{ fontWeight: 600 }}>Neby</T>
              <div style={{ marginTop: 14 * q, display: 'flex', flexDirection: 'column', gap: 4 * q }}>
                <TypeOn id="answer1" text={copy('answer1').text} frame={f} start={L(CUE.answer)} cps={28} role="ui" size={24 * q} caret={false} style={{ color: C.white }} />
                <TypeOn id="answer2" text={copy('answer2').text} frame={f} start={L(CUE.answer2)} cps={28} role="ui" size={24 * q} caret={false} style={{ color: C.white }} />
              </div>
            </div>
          </Phone>
        </div>
      </div>
      {frames && nebyIn > 0 && (
        <div style={{ position: 'absolute', left: 0, top: 0, opacity: nebyIn * (1 - out), transform: `translate(${nebyPos.x}px, ${nebyPos.y + (1 - land) * 160 * u + out * 60 * u}px)` }}>
          <Neby frames={frames} i={f} size={nebySize} />
        </div>
      )}
      {/* the act rises out of the ink the columns closed into */}
      <AbsoluteFill style={{ background: C.ink, opacity: 1 - prog(f, 0, f60(18), E.smooth) }} />
      {/* paper rises from the bottom edge into the next chapter */}
      <div style={{ position: 'absolute', left: 0, top: 0, width: S.w, height: S.h * out, background: C.white, transform: `translateY(${S.h * (1 - out)}px)` }} />
    </AbsoluteFill>
  );
};
