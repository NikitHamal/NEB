import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C } from '../brand/tokens';
import { ANSWER_INDEX, QUESTION, REPLIES } from '../data';
import { E, hitPulse, mix, prog } from '../lib/anim';
import { camera, lc } from '../lib/camera';
import { ACT, CUE, f60 } from '../timeline';
import { Avatar, Card, Check, Chip, mixQuad, PageShape, rectQuad, SHADOW, T } from '../ui/kit';
import { type Stage, useStage } from '../ui/stage';
import { AskBar, HOOK_END_SHOT, hookLayout, PageContent } from './Hook';

// ACT 2 - ask. "Ask" is pressed; the bar becomes the post and the page becomes its header, and the
// card glides into the feed. Replies bloom beside it, one per
// beat; the teacher's is marked as the answer in the accent. Then the whole forum tips back like a
// sheet laid on a table and sinks into the blue stage Act 3 opens on.

const L = (abs: number) => abs - ACT.ask.from;
const REPLY_AT = [CUE.reply1, CUE.reply2, CUE.reply3].map(L);

const layout = (S: Stage) => {
  const u = S.u;
  if (S.portrait) {
    const card = { x: S.band.x, y: S.band.y + 10 * u, w: S.band.w, h: 400 * u };
    const col = { x: S.band.x, y: card.y + card.h + 34 * u, w: S.band.w, rowH: 150 * u, gap: 22 * u };
    return { card, col };
  }
  const cardW = S.square ? S.band.w : Math.min(S.band.w * 0.5, 860 * u);
  const card = S.square
    ? { x: S.band.x, y: S.band.y + 20 * u, w: cardW, h: 360 * u }
    : { x: S.band.x + S.band.w * 0.02, y: S.cy - 210 * u, w: cardW, h: 420 * u };
  const col = S.square
    ? { x: S.band.x, y: card.y + card.h + 28 * u, w: S.band.w, rowH: 130 * u, gap: 16 * u }
    : { x: card.x + card.w + 56 * u, y: S.cy - 260 * u, w: S.band.x + S.band.w - (card.x + card.w + 56 * u), rowH: 150 * u, gap: 26 * u };
  return { card, col };
};

export const Ask: React.FC = () => {
  const f = useCurrentFrame();
  const S = useStage();
  const u = S.u;
  const H = hookLayout(S);
  const { card, col } = layout(S);

  // the camera settles from the hook's creep back to rest
  const cam = lc(HOOK_END_SHOT(S), { ax: S.cx, ay: H.lineMid, sx: S.cx, sy: H.lineMid, k: 1 }, prog(f, 0, f60(40), E.cam));

  // the bar becomes the card; the page becomes its header band
  const press = hitPulse(f - 0);
  const morph = prog(f, f60(4), L(CUE.land), E.glide);
  const bx = mix(H.bar.x, card.x, morph);
  const by = mix(H.bar.y, card.y, morph);
  const bw = mix(H.bar.w, card.w, morph);
  const bh = mix(H.bar.h, card.h, morph);
  const br = mix(H.bar.h / 2, 26 * u, morph);
  const band = 84 * u;
  const pageQuad = mixQuad(rectQuad(H.page.x, H.page.y, H.page.w, H.page.h), rectQuad(bx, by, bw, band), morph);
  const content = prog(f, L(CUE.land) - f60(6), L(CUE.land) + f60(18), E.out);
  const barFade = 1 - prog(f, f60(2), f60(16), E.smooth);

  const landed = REPLY_AT.filter((t) => f >= t + f60(10)).length;
  const answered = prog(f, L(CUE.answered), L(CUE.answered) + f60(14), E.out);
  const answerPulse = hitPulse(f - L(CUE.answered) - 2);

  // tip-back into the blue stage
  const tip = prog(f, L(CUE.tip), L(CUE.tip) + f60(36), E.smooth);
  const dim = prog(f, L(CUE.tip) + f60(22), L(CUE.tip) + f60(36), E.smooth);

  return (
    <AbsoluteFill style={{ background: C.accent, overflow: 'hidden' }}>
      <AbsoluteFill style={{ background: C.paper, transformOrigin: '50% 100%', transform: `perspective(${1200 * u}px) translateY(${tip * 10}%) rotateX(${tip * 40}deg)` }}>
        <div style={camera(cam)}>
          {/* the morphing body: the bar, then the card */}
          <div style={{ position: 'absolute', left: 0, top: 0, width: bw, height: bh, borderRadius: br, background: C.white, boxShadow: SHADOW, transform: `translate(${bx}px, ${by}px)`, overflow: 'hidden' }}>
            <div style={{ opacity: barFade }}>
              <AskBar w={H.bar.w} h={H.bar.h} u={u} f={f + ACT.ask.from - ACT.hook.from} typeFrom={L(CUE.type) + ACT.ask.from - ACT.hook.from} press={press} />
            </div>
          </div>
          <PageShape quad={pageQuad} w={S.w} h={S.h} />
          {morph < 0.5 && (
            <div style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${H.page.x}px, ${mix(H.page.y, by, morph)}px)` }}>
              <PageContent w={H.page.w} h={H.page.h} u={u} o={1 - prog(f, 0, f60(14), E.smooth)} />
            </div>
          )}
          {/* the post */}
          <div style={{ position: 'absolute', left: 0, top: 0, width: card.w, height: card.h, transform: `translate(${card.x}px, ${by}px)`, opacity: content }}>
            <div style={{ position: 'absolute', left: 32 * u, top: (band - 44 * u) / 2 }}>
              <Chip size={22 * u} tone="white">{QUESTION.subject}</Chip>
            </div>
            <div style={{ position: 'absolute', left: 36 * u, top: band + 30 * u, right: 36 * u, display: 'flex', alignItems: 'center', gap: 16 * u }}>
              <Avatar initial={QUESTION.initial} size={56 * u} />
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <T role="ui" size={26 * u} style={{ fontWeight: 600 }}>{QUESTION.author}</T>
                <T role="ui" size={22 * u} color={C.mute}>{`${QUESTION.klass} · just now`}</T>
              </div>
            </div>
            <div style={{ position: 'absolute', left: 36 * u, right: 36 * u, top: band + 120 * u }}>
              <T role="title" size={(S.portrait ? 36 : 34) * u} style={{ whiteSpace: 'normal' }}>{QUESTION.text}</T>
            </div>
            <div style={{ position: 'absolute', left: 36 * u, bottom: 30 * u, display: 'flex', alignItems: 'center', gap: 12 * u }}>
              <T role="ui" size={24 * u} color={landed ? C.accent : C.mute} style={{ fontWeight: 600 }}>{`${landed} ${landed === 1 ? 'reply' : 'replies'}`}</T>
            </div>
          </div>
          {/* replies bloom beside it */}
          {REPLIES.map((r, i) => {
            const t = REPLY_AT[i];
            const p = prog(f, t, t + f60(22), E.out);
            if (p <= 0) return null;
            const isAnswer = i === ANSWER_INDEX;
            const a = isAnswer ? answered : 0;
            const y = col.y + i * (col.rowH + col.gap) + (1 - p) * 24 * u;
            return (
              <div key={r.name} style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${col.x}px, ${y}px) scale(${(0.94 + 0.06 * p) * (1 + 0.02 * (isAnswer ? answerPulse : 0))})`, transformOrigin: '0 50%', opacity: p }}>
                <Card w={col.w} h={col.rowH} r={22 * u} pad={24 * u} style={{ boxShadow: `inset ${8 * u * a}px 0 0 ${C.accent}, ${SHADOW}` }}>
                  <div style={{ display: 'flex', gap: 18 * u, alignItems: 'flex-start' }}>
                    <Avatar initial={r.initial} size={50 * u} tone={isAnswer ? 'ink' : 'mist'} />
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 6 * u, minWidth: 0, flex: 1 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 12 * u }}>
                        <T role="ui" size={24 * u} style={{ fontWeight: 600 }}>{r.name}</T>
                        <T role="ui" size={22 * u} color={C.mute}>{r.role}</T>
                        {isAnswer && a > 0 && (
                          <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 6 * u, height: 40 * u, padding: `0 ${16 * u}px 0 ${10 * u}px`, borderRadius: 20 * u, background: C.accent, opacity: a }}>
                            <Check size={26 * u} p={a} />
                            <T role="ui" size={22 * u} color={C.white} style={{ fontWeight: 600 }}>Answer</T>
                          </div>
                        )}
                      </div>
                      <T role="ui" size={25 * u} style={{ whiteSpace: 'normal' }}>{r.text}</T>
                    </div>
                  </div>
                </Card>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: C.accent, opacity: dim * 0.9, pointerEvents: 'none' }} />
    </AbsoluteFill>
  );
};
