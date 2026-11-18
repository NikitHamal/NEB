/* Pathways v5 college detail and the compare table (colleges and countries). */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, M = V.ms, E = V.esc, PW = V.PW;
  V.views.college = function (id) {
    var p = V.P[id]; if (!p) return ui.empty('College not found.');
    var rs = Object.keys(p._r).map(function (i) { return V.R[i]; }).filter(Boolean).sort(function (a, b) { return a.stage.localeCompare(b.stage) || a.name.localeCompare(b.name); });
    var near = PW.providers.filter(function (x) { return x.district === p.district && x.id !== p.id; }).sort(function (a, b) { return b._n - a._n; }).slice(0, 4);
    var icon = p.kind === 'School' ? 'backpack' : p.kind === 'University' ? 'account_balance' : /medical|dental/i.test(p.kind) ? 'local_hospital' : 'apartment';
    return { title: p.name, html: '<div class="crumbs">' + ui.crumb('Colleges', 'colleges') + '</div>' +
      '<section class="dh card tone t-sc"><div class="row" style="align-items:flex-start"><span class="ic lg" style="background:var(--s0);color:var(--tf)">' + M(icon, 'lg') + '</span><div class="grow"><h1>' + E(p.name) + '</h1><div class="row" style="gap:4px;margin-top:6px">' + M('location_on', 'sm') + E(p.place) + ', ' + E(p.district) + '</div></div>' + V.saveBtn('college', p.id) + '</div>' +
      '<div class="row wrap" style="gap:6px"><span class="tag" style="background:var(--s0);color:var(--on)">' + E(p.kind) + '</span><span class="tag" style="background:var(--s0);color:var(--on)">' + E(V.cap(p.sector)) + '</span>' + (p.seats ? '<span class="tag" style="background:var(--s0);color:var(--on)">' + p.seats + ' seats</span>' : '') + '</div>' +
      '<div class="row wrap">' + (p.website ? '<a class="btn" target="_blank" rel="noopener" href="' + E(p.website) + '">' + M('open_in_new', 'sm') + 'Website</a>' : '') + V.cmpBtn('college', p.id).replace('class="chip"', 'class="chip" style="background:var(--s0)"') + '<a class="btn t" target="_blank" rel="noopener" href="https://www.google.com/maps/search/' + encodeURIComponent(p.name + ' ' + p.place) + '">' + M('map', 'sm') + 'Open in Maps</a></div></section>' +
      '<div class="cols sec"><div><div class="card"><h3>About</h3>' + V.facts(p.note) + '</div>' +
      ui.sec('Courses offered (' + rs.length + ')', rs.length ? '<div class="col">' + rs.map(function (r) {
        var f = (p.fees || {})[r.id], sn = (p.route_seats || {})[r.id], g = V.grp(r.group);
        return '<button class="card click row" data-go="course/' + r.id + '"><span class="ic sm ' + g[2] + '">' + M(g[1], 'sm') + '</span><div class="grow" style="text-align:left"><b>' + E(r.name) + '</b><div class="xs mut">' + E(r.years) + ' &middot; ' + E(V.ST[r.stage].label) + '</div></div><div style="text-align:right"><b class="sm">' + (f ? V.range(f) : '~' + V.range(r.fee)) + '</b><div class="xs mut">' + (sn ? sn + ' seats' : f ? 'college fee' : 'typical fee') + '</div></div></button>';
      }).join('') + '</div>' : '<div class="card flat sm mut">Course list is not published for this place yet. Ask the college for its current programmes and affiliation.</div>') + '</div>' +
      '<aside class="side col"><div class="card"><h3>Facts</h3><div class="kv"><span>Type</span><b>' + E(p.kind) + '</b></div><div class="kv"><span>Sector</span><b>' + E(V.cap(p.sector)) + '</b></div><div class="kv"><span>District</span><b>' + E(p.district) + '</b></div><div class="kv"><span>Place</span><b>' + E(p.place) + '</b></div>' + (p.seats ? '<div class="kv"><span>Seats</span><b>' + p.seats + '</b></div>' : '') + '</div>' +
      '<div class="card tone t-yc col"><h3>Before you pay</h3><div class="sm">Confirm affiliation, seats and fee in writing.</div><button class="btn" data-go="guide/check-college">Open checklist</button></div>' +
      (near.length ? '<div class="card"><h3 style="margin-bottom:8px">Also in ' + E(p.district) + '</h3>' + near.map(function (n) { return '<button class="pick" style="margin-bottom:6px" data-go="college/' + n.id + '"><div class="grow"><b class="sm">' + E(n.name) + '</b><div class="xs mut">' + E(n.kind) + '</div></div>' + M('chevron_right') + '</button>'; }).join('') + '</div>' : '') + '</aside></div>' };
  };
  var win = function (vals, low) { var best = low ? Math.min.apply(null, vals) : Math.max.apply(null, vals); return vals.map(function (v) { return v === best && vals.filter(function (x) { return x === best; }).length < vals.length ? ' class="win"' : ''; }); };
  function table(cols, rows) {
    return '<div class="scroll-x"><table class="tbl cmpx"><thead><tr><th></th>' + cols.map(function (c) { return '<th style="color:var(--on);font-size:14px;width:auto"><button data-go="' + c.go + '" style="text-align:left;font-weight:600;color:var(--p)">' + E(c.name) + '</button></th>'; }).join('') + '</tr></thead><tbody>' +
      rows.map(function (r) { var w = r.nums ? win(r.nums, r.low) : []; return '<tr><th>' + r.l + '</th>' + r.v.map(function (v, i) { return '<td' + (w[i] || '') + '>' + v + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table></div>';
  }
  V.views.compare = function (kind) {
    var ids = V.cmp.kind === kind ? V.cmp.ids : [], body;
    if (ids.length < 2) body = ui.empty('Pick at least two ' + (kind === 'country' ? 'countries' : 'colleges') + ' to compare.', 'compare_arrows');
    else if (kind === 'country') {
      var as = ids.map(function (i) { return V.A[i]; }), tot = function (a) { return V.mid(a.tuition) + V.mid(a.living); };
      body = table(as.map(function (a) { return { name: a.country, go: 'country/' + a.id }; }), [
        { l: 'Tuition a year', v: as.map(function (a) { return V.range(a.tuition); }), nums: as.map(function (a) { return V.mid(a.tuition); }), low: 1 },
        { l: 'Living a year', v: as.map(function (a) { return V.range(a.living); }), nums: as.map(function (a) { return V.mid(a.living); }), low: 1 },
        { l: 'Total a year', v: as.map(function (a) { return '<b>' + V.npr(tot(a)) + '</b>'; }), nums: as.map(tot), low: 1 },
        { l: 'Work while studying', v: as.map(function (a) { return a.work_hours ? a.work_hours + ' hours a week' : 'See rules'; }), nums: as.map(function (a) { return a.work_hours || 0; }) },
        { l: 'Stay back', v: as.map(function (a) { return E(a.stay_back || 'See rules'); }) }, { l: 'Language test', v: as.map(function (a) { return E(a.exams.join(', ')); }) },
        { l: 'Intakes', v: as.map(function (a) { return E(a.intakes); }) }, { l: 'Visa steps', v: as.map(function (a) { return a.visa.steps.length + ' steps, about ' + a.visa.steps.reduce(function (s, x) { return s + x[1]; }, 0) + ' days'; }) },
        { l: 'Grants listed', v: as.map(function (a) { return a.scholarships.length; }), nums: as.map(function (a) { return a.scholarships.length; }) }]);
    } else {
      var ps = ids.map(function (i) { return V.P[i]; }), shared = {}; ps.forEach(function (p) { Object.keys(p._r).forEach(function (r) { shared[r] = (shared[r] || 0) + 1; }); });
      var common = Object.keys(shared).filter(function (r) { return shared[r] >= 2 && V.R[r]; }).slice(0, 8);
      body = table(ps.map(function (p) { return { name: p.name, go: 'college/' + p.id }; }), [
        { l: 'Type', v: ps.map(function (p) { return E(p.kind); }) }, { l: 'Sector', v: ps.map(function (p) { return E(V.cap(p.sector)); }) }, { l: 'Where', v: ps.map(function (p) { return E(p.place + ', ' + p.district); }) },
        { l: 'Seats', v: ps.map(function (p) { return p.seats || 'n/a'; }), nums: ps.map(function (p) { return p.seats || 0; }) }, { l: 'Courses listed', v: ps.map(function (p) { return p._n; }), nums: ps.map(function (p) { return p._n; }) },
        { l: 'Website', v: ps.map(function (p) { return p.website ? '<a href="' + E(p.website) + '" target="_blank" rel="noopener" style="color:var(--p)">Visit</a>' : 'None listed'; }) }]
        .concat(common.map(function (r) { var fs = ps.map(function (p) { return (p.fees || {})[r] ? V.mid(p.fees[r]) : V.mid(V.R[r].fee); }); return { l: E(V.R[r].name) + ' fee', v: ps.map(function (p, i) { return (p.fees || {})[r] ? V.range(p.fees[r]) : '<span class="mut">typical ' + V.range(V.R[r].fee) + '</span>'; }), nums: ps.every(function (p) { return (p.fees || {})[r]; }) ? fs : null, low: 1 }; })));
    }
    return { title: 'Compare', html: '<div class="crumbs">' + ui.crumb(kind === 'country' ? 'Abroad' : 'Colleges', kind === 'country' ? 'abroad' : 'colleges') + '</div>' + ui.head('Compare', 'Green marks the better value in each row.', '<button class="btn t sm" data-act="cmpclear2">' + M('delete', 'sm') + 'Clear</button>') + body };
  };
  V.acts.cmpclear2 = function () { V.acts.cmpclear(); V.render(); };
})();
