/* Pathways: one dataset (json_script), hash routes, a detail sheet. No framework, events are delegated. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var D, routes, careers, providers, scholarships;
  var DISTRICTS = JSON.parse($('pw-districts').textContent);
  var by = function (list) { var m = {}; list.forEach(function (x) { m[x.id] = x; }); return m; };
  var tabsEl = $('pw-tabs'), view = $('pw-view'), sheet = $('pw-sheet'), scrim = $('pw-scrim'), sheetBody = $('pw-sheet-body');
  var TABS = [];
  var GROUPS = { school: 'School', tech: 'Engineering and IT', sci: 'Science', health: 'Health', biz: 'Business', arts: 'Arts and media', edu: 'Education', law: 'Law', ag: 'Agriculture', gov: 'Government', abroad: 'Abroad' };
  var state = { tab: 'after10', group: '', topic: '', scope: '', level: '', district: localStorage.getItem('pw-district') || '', open: '' };

  function h(tag, attrs, kids) {
    var el = document.createElement(tag);
    for (var k in (attrs || {})) {
      var v = attrs[k];
      if (v == null || v === false) continue;
      if (k === 'text') el.textContent = v; else if (k === 'class') el.className = v;
      else if (k === 'i') el.style.setProperty('--i', v); else if (k === 'w') el.style.setProperty('width', v);
      else el.setAttribute(k, v === true ? '' : v);
    }
    (kids || []).forEach(function (c) { if (c != null && c !== false) el.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return el;
  }
  function icon(name) { return h('span', { class: 'material-symbols-outlined', 'aria-hidden': 'true', text: name }); }
  function money(n) {
    if (n >= 10000000) return trim(n / 10000000) + ' crore';
    if (n >= 100000) return trim(n / 100000) + ' lakh';
    if (n >= 1000) return trim(n / 1000) + 'k';
    return String(n);
  }
  function trim(x) { return (Math.round(x * 10) / 10).toString().replace(/\.0$/, ''); }
  function range(r) { return r[1] === 0 ? 'Free' : (r[0] === 0 ? 'Free to ' : money(r[0]) + ' to ') + 'NPR ' + money(r[1]); }
  function npr(r) { return r[1] === 0 ? 'Free' : 'NPR ' + money(r[0]) + ' to ' + money(r[1]); }
  var TONE = { primary: 'primary', secondary: 'secondary', tertiary: 'tertiary' };
  function dots(n) { return n + ' of 5'; }

  /* ---- tabs ---- */
  function drawTabs() {
    tabsEl.textContent = '';
    TABS.forEach(function (t) {
      tabsEl.appendChild(h('button', { class: 'pw-tab', type: 'button', role: 'tab', 'data-tab': t.id, 'aria-selected': state.tab === t.id }, [icon(t.icon), t.label]));
    });
    var on = tabsEl.querySelector('[aria-selected="true"]');
    if (on && on.scrollIntoView) on.scrollIntoView({ inline: 'center', block: 'nearest' });
  }

  /* ---- stage view ---- */
  function routeCard(r, i) {
    var c = h('button', { class: 'pw-card', type: 'button', 'data-route': r.id, i: Math.min(i, 14) }, [
      h('div', { class: 'pw-card-top' }, [h('span', { class: 'pw-tag', text: r.kind }), h('span', { class: 'pw-tag', 'data-t': 'tertiary', text: GROUPS[r.group] || '' })]),
      h('h3', { text: r.name }),
      h('div', { class: 'pw-facts' }, [h('span', {}, [icon('schedule'), r.years]), h('span', {}, [icon('payments'), range(r.fee)])]),
      h('p', { text: r.about }),
    ]);
    return c;
  }
  function drawStage() {
    var stage = D.stages.filter(function (s) { return s.id === state.tab; })[0];
    var list = D.routes.filter(function (r) { return r.stage === stage.id; });
    var groups = [];
    list.forEach(function (r) { if (groups.indexOf(r.group) < 0) groups.push(r.group); });
    var f = h('div', { class: 'pw-filters', role: 'group', 'aria-label': 'Field' }, [chip('', 'All', !state.group, 'group')]);
    if (groups.length > 1) groups.forEach(function (g) { f.appendChild(chip(g, GROUPS[g] || g, state.group === g, 'group')); });
    var grid = h('div', { class: 'pw-grid' });
    list.filter(function (r) { return !state.group || r.group === state.group; }).forEach(function (r, i) { grid.appendChild(routeCard(r, i)); });
    view.textContent = '';
    view.appendChild(h('div', { class: 'pw-intro' }, [h('h2', { text: stage.label }), h('p', { text: stage.blurb }), h('p', { text: stage.tip })]));
    if (groups.length > 1) view.appendChild(f);
    view.appendChild(grid);
  }
  function chip(value, label, on, kind) {
    return h('button', { class: 'pw-chip', type: 'button', 'data-chip': kind, 'data-value': value, 'aria-pressed': on }, [label]);
  }

  /* ---- abroad ---- */
  function costBar(r, max, tone) {
    var left = (r[0] / max * 100), w = Math.max(3, (r[1] - r[0]) / max * 100);
    var fill = h('span', { class: 'pw-fill', 'data-t': tone });
    fill.style.left = left + '%'; fill.style.width = w + '%';
    return h('div', { class: 'pw-track' }, [fill]);
  }
  function drawAbroad() {
    var max = 11000000, grid = h('div', { class: 'pw-grid' });
    D.abroad.forEach(function (a, i) {
      var sch = (a.scholarships || []).map(function (id) { return scholarships[id]; }).filter(Boolean);
      grid.appendChild(h('article', { class: 'pw-card', i: Math.min(i, 14) }, [
        h('div', { class: 'pw-card-top' }, [h('h3', { text: a.country }), h('span', { class: 'pw-tag', 'data-t': 'primary', text: a.intakes })]),
        h('div', { class: 'pw-sec' }, [
          h('div', { class: 'pw-meter' }, [h('span', { text: 'Tuition / yr' }), costBar(a.tuition, max, 'primary'), h('output', { text: a.tuition[1] === 0 ? 'Free' : money(a.tuition[1]) })]),
          h('div', { class: 'pw-meter' }, [h('span', { text: 'Living / yr' }), costBar(a.living, max, 'secondary'), h('output', { text: money(a.living[1]) })]),
        ]),
        h('div', { class: 'pw-row' }, a.fields.map(function (x) { return h('span', { class: 'pw-tag', text: x }); })),
        h('p', { class: 'pw-empty', text: 'Tests: ' + a.exams.join(', ') + '.' }),
        h('p', { class: 'pw-empty', text: a.work + '. ' + a.note }),
      ].concat(sch.length ? [h('div', { class: 'pw-row' }, sch.map(function (s) { return h('button', { class: 'pw-chip', type: 'button', 'data-goto-sch': s.id }, [s.name]); }))] : [])));
    });
    view.textContent = '';
    view.appendChild(h('div', { class: 'pw-intro' }, [h('h2', { text: 'Study abroad' }), h('p', { text: 'Yearly cost bars show the low to high range in NPR on one shared scale.' })]));
    view.appendChild(grid);
  }

  /* ---- scholarships ---- */
  function drawSch() {
    var lv = ['bachelor', 'master', 'phd', 'diploma'];
    var f = h('div', { class: 'pw-filters' }, [chip('', 'All', !state.scope, 'scope'), chip('nepal', 'In Nepal', state.scope === 'nepal', 'scope'), chip('abroad', 'Abroad', state.scope === 'abroad', 'scope')]);
    lv.forEach(function (l) { f.appendChild(chip(l, l.charAt(0).toUpperCase() + l.slice(1), state.level === l, 'level')); });
    var grid = h('div', { class: 'pw-grid' }), n = 0;
    D.scholarships.filter(function (s) { return (!state.scope || s.scope === state.scope) && (!state.level || s.levels.indexOf(state.level) >= 0); }).forEach(function (s) {
      grid.appendChild(h('article', { class: 'pw-card', i: Math.min(n++, 14), id: 'sch-' + s.id }, [
        h('div', { class: 'pw-card-top' }, [h('span', { class: 'pw-tag', text: s.scope === 'nepal' ? 'Nepal' : 'Abroad' }), h('span', { class: 'pw-tag', 'data-t': 'tertiary', text: s.levels.join(', ') })]),
        h('h3', { text: s.name }),
        h('p', { class: 'pw-empty', text: s.by }),
        kv('Covers', s.covers), kv('Who', s.who), kv('How', s.how),
      ].concat(s.link ? [h('a', { class: 'pw-link', href: s.link, target: '_blank', rel: 'noopener nofollow' }, ['Official site', icon('open_in_new')])] : [])));
    });
    view.textContent = '';
    view.appendChild(h('div', { class: 'pw-intro' }, [h('h2', { text: 'Scholarships' }), h('p', { text: 'Embassy routes, government awards and fellowships.' })]));
    view.appendChild(f); view.appendChild(grid);
  }
  /* ---- questions ---- */
  function drawFaq() {
    var f = h('div', { class: 'pw-filters', role: 'group', 'aria-label': 'Topic' }, [chip('', 'All', !state.topic, 'topic')]);
    (D.topics || []).forEach(function (t) { f.appendChild(chip(t.id, t.label, state.topic === t.id, 'topic')); });
    var list = h('div', { class: 'pw-faq' });
    (D.faq || []).filter(function (q) { return !state.topic || q.topic === state.topic; }).forEach(function (q) {
      var go = (q.go || []).map(function (id) { return routes[id]; }).filter(Boolean);
      var body = h('div', { class: 'pw-q-body' }, [h('p', { text: q.a })].concat(go.length ? [h('div', { class: 'pw-row' }, go.map(function (r) { return h('button', { class: 'pw-chip', type: 'button', 'data-route': r.id, text: r.name }); }))] : []));
      list.appendChild(h('details', { class: 'pw-q' }, [h('summary', null, [h('span', { text: q.q }), icon('expand_more')]), body]));
    });
    view.textContent = '';
    view.appendChild(h('div', { class: 'pw-intro' }, [h('h2', { text: 'Questions' })]));
    view.appendChild(f); view.appendChild(list);
  }
  function kv(k, v) { return h('p', { class: 'pw-empty' }, [h('b', { text: k + ': ' }), v]); }

  /* ---- detail sheet ---- */
  function meter(label, n, tone, text) {
    var fill = h('span', { class: 'pw-fill', 'data-t': tone }); fill.style.width = (n / 5 * 100) + '%'; fill.style.left = '0';
    return h('div', { class: 'pw-meter' }, [h('span', { text: label }), h('div', { class: 'pw-track' }, [fill]), h('output', { text: text })]);
  }
  function careerCard(c) {
    var max = 600000, e = c.salary.entry, s = c.salary.senior;
    var sal = h('span', { class: 'pw-fill', 'data-t': 'secondary' }); sal.style.left = (e[0] / max * 100) + '%'; sal.style.width = Math.max(3, (s[1] - e[0]) / max * 100) + '%';
    var arrow = c.trend === 'rising' ? 'trending_up' : (c.trend === 'slowing' ? 'trending_down' : 'check');
    return h('div', { class: 'pw-career' }, [
      h('div', { class: 'pw-career-head' }, [h('b', { text: c.name }), h('span', { class: 'pw-tag', 'data-t': 'primary' }, [c.trend])]),
      h('p', { text: c.about }),
      meter('Demand', c.demand, 'primary', dots(c.demand)), meter('Competition', c.competition, 'tertiary', dots(c.competition)), meter('Abroad demand', c.abroad, 'primary', dots(c.abroad)),
      h('div', { class: 'pw-meter' }, [h('span', { text: 'Monthly pay' }), h('div', { class: 'pw-track' }, [sal]), h('output', { text: money(e[0]) + ' to ' + money(s[1]) })]),
    ]);
  }
  function drawPlaces(r, box) {
    var d = state.district;
    box.textContent = '';
    var curated = r.where.map(function (id) { return providers[id]; }).filter(function (p) { return p && (!d || p.district === d); });
    if (curated.length) curated.forEach(function (p) {
      box.appendChild(h(p.website ? 'a' : 'div', { class: 'pw-place', href: p.website || null, target: p.website ? '_blank' : null, rel: p.website ? 'noopener nofollow' : null }, [
        h('b', { text: p.name }), h('span', { text: p.kind + ', ' + p.sector + ', ' + p.place + ', ' + p.district }), h('span', { text: p.note })]));
    });
    else box.appendChild(h('p', { class: 'pw-empty', text: d ? 'No listed provider in ' + d + ' yet. Colleges found there:' : 'Pick a district to see providers near you.' }));
    if (d) {
      var kind = /Diploma|Technical/.test(r.kind) ? 'institute' : (r.stage === 'afterbach' ? 'university' : 'college');
      var live = h('div', { class: 'pw-sec' });
      box.appendChild(live);
      fetch('/api/institutions/?limit=6&kind=' + kind + '&district=' + encodeURIComponent(d)).then(function (x) { return x.json(); }).then(function (j) {
        (j.items || []).forEach(function (it) { live.appendChild(h('a', { class: 'pw-place', href: '/app/schools/' + it.slug + '/' }, [h('b', { text: it.name }), h('span', { text: it.location || it.district })])); });
        live.appendChild(h('a', { class: 'pw-link', href: '/app/schools/?kind=' + kind + '&district=' + encodeURIComponent(d) }, ['See all in ' + d, icon('arrow_forward')]));
      }).catch(function () {});
    }
  }
  function openRoute(id, push) {
    var r = routes[id]; if (!r) return;
    state.open = id;
    var sel = h('select', { class: 'md-select pw-select', 'aria-label': 'District' }, [h('option', { value: '', text: 'All districts' })].concat(DISTRICTS.map(function (x) { return h('option', { value: x, text: x }); })));
    sel.value = state.district;
    var places = h('div', { class: 'pw-sec' });
    sel.addEventListener('change', function () { state.district = sel.value; localStorage.setItem('pw-district', sel.value); drawPlaces(r, places); });
    var cs = r.careers.map(function (c) { return careers[c]; }).filter(Boolean);
    sheetBody.textContent = '';
    [
      h('div', { class: 'pw-sh-head' }, [h('div', { class: 'pw-row' }, [h('span', { class: 'pw-tag', text: r.kind }), h('span', { class: 'pw-tag', 'data-t': 'tertiary', text: GROUPS[r.group] || '' })]), h('h2', { text: r.name }), h('p', { text: r.about })]),
      h('div', { class: 'pw-stats' }, [stat('Duration', r.years), stat('Total cost', npr(r.fee)), stat('Entry test', r.exam.split(',')[0].split(' (')[0])]),
      sec('Who can apply', [h('p', { class: 'pw-empty', text: r.entry }), h('p', { class: 'pw-empty', text: 'Exam: ' + r.exam })]),
      r.skills.length ? sec('Skills you build', [h('div', { class: 'pw-row' }, r.skills.map(function (s) { return h('span', { class: 'pw-tag', text: s }); }))]) : null,
      cs.length ? sec('Careers it leads to', cs.map(careerCard)) : null,
      r.next.length ? sec('Next steps', [h('div', { class: 'pw-row' }, r.next.map(function (n) { return h('button', { class: 'pw-chip', type: 'button', 'data-route': n }, [routes[n].name]); }))]) : null,
      sec('Where to study', [sel, places]),
    ].forEach(function (n) { if (n) sheetBody.appendChild(n); });
    drawPlaces(r, places);
    sheet.hidden = false; scrim.hidden = false; sheetBody.scrollTop = 0;
    document.body.style.overflow = 'hidden';
    if (push !== false) history.pushState(null, '', '#route=' + id);
    $('pw-close').focus({ preventScroll: true });
  }
  function stat(k, v) { return h('div', { class: 'pw-stat' }, [h('b', { text: v }), h('span', { text: k })]); }
  function sec(title, kids) { return h('div', { class: 'pw-sec' }, [h('h4', { text: title })].concat(kids)); }
  function closeSheet(back) {
    if (sheet.hidden) return;
    sheet.hidden = true; scrim.hidden = true; state.open = ''; document.body.style.overflow = '';
    if (back !== false && /route=/.test(location.hash)) history.back();
  }

  /* ---- routing ---- */
  function draw() {
    drawTabs();
    if (state.tab === 'abroad') drawAbroad(); else if (state.tab === 'scholarships') drawSch(); else if (state.tab === 'faq') drawFaq(); else drawStage();
  }
  function setTab(t) { state.tab = t; state.group = ''; draw(); if (!/route=/.test(location.hash)) history.replaceState(null, '', '#' + t); window.scrollTo({ top: 0 }); }
  function fromHash(first) {
    var m = location.hash.replace('#', '');
    if (/^route=/.test(m)) {
      var id = m.slice(6), r = routes[id];
      if (r) { if (first || state.tab !== r.stage) { state.tab = r.stage; draw(); } openRoute(id, false); return; }
    } else {
      closeSheet(false);
      if (TABS.some(function (t) { return t.id === m; })) { state.tab = m; }
    }
    draw();
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-tab],[data-route],[data-chip],[data-goto-sch]');
    if (!t || !$('pw-root').contains(t)) return;
    if (t.dataset.tab) setTab(t.dataset.tab);
    else if (t.dataset.route) openRoute(t.dataset.route);
    else if (t.dataset.chip) { state[t.dataset.chip] = state[t.dataset.chip] === t.dataset.value ? '' : t.dataset.value; if (!t.dataset.value) state[t.dataset.chip] = ''; draw(); }
    else if (t.dataset.gotoSch) { state.tab = 'scholarships'; draw(); var el = $('sch-' + t.dataset.gotoSch); if (el) el.scrollIntoView({ block: 'center' }); }
  });
  scrim.addEventListener('click', function () { closeSheet(); });
  $('pw-close').addEventListener('click', function () { closeSheet(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeSheet(); });
  window.addEventListener('popstate', function () { fromHash(false); });
  // the data is one cacheable request (ETag, an hour); the shell is already on screen
  fetch(view.dataset.src, { credentials: 'omit' }).then(function (r) { return r.json(); }).then(function (data) {
    D = data; routes = by(D.routes); careers = by(D.careers); providers = by(D.providers); scholarships = by(D.scholarships);
    TABS = D.stages.map(function (s) { return { id: s.id, label: s.label, icon: s.icon }; })
      .concat([{ id: 'abroad', label: 'Abroad', icon: 'public' }, { id: 'scholarships', label: 'Scholarships', icon: 'payments' }].concat((D.faq || []).length ? [{ id: 'faq', label: 'Questions', icon: 'help' }] : []));
    fromHash(true);
  }).catch(function () {
    view.textContent = '';
    view.appendChild(h('p', { class: 'pw-empty', text: 'Could not load Pathways. Check your connection and reload.' }));
  });
})();
