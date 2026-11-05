/* Owner's portfolio editor on the profile: one dialog for add and edit. */
(function () {
  'use strict';
  var dlg = document.getElementById('pf-entry-dialog');
  if (!dlg) return;
  var $ = function (id) { return document.getElementById(id); };
  var TITLES = { education: 'Education', experience: 'Experience', project: 'Project', achievement: 'Achievement', certificate: 'Certificate', volunteering: 'Volunteering' };
  var busy = false;
  function csrf() { return (typeof CSRF_TOKEN !== 'undefined') ? CSRF_TOKEN : ''; }
  function open(entry, kind) {
    entry = entry || {};
    $('pf-entry-id').value = entry.id || '';
    $('pf-entry-kind').value = entry.kind || kind;
    $('pf-entry-title').textContent = (entry.id ? 'Edit ' : 'Add ') + (TITLES[$('pf-entry-kind').value] || 'entry').toLowerCase();
    $('pf-entry-name').value = entry.title || '';
    $('pf-entry-org').value = entry.org || '';
    $('pf-entry-start').value = entry.start || '';
    $('pf-entry-end').value = entry.end || '';
    $('pf-entry-current').checked = !!entry.isCurrent;
    $('pf-entry-end').disabled = !!entry.isCurrent;
    $('pf-entry-desc').value = entry.description || '';
    $('pf-entry-url').value = entry.url || '';
    $('pf-entry-error').textContent = '';
    $('pf-entry-delete').hidden = !entry.id;
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
    $('pf-entry-name').focus();
  }
  function close() { if (dlg.close) dlg.close(); else dlg.removeAttribute('open'); }
  function post(url, body) {
    return fetch(url, { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok && d.ok, d: d }; }); });
  }
  document.addEventListener('click', function (e) {
    var add = e.target.closest('[data-folio-add]');
    if (add) { open(null, add.dataset.folioAdd); return; }
    var edit = e.target.closest('[data-folio-edit]');
    if (edit) { try { open(JSON.parse(edit.closest('.pf-tl-item').dataset.entry)); } catch (x) { /* malformed row */ } }
  });
  $('pf-entry-current').addEventListener('change', function () { $('pf-entry-end').disabled = this.checked; if (this.checked) $('pf-entry-end').value = ''; });
  $('pf-entry-cancel').addEventListener('click', close);
  $('pf-entry-form').addEventListener('submit', function (e) {
    e.preventDefault();
    if (busy) return;
    busy = true;
    var body = { id: $('pf-entry-id').value || undefined, kind: $('pf-entry-kind').value, title: $('pf-entry-name').value, org: $('pf-entry-org').value,
      start: $('pf-entry-start').value, end: $('pf-entry-end').value, isCurrent: $('pf-entry-current').checked,
      description: $('pf-entry-desc').value, url: $('pf-entry-url').value };
    post('/ajax/portfolio/save/', body).then(function (res) {
      busy = false;
      if (res.ok) window.location.reload(); else $('pf-entry-error').textContent = res.d.error || 'Could not save.';
    }).catch(function () { busy = false; $('pf-entry-error').textContent = 'Network error. Try again.'; });
  });
  $('pf-entry-delete').addEventListener('click', function () {
    if (busy) return; busy = true;
    post('/ajax/portfolio/delete/', { id: Number($('pf-entry-id').value) }).then(function (res) {
      busy = false;
      if (res.ok) window.location.reload(); else $('pf-entry-error').textContent = res.d.error || 'Could not delete.';
    }).catch(function () { busy = false; });
  });
})();
