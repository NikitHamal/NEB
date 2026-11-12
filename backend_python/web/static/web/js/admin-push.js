/* Admin push composer: audience modes, live recipient counts, phone preview, counters, destination field. */
(function () {
  'use strict';
  var form = document.getElementById('pushForm');
  if (!form) return;
  var $ = function (id) { return document.getElementById(id); };
  var title = $('title'), body = $('body');
  var fmt = function (n) { return Number(n || 0).toLocaleString('en-US'); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var DEFAULT_TITLE = 'Title', DEFAULT_BODY = 'Your message appears here.';
  var mode = form.dataset.mode || 'all';
  var sample = null;

  function mirror() {
    var tm = parseInt(form.dataset.titleMax, 10), bm = parseInt(form.dataset.bodyMax, 10);
    if (mode === 'unnotified') {
      $('pvTitle').textContent = sample ? sample.title : 'One digest per person';
      $('pvBody').textContent = sample ? sample.body : 'Matched by class and subject';
      return;
    }
    $('pvTitle').textContent = title.value.trim() || DEFAULT_TITLE;
    $('pvBody').textContent = body.value.trim() || DEFAULT_BODY;
    $('titleCount').textContent = title.value.length + '/' + tm;
    $('bodyCount').textContent = body.value.length + '/' + bm;
    $('titleCount').classList.toggle('is-over', title.value.length > tm);
    $('bodyCount').classList.toggle('is-over', body.value.length > bm);
  }
  title.addEventListener('input', mirror);
  body.addEventListener('input', mirror);

  function dest() {
    var v = (form.querySelector('input[name="dest"]:checked') || {}).value || 'none';
    var wrap = $('destIdWrap');
    wrap.hidden = mode === 'unnotified' || !(v === 'resource' || v === 'post');
    $('dest_id').required = !wrap.hidden;
    $('dest_id').disabled = wrap.hidden;
  }
  form.querySelectorAll('input[name="dest"]').forEach(function (r) { r.addEventListener('change', dest); });

  function applyMode() {
    mode = (form.querySelector('input[name="mode"]:checked') || {}).value || 'all';
    form.dataset.mode = mode;
    form.querySelectorAll('[data-modes]').forEach(function (el) {
      var on = el.getAttribute('data-modes').split(' ').indexOf(mode) !== -1;
      el.hidden = !on;
      el.querySelectorAll('input,select,textarea').forEach(function (f) { f.disabled = !on; });
    });
    form.querySelectorAll('[data-hide-modes]').forEach(function (el) {
      var off = el.getAttribute('data-hide-modes').split(' ').indexOf(mode) !== -1;
      el.hidden = off;
      if (el.matches('input,select,textarea,button')) { if (el.type !== 'submit') el.disabled = off; }
      el.querySelectorAll('input,select,textarea').forEach(function (f) { f.disabled = off; });
    });
    var batch = mode === 'unnotified';
    title.required = !batch;
    body.required = !batch;
    $('sendLabel').textContent = batch ? 'Announce' : 'Send';
    $('sendIcon').textContent = batch ? 'campaign' : 'send';
    $('sendBtn').setAttribute('data-confirm-title', batch ? 'Announce unnotified uploads?' : 'Send this notification?');
    dest();
    mirror();
  }

  var names = ['class_level', 'subject', 'role', 'device', 'active_days', 'inactive_days', 'joined_days', 'gender',
    'min_age', 'max_age', 'pradesh', 'district', 'school', 'usernames_or_ids'];
  var timer = null, seq = 0, last = { users: 0 };
  function query() {
    var p = new URLSearchParams();
    p.set('mode', mode);
    names.forEach(function (n) {
      var el = form.elements[n];
      if (!el) return;
      var v = (el.value || '').trim();
      var disabled = el.length ? Array.prototype.every.call(el, function (x) { return x.disabled; }) : el.disabled;
      if (v && !disabled) p.set(n, v);
    });
    p.set('count_only', '1');
    return p;
  }
  function confirmText() {
    var btn = $('sendBtn');
    var later = $('send_at').value && mode !== 'unnotified' ? ' It will go out at the time you picked.' : '';
    var unit = mode === 'unnotified' ? fmt(last.resources) + ' resources. ' : '';
    btn.setAttribute('data-confirm-msg', unit + fmt(last.users) + ' people (' + fmt(last.device_users) + ' on Android) will get this.' + later);
  }
  function show(d) {
    last = d;
    $('cUsers').textContent = fmt(d.users);
    $('cApp').textContent = fmt(d.device_users);
    $('cInbox').textContent = fmt(d.inbox_only);
    $('cClasses').innerHTML = (d.classes || []).map(function (c) {
      return '<div class="pn-meter-row"><span>' + esc(c.label) + '</span><b>' + fmt(c.count) + '</b></div>';
    }).join('');
    if (mode === 'unnotified') {
      $('cResources').textContent = fmt(d.resources);
      $('cSingles').textContent = fmt(d.singles);
      sample = d.sample || null;
      mirror();
    }
    confirmText();
  }
  function refresh() {
    var my = ++seq;
    fetch(form.dataset.countUrl + '?' + query().toString(), { credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(function (r) { return r.json(); })
      .then(function (d) { if (my === seq) show(d); })
      .catch(function () { /* keep the numbers we have */ });
  }
  function later() { clearTimeout(timer); timer = setTimeout(refresh, 250); }

  form.querySelectorAll('input[name="mode"]').forEach(function (r) {
    r.addEventListener('change', function () { applyMode(); refresh(); });
  });
  names.forEach(function (n) {
    var el = form.elements[n];
    if (!el) return;
    var list = el.length ? Array.prototype.slice.call(el) : [el];
    list.forEach(function (x) { x.addEventListener('input', later); x.addEventListener('change', later); });
  });
  $('send_at').addEventListener('change', confirmText);
  last = {
    users: parseInt($('cUsers').textContent.replace(/,/g, ''), 10) || 0,
    device_users: parseInt($('cApp').textContent.replace(/,/g, ''), 10) || 0,
    resources: parseInt($('cResources').textContent.replace(/,/g, ''), 10) || 0
  };
  applyMode();
  if (mode === 'unnotified') refresh();
  confirmText();
})();
