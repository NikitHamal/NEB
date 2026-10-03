import { place } from './dom.js';
import { round } from './math.js';

export function makeFx(S, layers) {
  const flash = S.mk('div', { class: 'layer flash' });
  const vignette = S.mk('div', { class: 'layer vignette' });
  layers.fx.append(flash, vignette);
  const chromaR = document.getElementById('chroma-r');
  const chromaB = document.getElementById('chroma-b');
  const pulseCfg = S.spec.fx?.pulse ?? { from: 4, to: 28, amount: 0.012 };

  return {
    apply(t) {
      const boom = S.env(t, ['boom'], 0.2);
      const hit = S.env(t, ['hit', 'thud'], 0.14);
      flash.style.opacity = round(S.env(t, ['boom'], 0.075) * 0.95, 3);

      const shake = Math.max(boom, hit * 0.3);
      const cover = 1 + 0.02 * Math.min(1, shake * 3);
      const u = S.u;
      const sx = Math.sin(t * 131.7) * Math.cos(t * 71.3) * shake * 14 * u;
      const sy = Math.cos(t * 97.1) * Math.sin(t * 53.9) * shake * 11 * u;
      const sr = Math.sin(t * 61.7) * shake * 0.5;

      const b = t / S.bd;
      const inPulse = b >= pulseCfg.from && b < pulseCfg.to ? 1 : 0;
      const pulse = 1 + pulseCfg.amount * S.pulse(t, { tau: 0.16 }) * inPulse;
      place(layers.world, { x: sx, y: sy, rz: sr, s: pulse * cover });

      const amp = Math.max(boom * 5, hit * 1.6) * u;
      if (amp > 0.12) {
        layers.world.style.filter = 'url(#chroma)';
        chromaR.setAttribute('dx', round(amp));
        chromaB.setAttribute('dx', round(-amp));
      } else if (layers.world.style.filter) {
        layers.world.style.filter = '';
      }
    },
  };
}
