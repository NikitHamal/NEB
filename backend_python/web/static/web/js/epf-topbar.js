/* Edit profile: the sticky Back / Save bar turns solid once the page has scrolled past the cover. One passive listener, one class. */
(function () {
  'use strict';
  var bar = document.getElementById('epfTopbar');
  if (!bar) return;
  var cover = document.querySelector('.epf-cover');
  var ticking = false;
  function update() {
    ticking = false;
    var limit = cover ? Math.max(cover.offsetTop + cover.offsetHeight - bar.offsetHeight - 8, 40) : 40;
    bar.classList.toggle('is-stuck', window.scrollY > limit);
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  update();
})();
