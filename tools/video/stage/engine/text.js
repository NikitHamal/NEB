const segmenter = typeof Intl !== 'undefined' && Intl.Segmenter ? new Intl.Segmenter('en', { granularity: 'grapheme' }) : null;

export const graphemes = (text) => (segmenter ? [...segmenter.segment(text)].map((s) => s.segment) : [...text]);

let probe = null;
export function textWidth(text, { weight = 700, size = 100, ls = 0, family = 'Poppins' } = {}) {
  if (!probe) {
    probe = document.createElement('span');
    probe.style.cssText = 'position:absolute;left:-99999px;top:0;white-space:pre;visibility:hidden';
    document.body.appendChild(probe);
  }
  probe.style.font = `${weight} ${size}px ${family}`;
  probe.style.letterSpacing = `${ls}em`;
  probe.textContent = text;
  return probe.getBoundingClientRect().width;
}

export function fitSize(text, { weight = 700, ls = 0, target, max = Infinity, min = 8, family = 'Poppins' }) {
  const w = textWidth(text, { weight, size: 100, ls, family });
  return Math.max(min, Math.min(max, (target / w) * 100));
}
