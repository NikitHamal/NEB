(function () {
  'use strict';
  /* Drag-to-reorder for the composer's photo strip and attachment list.
     Pointer events, so mouse, pen and touch behave the same. The list is rebuilt by its owner after each move, so
     everything listens on the container. Keyboard: focus an item, then Arrow keys (or Alt+Arrow) move it.

       NebSortable(container, { item: '.x', handle: '.grip' (optional), onMove: function (from, to) {} })

     While dragging, the other items slide to where they would land (transform only); nothing is reordered in the
     DOM until the pointer is released. */
  var THRESHOLD = 6;

  function sortable(container, opts) {
    if (!container || container.__sortable) return;
    container.__sortable = true;
    var itemSel = opts.item;
    var drag = null;

    function items() { return Array.prototype.slice.call(container.querySelectorAll(itemSel)); }

    function down(e) {
      if (e.button != null && e.button !== 0) return;
      var item = e.target.closest(itemSel);
      if (!item || !container.contains(item) || item.hasAttribute('data-fixed')) return;
      if (opts.handle) { if (!e.target.closest(opts.handle)) return; }
      else if (e.target.closest('button, a, input')) return;
      var list = items();
      drag = {
        item: item, from: list.indexOf(item), to: list.indexOf(item), id: e.pointerId, list: list,
        rects: list.map(function (n) { return n.getBoundingClientRect(); }),
        x: e.clientX, y: e.clientY, live: false
      };
      window.addEventListener('pointermove', move);
      window.addEventListener('pointerup', up);
      window.addEventListener('pointercancel', cancel);
    }

    function begin() {
      drag.live = true;
      drag.item.classList.add('is-dragging');
      container.classList.add('is-sorting');
      drag.list.forEach(function (n) { if (n !== drag.item) n.style.transition = 'transform .28s cubic-bezier(.2,.8,.2,1)'; });
      try { drag.item.setPointerCapture(drag.id); } catch (_) {}
    }

    function target(cx, cy) {
      var best = drag.from, bestD = Infinity;
      drag.rects.forEach(function (r, i) {
        var d = Math.pow(cx - (r.left + r.width / 2), 2) + Math.pow(cy - (r.top + r.height / 2), 2);
        if (d < bestD) { bestD = d; best = i; }
      });
      return best;
    }

    function place(to) {
      var from = drag.from;
      drag.list.forEach(function (n, i) {
        if (n === drag.item) return;
        var at = i;
        if (from < to && i > from && i <= to) at = i - 1;
        else if (from > to && i >= to && i < from) at = i + 1;
        var a = drag.rects[i], b = drag.rects[at];
        n.style.transform = at === i ? '' : 'translate(' + (b.left - a.left) + 'px,' + (b.top - a.top) + 'px)';
      });
    }

    function move(e) {
      if (!drag || e.pointerId !== drag.id) return;
      var dx = e.clientX - drag.x, dy = e.clientY - drag.y;
      if (!drag.live) {
        if (Math.abs(dx) + Math.abs(dy) < THRESHOLD) return;
        begin();
      }
      e.preventDefault();
      drag.item.style.transform = 'translate(' + dx + 'px,' + dy + 'px) scale(1.04)';
      var r = drag.rects[drag.from];
      var to = target(r.left + r.width / 2 + dx, r.top + r.height / 2 + dy);
      if (to !== drag.to) { drag.to = to; place(to); }
    }

    function finish() {
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', up);
      window.removeEventListener('pointercancel', cancel);
      container.classList.remove('is-sorting');
      if (drag) {
        drag.list.forEach(function (n) { n.style.transform = ''; n.style.transition = ''; n.classList.remove('is-dragging'); });
      }
    }

    function up(e) {
      if (!drag || e.pointerId !== drag.id) return;
      var d = drag; finish(); drag = null;
      if (d.live) {
        var swallow = function (ev) { ev.stopPropagation(); ev.preventDefault(); };
        container.addEventListener('click', swallow, { capture: true, once: true });
        setTimeout(function () { container.removeEventListener('click', swallow, true); }, 0);
        if (d.to !== d.from) opts.onMove(d.from, d.to);
      }
    }

    function cancel() { finish(); drag = null; }

    container.addEventListener('pointerdown', down);
    container.addEventListener('dragstart', function (e) { e.preventDefault(); });

    container.addEventListener('keydown', function (e) {
      var item = e.target.closest(itemSel);
      if (!item || e.target !== item) return;
      var dir = (e.key === 'ArrowLeft' || e.key === 'ArrowUp') ? -1 : (e.key === 'ArrowRight' || e.key === 'ArrowDown') ? 1 : 0;
      if (!dir) return;
      var list = items(), from = list.indexOf(item), to = from + dir;
      if (to < 0 || to >= list.length) return;
      e.preventDefault();
      opts.onMove(from, to);
      var again = items()[to];
      if (again) again.focus();
    });
  }

  window.NebSortable = sortable;
})();
