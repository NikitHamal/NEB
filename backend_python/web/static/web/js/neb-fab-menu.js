/* NebFabMenu's stagger, scrim and focus.
 *
 * The CSS draws the pills, the scrim and the spin; what it cannot express is
 * the 40ms stagger, which runs bottom-up on open and top-down on close so the
 * row nearest the thumb is the first to arrive and the last to leave. That is
 * a per-item delay computed from the item's position, so it is set here.
 *
 * One menu per page. The markup is the contract:
 *
 *   <div class="neb-fab-menu" id="createMenu">
 *     <div class="neb-fab-menu-items">... .neb-fab-pill ...</div>
 *     <button class="md-fab" data-neb-fab-toggle>...</button>
 *   </div>
 *   <div class="neb-fab-scrim" data-neb-fab-scrim></div>
 */
(function () {
  'use strict';

  var STEP = 40;  // StaggerStepMillis.

  function reduced() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function stagger(menu, open) {
    var pills = Array.prototype.slice.call(menu.querySelectorAll('.neb-fab-pill'));
    var step = reduced() ? 0 : STEP;
    pills.forEach(function (pill, i) {
      /* Opening runs the list backwards -- the last pill is the one closest to
         the button, and it should move first. */
      var order = open ? (pills.length - 1 - i) : i;
      pill.style.transitionDelay = (order * step) + 'ms';
    });
  }

  function setOpen(menu, scrim, fab, open) {
    stagger(menu, open);
    if (open) {
      menu.setAttribute('data-open', '');
      if (scrim) scrim.setAttribute('data-open', '');
    } else {
      menu.removeAttribute('data-open');
      if (scrim) scrim.removeAttribute('data-open');
    }
    fab.setAttribute('aria-expanded', open ? 'true' : 'false');
    /* A closed pill is invisible and untouchable; it must also be unreachable
       by Tab, which pointer-events cannot do. */
    menu.querySelectorAll('.neb-fab-pill').forEach(function (p) {
      if (open) p.removeAttribute('tabindex');
      else p.setAttribute('tabindex', '-1');
    });
    if (open) {
      var first = menu.querySelector('.neb-fab-pill');
      if (first) first.focus({ preventScroll: true });
    }
  }

  function attach(menu) {
    var fab = menu.querySelector('[data-neb-fab-toggle]');
    if (!fab) return;
    var scrim = document.querySelector('[data-neb-fab-scrim]');

    setOpen(menu, scrim, fab, false);

    fab.addEventListener('click', function (e) {
      e.preventDefault();
      setOpen(menu, scrim, fab, !menu.hasAttribute('data-open'));
    });
    if (scrim) scrim.addEventListener('click', function () {
      setOpen(menu, scrim, fab, false);
      fab.focus({ preventScroll: true });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || !menu.hasAttribute('data-open')) return;
      setOpen(menu, scrim, fab, false);
      fab.focus({ preventScroll: true });
    });
    /* Every pill navigates, so the menu does not have to close itself -- the
       page is leaving. It closes anyway, because a back-button return from a
       bfcache-restored page would otherwise show it still open. */
    menu.addEventListener('click', function (e) {
      if (e.target.closest('.neb-fab-pill')) setOpen(menu, scrim, fab, false);
    });
    window.addEventListener('pageshow', function () {
      setOpen(menu, scrim, fab, false);
    });
  }

  function scan() {
    document.querySelectorAll('.neb-fab-menu').forEach(attach);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scan);
  } else {
    scan();
  }
})();
