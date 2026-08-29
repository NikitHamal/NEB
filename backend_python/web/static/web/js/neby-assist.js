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
    {
      name: 'generate_p5_art',
      description: 'Generate dynamic, interactive 2D/3D paintings, drawings, and generative art using p5.js canvas.',
      parameters: {
        type: 'object',
        properties: {
          prompt: { type: 'string', description: 'art description or topic e.g. cosmic nebula, flow field, mandala, sunset wave' },
          style: { type: 'string', enum: ['generative', 'fractal', 'landscape', 'pattern', 'animated', 'abstract', ''], description: 'artistic technique' },
          color_palette: { type: 'string', enum: ['vibrant', 'neon', 'pastel', 'monochrome', 'cyberpunk', 'warm', 'cool', ''], description: 'color scheme' },
          complexity: { type: 'string', enum: ['low', 'medium', 'high', 'extreme', ''], description: 'level of visual detail' },
          code: { type: 'string', description: 'optional custom p5.js sketch code' },
        },
        required: ['prompt'],
      },
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
      worker.postMessage({ type: 'initialize', tools: NEBY_TOOLS, snapshotNamespace: 'nebians-web-v1' });
    } catch (e) {
      console.error('Failed to create worker:', e);
      workerLoading = false;
      worker = null;
      useLocalModel = false;
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

    if (toolName === 'generate_p5_art') {
      renderP5Art(args, result);
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

  function renderP5Art(args, result) {
    var title = result.title || args.prompt || 'p5.js Artwork';
    var style = result.style || args.style || 'generative';
    var palette = result.color_palette || args.color_palette || 'vibrant';
    var code = result.code || args.code || generateClientP5Code(title, style, palette);

    var el = createAiMsgEl();
    var artId = 'p5-art-' + Math.random().toString(36).substring(2, 9);

    var html = '<div class="neby-bubble neby-p5-art-card" style="width:100%;max-width:340px;padding:12px;box-sizing:border-box;">';
    html += '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">';
    html += '  <div style="font-weight:600;font-size:0.9rem;display:flex;align-items:center;gap:6px;"><span class="material-symbols-outlined" style="font-size:1.1rem;color:#7c4dff;">palette</span> ' + escapeHtml(title) + '</div>';
    html += '  <span style="font-size:0.7rem;background:rgba(124,77,255,0.12);color:#7c4dff;padding:2px 6px;border-radius:12px;font-weight:500;">p5.js</span>';
    html += '</div>';
    html += '<div id="' + artId + '-container" style="width:100%;height:240px;border-radius:8px;overflow:hidden;background:#0f1117;position:relative;box-shadow:inset 0 0 10px rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;"></div>';
    html += '<div style="display:flex;align-items:center;justify-content:space-between;margin-top:8px;gap:4px;">';
    html += '  <button id="' + artId + '-toggle" class="neby-chip" style="font-size:0.75rem;padding:4px 8px;"><span class="material-symbols-outlined" style="font-size:0.9rem;vertical-align:middle;">pause</span> Pause</button>';
    html += '  <button id="' + artId + '-reseed" class="neby-chip" style="font-size:0.75rem;padding:4px 8px;"><span class="material-symbols-outlined" style="font-size:0.9rem;vertical-align:middle;">refresh</span> Re-seed</button>';
    html += '  <button id="' + artId + '-export" class="neby-chip" style="font-size:0.75rem;padding:4px 8px;"><span class="material-symbols-outlined" style="font-size:0.9rem;vertical-align:middle;">download</span> Save</button>';
    html += '  <button id="' + artId + '-code-btn" class="neby-chip" style="font-size:0.75rem;padding:4px 8px;"><span class="material-symbols-outlined" style="font-size:0.9rem;vertical-align:middle;">code</span> Code</button>';
    html += '</div>';
    html += '<div id="' + artId + '-code-box" style="display:none;margin-top:8px;background:#181b24;color:#a9b7c6;font-family:monospace;font-size:0.7rem;padding:8px;border-radius:6px;max-height:140px;overflow-y:auto;white-space:pre-wrap;">' + escapeHtml(code) + '</div>';
    html += '</div>';

    el.innerHTML = html;
    appendEl(el);

    ensureP5Loaded(function () {
      initP5Instance(artId, code);
    });
  }

  function ensureP5Loaded(callback) {
    if (window.p5) {
      callback();
      return;
    }
    var existing = document.getElementById('p5-cdn-script');
    if (existing) {
      existing.addEventListener('load', callback);
      return;
    }
    var script = document.createElement('script');
    script.id = 'p5-cdn-script';
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js';
    script.onload = callback;
    script.onerror = function () {
      console.error('Failed to load p5.js library');
    };
    document.head.appendChild(script);
  }

  function initP5Instance(artId, code) {
    var container = document.getElementById(artId + '-container');
    if (!container) return;

    try {
      var sketchFn = new Function('p', 'container', 'artId',
        'var setup, draw;\n' +
        'with (p) {\n' +
        '  var isLooping = true;\n' +
        '  ' + code + '\n' +
        '  if (typeof setup === "function") p.setup = setup;\n' +
        '  if (typeof draw === "function") p.draw = draw;\n' +
        '  var origSetup = p.setup;\n' +
        '  p.setup = function() {\n' +
        '    var w = container.clientWidth || 300;\n' +
        '    var h = container.clientHeight || 240;\n' +
        '    p.createCanvas(w, h);\n' +
        '    if (origSetup && origSetup !== p.setup) origSetup.call(p);\n' +
        '  };\n' +
        '}\n' +
        'var toggleBtn = document.getElementById(artId + "-toggle");\n' +
        'if (toggleBtn) {\n' +
        '  toggleBtn.onclick = function() {\n' +
        '    if (isLooping) {\n' +
        '      p.noLoop();\n' +
        '      isLooping = false;\n' +
        '      toggleBtn.innerHTML = \'<span class="material-symbols-outlined" style="font-size:0.9rem;vertical-align:middle;">play_arrow</span> Play\';\n' +
        '    } else {\n' +
        '      p.loop();\n' +
        '      isLooping = true;\n' +
        '      toggleBtn.innerHTML = \'<span class="material-symbols-outlined" style="font-size:0.9rem;vertical-align:middle;">pause</span> Pause\';\n' +
        '    }\n' +
        '  };\n' +
        '}\n' +
        'var reseedBtn = document.getElementById(artId + "-reseed");\n' +
        'if (reseedBtn) {\n' +
        '  reseedBtn.onclick = function() {\n' +
        '    p.noiseSeed(p.floor(p.random(10000)));\n' +
        '    p.randomSeed(p.floor(p.random(10000)));\n' +
        '    if (typeof p.setup === "function") p.setup();\n' +
        '    p.redraw();\n' +
        '  };\n' +
        '}\n' +
        'var exportBtn = document.getElementById(artId + "-export");\n' +
        'if (exportBtn) {\n' +
        '  exportBtn.onclick = function() {\n' +
        '    p.saveCanvas(artId + "-artwork", "png");\n' +
        '  };\n' +
        '}\n' +
        'var codeBtn = document.getElementById(artId + "-code-btn");\n' +
        'var codeBox = document.getElementById(artId + "-code-box");\n' +
        'if (codeBtn && codeBox) {\n' +
        '  codeBtn.onclick = function() {\n' +
        '    codeBox.style.display = codeBox.style.display === "none" ? "block" : "none";\n' +
        '  };\n' +
        '}'
      );

      new window.p5(function (p) {
        sketchFn(p, container, artId);
      }, container);
    } catch (e) {
      console.error('Error running p5 sketch:', e);
      container.innerHTML = '<div style="color:#ff5252;padding:12px;font-size:0.8rem;text-align:center;">Error initializing artwork sketch.</div>';
    }
  }

  function generateClientP5Code(prompt, style, palette) {
    return `
      let particles = [];
      let num = 120;

      setup = function() {
        background(15, 17, 23);
        for(let i=0; i<num; i++) {
          particles.push({
            x: random(width),
            y: random(height),
            vx: random(-1, 1),
            vy: random(-1, 1),
            color: color(random(100,255), random(100,220), random(200,255), 180)
          });
        }
      };

      draw = function() {
        background(15, 17, 23, 25);
        for(let p of particles) {
          let angle = noise(p.x * 0.005, p.y * 0.005, frameCount * 0.005) * TWO_PI * 2;
          p.vx = cos(angle) * 1.5;
          p.vy = sin(angle) * 1.5;
          p.x += p.vx;
          p.y += p.vy;
          if (p.x < 0) p.x = width; if (p.x > width) p.x = 0;
          if (p.y < 0) p.y = height; if (p.y > height) p.y = 0;

          stroke(p.color);
          strokeWeight(2);
          point(p.x, p.y);
        }
      };
    `;
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
