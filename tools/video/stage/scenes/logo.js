import { seg } from '../engine/tl.js';
import { outExpo, inOutCubic, spring, backWith } from '../engine/ease.js';
import { place, show } from '../engine/dom.js';
import { fitSize, graphemes, textWidth } from '../engine/text.js';
import { drawBurst } from '../engine/burst.js';
import { buildLogo } from '../engine/logo.js';
import { lerp } from '../engine/math.js';

const FLY = {
  dark: { x: 560, y: -900, r: 18, s: 0.9, delay: 0 },
  inner: { x: 900, y: 120, r: -14, s: 0.8, delay: 0.05 },
  light: { x: -700, y: -520, r: -24, s: 0.5, delay: 0.09 },
  front: { x: -820, y: 780, r: 10, s: 1, delay: 0.02 },
};

export default {
  build(S, cfg, entry, root) {
    const { W, H, bd, brand } = { ...S, brand: S.spec.brand };
    const big = S.portrait ? W * 0.34 : H * 0.36;
    const logo = buildLogo(S, S.assets.logoSvg, big);
    const wordSize = big * 0.62;
    const wordText = brand.name;
    const wordW = textWidth(wordText, { weight: 800, size: wordSize, ls: -0.045 });
    const gap = big * 0.13;
    const groupY = S.portrait ? H * 0.42 : H * 0.44;

    const wipe = S.mk('div', { class: 'fill', style: { background: '#fff', borderRadius: '50%', left: '0', top: '0', width: '100px', height: '100px', marginLeft: '-50px', marginTop: '-50px', position: 'absolute' } });
    const ring1 = S.mk('div', { style: { position: 'absolute', left: 0, top: 0, width: '100px', height: '100px', marginLeft: '-50px', marginTop: '-50px', borderRadius: '50%', border: '6px solid #fff', boxSizing: 'border-box' } });
    const ring2 = S.mk('div', { style: { position: 'absolute', left: 0, top: 0, width: '100px', height: '100px', marginLeft: '-50px', marginTop: '-50px', borderRadius: '50%', border: '3px solid rgba(0,74,198,0.55)', boxSizing: 'border-box' } });
    const logoBox = S.mk('div', { style: { position: 'absolute', left: 0, top: 0, width: `${logo.width}px`, height: `${logo.height}px` } }, [logo.svg]);
    const wordBox = S.mk('div', { class: 'logo-word', style: { position: 'absolute', left: 0, top: 0, fontSize: `${wordSize}px`, color: S.c('blue'), height: `${wordSize * 1.3}px`, overflow: 'hidden', display: 'flex', alignItems: 'center' } },
      [S.mk('span', { text: wordText, style: { display: 'inline-block', whiteSpace: 'nowrap', paddingRight: '0.05em' } })]);
    const tagSize = fitSize(cfg.tagline, { weight: 600, ls: -0.01, target: W * (S.portrait ? 0.86 : 0.5), max: big * 0.16 });
    const tagLetters = graphemes(cfg.tagline).map((ch) => S.mk('span', { class: 'tag-letter', text: ch }));
    const tagline = S.mk('div', { class: 'tagline', style: { fontSize: `${tagSize}px`, color: S.c('muted') } }, tagLetters);
    const sparks = S.mk('canvas', { class: 'fill', width: W, height: H });
    const ctx = sparks.getContext('2d');
    root.append(wipe, ring1, ring2, sparks, logoBox, wordBox, tagline);
    const tagW = tagline.getBoundingClientRect().width;
    const diag = Math.hypot(W, H);
    const dest = { x: S.header.pad, y: S.header.top - S.header.logoH / 2, s: S.header.logoH / big };

    return {
      pre: 0,
      update(lt, t) {
        const wipeE = outExpo(seg(lt, 0, 0.3));
        const wipeFade = 1 - seg(lt, 0.05, 0.26, inOutCubic);
        place(wipe, { x: W / 2, y: H / 2, s: (diag * 1.3 * wipeE) / 100 + 0.22, o: wipeFade });

        const r1 = outExpo(seg(lt, 0.02, 0.95));
        place(ring1, { x: W / 2, y: groupY, s: (diag * 0.95 * r1) / 100 + 0.2, o: (1 - r1) * 0.9 });
        ring1.style.borderWidth = `${lerp(14, 2, r1)}px`;
        const r2 = outExpo(seg(lt, 0.14, 1.1));
        place(ring2, { x: W / 2, y: groupY, s: (diag * 0.8 * r2) / 100 + 0.2, o: (1 - r2) * 0.7 });

        const facetT = lt - 0.06;
        for (const [name, g] of Object.entries(logo.facets)) {
          const f = FLY[name];
          if (!f) {
            const p = outExpo(seg(lt, 0.4, 0.4));
            g.style.opacity = p.toFixed(3);
            continue;
          }
          const p = outExpo(seg(facetT, f.delay, 0.55));
          const k = 1 - p;
          g.style.transform = `translate(${k * f.x}px,${k * f.y}px) rotate(${k * f.r}deg) scale(${lerp(f.s, 1, p)})`;
          g.style.opacity = Math.min(1, p * 4).toFixed(3);
        }

        const wordE = outExpo(seg(lt, bd * 0.85, 0.55));
        const lockW = logo.width + gap + wordW;
        const logoX = W / 2 - logo.width / 2 - (gap + wordW) * 0.5 * wordE;
        const land = seg(lt, 0.5, 0.5, spring(0.45, 15));
        const pulse = 1 + 0.05 * Math.exp(-Math.max(0, lt - 0.62) / 0.13) * (lt > 0.62 ? 1 : 0);

        const exit = inOutCubic(seg(lt, bd * 3.3, bd * 0.7));
        const x = lerp(logoX, dest.x, exit);
        const y = lerp(groupY - logo.height / 2, dest.y, exit);
        const s = lerp(1, dest.s, exit) * pulse * (0.9 + 0.1 * land);
        logoBox.style.transformOrigin = '0 0';
        place(logoBox, { x, y, s });

        const wordLeft = logoX + logo.width + gap;
        const wx = lerp(wordLeft, dest.x + logo.width * dest.s + gap * dest.s, exit);
        const wy = lerp(groupY - (wordSize * 1.3) / 2, S.header.top - (wordSize * 1.3 * dest.s) / 2, exit);
        wordBox.style.width = `${wordW * 1.04 * wordE}px`;
        wordBox.style.transformOrigin = '0 0';
        place(wordBox, { x: wx, y: wy, s: dest.s === 0 ? 1 : lerp(1, dest.s, exit) });
        wordBox.firstChild.style.transform = `translateX(${-(1 - wordE) * 60}px)`;

        const tagBase = groupY + big * 0.62;
        tagLetters.forEach((el, k) => {
          const e = outExpo(seg(lt, bd * 1.9 + k * 0.018, 0.45));
          place(el, { y: (1 - e) * 26, o: e * (1 - exit) });
        });
        place(tagline, { x: W / 2 - tagW / 2, y: tagBase });

        ctx.clearRect(0, 0, W, H);
        drawBurst(ctx, lt, {
          t0: 0.02, x: W / 2, y: groupY, n: 90, speed: 1500, life: 1.4, size: 24, gravity: 900, drag: 2.6,
          seed: 7, colors: [S.c('blue'), S.c('purple'), S.c('amber'), S.c('pink'), S.c('mint'), S.c('gold'), '#ffffff'],
        });
      },
    };
  },
};
