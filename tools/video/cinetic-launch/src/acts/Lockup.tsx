import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { MARK, Mark, type Facet } from '../brand/Mark';
import { C, TYPE } from '../brand/tokens';
import { URL } from '../data';
import { Words } from '../fx/Words';
import { E, mix, prog } from '../lib/anim';
import { measureTracked } from '../lib/measure';
import { ACT, copy, CUE, f60 } from '../timeline';
import { mixQuad, PageShape, type Quad, rectQuad, T } from '../ui/kit';
import { useStage } from '../ui/stage';
import { PassOn, passOnLayout } from './PassOn';

// ACT 7 - the lockup. "Study mates." leaves; the file's page lifts off and, in one move, becomes the
// logo's light facet and docks. The rest of the N assembles round it. The mark slides aside and the
// name follows out from behind it (stacked in 9:16); after the name is read, one line says what
// NEBians is, and the address. A slow creep keeps the held card alive.

const L = (abs: number) => abs - ACT.lockup.from;
const LIGHT: Quad = [[306, 320], [307, 377], [613, 706], [613, 485]];
const ASSEMBLE: { k: Facet; dy: number; at: number }[] = [
  { k: 'front', dy: 90, at: 0 },
  { k: 'back', dy: -110, at: 8 },
  { k: 'inner', dy: -80, at: 16 },
  { k: 'shade', dy: 0, at: 28 },
];

export const Lockup: React.FC = () => {
  const f = useCurrentFrame();
  const S = useStage();
  const u = S.u;
  const P = passOnLayout(S);

  // lockup geometry
  const markH = (S.portrait ? 320 : S.square ? 260 : 330) * S.ut;
  const k = markH / MARK.h;
  const markW = MARK.w * k;
  const nameSize = (S.portrait ? 150 : S.square ? 130 : 170) * S.ut;
  const nameW = measureTracked('NEBians', nameSize, TYPE.display.weight, TYPE.display.track);
  const gap = 64 * S.ut;
  const creep = 1 + 0.03 * prog(f, L(CUE.name), ACT.lockup.dur, E.linear);
  // where the mark sits: alone in the centre, then aside (16:9, 1:1) or above (9:16) the name
  const alone = { x: S.cx - markW / 2, y: S.cy - markH / 2 - (S.portrait ? 60 : 30) * u };
  const final = S.portrait
    ? { x: S.cx - markW / 2, y: S.cy - (markH + nameSize * 1.1) / 2 - 60 * u }
    : { x: S.cx - (markW + gap + nameW) / 2, y: S.cy - markH / 2 - 50 * u };
  const slide = prog(f, L(CUE.name), L(CUE.name) + f60(44), E.inOut);
  const mx = mix(alone.x, final.x, slide);
  const my = mix(alone.y, final.y, slide);
  const toScreen = ([x, y]: [number, number]): [number, number] => [mx + (x - MARK.x) * k, my + (y - MARK.y) * k];

  // the page: from the file's page to the light facet
  const lift = prog(f, L(CUE.lift), L(CUE.dock), E.smooth); // cubic: peaks at ~1.5x its mean speed, so the flight blurs cleanly
  const pageRect = rectQuad(P.file.x, P.file.y, P.file.h * 0.62, P.file.h);
  const facet = LIGHT.map(toScreen) as Quad;
  const docked = f >= L(CUE.dock);

  // the rest of the N
  const pose: Partial<Record<Facet, { y: number; o: number }>> = {};
  for (const a of ASSEMBLE) {
    const t = prog(f, L(CUE.dock) + a.at, L(CUE.dock) + a.at + f60(40), E.out);
    pose[a.k] = { y: a.dy * (1 - t), o: prog(f, L(CUE.dock) + a.at, L(CUE.dock) + a.at + f60(14), E.smooth) };
  }
  pose.light = { y: 0, o: docked ? 1 : 0 };

  // the name follows the mark out from behind it
  const name = prog(f, L(CUE.name) + f60(10), L(CUE.name) + f60(50), E.out);
  // the name rides the mark's right edge, so it follows the slide instead of waiting at its end
  const nameX = S.portrait ? S.cx - nameW / 2 : mx + markW + gap;
  const nameY = S.portrait ? final.y + markH + 40 * u : S.cy - nameSize * 0.62 - 50 * u;
  const nameShift = S.portrait ? { x: 0, y: (1 - name) * -40 * u } : { x: (1 - name) * -60 * u, y: 0 };

  const end = copy('endline');
  const endSize = TYPE.secondary.size * S.ut;
  const endW = measureTracked(end.text, endSize, TYPE.secondary.weight, TYPE.secondary.track);
  const endY = (S.portrait ? nameY + nameSize * 1.25 : final.y + markH + 70 * u);
  const url = prog(f, copy('url').in - ACT.lockup.from, copy('url').resolved - ACT.lockup.from, E.out);


  return (
    <AbsoluteFill style={{ background: C.paper, overflow: 'hidden' }}>
      {/* the upload scene carries on under the lift and fades, its line leaving as the page goes */}
      <AbsoluteFill style={{ opacity: 1 - prog(f, f60(6), f60(30), E.smooth) }}>
        <PassOn frame={ACT.passon.dur + f} out={ACT.passon.dur} />
      </AbsoluteFill>
      <div style={{ position: 'absolute', inset: 0, transformOrigin: `${S.cx}px ${S.cy}px`, transform: `scale(${creep})` }}>
        <div style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${mx}px, ${my}px)` }}>
          <Mark size={markH} id="lock" pose={Object.fromEntries(Object.entries(pose).map(([key, v]) => [key, { y: v!.y, o: v!.o }]))} />
        </div>
        {!docked && <PageShape quad={mixQuad(pageRect, facet, lift)} w={S.w} h={S.h} fill={C.sky} edge={lift * 13 * k} />}
        <div style={{ position: 'absolute', left: 0, top: 0, overflow: 'hidden', transform: `translate(${nameX}px, ${nameY}px)` }}>
          <div data-text="wordmark" style={{ transform: `translate(${nameShift.x}px, ${nameShift.y}px)`, opacity: name }}>
            <T role="display" size={nameSize} ui={false} style={{ fontWeight: 700 }}>NEBians</T>
          </div>
        </div>
      </div>
      {/* the line and the address sit outside the creep: scaled small text re-rasterises and shimmers */}
        <div style={{ position: 'absolute', left: 0, top: 0, transform: `translate(${S.cx - endW / 2}px, ${endY}px)` }}>
          <Words id="endline" text={end.text} frame={f} start={end.in - ACT.lockup.from} size={endSize} style={{ fontFamily: '"Poppins"', fontSize: endSize, fontWeight: TYPE.secondary.weight, letterSpacing: `${TYPE.secondary.track}em`, lineHeight: TYPE.secondary.lead, color: C.ink }} />
        </div>
        <div style={{ position: 'absolute', left: 0, top: 0, width: S.w, textAlign: 'center', transform: `translate(0px, ${endY + endSize * 1.6 + (1 - url) * 10 * u}px)`, opacity: url }}>
          <T role="ui" size={30 * u} color={C.accent} style={{ fontWeight: 600 }}>{URL}</T>
        </div>
    </AbsoluteFill>
  );
};
