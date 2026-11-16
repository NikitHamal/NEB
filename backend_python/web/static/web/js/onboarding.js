/* Welcome flow. One page, one state object. Three quick steps (who you are, a little about you,
   what you study) and done; everything else lives in the profile editor.
   Nothing is preselected for role or level: the answer a person gives is the answer saved.
   Controls are shared: NebEdu (js/neb-edu.js) and the date wheel + gender tiles the profile
   editor uses (components/_dob_field.html, _gender_tiles.html). */
(function () {
  'use strict';

  var boot = JSON.parse(document.getElementById('ob-boot').textContent);
  var E = window.NebEdu;
  var h = E.h, icon = E.icon, label = E.label, field = E.field, csv = E.csv;
  var CAT = boot.catalog;
  var LEVEL = {};
  CAT.levels.forEach(function (l) { LEVEL[l.value] = l; });
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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

  /* The shared date and gender controls arrive rendered by the server (so they are the very
     same markup the editor uses) and are carried into the step that needs them. */
  var PARTS = { dob: document.getElementById('dob-field'), gender: document.getElementById('gender-field') };
  var dobInput = document.getElementById('dob');
  if (dobInput) dobInput.addEventListener('change', function () { S.dob = dobInput.value; update(); });
  var genderGroup = PARTS.gender && PARTS.gender.querySelector('[data-neb-group]');
  if (genderGroup) genderGroup.addEventListener('neb:change', function (e) { S.gender = e.detail.value || ''; update(); });

  function eduLine() {
    var lv = LEVEL[S.level];
    if (!lv) return '';
    var parts = /^Class/.test(lv.label) ? [lv.label, S.program] : [S.program || lv.label, S.term];
    return parts.filter(Boolean).join(' \u00b7 ');
  }

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
        var out = h('div', { class: 'ob-form ob-form-stack' }, field('ob-name', 'Display name', name));
        if (I.autoUsername) {
          var un = h('input', { type: 'text', id: 'ob-user', class: 'ob-input', maxlength: '50', autocomplete: 'username', value: S.username, placeholder: 'letters, numbers, underscore',
            oninput: function () { S.username = un.value.trim(); update(); } });
          out.appendChild(field('ob-user', 'Username', un));
        }
        /* One above the other: the date field, then the three gender tiles. */
        if (S.role !== 'institution') {  /* an institution has no date of birth or gender */
          if (PARTS.dob) out.appendChild(PARTS.dob);
          if (PARTS.gender) out.appendChild(PARTS.gender);
        }
        return out;
      },
      valid: function () {
        if (!S.displayName.trim()) return 'Add the name people will see.';
        if (I.autoUsername && !/^[A-Za-z0-9_]{3,50}$/.test(S.username)) return 'Username: 3 to 50 letters, numbers or underscores.';
        if (S.role === 'institution') return '';
        if (!S.dob) return 'Pick your date of birth.';
        if (!S.gender) return 'Pick one of the gender options.';
        return '';
      }
    },
    learn: {
      title: function () { return 'What are you studying?'; },
      build: function () {
        return h('div', { class: 'ob-form' }, E.picker({ catalog: CAT, state: S, onChange: update }));
      },
      valid: function () { return S.level ? '' : 'Pick where you are.'; }
    },
    teach: {
      title: function () { return 'What do you teach?'; },
      build: function () {
        return h('div', { class: 'ob-form' }, E.tags({ placeholder: 'Search or type a subject', suggestions: boot.subjects, max: 20, shown: 12,
          get: function () { return S.teachingSubjects; }, set: function (v) { S.teachingSubjects = v; }, onChange: update }));
      },
      valid: function () { return S.teachingSubjects.length ? '' : 'Add at least one subject.'; }
    },
    org: {
      title: function () { return 'Your institution'; },
      build: function () {
        var name = h('input', { type: 'text', id: 'ob-school', class: 'ob-input', maxlength: '200', value: S.school, placeholder: 'Official name', oninput: function () { S.school = name.value; update(); } });
        return h('div', { class: 'ob-form' }, field('ob-school', 'Name', name), label('Kind'),
          E.chips({ options: boot.institutionTypes.map(function (t) { return { value: t.value, label: t.label }; }), get: function () { return S.institutionType ? [S.institutionType] : []; },
            set: function (v) { S.institutionType = v[0] || ''; update(); } }));
      },
      valid: function () { return !S.school.trim() ? 'Your institution needs a name.' : (!S.institutionType ? 'Pick the kind of institution.' : ''); }
    },
    done: {
      title: function () { return "You're in, " + (S.displayName.split(' ')[0] || 'friend') + '.'; },
      build: function () {
        var burst = h('div', { class: 'ob-burst', 'aria-hidden': 'true' });
        var shapes = ['cookie-9', 'clover', 'gem', 'slanted', 'sunny', 'pentagon', 'cookie-4', 'soft-burst'];
        shapes.forEach(function (s, i) { burst.appendChild(h('span', { class: 'ob-confetti md-shape-' + s, style: '--a:' + (i * 45) + 'deg;--i:' + i })); });
        var role = boot.roles.filter(function (r) { return r.value === S.role; })[0];
        return h('div', { class: 'ob-done' }, burst,
          h('div', { class: 'ob-done-core md-shape-' + (role ? role.shape : 'cookie-9') }, icon('check')));
      },
      valid: function () { return ''; }
    }
  };

  function flow() {
    var mid = { student: ['learn'], teacher: ['teach'], institution: ['org'], explorer: [] }[S.role];
    return ['role', 'you'].concat(mid || ['learn'], ['done']);
  }
  function saveStep() { var f = flow(); return f[f.length - 2]; }

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
    set('ob-card-edu', eduLine());
    var chipsEl = document.getElementById('ob-card-chips');
    var want = [];
    if (role) want.push(role.label);
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
    var last = id === saveStep();
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
            level: 'learn', status: 'learn', teachingSubjects: 'teach', school: 'org', institutionType: 'org' };
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
    if (id === saveStep()) { save(); return; }
    idx++; show(1);
  }

  nextBtn.addEventListener('click', next);
  backBtn.addEventListener('click', function () { if (idx > 0) { idx--; show(-1); } });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && e.target && e.target.tagName === 'INPUT' && e.target.type !== 'date' && !e.target.closest('.neb-scrim')) { e.preventDefault(); next(); }
  });
  show(1);
})();
