/* CodeUI — reusable boardui-style components (window.CodeUI) */
(function () {
  'use strict';

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function icon(name, cls) {
    return '<span class="material-symbols-outlined ' + (cls || 'ncu-icon') + '">' + name + '</span>';
  }

  /* ── IconButton ──────────────────────────────────────── */
  function IconButton(opts) {
    var b = el('button', 'ncu-iconbtn' + (opts.sm ? ' sm' : ''), icon(opts.icon));
    b.type = 'button';
    b.title = opts.title || '';
    b.addEventListener('click', function (e) { e.stopPropagation(); opts.onClick && opts.onClick(e); });
    return { el: b, setIcon: function (n) { b.innerHTML = icon(n); } };
  }

  /* ── MenuItem (sidebar row) ──────────────────────────── */
  function MenuItem(opts) {
    var b = el('button', 'ncu-menuitem', icon(opts.icon) + '<span>' + esc(opts.label) + '</span>');
    b.type = 'button';
    b.addEventListener('click', opts.onClick || function () {});
    return { el: b, setLabel: function (t) { b.querySelector('span').textContent = t; } };
  }

  /* ── Popover ─────────────────────────────────────────── */
  var _openPopovers = [];
  function closeAllPopovers() {
    _openPopovers.forEach(function (p) { p.destroy(); });
    _openPopovers = [];
  }
  document.addEventListener('click', function (e) {
    _openPopovers.slice().forEach(function (p) {
      if (!p.el.contains(e.target) && !p._trigger.contains(e.target)) p.destroy();
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAllPopovers();
  });

  function Popover(opts) {
    var panel = el('div', 'ncu-popover');
    panel.style.visibility = 'hidden';
    document.body.appendChild(panel);
    var api = {
      el: panel,
      _trigger: opts.trigger,
      destroy: function () {
        panel.remove();
        var i = _openPopovers.indexOf(api);
        if (i >= 0) _openPopovers.splice(i, 1);
        opts.onClose && opts.onClose();
      },
    };
    _openPopovers.push(api);
    opts.render(panel, api);
    var r = opts.trigger.getBoundingClientRect();
    panel.style.visibility = '';
    var pw = panel.offsetWidth, ph = panel.offsetHeight;
    var left = opts.align === 'right' ? r.right - pw : r.left;
    left = Math.max(8, Math.min(left, window.innerWidth - pw - 8));
    var top = opts.below ? r.bottom + 8 : r.top - ph - 8;
    if (top < 8) top = r.bottom + 8;
    panel.style.left = left + 'px';
    panel.style.top = top + 'px';
    return api;
  }

  /* ── RadioMenu — boardui picker (flat items or collapsible provider groups) ── */
  function RadioMenu(opts) {
    var root = el('div', 'ncu-radio-menu');
    var value = opts.value;
    var openGroups = {};
    (opts.groups || []).forEach(function (g) { openGroups[g.key] = !!g.open; });

    function rowEl(item) {
      var row = el('button', 'ncu-menu-row' + (item.value === value ? ' on' : ''));
      row.type = 'button';
      row.innerHTML = '<span class="ncu-menu-label">' + esc(item.label || item.value) + '</span><span class="ncu-radio' + (item.value === value ? ' on' : '') + '"></span>';
      row.addEventListener('click', function () {
        var changed = item.value !== value;
        value = item.value;
        render();
        if (changed && opts.onChange) opts.onChange(item.value);
      });
      return row;
    }
    function groupEl(group) {
      var wrap = el('div', 'ncu-menu-group' + (openGroups[group.key] ? ' open' : ''));
      var head = el('button', 'ncu-group-head');
      head.type = 'button';
      head.innerHTML = '<span class="material-symbols-outlined ncu-group-chev">chevron_right</span><span class="ncu-group-title">' + esc(group.title || group.key) + '</span>';
      head.addEventListener('click', function () {
        openGroups[group.key] = !openGroups[group.key];
        wrap.classList.toggle('open', openGroups[group.key]);
      });
      wrap.appendChild(head);
      var body = el('div', 'ncu-group-body');
      (group.items || []).forEach(function (item) { body.appendChild(rowEl(item)); });
      wrap.appendChild(body);
      return wrap;
    }
    function render() {
      root.innerHTML = '';
      if (opts.title) root.appendChild(el('div', 'ncu-menu-title', esc(opts.title)));
      if (opts.groups && opts.groups.length) {
        opts.groups.forEach(function (group) { root.appendChild(groupEl(group)); });
      } else {
        (opts.items || []).forEach(function (item) { root.appendChild(rowEl(item)); });
      }
    }
    render();
    return {
      el: root,
      get: function () { return value; },
      set: function (v) { value = v; render(); },
    };
  }

  /* ── FolderMenu — boardui-style folder picker (icon + parent/name two-tone path) ── */
  function FolderMenu(opts) {
    var root = el('div', 'ncu-radio-menu');
    var value = opts.value;
    function render() {
      root.innerHTML = '';
      if (opts.title) root.appendChild(el('div', 'ncu-menu-title', esc(opts.title)));
      (opts.items || []).forEach(function (item) {
        var row = el('button', 'ncu-menu-row ncu-folder-row' + (item.value === value ? ' on' : ''));
        row.type = 'button';
        row.innerHTML =
          '<span class="material-symbols-outlined ncu-folder-icon">folder</span>' +
          '<span class="ncu-folder-path">' +
          (item.parent ? '<span class="ncu-folder-parent">' + esc(item.parent) + '</span>' : '') +
          '<span class="ncu-folder-name">' + esc(item.name || item.value) + '</span>' +
          '</span>';
        row.addEventListener('click', function () {
          var changed = item.value !== value;
          value = item.value;
          render();
          if (changed && opts.onChange) opts.onChange(item.value);
          else if (!changed && opts.onReselect) opts.onReselect(item.value);
        });
        root.appendChild(row);
      });
    }
    render();
    return {
      el: root,
      get: function () { return value; },
      set: function (v) { value = v; render(); },
    };
  }

  /* ── ActionMenu — boardui "Add/Plugins" grouped menu (icon + bold label + gray desc) ── */
  function ActionMenu(opts) {
    var root = el('div', 'ncu-action-menu');
    (opts.sections || []).forEach(function (section) {
      if (section.title) root.appendChild(el('div', 'ncu-menu-title', esc(section.title)));
      (section.items || []).forEach(function (item) {
        var row = el('button', 'ncu-action-row');
        row.type = 'button';
        row.innerHTML =
          '<span class="material-symbols-outlined ncu-action-icon">' + esc(item.icon || 'bolt') + '</span>' +
          '<span class="ncu-action-copy"><span class="ncu-action-label">' + esc(item.label || '') + '</span>' +
          (item.desc ? '<span class="ncu-action-desc">' + esc(item.desc) + '</span>' : '') +
          '</span>';
        row.addEventListener('click', function () {
          if (opts.closeOnClick !== false && opts.pop) opts.pop.destroy();
          if (item.onClick) item.onClick();
        });
        root.appendChild(row);
      });
    });
    return { el: root };
  }

  /* -- EffortSlider - boardui pill track, draggable, N levels --
     opts: { value, levels: ['quick','balanced','deep'], names: {quick:'Low',...}, onChange(key) } */
  var EFFORT_DEFAULT_NAMES = { low: 'Low', medium: 'Medium', high: 'High', very_high: 'Very High', quick: 'Low', balanced: 'Medium', deep: 'High', max: 'Very High' };
  function EffortSlider(opts) {
    var levels = (opts.levels && opts.levels.length ? opts.levels : ['low', 'medium', 'high', 'very_high']).slice();
    var names = opts.names || EFFORT_DEFAULT_NAMES;
    var idx = Math.max(0, levels.indexOf(opts.value));
    if (idx < 0) idx = Math.min(levels.length - 1, 1);
    var root = el('div', 'ncu-effort');
    var THUMB = 46, PAD = 2;

    function nameFor(i) {
      var k = levels[i];
      return names[k] || k.charAt(0).toUpperCase() + k.slice(1);
    }
    function levelFromEvent(e, track) {
      var r = track.getBoundingClientRect();
      var frac = Math.max(0, Math.min(1, (e.clientX - r.left - THUMB / 2) / Math.max(1, r.width - THUMB)));
      return Math.round(frac * (levels.length - 1));
    }
    function position() {
      var thumb = root.querySelector('.ncu-effort-thumb');
      if (!thumb) return;
      var frac = levels.length > 1 ? idx / (levels.length - 1) : 0;
      thumb.style.left = 'calc(' + PAD + 'px + (100% - ' + (THUMB + PAD * 2) + 'px) * ' + frac + ')';
    }
    function render() {
      root.setAttribute('data-level', idx);
      var ticks = levels.map(function () { return '<span></span>'; }).join('');
      root.innerHTML =
        '<div class="ncu-effort-head"><span class="ncu-effort-label">Effort</span><span class="ncu-effort-val">' + esc(nameFor(idx)) + '</span></div>' +
        '<div class="ncu-effort-ends"><span>Faster</span><span>Smarter</span></div>' +
        '<div class="ncu-effort-track">' +
        '<div class="ncu-effort-ticks">' + ticks + '</div>' +
        '<div class="ncu-effort-thumb"></div></div>';
      position();
      var track = root.querySelector('.ncu-effort-track');
      track.addEventListener('pointerdown', function (e) {
        e.preventDefault();
        if (track.setPointerCapture) { try { track.setPointerCapture(e.pointerId); } catch (err) {} }
        set(levelFromEvent(e, track));
        function move(ev) { set(levelFromEvent(ev, track), true); }
        function up() {
          track.removeEventListener('pointermove', move);
          track.removeEventListener('pointerup', up);
          track.removeEventListener('pointercancel', up);
        }
        track.addEventListener('pointermove', move);
        track.addEventListener('pointerup', up);
        track.addEventListener('pointercancel', up);
      });
    }
    function set(i, quiet) {
      idx = Math.max(0, Math.min(levels.length - 1, i));
      var headVal = root.querySelector('.ncu-effort-val');
      if (headVal) headVal.textContent = nameFor(idx);
      root.setAttribute('data-level', idx);
      position();
      if (!quiet && opts.onChange) opts.onChange(levels[idx]);
    }
    render();
    return { el: root, set: set, get: function () { return levels[idx]; } };
  }

  /* ── TurnStepsCard (BoardUI style live execution card) ── */
  function TurnStepsCard() {
    var root = el('div', 'nc-steps-card');
    root.hidden = true;
    root.innerHTML =
      '<div class="nc-steps-head">' +
      '<div class="nc-steps-status">' +
      '<span class="nc-steps-spin"></span>' +
      '<span class="nc-steps-count">Working…</span>' +
      '</div>' +
      '<button type="button" class="ncu-iconbtn sm nc-steps-min" title="Toggle steps"><span class="material-symbols-outlined" style="font-size:16px">remove</span></button>' +
      '</div>' +
      '<div class="nc-steps-body"></div>';
    var countEl = root.querySelector('.nc-steps-count');
    var minBtn = root.querySelector('.nc-steps-min');
    var body = root.querySelector('.nc-steps-body');

    minBtn.addEventListener('click', function () {
      body.hidden = !body.hidden;
      minBtn.querySelector('.material-symbols-outlined').textContent = body.hidden ? 'add' : 'remove';
    });

    return {
      el: root,
      body: body,
      setSteps: function (left, label) {
        root.hidden = false;
        countEl.textContent = (left != null ? left + ' step' + (left === 1 ? '' : 's') + ' left' : '') + (label ? ' · ' + label : '');
      },
      setStatus: function (label) {
        root.hidden = false;
        countEl.textContent = label || 'Working';
      },
      addStep: function (data) {
        root.hidden = false;
        var stepRow = el('div', 'nc-step-item running');
        stepRow.innerHTML =
          '<span class="nc-step-ic"><span class="ncu-spin sm"></span></span>' +
          '<span class="nc-step-txt">' + esc(data.label || data.tool) + '</span>';
        body.appendChild(stepRow);
        return {
          el: stepRow,
          resolve: function (res) {
            stepRow.className = 'nc-step-item ' + (res.ok ? 'done' : 'fail');
            stepRow.querySelector('.nc-step-ic').innerHTML =
              '<span class="material-symbols-outlined" style="font-size:15px;color:' + (res.ok ? 'var(--ncu-green)' : 'var(--ncu-red)') + '">' + (res.ok ? 'check_circle' : 'error') + '</span>';
          },
        };
      },
      reset: function () {
        body.innerHTML = '';
        root.hidden = true;
      },
    };
  }

  /* ── StatusPill ──────────────────────────────────────── */
  function StatusPill() {
    var pill = el('div', 'ncu-statuspill');
    pill.hidden = true;
    var spinner = el('span', 'ncu-spin');
    var left = el('span', '', '');
    var arrow = el('span', 'ncu-arrow', '&#8594;');
    var strong = el('span', 'ncu-strong');
    pill.appendChild(spinner); pill.appendChild(left); pill.appendChild(arrow); pill.appendChild(strong);
    return {
      el: pill,
      show: function (stepsLeft, label) {
        pill.hidden = false;
        left.textContent = stepsLeft == null ? '' : stepsLeft + ' steps left';
        arrow.style.display = label ? '' : 'none';
        strong.textContent = label || '';
        strong.style.display = label ? '' : 'none';
      },
      hide: function () { pill.hidden = true; },
    };
  }

  /* ── ThinkingLine ────────────────────────────────────── */
  function ThinkingLine() {
    var root = el('div', 'ncu-thinking');
    root.innerHTML = '<span class="ncu-inf"></span><span class="ncu-label">Thinking</span><span class="ncu-secs"></span>';
    var label = root.querySelector('.ncu-label');
    var secs = root.querySelector('.ncu-secs');
    var t0 = 0, timer = null;
    function tick() {
      var s = (performance.now() - t0) / 1000;
      secs.textContent = s >= 10 ? s.toFixed(0) + 's' : s.toFixed(1) + 's';
    }
    return {
      el: root,
      start: function (text) {
        label.textContent = text || 'Thinking';
        t0 = performance.now();
        tick();
        root.hidden = false;
        clearInterval(timer);
        timer = setInterval(tick, 100);
      },
      stop: function () { clearInterval(timer); timer = null; root.hidden = true; },
    };
  }

  /* ── ProgressRing ────────────────────────────────────── */
  function ProgressRing(opts) {
    var size = opts.size || 26, sw = 2.5;
    var r = (size - sw) / 2, c = 2 * Math.PI * r;
    var root = el('div', 'ncu-ring');
    root.innerHTML =
      '<svg width="' + size + '" height="' + size + '">' +
      '<circle class="ncu-ring-bg" cx="' + size / 2 + '" cy="' + size / 2 + '" r="' + r + '" fill="none" stroke-width="' + sw + '"/>' +
      '<circle class="ncu-ring-fg" cx="' + size / 2 + '" cy="' + size / 2 + '" r="' + r + '" fill="none" stroke-width="' + sw +
      '" stroke-linecap="round" stroke-dasharray="' + c + '" stroke-dashoffset="' + c + '"/></svg>' +
      '<span class="ncu-ring-txt">0%</span>';
    var fg = root.querySelector('.ncu-ring-fg');
    var txt = root.querySelector('.ncu-ring-txt');
    return {
      el: root,
      set: function (pct) {
        pct = Math.max(0, Math.min(100, pct | 0));
        fg.style.strokeDashoffset = c * (1 - pct / 100);
        txt.textContent = pct + '%';
        root.style.display = pct === 0 ? 'none' : '';
      },
    };
  }

  /* ── ToolChip ────────────────────────────────────────── */
  var TOOL_ICONS = {
    list_dir: 'folder_open', read_file: 'description', write_file: 'edit_note',
    append_file: 'playlist_add', delete_path: 'delete', make_dirs: 'create_new_folder',
    search_files: 'search', run_command: 'terminal',
  };
  function ToolChip(data) {
    var chip = el('button', 'ncu-toolchip');
    chip.type = 'button';
    chip.innerHTML = icon(TOOL_ICONS[data.tool] || 'bolt') +
      '<span class="t-label">' + esc(data.label || data.tool) + '</span><span class="t-state">running</span>';
    var det = el('div', 'ncu-tooldetail');
    det.hidden = true;
    chip.addEventListener('click', function () { det.hidden = !det.hidden; });
    var wrap = el('div', '');
    wrap.style.display = 'contents';
    wrap.appendChild(chip);
    wrap.appendChild(det);
    return {
      el: wrap,
      resolve: function (res) {
        chip.classList.add(res.ok ? 'ok' : 'fail');
        chip.querySelector('.t-state').textContent = res.ok ? 'done' : 'failed';
        var lines = [res.summary || '', res.error ? 'error: ' + res.error : ''].filter(Boolean).join('\n');
        det.textContent = lines.slice(0, 4000);
      },
    };
  }

  /* ── Toast / Modal ───────────────────────────────────── */
  function toast(msg) {
    if (!msg) return;
    var t = el('div', 'ncu-toast', esc(typeof msg === 'string' ? msg : msg.message || 'Something went wrong'));
    document.body.appendChild(t);
    setTimeout(function () { t.classList.add('show'); }, 10);
    setTimeout(function () { t.classList.remove('show'); setTimeout(function () { t.remove(); }, 300); }, 3800);
  }

  function Modal(opts) {
    var scrim = el('div', 'ncu-modal-scrim');
    scrim.hidden = true;
    var box = el('div', 'ncu-modal');
    box.innerHTML = '<h3>' + esc(opts.title || '') + '</h3>';
    if (opts.subtitle) box.appendChild(el('p', 'ncu-modal-sub', opts.subtitle));
    var body = el('div', 'ncu-modal-body');
    box.appendChild(body);
    scrim.appendChild(box);
    document.body.appendChild(scrim);
    scrim.addEventListener('click', function (e) { if (e.target === scrim) api.close(); });
    var api = {
      el: scrim, body: body,
      open: function () { scrim.hidden = false; opts.onOpen && opts.onOpen(body); },
      close: function () { scrim.hidden = true; opts.onClose && opts.onClose(); },
    };
    return api;
  }

  /* ── Search box ──────────────────────────────────────── */
  function SearchBox(opts) {
    var wrap = el('div', 'ncu-search', icon('search') );
    var input = document.createElement('input');
    input.placeholder = opts.placeholder || 'Quick Search';
    var kbd = el('span', 'ncu-kbd', opts.kbd || '&#8984;L');
    wrap.appendChild(input);
    wrap.appendChild(kbd);
    input.addEventListener('input', function () { opts.onFilter && opts.onFilter(input.value); });
    if (opts.hotkey) {
      document.addEventListener('keydown', function (e) {
        if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'l') {
          e.preventDefault();
          input.focus();
        }
      });
    }
    return { el: wrap, input: input };
  }

  /* ── ThemeToggle ─────────────────────────────────────── */
  function ThemeToggle(app) {
    var wrap = el('div', 'ncu-themetoggle');
    function mk(n, ic) {
      var b = el('button', 'ncu-iconbtn sm', icon(ic));
      b.type = 'button';
      b.addEventListener('click', function () { apply(n); });
      return b;
    }
    var sun = mk('light', 'light_mode');
    var moon = mk('dark', 'dark_mode');
    wrap.appendChild(sun); wrap.appendChild(moon);
    function apply(n) {
      app.setAttribute('data-theme', n);
      try { localStorage.setItem('nc-theme', n); } catch (e) {}
    }
    try {
      var saved = localStorage.getItem('nc-theme');
      if (saved) app.setAttribute('data-theme', saved);
    } catch (e) {}
    return { el: wrap };
  }

  window.CodeUI = {
    el: el, esc: esc, icon: icon,
    IconButton: IconButton, MenuItem: MenuItem, Popover: Popover, closeAllPopovers: closeAllPopovers,
    RadioMenu: RadioMenu, FolderMenu: FolderMenu, ActionMenu: ActionMenu, EffortSlider: EffortSlider, StatusPill: StatusPill, TurnStepsCard: TurnStepsCard,
    ThinkingLine: ThinkingLine, ProgressRing: ProgressRing, ToolChip: ToolChip,
    toast: toast, Modal: Modal, SearchBox: SearchBox, ThemeToggle: ThemeToggle,
    TOOL_ICONS: TOOL_ICONS,
  };
})();
