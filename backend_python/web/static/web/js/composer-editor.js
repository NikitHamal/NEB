(function () {
  'use strict';
  /* The post composer's writing surface.
     1. The textarea has no height of its own: it takes the height of the text and the dialog body scrolls, so a long
        post is one continuous page (no inner scrollbar, wheel and touch scroll work everywhere). The caret is kept in
        view while typing.
     2. @mentions: type @ and pick a person; staff also get @all. Search is the same endpoint the replies use. */

  var MIRROR_PROPS = ['boxSizing', 'width', 'fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'letterSpacing', 'lineHeight',
    'textTransform', 'wordSpacing', 'textIndent', 'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
    'borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth', 'tabSize'];

  /* Where the caret is, relative to the textarea's top-left, measured on an invisible twin. */
  function caretPoint(ta, pos) {
    var cs = getComputedStyle(ta);
    var m = document.createElement('div');
    MIRROR_PROPS.forEach(function (p) { m.style[p] = cs[p]; });
    m.style.cssText += ';position:absolute;visibility:hidden;top:0;left:-9999px;white-space:pre-wrap;overflow-wrap:break-word;word-break:normal;height:auto';
    m.textContent = ta.value.substring(0, pos);
    var mark = document.createElement('span');
    mark.textContent = '\u200b';
    m.appendChild(mark);
    document.body.appendChild(m);
    var lh = parseFloat(cs.lineHeight) || 24;
    var pt = { x: mark.offsetLeft, y: mark.offsetTop, h: lh };
    document.body.removeChild(m);
    return pt;
  }

  function scroller(ta) { return ta.closest('.hf-dialog-body') || ta.parentElement; }

  function grow(ta) {
    if (!ta.offsetParent) return;
    var box = scroller(ta), keep = box ? box.scrollTop : 0;
    ta.style.height = 'auto';
    ta.style.height = ta.scrollHeight + 'px';
    if (box) box.scrollTop = keep;
  }

  function follow(ta) {
    var box = scroller(ta);
    if (!box || document.activeElement !== ta) return;
    var pos = ta.selectionEnd, pt = caretPoint(ta, pos);
    var t = ta.getBoundingClientRect(), b = box.getBoundingClientRect();
    var top = t.top + pt.y, bottom = top + pt.h;
    var pad = 28;
    if (bottom > b.bottom - pad) box.scrollTop += bottom - (b.bottom - pad);
    else if (top < b.top + pad) box.scrollTop -= (b.top + pad) - top;
  }

  function enhanceField(ta) {
    if (ta.__editor) return;
    ta.__editor = true;
    var tick = function () { grow(ta); follow(ta); };
    ta.addEventListener('input', tick);
    ta.addEventListener('keyup', function (e) { if (e.key.indexOf('Arrow') === 0 || e.key === 'Home' || e.key === 'End') follow(ta); });
    ta.addEventListener('focus', function () { grow(ta); });
    window.addEventListener('resize', function () { grow(ta); });
    /* A click on the empty page below the text lands in the field. */
    var box = scroller(ta);
    if (box) box.addEventListener('click', function (e) {
      if (e.target === box && ta.offsetParent) { ta.focus(); ta.setSelectionRange(ta.value.length, ta.value.length); follow(ta); }
    });
    var dlg = ta.closest('dialog');
    if (dlg && 'MutationObserver' in window) {
      new MutationObserver(function () { if (dlg.open) setTimeout(function () { grow(ta); }, 30); }).observe(dlg, { attributes: true, attributeFilter: ['open'] });
    }
    /* Programmatic changes (emoji, formatting, reset) fire input events or set value; poll the value cheaply. */
    var last = ta.value;
    setInterval(function () { if (ta.value !== last) { last = ta.value; grow(ta); } }, 250);
    grow(ta);
  }

  /* ---------------- mentions ---------------- */
  var ALL = { all: true, username: 'all', displayName: 'Everyone' };
  var TRIGGER = /(^|[\s(\[])@([A-Za-z0-9_.]{0,30})$/;

  function esc(s) { var d = document.createElement('div'); d.textContent = s == null ? '' : String(s); return d.innerHTML; }

  function mentions(ta) {
    if (ta.__mentions) return;
    ta.__mentions = true;
    var canAll = ta.getAttribute('data-can-mention-all') === '1';
    var host = ta.closest('dialog') || document.body;
    var pop = document.createElement('div');
    pop.className = 'hf-mention-pop';
    pop.setAttribute('role', 'listbox');
    pop.hidden = true;
    host.appendChild(pop);
    var rows = [], sel = 0, timer = 0, seq = 0, cache = {};

    function close() { pop.hidden = true; rows = []; }

    function query() {
      var pos = ta.selectionStart;
      if (pos !== ta.selectionEnd) return null;
      var m = ta.value.substring(0, pos).match(TRIGGER);
      return m ? { q: m[2], at: pos - m[2].length - 1, pos: pos } : null;
    }

    function paint() {
      pop.innerHTML = rows.map(function (u, i) {
        var av = u.all
          ? '<span class="hf-mention-av is-all"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11v2a1 1 0 0 0 1 1h2l5 4V6L6 10H4a1 1 0 0 0-1 1z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/></svg></span>'
          : '<span class="hf-mention-av">' + (u.photoUrl ? '<img src="' + esc(u.photoUrl) + '" alt="" width="32" height="32" loading="lazy">' : esc((u.displayName || u.username).charAt(0).toUpperCase())) + '</span>';
        return '<button type="button" class="hf-mention-row' + (i === sel ? ' is-active' : '') + '" role="option" data-i="' + i + '">' + av +
          '<span class="hf-mention-txt"><b>' + esc(u.displayName) + '</b><span>@' + esc(u.username) + '</span></span></button>';
      }).join('');
      var act = pop.querySelector('.is-active');
      if (act && act.scrollIntoView) act.scrollIntoView({ block: 'nearest' });
    }

    function place(info) {
      var pt = caretPoint(ta, info.at), r = ta.getBoundingClientRect();
      var w = Math.min(320, window.innerWidth - 16);
      pop.style.width = w + 'px';
      var left = Math.max(8, Math.min(r.left + pt.x, window.innerWidth - w - 8));
      var below = r.top + pt.y + pt.h + 6;
      var h = Math.min(pop.scrollHeight, 280);
      var top = (below + h > window.innerHeight - 8) ? Math.max(8, r.top + pt.y - h - 6) : below;
      pop.style.left = left + 'px';
      pop.style.top = top + 'px';
    }

    function show(list, info) {
      rows = list;
      if (!rows.length) { close(); return; }
      sel = Math.min(sel, rows.length - 1);
      pop.hidden = false;
      paint();
      place(info);
    }

    function choose(i) {
      var info = query(), u = rows[i];
      if (!info || !u) { close(); return; }
      var ins = '@' + u.username + ' ';
      ta.setRangeText(ins, info.at, info.pos, 'end');
      close();
      ta.focus();
      ta.dispatchEvent(new Event('input', { bubbles: true }));
    }

    function update() {
      var info = query();
      if (!info) { close(); return; }
      clearTimeout(timer);
      var q = info.q.toLowerCase();
      var head = canAll && 'all'.indexOf(q) === 0 ? [ALL] : [];
      if (!q) { sel = 0; show(head, info); return; }
      var my = ++seq;
      var cached = cache[q];
      if (cached) { show(head.concat(cached), info); return; }
      show(head, info);
      timer = setTimeout(function () {
        fetch('/ajax/user-search/?q=' + encodeURIComponent(q), { credentials: 'same-origin' })
          .then(function (r) { return r.ok ? r.json() : []; })
          .then(function (users) {
            if (!Array.isArray(users)) users = [];
            cache[q] = users;
            if (my !== seq) return;
            var now = query();
            if (!now || now.q.toLowerCase() !== q) return;
            sel = 0;
            show(head.concat(users), now);
          })
          .catch(function () {});
      }, 130);
    }

    ta.addEventListener('input', function () { sel = 0; update(); });
    ta.addEventListener('click', update);
    ta.addEventListener('blur', function () { setTimeout(close, 160); });
    ta.addEventListener('keydown', function (e) {
      if (pop.hidden || !rows.length) return;
      if (e.key === 'ArrowDown') { sel = (sel + 1) % rows.length; paint(); }
      else if (e.key === 'ArrowUp') { sel = (sel - 1 + rows.length) % rows.length; paint(); }
      else if (e.key === 'Enter' || e.key === 'Tab') { choose(sel); }
      else if (e.key === 'Escape') { close(); }
      else return;
      e.preventDefault();
      e.stopImmediatePropagation();
    }, true);
    pop.addEventListener('mousedown', function (e) {
      e.preventDefault();
      var b = e.target.closest('.hf-mention-row');
      if (b) choose(+b.getAttribute('data-i'));
    });
    var box = scroller(ta);
    if (box) box.addEventListener('scroll', close, { passive: true });
  }

  window.NebComposerEditor = { grow: grow, follow: follow, enhance: function (ta) { enhanceField(ta); mentions(ta); } };

  function boot() {
    var ta = document.getElementById('homePostContent');
    if (ta) window.NebComposerEditor.enhance(ta);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
