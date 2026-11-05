/* Profile editor: mounts the shared education picker (NebEdu), skills and "open to" and keeps
   the hidden inputs the form posts in step with them. The same picker runs in the welcome flow. */
(function () {
  'use strict';
  var bootEl = document.getElementById('epf-boot');
  var mount = document.getElementById('epf-edu');
  if (!bootEl || !mount || !window.NebEdu) return;
  var E = window.NebEdu;
  var boot = JSON.parse(bootEl.textContent);
  var CAT = boot.catalog, I = boot.initial;
  var form = document.querySelector('.epf-form');
  var section = document.getElementById('epf-edu-section');

  function put(id, v) { var el = document.getElementById(id); if (el) el.value = v || ''; }
  function ping() { if (form) form.dispatchEvent(new Event('change', { bubbles: true })); }

  var S = { status: I.status, level: I.level, program: I.program, term: I.term, completed: I.completed };
  function sync() {
    put('class_level', S.level); put('edu_status', S.status); put('edu_program', S.program);
    put('edu_term', S.term); put('edu_completed', S.completed);
    ping();
  }

  function role() {
    var on = document.querySelector('.role-radio-card.role-radio-active input[type="radio"]');
    return on ? on.value : 'student';
  }

  var TEACHER_LEVELS = ['+2 Passout', 'Diploma', 'Bachelors', 'Masters', 'PhD'];
  var mode = null;
  function render(first) {
    var r = role();
    if (section) section.hidden = r === 'institution';
    var teacher = r === 'teacher';
    if (mode === teacher) return;
    /* Switching role: a Class 8 answer means nothing to a teacher, so start that question over. */
    if (!first && teacher && S.level && TEACHER_LEVELS.indexOf(S.level) === -1) {
      S.level = ''; S.program = ''; S.term = ''; S.completed = ''; S.status = '';
      sync();
    }
    mode = teacher;
    mount.textContent = '';
    mount.appendChild(E.picker({ catalog: CAT, state: S, full: !teacher, teacher: teacher, onChange: sync }));
  }
  window.addEventListener('epf:role', function () { render(false); });
  render(true);

  var skills = E.csv(I.skills), openTo = E.csv(I.openTo);
  var IDEAS = ['Python', 'Public speaking', 'Graphic design', 'Video editing', 'Writing', 'Mathematics',
    'Teaching', 'Excel', 'Web design', 'Photography', 'Leadership', 'English'];
  var skillsMount = document.getElementById('epf-skills');
  if (skillsMount) {
    skillsMount.appendChild(E.tags({
      placeholder: 'Add a skill', suggestions: IDEAS, max: 15, shown: 8,
      get: function () { return skills; }, set: function (v) { skills = v; },
      onChange: function () { put('skills', skills.join(',')); ping(); }
    }));
  }
  var openMount = document.getElementById('epf-opento');
  if (openMount) {
    openMount.appendChild(E.chips({
      multi: true, max: 10,
      options: CAT.openTo.map(function (o) { return { value: o.value, label: o.label, icon: o.icon }; }),
      get: function () { return openTo; },
      set: function (v) { openTo = v; put('open_to', v.join(',')); ping(); }
    }));
  }
})();
