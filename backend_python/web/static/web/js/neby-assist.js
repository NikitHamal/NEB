(function () {
  'use strict';

  var useLocalModel = false;
  try {
    useLocalModel = localStorage.getItem('neby_use_local_model') === 'true';
  } catch (e) {}

  var worker = null;
  var workerReady = false;
  var workerLoading = false;
  var pendingRun = null;
  var runId = 0;
  var workerStartedAt = 0;

  var NEBY_MAX_TOKENS = 128;
  var CLOUD_CONFIDENCE_THRESHOLD = 0.35;
  var lastQuery = '';

  var isOpen = false;
  var isThinking = false;

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

  var fab, panel, chatArea, textarea, sendBtn, suggestionsEl;

  function ensureWorker() {
    if (worker || workerLoading) return;
    workerLoading = true;

    updateStatus('loading local AI model\u2026');
    if (isThinking) setThinking('Loading model', 'dots');

    try {
      workerStartedAt = performance.now();
      worker = new window.Worker(getWorkerUrl());
      worker.addEventListener('message', onWorkerMessage);
      worker.addEventListener('error', function (e) {
        console.error('Local worker error:', e);
        updateStatus('Local AI failed — using Cloud');
        workerLoading = false;
        workerReady = false;
        worker = null;
        useLocalModel = false;
        try { localStorage.setItem('neby_use_local_model', 'false'); } catch (err) {}
        if (isThinking) {
          routeToCloud(lastQuery, null);
        }
      });
      worker.postMessage({ type: 'initialize', tools: NEBY_TOOLS, snapshotNamespace: 'nebians-web-v3' });
    } catch (e) {
      console.error('Failed to create worker:', e);
      workerLoading = false;
      worker = null;
      useLocalModel = false;
    }
  }

  function getWorkerUrl() {
    return '/static/web/js/needle3/needle.worker.js?v=3';
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
      if (isThinking) setThinking(statusLabel(msg), 'dots');
      return;
    }

    if (msg.type === 'ready') {
      workerReady = true;
      workerLoading = false;
      var totalSecs = workerStartedAt ? (performance.now() - workerStartedAt) / 1000 : 0;
      var source = msg.source === 'snapshot' ? 'saved runtime' : 'ready';
      updateStatus('On-device AI \u00b7 ' + source + (totalSecs > 0 ? ' in ' + totalSecs.toFixed(1) + 's' : ''));
      if (sendBtn && textarea) sendBtn.disabled = !textarea.value.trim();
      if (isThinking) setThinking('Thinking', 'drive');
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
      routeToCloud(lastQuery, null);
      return;
    }
  }

  function updateStatus(text) {
    var el = document.getElementById('neby-status-text');
    if (el) el.textContent = text;
  }

  function updatePoweredFooter() {
    var footer = document.querySelector('.neby-powered');
    if (!footer) return;
    if (useLocalModel) {
      footer.innerHTML = '⚡ On-Device AI (Offline) &middot; <a href="#" id="neby-switch-cloud" style="color:var(--md-sys-color-primary);text-decoration:underline;">Switch to Cloud AI</a>';
    } else {
      footer.innerHTML = '⚡ Neby Cloud AI &middot; <a href="#" id="neby-switch-local" style="color:var(--md-sys-color-primary);text-decoration:underline;">Enable Offline Mode (~40MB)</a>';
    }

    var toCloud = document.getElementById('neby-switch-cloud');
    if (toCloud) {
      toCloud.addEventListener('click', function (e) {
        e.preventDefault();
        useLocalModel = false;
        try { localStorage.setItem('neby_use_local_model', 'false'); } catch (err) {}
        updateStatus('Online \u00b7 Neby Assistant');
        updatePoweredFooter();
      });
    }

    var toLocal = document.getElementById('neby-switch-local');
    if (toLocal) {
      toLocal.addEventListener('click', function (e) {
        e.preventDefault();
        useLocalModel = true;
        try { localStorage.setItem('neby_use_local_model', 'true'); } catch (err) {}
        ensureWorker();
        updatePoweredFooter();
      });
    }
  }

  function init() {
    fab = document.getElementById('neby-fab');
    panel = document.getElementById('neby-panel');
    chatArea = document.getElementById('neby-chat-area');
    textarea = document.getElementById('neby-input');
    sendBtn = document.getElementById('neby-send-btn');
    suggestionsEl = document.getElementById('neby-suggestions');

    if (!fab || !panel) return;

    updateStatus(useLocalModel ? 'Local AI' : 'Online \u00b7 Neby Assistant');
    updatePoweredFooter();

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
        if (sendBtn) sendBtn.disabled = !textarea.value.trim();
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
  }

  function togglePanel() { isOpen ? closePanel() : openPanel(); }

  function openPanel() {
    isOpen = true;
    panel.classList.add('open');
    fab.classList.add('panel-open');
    fab.setAttribute('aria-expanded', 'true');
    fab.setAttribute('aria-label', 'Close Neby AI');
    if (useLocalModel) ensureWorker();
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
    showThinking('Thinking', 'drive');
    lastQuery = query;

    if (!useLocalModel) {
      routeToCloud(query, null);
      return;
    }

    runId += 1;
    var id = runId;

    if (!workerReady) {
      ensureWorker();
      pendingRun = { query: query, id: id };
      return;
    }
    _runNeedle(query, id);
  }

  function _runNeedle(query, id) {
    if (!worker) return;
    worker.postMessage({ type: 'run', id: id, query: query, tools: NEBY_TOOLS, maxNewTokens: NEBY_MAX_TOKENS });
  }

  function handleNeedleResult(result, durationMs) {
    if (!result) { appendAiBubble('No results found. Try asking differently!'); return; }

    appendReasoning(result, durationMs);
    var calls = result.function_calls || [];

    if (!calls.length) {
      routeToCloud(lastQuery, result);
      return;
    }

    var confidence = typeof result.confidence === 'number' ? result.confidence : 1;
    if (confidence < CLOUD_CONFIDENCE_THRESHOLD) {
      routeToCloud(lastQuery, result);
      return;
    }

    calls.forEach(function (call) {
      handleNeedleCall(call, result.confidence);
    });
  }

  function routeToCloud(query, localResult) {
    updateStatus('Neby AI thinking\u2026');
    setThinking('Thinking', 'drive');
    var hint = null;
    if (localResult && localResult.function_calls && localResult.function_calls.length) {
      var first = localResult.function_calls[0];
      hint = { name: first.name, arguments: first.arguments || {} };
    }
    fetch('/ajax/neby-assist/cloud/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
      credentials: 'same-origin',
      body: JSON.stringify({ query: query, localGuess: hint }),
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        updateStatus(useLocalModel ? 'Local AI' : 'Online \u00b7 Neby Assistant');
        removeThinking();
        if (!data.mode) {
          fallbackToLocal(localResult, data.error);
          return;
        }
        if (data.mode === 'chat') {
          appendStreamingAi(data.text || 'Here you go!');
          return;
        }
        if (data.mode === 'tool') {
          if (data.tool === 'navigate_to') {
            handleNeedleCall({ name: 'navigate_to', arguments: data.args || {} }, 1);
            return;
          }
          if (data.result) {
            renderToolResult(data.tool, data.args || {}, data.result);
            return;
          }
          handleNeedleCall({ name: data.tool, arguments: data.args || {} }, 1);
          return;
        }
        appendAiBubble('Hmm, I couldn\u2019t figure that out. Try rephrasing!');
      })
      .catch(function () {
        updateStatus(useLocalModel ? 'Local AI' : 'Online \u00b7 Neby Assistant');
        removeThinking();
        fallbackToLocal(localResult, null);
      });
  }

  function fallbackToLocal(localResult, errMsg) {
    if (localResult && localResult.function_calls && localResult.function_calls.length) {
      localResult.function_calls.forEach(function (call) {
        handleNeedleCall(call, localResult.confidence);
      });
      return;
    }
    appendAiBubble(errMsg || 'Couldn\u2019t reach the cloud AI. Please try again.');
  }

  function handleNeedleCall(call, confidence) {
    var toolName = call.name;
    var args = call.arguments || {};

    if (toolName === 'navigate_to') {
      var routes = {
        home: '/', library: '/library/', forum: '/forum/', search: '/search/',
        news: '/news/', settings: '/settings/', bookmarks: '/bookmarks/',
        upload: '/upload/', results: '/results/check/',
        leaderboard: '/forum/leaderboard/', tools: '/tools/',
      };
      var page = args.page || 'home';
      var url = routes[page] || '/';
      appendNavBubble(page, url);
      setTimeout(function () { window.location.href = url; }, 800);
      return;
    }

    callServerTool(toolName, args, confidence);
  }

  function callServerTool(toolName, args, confidence) {
    showThinking('Finding resources\u2026', 'dots');
    fetch('/ajax/neby-assist/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
      credentials: 'same-origin',
      body: JSON.stringify({ tool: toolName, args: args }),
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        removeThinking();
        if (data.error) {
          appendAiBubble('Sorry, I couldn\u2019t load that. Try asking something else.');
          return;
        }
        renderToolResult(toolName, args, data.result);
      })
      .catch(function () {
        removeThinking();
        appendAiBubble('Connection error. Please try again.');
      });
  }

  function renderToolResult(toolName, args, result) {
    if (!result) {
      appendAiBubble('No results found. Try asking differently!');
      return;
    }

    if (toolName === 'search_resources' || toolName === 'find_notes') {
      var items = result.resources || [];
      if (!items.length) {
        var msg = 'I couldn\u2019t find any study materials';
        if (args.subject) msg += ' for ' + escapeHtml(args.subject);
        if (args.grade_level) msg += ' (' + escapeHtml(args.grade_level) + ')';
        msg += '. Try searching the Library!';
        appendAiBubble(msg);
        return;
      }
      var headerText = 'Found ' + items.length + ' study resource' + (items.length === 1 ? '' : 's') + ':';
      appendResourceCards(headerText, items);
      return;
    }

    if (toolName === 'get_forum_posts') {
      var posts = result.posts || [];
      if (!posts.length) {
        appendAiBubble('No forum discussions found' + (args.category ? ' in ' + escapeHtml(args.category) : '') + '. Check out the Forum to start one!');
        return;
      }
      appendForumCards('Here are some forum discussions:', posts);
      return;
    }

    if (toolName === 'get_subjects') {
      var subs = result.subjects || [];
      if (!subs.length) { appendAiBubble('No subjects found.'); return; }
      appendSubjectChips('Available subjects:', subs);
      return;
    }

    appendAiBubble(JSON.stringify(result));
  }

  function appendUserBubble(text) {
    var el = document.createElement('div');
    el.className = 'neby-msg user';
    el.innerHTML = '<div class="neby-bubble">' + escapeHtml(text) + '</div>';
    appendEl(el);
  }

  function appendAiBubble(text) {
    var el = createAiMsgEl();
    var bubble = document.createElement('div');
    bubble.className = 'neby-bubble';
    bubble.innerHTML = escapeHtml(text);
    el.appendChild(bubble);
    appendEl(el);
  }

  function appendReasoning(result, durationMs) {
    if (!window.AIWidgets || !window.AIWidgets.ReasoningBox) return;
    var text = (result.reasoning || '').trim();
    if (!text && result.function_calls && result.function_calls.length) {
      var first = result.function_calls[0];
      text = 'Decided on ' + first.name + ' with args ' + JSON.stringify(first.arguments || {});
    }
    if (!text) return;
    var el = createAiMsgEl();
    var box = window.AIWidgets.ReasoningBox.create({
      reasoning: text,
      durationMs: durationMs || null,
      tokens: result.tokens || null,
      confidence: typeof result.confidence === 'number' ? result.confidence : null,
      defaultOpen: false,
    });
    el.appendChild(box.el);
    appendEl(el);
  }

  function appendNavBubble(page, url) {
    var el = createAiMsgEl();
    el.innerHTML = '<div class="neby-bubble neby-bubble-nav"><span class="material-symbols-outlined">navigation</span> Navigating to <strong>' + escapeHtml(page) + '</strong>\u2026</div>';
    appendEl(el);
  }

  function appendResourceCards(headerText, items) {
    var el = createAiMsgEl();
    var html = '<div class="neby-bubble"><p style="margin:0 0 8px;font-weight:600;font-size:0.875rem;">' + escapeHtml(headerText) + '</p><div class="neby-result-list">';
    items.slice(0, 4).forEach(function (r) {
      var icon = resourceIcon(r.resource_type);
      html += '<a href="' + escapeHtml(r.url) + '" class="neby-result-item" target="_blank" rel="noopener">';
      html += '<span class="material-symbols-outlined neby-result-icon">' + icon + '</span>';
      html += '<div class="neby-result-info">';
      html += '<div class="neby-result-title">' + escapeHtml(r.title) + '</div>';
      html += '<div class="neby-result-sub">' + escapeHtml(r.subject || '') + (r.grade_level ? ' &middot; ' + escapeHtml(r.grade_level) : '') + (r.author ? ' &middot; by ' + escapeHtml(r.author) : '') + '</div>';
      html += '</div></a>';
    });
    html += '</div></div>';
    el.innerHTML = html;
    appendEl(el);
  }

  function appendForumCards(headerText, posts) {
    var el = createAiMsgEl();
    var html = '<div class="neby-bubble"><p style="margin:0 0 8px;font-weight:600;font-size:0.875rem;">' + escapeHtml(headerText) + '</p><div class="neby-result-list">';
    posts.slice(0, 4).forEach(function (p) {
      html += '<a href="' + escapeHtml(p.url) + '" class="neby-result-item">';
      html += '<span class="material-symbols-outlined neby-result-icon">chat</span>';
      html += '<div class="neby-result-info">';
      html += '<div class="neby-result-title">' + escapeHtml(p.title) + '</div>';
      html += '<div class="neby-result-sub">' + escapeHtml(p.category || 'General') + ' &middot; ' + (p.reply_count || 0) + ' replies</div>';
      html += '</div></a>';
    });
    html += '</div></div>';
    el.innerHTML = html;
    appendEl(el);
  }

  function appendSubjectChips(headerText, subjects) {
    var el = createAiMsgEl();
    var html = '<div class="neby-bubble"><p style="margin:0 0 8px;font-weight:600;font-size:0.875rem;">' + escapeHtml(headerText) + '</p><div class="neby-chips">';
    subjects.forEach(function (s) {
      var name = typeof s === 'string' ? s : s.name;
      html += '<button class="neby-chip" data-subject="' + escapeHtml(name) + '">' + escapeHtml(name) + '</button>';
    });
    html += '</div></div>';
    el.innerHTML = html;
    el.querySelectorAll('.neby-chip').forEach(function (chip) {
      chip.addEventListener('click', function () {
        var sub = chip.getAttribute('data-subject');
        if (sub) runQuery('Find notes for ' + sub);
      });
    });
    appendEl(el);
  }

  function appendStreamingAi(text) {
    var el = createAiMsgEl();
    var bubble = document.createElement('div');
    bubble.className = 'neby-bubble';
    if (window.AIWidgets && text && text.length > 40) {
      var stream = window.AIWidgets.StreamingText.create({
        text: text,
        actions: true,
        wordMs: 40,
        onRetry: function () {
          if (lastQuery) runQuery(lastQuery);
        },
        onVote: function (vote) {
          fetch('/ajax/ai-feedback/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
            credentials: 'same-origin',
            body: JSON.stringify({ surface: 'neby', vote: vote, provider: 'cloud', query: lastQuery || '' }),
          }).catch(function () {});
        },
      });
      bubble.appendChild(stream.el);
    } else {
      bubble.innerHTML = escapeHtml(text || 'Here you go!');
    }
    el.appendChild(bubble);
    appendEl(el);
    scrollToBottom();
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

  var thinkingEl = null;
  var thinkingLoader = null;

  function showThinking(label, variant) {
    isThinking = true;
    if (thinkingEl) thinkingEl.remove();
    thinkingEl = document.createElement('div');
    thinkingEl.className = 'neby-msg ai';
    thinkingEl.id = 'neby-thinking-el';
    if (window.AIWidgets) {
      thinkingLoader = window.AIWidgets.PixelLoader.create({ label: label || 'Thinking', variant: variant || 'drive' });
      thinkingEl.appendChild(thinkingLoader.el);
    } else {
      thinkingEl.innerHTML = '<div class="ai-widget ai-pixel-loader"><div class="ai-px-meta"><span class="ai-px-label">' + escapeHtml(label || 'Thinking') + '</span></div></div>';
    }
    appendEl(thinkingEl);
  }

  function setThinking(label, variant) {
    if (!isThinking) { showThinking(label, variant); return; }
    if (thinkingLoader) thinkingLoader.setLabel(label || 'Thinking', variant);
  }

  function removeThinking() {
    isThinking = false;
    if (thinkingLoader) { thinkingLoader.destroy(); thinkingLoader = null; }
    if (thinkingEl) { thinkingEl.remove(); thinkingEl = null; }
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

  function getCsrfToken() {
    var match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
