/* Pathways: Colleges (map + list), Abroad (countries, scholarships), Lok Sewa. */
(function () {
  'use strict';
  var PW = window.PW, h = PW.h, icon = PW.icon, view = PW.view;
  var cst = { q: '', sector: '' }, ss = { scope: '', level: '' }, gt = { track: '' };

  /* ---- colleges ---- */
  PW.views.colleges = function (routeId) {
    var r = routeId && PW.routes[routeId] ? PW.routes[routeId] : null;
    var pool = r ? r.where.map(function (id) { return PW.providers[id]; }).filter(Boolean) : PW.D.providers;
    var caption = h('div', { class: 'pw-mapcap' }), mapBox = h('div', { class: 'pw-mapbox' }), list = h('div', { class: 'pw-rows' });
    var qIn = h('input', { class: 'pw-input', type: 'search', placeholder: 'Search district, city or college', 'aria-label': 'Search colleges', value: cst.q });
    var sel = PW.districtPicker(function () { fill(); });
    var sectors = h('div', { class: 'pw-filters' }, [['', 'All'], ['Public', 'Public'], ['Private', 'Private'], ['Community', 'Community']].map(function (s) {
      var c = PW.chip(s[1], cst.sector === s[0]);
      c.addEventListener('click', function () { cst.sector = s[0]; Array.prototype.forEach.call(sectors.children, function (x) { x.setAttribute('aria-pressed', x === c); }); fill(); });
      return c;
    }));
    function match(p) {
      var q = cst.q.trim().toLowerCase();
      return (!cst.sector || p.sector === cst.sector) && (!q || q.split(/\s+/).every(function (w) { return (p.name + ' ' + p.district + ' ' + p.place).toLowerCase().indexOf(w) >= 0; }));
    }
    function fill() {
      var d = PW.state.district, base = pool.filter(match), counts = {};
      base.forEach(function (p) { counts[p.district] = (counts[p.district] || 0) + 1; });
      var shown = base.filter(function (p) { return !d || p.district === d; });
      shown.sort(function (a, b) { return (a.sector === 'Public' ? 0 : 1) - (b.sector === 'Public' ? 0 : 1) || a.name.localeCompare(b.name); });
      mapBox.textContent = ''; mapBox.appendChild(PW.map(counts, d, function (x) { PW.setDistrict(x); sel.value = x; fill(); }));
      caption.textContent = '';
      caption.appendChild(h('span', { class: 'pw-pill' }, [icon('location_on'), shown.length + (shown.length === 1 ? ' college' : ' colleges') + (d ? ' in ' + d : ' across Nepal')]));
      list.textContent = '';
      shown.slice(0, 60).forEach(function (p, i) { list.appendChild(PW.providerRow(p, i)); });
      if (shown.length > 60) list.appendChild(PW.empty('Showing 60. Pick a district or search to narrow it down.'));
      if (!shown.length) {
        list.appendChild(PW.empty(d ? 'No listed ' + (r ? 'provider of this course' : 'college') + ' in ' + d + ' yet.' : 'Nothing matches that search.'));
        if (d) fetch('/api/institutions/?limit=6&district=' + encodeURIComponent(d)).then(function (x) { return x.json(); }).then(function (j) {
          if ((j.items || []).length) list.appendChild(h('p', { class: 'pw-cap', text: 'Institutions listed in ' + d }));
          (j.items || []).forEach(function (it, i) { list.appendChild(h('a', { class: 'pw-row', href: '/app/schools/' + it.slug + '/' }, [h('span', { class: 'pw-mono', 'data-t': PW.tone(i), text: it.name.charAt(0).toUpperCase() }), h('span', { class: 'pw-row-b' }, [h('b', { text: it.name }), h('small', { text: it.location || it.district })])])); });
        }).catch(function () {});
      }
    }
    qIn.addEventListener('input', function () { cst.q = qIn.value; fill(); });
    view.appendChild(PW.head('Where to study', r ? r.name : 'Colleges and institutions', r ? '#levels/' + r.stage + '/' + r.id : null));
    if (r) view.appendChild(h('p', { class: 'pw-blurb', text: 'Course fee range: ' + PW.npr(r.fee) + ' in total, public and private seats together.' }));
    view.appendChild(h('div', { class: 'pw-split cols' }, [
      h('div', { class: 'pw-colA' }, [h('div', { class: 'pw-bar2' }, [h('div', { class: 'pw-search2' }, [icon('search'), qIn]), sel]), sectors, h('div', { class: 'pw-mapwrap' }, [mapBox, caption])]),
      h('div', { class: 'pw-colB' }, [PW.sectionTitle(r ? 'Colleges offering ' + PW.code(r.name) : 'Colleges'), list]),
    ]));
    fill();
  };

  /* ---- abroad ---- */
  function schRow(s, i) {
    return h('details', { class: 'pw-career', id: 'sch-' + s.id }, [
      h('summary', {}, [h('span', { class: 'pw-mono', 'data-t': PW.tone(i), text: s.name.replace(/[^A-Za-z]/g, '').slice(0, 2).toUpperCase() }), h('span', { class: 'pw-row-b' }, [h('b', { text: s.name }), h('small', { text: s.by })]), h('span', { class: 'pw-tag', text: s.scope === 'nepal' ? 'Nepal' : 'Abroad' }), icon('expand_more')]),
      h('div', { class: 'pw-career-b' }, [kv('Covers', s.covers), kv('Who', s.who), kv('How', s.how), s.link ? h('a', { class: 'pw-btn soft sm', href: s.link, target: '_blank', rel: 'noopener nofollow' }, ['Official site', icon('open_in_new')]) : null,
        h('p', { class: 'pw-cap', text: 'Levels: ' + s.levels.join(', ') + '. Deadlines change every year, read the official notice.' })]),
    ]);
  }
  function kv(k, v) { return h('p', { class: 'pw-kvp' }, [h('b', { text: k + ': ' }), v]); }
  function country(id) {
    var a = PW.abroadBy[id];
    if (!a) return PW.views.abroad();
    var sch = (a.scholarships || []).map(function (x) { return PW.schol[x]; }).filter(Boolean);
    var lo = a.tuition[0] + a.living[0], hi = a.tuition[1] + a.living[1];
    view.appendChild(PW.head(a.country, 'Costs, tests and visas, per year in NPR', '#abroad'));
    view.appendChild(h('div', { class: 'pw-hero', 'data-t': 'p' }, [h('small', { class: 'pw-mono-l', text: 'INTAKES \u00b7 ' + a.intakes.toUpperCase() }), h('h1', { text: 'NPR ' + PW.money(lo) + ' to ' + PW.money(hi) }), h('p', { text: 'Tuition plus living for one year. ' + a.note }), h('div', { class: 'pw-acts' }, [PW.saveBtn('a:' + a.id, a.country)])]));
    view.appendChild(h('div', { class: 'pw-tiles' }, [
      h('div', { class: 'pw-tile', 'data-t': 'b' }, [h('small', { class: 'pw-mono-l', text: 'TUITION / YEAR' }), h('b', { text: a.tuition[1] === 0 ? 'Free' : PW.money(a.tuition[0]) + ' to ' + PW.money(a.tuition[1]) })]),
      h('div', { class: 'pw-tile', 'data-t': 'y' }, [h('small', { class: 'pw-mono-l', text: 'LIVING / YEAR' }), h('b', { text: PW.money(a.living[0]) + ' to ' + PW.money(a.living[1]) })]),
      h('div', { class: 'pw-tile', 'data-t': 'l' }, [h('small', { class: 'pw-mono-l', text: 'TESTS' }), h('b', { text: a.exams.join(', ') })]),
    ]));
    view.appendChild(h('div', { class: 'pw-block' }, [PW.sectionTitle('Popular fields'), h('div', { class: 'pw-tags' }, a.fields.map(function (f) { return h('span', { class: 'pw-tag', 'data-t': 'b', text: f }); }))]));
    view.appendChild(h('div', { class: 'pw-block' }, [PW.sectionTitle('Work rules'), PW.empty(a.work + '.')]));
    if (sch.length) view.appendChild(h('div', { class: 'pw-block' }, [PW.sectionTitle('Scholarships for this country')].concat(sch.map(schRow))));
  }
  PW.views.abroad = function (id) {
    if (id) return country(id);
    view.appendChild(h('div', { class: 'pw-hero', 'data-t': 'p' }, [h('small', { class: 'pw-mono-l', text: 'BEYOND NEPAL' }), h('h1', { text: 'Study abroad, step by step.' }), h('p', { text: 'Countries, yearly costs, tests, work rules and scholarships in one place.' })]));
    view.appendChild(PW.sectionTitle('Destinations (' + PW.D.abroad.length + ')'));
    var max = 11000000, grid = h('div', { class: 'pw-grid' });
    PW.D.abroad.forEach(function (a, i) {
      grid.appendChild(h('a', { class: 'pw-dest', 'data-t': PW.tone(i), href: '#abroad/' + a.id, i: Math.min(i, 12) }, [
        h('span', { class: 'pw-mono' }, [a.country.slice(0, 2).toUpperCase()]), h('b', { text: a.country }),
        h('small', { text: a.intakes }), PW.bar(a.tuition[1] + a.living[1], max * 1.2, 'b'),
        h('small', { text: 'NPR ' + PW.money(a.tuition[0] + a.living[0]) + ' to ' + PW.money(a.tuition[1] + a.living[1]) + ' / yr' }),
      ]));
    });
    view.appendChild(grid);
    var f = h('div', { class: 'pw-filters' }), list = h('div', { class: 'pw-rows' });
    function fill() {
      f.textContent = '';
      [['', 'All'], ['abroad', 'Abroad'], ['nepal', 'In Nepal']].forEach(function (s) { var c = PW.chip(s[1], ss.scope === s[0]); c.addEventListener('click', function () { ss.scope = s[0]; fill(); }); f.appendChild(c); });
      ['bachelor', 'master', 'phd', 'diploma'].forEach(function (l) { var c = PW.chip(l.charAt(0).toUpperCase() + l.slice(1), ss.level === l); c.addEventListener('click', function () { ss.level = ss.level === l ? '' : l; fill(); }); f.appendChild(c); });
      list.textContent = '';
      var n = 0;
      PW.D.scholarships.filter(function (s) { return (!ss.scope || s.scope === ss.scope) && (!ss.level || s.levels.indexOf(ss.level) >= 0); }).forEach(function (s) { list.appendChild(schRow(s, n++)); });
      if (!n) list.appendChild(PW.empty('No scholarship matches that filter.'));
    }
    view.appendChild(h('div', { class: 'pw-block' }, [PW.sectionTitle('Scholarships'), f, list]));
    fill();
  };

  /* ---- Lok Sewa ---- */
  function govtPage(g) {
    var tr = (PW.D.govt_tracks || []).filter(function (t) { return t.id === g.track; })[0];
    view.appendChild(PW.head(g.name, g.level, '#govt'));
    view.appendChild(h('div', { class: 'pw-hero', 'data-t': 'l' }, [h('small', { class: 'pw-mono-l', text: (tr ? tr.label : 'Government').toUpperCase() + ' \u00b7 ' + g.body.toUpperCase() }), h('h1', { text: g.name }), h('p', { text: g.note || '' }), h('div', { class: 'pw-acts' }, [PW.saveBtn('g:' + g.id, g.name)])]));
    view.appendChild(h('div', { class: 'pw-tiles two' }, [
      h('div', { class: 'pw-tile', 'data-t': 'b' }, [h('small', { class: 'pw-mono-l', text: 'QUALIFICATION' }), h('b', { class: 'sm', text: g.need })]),
      h('div', { class: 'pw-tile', 'data-t': 'y' }, [h('small', { class: 'pw-mono-l', text: 'AGE' }), h('b', { class: 'sm', text: g.age })]),
    ]));
    view.appendChild(h('div', { class: 'pw-block' }, [PW.sectionTitle('Stages')].concat(g.stages.map(function (s, i) { return h('div', { class: 'pw-row' }, [h('span', { class: 'pw-mono', 'data-t': PW.tone(i), text: ('0' + (i + 1)).slice(-2) }), h('span', { class: 'pw-row-b' }, [h('b', { text: s[0] }), h('small', { text: s[1] })])]); }))));
    view.appendChild(h('div', { class: 'pw-block' }, [PW.sectionTitle('Subjects'), h('div', { class: 'pw-tags' }, g.subjects.map(function (s) { return h('span', { class: 'pw-tag', text: s }); }))]));
    view.appendChild(h('div', { class: 'pw-block' }, [PW.sectionTitle('How to prepare')].concat(g.prep.map(function (s, i) { return h('div', { class: 'pw-row' }, [h('span', { class: 'pw-mono', 'data-t': PW.tone(i + 1), text: ('0' + (i + 1)).slice(-2) }), h('span', { class: 'pw-row-b' }, [h('b', { text: s })])]); }))));
    view.appendChild(PW.empty('Syllabus, vacancies and dates change. Always read the official notice of the commission.'));
  }
  PW.views.govt = function (id) {
    if (id && PW.govtBy[id]) return govtPage(PW.govtBy[id]);
    view.appendChild(h('div', { class: 'pw-hero', 'data-t': 'l' }, [h('small', { class: 'pw-mono-l', text: 'GOVT JOBS AND EXAMS' }), h('h1', { text: 'Lok Sewa, step by step.' }), h('p', { text: 'Qualification, age, exam stages, subjects and a prep path for each service.' })]));
    var f = h('div', { class: 'pw-filters' }), list = h('div', { class: 'pw-rows' });
    function fill() {
      f.textContent = '';
      var all = PW.chip('All', !gt.track); all.addEventListener('click', function () { gt.track = ''; fill(); }); f.appendChild(all);
      (PW.D.govt_tracks || []).forEach(function (t) { var c = PW.chip(t.label, gt.track === t.id); c.addEventListener('click', function () { gt.track = gt.track === t.id ? '' : t.id; fill(); }); f.appendChild(c); });
      list.textContent = '';
      PW.D.govt.filter(function (g) { return !gt.track || g.track === gt.track; }).forEach(function (g, i) {
        list.appendChild(h('a', { class: 'pw-course', href: '#govt/' + g.id }, [h('span', { class: 'pw-mono', 'data-t': PW.tone(i), text: PW.code(g.name).slice(0, 3) }), h('span', { class: 'pw-row-b' }, [h('b', { text: g.name }), h('small', { text: g.level + ' \u00b7 ' + g.body })]), icon('chevron_right')]));
      });
    }
    view.appendChild(f); view.appendChild(list); fill();
  };
})();
