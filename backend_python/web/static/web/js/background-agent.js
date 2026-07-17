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
    sessionPage: app.dataset.sessionPageBase, // base like ".../session/"
  };

  const $ = (id) => document.getElementById(id);
  const els = {
    workerStatus: $('ba-worker-status'),
    accountInline: $('ba-account-inline'),
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
    els.workerStatus.classList.toggle('online', !!online);
    els.workerStatus.classList.toggle('offline', !online);
    els.workerStatus.querySelector('.material-symbols-outlined').textContent = online ? 'cloud_done' : 'cloud_off';
    els.workerStatus.querySelector('.ba-worker-label').textContent = online ? `${online} worker${online === 1 ? '' : 's'} online` : 'Worker offline';

    const connected = !!model.github.connected;
    els.connectEmpty.hidden = connected;
    els.workspace.hidden = !connected;
    els.disconnect.hidden = !connected;
    els.accountInline.hidden = !connected;
    if (connected) {
      const avatar = model.github.avatarUrl
        ? `<img src="${escapeHtml(model.github.avatarUrl)}" alt="">`
        : `<span class="ba-ai"><span class="material-symbols-outlined">person</span></span>`;
      els.accountInline.innerHTML = `${avatar}<span>@${escapeHtml(model.github.login || 'github')}</span>`;
      els.account.innerHTML = `${avatar}<div><strong>@${escapeHtml(model.github.login || 'github')}</strong><span>Repository access connected</span></div>`;
    }
    if (!connected) return;

    els.projectList.innerHTML = model.projects.length ? model.projects.map(project => `
      <button class="ba-project-item ${project.id === model.selectedProjectId ? 'active' : ''}" type="button" data-project-id="${escapeHtml(project.id)}">
        <span class="ba-repo-icon"><span class="material-symbols-outlined">${project.private ? 'lock' : 'folder_open'}</span></span>
        <span class="ba-project-copy"><strong>${escapeHtml(project.repoFullName)}</strong><span>${escapeHtml(project.preferredBaseBranch || project.defaultBranch)} · ${escapeHtml(project.status)}</span></span>
      </button>`).join('') : '<div class="ba-empty-small">Add a repository to create a codebase.</div>';

    els.sessionCount.textContent = String(model.sessions.length);
    els.sessionList.innerHTML = model.sessions.length ? model.sessions.map(session => `
      <a class="ba-session-item" href="${escapeHtml(urls.sessionPage + encodeURIComponent(session.id))}">
        <span class="ba-mini-status ${escapeHtml(session.status)}"></span>
        <span class="ba-session-copy"><strong>${escapeHtml(session.title || session.goal)}</strong><span>${escapeHtml(session.repoFullName)} · ${statusLabel(session.status)}</span></span>
        <span class="ba-session-time">${escapeHtml(formatTime(session.updatedAt || session.createdAt))}</span>
        <span class="ba-session-open"><span class="material-symbols-outlined">chevron_right</span></span>
      </a>`).join('') : '<div class="ba-empty-small">No tasks yet — describe one above and start it.</div>';

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
      const selected = currentBranch && cached.some(b => b.name === currentBranch) ? currentBranch : (project.preferredBaseBranch || project.defaultBranch);
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
      const data = await api(urls.sessions, { method: 'POST', body: { projectId, sourceBranch, providerId, goal } });
      // Open the dedicated session page (sessions are separate, uncluttered).
      window.location.href = urls.sessionPage + encodeURIComponent(data.session.id);
    } catch (error) {
      toast(error.message, 'error');
    } finally {
      els.start.disabled = false;
      els.start.innerHTML = original;
    }
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
      els.dialog.close();
      await loadState();
      toast('Repository added.');
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

  // ---- events ----
  els.addProject.addEventListener('click', openRepositoryDialog);
  els.disconnect.addEventListener('click', async () => {
    if (!confirm('Disconnect GitHub? Running sessions may fail when they next access the repository.')) return;
    try { await api(urls.disconnect, { method: 'POST', body: {} }); window.location.reload(); } catch (error) { toast(error.message, 'error'); }
  });
  els.projectList.addEventListener('click', event => {
    const button = event.target.closest('[data-project-id]');
    if (button) loadProjectBranches(button.dataset.projectId, false);
  });
  els.projectSelect.addEventListener('change', () => loadProjectBranches(els.projectSelect.value, false));
  els.start.addEventListener('click', startSession);
  els.goal.addEventListener('keydown', event => { if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') startSession(); });
  els.dialog.querySelectorAll('[data-close-dialog]').forEach(button => button.addEventListener('click', () => els.dialog.close()));
  els.repoRefresh.addEventListener('click', loadRepositories);
  let searchTimer;
  els.repoSearch.addEventListener('input', () => { clearTimeout(searchTimer); searchTimer = setTimeout(loadRepositories, 350); });
  els.repoResults.addEventListener('click', event => { const button = event.target.closest('[data-repo-name]'); if (button) selectRepository(button.dataset.repoName); });
  els.repoBack.addEventListener('click', () => { model.selectedRepo = null; els.repoConfig.hidden = true; els.repoResults.hidden = false; });
  els.saveProject.addEventListener('click', saveProject);

  // ---- boot ----
  loadState();
  model.pollTimer = setInterval(() => { if (!document.hidden) loadState(); }, 15000);
})();
