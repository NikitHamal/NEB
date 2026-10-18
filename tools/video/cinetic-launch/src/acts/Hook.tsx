import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C, TYPE } from '../brand/tokens';
import { QUESTION } from '../data';
import { Chain, chainLayout } from '../fx/Chain';
import { TypeOn } from '../fx/TypeOn';
import { arrive, E, mix, prog } from '../lib/anim';
import { camera, lc, type Shot } from '../lib/camera';
import { measureTracked } from '../lib/measure';
import { ACT, copy, CUE, f60 } from '../timeline';
import { Chip, PageShape, rectQuad, SHADOW, T } from '../ui/kit';
import { type Stage, useStage } from '../ui/stage';

// ACT 1 - the problem. The film opens inside the word "Stuck", its S cropped by the frame edge, and
// pulls back to the line. The page (the device: the logo's light facet) slides in under it with the
// exercise on it; "one question?" completes the thought. After the read a caret opens between the
// two fragments, swells into a capsule and widens into the Ask bar, shoving the words out of frame;
// the question types in. Act 2 opens on exactly this pose.

const L = (abs: number) => abs - ACT.hook.from;
/** The hook's living drift after the pull, px per frame at 1080p: alive, never enough to crop the line. */
const DRIFT = 0.12;

/** Layout shared with Act 2, which opens on this act's last pose. */
export const hookLayout = (S: Stage) => {
  const disp = TYPE.display;
  const full = copy('hook.1').text + ' ' + copy('hook.2').text;
  const unit = measureTracked(full, 100, disp.weight, disp.track) / 100;
  const size = Math.min(disp.size * S.ut * (S.portrait ? 0.9 : 1), (S.band.w * 0.94) / unit);
  const lineMid = S.portrait ? S.band.y + S.band.h * 0.36 : S.band.y + S.band.h * 0.3;
  const top = lineMid - (size * disp.lead) / 2;
  const pageW = Math.min(S.band.w * (S.portrait ? 1 : 0.62), 880 * S.u);
  const pageH = pageW * 0.42;
  const barW = Math.min(S.band.w * 0.92, 1460 * S.u);
  const barH = 104 * S.u;
  // the page sits under the line, and clear of the Ask bar the line becomes
  const page = { x: S.cx - pageW / 2, y: Math.max(lineMid + size * 0.95, lineMid + barH / 2 + 28 * S.u), w: pageW, h: pageH };
  const bar = { x: S.cx - barW / 2, y: lineMid - barH / 2, w: barW, h: barH };
  return { size, top, lineMid, page, bar };
};

/** The page's content: the exercise the student is stuck on. Shared with Act 2. */
export const PageContent: React.FC<{ w: number; h: number; u: number; o?: number }> = ({ w, h, u, o = 1 }) => (
  <div style={{ position: 'absolute', left: 0, top: 0, width: w, height: h, padding: 34 * u, boxSizing: 'border-box', opacity: o }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: 16 * u }}>
      <Chip size={22 * u} tone="white">Q5</Chip>
      <T role="ui" size={24 * u} color={C.ink}>{`${QUESTION.subject} · ${QUESTION.klass}`}</T>
    </div>
    <div style={{ marginTop: 22 * u, width: w - 68 * u }}>
      <T role="title" size={30 * u} style={{ whiteSpace: 'normal' }}>{copy('exercise').text}</T>
    </div>
    <div style={{ position: 'absolute', left: 34 * u, right: 34 * u, bottom: 30 * u, height: h * 0.2, borderRadius: 14 * u, border: `${2.5 * u}px dashed ${C.line}` }} />
  </div>
);

/** The Ask bar: input with the typed question and the Ask button. Shared with Act 2. */
export const AskBar: React.FC<{ w: number; h: number; u: number; f: number; typeFrom: number; press?: number; o?: number }> = ({ w, h, u, f, typeFrom, press = 0, o = 1 }) => {
  const btnW = 150 * u;
  return (
    <div style={{ position: 'absolute', left: 0, top: 0, width: w, height: h, borderRadius: h / 2, background: C.white, boxShadow: SHADOW }}>
      <div style={{ position: 'absolute', left: 44 * u, top: 0, height: h, display: 'flex', alignItems: 'center', opacity: o }}>
        <TypeOn id="question" text={copy('question').text} frame={f} start={typeFrom} cps={30} role="ui" size={30 * u} style={{ color: C.ink }} />
      </div>
      <div style={{ position: 'absolute', right: 12 * u, top: 12 * u, width: btnW, height: h - 24 * u, borderRadius: (h - 24 * u) / 2, background: C.accent, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${1 - 0.06 * press})`, opacity: o }}>
        <T role="ui" size={28 * u} color={C.white} style={{ fontWeight: 600 }}>Ask</T>
      </div>
    </div>
  );
};

export const Hook: React.FC = () => {
  const f = useCurrentFrame();
  const S = useStage();
  const lay = hookLayout(S);
  const { size, top, lineMid, page, bar } = lay;
  const disp = TYPE.display;
  const chain = chainLayout('hook', { role: 'display', size, x: S.cx, top });

  // camera: inside "Stuck" at 3.2x, the S cropped by the left edge; pull back on E.dolly to the
  // whole line, then a slow creep that keeps every read alive
  const stuckLeft = chain.lineLeft[0];
  const A: Shot = { ax: stuckLeft + size * 0.34, ay: lineMid, sx: 0, sy: S.h * 0.46, k: 3.2 };
  const B: Shot = { ax: S.cx, ay: lineMid, sx: S.cx, sy: lineMid, k: 1 };
  const pull = prog(f, L(CUE.pull), L(CUE.pull) + f60(56), E.dolly);
  const settle = (1 - prog(f, 0, f60(12), E.out)) * 13 * S.u;
  const shot = lc(A, B, pull);
  // after the pull the shot stays alive with a slow drift (translation only: a creeping scale makes
  // Chromium re-rasterise the page's text, which reads as a one-frame shimmer)
  const drift = prog(f, L(CUE.pull) + f60(56), ACT.hook.dur, E.linear) * -DRIFT * S.ut * (ACT.hook.dur - L(CUE.pull) - f60(56));
  const cam: Shot = { ...shot, sx: shot.sx + drift, sy: shot.sy + settle };

  // the page slides up under the line
  const pIn = arrive(prog(f, L(CUE.page), L(CUE.page) + f60(54), E.glide));
  const pageY = mix(S.h + 40 * S.u, page.y, pIn);

  // caret -> capsule -> bar, the words riding its edges
  const tCaret = L(CUE.caret);
  const caretH = prog(f, tCaret, tCaret + f60(6), E.out) * size * 0.86;
  const thick = prog(f, tCaret + f60(14), tCaret + f60(28), E.out);
  const widen = prog(f, L(CUE.widen), L(CUE.type), E.rest); // the short bar: formed the beat typing starts
  const slotX = chain.lineLeft[1] + chain.frags[1].left - measureTracked(' ', size, disp.weight, disp.track) / 2;
  const capW = mix(3 * S.u, 36 * S.u, thick);
  const slotW = mix(capW, bar.w, widen);
  const slotH = mix(caretH, bar.h, Math.max(thick * 0.4, widen));
  const slotCx = mix(slotX, S.cx, widen);
  const gap = 0.22 * size;
  const leftWord = copy('hook.1').text;
  const rightWord = copy('hook.2').text;
  const wL = measureTracked(leftWord, size, disp.weight, disp.track);
  const wordFade = 1 - prog(f, L(CUE.widen) + f60(8), L(CUE.widen) + f60(30), E.smooth);
  const caretOn = f >= tCaret;

  return (
    <AbsoluteFill style={{ background: C.paper, overflow: 'hidden' }}>
      <div style={camera(cam)}>
        {/* the page, behind the line */}
        <div style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${page.x}px, ${pageY}px)` }}>
          <PageShape quad={rectQuad(0, 0, page.w, page.h)} w={page.w} h={page.h} />
          <PageContent w={page.w} h={page.h} u={S.u} />
        </div>
        {!caretOn && <Chain chain="hook" frame={f} from={ACT.hook.from} role="display" size={size} x={S.cx} top={top} />}
        {caretOn && (
          <>
            <div data-text="hook.1" style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${slotCx - slotW / 2 - gap - wL}px, ${top}px)`, opacity: wordFade }}>
              <T role="display" size={size} ui={false}>{leftWord}</T>
            </div>
            <div data-text="hook.2" style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${slotCx + slotW / 2 + gap}px, ${top}px)`, opacity: wordFade }}>
              <T role="display" size={size} ui={false}>{rightWord}</T>
            </div>
            {widen <= 0 && (
              <div style={{ position: 'absolute', left: 0, top: 0, width: slotW, height: slotH, borderRadius: slotH / 2, background: C.accent, transform: `translate(${slotCx - slotW / 2}px, ${lineMid - slotH / 2}px)` }} />
            )}
            {widen > 0 && (
              <div style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${slotCx - slotW / 2}px, ${lineMid - slotH / 2}px)` }}>
                <AskBar w={slotW} h={slotH} u={S.u} f={f} typeFrom={L(CUE.type)} o={prog(f, L(CUE.widen) + f60(14), L(CUE.type), E.smooth)} />
              </div>
            )}
          </>
        )}
      </div>
    </AbsoluteFill>
  );
};

export const HOOK_END_SHOT = (S: Stage): Shot => ({ ax: S.cx, ay: hookLayout(S).lineMid, sx: S.cx - DRIFT * S.ut * (ACT.hook.dur - L(CUE.pull) - f60(56)), sy: hookLayout(S).lineMid, k: 1 });
