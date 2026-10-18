import React from 'react';
import { AbsoluteFill, getStaticFiles, Html5Audio, Sequence, staticFile } from 'remotion';
import { Card, Dawn, Kites, Study, Tihar, Tika, Turn } from './acts/Scenes';
import { C } from './brand/tokens';
import { Audit } from './lib/Audit';
import { FontGate } from './lib/FontGate';
import type { SafeSpec } from './lib/safe';
import { ACT } from './timeline';

/** Written by `npm run audio`. Renders are muted and scripts/render.sh muxes it with ffmpeg. */
export const SOUNDTRACK = 'audio/soundtrack.wav';

/** audit: draw and log the layout audit; safe: its safe zone (a lib/safe.ts preset or insets; default by aspect). */
export type FilmProps = { audit?: boolean; safe?: SafeSpec };

/** The acts in order; Root registers ActN for the Nth (scripts/layout-audit.sh relies on that order). */
export const ACTS: [keyof typeof ACT, React.FC, string][] = [
  ['dawn', Dawn, '1 Dawn'],
  ['kites', Kites, '2 Kites'],
  ['tika', Tika, '3 Tika'],
  ['turn', Turn, '4 Turn'],
  ['tihar', Tihar, '5 Tihar'],
  ['study', Study, '6 Study'],
  ['end', Card, '7 Card'],
];

// The film: one Sequence per act, handing off on exact frames; every seam is designed inside the
// acts (the next act opens on the last one's pose or stage colour), never a crossfade here.
export const Film: React.FC<FilmProps> = ({ audit = false, safe }) => {
  const hasScore = getStaticFiles().some((s) => s.name === SOUNDTRACK);
  return (
    <FontGate>
      <AbsoluteFill style={{ background: C.paper }}>
        {ACTS.map(([key, Act, name]) => (
          <Sequence key={key} from={ACT[key].from} durationInFrames={ACT[key].dur} name={name}>
            <Act />
          </Sequence>
        ))}
        {hasScore && <Html5Audio src={staticFile(SOUNDTRACK)} />}
        {audit && <Audit safe={safe} />}
      </AbsoluteFill>
    </FontGate>
  );
};
