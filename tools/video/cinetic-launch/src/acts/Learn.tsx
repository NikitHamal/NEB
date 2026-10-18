import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C, TYPE } from '../brand/tokens';
import { LEVELS, RESOURCES } from '../data';
import { Words } from '../fx/Words';
import { E, mix, prog, stagger } from '../lib/anim';
import { measureTracked } from '../lib/measure';
import { ACT, copy, CUE, f60 } from '../timeline';
import { Card, Chip, PageShape, rectQuad, T } from '../ui/kit';
import { useStage } from '../ui/stage';

// ACT 3 - learn. The blue chapter. The page drops in from the forum and multiplies into the library:
// notes, a past paper, a solved book, each carrying the page as its header band. Every level the
// library serves blooms round them. Only then the words: "Study materials." Stepped ink columns rise from
// the bottom edge and close into the ink stage the reader opens on.

const L = (abs: number) => abs - ACT.learn.from;

export const Learn: React.FC = () => {
  const f = useCurrentFrame();
  const S = useStage();
  const u = S.u;

  // the cards: a row in 16:9 and 1:1, a column in 9:16
  const n = RESOURCES.length;
  const cw = S.portrait ? S.band.w * 0.86 : S.square ? (S.band.w - 2 * 24 * u) / 3 : Math.min(520 * u, (S.band.w - 2 * 44 * u) / 3);
  const ch = S.portrait ? 230 * u : S.square ? 280 * u : 360 * u;
  const gap = S.portrait ? 26 * u : S.square ? 24 * u : 44 * u;
  const groupH = S.portrait ? n * ch + (n - 1) * gap : ch;
  const groupTop = S.portrait ? S.band.y + S.band.h * 0.26 : S.cy - ch / 2 + 20 * u;
  const slot = (i: number) =>
    S.portrait ? { x: S.cx - cw / 2, y: groupTop + i * (ch + gap) } : { x: S.cx - (n * cw + (n - 1) * gap) / 2 + i * (cw + gap), y: groupTop };
  const centre = { x: S.cx - cw / 2, y: groupTop + (S.portrait ? (groupH - ch) / 2 : 0) };

  // the page falls in from where the forum sank, then splits three ways
  const drop = prog(f, 0, f60(30), E.out);
  const fan = (i: number) => prog(f, f60(18) + stagger(i, n, f60(10)), f60(18) + stagger(i, n, f60(10)) + f60(42), E.glide);
  const content = (i: number) => prog(f, f60(44) + i * f60(4), f60(66) + i * f60(4), E.out);

  // levels bloom outward from the cards, in a centred row (two in 9:16)
  const chipSize = (S.portrait ? 26 : 24) * u;
  const chipW = (t: string) => measureTracked(t, chipSize, 600, TYPE.ui.track) + chipSize * 1.6;
  const rows: string[][] = S.portrait ? [LEVELS.slice(0, 3), LEVELS.slice(3)] : [LEVELS];
  const chipGap = 16 * u;
  const chipTop = groupTop + groupH + (S.portrait ? 54 : 56) * u;

  // "Study materials." over the cards
  const c = copy('learn');
  const size = TYPE.display.size * S.ut * (S.portrait ? 0.95 : 1);
  const textW = measureTracked(c.text, size, TYPE.display.weight, TYPE.display.track);
  const textTop = S.portrait ? S.band.y + 10 * u : S.band.y + (groupTop - S.band.y) / 2 - size * 0.62;

  // stepped columns of ink close the chapter
  const cols = S.portrait ? 9 : 15;
  const colW = S.w / cols;
  const mid = (cols - 1) / 2;
  const t0 = L(CUE.columns);

  return (
    <AbsoluteFill style={{ background: C.accent, overflow: 'hidden' }}>
      <div style={{ position: 'absolute', inset: 0, transformOrigin: `${S.cx}px ${S.cy}px`, transform: `scale(${1 + 0.04 * prog(f, 0, L(CUE.columns), E.linear)})` }}>
      <div style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${S.cx - textW / 2}px, ${textTop}px)` }}>
        <Words id="learn" text={c.text} frame={f} start={c.in - ACT.learn.from} out={c.out - ACT.learn.from} size={size} style={{ fontFamily: '"Poppins"', fontSize: size, fontWeight: TYPE.display.weight, letterSpacing: `${TYPE.display.track}em`, lineHeight: TYPE.display.lead, color: C.white }} />
      </div>
      {RESOURCES.map((r, i) => {
        const p = fan(i);
        const s = slot(i);
        const x = mix(centre.x, s.x, p);
        const y = mix(centre.y - (1 - drop) * S.h * 0.6, s.y, p);
        const k = content(i);
        return (
          <div key={r.kind} style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${x}px, ${y}px)`, zIndex: n - i }}>
            <Card w={cw} h={ch} r={24 * u} pad={0} ink>
              {/* the page fills the card, then settles into its header (its left band in 9:16) */}
              <PageShape quad={S.portrait ? rectQuad(0, 0, mix(cw, 150 * u, k), ch) : rectQuad(0, 0, cw, mix(ch, ch * 0.34, k))} w={cw} h={ch} />
              <div style={{ position: 'absolute', left: S.portrait ? 180 * u : 28 * u, top: S.portrait ? 34 * u : ch * 0.34 + 24 * u, right: 24 * u, opacity: k, display: 'flex', flexDirection: 'column', gap: 10 * u }}>
                <T role="title" size={(S.square ? 28 : 32) * u}>{r.title}</T>
                <T role="ui" size={22 * u} color={C.mute}>{r.meta}</T>
              </div>
              <div style={{ position: 'absolute', left: S.portrait ? 180 * u : 28 * u, top: S.portrait ? ch - 70 * u : (ch * 0.34 - 44 * u) / 2, opacity: k }}>
                <Chip size={20 * u} tone="white">{r.kind}</Chip>
              </div>
            </Card>
          </div>
        );
      })}
      {rows.map((row, ri) => {
        const total = row.reduce((s, t) => s + chipW(t), 0) + chipGap * (row.length - 1);
        let x = S.cx - total / 2;
        return row.map((t, i) => {
          const idx = ri * 3 + i;
          const at = L(CUE.chips) + idx * f60(5);
          const p = prog(f, at, at + f60(20), E.out);
          const cx0 = x;
          x += chipW(t) + chipGap;
          if (p <= 0) return null;
          return (
            <div key={t} style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${cx0}px, ${chipTop + ri * 70 * u + (1 - p) * -30 * u}px) scale(${0.8 + 0.2 * p})`, opacity: p }}>
              <Chip size={chipSize} tone="white">{t}</Chip>
            </div>
          );
        });
      })}
      </div>
      {Array.from({ length: cols }, (_, i) => {
        const s0 = t0 + Math.abs(i - mid) * f60(2);
        const hgt = prog(f, s0, s0 + f60(40), E.smooth) * S.h;
        if (hgt <= 0) return null;
        return <div key={i} style={{ position: 'absolute', left: 0, top: 0, width: colW + 1, height: hgt, background: C.ink, zIndex: 10, transform: `translate(${i * colW}px, ${S.h - hgt}px)` }} />;
      })}
    </AbsoluteFill>
  );
};
