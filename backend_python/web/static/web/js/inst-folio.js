/* Institution portfolio editor on the profile page. One section at a time, nothing required, any time.
   Sections mirror the app's SECTIONS (InstitutionManageScreen.kt) and api/institution_profile.py key for key. */
(function () {
  'use strict';
  var bootEl = document.getElementById('if-boot');
  if (!bootEl) return;
  var boot = JSON.parse(bootEl.textContent || '{}');
  var schema = boot.schema || {};
  var details = boot.details || {};
  var est = boot.est || '';
  var SOCIALS = [['facebook', 'Facebook'], ['instagram', 'Instagram'], ['youtube', 'YouTube'], ['tiktok', 'TikTok'], ['x', 'X'], ['linkedin', 'LinkedIn']];
  var SECTIONS = {
    about: ['About', [['about', 'About the institution', 'area'], ['motto', 'Motto', 'text']]],
    basics: ['Basics', [['est', 'Established (year)', 'year'], ['principal', 'Principal', 'text'], ['principalTitle', 'Principal title', 'text'],
      ['regNo', 'Registration number', 'text'], ['ownership', 'Ownership', 'one'], ['affiliations', 'Affiliated with', 'many'],
      ['streams', 'Streams', 'many'], ['mediums', 'Medium of teaching', 'many'], ['genderMix', 'Who studies here', 'one']]],
    levels: ['Levels offered', [['levels', 'Levels and courses', 'many']]],
    numbers: ['Numbers', [['students', 'Total students', 'num'], ['teachers', 'Teachers', 'num'], ['staff', 'Other staff', 'num'], ['classrooms', 'Classrooms', 'num']]],
    programs: ['Programs', [['programs', 'Program', 'rows', [['name', 'Program name'], ['level', 'Level'], ['seats', 'Seats'], ['fee', 'Yearly fee (Rs)']]]]],
    branches: ['Branches', [['branches', 'Branch', 'rows', [['name', 'Branch name'], ['place', 'Place'], ['phone', 'Phone']]]]],
    facilities: ['Facilities', [['facilities', 'What you offer', 'many']]],
    fees: ['Fees', [['feeMin', 'Lowest yearly fee (Rs)', 'num'], ['feeMax', 'Highest yearly fee (Rs)', 'num'], ['feeNote', 'Fee note', 'text']]],
    admissions: ['Admissions', [['admissionOpen', 'Admissions are open', 'toggle'], ['admissionNote', 'Intake note', 'text']]],
    contact: ['Contact', [['phone', 'Phone', 'text'], ['email', 'Email', 'text'], ['address', 'Address', 'text']]],
    socials: ['Social links', [['socials', 'Links', 'socials']]]
  };
  var scrim, form, body, titleEl, errEl, saveBtn, current;

  function el(tag, cls, html) { var n = document.createElement(tag); if (cls) n.className = cls; if (html != null) n.innerHTML = html; return n; }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function csrf() { return (typeof CSRF_TOKEN !== 'undefined') ? CSRF_TOKEN : ''; }

  function build() {
    scrim = el('div', 'neb-scrim neb-scrim-bottom');
    scrim.id = 'if-sheet';
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
    errEl = el('p', 'pf-error'); errEl.hidden = true; errEl.setAttribute('role', 'alert');
    form.addEventListener('submit', submit);
  }

  function opts(key) { return (schema[key] || []); }
  function chip(label, on) {
    var b = el('button', 'neb-choice-chip', '<span class="neb-chip-tick"></span>' + esc(label));
    b.type = 'button'; b.setAttribute('aria-pressed', on ? 'true' : 'false');
    return b;
  }
  function field(f) {
    var key = f[0], label = f[1], kind = f[2], box = el('div', 'pf-field pf-wide');
    var cap = el('span', 'md-label', esc(label));
    if (kind === 'toggle') {
      var t = chip(label, !!details[key]); t.dataset.key = key; t.dataset.kind = 'toggle';
      t.addEventListener('click', function () { t.setAttribute('aria-pressed', t.getAttribute('aria-pressed') === 'true' ? 'false' : 'true'); });
      box.appendChild(t); return box;
    }
    box.appendChild(cap);
    if (kind === 'many' || kind === 'one') {
      var picked = kind === 'many' ? (details[key] || []).slice() : (details[key] ? [details[key]] : []);
      var row = el('div', 'pf-folio-chips'); row.dataset.key = key; row.dataset.kind = kind;
      opts(key).forEach(function (o) {
        var c = chip(o.label, picked.indexOf(o.value) >= 0); c.dataset.value = o.value;
        c.addEventListener('click', function () {
          var on = c.getAttribute('aria-pressed') !== 'true';
          if (kind === 'one') row.querySelectorAll('.neb-choice-chip').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
          c.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        row.appendChild(c);
      });
      box.appendChild(row); return box;
    }
    if (kind === 'socials') {
      var s = details.socials || {}; box.removeChild(cap);
      SOCIALS.forEach(function (p) {
        var w = el('label', 'pf-field pf-wide', '<span class="md-label">' + p[1] + '</span><input class="md-input" data-social="' + p[0] + '" inputmode="url" placeholder="https://" value="' + esc(s[p[0]] || '') + '">');
        box.appendChild(w);
      });
      return box;
    }
    if (kind === 'rows') {
      var cols = f[3], list = el('div', 'if-rows'); list.dataset.key = key;
      var add = el('button', 'if-add', '<span class="material-symbols-outlined">add</span>Add ' + esc(label.toLowerCase())); add.type = 'button';
      var addRow = function (v) {
        var r = el('div', 'if-rowform');
        cols.forEach(function (c) { r.appendChild(el('input', 'md-input', '')); var i = r.lastChild; i.placeholder = c[1]; i.dataset.col = c[0]; i.value = v && v[c[0]] != null ? v[c[0]] : ''; i.maxLength = 100; });
        var x = el('button', 'if-x', '<span class="material-symbols-outlined">close</span>'); x.type = 'button'; x.setAttribute('aria-label', 'Remove');
        x.addEventListener('click', function () { r.remove(); }); r.appendChild(x); list.appendChild(r);
      };
      (details[key] || []).forEach(addRow); if (!(details[key] || []).length) addRow();
      add.addEventListener('click', function () { addRow(); });
      box.appendChild(list); box.appendChild(add); return box;
    }
    var inp = kind === 'area' ? el('textarea', 'md-input md-textarea') : el('input', 'md-input');
    inp.dataset.key = key; inp.dataset.kind = kind;
    if (kind === 'area') inp.rows = 5;
    if (kind === 'num' || kind === 'year') inp.inputMode = 'numeric';
    if (kind === 'year') inp.maxLength = 4;
    inp.value = key === 'est' ? est : (details[key] == null ? '' : details[key]);
    box.appendChild(inp); return box;
  }

  function open(id) {
    var sec = SECTIONS[id]; if (!sec) return;
    if (!scrim) build();
    current = id; titleEl.textContent = sec[0]; body.innerHTML = '';
    sec[1].forEach(function (f) { body.appendChild(field(f)); });
    body.appendChild(errEl); errEl.hidden = true; form.classList.remove('is-done'); saveBtn.textContent = 'Save'; saveBtn.disabled = false;
    if (window.NebUI) window.NebUI.open(scrim); else scrim.hidden = false;
  }

  function collect() {
    var out = {};
    body.querySelectorAll('[data-key]').forEach(function (n) {
      var k = n.dataset.key, kind = n.dataset.kind;
      if (kind === 'toggle') out[k] = n.getAttribute('aria-pressed') === 'true';
      else if (kind === 'many') out[k] = Array.prototype.map.call(n.querySelectorAll('[aria-pressed=true]'), function (c) { return c.dataset.value; });
      else if (kind === 'one') { var c = n.querySelector('[aria-pressed=true]'); out[k] = c ? c.dataset.value : ''; }
      else if (n.classList.contains('if-rows')) {
        out[k] = Array.prototype.map.call(n.querySelectorAll('.if-rowform'), function (r) {
          var o = {}; r.querySelectorAll('[data-col]').forEach(function (i) { o[i.dataset.col] = i.value.trim(); }); return o;
        }).filter(function (o) { return o.name; });
      } else if (n.tagName === 'INPUT' || n.tagName === 'TEXTAREA') out[k] = n.value.trim();
    });
    var soc = body.querySelectorAll('[data-social]');
    if (soc.length) { out.socials = {}; soc.forEach(function (i) { if (i.value.trim()) out.socials[i.dataset.social] = i.value.trim(); }); }
    return out;
  }

  function submit(e) {
    e.preventDefault();
    var data = collect(); data.slug = boot.slug;
    saveBtn.disabled = true; errEl.hidden = true;
    fetch('/ajax/institution/portfolio/save/', { method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify(data) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { ok: r.ok && d.ok, d: d }; }); })
      .then(function (res) {
        if (!res.ok) { errEl.textContent = res.d.error || 'That did not save. Try again.'; errEl.hidden = false; saveBtn.disabled = false; return; }
        form.classList.add('is-done'); saveBtn.textContent = 'Saved';
        setTimeout(function () { window.location.reload(); }, 380);
      })
      .catch(function () { errEl.textContent = 'No connection. Try again.'; errEl.hidden = false; saveBtn.disabled = false; });
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-inst-edit]');
    if (b) open(b.dataset.instEdit);
  });
  /* The profile's Edit button for an institution opens the first section that is still empty. */
  window.NebInstFolio = { open: open };
})();
