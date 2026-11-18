/* Pathways v5 home: stage picker, live numbers, open now, tools, hot careers, fields. */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, M = V.ms, E = V.esc, PW = V.PW;
  V.st.home = { stage: 'after12' };
  function stagePanel() {
    var s = V.ST[V.st.home.stage], rs = PW.routes.filter(function (r) { return r.stage === s.id; });
    rs.sort(function (a, b) { return (b._dem * 2 + b._pro.length / 8) - (a._dem * 2 + a._pro.length / 8); });
    return '<div class="card tone ' + V.STAGE_T[s.id] + ' sp-in"><div class="row" style="align-items:flex-start"><span class="ic lg" style="background:var(--s0);color:var(--tf)">' + M(s.icon, 'lg') + '</span><div class="grow"><h2>' + E(s.label) + '</h2><p style="margin-top:4px">' + E(s.blurb) + '</p></div></div>' +
      '<p class="sm row" style="gap:8px;margin-top:12px;opacity:.9">' + M('lightbulb', 'sm') + E(s.tip) + '</p></div>' +
      '<div class="hs stag" style="margin-top:12px">' + rs.slice(0, 6).map(function (r, i) { return ui.course(r, i); }).join('') + '</div>' +
      '<div class="row" style="margin-top:12px"><button class="btn t" data-act="stageAll">' + 'All ' + rs.length + ' routes after this stage' + M('arrow_forward', 'sm') + '</button></div>';
  }
  V.acts.stage = function (el) {
    V.st.home.stage = el.dataset.id; V.$$('#stages .stg').forEach(function (b) { b.setAttribute('aria-pressed', b === el); });
    var p = V.$('#stagePanel'); p.innerHTML = stagePanel();
  };
  V.acts.stageAll = function () { V.st.courses = Object.assign(V.st.courses || {}, { stage: V.st.home.stage, group: '', kind: '', q: '' }); V.go('courses'); };
  V.acts.field = function (el) { V.st.courses = Object.assign(V.st.courses || {}, { stage: '', group: el.dataset.id, kind: '', q: '' }); V.go('courses'); };
  V.acts.districtGo = function () { var d = V.$('#homeDist').value; if (!d) return; V.st.colleges = Object.assign(V.st.colleges || {}, { district: d }); V.go('colleges'); };

  V.views.home = function () {
    var st = PW.stats, nums = [['routes', 'Courses', 't-pc'], ['providers', 'Colleges and schools', 't-gc'], ['careers', 'Careers', 't-yc'], ['scholarships', 'Scholarships', 't-tc'], ['abroad', 'Countries', 't-rc'], ['districts', 'Districts covered', 't-sc']];
    var open = PW.scholarships.filter(function (s) { return V.ch.inWindow(s.open); }).slice(0, 8), exOpen = PW.govt.filter(function (g) { return V.ch.inWindow(g.apply); });
    var hot = PW.careers.slice().sort(function (a, b) { return V.opp(b) - V.opp(a); }).slice(0, 6);
    var dists = Object.keys(PW.providers.reduce(function (m, p) { m[p.district] = 1; return m; }, {})).sort();
    var tools = [['match', 'Match me', 'Five questions, ranked routes', 'auto_awesome', 't-pc'], ['roi', 'Is it worth it', 'Cost against what you earn', 'savings', 't-gc'], ['colleges', 'Colleges by district', 'Map of all 77 districts', 'map', 't-yc'], ['schol', 'Deadline planner', 'Grants and exams by month', 'calendar_month', 't-tc']];
    var fields = Object.keys(V.GROUPS).filter(function (k) { return PW.routes.some(function (r) { return r.group === k; }); });
    return { title: 'Home', html:
      '<section class="hero"><div class="hero-t"><h1>Where are you now?</h1><p class="mut">Pick your stage. See every course, college, career and grant that follows.</p></div>' +
      '<div class="stages stag" id="stages">' + PW.stages.map(function (s, i) { return '<button class="stg card click ' + V.STAGE_T[s.id] + ' tone" style="--i:' + i + '" data-act="stage" data-id="' + s.id + '" aria-pressed="' + (s.id === V.st.home.stage) + '"><span class="ic" style="background:var(--s0);color:var(--tf)">' + M(s.icon) + '</span><b>' + E(s.label.replace('After ', 'After ')) + '</b><span class="xs">' + PW.routes.filter(function (r) { return r.stage === s.id; }).length + ' routes</span></button>'; }).join('') + '</div></section>' +
      '<div id="stagePanel" style="margin-top:14px">' + stagePanel() + '</div>' +
      '<div class="grid g3 stag nums sec">' + nums.map(function (n, i) { return '<div class="stat ' + n[2] + '" style="--i:' + i + '"><b data-count="' + st[n[0]] + '">0</b><span>' + n[1] + '</span></div>'; }).join('') + '</div>' +
      (open.length || exOpen.length ? ui.sec('Open this month', '<div class="hs stag">' + open.map(function (s, i) { return ui.schol(s, i); }).join('') + exOpen.map(function (g, i) { return ui.exam(g, i); }).join('') + '</div>', ['schol', 'All deadlines']) : '') +
      ui.sec('Tools', '<div class="grid g4 stag">' + tools.map(function (t, i) { return '<button class="card click tone ' + t[4] + ' tool" style="--i:' + i + '" data-go="' + t[0] + '">' + M(t[3], 'lg') + '<h3>' + t[1] + '</h3><span class="sm">' + t[2] + '</span></button>'; }).join('') + '</div>') +
      ui.sec('Careers with the best outlook', '<div class="hs stag">' + hot.map(function (c, i) { return ui.career(c, i); }).join('') + '</div>', ['careers', 'All careers']) +
      ui.sec('Browse by field', '<div class="chips wrap">' + fields.map(function (k) { var g = V.GROUPS[k]; return '<button class="chip" data-act="field" data-id="' + k + '">' + M(g[1]) + g[0] + '</button>'; }).join('') + '</div>') +
      ui.sec('Colleges near you', '<div class="card flat row wrap"><div class="grow"><h3>Pick your district</h3><div class="sm mut">See every college, school and institute there.</div></div><label class="fld" style="min-width:220px">' + M('location_on') + '<select id="homeDist"><option value="">Choose district</option>' + dists.map(function (d) { return '<option>' + d + '</option>'; }).join('') + '</select></label><button class="btn" data-act="districtGo">Show colleges</button></div>') +
      '<p class="xs mut" style="margin-top:28px">Figures are indicative ranges reviewed ' + E(PW.reviewed) + '. Check with the college or the official body before you pay.</p>' };
  };
})();
