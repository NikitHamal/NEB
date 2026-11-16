/* Pathways (web). Same five sections as the Android screens: Explore, Study, Exams, Guides, Plan.
   Data: /api/pathways/ (schema in docs/PATHWAYS_SCHEMA.md). Optional fields hide their UI when missing. */
(function () {
  'use strict';
  const root = document.getElementById('pw-root');
  if (!root) return;

  /* ---------- utilities ---------- */
  const $ = (s, r = root) => r.querySelector(s);
  const $$ = (s, r = root) => [...r.querySelectorAll(s)];
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const LS = (k, d) => { try { const v = localStorage.getItem('pw2-' + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } };
  const put = (k, v) => { try { localStorage.setItem('pw2-' + k, JSON.stringify(v instanceof Set ? [...v] : v)); } catch (e) {} };
  const uniq = a => [...new Set(a)];
  const MN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const NOW = new Date().getMonth() + 1, YEAR = new Date().getFullYear();
  const EDU = ['Class 8', 'SEE', '+2', 'Bachelor', 'Master'];
  const GROUPS = { school: 'School', tech: 'Engineering and IT', sci: 'Science', health: 'Health', biz: 'Business', arts: 'Arts and media', edu: 'Education', law: 'Law', ag: 'Agriculture', gov: 'Government', abroad: 'Abroad' };
  const TONE = { tech: 'pc', sci: 'pc', arts: 'tc', law: 'tc', biz: 'yc', edu: 'yc', gov: 'yc', health: 'gc', ag: 'gc', abroad: 'gc' };
  const tone = g => TONE[g] || 'sc';
  const TONES = ['pc', 'tc', 'yc', 'gc', 'rc'];
  const PROV = ['Koshi', 'Madhesh', 'Bagmati', 'Gandaki', 'Lumbini', 'Karnali', 'Sudurpashchim'];
  const DP = {};
  [
    'Bhojpur Dhankuta Ilam Jhapa Khotang Morang Okhaldhunga Panchthar Sankhuwasabha Solukhumbu Sunsari Taplejung Terhathum Udayapur',
    'Bara Dhanusha Mahottari Parsa Rautahat Saptari Sarlahi Siraha',
    'Bhaktapur Chitwan Dhading Dolakha Kathmandu Kavrepalanchok Lalitpur Makwanpur Nuwakot Ramechhap Rasuwa Sindhuli Sindhupalchok',
    'Baglung Gorkha Kaski Lamjung Manang Mustang Myagdi Nawalparasi_East Parbat Syangja Tanahu',
    'Arghakhanchi Banke Bardiya Dang Gulmi Kapilvastu Nawalparasi_West Palpa Pyuthan Rolpa Rukum_East Rupandehi',
    'Dailekh Dolpa Humla Jajarkot Jumla Kalikot Mugu Rukum_West Salyan Surkhet',
    'Achham Baitadi Bajhang Bajura Dadeldhura Darchula Doti Kailali Kanchanpur',
  ].forEach((l, i) => l.split(' ').forEach(d => { DP[d.replace('_', ' ')] = i; }));

  const trim = x => (Math.round(x * 10) / 10).toString().replace(/\.0$/, '');
  const money = n => n >= 1e7 ? trim(n / 1e7) + ' crore' : n >= 1e5 ? trim(n / 1e5) + ' lakh' : n >= 1e3 ? trim(n / 1e3) + 'k' : String(Math.round(n || 0));
  const npr = n => n > 0 ? 'NPR ' + money(n) : 'Free';
  const pct = v => v >= 1 && v <= 5 ? v * 20 : Math.max(0, Math.min(100, +v || 0));
  const years = s => { const m = String(s || '').match(/\d+(\.\d+)?/); if (!m) return 0; return /month/i.test(s) ? m[0] / 12 : +m[0]; };
  const yr = y => !y ? '' : y < 1 ? Math.round(y * 12) + ' mo' : trim(y) + ' yr';
  const short = n => (String(n).split(' (')[0].split(' / ')[0].trim()) || n;
  const inWin = (a, b, m) => a <= b ? m >= a && m <= b : m >= a || m <= b;
  const winLabel = (a, b) => inWin(a, b, NOW) ? 'Closes ' + MN[b - 1] : 'Opens ' + MN[a - 1];
  const until = (a, b) => inWin(a, b, NOW) ? -1 : (a - NOW + 12) % 12;
  const monthsIn = t => MN.map((m, i) => new RegExp('\\b' + m, 'i').test(t || '') ? i + 1 : 0).filter(Boolean);
  const eduOf = need => {
    const t = String(need || '').toLowerCase();
    if (t.includes('master')) return 4;
    if (/bachelor|graduate|degree/.test(t)) return 3;
    if (/\+2|plus two|class 12|higher secondary/.test(t)) return 2;
    if (/\bsee\b|\bslc\b|class 10/.test(t)) return 1;
    return 0;
  };
  const ageOf = a => { const n = String(a || '').match(/\d+/g) || []; return n.length >= 2 ? [+n[0], +n[1], +(n[2] || n[1])] : null; };
  const ageText = a => { const x = ageOf(a); return x ? (x[2] > x[1] ? `${x[0]} to ${x[1]}, women ${x[2]}` : `${x[0]} to ${x[1]}`) : a; };

  /* ---------- state ---------- */
  const S = {
    view: 'explore', stage: '', group: '', course: null, career: null, sel: null, open: false, back: [],
    tabs: { route: 'overview', career: 'pay', exam: 'stages' }, cmp: null, trail: [], q: '', lens: '',
    study: 'colleges', cc: '', prov: -1, dist: '', sector: 'All', ab: '', scope: 'All', slvl: 'All', schC: '', schOpen: '',
    track: '', gcat: 'All', faqTopic: '', faqOpen: '', plan: 'plan', mstage: '', exp: 3, cpriv: 0, live: 0, aid: 0,
    edu: LS('edu', 2), age: LS('age', 17), woman: LS('woman', 0), abmax: LS('abmax', 60), mb: LS('mb', 15), hrs: LS('hrs', 3),
  };
  const SETS = {};
  ['saved', 'done', 'docs', 'have', 'mi', 'ms', 'mp'].forEach(k => { SETS[k] = new Set(LS(k, [])); });
  const tog = (k, v) => { const s = SETS[k]; s.has(v) ? s.delete(v) : s.add(v); put(k, s); };
  const has = (k, v) => SETS[k].has(v);
  let district = ''; try { district = localStorage.getItem('pw-district') || ''; } catch (e) {}

  /* ---------- data ---------- */
  let D = null;
  const R = {}, K = {}, P = {}, G = {}, GD = {}, SC = {}, AB = {}, KR = {};
  function index(d) {
    D = d;
    ['routes', 'careers', 'providers', 'scholarships', 'abroad', 'govt', 'guides', 'faq', 'topics', 'govt_tracks', 'stages'].forEach(k => { D[k] = D[k] || []; });
    D.routes.forEach(r => { R[r.id] = r; r.careers = r.careers || []; r.where = r.where || []; r.next = r.next || []; r.skills = r.skills || []; });
    D.careers.forEach(k => { K[k.id] = k; });
    D.providers.forEach(p => { P[p.id] = p; });
    D.govt.forEach(g => { G[g.id] = g; });
    D.guides.forEach(g => { GD[g.id] = g; });
    D.scholarships.forEach(s => { SC[s.id] = s; });
    D.abroad.forEach(a => { AB[a.id] = a; });
    D.routes.forEach(r => r.careers.forEach(k => { (KR[k] = KR[k] || []).push(r); }));
    D.maxSenior = Math.max(1, ...D.careers.map(k => (k.salary.senior[0] + k.salary.senior[1]) / 2));
    const st = D.stages.find(s => s.id === 'after12') || D.stages[0];
    S.stage = st ? st.id : '';
  }
  function met(r) {
    if (r._m) return r._m;
    const cs = r.careers.map(id => K[id]).filter(Boolean);
    const av = f => cs.length ? cs.reduce((s, k) => s + f(k), 0) / cs.length : 0;
    r._m = {
      d: r.demand ? pct(r.demand) : cs.length ? Math.round(av(k => pct(k.demand))) : 50,
      c: r.competition ? pct(r.competition) : cs.length ? Math.round(av(k => pct(k.competition))) : 50,
      lo: av(k => k.salary.entry[0]), hi: av(k => k.salary.entry[1]),
      sr: av(k => (k.salary.senior[0] + k.salary.senior[1]) / 2), ab: Math.round(av(k => pct(k.abroad))), y: years(r.years),
    };
    return r._m;
  }
  const payAt = (k, y) => {
    const e = (k.salary.entry[0] + k.salary.entry[1]) / 2, s = (k.salary.senior[0] + k.salary.senior[1]) / 2, m = e + (s - e) * 0.45;
    return y <= 5 ? e + (m - e) * y / 5 : m + (s - m) * Math.min(1, (y - 5) / 7);
  };
  const whyNot = g => {
    const need = eduOf(g.need);
    if (S.edu < need) return 'Needs ' + EDU[need];
    const a = ageOf(g.age); if (!a) return '';
    const mx = S.woman ? a[2] : a[1];
    return S.age < a[0] || S.age > mx ? `Age ${a[0]} to ${mx}` : '';
  };
  const odds = g => {
    if (!(g.seats > 0 && g.applicants > 0)) return null;
    const r = g.applicants / g.seats;
    if (r >= 20) { const n = Math.round(r); return { t: '1 in ' + n, big: n, pre: '1 in', post: '', r }; }
    const n = Math.min(100, Math.round(100 / r)); return { t: n + ' in 100', big: n, pre: '', post: 'in 100', r };
  };
  const prepHours = g => g.prep_hours || [500, 500, 700, 900, 900][eduOf(g.need)];

  /* ---------- matching: interests and strengths weigh most, then priorities, budget and demand ---------- */
  const INT = [['build', 'Building'], ['heal', 'Healing'], ['num', 'Numbers'], ['ppl', 'People'], ['make', 'Creating'], ['law', 'Justice'], ['nature', 'Nature'], ['serve', 'Serving']];
  const STR = [['math', 'Maths'], ['sci', 'Science'], ['bio', 'Biology'], ['lang', 'Languages'], ['biz', 'Business'], ['comp', 'Computers'], ['art', 'Art']];
  const PRI = [['pay', 'Pay'], ['demand', 'Demand'], ['ease', 'Easy entry'], ['cost', 'Low cost'], ['abroad', 'Abroad'], ['near', 'Near me']];
  const IG = { build: 'tech sci', heal: 'health', num: 'biz sci tech', ppl: 'edu biz arts gov', make: 'arts tech', law: 'law gov', nature: 'ag sci', serve: 'gov edu health' };
  const SG = { math: 'tech sci biz', sci: 'sci tech health ag', bio: 'health ag', lang: 'arts law edu gov', biz: 'biz', comp: 'tech', art: 'arts' };
  const HINT = { comp: ['program', 'computer', 'coding', 'software', 'data'], math: ['math', 'statist', 'account'], bio: ['biology', 'anatomy', 'patient', 'clinical'], lang: ['english', 'writing', 'nepali', 'communication'], art: ['design', 'drawing', 'creative'], biz: ['finance', 'account', 'market', 'sales'] };
  function match(stage) {
    const pool = D.routes.filter(r => r.stage === stage);
    if (!pool.length) return [];
    const maxSr = Math.max(1, ...pool.map(r => met(r).sr)), maxFee = Math.max(1, ...pool.map(r => r.fee[0])), budget = S.mb * 1e5;
    const mi = [...SETS.mi], ms = [...SETS.ms], mp = [...SETS.mp];
    return pool.map(r => {
      const m = met(r), tags = new Set(r.tags || []), text = (r.skills.join(' ') + ' ' + r.name + ' ' + (r.about || '')).toLowerCase();
      const iHit = mi.filter(i => tags.has(i) || (IG[i] || '').split(' ').includes(r.group)).length;
      const sHit = ms.filter(s => tags.has(s) || (SG[s] || '').split(' ').includes(r.group) || (HINT[s] || []).some(w => text.includes(w))).length;
      const interest = !mi.length ? 0.5 : !iHit ? 0 : 0.6 + 0.4 * iHit / mi.length;
      const strength = !ms.length ? 0.5 : !sHit ? 0.1 : 0.7 + 0.3 * sHit / ms.length;
      const fit = r.fee[1] <= budget ? 1 : r.fee[0] <= budget ? 0.4 + 0.6 * (budget - r.fee[0]) / Math.max(1, r.fee[1] - r.fee[0]) : Math.max(0, 0.3 * (1 - (r.fee[0] - budget) / Math.max(1, r.fee[0])));
      const near = !!district && r.where.some(id => P[id] && P[id].district === district);
      const pr = { pay: m.sr / maxSr, demand: m.d / 100, ease: 1 - m.c / 100, cost: 1 - r.fee[0] / maxFee, abroad: m.ab / 100, near: near ? 1 : 0 };
      const ps = mp.length ? mp.reduce((s, k) => s + pr[k], 0) / mp.length : (pr.demand + pr.pay) / 2;
      const score = Math.max(1, Math.min(99, Math.round(100 * (0.36 * interest + 0.18 * strength + 0.16 * fit + 0.22 * ps + 0.08 * m.d / 100))));
      const why = [];
      if (mi.length && interest >= 0.6) why.push('Interests');
      if (ms.length && strength >= 0.7) why.push('Strengths');
      if (fit >= 1) why.push('In budget');
      mp.filter(k => pr[k] >= 0.7).forEach(k => why.push(PRI.find(p => p[0] === k)[1]));
      return { r, score, why: why.slice(0, 3) };
    }).sort((a, b) => b.score - a.score).slice(0, 8);
  }

  /* ---------- pieces ---------- */
  const I = n => `<span class="material-symbols-outlined" aria-hidden="true">${n}</span>`;
  const shape = n => {
    let p = '';
    for (let i = 0; i < 96; i++) { const t = i / 96 * Math.PI * 2, r = 50 * (0.89 + 0.11 * Math.cos(n * t)); p += (i ? 'L' : 'M') + (50 + r * Math.cos(t)).toFixed(1) + ' ' + (50 + r * Math.sin(t)).toFixed(1); }
    return `<svg class="pw-shape" viewBox="0 0 100 100" aria-hidden="true"><path d="${p}Z"/></svg>`;
  };
  const ring = (v, l, cls = '') => `<div class="pw-ring ${cls}"><svg viewBox="0 0 44 44"><circle class="tr" cx="22" cy="22" r="18"/><circle class="fg" cx="22" cy="22" r="18" pathLength="100" style="stroke-dashoffset:${100 - v}"/></svg><b>${v}</b>${l ? `<span>${l}</span>` : ''}</div>`;
  const sig = v => { const n = v >= 75 ? 3 : v >= 50 ? 2 : 1; return `<svg class="pw-sig" viewBox="0 0 14 14" aria-hidden="true">${[0, 1, 2].map(i => `<rect x="${i * 5}" y="${9 - i * 4}" width="3.6" height="${5 + i * 4}" rx="1.2" class="${i < n ? 'f' : ''}"/>`).join('')}</svg>`; };
  const months = (f, cls = '') => `<div class="pw-mo ${cls}">${MN.map((m, i) => `<i class="${f(i + 1) ? 'f' : ''}${i + 1 === NOW ? ' now' : ''}">${m[0]}</i>`).join('')}</div>`;
  const cal = rows => rows.length ? `<div class="pw-cal">${rows.map(([l, f]) => `<span>${l}</span>${months(f)}`).join('')}</div>` : '';
  const examCal = g => cal([...(g.apply && g.apply.length === 2 ? [['Apply', m => inWin(g.apply[0], g.apply[1], m)]] : []), ...(g.exam_month ? [['Exam', m => m === g.exam_month]] : [])]);
  const seg = (list, v, a, cls = '') => `<div class="pw-seg ${cls}">${list.map(([k, n]) => `<button type="button" class="${String(k) === String(v) ? 'on' : ''}" data-a="${a}" data-v="${esc(k)}">${esc(n)}</button>`).join('')}</div>`;
  const chips = (list, on, a, cls = '') => `<div class="pw-chips ${cls}">${list.map(([k, n]) => `<button type="button" class="pw-chip ${on(k) ? 'on' : ''}" data-a="${a}" data-v="${esc(k)}">${esc(n)}</button>`).join('')}</div>`;
  const facts = l => l.length ? `<div class="pw-facts">${l.map(([a, b]) => `<div><small>${esc(a)}</small><b>${esc(b)}</b></div>`).join('')}</div>` : '';
  const h4 = t => `<h4 class="pw-h4">${esc(t)}</h4>`;
  const big = (b, s) => `<div class="pw-big"><b>${esc(b)}</b>${s ? `<span>${esc(s)}</span>` : ''}</div>`;
  const empty = t => `<div class="pw-empty">${shape(6)}<p>${esc(t)}</p></div>`;
  const bar = (f, start = 0) => `<div class="pw-bar"><i style="left:${start * 100}%;width:${Math.max(0, Math.min(1, f)) * 100}%"></i></div>`;
  const row = (a, v, t, s, tr, extra = '', cls = '') => `<button type="button" class="pw-row ${cls}" data-a="${a}" data-v="${esc(v)}"><span class="pw-row-h"><span><b>${esc(t)}</b>${s ? `<small>${esc(s)}</small>` : ''}</span>${tr ? `<em>${esc(tr)}</em>` : ''}</span>${extra}</button>`;
  const outline = t => `<span class="pw-ol">${esc(t)}</span>`;
  function split(parts, f = v => Math.round(v) + '%') {
    const ps = (parts || []).filter(p => p[1] > 0);
    if (!ps.length) return '';
    return `<div class="pw-split"><div class="pw-sbar">${ps.map((p, i) => `<button type="button" class="k${i % 7}" style="flex:${p[1]}" data-a="spot" data-v="${i}" aria-label="${esc(p[0])}"></button>`).join('')}</div>
      <div class="pw-sleg">${ps.map((p, i) => `<button type="button" class="k${i % 7}" data-a="spot" data-v="${i}"><i></i><span>${esc(p[0])}</span><b>${esc(f(p[1]))}</b></button>`).join('')}</div></div>`;
  }
  function steps(items, ck) {
    return `<div class="pw-steps">${items.map(([t, s, tr], i) => {
      const k = ck ? ck(i) : null, done = k && has('done', k);
      return `<${ck ? 'button type="button"' : 'div'} class="pw-step ${ck ? 'ck' : ''} ${done ? 'done' : ''}" style="--i:${i}" ${ck ? `data-a="step" data-v="${esc(k)}"` : ''}><b><i>${i + 1}</i>${I('check')}</b><span>${esc(t)}${s ? `<small>${esc(s)}</small>` : ''}</span>${tr ? `<em>${esc(tr)}</em>` : ''}</${ck ? 'button' : 'div'}>`;
    }).join('')}</div>`;
  }
  const saveBtn = key => `<button type="button" class="pw-ib ${has('saved', key) ? 'on' : ''}" data-a="save" data-v="${esc(key)}" aria-label="Save">${I('bookmark')}</button>`;
  const hero = (t, key, title, sub, badge) => `<header class="pw-hero t-${t}"><div class="pw-hero-r"><button type="button" class="pw-ib x" data-a="close" aria-label="Back">${I('arrow_back')}</button>${key ? saveBtn(key) : ''}</div>
    <div class="pw-hero-b"><div><h2>${esc(title)}</h2>${sub ? `<p>${esc(sub)}</p>` : ''}</div><div class="pw-badge">${badge}</div></div></header>`;
  const badge = (n, inner) => `${shape(n)}<div>${inner}</div>`;
  const meters = (d, c, b, s) => `<div class="pw-meters">${ring(d, 'Demand')}${ring(c, 'Competition', 'ink')}${b ? `<div class="pw-pay"><b id="pw-payb">${esc(b)}</b><span id="pw-pays">${esc(s)}</span></div>` : '<span></span>'}</div>`;
  const tabs = (kind, list) => `<div class="pw-chips pw-tabs">${list.map(([k, n]) => `<button type="button" class="pw-chip ${S.tabs[kind] === k ? 'on' : ''}" data-a="tab" data-v="${k}">${n}</button>`).join('')}</div>`;
  const acts = btns => btns.filter(Boolean).length ? `<div class="pw-acts">${btns.filter(Boolean).join('')}</div>` : '';
  const btn = (a, v, label, icon, filled) => `<button type="button" class="pw-btn ${filled ? 'f' : ''}" data-a="${a}" data-v="${esc(v)}">${icon ? I(icon) : ''}${esc(label)}</button>`;

  /* ---------- Explore ---------- */
  const stageObj = () => D.stages.find(s => s.id === S.stage) || D.stages[0];
  const stageShort = l => String(l).replace(/^After (a )?/i, '').replace(/^\w/, c => c.toUpperCase());
  function trailHTML(st) {
    if (!S.trail.length && !S.course && !S.career) return '';
    const items = S.trail.map((id, i) => R[id] && `<button type="button" class="pw-tc" data-a="trail" data-v="${i}">${esc(short(R[id].name))}</button>`).filter(Boolean);
    items.push(`<button type="button" class="pw-tc" data-a="home">${esc(st.label)}</button>`);
    if (S.course && R[S.course]) items.push(`<button type="button" class="pw-tc on" data-a="focus" data-v="route:${S.course}">${esc(short(R[S.course].name))}</button>`);
    if (S.career && K[S.career]) items.push(`<button type="button" class="pw-tc on" data-a="focus" data-v="career:${S.career}">${esc(K[S.career].name)}</button>`);
    return `<div class="pw-trail">${items.join('<i class="pw-sep"></i>')}</div>`;
  }
  const V = {};
  V.explore = () => {
    const st = stageObj();
    if (!st) return empty('Nothing here yet');
    S.stage = st.id;
    const inS = D.routes.filter(r => r.stage === st.id), groups = uniq(inS.map(r => r.group));
    if (!groups.includes(S.group)) S.group = groups[0] || '';
    const cs = inS.filter(r => r.group === S.group), ks = uniq(cs.flatMap(r => r.careers)).filter(id => K[id]);
    const hint = new Set(S.trail.length ? (R[S.trail[S.trail.length - 1]] || {}).next || [] : []);
    const node = (kind, id, label, sv, i) => `<button type="button" class="pw-nd ${kind}${hint.has(id) ? ' hint' : ''}" style="--i:${i}" data-a="${kind === 'c' ? 'course' : 'career'}" data-v="${esc(id)}"><i class="fl"></i>${sv != null ? sig(sv) : ''}<span>${esc(label)}</span><small></small></button>`;
    return `${trailHTML(st)}
      <div class="pw-stages">${D.stages.map(s => `<button type="button" class="pw-stage ${s.id === st.id ? 'on' : ''}" data-a="stage" data-v="${esc(s.id)}">${esc(stageShort(s.label))}</button>`).join('')}</div>
      <div class="pw-groups">${groups.map(g => `<button type="button" class="t-${tone(g)} ${g === S.group ? 'on' : ''}" data-a="group" data-v="${esc(g)}">${esc(GROUPS[g] || g)}</button>`).join('')}</div>
      <div class="pw-lens">${[['demand', 'Demand'], ['pay', 'Pay'], ['odds', 'Odds']].map(([k, n]) => `<button type="button" class="pw-chip sm ${S.lens === k ? 'on' : ''}" data-a="lens" data-v="${k}">${n}</button>`).join('')}</div>
      <div class="pw-flow" id="pw-flow"><svg class="pw-links" id="pw-links" aria-hidden="true"></svg>
        <div class="pw-col">${cs.map((r, i) => node('c', r.id, short(r.name), null, i)).join('')}</div>
        <div class="pw-col">${ks.map((id, i) => node('k', id, K[id].name, pct(K[id].demand), i + 2)).join('')}</div>
      </div><div class="pw-peek" id="pw-peek"></div>`;
  };
  function paint() {
    const f = $('#pw-flow'); if (!f) return;
    const c = S.course, k = S.career, any = c || k, cc = c && R[c] ? R[c].careers : [];
    const cs = id => c ? (id === c ? 2 : 0) : k && R[id] && R[id].careers.includes(k) ? 1 : 0;
    const ks = id => k ? (id === k ? 2 : 0) : cc.includes(id) ? 1 : 0;
    const set = (e, v) => { e.classList.toggle('on', v === 2); e.classList.toggle('lit', v === 1); e.classList.toggle('dim', !!any && !v); };
    $$('.pw-nd.c', f).forEach(e => set(e, cs(e.dataset.v)));
    $$('.pw-nd.k', f).forEach(e => set(e, ks(e.dataset.v)));
    const maxPay = Math.max(1, ...$$('.pw-nd', f).map(e => e.classList.contains('c') ? met(R[e.dataset.v]).hi : K[e.dataset.v].salary.entry[1]));
    $$('.pw-nd', f).forEach(e => {
      const isC = e.classList.contains('c'), o = isC ? R[e.dataset.v] : K[e.dataset.v], m = isC ? met(o) : null;
      const d = isC ? m.d : pct(o.demand), cp = isC ? m.c : pct(o.competition), pay = isC ? m.hi : o.salary.entry[1];
      let w = 0, t = '';
      if (S.lens === 'demand') { w = d; t = d; } else if (S.lens === 'odds') { w = 100 - cp; t = 100 - cp; } else if (S.lens === 'pay') { w = pay / maxPay * 100; t = pay ? money(pay) : ''; }
      e.style.setProperty('--w', w + '%'); $('small', e).textContent = t;
    });
    drawLinks(); peek();
  }
  // only the selection is drawn, so the map stays calm until the student asks a question
  function drawLinks() {
    const f = $('#pw-flow'), svg = $('#pw-links'); if (!f || !svg) return;
    const box = f.getBoundingClientRect(), c = S.course, k = S.career, out = [];
    const at = sel => { const e = $(sel, f); if (!e) return null; const b = e.getBoundingClientRect(); return { l: b.left - box.left, r: b.right - box.left, y: b.top - box.top + b.height / 2 }; };
    const pair = (cid, kid) => {
      const A = at(`.pw-nd.c[data-v="${CSS.escape(cid)}"]`), B = at(`.pw-nd.k[data-v="${CSS.escape(kid)}"]`); if (!A || !B) return;
      const m = (A.r + B.l) / 2; out.push(`<path pathLength="1" d="M${A.r} ${A.y}C${m} ${A.y} ${m} ${B.y} ${B.l} ${B.y}"/>`);
    };
    if (c && R[c]) R[c].careers.forEach(kid => { if (!k || kid === k) pair(c, kid); });
    else if (k) $$('.pw-nd.c', f).forEach(e => { if (R[e.dataset.v].careers.includes(k)) pair(e.dataset.v, k); });
    svg.setAttribute('viewBox', `0 0 ${box.width} ${box.height}`); svg.innerHTML = out.join('');
  }
  function peek() {
    const p = $('#pw-peek'); if (!p) return;
    const f = S.sel && (S.sel.t === 'route' || S.sel.t === 'career') ? S.sel : null;
    if (!f || wide()) { p.innerHTML = ''; return; }
    const r = f.t === 'route' ? R[f.id] : null, k = f.t === 'career' ? K[f.id] : null, o = r || k; if (!o) { p.innerHTML = ''; return; }
    const sub = r ? [r.kind, yr(met(r).y)].filter(Boolean).join(' · ') : `NPR ${money(k.salary.entry[0])} to ${money(k.salary.senior[1])} / month`;
    p.innerHTML = `<button type="button" class="pw-pk t-${r ? tone(r.group) : 'sc'}" data-a="open"><span><b>${esc(o.name)}</b><small>${esc(sub)}</small></span>${ring(r ? met(r).d : pct(k.demand), '', 'sm cur')}<i class="go">${I('arrow_forward')}</i></button>`;
  }

  /* ---------- Study ---------- */
  V.study = () => `${seg([['colleges', 'Colleges'], ['abroad', 'Abroad'], ['funding', 'Funding']], S.study, 'study', 'full')}${S.study === 'abroad' ? abroadHTML() : S.study === 'funding' ? fundingHTML() : collegesHTML()}`;
  function collegesHTML() {
    const pool = D.routes.filter(r => r.where.length);
    const r = R[[S.cc, S.course].find(id => id && R[id] && R[id].where.length)] || pool.find(x => x.stage === S.stage) || pool[0];
    if (!r) return empty('No colleges yet');
    S.cc = r.id;
    const near = uniq([r, ...pool.filter(x => x.stage === r.stage && x.group === r.group)]).slice(0, 24);
    const all = r.where.map(id => P[id]).filter(Boolean), counts = PROV.map((_, i) => all.filter(p => DP[p.district] === i).length);
    const inProv = all.filter(p => S.prov < 0 || DP[p.district] === S.prov), ds = uniq(inProv.map(p => p.district)).sort();
    if (!ds.includes(S.dist)) S.dist = '';
    const list = inProv.filter(p => (!S.dist || p.district === S.dist) && (S.sector === 'All' || p.sector === S.sector)).sort((a, b) => (a.sector === 'Public' ? 0 : 1) - (b.sector === 'Public' ? 0 : 1) || a.name.localeCompare(b.name));
    const maxFee = Math.max(1, ...all.map(p => p.fees && p.fees[r.id] ? p.fees[r.id][1] : 0));
    return `${chips(near.map(x => [x.id, short(x.name)]), id => id === r.id, 'cc')}
      <div class="pw-map">${PROV.map((n, i) => `<button type="button" class="p${i} ${S.prov === i ? 'on' : ''} ${counts[i] ? '' : 'nil'}" data-a="prov" data-v="${i}" ${counts[i] || S.prov === i ? '' : 'disabled'}><b>${counts[i]}</b><span>${n}</span></button>`).join('')}</div>
      ${ds.length > 1 ? chips(ds.map(d => [d, d]), d => d === S.dist, 'dist') : ''}
      ${seg([['All', 'All'], ['Public', 'Public'], ['Private', 'Private']], S.sector, 'sector', 'full')}
      <div class="pw-list">${list.map(p => {
        const fee = p.fees && p.fees[r.id];
        const sub = [p.place, p.district, p.seats ? p.seats + ' seats' : ''].filter(Boolean).filter((x, i, a) => a.indexOf(x) === i).join(' · ');
        const inner = `<span class="pw-row-h"><span><b>${esc(p.name)}</b><small>${esc(sub)}</small></span>${p.sector ? `<span class="pw-tag t-${p.sector === 'Public' ? 'gc' : 'tc'}">${esc(p.sector)}</span>` : ''}</span>${fee ? `<span class="pw-fee">${bar(fee[1] / maxFee)}<b>${esc(npr(fee[1]))}</b></span>` : ''}`;
        return p.website ? `<a class="pw-row" href="${esc(p.website)}" target="_blank" rel="noopener">${inner}</a>` : `<div class="pw-row">${inner}</div>`;
      }).join('') || empty('No colleges')}</div>`;
  }
  function abroadHTML() {
    const ordered = D.abroad.slice();
    return `<div class="pw-sl"><input type="range" id="pw-abmax" min="5" max="100" value="${S.abmax}" aria-label="Yearly budget in lakh"><output id="pw-abv">NPR ${S.abmax}L / yr</output></div>
      <div class="pw-cgrid">${ordered.map((a, i) => {
        const on = S.ab === a.id, cost = (a.tuition[0] + a.living[0]) / 1e5, ms = monthsIn(a.intakes);
        const fx = [['Tuition', money(a.tuition[0]) + ' to ' + money(a.tuition[1])], ['Living', money(a.living[0]) + ' to ' + money(a.living[1])]];
        if (a.work_hours > 0) fx.push(['Work', a.work_hours + ' h / week']);
        if (a.stay_back) fx.push(['Stay-back', a.stay_back]);
        if (a.visa_rate >= 0 && a.visa_rate != null) fx.push(['Visa rate', a.visa_rate + '%']);
        return `<div role="button" tabindex="0" class="pw-cc t-${TONES[i % 5]} ${on ? 'on' : ''} ${cost > S.abmax ? 'dim' : ''}" style="--i:${i}" data-a="ctry" data-v="${esc(a.id)}" data-cost="${cost}">
          <div class="pw-cb">${shape(i % 2 ? 8 : 6)}<b>${esc((a.code || a.country.slice(0, 2)).toUpperCase())}</b></div>
          <div class="pw-cco"><b>${esc(money(a.tuition[0] + a.living[0]).replace(' lakh', 'L'))}</b><small>per year</small></div>
          <div class="pw-cn">${esc(a.country)}</div>${ms.length ? months(m => ms.includes(m)) : ''}
          ${on ? `<div class="pw-more">${facts(fx)}${a.work ? `<p>${esc(a.work)}</p>` : ''}
            <div class="pw-chips w">${(a.exams || []).map(x => `<span class="pw-tchip s">${esc(x)}</span>`).join('')}${(a.fields || []).map(x => `<span class="pw-tchip">${esc(x)}</span>`).join('')}</div>
            ${(a.scholarships || []).length ? `<button type="button" class="pw-btn f" data-a="schc" data-v="${esc(a.id)}">Scholarships</button>` : ''}</div>` : ''}
        </div>`;
      }).join('')}</div>`;
  }
  const lvl = l => ({ phd: 'PhD', plus2: '+2' }[String(l).toLowerCase()] || String(l).replace(/^\w/, c => c.toUpperCase()));
  function fundingHTML() {
    const a = AB[S.schC], scopes = uniq(D.scholarships.map(s => s.scope).filter(Boolean)), levels = uniq(D.scholarships.flatMap(s => s.levels || [])).slice(0, 3);
    const list = D.scholarships.filter(s => (!a || (a.scholarships || []).includes(s.id) || s.country === a.id) && (S.scope === 'All' || s.scope === S.scope) && (S.slvl === 'All' || (s.levels || []).includes(S.slvl)))
      .sort((x, y) => ((x.open || []).length === 2 ? until(x.open[0], x.open[1]) : 99) - ((y.open || []).length === 2 ? until(y.open[0], y.open[1]) : 99) || x.name.localeCompare(y.name));
    const cl = [...(a ? [['x', a.country]] : []), ['All', 'All'], ...scopes.map(s => [s, lvl(s)])];
    return `${chips(cl, k => k === 'x' || k === S.scope, 'scope')}
      ${levels.length > 1 ? seg([['All', 'All'], ...levels.map(l => [l, lvl(l)])], S.slvl, 'slvl', 'full') : ''}
      <div class="pw-list">${list.map(s => {
        const w = (s.open || []).length === 2, live = w && inWin(s.open[0], s.open[1], NOW), open = S.schOpen === s.id, key = 'sch:' + s.id;
        return `<div role="button" tabindex="0" class="pw-srow ${live ? 'live' : ''} ${open ? 'open' : ''}" data-a="sch" data-v="${esc(s.id)}">
          <div class="pw-row-h"><span><b>${esc(s.name)}</b><small>${esc(s.by)}</small></span><em>${esc(w ? winLabel(s.open[0], s.open[1]) : (s.levels || []).map(lvl).join(', '))}</em></div>
          ${w ? months(m => inWin(s.open[0], s.open[1], m), live ? '' : 'soft') : ''}
          ${open ? `<div class="pw-sx">${[['Covers', s.covers], ['Who', s.who], ['How', s.how]].filter(x => x[1]).map(([k, v]) => `<div><small>${k}</small><p>${esc(v)}</p></div>`).join('')}
            <div class="pw-sxa"><b>${s.awards ? s.awards + ' awards' : ''}</b>${saveBtn(key)}${s.link ? `<a class="pw-btn" href="${esc(s.link)}" target="_blank" rel="noopener">${I('open_in_new')}Website</a>` : ''}</div></div>` : ''}
        </div>`;
      }).join('') || empty('No match')}</div>`;
  }

  /* ---------- Exams ---------- */
  V.exams = () => {
    const tracks = D.govt_tracks.filter(t => D.govt.some(g => g.track === t.id));
    if (!tracks.length) return empty('No exams yet');
    if (!tracks.some(t => t.id === S.track)) S.track = tracks[0].id;
    return `${seg(tracks.map(t => [t.id, t.label]), S.track, 'track', 'full')}
      ${chips([1, 2, 3, 4].map(i => [i, EDU[i]]), i => +i === S.edu, 'edu')}
      <div class="pw-ctl"><div class="pw-sl"><input type="range" id="pw-age" min="14" max="45" value="${S.age}" aria-label="Age"><output id="pw-agev">Age ${S.age}</output></div>${seg([[1, 'Woman'], [0, 'Man']], S.woman, 'woman')}</div>
      <div class="pw-list" id="pw-xlist">${xlist()}</div>`;
  };
  const xlist = () => D.govt.filter(g => g.track === S.track).map(g => [g, whyNot(g)]).sort((a, b) => !!a[1] - !!b[1]).map(([g, w]) => {
    const o = odds(g);
    return row('exam', g.id, g.name, w || g.level || g.body, o ? o.t : g.fee ? npr(g.fee) : '', '', `strong ${w ? 'no' : ''} ${S.sel && S.sel.t === 'exam' && S.sel.id === g.id && wide() ? 'cur' : ''}`);
  }).join('');

  /* ---------- Guides ---------- */
  const gdone = g => (g.steps || []).filter((_, i) => has('done', g.id + ':' + i)).length;
  const gcats = () => uniq(D.guides.map(g => g.cat));
  const gtone = c => ['pc', 'gc', 'yc', 'tc', 'sc', 'rc'][Math.max(0, gcats().indexOf(c)) % 6];
  V.guides = () => {
    let h = '';
    if (D.guides.length) {
      h += chips([['All', 'All'], ...gcats().map(c => [c, c])], c => c === S.gcat, 'gcat');
      h += `<div class="pw-ggrid">${D.guides.filter(g => S.gcat === 'All' || g.cat === S.gcat).map(g => {
        const n = (g.steps || []).length;
        return `<button type="button" class="pw-gd t-${gtone(g.cat)}" data-a="guide" data-v="${esc(g.id)}"><b>${esc(g.name)}</b><span class="pw-gp"><i style="width:${n ? gdone(g) / n * 100 : 0}%"></i></span><span class="pw-gm"><span>${n} steps</span><span>${(g.steps || []).reduce((a, s) => a + (+s[1] || 0), 0)} days</span></span></button>`;
      }).join('')}</div>`;
    }
    const topics = D.topics.filter(t => D.faq.some(f => f.topic === t.id));
    if (topics.length) {
      const cur = (topics.find(t => t.id === S.faqTopic) || topics[0]).id;
      h += h4('Questions') + chips(topics.map(t => [t.id, t.label]), id => id === cur, 'ftopic');
      h += `<div class="pw-list">${D.faq.filter(f => f.topic === cur).map(f => {
        const open = S.faqOpen === f.id;
        return `<div role="button" tabindex="0" class="pw-faq ${open ? 'open' : ''}" data-a="faq" data-v="${esc(f.id)}"><b>${esc(f.q)}</b>${open ? `<p>${esc(f.a)}</p>${(f.go || []).filter(id => R[id]).length ? `<div class="pw-chips w">${f.go.filter(id => R[id]).slice(0, 3).map(id => `<button type="button" class="pw-chip sm" data-a="goRoute" data-v="${esc(id)}">${esc(short(R[id].name))}</button>`).join('')}</div>` : ''}` : ''}</div>`;
      }).join('')}</div>`;
    }
    return h || empty('Guides are on the way');
  };

  /* ---------- Plan and Match ---------- */
  V.plan = () => `${seg([['plan', 'My plan'], ['match', 'Match']], S.plan, 'plan', 'full')}${S.plan === 'match' ? matchHTML() : `<p class="pw-mad">I am <output id="pw-pagev">${S.age}</output></p><input type="range" id="pw-page" min="13" max="40" value="${S.age}" aria-label="Age"><div id="pw-pout">${planOut()}</div>`}`;
  function matchHTML() {
    if (!D.stages.some(s => s.id === S.mstage)) S.mstage = S.stage;
    const pick = (t, k, list) => `<p class="pw-mad">${t}</p><div class="pw-chips w">${list.map(([id, n]) => `<button type="button" class="pw-chip ${has(k, id) ? 'on' : ''}" data-a="mset" data-v="${k}:${id}">${n}</button>`).join('')}</div>`;
    return `${chips(D.stages.map(s => [s.id, s.label]), id => id === S.mstage, 'mstage')}${pick('I enjoy', 'mi', INT)}${pick('I am strong in', 'ms', STR)}${pick('I care about', 'mp', PRI)}
      <p class="pw-mad">My budget is <output id="pw-mbv">NPR ${S.mb}L</output></p><input type="range" id="pw-mb" min="1" max="60" value="${S.mb}" aria-label="Budget in lakh"><div id="pw-mres" class="pw-mres"></div>`;
  }
  function renderMatch() {
    const box = $('#pw-mres'); if (!box) return;
    const old = {}; $$('.pw-mrow', box).forEach(e => { old[e.dataset.v] = e.offsetTop; });
    const l = match(S.mstage);
    box.innerHTML = l.map(({ r, score, why }) => `<button type="button" class="pw-mrow" data-a="goRoute" data-v="${esc(r.id)}">${ring(score, '', 'sm cur still')}<span><b>${esc(r.name)}</b><span class="pw-why">${why.map(w => `<i>${esc(w)}</i>`).join('')}</span></span>${I('arrow_forward')}</button>`).join('') || empty('No courses at this stage');
    $$('.pw-mrow', box).forEach(e => {
      const o = old[e.dataset.v]; if (!e.animate) return;
      if (o == null) e.animate([{ opacity: 0, transform: 'scale(.94)' }, { opacity: 1, transform: 'none' }], { duration: 320, easing: 'cubic-bezier(.2,0,0,1)' });
      else if (o !== e.offsetTop) e.animate([{ transform: `translateY(${o - e.offsetTop}px)` }, { transform: 'none' }], { duration: 500, easing: 'cubic-bezier(.34,1.56,.64,1)' });
    });
  }
  function planOut() {
    const route = uniq([...S.trail, S.course].filter(Boolean)).map(id => R[id]).filter(Boolean), h = [];
    if (route.length) {
      const last = route[route.length - 1], k = K[S.career && last.careers.includes(S.career) ? S.career : last.careers[0]];
      const ys = route.reduce((a, r) => a + met(r).y, 0), end = Math.ceil(S.age + ys);
      h.push(`<div class="pw-hl"><b>${esc((k || last).name)} at ${end}</b><div class="pw-tl">${route.map(r => `<button type="button" style="flex:${Math.max(0.5, met(r).y)}" data-a="goRoute" data-v="${esc(r.id)}"><span>${esc(short(r.name))}</span><small>${yr(met(r).y)}</small></button>`).join('')}<div class="end">${end}</div></div>
        ${facts([['Years', trim(ys)], ['Cost', money(route.reduce((a, r) => a + r.fee[0], 0)) + ' to ' + money(route.reduce((a, r) => a + r.fee[1], 0))], ...(k ? [['First pay', npr(k.salary.entry[0])]] : [])])}</div>`);
    }
    const dl = new Map();
    const addG = g => { if (g && g.apply && g.apply.length === 2) dl.set('exam:' + g.id, { n: g.name, s: g.apply[0], e: g.apply[1], a: 'exam', v: g.id }); };
    route.forEach(r => addG(G[r.exam_id]));
    SETS.saved.forEach(key => {
      const [t, id] = [key.slice(0, key.indexOf(':')), key.slice(key.indexOf(':') + 1)];
      if (t === 'exam') addG(G[id]);
      if (t === 'sch' && SC[id] && (SC[id].open || []).length === 2) dl.set(key, { n: SC[id].name, s: SC[id].open[0], e: SC[id].open[1], a: 'goSch', v: id });
    });
    const dls = [...dl.values()].sort((a, b) => until(a.s, a.e) - until(b.s, b.e));
    if (dls.length) h.push(h4('Deadlines') + dls.map(d => row(d.a, d.v, d.n, '', winLabel(d.s, d.e), months(m => inWin(d.s, d.e, m), inWin(d.s, d.e, NOW) ? '' : 'soft'))).join(''));
    const gs = D.guides.filter(g => has('saved', 'guide:' + g.id) || gdone(g));
    if (gs.length) h.push(h4('Guides') + gs.map(g => row('guide', g.id, g.name, '', `${gdone(g)} of ${(g.steps || []).length}`, bar(gdone(g) / Math.max(1, (g.steps || []).length)))).join(''));
    const sv = [...SETS.saved].map(key => {
      const t = key.slice(0, key.indexOf(':')), id = key.slice(key.indexOf(':') + 1);
      return t === 'route' && R[id] ? row('goRoute', id, R[id].name, '', 'Course') : t === 'career' && K[id] ? row('goCareer', id, K[id].name, '', 'Career') : t === 'exam' && G[id] ? row('exam', id, G[id].name, '', 'Exam') : '';
    }).join('');
    if (sv) h.push(h4('Saved') + sv);
    return h.join('') || empty('Nothing planned') + btn('nav', 'explore', 'Explore', 'arrow_forward', true);
  }

  /* ---------- Search ---------- */
  function searchHTML() {
    const w = S.q.toLowerCase().split(/\s+/).filter(x => x.length >= 2), hit = (...s) => { const t = s.join(' ').toLowerCase(); return w.every(x => t.includes(x)); }, out = [];
    D.routes.forEach(r => hit(r.name, r.kind, r.about) && out.push(row('goRoute', r.id, r.name, GROUPS[r.group] || r.group, 'Course')));
    D.careers.forEach(k => hit(k.name, k.about) && out.push(row('goCareer', k.id, k.name, `NPR ${money(k.salary.entry[0])} to ${money(k.salary.senior[1])} / month`, 'Career')));
    D.govt.forEach(g => hit(g.name, g.body, g.level) && out.push(row('goExam', g.id, g.name, g.body, 'Exam')));
    D.guides.forEach(g => hit(g.name, g.cat) && out.push(row('goGuide', g.id, g.name, g.cat, 'Guide')));
    D.providers.forEach(p => { if (hit(p.name, p.place, p.district)) { const r = D.routes.find(x => x.where.includes(p.id)); if (r) out.push(row('find', r.id, p.name, p.district, 'College')); } });
    D.scholarships.forEach(s => hit(s.name, s.by) && out.push(row('goSch', s.id, s.name, s.by, 'Scholarship')));
    D.abroad.forEach(a => hit(a.country) && out.push(row('goCountry', a.id, a.country, `NPR ${money(a.tuition[0] + a.living[0])} / year`, 'Country')));
    D.faq.forEach(f => hit(f.q) && out.push(row('goFaq', f.id, f.q, '', 'Question')));
    return `<div class="pw-list">${out.slice(0, 60).join('') || empty('No results')}</div>`;
  }

  /* ---------- detail sheets ---------- */
  const PANEL = {}, SHEET = {};
  SHEET.route = id => {
    const r = R[id]; if (!r) return '';
    const m = met(r), nx = r.next.map(x => R[x]).find(Boolean), ns = nx && D.stages.find(s => s.id === nx.stage);
    const [yn, yu] = m.y ? (m.y < 1 ? [Math.round(m.y * 12), 'months'] : [trim(m.y), m.y === 1 ? 'year' : 'years']) : [r.careers.length, 'careers'];
    return hero(tone(r.group), 'route:' + id, r.name, [r.kind, GROUPS[r.group]].filter(Boolean).join(' · '), badge(8, `<b>${yn}</b><small>${yu}</small>`))
      + meters(m.d, m.c, m.hi ? money(m.lo) + ' to ' + money(m.hi) : '', 'NPR / month to start')
      + tabs('route', [['overview', 'Overview'], ['careers', 'Careers'], ['cost', 'Cost'], ['entry', 'Entry'], ['compare', 'Compare']])
      + `<div class="pw-tabp" id="pw-tabp">${PANEL.route(id)}</div>`
      + acts([r.where.length && btn('find', id, 'Colleges', 'location_on', true), nx && btn('next', id, ns ? ns.label : 'Next', 'arrow_forward')]);
  };
  PANEL.route = id => {
    const r = R[id], m = met(r), t = S.tabs.route;
    if (t === 'careers') {
      const cs = r.careers.map(k => K[k]).filter(Boolean), mx = Math.max(1, ...cs.map(k => k.salary.senior[1]));
      return cs.map(k => row('goCareer', k.id, k.name, '', `${money(k.salary.entry[0])} to ${money(k.salary.senior[1])}`, bar((k.salary.senior[1] - k.salary.entry[0]) / mx, k.salary.entry[0] / mx))).join('') || empty('No careers listed');
    }
    if (t === 'cost') return seg([[0, 'Public'], [1, 'Private']], S.cpriv, 'cpriv', 'full') + seg([[0, 'Home'], [1, 'Hostel'], [2, 'Room']], S.live, 'live', 'full')
      + `<div class="pw-sl"><input type="range" id="pw-aid" min="0" max="100" step="10" value="${S.aid}" aria-label="Scholarship percent"><output id="pw-aidv">Aid ${S.aid}%</output></div><div id="pw-cost">${costOut(r)}</div>`;
    if (t === 'entry') {
      const g = G[r.exam_id];
      return `${r.entry ? `<div class="pw-need"><small>Needs</small><b>${esc(r.entry)}</b></div>` : ''}<div class="pw-tiles">
        ${r.exam ? `<${g ? 'button type="button" data-a="exam" data-v="' + esc(g.id) + '"' : 'div'} class="pw-tile"><small>Entrance</small><b>${esc(r.exam)}</b>${g ? I('arrow_forward') : ''}</${g ? 'button' : 'div'}>` : ''}
        ${m.y ? `<div class="pw-tile"><small>Duration</small><b>${yr(m.y)}</b></div>` : ''}</div>${g ? examCal(g) : ''}`;
    }
    if (t === 'compare') {
      const same = D.routes.filter(x => x.stage === r.stage && x.group === r.group && x.id !== r.id);
      const sib = [...same, ...D.routes.filter(x => x.stage === r.stage && x.id !== r.id && !same.includes(x))].slice(0, 12);
      if (!sib.length) return empty('Nothing to compare');
      const b = sib.find(x => x.id === S.cmp) || sib[0], mb = met(b);
      const rows = [['Demand', m.d, mb.d, ''], ['Competition', m.c, mb.c, ''], ['Start pay', (m.lo + m.hi) / 2000, (mb.lo + mb.hi) / 2000, 'k'], ['Fee', (r.fee[0] + r.fee[1]) / 2e5, (b.fee[0] + b.fee[1]) / 2e5, 'L'], ['Years', m.y, mb.y, '']];
      return chips(sib.map(x => [x.id, short(x.name)]), id => id === b.id, 'cmp') + `<div class="pw-bf"><div class="pw-bfh"><b>${esc(short(r.name))}</b><b>${esc(short(b.name))}</b></div>${rows.map(([l, a, v, u]) => {
        const mx = Math.max(a, v) || 1;
        return `<div class="pw-bfr"><span>${trim(a)}${u}</span><div class="a"><i style="width:${a / mx * 100}%"></i></div><em>${l}</em><div class="b"><i style="width:${v / mx * 100}%"></i></div><span class="vb">${trim(v)}${u}</span></div>`;
      }).join('')}</div>`;
    }
    return `${r.about ? `<p class="pw-p">${esc(r.about)}</p>` : ''}${(r.plan || []).length ? h4('Journey') + steps(r.plan.map(p => [p])) : ''}${r.skills.length ? h4('Skills') + `<div class="pw-chips w">${r.skills.map(outline).join('')}</div>` : ''}`;
  };
  function costOut(r) {
    const y = Math.max(1, met(r).y), t = (S.cpriv ? r.fee[1] : r.fee[0]) * (1 - S.aid / 100), l = [0, 18000, 12000][S.live] * 12 * y, b = 15000 * y, tot = t + l + b, m = met(r), avg = (m.lo + m.hi) / 2;
    return big(npr(tot), avg ? Math.round(tot / avg) + ' months of starting pay' : '') + split([['Tuition', t], ['Living', l], ['Books', b]], v => npr(v));
  }

  SHEET.career = id => {
    const k = K[id]; if (!k) return '';
    return hero('sc', 'career:' + id, k.name, `NPR ${money(k.salary.entry[0])} to ${money(k.salary.senior[1])} / month`, badge(5, sig(pct(k.demand))))
      + meters(pct(k.demand), pct(k.competition), ' ', '')
      + tabs('career', [['pay', 'Pay'], ['profile', 'Profile'], ['skills', 'Skills'], ['market', 'Market']])
      + `<div class="pw-tabp" id="pw-tabp">${PANEL.career(id)}</div>`;
  };
  const ladder = k => (k.ladder && k.ladder.length ? k.ladder : ['Entry', 'Mid-level', 'Senior', 'Lead']);
  const rungYears = k => ladder(k).map((_, i, a) => a.length > 1 ? Math.round(i * 12 / (a.length - 1)) : 0);
  PANEL.career = id => {
    const k = K[id], t = S.tabs.career;
    if (t === 'profile') {
      const ax = x => [['Pay', (x.salary.senior[0] + x.salary.senior[1]) / 2 / D.maxSenior * 100], ['Demand', pct(x.demand)], ['Entry', 100 - pct(x.competition)], ['Abroad', pct(x.abroad)],
        ...['stability', 'flexibility', 'growth'].filter(tr => k.traits && tr in k.traits).map(tr => [tr[0].toUpperCase() + tr.slice(1), (x.traits || {})[tr] || 50])];
      const mine = ax(k), avg = mine.map((_, i) => D.careers.reduce((s, x) => s + ax(x)[i][1], 0) / D.careers.length);
      return radar(mine.map(a => a[0]), mine.map(a => a[1]), avg) + ((k.day || []).length ? h4(k.hours ? `A ${k.hours}-hour week` : 'A week') + split(k.day) : '') + (k.about ? h4('About') + `<p class="pw-p">${esc(k.about)}</p>` : '');
    }
    if (t === 'skills') {
      const sk = (k.skills || []).length ? k.skills : uniq((KR[id] || []).flatMap(r => r.skills)).slice(0, 8), n = sk.filter(s => has('have', s)).length;
      const lic = k.licence, lg = lic && G[lic.exam];
      return `${sk.length ? `<div class="pw-rdy" id="pw-rdy">${ring(sk.length ? Math.round(n / sk.length * 100) : 0, 'Ready', 'still')}<div class="pw-chips w">${sk.map(s => `<button type="button" class="pw-chip ${has('have', s) ? 'on' : ''}" data-a="have" data-v="${esc(s)}">${esc(s)}</button>`).join('')}</div></div>` : ''}
        ${lic && lic.name ? h4('Licence') + (lg ? row('exam', lg.id, lic.name, lg.body, 'Exam') : `<div class="pw-row"><span class="pw-row-h"><span><b>${esc(lic.name)}</b></span></span></div>`) : ''}
        ${(KR[id] || []).length ? h4('Routes in') + `<div class="pw-chips w">${KR[id].map(r => `<button type="button" class="pw-chip" data-a="goRoute" data-v="${esc(r.id)}">${esc(short(r.name))}</button>`).join('')}</div>` : ''}`;
    }
    if (t === 'market') return h4('Demand, 5 years') + spark(k) + h4('Demand against competition') + scatter(k) + ((k.jobs || []).length ? h4('Where the jobs are') + split(k.jobs) : '') + ((k.employers || []).length ? h4('Employers') + `<div class="pw-chips w">${k.employers.map(outline).join('')}</div>` : '');
    const mx = Math.max(k.salary.senior[1], payAt(k, 12)), X = y => 10 + y * 25, Y = v => 122 - v / mx * 108;
    const line = [...Array(25)].map((_, i) => (i ? 'L' : 'M') + X(i / 2) + ' ' + Y(payAt(k, i / 2)).toFixed(1)).join('');
    const ry = rungYears(k);
    return `<svg class="pw-curve" viewBox="0 0 320 130" aria-hidden="true"><path d="${line}L310 128L10 128Z" class="area"/><path d="${line}" class="line"/><circle id="pw-dot" r="8"/></svg>
      <input type="range" id="pw-exp" min="0" max="12" value="${S.exp}" aria-label="Years of experience">
      <div class="pw-rungs">${ladder(k).map((n, i) => `<button type="button" class="pw-chip" data-a="rung" data-v="${ry[i]}">${esc(n)}</button>`).join('')}</div>`;
  };
  function updExp() {
    const s = S.sel; if (!s || s.t !== 'career' || !K[s.id]) return;
    const k = K[s.id], v = payAt(k, S.exp), ry = rungYears(k), ri = Math.max(0, ry.filter(y => y <= S.exp).length - 1);
    const b = $('#pw-payb'), t = $('#pw-pays'); if (b) b.textContent = 'NPR ' + money(v); if (t) t.textContent = (S.exp ? 'Year ' + S.exp : 'Entry') + ' · ' + ladder(k)[ri];
    const mx = Math.max(k.salary.senior[1], payAt(k, 12)), d = $('#pw-dot');
    if (d) { d.setAttribute('cx', 10 + S.exp * 25); d.setAttribute('cy', 122 - v / mx * 108); }
    const r = $('#pw-exp'); if (r && +r.value !== S.exp) r.value = S.exp;
    $$('.pw-rungs .pw-chip').forEach((e, i) => e.classList.toggle('on', i === ri));
  }
  function radar(labels, vals, avg) {
    const n = labels.length, pt = (v, i, R0 = 84) => { const a = (i * 360 / n - 90) * Math.PI / 180, r = R0 * v / 100; return [(160 + r * Math.cos(a)).toFixed(1), (120 + r * Math.sin(a)).toFixed(1)]; };
    const poly = vs => vs.map((v, i) => pt(v, i).join(',')).join(' ');
    return `<svg class="pw-radar" viewBox="0 0 320 240" aria-hidden="true">${[33, 66, 100].map(g => `<polygon class="grid" points="${poly(Array(n).fill(g))}"/>`).join('')}
      <polygon class="avg" points="${poly(avg)}"/><polygon class="me" points="${poly(vals)}"/>
      ${labels.map((t, i) => { const [x, y] = pt(100, i, 104); return `<text x="${x}" y="${+y + 4}" text-anchor="${Math.abs(x - 160) < 8 ? 'middle' : x > 160 ? 'start' : 'end'}">${esc(t)}</text>`; }).join('')}
      <circle class="avgdot" cx="14" cy="12" r="5"/><text x="24" y="16">Average</text></svg>`;
  }
  function spark(k) {
    const slope = { rising: 3, falling: -3 }[String(k.trend).toLowerCase()] || 0;
    const v = (k.history || []).length >= 2 ? k.history.map(pct) : [0, 1, 2, 3, 4, 5].map(i => Math.max(5, Math.min(99, pct(k.demand) - slope * (5 - i))));
    const lo = Math.min(...v) - 8, hi = Math.max(...v) + 8, px = i => 16 + i * 288 / (v.length - 1), py = a => 82 - (a - lo) / (hi - lo) * 64;
    const d = v.map((a, i) => (i ? 'L' : 'M') + px(i).toFixed(0) + ' ' + py(a).toFixed(1)).join('');
    return `<svg class="pw-plot" viewBox="0 0 320 106" aria-hidden="true"><path d="${d}L304 92L16 92Z" class="area"/><path d="${d}" class="line"/><circle class="me" cx="304" cy="${py(v[v.length - 1]).toFixed(1)}" r="6"/><text x="16" y="103">${YEAR - v.length + 1}</text><text x="304" y="103" text-anchor="end">${YEAR}</text></svg>`;
  }
  // ratings are whole steps, so a stable jitter per id keeps careers on the same step apart
  const jit = (s, m) => { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) | 0; return (Math.abs(h) % m) - (m >> 1); };
  const scatter = k => `<svg class="pw-plot" viewBox="0 0 320 190"><rect x="12" y="12" width="148" height="83" rx="16" class="good"/><text x="22" y="30">High demand, low competition</text><text x="308" y="182" text-anchor="end">Competition</text>
    ${D.careers.map(o => `<circle class="${o.id === k.id ? 'me' : ''}" data-a="goCareer" data-v="${esc(o.id)}" cx="${(16 + Math.max(0, Math.min(100, pct(o.competition) + jit(o.id, 13))) * 2.88).toFixed(0)}" cy="${(178 - Math.max(0, Math.min(100, pct(o.demand) + jit(o.id + 'd', 13))) * 1.66).toFixed(0)}" r="${o.id === k.id ? 10 : 5}"><title>${esc(o.name)}</title></circle>`).join('')}</svg>`;

  SHEET.exam = id => {
    const g = G[id]; if (!g) return '';
    const o = odds(g), ti = Math.max(0, D.govt_tracks.findIndex(t => t.id === g.track)), tl = [['stages', 'Stages']];
    if ((g.syllabus || []).length || (g.subjects || []).length) tl.push(['syllabus', 'Syllabus']);
    if (o) tl.push(['odds', 'Odds']);
    tl.push(['prepare', 'Prepare']);
    if ((g.ladder || []).length) tl.push(['ladder', 'Ladder']);
    if (!tl.some(t => t[0] === S.tabs.exam)) S.tabs.exam = 'stages';
    const f = [];
    if (g.seats) f.push(['Seats', money(g.seats)]);
    if (g.applicants) f.push(['Applicants', money(g.applicants)]);
    if (g.fee) f.push(['Fee', npr(g.fee)]);
    if (g.need) f.push(['Needs', eduOf(g.need) ? EDU[eduOf(g.need)] : g.need]);
    if (g.age) f.push(['Age', ageText(g.age)]);
    if (g.pay) f.push(['Starting pay', npr(g.pay)]);
    return hero(['yc', 'pc', 'gc', 'tc'][ti % 4], 'exam:' + id, g.name, g.body, badge(7, o ? `${o.pre ? `<small>${o.pre}</small>` : ''}<b>${o.big}</b>${o.post ? `<small>${o.post}</small>` : ''}` : `<b>${(g.stages || []).length}</b><small>stages</small>`))
      + `<div class="pw-pad">${facts(f)}${examCal(g)}</div>` + tabs('exam', tl) + `<div class="pw-tabp" id="pw-tabp">${PANEL.exam(id)}</div>`
      + acts([K[g.career] && btn('goCareer', g.career, K[g.career].name, 'arrow_forward', true)]);
  };
  PANEL.exam = id => {
    const g = G[id], t = S.tabs.exam;
    if (t === 'syllabus') return (g.syllabus || []).length ? split(g.syllabus) : `<div class="pw-chips w">${(g.subjects || []).map(outline).join('')}</div>`;
    if (t === 'odds') {
      const o = odds(g); if (!o) return '';
      const one = o.r >= 20, n = one ? Math.min(Math.round(o.r), 400) : 100, me = Math.floor(n * 0.37);
      return `<p class="pw-mad">${o.t}</p><div class="pw-waf">${[...Array(n)].map((_, i) => `<i class="${one ? (i === me ? 'me one' : '') : (i < o.big ? 'me' : '')}"></i>`).join('')}</div>${(g.quota || []).length ? h4('Seats by category') + split(g.quota) : ''}`;
    }
    if (t === 'prepare') return `<p class="pw-mad"><output id="pw-hrv">${S.hrs}</output> h a day</p><input type="range" id="pw-hrs" min="1" max="10" value="${S.hrs}" aria-label="Hours a day"><div id="pw-prep">${prepOut(g)}</div>${(g.prep || []).length ? h4('Checklist') + steps(g.prep.map(p => [p]), i => 'prep:' + id + ':' + i) : ''}`;
    if (t === 'ladder') {
      const n = g.ladder.length;
      return g.ladder.map((p, i) => `<div class="pw-rung ${i === g.rung ? 'on' : g.rung >= 0 && i < g.rung ? 'dim' : ''}" style="--w:${n > 1 ? 55 + 45 * i / (n - 1) : 100}%"><span>${esc(p[0])}</span>${p[1] ? `<b>${npr(p[1])}</b>` : ''}</div>`).reverse().join('');
    }
    return steps((g.stages || []).map(s => [s[0], s[1], s[2] || ''])) + (g.note ? `<p class="pw-p soft">${esc(g.note)}</p>` : '');
  };
  function prepOut(g) {
    const days = Math.ceil(prepHours(g) / S.hrs), sb = g.exam_month ? MN[((g.exam_month - 1 - Math.ceil(days / 30)) % 12 + 12) % 12] : '';
    const parts = (g.syllabus || []).length ? g.syllabus : (g.subjects || []).map(s => [s, 1]), tot = parts.reduce((a, p) => a + p[1], 0) || 1, mx = Math.max(1e-6, ...parts.map(p => p[1]));
    return big(days + ' days', sb ? 'Start by ' + sb : '') + (parts.length ? h4('Hours a week') + parts.map(([n, w]) => row('', '', n, '', trim(S.hrs * 7 * w / tot) + ' h', bar(w / mx), 'flat')).join('') : '');
  }

  SHEET.guide = id => {
    const g = GD[id]; if (!g) return '';
    const st = g.steps || [], n = st.length, d = gdone(g);
    return hero(gtone(g.cat), 'guide:' + id, g.name, g.cat, badge(6, `<b id="pw-gdone">${d}</b><small>of ${n}</small>`))
      + `<div class="pw-pad">${facts([['Time', st.reduce((a, s) => a + (+s[1] || 0), 0) + ' days'], ['Cost', npr(st.reduce((a, s) => a + (+s[2] || 0), 0))], ['Online', st.filter(s => s[3] === 'online' || s[3] === true).length + ' of ' + n]])}
        <div class="pw-gp lg"><i id="pw-gbar" style="width:${n ? d / n * 100 : 0}%"></i></div>
        ${steps(st.map(s => [s[0], [s[1] ? s[1] + ' days' : '', s[2] ? npr(s[2]) : '', s[3] === 'online' || s[3] === true ? 'Online' : 'In person'].filter(Boolean).join(' · ')]), i => id + ':' + i)}
        ${(g.docs || []).length ? h4('Documents') + `<div class="pw-chips w">${g.docs.map(x => `<button type="button" class="pw-chip ${has('docs', id + ':' + x) ? 'on' : ''}" data-a="doc" data-v="${esc(id + ':' + x)}">${esc(x)}</button>`).join('')}</div>` : ''}</div>`
      + acts([g.link && btn('link', g.link, { exam: 'Exam', route: 'Course', career: 'Career', guide: 'Guide' }[g.link.split(':')[0]] || 'Open', 'arrow_forward')]);
  };

  /* ---------- shell ---------- */
  const NAV = [['explore', 'route', 'Explore'], ['study', 'school', 'Study'], ['exams', 'task_alt', 'Exams'], ['guides', 'checklist', 'Guides'], ['plan', 'flag', 'Plan']];
  const wide = () => root.clientWidth >= 960;
  root.innerHTML = `<header class="pw-top"><h1 class="pw-title">Pathways</h1><label class="pw-search">${I('search')}<input id="pw-q" type="search" placeholder="Search" autocomplete="off" aria-label="Search Pathways"></label></header>
    <nav class="pw-nav" id="pw-nav" aria-label="Pathways sections"></nav>
    <div class="pw-body"><main class="pw-main" id="pw-main"><div class="pw-skel" aria-hidden="true"><i></i><i></i><i></i></div></main><aside class="pw-sheet" id="pw-sheet" aria-label="Details"></aside></div>`;
  const main = $('#pw-main'), sheet = $('#pw-sheet'), navEl = $('#pw-nav');
  let lastKey = '', freshT = 0;
  function renderNav() {
    navEl.innerHTML = NAV.map(([v, ic, n]) => `<button type="button" class="${S.view === v ? 'on' : ''}" data-a="nav" data-v="${v}" aria-label="${n}" title="${n}">${I(ic)}${v === 'plan' && SETS.saved.size ? `<i class="pw-cnt">${SETS.saved.size}</i>` : ''}</button>`).join('');
  }
  function renderMain() {
    const key = [S.q ? 'q' : '', S.view, S.stage, S.group, S.study, S.track, S.plan, S.gcat].join('|');
    if (key !== lastKey) { main.classList.add('fresh'); clearTimeout(freshT); freshT = setTimeout(() => main.classList.remove('fresh'), 900); lastKey = key; }
    main.innerHTML = S.q ? searchHTML() : V[S.view]();
    if (S.q) return;
    if (S.view === 'explore') paint();
    if (S.view === 'plan' && S.plan === 'match') renderMatch();
  }
  function renderSheet() {
    const s = S.sel, show = !!(s && SHEET[s.t] && (wide() || S.open));
    root.classList.toggle('has-sheet', !!(s && wide()));
    sheet.classList.toggle('open', show);
    document.documentElement.classList.toggle('pw-lock', show && !wide());
    sheet.innerHTML = s && SHEET[s.t] ? SHEET[s.t](s.id) : '';
    sheet.scrollTop = 0; updExp();
  }
  function repanel() { const s = S.sel, p = $('#pw-tabp'); if (s && p && PANEL[s.t]) { p.innerHTML = PANEL[s.t](s.id); updExp(); } }
  function render() { renderNav(); renderSheet(); renderMain(); }
  const setHash = () => { try { history.replaceState(null, '', '#' + S.view); } catch (e) {} };

  /* ---------- actions ---------- */
  const jump = () => { S.back.push({ view: S.view, sel: S.sel, open: S.open }); if (S.back.length > 10) S.back.shift(); };
  const leaveSearch = () => { S.q = ''; const q = $('#pw-q'); if (q) q.value = ''; };
  const focusRoute = id => { const r = R[id]; if (!r) return; S.stage = r.stage; S.group = r.group; S.course = id; if (S.career && !r.careers.includes(S.career)) S.career = null; S.sel = { t: 'route', id }; S.tabs.route = 'overview'; S.cmp = null; };
  const A = {
    nav(v) { S.view = v; S.sel = null; S.open = false; S.back = []; leaveSearch(); setHash(); render(); },
    stage(v) { S.stage = v; S.group = ''; S.course = S.career = S.sel = null; S.trail = []; render(); },
    group(v) { S.group = v; S.course = S.career = S.sel = null; render(); },
    home() { S.course = S.career = S.sel = null; render(); },
    lens(v) { S.lens = S.lens === v ? '' : v; $$('.pw-lens .pw-chip').forEach(b => b.classList.toggle('on', b.dataset.v === S.lens)); paint(); },
    course(v) {
      if (S.course === v) { S.course = null; S.sel = S.career ? { t: 'career', id: S.career } : null; }
      else { S.course = v; if (S.career && !R[v].careers.includes(S.career)) S.career = null; S.sel = { t: 'route', id: v }; S.tabs.route = 'overview'; S.cmp = null; }
      renderSheet(); paint(); const tr = $('.pw-trail'), nt = trailHTML(stageObj()); if (tr) tr.outerHTML = nt || ''; else if (nt) main.insertAdjacentHTML('afterbegin', nt);
    },
    career(v) {
      if (S.career === v) { S.career = null; S.sel = S.course ? { t: 'route', id: S.course } : null; }
      else { S.career = v; if (S.course && !R[S.course].careers.includes(v)) S.course = null; S.sel = { t: 'career', id: v }; S.exp = 3; }
      renderSheet(); paint(); const tr = $('.pw-trail'), nt = trailHTML(stageObj()); if (tr) tr.outerHTML = nt || ''; else if (nt) main.insertAdjacentHTML('afterbegin', nt);
    },
    focus(v) { const [t, id] = v.split(':'); S.sel = { t, id }; S.open = true; renderSheet(); peek(); },
    open() { S.open = true; renderSheet(); },
    close() {
      if (S.back.length) { const b = S.back.pop(); S.view = b.view; S.sel = b.sel; S.open = b.open; setHash(); render(); }
      else { S.open = false; if (wide()) S.sel = null; renderSheet(); if (S.view === 'explore') peek(); }
    },
    tab(v, t) { const s = S.sel; if (!s) return; S.tabs[s.t] = v; $$('.pw-tabs .pw-chip').forEach(b => b.classList.toggle('on', b === t)); repanel(); },
    spot(v, t) { const sp = t.closest('.pw-split'), was = t.classList.contains('on'); $$('button', sp).forEach(b => b.classList.toggle('on', !was && b.dataset.v === v)); sp.classList.toggle('has', !was); },
    cmp(v) { S.cmp = v; repanel(); },
    cpriv(v) { S.cpriv = +v; repanel(); }, live(v) { S.live = +v; repanel(); },
    rung(v) { S.exp = +v; updExp(); },
    have(v, t) { tog('have', v); t.classList.toggle('on'); const s = S.sel, box = $('#pw-rdy'); if (!s || !box) return; const all = $$('.pw-chip', box), n = all.filter(b => b.classList.contains('on')).length, p = Math.round(n / all.length * 100); $('.fg', box).style.strokeDashoffset = 100 - p; $('b', box).textContent = p; },
    save(v, t) { tog('saved', v); t.classList.toggle('on'); renderNav(); },
    next(v) {
      const r = R[v], nx = r && r.next.map(x => R[x]).find(Boolean); if (!nx) return;
      S.trail = uniq([...S.trail, v]); S.stage = nx.stage; S.group = nx.group; S.course = S.career = S.sel = null; S.open = false; S.back = []; S.view = 'explore'; setHash(); render();
    },
    trail(i) { const id = S.trail[+i]; if (!R[id]) return; S.trail = S.trail.slice(0, +i); focusRoute(id); render(); },
    goRoute(v) { if (!R[v]) return; if (S.view !== 'explore') jump(); if (R[v].stage !== S.stage) S.trail = []; focusRoute(v); S.open = true; S.view = 'explore'; leaveSearch(); setHash(); render(); },
    goCareer(v) {
      if (!K[v]) return; if (S.view !== 'explore') jump();
      const here = D.routes.some(r => r.stage === S.stage && r.group === S.group && r.careers.includes(v));
      if (!here) { const r = (KR[v] || [])[0]; if (r) { S.stage = r.stage; S.group = r.group; S.course = null; S.trail = []; } }
      if (S.course && !R[S.course].careers.includes(v)) S.course = null;
      S.career = v; S.sel = { t: 'career', id: v }; S.exp = 3; S.open = true; S.view = 'explore'; leaveSearch(); setHash(); render();
    },
    exam(v) { if (!G[v]) return; if (S.view !== 'exams') jump(); S.view = 'exams'; S.track = G[v].track; S.sel = { t: 'exam', id: v }; S.tabs.exam = 'stages'; S.open = true; leaveSearch(); setHash(); render(); },
    goExam(v) { A.exam(v); },
    guide(v) { if (!GD[v]) return; if (S.view !== 'guides') jump(); S.view = 'guides'; S.sel = { t: 'guide', id: v }; S.open = true; leaveSearch(); setHash(); render(); },
    goGuide(v) { A.guide(v); },
    link(v) { const [t, id] = v.split(':'); ({ exam: A.exam, route: A.goRoute, career: A.goCareer, guide: A.guide }[t] || (() => {}))(id); },
    find(v) { S.cc = v; S.prov = -1; S.dist = ''; S.view = 'study'; S.study = 'colleges'; S.sel = null; S.open = false; S.back = []; leaveSearch(); setHash(); render(); },
    goSch(v) { S.view = 'study'; S.study = 'funding'; S.scope = 'All'; S.slvl = 'All'; S.schC = ''; S.schOpen = v; S.sel = null; S.open = false; leaveSearch(); setHash(); render(); },
    goCountry(v) { S.view = 'study'; S.study = 'abroad'; S.ab = v; S.sel = null; S.open = false; leaveSearch(); setHash(); render(); },
    goFaq(v) { const f = D.faq.find(x => x.id === v); S.view = 'guides'; S.faqTopic = f ? f.topic : ''; S.faqOpen = v; S.sel = null; S.open = false; leaveSearch(); setHash(); render(); },
    study(v) { S.study = v; renderMain(); },
    cc(v) { S.cc = v; S.prov = -1; S.dist = ''; renderMain(); },
    prov(v) { S.prov = S.prov === +v ? -1 : +v; S.dist = ''; renderMain(); },
    dist(v) { S.dist = S.dist === v ? '' : v; if (S.dist) { district = S.dist; try { localStorage.setItem('pw-district', district); } catch (e) {} } renderMain(); },
    sector(v) { S.sector = v; renderMain(); },
    ctry(v) { S.ab = S.ab === v ? '' : v; renderMain(); },
    schc(v) { S.schC = v; S.study = 'funding'; S.scope = 'All'; renderMain(); },
    scope(v) { if (v === 'x') S.schC = ''; else S.scope = v; renderMain(); },
    slvl(v) { S.slvl = v; renderMain(); },
    sch(v) { S.schOpen = S.schOpen === v ? '' : v; renderMain(); },
    track(v) { S.track = v; renderMain(); },
    edu(v) { S.edu = +v; put('edu', S.edu); renderMain(); },
    woman(v) { S.woman = +v; put('woman', S.woman); renderMain(); },
    gcat(v) { S.gcat = v; renderMain(); },
    ftopic(v) { S.faqTopic = v; renderMain(); },
    faq(v) { S.faqOpen = S.faqOpen === v ? '' : v; renderMain(); },
    step(v, t) {
      tog('done', v); t.classList.toggle('done');
      const g = GD[v.split(':')[0]]; if (!g) return;
      const d = gdone(g), a = $('#pw-gdone'), b = $('#pw-gbar'); if (a) a.textContent = d; if (b) b.style.width = d / Math.max(1, g.steps.length) * 100 + '%';
    },
    doc(v, t) { tog('docs', v); t.classList.toggle('on'); },
    plan(v) { S.plan = v; renderMain(); },
    mstage(v) { S.mstage = v; renderMain(); },
    mset(v, t) { const i = v.indexOf(':'); tog(v.slice(0, i), v.slice(i + 1)); t.classList.toggle('on'); renderMatch(); },
  };
  const IN = {
    'pw-q'(v) { S.q = v.trim(); renderMain(); },
    'pw-exp'(v) { S.exp = +v; updExp(); },
    'pw-abmax'(v) { S.abmax = +v; put('abmax', S.abmax); $('#pw-abv').textContent = 'NPR ' + v + 'L / yr'; $$('.pw-cc').forEach(e => e.classList.toggle('dim', +e.dataset.cost > S.abmax)); },
    'pw-mb'(v) { S.mb = +v; put('mb', S.mb); $('#pw-mbv').textContent = 'NPR ' + v + 'L'; renderMatch(); },
    'pw-age'(v) { S.age = +v; put('age', S.age); $('#pw-agev').textContent = 'Age ' + v; $('#pw-xlist').innerHTML = xlist(); },
    'pw-page'(v) { S.age = +v; put('age', S.age); $('#pw-pagev').textContent = v; $('#pw-pout').innerHTML = planOut(); },
    'pw-hrs'(v) { S.hrs = +v; put('hrs', S.hrs); $('#pw-hrv').textContent = v; const s = S.sel; if (s && G[s.id]) $('#pw-prep').innerHTML = prepOut(G[s.id]); },
    'pw-aid'(v) { S.aid = +v; $('#pw-aidv').textContent = 'Aid ' + v + '%'; const s = S.sel; if (s && R[s.id]) $('#pw-cost').innerHTML = costOut(R[s.id]); },
  };
  root.addEventListener('click', e => { const t = e.target.closest('[data-a]'); if (!t || !root.contains(t) || !A[t.dataset.a]) return; if (t.tagName === 'A') return; e.preventDefault(); A[t.dataset.a](t.dataset.v, t); });
  root.addEventListener('input', e => { const f = IN[e.target.id]; if (f) f(e.target.value); });
  root.addEventListener('keydown', e => {
    if ((e.key === 'Enter' || e.key === ' ') && e.target.matches('[role=button]')) { e.preventDefault(); e.target.click(); }
    if (e.key === 'Escape' && S.sel) A.close();
  });
  let rz = 0;
  new ResizeObserver(() => { cancelAnimationFrame(rz); rz = requestAnimationFrame(() => { if (D) { drawLinks(); peek(); root.classList.toggle('has-sheet', !!(S.sel && wide())); } }); }).observe(root);

  const start = d => {
    index(d);
    const h = location.hash.slice(1); if (NAV.some(n => n[0] === h)) S.view = h;
    render();
  };
  if (window.PW_DATA) start(window.PW_DATA);
  else fetch(root.dataset.src || '/api/pathways/', { credentials: 'same-origin' }).then(r => r.json()).then(start)
    .catch(() => { main.innerHTML = empty('Could not load Pathways'); });
})();
