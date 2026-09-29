import { seg } from '../engine/tl.js';
import { outExpo, spring } from '../engine/ease.js';
import { place, icon } from '../engine/dom.js';
import { headlineRow, typedText } from '../engine/ui.js';
import { applyPush } from '../engine/transition.js';

const TILE_COLORS = [
  { fg: '#004AC6', bg: '#DBE1FF' },
  { fg: '#B84B0B', bg: '#FFEFCF' },
  { fg: '#6246D7', bg: '#EBE7FF' },
  { fg: '#12805C', bg: '#DDF6EA' },
];

function buildTile(S, tile, color) {
  const badge = tile.badge
    ? S.mk('div', { text: tile.badge, style: { position: 'absolute', right: '20px', top: '20px', padding: '5px 14px', borderRadius: '999px', background: '#EBE7FF', color: '#6246D7', fontWeight: 700, fontSize: '19px', letterSpacing: '0.03em' } })
    : null;
  const box = S.mk('div', { style: { width: '68px', height: '68px', borderRadius: '20px', background: color.bg, color: color.fg, display: 'flex', alignItems: 'center', justifyContent: 'center' } }, [icon(tile.icon, { style: { fontSize: '40px' } })]);
  const title = S.mk('div', { text: tile.title, style: { fontWeight: 700, fontSize: '32px', color: '#1D1F25', letterSpacing: '-0.01em' } });
  const text = S.mk('div', { text: tile.text, style: { fontWeight: 500, fontSize: '23px', lineHeight: 1.3, color: '#525663' } });
  return S.mk('div', {
    style: {
      position: 'absolute', left: 0, top: 0, width: '350px', boxSizing: 'border-box', padding: '26px', borderRadius: '32px', background: '#fff', display: 'flex', flexDirection: 'column', gap: '12px',
      boxShadow: '0 40px 80px rgba(0,30,90,.18), 0 8px 22px rgba(0,30,90,.10)', border: '2px solid rgba(14,32,53,.06)',
    },
  }, [box, title, text, badge]);
}

export default {
  pre: 0.4,
  post: 0.1,
  build(S, cfg, entry, root) {
    const { W, H, bd } = S;
    const dur = (entry.to - entry.from) * bd;
    const size = S.portrait ? 104 : 150;
    const head = headlineRow(S, { lead: cfg.lead, chip: cfg.chip, ic: cfg.icon, size, ink: S.c('ink'), fg: S.c('blue'), bg: S.c('blueWash') });
    root.append(head.node);
    const hb = head.node.getBoundingClientRect();

    const nebyAvatar = S.mk('div', { style: { width: '68px', height: '68px', borderRadius: '50%', background: `linear-gradient(135deg, ${S.c('blueBright')}, ${S.c('purple')})`, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', flex: 'none' } }, [icon('auto_awesome', { style: { fontSize: '38px' } })]);
    const aiName = S.mk('div', { text: cfg.ai.name, style: { fontWeight: 700, fontSize: '32px', color: '#1D1F25' } });
    const aiCtx = S.mk('div', { text: cfg.ai.context, style: { fontWeight: 500, fontSize: '23px', color: '#6B707D' } });
    const aiHead = S.mk('div', { style: { display: 'flex', alignItems: 'center', gap: '18px' } }, [nebyAvatar, S.mk('div', {}, [aiName, aiCtx])]);
    const question = S.mk('div', { text: cfg.ai.question, style: { alignSelf: 'flex-end', maxWidth: '78%', padding: '18px 28px', borderRadius: '30px 30px 8px 30px', background: S.c('blue'), color: '#fff', fontWeight: 600, fontSize: '30px', lineHeight: 1.3 } });
    const answer = typedText(cfg.ai.answer, { fontWeight: 500, fontSize: '30px', lineHeight: 1.38, color: '#1D1F25' });
    Object.assign(answer.node.style, { alignSelf: 'flex-start', maxWidth: '86%', padding: '20px 28px', borderRadius: '30px 30px 30px 8px', background: '#F1F4FF' });
    const dots = S.mk('div', { style: { display: 'flex', gap: '10px' } }, [0, 1, 2].map(() => S.mk('span', { style: { width: '14px', height: '14px', borderRadius: '50%', background: S.c('blue'), display: 'block' } })));
    const panelW = S.portrait ? W * 0.92 : 900;
    const panel = S.mk('div', {
      style: {
        position: 'absolute', left: 0, top: 0, width: `${panelW}px`, boxSizing: 'border-box', padding: '30px', borderRadius: '44px', background: '#fff', display: 'flex', flexDirection: 'column', gap: '22px',
        boxShadow: '0 60px 120px rgba(0,30,90,.20), 0 12px 30px rgba(0,30,90,.12)', border: '2px solid rgba(14,32,53,.06)',
      },
    }, [aiHead, question, answer.node]);
    root.append(panel);
    const panelBox = panel.getBoundingClientRect();
    const rowH = [aiHead, question, answer.node].map((n) => n.getBoundingClientRect().height);
    panel.style.overflow = 'hidden';
    const dotsHost = S.mk('div', { style: { position: 'absolute', left: 0, top: 0 } }, [dots]);
    panel.append(dotsHost);

    const tiles = cfg.tools.map((tile, i) => {
      const node = buildTile(S, tile, TILE_COLORS[i % TILE_COLORS.length]);
      root.append(node);
      return { node, h: node.getBoundingClientRect().height };
    });
    const rowStep = Math.max(...tiles.slice(0, 2).map((t) => t.h)) + 22;

    const headY = S.portrait ? H * 0.17 : 168;
    const panelX = S.portrait ? (W - panelW) / 2 : 130;
    const panelY = headY + size * 1.3 + 40;
    const gridX = S.portrait ? (W - 720) / 2 : 1090;
    const gridY = S.portrait ? panelY + panelBox.height + 40 : panelY + 10;

    return {
      update(lt, t) {
        applyPush(S, root, lt, dur, { exit: false });

        const lead = outExpo(seg(lt, -0.05, 0.5));
        const chipE = spring(0.5, 15)(seg(lt, 0.12, 0.7));
        const dotE = outExpo(seg(lt, 0.34, 0.4));
        place(head.node, { x: (W - hb.width) / 2, y: headY });
        place(head.lead, { y: (1 - lead) * 60, o: lead });
        place(head.chip, { y: (1 - chipE) * 40, s: 0.55 + 0.45 * chipE, o: Math.min(1, chipE * 2.2) });
        place(head.dot, { y: (1 - dotE) * 40, o: dotE });

        const panelE = outExpo(seg(lt, 0.25, 0.6));
        place(panel, { x: panelX, y: panelY + (1 - panelE) * 110, s: 0.96 + 0.04 * panelE, o: panelE });
        const grow1 = outExpo(seg(lt, 0.5, 0.45));
        const grow2 = outExpo(seg(lt, 1.25, 0.45));
        panel.style.height = `${60 + rowH[0] + grow1 * (rowH[1] + 22) + grow2 * (rowH[2] + 22)}px`;
        const qE = spring(0.6, 14)(seg(lt, 0.6, 0.55));
        place(question, { y: (1 - qE) * 30, s: 0.9 + 0.1 * qE, o: Math.min(1, qE * 2.4) });

        const typing = seg(lt, 1.0, 0.3) * (1 - seg(lt, 1.35, 0.12));
        dots.style.opacity = typing.toFixed(3);
        [...dots.children].forEach((d, i) => {
          d.style.transform = `translateY(${-Math.abs(Math.sin(t * 9 + i * 0.7)) * 10}px)`;
        });
        const aE = spring(0.6, 14)(seg(lt, 1.3, 0.5));
        place(answer.node, { y: (1 - aE) * 24, o: Math.min(1, aE * 2.4) });
        answer.set(seg(lt, 1.4, 1.35));
        place(dotsHost, { x: 34, y: 30 + rowH[0] + 22 + rowH[1] + 22 + 26 });

        tiles.forEach((tile, i) => {
          const e = spring(0.55, 13)(seg(lt, 0.95 + i * 0.22, 0.8));
          const col = i % 2;
          const row = Math.floor(i / 2);
          const float = Math.sin(t * 1.5 + i * 1.7) * 7;
          place(tile.node, { x: gridX + col * 370, y: gridY + row * rowStep + float + (1 - e) * 160, rz: (1 - e) * (col ? 8 : -8), s: 0.5 + 0.5 * e, o: Math.min(1, e * 2.2) });
        });
      },
    };
  },
};
