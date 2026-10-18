import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C, TYPE } from '../brand/tokens';
import { GPA, GRADES, HERO_GRADE, QUESTION } from '../data';
import { Words } from '../fx/Words';
import { E, fd, hitPulse, prog } from '../lib/anim';
import { breath, camera, lc, type Shot } from '../lib/camera';
import { ACT, copy, CUE, f60 } from '../timeline';
import { Card, PageShape, rectQuad, T } from '../ui/kit';
import { useStage } from '../ui/stage';

// ACT 5 - pass. Back on paper, in close-up: one bar grows, Chemistry, the subject the film was
// stuck on, and lands on A+. "Pass it." Then the camera pulls back to the whole gradesheet (the
// page again, as its header) and the GPA rolls in and locks.

const L = (abs: number) => abs - ACT.pass.from;

export const Pass: React.FC = () => {
  const f = useCurrentFrame();
  const S = useStage();
  const u = S.u;

  const cardW = S.portrait ? S.band.w : S.square ? S.band.w : Math.min(S.band.w * 0.58, 1020 * u);
  const cardH = (S.portrait ? 640 : S.square ? 560 : 640) * u;
  const card = S.portrait || S.square ? { x: S.cx - cardW / 2, y: S.band.y + S.band.h - cardH - (S.portrait ? 40 : 0) * u } : { x: S.band.x + S.band.w - cardW, y: S.cy - cardH / 2 };
  const head = 104 * u;
  const chart = { x: card.x + 44 * u, y: card.y + head + 70 * u, w: cardW - 88 * u, h: cardH - head - 160 * u };
  const n = GRADES.length;
  const slotW = chart.w / n;
  const barW = slotW * 0.5;
  const barX = (i: number) => chart.x + i * slotW + (slotW - barW) / 2;
  const barH = (gp: number) => (gp / 4) * chart.h;
  const heroTop = chart.y + chart.h - barH(GRADES[HERO_GRADE].gp);

  // close-up on the hero bar, then pull back to the sheet
  const A: Shot = { ax: barX(HERO_GRADE) + barW / 2, ay: heroTop + chart.h * 0.3, sx: S.portrait ? S.cx : S.w * 0.62, sy: S.cy, k: 2.8 };
  const B: Shot = { ax: S.cx, ay: S.cy, sx: S.cx, sy: S.cy, k: 1 };
  const pull = prog(f, L(CUE.pullback), L(CUE.pullback) + f60(60), E.cam);
  // the close-up is alive: a slow push and a rise while the bar holds
  const live = prog(f, 0, L(CUE.pullback) + f60(30), E.linear);
  const shot = lc({ ...A, sy: A.sy + live * 46 * u }, B, pull);
  const cam: Shot = { ...shot, k: shot.k * breath(live, 0.09) * breath(prog(f, L(CUE.pullback), ACT.pass.dur, E.linear), 0.03) };
  const header = prog(f, L(CUE.pullback), L(CUE.pullback) + f60(40), E.smooth);
  // the sheet lifts away before the cut, so both sides of the seam are empty paper
  const leave = prog(f, ACT.pass.dur - f60(30), ACT.pass.dur, E.exit);

  const grow = prog(f, L(CUE.bar), L(CUE.bar) + f60(60), E.out);
  const plus = prog(f, L(CUE.bar) + f60(50), L(CUE.bar) + f60(62), E.out);
  const gpaP = prog(f, L(CUE.gpa), L(CUE.gpaLock), E.out);
  const gpa = (Math.round(fd(gpaP * GPA * 100)) / 100).toFixed(2);
  const lock = hitPulse(f - L(CUE.gpaLock) - 2);
  const locked = f >= L(CUE.gpaLock);

  const c = copy('pass');
  const size = TYPE.display.size * S.ut;
  const textPos = S.portrait || S.square ? { x: S.band.x, y: S.band.y + (S.portrait ? 20 : 0) * u } : { x: S.band.x, y: S.cy - size * 0.55 };

  return (
    <AbsoluteFill style={{ background: C.paper, overflow: 'hidden' }}>
      <div style={camera(cam)}>
        <div style={{ opacity: 1 - leave, transform: `translateY(${-leave * 90 * u}px)` }}>
        <Card w={cardW} h={cardH} r={28 * u} pad={0} style={{ transform: `translate(${card.x}px, ${card.y}px)` }}>
          <div style={{ opacity: header }}><PageShape quad={rectQuad(0, 0, cardW, head)} w={cardW} h={cardH} /></div>
          <div style={{ position: 'absolute', left: 36 * u, top: 0, height: head, display: 'flex', flexDirection: 'column', justifyContent: 'center', opacity: header }}>
            <T role="title" size={30 * u}>Gradesheet</T>
            <T role="ui" size={22 * u} color={C.ink}>{QUESTION.klass}</T>
          </div>
          <div style={{ position: 'absolute', right: 36 * u, top: 0, height: head, display: 'flex', alignItems: 'center', gap: 14 * u, opacity: header }}>
            <T role="ui" size={24 * u}>GPA</T>
            <div style={{ transform: `scale(${1 + 0.06 * lock})`, transformOrigin: '100% 50%' }}>
              <T role="title" size={44 * u} color={locked ? C.accent : C.ink} style={{ fontWeight: 700 }}>{gpa}</T>
            </div>
          </div>
        </Card>
        {GRADES.map((g, i) => {
          const hero = i === HERO_GRADE;
          const h = barH(g.gp) * (hero ? grow : 1);
          // the rest of the sheet only joins as the camera pulls back, so the close-up reads alone
          const others = hero ? 1 : prog(f, L(CUE.pullback), L(CUE.pullback) + f60(40), E.smooth);
          return (
            <div key={g.subject} style={{ opacity: others }}>
              <div style={{ position: 'absolute', left: 0, top: 0, width: barW, height: h, borderRadius: `${10 * u}px ${10 * u}px 0 0`, background: hero ? C.accent : C.sky, transform: `translate(${barX(i)}px, ${chart.y + chart.h - h}px)` }} />
              <div style={{ position: 'absolute', left: 0, top: 0, width: slotW, textAlign: 'center', transform: `translate(${chart.x + i * slotW}px, ${chart.y + chart.h - h - 40 * u}px)`, opacity: hero ? plus : 1 }}>
                <T role="ui" size={(hero ? 26 : 22) * u} color={hero ? C.accent : C.ink} style={{ fontWeight: 700 }}>{g.grade}</T>
              </div>
              <div style={{ position: 'absolute', left: 0, top: 0, width: slotW, textAlign: 'center', transform: `translate(${chart.x + i * slotW}px, ${chart.y + chart.h + 16 * u}px)` }}>
                <T role="ui" size={22 * u} color={hero ? C.ink : C.mute} style={{ fontWeight: hero ? 600 : 500 }}>{g.subject}</T>
              </div>
            </div>
          );
        })}
        </div>
      </div>
      <div style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${textPos.x}px, ${textPos.y}px)` }}>
        <Words id="pass" text={c.text} frame={f} start={c.in - ACT.pass.from} out={c.out - ACT.pass.from} size={size} style={{ fontFamily: '"Poppins"', fontSize: size, fontWeight: TYPE.display.weight, letterSpacing: `${TYPE.display.track}em`, lineHeight: TYPE.display.lead, color: C.ink }} />
      </div>
    </AbsoluteFill>
  );
};
