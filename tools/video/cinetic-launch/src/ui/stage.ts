import { useVideoConfig } from 'remotion';
import { safeInsets } from '../lib/safe';

/**
 * The frame an act lays out in, whatever the aspect: 16:9 master, 9:16 feeds, 1:1 posts. `u` scales
 * sizes with the short side (1 at 1080); `safe` is the frame's safe zone (feed zones in 9:16);
 * `band` is the clear area inside it, where the visual mass belongs.
 */
export const useStage = () => {
  const { width: w, height: h } = useVideoConfig();
  const ut = Math.min(w, h) / 1080; // type: statements keep their sizes

  const safe = safeInsets(undefined, w, h);
  const portrait = h > w * 1.2;
  const square = !portrait && w < h * 1.2;
  // product UI is framed large, so it reads on a phone and fills the frame (cinetic: hero 40-70%)
  const u = ut * (portrait ? 1.15 : square ? 1.1 : 1.25);
  const band = { x: safe.left, y: safe.top, w: w - safe.left - safe.right, h: h - safe.top - safe.bottom };
  return { w, h, u, ut, safe, portrait, square, wide: !portrait && !square, band, cx: band.x + band.w / 2, cy: band.y + band.h / 2 };
};
export type Stage = ReturnType<typeof useStage>;
