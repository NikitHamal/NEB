/* Pathways v5 careers: ranked list and a deep detail page (pay ladder, outlook radar, routes in, exams). */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, ch = V.ch, M = V.ms, E = V.esc, PW = V.PW;
  var S = V.st.careers = V.st.careers || { q: '', trend: '', sort: 'opp', lic: false };
  var SORT = { opp: function (a, b) { return V.opp(b) - V.opp(a); }, pay: function (a, b) { return V.mid(b.salary.entry) - V.mid(a.salary.entry); }, senior: function (a, b) { return V.mid(b.salary.senior) - V.mid(a.salary.senior); },
    demand: function (a, b) { return b.demand - a.demand; }, open: function (a, b) { return a.competition - b.competition; }, abroad: function (a, b) { return b.abroad - a.abroad; }, name: function (a, b) { return a.name.localeCompare(b.name); } };
  function list() {
    var cs = PW.careers.filter(function (c) { return (!S.trend || c.trend === S.trend) && (!S.lic || c.licence) && (!S.q || (c.name + ' ' + c.about + ' ' + (c.skills || []).join(' ')).toLowerCase().indexOf(S.q.toLowerCase()) >= 0); }).sort(SORT[S.sort]);
    return '<div class="cnt">' + cs.length + ' careers</div>' + (cs.length ? '<div class="grid g3 stag">' + cs.map(function (c, i) { return ui.career(c, Math.min(i, 12)); }).join('') + '</div>' : ui.empty('No career matches.', 'work_off'));
  }
  V.chipH.r = function (el, k) { S.trend = k === 'x' ? '' : k; V.$$('[data-k^="r-"]').forEach(function (b) { b.setAttribute('aria-pressed', b === el); }); V.$('#res').innerHTML = list(); };
  V.ins.rq = function (el) { S.q = el.value; V.$('#res').innerHTML = list(); };
  V.ins.rs = function (el) { S.sort = el.value; V.$('#res').innerHTML = list(); };
  V.acts.rlic = function (el) { S.lic = !S.lic; el.setAttribute('aria-pressed', S.lic); V.$('#res').innerHTML = list(); };
  V.views.careers = function () {
    return { title: 'Careers', html: ui.head('Careers', 'Pay, demand and competition in Nepal, with the courses that lead there.') + '<div class="fb"><div class="rowf"><label class="fld grow" style="min-width:220px">' + M('search') + '<input type="search" data-in="rq" placeholder="Search careers or skills" value="' + E(S.q) + '"></label>' +
      '<label class="fld">' + M('sort') + '<select data-in="rs">' + [['opp', 'Best outlook'], ['pay', 'Highest starting pay'], ['senior', 'Highest senior pay'], ['demand', 'Most demand'], ['open', 'Least competition'], ['abroad', 'Best abroad'], ['name', 'A to Z']].map(function (o) { return '<option value="' + o[0] + '"' + (S.sort === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select></label></div>' +
      '<div class="chips">' + [['', 'Any trend'], ['rising', 'Rising'], ['steady', 'Steady'], ['falling', 'Falling']].map(function (x) { return '<button class="chip" data-act="chip" data-k="r-' + (x[0] || 'x') + '" aria-pressed="' + (S.trend === x[0]) + '">' + x[1] + '</button>'; }).join('') + '<button class="chip" data-act="rlic" aria-pressed="' + S.lic + '">' + M('verified') + 'Needs a licence</button></div></div><div id="res">' + list() + '</div>' };
  };
  var pay = function (c, y) { var a = V.mid(c.salary.entry), b = V.mid(c.salary.senior), t = Math.min(1, y / 15); return a + (b - a) * (1 - Math.pow(1 - t, 1.6)); };
  V.ins.yrs = function (el) { var c = V.C[el.dataset.id]; V.$('#yrl').textContent = el.value + (el.value === '1' ? ' year' : ' years'); V.$('#yrp').textContent = V.npr(Math.round(pay(c, +el.value) / 500) * 500); };
  V.views.career = function (id) {
    var c = V.C[id]; if (!c) return ui.empty('Career not found.');
    var o = V.opp(c), mx = Math.max(c.salary.senior[1], 1), lad = c.ladder || [], ex = PW.govt.filter(function (g) { return g.career === c.id; }), lic = c.licence && (V.G[c.licence.exam] || null);
    var axes = [['Demand', c.demand * 20], ['Pay', Math.min(100, V.mid(c.salary.senior) / 3000)], ['Abroad', c.abroad * 20], ['Openings', 100 - (c.competition - 1) * 22], ['Growth', c.trend === 'rising' ? 90 : c.trend === 'steady' ? 55 : 25]];
    return { title: c.name, html: '<div class="crumbs">' + ui.crumb('Careers', 'careers') + ch.trendTag(c.trend) + '</div>' +
      '<section class="dh card tone t-tc"><div class="row" style="align-items:flex-start"><div class="grow"><h1>' + E(c.name) + '</h1><p style="margin-top:8px;max-width:640px">' + E(c.about) + '</p></div>' + V.saveBtn('career', c.id) + '</div>' +
      '<div class="kpis"><div class="kpi"><b>' + V.range(c.salary.entry) + '</b><span>Starting, a month</span></div><div class="kpi"><b>' + V.range(c.salary.senior) + '</b><span>Senior, a month</span></div><div class="kpi"><b>' + (c.hours || 40) + ' h</b><span>A week</span></div><div class="kpi"><b>' + ch.level(c.demand) + '</b><span>Demand</span></div></div></section>' +
      '<div class="cols sec"><div class="col" style="gap:16px"><div class="card"><h3>Pay by experience</h3><div class="sl" style="margin-top:12px"><div class="row"><span class="sm mut">Experience</span><b id="yrl">5 years</b></div><input class="rng" type="range" min="0" max="15" value="5" data-in="yrs" data-id="' + c.id + '"><div class="big" style="margin-top:8px" id="yrp">' + V.npr(Math.round(pay(c, 5) / 500) * 500) + '</div><div class="xs mut">A month, estimated between the starting and senior ranges</div></div>' +
      '<div class="col" style="margin-top:16px"><div><div class="xs mut" style="margin-bottom:4px">Starting ' + V.range(c.salary.entry) + '</div>' + ch.range(c.salary.entry[0], c.salary.entry[1], mx, 'var(--p)', 'Starting') + '</div><div><div class="xs mut" style="margin-bottom:4px">Senior ' + V.range(c.salary.senior) + '</div>' + ch.range(c.salary.senior[0], c.salary.senior[1], mx, 'var(--good)', 'Senior') + '</div></div></div>' +
      (lad.length ? '<div class="card"><h3>Career ladder</h3><ol class="tl" style="margin-top:14px">' + lad.map(function (l, i) { return '<li style="--i:' + i + '"><span class="dot">' + (i + 1) + '</span><div><b>' + E(l) + '</b></div></li>'; }).join('') + '</ol></div>' : '') +
      '<div class="card flat"><h3>Skills and employers</h3><div class="row wrap" style="gap:8px;margin:10px 0">' + (c.skills || []).map(function (s) { return '<span class="tag t-pc">' + E(s) + '</span>'; }).join('') + '</div><div class="row wrap" style="gap:8px">' + (c.employers || []).map(function (s) { return '<span class="tag">' + M('business', 'xs') + E(s) + '</span>'; }).join('') + '</div></div>' +
      (c._routes.length ? ui.sec('Courses that lead here', '<div class="grid g2 stag">' + c._routes.slice(0, 8).map(ui.course).join('') + '</div>') : '') + (ex.length ? ui.sec('Exams for this career', '<div class="grid g2">' + ex.map(ui.exam).join('') + '</div>') : '') + '</div>' +
      '<aside class="side col"><div class="card"><div class="row"><div style="color:var(--p)">' + ch.ring(o, 64, 'Outlook') + '</div><div class="grow"><h3>Outlook score</h3><div class="xs mut">Computed from demand, competition, abroad and trend</div></div></div>' + ch.radar(axes) + '<div class="col">' + ch.meter('Demand', c.demand * 20, 'var(--good)', ch.level(c.demand)) + ch.meter('Competition', c.competition * 20, 'var(--warn)', ch.level(c.competition)) + ch.meter('Abroad', c.abroad * 20, 'var(--p)', ch.level(c.abroad)) + '</div></div>' +
      (c.licence ? '<div class="card tone t-yc col"><div class="row">' + M('verified') + '<h3>Licence needed</h3></div><div class="sm">' + E(c.licence.name) + '</div>' + (lic ? '<button class="btn" data-go="exam/' + lic.id + '">See the licence exam</button>' : '') + '</div>' : '') + '</aside></div>' };
  };
})();
