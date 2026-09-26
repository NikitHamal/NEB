/* One controller for every overlay and every choice control on the web.
 *
 * The app has NebDialog, NebModalSheet, NebSheetSurface, NebPickerSheet,
 * NebDateWheel, NebFilterChip, NebSelectRow, NebOptionCard, NebToggleRow and
 * NebChoiceTiles. The web had none of them: it had 148 distinct overlay classes
 * across roughly thirty prefixes, each with its own open/close code, its own
 * escape handler, and mostly no focus handling at all. This is the other half of
 * material3/09-overlays.css -- the CSS gives them the app's geometry, this gives
 * them the app's behaviour, once, for all of them.
 *
 * Everything is delegated off document, so markup swapped in by htmx works with
 * no re-initialisation. The only exceptions are the date wheels, which need
 * their columns measured, and those are picked up on htmx:load.
 *
 * Markup, in full:
 *
 *   <button data-neb-open="pick-class">Class</button>
 *   <div class="neb-scrim" id="pick-class" hidden>
 *     <div class="neb-sheet" role="dialog" aria-modal="true" aria-label="Class">
 *       <div class="neb-sheet-handle"></div>
 *       ...
 *       <button data-neb-close>Cancel</button>
 *     </div>
 *   </div>
 *
 *   <button data-neb-menu="post-actions" aria-expanded="false">...</button>
 *   <div class="neb-menu" id="post-actions" role="menu" hidden>...</div>
 *
 * And from script:  NebUI.open(id) / NebUI.close(id) / await NebUI.confirm({...})
 */
(function () {
  'use strict';

  var FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),' +
    'select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';

  /* The stack, not a single "current overlay": a picker sheet opened from inside
   * a dialog is normal, and Escape has to close the picker and leave the dialog
   * standing. */
  var stack = [];
  var openMenu = null;
  var scrollLock = { count: 0, top: 0 };

  function reducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  /* Locking the body by position:fixed rather than overflow:hidden, because on
   * iOS overflow:hidden on body does not stop the page behind a sheet from
   * scrolling, and the page loses its scroll position when it is released. */
  function lockScroll() {
    if (scrollLock.count++ > 0) return;
    scrollLock.top = window.scrollY || document.documentElement.scrollTop || 0;
    var bar = window.innerWidth - document.documentElement.clientWidth;
    document.body.style.position = 'fixed';
    document.body.style.top = -scrollLock.top + 'px';
    document.body.style.left = '0';
    document.body.style.right = '0';
    document.body.style.width = '100%';
    if (bar > 0) document.body.style.paddingRight = bar + 'px';
  }

  function unlockScroll() {
    if (--scrollLock.count > 0) return;
    scrollLock.count = 0;
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.left = '';
    document.body.style.right = '';
    document.body.style.width = '';
    document.body.style.paddingRight = '';
    window.scrollTo(0, scrollLock.top);
  }

  function panel(scrim) {
    return scrim.querySelector('.neb-dialog, .neb-sheet') || scrim.firstElementChild;
  }

  function focusFirst(scrim) {
    var p = panel(scrim);
    if (!p) return;
    /* A picker's search field should have the caret; a confirm dialog should
     * not open with Delete under the finger, so an explicit hint wins and
     * otherwise the first field beats the first button. */
    var target = p.querySelector('[data-neb-autofocus]') ||
      p.querySelector('input:not([type="hidden"]):not([disabled]), textarea:not([disabled])') ||
      p.querySelector(FOCUSABLE);
    if (target) {
      try { target.focus({ preventScroll: true }); } catch (e) { target.focus(); }
    } else {
      p.setAttribute('tabindex', '-1');
      p.focus();
    }
  }

  function trap(e) {
    var top = stack[stack.length - 1];
    if (!top || e.key !== 'Tab') return;
    var p = panel(top.el);
    if (!p) return;
    var items = Array.prototype.filter.call(p.querySelectorAll(FOCUSABLE), function (el) {
      return el.offsetWidth > 0 || el.offsetHeight > 0 || el === document.activeElement;
    });
    if (!items.length) return;
    var first = items[0];
    var last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }

  function open(idOrEl, opts) {
    var el = typeof idOrEl === 'string' ? document.getElementById(idOrEl) : idOrEl;
    if (!el || !el.classList.contains('neb-scrim')) return null;
    if (stack.some(function (f) { return f.el === el; })) return el;

    closeMenu();
    var entry = { el: el, restore: document.activeElement, opts: opts || {} };
    stack.push(entry);
    lockScroll();
    el.hidden = false;
    el.setAttribute('aria-hidden', 'false');
    /* Now that it has layout, anything that had to be measured can be. */
    Array.prototype.forEach.call(el.querySelectorAll('.neb-wheel'), function (w) {
      buildWheel(w);
      var h = wheels.get(w);
      if (h) h.seat();
    });
    /* Two frames, not one. The element has just stopped being display:none, and
     * a single rAF can still land in the same style recalculation, in which case
     * the browser has no "from" value and the transition does not run. */
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        el.setAttribute('data-open', '');
        focusFirst(el);
      });
    });
    el.dispatchEvent(new CustomEvent('neb:open', { bubbles: true }));
    return el;
  }

  function close(idOrEl, detail) {
    var el = typeof idOrEl === 'string' ? document.getElementById(idOrEl) : idOrEl;
    if (!el) return;
    var i = -1;
    for (var k = 0; k < stack.length; k++) if (stack[k].el === el) { i = k; break; }
    if (i < 0) return;
    var entry = stack.splice(i, 1)[0];

    el.removeAttribute('data-open');
    el.setAttribute('data-closing', '');
    var p = panel(el);
    if (p) p.removeAttribute('data-dragging');

    var done = function () {
      el.hidden = true;
      el.removeAttribute('data-closing');
      el.setAttribute('aria-hidden', 'true');
      if (p) p.style.transform = '';
      unlockScroll();
      if (entry.restore && document.contains(entry.restore)) {
        try { entry.restore.focus({ preventScroll: true }); } catch (e) { entry.restore.focus(); }
      }
      el.dispatchEvent(new CustomEvent('neb:close', { bubbles: true, detail: detail || null }));
      if (entry.opts && entry.opts.onClose) entry.opts.onClose(detail);
    };

    if (reducedMotion()) { done(); return; }
    /* transitionend is the right signal but it never fires if the panel has no
     * transition (a test stub, a stylesheet that failed to load), so the timer
     * is the floor, not the plan. */
    var fired = false;
    var finish = function () { if (!fired) { fired = true; done(); } };
    if (p) p.addEventListener('transitionend', finish, { once: true });
    setTimeout(finish, 460);
  }

  function closeTop(detail) {
    if (stack.length) close(stack[stack.length - 1].el, detail);
  }

  /* ── Menus ───────────────────────────────────────────────────────────────
   * Positioned in the viewport with position:fixed rather than appended next to
   * the trigger, because the triggers live inside cards with overflow:hidden and
   * inside sticky bars with their own stacking context -- an absolutely
   * positioned child of either one gets clipped. */
  /* Below this width a menu stops being a dropdown and becomes a bottom sheet,
   * which is what the app does: PostExtras opens NebModalSheet for the same
   * actions, not an anchored popup. A 180px popup pinned to a 34px icon button
   * is a desktop idea. */
  var MENU_SHEET_MAX = 600;

  function asSheet() {
    return window.matchMedia('(max-width: ' + MENU_SHEET_MAX + 'px)').matches;
  }

  /* The sheet form needs a scrim, and it cannot be drawn as a pseudo-element of
   * the sheet: the sheet is translated to slide in, a transform makes it the
   * containing block for any position:fixed descendant, and the pseudo ends up
   * covering the sheet instead of the page behind it. So the controller owns a
   * real element, one for the whole document, parked outside the sheet. */
  var menuScrim = null;

  function showMenuScrim() {
    if (!menuScrim) {
      menuScrim = document.createElement('div');
      menuScrim.className = 'neb-menu-scrim';
      menuScrim.addEventListener('click', function () { closeMenu(); });
    }
    if (menuScrim.parentNode !== document.body) document.body.appendChild(menuScrim);
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { if (menuScrim) menuScrim.setAttribute('data-open', ''); });
    });
  }

  function hideMenuScrim() {
    if (!menuScrim || !menuScrim.parentNode) return;
    var el = menuScrim;
    el.removeAttribute('data-open');
    var drop = function () { if (!el.hasAttribute('data-open') && el.parentNode) el.parentNode.removeChild(el); };
    if (reducedMotion()) drop(); else setTimeout(drop, 260);
  }

  function placeMenu(menu, trigger) {
    /* A sheet is positioned by the stylesheet. Clear anything a previous
     * desktop-width open left behind, or the inline top/left will pin the
     * sheet halfway up the screen after a resize. */
    if (asSheet()) {
      menu.classList.add('neb-menu-sheet');
      showMenuScrim();
      menu.classList.remove('neb-menu-up');
      ['position', 'top', 'bottom', 'left', 'right', 'maxHeight', 'visibility']
        .forEach(function (k) { menu.style[k] = ''; });
      menu.hidden = false;
      return;
    }
    menu.classList.remove('neb-menu-sheet');
    hideMenuScrim();
    var r = trigger.getBoundingClientRect();
    menu.style.position = 'fixed';
    menu.style.maxHeight = '';
    menu.classList.remove('neb-menu-up');
    menu.style.visibility = 'hidden';
    menu.hidden = false;
    var w = menu.offsetWidth;
    var h = menu.offsetHeight;
    var pad = 8;
    var below = window.innerHeight - r.bottom - pad;
    var above = r.top - pad;
    var up = below < Math.min(h, 240) && above > below;

    if (up) {
      menu.classList.add('neb-menu-up');
      menu.style.top = '';
      menu.style.bottom = (window.innerHeight - r.top + 6) + 'px';
      menu.style.maxHeight = Math.max(140, above) + 'px';
    } else {
      menu.style.bottom = '';
      menu.style.top = (r.bottom + 6) + 'px';
      menu.style.maxHeight = Math.max(140, below) + 'px';
    }

    var align = menu.dataset.nebAlign || 'end';
    var left = align === 'start' ? r.left : r.right - w;
    if (align === 'center') left = r.left + r.width / 2 - w / 2;
    left = Math.max(pad, Math.min(left, window.innerWidth - w - pad));
    menu.style.left = left + 'px';
    menu.style.right = '';
    menu.style.visibility = '';
  }

  function showMenu(menu, trigger) {
    if (openMenu && openMenu.menu === menu) { closeMenu(); return; }
    closeMenu();
    /* The .more-menu markup ships with style="display:none" on it, and an
     * inline style beats every rule in the stylesheet. Hand the element over
     * to `hidden` once and it stays handed over. */
    if (menu.style.display) menu.style.display = '';
    placeMenu(menu, trigger);
    trigger.setAttribute('aria-expanded', 'true');
    openMenu = { menu: menu, trigger: trigger };
    requestAnimationFrame(function () { menu.setAttribute('data-open', ''); });
    menu.dispatchEvent(new CustomEvent('neb:open', { bubbles: true }));
  }

  function closeMenu(refocus) {
    if (!openMenu) return;
    var m = openMenu.menu;
    var t = openMenu.trigger;
    openMenu = null;
    m.removeAttribute('data-open');
    t.setAttribute('aria-expanded', 'false');
    if (refocus) t.focus();
    hideMenuScrim();
    var hide = function () { if (!m.hasAttribute('data-open')) m.hidden = true; };
    if (reducedMotion()) hide(); else setTimeout(hide, 260);
    m.dispatchEvent(new CustomEvent('neb:close', { bubbles: true }));
  }

  function menuItems(menu) {
    return Array.prototype.filter.call(
      menu.querySelectorAll('.neb-menu-item:not([aria-disabled="true"]), .more-menu-item:not([disabled])'),
      function (el) { return el.offsetWidth > 0 || el.offsetHeight > 0; });
  }

  /* ── Choice controls ──────────────────────────────────────────────────────
   * A group is any element with data-neb-group; "single" clears its siblings,
   * "multi" does not. The state lives in aria-pressed or aria-checked so the
   * control is announced correctly without a parallel class to keep in sync,
   * and .is-selected is mirrored on for the stylesheet's sake. */
  function isOn(el) {
    return el.getAttribute('aria-pressed') === 'true' ||
      el.getAttribute('aria-checked') === 'true' ||
      el.classList.contains('is-selected');
  }

  function setOn(el, on) {
    if (el.hasAttribute('aria-pressed')) el.setAttribute('aria-pressed', on ? 'true' : 'false');
    else if (el.hasAttribute('role') && el.getAttribute('role') === 'switch') el.setAttribute('aria-checked', on ? 'true' : 'false');
    else if (el.hasAttribute('aria-checked')) el.setAttribute('aria-checked', on ? 'true' : 'false');
    else el.setAttribute('aria-pressed', on ? 'true' : 'false');
    el.classList.toggle('is-selected', !!on);
  }

  /* The hidden input is what actually gets submitted. Without it every one of
   * these controls needs its own onclick in the page to write a value
   * somewhere, which is how the web ended up with thirty of them. */
  function syncInput(group) {
    var name = group.dataset.nebName;
    if (!name) return;
    var form = group.closest('form') || document;
    var selected = Array.prototype.map.call(
      group.querySelectorAll('[data-neb-value].is-selected, [data-neb-value][aria-pressed="true"], [data-neb-value][aria-checked="true"]'),
      function (el) { return el.dataset.nebValue; });

    if (group.dataset.nebMode === 'multi') {
      /* One input per value, rebuilt on every change: a single comma-joined
       * field cannot carry a value that contains a comma, and subject names do. */
      Array.prototype.forEach.call(
        form.querySelectorAll('input[type="hidden"][data-neb-for="' + cssEscape(name) + '"]'),
        function (el) { el.remove(); });
      var anchor = group;
      selected.forEach(function (v) {
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = name;
        input.value = v;
        input.setAttribute('data-neb-for', name);
        anchor.parentNode.insertBefore(input, anchor.nextSibling);
      });
    } else {
      var one = form.querySelector('input[type="hidden"][data-neb-for="' + cssEscape(name) + '"]');
      if (!one) {
        one = document.createElement('input');
        one.type = 'hidden';
        one.name = name;
        one.setAttribute('data-neb-for', name);
        group.parentNode.insertBefore(one, group.nextSibling);
      }
      one.value = selected[0] || '';
    }
    group.dispatchEvent(new CustomEvent('neb:change', {
      bubbles: true,
      detail: { name: name, value: group.dataset.nebMode === 'multi' ? selected : (selected[0] || '') }
    }));
  }

  function cssEscape(s) {
    return String(s).replace(/["\\]/g, '\\$&');
  }

  function toggleChoice(el) {
    var group = el.closest('[data-neb-group]');
    if (!group) { setOn(el, !isOn(el)); return; }
    var multi = group.dataset.nebMode === 'multi';
    var on = isOn(el);
    if (multi) {
      setOn(el, !on);
    } else {
      /* data-neb-required keeps a single-select from being emptied by tapping
       * the answer again -- a role or a class has to be something. */
      if (on && group.dataset.nebRequired === undefined) {
        setOn(el, false);
      } else if (!on) {
        Array.prototype.forEach.call(group.querySelectorAll('[data-neb-value]'), function (sib) {
          if (sib !== el) setOn(sib, false);
        });
        setOn(el, true);
      }
    }
    syncInput(group);
  }

  /* ── The date wheel ─────────────────────────────────────────────────────── */
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var ROW = 44;

  function daysInMonth(year, month) {
    return new Date(year, month, 0).getDate();
  }

  function pad2(n) { return (n < 10 ? '0' : '') + n; }

  var wheels = new WeakMap();

  function buildWheel(root) {
    if (root.dataset.nebReady) return;
    root.dataset.nebReady = '1';

    var thisYear = new Date().getFullYear();
    var maxYear = parseInt(root.dataset.maxYear, 10) || (thisYear - 5);
    var minYear = parseInt(root.dataset.minYear, 10) || 1940;
    var value = (root.dataset.value || '').split('-');
    var year = parseInt(value[0], 10) || (thisYear - (parseInt(root.dataset.defaultAge, 10) || 17));
    var month = parseInt(value[1], 10) || 1;
    var day = parseInt(value[2], 10) || 1;
    year = Math.min(maxYear, Math.max(minYear, year));

    var cols = {};
    ['day', 'month', 'year'].forEach(function (kind) {
      var col = document.createElement('div');
      col.className = 'neb-wheel-col neb-wheel-' + kind;
      col.dataset.kind = kind;
      col.setAttribute('role', 'listbox');
      col.setAttribute('aria-label', kind);
      root.appendChild(col);
      cols[kind] = col;
    });

    function fill(col, labels) {
      col.textContent = '';
      labels.forEach(function (label, i) {
        var item = document.createElement('div');
        item.className = 'neb-wheel-item';
        item.textContent = label;
        item.dataset.index = i;
        item.setAttribute('role', 'option');
        col.appendChild(item);
      });
    }

    var years = [];
    for (var y = maxYear; y >= minYear; y--) years.push(String(y));
    fill(cols.year, years);
    fill(cols.month, MONTHS);

    function fillDays() {
      var n = daysInMonth(year, month);
      /* Rebuild only when the month actually has a different number of days.
       * A settle on the year column runs this every time, and refilling
       * unconditionally threw away the day column's paint -- which is why the
       * chosen day sat on the band in the unselected grey. */
      if (cols.day.children.length === n) return;
      var labels = [];
      for (var d = 1; d <= n; d++) labels.push(String(d));
      fill(cols.day, labels);
      if (day > n) day = n;
      cols.day.scrollTop = (day - 1) * ROW;
      paint('day');
    }
    fillDays();

    function indexOf(kind) {
      if (kind === 'day') return day - 1;
      if (kind === 'month') return month - 1;
      return maxYear - year;
    }

    /* The band in the CSS is fixed at the third row, so "selected" is whichever
     * item is scrolled to that offset; there is no separate highlight to keep in
     * step with the scroll. */
    function centre(kind, smooth) {
      var col = cols[kind];
      var top = indexOf(kind) * ROW;
      col.dataset.settling = '1';
      if (smooth && !reducedMotion()) col.scrollTo({ top: top, behavior: 'smooth' });
      else col.scrollTop = top;
      setTimeout(function () { delete col.dataset.settling; paint(kind); }, smooth ? 340 : 0);
    }

    function paint(kind) {
      var col = cols[kind];
      var active = Math.round(col.scrollTop / ROW);
      Array.prototype.forEach.call(col.children, function (item, i) {
        var d = Math.abs(i - active);
        if (d <= 2) item.setAttribute('data-near', String(d));
        else item.removeAttribute('data-near');
        item.setAttribute('aria-selected', d === 0 ? 'true' : 'false');
      });
    }

    function emit() {
      var iso = year + '-' + pad2(month) + '-' + pad2(day);
      root.dataset.value = iso;
      var target = root.dataset.nebTarget && document.getElementById(root.dataset.nebTarget);
      if (target) target.value = iso;
      root.dispatchEvent(new CustomEvent('neb:change', { bubbles: true, detail: { value: iso } }));
    }

    function settled(kind) {
      var col = cols[kind];
      if (col.dataset.settling) return;
      var i = Math.round(col.scrollTop / ROW);
      i = Math.max(0, Math.min(i, col.children.length - 1));
      if (kind === 'day') {
        day = i + 1;
      } else if (kind === 'month') {
        month = i + 1;
        var before = day;
        fillDays();
        if (day !== before) centre('day', true);
      } else {
        year = maxYear - i;
        var wasDay = day;
        fillDays();
        if (day !== wasDay) centre('day', true);
      }
      paint(kind);
      emit();
    }

    Object.keys(cols).forEach(function (kind) {
      var col = cols[kind];
      var timer = null;
      col.addEventListener('scroll', function () {
        paint(kind);
        clearTimeout(timer);
        /* scrollend is not in Safari yet, so the idle timer is the portable
         * version of it. 110ms is past the end of a snap and short enough that
         * the value feels committed as soon as the finger lifts. */
        timer = setTimeout(function () { settled(kind); }, 110);
      }, { passive: true });
      col.addEventListener('click', function (e) {
        var item = e.target.closest('.neb-wheel-item');
        if (!item) return;
        col.dataset.settling = '1';
        col.scrollTo({ top: parseInt(item.dataset.index, 10) * ROW, behavior: reducedMotion() ? 'auto' : 'smooth' });
        setTimeout(function () { delete col.dataset.settling; settled(kind); }, 340);
      });
      centre(kind, false);
    });
    emit();

    /* Built inside a hidden overlay, every scrollTop above was written to an
     * element with no layout and silently did nothing. The overlay re-seats
     * the wheel as it opens, and a caller can put a different date in it
     * without rebuilding the thing. */
    wheels.set(root, {
      seat: function () {
        Object.keys(cols).forEach(function (kind) { centre(kind, false); });
      },
      set: function (iso) {
        var m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(String(iso || ''));
        if (!m) return;
        year = Math.min(maxYear, Math.max(minYear, parseInt(m[1], 10)));
        month = Math.min(12, Math.max(1, parseInt(m[2], 10)));
        fillDays();
        day = Math.min(daysInMonth(year, month), Math.max(1, parseInt(m[3], 10)));
        Object.keys(cols).forEach(function (kind) { centre(kind, false); });
        emit();
      },
      value: function () { return root.dataset.value || ''; }
    });
  }

  /* ── Filtering a picker's list ─────────────────────────────────────────── */
  function filterList(input) {
    var scope = input.closest('.neb-sheet, .neb-dialog, .neb-menu') || document;
    var q = input.value.trim().toLowerCase();
    var rows = scope.querySelectorAll('[data-neb-filterable]');
    var shown = 0;
    Array.prototype.forEach.call(rows, function (row) {
      var hay = (row.dataset.nebFilterable || row.textContent || '').toLowerCase();
      var hit = !q || hay.indexOf(q) !== -1;
      row.hidden = !hit;
      if (hit) shown++;
    });
    var empty = scope.querySelector('[data-neb-empty]');
    if (empty) {
      empty.hidden = shown > 0;
      if (!shown) empty.textContent = q ? 'Nothing matches \u201C' + input.value.trim() + '\u201D.' : 'Nothing here yet.';
    }
  }

  /* ── Drag a sheet down to dismiss ───────────────────────────────────────── */
  function dragSheet(handle, startEvent) {
    var sheet = handle.closest('.neb-sheet, .neb-dialog');
    if (!sheet) return;
    var scrim = sheet.closest('.neb-scrim');
    var startY = startEvent.clientY;
    var height = sheet.offsetHeight;
    var moved = 0;
    sheet.setAttribute('data-dragging', '');
    handle.setPointerCapture && handle.setPointerCapture(startEvent.pointerId);

    function move(e) {
      moved = Math.max(0, e.clientY - startY);
      sheet.style.transform = 'translateY(' + moved + 'px)';
      if (scrim) scrim.style.opacity = String(Math.max(0.15, 1 - moved / height));
    }
    function up() {
      handle.removeEventListener('pointermove', move);
      handle.removeEventListener('pointerup', up);
      handle.removeEventListener('pointercancel', up);
      sheet.removeAttribute('data-dragging');
      if (scrim) scrim.style.opacity = '';
      /* A third of the way down, or a flick, counts as a dismiss. Anything less
       * springs back, which is the same threshold the app's sheet uses. */
      if (moved > height * 0.32) {
        close(scrim || sheet, { reason: 'drag' });
      } else {
        sheet.style.transform = '';
      }
    }
    handle.addEventListener('pointermove', move);
    handle.addEventListener('pointerup', up);
    handle.addEventListener('pointercancel', up);
  }

  /* ── Wiring ─────────────────────────────────────────────────────────────── */
  document.addEventListener('click', function (e) {
    var t = e.target;

    var opener = t.closest && t.closest('[data-neb-open]');
    if (opener) {
      e.preventDefault();
      open(opener.dataset.nebOpen);
      return;
    }

    var closer = t.closest && t.closest('[data-neb-close]');
    if (closer) {
      e.preventDefault();
      var id = closer.dataset.nebClose;
      close(id ? id : closer.closest('.neb-scrim'), { reason: 'button' });
      return;
    }

    var menuTrigger = t.closest && t.closest('[data-neb-menu]');
    if (menuTrigger) {
      e.preventDefault();
      var menu = document.getElementById(menuTrigger.dataset.nebMenu);
      if (menu) showMenu(menu, menuTrigger);
      return;
    }

    var choice = t.closest && t.closest('[data-neb-value]');
    if (choice && !choice.closest('.neb-toggle, .neb-toggle-row')) {
      /* A picker row both answers and dismisses, the way the app's does. */
      toggleChoice(choice);
      var sheet = choice.closest('.neb-scrim');
      if (sheet && choice.dataset.nebDismiss !== undefined) close(sheet, { reason: 'select' });
      var inMenu = choice.closest('.neb-menu');
      if (inMenu) closeMenu();
      return;
    }

    var sw = t.closest && t.closest('.neb-toggle, .neb-toggle-row');
    if (sw && !(t.tagName === 'A' || t.closest('a'))) {
      var knob = sw.classList.contains('neb-toggle') ? sw : sw.querySelector('.neb-toggle');
      if (knob && knob.tagName !== 'INPUT') {
        var on = knob.getAttribute('aria-checked') === 'true';
        knob.setAttribute('aria-checked', on ? 'false' : 'true');
        var bound = knob.dataset.nebTarget && document.getElementById(knob.dataset.nebTarget);
        if (bound) bound.value = on ? '' : (knob.dataset.nebValue || 'on');
        knob.dispatchEvent(new CustomEvent('neb:change', { bubbles: true, detail: { checked: !on } }));
        return;
      }
    }

    /* Anything outside the open menu closes it, and a click on the scrim's own
     * padding closes a dismissible overlay. The trigger is excluded because it
     * toggles: without that, this handler closes the menu in the same click
     * that the trigger's own handler opened it. */
    if (openMenu && !t.closest('.neb-menu, .more-menu') && !openMenu.trigger.contains(t)) {
      closeMenu();
    }

    var scrim = t.closest && t.closest('.neb-scrim');
    if (scrim && t === scrim && scrim.dataset.nebPersistent === undefined) {
      close(scrim, { reason: 'scrim' });
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (openMenu) { closeMenu(true); e.preventDefault(); return; }
      var top = stack[stack.length - 1];
      if (top && top.el.dataset.nebPersistent === undefined) {
        closeTop({ reason: 'escape' });
        e.preventDefault();
      }
      return;
    }

    if (openMenu && (e.key === 'ArrowDown' || e.key === 'ArrowUp' || e.key === 'Home' || e.key === 'End')) {
      var items = menuItems(openMenu.menu);
      if (!items.length) return;
      e.preventDefault();
      var at = items.indexOf(document.activeElement);
      var next;
      if (e.key === 'Home') next = 0;
      else if (e.key === 'End') next = items.length - 1;
      else if (e.key === 'ArrowDown') next = at < 0 ? 0 : (at + 1) % items.length;
      else next = at < 0 ? items.length - 1 : (at - 1 + items.length) % items.length;
      items[next].focus();
      return;
    }

    /* Space and Enter on a div-based control. Buttons get this from the
     * browser; a role="option" row does not. */
    if (e.key === ' ' || e.key === 'Enter') {
      var el = document.activeElement;
      if (el && el.tagName !== 'BUTTON' && el.tagName !== 'A' && el.tagName !== 'INPUT' &&
          el.matches && el.matches('[data-neb-value],[data-neb-open],[data-neb-close],[data-neb-menu]')) {
        e.preventDefault();
        el.click();
      }
      return;
    }

    trap(e);
  });

  document.addEventListener('input', function (e) {
    if (e.target.matches && e.target.matches('[data-neb-filter]')) filterList(e.target);
  });

  document.addEventListener('pointerdown', function (e) {
    var handle = e.target.closest && e.target.closest('.neb-sheet-handle');
    if (handle && e.isPrimary) {
      e.preventDefault();
      dragSheet(handle, e);
    }
  });

  /* A menu is positioned against the viewport, so it has to be repositioned or
   * dropped when the viewport moves under it. Dropping is the honest answer for
   * a scroll: the trigger has moved, and a menu that follows a scrolling card
   * around is worse than one that closes. */
  window.addEventListener('resize', function () { closeMenu(); });
  window.addEventListener('scroll', function () {
    if (openMenu && openMenu.menu.classList.contains('neb-menu-sheet')) return;
    closeMenu();
  }, { passive: true });

  function scan(root) {
    Array.prototype.forEach.call((root || document).querySelectorAll('.neb-wheel'), buildWheel);
  }

  document.addEventListener('DOMContentLoaded', function () { scan(document); });
  document.body && scan(document);
  document.addEventListener('htmx:load', function (e) { scan(e.target); });
  /* A swap can take the panel of an open overlay out from under us. */
  document.addEventListener('htmx:afterSwap', function () {
    for (var i = stack.length - 1; i >= 0; i--) {
      if (!document.contains(stack[i].el)) {
        var entry = stack.splice(i, 1)[0];
        unlockScroll();
        if (entry.opts && entry.opts.onClose) entry.opts.onClose({ reason: 'swap' });
      }
    }
    if (openMenu && !document.contains(openMenu.menu)) openMenu = null;
  });

  /* ── Confirm, as a promise ────────────────────────────────────────────────
   * The web still had bare window.confirm() in a dozen places -- an OS dialog
   * in the middle of the product, with the browser's own type and the site's
   * name above it. This is a real NebDialog that resolves true or false, so a
   * call site changes from `if (confirm(...))` to `if (await NebUI.confirm(...))`
   * and nothing else. */
  function confirmDialog(o) {
    o = o || {};
    return new Promise(function (resolve) {
      var scrim = document.createElement('div');
      scrim.className = 'neb-scrim';
      scrim.hidden = true;
      scrim.id = 'neb-confirm-' + Date.now().toString(36);

      var icon = o.icon ? '<div class="neb-dialog-icon' + (o.destructive ? ' neb-dialog-icon-danger' : '') +
        ' md-shape-cookie-9"><span class="material-symbols-outlined">' + esc(o.icon) + '</span></div>' : '';
      scrim.innerHTML =
        '<div class="neb-dialog" role="dialog" aria-modal="true">' +
          '<div class="neb-dialog-head">' + icon +
            '<h2 class="neb-dialog-title">' + esc(o.title || 'Are you sure?') + '</h2>' +
            (o.message ? '<p class="neb-dialog-support">' + esc(o.message) + '</p>' : '') +
          '</div>' +
          '<div class="neb-dialog-actions neb-dialog-actions-stack">' +
            '<button type="button" class="md-btn md-btn-text" data-neb-role="cancel">' +
              esc(o.cancelLabel || 'Cancel') + '</button>' +
            '<button type="button" class="md-btn ' + (o.destructive ? 'md-btn-error' : 'md-btn-filled') +
              '" data-neb-role="ok">' + esc(o.confirmLabel || 'Confirm') + '</button>' +
          '</div>' +
        '</div>';
      document.body.appendChild(scrim);

      var answered = false;
      function finish(v) {
        if (answered) return;
        answered = true;
        resolve(v);
        close(scrim, { reason: 'confirm' });
        setTimeout(function () { scrim.remove(); }, 520);
      }
      scrim.querySelector('[data-neb-role="ok"]').addEventListener('click', function () { finish(true); });
      scrim.querySelector('[data-neb-role="cancel"]').addEventListener('click', function () { finish(false); });
      scrim.addEventListener('neb:close', function () { finish(false); });
      open(scrim);
    });
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function wheel(el) {
    var node = typeof el === 'string' ? document.getElementById(el) : el;
    return node ? wheels.get(node) || null : null;
  }

  /* ── The .more-menu family ────────────────────────────────────────────────
   * Six templates -- forum, forum_post, home, profile, search, subject_page --
   * each carried a verbatim copy of the same fourteen lines: look the menu up
   * by id, read style.display to find out whether it is open, close every menu
   * on the page, set display, then attach a capturing document click handler
   * on a setTimeout to close it again. Six copies meant six places for the
   * Escape key to be missing, which it was in all of them, and aria-expanded
   * was never set anywhere.
   *
   * One implementation now, reached by the names the pages already call so the
   * markup does not have to change. Everything the controller already does for
   * .neb-menu -- outside click, Escape, focus return, roving arrow keys, and
   * the phone-width sheet -- these get for free.
   *
   * New markup should use data-neb-menu on the trigger and skip this. */
  function legacyMenus() {
    return document.querySelectorAll('.more-menu, .neb-menu');
  }

  function closeAllMenus() {
    closeMenu();
    /* Anything left showing was opened by a page that has not been converted
     * yet, or was open when htmx swapped its trigger out from under it. */
    Array.prototype.forEach.call(legacyMenus(), function (m) {
      if (m.style.display && m.style.display !== 'none') m.style.display = 'none';
    });
  }

  function toggleMoreMenu(menuId, trigger) {
    var menu = typeof menuId === 'string' ? document.getElementById(menuId) : menuId;
    if (!menu) return;
    if (!trigger) {
      trigger = document.querySelector('[data-menu-id="' + menu.id + '"]') || menu.previousElementSibling;
    }
    if (!trigger) return;
    showMenu(menu, trigger);
  }

  /* A click on an item inside one of these menus should dismiss it -- every
   * item in every copy was an action that navigates or fires a request, and
   * none of the six copies closed the menu afterwards, so the popup sat over
   * the thing it had just changed. */
  document.addEventListener('click', function (e) {
    var item = e.target.closest && e.target.closest('.more-menu-item');
    if (item && openMenu && openMenu.menu.contains(item)) closeMenu();
  });

  window.toggleMoreMenu = toggleMoreMenu;
  window.closeAllMenus = closeAllMenus;

  window.NebUI = {
    toggleMoreMenu: toggleMoreMenu,
    closeAllMenus: closeAllMenus,
    open: open,
    close: close,
    closeTop: closeTop,
    confirm: confirmDialog,
    menu: showMenu,
    closeMenu: closeMenu,
    scan: scan,
    wheel: wheel,
    isOpen: function (id) {
      var el = typeof id === 'string' ? document.getElementById(id) : id;
      return stack.some(function (f) { return f.el === el; });
    }
  };
})();
