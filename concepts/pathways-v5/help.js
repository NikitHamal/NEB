/* Pathways v5 guides (step by step with document checklists) and FAQ. */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, M = V.ms, E = V.esc, PW = V.PW;
  var S = V.st.help = V.st.help || { tab: 'guides', cat: '', topic: '', q: '' };
  var CATIC = { Documents: 'badge', Study: 'school', Abroad: 'flight_takeoff', Licence: 'verified', Government: 'account_balance' };
  function guides() {
    var cats = {}; PW.guides.forEach(function (g) { cats[g.cat] = 1; });
    var gs = PW.guides.filter(function (g) { return (!S.cat || g.cat === S.cat) && (!S.q || g.name.toLowerCase().indexOf(S.q.toLowerCase()) >= 0); });
    return '<div class="chips" style="margin-bottom:12px">' + [''].concat(Object.keys(cats)).map(function (c) { return '<button class="chip" data-act="chip" data-k="h-cat-' + (c || 'x') + '" data-v="' + E(c) + '" aria-pressed="' + (S.cat === c) + '">' + (c || 'All') + '</button>'; }).join('') + '</div><div class="grid g3 stag">' + gs.map(function (g, i) {
      var days = g.steps.reduce(function (s, x) { return s + x[1]; }, 0), fee = g.steps.reduce(function (s, x) { return s + (x[2] || 0); }, 0);
      return '<article class="card click" style="--i:' + i + '" data-go="guide/' + g.id + '" tabindex="0"><div class="row"><span class="ic t-yc">' + M(CATIC[g.cat] || 'description') + '</span><div class="grow"><h3>' + E(g.name) + '</h3><div class="xs mut">' + E(g.cat) + '</div></div></div><div class="row wrap" style="gap:6px"><span class="tag">' + g.steps.length + ' steps</span><span class="tag">' + M('schedule') + days + ' days</span>' + (fee ? '<span class="tag">' + M('payments') + 'NPR ' + fee.toLocaleString('en-US') + '</span>' : '<span class="tag t-gc">Free</span>') + '</div></article>'; }).join('') + '</div>';
  }
  function faq() {
    var q = S.q.toLowerCase(), fs = PW.faq.filter(function (f) { return (!S.topic || f.topic === S.topic) && (!q || (f.q + ' ' + f.a).toLowerCase().indexOf(q) >= 0); });
    return '<div class="chips" style="margin-bottom:12px">' + [{ id: '', label: 'All' }].concat(PW.topics).map(function (t) { return '<button class="chip" data-act="chip" data-k="h-topic-' + (t.id || 'x') + '" data-v="' + t.id + '" aria-pressed="' + (S.topic === t.id) + '">' + E(t.label) + '</button>'; }).join('') + '</div><div class="cnt">' + fs.length + ' answers</div><div class="col">' + fs.slice(0, 40).map(function (f) {
      return '<details class="acc"><summary>' + E(f.q) + M('expand_more') + '</summary><div class="bd">' + E(f.a) + ((f.go || []).length ? '<div class="row wrap" style="gap:6px;margin-top:10px">' + f.go.filter(function (i) { return V.R[i]; }).slice(0, 4).map(function (i) { return '<button class="chip" data-go="course/' + i + '">' + E(V.R[i].name) + '</button>'; }).join('') + '</div>' : '') + '</div></details>'; }).join('') + '</div>';
  }
  function paint() { V.$('#res').innerHTML = S.tab === 'guides' ? guides() : faq(); }
  V.chipH.h = function (el, k) { var key = k.split('-')[0]; S[key] = el.dataset.v; paint(); };
  V.acts.htab = function (el) { S.tab = el.dataset.v; S.q = ''; V.$$('#htab button').forEach(function (b) { b.setAttribute('aria-pressed', b === el); }); V.$('[data-in=hq]').value = ''; paint(); };
  V.ins.hq = function (el) { S.q = el.value; paint(); };
  V.views.help = function () {
    return { title: 'Guides', html: ui.head('Guides and answers', PW.guides.length + ' step by step guides and ' + PW.faq.length + ' answers, with real costs and days.') + '<div class="fb"><div class="rowf"><div class="seg" id="htab"><button data-act="htab" data-v="guides" aria-pressed="' + (S.tab === 'guides') + '">' + M('checklist', 'sm') + 'Guides</button><button data-act="htab" data-v="faq" aria-pressed="' + (S.tab === 'faq') + '">' + M('quiz', 'sm') + 'Questions</button></div><label class="fld grow" style="min-width:200px">' + M('search') + '<input type="search" data-in="hq" placeholder="Search" value="' + E(S.q) + '"></label></div></div><div id="res">' + (S.tab === 'guides' ? guides() : faq()) + '</div>' };
  };
  V.acts.tick = function (el) { var k = el.dataset.k, t = V.store.ticks; t[k] = !t[k]; V.persist(); el.setAttribute('aria-pressed', !!t[k]); };
  V.views.guide = function (id) {
    var g = V.GD[id]; if (!g) return ui.empty('Guide not found.'); var days = g.steps.reduce(function (s, x) { return s + x[1]; }, 0), fee = g.steps.reduce(function (s, x) { return s + (x[2] || 0); }, 0), link = g.link && g.link.split(':'), tgt = link && (link[0] === 'guide' ? V.GD[link[1]] : link[0] === 'exam' ? V.G[link[1]] : null);
    return { title: g.name, html: '<div class="crumbs">' + ui.crumb('Guides', 'help') + '<span class="tag">' + E(g.cat) + '</span></div><section class="dh card tone t-yc"><h1>' + E(g.name) + '</h1><div class="kpis"><div class="kpi"><b>' + g.steps.length + '</b><span>Steps</span></div><div class="kpi"><b>' + days + ' days</b><span>Usually</span></div><div class="kpi"><b>' + (fee ? 'NPR ' + fee.toLocaleString('en-US') : 'Free') + '</b><span>Official fees</span></div><div class="kpi"><b>' + g.docs.length + '</b><span>Documents</span></div></div></section>' +
      '<div class="cols sec"><div class="card"><h3>Steps</h3><ol class="tl" style="margin-top:14px">' + g.steps.map(function (s, i) { return '<li style="--i:' + i + '"><span class="dot">' + (i + 1) + '</span><div><b>' + E(s[0]) + '</b><div class="row wrap" style="gap:6px;margin-top:4px">' + (s[1] ? '<span class="tag">' + M('schedule', 'xs') + s[1] + ' day' + (s[1] > 1 ? 's' : '') + '</span>' : '') + (s[2] ? '<span class="tag t-yc">NPR ' + Number(s[2]).toLocaleString('en-US') + '</span>' : '') + (s[3] ? '<span class="tag">' + E(s[3]) + '</span>' : '') + '</div></div></li>'; }).join('') + '</ol></div>' +
      '<aside class="side col"><div class="card"><h3>Documents to carry</h3><div style="margin-top:8px">' + g.docs.map(function (d, i) { var k = g.id + ':' + i; return '<button class="chk" data-act="tick" data-k="' + k + '" aria-pressed="' + !!V.store.ticks[k] + '"><span class="bx">' + M('check', 'xs') + '</span><span class="tx">' + E(d) + '</span></button>'; }).join('') + '</div></div>' +
      (tgt ? '<button class="card click row" data-go="' + (link[0] === 'guide' ? 'guide/' : 'exam/') + tgt.id + '"><span class="ic t-sc">' + M('link') + '</span><div class="grow" style="text-align:left"><b>' + E(tgt.name) + '</b><div class="xs mut">Related</div></div>' + M('chevron_right') + '</button>' : '') + '</aside></div>' };
  };
})();
