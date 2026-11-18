/* Pathways v5 profile: a small saved profile (stage, interests, budget, district, goal) that powers the For you feed on Home. */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, M = V.ms, E = V.esc, PW = V.PW;
  var GOALS = [['job', 'A job soon', 'work'], ['abroad', 'Study abroad', 'flight_takeoff'], ['govt', 'Government service', 'account_balance'], ['biz', 'My own business', 'storefront'], ['unsure', 'Not sure yet', 'help']];
  var draft = null;
  function me() { return V.store.me || null; }
  function dists() { return Object.keys(PW.providers.reduce(function (m, p) { if (p.district) m[p.district] = 1; return m; }, {})).sort(); }
  function fields(stage) { var g = {}; PW.routes.forEach(function (r) { if (!stage || r.stage === stage) g[r.group] = 1; }); return Object.keys(g).filter(function (k) { return k !== 'school'; }); }
  function inDist(r, d) { return d ? r._pro.filter(function (p) { return p.district === d; }).length : 0; }
  function score(r, m) {
    var s = r._dem * 10 - r._comp * 2 + Math.min(r._pro.length, 60) / 6;
    if (m.groups.indexOf(r.group) >= 0) s += 30;
    if (r.fee[0] <= V.CAPS[m.cap]) s += 10; else s -= 30;
    if (m.goal === 'abroad') s += V.avg(r._c, function (c) { return c.abroad || 0; }) * 4;
    if (m.goal === 'job') s += Math.min(r._pay / 4000, 12);
    if (m.goal === 'biz' && r.group === 'biz') s += 10;
    s += Math.min(inDist(r, m.district), 3) * 3;
    return s;
  }
  function reason(r, m) {
    var a = [], n = inDist(r, m.district);
    if (m.groups.indexOf(r.group) >= 0) a.push(V.grp(r.group)[0]);
    if (n) a.push(n + ' in ' + m.district); else if (r.fee[0] <= V.CAPS[m.cap] && m.cap < 6) a.push('Within budget');
    if (!a.length) a.push('In demand');
    return a.slice(0, 2).join(' / ');
  }
  function picks(m) {
    return PW.routes.filter(function (r) { return r.stage === m.stage && r.group !== 'school'; }).sort(function (a, b) { return score(b, m) - score(a, m); });
  }
  V.foryou = function () {
    var m = me();
    if (!m) return '<button class="card click row fyo" data-act="me" style="margin-top:14px;width:100%;text-align:left"><span class="ic t-tc">' + M('auto_awesome') + '</span><div class="grow"><b>Make Pathways yours</b><div class="xs mut">Stage, interests, budget and district. Stays on this device.</div></div><span class="btn sm t">Set up</span></button>';
    var st = V.ST[m.stage], rs = picks(m), top = rs.slice(0, 6), n = PW.scholarships.filter(function (s) { return V.ch.inWindow(s.open); }).length;
    var dn = m.district ? PW.providers.filter(function (p) { return p.district === m.district; }).length : 0;
    var summary = [st.label].concat(m.groups.map(function (g) { return V.grp(g)[0]; }).slice(0, 2), m.cap < 6 ? ['Up to ' + V.CAPL[m.cap].replace('NPR ', '')] : [], m.district ? [m.district] : []);
    return '<section class="sec fy"><div class="hd"><h2>For you</h2><button class="more" data-act="me">' + M('edit', 'sm') + 'Edit</button></div>' +
      '<div class="chips fysum">' + summary.map(function (x) { return '<span class="tag">' + E(x) + '</span>'; }).join('') + '</div>' +
      '<div class="hs stag" style="margin-top:12px">' + top.map(function (r, i) { return ui.course(r, i, reason(r, m)); }).join('') + '</div>' +
      '<div class="grid g3 stag" style="margin-top:12px">' +
      '<button class="card click flat fyt" style="--i:0" data-act="meColleges">' + M('apartment', 'lg') + '<div><b>' + (m.district ? dn + ' places in ' + E(m.district) : 'Colleges near you') + '</b><span class="xs mut">' + (m.district ? 'Open the list' : 'Pick a district in your profile') + '</span></div></button>' +
      '<button class="card click flat fyt" style="--i:1" data-go="schol">' + M('workspace_premium', 'lg') + '<div><b>' + n + ' grants open this month</b><span class="xs mut">See deadlines</span></div></button>' +
      '<button class="card click flat fyt" style="--i:2" data-act="meRoad">' + M('route', 'lg') + '<div><b>Roadmap from ' + E(st.label.replace('After ', '')) + '</b><span class="xs mut">Time, fees and starting pay</span></div></button></div></section>';
  };
  function chips(id, items, on, multi) {
    return '<div class="chips wrap" id="' + id + '">' + items.map(function (x) { return '<button class="chip" data-act="meSet" data-k="' + id + '" data-v="' + E(x[0]) + '" aria-pressed="' + (multi ? on.indexOf(x[0]) >= 0 : on === x[0]) + '">' + (x[2] ? M(x[2]) : '') + E(x[1]) + '</button>'; }).join('') + '</div>';
  }
  function sheet() {
    var d = draft;
    return '<div class="mesh"><div class="row"><h2 class="grow">Make Pathways yours</h2><button class="save" data-act="meClose" aria-label="Close">' + M('close') + '</button></div>' +
      '<div class="pf"><h4>I am</h4>' + chips('mp-stage', PW.stages.map(function (s) { return [s.id, s.label, s.icon]; }), d.stage) + '</div>' +
      '<div class="pf" id="mp-fw"><h4>I like <span class="xs mut">pick up to 3</span></h4>' + chips('mp-groups', fields(d.stage).map(function (k) { return [k, V.grp(k)[0], V.grp(k)[1]]; }), d.groups, true) + '</div>' +
      '<div class="pf"><h4>I want</h4>' + chips('mp-goal', GOALS, d.goal) + '</div>' +
      '<div class="pf"><div class="row"><h4 class="grow">Budget for the whole course</h4><b id="mp-capl">' + V.CAPL[d.cap] + '</b></div><input class="rng" type="range" min="0" max="6" value="' + d.cap + '" data-in="mecap"></div>' +
      '<div class="pf"><h4>My district</h4><label class="fld">' + M('location_on') + '<select data-in="medist"><option value="">Anywhere in Nepal</option>' + dists().map(function (x) { return '<option' + (x === d.district ? ' selected' : '') + '>' + E(x) + '</option>'; }).join('') + '</select></label></div>' +
      '<div class="row" style="margin-top:20px;gap:8px"><button class="btn grow" data-act="meSave">Show my feed</button>' + (me() ? '<button class="btn o" data-act="meReset">Reset</button>' : '') + '</div></div>';
  }
  V.acts.me = function () { var m = me(); draft = m ? { stage: m.stage, groups: m.groups.slice(), cap: m.cap, district: m.district, goal: m.goal } : { stage: V.st.home.stage || 'after12', groups: [], cap: 6, district: '', goal: 'unsure' }; V.sheet(sheet()); };
  V.acts.meClose = function () { V.closeSheet(); };
  V.acts.meSet = function (el) {
    var k = el.dataset.k, v = el.dataset.v;
    if (k === 'mp-stage') { draft.stage = v; draft.groups = draft.groups.filter(function (g) { return fields(v).indexOf(g) >= 0; }); var f = V.$('#mp-fw'), h = f.cloneNode(false); f.innerHTML = '<h4>I like <span class="xs mut">pick up to 3</span></h4>' + chips('mp-groups', fields(v).map(function (x) { return [x, V.grp(x)[0], V.grp(x)[1]]; }), draft.groups, true); }
    if (k === 'mp-goal') draft.goal = v;
    if (k === 'mp-groups') { var i = draft.groups.indexOf(v); if (i >= 0) draft.groups.splice(i, 1); else if (draft.groups.length < 3) draft.groups.push(v); else return V.toast('Pick up to 3', 'info'); }
    V.$$('#' + k + ' .chip').forEach(function (b) { b.setAttribute('aria-pressed', k === 'mp-groups' ? draft.groups.indexOf(b.dataset.v) >= 0 : k === 'mp-stage' ? draft.stage === b.dataset.v : draft.goal === b.dataset.v); });
  };
  V.ins.mecap = function (el) { draft.cap = +el.value; V.$('#mp-capl').textContent = V.CAPL[draft.cap]; };
  V.ins.medist = function (el) { draft.district = el.value; };
  V.acts.meSave = function () {
    V.store.me = draft; V.persist(); var d = draft;
    V.st.home.stage = d.stage; V.st.home.field = d.groups[0] || '';
    Object.assign(V.st.courses, { stage: d.stage, group: d.groups.length === 1 ? d.groups[0] : '', cap: d.cap });
    if (d.district) Object.assign(V.st.colleges, { district: d.district, n: 24 });
    V.closeSheet(); V.toast('Your feed is ready', 'auto_awesome'); if (V.parse().name === 'home') V.render(); else V.go('home');
  };
  V.acts.meReset = function () { delete V.store.me; V.persist(); V.closeSheet(); V.toast('Profile cleared', 'restart_alt'); V.render(); };
  V.acts.meColleges = function () { var m = me(); if (m && m.district) Object.assign(V.st.colleges, { district: m.district, n: 24 }); V.go('colleges'); };
  V.acts.meRoad = function () { var m = me(), R = V.st.road; R.stage = m.stage; R.path = []; R.field = m.groups[0] || ''; V.go('roadmap'); };
})();
