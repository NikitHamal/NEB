/* Pathways v5 courses: filter list plus the course to career flow. */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, M = V.ms, E = V.esc, PW = V.PW;
  var CAPS = [100000, 300000, 600000, 1000000, 2500000, 5000000, 1e12], CAPL = ['NPR 1L', 'NPR 3L', 'NPR 6L', 'NPR 10L', 'NPR 25L', 'NPR 50L', 'Any fee'];
  V.CAPS = CAPS; V.CAPL = CAPL;
  var S = V.st.courses = V.st.courses || { stage: '', group: '', kind: '', q: '', cap: 6, sort: 'demand', view: 'grid', flow: '' };
  function pool() { return PW.routes.filter(function (r) { return (!S.stage || r.stage === S.stage) && (!S.group || r.group === S.group) && (!S.kind || r.kind === S.kind) && r.fee[0] <= CAPS[S.cap] && (!S.q || (r.name + ' ' + r.about + ' ' + r.kind + ' ' + r.skills.join(' ')).toLowerCase().indexOf(S.q.toLowerCase()) >= 0); }); }
  var SORTS = { demand: function (a, b) { return b._dem - a._dem || b._pro.length - a._pro.length; }, fee: function (a, b) { return a.fee[0] - b.fee[0]; }, colleges: function (a, b) { return b._pro.length - a._pro.length; }, pay: function (a, b) { return b._pay - a._pay; }, name: function (a, b) { return a.name.localeCompare(b.name); } };
  function list() {
    var rs = pool().sort(SORTS[S.sort]);
    if (S.view === 'flow') return flow(rs);
    return '<div class="cnt">' + rs.length + ' course' + (rs.length === 1 ? '' : 's') + '</div>' + (rs.length ? '<div class="grid g3 stag">' + rs.slice(0, 60).map(function (r, i) { return ui.course(r, Math.min(i, 12)); }).join('') + '</div>' + (rs.length > 60 ? '<p class="mut sm" style="margin-top:12px">Showing the first 60. Narrow with the filters.</p>' : '') : ui.empty('No course matches. Loosen a filter.'));
  }
  function flow(rs) {
    rs = rs.filter(function (r) { return r._c.length; }).slice(0, 14);
    if (!rs.length) return ui.empty('No linked careers for these filters.');
    var cs = {}; rs.forEach(function (r) { r._c.forEach(function (c) { cs[c.id] = c; }); });
    var carr = Object.keys(cs).map(function (k) { return cs[k]; }).sort(function (a, b) { return V.opp(b) - V.opp(a); });
    var sel = S.flow && V.R[S.flow] && rs.indexOf(V.R[S.flow]) >= 0 ? V.R[S.flow] : null, ok = sel ? sel.careers : null;
    if (ok) carr.sort(function (a, b) { return (ok.indexOf(b.id) >= 0 ? 1 : 0) - (ok.indexOf(a.id) >= 0 ? 1 : 0); });
    carr = carr.slice(0, Math.max(rs.length + 2, 16));
    return '<p class="sm mut" style="margin:4px 0 14px">Tap a course to see the careers it opens.</p><div class="flow" id="flow"><svg id="flowSvg" aria-hidden="true"></svg><div class="col"><h4>Courses</h4>' +
      rs.map(function (r) { var g = V.grp(r.group); return '<button data-act="flowPick" data-id="' + r.id + '" class="' + (sel ? (sel === r ? 'on' : 'dim') : '') + '" id="fr-' + r.id + '">' + M(g[1], 'sm') + '<span>' + E(r.name) + '</span></button>'; }).join('') + '</div><div class="col"><h4>Careers</h4>' +
      carr.map(function (c) { return '<button data-go="career/' + c.id + '" class="' + (ok ? (ok.indexOf(c.id) >= 0 ? 'on' : 'dim') : '') + '" id="fc-' + c.id + '"><span>' + E(c.name) + '</span></button>'; }).join('') + '</div></div>' +
      (sel ? '<div class="card tone t-pc row wrap sp-in" style="margin-top:16px"><div class="grow"><h3>' + E(sel.name) + '</h3><div class="sm">' + sel._c.length + ' careers, starting about ' + V.npr(sel._pay) + ' a month</div></div><button class="btn" data-go="course/' + sel.id + '">Open course' + M('arrow_forward', 'sm') + '</button></div>' : '');
  }
  function draw() {
    var f = V.$('#flow'), svg = V.$('#flowSvg'); if (!f || !svg) return; svg.innerHTML = '';
    var r = S.flow && V.R[S.flow]; if (!r) return; var b = f.getBoundingClientRect(), a = V.$('#fr-' + r.id); if (!a) return; var ab = a.getBoundingClientRect();
    r.careers.forEach(function (id) {
      var c = V.$('#fc-' + id); if (!c) return; var cb = c.getBoundingClientRect();
      var x1 = ab.right - b.left, y1 = ab.top + ab.height / 2 - b.top, x2 = cb.left - b.left, y2 = cb.top + cb.height / 2 - b.top, mx = (x1 + x2) / 2;
      var p = document.createElementNS('http://www.w3.org/2000/svg', 'path'); p.setAttribute('d', 'M' + x1 + ' ' + y1 + 'C' + mx + ' ' + y1 + ' ' + mx + ' ' + y2 + ' ' + x2 + ' ' + y2); svg.appendChild(p);
      var l = p.getTotalLength(); p.style.setProperty('--l', l);
    });
  }
  function active() {
    var a = []; if (S.stage) a.push(['stage', V.ST[S.stage].label]); if (S.group) a.push(['group', V.grp(S.group)[0]]); if (S.kind) a.push(['kind', S.kind]);
    if (S.cap < 6) a.push(['cap', 'Fee up to ' + CAPL[S.cap]]); return a;
  }
  function fsum() {
    var a = active();
    return a.map(function (x) { return '<button class="chip cx" data-act="fclr" data-k="' + x[0] + '">' + E(x[1]) + M('close', 'xs') + '</button>'; }).join('') + (a.length > 1 ? '<button class="chip" data-act="fclr" data-k="all">Clear all</button>' : '');
  }
  function refresh() {
    var r = V.$('#res'); if (r) r.innerHTML = list();
    var f = V.$('#fsum'); if (f) { f.innerHTML = fsum(); f.hidden = !active().length; }
    var n = V.$('#fcnt'); if (n) { n.textContent = active().length; n.hidden = !active().length; }
    draw();
  }
  V.acts.fbt = function () { var b = V.$('.fb'); b.classList.toggle('open'); V.$('.fbt').setAttribute('aria-expanded', b.classList.contains('open')); };
  V.acts.fclr = function (el) {
    var k = el.dataset.k; if (k === 'all') { S.stage = ''; S.group = ''; S.kind = ''; S.cap = 6; } else S[k] = k === 'cap' ? 6 : ''; S.flow = ''; V.render();
  };
  V.acts.flowPick = function (el) { S.flow = S.flow === el.dataset.id ? '' : el.dataset.id; refresh(); };
  V.chipH.c = function (el, key) {
    var k = 'c-' + key; S[key] = el.dataset.v; S.flow = '';
    V.$$('#' + k + ' .chip').forEach(function (b) { b.setAttribute('aria-pressed', b === el); });
    if (key === 'stage') { V.$('#c-group').outerHTML = groups(); }
    refresh();
  };
  V.ins.cq = function (el) { S.q = el.value; refresh(); };
  V.ins.ccap = function (el) { S.cap = +el.value; V.$('#capl').textContent = CAPL[S.cap]; refresh(); };
  V.ins.csort = function (el) { S.sort = el.value; refresh(); };
  V.acts.cview = function (el) { S.view = el.dataset.v; if (S.view === 'flow' && !S.stage) { S.stage = 'after12'; V.$('#c-stage').outerHTML = ui.chipRow('c-stage', stages(), S.stage); V.$('#c-group').outerHTML = groups(); } V.$$('#cview button').forEach(function (b) { b.setAttribute('aria-pressed', b === el); }); refresh(); };
  function stages() { return [['', 'All']].concat(PW.stages.map(function (s) { return [s.id, s.label.replace('After ', 'After '), s.icon]; })); }
  function groups() {
    var gs = {}; PW.routes.forEach(function (r) { if (!S.stage || r.stage === S.stage) gs[r.group] = 1; });
    if (S.group && !gs[S.group]) S.group = '';
    return ui.chipRow('c-group', [['', 'All fields']].concat(Object.keys(gs).sort().map(function (k) { return [k, V.grp(k)[0], V.grp(k)[1]]; })), S.group);
  }
  V.views.courses = function () {
    var n = active().length;
    return { title: 'Courses', html: ui.head('Courses', 'Every route after Class 8, SEE, +2 and your bachelor.') +
      '<div class="fb"><div class="rowf"><label class="fld grow" style="min-width:0">' + M('search') + '<input data-in="cq" type="search" placeholder="Search courses" value="' + E(S.q) + '"></label>' +
      '<button class="btn t sm fbt" data-act="fbt" aria-expanded="false">' + M('tune', 'sm') + 'Filters<span class="cnt-b" id="fcnt"' + (n ? '' : ' hidden') + '>' + n + '</span></button>' +
      '<div class="fx inl"><label class="fld">' + M('sort') + '<select data-in="csort">' + [['demand', 'Best demand'], ['colleges', 'Most colleges'], ['pay', 'Highest starting pay'], ['fee', 'Lowest fee'], ['name', 'A to Z']].map(function (o) { return '<option value="' + o[0] + '"' + (S.sort === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select></label>' +
      '<div class="seg" id="cview"><button data-act="cview" data-v="grid" aria-pressed="' + (S.view === 'grid') + '">' + M('grid_view', 'sm') + 'Grid</button><button data-act="cview" data-v="flow" aria-pressed="' + (S.view === 'flow') + '">' + M('account_tree', 'sm') + 'Flow</button></div></div></div>' +
      '<div class="fx">' + ui.chipRow('c-stage', stages(), S.stage) + groups() + '<div class="sl"><div class="row"><span class="sm mut">Course fee up to</span><b id="capl">' + CAPL[S.cap] + '</b></div><input class="rng" type="range" min="0" max="6" value="' + S.cap + '" data-in="ccap"></div></div>' +
      '<div class="chips fsum" id="fsum"' + (n ? '' : ' hidden') + '>' + fsum() + '</div></div><div id="res">' + list() + '</div>', after: function () { requestAnimationFrame(draw); } };
  };
})();
