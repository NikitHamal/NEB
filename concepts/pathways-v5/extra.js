/* Pathways v5 extras: keyboard activation for card buttons, header state on scroll. */
(function () {
  'use strict';
  var V = window.V, D = document;
  D.addEventListener('keydown', function (e) {
    if ((e.key === 'Enter' || e.key === ' ') && e.target.matches && e.target.matches('[tabindex="0"][data-go],[tabindex="0"][data-act]')) { e.preventDefault(); e.target.click(); }
  });
  window.addEventListener('scroll', function () { D.body.classList.toggle('scrolled', window.scrollY > 8); }, { passive: true });
})();
