import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C, TYPE } from '../brand/tokens';
import { QUESTION, UPLOAD } from '../data';
import { Words } from '../fx/Words';
import { E, fd, hitPulse, mix, prog } from '../lib/anim';
import { measureTracked } from '../lib/measure';
import { ACT, copy, CUE, f60 } from '../timeline';
import { Card, Check, PageShape, rectQuad, T } from '../ui/kit';
import { type Stage, useStage } from '../ui/stage';

// ACT 6 - pass it on. The student who asked uploads her notes: the page again, now a file. A
// progress spine walks it through Uploaded, Checked by a moderator, Published (the accent), and a
// counter climbs as other students read it. Then the line the whole film was heading for.

const L = (abs: number) => abs - ACT.passon.from;
const STEP_AT = [CUE.upload, CUE.checked, CUE.published, CUE.readers].map(L);

/** Where the file's page sits at the end of the act; the lockup lifts it from here. */
export const passOnLayout = (S: Stage) => {
  const u = S.u;
  const textSize = TYPE.display.size * S.ut * (S.portrait ? 0.95 : 1);
  if (S.portrait) {
    const file = { x: S.band.x, y: S.band.y + textSize * 1.5, w: S.band.w, h: 210 * u };
    const spine = { x: S.band.x + 30 * u, y: file.y + file.h + 70 * u, pitch: 130 * u };
    return { file, spine, textSize, text: { x: S.band.x, y: S.band.y } };
  }
  const fileW = (S.square ? 420 : 540) * u;
  const file = { x: S.square ? S.band.x : S.band.x + S.band.w * 0.04, y: S.cy - 60 * u, w: fileW, h: (S.square ? 230 : 280) * u };
  const spine = { x: file.x + fileW + (S.square ? 70 : 140) * u, y: S.cy - (S.square ? 40 : 110) * u, pitch: (S.square ? 100 : 120) * u };
  const text = { x: S.band.x + (S.square ? 0 : S.band.w * 0.04), y: S.band.y + (S.square ? 20 : 40) * u };
  return { file, spine, textSize, text };
};

/** `out`: frame (act-local) the line starts to leave; the lockup replays the act's last frame with it. */
export const PassOn: React.FC<{ frame?: number; out?: number }> = (o) => {
  const current = useCurrentFrame();
  const f = o.frame ?? current;
  const S = useStage();
  const u = S.u;
  const { file, spine, textSize, text } = passOnLayout(S);

  const enter = prog(f, 0, f60(30), E.out);
  const rowY = (i: number) => spine.y + i * spine.pitch;
  // the head moves between steps on E.rest, arriving on each step's cue
  let headY = rowY(0);
  for (let i = 1; i < STEP_AT.length; i++) headY = mix(headY, rowY(i), prog(f, STEP_AT[i] - f60(26), STEP_AT[i], E.rest));
  // a rolling counter updates at most 12 times a second, so each value can be seen (fx/Roll thinSteps)
  const fStep = Math.floor(fd(f) / 5) * 5;
  const readers = Math.round(prog(fStep, STEP_AT[3] + f60(4), STEP_AT[3] + f60(52), E.out) * UPLOAD.readers);
  const pub = hitPulse(f - STEP_AT[2] - 2);

  const labels = [...UPLOAD.steps, `Read by ${readers.toLocaleString('en-US')} students`];
  const c = copy('passon');
  const textW = measureTracked(c.text, textSize, TYPE.display.weight, TYPE.display.track);

  return (
    <AbsoluteFill style={{ background: C.paper, overflow: 'hidden' }}>
      <div style={{ position: 'absolute', inset: 0, transformOrigin: `${S.cx}px ${S.cy}px`, transform: `scale(${1 + 0.035 * prog(f, 0, ACT.passon.dur, E.linear)})` }}>
      {/* the file */}
      <div style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${file.x}px, ${file.y + (1 - enter) * 40 * u}px)`, opacity: enter }}>
        <Card w={file.w} h={file.h} r={26 * u} pad={0}>
          <PageShape quad={rectQuad(0, 0, file.h * 0.62, file.h)} w={file.w} h={file.h} />
          <div style={{ position: 'absolute', left: file.h * 0.62 + 30 * u, top: 0, bottom: 0, right: 24 * u, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 8 * u }}>
            <T role="title" size={(S.square ? 22 : 30) * u}>{UPLOAD.file}</T>
            <T role="ui" size={(S.square ? 18 : 22) * u} color={C.mute}>{`${UPLOAD.by} · ${QUESTION.subject} · ${QUESTION.klass}`}</T>
          </div>
        </Card>
      </div>
      {/* the spine */}
      <div style={{ position: 'absolute', left: 0, top: 0, width: 3 * u, height: rowY(3) - rowY(0), background: C.line, transform: `translate(${spine.x - 1.5 * u}px, ${rowY(0)}px)` }} />
      <div style={{ position: 'absolute', left: 0, top: 0, width: 3 * u, height: headY - rowY(0), background: C.ink, transform: `translate(${spine.x - 1.5 * u}px, ${rowY(0)}px)` }} />
      {labels.map((label, i) => {
        const at = STEP_AT[i];
        const p = prog(f, at - f60(4), at + f60(14), E.out);
        if (p <= 0) return null;
        const done = prog(f, at + f60(10), at + f60(18), E.out);
        const accent = i === 2;
        const dot = 40 * u;
        return (
          <div key={i} style={{ position: 'absolute', left: 0, top: 0, display: 'flex', alignItems: 'center', gap: 24 * u, transform: `translate(${spine.x - dot / 2}px, ${rowY(i) - dot / 2 + (1 - p) * 14 * u}px)`, opacity: p }}>
            <div style={{ width: dot, height: dot, borderRadius: dot / 2, background: accent ? C.accent : i === 3 ? C.sky : C.ink, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${1 + (accent ? 0.12 * pub : 0)})` }}>
              {i < 3 && <Check size={dot * 0.7} p={done} />}
            </div>
            <T role="title" size={(S.square ? 26 : 30) * u} color={accent ? C.accent : C.ink}>{label}</T>
          </div>
        );
      })}
      {/* the head of the spine */}
      <div style={{ position: 'absolute', left: 0, top: 0, width: 12 * u, height: 12 * u, borderRadius: 6 * u, background: C.ink, transform: `translate(${spine.x - 6 * u}px, ${headY - 6 * u}px)`, opacity: f < STEP_AT[3] + f60(20) ? 1 : 0 }} />
      <div style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${S.portrait ? S.cx - textW / 2 : text.x}px, ${text.y}px)` }}>
        <Words id="passon" text={c.text} frame={f} start={c.in - ACT.passon.from} out={o.out} size={textSize} style={{ fontFamily: '"Poppins"', fontSize: textSize, fontWeight: TYPE.display.weight, letterSpacing: `${TYPE.display.track}em`, lineHeight: TYPE.display.lead, color: C.ink }} />
      </div>
      </div>
    </AbsoluteFill>
  );
};
