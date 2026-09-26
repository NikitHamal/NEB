/* The travelling container, for the two components that have one.
 *
 * NebTabRail marks the selected tab with a pill and NebSegmentedChoice marks
 * the chosen segment with one, and in both the mark slides between answers
 * rather than fading out in one place and in again in another. The CSS can
 * draw everything else about either component -- and does, in
 * material3/09-overlays.css -- but it cannot know where the selected child is.
 * That needs measurement, so it happens here, once, for both.
 *
 * The contract is one attribute on exactly one child:
 *
 *   .neb-rail       .neb-rail-item[aria-selected="true"]
 *   .neb-segmented  .neb-segment[aria-pressed="true"]
 *
 * Set it however the page already sets it -- a click handler, a server round
 * trip, htmx swapping the panel out -- and the container follows. Nothing here
 * decides which child is selected, which is what lets rails that navigate
 * (links), rails that switch panels (buttons) and segmented banks that answer
 * a question all share one controller.
 */
(function () {
  'use strict';

  var SCROLL_MARGIN = 28;  // NebTabRail's margin, in px.

  /* What each component calls its parts, and whether it scrolls. A rail is a
     scroller with a selected tab somewhere in it; a bank is two to four
     segments that always fit. */
  var KINDS = [
    { root: '.neb-rail', item: '.neb-rail-item', ind: 'neb-rail-ind',
      state: 'aria-selected', scrolls: true },
    { root: '.neb-segmented', item: '.neb-segment', ind: 'neb-segmented-ind',
      state: 'aria-pressed', scrolls: false }
  ];
  var ROOTS = KINDS.map(function (k) { return k.root; }).join(',');

  function kindOf(rail) {
    for (var i = 0; i < KINDS.length; i++) {
      if (rail.matches(KINDS[i].root)) return KINDS[i];
    }
    return KINDS[0];
  }

  function indicatorOf(rail, kind) {
    var ind = rail.querySelector(':scope > .' + kind.ind);
    if (!ind) {
      ind = document.createElement('span');
      ind.className = kind.ind;
      ind.setAttribute('aria-hidden', 'true');
      rail.insertBefore(ind, rail.firstChild);
    }
    return ind;
  }

  function place(rail, animate) {
    var kind = kindOf(rail);
    var item = rail.querySelector(kind.item + '[' + kind.state + '="true"]');
    var ind = indicatorOf(rail, kind);
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
    if (kind.scrolls) keepVisible(rail, item);
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

    /* The state attribute is set by the page, not by this file, so the only
       way to hear about it is to watch. One observer per rail, attributes
       only. */
    new MutationObserver(function () { place(rail, true); }).observe(rail, {
      attributes: true, attributeFilter: [kindOf(rail).state], subtree: true
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
    (root || document).querySelectorAll(ROOTS).forEach(attach);
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
      document.querySelectorAll(ROOTS).forEach(function (r) { place(r, false); });
    });
  }

  window.NebRail = { scan: scan, place: place };
})();
