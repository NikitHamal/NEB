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
    disconnect: app.dataset.disconnectUrl,
    loginUrl: app.dataset.loginUrl || '/backgroundagent/login',
    sessionPage: app.dataset.sessionPageBase, // base like ".../session/"
  };

  // Element lookup that tolerates a missing node (defensive: one missing id
  // must never kill the whole dashboard).
  const $ = (id) => document.getElementById(id);
  const on = (el, evt, fn) => { if (el) el.addEventListener(evt, fn); };
  const setHTML = (el, html) => { if (el) el.innerHTML = html; };
  const setText = (el, text) => { if (el) el.textContent = text; };
  const setHidden = (el, hidden) => { if (el) el.hidden = !!hidden; };

  const els = {
    workerStatus: $('ba-worker-status'),
    disconnect: $('ba-disconnect-button'),
    connectEmpty: $('ba-connect-empty'),
    workspace: $('ba-workspace'),
    account: $('ba-github-account'),
    projectList: $('ba-project-list'),
    addProject: $('ba-add-project'),
    projectSelect: $('ba-project-select'),
    branchSelect: $('ba-branch-select'),
    providerSelect: $('ba-provider-select'),
    goal: $('ba-goal'),
    start: $('ba-start'),
    sessionList: $('ba-session-list'),
    sessionCount: $('ba-session-count'),
    dialog: $('ba-repo-dialog'),
    repoSearch: $('ba-repo-search'),
    repoRefresh: $('ba-repo-refresh'),
    repoResults: $('ba-repo-results'),
    repoConfig: $('ba-repo-config'),
    repoBack: $('ba-repo-back'),
    selectedRepoName: $('ba-selected-repo-name'),
    repoBaseBranch: $('ba-repo-base-branch'),
    saveProject: $('ba-save-project'),
    toastRegion: $('ba-toast-region'),
  };

  const model = {
    github: { connected: false },
    projects: [],
    sessions: [],
    providers: [],
    worker: { online: 0, healthy: false },
    selectedProjectId: '',
    selectedRepo: null,
    repositoryResults: [],
    branchCache: new Map(),
    branchProjectId: '',
    pollTimer: null,
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
      // Session expired — send the admin back to the standalone login.
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

  async function loadState() {
    try {
      const data = await api(urls.state);
      model.github = data.github || { connected: false };
      model.projects = data.projects || [];
      model.sessions = data.sessions || [];
      model.providers = data.providers || [];
      model.worker = data.worker || { online: 0, healthy: false };
      if (!model.selectedProjectId || !model.projects.some(p => p.id === model.selectedProjectId)) {
        model.selectedProjectId = model.projects[0] ? model.projects[0].id : '';
      }
      renderState();
      if (model.selectedProjectId) await loadProjectBranches(model.selectedProjectId, false);
    } catch (error) {
      toast(error.message, 'error');
    }
  }

  function renderState() {
    const online = Number(model.worker.online || 0);
    if (els.workerStatus) {
      els.workerStatus.classList.toggle('online', !!online);
      els.workerStatus.classList.toggle('offline', !online);
      const icon = els.workerStatus.querySelector('.material-symbols-outlined');
      const label = els.workerStatus.querySelector('.ba-worker-label');
      if (icon) icon.textContent = online ? 'cloud_done' : 'cloud_off';
      if (label) label.textContent = online ? `${online} worker${online === 1 ? '' : 's'} online` : 'Worker offline';
    }

    const connected = !!model.github.connected;
    setHidden(els.connectEmpty, connected);
    setHidden(els.workspace, !connected);
    setHidden(els.disconnect, !connected);
    if (connected) {
      const avatar = model.github.avatarUrl
        ? `<img src="${escapeHtml(model.github.avatarUrl)}" alt="">`
        : `<span class="ba-ai"><span class="material-symbols-outlined">person</span></span>`;
      setHTML(els.account, `${avatar}<div><strong>@${escapeHtml(model.github.login || 'github')}</strong><span>Repository access connected</span></div>`);
    }
    if (!connected) return;

    setHTML(els.projectList, model.projects.length ? model.projects.map(project => `
      <button class="ba-project-item ${project.id === model.selectedProjectId ? 'active' : ''}" type="button" data-project-id="${escapeHtml(project.id)}">
        <span class="ba-repo-icon"><span class="material-symbols-outlined">${project.private ? 'lock' : 'folder_open'}</span></span>
        <span class="ba-project-copy"><strong>${escapeHtml(project.repoFullName)}</strong><span>${escapeHtml(project.preferredBaseBranch || project.defaultBranch)} · ${escapeHtml(project.status)}</span></span>
      </button>`).join('') : '<div class="ba-empty-small">Add a repository to create a codebase.</div>');

    setText(els.sessionCount, String(model.sessions.length));
    setHTML(els.sessionList, model.sessions.length ? model.sessions.map(session => `
      <a class="ba-session-item" href="${escapeHtml(urls.sessionPage + encodeURIComponent(session.id))}">
        <span class="ba-mini-status ${escapeHtml(session.status)}"></span>
        <span class="ba-session-copy"><strong>${escapeHtml(session.title || session.goal)}</strong><span>${escapeHtml(session.repoFullName)} · ${statusLabel(session.status)}</span></span>
        <span class="ba-session-time">${escapeHtml(formatTime(session.updatedAt || session.createdAt))}</span>
        <span class="ba-session-open"><span class="material-symbols-outlined">chevron_right</span></span>
      </a>`).join('') : '<div class="ba-empty-small">No tasks yet — describe one above and start it.</div>');

    if (els.projectSelect) {
      const projectValue = model.selectedProjectId;
      els.projectSelect.innerHTML = '<option value="">Choose a project</option>' + model.projects.map(project => `<option value="${escapeHtml(project.id)}" ${project.id === projectValue ? 'selected' : ''}>${escapeHtml(project.repoFullName)}</option>`).join('');
    }
    if (els.providerSelect) {
      const providerValue = els.providerSelect.value;
      els.providerSelect.innerHTML = model.providers.length ? model.providers.map((provider, index) => `<option value="${escapeHtml(provider.id)}" ${(String(provider.id) === String(providerValue) || (!providerValue && index === 0)) ? 'selected' : ''}>${escapeHtml(provider.label)}</option>`).join('') : '<option value="">No enabled provider</option>';
    }

    if (els.start) els.start.disabled = !model.projects.length || !model.providers.length;
  }

  async function loadProjectBranches(projectId, force) {
    const project = model.projects.find(item => item.id === projectId);
    if (!project) {
      setHTML(els.branchSelect, '<option value="">Select repository first</option>');
      return;
    }
    const sameProject = model.branchProjectId === projectId;
    const currentBranch = sameProject ? (els.branchSelect && els.branchSelect.value) : '';
    model.selectedProjectId = projectId;
    model.branchProjectId = projectId;
    renderState();
    const repo = project.repoFullName;
    if (!force && model.branchCache.has(repo)) {
      const cached = model.branchCache.get(repo);
      const selected = currentBranch && cached.some(b => b.name === currentBranch) ? currentBranch : (project.preferredBaseBranch || project.defaultBranch);
      renderBranchOptions(cached, selected);
      return;
    }
    setHTML(els.branchSelect, '<option>Loading branches…</option>');
    try {
      const data = await api(`${urls.branches}?repo=${encodeURIComponent(repo)}`);
      model.branchCache.set(repo, data.branches || []);
      renderBranchOptions(data.branches || [], project.preferredBaseBranch || data.defaultBranch);
    } catch (error) {
      setHTML(els.branchSelect, `<option value="${escapeHtml(project.preferredBaseBranch || project.defaultBranch)}">${escapeHtml(project.preferredBaseBranch || project.defaultBranch)}</option>`);
      toast(error.message, 'error');
    }
  }

  function renderBranchOptions(branches, selected) {
    if (!els.branchSelect) return;
    if (!branches.length) {
      els.branchSelect.innerHTML = `<option value="${escapeHtml(selected || 'main')}">${escapeHtml(selected || 'main')}</option>`;
      return;
    }
    els.branchSelect.innerHTML = branches.map(branch => `<option value="${escapeHtml(branch.name)}" ${branch.name === selected ? 'selected' : ''}>${escapeHtml(branch.name)}</option>`).join('');
  }

  async function startSession() {
    const goal = els.goal ? els.goal.value.trim() : '';
    const projectId = els.projectSelect ? els.projectSelect.value : '';
    const sourceBranch = els.branchSelect ? els.branchSelect.value : '';
    const providerId = els.providerSelect ? els.providerSelect.value : '';
    if (!projectId) return toast('Choose a repository project.', 'error');
    if (goal.length < 10) return toast('Describe the task in a little more detail.', 'error');
    if (els.start) els.start.disabled = true;
    const original = els.start ? els.start.innerHTML : '';
    if (els.start) els.start.innerHTML = '<span class="material-symbols-outlined">progress_activity</span>Queuing…';
    try {
      const data = await api(urls.sessions, { method: 'POST', body: { projectId, sourceBranch, providerId, goal } });
      // Open the dedicated session page (sessions are separate, uncluttered).
      window.location.href = urls.sessionPage + encodeURIComponent(data.session.id);
    } catch (error) {
      toast(error.message, 'error');
    } finally {
      if (els.start) { els.start.disabled = false; els.start.innerHTML = original; }
    }
  }

  async function loadRepositories() {
    setHTML(els.repoResults, '<div class="ba-empty-small">Loading repositories…</div>');
    setHidden(els.repoConfig, true);
    setHidden(els.repoResults, false);
    try {
      const q = els.repoSearch ? els.repoSearch.value.trim() : '';
      const data = await api(`${urls.repositories}?per_page=100&q=${encodeURIComponent(q)}`);
      model.repositoryResults = data.repositories || [];
      renderRepositories();
    } catch (error) {
      setHTML(els.repoResults, `<div class="ba-empty-small">${escapeHtml(error.message)}</div>`);
    }
  }

  function renderRepositories() {
    const repos = model.repositoryResults;
    setHTML(els.repoResults, repos.length ? repos.map(repo => `
      <button class="ba-repo-result" type="button" data-repo-name="${escapeHtml(repo.fullName)}">
        <span class="ba-repo-icon"><span class="material-symbols-outlined">${repo.private ? 'lock' : 'folder_open'}</span></span>
        <span class="ba-repo-result-copy"><strong>${escapeHtml(repo.fullName)}</strong><p>${escapeHtml(repo.description || `Default branch: ${repo.defaultBranch}`)}</p></span>
        <span class="ba-repo-badges"><span class="ba-repo-badge">${repo.private ? 'Private' : 'Public'}</span>${repo.canPush ? '<span class="ba-repo-badge">Write</span>' : '<span class="ba-repo-badge">Read</span>'}</span>
      </button>`).join('') : '<div class="ba-empty-small">No matching repositories were returned by GitHub.</div>');
  }

  async function selectRepository(fullName) {
    const repo = model.repositoryResults.find(item => item.fullName === fullName);
    if (!repo) return;
    model.selectedRepo = repo;
    setHidden(els.repoResults, true);
    setHidden(els.repoConfig, false);
    setText(els.selectedRepoName, repo.fullName);
    setHTML(els.repoBaseBranch, `<option>${escapeHtml(repo.defaultBranch)}</option>`);
    try {
      const data = await api(`${urls.branches}?repo=${encodeURIComponent(repo.fullName)}`);
      setHTML(els.repoBaseBranch, (data.branches || []).map(branch => `<option value="${escapeHtml(branch.name)}" ${branch.name === repo.defaultBranch ? 'selected' : ''}>${escapeHtml(branch.name)}</option>`).join(''));
    } catch (error) { toast(error.message, 'error'); }
  }

  async function saveProject() {
    if (!model.selectedRepo) return;
    if (els.saveProject) els.saveProject.disabled = true;
    try {
      await api(urls.projects, { method: 'POST', body: { repoFullName: model.selectedRepo.fullName, baseBranch: els.repoBaseBranch ? els.repoBaseBranch.value : '' } });
      if (els.dialog) els.dialog.close();
      await loadState();
      toast('Repository added.');
    } catch (error) { toast(error.message, 'error'); }
    finally { if (els.saveProject) els.saveProject.disabled = false; }
  }

  function openRepositoryDialog() {
    model.selectedRepo = null;
    setHidden(els.repoConfig, true);
    setHidden(els.repoResults, false);
    if (els.dialog) els.dialog.showModal();
    loadRepositories();
  }

  // ---- events (each guarded so one missing node never breaks the page) ----
  on(els.addProject, 'click', openRepositoryDialog);
  on(els.disconnect, 'click', async () => {
    if (!confirm('Disconnect GitHub? Running sessions may fail when they next access the repository.')) return;
    try { await api(urls.disconnect, { method: 'POST', body: {} }); window.location.reload(); } catch (error) { toast(error.message, 'error'); }
  });
  on(els.projectList, 'click', event => {
    const button = event.target.closest('[data-project-id]');
    if (button) loadProjectBranches(button.dataset.projectId, false);
  });
  on(els.projectSelect, 'change', () => loadProjectBranches(els.projectSelect.value, false));
  on(els.start, 'click', startSession);
  on(els.goal, 'keydown', event => { if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') startSession(); });
  if (els.dialog) els.dialog.querySelectorAll('[data-close-dialog]').forEach(button => button.addEventListener('click', () => els.dialog.close()));
  on(els.repoRefresh, 'click', loadRepositories);
  let searchTimer;
  on(els.repoSearch, 'input', () => { clearTimeout(searchTimer); searchTimer = setTimeout(loadRepositories, 350); });
  on(els.repoResults, 'click', event => { const button = event.target.closest('[data-repo-name]'); if (button) selectRepository(button.dataset.repoName); });
  on(els.repoBack, 'click', () => { model.selectedRepo = null; setHidden(els.repoConfig, true); setHidden(els.repoResults, false); });
  on(els.saveProject, 'click', saveProject);

  // ---- boot ----
  loadState();
  model.pollTimer = setInterval(() => { if (!document.hidden) loadState(); }, 15000);
})();
