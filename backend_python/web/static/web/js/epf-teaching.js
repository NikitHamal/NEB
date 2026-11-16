/* Profile editor, teacher block: levels (many), type of work (one). Chips come from the catalogue
   the page already embeds; the hidden inputs the form posts follow the taps. */
(function () {
  'use strict';
  var bootEl = document.getElementById('epf-boot');
  var levelsBox = document.getElementById('teach-levels');
  var workBox = document.getElementById('employment-chips');
  if (!bootEl || !levelsBox || !workBox) return;
  var cat = JSON.parse(bootEl.textContent).catalog || {};
  var form = document.querySelector('.epf-form');
  var levelsIn = document.getElementById('teach-levels-hidden');
  var workIn = document.getElementById('employment-hidden');
  var picked = (levelsIn.value || '').split(',').filter(Boolean);

  function ping() { if (form) form.dispatchEvent(new Event('change', { bubbles: true })); }
  function build(box, list, on) {
    var frag = document.createDocumentFragment();
    list.forEach(function (o) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'md-chip'; b.dataset.v = o.value; b.textContent = o.label;
      on(b, o.value); frag.appendChild(b);
    });
    box.appendChild(frag);
  }
  function paintLevels() {
    levelsBox.querySelectorAll('.md-chip').forEach(function (b) {
      var on = picked.indexOf(b.dataset.v) > -1;
      b.classList.toggle('md-chip-active', on); b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    levelsIn.value = picked.join(',');
  }
  function paintWork() {
    workBox.querySelectorAll('.md-chip').forEach(function (b) {
      var on = b.dataset.v === workIn.value;
      b.classList.toggle('md-chip-active', on); b.setAttribute('aria-checked', on ? 'true' : 'false');
    });
  }
  build(levelsBox, cat.teachLevels || [], function () {});
  build(workBox, cat.employment || [], function () {});
  levelsBox.addEventListener('click', function (e) {
    var b = e.target.closest('.md-chip'); if (!b) return;
    var i = picked.indexOf(b.dataset.v);
    if (i > -1) picked.splice(i, 1); else picked.push(b.dataset.v);
    paintLevels(); ping();
  });
  workBox.addEventListener('click', function (e) {
    var b = e.target.closest('.md-chip'); if (!b) return;
    workIn.value = workIn.value === b.dataset.v ? '' : b.dataset.v;  // tap again to clear
    paintWork(); ping();
  });
  paintLevels(); paintWork();
})();
