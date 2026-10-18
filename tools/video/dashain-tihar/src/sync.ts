import { E, SPR } from './lib/anim';
import { hit, peak, settleOf } from './lib/sync';
import { ACT, copy, CUE, f60, FPS, TOTAL } from './timeline';

// Every sound in the festival film, placed on frames the picture computes. The diyos are a rising
// scale of bells, one per flame; the kites ride soft air; the tika lands; the card gets one hit.

export type Kind =
  | 'tick' | 'tock' | 'hit' | 'land' | 'pop' | 'whoosh' | 'riser'
  | 'drop' | 'key' | 'click' | 'snap' | 'swell' | 'bell' | 'suck' | 'text';

export type SoundEvent = { f: number; kind: Kind; weight?: number; pan?: number; pitch?: number | string; apexFrac?: number; dur?: number; variant?: string; id?: string };

const sec = (s: number) => Math.round(s * FPS);
const actOf = (f: number) => Object.entries(ACT).find(([, a]) => f >= a.from && f < a.from + a.dur)?.[0] ?? 'tail';
const move = (from: number, to: number, ease: (t: number) => number, weight: number, pan: number, id: string): SoundEvent => {
  const apex = peak(from, to, ease);
  return { f: apex, kind: 'whoosh', weight, pan, dur: Math.max(sec(0.3), to - from), apexFrac: (apex - from) / (to - from), id };
};
const textAt = (id: string) => copy(id).resolved - f60(4);

export default function cues(): SoundEvent[] {
  const ev: SoundEvent[] = [];
  ev.push({ f: CUE.jamara + f60(10), kind: 'pop', weight: 0.5, pan: -0.4, id: 'jamara' });
  ev.push({ f: textAt('dashain'), kind: 'text', weight: 0.8, id: 'dashain' });
  ev.push(move(CUE.kiteLift, ACT.dawn.from + ACT.dawn.dur + f60(20), E.inOut, 0.6, 0.4, 'kite-lifts'));
  ev.push({ f: CUE.drop, kind: 'hit', weight: 0.8, id: 'kites-drop' });
  ev.push({ f: CUE.ping + f60(8), kind: 'whoosh', weight: 0.5, pan: -0.5, dur: f60(40), apexFrac: 0.2, id: 'swing' });
  ev.push({ f: textAt('kites'), kind: 'text', weight: 0.8, id: 'kites' });
  ev.push({ f: settleOf(CUE.hand, CUE.tikaOn, E.out), kind: 'tick', weight: 0.4, pan: 0.4, id: 'hand' });
  ev.push({ f: hit(CUE.tikaOn - 6, SPR.land, 1), kind: 'land', variant: 'light', weight: 0.9, pan: 0.2, id: 'tika' });
  ev.push({ f: CUE.jamaraEar + f60(14), kind: 'pop', weight: 0.5, pan: -0.3, id: 'jamara-ear' });
  ev.push({ f: textAt('tika'), kind: 'text', weight: 0.8, id: 'tika' });
  ev.push({ f: textAt('swap.1'), kind: 'text', weight: 0.7, id: 'dashain-name' });
  ev.push({ f: CUE.dusk + f60(45), kind: 'whoosh', weight: 0.6, dur: f60(90), apexFrac: 0.5, id: 'night-falls' });
  ev.push({ f: textAt('swap.2'), kind: 'text', weight: 0.8, id: 'tihar-name' });
  ev.push({ f: CUE.lights + f60(14), kind: 'bell', weight: 0.6, id: 'string-lights' });
  // the diyos: a rising scale, one bell per flame
  const scale = ['D5', 'E5', 'F#5', 'A5', 'B5', 'D6'];
  [CUE.diyo1, CUE.diyo2, CUE.diyo3, CUE.diyo4, CUE.diyo5, CUE.diyo6].forEach((f, i) => ev.push({ f: f + 2, kind: 'bell', pitch: scale[i], weight: 0.8, pan: -0.6 + i * 0.24, id: `diyo${i + 1}` }));
  ev.push({ f: CUE.dog + 2, kind: 'pop', weight: 0.5, pan: 0.6, id: 'dog' });
  ev.push({ f: textAt('home'), kind: 'text', weight: 0.8, id: 'home' });
  ev.push({ f: CUE.books + f60(6), kind: 'whoosh', weight: 0.5, dur: f60(30), apexFrac: 0.2, id: 'books-fan' });
  ev.push({ f: CUE.phone + f60(26), kind: 'tick', variant: 'crisp', weight: 0.7, id: 'books-in' });
  ev.push({ f: textAt('study'), kind: 'text', weight: 0.8, id: 'study' });
  ev.push({ f: CUE.name + f60(30), kind: 'hit', weight: 1, id: 'lockup' });
  ev.push({ f: textAt('wish'), kind: 'text', weight: 0.6, id: 'wish' });
  for (const e of ev) {
    if (!(e.f >= 0 && e.f < TOTAL)) throw new Error(`sync: ${e.id} at f=${e.f} outside the film`);
    e.id = `${actOf(e.f)}:${e.id}`;
  }
  return ev.sort((a, b) => a.f - b.f);
}
