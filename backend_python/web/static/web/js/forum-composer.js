/* Forum writing tools. One module for every place a forum answer is written:
   the reply field, the thread field, the edit dialogs.

   ForumComposer.mount(textarea, { kinds: bool, key: 'main' }) adds
     - a kind row (Comment / Answer / Solution / Hint / Formula) that seeds a scaffold
     - a formatting toolbar that writes markdown the server already renders
     - a symbol palette for people who do not write TeX
     - Write / Preview, rendered by the server so the preview is exactly what is posted
     - a draft kept per field, shortcuts (Ctrl+B, I, K, E, Enter) and a counter near the limit
   Fields are found by [data-fc] and mounted on load; call mount() for ones built later. */
(function () {
  'use strict';

  var LIMIT = 10000;
  var KINDS = [
    { key: 'comment', label: 'Comment', icon: 'chat_bubble', scaffold: '' },
    { key: 'answer', label: 'Answer', icon: 'task_alt', scaffold: '**Answer:** ' },
    { key: 'solution', label: 'Solution', icon: 'format_list_numbered',
      scaffold: '**Given**\n- \n\n**To find**\n- \n\n**Solution**\n1. \n\n**Answer:** ' },
    { key: 'hint', label: 'Hint', icon: 'lightbulb', scaffold: '**Hint:** ' },
    { key: 'formula', label: 'Formula', icon: 'function',
      scaffold: '**Formula**\n$$\n\n$$\n\n**Where**\n- ' }
  ];
  var SYMBOLS = ['\u00b2', '\u00b3', '\u221a', '\u03c0', '\u03b8', '\u03b1', '\u03b2', '\u03bb', '\u03bc', '\u0394', '\u03a3', '\u222b',
    '\u00b1', '\u00d7', '\u00f7', '\u2260', '\u2264', '\u2265', '\u2248', '\u221e', '\u2192', '\u21cc', '\u00b0', '\u2234'];

  function csrf() {
    var m = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
    if (m) return decodeURIComponent(m[1]);
    return typeof window.CSRF_TOKEN === 'string' ? window.CSRF_TOKEN : '';
  }

  function icon(name) {
    return '<span class="material-symbols-outlined" aria-hidden="true">' + name + '</span>';
  }

  var TOOLS = [
    { id: 'bold', icon: 'format_bold', label: 'Bold', hint: 'Ctrl+B', wrap: ['**', '**'], ph: 'bold text' },
    { id: 'italic', icon: 'format_italic', label: 'Italic', hint: 'Ctrl+I', wrap: ['*', '*'], ph: 'italic text' },
    { id: 'code', icon: 'code', label: 'Code', hint: 'Ctrl+E', wrap: ['`', '`'], ph: 'code' },
    { id: 'codeblock', icon: 'terminal', label: 'Code block', block: ['```\n', '\n```'], ph: 'code' },
    { sep: true },
    { id: 'quote', icon: 'format_quote', label: 'Quote', prefix: '> ' },
    { id: 'ul', icon: 'format_list_bulleted', label: 'Bulleted list', prefix: '- ' },
    { id: 'ol', icon: 'format_list_numbered', label: 'Numbered list', prefix: 'num' },
    { id: 'link', icon: 'link', label: 'Link', hint: 'Ctrl+K', wrap: ['[', '](https://)'], ph: 'link text' },
    { sep: true },
    { id: 'math', icon: 'function', label: 'Formula in a line', wrap: ['$', '$'], ph: 'x^2 + y^2' },
    { id: 'mathblock', icon: 'calculate', label: 'Formula on its own line', block: ['$$\n', '\n$$'], ph: 'E = mc^2' },
    { id: 'step', icon: 'steps', label: 'Next step', step: true },
    { id: 'symbols', icon: 'special_character', label: 'Symbols', symbols: true }
  ];

  function replaceRange(ta, start, end, text, selStart, selEnd) {
    ta.focus();
    ta.setSelectionRange(start, end);
    var ok = false;
    try { ok = document.execCommand('insertText', false, text); } catch (e) { ok = false; }
    if (!ok) {
      ta.value = ta.value.slice(0, start) + text + ta.value.slice(end);
      ta.dispatchEvent(new Event('input', { bubbles: true }));
    }
    ta.setSelectionRange(selStart, selEnd);
  }

  function lineBounds(ta) {
    var v = ta.value;
    var s = v.lastIndexOf('\n', ta.selectionStart - 1) + 1;
    var e = v.indexOf('\n', ta.selectionEnd);
    return [s, e < 0 ? v.length : e];
  }

  function apply(ta, tool) {
    var v = ta.value, s = ta.selectionStart, e = ta.selectionEnd;
    var sel = v.slice(s, e);
    if (tool.wrap) {
      var a = tool.wrap[0], b = tool.wrap[1];
      if (sel.slice(0, a.length) === a && sel.slice(-b.length) === b && sel.length >= a.length + b.length) {
        var inner = sel.slice(a.length, sel.length - b.length);
        replaceRange(ta, s, e, inner, s, s + inner.length);
        return;
      }
      var body = sel || tool.ph;
      replaceRange(ta, s, e, a + body + b, s + a.length, s + a.length + body.length);
      return;
    }
    if (tool.block) {
      var pre = (s > 0 && v[s - 1] !== '\n') ? '\n' : '';
      var text = sel || tool.ph;
      var out = pre + tool.block[0] + text + tool.block[1] + '\n';
      var from = s + pre.length + tool.block[0].length;
      replaceRange(ta, s, e, out, from, from + text.length);
      return;
    }
    if (tool.prefix) {
      var lb = lineBounds(ta);
      var lines = v.slice(lb[0], lb[1]).split('\n');
      var allOn = lines.every(function (l) { return tool.prefix === 'num' ? /^\d+\.\s/.test(l) : l.indexOf(tool.prefix) === 0; });
      var next = lines.map(function (l, i) {
        if (tool.prefix === 'num') return allOn ? l.replace(/^\d+\.\s/, '') : (i + 1) + '. ' + l;
        return allOn ? l.slice(tool.prefix.length) : tool.prefix + l;
      }).join('\n');
      replaceRange(ta, lb[0], lb[1], next, lb[0], lb[0] + next.length);
      return;
    }
    if (tool.step) {
      var n = (v.match(/^\*\*Step \d+/gm) || []).length + 1;
      var before = v.slice(0, s);
      var lead = !before ? '' : (/\n\n$/.test(before) ? '' : (/\n$/.test(before) ? '\n' : '\n\n'));
      var label = lead + '**Step ' + n + ':** ';
      replaceRange(ta, s, e, label, s + label.length, s + label.length);
    }
  }

  function insertText(ta, text) {
    var s = ta.selectionStart;
    replaceRange(ta, s, ta.selectionEnd, text, s + text.length, s + text.length);
  }

  var seq = 0;

  function mount(ta, opts) {
    if (!ta) return null;
    if (ta._fc) return ta._fc;
    opts = opts || {};
    var id = ++seq;
    var host = ta.closest('.neb-composer-body') || ta.parentElement;
    var key = opts.key || ta.getAttribute('data-fc-key') || ta.id || ('f' + id);
    var kinds = opts.kinds !== undefined ? opts.kinds : ta.getAttribute('data-fc') === 'kinds';
    var actions = host.querySelector('.neb-composer-actions');
    var compact = !!(actions && ta.closest('.neb-composer'));
    var state = { kind: 'comment', preview: false, open: !compact, tall: false };
    var capBase = ta.getAttribute('data-autoheight-max') || '';
    var root = document.createElement('div');
    root.className = 'fc';
    ta.classList.add('fc-field');
    host.classList.add('fc-host');
    host.classList.add(compact ? 'is-compact' : 'is-open');

    function btn(cls, name, label, extra) {
      return '<button type="button" class="' + cls + '" aria-label="' + label + '" title="' + label + '"' + (extra || '') + '>' + icon(name) + '</button>';
    }

    root.innerHTML =
      '<div class="fc-inner"><div class="fc-bar" role="toolbar" aria-label="Formatting">' +
        '<div class="fc-tools">' + TOOLS.map(function (t) {
          if (t.sep) return '<span class="fc-sep" aria-hidden="true"></span>';
          return '<button type="button" class="fc-tool" data-tool="' + t.id + '" aria-label="' + t.label +
            '" title="' + t.label + (t.hint ? ' (' + t.hint + ')' : '') + '">' + icon(t.icon) + '</button>';
        }).join('') + '</div>' +
        (compact ? '' : btn('fc-iconbtn fc-modebtn', 'visibility', 'Preview', ' aria-pressed="false"')) +
      '</div></div>' +
      '<div class="neb-menu fc-pop" hidden role="menu" data-neb-align="start" aria-label="Symbols">' + SYMBOLS.map(function (c) {
        return '<button type="button" class="fc-sym" role="menuitem" data-sym="' + c + '">' + c + '</button>';
      }).join('') + '</div>';
    host.insertBefore(root, ta);

    var preview = document.createElement('div');
    preview.className = 'fc-preview';
    preview.hidden = true;
    preview.setAttribute('aria-live', 'polite');
    host.insertBefore(preview, ta.nextSibling);

    var counter = document.createElement('span');
    counter.className = 'fc-count';
    counter.hidden = true;

    var pop = root.querySelector('.fc-pop');
    var toolBtns = root.querySelectorAll('.fc-tool');
    var fmtBtn = null, growBtn = null, modeBtn = root.querySelector('.fc-modebtn'), kindBtn = null, kindMenu = null;

    if (compact) {
      fmtBtn = document.createElement('button');
      fmtBtn.type = 'button';
      fmtBtn.className = 'fc-iconbtn fc-fmt';
      fmtBtn.setAttribute('aria-expanded', 'false');
      fmtBtn.innerHTML = icon('text_format');
      actions.insertBefore(fmtBtn, actions.firstChild);

      var end = document.createElement('div');
      end.className = 'fc-end';
      end.appendChild(counter);
      end.insertAdjacentHTML('beforeend',
        btn('fc-iconbtn fc-modebtn', 'visibility', 'Preview', ' aria-pressed="false"') +
        btn('fc-iconbtn fc-growbtn', 'open_in_full', 'Taller writing area'));
      actions.insertBefore(end, actions.querySelector('.reply-send-btn'));
      modeBtn = end.querySelector('.fc-modebtn');
      growBtn = end.querySelector('.fc-growbtn');
    } else {
      host.appendChild(counter);
    }

    if (kinds) {
      var wrap = document.createElement('div');
      wrap.className = 'fc-kindwrap';
      wrap.innerHTML =
        '<button type="button" class="fc-iconbtn fc-kindbtn" aria-haspopup="menu" aria-expanded="false" title="What are you posting">' +
          icon('chat_bubble') + '<span class="fc-kindlabel"></span></button>' +
        '<div class="neb-menu fc-kindmenu" hidden role="menu" data-neb-align="start" aria-label="What are you posting">' +
          KINDS.map(function (k) {
            return '<button type="button" class="neb-menu-item fc-kindopt" role="menuitemradio" aria-checked="' + (k.key === 'comment') +
              '" data-kind="' + k.key + '">' + icon(k.icon) + '<span>' + k.label + '</span>' + icon('check') + '</button>';
          }).join('') + '</div>';
      if (actions && compact) actions.insertBefore(wrap, actions.querySelector('.fc-end'));
      else root.querySelector('.fc-bar').insertBefore(wrap, root.querySelector('.fc-tools'));
      kindBtn = wrap.querySelector('.fc-kindbtn');
      kindMenu = wrap.querySelector('.fc-kindmenu');
    }

    var toolsEl = root.querySelector('.fc-tools');
    function edges() {
      toolsEl.classList.toggle('can-right', toolsEl.scrollLeft + toolsEl.clientWidth < toolsEl.scrollWidth - 2);
      toolsEl.classList.toggle('can-left', toolsEl.scrollLeft > 2);
    }
    toolsEl.addEventListener('scroll', edges, { passive: true });
    window.addEventListener('resize', edges);
    toolsEl.addEventListener('wheel', function (e) {
      if (Math.abs(e.deltaY) > Math.abs(e.deltaX) && toolsEl.scrollWidth > toolsEl.clientWidth) { toolsEl.scrollLeft += e.deltaY; e.preventDefault(); }
    }, { passive: false });
    setTimeout(edges, 480);

    /* Both popups are NebUI menus: portaled to <body>, placed in the viewport and
       flipped or clamped at the edges, so no card, rail or sticky bar can clip them. */
    function popOpen() { return pop.hasAttribute('data-open'); }
    function closePop() {
      if (popOpen() && window.NebUI) NebUI.closeMenu();
    }

    function closeKindMenu() {
      if (kindMenu && kindMenu.hasAttribute('data-open') && window.NebUI) NebUI.closeMenu();
    }
    if (kindMenu) kindMenu.addEventListener('click', function (e) {
      var ko = e.target.closest('.fc-kindopt');
      if (!ko) return;
      setKind(ko.getAttribute('data-kind'));
      closeKindMenu();
      kindBtn.focus();
    });
    pop.addEventListener('click', function (e) {
      var sb = e.target.closest('.fc-sym');
      if (sb) insertText(ta, sb.getAttribute('data-sym'));
    });

    function regrow() {
      if (window.NebGrow && ta.hasAttribute('data-autoheight')) NebGrow(ta);
    }

    function setOpen(v, focus) {
      state.open = !!v;
      host.classList.toggle('is-open', state.open);
      host.classList.toggle('is-compact', !state.open);
      if (fmtBtn) {
        fmtBtn.setAttribute('aria-expanded', String(state.open));
        var l = state.open ? 'Hide formatting' : 'Show formatting';
        fmtBtn.setAttribute('aria-label', l);
        fmtBtn.title = l;
      }
      if (!state.open) {
        closePop();
        if (state.preview) setMode('write', true);
        setTall(false);
      } else if (focus) {
        ta.focus();
      }
      regrow();
      setTimeout(edges, 470);
    }

    function setTall(v) {
      state.tall = !!v;
      host.classList.toggle('is-tall', state.tall);
      if (!growBtn) return;
      growBtn.querySelector('.material-symbols-outlined').textContent = state.tall ? 'close_fullscreen' : 'open_in_full';
      var l = state.tall ? 'Shorter writing area' : 'Taller writing area';
      growBtn.setAttribute('aria-label', l);
      growBtn.title = l;
      if (capBase || ta.hasAttribute('data-autoheight-max')) {
        ta.setAttribute('data-autoheight-max', state.tall ? '460' : capBase);
      }
      regrow();
    }

    function setMode(mode, silent) {
      state.preview = mode === 'preview';
      toolBtns.forEach(function (b) { b.disabled = state.preview; });
      closePop();
      root.classList.toggle('is-preview', state.preview);
      host.classList.toggle('is-previewing', state.preview);
      if (modeBtn) {
        modeBtn.setAttribute('aria-pressed', String(state.preview));
        modeBtn.querySelector('.material-symbols-outlined').textContent = state.preview ? 'edit' : 'visibility';
        var l = state.preview ? 'Back to writing' : 'Preview';
        modeBtn.setAttribute('aria-label', l);
        modeBtn.title = l;
      }
      if (!state.preview) {
        preview.hidden = true; ta.hidden = false;
        regrow();
        if (!silent) ta.focus();
        return;
      }
      var text = ta.value.trim();
      ta.hidden = true; preview.hidden = false;
      if (!text) { preview.innerHTML = '<p class="fc-empty">Nothing to preview yet.</p>'; return; }
      preview.innerHTML = '<div class="fc-loading" aria-hidden="true"><i></i><i></i><i></i></div>';
      fetch('/ajax/forum/preview/', {
        method: 'POST', credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
        body: JSON.stringify({ content: text })
      }).then(function (r) { return r.json(); }).then(function (d) {
        if (!state.preview) return;
        preview.innerHTML = '<div class="fp-reply-body fc-rendered">' + (d.html || '') + '</div>';
        if (window.renderAllMath) window.renderAllMath(preview);
      }).catch(function () {
        preview.innerHTML = '<p class="fc-empty">Preview is not available right now.</p>';
      });
    }

    function setKind(k, silent) {
      var prev = KINDS.filter(function (x) { return x.key === state.kind; })[0];
      var nextK = KINDS.filter(function (x) { return x.key === k; })[0] || KINDS[0];
      var cur = ta.value;
      var untouched = !cur.trim() || (prev && prev.scaffold && cur === prev.scaffold);
      state.kind = nextK.key;
      host.querySelectorAll('.fc-kindopt').forEach(function (b) {
        b.setAttribute('aria-checked', String(b.getAttribute('data-kind') === nextK.key));
      });
      host.setAttribute('data-kind', nextK.key);
      if (kindBtn) {
        kindBtn.querySelector('.material-symbols-outlined').textContent = nextK.icon;
        kindBtn.querySelector('.fc-kindlabel').textContent = nextK.key === 'comment' ? '' : nextK.label;
        kindBtn.classList.toggle('is-set', nextK.key !== 'comment');
        kindBtn.title = 'Posting as: ' + nextK.label;
        kindBtn.setAttribute('aria-label', 'Posting as: ' + nextK.label + '. Change');
      }
      if (!silent && untouched) {
        ta.value = nextK.scaffold;
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        var at = nextK.key === 'formula' ? nextK.scaffold.indexOf('$$\n') + 3 : nextK.scaffold.length;
        if (nextK.scaffold) setOpen(true);
        ta.focus();
        ta.setSelectionRange(at, at);
      }
      if (!ta.hasAttribute('data-fc-ph')) ta.setAttribute('data-fc-ph', ta.getAttribute('placeholder') || '');
      var base = ta.getAttribute('data-fc-ph');
      var hints = { comment: base, answer: 'Write the answer', solution: 'Show the working, one step at a time',
        hint: 'Give a nudge without the full answer', formula: 'Write the formula and what each part means' };
      ta.setAttribute('placeholder', hints[nextK.key] || base);
      if (ta.hasAttribute('data-autoheight')) ta.dispatchEvent(new Event('input', { bubbles: true }));
    }

    host.addEventListener('click', function (e) {
      if (e.target.closest('.fc-kindbtn')) { NebUI.menu(kindMenu, kindBtn); return; }
      if (e.target.closest('.fc-fmt')) { setOpen(!state.open, true); return; }
      if (e.target.closest('.fc-growbtn')) { setTall(!state.tall); ta.focus(); return; }
      if (e.target.closest('.fc-modebtn')) { setMode(state.preview ? 'write' : 'preview'); return; }
      var tb = e.target.closest('.fc-tool');
      if (!tb) return;
      var tool = TOOLS.filter(function (t) { return t.id === tb.getAttribute('data-tool'); })[0];
      if (tool.symbols) {
        NebUI.menu(pop, tb);
        return;
      }
      closePop();
      apply(ta, tool);
    });

    ta.addEventListener('keydown', function (e) {
      if (!(e.ctrlKey || e.metaKey)) return;
      var k = e.key.toLowerCase();
      var map = { b: 'bold', i: 'italic', k: 'link', e: 'code' };
      if (map[k]) {
        e.preventDefault();
        apply(ta, TOOLS.filter(function (t) { return t.id === map[k]; })[0]);
      } else if (e.key === 'Enter') {
        var send = host.closest('.neb-composer, form, .fc-host, body').querySelector('.reply-send-btn');
        if (send && !send.disabled) { e.preventDefault(); send.click(); }
      }
    });

    var dk = 'fc:draft:' + location.pathname + ':' + key;
    var timer = 0;
    function save() {
      clearTimeout(timer);
      timer = setTimeout(function () {
        try {
          if (ta.value.trim()) localStorage.setItem(dk, JSON.stringify({ v: ta.value, k: state.kind }));
          else localStorage.removeItem(dk);
        } catch (err) { /* storage full or blocked */ }
      }, 400);
    }
    ta.addEventListener('input', function () {
      var n = ta.value.length;
      counter.hidden = n < LIMIT * 0.85;
      counter.textContent = n + ' / ' + LIMIT;
      counter.classList.toggle('is-over', n > LIMIT);
      save();
    });
    if (!opts.noDraft && !ta.hasAttribute('data-fc-nodraft') && !ta.value) {
      try {
        var d = JSON.parse(localStorage.getItem(dk) || 'null');
        if (d && d.v) {
          ta.value = d.v;
          if (kinds && d.k) setKind(d.k, true);
          if (compact && (d.v.length > 90 || d.v.indexOf('\n') >= 0)) setOpen(true);
          ta.dispatchEvent(new Event('input', { bubbles: true }));
        }
      } catch (err) { /* ignore a corrupt draft */ }
    }
    setKind(state.kind, true);

    var api = {
      textarea: ta, root: root,
      kind: function () { return state.kind; },
      open: function (v) { setOpen(v !== false, true); },
      reset: function () {
        setMode('write', true);
        setKind('comment', true);
        setOpen(!compact);
        regrow();
        try { localStorage.removeItem(dk); } catch (err) { /* ignore */ }
      }
    };
    ta._fc = api;
    return api;
  }

  function scan(scope) {
    (scope || document).querySelectorAll('textarea[data-fc]').forEach(function (t) { mount(t); });
  }

  function byId(id) { return typeof id === 'string' ? document.getElementById(id) : id; }

  window.ForumComposer = {
    mount: mount,
    scan: scan,
    kindOf: function (id) { var t = byId(id); return t && t._fc ? t._fc.kind() : 'comment'; },
    reset: function (id) { var t = byId(id); if (t && t._fc) t._fc.reset(); },
    KINDS: KINDS
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { scan(); });
  else scan();
})();
