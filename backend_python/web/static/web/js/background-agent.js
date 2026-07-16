/* Background Coding Agent — Task detail page JS */

(function() {
  const container = document.querySelector('.ba-task-container');
  if (!container) return;
  
  const taskId = container.dataset.taskId;
  const wsUrl = container.dataset.wsUrl;
  let pollInterval = null;
  let wsConnection = null;
  let activeTab = 'chat';
  
  function init() {
    formatTimestamps();
    startPolling();
    connectWebSocket();

    document.getElementById('chat-input').addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    var btnSend = document.getElementById('ba-btn-send');
    if (btnSend) btnSend.addEventListener('click', sendMessage);

    var btnPause = document.getElementById('ba-btn-pause');
    if (btnPause) btnPause.addEventListener('click', function() { taskAction('pause'); });

    var btnResume = document.getElementById('ba-btn-resume');
    if (btnResume) btnResume.addEventListener('click', function() { taskAction('resume'); });

    var btnStop = document.getElementById('ba-btn-stop');
    if (btnStop) btnStop.addEventListener('click', function() { taskAction('stop'); });

    var btnPush = document.getElementById('ba-btn-push');
    if (btnPush) btnPush.addEventListener('click', function() { pushToGithub(false); });

    var btnPushPr = document.getElementById('ba-btn-push-pr');
    if (btnPushPr) btnPushPr.addEventListener('click', function() { pushToGithub(true); });

    var btnRefreshDiff = document.getElementById('ba-btn-refresh-diff');
    if (btnRefreshDiff) btnRefreshDiff.addEventListener('click', refreshDiff);

    document.querySelectorAll('.ba-tab').forEach(function(tab) {
      tab.addEventListener('click', function() { switchTab(tab.dataset.tab); });
    });
  }
  
  function formatTimestamps() {
    document.querySelectorAll('[data-ts]').forEach(function(el) {
      const ts = parseInt(el.dataset.ts);
      if (ts && ts > 0) {
        const d = new Date(ts);
        el.textContent = d.toLocaleString();
      }
    });
  }
  
  function switchTab(tab) {
    activeTab = tab;
    document.querySelectorAll('.ba-tab').forEach(function(t) {
      t.classList.toggle('active', t.dataset.tab === tab);
    });
    document.querySelectorAll('.ba-tab-content').forEach(function(c) {
      c.classList.toggle('active', c.id === 'tab-' + tab);
    });
  }

  
  function startPolling() {
    if (pollInterval) clearInterval(pollInterval);
    pollInterval = setInterval(pollStatus, 5000);
    pollStatus();
  }
  
  async function pollStatus() {
    try {
      const resp = await fetch(`/backgroundagent/ajax/task/${taskId}/status/`, {
        headers: { 'X-CSRFToken': CSRF_TOKEN },
      });
      if (!resp.ok) return;
      const data = await resp.json();
      updateUI(data);
    } catch (e) {
      console.debug('Poll error:', e);
    }
  }
  
  function updateUI(data) {
    const task = data.task;
    if (!task) return;
    
    const statusEl = document.getElementById('sidebar-status');
    if (statusEl) {
      statusEl.textContent = task.status;
      statusEl.className = `ba-task-status-badge ba-status-badge-${task.status}`;
    }
    
    const iterEl = document.getElementById('sidebar-iteration');
    if (iterEl) {
      iterEl.textContent = `${task.iteration} / ${task.maxIterations}`;
    }
    
    const thoughtEl = document.getElementById('sidebar-thought');
    if (thoughtEl && task.lastThought) {
      thoughtEl.textContent = task.lastThought.substring(0, 200);
    }
    
    updateControls(task.status);
    updateRecentMessages(data.recentMessages);
    updateRecentActions(data.recentActions);
    
    if (task.prUrl && !document.querySelector('.ba-pr-banner')) {
      const banner = document.createElement('div');
      banner.className = 'ba-pr-banner';
      banner.innerHTML = `<span class="material-symbols-outlined" style="color:#10b981;">check_circle</span><span>Pull Request created: <a href="${task.prUrl}" target="_blank" style="color:var(--md-primary);">${task.prUrl}</a></span>`;
      container.querySelector('.ba-task-controls').after(banner);
    }
    
    if (task.status === 'completed' || task.status === 'failed' || task.status === 'stopped') {
      if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
      }
    }
  }
  
  function updateControls(status) {
    const pauseBtn = document.querySelector('.ba-btn-pause');
    const resumeBtn = document.querySelector('.ba-btn-resume');
    const stopBtn = document.querySelector('.ba-btn-stop');
    
    if (pauseBtn) pauseBtn.disabled = status !== 'running';
    if (resumeBtn) resumeBtn.disabled = status !== 'paused' && status !== 'stopped';
    if (stopBtn) stopBtn.disabled = status === 'completed' || status === 'failed';
  }
  
  function updateRecentMessages(messages) {
    if (!messages || !messages.length) return;
    const container = document.getElementById('chat-messages');
    if (!container) return;
    
    const existingIds = new Set();
    container.querySelectorAll('.ba-chat-msg').forEach(function(el) {
      if (el.dataset.msgId) existingIds.add(el.dataset.msgId);
    });
    
    let hasNew = false;
    messages.forEach(function(msg) {
      if (!existingIds.has(msg.id)) {
        hasNew = true;
        const msgEl = createMessageElement(msg);
        container.appendChild(msgEl);
      }
    });
    
    if (hasNew) {
      container.scrollTop = container.scrollHeight;
      formatTimestamps();
    }
  }
  
  function createMessageElement(msg) {
    const div = document.createElement('div');
    div.className = `ba-chat-msg ba-chat-msg-${msg.role}`;
    div.dataset.msgId = msg.id;
    
    let headerText = msg.role;
    let headerIcon = 'info';
    if (msg.role === 'user') { headerText = 'User'; headerIcon = 'person'; }
    else if (msg.role === 'assistant') { headerText = 'Agent'; headerIcon = 'smart_toy'; }
    else if (msg.role === 'tool_result') { headerText = 'Tool Results'; headerIcon = 'terminal'; }
    
    let html = `<div class="ba-chat-msg-header"><span class="material-symbols-outlined" style="font-size:16px;">${headerIcon}</span> ${headerText}<span class="ba-chat-msg-time" data-ts="${msg.createdAt}"></span></div>`;
    
    if (msg.thoughts) {
      html += `<div class="ba-chat-thoughts"><span class="material-symbols-outlined" style="font-size:14px;vertical-align:middle;">psychology</span> ${escapeHtml(msg.thoughts)}</div>`;
    }
    
    html += `<div class="ba-chat-content">${escapeHtml(msg.content).substring(0, 5000)}</div>`;
    
    if (msg.toolActions && msg.toolActions.length) {
      html += '<div class="ba-chat-actions">';
      msg.toolActions.forEach(function(action) {
        const argsStr = JSON.stringify(action.args || {}).substring(0, 80);
        html += `<div class="ba-chat-action-pill"><span class="material-symbols-outlined" style="font-size:14px;">build</span>${escapeHtml(action.tool)}(${escapeHtml(argsStr)})</div>`;
      });
      html += '</div>';
    }
    
    div.innerHTML = html;
    return div;
  }
  
  function updateRecentActions(actions) {
    if (!actions || !actions.length) return;
    const container = document.getElementById('logs-list');
    if (!container) return;
    
    const existingIds = new Set();
    container.querySelectorAll('.ba-log-row').forEach(function(el) {
      if (el.dataset.logId) existingIds.add(el.dataset.logId);
    });
    
    let hasNew = false;
    actions.forEach(function(log) {
      if (!existingIds.has(log.id)) {
        hasNew = true;
        const logEl = createLogElement(log);
        container.insertBefore(logEl, container.firstChild);
      }
    });
    
    if (hasNew) formatTimestamps();
  }
  
  function createLogElement(log) {
    const div = document.createElement('div');
    div.className = `ba-log-row ba-log-${log.status}`;
    div.dataset.logId = log.id;
    
    const icons = {
      read: 'file_open', write: 'edit_note', list: 'folder_open',
      search: 'search', command: 'terminal', git: 'git', status: 'info',
    };
    const icon = icons[log.actionType] || 'info';
    
    let html = `<span class="ba-log-icon"><span class="material-symbols-outlined" style="font-size:16px;">${icon}</span></span>`;
    html += '<div class="ba-log-content">';
    html += '<div class="ba-log-header">';
    html += `<span class="ba-log-type">${log.actionType}</span>`;
    if (log.filePath) html += `<span class="ba-log-file">${escapeHtml(log.filePath)}</span>`;
    html += `<span class="ba-log-time" data-ts="${log.createdAt}"></span>`;
    html += `<span class="ba-log-iter">iter ${log.iteration}</span>`;
    html += '</div>';
    html += `<div class="ba-log-desc">${escapeHtml(log.description).substring(0, 500)}</div>`;
    if (log.contentDiff) {
      html += `<pre class="ba-log-diff">${escapeHtml(log.contentDiff).substring(0, 500)}</pre>`;
    }
    html += '</div>';
    
    div.innerHTML = html;
    return div;
  }
  
  window.taskAction = async function(action) {
    try {
      const resp = await fetch(`/backgroundagent/ajax/task/${taskId}/action/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
        body: JSON.stringify({ action: action }),
      });
      const data = await resp.json();
      if (resp.ok) {
        showSnackbar(`Task ${data.status}`);
        setTimeout(pollStatus, 500);
      } else {
        showSnackbar(data.error || 'Action failed');
      }
    } catch (err) {
      showSnackbar('Error: ' + err.message);
    }
  };
  
  window.sendMessage = async function() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;
    
    input.value = '';
    
    const msgDiv = document.createElement('div');
    msgDiv.className = 'ba-chat-msg ba-chat-msg-user';
    msgDiv.innerHTML = `<div class="ba-chat-msg-header"><span class="material-symbols-outlined" style="font-size:16px;">person</span> User</div><div class="ba-chat-content">${escapeHtml(message)}</div>`;
    document.getElementById('chat-messages').appendChild(msgDiv);
    document.getElementById('chat-messages').scrollTop = 999999;
    
    try {
      const resp = await fetch(`/backgroundagent/ajax/task/${taskId}/send-message/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
        body: JSON.stringify({ message: message }),
      });
      const data = await resp.json();
      if (resp.ok) {
        showSnackbar('Message sent to agent');
        if (!pollInterval) startPolling();
      } else {
        showSnackbar(data.error || 'Failed to send message');
      }
    } catch (err) {
      showSnackbar('Error: ' + err.message);
    }
  };
  
  window.refreshDiff = async function() {
    try {
      const resp = await fetch(`/backgroundagent/ajax/task/${taskId}/diff/`, {
        headers: { 'X-CSRFToken': CSRF_TOKEN },
      });
      const data = await resp.json();
      if (resp.ok) {
        const viewer = document.getElementById('diff-viewer');
        if (viewer) viewer.textContent = data.diff || '(no changes)';
        showSnackbar('Diff refreshed');
      } else {
        showSnackbar(data.error || 'Failed to refresh diff');
      }
    } catch (err) {
      showSnackbar('Error: ' + err.message);
    }
  };
  
  window.pushToGithub = async function(createPr) {
    if (!confirm(createPr ? 'Push changes to GitHub and create a Pull Request?' : 'Push changes to GitHub?')) return;
    
    showSnackbar('Pushing to GitHub...');
    
    try {
      const resp = await fetch(`/backgroundagent/ajax/task/${taskId}/push-github/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
        body: JSON.stringify({ create_pr: createPr }),
      });
      const data = await resp.json();
      if (resp.ok) {
        if (data.prUrl) {
          showSnackbar(`PR created: ${data.prUrl}`);
          setTimeout(() => window.location.reload(), 2000);
        } else if (data.prError) {
          showSnackbar(`Pushed but PR failed: ${data.prError}`);
        } else {
          showSnackbar('Pushed to GitHub successfully');
        }
      } else {
        showSnackbar(data.error || 'Push failed');
      }
    } catch (err) {
      showSnackbar('Error: ' + err.message);
    }
  };
  
  function connectWebSocket() {
    if (!wsUrl || wsUrl === 'None') return;
    
    try {
      const ws = new WebSocket(wsUrl);
      wsConnection = ws;
      
      ws.onopen = function() {
        ws.send(JSON.stringify({ action: 'subscribe', channel: `codingagent.${taskId}` }));
      };
      
      ws.onmessage = function(event) {
        try {
          const msg = JSON.parse(event.data);
          if (msg.type === 'event' && msg.channel === `codingagent.${taskId}`) {
            pollStatus();
          }
        } catch (e) {}
      };
      
      ws.onclose = function() {
        wsConnection = null;
      };
      
      ws.onerror = function() {
        wsConnection = null;
      };
    } catch (e) {
      console.debug('WS connect failed:', e);
    }
  }
  
  function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
