import React, { useLayoutEffect, useRef } from 'react';
import { Px } from './canvas';

/**
 * One pixel-art scene: [draw] paints a w x h buffer for this frame, and the canvas shows it
 * scaled up by a whole number with no smoothing, so every art pixel is a crisp square.
 */
export const PixelLayer: React.FC<{ w: number; h: number; scale: number; draw: (px: Px) => void; frame: number; style?: React.CSSProperties }> = ({ w, h, scale, draw, frame, style }) => {
  const ref = useRef<HTMLCanvasElement>(null);
  useLayoutEffect(() => {
    const cv = ref.current;
    if (!cv) return;
    const ctx = cv.getContext('2d');
    if (!ctx) return;
    const px = new Px(w, h);
    draw(px);
    const img = new ImageData(new Uint8ClampedArray(px.data.buffer as ArrayBuffer), w, h);
    ctx.putImageData(img, 0, 0);
  }, [w, h, draw, frame]);
  return <canvas ref={ref} width={w} height={h} style={{ position: 'absolute', left: 0, top: 0, width: w * scale, height: h * scale, imageRendering: 'pixelated', ...style }} />;
};
