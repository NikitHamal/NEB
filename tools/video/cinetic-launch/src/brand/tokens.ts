// Brand tokens: the only place a colour, face or type size is written down. Acts import these;
// scripts/lint-film.mjs fails any hex colour that is not declared here.
//
// The NEBians brand, taken from its logo (n-logo-square-icon.svg): a royal blue front facet, a
// deep navy back, a sky-blue light facet, a pale edge. The light facet is the film's device.
import type React from 'react';
import { safeInsets } from '../lib/safe';
import { H, W } from '../timeline';

export const C = {
  ink: '#0A1636', // type and marks on paper; the dark stage (the logo's navy, not black)
  ink2: '#13244F', // raised surfaces on ink
  ink3: '#1E3470', // hairlines and quiet panels on ink
  paper: '#F4F6FB', // the light stage: a cool paper
  mist: '#E6ECF8', // soft panels on paper
  line: '#D3DCEE', // hairlines on paper, >= 1.5 px on screen
  mute: '#5B6785', // secondary text on paper (5.3:1)
  muteInk: '#9AA8CC', // secondary text on ink
  white: '#FFFFFF',
  // The one accent and its meaning: "answered" - help that has arrived and is yours. The logo's
  // royal blue (6.4:1 on paper). New things arrive in it and relax to ink.
  accent: '#004BD4',
  sky: '#A8C5FF', // the light facet: the page that travels through the film (the device)
  skyDeep: '#82A8F5', // the light facet's far edge
  edge: '#EEF5FF', // the logo's pale facet edge
  navy: '#052566', // the logo's back facet
  navyDeep: '#021B54',
  front: '#0058DF', // the logo's front facet, light end
};

// Poppins is the brand's own face (website, app, logo lockup). Three weights: 500 for UI, 600
// for lines, 700 for statements and the wordmark. // cinetic:brand-supplied font
export const FONT = {
  text: '"Poppins", system-ui, sans-serif',
  mono: '"Poppins", system-ui, sans-serif',
};

/** Faces the FontGate waits for before anything renders or measures (one entry per weight in use). */
export const FACES = ['500 16px "Poppins"', '600 16px "Poppins"', '700 16px "Poppins"'];

/** Layout unit: 1 at 1080p, scales every size with the short side of the frame (16:9, 9:16, 1:1). */
export const U = Math.min(W, H) / 1080;

// One token per role, reused everywhere, so nothing is "almost matched" (size in px at 1080p).
export const TYPE = {
  display: { size: 120, weight: 700, track: -0.045, lead: 1.0 }, // statements and the wordmark
  line: { size: 64, weight: 600, track: -0.03, lead: 1.1 }, // fragment chains (fx/Chain): a quiet line in open space
  secondary: { size: 44, weight: 500, track: -0.02, lead: 1.2 }, // descriptor lines, URLs
  title: { size: 34, weight: 600, track: -0.02, lead: 1.25 }, // product titles inside UI (post, resource)
  ui: { size: 24, weight: 500, track: -0.005, lead: 1.35 }, // smallest readable size on screen
};

/** CSS for a type role at a size (px). Tabular figures always, so numbers never jitter in width. */
export const typeStyle = (role: keyof typeof TYPE, size = TYPE[role].size * U): React.CSSProperties => ({
  fontFamily: FONT.text,
  fontSize: size,
  fontWeight: TYPE[role].weight,
  letterSpacing: `${TYPE[role].track}em`,
  lineHeight: TYPE[role].lead,
  fontVariantNumeric: 'tabular-nums',
  whiteSpace: 'pre',
});

/**
 * Safe margins for a w x h frame as a symmetric envelope: the larger inset of each pair from the
 * frame's safe-zone preset (src/lib/safe.ts), so a centred layout that fits inside clears every
 * side. 96 x 64 px at 1920x1080; 120 x 420 at 1080x1920, where the feed zones are asymmetric
 * (use safeBox() from lib/safe.ts there to centre on the clear band instead of the frame).
 */
export const safeArea = (w: number, h: number) => {
  const i = safeInsets(undefined, w, h);
  return { x: Math.max(i.left, i.right), y: Math.max(i.top, i.bottom) };
};
/** The film's safe margins; text stays inside them (scripts/layout-audit.sh checks). */
export const SAFE = safeArea(W, H);
