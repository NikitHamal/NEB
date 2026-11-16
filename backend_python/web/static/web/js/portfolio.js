/* Owner's portfolio editor on the profile: one sheet for add and edit (NebUI sheet: scrim, drag to dismiss,
   Escape, focus trap). Dates are a month and a year the member picks, never a typed or native "---- ----" field;
   the server still receives "YYYY-MM". Markup: web/profile/_portfolio.html. */
(function () {
  'use strict';
  var sheet = document.getElementById('pf-entry-sheet');
  if (!sheet) return;
  /* The sheet is fixed to the viewport, so it must not live inside a card that clips or transforms. */
  document.body.appendChild(sheet);

  var $ = function (id) { return document.getElementById(id); };
  var KINDS = {
    education: { label: 'education', icon: 'school', where: 'School or college' },
    experience: { label: 'experience', icon: 'work', where: 'Company or team' },
    past_school: { label: 'past school', icon: 'history_edu', where: 'School' },
    project: { label: 'project', icon: 'deployed_code', where: 'Where it lives' },
    achievement: { label: 'achievement', icon: 'emoji_events', where: 'Who gave it' },
    certificate: { label: 'certificate', icon: 'workspace_premium', where: 'Issued by' },
    volunteering: { label: 'volunteering', icon: 'volunteer_activism', where: 'Organisation' }
  };
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var form = $('pf-entry-form');
  var save = $('pf-entry-save');
  var del = $('pf-entry-delete');
  var err = $('pf-entry-error');
  var cur = $('pf-entry-current');
  var busy = false;
  var armed = 0;

  function csrf() { return (typeof CSRF_TOKEN !== 'undefined') ? CSRF_TOKEN : ''; }

  function fill(month, year) {
    var top = new Date().getFullYear() + 6;
    var m = '<option value="">Month</option>';
    MONTHS.forEach(function (name, i) { m += '<option value="' + ('0' + (i + 1)).slice(-2) + '">' + name + '</option>'; });
    var y = '<option value="">Year</option>';
    for (var n = top; n >= 1970; n--) y += '<option value="' + n + '">' + n + '</option>';
    month.innerHTML = m;
    year.innerHTML = y;
  }
  function pair(prefix) {
    var month = $('pf-entry-' + prefix + '-m');
    var year = $('pf-entry-' + prefix + '-y');
    fill(month, year);
    return {
      get: function () {
        if (!year.value) return '';
        return year.value + '-' + (month.value || '01');
      },
      set: function (iso) {
        var m = /^(\d{4})-(\d{2})/.exec(iso || '');
        year.value = m ? m[1] : '';
        month.value = m ? m[2] : '';
        /* NebSelect repaints on a change event; a bare assignment would leave the old label showing. */
        year.dispatchEvent(new Event('change', { bubbles: true }));
        month.dispatchEvent(new Event('change', { bubbles: true }));
      },
      lock: function (on) { month.disabled = on; year.disabled = on; }
    };
  }
  var start = pair('start');
  var end = pair('end');

  function setCurrent(on) {
    cur.setAttribute('aria-pressed', on ? 'true' : 'false');
    $('pf-entry-end-wrap').classList.toggle('is-off', on);
    end.lock(on);
    if (on) end.set('');
  }
  function say(text) {
    err.textContent = text || '';
    err.hidden = !text;
  }
  function disarm() {
    armed = 0;
    del.classList.remove('is-armed');
    del.textContent = 'Delete';
  }
  function open(entry, kind) {
    entry = entry || {};
    var k = entry.kind || kind;
    var meta = KINDS[k] || { label: 'entry', icon: 'add', where: 'Where' };
    busy = false;
    save.disabled = false;
    save.textContent = 'Save';
    sheet.classList.remove('is-done');
    disarm();
    $('pf-entry-id').value = entry.id || '';
    $('pf-entry-kind').value = k;
    $('pf-entry-title').textContent = (entry.id ? 'Edit ' : 'Add ') + meta.label;
    $('pf-entry-icon').textContent = meta.icon;
    $('pf-entry-name').value = entry.title || '';
    $('pf-entry-name').removeAttribute('aria-invalid');
    $('pf-entry-org').value = entry.org || '';
    $('pf-entry-org').placeholder = meta.where;
    start.set(entry.start || '');
    end.set(entry.end || '');
    setCurrent(!!entry.isCurrent);
    $('pf-entry-desc').value = entry.description || '';
    $('pf-entry-url').value = entry.url || '';
    say('');
    del.hidden = !entry.id;
    if (window.NebUI) window.NebUI.open(sheet); else sheet.hidden = false;
    setTimeout(function () { if (!entry.id) $('pf-entry-name').focus(); }, 60);
  }

  function post(url, body) {
    return fetch(url, { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { ok: r.ok && d.ok, d: d }; }); });
  }
  function finish() {
    sheet.classList.add('is-done');
    save.textContent = 'Saved';
    setTimeout(function () { window.location.reload(); }, 420);
  }

  document.addEventListener('click', function (e) {
    var add = e.target.closest('[data-folio-add]');
    if (add) { open(null, add.dataset.folioAdd); return; }
    var edit = e.target.closest('[data-folio-edit]');
    if (edit) { try { open(JSON.parse(edit.closest('.pf-tl-item').dataset.entry)); } catch (x) { /* malformed row */ } }
  });
  cur.addEventListener('click', function () { setCurrent(cur.getAttribute('aria-pressed') !== 'true'); });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (busy) return;
    if (!$('pf-entry-name').value.trim()) {
      say('Add a title.');
      $('pf-entry-name').setAttribute('aria-invalid', 'true');
      $('pf-entry-name').focus();
      return;
    }
    $('pf-entry-name').removeAttribute('aria-invalid');
    busy = true;
    save.disabled = true;
    save.textContent = 'Saving';
    say('');
    var body = { id: $('pf-entry-id').value || undefined, kind: $('pf-entry-kind').value, title: $('pf-entry-name').value, org: $('pf-entry-org').value,
      start: start.get(), end: end.get(), isCurrent: cur.getAttribute('aria-pressed') === 'true',
      description: $('pf-entry-desc').value, url: $('pf-entry-url').value };
    post('/ajax/portfolio/save/', body).then(function (res) {
      if (res.ok) { finish(); return; }
      busy = false; save.disabled = false; save.textContent = 'Save';
      say(res.d.error || 'Could not save.');
    }).catch(function () {
      busy = false; save.disabled = false; save.textContent = 'Save';
      say('Network error. Try again.');
    });
  });

  /* Delete asks once, in place: the first tap changes the button, the second does it. */
  del.addEventListener('click', function () {
    if (busy) return;
    if (!armed) {
      armed = Date.now();
      del.classList.add('is-armed');
      del.textContent = 'Delete for good';
      setTimeout(function () { if (armed && Date.now() - armed > 3500) disarm(); }, 3600);
      return;
    }
    busy = true;
    post('/ajax/portfolio/delete/', { id: Number($('pf-entry-id').value) }).then(function (res) {
      if (res.ok) { finish(); return; }
      busy = false; disarm();
      say(res.d.error || 'Could not delete.');
    }).catch(function () { busy = false; disarm(); say('Network error. Try again.'); });
  });
  sheet.addEventListener('neb:close', disarm);
})();
