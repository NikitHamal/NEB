(function () {
  'use strict';
  /* Turns <select data-chips-for> style duration pickers into M3 filter chips. The select stays in the DOM as the
     source of truth so the composer's own submit code reads it unchanged. */
  function enhance(select) {
    if (select.__chips) return;
    var wrap = document.createElement('div');
    wrap.className = 'hf-chips';
    wrap.setAttribute('role', 'radiogroup');
    wrap.setAttribute('aria-label', 'Poll duration');
    var labels = { '0': 'No expiry', '86400000': '24h', '259200000': '3d', '604800000': '7d' };
    function paint() {
      Array.prototype.forEach.call(wrap.children, function (b) {
        b.setAttribute('aria-pressed', b.dataset.value === select.value ? 'true' : 'false');
      });
    }
    Array.prototype.forEach.call(select.options, function (o) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'hf-chip';
      b.dataset.value = o.value;
      b.textContent = labels[o.value] || o.textContent;
      b.title = o.textContent;
      b.addEventListener('click', function () {
        select.value = o.value;
        select.dispatchEvent(new Event('change', { bubbles: true }));
        paint();
      });
      wrap.appendChild(b);
    });
    select.parentNode.insertBefore(wrap, select);
    select.__chips = wrap;
    select.addEventListener('change', paint);
    paint();
  }
  function scan() {
    Array.prototype.forEach.call(document.querySelectorAll('.hf-poll-duration-select'), enhance);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', scan); else scan();
  document.addEventListener('htmx:load', scan);
})();
