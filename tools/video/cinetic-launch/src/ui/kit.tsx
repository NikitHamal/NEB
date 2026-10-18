import React from 'react';
import { C, FONT, TYPE } from '../brand/tokens';

// The product's own pieces, drawn the way NEBians draws them (cards, avatars, chips, the reader),
// sized by the act. Product strings carry data-ui so the layout audit counts them apart from copy.

export const SHADOW = '0 28px 90px rgba(0,0,0,.14)';
export const SHADOW_INK = '0 28px 90px rgba(0,0,0,.28)';

type Role = keyof typeof TYPE;

/** Text in a type role at an explicit px size; `ui` marks product strings for the audit. */
export const T: React.FC<{ role: Role; size: number; color?: string; ui?: boolean; style?: React.CSSProperties; children: React.ReactNode }> = ({ role, size, color = C.ink, ui = true, style, children }) => (
  <span
    data-ui={ui ? '' : undefined}
    style={{
      fontFamily: FONT.text,
      fontSize: size,
      fontWeight: TYPE[role].weight,
      letterSpacing: `${TYPE[role].track}em`,
      lineHeight: TYPE[role].lead,
      fontVariantNumeric: 'tabular-nums',
      color,
      whiteSpace: 'pre',
      ...style,
    }}
  >
    {children}
  </span>
);

export const Avatar: React.FC<{ initial: string; size: number; tone?: 'accent' | 'mist' | 'ink' }> = ({ initial, size, tone = 'mist' }) => {
  const bg = tone === 'accent' ? C.accent : tone === 'ink' ? C.ink : C.mist;
  const fg = tone === 'mist' ? C.ink : C.white;
  return (
    <div style={{ width: size, height: size, borderRadius: size / 2, background: bg, display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 'none' }}>
      <T role="ui" size={size * 0.44} color={fg} style={{ fontWeight: 600 }}>{initial}</T>
    </div>
  );
};

export const Chip: React.FC<{ size: number; tone?: 'mist' | 'accent' | 'white' | 'sky'; children: React.ReactNode; style?: React.CSSProperties }> = ({ size, tone = 'mist', children, style }) => {
  const bg = { mist: C.mist, accent: C.accent, white: C.white, sky: C.sky }[tone];
  const fg = tone === 'accent' ? C.white : C.ink;
  return (
    <div style={{ display: 'inline-flex', alignItems: 'center', height: size * 1.9, padding: `0 ${size * 0.8}px`, borderRadius: size, background: bg, ...style }}>
      <T role="ui" size={size} color={fg} style={{ fontWeight: 600 }}>{children}</T>
    </div>
  );
};

/** A white product card. */
export const Card: React.FC<{ w: number; h?: number; r: number; pad: number; children?: React.ReactNode; style?: React.CSSProperties; ink?: boolean }> = ({ w, h, r, pad, children, style, ink }) => (
  <div style={{ position: 'absolute', left: 0, top: 0, width: w, height: h, borderRadius: r, background: C.white, boxShadow: ink ? SHADOW_INK : SHADOW, padding: pad, boxSizing: 'border-box', overflow: 'hidden', ...style }}>
    {children}
  </div>
);

/** A check mark drawn on (p: 0..1). */
export const Check: React.FC<{ size: number; p: number; color?: string }> = ({ size, p, color = C.white }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" style={{ display: 'block' }}>
    <path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke={color} strokeWidth={2.6} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - Math.max(0, Math.min(1, p))} />
  </svg>
);

/** Grey text lines standing for body copy on a page or in a reply (never fake words). */
export const Lines: React.FC<{ widths: number[]; h: number; gap: number; color?: string; draw?: number[] }> = ({ widths, h, gap, color = C.line, draw }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap }}>
    {widths.map((w, i) => (
      <div key={i} style={{ width: w * Math.max(0, Math.min(1, draw?.[i] ?? 1)), height: h, borderRadius: h / 2, background: color }} />
    ))}
  </div>
);

/** Polygon corners, clockwise from top-left: TL, BL, BR, TR (the light facet's own order). */
export type Quad = [[number, number], [number, number], [number, number], [number, number]];

export const rectQuad = (x: number, y: number, w: number, h: number): Quad => [[x, y], [x, y + h], [x + w, y + h], [x + w, y]];
export const mixQuad = (a: Quad, b: Quad, t: number): Quad => a.map(([x, y], i) => [x + (b[i][0] - x) * t, y + (b[i][1] - y) * t]) as Quad;

/**
 * The device: the page that travels through the film, the logo's light facet. Drawn as one
 * polygon so it can be a sheet, a card header or the facet itself without a cut.
 */
export const PageShape: React.FC<{ quad: Quad; w: number; h: number; fill?: string; edge?: number; style?: React.CSSProperties }> = ({ quad, w, h, fill = C.sky, edge = 0, style }) => (
  <svg width={w} height={h} style={{ position: 'absolute', left: 0, top: 0, overflow: 'visible', ...style }}>
    <polygon points={quad.map((p) => p.join(',')).join(' ')} fill={fill} stroke={edge ? C.edge : 'none'} strokeWidth={edge} strokeLinejoin="round" />
  </svg>
);

/** A phone: ink frame, rounded screen. Children are the screen, laid out at (0,0) in screen px. */
export const Phone: React.FC<{ w: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ w, children, style }) => {
  const h = w * 2.06;
  const bezel = w * 0.035;
  return (
    <div style={{ position: 'absolute', left: 0, top: 0, width: w, height: h, borderRadius: w * 0.14, background: C.ink, boxShadow: SHADOW_INK, ...style }}>
      <div style={{ position: 'absolute', left: bezel, top: bezel, width: w - 2 * bezel, height: h - 2 * bezel, borderRadius: w * 0.11, background: C.white, overflow: 'hidden' }}>
        {children}
      </div>
    </div>
  );
};
