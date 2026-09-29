import { seg } from '../engine/tl.js';
import { outExpo, spring } from '../engine/ease.js';
import { place, icon } from '../engine/dom.js';
import { headlineRow, avatar, typedText } from '../engine/ui.js';
import { applyPush } from '../engine/transition.js';

const CROWD = [
  { x: 150, y: 540, size: 150, a: 1.1 },
  { x: 92, y: 800, size: 118, a: 2.3 },
  { x: 262, y: 968, size: 134, a: 3.7 },
  { x: 1770, y: 540, size: 140, a: 0.4 },
  { x: 1830, y: 810, size: 116, a: 1.9 },
  { x: 1660, y: 972, size: 150, a: 3.1 },
];

function buildMessage(S, m) {
  const name = S.mk('div', { text: m.name, style: { fontWeight: 700, fontSize: '30px', color: '#1D1F25' } });
  const when = S.mk('div', { text: m.when, style: { fontWeight: 500, fontSize: '24px', color: '#6B707D' } });
  const count = S.mk('span', { text: '0' });
  const likes = S.mk('div', { style: { marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '8px', color: S.c('blue'), fontWeight: 700, fontSize: '26px' } }, [icon('thumb_up', { style: { fontSize: '28px' } }), count]);
  const head = S.mk('div', { style: { display: 'flex', alignItems: 'center', gap: '14px' } }, [name, when, likes]);
  const text = typedText(m.text, { fontWeight: 500, fontSize: '30px', lineHeight: 1.35, color: '#2B2D35' });
  const attach = m.attach
    ? S.mk('div', { style: { display: 'inline-flex', alignItems: 'center', gap: '10px', alignSelf: 'flex-start', marginTop: '6px', padding: '8px 18px', borderRadius: '14px', background: S.c('blueWash'), color: S.c('blue'), fontWeight: 600, fontSize: '24px' } }, [icon('picture_as_pdf', { style: { fontSize: '28px' } }), m.attach])
    : null;
  const body = S.mk('div', { style: { flex: 1, display: 'flex', flexDirection: 'column', gap: '6px' } }, [head, text.node, attach]);
  const row = S.mk('div', { style: { display: 'flex', gap: '22px', alignItems: 'flex-start', padding: '20px 26px', borderRadius: '30px', background: '#F5F7FD' } }, [avatar(S, m.name, 84), body]);
  return { row, text, count, attach, likes: m.likes };
}

export default {
  pre: 0.4,
  post: 0.4,
  build(S, cfg, entry, root) {
    const { W, H, bd } = S;
    const dur = (entry.to - entry.from) * bd;
    const size = S.portrait ? 104 : 150;
    const head = headlineRow(S, { lead: cfg.lead, chip: cfg.chip, ic: cfg.icon, size, ink: S.c('ink'), fg: S.c('amber'), bg: S.c('amberWash') });
    root.append(head.node);
    const hb = head.node.getBoundingClientRect();

    const cats = cfg.categories.map((label, i) => S.mk('div', {
      text: label,
      style: {
        padding: '13px 30px', borderRadius: '999px', fontWeight: 600, fontSize: '27px', whiteSpace: 'nowrap',
        background: i === 0 ? S.c('blueWash') : '#fff', color: i === 0 ? S.c('blue') : S.c('muted'), border: '2px solid rgba(14,32,53,.10)',
      },
    }));
    const catRow = S.mk('div', { style: { position: 'absolute', left: 0, top: 0, display: 'flex', gap: '16px' } }, cats);
    root.append(catRow);
    const cb = catRow.getBoundingClientRect();

    const messages = cfg.thread.map((m) => buildMessage(S, m));
    const cardW = S.portrait ? W * 0.92 : 1240;
    const card = S.mk('div', {
      style: {
        position: 'absolute', left: 0, top: 0, width: `${cardW}px`, boxSizing: 'border-box', padding: '30px', borderRadius: '44px', background: '#fff',
        display: 'flex', flexDirection: 'column', gap: '18px', boxShadow: '0 60px 120px rgba(0,30,90,.20), 0 12px 30px rgba(0,30,90,.12)', border: '2px solid rgba(14,32,53,.06)',
      },
    }, messages.map((m) => m.row));
    root.append(card);
    const cardBox = card.getBoundingClientRect();
    const rowH = messages.map((m) => m.row.getBoundingClientRect().height);
    card.style.overflow = 'hidden';

    const crowd = CROWD.map((slot, i) => {
      const node = avatar(S, cfg.crowd[i % cfg.crowd.length], slot.size);
      root.append(node);
      return { ...slot, node };
    });

    const headY = S.portrait ? H * 0.17 : 168;
    const catY = headY + size * 1.3;
    const cardY = catY + 100;
    const starts = [0.45, 1.05, 1.65];

    return {
      update(lt, t) {
        applyPush(S, root, lt, dur);

        const lead = outExpo(seg(lt, -0.05, 0.5));
        const chipE = spring(0.5, 15)(seg(lt, 0.12, 0.7));
        const dotE = outExpo(seg(lt, 0.34, 0.4));
        place(head.node, { x: (W - hb.width) / 2, y: headY });
        place(head.lead, { y: (1 - lead) * 60, o: lead });
        place(head.chip, { y: (1 - chipE) * 40, s: 0.55 + 0.45 * chipE, o: Math.min(1, chipE * 2.2) });
        place(head.dot, { y: (1 - dotE) * 40, o: dotE });

        cats.forEach((c, i) => {
          const e = spring(0.6, 14)(seg(lt, 0.25 + i * 0.06, 0.6));
          place(c, { y: (1 - e) * 34, s: 0.7 + 0.3 * e, o: Math.min(1, e * 2) });
        });
        place(catRow, { x: (W - cb.width) / 2, y: catY });

        const cardE = outExpo(seg(lt, 0.3, 0.6));
        place(card, { x: (W - cardBox.width) / 2, y: cardY + (1 - cardE) * 90, s: 0.96 + 0.04 * cardE, o: cardE });
        const grown = messages.reduce((sum, m, i) => sum + outExpo(seg(lt, starts[i] - 0.05, 0.45)) * (rowH[i] + (i ? 18 : 0)), 0);
        card.style.height = `${60 + grown}px`;

        messages.forEach((m, i) => {
          const s0 = starts[i];
          const pop = spring(0.6, 14)(seg(lt, s0, 0.55));
          place(m.row, { y: (1 - pop) * 40, s: 0.94 + 0.06 * pop, o: Math.min(1, pop * 2.4) });
          m.text.set(seg(lt, s0 + 0.1, 0.5));
          const like = seg(lt, s0 + 0.62, 0.3, outExpo);
          m.count.textContent = String(Math.round(m.likes * like));
          if (m.attach) place(m.attach, { s: 0.6 + 0.4 * spring(0.5, 15)(seg(lt, s0 + 0.62, 0.5)), o: seg(lt, s0 + 0.62, 0.15) });
        });

        crowd.forEach((c, i) => {
          const e = spring(0.55, 13)(seg(lt, 0.35 + i * 0.07, 0.7));
          const bob = Math.sin(t * 1.8 + c.a) * 10;
          place(c.node, { x: c.x - c.size / 2, y: c.y - c.size / 2 + bob + (1 - e) * 120, s: 0.3 + 0.7 * e, o: Math.min(1, e * 2) });
        });
      },
    };
  },
};
