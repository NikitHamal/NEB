/* Pathways v5 home: stage picker, live numbers, open now, tools, hot careers, fields. */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, M = V.ms, E = V.esc, PW = V.PW;
  V.st.home = { stage: 'after12' };
  function stagePanel() {
    var s = V.ST[V.st.home.stage], H = V.st.home, all = PW.routes.filter(function (r) { return r.stage === s.id; }), gs = {};
    all.forEach(function (r) { gs[r.group] = (gs[r.group] || 0) + 1; });
    if (H.field && !gs[H.field]) H.field = '';
    var rs = all.filter(function (r) { return !H.field || r.group === H.field; });
    rs.sort(function (a, b) { return (b._dem * 2 + b._pro.length / 8) - (a._dem * 2 + a._pro.length / 8); });
    var cs = {}; rs.forEach(function (r) { r._c.forEach(function (c) { cs[c.id] = c; }); });
    var top = Object.keys(cs).map(function (k) { return cs[k]; }).sort(function (a, b) { return V.opp(b) - V.opp(a); }).slice(0, 8);
    return '<div class="card tone ' + V.STAGE_T[s.id] + ' sp-in"><div class="row" style="align-items:flex-start"><span class="ic lg" style="background:var(--s0);color:var(--tf)">' + M(s.icon, 'lg') + '</span><div class="grow"><h2>' + E(s.label) + '</h2><p style="margin-top:4px">' + E(s.blurb) + '</p></div></div>' +
      '<p class="sm row" style="gap:8px;margin-top:12px;opacity:.9">' + M('lightbulb', 'sm') + E(s.tip) + '</p>' +
      '<div class="row wrap" style="margin-top:14px;gap:8px"><button class="btn sm" data-act="stageRoad">' + M('route', 'sm') + 'Build my roadmap</button><button class="btn sm o" style="background:var(--s0);border-color:transparent;color:var(--on)" data-act="stageAll">All ' + all.length + ' routes</button></div></div>' +
      '<div class="chips" style="margin-top:14px"><button class="chip" data-act="homeField" data-id="" aria-pressed="' + !H.field + '">All fields</button>' + Object.keys(gs).sort(function (a, b) { return gs[b] - gs[a]; }).map(function (k) { var g = V.grp(k); return '<button class="chip" data-act="homeField" data-id="' + k + '" aria-pressed="' + (H.field === k) + '">' + M(g[1]) + g[0] + '<span class="xs mut">' + gs[k] + '</span></button>'; }).join('') + '</div>' +
      '<div class="hs stag" style="margin-top:12px">' + rs.slice(0, 8).map(function (r, i) { return ui.course(r, i); }).join('') + '</div>' +
      (top.length ? '<div class="sec" style="margin-top:18px"><div class="hd"><h3>Careers these lead to</h3></div><div class="chips">' + top.map(function (c) { return '<button class="chip pay" data-go="career/' + c.id + '"><b>' + E(c.name) + '</b><span class="xs mut">' + V.npr(V.mid(c.salary.entry)) + '</span></button>'; }).join('') + '</div></div>' : '');
  }
  V.acts.homeField = function (el) { V.st.home.field = el.dataset.id; V.$('#stagePanel').innerHTML = stagePanel(); };
  V.acts.stageRoad = function () { var R = V.st.road; R.stage = V.st.home.stage; R.path = []; R.field = V.st.home.field; V.go('roadmap'); };
  V.acts.stage = function (el) {
    V.st.home.stage = el.dataset.id; V.st.home.field = ''; V.$$('#stages .stg').forEach(function (b) { b.setAttribute('aria-pressed', b === el); });
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
    var tools = [['roadmap', 'Roadmap', 'Build a path step by step', 'route', 't-rc'], ['match', 'Match me', 'Five questions, ranked routes', 'auto_awesome', 't-pc'], ['roi', 'Is it worth it', 'Cost against what you earn', 'savings', 't-gc'], ['colleges', 'Colleges by district', 'Map of all 77 districts', 'map', 't-yc'], ['schol', 'Deadline planner', 'Grants and exams by month', 'calendar_month', 't-tc'], ['plan', 'My plan', 'Saved courses, cost, deadlines', 'bookmark', 't-sc']];
    var fields = Object.keys(V.GROUPS).filter(function (k) { return PW.routes.some(function (r) { return r.group === k; }); });
    return { title: 'Home', html:
      (V.store.me ? V.foryou() : '') + '<section class="hero' + (V.store.me ? ' alt' : '') + '"><div class="hero-t">' + (V.store.me ? '<h2>Explore any stage</h2><p class="mut sm" style="margin-top:4px">Courses, colleges, careers and grants that follow each one.</p>' : '<h1>Where are you now?</h1><p class="mut">Pick your stage. See every course, college, career and grant that follows.</p>') + '</div>' +
      '<div class="stages stag" id="stages">' + PW.stages.map(function (s, i) { return '<button class="stg card click ' + V.STAGE_T[s.id] + ' tone" style="--i:' + i + '" data-act="stage" data-id="' + s.id + '" aria-pressed="' + (s.id === V.st.home.stage) + '"><span class="ic" style="background:var(--s0);color:var(--tf)">' + M(s.icon) + '</span><b>' + E(s.label.replace('After ', 'After ')) + '</b><span class="xs">' + PW.routes.filter(function (r) { return r.stage === s.id; }).length + ' routes</span></button>'; }).join('') + '</div></section>' +
      (V.store.me ? '' : V.foryou()) + V.recentHtml() + (V.st.road && V.st.road.path.length ? '<button class="card click flat row" style="margin-top:14px;width:100%;text-align:left" data-go="roadmap">' + M('route') + '<div class="grow"><b>Continue your roadmap</b><div class="xs mut">' + V.st.road.path.length + ' step' + (V.st.road.path.length > 1 ? 's' : '') + ', ending at ' + E(V.R[V.st.road.path[V.st.road.path.length - 1]].name) + '</div></div>' + M('arrow_forward', 'sm') + '</button>' : '') +
      '<div id="stagePanel" style="margin-top:14px">' + stagePanel() + '</div>' +
      '<div class="grid g3 stag nums sec">' + nums.map(function (n, i) { return '<div class="stat ' + n[2] + '" style="--i:' + i + '"><b data-count="' + st[n[0]] + '">0</b><span>' + n[1] + '</span></div>'; }).join('') + '</div>' +
      (open.length || exOpen.length ? ui.sec('Open this month', '<div class="hs stag">' + open.map(function (s, i) { return ui.schol(s, i); }).join('') + exOpen.map(function (g, i) { return ui.exam(g, i); }).join('') + '</div>', ['schol', 'All deadlines']) : '') +
      ui.sec('Tools', '<div class="grid g3 stag">' + tools.map(function (t, i) { return '<button class="card click tone ' + t[4] + ' tool" style="--i:' + i + '" data-go="' + t[0] + '">' + M(t[3], 'lg') + '<h3>' + t[1] + '</h3><span class="sm">' + t[2] + '</span></button>'; }).join('') + '</div>') +
      ui.sec('Careers with the best outlook', '<div class="hs stag">' + hot.map(function (c, i) { return ui.career(c, i); }).join('') + '</div>', ['careers', 'All careers']) +
      ui.sec('Colleges near you', '<div class="card flat row wrap"><div class="grow"><h3>Pick your district</h3><div class="sm mut">See every college, school and institute there.</div></div><label class="fld" style="min-width:220px">' + M('location_on') + '<select id="homeDist"><option value="">Choose district</option>' + dists.map(function (d) { return '<option>' + d + '</option>'; }).join('') + '</select></label><button class="btn t" data-act="locate">' + M('my_location', 'sm') + 'Near me</button><button class="btn" data-act="districtGo">Show colleges</button></div>') +
      '<p class="xs mut" style="margin-top:28px">Figures are indicative ranges reviewed ' + E(PW.reviewed) + '. Check with the college or the official body before you pay.</p>' };
  };
})();
