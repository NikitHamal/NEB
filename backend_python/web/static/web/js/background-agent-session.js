(function () {
  'use strict';
  var BA = window.BA;
  var root = BA.qs('#background-agent-session');
  if (!root) return;

  var state = { session: null, lastEvent: 0, messages: new Map(), files: [], activeFile: '', poll: null, detailTimer: null, diff: '', lifecycleAction: '' };
  var els = {
    title: BA.qs('#bs-title'), status: BA.qs('#bs-status-badge'), repoShort: BA.qs('#bs-repo-short'), branchShort: BA.qs('#bs-branch-short'),
    progressLabel: BA.qs('#bs-progress-label'), progressValue: BA.qs('#bs-progress-value'), progressBar: BA.qs('#bs-progress-bar'), updated: BA.qs('#bs-updated-label'),
    iteration: BA.qs('#bs-iteration-label'), contextBar: BA.qs('#bs-context-bar'), contextValue: BA.qs('#bs-context-value'), contextMeter: BA.qs('.ba-context-meter'),
    conversation: BA.qs('#bs-conversation'), pause: BA.qs('#bs-pause'), resume: BA.qs('#bs-resume'), stop: BA.qs('#bs-stop'), refresh: BA.qs('#bs-refresh'),
    followup: BA.qs('#bs-followup'), send: BA.qs('#bs-send'), attach: BA.qs('#bs-attach'), fileInput: BA.qs('#bs-file-input'), attachmentList: BA.qs('#bs-attachment-list'), followupWrap: BA.qs('#bs-followup-wrap'),
    fileCount: BA.qs('#bs-file-count'), diffSummary: BA.qs('#bs-diff-summary'), stackedDiff: BA.qs('#bs-stacked-diff'), copyDiff: BA.qs('#bs-copy-diff'),
    fileList: BA.qs('#bs-file-list'), fileSearch: BA.qs('#bs-file-search'), refreshFiles: BA.qs('#bs-refresh-files'), viewerIcon: BA.qs('#bs-viewer-icon'), viewerName: BA.qs('#bs-viewer-name'), viewerMeta: BA.qs('#bs-viewer-meta'), viewerContent: BA.qs('#bs-viewer-content'),
    downloads: BA.qs('#bs-download-actions'), push: BA.qs('#bs-push'), openPr: BA.qs('#bs-open-pr'), actions: BA.qs('#bs-action-history'), tests: BA.qs('#bs-test-summary'),
    more: BA.qs('#bs-more'), moreMenu: BA.qs('#bs-more-menu'), lifecycleDialog: BA.qs('#bs-lifecycle-dialog'), lifecycleTitle: BA.qs('#bs-lifecycle-title'),
    lifecycleCopy: BA.qs('#bs-lifecycle-copy'), lifecycleIcon: BA.qs('#bs-lifecycle-icon'), lifecycleCancel: BA.qs('#bs-lifecycle-cancel'), lifecycleConfirm: BA.qs('#bs-lifecycle-confirm')
  };
  var attachments = BA.createAttachmentController({ input: els.fileInput, list: els.attachmentList, dropZone: els.followupWrap });

  function terminal(status) { return ['completed', 'failed', 'cancelled'].includes(status); }
  function nearBottom() { return els.conversation.scrollHeight - els.conversation.scrollTop - els.conversation.clientHeight < 120; }
  function scrollBottom(force) { if (force || nearBottom()) requestAnimationFrame(function () { els.conversation.scrollTop = els.conversation.scrollHeight; }); }
  function statusLabel(value) { return String(value || 'queued').replace(/_/g, ' '); }
  function setButtonBusy(button, busy) {
    if (busy) { button.dataset.content = button.innerHTML; button.disabled = true; button.innerHTML = '<span class="ba-spinner"></span>'; }
    else { button.disabled = false; if (button.dataset.content) button.innerHTML = button.dataset.content; }
  }
  function updateSession(session) {
    var previousStatus = state.session && state.session.status;
    state.session = Object.assign({}, state.session || {}, session || {});
    var current = state.session;
    els.title.textContent = current.title || current.goal || 'Background task';
    els.status.className = 'ba-status-badge ' + current.status; els.status.textContent = statusLabel(current.status);
    els.repoShort.textContent = current.repoFullName || ''; els.branchShort.textContent = current.workBranch || current.sourceBranch || '';
    els.progressLabel.textContent = current.progressLabel || statusLabel(current.status);
    els.progressValue.textContent = Number(current.progress || 0) + '%'; els.progressBar.style.width = Number(current.progress || 0) + '%';
    els.updated.textContent = BA.timeAgo(current.updatedAt || current.createdAt);
    els.iteration.innerHTML = '<span class="material-symbols-outlined">repeat</span>Iteration ' + Number(current.iteration || 0);
    var context = current.context || {}; var percent = Number(context.percent || 0);
    els.contextBar.style.width = Math.min(100, percent) + '%'; els.contextValue.textContent = percent + '%';
    els.contextMeter.classList.toggle('warning', percent >= 65 && percent < 80); els.contextMeter.classList.toggle('danger', percent >= 80);
    els.contextMeter.title = 'Estimated context: ' + Number(context.estimatedTokens || 0).toLocaleString() + ' / ' + Number(context.windowTokens || 0).toLocaleString() + ' tokens · ' + Number(context.compactions || 0) + ' compactions';
    var active = ['queued', 'preparing', 'running'].includes(current.status);
    els.pause.hidden = !active; els.resume.hidden = !['paused', 'waiting', 'failed', 'completed'].includes(current.status); els.stop.disabled = terminal(current.status);
    if (current.testSummary) els.tests.textContent = current.testSummary;
    if (current.diff !== undefined && current.diff !== state.diff) { state.diff = current.diff || ''; renderDiff(); }
    if (current.changedFiles) els.fileCount.textContent = current.changedFiles.length;
    if (current.artifacts) renderArtifacts(current.artifacts);
    if (current.actions) renderActions(current.actions);
    if (current.summary && current.status === 'completed') renderSummary(current.summary);
    if (previousStatus !== current.status && current.status === 'completed') { loadDetail(); loadFiles(); }
    var lifecycleArchive = BA.qs('[data-session-action="archive"], [data-session-action="restore"]', els.moreMenu);
    var lifecycleDelete = BA.qs('[data-session-action="delete"]', els.moreMenu);
    if (lifecycleArchive) {
      lifecycleArchive.innerHTML = '<span class="material-symbols-outlined">' + (current.archived ? 'unarchive' : 'archive') + '</span>' + (current.archived ? 'Restore session' : 'Archive session');
      lifecycleArchive.dataset.sessionAction = current.archived ? 'restore' : 'archive';
      lifecycleArchive.disabled = active && !current.archived;
      lifecycleArchive.title = lifecycleArchive.disabled ? 'Stop this task before archiving it' : '';
    }
    if (lifecycleDelete) {
      lifecycleDelete.disabled = active;
      lifecycleDelete.title = active ? 'Stop this task before deleting it' : '';
    }
  }
  function renderSummary(summary) {
    var existing = BA.qs('[data-final-summary]', els.conversation);
    if (!existing) { existing = document.createElement('div'); existing.className = 'ba-summary-card'; existing.dataset.finalSummary = 'true'; existing.innerHTML = '<strong>Task completed</strong><p></p>'; els.conversation.appendChild(existing); }
    existing.querySelector('p').textContent = summary;
  }
  function messageNode(message) {
    if (message.role === 'tool') {
      var wrapper = document.createElement('div'); wrapper.className = 'ba-message tool';
      var detail = document.createElement('details'); detail.className = 'ba-tool-event ' + (message.metadata?.ok === false ? 'error' : 'ok');
      var summary = document.createElement('summary'); summary.innerHTML = '<span class="material-symbols-outlined">terminal</span><span class="ba-tool-label"></span><span class="ba-tool-state">' + (message.metadata?.ok === false ? 'Failed' : 'Done') + '</span>';
      summary.querySelector('.ba-tool-label').textContent = message.label || message.metadata?.tool || 'Tool result';
      var pre = document.createElement('pre');
      try { pre.textContent = JSON.stringify(JSON.parse(message.content), null, 2); } catch (error) { pre.textContent = message.content; }
      detail.append(summary, pre); wrapper.appendChild(detail); return wrapper;
    }
    var node = document.createElement('article'); node.className = 'ba-message ' + message.role;
    var avatar = document.createElement('div'); avatar.className = 'ba-message-avatar'; avatar.innerHTML = '<span class="material-symbols-outlined">' + (message.role === 'user' ? 'person' : 'smart_toy') + '</span>';
    var body = document.createElement('div'); body.className = 'ba-message-body';
    var head = document.createElement('div'); head.className = 'ba-message-head'; head.innerHTML = '<strong></strong><time></time>'; head.querySelector('strong').textContent = message.role === 'user' ? 'You' : 'Background Agent'; head.querySelector('time').textContent = BA.timeAgo(message.createdAt);
    var content = document.createElement('div'); content.className = 'ba-message-content'; content.innerHTML = BA.renderMarkdown(message.content || '');
    body.append(head, content);
    if (message.attachments && message.attachments.length) {
      var list = document.createElement('div'); list.className = 'ba-message-attachments';
      message.attachments.forEach(function (attachment) {
        var button = document.createElement('button'); button.type = 'button'; button.className = 'ba-message-attachment';
        button.innerHTML = '<span class="material-symbols-outlined">' + BA.fileIcon(attachment.name, attachment.kind) + '</span><div><strong></strong><small></small></div>';
        button.querySelector('strong').textContent = attachment.name; button.querySelector('small').textContent = BA.formatBytes(attachment.sizeBytes);
        button.addEventListener('click', function () { openReviewTab('files'); loadAttachment(attachment.id); }); list.appendChild(button);
      });
      body.appendChild(list);
    }
    node.append(avatar, body); return node;
  }
  function addMessage(message, initial) {
    if (!message || state.messages.has(String(message.id))) return;
    state.messages.set(String(message.id), message); var stick = initial || nearBottom(); els.conversation.appendChild(messageNode(message)); scrollBottom(stick);
  }
  function addEvent(event) {
    if (!event || Number(event.id || 0) <= state.lastEvent) return;
    state.lastEvent = Math.max(state.lastEvent, Number(event.id || 0));
    if (event.type === 'message.created' && event.payload?.message) { addMessage(event.payload.message, false); return; }
    if (['model.requested', 'model.retrying', 'model.format_retry', 'context.compacting', 'context.compacted', 'workspace.ready', 'session.paused', 'session.resumed', 'session.waiting', 'session.failed', 'session.cancelled'].includes(event.type)) {
      var node = document.createElement('div'); node.className = 'ba-system-event'; node.textContent = event.message || statusLabel(event.type); els.conversation.appendChild(node); scrollBottom(false);
    }
    if (event.type === 'tool.executed' || event.type === 'tool.failed') {
      var tool = event.payload?.tool || '';
      if (['write_file', 'edit_file', 'multi_edit', 'apply_patch', 'delete_file', 'copy_file', 'move_file', 'git_restore'].includes(tool)) scheduleDetailRefresh();
    }
    if (event.type === 'session.completed') scheduleDetailRefresh(true);
  }
  function renderDiff() {
    var files = BA.splitDiff(state.diff); els.stackedDiff.innerHTML = '';
    els.fileCount.textContent = files.length; els.diffSummary.textContent = files.length ? files.length + ' changed file' + (files.length === 1 ? '' : 's') : 'No changes yet';
    if (!files.length) { els.stackedDiff.innerHTML = '<div class="ba-empty-view"><span class="material-symbols-outlined">difference</span><p>Changes will appear here as the agent edits the workspace.</p></div>'; return; }
    files.forEach(function (file) {
      var card = document.createElement('article'); card.className = 'ba-diff-file';
      var header = document.createElement('header'); header.innerHTML = '<strong></strong><span class="ba-diff-stats"><i class="ba-diff-add"></i><i class="ba-diff-del"></i></span>'; header.querySelector('strong').textContent = file.path; header.querySelector('.ba-diff-add').textContent = '+' + file.added; header.querySelector('.ba-diff-del').textContent = '-' + file.removed;
      var lines = document.createElement('div'); lines.className = 'ba-diff-lines'; var number = 0;
      file.text.split('\n').forEach(function (line) {
        var row = document.createElement('div'); var type = 'meta';
        if (line.startsWith('+') && !line.startsWith('+++')) type = 'added'; else if (line.startsWith('-') && !line.startsWith('---')) type = 'removed'; else if (line.startsWith('@@')) type = 'hunk'; else if (!line.startsWith('diff ') && !line.startsWith('index ') && !line.startsWith('---') && !line.startsWith('+++')) type = '';
        row.className = 'ba-diff-line ' + type; if (!['meta', 'hunk'].includes(type)) number += 1;
        var num = document.createElement('span'); num.className = 'num'; num.textContent = ['meta', 'hunk'].includes(type) ? '' : number;
        var code = document.createElement('span'); code.className = 'code'; code.textContent = line || ' '; row.append(num, code); lines.appendChild(row);
      });
      card.append(header, lines); els.stackedDiff.appendChild(card);
    });
  }
  function renderArtifacts(artifacts) {
    els.downloads.innerHTML = '';
    [['changes_zip', 'Download ZIP'], ['patch', 'Download patch']].forEach(function (item) {
      var artifact = artifacts[item[0]]; if (!artifact) return;
      var link = document.createElement('a'); link.href = artifact.downloadUrl; link.textContent = item[1] + ' · ' + BA.formatBytes(artifact.sizeBytes); els.downloads.appendChild(link);
    });
    if (!els.downloads.children.length) els.downloads.textContent = 'Available when changes are ready';
  }
  function renderActions(actions) {
    els.actions.innerHTML = '';
    (actions || []).forEach(function (action) { var row = document.createElement('div'); row.className = 'ba-action-row'; row.textContent = action.action.replace('_', ' ') + ' · ' + action.status + (action.error ? ' · ' + action.error : ''); els.actions.appendChild(row); });
  }
  function openReviewTab(name) {
    BA.qsa('[data-review-tab]').forEach(function (button) { button.classList.toggle('active', button.dataset.reviewTab === name); });
    BA.qsa('.ba-review-panel').forEach(function (panel) { panel.classList.toggle('active', panel.id === 'bs-panel-' + name); });
    if (name === 'files' && !state.files.length) loadFiles();
  }
  async function loadFiles() {
    try { var data = await BA.api(root.dataset.filesUrl); state.files = data.files || []; renderFiles(); }
    catch (error) { els.fileList.innerHTML = '<div class="ba-empty-state"><p>' + BA.escapeHtml(error.message) + '</p></div>'; }
  }
  function renderFiles() {
    var query = els.fileSearch.value.trim().toLowerCase(); var files = state.files.filter(function (file) { return !query || file.path.toLowerCase().includes(query); });
    els.fileList.innerHTML = '';
    if (!files.length) { els.fileList.innerHTML = '<div class="ba-empty-state"><p>No files found.</p></div>'; return; }
    files.forEach(function (file) {
      var button = document.createElement('button'); button.type = 'button'; button.className = 'ba-file-row' + (state.activeFile === file.path ? ' active' : '');
      button.innerHTML = '<span class="material-symbols-outlined">' + BA.fileIcon(file.name, file.mode) + '</span><span></span>' + (file.changed ? '<i title="Changed"></i>' : ''); button.children[1].textContent = file.path;
      button.addEventListener('click', function () { loadWorkspaceFile(file.path); }); els.fileList.appendChild(button);
    });
  }
  async function loadWorkspaceFile(path) {
    state.activeFile = path; renderFiles(); await loadFilePayload(root.dataset.fileUrl + '?path=' + encodeURIComponent(path));
  }
  async function loadAttachment(id) { state.activeFile = ''; renderFiles(); await loadFilePayload(root.dataset.fileUrl + '?attachment=' + encodeURIComponent(id)); }
  async function loadFilePayload(url) {
    els.viewerContent.innerHTML = '<div class="ba-empty-view"><span class="ba-spinner"></span><p>Loading preview…</p></div>';
    try { var data = await BA.api(url); renderViewer(data.file); }
    catch (error) { els.viewerContent.innerHTML = '<div class="ba-empty-view"><span class="material-symbols-outlined">error</span><p>' + BA.escapeHtml(error.message) + '</p></div>'; }
  }
  function renderViewer(file) {
    els.viewerName.textContent = file.name || file.path; els.viewerMeta.textContent = BA.formatBytes(file.sizeBytes); els.viewerIcon.textContent = BA.fileIcon(file.name, file.mode); els.viewerContent.innerHTML = '';
    if (file.mode === 'markdown') { var md = document.createElement('article'); md.className = 'ba-markdown-view'; md.innerHTML = BA.renderMarkdown(file.content || ''); els.viewerContent.appendChild(md); }
    else if (file.mode === 'text') { var pre = document.createElement('pre'); pre.className = 'ba-code-view'; pre.textContent = file.content || ''; els.viewerContent.appendChild(pre); }
    else if (file.mode === 'image') { var imageWrap = document.createElement('div'); imageWrap.className = 'ba-image-view'; var img = document.createElement('img'); img.src = file.previewUrl; img.alt = file.name; imageWrap.appendChild(img); els.viewerContent.appendChild(imageWrap); }
    else if (file.mode === 'pdf') { var frame = document.createElement('iframe'); frame.className = 'ba-pdf-view'; frame.src = file.previewUrl; frame.title = file.name; els.viewerContent.appendChild(frame); }
    else if (file.mode === 'audio') { var audioWrap = document.createElement('div'); audioWrap.className = 'ba-media-view'; var audio = document.createElement('audio'); audio.controls = true; audio.preload = 'metadata'; audio.src = file.previewUrl; audioWrap.appendChild(audio); els.viewerContent.appendChild(audioWrap); }
    else if (file.mode === 'video') { var videoWrap = document.createElement('div'); videoWrap.className = 'ba-media-view'; var video = document.createElement('video'); video.controls = true; video.preload = 'metadata'; video.src = file.previewUrl; videoWrap.appendChild(video); els.viewerContent.appendChild(videoWrap); }
    else { var binary = document.createElement('div'); binary.className = 'ba-binary-view'; binary.innerHTML = '<span class="material-symbols-outlined">draft</span><p>This file type cannot be rendered in the browser.</p><a target="_blank" rel="noopener">Open file</a>'; binary.querySelector('a').href = file.previewUrl; els.viewerContent.appendChild(binary); }
    if (file.truncated) { var note = document.createElement('div'); note.className = 'ba-truncated-note'; note.textContent = 'Preview truncated for performance.'; els.viewerContent.appendChild(note); }
  }
  function openLifecycleDialog(action) {
    state.lifecycleAction = action;
    var deleting = action === 'delete';
    var restoring = action === 'restore';
    els.lifecycleIcon.textContent = deleting ? 'delete' : (restoring ? 'unarchive' : 'archive');
    els.lifecycleTitle.textContent = deleting ? 'Delete this session?' : (restoring ? 'Restore this session?' : 'Archive this session?');
    els.lifecycleCopy.textContent = deleting
      ? 'This permanently removes the task history, attachments, generated artifacts, and local worktree. This cannot be undone.'
      : (restoring ? 'The session will return to recent work.' : 'The session will move out of recent work without deleting its history or artifacts.');
    els.lifecycleConfirm.textContent = deleting ? 'Delete permanently' : (restoring ? 'Restore' : 'Archive');
    els.lifecycleConfirm.classList.toggle('ba-button-danger', deleting);
    els.lifecycleDialog.showModal();
  }
  async function applyLifecycle() {
    var actionName = state.lifecycleAction;
    if (!actionName) return;
    setButtonBusy(els.lifecycleConfirm, true);
    try {
      if (actionName === 'delete') {
        await BA.api(root.dataset.lifecycleUrl, { method: 'DELETE' });
        window.location.assign(root.dataset.dashboardUrl);
        return;
      }
      var data = await BA.json(root.dataset.lifecycleUrl, { action: actionName });
      updateSession(data.session);
      els.lifecycleDialog.close();
      BA.toast(actionName === 'restore' ? 'Session restored.' : 'Session archived.', 'success');
      if (actionName === 'archive') window.location.assign(root.dataset.dashboardUrl);
    } catch (error) {
      BA.toast(error.message, 'error');
    } finally {
      setButtonBusy(els.lifecycleConfirm, false);
      state.lifecycleAction = '';
    }
  }
  async function sendFollowup() {
    var content = els.followup.value.trim(); var files = attachments.files(); if (!content && !files.length) return;
    var form = new FormData(); form.append('content', content); form.append('resume', 'true'); files.forEach(function (file) { form.append('files', file, file.name); }); setButtonBusy(els.send, true);
    try { var data = await BA.api(root.dataset.messageUrl, { method: 'POST', body: form }); addMessage(data.message, false); els.followup.value = ''; attachments.clear(); await pollEvents(); }
    catch (error) { BA.toast(error.message, 'error'); } finally { setButtonBusy(els.send, false); }
  }
  async function control(command) { try { var data = await BA.json(root.dataset.controlUrl, { command: command }); updateSession(data.session); } catch (error) { BA.toast(error.message, 'error'); } }
  async function action(name, button) { setButtonBusy(button, true); try { await BA.json(root.dataset.actionUrl, { action: name }); BA.toast(name === 'open_pr' ? 'Pull request queued.' : 'Action queued.', 'success'); await pollEvents(); } catch (error) { BA.toast(error.message, 'error'); } finally { setButtonBusy(button, false); } }
  function scheduleDetailRefresh(immediate) { clearTimeout(state.detailTimer); state.detailTimer = setTimeout(function () { loadDetail(); loadFiles(); }, immediate ? 50 : 700); }
  async function loadDetail() {
    try {
      var data = await BA.api(root.dataset.detailUrl); var session = data.session;
      updateSession(session); (session.messages || []).forEach(function (message) { addMessage(message, true); });
      (session.events || []).forEach(addEvent); state.diff = session.diff || ''; renderDiff(); renderArtifacts(session.artifacts || {}); renderActions(session.actions || []);
      if (session.summary && session.status === 'completed') renderSummary(session.summary); scrollBottom(true);
    } catch (error) { BA.toast(error.message, 'error'); }
  }
  async function pollEvents() {
    try {
      var data = await BA.api(root.dataset.eventsUrl + '?after=' + state.lastEvent); updateSession(data.session); (data.events || []).forEach(addEvent); renderArtifacts(data.artifacts || {}); renderActions(data.actions || []);
    } catch (error) { if (error.status === 401 || error.status === 403) clearInterval(state.poll); }
  }

  BA.qsa('[data-review-tab]').forEach(function (button) { button.addEventListener('click', function () { openReviewTab(button.dataset.reviewTab); }); });
  els.more.addEventListener('click', function (event) { event.stopPropagation(); var opening = els.moreMenu.hidden; els.moreMenu.hidden = !opening; els.more.setAttribute('aria-expanded', opening ? 'true' : 'false'); });
  els.moreMenu.addEventListener('click', function (event) { var button = event.target.closest('[data-session-action]'); if (!button) return; els.moreMenu.hidden = true; els.more.setAttribute('aria-expanded', 'false'); openLifecycleDialog(button.dataset.sessionAction); });
  document.addEventListener('click', function (event) { if (!event.target.closest('.ba-session-command-menu-wrap')) { els.moreMenu.hidden = true; els.more.setAttribute('aria-expanded', 'false'); } });
  els.lifecycleCancel.addEventListener('click', function () { els.lifecycleDialog.close(); });
  els.lifecycleConfirm.addEventListener('click', applyLifecycle);
  els.lifecycleDialog.addEventListener('click', function (event) { if (event.target === els.lifecycleDialog) els.lifecycleDialog.close(); });
  els.pause.addEventListener('click', function () { control('pause'); }); els.resume.addEventListener('click', function () { control('resume'); }); els.stop.addEventListener('click', function () { if (window.confirm('Stop this task?')) control('stop'); });
  els.refresh.addEventListener('click', function () { loadDetail(); loadFiles(); }); els.attach.addEventListener('click', function () { els.fileInput.click(); }); els.send.addEventListener('click', sendFollowup);
  els.followup.addEventListener('keydown', function (event) { if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') { event.preventDefault(); sendFollowup(); } });
  els.copyDiff.addEventListener('click', async function () { try { await navigator.clipboard.writeText(state.diff || ''); BA.toast('Diff copied.', 'success'); } catch (error) { BA.toast('Could not copy the diff.', 'error'); } });
  els.refreshFiles.addEventListener('click', loadFiles); els.fileSearch.addEventListener('input', renderFiles); els.push.addEventListener('click', function () { action('push', els.push); }); els.openPr.addEventListener('click', function () { action('open_pr', els.openPr); });

  loadDetail().then(loadFiles); state.poll = setInterval(pollEvents, 2500); setInterval(function () { if (!document.hidden) loadDetail(); }, 15000);
})();
