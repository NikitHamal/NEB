import React from 'react';
import { AbsoluteFill, getStaticFiles, Html5Audio, Sequence, staticFile } from 'remotion';
import { Ask } from './acts/Ask';
import { Hook } from './acts/Hook';
import { Learn } from './acts/Learn';
import { Lockup } from './acts/Lockup';
import { Pass } from './acts/Pass';
import { PassOn } from './acts/PassOn';
import { Reader } from './acts/Reader';
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
  ['hook', Hook, '1 Hook'],
  ['ask', Ask, '2 Ask'],
  ['learn', Learn, '3 Learn'],
  ['reader', Reader, '4 Reader'],
  ['pass', Pass, '5 Pass'],
  ['passon', PassOn, '6 Pass on'],
  ['lockup', Lockup, '7 Lockup'],
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
