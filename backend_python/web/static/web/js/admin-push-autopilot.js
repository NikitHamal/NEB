/* Announce uploads by hand: pick resources, see what one-message-per-person means, then send. */
(function () {
  'use strict';
  var form = document.getElementById('announceForm');
  if (!form) return;
  var boxes = function () { return Array.prototype.slice.call(form.querySelectorAll('input[name="resource_ids"]')); };
  var btn = document.getElementById('announceBtn');
  var box = document.getElementById('previewBox');
  var fmt = function (n) { return Number(n || 0).toLocaleString('en-US'); };
  var timer = null, seq = 0;

  function csrf() { return (form.querySelector('input[name="csrfmiddlewaretoken"]') || {}).value || ''; }
  function picked() { return boxes().filter(function (b) { return b.checked; }).map(function (b) { return b.value; }); }

  function refresh() {
    var ids = picked();
    document.getElementById('pickCount').textContent = fmt(ids.length) + ' selected';
    btn.disabled = !ids.length;
    if (!ids.length) { box.style.display = 'none'; return; }
    var my = ++seq;
    fetch(form.dataset.previewUrl, {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify({ ids: ids })
    }).then(function (r) { return r.json(); }).then(function (d) {
      if (my !== seq) return;
      box.style.display = '';
      document.getElementById('pvPeople').textContent = fmt(d.people);
      document.getElementById('pvApp').textContent = fmt(d.devices_people);
      document.getElementById('pvSingles').textContent = fmt(d.would_send_as_singles);
      document.getElementById('pvSampleTitle').textContent = d.sample ? d.sample.title : 'Nobody matches these yet';
      document.getElementById('pvSampleBody').textContent = d.sample ? d.sample.body : '';
      btn.setAttribute('data-confirm-msg', fmt(d.people) + ' people get one message each for ' + fmt(d.resources) + ' resources.');
      btn.disabled = !d.people;
    }).catch(function () { /* keep what is on screen */ });
  }
  function later() { clearTimeout(timer); timer = setTimeout(refresh, 300); }

  form.addEventListener('change', function (e) { if (e.target.name === 'resource_ids') later(); });
  document.getElementById('pickAll') && document.getElementById('pickAll').addEventListener('click', function () {
    boxes().forEach(function (b) { b.checked = true; }); later();
  });
  document.getElementById('pickNone') && document.getElementById('pickNone').addEventListener('click', function () {
    boxes().forEach(function (b) { b.checked = false; }); later();
  });
})();
