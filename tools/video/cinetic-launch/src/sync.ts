import { TYPE, U } from './brand/tokens';
import { chainResolves } from './fx/Chain';
import { typeFrames } from './fx/TypeOn';
import { E, SPR, type Ease } from './lib/anim';
import { hit, peak, settleOf } from './lib/sync';
import { ACT, copy, CUE, f60, FPS, TOTAL } from './timeline';

// Every sound in the film, placed on frames computed from the picture code: contact frames, the
// velocity peak of a move, the frame a fragment comes to rest. Nothing here is a typed-in guess.

export type Kind =
  | 'tick' | 'tock' | 'hit' | 'land' | 'pop' | 'whoosh' | 'riser'
  | 'drop' | 'key' | 'click' | 'snap' | 'swell' | 'bell' | 'suck' | 'text';

export type SoundEvent = {
  f: number;
  kind: Kind;
  weight?: number;
  pan?: number;
  pitch?: number | string;
  apexFrac?: number;
  dur?: number;
  variant?: string;
  id?: string;
};

const sec = (s: number) => Math.round(s * FPS);
const actOf = (f: number) => Object.entries(ACT).find(([, a]) => f >= a.from && f < a.from + a.dur)?.[0] ?? 'tail';

/** A move from a to b on `ease`: a whoosh as long as the move, its apex on the velocity peak. */
const move = (from: number, to: number, ease: Ease, weight: number, pan: number, id: string): SoundEvent => {
  const apex = peak(from, to, ease);
  const dur = Math.max(sec(0.3), to - from);
  return { f: apex, kind: 'whoosh', weight, pan, dur, apexFrac: (apex - from) / (to - from), id };
};

/** One soft key per word of a typed string (typing faster than 25 chars/s gets a blip per word). */
const typedWords = (text: string, start: number, cps: number, id: string, pan = 0): SoundEvent[] => {
  const at = typeFrames(text.length, { start, cps });
  const ev: SoundEvent[] = [];
  for (let i = 0; i < text.length; i++) if (i === 0 || text[i - 1] === ' ') ev.push({ f: at[i], kind: 'key', variant: 'word', weight: 0.55, pan, id: `${id}-${i}` });
  return ev;
};

/** The frame a single line of copy (fx/Words) comes to rest: 97% of its last word's rise. */
const resolveOf = (id: string) => copy(id).resolved - f60(4);

export default function cues(): SoundEvent[] {
  const ev: SoundEvent[] = [];
  const disp = TYPE.display.size * U;

  // 1 hook
  chainResolves('hook', { size: disp }).forEach((f, i) => ev.push({ f, kind: 'text', weight: 0.8, pan: -0.1 + 0.2 * i, id: `fragment${i + 1}` }));
  ev.push({ f: settleOf(CUE.page, CUE.page + f60(54), E.glide), kind: 'land', variant: 'light', weight: 0.6, pan: 0, id: 'page-settles' });
  ev.push({ f: CUE.caret + 1, kind: 'tick', weight: 0.6, id: 'caret' });
  ev.push(move(CUE.widen, CUE.type, E.rest, 0.7, 0, 'bar-widens'));
  ev.push(...typedWords(copy('question').text, CUE.type, 30, 'question'));

  // 2 ask
  ev.push({ f: CUE.askTap + 1, kind: 'click', variant: 'confirm', weight: 0.9, pan: 0.3, id: 'ask' });
  ev.push({ f: CUE.land, kind: 'land', variant: 'light', weight: 0.8, pan: -0.2, id: 'post-lands' });
  [CUE.reply1, CUE.reply2, CUE.reply3].forEach((f, i) => ev.push({ f: f + 3, kind: 'pop', weight: 0.7, pan: 0.35, id: `reply${i + 1}` }));
  ev.push({ f: CUE.answered + 2, kind: 'bell', weight: 0.8, pan: 0.3, id: 'answered' });
  ev.push(move(CUE.tip, CUE.tip + f60(36), E.smooth, 0.8, 0, 'forum-tips-back'));

  // 3 learn
  ev.push({ f: settleOf(CUE.multiply, CUE.multiply + f60(30), E.out), kind: 'land', variant: 'light', weight: 0.6, id: 'page-drops' });
  [0, 1, 2].forEach((i) => ev.push({ f: CUE.multiply + f60(18) + i * f60(5) + f60(8), kind: 'pop', weight: 0.55, pan: -0.3 + 0.3 * i, id: `card${i + 1}` }));
  for (let i = 0; i < 6; i++) ev.push({ f: CUE.chips + i * f60(5) + f60(4), kind: 'tick', weight: 0.45, pan: -0.3 + 0.12 * i, id: `level${i + 1}` });
  ev.push({ f: resolveOf('learn'), kind: 'text', weight: 0.8, id: 'learn' });
  ev.push(move(CUE.columns, CUE.columns + f60(54), E.smooth, 0.9, 0, 'columns-close'));

  // 4 reader
  ev.push(move(CUE.phone, CUE.phone + f60(66), E.cam, 0.8, 0, 'zoom-out-hop'));
  ev.push({ f: CUE.askNeby + 2, kind: 'click', weight: 0.8, pan: -0.3, id: 'ask-neby' });
  ev.push({ f: hit(CUE.neby - 14, SPR.land, 1), kind: 'land', weight: 1, pan: 0.35, id: 'neby-lands' });
  ev.push(...typedWords(copy('answer1').text, CUE.answer, 28, 'answer1', -0.3));
  ev.push(...typedWords(copy('answer2').text, CUE.answer2, 28, 'answer2', -0.3));
  ev.push({ f: CUE.highlight + 2, kind: 'bell', weight: 0.7, pan: -0.3, id: 'line-lights' });
  // E.contact peaks on its last frame (the paper's edge meets the top): apex there, set by hand
  ev.push({ f: CUE.readerOut + f60(34), kind: 'whoosh', weight: 0.9, pan: 0, dur: f60(36), apexFrac: 34 / 36, id: 'paper-rises' });

  // 5 pass
  ev.push({ f: settleOf(CUE.bar, CUE.bar + f60(60), E.out), kind: 'land', variant: 'light', weight: 0.7, pan: 0.2, id: 'bar-grows' });
  ev.push({ f: CUE.plus, kind: 'pop', weight: 0.9, pan: 0.2, id: 'a-plus' });
  ev.push({ f: CUE.pulse + 2, kind: 'bell', weight: 0.7, pan: 0.2, id: 'yours' });
  ev.push(move(CUE.pullback, CUE.pullback + f60(60), E.cam, 0.8, 0, 'pull-back'));
  ev.push({ f: CUE.gpaLock + 1, kind: 'tick', variant: 'crisp', weight: 0.9, pan: 0.3, id: 'gpa-locks' });

  // 6 pass on
  ev.push({ f: CUE.upload + f60(6), kind: 'pop', weight: 0.6, pan: -0.3, id: 'uploaded' });
  ev.push({ f: CUE.checked, kind: 'tick', weight: 0.6, pan: 0.2, id: 'checked' });
  ev.push({ f: CUE.published + 2, kind: 'bell', weight: 0.9, pan: 0.2, id: 'published' });
  ev.push({ f: CUE.readers + f60(52), kind: 'tick', variant: 'crisp', weight: 0.8, pan: 0.2, id: 'read-count-locks' });
  ev.push({ f: resolveOf('passon'), kind: 'text', weight: 0.9, id: 'passon' });

  // 7 lockup: the page's flight, the facets, then one clean hit when the name is readable
  ev.push(move(CUE.lift, CUE.dock, E.smooth, 0.5, 0, 'page-flies'));
  ev.push({ f: CUE.dock, kind: 'land', variant: 'light', weight: 0.5, id: 'page-docks' });
  ev.push({ f: CUE.name + f60(44), kind: 'hit', weight: 1, id: 'lockup' });
  ev.push({ f: resolveOf('endline'), kind: 'text', weight: 0.6, id: 'endline' });

  for (const e of ev) {
    if (!(e.f >= 0 && e.f < TOTAL)) throw new Error(`sync: ${e.id} at f=${e.f} is outside the film (0..${TOTAL - 1})`);
    e.id = `${actOf(e.f)}:${e.id}`;
  }
  return ev.sort((a, b) => a.f - b.f);
}
