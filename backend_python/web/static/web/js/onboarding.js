/* Welcome flow. One page, one state object, steps rendered from the catalog the server embeds.
   Nothing is preselected for role, status or level: the answer a person gives is the answer saved. */
(function () {
  'use strict';

  var boot = JSON.parse(document.getElementById('ob-boot').textContent);
  var CAT = boot.catalog;
  var LEVELS = CAT.levels;
  var LEVEL = {};
  LEVELS.forEach(function (l) { LEVEL[l.value] = l; });
  var STATUS = {};
  CAT.statuses.forEach(function (s) { STATUS[s.value] = s; });
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function csv(v) { return String(v || '').split(',').map(function (x) { return x.trim(); }).filter(Boolean); }

  var I = boot.initial;
  var S = {
    role: I.role, username: I.username, displayName: I.displayName, dob: I.dob, gender: I.gender,
    status: I.status, level: I.level, program: I.program, term: I.term, completed: I.completed,
    subjects: csv(I.subjects), teachingSubjects: csv(I.teachingSubjects),
    institutionType: I.institutionType, school: I.school, pradesh: I.pradesh, district: I.district,
    headline: I.headline, skills: csv(I.skills), openTo: csv(I.openTo), bio: I.bio
  };

  var stage = document.getElementById('ob-stage');
  var nextBtn = document.getElementById('ob-next');
  var nextLabel = document.getElementById('ob-next-label');
  var backBtn = document.getElementById('ob-back');
  var errEl = document.getElementById('ob-error');
  var progress = document.getElementById('ob-progress');
  var idx = 0, saving = false, current = null;

  /* ---------- tiny DOM helpers ---------- */
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
      var b = h('button', {
        type: 'button', class: 'ob-chip', 'data-v': o.value, style: '--i:' + Math.min(i, 24),
        onclick: function () {
          var cur = opts.get().slice();
          var at = cur.indexOf(o.value);
          if (opts.multi) {
            if (at === -1) { if (opts.max && cur.length >= opts.max) return; cur.push(o.value); } else cur.splice(at, 1);
          } else {
            cur = (at !== -1 && opts.toggle) ? [] : [o.value];
          }
          opts.set(cur); paint(); update();
        }
      }, o.icon ? icon(o.icon) : null, h('span', { text: o.label }));
      wrap.appendChild(b);
    });
    paint();
    return wrap;
  }

  /* A text box that filters a long list and also accepts what you typed. */
  function combo(opts) {
    var input = h('input', { type: 'text', class: 'ob-input', placeholder: opts.placeholder, autocomplete: 'off', id: opts.id });
    var list = h('div', { class: 'ob-chips ob-combo-list' });
    var picked = h('div', { class: 'ob-picked' });
    function showPicked() {
      picked.textContent = '';
      var v = opts.get();
      if (v) picked.appendChild(h('button', { type: 'button', class: 'ob-chip is-on ob-chip-clear', onclick: function () { opts.set(''); showPicked(); filter(); update(); }, 'aria-label': 'Clear ' + v }, h('span', { text: v }), icon('close')));
    }
    function pick(v) { opts.set(v); input.value = ''; showPicked(); filter(); update(); }
    function filter() {
      var q = input.value.trim().toLowerCase();
      list.textContent = '';
      var items = opts.items.filter(function (x) { return !q || x.toLowerCase().indexOf(q) !== -1; });
      items.slice(0, q ? 30 : 18).forEach(function (x, i) {
        list.appendChild(h('button', { type: 'button', class: 'ob-chip' + (opts.get() === x ? ' is-on' : ''), style: '--i:' + Math.min(i, 24), onclick: function () { pick(x); } }, h('span', { text: x })));
      });
      if (q && !opts.items.some(function (x) { return x.toLowerCase() === q; })) {
        list.appendChild(h('button', { type: 'button', class: 'ob-chip ob-chip-custom', onclick: function () { pick(input.value.trim()); } }, icon('add'), h('span', { text: 'Use "' + input.value.trim() + '"' })));
      }
      if (!q && opts.items.length > 18) list.appendChild(h('span', { class: 'ob-more', text: 'Type to search ' + opts.items.length + ' options' }));
    }
    input.addEventListener('input', filter);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); e.stopPropagation(); var q = input.value.trim(); if (q) pick(q); } });
    showPicked(); filter();
    return h('div', { class: 'ob-combo' }, picked, input, list);
  }

  /* Free-form list (subjects, skills): suggestion chips plus whatever is typed. */
  function tags(opts) {
    var input = h('input', { type: 'text', class: 'ob-input', placeholder: opts.placeholder, autocomplete: 'off', maxlength: '40' });
    var chosen = h('div', { class: 'ob-chips ob-tags' });
    var sugg = h('div', { class: 'ob-chips ob-tags-sugg' });
    function paint() {
      chosen.textContent = '';
      opts.get().forEach(function (v) {
        chosen.appendChild(h('button', { type: 'button', class: 'ob-chip is-on', 'aria-label': 'Remove ' + v, onclick: function () { remove(v); } }, h('span', { text: v }), icon('close')));
      });
      sugg.textContent = '';
      var have = opts.get().map(function (x) { return x.toLowerCase(); });
      var q = input.value.trim().toLowerCase();
      opts.suggestions.filter(function (x) { return have.indexOf(x.toLowerCase()) === -1 && (!q || x.toLowerCase().indexOf(q) !== -1); })
        .slice(0, 14).forEach(function (x, i) {
          sugg.appendChild(h('button', { type: 'button', class: 'ob-chip', style: '--i:' + i, onclick: function () { add(x); } }, icon('add'), h('span', { text: x })));
        });
    }
    function add(v) {
      v = v.replace(/,/g, ' ').trim();
      if (!v) return;
      var cur = opts.get();
      if (cur.some(function (x) { return x.toLowerCase() === v.toLowerCase(); }) || cur.length >= opts.max) return;
      opts.set(cur.concat(v)); input.value = ''; paint(); update();
    }
    function remove(v) { opts.set(opts.get().filter(function (x) { return x !== v; })); paint(); update(); }
    input.addEventListener('input', paint);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ',') { e.preventDefault(); e.stopPropagation(); add(input.value); }
      else if (e.key === 'Backspace' && !input.value && opts.get().length) { remove(opts.get()[opts.get().length - 1]); }
    });
    paint();
    return h('div', { class: 'ob-tagbox' }, chosen, input, sugg);
  }

  /* ---------- education picker (status -> level -> program -> term -> completed) ---------- */
  var FORMAL = ['School', '+2 and equivalent', 'Technical and diploma', 'University'];
  var AUTO_LEVEL = { working: 'Professional', self_learning: 'Self Learner', abroad: 'Abroad' };
  var TERM_STATUSES = ['studying', 'dropped_out', 'gap_year', 'abroad'];
  var TEACHER_LEVELS = ['+2 Passout', 'Diploma', 'Bachelors', 'Masters', 'PhD'];

  function levelsFor(status, teacher) {
    if (teacher) return LEVELS.filter(function (l) { return TEACHER_LEVELS.indexOf(l.value) !== -1; });
    if (status === 'preparing') return LEVELS.filter(function (l) { return l.group === 'Preparing'; });
    if (AUTO_LEVEL[status]) return [];
    return LEVELS.filter(function (l) { return FORMAL.indexOf(l.group) !== -1 || l.value === 'Other'; });
  }

  function eduPicker(teacher) {
    var root = h('div', { class: 'ob-edu' });
    var blocks = {};
    function block(key, sig, build) {
      var b = blocks[key];
      if (b && b.sig === sig) return;
      if (b && b.el.parentNode) b.el.parentNode.removeChild(b.el);
      blocks[key] = null;
      if (!build) return;
      var el = h('section', { class: 'ob-reveal', 'data-k': key });
      build(el);
      blocks[key] = { sig: sig, el: el };
      var order = ['status', 'level', 'program', 'term', 'completed'];
      var after = null;
      for (var i = order.indexOf(key) + 1; i < order.length && !after; i++) { if (blocks[order[i]]) after = blocks[order[i]].el; }
      root.insertBefore(el, after);
    }
    function refresh() {
      var st = teacher ? 'completed' : S.status;
      if (teacher && !S.status) S.status = 'completed';
      if (!teacher) {
        block('status', 'status', function (el) {
          el.appendChild(label('Where are you right now?'));
          el.appendChild(h('div', { class: 'ob-tiles' }, CAT.statuses.map(function (s, i) {
            var t = h('button', { type: 'button', class: 'ob-tile' + (S.status === s.value ? ' is-on' : ''), 'data-v': s.value, style: '--i:' + i,
              onclick: function () { setStatus(s.value); } },
              h('span', { class: 'ob-tile-glyph' }, icon(s.icon)),
              h('span', { class: 'ob-tile-text' }, h('b', { text: s.label }), h('small', { text: s.hint })));
            return t;
          })));
        });
        Array.prototype.forEach.call(root.querySelectorAll('.ob-tile'), function (t) { t.classList.toggle('is-on', t.dataset.v === S.status); });
      }
      var auto = AUTO_LEVEL[st];
      if (auto && S.level !== auto) { S.level = auto; S.program = ''; S.term = ''; }
      var opts = levelsFor(st, teacher);
      var showLevel = (teacher || st) && opts.length;
      if (showLevel && S.level && !opts.some(function (l) { return l.value === S.level; })) { S.level = ''; S.program = ''; S.term = ''; }
      block('level', showLevel ? 'lv:' + st : '', showLevel ? function (el) {
        var q = teacher ? 'Your highest qualification' :
          (st === 'dropped_out' || st === 'gap_year') ? 'Which level were you in?' :
          st === 'preparing' ? 'What are you preparing for?' : 'Which level?';
        el.appendChild(label(q, teacher ? 'Optional' : ''));
        var groups = [];
        opts.forEach(function (l) { if (groups.indexOf(l.group) === -1) groups.push(l.group); });
        groups.forEach(function (g) {
          if (groups.length > 1) el.appendChild(h('div', { class: 'ob-group', text: g }));
          el.appendChild(chips({
            options: opts.filter(function (l) { return l.group === g; }).map(function (l) { return { value: l.value, label: l.label, icon: l.icon }; }),
            get: function () { return S.level ? [S.level] : []; },
            set: function (v) { S.level = v[0] || ''; S.program = ''; S.term = ''; refresh(); },
            toggle: teacher
          }));
        });
      } : null);
      // keep the selected level chip lit across groups
      Array.prototype.forEach.call(root.querySelectorAll('[data-k="level"] .ob-chip'), function (b) { b.classList.toggle('is-on', b.dataset.v === S.level); });
      var lv = LEVEL[S.level];
      var hasProg = lv && (lv.programs.length || lv.program_label);
      block('program', hasProg ? 'pg:' + S.level : '', hasProg ? function (el) {
        el.appendChild(label(lv.program_label || 'Course', 'Optional'));
        el.appendChild(combo({
          id: 'ob-program', items: lv.programs, placeholder: 'Search or type yours',
          get: function () { return S.program; }, set: function (v) { S.program = v; }
        }));
      } : null);
      var termKind = lv ? lv.terms : 'none';
      var showTerm = !teacher && termKind !== 'none' && TERM_STATUSES.indexOf(st) !== -1;
      block('term', showTerm ? 'tm:' + S.level + ':' + st : '', showTerm ? function (el) {
        el.appendChild(label(st === 'studying' ? 'Which year or semester?' : 'How far did you get?', 'Optional'));
        var mode = /^Semester/.test(S.term) ? 'semester' : 'year';
        var holder = h('div');
        function lists() {
          holder.textContent = '';
          var kinds = termKind === 'part' ? ['part'] : termKind === 'year' ? ['year'] : [mode];
          var items = kinds[0] === 'part' ? CAT.terms.part : kinds[0] === 'year' ? CAT.terms.year : CAT.terms[mode];
          if (termKind !== 'part') items = items.concat(CAT.terms.finished);
          holder.appendChild(chips({
            options: items.map(function (t) { return { value: t, label: t }; }),
            get: function () { return S.term ? [S.term] : []; }, set: function (v) { S.term = v[0] || ''; }, toggle: true
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
      var asks = !teacher && STATUS[st] && STATUS[st].ask_completed;
      block('completed', asks ? 'cp:' + st : '', asks ? function (el) {
        el.appendChild(label('Highest level you finished', 'Optional'));
        el.appendChild(chips({
          options: CAT.completed.map(function (c) { return { value: c.value, label: c.label }; }),
          get: function () { return S.completed ? [S.completed] : []; }, set: function (v) { S.completed = v[0] || ''; }, toggle: true
        }));
      } : null);
      if (!asks) S.completed = '';
      update();
    }
    function setStatus(v) {
      S.status = v;
      if (v !== 'preparing' && !AUTO_LEVEL[v] && LEVEL[S.level] && LEVEL[S.level].group === 'Preparing') { S.level = ''; S.program = ''; }
      refresh();
    }
    refresh();
    return root;
  }

  /* ---------- steps ---------- */
  function eduLine() {
    var lv = LEVEL[S.level];
    if (!lv) return '';
    var parts = /^Class/.test(lv.label) ? [lv.label, S.program] : [S.program || lv.label, S.term];
    return parts.filter(Boolean).join(' \u00b7 ');
  }

  var TIPS = {
    student: ['Learning something new every day', 'Preparing for my exams', 'Building my first projects'],
    teacher: ['Making hard subjects simple', 'Teaching with patience and examples'],
    institution: ['Quality education within reach'],
    explorer: ['Curious about everything']
  };
  var SKILL_IDEAS = ['Python', 'Public speaking', 'Graphic design', 'Video editing', 'Writing', 'Mathematics', 'Teaching', 'Excel', 'Web design', 'Photography', 'Leadership', 'English'];

  var STEPS = {
    role: {
      title: function () { return 'Welcome' + (S.displayName ? ', ' + S.displayName.split(' ')[0] : '') + '. Who are you here as?'; },
      build: function () {
        var cards = h('div', { class: 'ob-roles' }, boot.roles.map(function (r, i) {
          return h('button', { type: 'button', class: 'ob-role' + (S.role === r.value ? ' is-on' : ''), 'data-v': r.value, style: '--i:' + i,
            onclick: function (e) {
              S.role = r.value;
              Array.prototype.forEach.call(cards.children, function (c) { c.classList.toggle('is-on', c === e.currentTarget); });
              heroIcon.textContent = r.icon; heroIcon.classList.remove('pop'); void heroIcon.offsetWidth; heroIcon.classList.add('pop');
              drawProgress(); update();
            } },
            h('span', { class: 'ob-role-glyph md-shape-' + r.shape }, icon(r.icon)),
            h('span', { class: 'ob-role-text' }, h('b', { text: r.label }), h('small', { text: r.sub })),
            h('span', { class: 'ob-role-check' }, icon('check')));
        }));
        var heroIcon = icon((boot.roles.filter(function (r) { return r.value === S.role; })[0] || boot.roles[0]).icon);
        var hero = h('div', { class: 'ob-hero', 'aria-hidden': 'true' },
          h('span', { class: 'ob-blob b1' }), h('span', { class: 'ob-blob b2' }), h('span', { class: 'ob-blob b3' }),
          h('span', { class: 'ob-hero-core' }, heroIcon));
        return h('div', { class: 'ob-split' }, hero, cards);
      },
      valid: function () { return S.role ? '' : 'Pick one to continue.'; }
    },
    you: {
      title: function () { return S.role === 'institution' ? 'Who manages this account?' : 'A little about you'; },
      build: function () {
        var name = h('input', { type: 'text', id: 'ob-name', class: 'ob-input', maxlength: '150', autocomplete: 'name', value: S.displayName,
          placeholder: S.role === 'institution' ? 'Your name' : 'Name people will see',
          oninput: function () { S.displayName = name.value; update(); } });
        var today = new Date();
        var max = (today.getFullYear() - 4) + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2);
        var dob = h('input', { type: 'date', id: 'ob-dob', class: 'ob-input', value: S.dob, min: (today.getFullYear() - 100) + '-01-01', max: max,
          onchange: function () { S.dob = dob.value; update(); } });
        var out = h('div', { class: 'ob-form' }, field('ob-name', 'Display name', name));
        if (I.autoUsername) {
          var un = h('input', { type: 'text', id: 'ob-user', class: 'ob-input', maxlength: '50', autocomplete: 'username', value: S.username, placeholder: 'letters, numbers, underscore',
            oninput: function () { S.username = un.value.trim(); update(); } });
          out.appendChild(field('ob-user', 'Username', un));
        }
        out.appendChild(field('ob-dob', 'Date of birth', dob));
        out.appendChild(label('Gender'));
        out.appendChild(chips({ options: boot.genders.map(function (g) { return { value: g, label: g }; }), get: function () { return S.gender ? [S.gender] : []; }, set: function (v) { S.gender = v[0] || ''; } }));
        return out;
      },
      valid: function () {
        if (!S.displayName.trim()) return 'Add the name people will see.';
        if (I.autoUsername && !/^[A-Za-z0-9_]{3,50}$/.test(S.username)) return 'Username: 3 to 50 letters, numbers or underscores.';
        if (!S.dob) return 'Pick your date of birth.';
        if (!S.gender) return 'Pick one of the gender options.';
        return '';
      }
    },
    learn: {
      title: function () { return 'Where are you in your studies?'; },
      build: function () { return eduPicker(false); },
      valid: function () { return !S.status ? 'Pick what describes you best.' : (!S.level ? 'Pick your level.' : ''); }
    },
    teach: {
      title: function () { return 'What do you teach?'; },
      build: function () {
        return h('div', { class: 'ob-form' },
          label('Subjects you teach'),
          tags({ placeholder: 'Search or type a subject', suggestions: boot.subjects, max: 20, get: function () { return S.teachingSubjects; }, set: function (v) { S.teachingSubjects = v; } }),
          eduPicker(true));
      },
      valid: function () { return S.teachingSubjects.length ? '' : 'Add at least one subject.'; }
    },
    org: {
      title: function () { return 'Tell us about your institution'; },
      build: function () {
        var name = h('input', { type: 'text', id: 'ob-school', class: 'ob-input', maxlength: '200', value: S.school, placeholder: 'Official name', oninput: function () { S.school = name.value; update(); } });
        return h('div', { class: 'ob-form' }, field('ob-school', 'Institution name', name), label('Kind of institution'),
          chips({ options: boot.institutionTypes.map(function (t) { return { value: t.value, label: t.label }; }), get: function () { return S.institutionType ? [S.institutionType] : []; }, set: function (v) { S.institutionType = v[0] || ''; } }));
      },
      valid: function () { return !S.school.trim() ? 'Your institution needs a name.' : (!S.institutionType ? 'Pick the kind of institution.' : ''); }
    },
    interests: {
      title: function () { return 'What do you want to explore?'; },
      build: function () {
        return h('div', { class: 'ob-form' }, label('Subjects and topics', 'Optional'),
          tags({ placeholder: 'Search or type a topic', suggestions: boot.subjects, max: 30, get: function () { return S.subjects; }, set: function (v) { S.subjects = v; } }));
      },
      valid: function () { return ''; }
    },
    where: {
      title: function () { return 'Where are you based?'; },
      build: function () {
        var out = h('div', { class: 'ob-form' }, label('Province', 'Optional'),
          chips({ options: boot.pradesh, toggle: true, get: function () { return S.pradesh ? [S.pradesh] : []; }, set: function (v) { S.pradesh = v[0] || ''; } }),
          label('District', 'Optional'),
          combo({ id: 'ob-district', items: boot.districts, placeholder: 'Search your district', get: function () { return S.district; }, set: function (v) { S.district = boot.districts.indexOf(v) !== -1 ? v : ''; } }));
        if (S.role !== 'institution') {
          var sc = h('input', { type: 'text', id: 'ob-school', class: 'ob-input', maxlength: '200', value: S.school, oninput: function () { S.school = sc.value; update(); },
            placeholder: S.role === 'teacher' ? 'Where you teach' : 'Your school or college' });
          out.appendChild(field('ob-school', S.role === 'teacher' ? 'School or college' : 'School or college (optional)', sc));
        }
        return out;
      },
      valid: function () { return ''; }
    },
    shine: {
      title: function () { return 'Make your profile yours'; },
      build: function () {
        var hl = h('input', { type: 'text', id: 'ob-headline', class: 'ob-input', maxlength: '120', value: S.headline, placeholder: 'One line about you', oninput: function () { S.headline = hl.value; update(); } });
        var tips = (TIPS[S.role] || []).slice();
        if (eduLine()) tips.unshift(eduLine());
        var tipRow = h('div', { class: 'ob-chips' }, tips.slice(0, 4).map(function (t, i) {
          return h('button', { type: 'button', class: 'ob-chip', style: '--i:' + i, onclick: function () { hl.value = t; S.headline = t; update(); } }, h('span', { text: t }));
        }));
        var bio = h('textarea', { id: 'ob-bio', class: 'ob-input ob-textarea', maxlength: '300', rows: '3', placeholder: 'Anything else you want people to know', oninput: function () { S.bio = bio.value; } });
        bio.value = S.bio;
        var out = h('div', { class: 'ob-form' }, field('ob-headline', 'Headline', hl), tipRow);
        if (S.role === 'student') {
          out.appendChild(label('Subjects you study', 'Optional'));
          out.appendChild(tags({ placeholder: 'Search or type a subject', suggestions: boot.subjects, max: 30, get: function () { return S.subjects; }, set: function (v) { S.subjects = v; } }));
        }
        out.appendChild(label('Skills', 'Optional'));
        out.appendChild(tags({ placeholder: 'Add a skill', suggestions: SKILL_IDEAS, max: 15, get: function () { return S.skills; }, set: function (v) { S.skills = v; } }));
        out.appendChild(label('Open to', 'Optional'));
        out.appendChild(chips({ multi: true, max: 10, options: CAT.openTo.map(function (o) { return { value: o.value, label: o.label, icon: o.icon }; }), get: function () { return S.openTo; }, set: function (v) { S.openTo = v; } }));
        out.appendChild(field('ob-bio', 'About you', bio));
        return out;
      },
      valid: function () { return ''; }
    },
    done: {
      title: function () { return "You're in, " + (S.displayName.split(' ')[0] || 'friend') + '.'; },
      build: function () {
        var burst = h('div', { class: 'ob-burst', 'aria-hidden': 'true' });
        var shapes = ['cookie-9', 'clover', 'gem', 'slanted', 'sunny', 'pentagon', 'cookie-4', 'soft-burst'];
        shapes.forEach(function (s, i) { burst.appendChild(h('span', { class: 'ob-confetti md-shape-' + s, style: '--a:' + (i * 45) + 'deg;--i:' + i })); });
        var role = boot.roles.filter(function (r) { return r.value === S.role; })[0];
        return h('div', { class: 'ob-done' }, burst,
          h('div', { class: 'ob-done-core md-shape-' + (role ? role.shape : 'cookie-9') }, icon('check')),
          h('p', { class: 'ob-done-line', text: 'Your profile is live. Add projects, certificates and achievements from your profile any time.' }));
      },
      valid: function () { return ''; }
    }
  };

  function flow() {
    var mid = { student: ['learn'], teacher: ['teach'], institution: ['org'], explorer: ['interests'] }[S.role] || ['learn'];
    return ['role', 'you'].concat(mid, ['where', 'shine', 'done']);
  }

  /* ---------- chrome ---------- */
  function drawProgress() {
    var f = flow();
    progress.textContent = '';
    f.forEach(function (id, i) {
      progress.appendChild(h('li', { class: 'ob-seg-dot' + (i < idx ? ' is-done' : '') + (i === idx ? ' is-now' : '') }));
    });
  }

  function initial() { return ((S.displayName || S.username || 'N').trim().charAt(0) || 'N').toUpperCase(); }
  function update() {
    var role = boot.roles.filter(function (r) { return r.value === S.role; })[0];
    var avatar = document.getElementById('ob-card-avatar');
    avatar.className = 'ob-card-avatar md-shape-' + (role ? role.shape : 'cookie-9');
    var set = function (id, text) {
      var el = document.getElementById(id);
      if (el.textContent !== text) { el.textContent = text; el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop'); }
    };
    set('ob-card-initial', initial());
    set('ob-card-name', S.displayName.trim() || 'Your name');
    set('ob-card-user', '@' + (S.username || 'username'));
    set('ob-card-headline', S.headline);
    set('ob-card-edu', eduLine());
    var chipsEl = document.getElementById('ob-card-chips');
    var want = [];
    if (role) want.push(role.label);
    if (STATUS[S.status]) want.push(STATUS[S.status].label);
    if (S.district) want.push(S.district);
    S.openTo.slice(0, 3).forEach(function (k) { CAT.openTo.forEach(function (o) { if (o.value === k) want.push(o.label); }); });
    S.skills.slice(0, 3).forEach(function (k) { want.push(k); });
    var sig = want.join('|');
    if (chipsEl.dataset.sig !== sig) {
      chipsEl.dataset.sig = sig; chipsEl.textContent = '';
      want.forEach(function (w, i) { chipsEl.appendChild(h('span', { class: 'ob-card-chip', style: '--i:' + i, text: w })); });
    }
  }

  function setError(msg) {
    errEl.textContent = msg || '';
    errEl.classList.toggle('on', !!msg);
  }

  function show(dir) {
    var f = flow();
    var id = f[idx];
    var def = STEPS[id];
    var old = current;
    var el = h('section', { class: 'ob-step ' + (old ? (dir >= 0 ? 'in-fwd' : 'in-back') : 'in-first'), 'data-step': id });
    var head = h('h1', { class: 'ob-title', tabindex: '-1', text: def.title() });
    el.appendChild(head);
    el.appendChild(def.build());
    stage.appendChild(el);
    if (old) {
      old.classList.add(dir >= 0 ? 'out-fwd' : 'out-back');
      setTimeout(function () { if (old.parentNode) old.parentNode.removeChild(old); }, reduceMotion ? 0 : 320);
    }
    current = el;
    drawProgress();
    setError('');
    var last = id === 'shine';
    nextLabel.textContent = id === 'done' ? (boot.next ? 'Continue' : 'Open my profile') : (last ? 'Finish' : 'Continue');
    nextBtn.querySelector('.material-symbols-outlined').textContent = id === 'done' ? 'arrow_forward' : (last ? 'check' : 'arrow_forward');
    backBtn.hidden = idx === 0 || id === 'done';
    document.getElementById('ob').dataset.step = id;
    window.scrollTo(0, 0);
    try { head.focus({ preventScroll: true }); } catch (e) { /* older browsers */ }
    update();
  }

  function payload() {
    return {
      role: S.role, username: S.username, displayName: S.displayName, dob: S.dob, gender: S.gender,
      status: S.status, level: S.level, program: S.program, term: S.term, completed: S.completed,
      subjects: S.subjects.join(','), teachingSubjects: S.teachingSubjects.join(','),
      institutionType: S.institutionType, school: S.school, pradesh: S.pradesh, district: S.district,
      headline: S.headline, skills: S.skills.join(','), openTo: S.openTo.join(','), bio: S.bio, next: boot.next
    };
  }

  function csrf() { return (typeof CSRF_TOKEN !== 'undefined') ? CSRF_TOKEN : ''; }

  function save() {
    saving = true; nextBtn.disabled = true;
    nextLabel.textContent = 'Saving';
    fetch(boot.saveUrl + (boot.next ? '?next=' + encodeURIComponent(boot.next) : ''), {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify(payload())
    }).then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (res) {
        saving = false; nextBtn.disabled = false;
        if (res.ok && res.d.ok) {
          boot.profileUrl = res.d.profileUrl || boot.profileUrl;
          if (res.d.next) boot.next = res.d.next;
          idx = flow().length - 1; show(1);
        } else {
          nextLabel.textContent = 'Finish';
          setError(res.d.error || 'Something went wrong. Try again.');
          var f = flow();
          var stepFor = { role: 'role', displayName: 'you', username: 'you', dob: 'you', gender: 'you',
            level: f[2], status: f[2], teachingSubjects: 'teach', school: 'org', institutionType: 'org' };
          var target = f.indexOf(stepFor[res.d.field]);
          if (target > -1 && target !== idx) { idx = target; show(-1); setError(res.d.error); }
        }
      }).catch(function () {
        saving = false; nextBtn.disabled = false; nextLabel.textContent = 'Finish';
        setError('Network error. Check your connection and try again.');
      });
  }

  function next() {
    if (saving) return;
    var f = flow(), id = f[idx];
    if (id === 'done') { window.location.href = boot.next || boot.profileUrl; return; }
    var msg = STEPS[id].valid();
    if (msg) { setError(msg); nextBtn.classList.remove('shake'); void nextBtn.offsetWidth; nextBtn.classList.add('shake'); return; }
    if (id === 'shine') { save(); return; }
    idx++; show(1);
  }

  nextBtn.addEventListener('click', next);
  backBtn.addEventListener('click', function () { if (idx > 0) { idx--; show(-1); } });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && e.target && e.target.tagName === 'INPUT' && e.target.type !== 'date') { e.preventDefault(); next(); }
  });
  show(1);
})();
