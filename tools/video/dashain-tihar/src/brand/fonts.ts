// Poppins, the NEBians brand face, in Latin and Devanagari (Poppins ships a full Devanagari set,
// shaped by the browser so conjuncts and matras come out right). Local woff2, registered with
// the FontFace API: nothing is fetched at render time.
import { staticFile } from 'remotion';

const DEVANAGARI = 'U+0900-097F, U+1CD0-1CFF, U+200C-200D, U+20A8, U+20B9, U+25CC, U+A830-A839, U+A8E0-A8FF';

if (typeof document !== 'undefined') {
  for (const w of [500, 600, 700]) {
    // load() up front: unicode-range faces otherwise load lazily, after FontGate has measured
    for (const face of [
      new FontFace('Poppins', `url(${staticFile(`fonts/poppins-${w}-latin.woff2`)}) format('woff2')`, { weight: String(w) }),
      new FontFace('Poppins', `url(${staticFile(`fonts/poppins-${w}-devanagari.woff2`)}) format('woff2')`, { weight: String(w), unicodeRange: DEVANAGARI }),
    ]) {
      document.fonts.add(face);
      void face.load();
    }
  }
}
