/* Profile cover picker: the dialog lists the M3X art library covers (v7); a tap saves and swaps the cover in place. */
(function () {
  'use strict';
  var dlg = document.getElementById('coverPicker');
  if (!dlg) return;
  function csrf() { var m = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/); return m ? decodeURIComponent(m[1]) : ''; }
  function apply(id) {
    var art = document.querySelector('.pf-banner-art');
    if (!art) return;
    art.setAttribute('data-neb-cover', id);
    var imgs = art.querySelectorAll('img');
    for (var i = 0; i < imgs.length; i++) {
      var dark = imgs[i].classList.contains('neb-pixel-night');
      imgs[i].src = imgs[i].src.replace(/cover\/(light|dark)\/[^/]+$/, 'cover/' + (dark ? 'dark' : 'light') + '/' + id + '.webp');
    }
  }
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
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (t.closest('[data-action="open-cover-picker"]')) { dlg.showModal(); var on = dlg.querySelector('.is-on'); if (on) on.scrollIntoView({ block: 'center' }); return; }
    if (!dlg.open) return;
    if (t === dlg || t.closest('[data-cv-close]')) { dlg.close(); return; }
    if (t.closest('[data-cv-reset]')) { save('', t); return; }
    var pick = t.closest('.cv-pick'); if (pick) save(pick.getAttribute('data-cover'), pick);
  });
})();
