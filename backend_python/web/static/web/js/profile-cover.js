/* Profile cover picker: the dialog lists the M3X art library covers (v7), drawn by code (js/m3x-art.js) as they scroll into
   view; a tap saves and swaps the cover in place. */
(function () {
  'use strict';
  var dlg = document.getElementById('coverPicker');
  if (!dlg) return;
  function csrf() { var m = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/); return m ? decodeURIComponent(m[1]) : ''; }
  function apply(id) {
    var art = document.querySelector('.pf-banner-art');
    if (!art || !window.NebM3x) return;
    art.setAttribute('data-neb-cover', id);
    var old = art.querySelector('svg'); if (old) old.remove();
    art.insertAdjacentHTML('afterbegin', window.NebM3x.cover(id || window.NebM3x.defaultCover(art.getAttribute('data-neb-user')), true));
  }
  // tiles are drawn by code as they scroll into view, so opening the picker never builds 175 drawings at once
  var io = null;
  function tiles() {
    if (!window.NebM3x || !('IntersectionObserver' in window)) {
      dlg.querySelectorAll('[data-m3x-tile]').forEach(function (t) { t.innerHTML = window.NebM3x ? window.NebM3x.cover(t.getAttribute('data-m3x-tile'), false) : ''; });
      return;
    }
    if (!io) io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var t = e.target; io.unobserve(t);
        t.innerHTML = window.NebM3x.cover(t.getAttribute('data-m3x-tile'), false);
      });
    }, { root: dlg.querySelector('.cv-grid'), rootMargin: '120px' });
    dlg.querySelectorAll('[data-m3x-tile]').forEach(function (t) { if (!t.firstChild) io.observe(t); });
  }
  function open() { dlg.showModal(); tiles(); var on = dlg.querySelector('.is-on'); if (on) on.scrollIntoView({ block: 'center' }); }
  function save(id, btn) {
    fetch(dlg.getAttribute('data-url'), { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify({ cover: id }) })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (!d.ok) return;
        apply(d.cover);
        var on = dlg.querySelector('.cv-pick.is-on'); if (on) on.classList.remove('is-on');
        var now = dlg.querySelector('[data-cover="' + d.cover + '"]'); if (now) now.classList.add('is-on');
        dlg.close();
      }).catch(function () {});
  }
  // Edit profile links here with ?cover=1
  if (/[?&]cover=1(&|$)/.test(location.search) && document.querySelector('[data-action="open-cover-picker"]')) {
    open();
    history.replaceState(null, '', location.pathname);
  }
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (t.closest('[data-action="open-cover-picker"]')) { open(); return; }
    if (!dlg.open) return;
    if (t === dlg || t.closest('[data-cv-close]')) { dlg.close(); return; }
    if (t.closest('[data-cv-reset]')) { save('', t); return; }
    var pick = t.closest('.cv-pick'); if (pick) save(pick.getAttribute('data-cover'), pick);
  });
})();
