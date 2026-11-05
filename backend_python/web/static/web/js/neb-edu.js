/* NebEdu: the form controls the welcome flow and the profile editor share.
   h()/chips()/combo()/tags() are the small builders; picker() is the one education question
   (stage -> level -> course -> year -> status). Both pages hand it a state object and read it
   back, so a course is added in api/education_catalog.py and shows up in both places. */
(function () {
  'use strict';

  function h(tag, props) {
    var el = document.createElement(tag);
    props = props || {};
    Object.keys(props).forEach(function (k) {
      var v = props[k];
      if (v === null || v === undefined || v === false) return;
      if (k === 'class') el.className = v;
      else if (k === 'text') el.textContent = v;
      else if (k.slice(0, 2) === 'on') el.addEventListener(k.slice(2), v);
      else if (k === 'style') el.setAttribute('style', v);
      else el.setAttribute(k, v === true ? '' : v);
    });
    function add(c) {
      if (c === null || c === undefined || c === false || c === true) return;
      if (Array.isArray(c) || (typeof c.length === 'number' && typeof c !== 'string' && !c.nodeType)) {
        Array.prototype.forEach.call(c, add);
        return;
      }
      if (c.nodeType) el.appendChild(c);
      else el.appendChild(document.createTextNode(String(c)));
    }
    for (var i = 2; i < arguments.length; i++) add(arguments[i]);
    return el;
  }
  function icon(name) { return h('span', { class: 'material-symbols-outlined', 'aria-hidden': 'true', text: name }); }
  function label(text, sub) {
    return h('div', { class: 'ob-label' }, h('span', { text: text }), sub ? h('small', { text: sub }) : null);
  }
  function field(id, text, input) { return h('div', { class: 'ob-field' }, h('label', { for: id, text: text }), input); }
  function csv(v) { return String(v || '').split(',').map(function (x) { return x.trim(); }).filter(Boolean); }

  /* Chips. opts: options[{value,label,icon}], get() -> [values], set([values]), multi, max, toggle. */
  function chips(opts) {
    var wrap = h('div', { class: 'ob-chips', role: opts.multi ? 'group' : 'radiogroup' });
    function paint() {
      Array.prototype.forEach.call(wrap.children, function (b) {
        var on = opts.get().indexOf(b.dataset.v) !== -1;
        b.classList.toggle('is-on', on);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    }
    opts.options.forEach(function (o, i) {
      wrap.appendChild(h('button', {
        type: 'button', class: 'ob-chip', 'data-v': o.value, style: '--i:' + Math.min(i, 24),
        onclick: function () {
          var cur = opts.get().slice();
          var at = cur.indexOf(o.value);
          if (opts.multi) {
            if (at === -1) { if (opts.max && cur.length >= opts.max) return; cur.push(o.value); } else cur.splice(at, 1);
          } else {
            cur = (at !== -1 && opts.toggle) ? [] : [o.value];
          }
          opts.set(cur); paint();
        }
      }, o.icon ? icon(o.icon) : null, h('span', { text: o.label })));
    });
    paint();
    return wrap;
  }

  /* A search box over a long list that also accepts what was typed.
     opts.pinned is what shows before anyone types (the popular few). */
  function combo(opts) {
    var input = h('input', { type: 'text', class: 'ob-input', placeholder: opts.placeholder, autocomplete: 'off', id: opts.id, 'data-neb-skip': '' });
    var list = h('div', { class: 'ob-chips ob-combo-list' });
    var picked = h('div', { class: 'ob-picked' });
    var shown = opts.pinned || opts.items.slice(0, 18);
    function done() { if (opts.onChange) opts.onChange(); }
    function showPicked() {
      picked.textContent = '';
      var v = opts.get();
      if (v && shown.indexOf(v) === -1) {
        picked.appendChild(h('button', { type: 'button', class: 'ob-chip is-on ob-chip-clear', 'aria-label': 'Clear ' + v,
          onclick: function () { opts.set(''); showPicked(); filter(); done(); } }, h('span', { text: v }), icon('close')));
      }
    }
    function pick(v) {
      opts.set(opts.get() === v ? '' : v);
      input.value = ''; showPicked(); filter(); done();
    }
    function filter() {
      var q = input.value.trim().toLowerCase();
      list.textContent = '';
      var items = q ? opts.items.filter(function (x) { return x.toLowerCase().indexOf(q) !== -1; }).slice(0, 30) : shown;
      items.forEach(function (x, i) {
        list.appendChild(h('button', { type: 'button', class: 'ob-chip' + (opts.get() === x ? ' is-on' : ''), 'aria-pressed': opts.get() === x ? 'true' : 'false',
          style: '--i:' + Math.min(i, 24), onclick: function () { pick(x); } }, h('span', { text: x })));
      });
      if (q && !opts.items.some(function (x) { return x.toLowerCase() === q; })) {
        list.appendChild(h('button', { type: 'button', class: 'ob-chip ob-chip-custom', onclick: function () { pick(input.value.trim()); } }, icon('add'), h('span', { text: 'Use "' + input.value.trim() + '"' })));
      }
    }
    input.addEventListener('input', filter);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); e.stopPropagation(); var q = input.value.trim(); if (q) pick(q); } });
    showPicked(); filter();
    return h('div', { class: 'ob-combo' }, list, picked, input);
  }

  /* Free-form list (subjects, skills): suggestion chips plus whatever is typed. */
  function tags(opts) {
    var input = h('input', { type: 'text', class: 'ob-input', placeholder: opts.placeholder, autocomplete: 'off', maxlength: '40', 'data-neb-skip': '' });
    var chosen = h('div', { class: 'ob-chips ob-tags' });
    var sugg = h('div', { class: 'ob-chips ob-tags-sugg' });
    function done() { if (opts.onChange) opts.onChange(); }
    function paint() {
      chosen.textContent = '';
      opts.get().forEach(function (v) {
        chosen.appendChild(h('button', { type: 'button', class: 'ob-chip is-on', 'aria-label': 'Remove ' + v, onclick: function () { remove(v); } }, h('span', { text: v }), icon('close')));
      });
      sugg.textContent = '';
      var have = opts.get().map(function (x) { return x.toLowerCase(); });
      var q = input.value.trim().toLowerCase();
      opts.suggestions.filter(function (x) { return have.indexOf(x.toLowerCase()) === -1 && (!q || x.toLowerCase().indexOf(q) !== -1); })
        .slice(0, opts.shown || 10).forEach(function (x, i) {
          sugg.appendChild(h('button', { type: 'button', class: 'ob-chip', style: '--i:' + i, onclick: function () { add(x); } }, icon('add'), h('span', { text: x })));
        });
    }
    function add(v) {
      v = v.replace(/,/g, ' ').trim();
      if (!v) return;
      var cur = opts.get();
      if (cur.some(function (x) { return x.toLowerCase() === v.toLowerCase(); }) || cur.length >= opts.max) return;
      opts.set(cur.concat(v)); input.value = ''; paint(); done();
    }
    function remove(v) { opts.set(opts.get().filter(function (x) { return x !== v; })); paint(); done(); }
    input.addEventListener('input', paint);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ',') { e.preventDefault(); e.stopPropagation(); add(input.value); }
      else if (e.key === 'Backspace' && !input.value && opts.get().length) { remove(opts.get()[opts.get().length - 1]); }
    });
    paint();
    return h('div', { class: 'ob-tagbox' }, chosen, input, sugg);
  }

  /* The education question. opts: catalog, state {status, level, program, term, completed},
     full (adds year and status), teacher (qualification, not a current class), onChange(). */
  var TERM_STATUSES = ['studying', 'gap_year', 'dropped_out'];
  var FORMAL_STATUSES = ['studying', 'completed', 'gap_year', 'dropped_out'];
  var TEACHER_LEVELS = ['+2 Passout', 'Diploma', 'Bachelors', 'Masters', 'PhD'];
  var LEVEL_LABEL_BY_STAGE = { school: 'Class', plus2: 'Level', diploma: 'Level', masters: 'Level', prep: 'Preparing for', other: 'Which fits you?' };

  function picker(opts) {
    var CAT = opts.catalog, S = opts.state, full = !!opts.full, teacher = !!opts.teacher;
    var LEVEL = {}, STATUS = {};
    CAT.levels.forEach(function (l) { LEVEL[l.value] = l; });
    CAT.statuses.forEach(function (s) { STATUS[s.value] = s; });
    var stages = CAT.stages.map(function (st) {
      var lv = teacher ? st.levels.filter(function (v) { return TEACHER_LEVELS.indexOf(v) !== -1; }) : st.levels;
      return { key: st.key, label: st.label, icon: st.icon, status: st.status, levels: lv };
    }).filter(function (st) { return st.levels.length; });
    function stageOf(level) {
      for (var i = 0; i < stages.length; i++) { if (stages[i].levels.indexOf(level) !== -1) return stages[i]; }
      return null;
    }
    var stage = stageOf(S.level);
    var root = h('div', { class: 'ob-edu' });
    var blocks = {};
    var ORDER = ['stage', 'level', 'program', 'term', 'status', 'completed'];

    function block(key, sig, build) {
      var b = blocks[key];
      if (b && b.sig === sig) return;
      if (b && b.el.parentNode) b.el.parentNode.removeChild(b.el);
      blocks[key] = null;
      if (!build) return;
      var el = h('section', { class: 'ob-reveal', 'data-k': key });
      build(el);
      blocks[key] = { sig: sig, el: el };
      var after = null;
      for (var i = ORDER.indexOf(key) + 1; i < ORDER.length && !after; i++) { if (blocks[ORDER[i]]) after = blocks[ORDER[i]].el; }
      root.insertBefore(el, after);
    }
    function changed() { if (opts.onChange) opts.onChange(S); }

    function impliedStatus() {
      if (teacher) return 'completed';
      if (S.level && CAT.levelStatus[S.level]) return CAT.levelStatus[S.level];
      if (stage && stage.status) return stage.status;
      return S.status || 'studying';
    }
    function pickLevel(v) {
      S.level = v; S.program = ''; S.term = '';
      var implied = impliedStatus();
      var keep = full && stage && ['prep', 'other'].indexOf(stage.key) === -1 && FORMAL_STATUSES.indexOf(S.status) !== -1;
      S.status = keep ? S.status : implied;
      refresh(); changed();
    }
    function pickStage(st) {
      stage = st; S.program = ''; S.term = '';
      if (st.levels.length === 1) { pickLevel(st.levels[0]); return; }
      S.level = ''; S.status = teacher ? 'completed' : (st.status || S.status);
      refresh(); changed();
    }

    function refresh() {
      /* stage tiles */
      block('stage', 'stage', function (el) {
        if (opts.stageLabel) el.appendChild(label(opts.stageLabel));
        el.appendChild(h('div', { class: 'ob-tiles ob-tiles-compact', role: 'radiogroup' }, stages.map(function (st, i) {
          return h('button', { type: 'button', class: 'ob-tile', role: 'radio', 'data-v': st.key, style: '--i:' + i, onclick: function () { pickStage(st); } },
            h('span', { class: 'ob-tile-glyph' }, icon(st.icon)),
            h('span', { class: 'ob-tile-text' }, h('b', { text: st.label })));
        })));
      });
      Array.prototype.forEach.call(root.querySelectorAll('[data-k="stage"] .ob-tile'), function (t) {
        var on = !!stage && t.dataset.v === stage.key;
        t.classList.toggle('is-on', on); t.setAttribute('aria-checked', on ? 'true' : 'false');
      });

      /* level chips, only when the stage has more than one */
      var many = stage && stage.levels.length > 1;
      block('level', many ? 'lv:' + stage.key : '', many ? function (el) {
        el.appendChild(label(LEVEL_LABEL_BY_STAGE[stage.key] || 'Level'));
        el.appendChild(chips({
          options: stage.levels.map(function (v) { return { value: v, label: LEVEL[v].label }; }),
          get: function () { return S.level ? [S.level] : []; },
          set: function (v) { if (v[0]) pickLevel(v[0]); }
        }));
      } : null);
      if (many) {
        Array.prototype.forEach.call(root.querySelectorAll('[data-k="level"] .ob-chip'), function (b) {
          var on = b.dataset.v === S.level; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
      }

      /* course */
      var lv = LEVEL[S.level];
      var hasProg = !!lv && (lv.programs.length || lv.program_label);
      block('program', hasProg ? 'pg:' + S.level : '', hasProg ? function (el) {
        var pinned = lv.popular && lv.popular.length ? lv.popular : lv.programs.slice(0, 18);
        el.appendChild(label(lv.program_label || 'Course', 'Optional'));
        el.appendChild(combo({
          id: 'neb-edu-program', items: lv.programs, pinned: pinned,
          placeholder: lv.programs.length > pinned.length ? 'Search ' + lv.programs.length + ' courses or type yours' : 'Or type yours',
          get: function () { return S.program; }, set: function (v) { S.program = v; }, onChange: changed
        }));
      } : null);

      /* year or semester, editor only */
      var termKind = lv ? lv.terms : 'none';
      var showTerm = full && !teacher && termKind !== 'none' && TERM_STATUSES.indexOf(S.status) !== -1;
      block('term', showTerm ? 'tm:' + S.level + ':' + S.status : '', showTerm ? function (el) {
        el.appendChild(label(S.status === 'studying' ? 'Year or semester' : 'How far did you get?', 'Optional'));
        var mode = /^Semester/.test(S.term) ? 'semester' : 'year';
        var holder = h('div');
        function lists() {
          holder.textContent = '';
          var items = termKind === 'part' ? CAT.terms.part : termKind === 'year' ? CAT.terms.year : CAT.terms[mode];
          if (termKind !== 'part') items = items.concat(CAT.terms.finished);
          holder.appendChild(chips({
            options: items.map(function (t) { return { value: t, label: t }; }),
            get: function () { return S.term ? [S.term] : []; }, set: function (v) { S.term = v[0] || ''; changed(); }, toggle: true
          }));
        }
        if (termKind === 'any') {
          el.appendChild(h('div', { class: 'ob-seg', role: 'tablist' }, ['year', 'semester'].map(function (m) {
            return h('button', { type: 'button', class: 'ob-seg-btn' + (m === mode ? ' is-on' : ''), onclick: function (e) {
              mode = m; Array.prototype.forEach.call(e.currentTarget.parentNode.children, function (x) { x.classList.toggle('is-on', x === e.currentTarget); });
              lists();
            }, text: m === 'year' ? 'Yearly' : 'Semesters' });
          })));
        }
        el.appendChild(holder); lists();
      } : null);

      /* where they are with it, editor only, formal stages only */
      var showStatus = full && !teacher && stage && ['prep', 'other'].indexOf(stage.key) === -1 && !!S.level;
      block('status', showStatus ? 'st' : '', showStatus ? function (el) {
        el.appendChild(label('Status'));
        el.appendChild(h('div', { class: 'ob-seg', role: 'radiogroup' }, FORMAL_STATUSES.map(function (v) {
          return h('button', { type: 'button', class: 'ob-seg-btn', 'data-v': v, role: 'radio', onclick: function () {
            S.status = v; if (TERM_STATUSES.indexOf(v) === -1) S.term = '';
            refresh(); changed();
          }, text: STATUS[v].label });
        })));
      } : null);
      Array.prototype.forEach.call(root.querySelectorAll('[data-k="status"] .ob-seg-btn'), function (b) {
        var on = b.dataset.v === S.status; b.classList.toggle('is-on', on); b.setAttribute('aria-checked', on ? 'true' : 'false');
      });

      var asks = full && !teacher && STATUS[S.status] && STATUS[S.status].ask_completed && S.level && showStatus;
      block('completed', asks ? 'cp:' + S.status : '', asks ? function (el) {
        el.appendChild(label('Highest level you finished', 'Optional'));
        el.appendChild(chips({
          options: CAT.completed.map(function (c) { return { value: c.value, label: c.label }; }),
          get: function () { return S.completed ? [S.completed] : []; }, set: function (v) { S.completed = v[0] || ''; changed(); }, toggle: true
        }));
      } : null);
      if (!asks) S.completed = '';
    }
    refresh();
    return root;
  }

  window.NebEdu = { h: h, icon: icon, label: label, field: field, csv: csv, chips: chips, combo: combo, tags: tags, picker: picker };
})();
