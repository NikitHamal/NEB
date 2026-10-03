import { el, icon } from './dom.js';
import { graphemes } from './text.js';

export function makeChip(S, { text, ic, fg, bg, size, weight = 800, ls = -0.04 }) {
  const parts = [];
  if (ic) parts.push(icon(ic, { style: { fontSize: `${size * 0.72}px`, color: fg, marginRight: `${size * 0.18}px` } }));
  parts.push(el('span', { text, style: { color: fg } }));
  return el('div', {
    style: {
      display: 'inline-flex', alignItems: 'center', whiteSpace: 'nowrap', fontWeight: weight, fontSize: `${size}px`, letterSpacing: `${ls}em`,
      lineHeight: 1, background: bg, borderRadius: `${size * 0.3}px`, padding: `${size * 0.16}px ${size * 0.3}px ${size * 0.2}px`,
    },
  }, parts);
}

export function headlineRow(S, { lead, chip, size, ink, fg, bg, ic }) {
  const leadEl = el('div', { text: lead, style: { fontSize: `${size}px`, fontWeight: 800, letterSpacing: '-0.052em', color: ink, lineHeight: 1 } });
  const chipEl = makeChip(S, { text: chip, ic, fg, bg, size: size * 0.85 });
  const dotEl = el('div', { text: '.', style: { fontSize: `${size}px`, fontWeight: 800, color: ink, lineHeight: 1, marginLeft: `${-size * 0.04}px` } });
  const node = el('div', {
    style: { position: 'absolute', left: 0, top: 0, display: 'flex', alignItems: 'center', gap: `${size * 0.14}px`, whiteSpace: 'nowrap' },
  }, [leadEl, chipEl, dotEl]);
  return { node, lead: leadEl, chip: chipEl, dot: dotEl };
}

function skeleton(S, w, h) {
  const rows = [];
  for (let i = 0; i < 12; i += 1) {
    rows.push(el('div', { style: { width: `${w * 0.3}px`, height: `${h * 0.14}px`, borderRadius: '16px', background: i % 2 ? '#E7E9ED' : '#DDE3F3', display: 'inline-block', margin: '12px' } }));
  }
  return el('div', { style: { width: `${w}px`, padding: '24px' } }, rows);
}

export function browserFrame(S, { w, h, image, url, barH = 68 }) {
  const dots = ['#FF5F57', '#FEBC2E', '#28C840'].map((c) => el('span', { style: { width: '17px', height: '17px', borderRadius: '50%', background: c, display: 'inline-block' } }));
  const urlPill = el('div', {
    text: url,
    style: { marginLeft: '18px', flex: 1, maxWidth: `${w * 0.5}px`, height: '38px', lineHeight: '38px', borderRadius: '19px', background: '#fff', color: '#525663', fontWeight: 500, fontSize: '20px', padding: '0 20px', border: '1px solid rgba(14,32,53,.08)' },
  });
  const bar = el('div', { style: { height: `${barH}px`, flex: 'none', background: '#EFF0F3', display: 'flex', alignItems: 'center', gap: '10px', padding: '0 26px', borderBottom: '1px solid rgba(14,32,53,.08)' } }, [...dots, urlPill]);
  const view = el('div', { style: { position: 'relative', flex: 1, overflow: 'hidden', background: '#F3F4F6' } });
  let page;
  let pageH = h * 2;
  if (image) {
    const scale = Math.min(1, (w * 1.6) / image.naturalWidth);
    const canvas = el('canvas', { width: Math.round(image.naturalWidth * scale), height: Math.round(image.naturalHeight * scale) });
    canvas.getContext('2d').drawImage(image, 0, 0, canvas.width, canvas.height);
    canvas.style.cssText = `display:block;width:${w}px;height:${(w * canvas.height) / canvas.width}px`;
    page = canvas;
    pageH = (w * canvas.height) / canvas.width;
  } else {
    page = skeleton(S, w, h);
  }
  page.style.position = 'absolute';
  page.style.left = '0';
  page.style.top = '0';
  view.append(page);
  const node = el('div', {
    style: {
      position: 'absolute', left: 0, top: 0, width: `${w}px`, height: `${h}px`, borderRadius: '30px', background: '#fff', overflow: 'hidden',
      display: 'flex', flexDirection: 'column', boxShadow: '0 70px 130px rgba(0,30,90,.30), 0 14px 36px rgba(0,30,90,.16)', border: '2px solid rgba(255,255,255,.95)',
    },
  }, [bar, view]);
  return { node, page, range: Math.max(0, pageH - (h - barH)) };
}

const hueOf = (subject) => (window.NebArt?.subjectHue ? window.NebArt.subjectHue(subject) : 220);

export function libraryCard(S, { subject, seed, type, title, meta, w = 560 }) {
  const artH = w * 0.5;
  const hue = hueOf(subject);
  const art = el('div', {
    class: 'neb-art', 'data-neb-art': 'banner', 'data-neb-subject': subject, 'data-neb-seed': seed,
    style: { position: 'relative', width: `${w}px`, height: `${artH}px`, overflow: 'hidden' },
  });
  const pill = el('div', {
    text: type.toUpperCase(),
    style: { position: 'absolute', left: `${w * 0.035}px`, top: `${w * 0.035}px`, zIndex: 2, background: 'rgba(255,255,255,.92)', color: '#1D1F25', fontWeight: 700, fontSize: `${w * 0.04}px`, letterSpacing: '0.06em', padding: `${w * 0.012}px ${w * 0.03}px`, borderRadius: '8px' },
  });
  art.append(pill);
  const chip = el('div', {
    text: subject.toUpperCase(),
    style: { alignSelf: 'flex-start', fontWeight: 700, fontSize: `${w * 0.037}px`, letterSpacing: '0.05em', padding: `${w * 0.01}px ${w * 0.026}px`, borderRadius: '8px', color: `hsl(${hue},70%,32%)`, background: `hsl(${hue},85%,93%)` },
  });
  const heading = el('div', { text: title, style: { fontWeight: 700, fontSize: `${w * 0.058}px`, lineHeight: 1.25, color: '#1D1F25', letterSpacing: '-0.01em' } });
  const foot = el('div', { text: meta, style: { fontWeight: 500, fontSize: `${w * 0.04}px`, color: '#6B707D' } });
  const info = el('div', { style: { display: 'flex', flexDirection: 'column', gap: `${w * 0.028}px`, padding: `${w * 0.045}px ${w * 0.05}px ${w * 0.05}px` } }, [chip, heading, foot]);
  const node = el('div', {
    style: {
      position: 'absolute', left: 0, top: 0, width: `${w}px`, background: '#fff', borderRadius: `${w * 0.05}px`, overflow: 'hidden',
      border: '2px solid rgba(14,32,53,.08)', boxShadow: '0 30px 60px rgba(0,30,90,.20), 0 8px 20px rgba(0,30,90,.12)',
    },
  }, [art, info]);
  return { node, w };
}

export function avatar(S, name, size) {
  const svg = window.Blobatar ? window.Blobatar.blobatar(name, { size }) : '';
  return el('div', {
    html: svg,
    style: { width: `${size}px`, height: `${size}px`, borderRadius: '50%', background: '#fff', overflow: 'hidden', border: '3px solid #fff', boxShadow: '0 8px 22px rgba(0,30,90,.20)', boxSizing: 'border-box', flex: 'none' },
  });
}

export function typedText(text, style) {
  const chars = graphemes(text).map((ch) => el('span', { text: ch, style: { opacity: 0 } }));
  const node = el('div', { style: { whiteSpace: 'normal', ...style } }, chars);
  let shown = 0;
  return {
    node,
    set(progress) {
      const n = Math.round(Math.max(0, Math.min(1, progress)) * chars.length);
      if (n === shown) return;
      const lo = Math.min(n, shown);
      const hi = Math.max(n, shown);
      for (let i = lo; i < hi; i += 1) chars[i].style.opacity = i < n ? 1 : 0;
      shown = n;
    },
  };
}
