(function () {
  'use strict';

  /* ── WASM Worker state ────────────────────────────────────────────────────── */
  var worker = null;
  var workerReady = false;
  var workerLoading = false;
  var pendingRun = null;
  var runId = 0;
  var workerStartedAt = 0;

  var NEBY_MAX_TOKENS = 128;
  var preloadScheduled = false;

  /* ── UI state ─────────────────────────────────────────────────────────────── */
  var isOpen = false;
  var isThinking = false;

  /* ── Tool schemas for Needle 2 ────────────────────────────────────────────── */
  var NEBY_TOOLS = JSON.stringify([
    {
      name: 'search_resources',
      description: 'Search for study resources on NEBians — notes, past papers, textbooks, PDFs.',
      parameters: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'search keywords' },
          subject: { type: 'string', description: 'subject name e.g. Mathematics, Physics, English' },
          resource_type: { type: 'string', enum: ['PDF', 'Note', 'Past Paper', 'Textbook', 'Video', 'Link', ''], description: 'optional type filter' },
        },
        required: ['query'],
      },
    },
    {
      name: 'find_notes',
      description: 'Find study notes or past exam papers for a specific subject and grade on NEBians.',
      parameters: {
        type: 'object',
        properties: {
          subject: { type: 'string', description: 'subject name e.g. Mathematics, Physics, Chemistry' },
          grade_level: { type: 'string', description: 'e.g. Class 11, Class 12, SEE' },
          exam_type: { type: 'string', enum: ['Notes', 'Board', 'Final', 'SEE', 'Mock', 'Reference', ''], description: 'type of material' },
        },
        required: [],
      },
    },
    {
      name: 'get_forum_posts',
      description: 'Get forum posts from the NEBians discussion forum.',
      parameters: {
        type: 'object',
        properties: {
          category: { type: 'string', description: 'category to filter e.g. Science, Math, Help, General' },
          sort: { type: 'string', enum: ['recent', 'popular'], description: 'sort order' },
        },
        required: [],
      },
    },
    {
      name: 'navigate_to',
      description: 'Navigate the user to a specific page on NEBians.',
      parameters: {
        type: 'object',
        properties: {
          page: {
            type: 'string',
            enum: ['home', 'library', 'forum', 'search', 'news', 'settings', 'bookmarks', 'upload', 'results', 'leaderboard', 'tools'],
            description: 'destination page',
          },
        },
        required: ['page'],
      },
    },
    {
      name: 'get_subjects',
      description: 'List all available subjects on NEBians.',
      parameters: { type: 'object', properties: {}, required: [] },
    },
  ]);

  /* ── DOM refs ─────────────────────────────────────────────────────────────── */
  var fab, panel, chatArea, textarea, sendBtn, suggestionsEl;

  /* ── Idle preload ──────────────────────────────────────────────────────────
     The first setup runs in a Web Worker and later launches restore the
     initialized runtime from IndexedDB instead of compiling the grammar again. */
  function preloadNeedle() {
    if (preloadScheduled) return;
    preloadScheduled = true;

    function start() {
      if (document.getElementById('neby-fab')) ensureWorker();
    }

    var connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    var constrained = connection && (connection.saveData || /(^|-)2g$/.test(connection.effectiveType || ''));
    if (!constrained) {
      if ('requestIdleCallback' in window) {
        window.requestIdleCallback(start, { timeout: 3000 });
      } else {
        setTimeout(start, 1500);
      }
    }

    var done = false;
    function onGesture() {
      if (done || constrained) return;
      done = true;
      start();
      ['pointerdown', 'mousemove', 'scroll', 'touchstart', 'keydown'].forEach(function (t) {
        document.removeEventListener(t, onGesture, true);
      });
    }
    if (!constrained) {
      ['pointerdown', 'mousemove', 'scroll', 'touchstart', 'keydown'].forEach(function (t) {
        document.addEventListener(t, onGesture, true);
      });
    }
  }

  /* ── Worker bootstrap ─────────────────────────────────────────────────────── */
  function ensureWorker() {
    if (worker) return;
    if (workerLoading) return;
    workerLoading = true;

    updateStatus('loading model\u2026');

    try {
      workerStartedAt = performance.now();
      worker = new window.Worker(getWorkerUrl());
      worker.addEventListener('message', onWorkerMessage);
      worker.addEventListener('error', function (e) {
        console.error('Needle worker error:', e);
        updateStatus('failed to load');
        workerLoading = false;
        workerReady = false;
        worker = null;
        if (isThinking) {
          removeThinking();
          appendAiBubble('The AI model failed to load. Please refresh and try again.');
        }
      });
      worker.postMessage({ type: 'initialize', tools: NEBY_TOOLS, snapshotNamespace: 'nebians-web-v1' });
    } catch (e) {
      console.error('Failed to create worker:', e);
      workerLoading = false;
      worker = null;
    }
  }

  function getWorkerUrl() {
    return '/static/web/js/needle2/needle.worker.js?v=3';
  }

  function statusLabel(msg) {
    if (msg.status === 'loading-engine') return 'loading AI engine\u2026';
    if (msg.status === 'restoring') return 'restoring saved runtime' + progressSuffix(msg.progress);
    if (msg.status === 'cache-hit') return msg.asset === 'model' ? 'model found on device' : 'engine found on device';
    if (msg.status === 'downloading') return 'downloading ' + (msg.asset || 'model') + progressSuffix(msg.progress);
    if (msg.status === 'loading-model') return 'loading model into memory\u2026';
    if (msg.status === 'preparing-tools') return 'preparing on-device tools\u2026';
    if (msg.status === 'saving') return 'optimizing future launches' + progressSuffix(msg.progress);
    return 'loading on-device AI\u2026';
  }

  function progressSuffix(value) {
    return typeof value === 'number' && value > 0 ? ' \u00b7 ' + Math.round(value * 100) + '%' : '';
  }

  function onWorkerMessage(e) {
    var msg = e.data;
    if (!msg) return;

    if (msg.type === 'status') {
      updateStatus(statusLabel(msg));
      return;
    }

    if (msg.type === 'ready') {
      workerReady = true;
      workerLoading = false;
      var totalSecs = workerStartedAt ? (performance.now() - workerStartedAt) / 1000 : 0;
      var source = msg.source === 'snapshot' ? 'saved runtime' : 'ready';
      updateStatus('on-device AI \u00b7 ' + source + (totalSecs > 0 ? ' in ' + totalSecs.toFixed(1) + 's' : ''));
      if (sendBtn) sendBtn.disabled = !(textarea && textarea.value.trim());
      if (pendingRun) {
        var p = pendingRun;
        pendingRun = null;
        _runNeedle(p.query, p.id);
      }
      return;
    }

    if (msg.type === 'result') {
      if (msg.id !== runId) return;
      removeThinking();
      handleNeedleResult(msg.result, msg.durationMs);
      return;
    }

    if (msg.type === 'error') {
      removeThinking();
      appendAiBubble('Hmm, I couldn\u2019t process that. Try rephrasing!');
      updateStatus('on-device AI');
      return;
    }
  }

  function updateStatus(text) {
    var el = document.getElementById('neby-status-text');
    if (el) el.textContent = text;
  }

  /* ── Init ─────────────────────────────────────────────────────────────────── */
  function init() {
    fab = document.getElementById('neby-fab');
    panel = document.getElementById('neby-panel');
    chatArea = document.getElementById('neby-chat-area');
    textarea = document.getElementById('neby-input');
    sendBtn = document.getElementById('neby-send-btn');
    suggestionsEl = document.getElementById('neby-suggestions');

    if (!fab || !panel) return;

    fab.addEventListener('click', togglePanel);

    document.addEventListener('click', function (e) {
      if (isOpen && !panel.contains(e.target) && !fab.contains(e.target)) closePanel();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isOpen) closePanel();
    });

    if (sendBtn) sendBtn.addEventListener('click', sendMessage);
    if (textarea) {
      textarea.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
      });
      textarea.addEventListener('input', function () {
        sendBtn.disabled = !textarea.value.trim() || !workerReady;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 80) + 'px';
      });
    }

    if (suggestionsEl) {
      suggestionsEl.querySelectorAll('.neby-suggestion-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var q = btn.getAttribute('data-query');
          if (q) runQuery(q);
        });
      });
    }

    var closeBtn = document.getElementById('neby-close-btn');
    if (closeBtn) closeBtn.addEventListener('click', closePanel);

    // Start loading model when panel opens (lazy)
  }

  /* ── Panel toggle ─────────────────────────────────────────────────────────── */
  function togglePanel() { isOpen ? closePanel() : openPanel(); }

  function openPanel() {
    isOpen = true;
    panel.classList.add('open');
    fab.classList.add('panel-open');
    fab.setAttribute('aria-expanded', 'true');
    fab.setAttribute('aria-label', 'Close Neby AI');
    ensureWorker();
    if (textarea) setTimeout(function () { textarea.focus(); }, 280);
    scrollToBottom();
  }

  function closePanel() {
    isOpen = false;
    panel.classList.remove('open');
    fab.classList.remove('panel-open');
    fab.setAttribute('aria-expanded', 'false');
    fab.setAttribute('aria-label', 'Open Neby AI Assistant');
  }

  /* ── Send & run ───────────────────────────────────────────────────────────── */
  function sendMessage() {
    if (!textarea || isThinking) return;
    var msg = textarea.value.trim();
    if (!msg) return;
    textarea.value = '';
    textarea.style.height = 'auto';
    if (sendBtn) sendBtn.disabled = true;
    runQuery(msg);
  }

  function runQuery(query) {
    hideSuggestions();
    appendUserBubble(query);
    showThinking();
    ensureWorker();

    runId += 1;
    var id = runId;

    if (!workerReady) {
      pendingRun = { query: query, id: id };
      return;
    }
    _runNeedle(query, id);
  }

  function _runNeedle(query, id) {
    if (!worker) return;
    worker.postMessage({ type: 'run', id: id, query: query, tools: NEBY_TOOLS, maxNewTokens: NEBY_MAX_TOKENS });
  }

  /* ── Needle result handler ────────────────────────────────────────────────── */
  function handleNeedleResult(result, durationMs) {
    console.log('[Neby] raw result:', result);
    if (!result) { appendAiBubble('No results found. Try asking differently!'); return; }

    appendReasoning(result, durationMs);
    var calls = result.function_calls || [];

    if (!calls.length) {
      appendAiBubble('I can help you find resources, forum posts, subjects, or navigate NEBians. Try: \u201cFind Physics notes for Class 12\u201d or \u201cshow popular forum posts\u201d.');
      return;
    }

    calls.forEach(function (call) {
      handleNeedleCall(call, result.confidence);
    });
  }

  function handleNeedleCall(call, confidence) {
    var toolName = call.name;
    var args = call.arguments || {};
    console.log('[Neby] tool:', toolName, '| args:', args, '| confidence:', confidence);

    if (toolName === 'navigate_to') {
      var routes = {
        home: '/', library: '/library/', forum: '/forum/', search: '/search/',
        news: '/news/', settings: '/settings/', bookmarks: '/bookmarks/',
        upload: '/upload/', results: '/results/check/',
        leaderboard: '/forum/leaderboard/', tools: '/tools/',
      };
      var page = args.page || 'home';
      var url = routes[page] || '/';
      var msgEl = createAiMsgEl();
      msgEl.innerHTML =
        '<div class="neby-bubble">Sure! Here\u2019s the link to <strong>' + escapeHtml(page) + '</strong>:' +
        '<a href="' + escapeHtml(url) + '" class="neby-nav-card" style="margin-top:8px;display:flex;">' +
        '<span class="material-symbols-outlined">open_in_new</span>' +
        'Go to ' + escapeHtml(page) +
        '<span class="material-symbols-outlined neby-result-arrow" style="margin-left:auto;">arrow_forward</span>' +
        '</a></div>';
      appendEl(msgEl);
      return;
    }

    if (toolName === 'get_subjects') {
      fetchAndRender('get_subjects', {});
      return;
    }

    if (toolName === 'search_resources' || toolName === 'find_notes' || toolName === 'get_forum_posts') {
      fetchAndRender(toolName, args);
      return;
    }

    appendAiBubble('Got it! Let me know if you need anything else.');
  }

  function appendReasoning(result, durationMs) {
    var reasoning = String(result.reasoning || '').trim();
    if (!reasoning) return;

    var message = createAiMsgEl();
    var content = document.createElement('div');
    content.className = 'neby-msg-content';
    var details = document.createElement('details');
    details.className = 'neby-reasoning';
    var summary = document.createElement('summary');
    summary.textContent = 'How Needle understood this';
    var body = document.createElement('div');
    body.className = 'neby-reasoning-body';
    body.textContent = reasoning;
    var metrics = document.createElement('div');
    metrics.className = 'neby-reasoning-metrics';
    var parts = [];
    if (typeof result.confidence === 'number') parts.push('confidence ' + Math.round(result.confidence * 100) + '%');
    if (typeof durationMs === 'number') parts.push(Math.round(durationMs) + ' ms on this device');
    if (typeof result.decode_tps === 'number') parts.push(Math.round(result.decode_tps) + ' tok/s');
    metrics.textContent = parts.join(' \u00b7 ');
    details.appendChild(summary);
    details.appendChild(body);
    if (parts.length) details.appendChild(metrics);
    content.appendChild(details);
    message.innerHTML = '<div class="neby-msg-avatar"><span class="material-symbols-outlined">psychology</span></div>';
    message.appendChild(content);
    appendEl(message);
  }

  /* ── Backend fetch for DB results ─────────────────────────────────────────── */
  function getCsrfToken() {
    var m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? m[1] : '';
  }

  function fetchAndRender(toolName, args) {
    fetch('/ajax/neby-assist/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
      credentials: 'same-origin',
      body: JSON.stringify({ tool: toolName, args: args }),
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data.error) { appendAiBubble(data.error); return; }
        renderToolResult(toolName, args, data.result || data);
      })
      .catch(function () {
        appendAiBubble('Couldn\u2019t fetch results right now. Please try again.');
      });
  }

  /* ── Tool result renderers ────────────────────────────────────────────────── */
  function renderToolResult(tool, args, result) {
    if (!result) { appendAiBubble('No results found.'); return; }

    if (tool === 'get_subjects') {
      var subjects = (result.subjects || []).slice(0, 12);
      if (!subjects.length) { appendAiBubble('No subjects found.'); return; }
      var msgEl = createAiMsgEl();
      var chips = subjects.map(function (s) {
        return '<span class="neby-chip">' + escapeHtml(s.subject) + ' <span style="opacity:.55">(' + s.count + ')</span></span>';
      }).join('');
      msgEl.innerHTML = '<div class="neby-bubble">Here are the subjects available on NEBians:<div class="neby-chips">' + chips + '</div></div>';
      appendEl(msgEl);
      return;
    }

    if (tool === 'search_resources' || tool === 'find_notes') {
      var resources = result.resources || [];
      if (!resources.length) { appendAiBubble('No resources found. Try different keywords!'); return; }
      var intro = tool === 'find_notes' ? 'Here are some study materials:' : 'Here\u2019s what I found:';
      var msgEl2 = createAiMsgEl();
      var cards = resources.map(function (r) {
        var icon = resourceIcon(r.type);
        var meta = [r.subject, r.grade_level, r.exam_type].filter(Boolean).join(' \u00b7 ');
        return '<a href="/reader/' + escapeHtml(r.id) + '/" class="neby-result-card">' +
          '<div class="neby-result-icon"><span class="material-symbols-outlined">' + icon + '</span></div>' +
          '<div class="neby-result-body"><div class="neby-result-title">' + escapeHtml(r.title) + '</div>' +
          (meta ? '<div class="neby-result-meta">' + escapeHtml(meta) + '</div>' : '') + '</div>' +
          '<div class="neby-result-arrow"><span class="material-symbols-outlined">chevron_right</span></div></a>';
      }).join('');
      msgEl2.innerHTML = '<div class="neby-bubble">' + intro + '<span class="neby-count-badge">' + resources.length + '</span><div class="neby-results">' + cards + '</div></div>';
      appendEl(msgEl2);
      return;
    }

    if (tool === 'get_forum_posts') {
      var posts = result.posts || [];
      if (!posts.length) { appendAiBubble('No forum posts found.'); return; }
      var msgEl3 = createAiMsgEl();
      var pcards = posts.map(function (p) {
        return '<a href="/forum/post/' + escapeHtml(p.id) + '/" class="neby-result-card">' +
          '<div class="neby-result-icon"><span class="material-symbols-outlined">forum</span></div>' +
          '<div class="neby-result-body"><div class="neby-result-title">' + escapeHtml(p.title) + '</div>' +
          '<div class="neby-result-meta">' + escapeHtml(p.category) + ' \u00b7 \uD83D\uDC4D ' + p.thumbs_up_count + ' \u00b7 \uD83D\uDCAC ' + p.reply_count + '</div>' +
          '</div><div class="neby-result-arrow"><span class="material-symbols-outlined">chevron_right</span></div></a>';
      }).join('');
      msgEl3.innerHTML = '<div class="neby-bubble">Here are some forum discussions:<span class="neby-count-badge">' + posts.length + '</span><div class="neby-results">' + pcards + '</div></div>';
      appendEl(msgEl3);
      return;
    }
  }

  /* ── DOM helpers ──────────────────────────────────────────────────────────── */
  function appendUserBubble(text) {
    var el = document.createElement('div');
    el.className = 'neby-msg user';
    el.innerHTML = '<div class="neby-bubble">' + escapeHtml(text) + '</div>';
    appendEl(el);
  }

  function appendAiBubble(text) {
    var el = createAiMsgEl();
    el.innerHTML = '<div class="neby-msg-avatar"><span class="material-symbols-outlined">auto_awesome</span></div>' +
      '<div class="neby-bubble">' + escapeHtml(text) + '</div>';
    appendEl(el);
  }

  function createAiMsgEl() {
    var el = document.createElement('div');
    el.className = 'neby-msg ai';
    return el;
  }

  function appendEl(el) {
    var empty = chatArea && chatArea.querySelector('.neby-empty-state');
    if (empty) empty.remove();
    if (chatArea) chatArea.appendChild(el);
    scrollToBottom();
  }

  function showThinking() {
    isThinking = true;
    var el = document.createElement('div');
    el.className = 'neby-msg ai';
    el.id = 'neby-thinking-el';
    el.innerHTML = '<div class="neby-msg-avatar"><span class="material-symbols-outlined">auto_awesome</span></div>' +
      '<div class="neby-thinking"><span></span><span></span><span></span></div>';
    appendEl(el);
  }

  function removeThinking() {
    isThinking = false;
    var el = document.getElementById('neby-thinking-el');
    if (el) el.remove();
  }

  function scrollToBottom() {
    if (chatArea) requestAnimationFrame(function () { chatArea.scrollTop = chatArea.scrollHeight; });
  }

  function hideSuggestions() {
    if (suggestionsEl) suggestionsEl.style.display = 'none';
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  function resourceIcon(type) {
    return { PDF: 'picture_as_pdf', Note: 'description', Video: 'smart_display', Audio: 'headphones', Image: 'image', Link: 'link' }[type] || 'description';
  }

  /* ── Bootstrap ────────────────────────────────────────────────────────────── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      init();
      preloadNeedle();
    });
  } else {
    init();
    preloadNeedle();
  }

})();
