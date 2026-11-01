/* Reply boxes that grow with what you type. A fixed-height textarea grows a
   native scrollbar after two lines, which turns a two-second reply into a
   scrolling window; the field takes the height of its content instead, up to a
   cap, and only then scrolls.

   Listened for on the document, because composers are also built after load --
   the inline reply on a resource comment would otherwise arrive unbound. */
(function () {
  'use strict';

  var DEFAULT_MAX = 240;

  function field(el) {
    return el && el.tagName === 'TEXTAREA' && el.hasAttribute('data-autoheight') ? el : null;
  }

  function grow(el) {
    /* A hidden field reports scrollHeight 0, and writing that back leaves it
       collapsed when its sheet opens. Measure only what the browser can lay
       out; focus is what makes the sheet's box measurable. */
    if (!el.offsetParent) return;
    var max = parseFloat(el.getAttribute('data-autoheight-max')) || DEFAULT_MAX;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, max) + 'px';
    el.classList.toggle('is-scrolling', el.scrollHeight > max);
  }

  document.addEventListener('input', function (e) {
    var el = field(e.target);
    if (el) grow(el);
  });

  document.addEventListener('focusin', function (e) {
    var el = field(e.target);
    if (el) grow(el);
  });

  document.querySelectorAll('textarea[data-autoheight]').forEach(grow);
})();
