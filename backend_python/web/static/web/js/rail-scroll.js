/* Horizontal rails say when there is more to see: a fade at the edge that still
   has content, and a button that steps one card at a time. Both are driven by
   three classes on .hf-rail-wrap -- is-scrollable, at-start, at-end -- which the
   CSS turns into visibility. */
(function () {
  'use strict';

  function reducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function cardStep(rail) {
    var card = rail.firstElementChild;
    if (!card) return rail.clientWidth * 0.8;
    var style = getComputedStyle(rail);
    var gap = parseFloat(style.columnGap || style.gap) || 0;
    return card.getBoundingClientRect().width + gap;
  }

  function sync(wrap, rail) {
    var max = Math.max(0, rail.scrollWidth - rail.clientWidth);
    var x = rail.scrollLeft;
    wrap.classList.toggle('is-scrollable', max > 4);
    wrap.classList.toggle('at-start', x <= 2);
    wrap.classList.toggle('at-end', x >= max - 2);
  }

  function init(wrap) {
    if (wrap._railNav) return;
    wrap._railNav = true;
    var rail = wrap.querySelector('.hf-rail');
    if (!rail) return;

    var buttons = { prev: wrap.querySelector('[data-rail-prev]'), next: wrap.querySelector('[data-rail-next]') };
    Object.keys(buttons).forEach(function (side) {
      var btn = buttons[side];
      if (!btn) return;
      btn.addEventListener('click', function () {
        var dir = side === 'prev' ? -1 : 1;
        rail.scrollBy({ left: dir * cardStep(rail), behavior: reducedMotion() ? 'auto' : 'smooth' });
      });
    });

    rail.addEventListener('scroll', function () { sync(wrap, rail); }, { passive: true });
    if ('ResizeObserver' in window) {
      new ResizeObserver(function () { sync(wrap, rail); }).observe(rail);
    } else {
      window.addEventListener('resize', function () { sync(wrap, rail); });
    }
    sync(wrap, rail);
  }

  function boot() {
    document.querySelectorAll('.hf-rail-wrap').forEach(init);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
