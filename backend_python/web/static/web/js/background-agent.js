(function () {
  'use strict';
  var BA = window.BA;
  var root = BA.qs('#background-agent-app');
  if (!root) return;

  var state = { github: null, projects: [], sessions: [], model: null, selectedProject: '', repositories: [], selectedRepo: null };
  var els = {
    connect: BA.qs('#ba-connect-panel'), workspace: BA.qs('#ba-connected-workspace'), githubCard: BA.qs('#ba-github-connected'),
    githubLogin: BA.qs('#ba-github-login'), disconnect: BA.qs('#ba-disconnect'), addRepo: BA.qs('#ba-open-repo-dialog'),
    projectList: BA.qs('#ba-project-list'), projectSelect: BA.qs('#ba-project-select'), branchSelect: BA.qs('#ba-branch-select'),
    goal: BA.qs('#ba-goal'), start: BA.qs('#ba-start'), sessionList: BA.qs('#ba-session-list'), sessionCount: BA.qs('#ba-session-count'),
    worker: BA.qs('#ba-worker-state'), dialog: BA.qs('#ba-repo-dialog'), repoSearchView: BA.qs('#ba-repo-search-view'),
    repoSearch: BA.qs('#ba-repo-search'), repoResults: BA.qs('#ba-repo-results'), repoRefresh: BA.qs('#ba-repo-refresh'),
    repoConfig: BA.qs('#ba-repo-config'), repoBack: BA.qs('#ba-repo-back'), selectedRepoName: BA.qs('#ba-selected-repo-name'),
    repoBase: BA.qs('#ba-repo-base-branch'), saveProject: BA.qs('#ba-save-project'), fileInput: BA.qs('#ba-file-input'),
    attachmentList: BA.qs('#ba-attachment-list'), composer: BA.qs('#ba-task-composer'), attach: BA.qs('#ba-attach')
  };
  var attachments = BA.createAttachmentController({ input: els.fileInput, list: els.attachmentList, dropZone: els.composer });

  function sessionUrl(id) { return root.dataset.sessionUrlTemplate.replace('__SESSION__', encodeURIComponent(id)); }
  function statusLabel(value) { return String(value || 'queued').replace(/_/g, ' '); }
  function setBusy(button, busy, label) {
    if (!button) return;
    if (busy) { button.dataset.label = button.innerHTML; button.disabled = true; button.innerHTML = '<span class="ba-spinner"></span>'; }
    else { button.disabled = false; if (button.dataset.label) button.innerHTML = button.dataset.label; if (label) button.textContent = label; }
  }
  function applyGithub(github) {
    var connected = Boolean(github && github.connected);
    els.connect.hidden = connected;
    els.workspace.hidden = !connected;
    els.githubCard.hidden = !connected;
    els.addRepo.disabled = !connected;
    if (connected) els.githubLogin.textContent = github.login || 'GitHub';
  }
  function renderWorker(worker) {
    var healthy = Boolean(worker && worker.healthy);
    els.worker.className = 'ba-worker-state ' + (healthy ? 'online' : 'offline');
    els.worker.lastElementChild.textContent = healthy ? (worker.online + ' worker' + (worker.online === 1 ? '' : 's') + ' online') : 'Worker offline';
  }
  function renderProjects() {
    els.projectList.innerHTML = '';
    els.projectSelect.innerHTML = '<option value="">Select a repository</option>';
    if (!state.projects.length) {
      els.projectList.innerHTML = '<div class="ba-empty-state"><span class="material-symbols-outlined">folder_off</span><p>Add a GitHub repository to begin.</p></div>';
      return;
    }
    state.projects.forEach(function (project) {
      var option = document.createElement('option');
      option.value = project.id; option.textContent = project.repoFullName; els.projectSelect.appendChild(option);
      var button = document.createElement('button');
      button.type = 'button'; button.className = 'ba-project-item' + (state.selectedProject === project.id ? ' active' : '');
      button.innerHTML = '<span class="material-symbols-outlined">folder_open</span><div><strong></strong><small></small></div>';
      button.querySelector('strong').textContent = project.repoFullName;
      button.querySelector('small').textContent = project.preferredBaseBranch || project.defaultBranch;
      button.addEventListener('click', function () { selectProject(project.id); });
      els.projectList.appendChild(button);
    });
    if (!state.selectedProject || !state.projects.some(function (project) { return project.id === state.selectedProject; })) state.selectedProject = state.projects[0].id;
    els.projectSelect.value = state.selectedProject;
    BA.qsa('.ba-project-item', els.projectList).forEach(function (button, index) { button.classList.toggle('active', state.projects[index].id === state.selectedProject); });
  }
  function renderSessions() {
    els.sessionCount.textContent = state.sessions.length;
    els.sessionList.innerHTML = '';
    if (!state.sessions.length) {
      els.sessionList.innerHTML = '<div class="ba-empty-state"><span class="material-symbols-outlined">auto_awesome</span><p>Your delegated tasks will appear here.</p></div>';
      return;
    }
    state.sessions.forEach(function (session) {
      var link = document.createElement('a');
      link.href = sessionUrl(session.id); link.className = 'ba-session-card';
      var title = session.title || session.goal || 'Untitled task';
      link.innerHTML = '<div class="ba-session-card-main"><div class="ba-session-card-title"><span class="ba-status-pill"></span><strong></strong></div><p></p><div class="ba-session-card-meta"><span class="repo"></span><span class="branch"></span><span class="time"></span></div></div><div class="ba-session-card-side"><div class="ba-session-progress"><span></span></div><span class="material-symbols-outlined">chevron_right</span></div>';
      var pill = link.querySelector('.ba-status-pill'); pill.className += ' ' + session.status; pill.textContent = statusLabel(session.status);
      link.querySelector('strong').textContent = title;
      link.querySelector('p').textContent = session.progressLabel || session.summary || session.goal;
      link.querySelector('.repo').textContent = session.repoFullName;
      link.querySelector('.branch').textContent = session.workBranch || session.sourceBranch;
      link.querySelector('.time').textContent = BA.timeAgo(session.updatedAt || session.createdAt);
      link.querySelector('.ba-session-progress span').style.width = Math.max(2, Number(session.progress || 0)) + '%';
      els.sessionList.appendChild(link);
    });
  }
  async function loadState() {
    try {
      var data = await BA.api(root.dataset.stateUrl);
      state.github = data.github; state.projects = data.projects || []; state.sessions = data.sessions || []; state.model = data.model || {};
      applyGithub(state.github); renderWorker(data.worker); renderProjects(); renderSessions();
      els.start.disabled = !state.model.configured;
      if (!state.model.configured) BA.toast('Enable a Qwen provider configuration before starting tasks.', 'error');
      if (state.selectedProject) await loadBranches(state.selectedProject, false);
    } catch (error) { BA.toast(error.message, 'error'); }
  }
  async function selectProject(projectId) {
    state.selectedProject = projectId;
    els.projectSelect.value = projectId;
    renderProjects();
    await loadBranches(projectId, true);
  }
  async function loadBranches(projectId, preserve) {
    var previousValue = preserve ? els.branchSelect.value : '';
    var project = state.projects.find(function (item) { return item.id === projectId; });
    els.branchSelect.innerHTML = '<option value="">Loading branches…</option>'; els.branchSelect.disabled = true;
    if (!project) { els.branchSelect.innerHTML = '<option value="">Select repository first</option>'; return; }
    try {
      var data = await BA.api(root.dataset.branchesUrl + '?repo=' + encodeURIComponent(project.repoFullName));
      els.branchSelect.innerHTML = '';
      (data.branches || []).forEach(function (branch) { var option = document.createElement('option'); option.value = branch.name; option.textContent = branch.name; els.branchSelect.appendChild(option); });
      var preferred = previousValue || project.preferredBaseBranch || data.defaultBranch || project.defaultBranch;
      if (preferred && Array.from(els.branchSelect.options).some(function (option) { return option.value === preferred; })) els.branchSelect.value = preferred;
    } catch (error) {
      var fallback = project.preferredBaseBranch || project.defaultBranch;
      els.branchSelect.innerHTML = '';
      var fallbackOption = document.createElement('option');
      fallbackOption.value = fallback; fallbackOption.textContent = fallback; els.branchSelect.appendChild(fallbackOption);
      BA.toast(error.message, 'error');
    } finally { els.branchSelect.disabled = false; }
  }
  async function startSession() {
    var goal = els.goal.value.trim();
    if (goal.length < 10) return BA.toast('Describe the task in at least 10 characters.', 'error');
    if (!els.projectSelect.value) return BA.toast('Select a repository.', 'error');
    var form = new FormData();
    form.append('projectId', els.projectSelect.value); form.append('sourceBranch', els.branchSelect.value); form.append('goal', goal);
    attachments.files().forEach(function (file) { form.append('files', file, file.name); });
    setBusy(els.start, true);
    try {
      var data = await BA.api(root.dataset.sessionsUrl, { method: 'POST', body: form });
      window.location.assign(sessionUrl(data.session.id));
    } catch (error) { BA.toast(error.message, 'error'); setBusy(els.start, false); }
  }
  async function loadRepositories() {
    els.repoResults.innerHTML = '<div class="ba-empty-state"><span class="ba-spinner"></span><p>Loading repositories…</p></div>';
    try { var data = await BA.api(root.dataset.repositoriesUrl + '?per_page=100&q=' + encodeURIComponent(els.repoSearch.value.trim())); state.repositories = data.repositories || []; renderRepositories(); }
    catch (error) { els.repoResults.innerHTML = '<div class="ba-empty-state"><p>' + BA.escapeHtml(error.message) + '</p></div>'; }
  }
  function renderRepositories() {
    els.repoResults.innerHTML = '';
    if (!state.repositories.length) { els.repoResults.innerHTML = '<div class="ba-empty-state"><span class="material-symbols-outlined">search_off</span><p>No repositories found.</p></div>'; return; }
    state.repositories.forEach(function (repo) {
      var row = document.createElement('button'); row.type = 'button'; row.className = 'ba-repo-row';
      row.innerHTML = '<span class="material-symbols-outlined">' + (repo.private ? 'lock' : 'public') + '</span><div><strong></strong><small></small></div><span class="material-symbols-outlined">chevron_right</span>';
      row.querySelector('strong').textContent = repo.fullName; row.querySelector('small').textContent = repo.description || repo.defaultBranch;
      row.addEventListener('click', function () { configureRepository(repo); }); els.repoResults.appendChild(row);
    });
  }
  async function configureRepository(repo) {
    state.selectedRepo = repo; els.repoSearchView.hidden = true; els.repoConfig.hidden = false; els.selectedRepoName.textContent = repo.fullName;
    els.repoBase.innerHTML = '<option value="">Loading branches…</option>';
    try { var data = await BA.api(root.dataset.branchesUrl + '?repo=' + encodeURIComponent(repo.fullName)); els.repoBase.innerHTML = ''; (data.branches || []).forEach(function (branch) { var option = document.createElement('option'); option.value = branch.name; option.textContent = branch.name; els.repoBase.appendChild(option); }); els.repoBase.value = data.defaultBranch || repo.defaultBranch; }
    catch (error) { els.repoBase.innerHTML = ''; var fallbackOption = document.createElement('option'); fallbackOption.value = repo.defaultBranch; fallbackOption.textContent = repo.defaultBranch; els.repoBase.appendChild(fallbackOption); BA.toast(error.message, 'error'); }
  }
  async function saveProject() {
    if (!state.selectedRepo) return;
    setBusy(els.saveProject, true);
    try {
      var data = await BA.json(root.dataset.projectsUrl, { repoFullName: state.selectedRepo.fullName, baseBranch: els.repoBase.value });
      state.projects = [data.project].concat(state.projects.filter(function (item) { return item.id !== data.project.id; }));
      state.selectedProject = data.project.id; renderProjects(); await loadBranches(data.project.id, false); els.dialog.close(); BA.toast('Repository added.', 'success');
    } catch (error) { BA.toast(error.message, 'error'); } finally { setBusy(els.saveProject, false); }
  }

  els.attach.addEventListener('click', function () { els.fileInput.click(); });
  els.start.addEventListener('click', startSession);
  els.goal.addEventListener('keydown', function (event) { if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') startSession(); });
  els.projectSelect.addEventListener('change', function () { selectProject(els.projectSelect.value); });
  els.addRepo.addEventListener('click', function () { els.repoSearchView.hidden = false; els.repoConfig.hidden = true; els.dialog.showModal(); loadRepositories(); });
  BA.qs('[data-close-dialog]', els.dialog).addEventListener('click', function () { els.dialog.close(); });
  els.repoRefresh.addEventListener('click', loadRepositories);
  var searchTimer; els.repoSearch.addEventListener('input', function () { clearTimeout(searchTimer); searchTimer = setTimeout(loadRepositories, 300); });
  els.repoBack.addEventListener('click', function () { els.repoConfig.hidden = true; els.repoSearchView.hidden = false; });
  els.saveProject.addEventListener('click', saveProject);
  els.disconnect.addEventListener('click', async function () { if (!window.confirm('Disconnect GitHub from the Background Agent?')) return; try { await BA.json(root.dataset.disconnectUrl, {}); state.github = { connected: false }; applyGithub(state.github); state.projects = []; state.sessions = []; renderProjects(); renderSessions(); } catch (error) { BA.toast(error.message, 'error'); } });

  applyGithub({ connected: root.dataset.initialConnected === 'true', login: els.githubLogin.textContent });
  loadState();
})();
