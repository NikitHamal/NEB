/* Reply boxes that grow with what you type, and shrink back when there is less.
   A fixed-height textarea grows a native scrollbar after two lines, which turns a two-second reply into a
   scrolling window; the field takes the height of its content instead, up to a cap, and only then scrolls.

   The floor comes from the CSS custom property --ah-min on the field (the writing tools raise it while open),
   so opening, closing, clearing or sending are all the same measurement: window.NebGrow(el) re-reads the
   content and the floor and moves the height there. Height is the only thing that animates.

   Listened for on the document, because composers are also built after load. */
(function () {
  'use strict';

  var DEFAULT_MAX = 240;

  function field(el) {
    return el && el.tagName === 'TEXTAREA' && el.hasAttribute('data-autoheight') ? el : null;
  }

  function floorOf(el) {
    var v = parseFloat(getComputedStyle(el).getPropertyValue('--ah-min'));
    return isNaN(v) ? 0 : v;
  }

  function grow(el) {
    /* A hidden field reports scrollHeight 0, and writing that back leaves it collapsed when its sheet opens.
       Measure only what the browser can lay out. */
    if (!el.offsetParent) return;
    var max = parseFloat(el.getAttribute('data-autoheight-max')) || DEFAULT_MAX;
    var from = el.offsetHeight;
    el.style.height = 'auto';
    var want = el.scrollHeight;
    var to = Math.round(Math.min(Math.max(want, floorOf(el)), Math.max(max, floorOf(el))));
    if (from && from !== to) {
      el.style.height = from + 'px';
      void el.offsetHeight;
    }
    el.style.height = to + 'px';
    el.classList.toggle('is-scrolling', want > to + 1);
  }

  document.addEventListener('input', function (e) {
    var el = field(e.target);
    if (el) grow(el);
  });

  document.addEventListener('focusin', function (e) {
    var el = field(e.target);
    if (el) grow(el);
  });

  window.addEventListener('resize', function () {
    document.querySelectorAll('textarea[data-autoheight]').forEach(grow);
  });

  window.NebGrow = function (el) { if (field(el)) grow(el); };

  document.querySelectorAll('textarea[data-autoheight]').forEach(grow);
})();
