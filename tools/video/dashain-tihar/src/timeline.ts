// The single source of truth for time. Picture (src/acts), sound (src/sync.ts -> out/cues.json)
// and QA (scripts/grid-check.ts) all import this file, so a change here moves everything together.
// Think in bars and beats, never in seconds. Keep this file free of React and CSS imports:
// Node scripts load it directly.
import { holdFor, PACE, readingWindows, revealFor, wordCount, type PaceName } from './lib/pace';

export { PACE } from './lib/pace'; // grid-check checks COPY against the film's own pace numbers

export const FPS = 60;
export const BPM = 100;
export const W = 1920;
export const H = 1080;
/**
 * The film's pace (src/lib/pace.ts). calm: text arrives as short fragments that take turns with
 * the picture, held about 1-1.5 s (the default for text-led films, at 90-100 BPM). crisp: the
 * denser launch-film tempo, for briefs that ask for energy (at 120 BPM).
 */
export const PACE_NAME: PaceName = 'calm';

/** Frames per beat. Must be a whole number (grid-check fails otherwise): 60 fps -> 90, 100, 120, 144, 150 BPM. */
export const BEAT = (60 / BPM) * FPS;
export const BAR = BEAT * 4;
/**
 * Absolute frame of a grid position: bar is 1-based, beat 0-3, sub = 16ths within the beat.
 * b(3) is the downbeat of bar 3; b(2, 1, 2) is the "and" of beat 2 in bar 2.
 */
export const b = (bar: number, beat = 0, sub = 0) => Math.round(((bar - 1) * 4 + beat) * BEAT + sub * (BEAT / 4));

/**
 * A choreography length written in 60 fps frames (the unit every number in the cinetic
 * references uses), converted to this film's fps. Cues come from b(); durations inside a move
 * use f60(), so the film keeps its timing if --fps changes.
 */
export const f60 = (frames: number) => Math.round((frames * FPS) / 60);

/** After the last bar the picture holds while the audio decays to digital silence. */
export const TAIL = FPS;

// Acts: contiguous, bar-aligned. Dashain by day, the turn at dusk, Tihar by night, the student
// reading by diyo light, the card. The device is one kite: it rises in Dashain, holds its place
// while the world turns to night, and its string becomes Tihar's string of lights.
export const ACT = {
  dawn: { from: b(1), dur: b(3) - b(1) },
  kites: { from: b(3), dur: b(5) - b(3) },
  tika: { from: b(5), dur: b(7) - b(5) },
  turn: { from: b(7), dur: b(9) - b(7) },
  tihar: { from: b(9), dur: b(11) - b(9) },
  study: { from: b(11), dur: b(13) - b(11) },
  end: { from: b(13), dur: b(15) + TAIL - b(13) },
};

export const TOTAL = b(15) + TAIL;

export const CUE = {
  // dawn: quiet, the sun already rising on frame 0
  jamara: b(1, 2), // jamara shoots up in its pot
  fragDashain: b(2), // "दशैं आयो"
  kiteLift: b(2, 3), // a kite leaves the rooftop
  // kites: the drop
  drop: b(3), // the sky fills with kites
  ping: b(3, 2), // the bamboo swing swings out
  fragKites: b(4), // "आकाशभरि चङ्गा"
  // tika
  hand: b(5), // an elder's hand comes in
  tikaOn: b(5, 2), // the red tika lands (a true landing)
  jamaraEar: b(5, 3), // jamara tucked behind the ear
  fragTika: b(6), // "टीका र जमरा"
  // the turn: the kite holds, the world goes to night
  hold: b(7), // the kite alone in the sky
  dusk: b(7, 3, 2), // after the name is read, day drains out and night comes in
  fragSwap: b(8), // "दशैं" becomes "तिहार"
  lights: b(8, 3), // the kite string lights up
  // tihar: one diyo per beat
  diyo1: b(9), diyo2: b(9, 1), diyo3: b(9, 2), diyo4: b(9, 3), diyo5: b(10), diyo6: b(10, 1),
  dog: b(9, 2), // the dog in its garland looks up
  rangoli: b(9, 1), // the rangoli fills in
  fragHome: b(10, 2), // "घर उज्यालो"
  // study by diyo light
  books: b(11, 1), // books fan out of the phone
  phone: b(11, 2), // they settle into the library on the phone
  fragStudy: b(12), // "बिदामा पनि पढाइ"
  // card
  mark: b(13), // the mark assembles over the night town
  name: b(13, 1, 2),
  wish: b(14, 0, 2), // "शुभ दशैं, शुभ तिहार", once the name is read
  end: b(15),
};

export type Copy = {
  id: string;
  text: string; // exactly what is on screen (\n separates lines)
  in: number; // first frame any of it is visible
  resolved: number; // first frame it is fully readable
  out: number; // first frame it starts to leave (TOTAL if it stays)
  kind?: 'copy' | 'ui'; // 'ui': a string the product shows (a typed command, code, a URL, an app label); not budgeted
  chain?: string; // the thought this fragment belongs to (fx/Chain renders a chain; grid-check checks its gaps)
  mode?: 'build' | 'replace'; // build: fragments append to one held line; replace: each takes the last one's place
};

const pace = PACE[PACE_NAME];

/**
 * One line of copy revealed word by word with this film's pace (the numbers <Words> uses), so
 * `resolved` is the frame its last word is fully in. `out` defaults to the pace's hold.
 */
export const line = (id: string, text: string, inF: number, out?: number): Copy => {
  const n = wordCount(text);
  const resolved = inF + f60(revealFor(n, pace));
  return { id, text, in: inF, resolved, out: out ?? resolved + f60(holdFor(n, pace)) };
};

/**
 * One thought as a chain of fragments, one COPY entry each (`<id>.1`, `<id>.2`, ...), rendered by
 * fx/Chain. A thought longer than 4 words arrives this way: 1-4 words per fragment, never a whole
 * sentence at once, with a picture beat between fragments (the product does what the fragment set
 * up). Give each fragment its first frame; `resolved` follows from the pace.
 *   build    fragments append to one held line, which re-centres; the line clears as a whole, at
 *            `out` (default: the last fragment's resolve plus the hold of the full line)
 *   replace  each fragment leaves (as a whole, over pace.exitDur: 24 f when calm) and has gone
 *            6 f before the next one rises in its place, so two fragments never share the spot;
 *            the last one leaves at `out` (default: its resolve plus its hold)
 * grid-check checks the result: every fragment is read before the next arrives, the picture beat
 * between them, the words on screen at once and the copy rate.
 */
export const chain = (id: string, mode: 'build' | 'replace', fragments: [text: string, inF: number][], o: { out?: number } = {}): Copy[] => {
  const base = fragments.map(([text, inF], i) => ({ id: `${id}.${i + 1}`, text, in: inF, resolved: inF + f60(revealFor(wordCount(text), pace)), chain: id, mode }));
  const last = base[base.length - 1];
  if (!last) throw new Error(`timeline: chain "${id}" has no fragments`);
  const words = (list: { text: string }[]) => list.reduce((n, c) => n + wordCount(c.text), 0);
  if (mode === 'build') {
    const out = o.out ?? last.resolved + f60(holdFor(words(base), pace));
    return base.map((c) => ({ ...c, out }));
  }
  // replace: the outgoing fragment's exit (exitDur) is over 6 f before the next one starts to rise
  const leave = f60(pace.exitDur) + f60(6);
  return base.map((c, i) => ({ ...c, out: base[i + 1] ? base[i + 1].in - leave : (o.out ?? c.resolved + f60(holdFor(wordCount(c.text), pace))) }));
};

// Every on-screen word: the word budget (kind: 'ui' entries are counted apart), the hold check,
// and the text-flow checks (fragments, words on screen at once, copy rate, text share) read this.
export const COPY: Copy[] = [
  line('dashain', 'दशैं आयो', CUE.fragDashain),
  line('kites', 'आकाशभरि चङ्गा', CUE.fragKites),
  line('tika', 'टीका र जमरा', CUE.fragTika),
  // the festival's name changes in place: Dashain, then Tihar
  ...chain('swap', 'replace', [['दशैं', CUE.hold + f60(18)], ['तिहार', CUE.fragSwap]]),
  line('home', 'घर उज्यालो', CUE.fragHome),
  line('study', 'बिदामा पनि पढाइ', CUE.fragStudy),
  { id: 'wordmark', text: 'NEBians', in: CUE.name, resolved: CUE.name + f60(34), out: TOTAL },
  line('wish', 'शुभ दशैं, शुभ तिहार', CUE.wish, TOTAL),
  { id: 'url', text: 'nebians.consica.com.np', in: CUE.wish + f60(30), resolved: CUE.wish + f60(54), out: TOTAL, kind: 'ui' },
];

/**
 * When each COPY entry is being read: [from, to) frame ranges by id (src/lib/pace.ts
 * readingWindows(): from `resolved` for at most readMax, an earlier fragment of a build chain only
 * for its own hold, then the whole line again). The one rule every check uses: export-cues.ts
 * writes it into out/cues.json, and grid-check, layout-audit, measure-speed and forensics read it.
 * Nothing new should start inside a window: the read happens in the quiet.
 */
export const READ = readingWindows(COPY, pace, FPS, TOTAL);

/** One COPY entry by id; acts read their text and timing from here so the budget stays true. */
export const copy = (id: string): Copy => {
  const c = COPY.find((x) => x.id === id);
  if (!c) throw new Error(`timeline: no COPY entry "${id}"`);
  return c;
};

/** The fragments of one chain, in order of arrival. */
export const chainOf = (id: string): Copy[] => {
  const list = COPY.filter((x) => x.chain === id).sort((p, q) => p.in - q.in);
  if (!list.length) throw new Error(`timeline: no COPY chain "${id}"`);
  return list;
};
