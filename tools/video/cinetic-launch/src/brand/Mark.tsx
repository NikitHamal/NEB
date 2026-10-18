import React from 'react';
import { C } from './tokens';

// The NEBians N, from the brand's n-logo-square-icon.svg: five facets in logo units (the SVG's
// own source coordinates), each drawn with its brand gradient and pale edge, each movable on its
// own. The light facet ("light") is the film's device: the page that travels and docks here.
// // cinetic:brand-supplied logo gradients (multi-stop blues inside each facet)

export type Facet = 'back' | 'inner' | 'light' | 'front' | 'shade';

export const FACETS: Record<Facet, { d: string; grad: [string, number][]; from: [number, number]; to: [number, number]; edge: boolean }> = {
  back: { d: 'M500 42 L501 135 L856 370 L858 1287 L943 1219 L943 331 Z', grad: [[C.navy, 0], [C.navy, 0.55], [C.navyDeep, 1]], from: [505, 30], to: [960, 1290], edge: true },
  inner: { d: 'M441 191 L441 282 L691 447 L691 799 L774 886 L775 408 Z', grad: [[C.ink2, 0], [C.navyDeep, 1]], from: [435, 180], to: [780, 890], edge: true },
  light: { d: 'M306 320 L307 377 L613 706 L613 485 Z', grad: [[C.sky, 0], [C.skyDeep, 1]], from: [305, 320], to: [615, 705], edge: true },
  front: { d: 'M51 228 L51 1132 L263 1346 L267 812 L775 1353 L775 887 L691 800 L685 902 Z', grad: [[C.front, 0], [C.accent, 0.48], [C.accent, 1]], from: [40, 220], to: [800, 1350], edge: true },
  shade: { d: 'M691 800 L775 887 L775 1052 L691 958 Z', grad: [[C.navy, 0], [C.navyDeep, 1]], from: [690, 780], to: [780, 1050], edge: false },
};
export const ORDER: Facet[] = ['back', 'inner', 'light', 'front', 'shade'];

/** The mark's box in logo units: everything inside lands in [0, MARK.w] x [0, MARK.h]. */
export const MARK = { x: 26, y: 15, w: 948, h: 1361 };
/** Centre of the light facet in logo units (where the travelling page docks). */
export const LIGHT_CENTRE = { x: 460, y: 497 };

/** Per-facet pose in logo units. */
export type FacetXf = { x?: number; y?: number; rot?: number; s?: number; o?: number };

const xf = (p: FacetXf | undefined, cx: number, cy: number) => {
  if (!p) return undefined;
  const s = Math.max(0, p.s ?? 1);
  return `translate(${p.x ?? 0} ${p.y ?? 0}) rotate(${p.rot ?? 0} ${cx} ${cy}) translate(${cx} ${cy}) scale(${s}) translate(${-cx} ${-cy})`;
};

const centre = (d: string) => {
  const n = d.match(/-?\d+(\.\d+)?/g)!.map(Number);
  let x = 0;
  let y = 0;
  for (let i = 0; i < n.length; i += 2) { x += n[i]; y += n[i + 1]; }
  return { x: (2 * x) / n.length, y: (2 * y) / n.length };
};
const CENTRES = Object.fromEntries(ORDER.map((k) => [k, centre(FACETS[k].d)])) as Record<Facet, { x: number; y: number }>;

/** The mark at `size` px tall. `pose` moves facets; `only` draws a subset; `id` keeps gradient ids unique. */
export const Mark: React.FC<{
  size: number;
  pose?: Partial<Record<Facet, FacetXf>>;
  only?: Facet[];
  id?: string;
  style?: React.CSSProperties;
}> = ({ size, pose = {}, only = ORDER, id = 'm', style }) => {
  const w = (size * MARK.w) / MARK.h;
  return (
    <svg width={w} height={size} viewBox={`${MARK.x} ${MARK.y} ${MARK.w} ${MARK.h}`} style={{ overflow: 'visible', display: 'block', ...style }}>
      <defs>
        {ORDER.map((k) => (
          <linearGradient key={k} id={`${id}-${k}`} x1={FACETS[k].from[0]} y1={FACETS[k].from[1]} x2={FACETS[k].to[0]} y2={FACETS[k].to[1]} gradientUnits="userSpaceOnUse">
            {FACETS[k].grad.map(([c, o]) => <stop key={o} offset={o} stopColor={c} />)}
          </linearGradient>
        ))}
      </defs>
      {ORDER.filter((k) => only.includes(k)).map((k) => {
        const p = pose[k];
        const o = Math.max(0, Math.min(1, p?.o ?? 1));
        if (o <= 0) return null;
        return (
          <path
            key={k}
            d={FACETS[k].d}
            fill={`url(#${id}-${k})`}
            stroke={FACETS[k].edge ? C.edge : 'none'}
            strokeWidth={13}
            strokeLinejoin="round"
            opacity={o}
            transform={xf(p, CENTRES[k].x, CENTRES[k].y)}
          />
        );
      })}
    </svg>
  );
};

/** The light facet alone as a page (device) centred at its own centre, `size` px tall for the whole mark's scale. */
export const pageScale = (markHeight: number) => markHeight / MARK.h;

/** CSS to place a Mark's top-left at (x, y) with transform only (no fractional left/top). */
export const placeMark = (x: number, y: number, k = 1): React.CSSProperties => ({
  position: 'absolute',
  left: 0,
  top: 0,
  transformOrigin: '0 0',
  transform: `translate(${x}px, ${y}px) scale(${k})`,
});

export { CENTRES as FACET_CENTRES };
