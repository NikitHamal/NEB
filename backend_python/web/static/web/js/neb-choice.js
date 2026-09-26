/* NebChoiceSheet + NebSelectField, ported.
 *
 * A form field that shows what you chose, and a sheet full of chips that is
 * how you choose it. On Android these are two composables and the screen wires
 * them together; on the web the wiring is here, so a page declares the pair in
 * markup and never writes a picker again.
 *
 * The contract is one hidden input. It holds the answer as a comma-separated
 * list, which is what the upload form already posts and what the app's
 * asCsvList() already reads, so nothing on the server changes:
 *
 *   <input type="hidden" name="subject" id="subject-value" value="Physics, Maths">
 *
 *   <button type="button" class="neb-select-field" id="subjectField"
 *           data-neb-choice="subjectSheet"
 *           data-placeholder="Choose one or more">
 *     <span class="neb-select-field-tile">...</span>
 *     <span class="neb-select-field-text">
 *       <span class="neb-select-field-label">Subject</span>
 *     </span>
 *     <span class="material-symbols-outlined">chevron_right</span>
 *   </button>
 *
 *   <div class="neb-scrim neb-scrim-bottom" id="subjectSheet" data-neb-close hidden
 *        data-choice-input="subject-value" data-choice-field="subjectField"
 *        data-choice-multi data-choice-custom="Add your own">
 *     <div class="neb-sheet neb-choice-sheet"> ... </div>
 *   </div>
 *
 * The sheet's own chrome is .neb-sheet's -- scrim, handle, head, drag to
 * dismiss, Escape, focus trap and scroll lock all belong to NebUI and none of
 * it is repeated here. What this file adds is the selection: which chips are
 * on, what the search hides, what "Add" does with a word that is not on the
 * list, and writing the answer back to the input and the field.
 *
 * Single-select confirms on tap and closes, exactly as the app does; multi
 * keeps the sheet open and commits on Done, so a wrong tap costs one more tap
 * and not the whole answer.
 */
(function () {
  'use strict';

  /* The app shows the search only when the list is long enough to need one.
     Below this a search box above six chips is furniture. */
  var SEARCH_MIN = 10;
  /* NebSelectField draws six pills and counts the rest. Past six the row is
     taller than the thing it is on a form to summarise. */
  var PILL_MAX = 6;

  function csv(value) {
    return (value || '').split(',').map(function (s) { return s.trim(); })
      .filter(function (s) { return s; });
  }

  function same(a, b) { return a.toLowerCase() === b.toLowerCase(); }

  function has(list, value) {
    return list.some(function (s) { return same(s, value); });
  }

  /* ── The field ───────────────────────────────────────────────────────────
     Redrawn from the answer every time it changes, because the answer is the
     only state -- there is nothing to keep in sync and so nothing that can
     drift. */
  function paint(field, values) {
    if (!field) return;
    var text = field.querySelector('.neb-select-field-text');
    if (!text) return;

    var hint = text.querySelector('.neb-select-field-placeholder');
    var bank = text.querySelector('.neb-select-field-values');
    if (!bank) {
      bank = document.createElement('span');
      bank.className = 'neb-select-field-values';
      text.appendChild(bank);
    }
    bank.textContent = '';

    if (!values.length) {
      if (!hint) {
        hint = document.createElement('span');
        hint.className = 'neb-select-field-placeholder';
        text.appendChild(hint);
      }
      hint.textContent = field.dataset.placeholder || 'Select';
      hint.hidden = false;
      return;
    }
    if (hint) hint.hidden = true;

    values.slice(0, PILL_MAX).forEach(function (value) {
      var pill = document.createElement('span');
      pill.className = 'neb-value-pill';
      pill.textContent = value;
      bank.appendChild(pill);
    });
    if (values.length > PILL_MAX) {
      var more = document.createElement('span');
      more.className = 'neb-value-pill';
      more.textContent = '+' + (values.length - PILL_MAX);
      bank.appendChild(more);
    }
  }

  /* ── The sheet ───────────────────────────────────────────────────────── */
  function chipFor(value) {
    var chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'neb-choice-chip';
    chip.setAttribute('aria-pressed', 'false');
    chip.dataset.value = value;

    var tick = document.createElement('span');
    tick.className = 'neb-chip-tick';
    tick.setAttribute('aria-hidden', 'true');
    chip.appendChild(tick);
    chip.appendChild(document.createTextNode(value));
    return chip;
  }

  function attach(scrim) {
    if (scrim.__nebChoice) return;
    scrim.__nebChoice = true;

    var input = document.getElementById(scrim.dataset.choiceInput || '');
    var field = document.getElementById(scrim.dataset.choiceField || '');
    var multi = scrim.hasAttribute('data-choice-multi');
    var options = scrim.querySelector('[data-choice-options]');
    var search = scrim.querySelector('[data-choice-search]');
    var addRow = scrim.querySelector('[data-choice-add]');
    var addField = addRow && addRow.querySelector('input');
    var addBtn = addRow && addRow.querySelector('button');
    var clearBtn = scrim.querySelector('[data-choice-clear]');
    var doneBtn = scrim.querySelector('[data-choice-done]');
    var empty = scrim.querySelector('[data-choice-empty]');
    if (!input || !options) return;

    /* What the sheet is editing. Committed to the input on Done, or straight
       away when there is only one answer to give. */
    var picked = [];

    function chips() {
      return Array.prototype.slice.call(options.querySelectorAll('.neb-choice-chip'));
    }

    function commit() {
      input.value = picked.join(', ');
      paint(field, picked);
      input.dispatchEvent(new CustomEvent('change', { bubbles: true }));
      scrim.dispatchEvent(new CustomEvent('neb:change', {
        bubbles: true, detail: { values: picked.slice() }
      }));
    }

    function mark() {
      chips().forEach(function (chip) {
        chip.setAttribute('aria-pressed', has(picked, chip.dataset.value) ? 'true' : 'false');
      });
      if (clearBtn) clearBtn.disabled = !picked.length;
      if (doneBtn) {
        doneBtn.textContent = picked.length ? 'Done (' + picked.length + ')' : 'Done';
      }
    }

    /* The app filters a list it rebuilds; here the chips are already in the
       DOM, so hiding is both cheaper and keeps a chip's selected state across
       a search the user then clears. */
    function filter() {
      var q = search ? search.value.trim().toLowerCase() : '';
      var shown = 0;
      chips().forEach(function (chip) {
        var hit = !q || chip.dataset.value.toLowerCase().indexOf(q) >= 0;
        /* A chosen answer stays visible whatever the search says, so Done
           never commits something the user cannot see. */
        if (!hit && has(picked, chip.dataset.value)) hit = true;
        chip.hidden = !hit;
        if (hit) shown++;
      });
      if (empty) {
        empty.hidden = shown > 0;
        if (!shown) empty.textContent = q ? 'Nothing matches “' + q + '”.' : 'Nothing to choose from yet.';
      }
    }

    function choose(value) {
      if (!multi) {
        picked = [value];
        mark();
        commit();
        NebUI.close(scrim);
        return;
      }
      picked = has(picked, value)
        ? picked.filter(function (s) { return !same(s, value); })
        : picked.concat([value]);
      mark();
    }

    function addCustom() {
      if (!addField) return;
      var value = addField.value.trim();
      if (!value) return;
      addField.value = '';
      if (addBtn) addBtn.disabled = true;

      /* A word that is not on the list becomes one, so it can be unchosen
         again without retyping it. */
      if (!chips().some(function (c) { return same(c.dataset.value, value); })) {
        options.appendChild(chipFor(value));
      }
      if (!multi) {
        picked = [value];
        mark();
        commit();
        NebUI.close(scrim);
        return;
      }
      if (!has(picked, value)) picked = picked.concat([value]);
      if (search) search.value = '';
      filter();
      mark();
    }

    options.addEventListener('click', function (e) {
      var chip = e.target.closest ? e.target.closest('.neb-choice-chip') : null;
      if (chip && options.contains(chip)) choose(chip.dataset.value);
    });

    if (search) {
      search.addEventListener('input', filter);
      /* Escape inside the search clears it rather than closing the sheet --
         the sheet is still the thing the user wants. */
      search.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && search.value) { e.stopPropagation(); search.value = ''; filter(); }
        if (e.key === 'Enter') e.preventDefault();
      });
    }
    if (addField) {
      addField.addEventListener('input', function () {
        if (addBtn) addBtn.disabled = !addField.value.trim();
      });
      addField.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') { e.preventDefault(); addCustom(); }
      });
    }
    if (addBtn) addBtn.addEventListener('click', addCustom);
    if (clearBtn) clearBtn.addEventListener('click', function () { picked = []; mark(); });
    if (doneBtn) {
      doneBtn.addEventListener('click', function () { commit(); NebUI.close(scrim); });
    }

    /* Opening starts from the input, not from whatever the last visit left
       behind, so dismissing the sheet really does discard the edit. */
    scrim.addEventListener('neb:open', function () {
      picked = csv(input.value);
      if (search) search.value = '';
      if (addField) addField.value = '';
      if (addBtn) addBtn.disabled = true;
      mark();
      filter();
    });

    /* The search earns its place or it is not shown at all. */
    var count = chips().length;
    if (search && count < SEARCH_MIN) {
      var wrap = search.closest('.neb-field-search');
      if (wrap) wrap.hidden = true;
    }
    if (doneBtn && !multi) {
      var foot = doneBtn.closest('.neb-sheet-foot');
      if (foot) foot.hidden = true;
    }

    /* The field is server-rendered empty; the answer it shows is whatever the
       input arrived holding, which is also what a failed form post returns. */
    paint(field, csv(input.value));
    mark();
    filter();
  }

  function scan(root) {
    var scope = root || document;
    var all = scope.querySelectorAll ? scope.querySelectorAll('[data-choice-input]') : [];
    Array.prototype.forEach.call(all, attach);
    if (scope.matches && scope.matches('[data-choice-input]')) attach(scope);
  }

  document.addEventListener('DOMContentLoaded', function () { scan(document); });
  if (document.readyState !== 'loading') scan(document);
  document.addEventListener('htmx:load', function (e) { scan(e.target); });

  window.NebChoice = { scan: scan, paint: paint };
})();
