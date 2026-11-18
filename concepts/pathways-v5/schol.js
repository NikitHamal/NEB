/* Pathways v5 grants: scholarship finder and the year planner of deadlines. */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, ch = V.ch, M = V.ms, E = V.esc, PW = V.PW;
  var S = V.st.schol = V.st.schol || { tab: 'find', scope: '', type: '', level: '', open: false, q: '' };
  var LVL = ['plus2', 'bachelor', 'master', 'phd', 'school', 'diploma', 'any'];
  function list() {
    var rs = PW.scholarships.filter(function (s) { return (!S.scope || s.scope === S.scope) && (!S.type || s.type === S.type) && (!S.level || (s.levels || []).indexOf(S.level) >= 0) && (!S.open || ch.inWindow(s.open)) && (!S.q || (s.name + ' ' + s.by + ' ' + s.covers).toLowerCase().indexOf(S.q.toLowerCase()) >= 0); });
    rs.sort(function (a, b) { return (ch.inWindow(b.open) ? 1 : 0) - (ch.inWindow(a.open) ? 1 : 0); });
    return '<div class="cnt">' + rs.length + ' scholarships</div>' + (rs.length ? '<div class="grid g3 stag">' + rs.slice(0, 48).map(function (s, i) { return ui.schol(s, Math.min(i, 12)); }).join('') + '</div>' : ui.empty('No scholarship matches.', 'workspace_premium'));
  }
  function plan() {
    var items = PW.scholarships.filter(function (s) { return s.open; }).map(function (s) { return { n: s.name, w: s.open, c: 'var(--good)', a: 'data-act="schol" data-id="' + s.id + '"', k: s.type }; })
      .concat(PW.govt.filter(function (g) { return g.apply; }).map(function (g) { return { n: g.name, w: g.apply, c: 'var(--p)', a: 'data-go="exam/' + g.id + '"', k: 'Exam' }; }));
    var dist = function (w) { return ((w[0] - V.now) + 12) % 12; };
    items = items.filter(function (i) { return !S.open || ch.inWindow(i.w); }).sort(function (a, b) { return (ch.inWindow(b.w) ? 1 : 0) - (ch.inWindow(a.w) ? 1 : 0) || dist(a.w) - dist(b.w); });
    return '<div class="cnt">' + items.length + ' deadlines. Green is a scholarship, blue is an exam. Today is ' + V.MONTHS[V.now - 1] + '.</div><div class="card" style="padding:6px 16px">' + items.map(function (i) {
      return '<button class="lane" style="width:100%;text-align:left" ' + i.a + '><span class="nm2">' + E(i.n) + '<span class="xs mut" style="display:block">' + E(i.k) + ' &middot; ' + V.MONTHS[i.w[0] - 1] + ' to ' + V.MONTHS[i.w[1] - 1] + '</span></span>' + ch.months(i.w[0], i.w[1], i.c) + '</button>'; }).join('') + '</div>';
  }
  function paint() { V.$('#res').innerHTML = S.tab === 'find' ? list() : plan(); V.$('#sfilt').hidden = S.tab !== 'find'; }
  V.acts.stab = function (el) { S.tab = el.dataset.v; V.$$('#stab button').forEach(function (b) { b.setAttribute('aria-pressed', b === el); }); paint(); };
  V.chipH.s = function (el, k) { var key = k.split('-')[0]; S[key] = el.dataset.v; V.$$('[data-k^="s-' + key + '-"]').forEach(function (b) { b.setAttribute('aria-pressed', b === el); }); paint(); };
  V.ins.sq = function (el) { S.q = el.value; paint(); };
  V.acts.sopen = function (el) { S.open = !S.open; el.setAttribute('aria-pressed', S.open); paint(); };
  function chips(key, items) { return '<div class="chips">' + items.map(function (x) { return '<button class="chip" data-act="chip" data-k="s-' + key + '-' + (x[0] || 'any') + '" data-v="' + x[0] + '" aria-pressed="' + (S[key] === x[0]) + '">' + x[1] + '</button>'; }).join('') + '</div>'; }
  V.views.schol = function () {
    var types = ['Government', 'University', 'Embassy', 'Foundation'];
    return { title: 'Grants', html: ui.head('Scholarships and deadlines', PW.stats.scholarships + ' scholarships, embassy and government ones included, with a year planner.') +
      '<div class="fb"><div class="rowf"><div class="seg" id="stab"><button data-act="stab" data-v="find" aria-pressed="' + (S.tab === 'find') + '">' + M('search', 'sm') + 'Find</button><button data-act="stab" data-v="plan" aria-pressed="' + (S.tab === 'plan') + '">' + M('calendar_month', 'sm') + 'Year planner</button></div>' +
      '<button class="chip" data-act="sopen" aria-pressed="' + S.open + '">' + M('radio_button_checked') + 'Open now</button></div>' +
      '<div class="col" id="sfilt"><label class="fld" style="max-width:480px">' + M('search') + '<input type="search" data-in="sq" placeholder="Search scholarships" value="' + E(S.q) + '"></label>' + chips('scope', [['', 'Everywhere'], ['abroad', 'Abroad'], ['nepal', 'In Nepal']]) + chips('type', [['', 'Any provider']].concat(types.map(function (t) { return [t, t]; }))) + chips('level', [['', 'Any level']].concat(['plus2', 'bachelor', 'master', 'phd'].map(function (l) { return [l, { plus2: '+2', bachelor: 'Bachelor', master: 'Master', phd: 'PhD' }[l]]; }))) + '</div></div><div id="res">' + (S.tab === 'find' ? list() : plan()) + '</div>', after: function () { V.$('#sfilt').hidden = S.tab !== 'find'; } };
  };
})();
