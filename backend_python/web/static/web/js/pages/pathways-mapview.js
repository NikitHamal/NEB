/* Pathways: the Nepal map used on the Colleges page. Inline card plus a full view (dialog) with the same data.
   PW.map(counts, selected, onPick) returns {el, update(counts, selected)}. */
(function () {
  'use strict';
  var PW = window.PW, h = PW.h, icon = PW.icon;

  PW.map = function (counts, selected, onPick) {
    var cur = { c: counts || {}, d: selected || '' }, big = null;
    var openBtn = h('button', { class: 'pw-round sm', type: 'button', 'aria-label': 'Open full map' }, [icon('open_in_full')]);
    var inline = PW.mapCore({ counts: cur.c, selected: cur.d, onPick: onPick, extra: openBtn });
    openBtn.addEventListener('click', openFull);

    function openFull() {
      var from = document.activeElement, close = h('button', { class: 'pw-round', type: 'button', 'aria-label': 'Close map' }, [icon('close')]);
      var sub = h('p', { class: 'pw-geo-sub' });
      var legend = h('div', { class: 'pw-geo-legend', 'aria-hidden': 'true' }, [h('span', { text: 'Fewer' })].concat([0, 1, 2, 3, 4].map(function (i) { return h('i', { class: 'pw-dist pwl' + i }); }), [h('span', { text: 'More colleges' })]));
      var cta = h('button', { class: 'pw-btn', type: 'button', text: 'Show colleges' });
      var m = PW.mapCore({ full: true, counts: cur.c, selected: cur.d, onPick: function (n) { onPick(n); } });
      var ov = h('div', { class: 'pw-geo-ov pw-page', role: 'dialog', 'aria-modal': 'true', 'aria-label': 'Map of Nepal' }, [
        h('div', { class: 'pw-geo-bar' }, [h('div', {}, [h('b', { text: 'Nepal' }), sub]), close]), m.el, legend, cta,
      ]);
      function stat() {
        var n = 0, d = Object.keys(cur.c).length; Object.keys(cur.c).forEach(function (k) { n += cur.c[k]; });
        sub.textContent = n + ' colleges in ' + d + ' districts';
        cta.hidden = !cur.d; cta.textContent = cur.d ? 'Show colleges in ' + cur.d : '';
      }
      function shut() {
        document.removeEventListener('keydown', key); m.destroy(); big = null; ov.classList.add('out');
        document.documentElement.classList.remove('pw-lock');
        setTimeout(function () { ov.remove(); }, 160); if (from && from.focus) from.focus();
      }
      function key(e) { if (e.key === 'Escape') shut(); }
      close.addEventListener('click', shut); cta.addEventListener('click', shut); document.addEventListener('keydown', key);
      big = { m: m, stat: stat }; stat();
      document.documentElement.classList.add('pw-lock'); document.body.appendChild(ov); close.focus();
    }
    return {
      el: inline.el,
      update: function (c, d) { cur = { c: c || {}, d: d || '' }; inline.update(cur.c, cur.d); if (big) { big.m.update(cur.c, cur.d); big.stat(); } },
    };
  };
})();
