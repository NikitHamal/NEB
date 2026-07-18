(function () {
  'use strict';

  if (!window.fetch) return;

  var currentAttachments = [];

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

  function apiPost(url, body) {
    return fetch(url, { method: 'POST', credentials: 'same-origin', headers: csrfHeader(), body: JSON.stringify(body || {}) })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); });
  }

  function apiGet(url) {
    return fetch(url, { credentials: 'same-origin', headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); });
  }

  function renderSimpleMarkdown(text) {
    if (!text) return '';
    var esc = String(text)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
    
    // Code blocks
    esc = esc.replace(/```([\s\S]*?)```/g, function (match, p1) {
      return '<pre class="code-preview"><code>' + p1 + '</code></pre>';
    });
    // Inline code
    esc = esc.replace(/`([^`]+)`/g, '<code>$1</code>');
    // Bold
    esc = esc.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    // Headings
    esc = esc.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    esc = esc.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    esc = esc.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    // Paragraphs
    esc = esc.replace(/\n\n/g, '</p><p>');
    return '<p>' + esc + '</p>';
  }

  function init() {
    if (document.body.dataset.agentReady === '1') return;
    document.body.dataset.agentReady = '1';

    bindModelSelector();
    bindAttachments();
    bindHomeSessionForm();
    bindRightPaneTabs();
    bindInbuiltFileViewer();

    document.addEventListener('click', handleClick);
    document.addEventListener('submit', handleSubmit);

    var session = window.AGENT_SESSION;
    if (session) {
      initSessionSocket();
      loadWorkspaceFiles(session.id);
      loadSessionLogs(session.id);
    }
  }

  function bindModelSelector() {
    var dropdownBtn = document.getElementById('agent_model_dropdown_btn');
    var popover = document.getElementById('agent_model_popover');
    var searchInput = document.getElementById('agent_model_search_input');

    if (dropdownBtn && popover) {
      dropdownBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        popover.hidden = !popover.hidden;
        if (!popover.hidden && searchInput) searchInput.focus();
      });

      document.addEventListener('click', function (e) {
        if (!popover.contains(e.target) && !dropdownBtn.contains(e.target)) {
          popover.hidden = true;
        }
      });

      var options = popover.querySelectorAll('.agent-model-option');
      for (var i = 0; i < options.length; i++) {
        options[i].addEventListener('click', function () {
          var opt = this;
          var provider = opt.dataset.provider;
          var model = opt.dataset.model;
          var name = opt.querySelector('.opt-name').textContent;

          popover.querySelectorAll('.agent-model-option').forEach(function (o) {
            o.classList.remove('active');
            var chk = o.querySelector('.opt-check');
            if (chk) chk.textContent = '';
          });

          opt.classList.add('active');
          var check = opt.querySelector('.opt-check');
          if (check) check.textContent = 'check';

          var label = document.getElementById('agent_selected_model_label');
          if (label) label.textContent = name + ': Qwen 3.7 Plus';

          dropdownBtn.dataset.provider = provider;
          dropdownBtn.dataset.model = model;
          popover.hidden = true;
        });
      }

      if (searchInput) {
        searchInput.addEventListener('input', function () {
          var q = searchInput.value.toLowerCase();
          options.forEach(function (o) {
            var txt = o.textContent.toLowerCase();
            o.style.display = txt.indexOf(q) !== -1 ? 'flex' : 'none';
          });
        });
      }
    }
  }

  function bindAttachments() {
    var attachBtns = ['agent_home_attach_btn', 'agent_session_attach_btn', 'agent_detail_attach_btn'];
    var fileInputs = ['agent_home_file_input', 'agent_session_file_input', 'agent_detail_file_input'];

    attachBtns.forEach(function (btnId, idx) {
      var btn = document.getElementById(btnId);
      var inp = document.getElementById(fileInputs[idx]);
      if (btn && inp) {
        btn.addEventListener('click', function () { inp.click(); });
        inp.addEventListener('change', function () {
          if (!inp.files || !inp.files.length) return;
          for (var i = 0; i < inp.files.length; i++) {
            uploadFileAttachment(inp.files[i]);
          }
          inp.value = '';
        });
      }
    });
  }

  function uploadFileAttachment(file) {
    var formData = new FormData();
    formData.append('file', file);

    fetch('/backgroundagent/ajax/upload-attachment/', {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken() },
      body: formData,
    })
    .then(function (r) { return r.json(); })
    .then(function (res) {
      if (res.ok && res.attachment) {
        currentAttachments.push(res.attachment);
        renderAttachmentPreviews();
        showToast('Attached ' + res.attachment.name, 'success');
      } else {
        showToast(res.error || 'Upload failed', 'error');
      }
    })
    .catch(function (err) {
      showToast('Upload error: ' + err, 'error');
    });
  }

  function renderAttachmentPreviews() {
    var previewRows = [
      document.getElementById('agent_home_attachments_preview'),
      document.getElementById('agent_chat_attachments_preview'),
      document.getElementById('agent_detail_attachments_preview')
    ];

    previewRows.forEach(function (row) {
      if (!row) return;
      row.innerHTML = '';
      if (!currentAttachments.length) {
        row.hidden = true;
        return;
      }
      row.hidden = false;
      currentAttachments.forEach(function (att, idx) {
        var chip = el('div', { class: 'attachment-chip' }, [
          att.is_image ? el('img', { src: att.url, alt: att.name }) : el('span', { class: 'material-symbols-outlined' }, ['attach_file']),
          el('span', null, [att.name]),
          el('span', { class: 'attachment-remove-btn', onclick: function () {
            currentAttachments.splice(idx, 1);
            renderAttachmentPreviews();
          } }, ['×'])
        ]);
        row.appendChild(chip);
      });
    });
  }

  function bindHomeSessionForm() {
    var homeForm = document.getElementById('agent_home_session_form');
    if (homeForm) {
      homeForm.addEventListener('submit', function (e) {
        e.preventDefault();
        var taskInput = document.getElementById('agent_home_task_input');
        var projSelect = document.getElementById('agent_home_project_select');
        var dropdownBtn = document.getElementById('agent_model_dropdown_btn');

        if (!taskInput || !taskInput.value.trim()) {
          showToast('Please enter a task prompt', 'error');
          return;
        }
        if (!projSelect || !projSelect.value) {
          showToast('Please select or connect a GitHub repository first', 'error');
          return;
        }

        var provider = (dropdownBtn && dropdownBtn.dataset.provider) || 'qwen';
        var model = (dropdownBtn && dropdownBtn.dataset.model) || 'qwen3.7-plus';

        showToast('Queueing background session...', 'info');

        apiPost('/backgroundagent/ajax/sessions/create/', {
          project_id: projSelect.value,
          task: taskInput.value.trim(),
          provider: provider,
          model: model,
          attachments: currentAttachments,
        }).then(function (res) {
          if (res.ok && res.data.session_id) {
            currentAttachments = [];
            window.location.href = '/backgroundagent/sessions/' + res.data.session_id + '/';
          } else {
            showToast(res.data.error || 'Could not start session', 'error');
          }
        });
      });
    }
  }

  function bindRightPaneTabs() {
    var tabs = document.querySelectorAll('.pane-tab');
    var addViewBtn = document.getElementById('pane_add_view_btn');
    var addViewMenu = document.getElementById('pane_add_view_menu');
    var togglePaneBtn = document.getElementById('toggle_right_pane_btn');
    var rightPane = document.getElementById('agent_right_pane');

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (t) { t.classList.remove('active'); });
        tab.classList.add('active');

        var targetTab = tab.dataset.tab;
        var contents = document.querySelectorAll('.tab-content');
        contents.forEach(function (c) { c.classList.remove('active'); });

        var targetContent = document.getElementById('tab_' + targetTab + '_content');
        if (targetContent) targetContent.classList.add('active');
      });
    });

    if (addViewBtn && addViewMenu) {
      addViewBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        addViewMenu.hidden = !addViewMenu.hidden;
      });

      document.addEventListener('click', function (e) {
        if (!addViewMenu.contains(e.target) && !addViewBtn.contains(e.target)) {
          addViewMenu.hidden = true;
        }
      });

      var items = addViewMenu.querySelectorAll('.add-view-item');
      items.forEach(function (item) {
        item.addEventListener('click', function () {
          var tabName = item.dataset.tab;
          var matchingTab = document.querySelector('.pane-tab[data-tab="' + tabName + '"]');
          if (matchingTab) matchingTab.click();
          addViewMenu.hidden = true;
        });
      });
    }

    if (togglePaneBtn && rightPane) {
      togglePaneBtn.addEventListener('click', function () {
        if (rightPane.style.display === 'none') {
          rightPane.style.display = 'flex';
          togglePaneBtn.classList.add('active');
        } else {
          rightPane.style.display = 'none';
          togglePaneBtn.classList.remove('active');
        }
      });
    }
  }

  function bindInbuiltFileViewer() {
    var refreshTreeBtn = document.getElementById('refresh_files_tree_btn');
    var session = window.AGENT_SESSION;

    if (refreshTreeBtn && session) {
      refreshTreeBtn.addEventListener('click', function () {
        loadWorkspaceFiles(session.id);
      });
    }

    var modeRendered = document.getElementById('viewer_mode_rendered');
    var modeSource = document.getElementById('viewer_mode_source');
    var mdPreview = document.getElementById('viewer_md_preview');
    var codePreview = document.getElementById('viewer_code_preview');

    if (modeRendered && modeSource) {
      modeRendered.addEventListener('click', function () {
        modeRendered.classList.add('active');
        modeSource.classList.remove('active');
        if (mdPreview) mdPreview.hidden = false;
        if (codePreview) codePreview.hidden = true;
      });
      modeSource.addEventListener('click', function () {
        modeSource.classList.add('active');
        modeRendered.classList.remove('active');
        if (mdPreview) mdPreview.hidden = true;
        if (codePreview) codePreview.hidden = false;
      });
    }
  }

  function loadWorkspaceFiles(sessionId) {
    var container = document.getElementById('file_tree_container');
    if (!container) return;

    apiGet('/backgroundagent/ajax/sessions/' + sessionId + '/workspace-files/')
      .then(function (res) {
        if (res.ok && res.data.files) {
          container.innerHTML = '';
          if (!res.data.files.length) {
            container.innerHTML = '<div class="file-tree-loading">No workspace files found yet.</div>';
            return;
          }
          res.data.files.forEach(function (f) {
            var icon = f.is_md ? 'description' : 'code';
            var item = el('div', { class: 'file-tree-item', onclick: function () { openFileInViewer(f.path); } }, [
              el('span', { class: 'material-symbols-outlined' }, [icon]),
              el('span', null, [f.path])
            ]);
            container.appendChild(item);
          });
        } else {
          container.innerHTML = '<div class="file-tree-loading">Workspace initializing...</div>';
        }
      });
  }

  window.openFileInViewer = function (filePath) {
    var session = window.AGENT_SESSION;
    if (!session) return;

    var viewer = document.getElementById('inbuilt_file_viewer');
    var filenameLabel = document.getElementById('viewer_filename');
    var mdPreview = document.getElementById('viewer_md_preview');
    var codePreview = document.getElementById('viewer_code_preview');
    var imgPreview = document.getElementById('viewer_img_preview');

    if (!viewer) return;
    viewer.hidden = false;
    if (filenameLabel) filenameLabel.textContent = filePath;

    apiGet('/backgroundagent/ajax/sessions/' + session.id + '/file-content/?path=' + encodeURIComponent(filePath))
      .then(function (res) {
        if (!res.ok || !res.data) {
          showToast('Could not load file', 'error');
          return;
        }
        var data = res.data;
        if (data.is_image) {
          if (mdPreview) mdPreview.hidden = true;
          if (codePreview) codePreview.hidden = true;
          if (imgPreview) {
            imgPreview.hidden = false;
            imgPreview.querySelector('img').src = data.url;
          }
        } else if (data.is_md) {
          if (imgPreview) imgPreview.hidden = true;
          if (mdPreview) {
            mdPreview.hidden = false;
            mdPreview.innerHTML = renderSimpleMarkdown(data.content);
          }
          if (codePreview) {
            codePreview.hidden = true;
            codePreview.querySelector('code').textContent = data.content;
          }
        } else {
          if (imgPreview) imgPreview.hidden = true;
          if (mdPreview) mdPreview.hidden = true;
          if (codePreview) {
            codePreview.hidden = false;
            codePreview.querySelector('code').textContent = data.content;
          }
        }
      });
  };

  function loadSessionLogs(sessionId) {
    var termBody = document.getElementById('terminal_output_log');
    var vmLogsContainer = document.getElementById('vm_logs_container');

    apiGet('/backgroundagent/ajax/sessions/' + sessionId + '/logs/')
      .then(function (res) {
        if (res.ok && res.data.logs) {
          if (termBody) {
            var termText = "$ worker status: " + res.data.status + "\n$ branch: " + res.data.branch + "\n\n";
            res.data.logs.forEach(function (l) {
              termText += l.text + "\n---\n";
            });
            termBody.textContent = termText;
          }
        }
      });
  }

  function handleClick(ev) {
    var t = ev.target.closest('[data-action]');
    if (!t) return;
    var action = t.dataset.action;
    var id = t.dataset.sessionId || t.dataset.projectId;
    ev.preventDefault();
    switch (action) {
      case 'push-branch':
        showToast('Pushing branch...', 'info');
        apiPost('/backgroundagent/ajax/sessions/' + id + '/push/').then(function (r) {
          if (r.ok) showToast('Branch pushed successfully', 'success');
          else showToast(r.data.error || 'Push failed', 'error');
        });
        break;
      case 'open-pr':
        showToast('Opening pull request...', 'info');
        apiPost('/backgroundagent/ajax/sessions/' + id + '/pr/').then(function (r) {
          if (r.ok) showToast('Pull request #' + r.data.pr_number + ' opened', 'success');
          else showToast(r.data.error || 'PR failed', 'error');
        });
        break;
    }
  }

  function handleSubmit(ev) {
    if (ev.target.id === 'agent_chat_form') {
      ev.preventDefault();
      sendUserMessage();
    }
  }

  function sendUserMessage() {
    var input = document.getElementById('agent_chat_input');
    var session = window.AGENT_SESSION;
    if (!input || !session) return;
    var text = input.value.trim();
    if (!text && !currentAttachments.length) return;

    input.value = '';
    var attachmentsToSend = currentAttachments.slice();
    currentAttachments = [];
    renderAttachmentPreviews();

    apiPost('/backgroundagent/ajax/sessions/' + session.id + '/message/', {
      content: text,
      attachments: attachmentsToSend,
    }).then(function (r) {
      if (!r.ok) showToast(r.data.error || 'Send failed', 'error');
      else loadSessionLogs(session.id);
    });
  }

  function initSessionSocket() {
    var session = window.AGENT_SESSION;
    if (!session) return;
    var url = (window.WS_CONFIG && window.WS_CONFIG.url) || (window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/';
    try {
      var ws = new WebSocket(url);
      ws.onopen = function () {
        ws.send(JSON.stringify({ action: 'subscribe', channel: session.wsGroup }));
      };
      ws.onmessage = function (msg) {
        try {
          var data = JSON.parse(msg.data);
          if (data.event === 'agent.message_added' || data.event === 'agent.event') {
            loadSessionLogs(session.id);
            loadWorkspaceFiles(session.id);
          }
        } catch (e) {}
      };
    } catch (e) {}
  }

  init();
})();
