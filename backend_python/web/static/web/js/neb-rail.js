/* NebTabRail's travelling container.
 *
 * The CSS can draw the rail, the tabs, the counts and the pill; what it cannot
 * do is know where the selected tab is. That needs measurement, so it happens
 * here -- and only here. Everything else about the component, including how it
 * looks with this file missing, is in material3/09-overlays.css.
 *
 * The contract is one attribute: aria-selected="true" on exactly one
 * .neb-rail-item. Set it however the page already sets it -- a click handler, a
 * server round trip, htmx swapping the rail out -- and the container follows.
 * Nothing here decides which tab is selected, which is what lets rails that
 * navigate (links) and rails that switch panels (buttons) share one controller.
 */
(function () {
  'use strict';

  var SCROLL_MARGIN = 28;  // NebTabRail's margin, in px.

  function indicatorOf(rail) {
    var ind = rail.querySelector(':scope > .neb-rail-ind');
    if (!ind) {
      ind = document.createElement('span');
      ind.className = 'neb-rail-ind';
      ind.setAttribute('aria-hidden', 'true');
      rail.insertBefore(ind, rail.firstChild);
    }
    return ind;
  }

  function place(rail, animate) {
    var item = rail.querySelector('.neb-rail-item[aria-selected="true"]');
    var ind = indicatorOf(rail);
    if (!item) { ind.removeAttribute('data-placed'); return; }

    /* offsetLeft is relative to the rail's padding box and unaffected by its
       scroll position, which is exactly what a container inside the scroller
       needs -- getBoundingClientRect would have to be corrected for scrollLeft
       and would be wrong for one frame after every flick. */
    var left = item.offsetLeft;
    var top = item.offsetTop;
    if (!item.offsetWidth) return;  // display:none, or not laid out yet.

    ind.style.width = item.offsetWidth + 'px';
    ind.style.height = item.offsetHeight + 'px';
    ind.style.transform = 'translate(' + left + 'px,' + top + 'px)';
    ind.setAttribute('data-placed', animate ? 'yes' : 'first');
    if (!animate) {
      /* Commit the jump before re-enabling the transition, or the browser
         coalesces both writes and the container slides anyway. */
      void ind.offsetWidth;
      requestAnimationFrame(function () { ind.setAttribute('data-placed', 'yes'); });
    }
    rail.setAttribute('data-rail-ready', '');
    keepVisible(rail, item);
  }

  /* The app scrolls the selected tab back into view with a 28px margin, so a
     selection made with the keyboard at the end of a long rail is not left
     flush against the edge where it looks clipped. */
  function keepVisible(rail, item) {
    if (rail.scrollWidth <= rail.clientWidth) return;
    var start = item.offsetLeft - SCROLL_MARGIN;
    var end = item.offsetLeft + item.offsetWidth + SCROLL_MARGIN;
    if (start < rail.scrollLeft) rail.scrollLeft = Math.max(0, start);
    else if (end > rail.scrollLeft + rail.clientWidth) rail.scrollLeft = end - rail.clientWidth;
  }

  function attach(rail) {
    if (rail.__nebRail) return;
    rail.__nebRail = true;

    /* aria-selected is set by the page, not by this file, so the only way to
       hear about it is to watch. One observer per rail, attributes only. */
    new MutationObserver(function () { place(rail, true); }).observe(rail, {
      attributes: true, attributeFilter: ['aria-selected'], subtree: true
    });

    if (window.ResizeObserver) {
      /* A rail reflows when the window changes, when a font finally loads, and
         when a count goes from 9 to 10. All three move the tabs; none of them
         fire a mutation. */
      new ResizeObserver(function () { place(rail, false); }).observe(rail);
    }
    place(rail, false);
  }

  function scan(root) {
    (root || document).querySelectorAll('.neb-rail').forEach(attach);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { scan(); });
  } else {
    scan();
  }
  /* htmx swaps whole panels in; a rail that arrives that way gets a controller
     too. */
  document.body && document.addEventListener('htmx:afterSwap', function (e) {
    scan(e.target);
  });
  /* Fonts land after first paint and every label changes width when they do. */
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () {
      document.querySelectorAll('.neb-rail').forEach(function (r) { place(r, false); });
    });
  }

  window.NebRail = { scan: scan, place: place };
})();
