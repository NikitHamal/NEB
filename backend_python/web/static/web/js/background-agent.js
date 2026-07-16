(function () {
  'use strict';

  const app = document.getElementById('background-agent-app');
  if (!app) return;

  const urls = {
    state: app.dataset.stateUrl,
    repositories: app.dataset.repositoriesUrl,
    branches: app.dataset.branchesUrl,
    projects: app.dataset.projectsUrl,
    sessions: app.dataset.sessionsUrl,
    connect: app.dataset.connectUrl,
    disconnect: app.dataset.disconnectUrl
  };

  const $ = (id) => document.getElementById(id);
  const els = {
    connectEmpty: $('ba-connect-empty'), workspace: $('ba-workspace'), connect: $('ba-connect-button'), disconnect: $('ba-disconnect-button'), workerStatus: $('ba-worker-status'),
    account: $('ba-github-account'), projectList: $('ba-project-list'), sessionList: $('ba-session-list'), sessionCount: $('ba-session-count'),
    projectSelect: $('ba-project-select'), branchSelect: $('ba-branch-select'), providerSelect: $('ba-provider-select'), maxIterations: $('ba-max-iterations'),
    goal: $('ba-goal'), start: $('ba-start'), addProject: $('ba-add-project'), detailEmpty: $('ba-session-empty'), detail: $('ba-session-detail'),
    detailRepo: $('ba-detail-repo'), detailBranch: $('ba-detail-branch'), detailTitle: $('ba-detail-title'), statusIcon: $('ba-status-icon'),
    progressLabel: $('ba-progress-label'), progressValue: $('ba-progress-value'), progressBar: $('ba-progress-bar'), providerLabel: $('ba-provider-label'),
    iterationLabel: $('ba-iteration-label'), updatedLabel: $('ba-updated-label'), pause: $('ba-pause'), resume: $('ba-resume'), stop: $('ba-stop'), refresh: $('ba-more'),
    conversation: $('ba-conversation'), followup: $('ba-followup'), sendFollowup: $('ba-send-followup'), changedFiles: $('ba-changed-files'),
    fileCount: $('ba-file-count'), diff: $('ba-diff'), copyDiff: $('ba-copy-diff'), downloadActions: $('ba-download-actions'), push: $('ba-push'),
    openPr: $('ba-open-pr'), actionHistory: $('ba-action-history'), dialog: $('ba-repo-dialog'), repoSearch: $('ba-repo-search'),
    repoRefresh: $('ba-repo-refresh'), repoResults: $('ba-repo-results'), repoConfig: $('ba-repo-config'), repoBack: $('ba-repo-back'),
    selectedRepoName: $('ba-selected-repo-name'), repoBaseBranch: $('ba-repo-base-branch'), saveProject: $('ba-save-project'), toastRegion: $('ba-toast-region')
  };

  const model = {
    github: { connected: false },
    projects: [],
    sessions: [],
    providers: [],
    worker: { online: 0, healthy: false },
    selectedProjectId: '',
    selectedSessionId: '',
    detail: null,
    selectedRepo: null,
    repositoryResults: [],
    branchCache: new Map(),
    branchProjectId: '',
    pollTimer: null,
    stateTimer: null,
    loadingDetail: false,
    pollingEvents: false,
    lastEventId: 0
  };

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  function toast(message, type) {
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
    if (!response.ok || data.ok === false) throw new Error(data.error || `Request failed (${response.status})`);
    return data;
  }

  function formatTime(ms) {
    if (!ms) return '—';
    const date = new Date(Number(ms));
    const now = Date.now();
    const diff = Math.max(0, now - date.getTime());
    if (diff < 60000) return 'just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return date.toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  }

  function statusIcon(status) {
    return ({
      queued: 'schedule', preparing: 'sync', running: 'smart_toy', paused: 'pause_circle', waiting: 'help',
      completed: 'check_circle', failed: 'error', cancelled: 'cancel'
    })[status] || 'pending';
  }

  function statusLabel(status) {
    return ({ queued: 'Queued', preparing: 'Preparing', running: 'Running', paused: 'Paused', waiting: 'Waiting', completed: 'Completed', failed: 'Failed', cancelled: 'Cancelled' })[status] || status;
  }

  async function loadState(options) {
    const preserve = options && options.preserveSelection;
    try {
      const data = await api(urls.state);
      model.github = data.github || { connected: false };
      model.projects = data.projects || [];
      model.sessions = data.sessions || [];
      model.providers = data.providers || [];
      model.worker = data.worker || { online: 0, healthy: false };
      if (!preserve || !model.selectedProjectId || !model.projects.some(p => p.id === model.selectedProjectId)) {
        model.selectedProjectId = model.projects[0] ? model.projects[0].id : '';
      }
      if (!preserve && !model.selectedSessionId && model.sessions[0]) model.selectedSessionId = model.sessions[0].id;
      renderState();
      if (model.selectedProjectId) await loadProjectBranches(model.selectedProjectId, false);
      if (model.selectedSessionId && (!preserve || !model.detail || model.detail.id !== model.selectedSessionId)) {
        await loadDetail(model.selectedSessionId, true);
      }
    } catch (error) {
      toast(error.message, 'error');
    }
  }

  function renderState() {
    const workerOnline = Number(model.worker.online || 0);
    els.workerStatus.classList.toggle('offline', !workerOnline);
    els.workerStatus.querySelector('.material-symbols-outlined').textContent = workerOnline ? 'cloud_done' : 'cloud_off';
    els.workerStatus.querySelector('span:last-child').textContent = workerOnline ? `${workerOnline} worker${workerOnline === 1 ? '' : 's'} online` : 'Worker offline';
    const connected = !!model.github.connected;
    els.connectEmpty.hidden = connected;
    els.workspace.hidden = !connected;
    els.connect.hidden = connected;
    els.disconnect.hidden = !connected;
    if (!connected) return;

    els.account.innerHTML = `${model.github.avatarUrl ? `<img src="${escapeHtml(model.github.avatarUrl)}" alt="">` : '<div class="ba-repo-icon"><span class="material-symbols-outlined">person</span></div>'}<div><strong>@${escapeHtml(model.github.login || 'github')}</strong><span>Repository access connected</span></div>`;

    els.projectList.innerHTML = model.projects.length ? model.projects.map(project => `
      <button class="ba-project-item ${project.id === model.selectedProjectId ? 'active' : ''}" type="button" data-project-id="${escapeHtml(project.id)}">
        <span class="ba-repo-icon"><span class="material-symbols-outlined">${project.private ? 'lock' : 'folder_open'}</span></span>
        <span class="ba-project-copy"><strong>${escapeHtml(project.repoFullName)}</strong><span>${escapeHtml(project.preferredBaseBranch || project.defaultBranch)} · ${escapeHtml(project.status)}</span></span>
      </button>`).join('') : '<div class="ba-empty-small">Add a repository to create an isolated codebase.</div>';

    els.sessionCount.textContent = String(model.sessions.length);
    els.sessionList.innerHTML = model.sessions.length ? model.sessions.map(session => `
      <button class="ba-session-item ${session.id === model.selectedSessionId ? 'active' : ''}" type="button" data-session-id="${escapeHtml(session.id)}">
        <span class="ba-mini-status ${escapeHtml(session.status)}"></span>
        <span class="ba-session-copy"><strong>${escapeHtml(session.title || session.goal)}</strong><span>${escapeHtml(session.repoFullName)} · ${statusLabel(session.status)}</span></span>
      </button>`).join('') : '<div class="ba-empty-small">No tasks yet. Describe one in the composer.</div>';

    const projectValue = model.selectedProjectId;
    els.projectSelect.innerHTML = '<option value="">Choose a project</option>' + model.projects.map(project => `<option value="${escapeHtml(project.id)}" ${project.id === projectValue ? 'selected' : ''}>${escapeHtml(project.repoFullName)}</option>`).join('');
    const providerValue = els.providerSelect.value;
    els.providerSelect.innerHTML = model.providers.length ? model.providers.map((provider, index) => `<option value="${escapeHtml(provider.id)}" ${(String(provider.id) === String(providerValue) || (!providerValue && index === 0)) ? 'selected' : ''}>${escapeHtml(provider.label)}</option>`).join('') : '<option value="">No enabled provider</option>';

    els.start.disabled = !model.projects.length || !model.providers.length;
  }

  async function loadProjectBranches(projectId, force) {
    const project = model.projects.find(item => item.id === projectId);
    if (!project) {
      els.branchSelect.innerHTML = '<option value="">Select repository first</option>';
      return;
    }
    const sameProject = model.branchProjectId === projectId;
    const currentBranch = sameProject ? els.branchSelect.value : '';
    model.selectedProjectId = projectId;
    model.branchProjectId = projectId;
    renderState();
    const repo = project.repoFullName;
    if (!force && model.branchCache.has(repo)) {
      const cached = model.branchCache.get(repo);
      const selected = currentBranch && cached.some(branch => branch.name === currentBranch)
        ? currentBranch
        : (project.preferredBaseBranch || project.defaultBranch);
      renderBranchOptions(cached, selected);
      return;
    }
    els.branchSelect.innerHTML = '<option>Loading branches…</option>';
    try {
      const data = await api(`${urls.branches}?repo=${encodeURIComponent(repo)}`);
      model.branchCache.set(repo, data.branches || []);
      renderBranchOptions(data.branches || [], project.preferredBaseBranch || data.defaultBranch);
    } catch (error) {
      els.branchSelect.innerHTML = `<option value="${escapeHtml(project.preferredBaseBranch || project.defaultBranch)}">${escapeHtml(project.preferredBaseBranch || project.defaultBranch)}</option>`;
      toast(error.message, 'error');
    }
  }

  function renderBranchOptions(branches, selected) {
    if (!branches.length) {
      els.branchSelect.innerHTML = `<option value="${escapeHtml(selected || 'main')}">${escapeHtml(selected || 'main')}</option>`;
      return;
    }
    els.branchSelect.innerHTML = branches.map(branch => `<option value="${escapeHtml(branch.name)}" ${branch.name === selected ? 'selected' : ''}>${escapeHtml(branch.name)}</option>`).join('');
  }

  async function startSession() {
    const goal = els.goal.value.trim();
    const projectId = els.projectSelect.value;
    const sourceBranch = els.branchSelect.value;
    const providerId = els.providerSelect.value;
    if (!projectId) return toast('Choose a repository project.', 'error');
    if (goal.length < 10) return toast('Describe the task in a little more detail.', 'error');
    els.start.disabled = true;
    const original = els.start.innerHTML;
    els.start.innerHTML = '<span class="material-symbols-outlined">progress_activity</span>Queuing…';
    try {
      const data = await api(urls.sessions, { method: 'POST', body: { projectId, sourceBranch, providerId, goal, maxIterations: Number(els.maxIterations.value || 30) } });
      els.goal.value = '';
      model.selectedSessionId = data.session.id;
      await loadState({ preserveSelection: true });
      await loadDetail(data.session.id, true);
      toast('Task queued. The server worker can continue after you close this page.');
    } catch (error) {
      toast(error.message, 'error');
    } finally {
      els.start.disabled = false;
      els.start.innerHTML = original;
    }
  }

  async function loadDetail(sessionId, quiet) {
    if (!sessionId || model.loadingDetail) return;
    model.loadingDetail = true;
    try {
      const data = await api(`${urls.sessions}/${encodeURIComponent(sessionId)}`);
      model.selectedSessionId = sessionId;
      model.detail = data.session;
      model.lastEventId = Math.max(0, ...(model.detail.events || []).map(event => Number(event.id || 0)));
      const found = model.sessions.findIndex(item => item.id === sessionId);
      if (found >= 0) model.sessions[found] = Object.assign({}, model.sessions[found], data.session);
      renderState();
      renderDetail();
    } catch (error) {
      if (!quiet) toast(error.message, 'error');
    } finally {
      model.loadingDetail = false;
    }
  }

  async function pollSessionEvents() {
    if (!model.selectedSessionId || !model.detail || model.pollingEvents || model.loadingDetail) return;
    model.pollingEvents = true;
    try {
      const sessionId = model.selectedSessionId;
      const data = await api(`${urls.sessions}/${encodeURIComponent(sessionId)}/events?after=${model.lastEventId}`);
      if (sessionId !== model.selectedSessionId || !model.detail) return;
      const sessionSummary = Object.assign({}, data.session || {});
      delete sessionSummary.goal;
      model.detail = Object.assign({}, model.detail, sessionSummary);
      model.detail.actions = data.actions || model.detail.actions || [];
      model.detail.artifacts = data.artifacts || model.detail.artifacts || {};
      const knownEventIds = new Set((model.detail.events || []).map(event => Number(event.id)));
      const knownMessageIds = new Set((model.detail.messages || []).map(message => String(message.id)));
      let needsFullRefresh = false;
      for (const event of (data.events || [])) {
        const eventId = Number(event.id || 0);
        model.lastEventId = Math.max(model.lastEventId, eventId);
        if (!knownEventIds.has(eventId)) {
          model.detail.events = model.detail.events || [];
          model.detail.events.push(event);
          knownEventIds.add(eventId);
        }
        const message = event.payload && event.payload.message;
        if (message && !knownMessageIds.has(String(message.id))) {
          model.detail.messages = model.detail.messages || [];
          model.detail.messages.push(message);
          knownMessageIds.add(String(message.id));
        }
        if (['session.completed', 'artifacts.rebuilt'].includes(event.type)) needsFullRefresh = true;
      }
      model.detail.events = (model.detail.events || []).slice(-500);
      model.detail.messages = (model.detail.messages || []).slice(-300);
      const found = model.sessions.findIndex(item => item.id === sessionId);
      if (found >= 0) model.sessions[found] = Object.assign({}, model.sessions[found], data.session || {});
      if (needsFullRefresh) await loadDetail(sessionId, true);
      else renderDetail();
    } catch (_) {
      // A transient polling failure is retried on the next interval. Explicit
      // user actions still surface errors through their own request paths.
    } finally {
      model.pollingEvents = false;
    }
  }

  function renderDetail() {
    const session = model.detail;
    const has = !!session;
    els.detailEmpty.hidden = has;
    els.detail.hidden = !has;
    if (!has) return;

    els.detailRepo.textContent = session.repoFullName || '';
    els.detailBranch.textContent = session.workBranch || session.sourceBranch || '';
    els.detailTitle.textContent = session.title || session.goal || 'Background task';
    els.statusIcon.className = `ba-status-icon ${session.status}`;
    els.statusIcon.innerHTML = `<span class="material-symbols-outlined">${statusIcon(session.status)}</span>`;
    els.progressLabel.textContent = session.progressLabel || statusLabel(session.status);
    els.progressValue.textContent = `${session.progress || 0}%`;
    els.progressBar.style.width = `${session.progress || 0}%`;
    els.providerLabel.textContent = session.provider ? `${session.provider.provider}/${session.provider.model}` : 'Provider unavailable';
    els.iterationLabel.textContent = `Iteration ${session.iteration || 0}/${session.maxIterations || 0}`;
    els.updatedLabel.textContent = `Updated ${formatTime(session.updatedAt || session.createdAt)}`;

    const active = ['queued', 'preparing', 'running'].includes(session.status);
    els.pause.hidden = !active;
    els.resume.hidden = !['paused', 'waiting', 'failed'].includes(session.status);
    els.stop.disabled = ['completed', 'cancelled'].includes(session.status);

    renderConversation(session);
    renderFiles(session.changedFiles || []);
    els.diff.textContent = session.diff || 'No diff available yet. It will appear when the agent finishes or rebuilds artifacts.';
    renderDelivery(session);
  }

  function renderConversation(session) {
    const messages = session.messages || [];
    const events = session.events || [];
    const rows = [];
    messages.forEach(message => rows.push({ kind: 'message', at: Number(message.createdAt || 0), value: message }));
    events.filter(event => !['message.created'].includes(event.type)).forEach(event => rows.push({ kind: 'event', at: Number(event.createdAt || 0), value: event }));
    rows.sort((a, b) => a.at - b.at);
    if (!rows.length) {
      els.conversation.innerHTML = '<div class="ba-empty-small">The worker activity stream will appear here.</div>';
      return;
    }
    els.conversation.innerHTML = rows.map(row => row.kind === 'message' ? renderMessage(row.value) : renderEvent(row.value)).join('');
    els.conversation.scrollTop = els.conversation.scrollHeight;
  }

  function renderMessage(message) {
    const role = message.role || 'assistant';
    const icon = role === 'user' ? 'person' : role === 'tool' ? 'terminal' : role === 'system' ? 'settings' : 'robot_2';
    let content = String(message.content || '');
    if (role === 'tool' && content.length > 10000) content = content.slice(0, 10000) + '\n[tool output truncated in UI]';
    return `<article class="ba-message ${escapeHtml(role)}"><div class="ba-message-avatar"><span class="material-symbols-outlined">${icon}</span></div><div><div class="ba-message-head"><strong>${escapeHtml(role === 'assistant' ? 'Agent' : role)}</strong><time>${escapeHtml(formatTime(message.createdAt))}</time></div><div class="ba-message-body">${escapeHtml(content)}</div></div></article>`;
  }

  function renderEvent(event) {
    const important = ['session.completed', 'session.failed', 'session.paused', 'session.waiting', 'github.pushed', 'github.pr_opened', 'github.pr_found', 'artifacts.rebuilt', 'repository.refreshed', 'action.failed', 'session.cancelled'].includes(event.type);
    if (!important && !String(event.type).startsWith('tool.')) return '';
    const failed = String(event.type).includes('failed');
    return `<article class="ba-message tool"><div class="ba-message-avatar"><span class="material-symbols-outlined">${failed ? 'error' : 'bolt'}</span></div><div><div class="ba-message-head"><strong>${escapeHtml(event.type.replace(/\./g, ' '))}</strong><time>${escapeHtml(formatTime(event.createdAt))}</time></div><div class="ba-message-body">${escapeHtml(event.message || '')}</div></div></article>`;
  }

  function renderFiles(files) {
    els.fileCount.textContent = String(files.length);
    els.changedFiles.innerHTML = files.length ? files.map(path => `<div class="ba-file-row"><span class="material-symbols-outlined">description</span><span>${escapeHtml(path)}</span></div>`).join('') : '<div class="ba-empty-small">No changed files recorded yet.</div>';
  }

  function renderDelivery(session) {
    const artifacts = session.artifacts || {};
    const buttons = [];
    if (artifacts.changes_zip) buttons.push(`<a class="ba-btn ba-btn-primary" href="${escapeHtml(artifacts.changes_zip.downloadUrl)}"><span class="material-symbols-outlined">folder_zip</span>ZIP</a>`);
    if (artifacts.patch) buttons.push(`<a class="ba-btn ba-btn-ghost" href="${escapeHtml(artifacts.patch.downloadUrl)}"><span class="material-symbols-outlined">difference</span>Patch</a>`);
    if (!buttons.length) buttons.push('<button class="ba-btn ba-btn-ghost" type="button" data-rebuild-artifacts><span class="material-symbols-outlined">refresh</span>Build artifacts</button>');
    els.downloadActions.innerHTML = buttons.join('');
    const hasWorkspace = !!session.workBranch;
    els.push.disabled = !hasWorkspace || ['queued', 'preparing', 'running'].includes(session.status);
    els.openPr.disabled = !hasWorkspace || ['queued', 'preparing', 'running'].includes(session.status);
    const actions = session.actions || [];
    els.actionHistory.innerHTML = actions.length ? actions.map(action => {
      const link = action.result && action.result.url ? `<a href="${escapeHtml(action.result.url)}" target="_blank" rel="noopener">Open on GitHub</a>` : '';
      return `<div class="ba-action-row"><span><strong>${escapeHtml(action.action.replace('_', ' '))}</strong> · ${escapeHtml(action.status)}${action.error ? ` · ${escapeHtml(action.error)}` : ''}</span>${link}</div>`;
    }).join('') : '';
  }

  async function control(command) {
    if (!model.selectedSessionId) return;
    try {
      await api(`${urls.sessions}/${encodeURIComponent(model.selectedSessionId)}/control`, { method: 'POST', body: { command } });
      toast(`${command.charAt(0).toUpperCase() + command.slice(1)} requested.`);
      await loadDetail(model.selectedSessionId, true);
    } catch (error) { toast(error.message, 'error'); }
  }

  async function sendFollowup() {
    const content = els.followup.value.trim();
    if (!content || !model.selectedSessionId) return;
    els.sendFollowup.disabled = true;
    try {
      await api(`${urls.sessions}/${encodeURIComponent(model.selectedSessionId)}/messages`, { method: 'POST', body: { content, resume: true } });
      els.followup.value = '';
      await loadDetail(model.selectedSessionId, true);
      toast('Guidance sent to the agent.');
    } catch (error) { toast(error.message, 'error'); }
    finally { els.sendFollowup.disabled = false; }
  }

  async function queueAction(action, payload) {
    if (!model.selectedSessionId) return;
    try {
      await api(`${urls.sessions}/${encodeURIComponent(model.selectedSessionId)}/actions`, { method: 'POST', body: { action, payload: payload || {} } });
      toast(`${action.replace('_', ' ')} queued.`);
      await loadDetail(model.selectedSessionId, true);
    } catch (error) { toast(error.message, 'error'); }
  }

  async function loadRepositories() {
    els.repoResults.innerHTML = '<div class="ba-empty-small">Loading repositories…</div>';
    els.repoConfig.hidden = true;
    els.repoResults.hidden = false;
    try {
      const q = els.repoSearch.value.trim();
      const data = await api(`${urls.repositories}?per_page=100&q=${encodeURIComponent(q)}`);
      model.repositoryResults = data.repositories || [];
      renderRepositories();
    } catch (error) {
      els.repoResults.innerHTML = `<div class="ba-empty-small">${escapeHtml(error.message)}</div>`;
    }
  }

  function renderRepositories() {
    const repos = model.repositoryResults;
    els.repoResults.innerHTML = repos.length ? repos.map(repo => `
      <button class="ba-repo-result" type="button" data-repo-name="${escapeHtml(repo.fullName)}">
        <span class="ba-repo-icon"><span class="material-symbols-outlined">${repo.private ? 'lock' : 'folder_open'}</span></span>
        <span class="ba-repo-result-copy"><strong>${escapeHtml(repo.fullName)}</strong><p>${escapeHtml(repo.description || `Default branch: ${repo.defaultBranch}`)}</p></span>
        <span class="ba-repo-badges"><span class="ba-repo-badge">${repo.private ? 'Private' : 'Public'}</span>${repo.canPush ? '<span class="ba-repo-badge">Write</span>' : '<span class="ba-repo-badge">Read</span>'}</span>
      </button>`).join('') : '<div class="ba-empty-small">No matching repositories were returned by GitHub.</div>';
  }

  async function selectRepository(fullName) {
    const repo = model.repositoryResults.find(item => item.fullName === fullName);
    if (!repo) return;
    model.selectedRepo = repo;
    els.repoResults.hidden = true;
    els.repoConfig.hidden = false;
    els.selectedRepoName.textContent = repo.fullName;
    els.repoBaseBranch.innerHTML = `<option>${escapeHtml(repo.defaultBranch)}</option>`;
    try {
      const data = await api(`${urls.branches}?repo=${encodeURIComponent(repo.fullName)}`);
      els.repoBaseBranch.innerHTML = (data.branches || []).map(branch => `<option value="${escapeHtml(branch.name)}" ${branch.name === repo.defaultBranch ? 'selected' : ''}>${escapeHtml(branch.name)}</option>`).join('');
    } catch (error) { toast(error.message, 'error'); }
  }

  async function saveProject() {
    if (!model.selectedRepo) return;
    els.saveProject.disabled = true;
    try {
      const data = await api(urls.projects, { method: 'POST', body: { repoFullName: model.selectedRepo.fullName, baseBranch: els.repoBaseBranch.value } });
      model.selectedProjectId = data.project.id;
      els.dialog.close();
      await loadState({ preserveSelection: true });
      await loadProjectBranches(data.project.id, true);
      toast('Repository added. Its mirror will be prepared by the worker when the first task starts.');
    } catch (error) { toast(error.message, 'error'); }
    finally { els.saveProject.disabled = false; }
  }

  function openRepositoryDialog() {
    model.selectedRepo = null;
    els.repoConfig.hidden = true;
    els.repoResults.hidden = false;
    els.dialog.showModal();
    loadRepositories();
  }

  function activateTab(name) {
    document.querySelectorAll('.ba-tab').forEach(tab => tab.classList.toggle('active', tab.dataset.tab === name));
    document.querySelectorAll('.ba-tab-panel').forEach(panel => panel.classList.toggle('active', panel.id === `ba-tab-${name}`));
  }

  function startPolling() {
    clearInterval(model.pollTimer);
    clearInterval(model.stateTimer);
    model.pollTimer = setInterval(() => {
      if (model.selectedSessionId && !document.hidden) pollSessionEvents();
    }, 3000);
    model.stateTimer = setInterval(() => {
      if (!document.hidden) loadState({ preserveSelection: true });
    }, 15000);
  }

  els.addProject.addEventListener('click', openRepositoryDialog);
  els.disconnect.addEventListener('click', async () => {
    if (!confirm('Disconnect GitHub? Running sessions may fail when they next access the repository.')) return;
    try { await api(urls.disconnect, { method: 'POST', body: {} }); window.location.reload(); } catch (error) { toast(error.message, 'error'); }
  });
  els.projectList.addEventListener('click', event => {
    const button = event.target.closest('[data-project-id]');
    if (button) loadProjectBranches(button.dataset.projectId, false);
  });
  els.sessionList.addEventListener('click', event => {
    const button = event.target.closest('[data-session-id]');
    if (button) loadDetail(button.dataset.sessionId, false);
  });
  els.projectSelect.addEventListener('change', () => loadProjectBranches(els.projectSelect.value, false));
  els.start.addEventListener('click', startSession);
  els.goal.addEventListener('keydown', event => { if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') startSession(); });
  els.pause.addEventListener('click', () => control('pause'));
  els.resume.addEventListener('click', () => control('resume'));
  els.stop.addEventListener('click', () => { if (confirm('Stop this session? The task branch and current workspace will be preserved.')) control('stop'); });
  els.refresh.addEventListener('click', () => loadDetail(model.selectedSessionId, false));
  els.sendFollowup.addEventListener('click', sendFollowup);
  els.followup.addEventListener('keydown', event => { if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') sendFollowup(); });
  els.copyDiff.addEventListener('click', async () => { try { await navigator.clipboard.writeText((model.detail && model.detail.diff) || ''); toast('Diff copied.'); } catch (_) { toast('Could not copy the diff.', 'error'); } });
  els.push.addEventListener('click', () => queueAction('push'));
  els.openPr.addEventListener('click', () => queueAction('open_pr'));
  els.downloadActions.addEventListener('click', event => { if (event.target.closest('[data-rebuild-artifacts]')) queueAction('artifacts'); });
  document.querySelectorAll('.ba-tab').forEach(tab => tab.addEventListener('click', () => activateTab(tab.dataset.tab)));
  els.dialog.querySelectorAll('[data-close-dialog]').forEach(button => button.addEventListener('click', () => els.dialog.close()));
  els.repoRefresh.addEventListener('click', loadRepositories);
  let searchTimer;
  els.repoSearch.addEventListener('input', () => { clearTimeout(searchTimer); searchTimer = setTimeout(loadRepositories, 350); });
  els.repoResults.addEventListener('click', event => { const button = event.target.closest('[data-repo-name]'); if (button) selectRepository(button.dataset.repoName); });
  els.repoBack.addEventListener('click', () => { model.selectedRepo = null; els.repoConfig.hidden = true; els.repoResults.hidden = false; });
  els.saveProject.addEventListener('click', saveProject);
  document.addEventListener('visibilitychange', () => { if (!document.hidden && model.selectedSessionId) loadDetail(model.selectedSessionId, true); });

  loadState().then(startPolling);
})();
