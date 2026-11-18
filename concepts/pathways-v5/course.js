/* Pathways v5 course detail: overview journey, colleges (list and map), careers, entry, next steps. */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, ch = V.ch, M = V.ms, E = V.esc, PW = V.PW;
  var T = V.st.course = { id: '', tab: 'overview', d: '', sec: '', map: false }, mapH = null;
  function colRows(r) {
    var rows = r._pro.filter(function (p) { return (!T.d || p.district === T.d) && (!T.sec || p.sector.toLowerCase() === T.sec); });
    rows.sort(function (a, b) { return ((b.route_seats || {})[r.id] || 0) - ((a.route_seats || {})[r.id] || 0) || a.name.localeCompare(b.name); });
    return rows;
  }
  function colList(r) {
    var rows = colRows(r);
    return '<div class="cnt">' + rows.length + ' of ' + r._pro.length + ' colleges' + (T.d ? ' in ' + E(T.d) : '') + '</div>' + (rows.length ? '<div class="grid g2 stag">' + rows.slice(0, 40).map(function (p, i) {
      var f = (p.fees || {})[r.id], sn = (p.route_seats || {})[r.id];
      return '<article class="card click" style="--i:' + Math.min(i, 10) + '" data-go="college/' + p.id + '"><div class="row"><div class="grow"><h3>' + E(p.name) + '</h3><div class="xs mut row" style="gap:4px">' + M('location_on', 'xs') + E(p.place) + ', ' + E(p.district) + '</div></div>' + V.saveBtn('college', p.id) + '</div>' +
        '<div class="row wrap" style="gap:6px"><span class="tag">' + E(V.cap(p.sector)) + '</span><span class="tag ' + (f ? 't-gc' : '') + '">' + M('payments') + (f ? V.range(f) : 'About ' + V.range(r.fee)) + '</span>' + (sn ? '<span class="tag">' + M('event_seat') + sn + ' seats</span>' : '') + '</div></article>';
    }).join('') + '</div>' : ui.empty('No college here yet for this course.', 'location_off'));
  }
  function colTab(r) {
    var ds = {}; r._pro.forEach(function (p) { ds[p.district] = (ds[p.district] || 0) + 1; });
    if (!r._pro.length) return ui.empty('We have no listed colleges for this course yet. Check the official body for the current list.', 'apartment');
    return '<div class="fb"><div class="rowf"><label class="fld">' + M('location_on') + '<select data-in="cdist"><option value="">All districts</option>' + Object.keys(ds).sort().map(function (d) { return '<option' + (T.d === d ? ' selected' : '') + '>' + E(d) + '</option>'; }).join('') + '</select></label>' +
      '<div class="chips">' + [['', 'Any'], ['public', 'Public'], ['private', 'Private'], ['community', 'Community']].map(function (x) { return '<button class="chip" data-act="chip" data-k="cs-' + x[0] + '" data-v="' + x[0] + '" aria-pressed="' + (T.sec === x[0]) + '">' + x[1] + '</button>'; }).join('') + '</div>' +
      '<button class="chip" data-act="cmapt" aria-pressed="' + T.map + '">' + M('map') + 'Map</button></div>' + (T.map ? '<div id="cmap" style="margin-top:6px"></div><div class="legend"><i style="background:var(--s4)"></i>none<i style="background:color-mix(in srgb,var(--p) 40%,var(--s4))"></i>some<i style="background:var(--p)"></i>many</div>' : '') + '</div><div id="clist">' + colList(r) + '</div>';
  }
  function tabBody(r) {
    if (T.tab === 'overview') return '<div class="card"><h3>Your journey</h3><ol class="tl" style="margin-top:14px">' + (r.plan || []).map(function (s, i) { var c = s.indexOf(':'); return '<li style="--i:' + i + '"><span class="dot">' + (i + 1) + '</span><div>' + (c > 0 && c < 22 ? '<b>' + E(s.slice(0, c)) + '</b><div class="sm mut">' + E(s.slice(c + 1).trim()) + '</div>' : '<div class="sm">' + E(s) + '</div>') + '</div></li>'; }).join('') + '</ol></div>' +
      '<div class="card sec flat"><h3>Skills you build</h3><div class="row wrap" style="gap:8px;margin-top:10px">' + r.skills.map(function (s) { return '<span class="tag t-pc">' + E(s) + '</span>'; }).join('') + '</div></div>' + faqs(r);
    if (T.tab === 'colleges') return colTab(r);
    if (T.tab === 'careers') return r._c.length ? '<div class="grid g2 stag">' + r._c.map(ui.career).join('') + '</div>' : ui.empty('This course is a step, not a job. See what comes next.', 'route');
    if (T.tab === 'entry') { var g = r.exam_id && V.G[r.exam_id]; return '<div class="card"><div class="kv"><span>You need</span><b>' + E(r.entry) + '</b></div><div class="kv"><span>Exam or assessment</span><b>' + E(r.exam) + '</b></div><div class="kv"><span>Length</span><b>' + E(r.years) + '</b></div><div class="kv"><span>Typical fee</span><b>' + V.range(r.fee) + ' in total</b></div></div>' + (g ? '<div class="sec"><h3 style="margin-bottom:10px">Entrance exam</h3><div class="grid g2">' + ui.exam(g) + '</div></div>' : '') + '<div class="sec"><button class="btn t" data-go="guide/check-college">' + M('verified_user', 'sm') + 'Check a college before paying</button></div>'; }
    var nx = (r.next || []).map(function (i) { return V.R[i]; }).filter(Boolean);
    return nx.length ? '<div class="grid g2 stag">' + nx.map(ui.course).join('') + '</div>' : ui.empty('This is the top of this path. Careers and exams are next.', 'flag');
  }
  function faqs(r) { var f = PW.faq.filter(function (q) { return (q.go || []).indexOf(r.id) >= 0; }).slice(0, 4); return f.length ? '<div class="sec"><h3 style="margin-bottom:10px">Common questions</h3><div class="col">' + f.map(function (q) { return '<details class="acc"><summary>' + E(q.q) + M('expand_more') + '</summary><div class="bd">' + E(q.a) + '</div></details>'; }).join('') + '</div></div>' : ''; }
  function paint(r) { V.$('#tabBody').innerHTML = tabBody(r); if (T.tab === 'colleges' && T.map) mountMap(r); }
  function mountMap(r) {
    var counts = {}; r._pro.forEach(function (p) { counts[p.district] = (counts[p.district] || 0) + 1; });
    var el = V.$('#cmap'); if (el) mapH = window.PWMAP.mount(el, { counts: counts, selected: T.d, onPick: function (n) { T.d = n; var s = V.$('[data-in=cdist]'); if (s) s.value = n; mapH.update(counts, n); V.$('#clist').innerHTML = colList(r); } });
  }
  V.ins.cdist = function (el) { T.d = el.value; var r = V.R[T.id]; V.$('#clist').innerHTML = colList(r); if (mapH) { var c = {}; r._pro.forEach(function (p) { c[p.district] = (c[p.district] || 0) + 1; }); mapH.update(c, T.d); } };
  V.chipH.cs = function (el, k) { T.sec = k; V.$$('[data-k^="cs-"]').forEach(function (b) { b.setAttribute('aria-pressed', b === el); }); V.$('#clist').innerHTML = colList(V.R[T.id]); };
  V.acts.cmapt = function (el) { T.map = !T.map; paint(V.R[T.id]); };
  V.acts.ctab = function (el) { T.tab = el.dataset.t; V.$$('#ctabs button').forEach(function (b) { b.setAttribute('aria-selected', b === el); }); paint(V.R[T.id]); };
  V.acts.roiGo = function (el) { V.st.roi = Object.assign(V.st.roi || {}, { route: el.dataset.id }); V.go('roi'); };
  V.views.course = function (id) {
    var r = V.R[id]; if (!r) return ui.empty('Course not found.');
    if (T.id !== id) { T.id = id; T.tab = 'overview'; T.d = ''; T.sec = ''; T.map = false; }
    var g = V.grp(r.group), st = V.ST[r.stage], o = r._c.length ? Math.round(V.avg(r._c, V.opp)) : 0;
    var tabs = [['overview', 'Overview', 0], ['colleges', 'Colleges', r._pro.length], ['careers', 'Careers', r._c.length], ['entry', 'Entry and exam', 0], ['next', 'What next', (r.next || []).length]];
    return { title: r.name, html: '<div class="crumbs">' + ui.crumb('Courses', 'courses') + '<span class="tag">' + E(st ? st.label : '') + '</span></div>' +
      '<section class="dh card tone ' + g[2] + '"><div class="row" style="align-items:flex-start"><span class="ic lg" style="background:var(--s0);color:var(--tf)">' + M(g[1], 'lg') + '</span><div class="grow"><div class="row wrap" style="gap:6px"><span class="tag" style="background:var(--s0);color:var(--on)">' + E(r.kind) + '</span><span class="tag" style="background:var(--s0);color:var(--on)">' + g[0] + '</span></div><h1 style="margin-top:8px">' + E(r.name) + '</h1></div>' + V.saveBtn('course', r.id) + '</div>' +
      '<p style="max-width:720px">' + E(r.about) + '</p><div class="kpis"><div class="kpi"><b>' + E(r.years) + '</b><span>Length</span></div><div class="kpi"><b>' + V.range(r.fee) + '</b><span>Total fee</span></div><div class="kpi"><b>' + r._pro.length + '</b><span>Colleges listed</span></div><div class="kpi"><b>' + (r._pay ? V.npr(r._pay) : 'n/a') + '</b><span>Starting pay a month</span></div></div></section>' +
      '<div class="tabs" id="ctabs" role="tablist">' + tabs.map(function (t) { return '<button role="tab" data-act="ctab" data-t="' + t[0] + '" aria-selected="' + (T.tab === t[0]) + '">' + t[1] + (t[2] ? '<span class="n">' + t[2] + '</span>' : '') + '</button>'; }).join('') + '</div>' +
      '<div class="cols"><div id="tabBody">' + tabBody(r) + '</div><aside class="side col">' + (r._c.length ? '<div class="card"><div class="row"><div style="color:var(--p)">' + ch.ring(o, 64, 'Outlook') + '</div><div class="grow"><h3>Career outlook</h3><div class="xs mut">Demand, competition and pay together</div></div></div><div class="col" style="margin-top:12px">' + ch.meter('Demand', r._dem * 20, 'var(--good)', ch.level(r._dem)) + ch.meter('Competition', r._comp * 20, 'var(--warn)', ch.level(r._comp)) + '</div></div>' : '') +
      '<div class="card flat col"><h3>Worth the fee?</h3><div class="sm mut">See how long this course takes to pay for itself.</div><button class="btn" data-act="roiGo" data-id="' + r.id + '">' + M('savings', 'sm') + 'Open calculator</button></div></aside></div>',
      after: function () { if (T.tab === 'colleges' && T.map) mountMap(r); } };
  };
})();
