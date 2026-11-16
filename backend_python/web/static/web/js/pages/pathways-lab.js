/* Pathways: Course Lab (match), Questions, Saved, Compare. Matching rules mirror PwMatch.kt:
   1 only courses of the chosen level; 2 stream gate after +2; 3 hard budget and time gates;
   4 interest fit over eight dimensions; 5 a course must reach 55% of the best score and an absolute floor.
   An empty result says so instead of padding the list. */
(function () {
  'use strict';
  var PW = window.PW, h = PW.h, icon = PW.icon, view = PW.view;
  var DIMS = ['Building things', 'Caring for people', 'Business and money', 'Law and public service', 'Creative work', 'Nature and fieldwork', 'Teaching and society', 'Hands on technical skill'];
  function o(label, w, extra) { var x = { label: label, w: w || {} }; for (var k in (extra || {})) x[k] = extra[k]; return x; }
  var Q = [
    { t: 'Which task would you happily do for an hour?', k: 'taste', o: [o('Fix a gadget or write some code', { 0: 3, 7: 1 }), o('Help someone feel better', { 1: 3, 6: 1 }), o('Plan a budget or run a small shop', { 2: 3 }), o('Draw, design or write a story', { 4: 3 }), o('Work with plants, animals or soil', { 5: 3, 7: 1 }), o('Explain something to a friend', { 6: 3, 3: 1 })] },
    { t: 'Which subject feels easiest?', k: 'taste', o: [o('Maths and computer', { 0: 2, 2: 1 }), o('Biology and chemistry', { 1: 2, 5: 1 }), o('Accountancy and economics', { 2: 2 }), o('English and social studies', { 3: 2, 6: 1, 4: 1 }), o('Art and languages', { 4: 2, 6: 1 }), o('Practical and workshop work', { 7: 2, 5: 1 })] },
    { t: 'Where do you picture yourself working?', k: 'taste', o: [o('Office or lab with computers', { 0: 1, 2: 1 }), o('Hospital, clinic or classroom', { 1: 2, 6: 2 }), o('Field, farm or building site', { 5: 2, 7: 2 }), o('Studio or creative space', { 4: 2 }), o('Government office or court', { 3: 2, 2: 1 })] },
    { t: 'How much can the whole course cost?', k: 'budget', o: [o('Under NPR 2 lakh', 0, { cap: 200000 }), o('Up to NPR 6 lakh', 0, { cap: 600000 }), o('Up to NPR 15 lakh', 0, { cap: 1500000 }), o('No limit', 0, { cap: 1e12 })] },
    { t: 'How long can you study before earning?', k: 'time', o: [o('Up to 2 years', 0, { cap: 2 }), o('Up to 4 years', 0, { cap: 4 }), o('Up to 6 years', 0, { cap: 6 }), o('As long as needed', 0, { cap: 99 })] },
    { t: 'What matters most after you finish?', k: 'goal', o: [o('Earn early', 0, { tag: 'early' }), o('A stable job', 0, { tag: 'stable' }), o('Work abroad', 0, { tag: 'abroad' }), o('Serve society', 0, { tag: 'serve' })] },
  ];
  var KEYS = [
    [0, /\b(computer|software|data|civil|electrical|electronics|mechanical|architecture|engineering|it|csit|bit|bca|geomatics|aerospace)\b/],
    [1, /\b(nursing|pharm\w*|medicine|medical|dental|health|physiotherapy|optometry|laboratory|ayurved\w*|mbbs|bds)\b/],
    [2, /\b(account\w*|bank\w*|finance|business|management|hotel|tourism|insurance|bba|bbs|bbm|bim|acca)\b/],
    [3, /\b(law|llb|public|police|army|civil service|administration|lok)\b/],
    [4, /\b(design|media|journalism|music|fine|film|fashion|arts?|bfa|bjmc)\b/],
    [5, /\b(agriculture|forestry|environmental?|veterinary|geology|food|microbiology|biotechnology)\b/],
    [6, /\b(education|teaching|teacher|social|humanities|bed|bsw)\b/],
    [7, /\b(technician|diploma|skill|electrician|plumbing|mechanic|training|pilot|pre-diploma)\b/],
  ];
  var G = { tech: { 0: .9, 7: .3 }, sci: { 5: .6, 0: .5, 6: .2 }, health: { 1: 1, 5: .2 }, biz: { 2: 1, 3: .2 }, arts: { 4: 1, 6: .3 }, edu: { 6: 1, 1: .2 }, law: { 3: 1, 2: .2 }, ag: { 5: 1, 7: .4 }, gov: { 3: .8, 7: .3 } };
  function vec(r) {
    var v = [0, 0, 0, 0, 0, 0, 0, 0], g = G[r.group], i;
    if (g) for (var k in g) v[k] = g[k]; else for (i = 0; i < 8; i++) v[i] = .2;
    var name = r.name.toLowerCase();
    KEYS.forEach(function (p) { if (p[1].test(name)) v[p[0]] = Math.min(1, v[p[0]] + .3); });
    if (r.kind === 'Diploma' || r.kind === 'Technical') v[7] = Math.min(1, v[7] + .4);
    return v;
  }
  function match(stage, stream, ans) {
    var taste = [0, 0, 0, 0, 0, 0, 0, 0], budget = 1e12, time = 99, goal = '';
    Q.forEach(function (q, i) {
      var op = q.o[ans[i]]; if (!op) return;
      if (q.k === 'taste') for (var k in op.w) taste[k] += op.w[k];
      else if (q.k === 'budget') budget = op.cap; else if (q.k === 'time') time = op.cap; else goal = op.tag;
    });
    var total = taste.reduce(function (a, b) { return a + b; }, 0);
    if (!total) return [];
    taste = taste.map(function (x) { return x / total; });
    var pool = PW.D.routes.filter(function (r) { return r.stage === stage && r.group !== 'school' && r.group !== 'abroad' && (stage !== 'after12' || PW.streamOk(r, stream)) && r.fee[0] <= budget && PW.yearsNum(r.years) <= time + .01; });
    var scored = pool.map(function (r) { var v = vec(r), s = 0; for (var k = 0; k < 8; k++) s += taste[k] * v[k]; return { r: r, s: s, v: v }; });
    var top = scored.reduce(function (m, x) { return Math.max(m, x.s); }, 0);
    if (top < .12) return [];
    return scored.filter(function (x) { return x.s >= top * .55 && x.s >= .1; }).map(function (x) {
      var r = x.r, cs = PW.careersOf(r), bonus = 0, yrs = PW.yearsNum(r.years);
      if (goal === 'early') bonus = Math.max(-1, Math.min(2, 4 - yrs)) * .012;
      else if (goal === 'stable') bonus = Math.max(-1, Math.min(2, 3 - PW.compet(r))) * .01 + PW.demand(r) * .008;
      else if (goal === 'abroad') bonus = (cs.length ? cs.reduce(function (a, c) { return a + c.abroad; }, 0) / cs.length : 0) * .015;
      else if (goal === 'serve') bonus = (x.v[1] + x.v[6] + x.v[3]) * .03;
      var reasons = [0, 1, 2, 3, 4, 5, 6, 7].filter(function (i) { return taste[i] * x.v[i] > .06; }).sort(function (a, b) { return taste[b] * x.v[b] - taste[a] * x.v[a]; }).slice(0, 2).map(function (i) { return DIMS[i]; });
      return { r: r, score: Math.max(40, Math.min(99, Math.floor(x.s / top * 90 + bonus * 100))), reasons: reasons };
    }).sort(function (a, b) { return b.score - a.score; }).slice(0, 6);
  }
  PW.match = match;

  var lab = { stage: '', stream: '', step: -1, ans: [] };
  PW.views.lab = function (stage) {
    if (stage && PW.stages.some(function (s) { return s.id === stage; }) && lab.stage !== stage) lab = { stage: stage, stream: '', step: -1, ans: [] };
    draw();
  };
  function draw() {
    view.textContent = '';
    var head = h('div', { class: 'pw-hero', 'data-t': 'p' }, [h('small', { class: 'pw-mono-l', text: 'COURSE LAB' }), h('h1', { text: 'Not sure yet? Let us match.' }), h('p', { text: 'Six quick questions. We only show courses that fit your level, budget and time, and say so when nothing does.' })]);
    var box = h('div', { class: 'pw-lab' });
    view.appendChild(head); view.appendChild(box);
    function again() { lab = { stage: '', stream: '', step: -1, ans: [] }; draw(); }
    if (!lab.stage) {
      box.appendChild(PW.sectionTitle('Where are you now?'));
      box.appendChild(h('div', { class: 'pw-opts' }, PW.stages.filter(function (s) { return s.id !== 'after8'; }).map(function (s) { var b = h('button', { class: 'pw-opt', type: 'button', text: PW.stageWord(s.label) }); b.addEventListener('click', function () { lab.stage = s.id; lab.step = s.id === 'after12' ? -1 : 0; draw(); }); return b; })));
      return;
    }
    if (lab.stage === 'after12' && !lab.stream) {
      box.appendChild(PW.sectionTitle('What did you study in +2?'));
      box.appendChild(h('div', { class: 'pw-opts' }, ['Science', 'Management', 'Humanities'].map(function (s) { var b = h('button', { class: 'pw-opt', type: 'button', text: s }); b.addEventListener('click', function () { lab.stream = s.toLowerCase(); lab.step = 0; draw(); }); return b; })));
      return;
    }
    if (lab.step < 0) lab.step = 0;
    if (lab.step < Q.length) {
      var q = Q[lab.step];
      box.appendChild(h('div', { class: 'pw-prog' }, [h('small', { class: 'pw-mono-l', text: 'QUESTION ' + (lab.step + 1) + ' OF ' + Q.length }), PW.bar(lab.step + 1, Q.length, 'b')]));
      box.appendChild(h('h2', { class: 'pw-q', text: q.t }));
      box.appendChild(h('div', { class: 'pw-opts' }, q.o.map(function (op, i) { var b = h('button', { class: 'pw-opt', type: 'button', 'aria-pressed': lab.ans[lab.step] === i, text: op.label }); b.addEventListener('click', function () { lab.ans[lab.step] = i; lab.step++; draw(); }); return b; })));
      var back = h('button', { class: 'pw-btn soft sm', type: 'button' }, [icon('arrow_back'), lab.step ? 'Back' : 'Start over']);
      back.addEventListener('click', function () { if (lab.step) { lab.step--; draw(); } else again(); });
      box.appendChild(back);
      return;
    }
    var hits = match(lab.stage, lab.stream, lab.ans);
    box.appendChild(PW.sectionTitle(hits.length ? 'Your best matches' : 'No clean match'));
    if (!hits.length) box.appendChild(PW.empty('Nothing at this level fits that budget and time together. Try a higher budget or more years.'));
    var rows = h('div', { class: 'pw-rows' });
    hits.forEach(function (x, i) {
      rows.appendChild(h('a', { class: 'pw-course', href: '#levels/' + x.r.stage + '/' + x.r.id }, [h('span', { class: 'pw-mono', 'data-t': PW.tone(i), text: PW.code(x.r.name) }), h('span', { class: 'pw-row-b' }, [h('b', { text: x.r.name }), h('small', { text: x.r.years + ' \u00b7 ' + PW.npr(x.r.fee) + (x.reasons.length ? ' \u00b7 ' + x.reasons.join(', ') : '') })]), h('span', { class: 'pw-dem' }, [h('small', { text: x.score + '%' }), PW.bar(x.score, 100, 'b')])]));
    });
    box.appendChild(rows);
    var redo = h('button', { class: 'pw-btn soft', type: 'button', text: 'Answer again' }); redo.addEventListener('click', function () { lab.step = 0; lab.ans = []; draw(); });
    var cmp = hits.length > 1 ? h('a', { class: 'pw-btn', href: '#compare/' + hits.slice(0, 3).map(function (x) { return x.r.id; }).join('+') }, ['Compare top ' + Math.min(3, hits.length)]) : null;
    box.appendChild(h('div', { class: 'pw-acts' }, [cmp, redo]));
  }

  /* ---- compare ---- */
  PW.views.compare = function (ids) {
    var list = (ids || '').split('+').map(function (x) { return PW.routes[x]; }).filter(Boolean).slice(0, 3);
    view.appendChild(PW.head('Compare courses', 'Up to three, side by side', list[0] ? '#levels/' + list[0].stage + '/' + list[0].id : '#levels'));
    var stage = list[0] ? list[0].stage : 'after12';
    var add = h('select', { class: 'pw-select', 'aria-label': 'Add a course' }, [h('option', { value: '', text: 'Add a course' })].concat(PW.D.routes.filter(function (r) { return r.stage === stage && list.indexOf(r) < 0 && r.group !== 'abroad'; }).map(function (r) { return h('option', { value: r.id, text: r.name }); })));
    add.addEventListener('change', function () { if (add.value && list.length < 3) location.hash = '#compare/' + list.map(function (r) { return r.id; }).concat(add.value).join('+'); });
    if (list.length < 3) view.appendChild(h('div', { class: 'pw-acts' }, [add]));
    var rows = [['Duration', function (r) { return r.years; }], ['Total cost', function (r) { return PW.npr(r.fee); }], ['Demand', function (r) { return PW.word(PW.demand(r), 'Steady'); }], ['Competition', function (r) { return PW.word(PW.compet(r), 'Low'); }], ['Start pay (NPR / month)', function (r) { var p = PW.pay(r); return p ? PW.money(p[0]) + ' to ' + PW.money(p[1]) : 'Varies'; }], ['Who can apply', function (r) { return r.entry; }], ['Careers', function (r) { return PW.careersOf(r).slice(0, 3).map(function (c) { return c.name; }).join(', ') || 'Opens at the next level'; }]];
    var table = h('div', { class: 'pw-cmp', 'data-n': list.length }, [h('div', { class: 'pw-cmp-h' }, [h('span')].concat(list.map(function (r, i) { return h('a', { class: 'pw-cmp-c', 'data-t': PW.tone(i), href: '#levels/' + r.stage + '/' + r.id, text: r.name }); })))]);
    rows.forEach(function (row) { table.appendChild(h('div', { class: 'pw-cmp-r' }, [h('b', { text: row[0] })].concat(list.map(function (r) { return h('span', { text: row[1](r) }); })))); });
    view.appendChild(list.length ? table : PW.empty('Open a course and press Compare to start.'));
  };

  /* ---- questions ---- */
  var fq = { topic: '' };
  PW.views.faq = function () {
    view.appendChild(PW.head('Questions', 'Plain answers for students and parents'));
    var f = h('div', { class: 'pw-filters' }), list = h('div', { class: 'pw-faq' });
    function fill() {
      f.textContent = '';
      var all = PW.chip('All', !fq.topic); all.addEventListener('click', function () { fq.topic = ''; fill(); }); f.appendChild(all);
      (PW.D.topics || []).forEach(function (t) { var c = PW.chip(t.label, fq.topic === t.id); c.addEventListener('click', function () { fq.topic = fq.topic === t.id ? '' : t.id; fill(); }); f.appendChild(c); });
      list.textContent = '';
      (PW.D.faq || []).filter(function (x) { return !fq.topic || x.topic === fq.topic; }).forEach(function (x) {
        var go = (x.go || []).map(function (id) { return PW.routes[id]; }).filter(Boolean);
        list.appendChild(h('details', { class: 'pw-q' }, [h('summary', {}, [h('span', { text: x.q }), icon('expand_more')]), h('div', { class: 'pw-q-b' }, [h('p', { text: x.a })].concat(go.length ? [h('div', { class: 'pw-tags' }, go.map(function (r) { return h('a', { class: 'pw-chip', href: '#levels/' + r.stage + '/' + r.id, text: r.name }); }))] : []))]));
      });
    }
    view.appendChild(f); view.appendChild(list); fill();
  };

  /* ---- saved ---- */
  PW.views.saved = function () {
    view.appendChild(PW.head('Saved', 'Courses, countries and jobs you kept on this device'));
    var rows = h('div', { class: 'pw-rows' }), n = 0;
    PW.saved.all().forEach(function (k) {
      var id = k.slice(2), x;
      if (k[0] === 'r' && (x = PW.routes[id])) rows.appendChild(h('a', { class: 'pw-course', href: '#levels/' + x.stage + '/' + x.id }, [h('span', { class: 'pw-mono', 'data-t': PW.tone(n), text: PW.code(x.name) }), h('span', { class: 'pw-row-b' }, [h('b', { text: x.name }), h('small', { text: x.years + ' \u00b7 ' + x.kind })]), icon('chevron_right')]));
      else if (k[0] === 'a' && (x = PW.abroadBy[id])) rows.appendChild(h('a', { class: 'pw-course', href: '#abroad/' + id }, [h('span', { class: 'pw-mono', 'data-t': PW.tone(n), text: x.country.slice(0, 2).toUpperCase() }), h('span', { class: 'pw-row-b' }, [h('b', { text: x.country }), h('small', { text: 'Study abroad' })]), icon('chevron_right')]));
      else if (k[0] === 'g' && (x = PW.govtBy[id])) rows.appendChild(h('a', { class: 'pw-course', href: '#govt/' + id }, [h('span', { class: 'pw-mono', 'data-t': PW.tone(n), text: PW.code(x.name).slice(0, 3) }), h('span', { class: 'pw-row-b' }, [h('b', { text: x.name }), h('small', { text: x.level })]), icon('chevron_right')]));
      else return;
      n++;
    });
    view.appendChild(n ? rows : PW.empty('Nothing saved yet. Use the bookmark on a course, country or job.'));
  };

  PW.ready = true;
  PW.tryStart();
})();
