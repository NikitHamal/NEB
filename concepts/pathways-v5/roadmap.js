/* Pathways v5 roadmap: build a path step by step from any stage. Shows time, cost, pay and the careers at the end. */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, M = V.ms, E = V.esc, PW = V.PW, ch = V.ch;
  var S = V.st.road = { stage: 'after10', path: [], field: '' };
  if (V.store.road && V.store.road.path) { S.stage = V.store.road.stage; S.path = V.store.road.path.filter(function (i) { return V.R[i]; }); }
  var START = { after8: 'After Class 8', after10: 'After SEE', after12: 'After +2', afterbach: 'After Bachelor' };
  function yrs(r) { var m = /(\d+(?:\.\d+)?)/.exec(r.years || ''); if (!m) return 0; return /month/i.test(r.years) ? +m[1] / 12 : +m[1]; }
  function lastR() { return S.path.length ? V.R[S.path[S.path.length - 1]] : null; }
  function rank(a, b) { return (b._dem * 2 + b._pro.length / 8) - (a._dem * 2 + a._pro.length / 8); }
  function all() {
    var l = lastR();
    return (l ? (l.next || []).map(function (i) { return V.R[i]; }).filter(Boolean) : PW.routes.filter(function (r) { return r.stage === S.stage; })).filter(function (r) { return S.path.indexOf(r.id) < 0; }).sort(rank);
  }
  function totals() {
    var t = { y: 0, lo: 0, hi: 0 };
    S.path.forEach(function (id) { var r = V.R[id]; t.y += yrs(r); t.lo += r.fee ? r.fee[0] : 0; t.hi += r.fee ? r.fee[1] : 0; });
    return t;
  }
  function node(ic, cls) { return '<span class="rn ' + (cls || '') + '">' + ic + '</span>'; }
  function pathCard() {
    var t = totals(), l = lastR(), pay = l && l._pay;
    var steps = S.path.map(function (id, i) {
      var r = V.R[id];
      return '<li class="rs" style="--i:' + i + '">' + node(i + 1) + '<div class="grow"><b data-act="roadInfo" data-id="' + id + '" class="lnk">' + E(r.name) + '</b><div class="xs mut">' + E(r.years) + ' &middot; ' + V.range(r.fee) + '</div></div>' +
        (i === S.path.length - 1 ? '<button class="ib sm" data-act="roadUndo" aria-label="Remove step">' + M('undo', 'sm') + '</button>' : '') + '</li>';
    }).join('');
    var end = l && l._c.length ? '<li class="rs end">' + node(M('work', 'sm'), 'g') + '<div class="grow"><b>' + l._c.length + ' careers open up</b><div class="xs mut">' + E(l._c.slice(0, 3).map(function (c) { return c.name; }).join(', ')) + '</div></div></li>' : '';
    return '<div class="card road-path"><div class="row"><h3 class="grow">Your path</h3>' + (S.path.length ? '<button class="btn g sm" data-act="roadReset">Start over</button>' : '') + '</div>' +
      '<ol class="rl"><li class="rs">' + node(M('flag', 'sm'), 'p') + '<div class="grow"><b>' + START[S.stage] + '</b><div class="xs mut">You are here</div></div></li>' + steps + end + '</ol>' +
      (S.path.length ? '<div class="kpis rk"><div class="kpi"><b>' + +t.y.toFixed(1) + ' yrs</b><span>Study time</span></div><div class="kpi"><b>' + V.npr(t.lo) + ' to ' + V.npr(t.hi).replace('NPR ', '') + '</b><span>Total fees</span></div><div class="kpi"><b>' + (pay ? V.npr(Math.round(pay / 500) * 500) : 'n/a') + '</b><span>Starting pay a month</span></div></div>' +
        '<div class="row wrap" style="margin-top:12px;gap:8px"><button class="btn sm" data-act="roadSave">' + M('bookmark_add', 'sm') + 'Save path</button><button class="btn t sm" data-act="roadCopy">' + M('share', 'sm') + 'Share</button></div>' : '') + '</div>';
  }
  function opt(r, i) {
    var g = V.grp(r.group);
    return '<div class="card click opt" style="--i:' + i + '" role="button" tabindex="0" data-act="roadPick" data-id="' + r.id + '"><span class="ic ' + g[2] + '">' + M(g[1]) + '</span><div class="grow"><h3>' + E(r.name) + '</h3><div class="xs mut">' + E(r.kind) + ' &middot; ' + E(r.years) + ' &middot; ' + V.range(r.fee) + '</div>' +
      '<div class="row wrap" style="gap:12px;margin-top:6px"><span class="xs mut row" style="gap:6px">Demand ' + ch.dots(r._dem, 'var(--good)') + '</span>' + (r._pro.length ? '<span class="xs mut">' + r._pro.length + ' colleges</span>' : '') + ((r.next || []).length ? '<span class="xs mut">' + r.next.length + ' next steps</span>' : '') + '</div></div>' +
      '<span class="ib sm info" data-act="roadInfo" data-id="' + r.id + '" aria-label="Course details" title="Course details">' + M('info', 'sm') + '</span>' + M('arrow_forward', 'sm') + '</div>';
  }
  function body() {
    var l = lastR(), list = all(), groups = {};
    list.forEach(function (r) { groups[r.group] = 1; });
    var fl = S.field && groups[S.field] ? list.filter(function (r) { return r.group === S.field; }) : list;
    if (!groups[S.field]) S.field = '';
    var chips = Object.keys(groups).length > 1 ? '<div class="chips" style="margin-bottom:12px"><button class="chip" data-act="roadField" data-id="" aria-pressed="' + !S.field + '">All</button>' + Object.keys(groups).map(function (k) { var g = V.grp(k); return '<button class="chip" data-act="roadField" data-id="' + k + '" aria-pressed="' + (S.field === k) + '">' + M(g[1]) + g[0] + '</button>'; }).join('') + '</div>' : '';
    var h = l ? 'Next step after ' + E(l.name) : 'Choose your first step';
    var main = '<div class="sec" style="margin-top:0"><div class="hd"><h2>' + h + '</h2><span class="xs mut">' + fl.length + ' options</span></div>' + chips +
      (fl.length ? '<div class="col stag" style="gap:10px">' + fl.slice(0, 12).map(opt).join('') + '</div>' + (fl.length > 12 ? '<p class="xs mut" style="margin-top:10px">Showing the 12 in highest demand. Use the field chips to narrow.</p>' : '') : '<div class="empty">' + M('flag') + '<p>This is the end of the listed steps. See careers and colleges below.</p></div>') + '</div>';
    var extra = '';
    if (l && l._c.length) extra += ui.sec('Careers this opens', '<div class="hs stag">' + l._c.map(function (c, i) { return ui.career(c, i); }).join('') + '</div>');
    if (l && l._pro.length) extra += ui.sec('Where to study ' + E(l.name), '<div class="hs stag">' + l._pro.slice().sort(function (a, b) { return (b.seats || 0) - (a.seats || 0); }).slice(0, 8).map(function (p, i) { return ui.college(p, i); }).join('') + '</div>', ['course/' + l.id, 'Full course page']);
    return '<div class="cols"><div>' + main + extra + '</div><aside class="side">' + pathCard() + '</aside></div>';
  }
  function sync() { V.store.road = { stage: S.stage, path: S.path.slice() }; V.persist(); try { history.replaceState(null, '', '#/roadmap' + (S.path.length ? '/' + S.path.join(',') : '')); } catch (e) {} }
  function refresh(scroll) { sync(); V.$('#roadBody').innerHTML = body(); if (scroll) V.$('#roadBody').scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  V.acts.roadStart = function (el) { S.stage = el.dataset.id; S.path = []; S.field = ''; V.$$('#roadStart .chip').forEach(function (b) { b.setAttribute('aria-pressed', b === el); }); refresh(); };
  V.acts.roadPick = function (el) { S.path.push(el.dataset.id); S.field = ''; refresh(true); };
  V.acts.roadInfo = function (el, e) { e.stopPropagation(); V.go('course/' + el.dataset.id); };
  V.acts.roadUndo = function () { S.path.pop(); S.field = ''; refresh(); };
  V.acts.roadReset = function () { S.path = []; S.field = ''; refresh(); };
  V.acts.roadField = function (el) { S.field = el.dataset.id; refresh(); };
  V.acts.roadSave = function () { var a = V.store.saved.course = V.store.saved.course || []; S.path.forEach(function (id) { if (a.indexOf(id) < 0) a.push(id); }); V.persist(); V.badge(); V.toast('Path saved to My plan', 'bookmark_added'); };
  V.acts.roadCopy = function () {
    var t = totals(), txt = START[S.stage] + ' > ' + S.path.map(function (id) { return V.R[id].name; }).join(' > ') + ' (' + +t.y.toFixed(1) + ' years, ' + V.range([t.lo, t.hi]) + ')\n' + location.href;
    if (navigator.clipboard) navigator.clipboard.writeText(txt); V.toast('Path and link copied', 'content_copy');
  };
  V.views.roadmap = function (arg) {
    var ids = (arg || '').split(',').filter(function (i) { return V.R[i]; });
    if (ids.length) { S.stage = V.R[ids[0]].stage; S.path = ids; S.field = ''; }
    return { title: 'Roadmap', html: ui.head('Roadmap', 'Pick a start, then choose each next step. See time, cost and careers add up.') +
      '<div class="chips" id="roadStart" style="margin-bottom:16px">' + Object.keys(START).map(function (k) { return '<button class="chip" data-act="roadStart" data-id="' + k + '" aria-pressed="' + (S.stage === k) + '">' + M(V.ST[k].icon) + START[k] + '</button>'; }).join('') + '</div><div id="roadBody">' + body() + '</div>' };
  };
})();
