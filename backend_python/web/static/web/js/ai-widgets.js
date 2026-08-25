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

    function setRows(nextRows) {
      if (settled) return;
      rows = nextRows || [];
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
      setRows: setRows,
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

  function buildActions(text, opts) {
    opts = opts || {};
    var actionsEl = document.createElement('div');
    actionsEl.className = 'ai-stream-actions';
    actionsEl.hidden = true;
    actionsEl.innerHTML =
      '<button type="button" class="ai-stream-action" data-action="copy" aria-label="Copy" title="Copy">' + streamSvg() + '</button>';
    actionsEl.addEventListener('click', function (event) {
      var btn = event.target.closest('.ai-stream-action');
      if (!btn) return;
      var action = btn.dataset.action;
      if (action === 'copy') {
        if (opts.onCopy) opts.onCopy(text);
        else if (navigator.clipboard) navigator.clipboard.writeText(text).then(function () {
          btn.classList.add('ai-stream-action-on');
          setTimeout(function () { btn.classList.remove('ai-stream-action-on'); }, 1200);
        }).catch(function () {});
      }
    });
    return actionsEl;
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
      (sources.length ? '<div class="ai-stream-sources"><div class="ai-stream-sources-list"></div></div>' : '');

    var wordsEl = el.querySelector('.ai-stream-words');
    var cursorEl = el.querySelector('.ai-stream-cursor');
    var sourcesEl = el.querySelector('.ai-stream-sources');
    var actionsEl = null;
    if (showActions) {
      actionsEl = buildActions(text, opts);
      el.appendChild(actionsEl);
    }

    if (sources.length) {
      var sourcesBtn = document.createElement('button');
      sourcesBtn.type = 'button';
      sourcesBtn.className = 'ai-stream-sources-btn';
      sourcesBtn.setAttribute('aria-expanded', 'false');
      sourcesBtn.innerHTML = '<span class="ai-stream-source-stack"></span><span class="ai-stream-sources-count"></span>';
      if (actionsEl) actionsEl.appendChild(sourcesBtn);
      else el.appendChild(sourcesBtn);
      sourcesBtn.querySelector('.ai-stream-source-stack').innerHTML = sources.slice(0, 3).map(function (s) {
        return '<img src="' + escapeHtml(s.image || '') + '" alt="" class="ai-stream-source-avatar">';
      }).join('');
      sourcesBtn.querySelector('.ai-stream-sources-count').textContent = sources.length + ' source' + (sources.length === 1 ? '' : 's');
      var list = el.querySelector('.ai-stream-sources-list');
      list.innerHTML = sources.map(function (s) {
        return '<a href="' + escapeHtml(s.href || '#') + '" target="_blank" rel="noreferrer" class="ai-stream-source-row">' +
          '<img src="' + escapeHtml(s.image || '') + '" alt="" class="ai-stream-source-icon">' +
          '<span class="ai-stream-source-name">' + escapeHtml(s.name || s.domain || '') + '</span>' +
          '<span class="ai-stream-source-domain">' + escapeHtml(s.domain || '') + '</span></a>';
      }).join('');
      sourcesBtn.addEventListener('click', function () {
        var open = sourcesEl.classList.toggle('open');
        sourcesBtn.setAttribute('aria-expanded', String(open));
      });
    }

    function citeChip(source) {
      return '<a href="' + escapeHtml(source.href || '#') + '" target="_blank" rel="noreferrer" class="ai-stream-cite">' +
        (source.image ? '<img src="' + escapeHtml(source.image) + '" alt="" class="ai-stream-cite-img">' : '') +
        '<span>' + escapeHtml(source.domain || source.name || 'source') + '</span></a>';
    }

    function tick() {
      if (done) return;
      if (count >= words.length) { finish(); return; }
      var span = document.createElement('span');
      span.className = 'ai-stream-word';
      span.textContent = words[count] + ' ';
      wordsEl.appendChild(span);

      if (citeAfter >= 0 && count === citeAfter && sources.length) {
        var chipContainer = document.createElement('span');
        chipContainer.innerHTML = citeChip(sources[0]) + ' ';
        wordsEl.appendChild(chipContainer);
      }
      count += 1;
      timer = setTimeout(tick, wordMs);
    }

    function finish() {
      done = true;
      clearTimeout(timer);
      while (count < words.length) {
        var span = document.createElement('span');
        span.className = 'ai-stream-word';
        span.textContent = words[count] + ' ';
        wordsEl.appendChild(span);
        count += 1;
      }
      if (citeAfter >= 0 && sources.length && !wordsEl.querySelector('.ai-stream-cite')) {
        var chipContainer = document.createElement('span');
        chipContainer.innerHTML = citeChip(sources[0]) + ' ';
        wordsEl.appendChild(chipContainer);
      }
      cursorEl.style.display = 'none';
      if (actionsEl) actionsEl.hidden = false;
      if (onDone) onDone();
    }

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
  function streamSSE(url, opts) {
    opts = opts || {};
    var callbacks = opts.onEvent || opts;
    var controller = typeof AbortController !== 'undefined' ? new AbortController() : null;

    function handle(event) {
      if (!event || typeof event !== 'object') return;
      if (callbacks.onText && event.type === 'text') callbacks.onText(String(event.content || ''));
      else if (callbacks.onThought && event.type === 'thought') callbacks.onThought(String(event.content || ''));
      else if (callbacks.onError && event.type === 'error') callbacks.onError(event.message || 'stream error');
      else if (callbacks.onDone && event.type === 'done') callbacks.onDone(event);
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

    var init = {
      headers: opts.headers || { 'Accept': 'text/event-stream' },
      credentials: opts.credentials || 'same-origin',
      signal: controller ? controller.signal : undefined,
    };
    if (opts.method) init.method = opts.method;
    if (opts.body !== undefined) init.body = opts.body;

    fetch(url, init)
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

  /* ── ApprovalCard ──────────────────────────────────────────────────────── */
  function ApprovalCard(opts) {
    opts = opts || {};
    var questions = opts.questions || [];
    var onSubmit = opts.onSubmit || function () {};
    var onDismiss = opts.onDismiss || function () {};
    var title = opts.title || 'A few quick questions';
    var subtitle = opts.subtitle || '';

    var el = document.createElement('div');
    el.className = 'ai-widget ai-approval';
    var body = document.createElement('div');
    body.className = 'ai-approval-body';
    el.appendChild(body);

    var idx = 0;
    var answers = {};
    var custom = {};
    var sent = false;
    var timers = [];

    function currentAnswers() {
      var q = questions[idx];
      if (!q) return [];
      return Array.from(answers[q.q] || []);
    }

    function renderPill() {
      body.innerHTML =
        '<button type="button" class="ai-approval-pill">' +
        '<span class="ai-approval-pill-dot"></span>' +
        '<span class="ai-approval-pill-label">' + escapeHtml(title) + '</span>' +
        '<span class="ai-approval-pill-arrow">keyboard_arrow_up</span>' +
        '</button>';
      body.querySelector('.ai-approval-pill').addEventListener('click', function () { open(); });
    }

    function renderSent() {
      body.innerHTML =
        '<div class="ai-approval-sent">' +
        '<span class="ai-approval-sent-icon">check</span>' +
        '<div class="ai-approval-sent-title">Thanks for your feedback!</div>' +
        '<button type="button" class="ai-approval-restart">Start over</button>' +
        '</div>';
      body.querySelector('.ai-approval-restart').addEventListener('click', function () {
        reset();
        open();
      });
    }

    function renderQuestion() {
      var q = questions[idx];
      if (!q) { finish(); return; }
      var qAnswers = answers[q.q] || new Set();
      var isLast = idx === questions.length - 1;
      var answered = qAnswers.size > 0;

      var dots = '';
      for (var i = 0; i < questions.length; i++) {
        dots += '<span class="ai-approval-dot' + (i === idx ? ' ai-approval-dot-on' : '') + '"></span>';
      }
      var customVal = custom[q.q] || '';

      var optsHtml = (q.options || []).map(function (opt) {
        var selected = qAnswers.has(opt);
        var input = q.type === 'check'
          ? '<span class="ai-approval-opt-check' + (selected ? ' ai-approval-opt-check-on' : '') + '">' + (selected ? 'check' : '') + '</span>'
          : '<span class="ai-approval-opt-radio' + (selected ? ' ai-approval-opt-radio-on' : '') + '"></span>';
        return '<button type="button" class="ai-approval-opt' + (selected ? ' ai-approval-opt-on' : '') + '" data-opt="' + escapeHtml(opt) + '">' +
          input + '<span class="ai-approval-opt-text">' + escapeHtml(opt) + '</span></button>';
      }).join('');

      var inner =
        '<div class="ai-approval-head">' +
        '<div class="ai-approval-head-text"><div class="ai-approval-title">' + escapeHtml(title) + '</div>' +
        (subtitle ? '<div class="ai-approval-sub">' + escapeHtml(subtitle) + '</div>' : '') + '</div>' +
        '<button type="button" class="ai-approval-close" aria-label="Dismiss">close</button>' +
        '</div>' +
        '<div class="ai-approval-progress">' + dots + '</div>' +
        '<div class="ai-approval-q">' + escapeHtml(q.q) + '</div>' +
        '<div class="ai-approval-opts">' + optsHtml + '</div>' +
        (q.allowCustom ? '<input type="text" class="ai-approval-custom" placeholder="Other…" value="' + escapeHtml(customVal) + '">' : '') +
        '<div class="ai-approval-footer">' +
        (idx > 0 ? '<button type="button" class="ai-approval-prev">arrow_back</button>' : '') +
        '<div class="ai-approval-step">' + (idx + 1) + ' / ' + questions.length + '</div>' +
        (isLast
          ? '<button type="button" class="ai-approval-send' + (answered ? ' ai-approval-send-ready' : '') + '"' + (answered ? '' : ' disabled') + '>arrow_forward</button>'
          : '<button type="button" class="ai-approval-next' + (answered ? ' ai-approval-next-ready' : '') + '"' + (answered ? '' : ' disabled') + '>arrow_forward</button>') +
        '</div>';
      body.innerHTML = '<div class="ai-approval-card">' + inner + '</div>';

      body.querySelector('.ai-approval-close').addEventListener('click', function () { close(); });
      if (idx > 0) body.querySelector('.ai-approval-prev').addEventListener('click', function () {
        idx -= 1;
        renderQuestion();
      });
      var advanceBtn = body.querySelector(isLast ? '.ai-approval-send' : '.ai-approval-next');
      if (answered) advanceBtn.addEventListener('click', function () {
        if (isLast) finish();
        else { idx += 1; renderQuestion(); }
      });

      body.querySelectorAll('.ai-approval-opt').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var opt = btn.dataset.opt;
          if (q.type === 'check') {
            if (qAnswers.has(opt)) qAnswers.delete(opt);
            else qAnswers.add(opt);
          } else {
            qAnswers.clear();
            qAnswers.add(opt);
          }
          answers[q.q] = qAnswers;
          renderQuestion();
          if (q.type === 'radio') {
            timers.push(setTimeout(function () {
              if (isLast) finish();
              else { idx += 1; renderQuestion(); }
            }, 480));
          }
        });
      });

      var customInput = body.querySelector('.ai-approval-custom');
      if (customInput) {
        customInput.addEventListener('input', function () {
          custom[q.q] = customInput.value;
          if (customInput.value.trim()) {
            qAnswers.add(customInput.value.trim());
            answers[q.q] = qAnswers;
            var sendBtn = body.querySelector('.ai-approval-send');
            if (sendBtn) { sendBtn.disabled = false; sendBtn.classList.add('ai-approval-send-ready'); }
          }
        });
        customInput.addEventListener('keydown', function (event) {
          if (event.key === 'Enter' && customInput.value.trim()) {
            event.preventDefault();
            if (isLast) finish();
            else { idx += 1; renderQuestion(); }
          }
        });
      }
    }

    function finish() {
      if (sent) return;
      sent = true;
      var flat = {};
      Object.keys(answers).forEach(function (key) { flat[key] = Array.from(answers[key] || []); });
      onSubmit(flat, custom);
      renderSent();
    }

    function open() {
      if (sent) { reset(); }
      el.classList.add('ai-approval-open');
      renderQuestion();
    }

    function close() {
      el.classList.remove('ai-approval-open');
      renderPill();
      onDismiss();
    }

    function reset() {
      idx = 0;
      answers = {};
      custom = {};
      sent = false;
      timers.forEach(clearTimeout);
      timers = [];
    }

    renderPill();

    return {
      el: el,
      destroy: function () {
        timers.forEach(clearTimeout);
        if (el.parentNode) el.parentNode.removeChild(el);
      },
      open: open,
      close: close,
      reset: reset,
      get sent() { return sent; },
    };
  }

  /* ── ToolChips ──────────────────────────────────────────────────────────── */
  function chipsSvg(icon) {
    if (icon === 'think') {
      return '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z"/></svg>';
    }
    if (icon === 'write') {
      return '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.8 2.8 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5z"/></svg>';
    }
    if (icon === 'read') {
      return '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>';
    }
    return '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 17l6-5-6-5M12 19h8"/></svg>';
  }
  function chipsChevronSvg() {
    return '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>';
  }

  function ToolChips(opts) {
    opts = opts || {};
    var stepMs = typeof opts.stepMs === 'number' ? opts.stepMs : 700;
    var reveal = opts.reveal || 'stagger';
    var runOpen = opts.open !== false;
    var header = { calls: opts.calls || 0, messages: opts.messages || 0 };
    var rows = (opts.rows || []).slice();
    var diffs = (opts.diffs || []).slice();
    var moreCount = opts.more || 0;
    var shown = 0;
    var timer = null;
    var rowSeq = 0;
    if (!opts.calls && rows.length) header.calls = rows.length;

    var el = document.createElement('div');
    el.className = 'ai-widget ai-chips';
    el.innerHTML =
      '<button type="button" class="ai-chips-header" aria-expanded="' + (runOpen ? 'true' : 'false') + '">' +
      '<span class="ai-chips-header-chevron">' + chipsChevronSvg() + '</span>' +
      '<span class="ai-chips-header-text"></span>' +
      '</button>' +
      '<div class="ai-chips-grid" style="grid-template-rows:' + (runOpen ? '1fr' : '0fr') + ';opacity:' + (runOpen ? 1 : 0) + '">' +
      '<div class="ai-chips-clip">' +
      '<div class="ai-chips-rows"></div>' +
      '<div class="ai-chips-diffs" hidden></div>' +
      '</div></div>';

    var headerBtn = el.querySelector('.ai-chips-header');
    var headerText = el.querySelector('.ai-chips-header-text');
    var gridEl = el.querySelector('.ai-chips-grid');
    var rowsEl = el.querySelector('.ai-chips-rows');
    var diffsEl = el.querySelector('.ai-chips-diffs');
    var openRows = {};

    function headerLabel() {
      return header.calls + ' tool call' + (header.calls === 1 ? '' : 's') + ', ' + header.messages + ' message' + (header.messages === 1 ? '' : 's');
    }

    function renderHeader() {
      headerText.textContent = headerLabel();
    }

    function rowDetailHtml(row) {
      var lines = row.detail || [];
      if (!lines.length) return '';
      var mono = row.detailMono !== false ? ' ai-chips-detail-mono' : '';
      var html = '';
      lines.forEach(function (line) {
        var tone = line.tone === 'add' ? ' ai-chips-detail-line-add' : '';
        html += '<span class="ai-chips-detail-line' + tone + mono + '">' + escapeHtml(line.text) + '</span>';
      });
      return html;
    }

    function renderRow(row, animate) {
      row._id = 'r' + (rowSeq += 1);
      var wrap = document.createElement('div');
      wrap.className = 'ai-chips-row' + (row.error ? ' ai-chips-row-error' : '');
      if (animate) wrap.style.animation = 'ai-fade-up 300ms cubic-bezier(0.23,1,0.32,1) both';
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'ai-chips-row-btn';
      btn.setAttribute('aria-expanded', 'false');
      var icon = chipsSvg(row.icon || 'run');
      btn.innerHTML =
        '<span class="ai-chips-row-icon">' +
        '<span class="ai-chips-row-icon-main">' + icon + '</span>' +
        '<span class="ai-chips-row-chevron">' + chipsChevronSvg() + '</span>' +
        '</span>' +
        '<span class="ai-chips-row-label">' + escapeHtml(row.label || '') + '</span>' +
        '<span class="ai-chips-chip' + (row.mono === false ? '' : ' ai-chips-chip-mono') + '">' + escapeHtml(row.chip || '') + '</span>';
      var detail = document.createElement('div');
      detail.className = 'ai-chips-row-detail';
      detail.style.gridTemplateRows = '0fr';
      detail.style.opacity = '0';
      detail.innerHTML = '<div class="ai-chips-row-detail-clip"><div class="ai-chips-row-detail-lines">' +
        rowDetailHtml(row) + '</div></div>';
      btn.addEventListener('click', function () {
        var isOpen = !!openRows[row._id];
        openRows[row._id] = !isOpen;
        btn.setAttribute('aria-expanded', String(!isOpen));
        var chevron = btn.querySelector('.ai-chips-row-chevron');
        if (chevron) chevron.style.transform = !isOpen ? 'rotate(0deg)' : 'rotate(-90deg)';
        detail.style.gridTemplateRows = !isOpen ? '1fr' : '0fr';
        detail.style.opacity = !isOpen ? '1' : '0';
      });
      wrap.appendChild(btn);
      wrap.appendChild(detail);
      rowsEl.appendChild(wrap);
    }

    function maybeShowDiffs() {
      if (diffsEl.hidden) return;
      if (reveal === 'stagger' && shown < rows.length) return;
      diffsEl.hidden = false;
      diffsEl.innerHTML = '';
      diffs.forEach(function (d, i) {
        var chip = document.createElement('span');
        chip.className = 'ai-chips-diff';
        chip.style.animation = 'ai-pop-in 250ms cubic-bezier(0.23,1,0.32,1) ' + (i * 80) + 'ms both';
        var add = typeof d.add === 'number' && d.add > 0 ? '<span class="ai-chips-diff-add">+' + d.add + '</span>' : '';
        var del = typeof d.del === 'number' && d.del > 0 ? '<span class="ai-chips-diff-del">\u2212' + d.del + '</span>' : '';
        chip.innerHTML = '<span class="ai-chips-diff-file">' + escapeHtml(d.file) + '</span>' + add + del;
        diffsEl.appendChild(chip);
      });
      if (moreCount > 0) {
        var moreBtn = document.createElement('button');
        moreBtn.type = 'button';
        moreBtn.className = 'ai-chips-more';
        moreBtn.style.animation = 'ai-fade-in 300ms ease-out ' + (diffs.length * 80) + 'ms both';
        moreBtn.textContent = '+' + moreCount + ' more';
        moreBtn.addEventListener('click', function () {
          var extra = rows.splice(shown, moreCount);
          extra.forEach(function (row) { renderRow(row, true); shown += 1; });
          header.calls += extra.length;
          renderHeader();
          moreCount = 0;
          moreBtn.remove();
          maybeShowDiffs();
        });
        diffsEl.appendChild(moreBtn);
      }
    }

    function scheduleReveal() {
      if (reveal !== 'stagger' || shown >= rows.length) return;
      clearTimeout(timer);
      timer = setTimeout(function () {
        renderRow(rows[shown], true);
        shown += 1;
        renderHeader();
        maybeShowDiffs();
        scheduleReveal();
      }, stepMs);
    }

    function renderAll() {
      while (shown < rows.length) { renderRow(rows[shown], false); shown += 1; }
      renderHeader();
      maybeShowDiffs();
    }

    headerBtn.addEventListener('click', function () {
      runOpen = !runOpen;
      gridEl.style.gridTemplateRows = runOpen ? '1fr' : '0fr';
      gridEl.style.opacity = runOpen ? '1' : '0';
      headerBtn.setAttribute('aria-expanded', String(runOpen));
      var chevron = headerBtn.querySelector('.ai-chips-header-chevron svg');
      if (chevron) chevron.style.transform = runOpen ? 'rotate(0deg)' : 'rotate(-90deg)';
    });

    renderHeader();
    if (reveal === 'stagger') scheduleReveal();
    else renderAll();

    return {
      el: el,
      destroy: function () {
        clearTimeout(timer);
        if (el.parentNode) el.parentNode.removeChild(el);
      },
      addRow: function (row) {
        rows.push(row || {});
        header.calls += 1;
        if (reveal === 'stagger') { renderHeader(); scheduleReveal(); }
        else renderAll();
      },
      addRows: function (list) {
        (list || []).forEach(function (row) { rows.push(row || {}); header.calls += 1; });
        if (reveal === 'stagger') { renderHeader(); scheduleReveal(); }
        else renderAll();
      },
      setDiffs: function (list, more) {
        diffs = (list || []).slice();
        if (typeof more === 'number') moreCount = more;
        maybeShowDiffs();
      },
      setHeader: function (calls, messages) {
        if (typeof calls === 'number') header.calls = calls;
        if (typeof messages === 'number') header.messages = messages;
        renderHeader();
      },
      open: function () { runOpen = true; gridEl.style.gridTemplateRows = '1fr'; gridEl.style.opacity = '1'; headerBtn.setAttribute('aria-expanded', 'true'); },
      close: function () { runOpen = false; gridEl.style.gridTemplateRows = '0fr'; gridEl.style.opacity = '0'; headerBtn.setAttribute('aria-expanded', 'false'); },
      toggle: function () { runOpen ? this.close() : this.open(); },
      revealAll: renderAll,
    };
  }

  /* ── TaskRows (Image 4) ─────────────────────────────────────────────────── */
  function TaskRows(opts) {
    opts = opts || {};
    var variant = opts.variant || 'List';
    var rows = (opts.rows || []).slice();
    var manualOpen = {};

    var el = document.createElement('div');
    el.className = 'ai-widget ai-task-rows ' + (variant === 'List' ? 'ai-task-list' : 'ai-task-capsules');
    render();

    function render() {
      el.innerHTML = '';
      rows.forEach(function (row, i) {
        var open = !!manualOpen[row.key];
        var itemEl = document.createElement('div');
        itemEl.className = 'ai-task-row-item' + (open ? ' open' : '');
        itemEl.style.animation = 'ai-fade-up 450ms cubic-bezier(0.23,1,0.32,1) ' + (i * 80) + 'ms both';

        var badgeHtml = '';
        if (row.status === 'done' || row.status === 'completed') {
          badgeHtml = '<span class="ai-task-badge green"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg></span>';
        } else if (row.status === 'failed') {
          badgeHtml = '<span class="ai-task-badge red"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round"><path d="M18 6L6 18M6 6l12 12"/></svg></span>';
        } else if (row.active || row.status === 'running' || row.status === 'in_progress') {
          badgeHtml = '<span class="ai-task-ring active"><svg width="24" height="24" class="ai-task-spin"><circle cx="12" cy="12" r="10" fill="none" stroke="var(--ai-line)" stroke-width="2"/><circle cx="12" cy="12" r="10" fill="none" stroke="var(--ai-ink-3)" stroke-width="2" stroke-linecap="round" stroke-dasharray="18 45"/></svg><span class="ai-task-ring-num">' + (row.index || (i + 1)) + '</span></span>';
        } else {
          badgeHtml = '<span class="ai-task-ring"><svg width="24" height="24"><circle cx="12" cy="12" r="10" fill="none" stroke="var(--ai-line)" stroke-width="2"/></svg><span class="ai-task-ring-num">' + (row.index || (i + 1)) + '</span></span>';
        }

        var pillHtml = '';
        if (row.status === 'done' || row.status === 'completed') {
          pillHtml = '<span class="ai-task-pill green">Completed</span>';
        } else if (row.status === 'failed') {
          pillHtml = '<span class="ai-task-pill red">Failed <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="ai-task-spin"><path d="M21 12a9 9 0 1 1-2.64-6.36M21 3v6h-6"/></svg></span>';
        }

        var detailsHtml = (row.details || []).map(function (d) {
          return '<div class="ai-task-detail-row"><span class="ai-task-detail-label">' + escapeHtml(d.label || '') + '</span><span class="ai-task-detail-meta">' + escapeHtml(d.meta || '') + '</span></div>';
        }).join('');

        itemEl.innerHTML =
          '<button type="button" class="ai-task-row-btn" aria-expanded="' + (open ? 'true' : 'false') + '">' +
          '<span class="ai-task-badge-wrap">' + badgeHtml + '</span>' +
          '<span class="ai-task-row-label">' + escapeHtml(row.label || '') + '</span>' +
          (row.amount ? '<span class="ai-task-row-amount">' + escapeHtml(row.amount) + '</span>' : '') +
          pillHtml +
          '<span class="ai-task-row-chevron"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg></span>' +
          '</button>' +
          '<div class="ai-task-dropdown" style="grid-template-rows:' + (open ? '1fr' : '0fr') + ';opacity:' + (open ? '1' : '0') + '">' +
          '<div class="ai-task-dropdown-clip">' +
          '<div class="ai-task-dropdown-grid"><span class="ai-task-dropdown-line"></span><div class="ai-task-dropdown-items">' + detailsHtml + '</div></div>' +
          '</div></div>';

        itemEl.querySelector('.ai-task-row-btn').addEventListener('click', function () {
          manualOpen[row.key] = !manualOpen[row.key];
          render();
        });

        el.appendChild(itemEl);
      });
    }

    return {
      el: el,
      setRows: function (nextRows) {
        rows = (nextRows || []).slice();
        render();
      },
      setVariant: function (v) {
        variant = v;
        el.className = 'ai-widget ai-task-rows ' + (variant === 'List' ? 'ai-task-list' : 'ai-task-capsules');
        render();
      },
      destroy: function () {
        if (el.parentNode) el.parentNode.removeChild(el);
      }
    };
  }

  /* ── RecommendationCard ─────────────────────────────────────────────────── */
  function RecommendationCard(opts) {
    opts = opts || {};
    var title = opts.title || 'Recommendation';
    var options = (opts.options || []).slice();
    var selected = typeof opts.selected === 'number' ? opts.selected : 0;
    var open = false;
    var accepted = false;

    var el = document.createElement('div');
    el.className = 'ai-widget ai-rec-card';
    render();

    function renderMeter(signal, tone) {
      var html = '<span class="ai-rec-meter">';
      for (var bar = 0; bar < 3; bar++) {
        var fill = bar < signal ? (tone || 'var(--ai-green)') : 'var(--ai-line)';
        html += '<span class="ai-rec-meter-bar" style="background:' + fill + '"></span>';
      }
      return html + '</span>';
    }

    function render() {
      var active = options[selected] || { label: 'High confidence', body: '', signal: 3, tone: 'var(--ai-green)', cta: 'Accept' };
      var others = options.map(function (o, i) { return { o: o, i: i }; }).filter(function (x) { return x.i !== selected; });

      var othersHtml = others.map(function (item) {
        return '<button type="button" class="ai-rec-alt-row" data-idx="' + item.i + '">' +
          renderMeter(item.o.signal, item.o.tone) +
          '<span class="ai-rec-alt-short">' + escapeHtml(item.o.short || '') + '</span>' +
          '<span class="ai-rec-alt-label">' + escapeHtml(item.o.label || '') + '</span>' +
          '</button>';
      }).join('');

      el.innerHTML =
        '<div class="ai-rec-pad">' +
        '<span class="ai-rec-title">' + escapeHtml(title) + '</span>' +
        '<p class="ai-rec-body">' + (active.bodyHtml || escapeHtml(active.body || '')) + '</p>' +
        '</div>' +
        '<div class="ai-rec-drawer" style="grid-template-rows:' + (open ? '1fr' : '0fr') + ';opacity:' + (open ? '1' : '0') + '">' +
        '<div class="ai-rec-drawer-clip"><div class="ai-rec-alts">' +
        '<p class="ai-rec-alts-head">Other options</p>' +
        othersHtml +
        '</div></div></div>' +
        '<div class="ai-rec-footer">' +
        '<span class="ai-rec-foot-meta">' + renderMeter(active.signal, active.tone) + '<span class="ai-rec-foot-label">' + escapeHtml(active.label || '') + '</span></span>' +
        '<span class="ai-rec-foot-actions">' +
        (others.length ? '<button type="button" class="ai-rec-btn-alt" aria-expanded="' + (open ? 'true' : 'false') + '">Alternatives</button>' : '') +
        '<button type="button" class="ai-rec-btn-cta' + (accepted ? ' accepted' : '') + '">' + (accepted ? 'Accepted' : escapeHtml(active.cta || 'Accept')) + '</button>' +
        '</span>' +
        '</div>';

      if (el.querySelector('.ai-rec-btn-alt')) {
        el.querySelector('.ai-rec-btn-alt').addEventListener('click', function () {
          open = !open;
          render();
        });
      }
      el.querySelector('.ai-rec-btn-cta').addEventListener('click', function () {
        accepted = true;
        render();
        if (opts.onAccept) opts.onAccept(options[selected]);
      });
      el.querySelectorAll('.ai-rec-alt-row').forEach(function (btn) {
        btn.addEventListener('click', function () {
          selected = Number(btn.getAttribute('data-idx'));
          accepted = false;
          render();
        });
      });
    }

    return {
      el: el,
      destroy: function () {
        if (el.parentNode) el.parentNode.removeChild(el);
      }
    };
  }

  /* ── CodeBlock (Code & Unified Diff) ─────────────────────────────────────── */
  var KEYWORDS_SET = new Set(["import", "from", "export", "default", "async", "function", "const", "let", "var", "await", "return", "if", "else", "for", "while", "new", "throw", "try", "catch", "null", "true", "false", "undefined"]);
  var CODE_TOKEN_RE = /("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`[^`]*`|\b\d+(?:\.\d+)?\b|\b(?:import|from|export|default|async|function|const|let|var|await|return|if|else|for|while|new|throw|try|catch|null|true|false|undefined)\b|[A-Za-z_$][\w$]*(?=\s*\())/g;

  function highlightCode(text) {
    text = String(text || '');
    var html = '';
    var last = 0;
    var match;
    CODE_TOKEN_RE.lastIndex = 0;
    while ((match = CODE_TOKEN_RE.exec(text)) !== null) {
      var idx = match.index;
      var t = match[0];
      if (idx > last) html += escapeHtml(text.slice(last, idx));
      if (/^["'`]/.test(t) || /^\d/.test(t)) {
        html += '<span class="ai-tok-str">' + escapeHtml(t) + '</span>';
      } else if (KEYWORDS_SET.has(t)) {
        html += '<span class="ai-tok-kw">' + escapeHtml(t) + '</span>';
      } else {
        html += '<span class="ai-tok-fn">' + escapeHtml(t) + '</span>';
      }
      last = idx + t.length;
    }
    if (last < text.length) html += escapeHtml(text.slice(last));
    return html;
  }

  function renderPiecesHtml(pieces) {
    return (pieces || []).map(function (p) {
      if (p.change) {
        var add = p.change === 'add';
        return '<span class="ai-codeblock-piece ' + (add ? 'add' : 'del') + '">' + highlightCode(p.text) + '</span>';
      }
      return highlightCode(p.text);
    }).join('');
  }

  function CodeBlock(opts) {
    opts = opts || {};
    var file = opts.file || 'code.ts';
    var variant = opts.variant || 'Code';
    var codeLines = Array.isArray(opts.code) ? opts.code : (typeof opts.code === 'string' ? opts.code.split('\n') : []);
    var diffRows = (opts.diff || []).slice();
    var copied = false;

    var el = document.createElement('div');
    el.className = 'ai-widget ai-codeblock';
    render();

    function render() {
      var isDiff = variant === 'Diff';
      var raw = isDiff
        ? diffRows.filter(function (r) { return r.type !== 'del'; }).map(function (r) { return (r.pieces || []).map(function (p) { return p.text; }).join(''); }).join('\n')
        : codeLines.join('\n');

      var addedCount = diffRows.filter(function (r) { return r.type === 'add'; }).length;
      var removedCount = diffRows.filter(function (r) { return r.type === 'del'; }).length;

      var headRightHtml = '';
      if (isDiff) {
        headRightHtml = '<span class="ai-codeblock-stats"><span class="stat-add">+' + addedCount + '</span><span class="stat-del">-' + removedCount + '</span></span>';
      } else {
        headRightHtml = '<button type="button" class="ai-codeblock-copy' + (copied ? ' copied' : '') + '">' +
          (copied
            ? '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg> Copied'
            : '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="12" height="12" rx="2.5"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg> Copy') +
          '</button>';
      }

      var rowsHtml = '';
      if (isDiff) {
        rowsHtml = diffRows.map(function (r) {
          var add = r.type === 'add';
          var del = r.type === 'del';
          var num = del ? r.old : r.cur;
          var accentHtml = (add || del) ? '<span class="ai-codeblock-accent ' + (add ? 'add' : 'del') + '"></span>' : '';
          return '<div class="ai-codeblock-row ' + (add ? 'add' : del ? 'del' : '') + '">' +
            accentHtml +
            '<span class="ai-codeblock-num">' + (num != null ? num : '') + '</span>' +
            '<code class="ai-codeblock-code">' + renderPiecesHtml(r.pieces) + '</code>' +
            '</div>';
        }).join('');
      } else {
        rowsHtml = codeLines.map(function (line, i) {
          return '<div class="ai-codeblock-row">' +
            '<span class="ai-codeblock-num">' + (i + 1) + '</span>' +
            '<code class="ai-codeblock-code">' + highlightCode(line) + '</code>' +
            '</div>';
        }).join('');
      }

      el.innerHTML =
        '<div class="ai-codeblock-head">' +
        '<span class="ai-codeblock-file">' +
        '<svg aria-hidden="true" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5"/></svg>' +
        '<span class="ai-codeblock-filename">' + escapeHtml(file) + '</span>' +
        '</span>' +
        headRightHtml +
        '</div>' +
        '<div class="ai-codeblock-body">' +
        '<span class="ai-codeblock-divider"></span>' +
        rowsHtml +
        '</div>';

      var copyBtn = el.querySelector('.ai-codeblock-copy');
      if (copyBtn) {
        copyBtn.addEventListener('click', function () {
          navigator.clipboard.writeText(raw).then(function () {
            copied = true;
            render();
            setTimeout(function () { copied = false; render(); }, 1500);
          });
        });
      }
    }

    return {
      el: el,
      setVariant: function (v) {
        variant = v;
        render();
      },
      destroy: function () {
        if (el.parentNode) el.parentNode.removeChild(el);
      }
    };
  }

  /* ── Flowchart ───────────────────────────────────────────────────────────── */
  function Flowchart(opts) {
    opts = opts || {};
    var title = opts.title || 'Process Flow';
    var nodes = (opts.nodes || []).slice();

    var el = document.createElement('div');
    el.className = 'ai-widget ai-flowchart';
    render();

    function render() {
      var nodesHtml = nodes.map(function (node, i) {
        var isLast = i === nodes.length - 1;
        var iconHtml = node.icon ? '<span class="material-symbols-outlined">' + escapeHtml(node.icon) + '</span>' : '<span class="material-symbols-outlined">schema</span>';
        var arrowHtml = isLast ? '' : '<div class="ai-flowchart-arrow"><span class="ai-flowchart-arrow-line"></span><span class="ai-flowchart-arrow-head"></span></div>';

        return '<div class="ai-flowchart-node' + (node.active ? ' active' : '') + '" data-id="' + escapeHtml(node.id || String(i)) + '">' +
          '<span class="ai-flowchart-node-icon">' + iconHtml + '</span>' +
          '<div class="ai-flowchart-node-text">' +
          '<div class="ai-flowchart-node-label">' + escapeHtml(node.label || '') + '</div>' +
          (node.desc ? '<div class="ai-flowchart-node-desc">' + escapeHtml(node.desc) + '</div>' : '') +
          '</div>' +
          '</div>' + arrowHtml;
      }).join('');

      el.innerHTML =
        '<div class="ai-flowchart-head">' +
        '<span class="ai-flowchart-title">' +
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="3" width="6" height="6" rx="1"/><rect x="9" y="15" width="6" height="6" rx="1"/><path d="M6 9v3a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V9M12 13v2"/></svg>' +
        escapeHtml(title) +
        '</span>' +
        '</div>' +
        '<div class="ai-flowchart-canvas">' +
        nodesHtml +
        '</div>';

      el.querySelectorAll('.ai-flowchart-node').forEach(function (nodeEl) {
        nodeEl.addEventListener('click', function () {
          var id = nodeEl.getAttribute('data-id');
          if (opts.onSelect) opts.onSelect(id);
        });
      });
    }

    return {
      el: el,
      destroy: function () {
        if (el.parentNode) el.parentNode.removeChild(el);
      }
    };
  }

  PixelLoader.create = PixelLoader;
  Trace.create = Trace;
  StreamingText.create = StreamingText;
  ApprovalCard.create = ApprovalCard;
  ToolChips.create = ToolChips;
  TaskRows.create = TaskRows;
  RecommendationCard.create = RecommendationCard;
  CodeBlock.create = CodeBlock;
  Flowchart.create = Flowchart;

  window.AIWidgets = {
    PixelLoader: PixelLoader,
    Trace: Trace,
    StreamingText: StreamingText,
    ApprovalCard: ApprovalCard,
    ToolChips: ToolChips,
    TaskRows: TaskRows,
    RecommendationCard: RecommendationCard,
    CodeBlock: CodeBlock,
    Flowchart: Flowchart,
    actionRow: function (opts) {
      var row = buildActions(String(opts && opts.text || ''), opts || {});
      row.hidden = false;
      return row;
    },
    streamSSE: streamSSE,
    escapeHtml: escapeHtml,
  };
})();