import React, { useEffect, useState } from 'react';
import { staticFile, useDelayRender } from 'remotion';

// Neby, played back from frames baked by tools/bake-neby.mjs (the product's own avatar engine).
// The JSON is fetched once per tab and the render waits for it, so no frame ever shows a gap.
let cache: string[] | null = null;
let pending: Promise<string[]> | null = null;

export const useNebyFrames = (): string[] | null => {
  const { delayRender, continueRender, cancelRender } = useDelayRender();
  const [frames, setFrames] = useState<string[] | null>(cache);
  const [handle] = useState(() => (cache ? null : delayRender('Neby frames')));
  useEffect(() => {
    if (cache || handle === null) return;
    pending ??= fetch(staticFile('neby/reader.json')).then((r) => r.json() as Promise<string[]>);
    pending
      .then((d) => {
        cache = d.map((svg) => svg.replace('<svg ', '<svg width="100%" height="100%" '));
        setFrames(cache);
        continueRender(handle);
      })
      .catch((e) => cancelRender(e));
  }, [handle, continueRender, cancelRender]);
  return frames;
};

export const Neby: React.FC<{ frames: string[]; i: number; size: number }> = ({ frames, i, size }) => (
  <div style={{ width: size, height: size }} dangerouslySetInnerHTML={{ __html: frames[Math.max(0, Math.min(frames.length - 1, Math.round(i)))] }} />
);
