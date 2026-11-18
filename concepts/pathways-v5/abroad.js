/* Pathways v5 abroad: 46 destinations with budget, visa timeline planner, intakes and grants. */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, ch = V.ch, M = V.ms, E = V.esc, PW = V.PW;
  var S = V.st.abroad = V.st.abroad || { q: '', cap: 60, exam: '', sort: 'cost' };
  var FULL = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
  var total = function (a) { return V.mid(a.tuition) + V.mid(a.living); };
  var intakeMonths = function (a) { var t = a.intakes.toLowerCase(), r = []; FULL.forEach(function (m, i) { if (t.indexOf(m) >= 0 || t.indexOf(m.slice(0, 3) + ' ') >= 0) r.push(i + 1); }); return r; };
  var SORT = { cost: function (a, b) { return total(a) - total(b); }, work: function (a, b) { return (b.work_hours || 0) - (a.work_hours || 0); }, grants: function (a, b) { return b.scholarships.length - a.scholarships.length; }, name: function (a, b) { return a.country.localeCompare(b.country); } };
  function list() {
    var as = PW.abroad.filter(function (a) { return total(a) <= S.cap * 1e5 && (!S.exam || a.exams.indexOf(S.exam) >= 0) && (!S.q || (a.country + ' ' + a.fields.join(' ')).toLowerCase().indexOf(S.q.toLowerCase()) >= 0); }).sort(SORT[S.sort]);
    return '<div class="cnt">' + as.length + ' countries within ' + (S.cap >= 150 ? 'any budget' : 'NPR ' + S.cap + ' L a year') + '</div>' + (as.length ? '<div class="grid g3 stag">' + as.map(function (a, i) { return ui.country(a, Math.min(i, 12)); }).join('') + '</div>' : ui.empty('Nothing fits this budget. Raise it or try Germany, Norway and other low tuition options.', 'public_off'));
  }
  V.chipH.a = function (el) { S.exam = el.dataset.v; V.$$('#a-exam .chip').forEach(function (b) { b.setAttribute('aria-pressed', b === el); }); V.$('#res').innerHTML = list(); };
  V.ins.aq = function (el) { S.q = el.value; V.$('#res').innerHTML = list(); };
  V.ins.as = function (el) { S.sort = el.value; V.$('#res').innerHTML = list(); };
  V.ins.acap = function (el) { S.cap = +el.value; V.$('#acapl').textContent = S.cap >= 150 ? 'Any' : 'NPR ' + S.cap + ' L'; V.$('#res').innerHTML = list(); };
  V.views.abroad = function () {
    var ex = {}; PW.abroad.forEach(function (a) { a.exams.forEach(function (e) { ex[e] = (ex[e] || 0) + 1; }); });
    var top = Object.keys(ex).sort(function (a, b) { return ex[b] - ex[a]; }).slice(0, 7);
    return { title: 'Abroad', html: ui.head('Study abroad', 'Yearly cost, visa steps, work rules and grants for ' + PW.stats.abroad + ' countries.') + '<div class="fb"><div class="rowf"><label class="fld grow" style="min-width:200px">' + M('search') + '<input type="search" data-in="aq" placeholder="Search country or field" value="' + E(S.q) + '"></label>' +
      '<label class="fld">' + M('sort') + '<select data-in="as">' + [['cost', 'Lowest cost'], ['work', 'Most work hours'], ['grants', 'Most grants'], ['name', 'A to Z']].map(function (o) { return '<option value="' + o[0] + '"' + (S.sort === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select></label></div>' +
      ui.chipRow('a-exam', [['', 'Any test']].concat(top.map(function (e) { return [e, e]; })), S.exam) + '<div class="sl" style="max-width:440px"><div class="row"><span class="sm mut">Budget a year, tuition and living</span><b id="acapl">' + (S.cap >= 150 ? 'Any' : 'NPR ' + S.cap + ' L') + '</b></div><input class="rng" type="range" min="10" max="150" step="5" value="' + S.cap + '" data-in="acap"></div></div><div id="res">' + list() + '</div>' };
  };
  V.ins.yrsA = V.ins.grA = function () { var a = V.A[V.$('#abox').dataset.id], y = +V.$('#ay').value, g = +V.$('#ag').value; var t = V.mid(a.tuition) * y * (1 - g / 100), l = V.mid(a.living) * y;
    V.$('#ayl').textContent = y + (y === 1 ? ' year' : ' years'); V.$('#agl').textContent = g + '%'; V.$('#abig').textContent = V.npr(t + l); V.$('#astk').innerHTML = ch.stack([['Tuition', t, 'var(--p)'], ['Living', l, 'var(--warn)']]); };
  V.ins.intake = function (el) {
    var a = V.A[el.dataset.id], days = a.visa.steps.reduce(function (s, x) { return s + x[1]; }, 0), m = +el.value; if (!m) return V.$('#abegin').innerHTML = '';
    var back = Math.ceil((days + 45) / 30), b = ((m - 1 - back) % 12 + 12) % 12 + 1;
    V.$('#abegin').innerHTML = '<div class="verdict ' + 't-gc' + '" style="--tb:var(--gc);--tf:var(--ongc)">' + M('event_available') + '<div>Start paperwork by <b>' + V.MONTHS[b - 1] + '</b>. The visa steps take about ' + days + ' days, plus 45 days of buffer.</div></div>';
  };
  V.views.country = function (id) {
    var a = V.A[id]; if (!a) return ui.empty('Country not found.'); var st = a.visa.steps, days = st.reduce(function (s, x) { return s + x[1]; }, 0), im = intakeMonths(a), ss = a.scholarships.map(function (i) { return V.S[i]; }).filter(Boolean);
    var t = V.mid(a.tuition) * 3, l = V.mid(a.living) * 3;
    return { title: a.country, html: '<div class="crumbs">' + ui.crumb('Abroad', 'abroad') + '</div><section class="dh card tone t-pc"><div class="row" style="align-items:flex-start"><span class="ic lg" style="background:var(--s0);color:var(--tf);font-weight:600">' + E(a.code) + '</span><div class="grow"><h1>' + E(a.country) + '</h1><div style="margin-top:4px">' + E(a.intakes) + ' intakes</div></div>' + V.saveBtn('country', a.id) + '</div>' +
      '<div class="kpis"><div class="kpi"><b>' + V.range(a.tuition) + '</b><span>Tuition a year</span></div><div class="kpi"><b>' + V.range(a.living) + '</b><span>Living a year</span></div><div class="kpi"><b>' + (a.work_hours ? a.work_hours + ' h a week' : 'See rules') + '</b><span>Work while studying</span></div><div class="kpi"><b>' + E((a.stay_back || 'See rules').split(',')[0].slice(0, 28)) + '</b><span>Stay back</span></div></div><div class="row wrap">' + V.cmpBtn('country', a.id).replace('class="chip"', 'class="chip" style="background:var(--s0)"') + '</div></section>' +
      '<div class="cols sec"><div class="col" style="gap:16px"><div class="card" id="abox" data-id="' + a.id + '"><h3>Budget planner</h3><div class="grid g2" style="margin-top:12px"><div class="sl"><div class="row"><span class="sm mut">Years of study</span><b id="ayl">3 years</b></div><input class="rng" id="ay" type="range" min="1" max="5" value="3" data-in="yrsA"></div><div class="sl"><div class="row"><span class="sm mut">Scholarship on tuition</span><b id="agl">0%</b></div><input class="rng" id="ag" type="range" min="0" max="100" step="5" value="0" data-in="grA"></div></div><div class="big" id="abig" style="margin:14px 0 10px">' + V.npr(t + l) + '</div><div id="astk">' + ch.stack([['Tuition', t, 'var(--p)'], ['Living', l, 'var(--warn)']]) + '</div></div>' +
      '<div class="card"><h3>Visa timeline</h3><div class="xs mut" style="margin:2px 0 12px">' + E(a.visa.name) + ', about ' + days + ' days in total</div><ol class="tl">' + st.map(function (s, i) { return '<li style="--i:' + i + '"><span class="dot">' + (i + 1) + '</span><div><b>' + E(s[0]) + '</b> <span class="xs mut">' + (s[1] ? s[1] + ' day' + (s[1] > 1 ? 's' : '') : '') + (s[3] ? ' &middot; ' + s[3] : '') + (s[2] ? ' &middot; ' + E(s[2]) : '') + '</span>' + (s[4] ? '<div class="sm mut">' + E(s[4]) + '</div>' : '') + '</div></li>'; }).join('') + '</ol>' +
      '<label class="fld" style="margin-top:6px">' + M('event') + '<select data-in="intake" data-id="' + a.id + '"><option value="0">When do you want to start studying?</option>' + V.MONTHS.map(function (m, i) { return '<option value="' + (i + 1) + '">' + m + '</option>'; }).join('') + '</select></label><div id="abegin" style="margin-top:10px"></div></div>' +
      (im.length ? '<div class="card"><h3>Intakes</h3><div style="margin-top:10px">' + ch.monthSet(im, 'var(--p)') + '</div></div>' : '') +
      (ss.length ? ui.sec('Grants for ' + E(a.country), '<div class="grid g2 stag">' + ss.map(ui.schol).join('') + '</div>') : '') + '</div>' +
      '<aside class="side col"><div class="card"><h3>Fields to look at</h3><div class="row wrap" style="gap:8px;margin-top:10px">' + a.fields.map(function (f) { return '<span class="tag t-pc">' + E(f) + '</span>'; }).join('') + '</div><div class="kv" style="margin-top:10px"><span>Language test</span><b>' + E(a.exams.join(', ')) + '</b></div><div class="kv"><span>Work</span><b>' + E(a.work) + '</b></div></div><div class="card flat"><h3>Notes</h3><p class="sm mut" style="margin-top:8px">' + E(a.note) + '</p></div></aside></div>' };
  };
})();
