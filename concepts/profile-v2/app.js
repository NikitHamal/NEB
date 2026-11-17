// Board logic: renders the phones, keeps tabs, the sliding pill, the collapsing top bar and the board controls.
const KEYS = ['student', 'teacher', 'institution', 'contributor'];
const state = { type: (location.hash || '').slice(1) || 'all', self: false, theme: matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light' };
const motif = p => `<div class="m" style="right:-36px;top:-26px;width:176px;height:176px;${shape(p.sh === 'squircle' ? 'flower' : p.sh)}"></div><div class="m" style="right:112px;top:82px;width:64px;height:64px;${shape('cookie')};opacity:.07"></div><div class="m" style="left:-24px;top:70px;width:92px;height:92px;${shape('clover')};opacity:.06"></div>`;
const actions = (p, self) => self
  ? `<button class="btn t">${ic('edit', 's')}Edit profile</button><button class="btn t ib" aria-label="Share">${ic('share', 's')}</button>`
  : `<button class="btn f" data-follow>${ic('plus', 's')}<span>Follow</span></button><button class="btn t ib" aria-label="Message">${ic(p.label === 'Institution' ? 'phone' : 'chat', 's')}</button>`;
function phoneHtml(key, self) {
  const p = PROFILES[key], tabs = p.tabs(self);
  const letters = p.letter.length > 1 ? 'style="font-size:1.55rem;' + shape(p.sh).slice(0) + '"' : `style="${shape(p.sh)}"`;
  return `<div class="phone" data-key="${key}"><div class="dev" data-stuck="0"><div class="sb"><span>9:41</span><i></i><span>100%</span></div><div class="scr">
  <div class="top"><button class="iconbtn" aria-label="Back">${ic('back')}</button><div class="mini">${avatar(p.letter, p.tone, 'xs', p.sh)}<b>${p.name}</b></div><span style="flex:1"></span><button class="iconbtn" aria-label="Share">${ic('share')}</button><button class="iconbtn" aria-label="More">${ic('more')}</button></div>
  <div class="cover" style="--cv:var(--${p.cv});--cvon:var(--on${p.cv})">${motif(p)}</div>
  <div class="hd"><div class="hd-top"><div class="av t${p.tone}" ${letters}>${p.letter}</div><div class="acts">${actions(p, self)}</div></div>
   <div class="nm"><h2>${p.name}</h2>${p.v ? verified() : ''}</div>
   <div class="sub"><span>${p.handle}</span><span class="role">${ic(p.role[1])}${p.role[0]}</span></div>
   <p class="hl">${p.headline}</p>
   <div class="meta">${p.meta.map(m => `<span>${ic(m[0], 'xs')}${m[1]}</span>`).join('')}</div>
   <div class="nums">${p.nums.map(n => `<button><b>${n[0]}</b><small>${n[1]}</small></button>`).join('')}</div>
   <div class="strip"><span class="lbl">${p.strip[0]}</span>${p.strip[1].map(c => chip(c[0], c[1], c[2])).join('')}</div></div>
  <div class="rail"><div class="rail-in" role="tablist"><span class="pill"></span>${tabs.map((t, i) => `<button role="tab" data-tab="${t[0]}" aria-selected="${i === 0}">${t[4] ? ic('lock') : ''}${t[1]}${t[3] ? `<span class="n">${t[3]}</span>` : ''}</button>`).join('')}</div></div>
  <div class="pane"></div></div></div></div>`;
}
function select(ph, id, jump) {
  const key = ph.dataset.key, p = PROFILES[key], scr = ph.querySelector('.scr'), rail = ph.querySelector('.rail-in');
  const btn = rail.querySelector(`[data-tab="${id}"]`); if (!btn) return;
  rail.querySelectorAll('[role=tab]').forEach(b => b.setAttribute('aria-selected', b === btn));
  const pill = rail.querySelector('.pill'); pill.style.width = btn.offsetWidth + 'px'; pill.style.transform = `translateX(${btn.offsetLeft}px)`;
  rail.scrollTo({ left: btn.offsetLeft - 28, behavior: 'smooth' });
  const pane = ph.querySelector('.pane'); pane.style.animation = 'none'; void pane.offsetWidth; pane.style.animation = '';
  pane.innerHTML = (p.panes[id](state.self) || []).filter(Boolean).join('');
  const top = ph.querySelector('.rail').offsetTop - 84;
  if (jump || scr.scrollTop > top) scr.scrollTo({ top, behavior: 'smooth' });
}
function mount() {
  const stage = document.getElementById('stage'), keys = state.type === 'all' ? KEYS : [state.type];
  stage.className = 'stage' + (keys.length === 1 ? ' one' : '');
  stage.innerHTML = keys.map(k => `<div class="slot"><div class="cap">${PROFILES[k].label} profile <i>${state.self ? 'your own view' : 'visitor view'}</i></div>${phoneHtml(k, state.self)}</div>`).join('');
  stage.querySelectorAll('.phone').forEach(ph => {
    const dev = ph.querySelector('.dev'), scr = ph.querySelector('.scr');
    scr.addEventListener('scroll', () => { dev.dataset.stuck = scr.scrollTop > 130 ? '1' : '0'; }, { passive: true });
    ph.addEventListener('click', e => {
      const t = e.target.closest('[data-tab]'), g = e.target.closest('[data-go]'), f = e.target.closest('[data-follow]');
      if (t) select(ph, t.dataset.tab); else if (g) select(ph, g.dataset.go, true);
      if (f) { const on = f.classList.toggle('on'); f.innerHTML = ic(on ? 'check' : 'plus', 's') + `<span>${on ? 'Following' : 'Follow'}</span>`; }
    });
    select(ph, 'overview');
  });
}
function sync() {
  document.documentElement.dataset.theme = state.theme;
  document.querySelectorAll('[data-type]').forEach(b => b.setAttribute('aria-pressed', b.dataset.type === state.type));
  document.querySelectorAll('[data-self]').forEach(b => b.setAttribute('aria-pressed', (b.dataset.self === '1') === state.self));
}
document.addEventListener('click', e => {
  const t = e.target.closest('[data-type]'), s = e.target.closest('[data-self]'), th = e.target.closest('#theme');
  if (t) { state.type = t.dataset.type; history.replaceState(null, '', '#' + state.type); sync(); mount(); }
  if (s) { state.self = s.dataset.self === '1'; sync(); mount(); }
  if (th) { state.theme = state.theme === 'dark' ? 'light' : 'dark'; sync(); }
});
sync(); mount();
if (document.fonts) document.fonts.ready.then(() => document.querySelectorAll('.phone').forEach(ph => select(ph, ph.querySelector('[aria-selected=true]').dataset.tab)));
