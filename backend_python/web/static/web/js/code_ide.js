(function () {
  'use strict';
  var UI = window.CodeUI;
  var Panels = window.CodePanels;
  var BOOT = window.CODE_BOOT || {};
  var API = new window.NebyCodeAPI(BOOT);
  var $ = function (id) { return document.getElementById(id); };
  var els = {
    app: $('ncApp'), rail: $('ncRail'), railScrim: $('ncRailScrim'), panel: $('ncPanel'), panelScrim: $('ncPanelScrim'),
    transcript: $('ncTranscript'), input: $('ncInput'), send: $('ncSendBtn'), stop: $('ncStopBtn'),
    modelChip: $('ncModelChip'), modelLabel: $('ncModelChipLabel'), modeChip: $('ncAgentChip'), modeLabel: $('ncAgentLabel'),
    workspaceMount: $('ncWorkspaceMount'), crumbRoot: $('ncCrumbRoot'), crumbName: $('ncCrumbName'),
    daemonDot: $('ncDaemonDot'), daemonLabel: $('ncDaemonLabel'), machineCopy: $('ncMachineCardCopy'),
    branch: $('ncBranchLabel'), project: $('ncProjectLabel'), projectChip: $('ncProjectChip'), cwd: $('ncCwd'), ringMount: $('ncRingMount'),
    composer: $('ncComposerOuter'), composerOuter: $('ncComposerOuter'), diff: $('ncDiffView'), attach: $('ncAttachBtn'), mic: $('ncMicBtn'),
  };
  var modelCatalog = BOOT.models || {};
  var modelGroups = Array.isArray(modelCatalog.groups) ? modelCatalog.groups : [];
  var allModels = [];
  modelGroups.forEach(function (group) {
    (group.models || []).forEach(function (model) { allModels.push(model); });
  });
  var state = {
    sessions: Array.isArray(BOOT.sessions) ? BOOT.sessions : [],
    sessionId: '',
    session: null,
    filter: '',
    running: false,
    daemonOnline: !!BOOT.daemonOnline,
    daemonInfo: BOOT.daemonInfo || {},
    model: chooseDefaultModel(),
    effort: 'balanced',
    mode: 'agent',
    workspaceFilter: '',
    goal: '',
    currentPanel: 'changes',
    changes: [],
    activeDiff: '',
    activeTermCalls: {},
  };
  var ring = UI.ProgressRing({ size: 26 });
  els.ringMount.appendChild(ring.el);
  ring.set(0);
  var tree = Panels.Tree({ api: API, onOpenFile: openFile, onError: notifyError });
  var editor = Panels.Editor({ onSave: function (path, content) { return API.fsWrite(path, content); }, onError: notifyError, onSaved: function () { refreshChanges(true); } });
  var terminal = Panels.Terminal({ onRun: runTerminal });
  var changesList = Panels.ChangesList({ getActive: function () { return state.activeDiff; }, onOpen: openDiff });
  var chat = new window.NebyCodeChat({
    transcript: els.transcript,
    onPrompt: function (prompt) {
      els.input.value = prompt;
      autosize();
      sendMessage();
    },
  });
  $('ncTreeMount').appendChild(tree.el);
  $('ncEditorMount').appendChild(editor.el);
  $('ncTermMount').appendChild(terminal.el);
  $('ncChangesMount').appendChild(changesList.el);
  function chooseDefaultModel() {
    var wanted = modelCatalog.default || {};
    var match = allModels.find(function (model) {
      return model.provider === wanted.provider && model.model === wanted.model && (model.provider_id || '') === (wanted.provider_id || '');
    });
    return match || allModels.find(function (model) { return model.available; }) || allModels[0] || {
      provider: 'tryingopen', provider_id: '', model: 'qwen/qwen3.8-27b', label: 'Qwen 3.8 27B', available: true, context_window: 262144,
    };
  }
  function currentSelection() {
    return {
      provider: state.model.provider || '',
      provider_id: state.model.provider_id || '',
      model: state.model.model || '',
      effort: state.effort,
      mode: state.mode,
    };
  }
  var workspaceTree = null;

  function formatWorkspaceLabel(raw) {
    if (!raw || raw === 'Default Workspace') {
      var d = state.daemonInfo && (state.daemonInfo.workspace_label || state.daemonInfo.cwd);
      if (d) {
        var cleanD = String(d).trim().replace(/[\\/]+$/, '');
        var p = cleanD.split(/[\\/]/);
        return p[p.length - 1] || cleanD;
      }
      return 'NEB Workspace';
    }
    var clean = String(raw).trim().replace(/[\\/]+$/, '');
    var parts = clean.split(/[\\/]/);
    return parts[parts.length - 1] || clean;
  }

  function buildWorkspacesData() {
    var map = {};
    var defaultRaw = (state.daemonInfo && (state.daemonInfo.workspace_label || state.daemonInfo.cwd)) || 'Default Workspace';
    var defaultLabel = formatWorkspaceLabel(defaultRaw);

    // Ensure default daemon workspace is present
    map[defaultLabel] = {
      id: 'ws-' + encodeURIComponent(defaultLabel),
      label: defaultLabel,
      rawPath: defaultRaw,
      sessions: [],
    };

    state.sessions.forEach(function (session) {
      var wsLabel = formatWorkspaceLabel((session.workspace_label || '').trim() || defaultRaw);
      if (!map[wsLabel]) {
        map[wsLabel] = {
          id: 'ws-' + encodeURIComponent(wsLabel),
          label: wsLabel,
          rawPath: session.workspace_label || defaultRaw,
          sessions: [],
        };
      }
      map[wsLabel].sessions.push(session);
    });

    return Object.values(map);
  }

  function initWorkspaceTree() {
    var mount = $('ncWorkspaceMount');
    if (!mount || !window.NebyWorkspaceTree) return;
    var wsData = buildWorkspacesData();
    var defaultWsId = wsData.length ? wsData[0].id : '';
    var activeWsId = state.session ? ('ws-' + encodeURIComponent(state.session.workspace_label || '')) : defaultWsId;

    workspaceTree = new window.NebyWorkspaceTree({
      mount: mount,
      workspaces: wsData,
      activeWorkspaceId: activeWsId,
      activeSessionId: state.sessionId,
      filter: state.filter,
      onSelectSession: function (sessionId, wsId, session) {
        selectSession(sessionId);
        closeRail();
      },
      onSelectWorkspace: function (wsId, workspace) {
        // Active workspace selected
      },
      onCreateSession: function (wsId, workspace) {
        var wsLabel = workspace ? workspace.label : '';
        createSession('New session', wsLabel).then(function () {
          els.input.focus();
          closeRail();
        }).catch(notifyError);
      },
      onDeleteSession: function (sessionId, wsId, session) {
        if (!window.confirm('Delete "' + (session.name || 'this session') + '"?')) return;
        API.deleteSession(sessionId).then(function () {
          if (window.WS) window.WS.unsubscribe('code.ui.' + sessionId);
          state.sessions = state.sessions.filter(function (item) { return item.id !== sessionId; });
          if (state.sessionId === sessionId) {
            state.sessionId = '';
            state.session = null;
            history.replaceState(null, '', location.pathname);
            chat.renderHero();
            setCrumb();
          }
          renderSessions();
          UI.toast('Session deleted');
        }).catch(notifyError);
      },
    });
  }

  function renderSessions() {
    if (!workspaceTree) {
      initWorkspaceTree();
      return;
    }
    var wsData = buildWorkspacesData();
    var defaultWsId = wsData.length ? wsData[0].id : '';
    var activeWsId = state.session ? ('ws-' + encodeURIComponent(state.session.workspace_label || '')) : defaultWsId;
    workspaceTree.setData({
      workspaces: wsData,
      activeWorkspaceId: activeWsId,
      activeSessionId: state.sessionId,
      filter: state.filter,
    });
  }

  function syncSessionConfig(session) {
    if (!session) return;
    state.effort = session.effort || 'balanced';
    state.mode = session.mode || 'agent';
    var match = allModels.find(function (model) {
      return model.provider === session.provider && model.model === session.model && (model.provider_id || '') === (session.provider_id || '');
    });
    if (match) state.model = match;
    updateModelChip();
    updateModeChip();
  }

  function setCrumb() {
    var info = state.daemonInfo || {};
    els.crumbRoot.textContent = info.workspace_label || state.session && state.session.workspace_label || 'local workspace';
    els.crumbName.textContent = state.session ? state.session.name || 'New session' : 'New session';
  }

  function selectSession(id) {
    if (!id || id === state.sessionId && state.session) return Promise.resolve();
    var previous = state.sessionId;
    state.sessionId = id;
    state.session = state.sessions.find(function (item) { return item.id === id; }) || null;
    if (previous && window.WS) window.WS.unsubscribe('code.ui.' + previous);
    if (window.WS) window.WS.subscribe('code.ui.' + id);
    syncSessionConfig(state.session);
    setCrumb();
    renderSessions();
    chat.resetLive();
    return API.session(id).then(function (data) {
      state.session = data.session;
      replaceSession(data.session);
      syncSessionConfig(data.session);
      setCrumb();
      setRunning(data.session.status === 'queued' || data.session.status === 'running');
      chat.renderTranscript(data.messages || []);
      history.replaceState(null, '', location.pathname + '?session=' + encodeURIComponent(id));
    }).catch(function (error) {
      notifyError(error);
      chat.renderHero();
    });
  }

  function replaceSession(session) {
    if (!session) return;
    var index = state.sessions.findIndex(function (item) { return item.id === session.id; });
    if (index >= 0) state.sessions[index] = session;
    else state.sessions.unshift(session);
    state.sessions.sort(function (a, b) { return Number(b.updated_at || 0) - Number(a.updated_at || 0); });
    renderSessions();
  }

  function createSession(name, workspaceLabel) {
    var values = currentSelection();
    values.name = String(name || 'New session').slice(0, 120);
    if (workspaceLabel) {
      values.workspace_label = workspaceLabel;
    } else if (state.daemonInfo && (state.daemonInfo.workspace_label || state.daemonInfo.cwd)) {
      values.workspace_label = state.daemonInfo.workspace_label || state.daemonInfo.cwd;
    }
    return API.createSession(values).then(function (data) {
      replaceSession(data.session);
      return selectSession(data.session.id).then(function () { return data.session; });
    });
  }
  function loadSessions(silent) {
    return API.sessions().then(function (data) {
      state.sessions = data.sessions || [];
      setDaemon(data.daemon_online, data.daemon_info || {});
      renderSessions();
    }).catch(function (error) { if (!silent) notifyError(error); });
  }
  function sendMessage() {
    var content = els.input.value.trim();
    if (!content || state.running) return;
    if (!state.daemonOnline) {
      openConnect();
      UI.toast('Connect your local machine before running an agent.');
      return;
    }
    var before = content;
    if (state.goal) before = 'Goal: ' + state.goal + '\n\n' + before;
    var ready = state.sessionId ? Promise.resolve(state.session) : createSession(content.replace(/\s+/g, ' ').slice(0, 58));
    ready.then(function () {
      if (state.session && /^New session$/i.test(state.session.name || '')) {
        var name = before.replace(/\s+/g, ' ').slice(0, 58);
        API.updateSession(state.sessionId, { name: name }).then(function (data) { state.session = data.session; replaceSession(data.session); setCrumb(); }).catch(function () {});
      }
      els.input.value = '';
      autosize();
      if (!els.transcript.querySelector('.nc-thread')) els.transcript.innerHTML = '';
      chat.addUser(before);
      chat.ensureLive();
      setRunning(true);
      chat.setStatus({ phase: 'starting' });
      return API.send(state.sessionId, Object.assign({ content: before }, currentSelection()));
    }).then(function (data) {
      if (data && data.session) { state.session = data.session; replaceSession(data.session); }
    }).catch(function (error) {
      setRunning(false);
      chat.removeLive();
      chat.addError(error.message || 'Unable to start the agent.');
      if (error.code === 'daemon_offline') openConnect();
    });
  }
  function setRunning(on) {
    state.running = !!on;
    if (els.send) {
      els.send.classList.toggle('running', !!on);
      var ic = els.send.querySelector('.material-symbols-outlined');
      if (ic) ic.textContent = on ? 'stop' : 'arrow_upward';
      els.send.setAttribute('aria-label', on ? 'Stop agent' : 'Send message');
      els.send.setAttribute('title', on ? 'Stop agent' : 'Send');
    }
    if (els.composerOuter) els.composerOuter.classList.toggle('loading', !!on);
  }
  function cancelAgent() {
    if (!state.sessionId || !state.running) return;
    chat.setStatus({ phase: 'cancelling' });
    API.cancel(state.sessionId).catch(notifyError);
  }
  function refreshTree(silent) {
    if (!state.daemonOnline) return Promise.resolve();
    return tree.refresh().then(function () {
      els.cwd.textContent = state.daemonInfo.cwd || state.daemonInfo.workspace_label || 'Local workspace';
    }).catch(function (error) { if (!silent) notifyError(error); });
  }
  function refreshChanges(silent) {
    if (!state.daemonOnline) {
      state.changes = [];
      changesList.render([]);
      return Promise.resolve();
    }
    return API.git('status').then(function (data) {
      state.changes = data.changes || [];
      changesList.render(state.changes);
      if (data.branch) els.branch.textContent = data.branch;
      return data;
    }).catch(function (error) { if (!silent) notifyError(error); });
  }
  function openFile(path) {
    showPanel('files');
    return API.fsRead(path).then(function (data) { editor.open(path, data.content || ''); }).catch(notifyError);
  }
  function openDiff(path) {
    state.activeDiff = path;
    changesList.render(state.changes);
    els.diff.innerHTML = '<div class="nc-panel-empty"><span class="ncu-spin"></span><strong>Loading diff</strong></div>';
    API.git('diff', { path: path, context: 4 }).then(function (data) {
      var patch = String(data.patch || '');
      if (!patch) {
        els.diff.innerHTML = '<div class="nc-panel-empty"><span class="material-symbols-outlined">check</span><strong>No textual diff</strong><span>The path may be binary, staged differently, or already clean.</span></div>';
        return;
      }
      var lines = patch.split('\n').map(function (line) {
        var cls = line.indexOf('+++') === 0 || line.indexOf('---') === 0 ? '' : line.indexOf('+') === 0 ? ' add' : line.indexOf('-') === 0 ? ' del' : line.indexOf('@@') === 0 ? ' hunk' : '';
        return '<span class="nc-diff-line' + cls + '">' + UI.esc(line || ' ') + '</span>';
      }).join('');
      els.diff.innerHTML = '<div class="nc-diff-head"><span class="material-symbols-outlined" style="font-size:15px">difference</span><span class="nc-diff-path">' + UI.esc(path) + '</span><button type="button" class="ncu-iconbtn sm" data-open-file title="Open file"><span class="material-symbols-outlined">open_in_new</span></button></div><pre class="nc-diff-pre">' + lines + '</pre>';
      var open = els.diff.querySelector('[data-open-file]');
      if (open) open.addEventListener('click', function () { openFile(path); });
    }).catch(function (error) { els.diff.innerHTML = '<div class="nc-panel-empty"><span class="material-symbols-outlined">error</span><strong>Diff unavailable</strong><span>' + UI.esc(error.message || 'Unable to read Git diff') + '</span></div>'; });
  }
  function runTerminal(command) {
    if (!state.daemonOnline) { openConnect(); return; }
    var ready = state.sessionId ? Promise.resolve() : createSession('Terminal session');
    ready.then(function () { return API.term(state.sessionId, command, 1800); }).then(function (data) {
      var result = data.data || {};
      if (result.call_id) state.activeTermCalls[result.call_id] = true;
      if (result.stdout_tail) terminal.appendChunk(result.stdout_tail, 'out');
      if (result.stderr_tail) terminal.appendChunk(result.stderr_tail, 'err');
      if (result.exit_code != null) terminal.finish(result.exit_code, result.duration_ms);
    }).catch(function (error) { terminal.appendChunk(error.message || String(error), 'err'); });
  }
  function setDaemon(online, info) {
    var wasOffline = !state.daemonOnline;
    state.daemonOnline = !!online;
    if (info) state.daemonInfo = info;
    els.daemonDot.classList.toggle('online', state.daemonOnline);
    els.daemonLabel.textContent = state.daemonOnline ? 'Local machine connected' : 'Local machine offline';
    els.machineCopy.textContent = state.daemonOnline ? (state.daemonInfo.workspace_label || state.daemonInfo.cwd || 'Workspace connected') : 'Connect to code on this machine';
    els.project.textContent = state.daemonOnline ? (state.daemonInfo.workspace_label || 'workspace') : 'No workspace';
    els.branch.textContent = state.daemonOnline ? (state.daemonInfo.git_branch || '—') : '—';
    els.cwd.textContent = state.daemonOnline ? (state.daemonInfo.cwd || state.daemonInfo.workspace_label || 'Local workspace') : 'Local machine offline';
    setCrumb();
    if (state.daemonOnline) {
      if (connectModal && typeof connectModal.close === 'function') connectModal.close();
      if (wasOffline) {
        UI.toast('Local machine connected: ' + (state.daemonInfo.workspace_label || state.daemonInfo.cwd || 'workspace'));
      }
      refreshTree(true);
      refreshChanges(true);
    }
  }
  function updateModelChip() {
    els.modelLabel.textContent = state.model.label || state.model.model || 'Model';
    els.modelChip.title = (state.model.provider || '') + ' · ' + (state.model.model || '');
  }
  function updateModeChip() {
    var names = { agent: 'Agent', ask: 'Ask', plan: 'Plan' };
    els.modeLabel.textContent = names[state.mode] || 'Agent';
  }
  function saveSessionConfig() {
    if (!state.sessionId) return;
    API.updateSession(state.sessionId, currentSelection()).then(function (data) { state.session = data.session; replaceSession(data.session); }).catch(notifyError);
  }
  function modelKey(model) {
    return (model.provider || '') + '|' + (model.provider_id || '') + '|' + (model.model || '');
  }
  function effortLevelsFor(model) {
    var group = modelGroups.find(function (g) { return g.provider === model.provider; });
    return (group && group.effort_levels) || (model && model.effort_levels) || [];
  }
  var EFFORT_DISPLAY = { quick: 'Low', balanced: 'Medium', deep: 'High', low: 'Low', medium: 'Medium', high: 'High', max: 'Very High' };
  function openModelPicker(trigger) {
    UI.closeAllPopovers();
    var groups = [];
    modelGroups.forEach(function (group) {
      var items = (group.models || []).filter(function (m) { return m.available !== false; })
        .map(function (m) { return { value: modelKey(m), label: m.label || m.model, model: m }; });
      if (items.length) groups.push({ key: group.provider, title: group.title || group.provider, items: items, effort: group.effort_levels || [] });
    });
    function findItem(key) {
      for (var i = 0; i < groups.length; i++) {
        var hit = groups[i].items.find(function (item) { return item.value === key; });
        if (hit) return hit;
      }
      return null;
    }
    function levelsForCurrent() {
      var hit = findItem(modelKey(state.model));
      return hit ? hit.model.effort_levels || [] : [];
    }
    UI.Popover({
      trigger: trigger,
      align: 'right',
      render: function (panel, pop) {
        function renderSlider() {
          var old = panel.querySelector('.ncu-effort-wrap');
          if (old) old.remove();
          var levels = levelsForCurrent();
          if (!levels.length) return;
          var wrap = UI.el('div', 'ncu-effort-wrap');
          var value = levels.indexOf(state.effort) >= 0 ? state.effort : levels[Math.min(1, levels.length - 1)];
          wrap.appendChild(UI.EffortSlider({
            value: value,
            levels: levels,
            names: EFFORT_DISPLAY,
            onChange: function (key) { state.effort = key; saveSessionConfig(); },
          }).el);
          panel.appendChild(wrap);
        }
        var menu = UI.RadioMenu({
          title: 'Models',
          groups: groups.map(function (g) {
            return { key: g.key, title: g.title, items: g.items, open: g.key === 'poolside' };
          }),
          value: modelKey(state.model),
          onChange: function (key) {
            var hit = findItem(key);
            if (hit) {
              state.model = hit.model;
              var levels = effortLevelsFor(state.model);
              if (levels.length && levels.indexOf(state.effort) < 0) state.effort = levels[Math.min(1, levels.length - 1)];
              if (!levels.length) state.effort = 'balanced';
              updateModelChip();
              saveSessionConfig();
              renderSlider();
            }
          },
        });
        panel.appendChild(menu.el);
        var divider = UI.el('div', 'ncu-popover-divider');
        panel.appendChild(divider);
        renderSlider();
      },
    });
  }
  function openModePicker() {
    UI.closeAllPopovers();
    UI.Popover({
      trigger: els.modeChip,
      align: 'right',
      render: function (panel, pop) {
        var modes = [['agent', 'Agent'], ['ask', 'Ask'], ['plan', 'Plan']];
        var menu = UI.RadioMenu({
          title: 'Agent mode',
          items: modes.map(function (entry) { return { value: entry[0], label: entry[1] }; }),
          value: state.mode,
          onChange: function (mode) {
            state.mode = mode;
            updateModeChip();
            saveSessionConfig();
            setTimeout(function () { pop.destroy(); }, 120);
          },
        });
        panel.appendChild(menu.el);
      },
    });
  }
  function openProjectPicker() {
    UI.closeAllPopovers();
    var seen = {};
    var items = [];
    var current = state.daemonInfo.workspace_label || state.daemonInfo.cwd || '';
    if (current && !seen[current]) {
      seen[current] = true;
      items.push({ value: current, parent: '', name: current });
    }
    state.sessions.forEach(function (session) {
      var label = session.workspace_label || '';
      if (label && !seen[label]) {
        seen[label] = true;
        var idx = label.replace(/[\\/]+$/, '').lastIndexOf('/');
        var parentPart = idx > 0 ? label.slice(0, idx + 1) : '';
        var namePart = idx > 0 ? label.slice(idx + 1) : label;
        items.push({ value: label, parent: parentPart, name: namePart });
      }
    });
    if (!items.length) { UI.toast('No known folders yet — connect your machine first.'); return; }
    UI.Popover({
      trigger: els.projectChip,
      align: 'left',
      render: function (panel, pop) {
        var menu = UI.FolderMenu({
          title: 'Local Folders',
          items: items,
          value: current,
          onChange: function (label) {
            state.workspaceFilter = label;
            renderSessions();
            updateProjectChip();
            setTimeout(function () { pop.destroy(); }, 120);
          },
          onReselect: function () {
            state.workspaceFilter = '';
            renderSessions();
            updateProjectChip();
            setTimeout(function () { pop.destroy(); }, 120);
          },
        });
        panel.appendChild(menu.el);
      },
    });
  }
  function updateProjectChip() {
    var label = state.workspaceFilter || (state.daemonInfo.workspace_label || 'workspace');
    var idx = label.replace(/[\\/]+$/, '').lastIndexOf('/');
    els.project.textContent = idx > 0 ? label.slice(idx + 1) : label;
  }
  var connectModal = UI.Modal({ title: 'Connect local machine', subtitle: 'Neby Code keeps file and terminal execution on your computer. The cloud agent talks to this authenticated local runtime.' });
  var connectPollTimer = null;
  function openConnect() {
    connectModal.open();
    var body = connectModal.body;
    body.innerHTML = '<div class="nc-connect-status' + (state.daemonOnline ? ' online' : '') + '"><i></i><span>' + (state.daemonOnline ? 'Connected to ' + UI.esc(state.daemonInfo.cwd || state.daemonInfo.workspace_label || 'your workspace') : 'No local runtime is connected yet.') + '</span></div><div class="nc-connect-grid"><div class="nc-connect-step"><b>1</b><div><strong>Install the local dependency once</strong><div class="nc-command-box"><code>python -m pip install websockets&gt;=12</code><button class="ncu-iconbtn" type="button" data-copy-install><span class="material-symbols-outlined">content_copy</span></button></div></div></div><div class="nc-connect-step"><b>2</b><div><strong>Run this from the repository you want to edit</strong><p>The ticket is scoped to your account and expires automatically. Generate a new one whenever you need it.</p><div class="nc-command-box"><code data-command>Generating secure command…</code><button class="ncu-iconbtn" type="button" data-copy-command disabled><span class="material-symbols-outlined">content_copy</span></button></div></div></div></div>';
    var copyInstall = body.querySelector('[data-copy-install]');
    copyInstall.addEventListener('click', function () { copyText('python -m pip install websockets>=12', 'Install command copied'); });
    API.connection().then(function (data) {
      var command = data.command || '';
      body.querySelector('[data-command]').textContent = command || 'WebSocket endpoint is unavailable on the server.';
      var copy = body.querySelector('[data-copy-command]');
      copy.disabled = !command;
      copy.addEventListener('click', function () { copyText(command, 'Connection command copied'); });
    }).catch(function (error) { body.querySelector('[data-command]').textContent = error.message || 'Unable to generate connection command.'; });
    if (connectPollTimer) clearInterval(connectPollTimer);
    connectPollTimer = setInterval(function () {
      if (connectModal.el && connectModal.el.hidden) {
        clearInterval(connectPollTimer);
        connectPollTimer = null;
        return;
      }
      API.status().then(function (data) {
        if (data && data.daemon_online) {
          clearInterval(connectPollTimer);
          connectPollTimer = null;
          setDaemon(true, data.info || {});
        }
      }).catch(function () {});
    }, 2000);
  }
  function setGoal() {
    var goal = window.prompt('Set a goal for faster results:', state.goal || '');
    if (goal === null) return;
    goal = goal.trim();
    if (!goal) { state.goal = ''; UI.toast('Goal cleared'); return; }
    state.goal = goal;
    UI.toast('Goal set — Neby will optimize for it');
  }
  function prefill(text) {
    els.input.value = text;
    autosize();
    els.input.focus();
    var n = els.input.value.length;
    els.input.setSelectionRange(n, n);
  }
  function openAttachMenu() {
    UI.closeAllPopovers();
    UI.Popover({
      trigger: els.attach,
      below: false,
      render: function (panel, pop) {
        panel.appendChild(UI.ActionMenu({
          pop: pop,
          sections: [
            { title: 'Add', items: [
              { icon: 'attach_file', label: 'Files and folders', desc: 'Browse the workspace', onClick: function () { showPanel('files'); refreshTree(); } },
              { icon: 'my_location', label: 'Goal', desc: 'Set a goal for faster results', onClick: setGoal },
              { icon: 'checklist', label: 'Plan mode', desc: 'Manage complex tasks', onClick: function () { state.mode = 'plan'; updateModeChip(); saveSessionConfig(); UI.toast('Plan mode on — Neby will research before acting'); } },
            ] },
            { title: 'Plugins', items: [
              { icon: 'description', label: 'Documents', desc: 'Create and edit documents', onClick: function () { prefill('Create a well-structured document at '); } },
              { icon: 'table_chart', label: 'Spreadsheets', desc: 'Generate spreadsheets', onClick: function () { prefill('Generate a spreadsheet (CSV) for '); } },
              { icon: 'co_present', label: 'Presentations', desc: 'Create marketing assets', onClick: function () { prefill('Create a presentation (HTML slides) for '); } },
              { icon: 'code_blocks', label: 'Code blocks', desc: 'Write and edit existing code', onClick: function () { showPanel('files'); refreshTree(); } },
            ] },
          ],
        }).el);
      },
    });
  }
  function createFile() {
    if (!state.daemonOnline) { openConnect(); return; }
    var path = window.prompt('New file path relative to the workspace:');
    if (!path) return;
    API.fsWrite(path, '').then(function () { refreshTree(true); openFile(path); refreshChanges(true); }).catch(notifyError);
  }
  function createFolder() {
    if (!state.daemonOnline) { openConnect(); return; }
    var path = window.prompt('New folder path relative to the workspace:');
    if (!path) return;
    API.fsMkdir(path).then(function () { refreshTree(true); refreshChanges(true); }).catch(notifyError);
  }
  function showPanel(name) {
    state.currentPanel = name;
    document.querySelectorAll('.nc-ptab').forEach(function (tab) { tab.classList.toggle('active', tab.getAttribute('data-tab') === name); });
    document.querySelectorAll('.nc-panel-page').forEach(function (page) { page.hidden = page.getAttribute('data-page') !== name; });
    els.app.classList.remove('panel-hidden');
    if (window.innerWidth <= 1180) els.panel.classList.add('open');
    if (name === 'term') terminal.focus();
  }
  function hidePanel() {
    if (window.innerWidth <= 1180) els.panel.classList.remove('open');
    else els.app.classList.add('panel-hidden');
  }
  function openRail() { els.rail.classList.add('open'); }
  function closeRail() { els.rail.classList.remove('open'); }
  function openSessionMenu() {
    if (!state.sessionId) return;
    UI.closeAllPopovers();
    UI.Popover({
      trigger: $('ncMoreBtn'), align: 'right', below: true,
      render: function (panel, pop) {
        panel.appendChild(UI.MenuItem({ icon: 'drive_file_rename_outline', label: 'Rename session', onClick: function () {
          pop.destroy();
          var name = window.prompt('Session name:', state.session && state.session.name || '');
          if (!name) return;
          API.updateSession(state.sessionId, { name: name }).then(function (data) { state.session = data.session; replaceSession(data.session); setCrumb(); }).catch(notifyError);
        } }).el);
        panel.appendChild(UI.MenuItem({ icon: 'delete', label: 'Delete session', onClick: function () {
          pop.destroy();
          if (!window.confirm('Delete this coding session?')) return;
          var id = state.sessionId;
          API.deleteSession(id).then(function () {
            if (window.WS) window.WS.unsubscribe('code.ui.' + id);
            state.sessions = state.sessions.filter(function (item) { return item.id !== id; });
            state.sessionId = '';
            state.session = null;
            history.replaceState(null, '', location.pathname);
            renderSessions();
            chat.renderHero();
            setCrumb();
          }).catch(notifyError);
        } }).el);
      },
    });
  }
  function routeEvent(data, channel, event) {
    if (event === 'daemon.status') {
      setDaemon(!!data.online, data.info || {});
      return;
    }
    if (!state.sessionId || channel !== 'code.ui.' + state.sessionId) return;
    if (event === 'status') {
      setRunning(true);
      chat.setStatus(data || {});
    } else if (event === 'context') {
      ring.set(Number(data.percent || 0));
    } else if (event === 'delta') {
      chat.appendDelta(data.text || '');
    } else if (event === 'tool_call') {
      chat.toolCall(data || {});
    } else if (event === 'tool_result') {
      chat.toolResult(data || {});
      if (['write_file', 'edit_file', 'append_file', 'apply_patch', 'make_dirs', 'move_path', 'delete_path'].indexOf(data.tool) >= 0) {
        refreshChanges(true);
        refreshTree(true);
      }
    } else if (event === 'plan') {
      chat.renderPlan(data.todos || []);
    } else if (event === 'term.data') {
      terminal.appendChunk(data.chunk || '', data.stream || 'out');
    } else if (event === 'term.exit') {
      terminal.finish(data.exit_code, data.duration_ms);
      refreshChanges(true);
    } else if (event === 'done') {
      setRunning(false);
      chat.finishLive();
      if (data.error && data.error !== 'Cancelled') chat.addError(data.error);
      API.session(state.sessionId).then(function (result) {
        state.session = result.session;
        replaceSession(result.session);
        chat.renderTranscript(result.messages || []);
        chat.resetLive();
        refreshChanges(true);
        refreshTree(true);
      }).catch(function () { chat.resetLive(); });
    }
  }
  function wireRealtime() {
    if (!window.WS) return;
    window.WS.on('*', routeEvent);
    window.WS.subscribe('user');
    if (state.sessionId) window.WS.subscribe('code.ui.' + state.sessionId);
  }
  function setupVoice() {
    var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      if (els.mic) els.mic.addEventListener('click', function () { UI.toast('Voice input is not supported in this browser.'); });
      return;
    }
    var recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    var listening = false;
    recognition.addEventListener('result', function (event) {
      var text = event.results && event.results[0] && event.results[0][0] && event.results[0][0].transcript;
      if (text) { els.input.value = (els.input.value ? els.input.value + ' ' : '') + text; autosize(); }
    });
    recognition.addEventListener('end', function () {
      listening = false;
      if (els.mic) els.mic.style.color = '';
    });
    recognition.addEventListener('error', function () {
      listening = false;
      if (els.mic) els.mic.style.color = '';
      UI.toast('Voice input error.');
    });
    if (els.mic) {
      els.mic.addEventListener('click', function () {
        if (listening) {
          try { recognition.stop(); } catch (e) {}
          listening = false;
          els.mic.style.color = '';
        } else {
          try {
            recognition.start();
            listening = true;
            els.mic.style.color = 'var(--ncu-red)';
            UI.toast('Listening… speak now');
          } catch (error) {
            listening = false;
            els.mic.style.color = '';
          }
        }
      });
    }
  }
  function autosize() {
    els.input.style.height = 'auto';
    els.input.style.height = Math.min(180, els.input.scrollHeight) + 'px';
  }
  function copyText(text, success) {
    if (!text) return;
    navigator.clipboard.writeText(text).then(function () { UI.toast(success || 'Copied'); }).catch(function () { UI.toast('Unable to copy'); });
  }
  function notifyError(error) {
    UI.toast(error && error.message ? error.message : String(error || 'Something went wrong'));
  }
  function bindEvents() {
    var search = UI.SearchBox({ placeholder: 'Search sessions', kbd: '⌘K', onFilter: function (value) { state.filter = value; renderSessions(); } });
    $('ncSearchMount').appendChild(search.el);
    $('ncRailSearchBtn').addEventListener('click', function () { search.input.focus(); });
    document.addEventListener('keydown', function (event) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); openRail(); setTimeout(function () { search.input.focus(); }, 50); }
    });
    $('ncThemeMount').appendChild(UI.ThemeToggle(els.app).el);
    $('ncNewSessionBtn').addEventListener('click', function () { createSession('New session').then(function () { els.input.focus(); closeRail(); }).catch(notifyError); });
    if ($('ncRefreshSessions')) $('ncRefreshSessions').addEventListener('click', function () { loadSessions(false); });
    $('ncOpenWorkspaceBtn').addEventListener('click', function () { showPanel('files'); refreshTree(); closeRail(); });
    $('ncConnectRailBtn').addEventListener('click', function () { closeRail(); openConnect(); });
    $('ncConnectBtn').addEventListener('click', openConnect);
    $('ncMenuBtnMobile').addEventListener('click', openRail);
    els.railScrim.addEventListener('click', closeRail);
    $('ncPanelBtnMobile').addEventListener('click', function () { showPanel(state.currentPanel || 'changes'); });
    $('ncTogglePanelBtn').addEventListener('click', function () {
      if (window.innerWidth <= 1180) els.panel.classList.toggle('open');
      else els.app.classList.toggle('panel-hidden');
    });
    $('ncPanelClose').addEventListener('click', hidePanel);
    els.panelScrim.addEventListener('click', hidePanel);
    document.querySelectorAll('.nc-ptab').forEach(function (tab) { tab.addEventListener('click', function () { showPanel(tab.getAttribute('data-tab')); }); });
    $('ncPanelRefresh').addEventListener('click', function () {
      if (state.currentPanel === 'files') refreshTree();
      else if (state.currentPanel === 'changes') refreshChanges();
    });
    $('ncNewFile').addEventListener('click', createFile);
    $('ncNewFolder').addEventListener('click', createFolder);
    if (els.send) {
      els.send.addEventListener('click', function () {
        if (state.running) cancelAgent();
        else sendMessage();
      });
    }
    els.input.addEventListener('input', autosize);
    els.input.addEventListener('keydown', function (event) { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); if (state.running) cancelAgent(); else sendMessage(); } });
    els.modelChip.addEventListener('click', function () { openModelPicker(els.modelChip); });
    els.modeChip.addEventListener('click', openModePicker);
    els.attach.addEventListener('click', openAttachMenu);
    $('ncMoreBtn').addEventListener('click', openSessionMenu);
    $('ncShareBtn').addEventListener('click', function () { copyText(location.href, 'Session link copied'); });
    setupVoice();
  }
  function init() {
    bindEvents();
    setDaemon(state.daemonOnline, state.daemonInfo);
    updateModelChip();
    updateModeChip();
    renderSessions();
    wireRealtime();
    var requested = new URLSearchParams(location.search).get('session');
    var initial = requested && state.sessions.some(function (item) { return item.id === requested; }) ? requested : (state.sessions[0] && state.sessions[0].id);
    if (initial) selectSession(initial);
    else chat.renderHero();
    loadSessions(true);
    setInterval(function () { API.status().then(function (data) { setDaemon(data.daemon_online, data.info || {}); }).catch(function () { setDaemon(false, {}); }); }, 20000);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
