/* Admin push composer: live audience numbers, phone preview, counters, destination field. */
(function () {
  'use strict';
  var form = document.getElementById('pushForm');
  if (!form) return;
  var $ = function (id) { return document.getElementById(id); };
  var title = $('title'), body = $('body');
  var fmt = function (n) { return Number(n || 0).toLocaleString('en-US'); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };

  function mirror() {
    var tm = parseInt(form.dataset.titleMax, 10), bm = parseInt(form.dataset.bodyMax, 10);
    $('pvTitle').textContent = title.value.trim() || 'Title';
    $('pvBody').textContent = body.value.trim() || 'Your message appears here.';
    $('titleCount').textContent = title.value.length + '/' + tm;
    $('bodyCount').textContent = body.value.length + '/' + bm;
    $('titleCount').classList.toggle('is-over', title.value.length > tm);
    $('bodyCount').classList.toggle('is-over', body.value.length > bm);
  }
  title.addEventListener('input', mirror);
  body.addEventListener('input', mirror);
  mirror();

  function dest() {
    var v = (form.querySelector('input[name="dest"]:checked') || {}).value || 'none';
    var wrap = $('destIdWrap');
    wrap.hidden = !(v === 'resource' || v === 'post');
    $('dest_id').required = !wrap.hidden;
  }
  form.querySelectorAll('input[name="dest"]').forEach(function (r) { r.addEventListener('change', dest); });
  dest();

  var names = ['class_level', 'subject', 'role', 'device', 'active_days', 'inactive_days', 'joined_days', 'gender',
    'min_age', 'max_age', 'pradesh', 'district', 'school', 'usernames_or_ids'];
  var timer = null, seq = 0, last = { users: 0 };
  function query() {
    var p = new URLSearchParams();
    names.forEach(function (n) { var el = form.elements[n]; if (el && el.value.trim()) p.set(n, el.value.trim()); });
    p.set('count_only', '1');
    return p;
  }
  function confirmText() {
    var btn = $('sendBtn');
    var later = $('send_at').value ? ' It will go out at the time you picked.' : '';
    btn.setAttribute('data-confirm-msg', fmt(last.users) + ' people (' + fmt(last.device_users) + ' with the app) will get this.' + later);
  }
  function refresh() {
    var my = ++seq;
    fetch(form.dataset.countUrl + '?' + query().toString(), { credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (my !== seq) return;
        last = d;
        $('cUsers').textContent = fmt(d.users);
        $('cApp').textContent = fmt(d.device_users);
        $('cInbox').textContent = fmt(d.inbox_only);
        $('cClasses').innerHTML = (d.classes || []).map(function (c) {
          return '<div class="pn-meter-row"><span>' + esc(c.label) + '</span><b>' + fmt(c.count) + '</b></div>';
        }).join('');
        confirmText();
      }).catch(function () { /* keep the numbers we have */ });
  }
  function later() { clearTimeout(timer); timer = setTimeout(refresh, 250); }
  names.forEach(function (n) {
    var el = form.elements[n];
    if (el) { el.addEventListener('input', later); el.addEventListener('change', later); }
  });
  $('send_at').addEventListener('change', confirmText);
  last = { users: parseInt($('cUsers').textContent.replace(/,/g, ''), 10) || 0, device_users: parseInt($('cApp').textContent.replace(/,/g, ''), 10) || 0 };
  confirmText();
})();
