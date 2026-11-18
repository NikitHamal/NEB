/* Pathways v5 match: a five step wizard that ranks routes with the reasons for each. */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, ch = V.ch, M = V.ms, E = V.esc, PW = V.PW;
  var S = V.st.match = V.st.match || { step: 0, stage: '', ints: [], budget: 0, where: 'any', dist: '', prio: '' };
  var INT = { build: ['Build things', 'engineering, software, design', 'construction', ['tech']], heal: ['Heal people', 'medicine, nursing, care', 'health_and_safety', ['health']], num: ['Numbers and business', 'finance, trade, management', 'monitoring', ['biz']], make: ['Create', 'art, media, design', 'brush', ['arts']], disc: ['Discover', 'science, research', 'biotech', ['sci']], serve: ['Teach and serve', 'teaching, government', 'diversity_3', ['edu', 'gov']], nature: ['Work with nature', 'farming, forests, animals', 'forest', ['ag']], law: ['Justice and law', 'courts, rights, policy', 'balance', ['law']] };
  var BUD = [['Up to NPR 3 lakh', 3e5], ['Up to NPR 10 lakh', 1e6], ['Up to NPR 30 lakh', 3e6], ['No limit', 1e12]];
  var PRI = { pay: ['High pay', 'Best starting salary', 'payments'], safe: ['Steady jobs', 'High demand in Nepal', 'shield'], abroad: ['Go abroad', 'Skills that travel', 'flight_takeoff'], open: ['Less competition', 'Easier to get in and get hired', 'trending_down'], quick: ['Earn sooner', 'Shorter courses', 'bolt'] };
  var yrs = function (r) { var m = r.years.match(/\d+(\.\d+)?/); return m ? +m[0] : 3; };
  function score(r) {
    var why = [], s = 0, gi = S.ints.reduce(function (a, k) { return a.concat(INT[k][3]); }, []);
    if (gi.indexOf(r.group) >= 0) { s += 38; why.push(V.grp(r.group)[0] + ' fits your interests'); } else if (!S.ints.length) s += 15;
    if (r.fee[0] <= BUD[S.budget][1]) { s += 14; if (r.fee[0] <= BUD[S.budget][1] / 2) why.push('Fits your budget'); } else s -= 18;
    if (S.where === 'abroad') { var ab = V.avg(r._c, function (c) { return c.abroad; }); s += ab * 3; if (ab >= 4) why.push('Skills that travel'); }
    else if (S.where === 'dist') { var here = r._pro.filter(function (p) { return p.district === S.dist; }).length; if (here) { s += 16; why.push(here + ' in ' + S.dist); } } else s += Math.min(10, r._pro.length);
    if (S.prio === 'pay') { s += Math.min(18, r._pay / 3000); if (r._pay > 40000) why.push('Starts near ' + V.npr(r._pay)); }
    if (S.prio === 'safe') { s += r._dem * 3.6; if (r._dem >= 4) why.push('High demand'); }
    if (S.prio === 'abroad') s += V.avg(r._c, function (c) { return c.abroad; }) * 3.6;
    if (S.prio === 'open') { s += (5 - r._comp) * 3.6; if (r._comp && r._comp <= 3) why.push('Lower competition'); }
    if (S.prio === 'quick') { s += Math.max(0, 18 - yrs(r) * 4); if (yrs(r) <= 2) why.push('Done in ' + r.years); }
    s += r._dem * 1.5; return { r: r, s: Math.max(0, Math.min(99, Math.round(s))), why: why.slice(0, 3) };
  }
  function opt(k, t, sub, ic, on, act, extra) { return '<button class="opt" data-act="' + act + '" data-v="' + k + '" aria-pressed="' + on + '">' + M(ic) + '<span><b>' + t + '</b>' + (sub ? '<small>' + sub + '</small>' : '') + '</span></button>'; }
  function body() {
    var st = S.step, h = '<div class="wbar">' + [0, 1, 2, 3, 4].map(function (i) { return '<i class="' + (i <= st ? 'on' : '') + '"></i>'; }).join('') + '</div>', nav = function (ok) { return '<div class="row" style="justify-content:space-between;margin-top:18px"><button class="btn g" data-act="mback"' + (st ? '' : ' disabled') + '>' + M('arrow_back', 'sm') + 'Back</button><button class="btn" data-act="mnext"' + (ok ? '' : ' disabled') + '>' + (st === 4 ? 'Show my matches' : 'Next') + M('arrow_forward', 'sm') + '</button></div>'; };
    if (st === 0) return h + '<h2>Where are you now?</h2><div class="opts c2" style="margin-top:14px">' + PW.stages.map(function (s) { return opt(s.id, E(s.label), E(s.blurb), s.icon, S.stage === s.id, 'm0'); }).join('') + '</div>' + nav(S.stage);
    if (st === 1) return h + '<h2>What pulls you in?</h2><p class="sm mut">Pick up to three.</p><div class="opts c2" style="margin-top:14px">' + Object.keys(INT).map(function (k) { return opt(k, INT[k][0], INT[k][1], INT[k][2], S.ints.indexOf(k) >= 0, 'm1'); }).join('') + '</div>' + nav(S.ints.length);
    if (st === 2) return h + '<h2>What can the course cost?</h2><p class="sm mut">Total course fee, not a year.</p><div class="opts c2" style="margin-top:14px">' + BUD.map(function (b, i) { return opt(i, b[0], '', 'payments', S.budget === i, 'm2'); }).join('') + '</div>' + nav(true);
    if (st === 3) { var ds = Object.keys(PW.providers.reduce(function (m, p) { m[p.district] = 1; return m; }, {})).sort(); return h + '<h2>Where do you want to study?</h2><div class="opts" style="margin-top:14px">' + opt('any', 'Anywhere in Nepal', '', 'flag', S.where === 'any', 'm3') + opt('dist', 'Near my district', '', 'location_on', S.where === 'dist', 'm3') + (S.where === 'dist' ? '<label class="fld">' + M('location_on') + '<select data-in="mdist"><option value="">Choose district</option>' + ds.map(function (d) { return '<option' + (S.dist === d ? ' selected' : '') + '>' + d + '</option>'; }).join('') + '</select></label>' : '') + opt('abroad', 'Abroad', '', 'flight_takeoff', S.where === 'abroad', 'm3') + '</div>' + nav(S.where !== 'dist' || S.dist); }
    return h + '<h2>What matters most?</h2><div class="opts c2" style="margin-top:14px">' + Object.keys(PRI).map(function (k) { return opt(k, PRI[k][0], PRI[k][1], PRI[k][2], S.prio === k, 'm4'); }).join('') + '</div>' + nav(S.prio);
  }
  function results() {
    var rs = PW.routes.filter(function (r) { return r.stage === S.stage; }).map(score).sort(function (a, b) { return b.s - a.s; }).slice(0, 8);
    return '<div class="row wrap" style="justify-content:space-between;margin-bottom:12px"><div><h2>Your top matches</h2><div class="sm mut">' + V.ST[S.stage].label + ', ' + S.ints.map(function (k) { return INT[k][0].toLowerCase(); }).join(' and ') + '</div></div><button class="btn t sm" data-act="mreset">' + M('restart_alt', 'sm') + 'Start over</button></div><div class="col stag">' + rs.map(function (x, i) {
      var g = V.grp(x.r.group); return '<article class="card click row" style="--i:' + i + ';align-items:flex-start" data-go="course/' + x.r.id + '"><div class="score">' + ch.ring(x.s, 56, 'Match') + '</div><div class="grow"><h3>' + E(x.r.name) + '</h3><div class="xs mut">' + E(x.r.kind) + ' &middot; ' + E(x.r.years) + ' &middot; ' + V.range(x.r.fee) + '</div><div class="why" style="margin-top:8px">' + x.why.map(function (w) { return '<span class="tag t-gc">' + M('check', 'xs') + E(w) + '</span>'; }).join('') + '</div></div>' + V.saveBtn('course', x.r.id) + '</article>'; }).join('') + '</div><p class="xs mut" style="margin-top:14px">Scores weigh your interests, budget, place and priority. They are a starting point, not a verdict.</p>';
  }
  function paint() { V.$('#wiz').innerHTML = S.step > 4 ? results() : body(); }
  V.acts.m0 = function (el) { S.stage = el.dataset.v; paint(); };
  V.acts.m1 = function (el) { var k = el.dataset.v, i = S.ints.indexOf(k); if (i >= 0) S.ints.splice(i, 1); else if (S.ints.length < 3) S.ints.push(k); paint(); };
  V.acts.m2 = function (el) { S.budget = +el.dataset.v; paint(); };
  V.acts.m3 = function (el) { S.where = el.dataset.v; paint(); };
  V.acts.m4 = function (el) { S.prio = el.dataset.v; paint(); };
  V.ins.mdist = function (el) { S.dist = el.value; V.$$('#wiz .btn:not(.g)').forEach(function (b) { b.disabled = !S.dist; }); };
  V.acts.mnext = function () { S.step++; paint(); window.scrollTo({ top: 0 }); };
  V.acts.mback = function () { S.step = Math.max(0, S.step - 1); paint(); };
  V.acts.mreset = function () { Object.assign(S, { step: 0, stage: '', ints: [], budget: 0, where: 'any', dist: '', prio: '' }); paint(); };
  V.views.match = function () { return { title: 'Match', html: ui.head('Match me', 'Five quick questions. A ranked list with the reason for each pick.') + '<div class="wiz"><div class="card" id="wiz">' + (S.step > 4 ? results() : body()) + '</div></div>' }; };
})();
