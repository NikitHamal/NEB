import { seg } from './tl.js';
import { outExpo, inExpo, inOutCubic } from './ease.js';
import { place, show, icon } from './dom.js';
import { buildLogo } from './logo.js';
import { textWidth } from './text.js';
import { lerp, clamp } from './math.js';
import { mixHex } from './color.js';

function makePill(S, items) {
  const fs = S.portrait ? 24 : 27;
  const padX = fs * 1.05;
  const inner = 8;
  const h = fs * 2.5;
  const widths = items.map((t) => textWidth(t, { weight: 600, size: fs }) + padX * 2);
  const xs = [];
  let acc = inner;
  widths.forEach((w) => {
    xs.push(acc);
    acc += w;
  });
  const total = acc + inner;
  const hi = S.mk('div', { style: { position: 'absolute', top: `${inner}px`, left: 0, height: `${h}px`, borderRadius: '999px', background: S.c('blueWash') } });
  const labels = items.map((text, i) => S.mk('div', {
    text,
    style: { position: 'absolute', top: `${inner}px`, left: `${xs[i]}px`, width: `${widths[i]}px`, height: `${h}px`, lineHeight: `${h}px`, textAlign: 'center', fontWeight: 600, fontSize: `${fs}px`, color: S.c('muted'), whiteSpace: 'nowrap' },
  }));
  const node = S.mk('div', {
    style: {
      position: 'absolute', left: 0, top: 0, width: `${total}px`, height: `${h + inner * 2}px`, borderRadius: '999px', background: 'rgba(255,255,255,.88)',
      border: '2px solid rgba(14,32,53,.09)', boxShadow: '0 12px 34px rgba(0,40,120,.14)', boxSizing: 'border-box',
    },
  }, [hi, ...labels]);
  return { node, xs, widths, hi, labels, width: total, height: h + inner * 2 };
}

export function makeChrome(S) {
  const cfg = S.spec.chrome;
  if (!cfg) return null;
  const { W, bd } = S;
  const hd = S.header;
  const root = S.mk('div', { class: 'fill' });
  S.layers.chrome.append(root);

  const logo = buildLogo(S, S.assets.logoSvg, hd.logoH);
  const logoBox = S.mk('div', { style: { position: 'absolute', left: 0, top: 0, width: `${logo.width}px`, height: `${hd.logoH}px` } }, [logo.svg]);
  const wordSize = hd.logoH * 0.62;
  const word = S.mk('div', {
    text: S.spec.brand.name,
    style: { position: 'absolute', left: 0, top: 0, fontWeight: 800, letterSpacing: '-0.045em', color: S.c('blue'), fontSize: `${wordSize}px`, lineHeight: 1, whiteSpace: 'nowrap' },
  });
  const pills = { nav: makePill(S, cfg.nav), tabs: makePill(S, cfg.tabs) };
  const ctaSize = S.portrait ? 24 : 27;
  const ctaIcon = icon('smartphone', { style: { fontSize: `${ctaSize * 1.15}px`, marginRight: `${ctaSize * 0.4}px` } });
  const cta = S.mk('div', {
    style: { position: 'absolute', left: 0, top: 0, display: 'flex', alignItems: 'center', whiteSpace: 'nowrap', background: S.c('blue'), color: '#fff', fontWeight: 700, fontSize: `${ctaSize}px`, padding: `${ctaSize * 0.78}px ${ctaSize * 1.25}px`, borderRadius: '999px', boxShadow: '0 12px 30px rgba(0,74,198,.32)' },
  }, [ctaIcon, S.mk('span', { text: cfg.cta })]);
  root.append(logoBox, word, pills.nav.node, pills.tabs.node, cta);
  const ctaBox = cta.getBoundingClientRect();

  const top = hd.top;
  const pillY = top - pills.nav.height / 2;
  const pillX = (W - pills.nav.width) / 2;
  const tabsX = (W - pills.tabs.width) / 2;
  const ctaX = W - hd.pad - ctaBox.width;

  const stops = cfg.active.map((a) => ({ ...a, t: a.beat * bd, index: cfg[a.group === 'nav' ? 'nav' : 'tabs'].indexOf(a.item) }));
  const from = cfg.from * bd;
  const to = cfg.to * bd;
  const lastNav = stops.filter((s) => s.group === 'nav').slice(-1)[0];
  const firstTabs = stops.find((s) => s.group === 'tabs');

  function state(t) {
    let i = 0;
    while (i + 1 < stops.length && t >= stops[i + 1].t - 0.14) i += 1;
    const cur = stops[i];
    const prev = stops[Math.max(0, i - 1)];
    const k = i === 0 ? 1 : inOutCubic(seg(t, cur.t - 0.14, 0.5));
    return { cur, prev, k };
  }

  function drawPill(name, px, opacity, activeFloat, enter, drop) {
    const pill = pills[name];
    show(pill.node, opacity > 0.01);
    place(pill.node, { x: px, y: pillY + drop + (1 - opacity) * -18, o: opacity * enter });
    const lo = Math.floor(activeFloat);
    const hiIndex = Math.min(pill.xs.length - 1, lo + 1);
    const f = activeFloat - lo;
    pill.hi.style.width = `${lerp(pill.widths[lo], pill.widths[hiIndex], f)}px`;
    place(pill.hi, { x: lerp(pill.xs[lo], pill.xs[hiIndex], f), y: 0 });
    pill.labels.forEach((label, i) => {
      label.style.color = mixHex(S.c('muted'), S.c('blue'), clamp(1 - Math.abs(activeFloat - i)));
    });
  }

  return {
    update(t) {
      const on = t >= from - 0.02 && t < to + 0.5;
      show(root, on);
      if (!on) return;
      const enter = outExpo(seg(t, from + 0.04, 0.55));
      const enterCta = outExpo(seg(t, from + 0.18, 0.55));
      const leave = inExpo(seg(t, to - 0.36, 0.4));
      const drop = -(1 - enter) * 140 - leave * 160;
      place(logoBox, { x: hd.pad, y: top - hd.logoH / 2 - leave * 160 });
      place(word, { x: hd.pad + logo.width + hd.logoH * 0.13, y: top - wordSize / 2 - leave * 160 });
      place(cta, { x: ctaX, y: top - ctaBox.height / 2 - (1 - enterCta) * 140 - leave * 160, o: enterCta });

      const { cur, prev, k } = state(t);
      const swap = cur.group !== prev.group ? k : 1;
      const navOn = cur.group === 'nav' ? swap : 1 - swap;
      const tabsOn = cur.group === 'tabs' ? swap : 1 - swap;
      const navFloat = cur.group === 'nav' ? lerp(prev.group === 'nav' ? prev.index : cur.index, cur.index, k) : lastNav.index;
      const tabsFloat = cur.group === 'tabs' ? lerp(prev.group === 'tabs' ? prev.index : cur.index, cur.index, k) : firstTabs.index;
      drawPill('nav', pillX, navOn, navFloat, enter, drop);
      drawPill('tabs', tabsX, tabsOn, tabsFloat, enter, drop);
    },
  };
}
