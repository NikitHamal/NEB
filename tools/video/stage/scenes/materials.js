import { seg } from '../engine/tl.js';
import { outExpo, outCubic, spring } from '../engine/ease.js';
import { place } from '../engine/dom.js';
import { headlineRow, browserFrame, libraryCard } from '../engine/ui.js';
import { applyPush } from '../engine/transition.js';

export default {
  pre: 0.4,
  post: 0.4,
  build(S, cfg, entry, root) {
    const { W, H, bd } = S;
    const dur = (entry.to - entry.from) * bd;
    root.style.perspective = '2400px';

    const size = S.portrait ? 104 : 150;
    const head = headlineRow(S, { lead: cfg.lead, chip: cfg.chip, ic: cfg.icon, size, ink: S.c('ink'), fg: S.c('purple'), bg: S.c('purpleWash') });
    root.append(head.node);
    const hb = head.node.getBoundingClientRect();
    const headX = (W - hb.width) / 2;
    const headY = S.portrait ? H * 0.17 : 168;

    const frameW = S.portrait ? W * 0.9 : 1440;
    const frameH = S.portrait ? H * 0.5 : 860;
    const frame = browserFrame(S, { w: frameW, h: frameH, image: S.capture('library'), url: cfg.url });
    root.append(frame.node);
    const frameX = (W - frameW) / 2;
    const frameY = S.portrait ? H * 0.34 : 410;

    const slots = S.portrait
      ? [{ cx: W * 0.16, cy: H * 0.74, rot: -8, k: 0.36, delay: 0.2 }, { cx: W * 0.86, cy: H * 0.66, rot: 7, k: 0.34, delay: 0.3 }]
      : [
        { cx: 170, cy: 660, rot: -7, k: 0.54, delay: 0.16, float: 0 },
        { cx: 140, cy: 950, rot: 6, k: 0.5, delay: 0.26, float: 1.3 },
        { cx: 1755, cy: 620, rot: 6, k: 0.54, delay: 0.22, float: 2.1 },
        { cx: 1790, cy: 930, rot: -6, k: 0.5, delay: 0.32, float: 3.4 },
      ];
    const cards = slots.map((slot, i) => {
      const card = libraryCard(S, { ...cfg.cards[i % cfg.cards.length], w: 560 });
      root.append(card.node);
      return { ...slot, card, h: card.node.getBoundingClientRect().height };
    });

    return {
      update(lt, t) {
        applyPush(S, root, lt, dur);

        const lead = outExpo(seg(lt, -0.05, 0.5));
        const chipE = spring(0.5, 15)(seg(lt, 0.12, 0.7));
        const dotE = outExpo(seg(lt, 0.34, 0.4));
        place(head.node, { x: headX, y: headY });
        place(head.lead, { y: (1 - lead) * 60, o: lead });
        place(head.chip, { y: (1 - chipE) * 40, s: 0.55 + 0.45 * chipE, o: Math.min(1, chipE * 2.2) });
        place(head.dot, { y: (1 - dotE) * 40, o: dotE });

        const rise = outExpo(seg(lt, -0.02, 0.85));
        const scroll = outCubic(seg(lt, 0.55, 2.1)) * frame.range * 0.85;
        place(frame.node, { x: frameX, y: frameY + (1 - rise) * H * 0.85 - outCubic(seg(lt, 0.5, 2.4)) * 46, rx: 24 * (1 - rise) + 4, rz: (1 - rise) * -3, o: 1 });
        frame.page.style.transform = `translateY(${-scroll}px)`;

        cards.forEach((c, i) => {
          const e = spring(0.55, 13)(seg(lt, c.delay, 0.8));
          const float = Math.sin(t * 1.6 + (c.float ?? i)) * 9;
          place(c.card.node, {
            x: c.cx - c.card.w / 2, y: c.cy - c.h / 2 + (1 - e) * 520 + float, rz: c.rot * (0.4 + 0.6 * e), s: c.k * (0.6 + 0.4 * e), o: Math.min(1, e * 2),
          });
        });
      },
    };
  },
};
