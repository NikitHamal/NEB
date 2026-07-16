(function () {
  'use strict';

  if (!window.fetch) return;

  function csrfToken() {
    var m = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return m ? decodeURIComponent(m[1]) : '';
  }

  function csrfHeader() {
    return { 'X-CSRFToken': csrfToken(), 'Content-Type': 'application/json' };
  }

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      for (var k in attrs) {
        if (k === 'class') node.className = attrs[k];
        else if (k === 'html') node.innerHTML = attrs[k];
        else if (k === 'text') node.textContent = attrs[k];
        else if (k.indexOf('on') === 0 && typeof attrs[k] === 'function') {
          node.addEventListener(k.substring(2).toLowerCase(), attrs[k]);
        } else if (attrs[k] != null) node.setAttribute(k, attrs[k]);
      }
    }
    if (children) {
      for (var i = 0; i < children.length; i++) {
        var c = children[i];
        if (c == null) continue;
        node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
      }
    }
    return node;
  }

  function escapeHtml(s) {
    if (s == null) return '';
    return String(s).replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  }

  function showToast(message, kind) {
    var root = document.getElementById('agent_toast_root');
    if (!root) return;
    var stack = root.querySelector('.agent-toast-stack');
    if (!stack) {
      stack = el('div', { class: 'agent-toast-stack' });
      root.appendChild(stack);
    }
    var toast = el('div', { class: 'agent-toast agent-toast-' + (kind || 'info') }, [message]);
    stack.appendChild(toast);
    setTimeout(function () { toast.style.opacity = '0'; setTimeout(function () { toast.remove(); }, 200); }, 5000);
  }

  function askConfirm(title, body, confirmLabel) {
    return new Promise(function (resolve) {
      var root = document.getElementById('agent_modal_root');
      if (!root) return resolve(window.confirm(title + '\n\n' + body));
      var backdrop = el('div', { class: 'agent-modal-backdrop' });
      var wrap = el('div', { class: 'agent-modal', role: 'dialog', 'aria-modal': 'true' }, [
        el('h3', null, [title]),
        el('p', null, [body]),
        el('div', { class: 'agent-modal-actions' }, [
          el('button', { type: 'button', class: 'md-btn md-btn-text', onclick: function () { backdrop.remove(); resolve(false); } }, ['Cancel']),
          el('button', { type: 'button', class: 'md-btn md-btn-filled', onclick: function () { backdrop.remove(); resolve(true); } }, [confirmLabel || 'Confirm']),
        ]),
      ]);
      backdrop.appendChild(wrap);
      root.appendChild(backdrop);
    });
  }

  function apiPost(url, body) {
    return fetch(url, { method: 'POST', credentials: 'same-origin', headers: csrfHeader(), body: JSON.stringify(body || {}) })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); });
  }

  function apiGet(url) {
    return fetch(url, { credentials: 'same-origin', headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); });
  }

  function formatTime(ms) {
    if (!ms) return '';
    var d = new Date(Number(ms));
    if (isNaN(d.getTime())) return String(ms);
    var pad = function (n) { return n < 10 ? '0' + n : '' + n; };
    return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()) + ' ' + pad(d.getHours()) + ':' + pad(d.getMinutes());
  }

  function init() {
    if (document.body.dataset.agentReady === '1') return;
    document.body.dataset.agentReady = '1';

    document.addEventListener('click', handleClick);
    document.addEventListener('submit', handleSubmit);
    document.addEventListener('input', handleInput);
  }

  function handleClick(ev) {
    var t = ev.target.closest('[data-action]');
    if (!t) return;
    var action = t.dataset.action;
    var id = t.dataset.sessionId || t.dataset.projectId;
    ev.preventDefault();
    switch (action) {
      case 'pause-session': controlSession(id, 'pause'); break;
      case 'resume-session': controlSession(id, 'resume'); break;
      case 'stop-session':
        askConfirm('Stop this session', 'The agent will halt after the next tool call. You can still see the diff and download a zip.', 'Stop').then(function (yes) {
          if (yes) controlSession(id, 'stop');
        });
        break;
      case 'refresh-project': refreshProject(id); break;
      case 'push-branch': pushBranch(id); break;
      case 'reload-diff': loadDiff(id); break;
      case 'open-pr':
        askConfirm('Open pull request', 'This will push the session branch to the repo\'s default branch’s upstream and open a PR. Continue?', 'Open PR').then(function (yes) {
          if (yes) openPr(id);
        });
        break;
      case 'archive-project':
        askConfirm('Archive this project', 'It will be hidden from the project list. Sessions remain intact.', 'Archive').then(function (yes) {
          if (yes) deleteProject(id);
        });
        break;
      case 'open-new-session':
        var taskEl = document.getElementById('agent_new_task');
        if (taskEl) taskEl.focus();
        break;
    }
  }

  function handleInput(ev) {
    if (ev.target.id === 'agent_repo_search') {
      loadRepos(ev.target.value.trim());
    }
  }

  function handleSubmit(ev) {
    if (ev.target.id === 'agent_chat_form') {
      ev.preventDefault();
      sendUserMessage();
      return;
    }
    if (ev.target.id === 'agent_project_create_btn' || (ev.target.tagName === 'BUTTON' && ev.target.closest('#agent_project_create_btn'))) {
      ev.preventDefault();
      return;
    }
  }

  function sendUserMessage() {
    var input = document.getElementById('agent_chat_input');
    var session = window.AGENT_SESSION;
    if (!input || !session) return;
    var text = input.value.trim();
    if (!text) return;
    input.value = '';
    appendMessage({
      id: 'tmp_' + Date.now(),
      role: 'user',
      kind: 'message',
      content: text,
      iteration: 0,
      sequence: (nextSeq() + 1),
      created_at: Date.now(),
    });
    apiPost('/admin/background-agent/ajax/sessions/' + session.id + '/message/', { content: text })
      .then(function (r) {
        if (!r.ok) showToast(r.data.error || 'send failed', 'error');
      })
      .catch(function (e) { showToast(String(e), 'error'); });
  }

  function controlSession(sessionId, action) {
    apiPost('/admin/background-agent/ajax/sessions/' + sessionId + '/control/', { action: action })
      .then(function (r) {
        if (!r.ok) { showToast(r.data.error || 'control failed', 'error'); return; }
        showToast('Session ' + action + 'd', 'success');
        if (r.data.status) updateStatusPill(r.data.status);
      });
  }

  function refreshProject(projectId) {
    apiPost('/admin/background-agent/ajax/projects/' + projectId + '/refresh/')
      .then(function (r) {
        if (!r.ok) { showToast(r.data.error || 'refresh failed', 'error'); return; }
        showToast('Repo refreshed', 'success');
      });
  }

  function deleteProject(projectId) {
    apiPost('/admin/background-agent/ajax/projects/' + projectId + '/delete/')
      .then(function (r) {
        if (!r.ok) { showToast(r.data.error || 'archive failed', 'error'); return; }
        showToast('Project archived', 'success');
        setTimeout(function () { location.reload(); }, 700);
      });
  }

  function pushBranch(sessionId) {
    showToast('Pushing branch to origin…', 'info');
    apiPost('/admin/background-agent/ajax/sessions/' + sessionId + '/push/')
      .then(function (r) {
        if (!r.ok) { showToast(r.data.error || 'push failed', 'error'); return; }
        showToast('Branch pushed', 'success');
      });
  }

  function openPr(sessionId) {
    showToast('Opening pull request…', 'info');
    apiPost('/admin/background-agent/ajax/sessions/' + sessionId + '/pr/', {})
      .then(function (r) {
        if (!r.ok) { showToast(r.data.error || 'PR failed', 'error'); return; }
        showToast('PR #' + r.data.pr_number + ' opened', 'success');
        if (r.data.pr_url) {
          var link = document.querySelector('.agent-pr-link');
          if (!link) {
            var row = document.querySelector('.agent-session-meta');
            if (row) {
              var cell = el('div', { class: 'agent-meta-cell' }, [
                el('span', { class: 'agent-meta-label' }, ['Pull request']),
                el('a', { href: r.data.pr_url, target: '_blank', rel: 'noopener', class: 'agent-pr-link', text: r.data.pr_url }),
              ]);
              row.appendChild(cell);
            }
          } else {
            link.href = r.data.pr_url;
            link.textContent = r.data.pr_url;
          }
        }
        updateStatusPill('pr_opened');
      });
  }

  function loadDiff(sessionId) {
    var pre = document.getElementById('agent_diff_view');
    if (!pre) return;
    pre.hidden = false;
    pre.textContent = 'Loading diff…';
    apiGet('/admin/background-agent/ajax/sessions/' + sessionId + '/diff/')
      .then(function (r) {
        if (!r.ok) { pre.textContent = r.data.error || 'diff failed'; return; }
        pre.textContent = r.data.diff || '(no diff yet)';
      });
  }

  function nextSeq() {
    var last = document.querySelector('.agent-message[data-sequence]');
    if (!last) return 0;
    return parseInt(last.dataset.sequence || '0', 10);
  }

  function appendMessage(m) {
    var container = document.getElementById('agent_messages');
    if (!container) return;
    if (m.id && document.querySelector('[data-message-id="' + m.id + '"]')) return;
    var node = renderMessage(m);
    container.appendChild(node);
    container.parentElement.scrollTop = container.parentElement.scrollHeight;
  }

  function renderMessage(m) {
    var cls = 'agent-message agent-message-' + m.role + ' agent-message-' + m.kind;
    var roleLabel = m.role === 'assistant' ? 'Agent' : (m.role === 'user' ? 'You' : (m.tool_name || 'Tool'));
    var header = el('header', { class: 'agent-message-head' }, [
      el('span', { class: 'material-symbols-outlined agent-message-icon', text: m.role === 'user' ? 'person' : (m.role === 'assistant' ? 'smart_toy' : 'build') }),
      el('span', { class: 'agent-message-role', text: roleLabel + (m.iteration ? ' #' + m.iteration : '') }),
      el('span', { class: 'agent-message-time', text: '#' + (m.sequence || '?') }),
    ]);
    var body = el('div', { class: 'agent-message-body' });
    if (m.kind === 'message') {
      if (m.content) body.appendChild(el('pre', { class: 'agent-message-text', text: m.content }));
    } else if (m.kind === 'tool_call') {
      var card = el('div', { class: 'agent-tool-card agent-tool-call' }, [
        el('header', null, [el('span', { class: 'material-symbols-outlined', text: 'play_arrow' }), m.tool_name || '']),
      ]);
      if (m.tool_args) card.appendChild(el('pre', { class: 'agent-tool-args', text: m.tool_args }));
      body.appendChild(card);
    } else if (m.kind === 'tool_result') {
      var cardR = el('div', { class: 'agent-tool-card agent-tool-result agent-tool-status-' + (m.tool_status || 'pending') }, [
        el('header', null, [
          el('span', { class: 'material-symbols-outlined', text: m.tool_status === 'ok' ? 'check_circle' : (m.tool_status === 'error' ? 'error' : (m.tool_status === 'timeout' ? 'timer_off' : 'pending')) }),
          (m.tool_name || 'Tool') + ' — ' + (m.tool_status || 'pending'),
        ]),
      ]);
      if (m.tool_result) cardR.appendChild(el('pre', { class: 'agent-tool-result-text', text: m.tool_result }));
      body.appendChild(cardR);
    }
    var wrap = el('div', { class: cls, 'data-message-id': m.id || '', 'data-sequence': m.sequence || 0 }, []);
    if (m.role !== 'system') wrap.appendChild(header);
    wrap.appendChild(body);
    return wrap;
  }

  function updateStatusPill(status) {
    var pill = document.getElementById('agent-status-pill');
    if (!pill) return;
    pill.className = 'agent-status-pill agent-status-' + status;
    pill.textContent = status.replace(/_/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); });
  }

  function appendTimeline(ev) {
    var root = document.getElementById('agent_timeline');
    if (!root) return;
    var row = el('div', { class: 'agent-timeline-row timeline-' + (ev.event_type || 'log') }, [
      el('span', { class: 'agent-timeline-dot' }),
      el('div', null, [
        el('div', { class: 'agent-timeline-summary', text: ev.summary || '' }),
        ev.detail ? el('div', { class: 'agent-timeline-detail', text: String(ev.detail).substring(0, 400) }) : null,
        el('div', { class: 'agent-timeline-time', text: formatTime(ev.created_at) }),
      ]),
    ]);
    root.insertBefore(row, root.firstChild);
    while (root.children.length > 100) root.removeChild(root.lastChild);
  }

  function upsertFileChange(fc) {
    var root = document.getElementById('agent_file_changes');
    if (!root) return;
    var existing = root.querySelector('[data-path="' + CSS.escape(fc.path) + '"][data-op="' + fc.op + '"]');
    if (existing) {
      var stats = existing.querySelector('.agent-file-stats');
      if (stats) stats.textContent = '+' + fc.additions + '/-' + fc.deletions;
      return;
    }
    var row = el('div', { class: 'agent-file-row', 'data-path': fc.path, 'data-op': fc.op }, [
      el('span', { class: 'agent-file-op agent-file-op-' + fc.op, text: fc.op.charAt(0).toUpperCase() + fc.op.slice(1) }),
      el('span', { class: 'agent-file-path', title: fc.path, text: fc.path }),
      el('span', { class: 'agent-file-stats', text: '+' + fc.additions + '/-' + fc.deletions }),
      el('span', { class: 'agent-file-committed ' + (fc.committed ? 'committed' : 'uncommitted') }, [
        el('span', { class: 'material-symbols-outlined', style: 'font-size:14px;', text: fc.committed ? 'check_circle' : 'pending' }),
      ]),
    ]);
    var empty = root.querySelector('.agent-empty-inline');
    if (empty) empty.remove();
    root.insertBefore(row, root.firstChild);
  }

  if (window.AGENT_GH_CONNECTED) {
    loadRepos('');
    var search = document.getElementById('agent_repo_search');
    var refresh = document.getElementById('agent_repo_refresh');
    if (search) search.addEventListener('input', debounce(function () { loadRepos(search.value.trim()); }, 250));
    if (refresh) refresh.addEventListener('click', function () { loadRepos(search ? search.value.trim() : '', true); });
  }

  var projectNewBtn = document.getElementById('agent_project_create_btn');
  if (projectNewBtn) {
    projectNewBtn.addEventListener('click', function (ev) {
      ev.preventDefault();
      createProject();
    });
  }

  var newSessionBtn = document.getElementById('agent_new_session_btn');
  if (newSessionBtn) {
    newSessionBtn.addEventListener('click', createNewSession);
  }

  function debounce(fn, wait) {
    var t = null;
    return function () { var args = arguments, self = this; clearTimeout(t); t = setTimeout(function () { fn.apply(self, args); }, wait); };
  }

  function loadRepos(query, refresh) {
    var root = document.getElementById('agent_repo_results');
    if (!root) return;
    root.dataset.loading = 'true';
    var qs = '?q=' + encodeURIComponent(query || '');
    if (refresh) qs += '&refresh=1';
    fetch('/admin/background-agent/ajax/github/repos/' + qs, { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        root.dataset.loading = 'false';
        root.innerHTML = '';
        if (!data.repos || !data.repos.length) {
          root.appendChild(el('div', { class: 'agent-empty' }, [
            el('span', { class: 'material-symbols-outlined agent-empty-icon', text: 'search_off' }),
            el('p', null, [query ? 'No repos match "' + query + '"' : 'No repositories visible to this GitHub account.']),
          ]));
          return;
        }
        for (var i = 0; i < data.repos.length; i++) {
          (function (repo) {
            var row = el('div', { class: 'agent-repo-row', 'data-full-name': repo.full_name }, [
              el('div', null, [
                el('div', { class: 'agent-repo-name' }, [repo.full_name + ' ']),
                el('div', { class: 'agent-repo-desc', text: repo.description || '' }),
                el('div', { class: 'agent-repo-meta' }, [
                  el('span', { class: 'agent-chip agent-chip-' + (repo.private ? 'private' : 'public'), text: repo.private ? 'private' : 'public' }),
                  el('span', { class: 'agent-chip', text: '⭐ ' + (repo.stargazers_count || 0) }),
                  el('span', { class: 'agent-chip', text: 'updated ' + (repo.updated_at || '').substring(0, 10) }),
                ]),
              ]),
            ]);
            row.addEventListener('click', function () {
              var sel = root.querySelector('.agent-repo-row.selected');
              if (sel) sel.classList.remove('selected');
              row.classList.add('selected');
              if (projectNewBtn) projectNewBtn.disabled = false;
              projectNewBtn.dataset.fullName = repo.full_name;
            });
            root.appendChild(row);
          })(data.repos[i]);
        }
      })
      .catch(function (e) {
        root.dataset.loading = 'false';
        root.innerHTML = '';
        root.appendChild(el('div', { class: 'agent-empty' }, [
          el('span', { class: 'material-symbols-outlined agent-empty-icon', text: 'error' }),
          el('p', null, ['GitHub fetch failed: ' + (e.message || e)]),
        ]));
      });
  }

  function createProject() {
    var btn = document.getElementById('agent_project_create_btn');
    if (!btn || !btn.dataset.fullName) return;
    var provider = document.getElementById('agent_project_provider').value;
    var model = document.getElementById('agent_project_model').value.trim();
    var sysp = document.getElementById('agent_project_system_prompt').value;
    btn.disabled = true;
    btn.innerHTML = '<span class="agent-spinner"><span class="agent-spinner-dot"></span><span class="agent-spinner-dot"></span><span class="agent-spinner-dot"></span></span> Connecting…';
    apiPost('/admin/background-agent/ajax/projects/create/', {
      repo_full_name: btn.dataset.fullName,
      provider: provider, model: model, system_prompt: sysp,
    }).then(function (r) {
      if (!r.ok) {
        btn.disabled = false;
        btn.innerHTML = '<span class="material-symbols-outlined" style="font-size:18px;">add</span> Connect this repository';
        showToast(r.data.error || 'Connection failed', 'error');
        return;
      }
      showToast('Repo connected', 'success');
      window.location.href = '/admin/background-agent/projects/' + r.data.project_id + '/';
    });
  }

  function createNewSession() {
    var taskEl = document.getElementById('agent_new_task');
    var titleEl = document.getElementById('agent_new_title');
    var providerEl = document.getElementById('agent_new_provider');
    var modelEl = document.getElementById('agent_new_model');
    if (!taskEl) return;
    var task = taskEl.value.trim();
    if (!task) { showToast('Add a task first', 'error'); return; }
    var data = {
      project_id: document.body.dataset.agentProjectId || document.querySelector('[data-page="project-detail"]').dataset.projectId,
      task: task,
      title: titleEl ? titleEl.value : '',
      provider: providerEl ? providerEl.value : '',
      model: modelEl ? modelEl.value.trim() : '',
    };
    apiPost('/admin/background-agent/ajax/sessions/create/', data).then(function (r) {
      if (!r.ok) { showToast(r.data.error || 'Could not start session', 'error'); return; }
      window.location.href = '/admin/background-agent/sessions/' + r.data.session_id + '/';
    });
  }

  var session = window.AGENT_SESSION;
  if (session) {
    preloadInitialState();
    initSessionSocket();
    var form = document.getElementById('agent_chat_form');
    if (form) {
      var inputEl = document.getElementById('agent_chat_input');
      if (inputEl) {
        inputEl.addEventListener('keydown', function (e) {
          if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') { e.preventDefault(); form.dispatchEvent(new Event('submit')); }
        });
      }
    }
  }

  function preloadInitialState() {
    var dataEl = document.getElementById('agent_session_data');
    if (!dataEl) return;
    var parseMaybe = function (s) { try { return JSON.parse(s || '[]'); } catch (e) { return []; } };
    var messages = parseMaybe(dataEl.dataset.initialMessages);
    var events = parseMaybe(dataEl.dataset.initialEvents);
    var files = parseMaybe(dataEl.dataset.initialFiles);
    var container = document.getElementById('agent_messages');
    if (container) {
      container.innerHTML = '';
      for (var i = 0; i < messages.length; i++) container.appendChild(renderMessage(messages[i]));
      container.parentElement.scrollTop = container.parentElement.scrollHeight;
    }
    var evRoot = document.getElementById('agent_timeline');
    if (evRoot) {
      for (var j = 0; j < events.length; j++) appendTimeline(events[j]);
    }
    var fileRoot = document.getElementById('agent_file_changes');
    if (fileRoot) {
      fileRoot.innerHTML = '';
      if (!files.length) {
        fileRoot.appendChild(el('div', { class: 'agent-empty-inline', text: 'No file changes yet.' }));
      } else {
        for (var k = 0; k < files.length; k++) upsertFileChange(files[k]);
      }
    }
  }

  function initSessionSocket() {
    var url = (window.WS_CONFIG && window.WS_CONFIG.url) || (window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/';
    var stateLabel = document.getElementById('agent_connection_label');
    var stateDot = document.querySelector('.agent-conn-dot');

    function setState(state) {
      if (stateDot) stateDot.dataset.state = state;
      if (stateLabel) stateLabel.textContent = state === 'open' ? 'live' : state;
    }

    function connect() {
      setState('connecting');
      try {
        var ws = new WebSocket(url);
        ws.onopen = function () {
          setState('open');
          ws.send(JSON.stringify({ action: 'subscribe', channel: session.wsGroup }));
          ws.send(JSON.stringify({ action: 'subscribe', channel: session.userWsGroup }));
        };
        ws.onmessage = function (msg) {
          try { handleWsEvent(JSON.parse(msg.data)); } catch (e) {}
        };
        ws.onclose = function () { setState('closed'); setTimeout(connect, 2500); };
        ws.onerror = function () { setState('closed'); };
      } catch (e) {
        setState('closed');
        setTimeout(connect, 4000);
      }
    }

    function pollFallback() {
      apiGet('/admin/background-agent/ajax/sessions/' + session.id + '/files/').then(function (r) {
        if (r.ok && r.data.changes) {
          for (var i = 0; i < r.data.changes.length; i++) upsertFileChange(r.data.changes[i]);
        }
      });
    }
    setInterval(pollFallback, 8000);

    connect();
  }

  function handleWsEvent(msg) {
    if (!msg || !msg.data) return;
    if (msg.event === 'agent.message_added') { appendMessage(msg.data); refreshCounters(); }
    else if (msg.event === 'agent.tool_call') { refreshFiles(); refreshCounters(); }
    else if (msg.event === 'agent.event') { appendTimeline(msg.data); refreshFiles(); }
    else if (msg.event === 'agent.status') { if (msg.data && msg.data.status) updateStatusPill(msg.data.status); refreshCounters(); }
    else if (msg.event === 'agent.file_change') { upsertFileChange(msg.data); }
  }

  function refreshFiles() {
    apiGet('/admin/background-agent/ajax/sessions/' + session.id + '/files/').then(function (r) {
      if (r.ok && r.data && r.data.changes) {
        var root = document.getElementById('agent_file_changes');
        if (root) root.innerHTML = '';
        for (var i = 0; i < r.data.changes.length; i++) upsertFileChange(r.data.changes[i]);
      }
    });
  }

  function refreshCounters() {
    apiGet('/admin/background-agent/ajax/sessions/' + session.id + '/files/').then(function (r) {
      if (!r.ok) return;
      var meta = document.getElementById('agent_meta_branch');
      if (meta && r.data.branch) meta.textContent = r.data.branch;
    });
  }

  init();
})();
