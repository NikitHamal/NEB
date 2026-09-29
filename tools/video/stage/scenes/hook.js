import { seg } from '../engine/tl.js';
import { outExpo, inExpo, inOutCubic, spring } from '../engine/ease.js';
import { place, show, icon, setStyle } from '../engine/dom.js';
import { fitSize, graphemes } from '../engine/text.js';
import { drawBurst } from '../engine/burst.js';
import { clamp, lerp } from '../engine/math.js';

function buildPanel(S, word, index, total, host) {
  const { mk, W, H } = S;
  const maxSize = S.portrait ? 330 : 400;
  const size = fitSize(word.text, { weight: 900, ls: -0.05, target: W * 0.84, max: maxSize });
  const pad = S.portrait ? 56 : 96;
  const bg = S.c(word.bg);
  const fg = S.c(word.fg);

  const glyph = icon(word.icon, { class: 'hook-icon', style: { fontSize: `${H * (S.portrait ? 0.62 : 1.18)}px`, color: fg } });
  const letters = graphemes(word.text).map((ch) => mk('span', { class: 'hook-letter', text: ch }));
  const text = mk('div', { class: 'hook-word', style: { fontSize: `${size}px`, color: fg } }, letters);
  const tag = mk('div', { class: 'hook-meta', text: word.tag, style: {
    fontSize: `${S.portrait ? 26 : 32}px`, color: fg, border: `2px solid ${fg}`, borderRadius: '999px', padding: '10px 26px', opacity: 0.8,
  } });
  const count = mk('div', { class: 'hook-meta', text: `${String(index + 1).padStart(2, '0')} / ${String(total).padStart(2, '0')}`, style: {
    fontSize: `${S.portrait ? 26 : 32}px`, color: fg, opacity: 0.75,
  } });
  const bar = mk('div', { class: 'hook-bar', style: { width: `${W}px`, color: fg, opacity: 0.85 } });
  const dim = mk('div', { class: 'fill', style: { background: '#000', opacity: 0 } });
  const node = mk('div', { class: 'hook-panel fill', style: { background: bg } }, [glyph, text, tag, count, bar, dim]);
  host.append(node);

  const wordBox = text.getBoundingClientRect();
  const layout = {
    wordW: wordBox.width,
    wordH: wordBox.height,
    wordX: (W - wordBox.width) / 2,
    wordY: (H - wordBox.height) / 2 + (S.portrait ? 0 : 10),
    iconSize: H * (S.portrait ? 0.62 : 1.18),
    pad,
  };
  place(text, { x: layout.wordX, y: layout.wordY });
  place(tag, { x: pad, y: pad });
  place(count, { x: pad, y: H - pad - 44 });
  return { node, glyph, text, letters, tag, count, bar, dim, size, layout, bg, fg };
}

export default {
  build(S, cfg, entry, root) {
    const { W, H, bd } = S;
    const words = cfg.words;
    const stack = S.mk('div', { class: 'fill', style: { overflow: 'hidden', transformOrigin: '50% 50%' } });
    root.append(stack);
    const panels = words.map((w, i) => buildPanel(S, w, i, words.length, stack));
    const sparks = S.mk('canvas', { class: 'fill', width: W, height: H });
    const ctx = sparks.getContext('2d');
    const dot = S.mk('div', { class: 'hook-dot', style: { width: '44px', height: '44px', marginLeft: '-22px', marginTop: '-22px' } });
    root.append(sparks, dot);
    const tilt = [-1, 1, -1, 1];
    const implodeAt = (words.length - 0.65) * bd;
    const implodeEnd = (words.length - 0.08) * bd;
    const radius0 = Math.hypot(W, H) / 2;

    return {
      update(lt, t) {
        const collapse = clamp((lt - implodeAt) / (implodeEnd - implodeAt));
        const shrink = inExpo(collapse);
        place(stack, { x: 0, y: 0, s: Math.max(0.0001, 1 - shrink), rz: shrink * -18 });
        setStyle(stack, 'clipPath', collapse > 0 ? `circle(${lerp(radius0, H * 0.5, inOutCubic(collapse))}px at 50% 50%)` : 'none');

        panels.forEach((p, i) => {
          const t0 = i * bd;
          const age = lt - t0;
          show(p.node, age >= -0.001);
          const enter = i === 0 ? 1 : outExpo(seg(lt, t0, 0.26));
          const cornerR = i === 0 ? 0 : (1 - enter) * 90;
          setStyle(p.node, 'borderRadius', `${cornerR}px ${cornerR}px 0 0`);
          const settle = i === 0 ? 1.07 - 0.07 * outExpo(seg(lt, 0, 0.4)) : 1;
          place(p.node, { x: 0, y: (1 - enter) * H * 1.02, s: settle });

          const next = panels[i + 1];
          const cover = next ? outExpo(seg(lt, (i + 1) * bd, 0.26)) : 0;
          place(p.text, { x: p.layout.wordX, y: p.layout.wordY - cover * H * 0.05 });
          p.dim.style.opacity = (cover * 0.35).toFixed(3);

          const wobble = spring(0.4, 16)(seg(age, 0, 0.7));
          const start = i === 0 ? -0.55 : 0.04;
          const hit = S.env(t, ['hit'], 0.13);
          p.letters.forEach((el, k) => {
            const e = outExpo(seg(lt, t0 + start + k * 0.024, 0.36));
            place(el, { y: (1 - e) * p.size * 1.55, rz: (1 - e) * tilt[i % 4] * 9 });
          });
          setStyle(p.text, 'transform', `translate(${p.layout.wordX}px,${p.layout.wordY - cover * H * 0.05}px) rotate(${(1 - wobble) * tilt[i % 4] * 3}deg) scale(${1 + hit * 0.04})`);

          const drift = Math.max(0, age);
          place(p.glyph, { x: W * (S.portrait ? 0.32 : 0.6), y: H * 0.5 - p.layout.iconSize / 2 + drift * 24, rz: -8 + drift * 5, s: 1 + drift * 0.09 });
          place(p.tag, { x: p.layout.pad, y: p.layout.pad - (1 - outExpo(seg(age, 0.05, 0.3))) * 30, o: outExpo(seg(age, 0.05, 0.3)) * 0.8 });
          place(p.count, { x: p.layout.pad, y: H - p.layout.pad - 44 });
          setStyle(p.bar, 'transform', `translate(0px,0px) scaleX(${clamp(age / bd)})`);
        });

        ctx.clearRect(0, 0, W, H);
        words.forEach((w, i) => {
          drawBurst(ctx, lt, {
            t0: i * bd + 0.02, x: W / 2, y: H * 0.5 + panels[i].size * 0.28, n: 30, speed: 1000, life: 0.85, size: 22, gravity: 1400,
            drag: 3.2, angle: -Math.PI / 2, spread: Math.PI * 1.15, seed: 100 + i * 13,
            colors: [S.c(w.fg), S.c('gold'), S.c('pink'), S.c('skyDeep')],
          });
        });

        const dotE = seg(lt, implodeAt + (implodeEnd - implodeAt) * 0.55, (implodeEnd - implodeAt) * 0.45, outExpo);
        place(dot, { x: W / 2, y: H / 2, s: dotE, o: dotE });
        dot.style.boxShadow = `0 0 ${20 + dotE * 60}px ${6 + dotE * 24}px rgba(255,255,255,0.75)`;
      },
    };
  },
};
