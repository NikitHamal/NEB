import React from 'react';
import { Composition, Folder, Still } from 'remotion';
import { C, U } from './brand/tokens';
import { ACTS, Film, FilmProps } from './Film';
import { FilmSub, subMetadata } from './FilmSub';
import { Audit } from './lib/Audit';
import { FontGate } from './lib/FontGate';
import { MarkSizes, MarkStill } from './Stills';
import { ACT, FPS, H, TOTAL, W } from './timeline';

// An act on its own, font-gated like the film, so it can be iterated without scrubbing the film.
const solo = (Act: React.FC) => {
  const Solo: React.FC<FilmProps> = ({ audit = false, safe }) => (
    <FontGate>
      <div style={{ position: 'absolute', inset: 0, background: C.paper }}>
        <Act />
        {audit && <Audit safe={safe} />}
      </div>
    </FontGate>
  );
  return Solo;
};

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Film" component={Film} durationInFrames={TOTAL} fps={FPS} width={W} height={H} defaultProps={{ audit: false } as FilmProps} />
    <Composition id="FilmSub" component={FilmSub} durationInFrames={TOTAL} fps={FPS} width={W} height={H} defaultProps={{ groups: [] as number[] }} calculateMetadata={subMetadata} />
    {/* social re-layouts from the same timeline: every act lays out from the frame it is given */}
    <Composition id="Film9x16" component={Film} durationInFrames={TOTAL} fps={FPS} width={1080} height={1920} defaultProps={{ audit: false } as FilmProps} />
    <Composition id="Film1x1" component={Film} durationInFrames={TOTAL} fps={FPS} width={1080} height={1080} defaultProps={{ audit: false } as FilmProps} />
    <Folder name="Acts">
      {ACTS.map(([key, Act], i) => (
        <Composition key={key} id={`Act${i + 1}`} component={solo(Act)} durationInFrames={ACT[key].dur} fps={FPS} width={W} height={H} defaultProps={{ audit: false } as FilmProps} />
      ))}
      {ACTS.map(([key, Act], i) => (
        <Composition key={`v${key}`} id={`Act${i + 1}v`} component={solo(Act)} durationInFrames={ACT[key].dur} fps={FPS} width={1080} height={1920} defaultProps={{ audit: false } as FilmProps} />
      ))}
    </Folder>
    <Folder name="Stills">
      <Still id="Mark16" component={MarkStill} width={16} height={16} defaultProps={{ size: 16, surface: 'paper' as const }} />
      <Still id="MarkLarge" component={MarkStill} width={W} height={H} defaultProps={{ size: 640 * U, surface: 'paper' as const }} />
      <Still id="MarkSizes" component={MarkSizes} width={W} height={H} />
    </Folder>
  </>
);
