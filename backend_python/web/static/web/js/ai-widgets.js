/* ── AI Widgets — reusable vanilla UI components for AI surfaces ──────────────
 * PixelLoader  3x3 pixel-grid loader (beautifului port): drive/dots/orbit
 * Trace        expandable agent trace (ThinkingState port): steps/reasoning/
 *              search/coding — shimmer header, growing rail, staggered rows
 * StreamingText  word-by-word blur resolve, inline citation chips, action row
 * streamSSE    fetch() + ReadableStream SSE reader (avatar-lab technique)
 *
 * Every widget is self-contained: returns { el, ... } so any surface (Neby
 * assistant, background agent, future chat UIs) can embed it.
 * ──────────────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var WORD_MS = 55;

  function escapeHtml(str) {
    if (str === undefined || str === null) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  function formatElapsed(ms) {
    var s = ms / 1000;
    if (s < 60) return s.toFixed(1) + 's';
    var m = Math.floor(s / 60);
    var sec = Math.floor(s % 60);
    return m + 'm ' + sec + 's';
  }

  /* ── PixelLoader ─────────────────────────────────────────────────────────── */
  function pixelGridCells(variant) {
    var cells = [];
    if (variant === 'orbit') {
      var order = [0, 1, 2, 5, 8, 7, 6, 3];
      for (var i = 0; i < 9; i++) {
        var idx = order.indexOf(i);
        cells.push(idx === -1 ? null : idx * 110);
      }
    } else {
      for (var r = 0; r < 3; r++) {
        for (var c = 0; c < 3; c++) {
          cells.push((c + Math.abs(r - 1)) * 90);
        }
      }
    }
    return cells;
  }

  function pixelGridHtml(variant) {
    var cells = pixelGridCells(variant);
    return cells.map(function (d) {
      if (d === null) return '<span class="ai-px-cell dim"></span>';
      return '<span class="ai-px-cell" style="animation-delay:' + d + 'ms"></span>';
    }).join('');
  }

  function PixelLoader(opts) {
    opts = opts || {};
    var label = opts.label || 'Thinking';
    var variant = opts.variant || 'drive';
    var startedAt = Date.now();
    var timer = null;

    var el = document.createElement('div');
    el.className = 'ai-widget ai-pixel-loader';
    render();

    function render() {
      var v = variant;
      var dur = v === 'orbit' ? 950 : 650;
      el.innerHTML =
        '<div class="ai-px-grid' + (v === 'dots' ? ' dots' : '') + '" style="--dur:' + dur + 'ms">' + pixelGridHtml(v) + '</div>' +
        '<div class="ai-px-meta"><span class="ai-px-label">' + escapeHtml(label) + '</span>' +
        '<span class="ai-px-timer">0.0s</span></div>';
      if (opts.timer !== false) {
        if (timer) clearInterval(timer);
        timer = setInterval(function () {
          var t = el.querySelector('.ai-px-timer');
          if (t) t.textContent = formatElapsed(Date.now() - startedAt);
        }, 100);
      }
    }

    return {
      el: el,
      setLabel: function (nextLabel, nextVariant) {
        if (nextLabel) label = nextLabel;
        if (nextVariant) variant = nextVariant;
        render();
      },
      destroy: function () {
        if (timer) clearInterval(timer);
        if (el.parentNode) el.parentNode.removeChild(el);
      },
    };
  }

  /* ── Trace (ThinkingState port) ──────────────────────────────────────────── */
  var TONES = ['ai-dot-accent', 'ai-dot-orange', 'ai-dot-green'];
  var AUTO_SETTLE_MS = 8000;

  function starSvg() {
    return '<svg class="ai-trace-star" width="16" height="16" viewBox="0 0 24 24"><path d="M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z"/></svg>';
  }
  function chevronSvg() {
    return '<svg class="ai-trace-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>';
  }
  function checkSvg() {
    return '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>';
  }
  function searchSvg() {
    return '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>';
  }
  function dotSvg(tone) {
    return '<span class="ai-trace-dot ' + tone + '"><svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="9"/><path d="M3.5 12h17M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg></span>';
  }

  function renderTraceRow(variant, row, i, working, shown) {
    var parts = [];
    if (variant === 'search') parts.push(dotSvg(TONES[i % TONES.length]));
    if (variant === 'steps') {
      if (working && i === shown - 1) parts.push('<span class="ai-trace-spinner"></span>');
      else parts.push('<span style="color:var(--ai-ink-3);display:flex">' + checkSvg() + '</span>');
    }
    parts.push('<span class="ai-trace-primary">' + escapeHtml(row.primary) + '</span>');
    if (row.secondary) {
      parts.push('<span class="ai-trace-secondary' + (row.mono ? ' mono' : '') + '">' + escapeHtml(row.secondary) + '</span>');
    }
    if (row.add !== undefined && row.del !== undefined) {
      parts.push('<span class="ai-trace-diff"><span class="ai-trace-add">+' + row.add + '</span> <span class="ai-trace-del">\u2212' + row.del + '</span></span>');
    }
    var style = 'animation:ai-fade-up 320ms cubic-bezier(.23,1,.32,1) ' + (i * 120) + 'ms both';
    var baseClass = 'ai-trace-row' + (variant === 'reasoning' ? ' reasoning' : '');
    if (variant === 'search' && row.href) {
      return '<a class="' + baseClass + '" href="' + escapeHtml(row.href) + '" target="_blank" rel="noreferrer" style="' + style + '">' + parts.join('') + '</a>';
    }
    if (variant === 'coding') {
      return '<button type="button" class="' + baseClass + '" data-tool="' + escapeHtml(row.primary) + '" aria-pressed="false" style="' + style + '">' + parts.join('') + '</button>';
    }
    return '<div class="' + baseClass + '" style="' + style + '">' + parts.join('') + '</div>';
  }

  function Trace(opts) {
    opts = opts || {};
    var variant = opts.variant || 'steps';
    var rows = opts.rows || [];
    var query = opts.query || '';
    var working = true;
    var expanded = true;
    var manual = null;
    var settled = false;
    var autoTimer = null;
    var total = rows.length;

    var el = document.createElement('div');
    el.className = 'ai-widget ai-trace expanded';
    el.innerHTML =
      '<button type="button" class="ai-trace-header working" aria-expanded="true">' +
      starSvg() +
      '<span class="ai-trace-label working">' + escapeHtml(opts.active || 'Thinking') + '</span>' +
      chevronSvg() +
      '</button>' +
      '<div class="ai-trace-collapse"><div class="ai-trace-clip"><div class="ai-trace-track">' +
      '<span class="ai-trace-line"></span>' +
      '<div class="ai-trace-rows"></div>' +
      '</div></div></div>';

    var headerEl = el.querySelector('.ai-trace-header');
    var labelEl = el.querySelector('.ai-trace-label');
    var rowsEl = el.querySelector('.ai-trace-rows');
    var lineEl = el.querySelector('.ai-trace-line');

    function measure() {
      requestAnimationFrame(function () {
        lineEl.style.height = (rowsEl.offsetHeight > 0 ? rowsEl.offsetHeight - 2 : 0) + 'px';
      });
    }

    function renderRows() {
      var html = '';
      if (variant === 'search' && query) {
        html += '<div class="ai-trace-query">' + searchSvg() + '<span>' + escapeHtml(query) + '</span></div>';
      }
      var shown = variant === 'search' ? Math.min(3, rows.length) : rows.length;
      rows.slice(0, shown).forEach(function (row, i) {
        html += renderTraceRow(variant, row, i, working, shown);
      });
      if (variant === 'search' && settled && total > shown) {
        html += '<span class="ai-trace-more">+' + (total - shown) + ' more</span>';
      }
      rowsEl.innerHTML = html;
      if (variant === 'coding') {
        rowsEl.querySelectorAll('button[data-tool]').forEach(function (btn) {
          btn.addEventListener('click', function () {
            var sel = btn.classList.contains('selected');
            btn.classList.toggle('selected', !sel);
            btn.setAttribute('aria-pressed', String(!sel));
          });
        });
      }
      measure();
    }

    function settle(doneText, newRows, newTotal) {
      if (settled) return;
      settled = true;
      working = false;
      if (autoTimer) { clearTimeout(autoTimer); autoTimer = null; }
      if (newRows) rows = newRows;
      if (typeof newTotal === 'number') total = newTotal;
      headerEl.classList.remove('working');
      headerEl.classList.add('done');
      labelEl.classList.remove('working');
      labelEl.classList.add('done');
      labelEl.textContent = doneText || opts.done || 'Done';
      renderRows();
    }

    headerEl.addEventListener('click', function () {
      manual = !(manual !== null ? manual : true);
      expanded = manual;
      el.classList.toggle('expanded', expanded);
      headerEl.setAttribute('aria-expanded', String(expanded));
      if (expanded) measure();
    });

    renderRows();
    autoTimer = setTimeout(function () { settle(); }, opts.settleDelay || AUTO_SETTLE_MS);

    return {
      el: el,
      settle: settle,
      destroy: function () {
        if (autoTimer) clearTimeout(autoTimer);
        if (el.parentNode) el.parentNode.removeChild(el);
      },
    };
  }

  /* ── StreamingText ───────────────────────────────────────────────────────── */
  function streamSvg() {
    return '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' +
      '<rect x="9" y="9" width="12" height="12" rx="2.5"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
  }
  function retrySvg() {
    return '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-2.64-6.36M21 3v6h-6"/></svg>';
  }
  function thumbsSvg(up) {
    return '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' +
      (up
        ? '<path d="M7 10v12M15 5.88L14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2a3.13 3.13 0 0 1 3 3.88z"/>'
        : '<path d="M17 14V2M9 18.12L10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H20a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.76a2 2 0 0 0-1.79 1.11L12 22a3.13 3.13 0 0 1-3-3.88z"/>');
  }

  function StreamingText(opts) {
    opts = opts || {};
    var text = String(opts.text || '');
    var wordMs = typeof opts.wordMs === 'number' ? opts.wordMs : WORD_MS;
    var sources = opts.sources || [];
    var citeAfter = typeof opts.citeAfter === 'number' ? opts.citeAfter : -1;
    var showActions = !!opts.actions;
    var onDone = opts.onDone;
    var words = text.split(/\s+/).filter(Boolean);
    var count = 0;
    var done = false;
    var timer = null;

    var el = document.createElement('div');
    el.className = 'ai-widget ai-stream';
    el.innerHTML =
      '<p class="ai-stream-text"><span class="ai-stream-words"></span><span class="ai-stream-cursor"></span></p>' +
      '<div class="ai-stream-actions" hidden>' +
      '<button type="button" class="ai-stream-action" data-action="copy" aria-label="Copy">' + streamSvg() + '</button>' +
      '<button type="button" class="ai-stream-action" data-action="retry" aria-label="Retry">' + retrySvg() + '</button>' +
      '<button type="button" class="ai-stream-action" data-action="up" aria-label="Helpful">' + thumbsSvg(true) + '</button>' +
      '<button type="button" class="ai-stream-action" data-action="down" aria-label="Not helpful">' + thumbsSvg(false) + '</button>' +
      (sources.length ? '<button type="button" class="ai-stream-sources-btn" aria-expanded="false"><span class="ai-stream-source-stack"></span><span class="ai-stream-sources-count"></span></button>' : '') +
      '</div>' +
      (sources.length ? '<div class="ai-stream-sources"><div class="ai-stream-sources-list"></div></div>' : '');

    var wordsEl = el.querySelector('.ai-stream-words');
    var cursorEl = el.querySelector('.ai-stream-cursor');
    var actionsEl = el.querySelector('.ai-stream-actions');
    var sourcesEl = el.querySelector('.ai-stream-sources');
    var sourcesBtn = el.querySelector('.ai-stream-sources-btn');

    if (sources.length) {
      var stack = el.querySelector('.ai-stream-source-stack');
      stack.innerHTML = sources.slice(0, 3).map(function (s) {
        return '<img src="' + escapeHtml(s.image || '') + '" alt="" class="ai-stream-source-avatar">';
      }).join('');
      el.querySelector('.ai-stream-sources-count').textContent = sources.length + ' source' + (sources.length === 1 ? '' : 's');
      var list = el.querySelector('.ai-stream-sources-list');
      list.innerHTML = sources.map(function (s) {
        return '<a href="' + escapeHtml(s.href || '#') + '" target="_blank" rel="noreferrer" class="ai-stream-source-row">' +
          '<img src="' + escapeHtml(s.image || '') + '" alt="" class="ai-stream-source-icon">' +
          '<span class="ai-stream-source-name">' + escapeHtml(s.name || s.domain || '') + '</span>' +
          '<span class="ai-stream-source-domain">' + escapeHtml(s.domain || '') + '</span></a>';
      }).join('');
      if (sourcesBtn) {
        sourcesBtn.addEventListener('click', function () {
          var open = sourcesEl.classList.toggle('open');
          sourcesBtn.setAttribute('aria-expanded', String(open));
        });
      }
    }

    function citeChip(source) {
      return '<a href="' + escapeHtml(source.href || '#') + '" target="_blank" rel="noreferrer" class="ai-stream-cite">' +
        (source.image ? '<img src="' + escapeHtml(source.image) + '" alt="" class="ai-stream-cite-img">' : '') +
        '<span>' + escapeHtml(source.domain || source.name || 'source') + '</span></a>';
    }

    function tick() {
      if (done) return;
      if (count >= words.length) { finish(); return; }
      var html = '';
      for (var i = 0; i < count; i++) {
        html += '<span class="ai-stream-word" style="animation-delay:' + (i * 12) + 'ms">' + escapeHtml(words[i]) + '</span> ';
      }
      if (citeAfter >= 0 && count === citeAfter && sources.length) html += citeChip(sources[0]);
      wordsEl.innerHTML = html + '<span class="ai-stream-word" style="animation-delay:0ms">' + escapeHtml(words[count]) + '</span> ';
      count += 1;
      timer = setTimeout(tick, wordMs);
    }

    function finish() {
      done = true;
      clearTimeout(timer);
      var html = '';
      for (var i = 0; i < words.length; i++) {
        html += '<span class="ai-stream-word" style="animation-delay:' + (i * 12) + 'ms">' + escapeHtml(words[i]) + '</span> ';
      }
      if (citeAfter >= 0 && sources.length) html += citeChip(sources[0]);
      wordsEl.innerHTML = html;
      cursorEl.style.display = 'none';
      if (actionsEl) actionsEl.hidden = false;
      if (onDone) onDone();
    }

    actionsEl.addEventListener('click', function (event) {
      var btn = event.target.closest('.ai-stream-action');
      if (!btn) return;
      var action = btn.dataset.action;
      if (action === 'copy') {
        if (opts.onCopy) opts.onCopy(text);
        else if (navigator.clipboard) navigator.clipboard.writeText(text).then(function () { btn.classList.add('ai-stream-action-on'); setTimeout(function () { btn.classList.remove('ai-stream-action-on'); }, 1200); }).catch(function () {});
      } else if (action === 'retry' && opts.onRetry) opts.onRetry();
      else if (action === 'up' && opts.onVote) opts.onVote(1);
      else if (action === 'down' && opts.onVote) opts.onVote(-1);
    });

    if (!words.length) { finish(); }
    else { timer = setTimeout(tick, wordMs); }

    return {
      el: el,
      destroy: function () {
        clearTimeout(timer);
        if (el.parentNode) el.parentNode.removeChild(el);
      },
      get done() { return done; },
    };
  }

  /* ── streamSSE (avatar-lab technique) ────────────────────────────────────── */
  function streamSSE(url, callbacks) {
    callbacks = callbacks || {};
    var controller = typeof AbortController !== 'undefined' ? new AbortController() : null;

    function handle(event) {
      if (!event || typeof event !== 'object') return;
      if (event.type === 'text' && callbacks.onText) callbacks.onText(String(event.content || ''));
      else if (event.type === 'thought' && callbacks.onThought) callbacks.onThought(String(event.content || ''));
      else if (event.type === 'error') { if (callbacks.onError) callbacks.onError(event.message || 'stream error'); }
      else if (event.type === 'done') { if (callbacks.onDone) callbacks.onDone(event); }
      else if (callbacks.onEvent) callbacks.onEvent(event);
    }

    function pump(reader, decoder) {
      var buffer = '';
      function read() {
        return reader.read().then(function (result) {
          if (result.done) { if (callbacks.onDone) callbacks.onDone(); return; }
          buffer += decoder.decode(result.value, { stream: true });
          var lines = buffer.split('\n');
          buffer = lines.pop() || '';
          lines.forEach(function (line) {
            var trimmed = line.trim();
            if (!trimmed.startsWith('data:')) return;
            var raw = trimmed.slice(5).trim();
            if (!raw || raw === '[DONE]') { if (callbacks.onDone) callbacks.onDone(); return; }
            try { handle(JSON.parse(raw)); } catch (e) { /* partial frame */ }
          });
          return read();
        });
      }
      return read();
    }

    fetch(url, {
      headers: { 'Accept': 'text/event-stream' },
      credentials: 'same-origin',
      signal: controller ? controller.signal : undefined,
    })
      .then(function (res) {
        if (!res.ok || !res.body) throw new Error('stream unavailable (' + res.status + ')');
        return pump(res.body.getReader(), new TextDecoder());
      })
      .catch(function (err) {
        if (!controller || err.name !== 'AbortError') {
          if (callbacks.onError) callbacks.onError(err && err.message ? err.message : 'stream failed');
        }
      });

    return {
      abort: function () { if (controller) controller.abort(); },
    };
  }

  PixelLoader.create = PixelLoader;
  Trace.create = Trace;
  StreamingText.create = StreamingText;

  window.AIWidgets = {
    PixelLoader: PixelLoader,
    Trace: Trace,
    StreamingText: StreamingText,
    streamSSE: streamSSE,
    escapeHtml: escapeHtml,
  };
})();