/* NebSelect: every <select> on the site becomes an M3 field that opens an M3 menu.
 *
 * Nothing in the markup changes. The native <select> stays in the form, hidden,
 * and stays the source of truth: forms post it, scripts read `.value`, and a
 * pick fires a real `change` event. The field and menu are drawn from it.
 *
 *   - Setting `select.value` / `selectedIndex` from script, or rewriting its
 *     options, redraws the field. No call needed.
 *   - Under 600px the menu is a bottom sheet (NebUI decides), titled with the
 *     field's label.
 *   - Opt out with `data-native` on the select, or `[multiple]` / `[size]`.
 *
 * The menu is NebUI.menu(): portaled to <body>, flipped and clamped to the
 * viewport, Escape / arrows / outside tap handled in one place.
 */
(function () {
  'use strict';

  var CHEVRON = '<svg class="neb-sel-chev" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M7 10l5 5 5-5z" fill="currentColor"/></svg>';
  var CHECK = '<svg class="neb-sel-check" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z" fill="currentColor"/></svg>';
  var uid = 0;

  function eligible(sel) {
    return sel.tagName === 'SELECT' && !sel._nebSel && !sel.multiple && !(sel.size > 1) &&
      !sel.hasAttribute('data-native') && !sel.closest('[data-native-select]');
  }

  function labelText(sel) {
    var text = sel.getAttribute('aria-label') || '';
    if (!text && sel.id) {
      var l = document.querySelector('label[for="' + sel.id.replace(/"/g, '\\"') + '"]');
      if (l) text = l.textContent;
    }
    if (!text) { var wrap = sel.closest('label'); if (wrap) text = wrap.firstChild && wrap.firstChild.textContent; }
    return (text || '').replace(/\s+/g, ' ').trim();
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }

  function enhance(sel) {
    if (!eligible(sel)) return;
    var id = 'nebsel' + (++uid);
    var cs = getComputedStyle(sel);
    var parent = sel.parentElement;
    var full = true;
    if (parent && cs.display !== 'none') {
      var pw = parent.clientWidth - parseFloat(getComputedStyle(parent).paddingLeft || 0) - parseFloat(getComputedStyle(parent).paddingRight || 0);
      var sw = sel.getBoundingClientRect().width;
      full = !sw || Math.abs(pw - sw) < 4 || sw > pw;
    }

    var field = document.createElement('button');
    field.type = 'button';
    field.className = 'neb-sel' + (full ? '' : ' is-inline');
    field.id = id;
    field.setAttribute('aria-haspopup', 'listbox');
    field.setAttribute('aria-expanded', 'false');
    if (!full) field.style.minWidth = Math.ceil(sel.getBoundingClientRect().width) + 'px';
    if (cs.flexGrow !== '0') field.style.flexGrow = cs.flexGrow;
    if (cs.marginTop !== '0px') field.style.marginTop = cs.marginTop;
    if (cs.marginBottom !== '0px') field.style.marginBottom = cs.marginBottom;
    if (sel.hasAttribute('aria-label')) field.setAttribute('aria-label', sel.getAttribute('aria-label'));
    field.innerHTML = '<span class="neb-sel-value"></span>' + CHEVRON;

    var menu = document.createElement('div');
    menu.className = 'neb-menu neb-sel-menu';
    menu.setAttribute('role', 'listbox');
    menu.setAttribute('data-neb-align', 'start');
    menu.hidden = true;

    sel.classList.add('neb-sel-native');
    sel.tabIndex = -1;
    sel.setAttribute('aria-hidden', 'true');
    sel.parentNode.insertBefore(field, sel.nextSibling);
    field.parentNode.insertBefore(menu, field.nextSibling);
    sel._nebSel = { field: field, menu: menu };

    function draw() {
      var opt = sel.options[sel.selectedIndex];
      var v = field.querySelector('.neb-sel-value');
      v.textContent = opt ? opt.textContent.trim() : '';
      field.classList.toggle('is-placeholder', !opt || (opt.value === '' && sel.options.length > 1));
      field.disabled = sel.disabled;
      var gone = sel.hidden || sel.style.display === 'none';
      field.hidden = gone;
      if (!field.getAttribute('aria-label') && !field.hasAttribute('aria-labelledby')) {
        var t = labelText(sel);
        if (t) field.setAttribute('aria-label', t + ': ' + v.textContent);
      }
    }

    function build() {
      var title = labelText(sel);
      var html = title ? '<div class="neb-menu-label">' + esc(title) + '</div>' : '';
      function item(o, i) {
        var on = i === sel.selectedIndex;
        return '<button type="button" class="neb-menu-item neb-sel-item" role="option" data-i="' + i + '"' +
          (o.disabled ? ' aria-disabled="true"' : '') + ' aria-checked="' + on + '" aria-selected="' + on + '">' +
          '<span class="neb-menu-item-label">' + esc(o.textContent.trim() || '\u00a0') + '</span>' + CHECK + '</button>';
      }
      Array.prototype.forEach.call(sel.children, function (n) {
        if (n.tagName === 'OPTGROUP') {
          html += '<div class="neb-menu-label">' + esc(n.label) + '</div>';
          Array.prototype.forEach.call(n.children, function (o) { html += item(o, o.index); });
        } else if (n.tagName === 'OPTION') {
          html += item(n, n.index);
        }
      });
      menu.innerHTML = html;
    }

    function sync() { draw(); }
    sel._nebSel.sync = sync;

    /* Scripts set .value and .selectedIndex without firing anything. Wrap both on
       this instance so the field follows. */
    ['value', 'selectedIndex'].forEach(function (prop) {
      var d = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, prop);
      if (!d || !d.set) return;
      Object.defineProperty(sel, prop, {
        configurable: true,
        get: function () { return d.get.call(sel); },
        set: function (v) { d.set.call(sel, v); draw(); }
      });
    });

    new MutationObserver(function () { draw(); if (menu.hasAttribute('data-open')) build(); })
      .observe(sel, { childList: true, subtree: true, attributes: true, attributeFilter: ['disabled', 'hidden', 'style', 'selected'], characterData: true });
    sel.addEventListener('change', draw);
    if (sel.form) sel.form.addEventListener('reset', function () { setTimeout(draw, 0); });
    sel.addEventListener('focus', function () { if (!field.disabled && !field.hidden) field.focus(); });

    field.addEventListener('click', function () {
      if (field.disabled) return;
      build();
      menu.style.minWidth = Math.max(field.offsetWidth, 168) + 'px';
      NebUI.menu(menu, field);
      var cur = menu.querySelector('[aria-checked="true"]');
      if (cur) { try { cur.scrollIntoView({ block: 'nearest' }); } catch (e) { /* ignore */ } }
    });
    field.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); field.click(); }
    });
    menu.addEventListener('click', function (e) {
      var it = e.target.closest('.neb-sel-item');
      if (!it || it.getAttribute('aria-disabled') === 'true') return;
      var d = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'selectedIndex');
      d.set.call(sel, parseInt(it.getAttribute('data-i'), 10));
      draw();
      NebUI.closeMenu(true);
      sel.dispatchEvent(new Event('input', { bubbles: true }));
      sel.dispatchEvent(new Event('change', { bubbles: true }));
    });
    menu.addEventListener('neb:open', function () { field.classList.add('is-open'); });
    menu.addEventListener('neb:close', function () { field.classList.remove('is-open'); });
    draw();
  }

  function scan(scope) {
    (scope || document).querySelectorAll('select').forEach(enhance);
  }

  window.NebSelect = {
    scan: scan,
    refresh: function (sel) { if (sel && sel._nebSel) sel._nebSel.sync(); }
  };

  function start() {
    scan();
    new MutationObserver(function (list) {
      list.forEach(function (m) {
        m.addedNodes.forEach(function (n) {
          if (n.nodeType !== 1) return;
          if (n.tagName === 'SELECT') enhance(n); else if (n.querySelector) scan(n);
        });
      });
    }).observe(document.body, { childList: true, subtree: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
