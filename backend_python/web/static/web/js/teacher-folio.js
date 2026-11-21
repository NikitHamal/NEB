/* Teacher section editor on the profile page. One section at a time, nothing required, any time.
   Writes through POST /ajax/teacher/profile/save/ (same validation as the app's profile update). */
(function () {
  'use strict';
  var bootEl = document.getElementById('tf-boot');
  if (!bootEl) return;
  var boot = JSON.parse(bootEl.textContent || '{}');
  var SECTIONS = {
    school: ['Where you teach', [['school', 'Current school', 'text'], ['employment', 'Type of work', 'one', boot.optEmployment]]],
    teach: ['What you teach', [['teaching_subjects', 'Subjects, separated by commas', 'csv'], ['teach_levels', 'Levels', 'many', boot.optLevels]]],
    exp: ['Experience', [['experience_years', 'Years of teaching', 'num']]]
  };
  var VALUE = { school: boot.school, employment: boot.employment, teaching_subjects: (boot.subjects || []).join(', '),
    teach_levels: boot.levels || [], experience_years: boot.years || '' };
  var scrim, form, body, titleEl, errEl, saveBtn;

  function el(tag, cls, html) { var n = document.createElement(tag); if (cls) n.className = cls; if (html != null) n.innerHTML = html; return n; }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function csrf() { return (typeof CSRF_TOKEN !== 'undefined') ? CSRF_TOKEN : ''; }

  function build() {
    scrim = el('div', 'neb-scrim neb-scrim-bottom');
    scrim.setAttribute('data-neb-close', '');
    scrim.hidden = true;
    form = el('form', 'neb-sheet pf-sheet');
    form.setAttribute('role', 'dialog');
    form.setAttribute('aria-modal', 'true');
    form.noValidate = true;
    form.innerHTML = '<div class="neb-sheet-handle"></div><div class="neb-sheet-head"><div class="neb-sheet-head-text"><h3 class="neb-sheet-title"></h3></div>' +
      '<button type="button" class="neb-sheet-close" data-neb-close aria-label="Close"><span class="material-symbols-outlined">close</span></button></div>' +
      '<div class="neb-sheet-body pf-fields"></div><div class="neb-sheet-foot pf-foot"><span class="pf-foot-gap"></span>' +
      '<button type="button" class="md-btn md-btn-text" data-neb-close>Cancel</button><button type="submit" class="md-btn md-btn-filled">Save</button></div>';
    scrim.appendChild(form);
    document.body.appendChild(scrim);
    body = form.querySelector('.pf-fields');
    titleEl = form.querySelector('.neb-sheet-title');
    saveBtn = form.querySelector('[type=submit]');
    errEl = el('p', 'pf-error');
    errEl.hidden = true;
    errEl.setAttribute('role', 'alert');
    form.addEventListener('submit', submit);
  }

  function chip(label, on) {
    var b = el('button', 'neb-choice-chip', '<span class="neb-chip-tick"></span>' + esc(label));
    b.type = 'button';
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
    return b;
  }

  function field(f) {
    var key = f[0], kind = f[2], box = el('div', 'pf-field pf-wide');
    box.appendChild(el('span', 'md-label', esc(f[1])));
    if (kind === 'one' || kind === 'many') {
      var picked = kind === 'many' ? (VALUE[key] || []) : (VALUE[key] ? [VALUE[key]] : []);
      var row = el('div', 'pf-folio-chips');
      row.dataset.key = key;
      row.dataset.kind = kind;
      (f[3] || []).forEach(function (o) {
        var c = chip(o.label, picked.indexOf(o.value) >= 0);
        c.dataset.value = o.value;
        c.addEventListener('click', function () {
          var on = c.getAttribute('aria-pressed') !== 'true';
          if (kind === 'one') row.querySelectorAll('.neb-choice-chip').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
          c.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        row.appendChild(c);
      });
      box.appendChild(row);
      return box;
    }
    var inp = el('input', 'md-input');
    inp.dataset.key = key;
    inp.dataset.kind = kind;
    inp.autocomplete = 'off';
    inp.maxLength = kind === 'csv' ? 300 : (kind === 'num' ? 2 : 150);
    if (kind === 'num') inp.inputMode = 'numeric';
    inp.value = VALUE[key] == null ? '' : VALUE[key];
    box.appendChild(inp);
    return box;
  }

  function open(id) {
    var sec = SECTIONS[id];
    if (!sec) return;
    if (!scrim) build();
    titleEl.textContent = sec[0];
    body.innerHTML = '';
    sec[1].forEach(function (f) { body.appendChild(field(f)); });
    body.appendChild(errEl);
    errEl.hidden = true;
    form.classList.remove('is-done');
    saveBtn.textContent = 'Save';
    saveBtn.disabled = false;
    if (window.NebUI) window.NebUI.open(scrim); else scrim.hidden = false;
  }

  function collect() {
    var out = {};
    body.querySelectorAll('[data-key]').forEach(function (n) {
      var k = n.dataset.key, kind = n.dataset.kind;
      if (kind === 'many') out[k] = Array.prototype.map.call(n.querySelectorAll('[aria-pressed=true]'), function (c) { return c.dataset.value; });
      else if (kind === 'one') { var c = n.querySelector('[aria-pressed=true]'); out[k] = c ? c.dataset.value : ''; }
      else out[k] = n.value.trim();
    });
    return out;
  }

  function submit(e) {
    e.preventDefault();
    saveBtn.disabled = true;
    errEl.hidden = true;
    fetch('/ajax/teacher/profile/save/', { method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify(collect()) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { ok: r.ok && d.ok, d: d }; }); })
      .then(function (res) {
        if (!res.ok) { errEl.textContent = res.d.error || 'That did not save. Try again.'; errEl.hidden = false; saveBtn.disabled = false; return; }
        form.classList.add('is-done');
        saveBtn.textContent = 'Saved';
        setTimeout(function () { window.location.reload(); }, 380);
      })
      .catch(function () { errEl.textContent = 'No connection. Try again.'; errEl.hidden = false; saveBtn.disabled = false; });
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-tf-edit]');
    if (b) open(b.getAttribute('data-tf-edit'));
  });
})();
