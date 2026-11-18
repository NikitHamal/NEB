/* Pathways v5 My plan: everything the student saved, the cost, the deadlines, one copyable summary. */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, ch = V.ch, M = V.ms, E = V.esc, PW = V.PW;
  var KINDS = [['course', 'Courses', 'school', function (id) { return V.R[id] && ui.course(V.R[id]); }], ['college', 'Colleges', 'apartment', function (id) { return V.P[id] && ui.college(V.P[id]); }], ['career', 'Careers', 'work', function (id) { return V.C[id] && ui.career(V.C[id]); }],
    ['exam', 'Exams', 'quiz', function (id) { return V.G[id] && ui.exam(V.G[id]); }], ['country', 'Countries', 'public', function (id) { return V.A[id] && ui.country(V.A[id]); }], ['schol', 'Scholarships', 'workspace_premium', function (id) { return V.S[id] && ui.schol(V.S[id]); }]];
  var NAME = { course: function (i) { return V.R[i] && V.R[i].name; }, college: function (i) { return V.P[i] && V.P[i].name; }, career: function (i) { return V.C[i] && V.C[i].name; }, exam: function (i) { return V.G[i] && V.G[i].name; }, country: function (i) { return V.A[i] && V.A[i].country; }, schol: function (i) { return V.S[i] && V.S[i].name; } };
  function text() {
    var out = ['My Pathways plan', ''];
    KINDS.forEach(function (k) { var a = (V.store.saved[k[0]] || []).map(NAME[k[0]]).filter(Boolean); if (a.length) out.push(k[1] + ': ' + a.join('; ')); });
    return out.join('\n') + '\n\nBuilt on NEBians Pathways';
  }
  V.acts.copyPlan = function () { var t = text(); (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { V.toast('Plan copied', 'content_copy'); }, function () { V.toast('Copy is not available here', 'info'); }); };
  V.acts.printPlan = function () { window.print(); };
  V.acts.clearPlan = function () { V.store.saved = {}; V.persist(); V.badge(); V.render(); };
  V.views.plan = function () {
    var sv = V.store.saved, n = V.savedCount();
    if (!n) return { title: 'My plan', html: ui.head('My plan', 'Everything you save lands here.') + '<div class="empty">' + M('bookmark_add') + '<p>Nothing saved yet. Tap the bookmark on any course, college, career, exam, country or scholarship.</p><div class="row wrap" style="justify-content:center;margin-top:12px"><button class="btn" data-go="courses">Browse courses</button><button class="btn t" data-go="match">Match me</button></div></div>' };
    var courses = (sv.course || []).map(function (i) { return V.R[i]; }).filter(Boolean), cost = courses.reduce(function (s, r) { return s + V.mid(r.fee); }, 0);
    var dl = (sv.schol || []).map(function (i) { return V.S[i]; }).filter(function (s) { return s && s.open; }).map(function (s) { return { n: s.name, w: s.open, c: 'var(--good)', a: 'data-act="schol" data-id="' + s.id + '"' }; })
      .concat((sv.exam || []).map(function (i) { return V.G[i]; }).filter(function (g) { return g && g.apply; }).map(function (g) { return { n: g.name, w: g.apply, c: 'var(--p)', a: 'data-go="exam/' + g.id + '"' }; }));
    var pay = V.avg(courses.reduce(function (a, r) { return a.concat(r._c); }, []), function (c) { return V.mid(c.salary.entry); });
    return { title: 'My plan', html: ui.head('My plan', n + ' saved. Kept on this device.', '<div class="row"><button class="btn t sm" data-act="printPlan">' + M('print', 'sm') + 'Print</button><button class="btn t sm" data-act="copyPlan">' + M('content_copy', 'sm') + 'Copy</button><button class="btn g sm" data-act="clearPlan">Clear</button></div>') +
      (courses.length ? '<div class="grid g3"><div class="stat t-pc"><b>' + V.npr(cost) + '</b><span>Typical cost of ' + courses.length + ' saved course' + (courses.length > 1 ? 's' : '') + '</span></div><div class="stat t-gc"><b>' + (pay ? V.npr(pay) : 'n/a') + '</b><span>Average starting pay of linked careers</span></div><div class="stat t-yc"><b>' + (sv.college || []).length + '</b><span>Colleges shortlisted</span></div></div>' : '') +
      (dl.length ? ui.sec('Your deadlines', '<div class="card" style="padding:6px 16px">' + dl.map(function (i) { return '<button class="lane" style="width:100%;text-align:left" ' + i.a + '><span class="nm2">' + E(i.n) + '<span class="xs mut" style="display:block">' + V.MONTHS[i.w[0] - 1] + ' to ' + V.MONTHS[i.w[1] - 1] + '</span></span>' + ch.months(i.w[0], i.w[1], i.c) + '</button>'; }).join('') + '</div>') : '') +
      KINDS.map(function (k) { var a = (sv[k[0]] || []).map(k[3]).filter(Boolean); return a.length ? ui.sec(k[1] + ' (' + a.length + ')', '<div class="grid g3 stag">' + a.join('') + '</div>') : ''; }).join('') };
  };
})();
