// Poppins, the NEBians brand face, vendored as local woff2 in public/fonts (it ships no variable
// version, so each weight in use is its own file). Registered with the FontFace API so the font
// is bundled with the film and nothing is fetched at render time. Browser-only: only FontGate
// imports this file.
import { staticFile } from 'remotion';

const WEIGHTS = [500, 600, 700];

if (typeof document !== 'undefined') {
  for (const w of WEIGHTS) {
    const face = new FontFace('Poppins', `url(${staticFile(`fonts/poppins-${w}-latin.woff2`)}) format('woff2')`, { weight: String(w), style: 'normal' });
    document.fonts.add(face);
  }
}
