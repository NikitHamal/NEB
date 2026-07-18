(function () {
  'use strict';

  var BA = window.BA;
  var root = BA.qs('#background-agent-app');
  if (!root) return;

  var state = { github: null, projects: [], sessions: [], model: null, selectedProject: '', repositories: [], selectedRepo: null };
  var els = {
    connect: BA.qs('#ba-connect-panel'), workspace: BA.qs('#ba-connected-workspace'), githubCard: BA.qs('#ba-github-connected'),
    githubLogin: BA.qs('#ba-github-login'), disconnect: BA.qs('#ba-disconnect'), addRepo: BA.qs('#ba-open-repo-dialog'),
    projectList: BA.qs('#ba-project-list'), projectPicker: BA.qs('#ba-project-picker'), branchPicker: BA.qs('#ba-branch-picker'),
    goal: BA.qs('#ba-goal'), start: BA.qs('#ba-start'), sessionList: BA.qs('#ba-session-list'), sessionCount: BA.qs('#ba-session-count'),
    worker: BA.qs('#ba-worker-state'), dialog: BA.qs('#ba-repo-dialog'), repoSearchView: BA.qs('#ba-repo-search-view'),
    repoSearch: BA.qs('#ba-repo-search'), repoResults: BA.qs('#ba-repo-results'), repoRefresh: BA.qs('#ba-repo-refresh'), repoCount: BA.qs('#ba-repo-count'),
    repoConfig: BA.qs('#ba-repo-config'), repoBack: BA.qs('#ba-repo-back'), selectedRepoName: BA.qs('#ba-selected-repo-name'),
    selectedRepoDescription: BA.qs('#ba-selected-repo-description'), repoBasePicker: BA.qs('#ba-repo-base-picker'),
    saveProject: BA.qs('#ba-save-project'), cancelProject: BA.qs('#ba-cancel-project'), fileInput: BA.qs('#ba-file-input'),
    attachmentList: BA.qs('#ba-attachment-list'), composer: BA.qs('#ba-task-composer'), attach: BA.qs('#ba-attach')
  };

  var projectPicker = BA.createPicker({
    root: els.projectPicker,
    minWidth: 300,
    onChange: function (value) { if (value && value !== state.selectedProject) selectProject(value); }
  });
  var branchPicker = BA.createPicker({ root: els.branchPicker, minWidth: 320, maxHeight: 410 });
  var repoBasePicker = BA.createPicker({ root: els.repoBasePicker, minWidth: 420, maxHeight: 410 });
  var attachments = BA.createAttachmentController({ input: els.fileInput, list: els.attachmentList, dropZone: els.composer });

  function sessionUrl(id) { return root.dataset.sessionUrlTemplate.replace('__SESSION__', encodeURIComponent(id)); }
  function statusLabel(value) { return String(value || 'queued').replace(/_/g, ' '); }

  function setBusy(button, busy) {
    if (!button) return;
    if (busy) {
      button.dataset.label = button.innerHTML;
      button.disabled = true;
      button.innerHTML = '<span class="ba-spinner"></span>';
    } else {
      button.disabled = false;
      if (button.dataset.label) button.innerHTML = button.dataset.label;
    }
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

  function projectOptions() {
    return state.projects.map(function (project) {
      return {
        value: project.id,
        label: project.repoFullName,
        meta: project.preferredBaseBranch || project.defaultBranch || 'Repository',
        icon: 'folder_open'
      };
    });
  }

  function renderProjects() {
    els.projectList.innerHTML = '';
    if (!state.projects.length) {
      state.selectedProject = '';
      projectPicker.setOptions([], '');
      projectPicker.setPlaceholder('Add a repository first');
      projectPicker.setDisabled(true);
      branchPicker.setOptions([], '');
      branchPicker.setPlaceholder('Select repository first');
      branchPicker.setDisabled(true);
      els.projectList.innerHTML = '<div class="ba-empty-state ba-project-empty"><span class="material-symbols-outlined">folder_off</span><p>Add a GitHub repository to begin.</p></div>';
      return;
    }

    if (!state.selectedProject || !state.projects.some(function (project) { return String(project.id) === String(state.selectedProject); })) {
      state.selectedProject = String(state.projects[0].id);
    }

    projectPicker.setPlaceholder('Select a repository');
    projectPicker.setOptions(projectOptions(), state.selectedProject);

    state.projects.forEach(function (project) {
      var projectId = String(project.id);
      var button = document.createElement('button');
      button.type = 'button';
      button.className = 'ba-project-item' + (String(state.selectedProject) === projectId ? ' active' : '');
      button.innerHTML = '<span class="material-symbols-outlined">folder_open</span><div><strong></strong><small></small></div>';
      button.querySelector('strong').textContent = project.repoFullName;
      button.querySelector('small').textContent = project.preferredBaseBranch || project.defaultBranch || 'Repository';
      button.addEventListener('click', function () { selectProject(projectId); });
      els.projectList.appendChild(button);
    });
  }

  function renderSessions() {
    els.sessionCount.textContent = state.sessions.length;
    els.sessionList.innerHTML = '';
    if (!state.sessions.length) {
      els.sessionList.innerHTML = '<div class="ba-empty-state"><span class="material-symbols-outlined">history</span><p>Your tasks will appear here.</p></div>';
      return;
    }
    state.sessions.forEach(function (session) {
      var link = document.createElement('a');
      link.href = sessionUrl(session.id);
      link.className = 'ba-session-card';
      var title = session.title || session.goal || 'Untitled task';
      link.innerHTML = '<div class="ba-session-card-main"><div class="ba-session-card-title"><span class="ba-status-pill"></span><strong></strong></div><p></p><div class="ba-session-card-meta"><span class="repo"></span><span class="branch"></span><span class="time"></span></div></div><div class="ba-session-card-side"><div class="ba-session-progress"><span></span></div><span class="material-symbols-outlined">chevron_right</span></div>';
      var pill = link.querySelector('.ba-status-pill');
      pill.className += ' ' + session.status;
      pill.textContent = statusLabel(session.status);
      link.querySelector('strong').textContent = title;
      link.querySelector('p').textContent = session.progressLabel || session.summary || session.goal;
      link.querySelector('.repo').textContent = session.repoFullName;
      link.querySelector('.branch').textContent = session.workBranch || session.sourceBranch;
      link.querySelector('.time').textContent = BA.timeAgo(session.updatedAt || session.createdAt);
      link.querySelector('.ba-session-progress span').style.width = Math.max(2, Number(session.progress || 0)) + '%';
      els.sessionList.appendChild(link);
    });
  }

  function branchOptions(branches, defaultBranch) {
    var seen = new Set();
    var names = (branches || []).map(function (branch) { return String(branch.name || branch); }).filter(function (name) {
      if (!name || seen.has(name)) return false;
      seen.add(name);
      return true;
    });
    var priority = ['main', 'master', 'develop', 'development', 'staging'];
    names.sort(function (left, right) {
      if (left === defaultBranch) return -1;
      if (right === defaultBranch) return 1;
      var leftPriority = priority.indexOf(left);
      var rightPriority = priority.indexOf(right);
      if (leftPriority !== rightPriority) {
        if (leftPriority === -1) return 1;
        if (rightPriority === -1) return -1;
        return leftPriority - rightPriority;
      }
      return left.localeCompare(right);
    });
    return names.map(function (name) {
      return {
        value: name,
        label: name,
        badge: name === defaultBranch ? 'Default' : '',
        meta: name === defaultBranch ? 'Repository default branch' : '',
        icon: name === defaultBranch ? 'account_tree' : 'commit'
      };
    });
  }

  async function loadState() {
    try {
      var data = await BA.api(root.dataset.stateUrl);
      state.github = data.github;
      state.projects = data.projects || [];
      state.sessions = data.sessions || [];
      state.model = data.model || {};
      applyGithub(state.github);
      renderWorker(data.worker);
      renderProjects();
      renderSessions();
      els.start.disabled = !state.model.configured;
      if (!state.model.configured) BA.toast('Enable the Qwen provider before starting tasks.', 'error');
      if (state.selectedProject) await loadBranches(state.selectedProject, false);
    } catch (error) {
      BA.toast(error.message, 'error');
    }
  }

  async function selectProject(projectId) {
    state.selectedProject = String(projectId || '');
    projectPicker.setValue(state.selectedProject, false);
    renderProjects();
    await loadBranches(state.selectedProject, true);
  }

  async function loadBranches(projectId, preserve) {
    var previousValue = preserve ? branchPicker.value() : '';
    var project = state.projects.find(function (item) { return String(item.id) === String(projectId); });
    if (!project) {
      branchPicker.setOptions([], '');
      branchPicker.setPlaceholder('Select repository first');
      branchPicker.setDisabled(true);
      return;
    }

    branchPicker.setPlaceholder('Select a branch');
    branchPicker.setLoading('Loading branches…');
    try {
      var data = await BA.api(root.dataset.branchesUrl + '?repo=' + encodeURIComponent(project.repoFullName));
      var defaultBranch = data.defaultBranch || project.defaultBranch || project.preferredBaseBranch;
      var options = branchOptions(data.branches || [], defaultBranch);
      var preferred = previousValue || project.preferredBaseBranch || defaultBranch;
      branchPicker.setOptions(options, preferred);
    } catch (error) {
      var fallback = project.preferredBaseBranch || project.defaultBranch;
      branchPicker.setOptions(branchOptions([fallback], fallback), fallback);
      BA.toast(error.message, 'error');
    }
  }

  async function startSession() {
    var goal = els.goal.value.trim();
    var projectId = projectPicker.value();
    var sourceBranch = branchPicker.value();
    if (goal.length < 10) return BA.toast('Describe the task in at least 10 characters.', 'error');
    if (!projectId) return BA.toast('Select a repository.', 'error');
    if (!sourceBranch) return BA.toast('Select a base branch.', 'error');

    var form = new FormData();
    form.append('projectId', projectId);
    form.append('sourceBranch', sourceBranch);
    form.append('goal', goal);
    attachments.files().forEach(function (file) { form.append('files', file, file.name); });
    setBusy(els.start, true);
    try {
      var data = await BA.api(root.dataset.sessionsUrl, { method: 'POST', body: form });
      window.location.assign(sessionUrl(data.session.id));
    } catch (error) {
      BA.toast(error.message, 'error');
      setBusy(els.start, false);
    }
  }

  function setRepositoryLoading(loading) {
    els.repoRefresh.disabled = loading;
    els.repoRefresh.classList.toggle('loading', loading);
  }

  async function loadRepositories() {
    setRepositoryLoading(true);
    els.repoResults.innerHTML = '<div class="ba-empty-state"><span class="ba-spinner"></span><p>Loading repositories…</p></div>';
    try {
      var data = await BA.api(root.dataset.repositoriesUrl + '?per_page=100&q=' + encodeURIComponent(els.repoSearch.value.trim()));
      state.repositories = data.repositories || [];
      renderRepositories();
    } catch (error) {
      els.repoCount.textContent = 'Unavailable';
      els.repoResults.innerHTML = '<div class="ba-empty-state"><span class="material-symbols-outlined">cloud_off</span><p>' + BA.escapeHtml(error.message) + '</p></div>';
    } finally {
      setRepositoryLoading(false);
    }
  }

  function renderRepositories() {
    els.repoResults.innerHTML = '';
    els.repoCount.textContent = state.repositories.length + ' repositor' + (state.repositories.length === 1 ? 'y' : 'ies');
    if (!state.repositories.length) {
      els.repoResults.innerHTML = '<div class="ba-empty-state"><span class="material-symbols-outlined">search_off</span><p>No repositories found.</p></div>';
      return;
    }

    state.repositories.forEach(function (repo) {
      var row = document.createElement('button');
      row.type = 'button';
      row.className = 'ba-repo-row';
      row.innerHTML = '<span class="ba-repo-icon"><span class="material-symbols-outlined"></span></span><span class="ba-repo-copy"><span class="ba-repo-title"><strong></strong><em></em></span><small class="ba-repo-description"></small><span class="ba-repo-meta"><span class="material-symbols-outlined">account_tree</span><span></span></span></span><span class="ba-repo-open material-symbols-outlined">arrow_forward</span>';
      row.querySelector('.ba-repo-icon .material-symbols-outlined').textContent = repo.private ? 'lock' : 'public';
      row.querySelector('strong').textContent = repo.fullName;
      row.querySelector('em').textContent = repo.private ? 'Private' : 'Public';
      row.querySelector('.ba-repo-description').textContent = repo.description || 'No repository description';
      row.querySelector('.ba-repo-meta span:last-child').textContent = repo.defaultBranch || 'main';
      row.addEventListener('click', function () { configureRepository(repo); });
      els.repoResults.appendChild(row);
    });
  }

  async function configureRepository(repo) {
    state.selectedRepo = repo;
    els.repoSearchView.hidden = true;
    els.repoConfig.hidden = false;
    els.selectedRepoName.textContent = repo.fullName;
    els.selectedRepoDescription.textContent = repo.description || 'Choose the branch new tasks should start from.';
    repoBasePicker.setLoading('Loading branches…');
    try {
      var data = await BA.api(root.dataset.branchesUrl + '?repo=' + encodeURIComponent(repo.fullName));
      var defaultBranch = data.defaultBranch || repo.defaultBranch;
      repoBasePicker.setOptions(branchOptions(data.branches || [], defaultBranch), defaultBranch);
    } catch (error) {
      repoBasePicker.setOptions(branchOptions([repo.defaultBranch], repo.defaultBranch), repo.defaultBranch);
      BA.toast(error.message, 'error');
    }
  }

  async function saveProject() {
    if (!state.selectedRepo) return;
    var baseBranch = repoBasePicker.value();
    if (!baseBranch) return BA.toast('Select a base branch.', 'error');
    setBusy(els.saveProject, true);
    try {
      var data = await BA.json(root.dataset.projectsUrl, { repoFullName: state.selectedRepo.fullName, baseBranch: baseBranch });
      state.projects = [data.project].concat(state.projects.filter(function (item) { return String(item.id) !== String(data.project.id); }));
      state.selectedProject = String(data.project.id);
      renderProjects();
      await loadBranches(data.project.id, false);
      els.dialog.close();
      BA.toast('Project added.', 'success');
    } catch (error) {
      BA.toast(error.message, 'error');
    } finally {
      setBusy(els.saveProject, false);
    }
  }

  function openRepositoryDialog() {
    state.selectedRepo = null;
    els.repoSearch.value = '';
    els.repoSearchView.hidden = false;
    els.repoConfig.hidden = true;
    els.dialog.showModal();
    requestAnimationFrame(function () { els.repoSearch.focus(); });
    loadRepositories();
  }

  function closeRepositoryDialog() {
    projectPicker.close();
    branchPicker.close();
    repoBasePicker.close();
    els.dialog.close();
  }

  els.attach.addEventListener('click', function () { els.fileInput.click(); });
  els.start.addEventListener('click', startSession);
  els.goal.addEventListener('keydown', function (event) { if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') startSession(); });
  els.addRepo.addEventListener('click', openRepositoryDialog);
  BA.qs('[data-close-dialog]', els.dialog).addEventListener('click', closeRepositoryDialog);
  els.cancelProject.addEventListener('click', closeRepositoryDialog);
  els.repoRefresh.addEventListener('click', loadRepositories);
  var searchTimer;
  els.repoSearch.addEventListener('input', function () {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(loadRepositories, 300);
  });
  els.repoBack.addEventListener('click', function () {
    repoBasePicker.close();
    els.repoConfig.hidden = true;
    els.repoSearchView.hidden = false;
    requestAnimationFrame(function () { els.repoSearch.focus(); });
  });
  els.saveProject.addEventListener('click', saveProject);
  els.dialog.addEventListener('click', function (event) { if (event.target === els.dialog) closeRepositoryDialog(); });
  els.dialog.addEventListener('close', function () { repoBasePicker.close(); });
  els.disconnect.addEventListener('click', async function () {
    if (!window.confirm('Disconnect GitHub from the Background Agent?')) return;
    try {
      await BA.json(root.dataset.disconnectUrl, {});
      state.github = { connected: false };
      state.projects = [];
      state.sessions = [];
      applyGithub(state.github);
      renderProjects();
      renderSessions();
    } catch (error) {
      BA.toast(error.message, 'error');
    }
  });

  applyGithub({ connected: root.dataset.initialConnected === 'true', login: els.githubLogin.textContent });
  loadState();
})();
