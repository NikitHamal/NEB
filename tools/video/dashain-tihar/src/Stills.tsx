import React from 'react';
import { AbsoluteFill } from 'remotion';
import { Mark } from './brand/Mark';
import { C, U } from './brand/tokens';
import { FontGate } from './lib/FontGate';

// Style stills: the supplied mark at 16 px and at full size, on paper and on ink.
export const MarkStill: React.FC<{ size: number; surface: 'paper' | 'ink' }> = ({ size, surface }) => (
  <FontGate>
    <AbsoluteFill style={{ background: surface === 'ink' ? C.ink : C.paper, alignItems: 'center', justifyContent: 'center' }}>
      <Mark size={size} id={`s${size}`} />
    </AbsoluteFill>
  </FontGate>
);

export const MarkSizes: React.FC = () => (
  <FontGate>
    <AbsoluteFill style={{ background: C.paper, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 80 * U }}>
      {[16, 32, 64, 160, 480].map((s) => <Mark key={s} size={s * U} id={`z${s}`} />)}
    </AbsoluteFill>
  </FontGate>
);
