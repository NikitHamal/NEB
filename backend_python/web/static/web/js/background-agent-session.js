(function () {
  'use strict';

  const app = document.getElementById('background-agent-session');
  if (!app) return;

  const SESSION_ID = app.dataset.sessionId;
  const urls = {
    detail: app.dataset.detailUrl,
    events: app.dataset.eventsUrl,
    message: app.dataset.messageUrl,
    control: app.dataset.controlUrl,
    action: app.dataset.actionUrl,
    dashboard: app.dataset.dashboardUrl,
    loginUrl: app.dataset.loginUrl || '/backgroundagent/login',
  };

  // Defensive helpers: a missing element must never crash the whole session.
  const $ = (id) => document.getElementById(id);
  const on = (el, evt, fn) => { if (el) el.addEventListener(evt, fn); };
  const setHTML = (el, html) => { if (el) el.innerHTML = html; };
  const setText = (el, text) => { if (el) el.textContent = text; };
  const setHidden = (el, hidden) => { if (el) el.hidden = !!hidden; };

  const els = {
    statusBadge: $('bs-status-badge'),
    statusIcon: $('bs-status-icon'),
    detailRepo: $('bs-detail-repo'),
    detailBranch: $('bs-detail-branch'),
    detailTitle: $('bs-detail-title'),
    progressLabel: $('bs-progress-label'),
    progressValue: $('bs-progress-value'),
    progressBar: $('bs-progress-bar'),
    providerLabel: $('bs-provider-label'),
    iterationLabel: $('bs-iteration-label'),
    updatedLabel: $('bs-updated-label'),
    pause: $('bs-pause'),
    resume: $('bs-resume'),
    stop: $('bs-stop'),
    refresh: $('bs-refresh'),
    conversation: $('bs-conversation'),
    followup: $('bs-followup'),
    sendFollowup: $('bs-send-followup'),
    fileCount: $('bs-file-count'),
    changedFiles: $('bs-changed-files'),
    diff: $('bs-diff'),
    copyDiff: $('bs-copy-diff'),
    downloadActions: $('bs-download-actions'),
    push: $('bs-push'),
    openPr: $('bs-open-pr'),
    actionHistory: $('bs-action-history'),
    toastRegion: $('bs-toast-region'),
  };

  const TOOL_ICON = {
    read_file: 'description', write_file: 'edit_note', edit_file: 'edit', multi_edit: 'edit_note',
    delete_file: 'delete', copy_file: 'content_copy', move_file: 'drive_file_move',
    create_directory: 'create_new_folder', list_files: 'folder_open', search_text: 'search',
    apply_patch: 'difference', run_command: 'terminal',
    git_status: 'task', git_diff: 'difference', git_log: 'history', git_stage: 'add_circle',
    git_commit: 'commit', git_push: 'cloud_upload', git_pull: 'cloud_download', git_restore: 'undo',
  };

  const model = {
    detail: null,
    lastEventId: 0,
    polling: false,
    loadingDetail: false,
    pollTimer: null,
    stickToBottom: true,
    renderedSignature: '',
    terminalStatusSeen: false,
  };

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  function toast(message, type) {
    if (!els.toastRegion) return;
    const node = document.createElement('div');
    node.className = 'ba-toast' + (type === 'error' ? ' error' : '');
    node.textContent = message;
    els.toastRegion.appendChild(node);
    setTimeout(() => node.remove(), 4200);
  }

  function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(';') : [];
    for (const rawCookie of cookies) {
      const cookie = rawCookie.trim();
      if (cookie.startsWith(`${name}=`)) return decodeURIComponent(cookie.slice(name.length + 1));
    }
    return '';
  }

  async function api(url, options) {
    const opts = Object.assign({ credentials: 'same-origin' }, options || {});
    opts.headers = Object.assign({ 'Accept': 'application/json' }, opts.headers || {});
    if (opts.body && typeof opts.body !== 'string') {
      opts.headers['Content-Type'] = 'application/json';
      opts.body = JSON.stringify(opts.body);
    }
    if (opts.method && opts.method !== 'GET') opts.headers['X-CSRFToken'] = getCookie('csrftoken');
    const response = await fetch(url, opts);
    let data;
    try { data = await response.json(); } catch (_) { data = { ok: false, error: 'Server returned an invalid response.' }; }
    if (response.status === 401 || data.authRequired) {
      const next = encodeURIComponent(window.location.pathname + window.location.search);
      window.location.href = urls.loginUrl + '?next=' + next;
      throw new Error('Session expired. Redirecting to sign in…');
    }
    if (!response.ok || data.ok === false) throw new Error(data.error || `Request failed (${response.status})`);
    return data;
  }

  function formatTime(ms) {
    if (!ms) return '—';
    const date = new Date(Number(ms));
    const diff = Math.max(0, Date.now() - date.getTime());
    if (diff < 60000) return 'just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return date.toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  }

  function statusLabel(status) {
    return ({ queued: 'Queued', preparing: 'Preparing', running: 'Running', paused: 'Paused', waiting: 'Waiting', completed: 'Completed', failed: 'Failed', cancelled: 'Cancelled' })[status] || status;
  }

  function statusIconName(status) {
    return ({ queued: 'schedule', preparing: 'sync', running: 'smart_toy', paused: 'pause_circle', waiting: 'help', completed: 'check_circle', failed: 'error', cancelled: 'cancel' })[status] || 'pending';
  }

  // ---- smart auto-scroll ----
  function nearBottom() {
    const el = els.conversation;
    if (!el) return true;
    return el.scrollHeight - el.scrollTop - el.clientHeight < 90;
  }
  on(els.conversation, 'scroll', () => { model.stickToBottom = nearBottom(); });

  function scrollToBottom() {
    const el = els.conversation;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
    model.stickToBottom = true;
  }

  // ---- loading ----
  async function loadDetail(quiet) {
    if (model.loadingDetail) return;
    model.loadingDetail = true;
    try {
      const data = await api(urls.detail);
      model.detail = data.session;
      model.lastEventId = Math.max(0, ...(model.detail.events || []).map(e => Number(e.id || 0)));
      model.renderedSignature = '';
      render();
    } catch (error) {
      if (!quiet) toast(error.message, 'error');
    } finally {
      model.loadingDetail = false;
    }
  }

  async function pollEvents() {
    if (!model.detail || model.polling || model.loadingDetail) return;
    model.polling = true;
    try {
      const data = await api(`${urls.events}?after=${model.lastEventId}`);
      if (!model.detail) return;
      const summary = Object.assign({}, data.session || {});
      delete summary.goal;
      model.detail = Object.assign({}, model.detail, summary);
      model.detail.actions = data.actions || model.detail.actions || [];
      model.detail.artifacts = data.artifacts || model.detail.artifacts || {};
      const knownEvents = new Set((model.detail.events || []).map(e => Number(e.id)));
      const knownMessages = new Set((model.detail.messages || []).map(m => String(m.id)));
      let needsFull = false;
      let becameTerminal = false;
      for (const event of (data.events || [])) {
        const id = Number(event.id || 0);
        model.lastEventId = Math.max(model.lastEventId, id);
        if (!knownEvents.has(id)) {
          (model.detail.events = model.detail.events || []).push(event);
          knownEvents.add(id);
        }
        const message = event.payload && event.payload.message;
        if (message && !knownMessages.has(String(message.id))) {
          (model.detail.messages = model.detail.messages || []).push(message);
          knownMessages.add(String(message.id));
        }
        if (event.type === 'session.completed' || event.type === 'artifacts.rebuilt') needsFull = true;
        if (['session.completed', 'session.failed', 'session.cancelled'].includes(event.type)) becameTerminal = true;
      }
      model.detail.events = (model.detail.events || []).slice(-600);
      model.detail.messages = (model.detail.messages || []).slice(-400);
      if (needsFull) { await loadDetail(true); }
      else render();
      if (becameTerminal && !model.terminalStatusSeen) {
        model.terminalStatusSeen = true;
        model.stickToBottom = true;
        render();
      }
    } catch (_) { /* transient; retried next interval */ }
    finally { model.polling = false; }
  }

  // ---- rendering ----
  function render() {
    const session = model.detail;
    if (!session) return;

    if (els.statusBadge) { els.statusBadge.className = `ba-status-badge ${escapeHtml(session.status)}`; els.statusBadge.textContent = statusLabel(session.status); }
    if (els.statusIcon) { els.statusIcon.className = `ba-status-icon ${escapeHtml(session.status)}`; els.statusIcon.innerHTML = `<span class="material-symbols-outlined">${statusIconName(session.status)}</span>`; }
    setText(els.detailRepo, session.repoFullName || '');
    setText(els.detailBranch, session.workBranch || session.sourceBranch || '');
    setText(els.progressLabel, session.progressLabel || statusLabel(session.status));
    setText(els.progressValue, `${session.progress || 0}%`);
    if (els.progressBar) els.progressBar.style.width = `${session.progress || 0}%`;
    setText(els.providerLabel, session.provider ? `${session.provider.provider}/${session.provider.model}` : '');
    setText(els.iterationLabel, `Iteration ${session.iteration || 0}`);
    setText(els.updatedLabel, `Updated ${formatTime(session.updatedAt || session.createdAt)}`);

    const active = ['queued', 'preparing', 'running'].includes(session.status);
    setHidden(els.pause, !active);
    setHidden(els.resume, !['paused', 'waiting', 'failed', 'completed'].includes(session.status));
    if (els.stop) els.stop.disabled = ['completed', 'cancelled'].includes(session.status);

    renderConversation(session);
    renderFiles(session.changedFiles || []);
    setText(els.diff, session.diff || 'No diff available yet. It appears when the agent finishes or rebuilds artifacts.');
    renderDelivery(session);

    // Stop polling once the session has settled into a terminal state.
    if (['completed', 'failed', 'cancelled'].includes(session.status)) {
      if (model.pollTimer) { clearInterval(model.pollTimer); model.pollTimer = null; }
    }
  }

  function renderConversation(session) {
    if (!els.conversation) return;
    const messages = session.messages || [];
    // Signature so we skip no-op re-renders (preserves the user's scroll position).
    const signature = messages.map(m => `${m.id}:${m.createdAt}`).join('|');
    if (signature === model.renderedSignature) return;
    const firstRender = !model.renderedSignature;
    model.renderedSignature = signature;

    if (!messages.length) {
      els.conversation.innerHTML = '<div class="ba-empty-small">The agent activity stream will appear here.</div>';
      return;
    }
    const rows = messages
      .slice()
      .sort((a, b) => Number(a.createdAt || 0) - Number(b.createdAt || 0));
    const html = rows.map(message =>
      message.role === 'tool' ? renderToolRow(message) : renderMessage(message)
    ).join('');
    const wasNear = firstRender || model.stickToBottom;
    const prevScroll = els.conversation.scrollTop;
    els.conversation.innerHTML = html;
    if (wasNear) scrollToBottom();
    else els.conversation.scrollTop = prevScroll;
  }

  function renderMessage(message) {
    const role = message.role || 'assistant';
    const icon = role === 'user' ? 'person' : role === 'system' ? 'settings' : 'smart_toy';
    let content = String(message.content || '');
    if (role !== 'tool' && content.length > 20000) content = content.slice(0, 20000) + '\n…';
    return `<article class="ba-message ${escapeHtml(role)}">
      <div class="ba-message-avatar"><span class="material-symbols-outlined">${icon}</span></div>
      <div>
        <div class="ba-message-head"><strong>${escapeHtml(role === 'assistant' ? 'Agent' : role)}</strong><time>${escapeHtml(formatTime(message.createdAt))}</time></div>
        <div class="ba-message-body">${escapeHtml(content)}</div>
      </div>
    </article>`;
  }

  function renderToolRow(message) {
    const meta = message.metadata || {};
    const label = message.label || meta.label || (meta.tool ? meta.tool.replace(/_/g, ' ') : 'Tool');
    const ok = meta.ok !== false;
    const icon = ok ? (TOOL_ICON[meta.tool] || 'bolt') : 'error';
    let body = '';
    try {
      const obj = JSON.parse(message.content || '{}');
      if (obj.error) body = String(obj.error);
      else if (obj.result != null) body = typeof obj.result === 'string' ? obj.result : JSON.stringify(obj.result, null, 2);
      else body = JSON.stringify(obj, null, 2);
    } catch (_) { body = String(message.content || ''); }
    if (body.length > 8000) body = body.slice(0, 8000) + '\n…';
    const bodyClass = ok ? '' : ' ba-tool-error';
    const id = 'tr-' + String(message.id).replace(/[^a-z0-9]/gi, '');
    return `<article class="ba-tool-row ${ok ? 'ok' : 'failed'}" id="${id}">
      <div class="ba-tool-icon"><span class="material-symbols-outlined">${icon}</span></div>
      <div class="ba-tool-main">
        <div class="ba-tool-line" data-toggle="${id}">
          <span class="ba-tool-label">${escapeHtml(label)}</span>
          <span class="ba-tool-toggle">${ok ? '' : 'failed'}<span class="material-symbols-outlined">expand_more</span></span>
        </div>
        <pre class="ba-tool-result${bodyClass}">${escapeHtml(body)}</pre>
      </div>
    </article>`;
  }

  function renderFiles(files) {
    setText(els.fileCount, String(files.length));
    setHTML(els.changedFiles, files.length ? files.map(path => `<div class="ba-file-row"><span class="material-symbols-outlined">description</span><span>${escapeHtml(path)}</span></div>`).join('') : '<div class="ba-empty-small">No changed files recorded yet.</div>');
  }

  function renderDelivery(session) {
    const artifacts = session.artifacts || {};
    const buttons = [];
    if (artifacts.changes_zip) buttons.push(`<a class="ba-btn ba-btn-primary" href="${escapeHtml(artifacts.changes_zip.downloadUrl)}"><span class="material-symbols-outlined">folder_zip</span>ZIP</a>`);
    if (artifacts.patch) buttons.push(`<a class="ba-btn ba-btn-ghost" href="${escapeHtml(artifacts.patch.downloadUrl)}"><span class="material-symbols-outlined">difference</span>Patch</a>`);
    if (!buttons.length) buttons.push('<button class="ba-btn ba-btn-ghost" type="button" data-rebuild-artifacts><span class="material-symbols-outlined">refresh</span>Build artifacts</button>');
    setHTML(els.downloadActions, buttons.join(''));
    const hasWorkspace = !!session.workBranch;
    const running = ['queued', 'preparing', 'running'].includes(session.status);
    if (els.push) els.push.disabled = !hasWorkspace || running;
    if (els.openPr) els.openPr.disabled = !hasWorkspace || running;
    const actions = session.actions || [];
    setHTML(els.actionHistory, actions.length ? actions.map(action => {
      const link = action.result && action.result.url ? `<a href="${escapeHtml(action.result.url)}" target="_blank" rel="noopener">Open on GitHub</a>` : '';
      return `<div class="ba-action-row"><span><strong>${escapeHtml(action.action.replace('_', ' '))}</strong> · ${escapeHtml(action.status)}${action.error ? ` · ${escapeHtml(action.error)}` : ''}</span>${link}</div>`;
    }).join('') : '');
  }

  // ---- actions ----
  async function control(command) {
    try {
      await api(urls.control, { method: 'POST', body: { command } });
      toast(`${command.charAt(0).toUpperCase() + command.slice(1)} requested.`);
      await loadDetail(true);
    } catch (error) { toast(error.message, 'error'); }
  }

  async function sendFollowup() {
    const content = els.followup ? els.followup.value.trim() : '';
    if (!content) return;
    if (els.sendFollowup) els.sendFollowup.disabled = true;
    try {
      await api(urls.message, { method: 'POST', body: { content, resume: true } });
      if (els.followup) els.followup.value = '';
      model.terminalStatusSeen = false; // a resume may restart the loop
      model.stickToBottom = true;
      await loadDetail(true);
      startPolling();
      toast('Guidance sent to the agent.');
    } catch (error) { toast(error.message, 'error'); }
    finally { if (els.sendFollowup) els.sendFollowup.disabled = false; }
  }

  async function queueAction(action, payload) {
    try {
      await api(urls.action, { method: 'POST', body: { action, payload: payload || {} } });
      toast(`${action.replace('_', ' ')} queued.`);
      await loadDetail(true);
    } catch (error) { toast(error.message, 'error'); }
  }

  function activateTab(name) {
    document.querySelectorAll('.ba-tab').forEach(tab => tab.classList.toggle('active', tab.dataset.tab === name));
    document.querySelectorAll('.ba-tab-panel').forEach(panel => panel.classList.toggle('active', panel.id === `bs-tab-${name}`));
  }

  function startPolling() {
    if (model.pollTimer) clearInterval(model.pollTimer);
    model.pollTimer = setInterval(() => {
      if (!document.hidden && model.detail && !['completed', 'failed', 'cancelled'].includes(model.detail.status)) pollEvents();
    }, 2500);
  }

  // ---- events (each guarded so one missing node never breaks the page) ----
  on(els.pause, 'click', () => control('pause'));
  on(els.resume, 'click', () => control('resume'));
  on(els.stop, 'click', () => { if (confirm('Stop this session? The task branch and workspace will be preserved.')) control('stop'); });
  on(els.refresh, 'click', () => loadDetail(false));
  on(els.sendFollowup, 'click', sendFollowup);
  on(els.followup, 'keydown', event => { if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') sendFollowup(); });
  on(els.copyDiff, 'click', async () => { try { await navigator.clipboard.writeText((model.detail && model.detail.diff) || ''); toast('Diff copied.'); } catch (_) { toast('Could not copy the diff.', 'error'); } });
  on(els.push, 'click', () => queueAction('push'));
  on(els.openPr, 'click', () => queueAction('open_pr'));
  on(els.downloadActions, 'click', event => { if (event.target.closest('[data-rebuild-artifacts]')) queueAction('artifacts'); });
  document.querySelectorAll('.ba-tab').forEach(tab => tab.addEventListener('click', () => activateTab(tab.dataset.tab)));
  // Toggle tool result expansion (event delegation for dynamically rendered rows).
  on(els.conversation, 'click', event => {
    const line = event.target.closest('[data-toggle]');
    if (line) {
      const target = document.getElementById(line.dataset.toggle);
      if (target) target.classList.toggle('open');
    }
  });
  document.addEventListener('visibilitychange', () => { if (!document.hidden && model.detail) loadDetail(true); });

  // ---- boot ----
  loadDetail().then(() => {
    model.stickToBottom = true;
    if (model.detail) {
      scrollToBottom();
      if (!['completed', 'failed', 'cancelled'].includes(model.detail.status)) startPolling();
    }
  });
})();
