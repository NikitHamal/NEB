/* Pathways: the levels view (course list + course page) and the shared "where to study" pieces. */
(function () {
  'use strict';
  var PW = window.PW, h = PW.h, icon = PW.icon, view = PW.view;
  var STREAMS = [['', 'All'], ['science', 'Science'], ['management', 'Management'], ['humanities', 'Humanities']];
  var fstate = { stream: '', group: '', tab: 'careers' };
  var DISTRICT_KIND = function (r) { return /Diploma|Technical/.test(r.kind) ? 'institute' : (r.stage === 'afterbach' ? 'university' : 'college'); };

  // mirrors streamOk in PwMatch.kt: a Science-only route never reaches a Management student
  PW.streamOk = function (r, stream) {
    var e = r.entry.toLowerCase();
    if (e.indexOf('+2') < 0 && e.indexOf('any') < 0) return false;
    if (e.indexOf('any stream') >= 0) return true;
    var needs = [];
    if (e.indexOf('science') >= 0) needs.push('science');
    if (e.indexOf('management') >= 0 || e.indexOf('commerce') >= 0) needs.push('management');
    if (e.indexOf('humanities') >= 0) needs.push('humanities');
    return !needs.length || needs.indexOf(stream) >= 0;
  };

  /* ---- colleges for a course, shared with the Colleges section ---- */
  PW.providerRow = function (p, i) {
    var tag = p.website ? 'a' : 'div';
    return h(tag, { class: 'pw-row', href: p.website || null, target: p.website ? '_blank' : null, rel: p.website ? 'noopener nofollow' : null }, [
      h('span', { class: 'pw-mono', 'data-t': PW.tone(i || 0), text: p.name.replace(/[^A-Za-z]/g, '').charAt(0).toUpperCase() }),
      h('span', { class: 'pw-row-b' }, [h('b', { text: p.name }), h('small', { text: p.place + ', ' + p.district + ' \u00b7 ' + p.sector + ' \u00b7 ' + p.kind }), p.note ? h('small', { class: 'pw-note', text: p.note }) : null]),
      p.website ? icon('open_in_new') : null,
    ]);
  };
  PW.districtPicker = function (onChange) {
    var sel = h('select', { class: 'pw-select', 'aria-label': 'District' }, [h('option', { value: '', text: 'All districts' })].concat(PW.districts.map(function (x) { return h('option', { value: x, text: x }); })));
    sel.value = PW.state.district;
    sel.addEventListener('change', function () { PW.setDistrict(sel.value); onChange(sel.value); });
    return sel;
  };
  PW.drawPlaces = function (r, box) {
    var d = PW.state.district;
    box.textContent = '';
    var cur = r.where.map(function (id) { return PW.providers[id]; }).filter(function (p) { return p && (!d || p.district === d); });
    cur.sort(function (a, b) { return (a.sector === 'Public' ? 0 : 1) - (b.sector === 'Public' ? 0 : 1); });
    cur.forEach(function (p, i) { box.appendChild(PW.providerRow(p, i)); });
    if (!cur.length) box.appendChild(PW.empty(d ? 'No listed college for this course in ' + d + ' yet.' : 'Pick a district to narrow the list.'));
    if (d) {
      var kind = DISTRICT_KIND(r), live = h('div', { class: 'pw-live' });
      box.appendChild(live);
      fetch('/api/institutions/?limit=5&kind=' + kind + '&district=' + encodeURIComponent(d)).then(function (x) { return x.json(); }).then(function (j) {
        if (!(j.items || []).length) return;
        live.appendChild(h('p', { class: 'pw-cap', text: 'Other ' + kind + 's in ' + d }));
        j.items.forEach(function (it, i) { live.appendChild(h('a', { class: 'pw-row', href: '/app/schools/' + it.slug + '/' }, [h('span', { class: 'pw-mono', 'data-t': PW.tone(i + 1), text: it.name.charAt(0).toUpperCase() }), h('span', { class: 'pw-row-b' }, [h('b', { text: it.name }), h('small', { text: it.location || it.district })])])); });
      }).catch(function () {});
    }
  };

  /* ---- course page ---- */
  function tile(label, word, bar, tone, sub) {
    return h('div', { class: 'pw-tile', 'data-t': tone }, [h('small', { class: 'pw-mono-l', text: label }), h('b', { text: word }), bar || null, sub ? h('small', { text: sub }) : null]);
  }
  function careerRow(c, i) {
    var e = c.salary.entry, s = c.salary.senior, max = 600000;
    var pay = h('span', { class: 'pw-bar range', 'data-t': 'y' }, [h('i')]);
    pay.firstChild.style.setProperty('--l', (e[0] / max * 100) + '%'); pay.firstChild.style.setProperty('--w', Math.max(4, (s[1] - e[0]) / max * 100) + '%');
    function m(label, v, tone) { return h('div', { class: 'pw-meter' }, [h('span', { text: label }), PW.bar(v, 5, tone), h('output', { text: v + ' of 5' })]); }
    return h('details', { class: 'pw-career' }, [
      h('summary', {}, [h('span', { class: 'pw-mono', 'data-t': PW.tone(i), text: ('0' + (i + 1)).slice(-2) }), h('span', { class: 'pw-row-b' }, [h('b', { text: c.name }), h('small', { text: c.about })]), icon('expand_more')]),
      h('div', { class: 'pw-career-b' }, [
        m('Demand', c.demand, 'b'), m('Competition', c.competition, 'p'), m('Abroad demand', c.abroad, 'b'),
        h('div', { class: 'pw-meter' }, [h('span', { text: 'Monthly pay' }), pay, h('output', { text: PW.money(e[0]) + ' to ' + PW.money(s[1]) })]),
        h('div', { class: 'pw-tags' }, [h('span', { class: 'pw-tag', text: 'Trend: ' + c.trend })].concat(c.skills.slice(0, 4).map(function (x) { return h('span', { class: 'pw-tag', text: x }); }))),
      ]),
    ]);
  }
  function tabBody(r, box) {
    box.textContent = '';
    var cs = PW.careersOf(r);
    if (fstate.tab === 'careers') {
      if (!cs.length) box.appendChild(PW.empty('This is a stepping stone. The careers open up at the next level below.'));
      cs.forEach(function (c, i) { box.appendChild(careerRow(c, i)); });
    } else if (fstate.tab === 'skills') {
      var all = r.skills.slice();
      cs.forEach(function (c) { c.skills.forEach(function (s) { if (all.indexOf(s) < 0) all.push(s); }); });
      box.appendChild(h('p', { class: 'pw-cap', text: 'You build these in the course' }));
      box.appendChild(h('div', { class: 'pw-tags' }, r.skills.map(function (s) { return h('span', { class: 'pw-tag', 'data-t': 'b', text: s }); })));
      var more = all.filter(function (s) { return r.skills.indexOf(s) < 0; });
      if (more.length) { box.appendChild(h('p', { class: 'pw-cap', text: 'Employers also ask for' })); box.appendChild(h('div', { class: 'pw-tags' }, more.map(function (s) { return h('span', { class: 'pw-tag', text: s }); }))); }
    } else if (fstate.tab === 'cost') {
      var yrs = PW.yearsNum(r.years), per = r.fee[1] ? Math.round(r.fee[1] / yrs / 1000) * 1000 : 0;
      box.appendChild(h('div', { class: 'pw-tiles two' }, [tile('TOTAL COST', PW.npr(r.fee), null, 'y', r.years), tile('PER YEAR AT THE TOP', per ? 'NPR ' + PW.money(per) : 'Free', null, 'l', 'Public seats cost far less than private ones')]));
      box.appendChild(PW.empty('Ranges cover public and private seats, fees only. Add hostel, books and travel. Confirm with the college.'));
    } else {
      box.appendChild(h('div', { class: 'pw-kv' }, [h('b', { text: 'Who can apply' }), h('p', { text: r.entry }), h('b', { text: 'Entrance or exam' }), h('p', { text: r.exam })]));
    }
  }
  function detail(r) {
    var stage = PW.stages.filter(function (s) { return s.id === r.stage; })[0];
    var dem = PW.demand(r), com = PW.compet(r), pay = PW.pay(r);
    var places = h('div', { class: 'pw-places' }), body = h('div', { class: 'pw-tabbody' });
    var tabs = h('div', { class: 'pw-seg', role: 'tablist' }, [['careers', 'Careers'], ['skills', 'Skills'], ['cost', 'Cost'], ['entry', 'Entry']].map(function (t) {
      var b = h('button', { class: 'pw-segb', type: 'button', role: 'tab', 'aria-selected': fstate.tab === t[0], text: t[1] });
      b.addEventListener('click', function () { fstate.tab = t[0]; Array.prototype.forEach.call(tabs.children, function (x) { x.setAttribute('aria-selected', x === b); }); tabBody(r, body); });
      return b;
    }));
    tabBody(r, body); PW.drawPlaces(r, places);
    var next = r.next.map(function (n) { return PW.routes[n]; }).filter(Boolean);
    var also = PW.D.routes.filter(function (x) { return x.stage === r.stage && x.group === r.group && x.id !== r.id; }).slice(0, 6);
    function chips(list) { return h('div', { class: 'pw-tags' }, list.map(function (x) { return h('a', { class: 'pw-chip', href: '#levels/' + x.stage + '/' + x.id, text: x.name.length > 34 ? x.name.slice(0, 32) + '...' : x.name }); })); }
    return h('article', { class: 'pw-detail-in' }, [
      h('div', { class: 'pw-hero', 'data-t': 'b' }, [
        h('small', { class: 'pw-mono-l', text: (stage ? stage.label : '').toUpperCase() + ' \u00b7 ' + r.kind.toUpperCase() }),
        h('h1', { text: r.name }), h('p', { text: r.about }),
        h('div', { class: 'pw-tags' }, [h('span', { class: 'pw-pill' }, [icon('schedule'), r.years]), h('span', { class: 'pw-pill' }, [icon('payments'), PW.npr(r.fee)])]),
        h('div', { class: 'pw-acts' }, [
          h('a', { class: 'pw-btn', href: '#colleges/' + r.id }, [icon('location_on'), 'Find colleges']),
          h('a', { class: 'pw-btn soft', href: '#compare/' + r.id }, ['Compare']), PW.saveBtn('r:' + r.id, r.name),
        ]),
      ]),
      h('div', { class: 'pw-tiles' }, [
        tile('DEMAND', PW.word(dem, 'Steady'), PW.bar(dem, 5, 'b'), 'b'), tile('COMPETITION', PW.word(com, 'Low'), PW.bar(com, 5, 'p'), 'p'),
        tile('START PAY', pay ? PW.money(pay[0]) + ' to ' + PW.money(pay[1]) : 'Varies', null, 'y', 'NPR per month'),
      ]),
      tabs, body,
      next.length ? h('div', { class: 'pw-block' }, [PW.sectionTitle('What comes next'), chips(next)]) : null,
      also.length ? h('div', { class: 'pw-block' }, [PW.sectionTitle('People also explore'), chips(also)]) : null,
      h('div', { class: 'pw-block' }, [PW.sectionTitle('Where to study', PW.districtPicker(function () { PW.drawPlaces(r, places); })), places]),
    ]);
  }

  /* ---- levels view ---- */
  PW.views.levels = function (stageId, routeId) {
    var stages = PW.stages;
    var st = stages.filter(function (s) { return s.id === stageId; })[0];
    if (!st && routeId && PW.routes[routeId]) st = stages.filter(function (s) { return s.id === PW.routes[routeId].stage; })[0];
    if (!st) { st = stages.filter(function (s) { return s.id === 'after12'; })[0] || stages[0]; }
    var list = PW.D.routes.filter(function (r) { return r.stage === st.id && r.group !== 'abroad' && (st.id !== 'after12' || !fstate.stream || PW.streamOk(r, fstate.stream)); });
    var groups = []; PW.D.routes.forEach(function (r) { if (r.stage === st.id && groups.indexOf(r.group) < 0) groups.push(r.group); });
    if (st.id !== 'after12' && fstate.group) list = list.filter(function (r) { return r.group === fstate.group; });
    var wide = window.matchMedia('(min-width:900px)').matches;
    var cur = routeId && PW.routes[routeId] ? PW.routes[routeId] : (wide ? list[0] : null);

    var levelTabs = h('div', { class: 'pw-levels', role: 'tablist' }, stages.map(function (s) { return h('a', { class: 'pw-level', href: '#levels/' + s.id, role: 'tab', 'aria-selected': s.id === st.id }, [PW.stageWord(s.label)]); }));
    var filters = h('div', { class: 'pw-filters' });
    if (st.id === 'after12') STREAMS.forEach(function (s) { var c = PW.chip(s[1], fstate.stream === s[0]); c.addEventListener('click', function () { fstate.stream = s[0]; PW.route(); }); filters.appendChild(c); });
    else if (groups.length > 1) { var all = PW.chip('All', !fstate.group); all.addEventListener('click', function () { fstate.group = ''; PW.route(); }); filters.appendChild(all); groups.forEach(function (g) { var c = PW.chip(PW.GROUPS[g] || g, fstate.group === g); c.addEventListener('click', function () { fstate.group = fstate.group === g ? '' : g; PW.route(); }); filters.appendChild(c); }); }

    var rows = h('div', { class: 'pw-rows' });
    list.forEach(function (r, i) {
      var dem = PW.demand(r);
      rows.appendChild(h('a', { class: 'pw-course', href: '#levels/' + st.id + '/' + r.id, 'aria-current': cur && cur.id === r.id ? 'true' : null, i: Math.min(i, 12) }, [
        h('span', { class: 'pw-mono', 'data-t': PW.tone(i), text: PW.code(r.name) }),
        h('span', { class: 'pw-row-b' }, [h('b', { text: r.name }), h('small', { text: r.years + ' \u00b7 ' + (PW.GROUPS[r.group] || r.kind) })]),
        h('span', { class: 'pw-dem' }, [h('small', { text: dem ? PW.word(dem, 'Steady') : r.kind }), dem ? PW.bar(dem, 5, 'b') : null]),
      ]));
    });
    if (!list.length) rows.appendChild(PW.empty('No course matches that filter.'));
    var match = h('div', { class: 'pw-match', 'data-t': 'p' }, [h('div', {}, [h('b', { text: 'Not sure yet?' }), h('p', { text: 'Six quick questions, then we match courses to your strengths.' })]), h('a', { class: 'pw-btn dark', href: '#lab/' + st.id, text: 'Start match' })]);
    var left = h('aside', { class: 'pw-list' }, [PW.sectionTitle('Courses ' + PW.stageWord(st.label).toLowerCase() + (list.length ? ' (' + list.length + ')' : '')), filters, rows, match]);
    var right = h('section', { class: 'pw-detail' }, [cur ? h('a', { class: 'pw-back', href: '#levels/' + st.id }, [icon('arrow_back'), 'All courses']) : null, cur ? detail(cur) : PW.empty('Pick a course to see careers, pay and colleges.')]);
    view.appendChild(levelTabs);
    view.appendChild(h('p', { class: 'pw-blurb', text: st.blurb + ' ' + st.tip }));
    view.appendChild(h('div', { class: 'pw-split', 'data-mode': routeId ? 'detail' : 'list' }, [left, right]));
    var l = view.querySelector('.pw-list'); if (l) l.scrollTop = PW.keepScroll || 0;
  };
})();
