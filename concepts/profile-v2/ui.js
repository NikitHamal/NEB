// Small render helpers. Every screen below is composed from these, so the four profile types share one vocabulary.
const poly = (n, a, ph = 0) => {
  const pts = [];
  for (let i = 0; i < 120; i++) {
    const t = (i / 120) * Math.PI * 2, r = 50 - (a * 50 * (1 - Math.cos(n * t + ph))) / 2;
    pts.push(`${(50 + r * Math.cos(t)).toFixed(2)}% ${(50 + r * Math.sin(t)).toFixed(2)}%`);
  }
  return `polygon(${pts.join(',')})`;
};
const SHAPES = { cookie: poly(9, .09), sunny: poly(8, .15), clover: poly(4, .34, Math.PI / 4), burst: poly(12, .17), gem: poly(6, .16), squircle: poly(4, .06, Math.PI / 4), flower: poly(6, .3) };
window.shape = k => `clip-path:${SHAPES[k] || SHAPES.cookie}`;
window.avatar = (letter, tone = 1, size = '', sh = 'cookie') => `<div class="av ${size} t${tone}" style="${shape(sh)}">${letter}</div>`;
window.chip = (t, c = '', i = '') => `<span class="chip ${c}">${i ? ic(i) : ''}${t}</span>`;
window.verified = () => `<span class="vf" title="Verified">${ic('verified')}</span>`;
window.mh = (title, icon, to, label = 'See all') => `<div class="mh"><h3>${icon ? ic(icon) : ''}${title}</h3>${to ? `<button data-go="${to}">${label}${ic('chev', 'xs')}</button>` : ''}</div>`;
window.mod = (title, icon, to, body, label) => `<section class="mod">${mh(title, icon, to, label)}${body}</section>`;
window.stat = (v, l, d) => `<div class="stat"><b>${v}</b><small>${l}</small>${d ? `<span class="d">${ic('trend', 'xs')}${d}</span>` : ''}</div>`;
window.stats = (a, cols = 4) => `<div class="${cols === 3 ? 'grid3' : 'grid4'}">${a.map(x => stat(...x)).join('')}</div>`;
window.bar = pct => `<div class="bar-t"><i style="width:${pct}%"></i></div>`;
window.card = (body, c = '') => `<div class="card ${c}">${body}</div>`;
window.res = r => `<div class="res"><div class="ft ${r.k || ''}">${r.t}</div><div class="tx"><h4>${r.n}</h4><small>${r.m}</small></div><button class="read">${ic('book', 'xs')}Read</button></div>`;
window.resCard = r => `<div class="rc"><div class="row"><div class="ft ${r.k || ''}">${r.t}</div><div class="tx"><small>${r.sub}</small></div></div><h4>${r.n}</h4><div class="foot"><span>${r.m}</span><button class="read t">${ic('book', 'xs')}Read</button></div></div>`;
window.post = p => `<article class="pc-post">${p.pin ? `<div class="pin">${ic('pin', 'xs')}Pinned</div>` : ''}<div class="row">${avatar(p.l, p.tone || 1, 'xs', p.sh)}<div class="tx"><b class="ell" style="font-size:.78rem">${p.by}</b><small>${p.time}</small></div>${chip(p.tag, 'sm')}</div><h4>${p.h}</h4><p>${p.b}</p><div class="ft2"><span>${ic('heart', 'xs')}${p.up}</span><span>${ic('chat', 'xs')}${p.c}</span>${p.solved ? chip('Solved', 'g sm', 'check') : ''}<span style="margin-left:auto">${ic('bm', 'xs')}</span></div></article>`;
window.reply = r => `<article class="pc-post"><div class="pin">${ic('reply', 'xs')}Replied in <b style="color:var(--on);font-weight:600">${r.in}</b></div><div class="quote">${r.q}</div><p style="-webkit-line-clamp:4;color:var(--on)">${r.b}</p><div class="ft2"><span>${ic('heart', 'xs')}${r.up}</span>${r.tag ? chip(r.tag, (r.tc || 'g') + ' sm', 'check') : ''}<span style="margin-left:auto">${r.time}</span></div></article>`;
window.tl = a => `<div class="tl">${a.map(x => `<div class="${x.now ? 'now' : ''}"><span class="yr">${x.y}</span><b>${x.t}</b><small>${x.s}</small></div>`).join('')}</div>`;
window.person = (p, btn = 'Follow') => `<div class="row">${avatar(p.l, p.tone, 'md', p.sh)}<div class="tx"><b class="ell">${p.n}${p.v ? ' ' + verified() : ''}</b><small class="ell">${p.s}</small></div><button class="btn t" style="height:34px;padding:0 14px;font-size:.74rem">${btn}</button></div>`;
window.empty = (icon, t, s, sh = 'clover') => `<div class="empty"><div class="tile" style="${shape(sh)}">${ic(icon)}</div><b>${t}</b><p>${s}</p></div>`;
window.locked = t => `<div class="lockrow">${ic('lock', 's')}${t}</div>`;
window.bars = (a, hi) => `<div class="bars">${a.map((v, i) => `<i class="${i === hi ? 'hi' : ''}" style="height:${v}%;animation-delay:${i * 40}ms"></i>`).join('')}</div>`;
window.strength = (pct, steps) => card(`<div class="row"><div class="tx"><b style="font-size:.92rem">Profile strength</b><small>${steps.filter(s => s[1]).length} of ${steps.length} done. Complete profiles get more follows.</small></div><b style="font-size:1.3rem;font-weight:600">${pct}%</b></div><div style="margin-top:12px">${bar(pct)}</div><div class="steps">${steps.map(([t, d, to]) => `<div class="st ${d ? '' : 'todo'}"><span class="tick">${d ? ic('check') : ''}</span>${t}${d ? '' : `<em><button data-go="${to}" style="color:var(--p);font-weight:600">Add</button></em>`}</div>`).join('')}</div>`, 'pc strength');
