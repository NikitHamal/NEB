// Brand tokens: the only place a colour, face or type size is written down. Acts import these;
// scripts/lint-film.mjs fails any hex colour that is not declared here.
//
// The NEBians brand, taken from its logo (n-logo-square-icon.svg): a royal blue front facet, a
// deep navy back, a sky-blue light facet, a pale edge. The light facet is the film's device.
import type React from 'react';
import { safeInsets } from '../lib/safe';
import { rgb } from '../pixel/canvas';
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

// The festival palette for the pixel scenes: Dashain's tika red, jamara green and kite colours,
// Tihar's marigolds and diyo flames, and the valley's sky from dawn to night.
// cinetic:brand-supplied festival palette (marigold, tika red, jamara green are Dashain and Tihar themselves)
export const P = {
  line: rgb('#1A1530'), // cinetic:brand-supplied festival palette
  dawn: [rgb('#5E7FD6'), rgb('#8FA9E8'), rgb('#C9B7E6'), rgb('#F2B9B0'), rgb('#FFD4A8')], // cinetic:brand-supplied festival palette
  day: [rgb('#4F9BEA'), rgb('#7DB6F2'), rgb('#A9CDF6'), rgb('#CFE3FA'), rgb('#E8F2FD')], // cinetic:brand-supplied festival palette
  night: [rgb('#0B0F2A'), rgb('#141A3E'), rgb('#1F2754'), rgb('#2C2F63'), rgb('#3A3570')], // cinetic:brand-supplied festival palette
  sun: rgb('#FFE6A0'), sunCore: rgb('#FFF6D6'), moon: rgb('#F3F0E2'), star: rgb('#FFF7D6'), // cinetic:brand-supplied festival palette
  snow: rgb('#F4F6FF'), ridgeFar: rgb('#9AA8D6'), ridgeMid: rgb('#6F7FB8'), hill: rgb('#3E6B5A'), hillLo: rgb('#2E5246'), // cinetic:brand-supplied festival palette
  brick: rgb('#A2492E'), brickLo: rgb('#7A3522'), roof: rgb('#4A2C24'), roofLo: rgb('#35201B'), wood: rgb('#6B3F2A'), // cinetic:brand-supplied festival palette
  window: rgb('#2A1C2E'), windowLit: rgb('#FFC65A'), // cinetic:brand-supplied festival palette
  marigold: rgb('#FF9F1C'), marigoldLo: rgb('#E0731A'), yellow: rgb('#FFD23F'), // cinetic:brand-supplied festival palette
  red: rgb('#D7263D'), redLo: rgb('#9E1B2E'), green: rgb('#5DBB46'), greenLo: rgb('#3E8C2F'), jamara: rgb('#D9E86A'), // cinetic:brand-supplied festival palette
  clay: rgb('#B5653A'), clayLo: rgb('#8A4628'), flame: rgb('#FFB020'), flameHi: rgb('#FFF3B0'), // cinetic:brand-supplied festival palette
  skin: rgb('#C98B67'), skinLo: rgb('#A86E52'), hair: rgb('#22151C'), cloth: rgb('#2F64D6'), clothHi: rgb('#5A8BEA'), // cinetic:brand-supplied festival palette
  dog: rgb('#C9A27A'), dogLo: rgb('#9C7754'), white: rgb('#FFFFFF'), magenta: rgb('#C2338A'), teal: rgb('#1FA597'), // cinetic:brand-supplied festival palette
  phone: rgb('#11182E'), screen: rgb('#004BD4'), screenHi: rgb('#A8C5FF'), // cinetic:brand-supplied festival palette
  tealHi: rgb('#9FE6D9'), magentaHi: rgb('#FFB0CB'), // cinetic:brand-supplied festival palette
  wall: rgb('#5A2A20'), wallLo: rgb('#4A2219'), door: rgb('#2A1418'), ledge: rgb('#3A1C16'), floor: rgb('#2B2433'), // cinetic:brand-supplied festival palette
  room: [rgb('#2A1A2C'), rgb('#3A2230'), rgb('#4A2A30')], frame: rgb('#6B3F2A'), // cinetic:brand-supplied festival palette
  warm: [rgb('#F7D9B5'), rgb('#F2C79A'), rgb('#E9B482')], rice: rgb('#F7F0E0'), road: rgb('#7A6A5A'), // cinetic:brand-supplied festival palette
};
