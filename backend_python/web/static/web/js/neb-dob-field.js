/* Date of birth: the wheel commits on "Set date", not on every scroll (the wheel emits a value
   each time a column settles, so wiring it straight to the field would make Cancel a lie).
   Markup: components/_dob_field.html + _dob_sheet.html. The field fires a bubbling `change`. */
(function () {
  'use strict';
  var trigger = document.getElementById('dob-trigger');
  var display = document.getElementById('dob-display');
  var field = document.getElementById('dob');
  var wheel = document.getElementById('dob-wheel');
  var confirmBtn = document.getElementById('dob-confirm');
  var sheet = document.getElementById('dob-sheet');
  if (!trigger || !wheel || !confirmBtn || !sheet || !field) return;

  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function pretty(iso) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || '');
    return m ? parseInt(m[3], 10) + ' ' + MONTHS[parseInt(m[2], 10) - 1] + ' ' + m[1] : '';
  }
  function paint() {
    if (!field.value) return;
    display.textContent = pretty(field.value) || field.value;
    display.classList.remove('neb-field-trigger-placeholder');
  }

  /* Reopening shows the date in the field, not wherever the wheel was left when cancelled. */
  sheet.addEventListener('neb:open', function () {
    var handle = window.NebUI && window.NebUI.wheel(wheel);
    if (handle && field.value) handle.set(field.value);
  });
  confirmBtn.addEventListener('click', function () {
    var iso = wheel.dataset.value || '';
    if (iso) {
      field.value = iso;
      paint();
      field.dispatchEvent(new Event('change', { bubbles: true }));
    }
    window.NebUI.close(sheet);
  });
  /* A caller that sets the value from script (the welcome flow) asks for a repaint. */
  field.addEventListener('neb:sync', paint);
  paint();
})();
