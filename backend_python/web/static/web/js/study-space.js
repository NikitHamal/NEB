(function () {
  'use strict';

  var SPACE_ID = null;
  var SPACE_DATA = null;
  var SUMMARY_MODE = 'compact';
  var CURRENT_TAB = 'summary';
  var QUIZ_DATA = null;
  var QUIZ_ANSWERS = {};
  var QUIZ_CURRENT = 0;
  var FLASHCARDS = [];
  var FLASH_INDEX = 0;
  var MINDMAP_DATA = null;
  var PRESENCE_SESSION = 'ss-' + Math.random().toString(36).slice(2);
  var PRESENCE_TIMER = null;
  var NOTES_SAVE_TIMER = null;
  var SSYJS_INST = null;
  var EXAM_ACTIVE = false;
  var EXAM_DEADLINE = 0;
  var EXAM_TIMER = null;
  var GENERATION_POLL_INTERVAL = 2000;
  var GENERATION_POLLS = {};

  function csrf() {
    return document.querySelector('meta[name="csrf-token"]')?.content ||
      document.cookie.split('csrftoken=').pop()?.split(';')[0] || '';
  }

  function toast(msg) {
    if (typeof window.showSnackbar === 'function') window.showSnackbar(msg);
    else alert(msg);
  }

  function esc(t) {
    var d = document.createElement('div'); d.textContent = t; return d.innerHTML;
  }

  function pollGenerationJob(jobId, onProgress, onCompleted, onFailed) {
    if (GENERATION_POLLS[jobId]) return;
    var poll = function () {
      fetch('/ajax/study-space/generation/' + jobId + '/', {
        headers: { 'X-CSRFToken': csrf() },
        credentials: 'same-origin'
      }).then(function (r) { return r.json() }).then(function (data) {
        if (data.status === 'completed') {
          delete GENERATION_POLLS[jobId];
          if (onCompleted) onCompleted(data);
        } else if (data.status === 'failed' || data.status === 'cancelled') {
          delete GENERATION_POLLS[jobId];
          if (onFailed) onFailed(data.error || 'Generation failed');
        } else if (data.status === 'processing' || data.status === 'queued') {
          if (onProgress) onProgress(data.progress || 0, data.status === 'queued' ? 'Waiting in queue...' : 'Generating...');
          GENERATION_POLLS[jobId] = setTimeout(poll, GENERATION_POLL_INTERVAL);
        } else {
          delete GENERATION_POLLS[jobId];
          if (onFailed) onFailed('Unexpected status: ' + (data.status || 'unknown'));
        }
      }).catch(function (e) {
        delete GENERATION_POLLS[jobId];
        if (onFailed) onFailed('Connection error. Please try again.');
      });
    };
    GENERATION_POLLS[jobId] = setTimeout(poll, GENERATION_POLL_INTERVAL);
  }

  function cancelAllGenerationPolls() {
    Object.keys(GENERATION_POLLS).forEach(function (k) {
      clearTimeout(GENERATION_POLLS[k]);
    });
    GENERATION_POLLS = {};
  }

  function $(id) { return document.getElementById(id); }
  function $$(sel) { return document.querySelectorAll(sel); }

  function init() {
    var el = $('ssTitle');
    if (!el) return;
    SPACE_ID = el.dataset.spaceId || window.location.pathname.split('/')[2];
    if (!SPACE_ID) return;
    initTabOverflowHint();
    loadSpace();
  }

  // Show/hide the fade hint at the right edge of the tab bar when it
  // overflows (mobile affordance for off-screen tabs).
  function initTabOverflowHint() {
    var wrap = $('ssTabsWrap');
    var tabs = $('ssTabs');
    if (!wrap || !tabs) return;
    function update() {
      var overflowing = tabs.scrollWidth > tabs.clientWidth + 2;
      var atEnd = tabs.scrollLeft + tabs.clientWidth >= tabs.scrollWidth - 4;
      wrap.classList.toggle('ss-tabs-overflow', overflowing && !atEnd);
    }
    tabs.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  function loadSpace() {
    fetch('/ajax/study-space/' + SPACE_ID + '/', { headers: { 'X-CSRFToken': csrf(), 'Accept': 'application/json' } })
      .then(function (r) { return r.json() })
      .then(function (data) {
        SPACE_DATA = data;
        renderFiles();
        renderLinkedGen();
        renderMembers();
        renderPresence();
        renderAnalytics();
        hydrateNotes();
        loadExistingContent();
        loadSavedFlashcards();
        loadSavedQuiz();
        loadQuizHistory();
        loadSavedLearningPlan();
        startPresenceLoop();
      })
      .catch(function (e) { console.error('Failed to load space:', e); });
  }

  function renderFiles() {
    var list = $('ssFileList');
    if (!list) return;
    var docs = SPACE_DATA.documents || [];
    if (!docs.length) {
      list.innerHTML = '<div style="text-align:center;padding:12px;color:var(--md-on-surface-variant);font-size:0.8125rem;">No documents yet</div>';
      return;
    }
    var html = '';
    var needsParse = [];
    docs.forEach(function (d) {
      var icon, statusLabel = '', statusClass = '';
      var ps = d.parseStatus || 'pending';
      if (ps === 'pending') {
        icon = 'hourglass_top'; statusLabel = 'Preparing...'; statusClass = 'ss-file-status-parsing';
        needsParse.push(d.id);
      } else if (ps === 'uploading' || ps === 'parsing' || ps === 'extracting') {
        icon = 'hourglass_top'; statusLabel = 'Parsing...'; statusClass = 'ss-file-status-parsing';
      } else if (ps === 'failed') {
        icon = 'error'; statusLabel = 'Parse failed'; statusClass = 'ss-file-status-failed';
      } else if (ps === 'ready') {
        icon = 'description'; statusLabel = ''; statusClass = 'ss-file-status-ready';
      } else {
        icon = 'description'; statusLabel = ''; statusClass = '';
      }
      html += '<div class="ss-file-item' + (statusClass ? ' ' + statusClass : '') + '" data-doc-id="' + d.id + '" data-parse-status="' + ps + '">'
        + '<span class="material-symbols-outlined ss-file-icon">' + icon + '</span>'
        + '<div class="ss-file-info">'
        + '<span class="ss-file-name">' + esc(d.title || d.fileName || 'Untitled') + '</span>'
        + (statusLabel ? '<span class="ss-file-status-text">' + statusLabel + '</span>' : '')
        + (ps === 'failed' ? '<button class="ss-file-retry-btn" data-action="ss-retry-parse" data-doc-id="' + d.id + '" title="Retry parsing"><span class="material-symbols-outlined">refresh</span></button>' : '')
        + (ps === 'pending' ? '<button class="ss-file-retry-btn" data-action="ss-retry-parse" data-doc-id="' + d.id + '" title="Start parsing"><span class="material-symbols-outlined">play_arrow</span></button>' : '')
        + '</div>'
        + '<button class="ss-file-remove" data-action="ss-remove-doc" data-doc-id="' + d.id + '" title="Remove"><span class="material-symbols-outlined">close</span></button>'
        + '</div>';
    });
    list.innerHTML = html;
    // Auto-trigger parse for pending docs
    if (needsParse.length) {
      needsParse.forEach(function (id) { retryParse(id); });
    }
    // Start polling for docs still parsing
    _pollParsingDocs();
  }

  function renderLinkedGen() {
    var section = $('ssLinkedGen');
    if (!section) return;
    var docs = SPACE_DATA.documents || [];
    section.style.display = docs.length ? '' : 'none';
  }

  function renderMemberList(targetId, manage) {
    var list = $(targetId);
    if (!list || !SPACE_DATA) return;
    var members = SPACE_DATA.members || [];
    if (!members.length) { list.innerHTML = '<div style="color:var(--md-on-surface-variant);font-size:.8125rem;">Only you for now</div>'; return; }
    list.innerHTML = members.map(function (m) {
      var avatar = m.photoUrl ? '<img src="' + esc(m.photoUrl) + '" alt="">' : esc((m.displayName || m.username || '?').charAt(0).toUpperCase());
      var actions = '';
      if (manage && SPACE_DATA.isOwner && m.role !== 'owner') {
        actions = '<span class="ss-member-actions"><select class="ss-member-role-select" data-member-id="' + m.id + '">'
          + '<option value="member" ' + (m.role === 'member' ? 'selected' : '') + '>Member</option>'
          + '<option value="moderator" ' + (m.role === 'moderator' ? 'selected' : '') + '>Moderator</option>'
          + '<option value="admin" ' + (m.role === 'admin' ? 'selected' : '') + '>Admin</option>'
          + '</select>'
          + '<button class="ss-member-remove" data-action="ss-remove-member" data-member-id="' + m.id + '">Remove</button></span>';
      }
      return '<div class="ss-member-item"><span class="ss-member-avatar">' + avatar + '</span>'
        + '<span class="ss-member-info"><span class="ss-member-name">' + esc(m.displayName || m.username) + '</span><span class="ss-member-role">' + esc(m.role) + '</span></span>'
        + actions + '</div>';
    }).join('');
  }

  function renderMembers() {
    renderMergedMemberList('ssMemberList', false);
    renderMemberList('ssShareMembers', true);
    renderMemberList('ssMembersModalList', true);
  }

  function renderPresence() {
    renderMembers();
  }

  function renderMergedMemberList(targetId, manage) {
    var list = $(targetId);
    if (!list || !SPACE_DATA) return;
    var members = SPACE_DATA.members || [];
    var presence = SPACE_DATA.presence || [];
    var onlineMap = {};
    presence.forEach(function (p) { onlineMap[p.username] = p; });
    var onlineCount = presence.length;
    var countEl = $('ssActiveNowCount');
    if (countEl) countEl.textContent = onlineCount > 0 ? onlineCount + ' online' : '';
    if (!members.length) { list.innerHTML = '<div style="color:var(--md-on-surface-variant);font-size:.8125rem;">Only you for now</div>'; return; }
    var sorted = members.slice().sort(function (a, b) {
      var aOn = onlineMap[a.username] ? 1 : 0;
      var bOn = onlineMap[b.username] ? 1 : 0;
      return bOn - aOn;
    });
    list.innerHTML = sorted.map(function (m) {
      var avatar = m.photoUrl ? '<img src="' + esc(m.photoUrl) + '" alt="">' : esc((m.displayName || m.username || '?').charAt(0).toUpperCase());
      var online = onlineMap[m.username];
      var dot = online ? '<span class="ss-live-dot"></span>' : '';
      var detail = '';
      if (online && online.detail) {
        detail = '<span class="ss-member-activity">' + esc(online.detail) + '</span>';
      } else if (online) {
        detail = '<span class="ss-member-activity">Inside</span>';
      }
      var actions = '';
      if (manage && SPACE_DATA.isOwner && m.role !== 'owner') {
        actions = '<span class="ss-member-actions"><select class="ss-member-role-select" data-member-id="' + m.id + '">'
          + '<option value="member" ' + (m.role === 'member' ? 'selected' : '') + '>Member</option>'
          + '<option value="moderator" ' + (m.role === 'moderator' ? 'selected' : '') + '>Moderator</option>'
          + '<option value="admin" ' + (m.role === 'admin' ? 'selected' : '') + '>Admin</option>'
          + '</select>'
          + '<button class="ss-member-remove" data-action="ss-remove-member" data-member-id="' + m.id + '">Remove</button></span>';
      }
      return '<div class="ss-member-item' + (online ? ' ss-member-online' : '') + '"><span class="ss-member-avatar">' + dot + avatar + '</span>'
        + '<span class="ss-member-info"><span class="ss-member-name">' + esc(m.displayName || m.username) + '</span><span class="ss-member-role">' + esc(m.role) + (detail ? ' · ' : '. ') + detail + '</span></span>'
        + actions + '</div>';
    }).join('');
  }

  function renderAnalytics() {
    var grid = $('ssAnalyticsGrid');
    if (!grid || !SPACE_DATA || !SPACE_DATA.analytics) return;
    var a = SPACE_DATA.analytics;
    var cards = [
      ['Active now', a.activeNow || 0],
      ['Members', a.memberCount || 0],
      ['Documents', a.docCount || 0],
      ['Quizzes created', a.quizCount || 0],
      ['Quiz attempts', a.attemptCount || 0],
      ['Avg quiz completion', (a.avgQuizCompletion || 0) + '%'],
      ['Flashcards', a.flashcardCount || 0],
      ['Reviews done', a.reviewsCount || 0],
      ['Due flashcards', a.dueFlashcards || 0],
      ['Resource views (est.)', a.resourceViews || 0]
    ];
    grid.innerHTML = cards.map(function (c) {
      return '<div class="ss-kpi"><div class="ss-kpi-label">' + esc(c[0]) + '</div><div class="ss-kpi-value">' + esc(String(c[1])) + '</div></div>';
    }).join('');
  }

  function hydrateNotes() {
    if (SSYJS_INST) return;
    var ta = $('ssNotesTextarea');
    if (!ta || !SPACE_DATA || !SPACE_DATA.note) return;
    ta.value = SPACE_DATA.note.content || '';
  }

  function loadSavedFlashcards() {
    if (!SPACE_DATA || !SPACE_DATA.flashcards || !SPACE_DATA.flashcards.length) return;
    FLASHCARDS = SPACE_DATA.flashcards;
    FLASH_INDEX = 0;
  }

  function loadSavedQuiz() {
    if (!SPACE_DATA || !SPACE_DATA.quizzes || !SPACE_DATA.quizzes.length) return;
    var latest = SPACE_DATA.quizzes[0];
    fetch('/ajax/study-space/quiz/' + latest.id + '/', { headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.json() })
      .then(function (data) {
        if (data && data.quiz && data.quiz.questions && data.quiz.questions.length) {
          QUIZ_DATA = data.quiz;
          QUIZ_ANSWERS = {};
          QUIZ_CURRENT = 0;
        }
      }).catch(function () { });
  }

  function loadExistingContent() {
    if (SPACE_DATA.linkSummaryCompact || SPACE_DATA.linkSummaryDetailed) {
      // Default to the mode that actually has content (compact preferred).
      SUMMARY_MODE = SPACE_DATA.linkSummaryCompact ? 'compact' : 'detailed';
      syncSummaryModeButtons();
    }
    renderSummaryPanel();
    if (SPACE_DATA.linkMindmapJson) {
      try {
        MINDMAP_DATA = JSON.parse(SPACE_DATA.linkMindmapJson);
        showMindmap(MINDMAP_DATA);
      } catch (e) { }
    }
  }

  function summaryTextForMode() {
    if (!SPACE_DATA) return '';
    return SUMMARY_MODE === 'detailed' ? (SPACE_DATA.linkSummaryDetailed || '') : (SPACE_DATA.linkSummaryCompact || '');
  }

  function syncSummaryModeButtons() {
    $$('.ss-mode-btn').forEach(function (b) {
      b.classList.toggle('ss-mode-active', b.dataset.mode === SUMMARY_MODE);
    });
    var label = $('ssSummaryGenerateLabel');
    if (label) label.textContent = SUMMARY_MODE === 'detailed' ? 'Generate Detailed Summary' : 'Generate Compact Summary';
    var promptText = $('ssSummaryPromptText');
    if (promptText) promptText.textContent = SUMMARY_MODE === 'detailed'
      ? 'Generate a detailed, comprehensive summary from all documents.'
      : 'Generate a compact, high-yield summary from all documents.';
  }

  // Render the summary panel for the current mode: shows the saved text if
  // it exists, or the generate prompt for this mode otherwise.
  function renderSummaryPanel() {
    var text = summaryTextForMode();
    var editor = $('ssSummaryEditor');
    if (editor) editor.style.display = 'none';
    if (text) {
      showSummary(text);
    } else {
      $('ssSummaryContent').style.display = 'none';
      $('ssSummaryPrompt').style.display = '';
      var meta = $('ssSummaryMeta');
      if (meta) meta.textContent = '';
    }
  }

  // ── Tab switching ──
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-action]');
    if (!el) return;
    var action = el.getAttribute('data-action');

    switch (action) {
      case 'ss-switch-tab':
        switchTab(el.dataset.tab);
        break;
      case 'ss-summary-mode':
        SUMMARY_MODE = el.dataset.mode;
        syncSummaryModeButtons();
        renderSummaryPanel();
        break;
      case 'ss-generate-summary':
        generateSummary();
        break;
      case 'ss-edit-summary':
        // Edit the RAW markdown source (not rendered DOM text, which would
        // destroy LaTeX/markdown on save).
        $('ssSummaryEditor').style.display = 'block';
        $('ssSummaryText').style.display = 'none';
        $('ssSummaryTextarea').value = summaryTextForMode();
        break;
      case 'ss-save-summary':
        saveSummary();
        break;
      case 'ss-cancel-summary-edit':
        $('ssSummaryEditor').style.display = 'none';
        $('ssSummaryText').style.display = '';
        break;
      case 'ss-regenerate-summary':
        generateSummary();
        break;
      case 'ss-generate-mindmap':
        generateMindmap();
        break;
      case 'ss-regenerate-mindmap':
        generateMindmap();
        break;
      case 'ss-generate-quiz':
      case 'ss-gen-linked-quiz':
        switchTab('quiz');
        generateQuiz();
        break;
      case 'ss-generate-flashcards':
      case 'ss-gen-linked-flashcards':
        switchTab('flashcards');
        generateFlashcards();
        break;
      case 'ss-gen-linked-summary':
        switchTab('summary');
        generateSummary();
        break;
      case 'ss-gen-linked-mindmap':
        switchTab('mindmap');
        generateMindmap();
        break;
      case 'ss-count-choice':
        selectCountChoice(el);
        break;
      case 'ss-quiz-select':
        selectQuizAnswer(el);
        break;
      case 'ss-upload-file':
        $('ssFileInput').click();
        break;
      case 'ss-select-doc':
        openDocSelectModal();
        break;
      case 'ss-remove-doc':
        removeDoc(el.dataset.docId);
        break;
      case 'ss-retry-parse':
        retryParse(el.dataset.docId);
        break;
      case 'ss-close-select-doc':
        $('ssSelectDocModal').style.display = 'none';
        break;
      case 'cb-zoom-out':
        if (typeof CollabBoard !== 'undefined') CollabBoard.zoomOut();
        break;
      case 'cb-zoom-in':
        if (typeof CollabBoard !== 'undefined') CollabBoard.zoomIn();
        break;
      case 'cb-zoom-fit':
        if (typeof CollabBoard !== 'undefined') CollabBoard.zoomFit();
        break;
      case 'cb-file-tab':
        if (typeof CollabBoard !== 'undefined') CollabBoard.switchFileTab(el.dataset.tab);
        break;
      case 'cb-close-file-picker':
        var cbModal = $('cbFilePickerModal');
        if (cbModal) cbModal.style.display = 'none';
        break;
      case 'cb-trigger-local-upload':
        var cbInput = $('cbLocalFileInput');
        if (cbInput) cbInput.click();
        break;
      case 'cb-select-file':
        if (typeof CollabBoard !== 'undefined') {
          CollabBoard.selectFileItem(
            el.dataset.id,
            el.dataset.type,
            el.dataset.title,
            el.dataset.url,
            el.dataset.size
          );
        }
        break;
      case 'ss-submit-select-doc':
        submitDocSelection();
        break;
      case 'ss-share':
        openShareModal();
        break;
      case 'ss-open-members':
        $('ssMembersModal').style.display = 'flex';
        renderMembers();
        break;
      case 'ss-close-members':
        $('ssMembersModal').style.display = 'none';
        break;
      case 'ss-open-settings':
        openSettingsModal();
        break;
      case 'ss-close-settings':
        $('ssSettingsModal').style.display = 'none';
        break;
      case 'ss-save-settings':
        saveSettings();
        break;
      case 'ss-close-share':
        $('ssShareModal').style.display = 'none';
        break;
      case 'ss-copy-share-link':
        copyShareLink();
        break;
      case 'ss-save-share':
        saveShare();
        break;
      case 'ss-save-notes':
        saveNotes(true);
        break;
      case 'ss-ask-tutor':
        askTutor();
        break;
      case 'ss-generate-learning-path':
        generateLearningPath();
        break;
      case 'ss-start-exam-mode':
        startExamMode();
        break;
      case 'ss-exam-stop':
        stopExamTimer();
        toast('Exam mode ended. You can keep answering without the timer.');
        break;
      case 'ss-toggle-sidebar':
        toggleMobileSidebar();
        break;
      case 'ss-remove-member':
        removeMember(el.dataset.memberId);
        break;
      case 'ss-rename':
        openRenameModal();
        break;
      case 'ss-close-rename':
        $('ssRenameModal').style.display = 'none';
        break;
      case 'ss-submit-rename':
        submitRename();
        break;
      case 'ss-delete-space':
        $('ssDeleteModal').style.display = 'flex';
        break;
      case 'ss-close-delete':
        $('ssDeleteModal').style.display = 'none';
        break;
      case 'ss-confirm-delete':
        deleteSpace();
        break;
      // Mindmap zoom
      case 'ss-mm-zoom-in':
        if (window.NEBiansMindmap && $('ssMindmapTree')) window.NEBiansMindmap.setZoom($('ssMindmapTree'), 0.12, MINDMAP_DATA);
        break;
      case 'ss-mm-zoom-out':
        if (window.NEBiansMindmap && $('ssMindmapTree')) window.NEBiansMindmap.setZoom($('ssMindmapTree'), -0.12, MINDMAP_DATA);
        break;
      case 'ss-mm-fit':
        if (window.NEBiansMindmap && $('ssMindmapTree')) window.NEBiansMindmap.fitView($('ssMindmapTree'), MINDMAP_DATA);
        break;
      case 'ss-mm-export':
        if (window.NEBiansMindmap && $('ssMindmapTree')) window.NEBiansMindmap.downloadPng($('ssMindmapTree'));
        break;
      // Flashcard navigation
      case 'ss-flash-prev':
        flashNav(-1);
        break;
      case 'ss-flash-next':
        flashNav(1);
        break;
      case 'ss-flip-card':
        var card = el.closest('.sl-flash-card');
        if (card) card.classList.toggle('sl-flash-flipped');
        break;
      case 'ss-flash-confidence':
        flashConfidence(el.dataset.level);
        break;
      case 'ss-flash-more':
        generateFlashcards();
        break;
      // Quiz navigation
      case 'ss-quiz-prev':
        quizNav(-1);
        break;
      case 'ss-quiz-next':
        quizNav(1);
        break;
      case 'ss-quiz-submit':
        submitQuiz();
        break;
      case 'ss-quiz-retake':
        retakeQuiz();
        break;
      case 'ss-quiz-new':
        generateQuiz();
        break;
      case 'ss-load-past-quiz':
        loadPastQuiz(el.dataset.quizId);
        break;
    }
  });

  // ── Share modal radio toggle ──
  document.addEventListener('change', function (e) {
    if (e.target.name === 'ssShareMode') {
      $('ssShareSpecific').style.display = e.target.value === 'specific' ? 'block' : 'none';
    }
    if (e.target.classList && e.target.classList.contains('ss-member-role-select')) {
      updateMemberRole(e.target.dataset.memberId, e.target.value);
    }
  });

  // ── Upload ──
  document.addEventListener('DOMContentLoaded', function () {
    var fi = $('ssFileInput');
    if (fi) fi.addEventListener('change', function () {
      if (this.files.length) uploadFile(this.files[0]);
      this.value = '';
    });
    var notes = $('ssNotesTextarea');
    if (notes) {
      notes.addEventListener('input', function () {
        if (NOTES_SAVE_TIMER) clearTimeout(NOTES_SAVE_TIMER);
        sendPresence('typing', 'editing shared notes', true);
        NOTES_SAVE_TIMER = setTimeout(function () { saveNotes(false); }, 2000);
      });
    }
  });
  window.addEventListener('beforeunload', function () {
    if (SSYJS_INST) SSYJS_INST.disconnect();
    try { navigator.sendBeacon('/ajax/study-space/' + SPACE_ID + '/presence/', new Blob([JSON.stringify({ status: 'idle', currentTab: CURRENT_TAB, isTyping: false, sessionId: PRESENCE_SESSION })], { type: 'application/json' })); } catch (e) { }
  });

  function uploadFile(file) {
    $('ssUploadProgress').style.display = 'flex';
    $('ssUploadProgressBar').style.width = '0%';
    $('ssUploadProgressPercent').textContent = '0%';
    $('ssUploadProgressSubtitle').textContent = 'Uploading ' + file.name + '...';
    var fd = new FormData();
    fd.append('file', file);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/ajax/study-space/' + SPACE_ID + '/upload/');
    xhr.setRequestHeader('X-CSRFToken', csrf());
    xhr.upload.onprogress = function (e) {
      if (e.lengthComputable) {
        var pct = Math.round(e.loaded / e.total * 100);
        $('ssUploadProgressBar').style.width = pct + '%';
        $('ssUploadProgressPercent').textContent = pct + '%';
      }
    };
    xhr.onload = function () {
      $('ssUploadProgress').style.display = 'none';
      if (xhr.status >= 200 && xhr.status < 300) {
        loadSpace();
      } else {
        try { var d = JSON.parse(xhr.responseText); toast(d.error || 'Upload failed'); } catch (e) { toast('Upload failed'); }
      }
    };
    xhr.onerror = function () {
      $('ssUploadProgress').style.display = 'none';
      toast('Upload failed — network error');
    };
    xhr.send(fd);
  }

  function removeDoc(docId) {
    if (!confirm('Remove this document from the space?')) return;
    fetch('/ajax/study-space/' + SPACE_ID + '/document/' + docId + '/remove/', {
      method: 'POST', headers: { 'X-CSRFToken': csrf(), 'Content-Type': 'application/json' }
    }).then(function (r) { return r.json() })
      .then(function (data) {
        if (data.error) toast(data.error);
        else loadSpace();
      });
  }

  // ── Parse status polling ──
  var PARSE_POLL_TIMER = null;

  function _pollParsingDocs() {
    if (PARSE_POLL_TIMER) clearTimeout(PARSE_POLL_TIMER);
    var docs = SPACE_DATA.documents || [];
    var parsingIds = [];
    docs.forEach(function (d) {
      var ps = d.parseStatus || 'pending';
      if (ps === 'uploading' || ps === 'parsing' || ps === 'extracting') parsingIds.push(d.id);
    });
    if (!parsingIds.length) return;
    PARSE_POLL_TIMER = setTimeout(function () {
      Promise.all(parsingIds.map(function (id) {
        return fetch('/ajax/study-space/' + SPACE_ID + '/document/' + id + '/parse-status/', { headers: { 'X-CSRFToken': csrf(), 'Accept': 'application/json' } })
          .then(function (r) { return r.json(); })
          .then(function (data) {
            // Update local data
            var doc = (SPACE_DATA.documents || []).find(function (d) { return d.id === id; });
            if (doc && data.status) {
              doc.parseStatus = data.status;
              if (data.error) doc.parseError = data.error;
            }
            return data;
          });
      })).then(function () {
        renderFiles();
        renderLinkedGen();
        // Keep polling if any still parsing
        var stillParsing = (SPACE_DATA.documents || []).filter(function (d) {
          var ps = d.parseStatus || 'pending';
          return ps === 'uploading' || ps === 'parsing' || ps === 'extracting';
        });
        if (stillParsing.length) _pollParsingDocs();
      });
    }, 3000);
  }

  function showParseStatusMessage(msg) {
    var existing = document.getElementById('ssParseStatusMsg');
    if (existing) { existing.remove(); }
    var el = document.createElement('div');
    el.id = 'ssParseStatusMsg';
    el.className = 'ss-status-msg';
    el.innerHTML = '<span class="material-symbols-outlined">hourglass_top</span>' + esc(msg);
    var panel = $('ssTabSummary') || $('ssSummaryPrompt');
    if (panel) panel.parentNode.insertBefore(el, panel.nextSibling);
    setTimeout(function () { if (el.parentNode) el.remove(); }, 8000);
  }

  function retryParse(docId) {
    fetch('/ajax/study-space/' + SPACE_ID + '/document/' + docId + '/reparse/?force=true', {
      method: 'POST', headers: { 'X-CSRFToken': csrf(), 'Content-Type': 'application/json' }
    }).then(function (r) { return r.json(); })
      .then(function (data) {
        if (data.error) toast(data.error);
        else loadSpace();
      });
  }

  // ── Yjs CRDT collaborative board ──
  function initCollabNotes() {
    if (SSYJS_INST) return;
    if (typeof Y === 'undefined' || typeof SSYjs === 'undefined' || typeof CollabBoard === 'undefined') return;
    if (!SPACE_DATA) return;
    var initial = SPACE_DATA.note ? SPACE_DATA.note.content || '' : '';
    var userName = SPACE_DATA.currentUser ? (SPACE_DATA.currentUser.displayName || SPACE_DATA.currentUser.username) : 'Anonymous';
    var bridge = new SSYjs();
    bridge.init(SPACE_ID, '', userName);
    CollabBoard.init(SPACE_ID, bridge, initial);
    SSYJS_INST = bridge;
  }

  function destroyCollabNotes() {
    if (SSYJS_INST) {
      CollabBoard.destroy();
      SSYJS_INST.disconnect();
      SSYJS_INST = null;
    }
  }

  // ── Tab switching ──
  function switchTab(tab) {
    CURRENT_TAB = tab;
    // Close mobile drawer when navigating
    var sidebar = $('ssSidebar');
    if (sidebar && sidebar.classList.contains('ss-sidebar-mobile-open')) {
      sidebar.classList.remove('ss-sidebar-mobile-open');
      var scrim = $('ssSidebarScrim');
      if (scrim) scrim.classList.remove('ss-sidebar-scrim-open');
    }
    $$('.ss-tab').forEach(function (t) { t.classList.toggle('ss-tab-active', t.dataset.tab === tab); });
    $$('.ss-tab-content').forEach(function (c) { c.classList.remove('ss-tab-content-active'); });
    var panel = $('ssTab' + tab.charAt(0).toUpperCase() + tab.slice(1));
    if (panel) panel.classList.add('ss-tab-content-active');
    if (tab === 'notes') { initCollabNotes(); }
    else { destroyCollabNotes(); }
    if (tab === 'quiz' && QUIZ_DATA && QUIZ_DATA.questions && QUIZ_DATA.questions.length) {
      $('ssQuizPrompt').style.display = 'none';
      $('ssQuizLoading').style.display = 'none';
      renderQuiz();
    } else if (tab === 'quiz') {
      $('ssQuizPrompt').style.display = '';
      $('ssQuizActive').style.display = 'none';
      $('ssQuizResults').style.display = 'none';
      var qHint = $('ssQuizKeyHint');
      if (qHint) qHint.style.display = 'none';
    }
    if (tab === 'flashcards' && FLASHCARDS && FLASHCARDS.length) {
      $('ssFlashPrompt').style.display = 'none';
      $('ssFlashLoading').style.display = 'none';
      $('ssFlashDeck').style.display = 'block';
      renderFlashcard();
    } else if (tab === 'flashcards') {
      $('ssFlashPrompt').style.display = '';
      $('ssFlashDeck').style.display = 'none';
      var fHint = $('ssFlashKeyHint');
      if (fHint) fHint.style.display = 'none';
    }
    if (tab === 'analytics') renderAnalytics();
    sendPresence(activityStatus(), activityDetail(), false);
  }

  function selectCountChoice(el) {
    var picker = el.closest('.ss-count-picker');
    if (!picker) return;
    picker.querySelectorAll('.ss-count-choice').forEach(function (b) { b.classList.remove('active'); });
    el.classList.add('active');
    var target = $(picker.dataset.target);
    if (target) target.value = el.dataset.value;
  }

  function selectQuizAnswer(el) {
    if (!QUIZ_DATA) return;
    QUIZ_ANSWERS[el.dataset.qid] = el.dataset.answer;
    renderQuiz();
  }

  // ── Summary ──
  function generateSummary() {
    $('ssSummaryPrompt').style.display = 'none';
    $('ssSummaryLoading').style.display = 'block';
    $('ssSummaryContent').style.display = 'none';
    fetch('/ajax/study-space/' + SPACE_ID + '/summary/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({ mode: SUMMARY_MODE })
    }).then(function (r) {
      if (r.status === 202) {
        return r.json().then(function (data) {
          if (data.jobId) {
            pollGenerationJob(data.jobId,
              function (pct, msg) { $('ssSummaryLoading').textContent = msg || ('Generating... ' + pct + '%'); },
              function (result) { handleSummaryResult(result); },
              function (err) { $('ssSummaryLoading').style.display = 'none'; $('ssSummaryPrompt').style.display = ''; showParseStatusMessage(err); }
            );
            return null;
          }
          $('ssSummaryLoading').style.display = 'none';
          $('ssSummaryPrompt').style.display = '';
          showParseStatusMessage(data.error || 'Documents are still being parsed. Please wait a moment and try again.');
          return null;
        });
      }
      return r.json();
    }).then(function (data) {
      if (!data) return;
      $('ssSummaryLoading').style.display = 'none';
      if (data.error) { $('ssSummaryPrompt').style.display = ''; showParseStatusMessage(data.error); return; }
      handleSummaryResult(data);
    }).catch(function (e) {
      $('ssSummaryLoading').style.display = 'none';
      $('ssSummaryPrompt').style.display = '';
      showParseStatusMessage('Failed to generate summary. Please try again.');
    });
  }

  function handleSummaryResult(data) {
    if (data.error) { $('ssSummaryPrompt').style.display = ''; showParseStatusMessage(data.error); return; }
    SPACE_DATA.linkSummaryCompact = data.summaryCompact || '';
    SPACE_DATA.linkSummaryDetailed = data.summaryDetailed || '';
    if (data.mode) { SUMMARY_MODE = data.mode; syncSummaryModeButtons(); }
    renderSummaryPanel();
  }

  function showSummary(text) {
    $('ssSummaryPrompt').style.display = 'none';
    $('ssSummaryContent').style.display = 'block';
    $('ssSummaryText').innerHTML = renderMarkdown(text);
    renderMathInElement($('ssSummaryText'));
  }

  function renderMarkdown(text) {
    if (!text) return '';
    text = wrapBareLatex(text);
    if (typeof window.renderMarkdown === 'function') {
      return sanitizeRendered(window.renderMarkdown(text));
    }
    var s = esc(text);
    return sanitizeRendered(s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>'));
  }

  function sanitizeRendered(html) {
    var template = document.createElement('template');
    template.innerHTML = html;
    template.content.querySelectorAll('script,style,iframe,object,embed').forEach(function (el) { el.remove(); });
    template.content.querySelectorAll('*').forEach(function (el) {
      Array.prototype.slice.call(el.attributes).forEach(function (attr) {
        var name = attr.name.toLowerCase();
        var value = String(attr.value || '').trim().toLowerCase();
        if (name.indexOf('on') === 0 || value.indexOf('javascript:') === 0) el.removeAttribute(attr.name);
      });
    });
    return template.innerHTML;
  }

  function wrapBareLatex(text) {
    if (!text) return text;
    text = text.replace(/\$+/g, '');
    var out = '', i = 0;
    while (i < text.length) {
      if (text[i] === '\\') {
        if (text.slice(i, i + 4) === '\\ce{') {
          var depth = 1, j = i + 4;
          while (j < text.length && depth > 0) {
            if (text[j] === '{') depth++;
            else if (text[j] === '}') depth--;
            j++;
          }
          out += '$' + text.slice(i, j) + '$';
          i = j;
        } else {
          var cmd = text.slice(i + 1).match(/^[A-Za-z]+/);
          if (cmd) {
            var known = ['Delta', 'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'theta', 'lambda', 'sigma', 'omega', 'mu', 'nu', 'pi', 'rho', 'tau', 'phi', 'psi', 'chi', 'kappa', 'xi', 'zeta', 'eta', 'upsilon', 'varphi', 'varepsilon', 'vartheta', 'varpi', 'varrho', 'varsigma', 'rightarrow', 'leftarrow', 'leftrightarrow', 'longrightarrow', 'longleftarrow', 'Rightarrow', 'Leftarrow', 'Leftrightarrow', 'approx', 'neq', 'leq', 'geq', 'leqslant', 'geqslant', 'pm', 'mp', 'times', 'div', 'cdot', 'partial', 'nabla', 'infty', 'sum', 'prod', 'int', 'oint', 'sqrt', 'frac', 'circ', 'bullet', 'oplus', 'otimes', 'perp', 'parallel', 'angle', 'triangle', 'cong', 'sim', 'simeq', 'propto', 'equiv', 'subset', 'supset', 'subseteq', 'supseteq', 'cup', 'cap', 'in', 'notin', 'forall', 'exists', 'neg', 'land', 'lor', 'implies', 'iff', 'prime', 'ell', 'Re', 'Im', 'aleph', 'hbar', 'top', 'bot', 'vdots', 'cdots', 'ddots', 'ldots', 'quad', 'qquad', 'mathrm', 'text', 'operatorname', 'overline', 'underline', 'hat', 'bar', 'vec', 'tilde', 'dot', 'ddot', 'widehat', 'widetilde', 'overrightarrow', 'overleftarrow', 'xrightarrow', 'xleftarrow'];
            if (known.indexOf(cmd[0]) !== -1) {
              var math = '$\\' + cmd[0];
              var k = i + 1 + cmd[0].length;
              var spaceConsumed = false;
              while (k < text.length) {
                if (text[k] === '_' || text[k] === '^') {
                  math += text[k];
                  k++;
                  if (text[k] === '{') {
                    var d2 = 1, m = k + 1;
                    while (m < text.length && d2 > 0) {
                      if (text[m] === '{') d2++;
                      else if (text[m] === '}') d2--;
                      m++;
                    }
                    math += text.slice(k, m);
                    k = m;
                  } else if (text[k]) {
                    math += text[k];
                    k++;
                  }
                } else if (!spaceConsumed && text[k] === ' ' && k + 1 < text.length && /[A-Za-z]/.test(text[k + 1]) && text[k + 1] !== '\\') {
                  spaceConsumed = true;
                  math += text[k];
                  k++;
                  while (k < text.length && /[A-Za-z0-9]/.test(text[k])) {
                    math += text[k];
                    k++;
                    if (text[k] === '_' || text[k] === '^') {
                      math += text[k];
                      k++;
                      if (text[k] === '{') {
                        var d3 = 1, m2 = k + 1;
                        while (m2 < text.length && d3 > 0) {
                          if (text[m2] === '{') d3++;
                          else if (text[m2] === '}') d3--;
                          m2++;
                        }
                        math += text.slice(k, m2);
                        k = m2;
                      } else if (text[k]) {
                        math += text[k];
                        k++;
                      }
                    }
                  }
                } else {
                  break;
                }
              }
              math += '$';
              out += math;
              i = k;
            } else {
              out += text[i];
              i++;
            }
          } else {
            out += text[i];
            i++;
          }
        }
      } else {
        out += text[i];
        i++;
      }
    }
    return out;
  }

  function renderMathInElement(el) {
    if (window.renderMathInElement) {
      window.renderMathInElement(el, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false },
          { left: '\\(', right: '\\)', display: false },
          { left: '\\[', right: '\\]', display: true }
        ],
        throwOnError: false,
        strict: false
      });
    }
  }

  function saveSummary() {
    var text = $('ssSummaryTextarea').value.trim();
    if (!text) { alert('Summary cannot be empty'); return; }
    fetch('/ajax/study-space/' + SPACE_ID + '/summary/edit/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({ summary: text, mode: SUMMARY_MODE })
    }).then(function (r) { return r.json() })
      .then(function (data) {
        if (data.error) { alert(data.error); return; }
        $('ssSummaryEditor').style.display = 'none';
        showSummary(data.summary);
      });
  }

  // ── Mindmap ──
  function generateMindmap() {
    $('ssMindmapPrompt').style.display = 'none';
    $('ssMindmapLoading').style.display = 'block';
    $('ssMindmapContent').style.display = 'none';
    fetch('/ajax/study-space/' + SPACE_ID + '/mindmap/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }
    }).then(function (r) {
      if (r.status === 202) {
        return r.json().then(function (data) {
          if (data.jobId) {
            pollGenerationJob(data.jobId,
              function (pct, msg) { $('ssMindmapLoading').textContent = msg || ('Generating... ' + pct + '%'); },
              function (result) { handleMindmapResult(result); },
              function (err) { $('ssMindmapLoading').style.display = 'none'; $('ssMindmapPrompt').style.display = ''; showParseStatusMessage(err); }
            );
            return null;
          }
          $('ssMindmapLoading').style.display = 'none';
          $('ssMindmapPrompt').style.display = '';
          showParseStatusMessage(data.error || 'Documents are still being parsed. Please wait and try again.');
          return null;
        });
      }
      return r.json();
    }).then(function (data) {
      if (!data) return;
      $('ssMindmapLoading').style.display = 'none';
      if (data.error) { $('ssMindmapPrompt').style.display = ''; showParseStatusMessage(data.error); return; }
      handleMindmapResult(data);
    }).catch(function (e) {
      $('ssMindmapLoading').style.display = 'none';
      $('ssMindmapPrompt').style.display = '';
      showParseStatusMessage('Failed to generate mindmap. Please try again.');
    });
  }

  function handleMindmapResult(data) {
    if (data.error) { $('ssMindmapPrompt').style.display = ''; showParseStatusMessage(data.error); return; }
    MINDMAP_DATA = data.mindmap;
    showMindmap(data.mindmap);
  }

  function showMindmap(data) {
    if (!data) return;
    $('ssMindmapPrompt').style.display = 'none';
    $('ssMindmapContent').style.display = 'block';
    var tree = $('ssMindmapTree');
    if (tree && window.NEBiansMindmap) {
      window.NEBiansMindmap.render(tree, data, {});
    } else if (tree) {
      tree.innerHTML = '<pre style="white-space:pre-wrap;font-size:0.8125rem;">' + esc(JSON.stringify(data, null, 2)) + '</pre>';
    }
  }

  // ── Quiz ──
  function generateQuiz() {
    stopExamTimer();
    $('ssQuizPrompt').style.display = 'none';
    $('ssQuizHistorySection').style.display = 'none';
    $('ssQuizLoading').style.display = 'block';
    $('ssQuizActive').style.display = 'none';
    $('ssQuizResults').style.display = 'none';
    var count = parseInt($('ssQuizCount')?.value || '10');
    fetch('/ajax/study-space/' + SPACE_ID + '/quiz/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({ count: count })
    }).then(function (r) {
      if (r.status === 202) {
        return r.json().then(function (data) {
          if (data.jobId) {
            pollGenerationJob(data.jobId,
              function (pct, msg) { $('ssQuizLoading').textContent = msg || ('Generating... ' + pct + '%'); },
              function (result) { handleQuizResult(result); },
              function (err) { $('ssQuizLoading').style.display = 'none'; $('ssQuizPrompt').style.display = ''; $('ssQuizHistorySection').style.display = ''; showParseStatusMessage(err); }
            );
            return null;
          }
          $('ssQuizLoading').style.display = 'none';
          $('ssQuizPrompt').style.display = '';
          $('ssQuizHistorySection').style.display = '';
          showParseStatusMessage(data.error || 'Documents are still being parsed. Please wait and try again.');
          return null;
        });
      }
      return r.json();
    }).then(function (data) {
      if (!data) return;
      $('ssQuizLoading').style.display = 'none';
      if (data.error) { $('ssQuizPrompt').style.display = ''; $('ssQuizHistorySection').style.display = ''; EXAM_PENDING_MINUTES = 0; showParseStatusMessage(data.error); return; }
      handleQuizResult(data);
    }).catch(function (e) {
      $('ssQuizLoading').style.display = 'none';
      $('ssQuizPrompt').style.display = '';
      $('ssQuizHistorySection').style.display = '';
      EXAM_PENDING_MINUTES = 0;
      showParseStatusMessage('Failed to generate quiz. Please try again.');
    });
  }

  function handleQuizResult(data) {
    if (data.error) { $('ssQuizPrompt').style.display = ''; $('ssQuizHistorySection').style.display = ''; showParseStatusMessage(data.error); return; }
    QUIZ_DATA = data.quiz;
    QUIZ_ANSWERS = {};
    QUIZ_CURRENT = 0;
    renderQuiz();
    if (EXAM_PENDING_MINUTES > 0) {
      startExamTimer(EXAM_PENDING_MINUTES);
      toast('Exam started — ' + EXAM_PENDING_MINUTES + ' minutes on the clock.');
      EXAM_PENDING_MINUTES = 0;
    }
  }

  function answeredCount() {
    var qs = (QUIZ_DATA && QUIZ_DATA.questions) || [];
    var n = 0;
    qs.forEach(function (q) { if (QUIZ_ANSWERS[q.id]) n++; });
    return n;
  }

  function renderQuiz() {
    if (!QUIZ_DATA) return;
    $('ssQuizActive').style.display = 'block';
    var hint = $('ssQuizKeyHint');
    if (hint) hint.style.display = '';
    var qs = QUIZ_DATA.questions || [];
    if (!qs.length) { $('ssQuizActive').innerHTML = '<p>No questions generated.</p>'; return; }
    var q = qs[QUIZ_CURRENT];
    var answered = answeredCount();
    var isLast = QUIZ_CURRENT >= qs.length - 1;
    var allAnswered = answered >= qs.length;
    $('ssQuizActive').innerHTML = '<div class="sl-quiz-progress"><span>Question ' + (QUIZ_CURRENT + 1) + ' of ' + qs.length + '</span><span>Answered: ' + answered + '/' + qs.length + '</span></div>'
      + '<div class="sl-quiz-question">' + renderMarkdown(q.questionText) + '</div>'
      + '<div class="sl-quiz-options-list" role="radiogroup" aria-label="Answer options">'
      + formatOption(q.id, 'A', q.optionA, QUIZ_ANSWERS[q.id] === 'A')
      + formatOption(q.id, 'B', q.optionB, QUIZ_ANSWERS[q.id] === 'B')
      + formatOption(q.id, 'C', q.optionC, QUIZ_ANSWERS[q.id] === 'C')
      + formatOption(q.id, 'D', q.optionD, QUIZ_ANSWERS[q.id] === 'D')
      + '</div>'
      + '<div class="sl-quiz-nav">'
      + '<button class="md-btn md-btn-outlined" data-action="ss-quiz-prev" ' + (QUIZ_CURRENT === 0 ? 'disabled' : '') + '>Previous</button>'
      + (isLast || allAnswered
        ? '<button class="md-btn md-btn-filled" data-action="ss-quiz-submit" ' + (answered === 0 ? 'disabled' : '') + '>Submit Quiz</button>'
        : '')
      + (!isLast
        ? '<button class="md-btn md-btn-filled" data-action="ss-quiz-next">Next</button>'
        : '')
      + '</div>';
    renderMathInElement($('ssQuizActive'));
  }

  function formatOption(qid, letter, text, selected) {
    var sel = selected ? ' sl-quiz-option-selected' : '';
    return '<button type="button" class="sl-quiz-option' + sel + '" role="radio" aria-checked="' + (selected ? 'true' : 'false') + '" data-action="ss-quiz-select" data-qid="' + qid + '" data-answer="' + letter + '">'
      + '<span class="sl-quiz-option-letter">' + letter + '</span><span class="sl-quiz-option-text">' + renderMarkdown(text) + '</span></button>';
  }

  // ── Flashcards ──
  function generateFlashcards() {
    $('ssFlashPrompt').style.display = 'none';
    $('ssFlashLoading').style.display = 'block';
    $('ssFlashDeck').style.display = 'none';
    var count = parseInt($('ssFlashCount')?.value || '8');
    fetch('/ajax/study-space/' + SPACE_ID + '/flashcards/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({ count: count })
    }).then(function (r) {
      if (r.status === 202) {
        return r.json().then(function (data) {
          if (data.jobId) {
            pollGenerationJob(data.jobId,
              function (pct, msg) { $('ssFlashLoading').textContent = msg || ('Generating... ' + pct + '%'); },
              function (result) { handleFlashcardResult(result); },
              function (err) { $('ssFlashLoading').style.display = 'none'; $('ssFlashPrompt').style.display = ''; showParseStatusMessage(err); }
            );
            return null;
          }
          $('ssFlashLoading').style.display = 'none';
          $('ssFlashPrompt').style.display = '';
          showParseStatusMessage(data.error || 'Documents are still being parsed. Please wait and try again.');
          return null;
        });
      }
      return r.json();
    }).then(function (data) {
      if (!data) return;
      $('ssFlashLoading').style.display = 'none';
      if (data.error) { $('ssFlashPrompt').style.display = ''; showParseStatusMessage(data.error); return; }
      handleFlashcardResult(data);
    }).catch(function (e) {
      $('ssFlashLoading').style.display = 'none';
      $('ssFlashPrompt').style.display = '';
      showParseStatusMessage('Failed to generate flashcards. Please try again.');
    });
  }

  function handleFlashcardResult(data) {
    if (data.error) { $('ssFlashPrompt').style.display = ''; showParseStatusMessage(data.error); return; }
    FLASHCARDS = data.flashcards || [];
    FLASH_INDEX = 0;
    renderFlashcard();
  }

  function renderFlashcard() {
    if (!FLASHCARDS.length) { $('ssFlashDeck').style.display = 'none'; return; }
    $('ssFlashDeck').style.display = 'block';
    var fHint = $('ssFlashKeyHint');
    if (fHint) fHint.style.display = '';
    var c = FLASHCARDS[FLASH_INDEX];
    var pct = Math.round(((FLASH_INDEX + 1) / FLASHCARDS.length) * 100);
    $('ssFlashDeck').innerHTML = '<div class="sl-flash-topbar">'
      + '<div class="sl-flash-counter">' + (FLASH_INDEX + 1) + ' / ' + FLASHCARDS.length + '</div>'
      + '<button class="md-btn md-btn-tonal" data-action="ss-flash-more">More cards</button>'
      + '</div>'
      + '<div class="ss-flash-progress"><div class="ss-flash-progress-fill" style="width:' + pct + '%"></div></div>'
      + '<div class="sl-flash-card" data-action="ss-flip-card">'
      + '<div class="sl-flash-card-inner">'
      + '<div class="sl-flash-front"><span class="sl-flash-label">Question</span>' + renderMarkdown(c.front) + '</div>'
      + '<div class="sl-flash-back"><span class="sl-flash-label">Answer</span>' + renderMarkdown(c.back) + '</div>'
      + '</div></div>'
      + '<div class="sl-flash-confidence">'
      + '<button class="sl-conf-btn sl-conf-hard" data-action="ss-flash-confidence" data-level="hard"><span class="material-symbols-outlined">close</span> Hard</button>'
      + '<button class="sl-conf-btn sl-conf-medium" data-action="ss-flash-confidence" data-level="medium"><span class="material-symbols-outlined">remove</span> Okay</button>'
      + '<button class="sl-conf-btn sl-conf-easy" data-action="ss-flash-confidence" data-level="easy"><span class="material-symbols-outlined">check</span> Easy</button>'
      + '</div>'
      + '<div class="sl-flash-nav">'
      + '<button class="md-btn md-btn-outlined" data-action="ss-flash-prev" ' + (FLASH_INDEX === 0 ? 'disabled' : '') + '><span class="material-symbols-outlined">arrow_back</span> Previous</button>'
      + '<button class="md-btn md-btn-outlined" data-action="ss-flash-next" ' + (FLASH_INDEX >= FLASHCARDS.length - 1 ? 'disabled' : '') + '>Next <span class="material-symbols-outlined">arrow_forward</span></button>'
      + '</div>';
    renderMathInElement($('ssFlashDeck'));
  }

  function flashNav(dir) {
    FLASH_INDEX = Math.max(0, Math.min(FLASHCARDS.length - 1, FLASH_INDEX + dir));
    renderFlashcard();
  }

  function flashConfidence(level) {
    if (!FLASHCARDS.length) return;
    var c = FLASHCARDS[FLASH_INDEX];
    fetch('/ajax/study-space/flashcard/' + c.id + '/review/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({ confidence: level })
    });
    if (FLASH_INDEX < FLASHCARDS.length - 1) {
      FLASH_INDEX++;
      renderFlashcard();
    }
  }

  function quizNav(dir) {
    if (!QUIZ_DATA) return;
    QUIZ_CURRENT = Math.max(0, Math.min(QUIZ_DATA.questions.length - 1, QUIZ_CURRENT + dir));
    renderQuiz();
  }

  var QUIZ_SUBMITTING = false;
  function submitQuiz() {
    if (!QUIZ_DATA || QUIZ_SUBMITTING) return;
    QUIZ_SUBMITTING = true;
    stopExamTimer();
    fetch('/ajax/study-space/quiz/' + QUIZ_DATA.id + '/submit/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({ answers: QUIZ_ANSWERS })
    }).then(function (r) { return r.json() })
      .then(function (data) {
        QUIZ_SUBMITTING = false;
        if (data.error) { toast(data.error); return; }
        showQuizResults(data.attempt || {}, data.results || (data.attempt && data.attempt.results) || []);
        loadQuizHistory();
      }).catch(function () {
        QUIZ_SUBMITTING = false;
        toast('Failed to submit quiz. Please try again.');
      });
  }

  function showQuizResults(attempt, results) {
    $('ssQuizActive').style.display = 'none';
    $('ssQuizResults').style.display = 'block';
    var hint = $('ssQuizKeyHint');
    if (hint) hint.style.display = 'none';
    var xpLine = attempt.xpEarned > 0
      ? '<div class="sl-quiz-xp">+' + attempt.xpEarned + ' XP</div>'
      : (attempt.firstAttempt === false ? '<div class="ss-text-xs">XP is only earned on the first attempt.</div>' : '');
    var html = '<div class="sl-quiz-results-header">'
      + '<span class="material-symbols-outlined">emoji_events</span>'
      + '<h2>Quiz Complete</h2>'
      + '<div class="sl-quiz-score-display"><span class="sl-quiz-score-num">' + (attempt.score || 0) + '</span><span class="sl-quiz-score-total">/' + (attempt.totalQuestions || 0) + '</span></div>'
      + xpLine + '</div>'
      + '<div class="ss-results-list">';
    (results || []).forEach(function (r, idx) {
      var ok = !!r.isCorrect;
      var icon = ok ? 'done' : 'cancel';
      var given = r.userAnswer || '—';
      var givenText = r.options && r.options[given] ? renderMarkdown(r.options[given]) : '';
      var correctText = r.options && r.options[r.correctAnswer] ? renderMarkdown(r.options[r.correctAnswer]) : '';
      html += '<div class="ss-result-item ' + (ok ? 'ss-result-item-correct' : 'ss-result-item-wrong') + '">'
        + '<div class="ss-result-q"><span class="material-symbols-outlined">' + icon + '</span>'
        + '<span class="ss-result-q-num">' + (idx + 1) + '.</span>'
        + '<div class="ss-result-q-text">' + renderMarkdown(r.question || '') + '</div></div>'
        + '<div class="ss-result-answers">'
        + '<span class="ss-result-given">Your answer: <strong>' + esc(given) + '</strong>' + (givenText ? ' — ' + givenText : '') + '</span>'
        + (!ok ? '<span class="ss-result-correct-ans">Correct: <strong>' + esc(r.correctAnswer || '') + '</strong>' + (correctText ? ' — ' + correctText : '') + '</span>' : '')
        + '</div>'
        + (r.explanation ? '<div class="ss-result-explanation">' + renderMarkdown(r.explanation) + '</div>' : '')
        + '</div>';
    });
    html += '</div><div class="sl-quiz-results-actions">'
      + '<button class="md-btn md-btn-outlined" data-action="ss-quiz-retake">Retake Quiz</button>'
      + '<button class="md-btn md-btn-tonal" data-action="ss-quiz-new">Generate New Quiz</button>'
      + '</div>';
    $('ssQuizResults').innerHTML = html;
    renderMathInElement($('ssQuizResults'));
  }

  function retakeQuiz() {
    QUIZ_ANSWERS = {};
    QUIZ_CURRENT = 0;
    $('ssQuizResults').style.display = 'none';
    renderQuiz();
  }

  // ── Exam mode timer ──
  function startExamTimer(minutes) {
    EXAM_ACTIVE = true;
    EXAM_DEADLINE = Date.now() + minutes * 60 * 1000;
    var bar = $('ssExamTimer');
    if (bar) { bar.classList.add('ss-exam-timer-on'); bar.classList.remove('ss-exam-timer-low'); }
    if (EXAM_TIMER) clearInterval(EXAM_TIMER);
    updateExamClock();
    EXAM_TIMER = setInterval(updateExamClock, 1000);
  }

  function updateExamClock() {
    var clock = $('ssExamTimerClock');
    var remaining = Math.max(0, EXAM_DEADLINE - Date.now());
    var mins = Math.floor(remaining / 60000);
    var secs = Math.floor((remaining % 60000) / 1000);
    if (clock) clock.textContent = mins + ':' + (secs < 10 ? '0' : '') + secs;
    var bar = $('ssExamTimer');
    if (bar && remaining < 60 * 1000) bar.classList.add('ss-exam-timer-low');
    if (remaining <= 0) {
      stopExamTimer();
      toast('Time is up — submitting your answers.');
      submitQuiz();
    }
  }

  function stopExamTimer() {
    EXAM_ACTIVE = false;
    if (EXAM_TIMER) { clearInterval(EXAM_TIMER); EXAM_TIMER = null; }
    var bar = $('ssExamTimer');
    if (bar) bar.classList.remove('ss-exam-timer-on');
  }

  function loadQuizHistory() {
    if (!SPACE_ID) return;
    fetch('/ajax/study-space/' + SPACE_ID + '/quizzes/', { headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.json() })
      .then(function (data) {
        if (!data || !data.quizzes) return;
        renderQuizHistory(data.quizzes);
      }).catch(function () { });
  }

  function renderQuizHistory(quizzes) {
    var section = $('ssQuizHistorySection');
    var list = $('ssQuizHistoryList');
    if (!section || !list) return;
    if (!quizzes || !quizzes.length) {
      section.style.display = 'none';
      return;
    }
    section.style.display = 'block';
    var html = '';
    quizzes.forEach(function (q) {
      var pct = q.attemptCount > 0 ? Math.round((q.bestScore / q.questionCount) * 100) : 0;
      var scoreText = q.attemptCount > 0 ? q.bestScore + '/' + q.questionCount + ' best' : 'No attempts';
      var metaText = q.attemptCount > 0 ? q.attemptCount + ' attempt' + (q.attemptCount === 1 ? '' : 's') : '';
      if (q.lastAttemptAt) {
        var d = new Date(q.lastAttemptAt);
        metaText += (metaText ? ' \u00b7 ' : '') + d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
      }
      if (!metaText) metaText = q.questionCount + ' questions \u00b7 ' + new Date(q.createdAt).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
      html += '<div class="ss-quiz-history-item" data-action="ss-load-past-quiz" data-quiz-id="' + q.id + '">'
        + '<div class="ss-quiz-hist-icon"><span class="material-symbols-outlined">quiz</span></div>'
        + '<div class="ss-quiz-hist-info">'
        + '<div class="ss-quiz-hist-title">' + esc(q.title || 'Quiz') + '</div>'
        + '<div class="ss-quiz-hist-meta">' + esc(metaText) + '</div>'
        + '</div>'
        + (q.attemptCount > 0 ? '<div class="ss-quiz-hist-score"><span class="ss-quiz-hist-score-num">' + pct + '%</span><div class="ss-quiz-hist-score-total">' + scoreText + '</div></div>' : '')
        + '</div>';
    });
    list.innerHTML = html;
  }

  function loadPastQuiz(quizId) {
    $('ssQuizPrompt').style.display = 'none';
    $('ssQuizHistorySection').style.display = 'none';
    $('ssQuizLoading').style.display = 'block';
    $('ssQuizActive').style.display = 'none';
    $('ssQuizResults').style.display = 'none';
    fetch('/ajax/study-space/quiz/' + quizId + '/', { headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.json() })
      .then(function (data) {
        $('ssQuizLoading').style.display = 'none';
        if (!data || !data.quiz || !data.quiz.questions || !data.quiz.questions.length) {
          $('ssQuizPrompt').style.display = '';
          showParseStatusMessage('Could not load quiz.');
          return;
        }
        QUIZ_DATA = data.quiz;
        QUIZ_ANSWERS = {};
        QUIZ_CURRENT = 0;
        renderQuiz();
      }).catch(function () {
        $('ssQuizLoading').style.display = 'none';
        $('ssQuizPrompt').style.display = '';
        showParseStatusMessage('Failed to load quiz.');
      });
  }

  // ── Mobile sidebar drawer ──
  function toggleMobileSidebar() {
    var sidebar = $('ssSidebar');
    var scrim = $('ssSidebarScrim');
    if (!sidebar) return;
    var open = !sidebar.classList.contains('ss-sidebar-mobile-open');
    sidebar.classList.toggle('ss-sidebar-mobile-open', open);
    if (scrim) scrim.classList.toggle('ss-sidebar-scrim-open', open);
  }

  // ── Share ──
  function copyShareLink() {
    var link = $('ssShareLink');
    if (!link || !link.value) return;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(link.value).then(function () { toast('Link copied'); })
        .catch(function () { link.select(); document.execCommand('copy'); toast('Link copied'); });
    } else {
      link.select(); document.execCommand('copy'); toast('Link copied');
    }
  }

  function inviteLink() {
    return window.location.origin + '/study-space/shared/' + SPACE_DATA.shareToken + '/';
  }

  function openShareModal() {
    if (!SPACE_DATA) return;
    var modal = $('ssShareModal');
    var radios = modal.querySelectorAll('input[name="ssShareMode"]');
    radios.forEach(function (r) { r.checked = r.value === SPACE_DATA.shareMode; });
    $('ssShareSpecific').style.display = SPACE_DATA.shareMode === 'specific' ? 'block' : 'none';
    var publicToggle = $('ssPublicSpace');
    if (publicToggle) publicToggle.checked = SPACE_DATA.visibility === 'public';
    $('ssShareLink').value = SPACE_DATA.shareToken ? inviteLink() : '';
    $('ssInviteCode').textContent = SPACE_DATA.inviteCode || '—';
    var current = $('ssShareCurrent');
    if (current) {
      current.innerHTML = '<div class="ss-inline-meta">'
        + '<span class="ss-chip">' + esc((SPACE_DATA.members || []).length + ' members') + '</span>'
        + '<span class="ss-chip">' + esc((SPACE_DATA.visibility || 'private')) + '</span>'
        + '<span class="ss-chip">' + esc(SPACE_DATA.permissions?.inviteMinRole || 'admin') + '+ can invite</span>'
        + '</div>';
    }
    renderMemberList('ssShareMembers', true);
    modal.style.display = 'flex';
  }

  function saveShare() {
    var modal = $('ssShareModal');
    var mode = modal.querySelector('input[name="ssShareMode"]:checked').value;
    var users = [];
    if (mode === 'specific') {
      users = $('ssShareUsers').value.split(',').map(function (u) { return u.trim() }).filter(Boolean);
    }
    var visibility = $('ssPublicSpace') && $('ssPublicSpace').checked ? 'public' : (mode === 'private' ? 'private' : 'unlisted');
    fetch('/ajax/study-space/' + SPACE_ID + '/share/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({ mode: mode, users: users, visibility: visibility, allowJoinByCode: true })
    }).then(function (r) { return r.json() })
      .then(function (data) {
        if (data.error) { toast(data.error); return; }
        SPACE_DATA = data;
        if (data.shareToken) { $('ssShareLink').value = inviteLink(); }
        $('ssInviteCode').textContent = data.inviteCode || '—';
        renderMembers();
        modal.style.display = 'none';
        if (data.missingUsers && data.missingUsers.length) { toast('Saved, but these users were not found: ' + data.missingUsers.join(', ')); }
      });
  }

  function updateMemberRole(memberId, role) {
    fetch('/ajax/study-space/' + SPACE_ID + '/members/' + memberId + '/role/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({ role: role })
    }).then(function (r) { return r.json() })
      .then(function (data) {
        if (data.error) { toast(data.error); loadSpace(); return; }
        SPACE_DATA = data.space || SPACE_DATA;
        renderMembers();
      });
  }

  function removeMember(memberId) {
    if (!confirm('Remove this member from the StudySpace?')) return;
    fetch('/ajax/study-space/' + SPACE_ID + '/members/' + memberId + '/remove/', {
      method: 'POST', headers: { 'X-CSRFToken': csrf() }
    }).then(function (r) { return r.json() })
      .then(function (data) {
        if (data.error) { toast(data.error); return; }
        SPACE_DATA = data.space || SPACE_DATA;
        renderMembers();
        renderPresence();
      });
  }

  function startPresenceLoop() {
    if (PRESENCE_TIMER) clearInterval(PRESENCE_TIMER);
    sendPresence('inside', 'inside StudySpace', false);
    PRESENCE_TIMER = setInterval(function () { sendPresence(activityStatus(), activityDetail(), false); }, 15000);
  }

  function activityStatus() {
    if (CURRENT_TAB === 'notes') return 'editing';
    if (CURRENT_TAB === 'summary' || CURRENT_TAB === 'mindmap' || CURRENT_TAB === 'quiz' || CURRENT_TAB === 'flashcards') return 'reading';
    return 'inside';
  }

  function activityDetail() {
    if (CURRENT_TAB === 'notes') return 'editing shared notes';
    if (CURRENT_TAB === 'tutor') return 'asking the AI tutor';
    if (CURRENT_TAB === 'analytics') return 'reviewing analytics';
    if (CURRENT_TAB === 'learningPath') return 'planning study path';
    if (CURRENT_TAB === 'examMode') return 'setting up exam mode';
    return 'browsing ' + CURRENT_TAB;
  }

  function loadSavedLearningPlan() {
    if (!SPACE_DATA || !SPACE_DATA.learningPlan) return;
    var days = SPACE_DATA.learningPlanDays || 10;
    $('ssLearningEmpty').style.display = 'none';
    renderLearningPlanInto(SPACE_DATA.learningPlan, days);
  }

  function renderLearningPlanInto(plan, days) {
    var el = $('ssLearningPlan');
    var html = '<div class="ss-learning-plan-header"><span class="material-symbols-outlined">route</span><span>' + days + '-Day Study Plan</span></div>';
    var blocks = splitDayBlocks(plan);
    blocks.forEach(function (b) {
      if (b.isDay) {
        html += '<div class="ss-day-card"><div class="ss-day-card-head"><span class="material-symbols-outlined ss-day-icon">calendar_today</span>' + esc(b.title) + '</div><div class="ss-day-card-body">' + renderMarkdown(b.body) + '</div></div>';
      } else {
        html += renderMarkdown(b.body);
      }
    });
    html += '<div class="ss-learning-plan-actions"><button class="md-btn md-btn-outlined" data-action="ss-generate-learning-path"><span class="material-symbols-outlined">refresh</span> Regenerate</button></div>';
    el.innerHTML = html;
    renderMathInElement(el);
    el.style.display = 'block';
  }

  function splitDayBlocks(plan) {
    var lines = plan.split('\n');
    var blocks = [];
    var current = null;
    for (var i = 0; i < lines.length; i++) {
      var m = lines[i].match(/^(#{1,3})\s*(Day\s*\d[\s\S]*?)$/i);
      if (m) {
        if (current) blocks.push(current);
        current = { isDay: true, title: m[2].trim(), body: '' };
      } else {
        if (!current) current = { isDay: false, body: '' };
        current.body += lines[i] + '\n';
      }
    }
    if (current) blocks.push(current);
    return blocks;
  }

  function sendPresence(status, detail, isTyping) {
    if (!SPACE_ID) return;
    fetch('/ajax/study-space/' + SPACE_ID + '/presence/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({ status: status, currentTab: CURRENT_TAB, detail: detail || '', isTyping: !!isTyping, sessionId: PRESENCE_SESSION })
    }).then(function (r) { return r.json() })
      .then(function (data) {
        if (data.presence) {
          SPACE_DATA.presence = data.presence;
          if (SPACE_DATA.analytics) SPACE_DATA.analytics.activeNow = data.activeNow || data.presence.length;
          renderPresence();
          renderAnalytics();
        }
      }).catch(function () { });
  }

  function openSettingsModal() {
    if (!SPACE_DATA) return;
    $('ssSettingsTitle').value = SPACE_DATA.title || '';
    $('ssSettingsDescription').value = SPACE_DATA.description || '';
    $('ssSettingsLevel').value = SPACE_DATA.studyLevel || '';
    $('ssSettingsSubject').value = SPACE_DATA.subject || '';
    $('ssSettingsExam').value = SPACE_DATA.exam || '';
    $('ssSettingsVisibility').value = SPACE_DATA.visibility || 'private';
    $('ssPermGenerate').value = SPACE_DATA.permissions?.generateMinRole || 'moderator';
    $('ssPermUpload').value = SPACE_DATA.permissions?.uploadMinRole || 'member';
    $('ssPermInvite').value = SPACE_DATA.permissions?.inviteMinRole || 'admin';
    $('ssPermPublish').value = SPACE_DATA.permissions?.publishMinRole || 'owner';
    $('ssSettingsModal').style.display = 'flex';
  }

  function saveSettings() {
    var body = {
      title: $('ssSettingsTitle').value.trim(),
      description: $('ssSettingsDescription').value.trim(),
      study_level: $('ssSettingsLevel').value.trim(),
      subject: $('ssSettingsSubject').value.trim(),
      exam: $('ssSettingsExam').value.trim(),
      visibility: $('ssSettingsVisibility').value,
      generate_min_role: $('ssPermGenerate').value,
      upload_min_role: $('ssPermUpload').value,
      invite_min_role: $('ssPermInvite').value,
      publish_min_role: $('ssPermPublish').value
    };
    fetch('/ajax/study-space/' + SPACE_ID + '/settings/', {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify(body)
    }).then(function (r) { return r.json() })
      .then(function (data) {
        if (data.error) { toast(data.error); return; }
        SPACE_DATA = data;
        $('ssTitle').textContent = data.title || 'Untitled Space';
        $('ssSettingsModal').style.display = 'none';
        renderAnalytics();
      });
  }

  function saveNotes(showToast) {
    var content = '';
    if (SSYJS_INST && SSYJS_INST.getContent) {
      content = SSYJS_INST.getContent();
    } else {
      var ta = $('ssNotesTextarea');
      if (ta) content = ta.value;
    }
    if (!content && content !== '') return;
    fetch('/ajax/study-space/' + SPACE_ID + '/notes/', {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify({ content: content })
    }).then(function (r) { return r.json() })
      .then(function (data) {
        if (data.error) { if (showToast) toast(data.error); return; }
        SPACE_DATA.note = data.note;
        sendPresence('editing', 'editing shared notes', false);
      }).catch(function () { });
  }

  function askTutor() {
    var q = $('ssTutorQuestion').value.trim();
    if (!q) { toast('Enter a question first'); return; }
    $('ssTutorStatus').textContent = 'Thinking...';
    $('ssTutorAnswer').style.display = 'none';
    fetch('/ajax/study-space/' + SPACE_ID + '/tutor/', {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify({ question: q })
    }).then(function (r) { return r.json() })
      .then(function (data) {
        $('ssTutorStatus').textContent = '';
        if (data.error) { toast(data.error); return; }
        $('ssTutorAnswer').style.display = 'block';
        $('ssTutorAnswer').innerHTML = renderMarkdown(data.answer || '');
        renderMathInElement($('ssTutorAnswer'));
        $('ssTutorCitations').textContent = 'Sources: ' + (data.citations || []).map(function (c) { return c.title; }).join(', ');
        sendPresence('generating', 'asking the AI tutor', false);
      }).catch(function () { $('ssTutorStatus').textContent = ''; toast('Tutor request failed'); });
  }

  function generateLearningPath() {
    var days = parseInt($('ssLearningDays')?.value || '10', 10);
    $('ssLearningEmpty').style.display = 'none';
    $('ssLearningPlan').style.display = 'none';
    $('ssLearningLoading').style.display = 'block';
    fetch('/ajax/study-space/' + SPACE_ID + '/learning-path/', {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify({ days: days })
    }).then(function (r) { return r.json() })
      .then(function (data) {
        $('ssLearningLoading').style.display = 'none';
        if (data.error) { toast(data.error); $('ssLearningEmpty').style.display = 'block'; return; }
        if (data.plan) {
          renderLearningPlanInto(data.plan, days);
        }
        sendPresence('generating', 'generating learning path', false);
      }).catch(function () {
        $('ssLearningLoading').style.display = 'none';
        $('ssLearningEmpty').style.display = 'block';
      });
  }
  var EXAM_PENDING_MINUTES = 0;
  function startExamMode() {
    var count = parseInt($('ssExamQuestionCount')?.value || '10', 10);
    var mins = parseInt($('ssExamMinutes')?.value || '10', 10);
    switchTab('quiz');
    $('ssQuizCount').value = String(count);
    $$('.ss-count-choice').forEach(function (b) {
      if (b.closest('#ssQuizCountPicker')) b.classList.toggle('active', b.dataset.value === String(count));
    });
    EXAM_PENDING_MINUTES = mins;
    generateQuiz();
  }
  // ── Rename ──
  function openRenameModal() {
    $('ssRenameTitle').value = SPACE_DATA.title || '';
    $('ssRenameDesc').value = SPACE_DATA.description || '';
    $('ssRenameModal').style.display = 'flex';
  }

  function submitRename() {
    var title = $('ssRenameTitle').value.trim();
    var desc = $('ssRenameDesc').value.trim();
    fetch('/ajax/study-space/' + SPACE_ID + '/update/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({ title: title, description: desc })
    }).then(function (r) { return r.json() })
      .then(function (data) {
        if (data.error) { toast(data.error); return; }
        SPACE_DATA = data;
        $('ssTitle').textContent = data.title || 'Untitled Space';
        $('ssRenameModal').style.display = 'none';
      });
  }

  // ── Delete ──
  function deleteSpace() {
    fetch('/ajax/study-space/' + SPACE_ID + '/delete/', {
      method: 'POST',
      headers: { 'X-CSRFToken': csrf() }
    }).then(function (r) { return r.json() })
      .then(function (data) {
        if (data.success) window.location.href = '/study-lab/';
        else toast(data.error || 'Failed to delete');
      });
  }

  // ── Document selection ──
  var selectedDocId = null;
  var docSelectTab = 'docs';

  function openDocSelectModal() {
    var modal = $('ssSelectDocModal');
    var list = $('ssDocSelectList');
    var rlist = $('ssResourceSelectList');
    list.innerHTML = '<div class="ss-doc-select-empty"><span class="material-symbols-outlined">hourglass_top</span><p>Loading documents...</p></div>';
    rlist.innerHTML = '<div class="ss-doc-select-empty"><span class="material-symbols-outlined">hourglass_top</span><p>Loading resources...</p></div>';
    selectedDocId = null;
    modal.style.display = 'flex';
    loadDocSelectDocs();
    loadDocSelectResources();
  }

  function loadDocSelectDocs() {
    var list = $('ssDocSelectList');
    fetch('/ajax/study-space/' + SPACE_ID + '/document/list/', { headers: { 'X-CSRFToken': csrf(), 'Accept': 'application/json' } })
      .then(function (r) { return r.json() })
      .then(function (data) {
        var docs = data.documents || [];
        if (!docs.length) {
          list.innerHTML = '<div class="ss-doc-select-empty"><span class="material-symbols-outlined">description</span><p>No study documents yet</p></div>';
          return;
        }
        var html = '';
        docs.forEach(function (d) {
          var icon = d.status === 'ready' ? 'description' : 'error';
          var inSpace = d.spaceId === SPACE_ID;
          var selClass = inSpace ? ' selected' : '';
          var meta = [];
          if (d.fileName) meta.push(d.fileName);
          if (d.fileSize) meta.push((d.fileSize / 1024).toFixed(0) + 'KB');
          html += '<div class="ss-doc-select-item' + selClass + '" data-doc-id="' + d.id + '" data-doc-type="studydoc" data-action="ss-select-doc-item">'
            + '<span class="material-symbols-outlined">' + icon + '</span>'
            + '<div class="ss-doc-select-info">'
            + '<span class="ss-doc-select-title">' + esc(d.title) + '</span>'
            + (meta.length ? '<span class="ss-doc-select-meta">' + esc(meta.join(' · ')) + '</span>' : '')
            + '</div>'
            + (inSpace ? '<span class="material-symbols-outlined ss-doc-select-check">done</span>' : '')
            + '</div>';
        });
        list.innerHTML = html;
      }).catch(function (e) {
        list.innerHTML = '<div class="ss-doc-select-empty"><span class="material-symbols-outlined">error</span><p>Failed to load documents.</p></div>';
      });
  }

  function loadDocSelectResources() {
    var list = $('ssResourceSelectList');
    fetch('/ajax/study-space/' + SPACE_ID + '/resource/list/', { headers: { 'X-CSRFToken': csrf(), 'Accept': 'application/json' } })
      .then(function (r) { return r.json() })
      .then(function (data) {
        var resources = data.resources || [];
        if (!resources.length) {
          list.innerHTML = '<div class="ss-doc-select-empty"><span class="material-symbols-outlined">folder_off</span><p>No resources uploaded yet</p></div>';
          return;
        }
        var html = '';
        resources.forEach(function (r) {
          var icon = r.type === 'PDF' ? 'picture_as_pdf' : r.type === 'Video' ? 'play_circle' : 'article';
          var meta = [];
          if (r.subject) meta.push(r.subject);
          if (r.type) meta.push(r.type);
          if (r.fileSize) meta.push((r.fileSize / 1024).toFixed(0) + 'KB');
          html += '<div class="ss-doc-select-item" data-resource-id="' + r.id + '" data-doc-type="resource" data-action="ss-select-doc-item">'
            + '<span class="material-symbols-outlined">' + icon + '</span>'
            + '<div class="ss-doc-select-info">'
            + '<span class="ss-doc-select-title">' + esc(r.title) + '</span>'
            + (meta.length ? '<span class="ss-doc-select-meta">' + esc(meta.join(' · ')) + '</span>' : '')
            + '</div>'
            + '</div>';
        });
        list.innerHTML = html;
      }).catch(function (e) {
        list.innerHTML = '<div class="ss-doc-select-empty"><span class="material-symbols-outlined">error</span><p>Failed to load resources.</p></div>';
      });
  }

  function submitDocSelection() {
    if (!selectedDocId) { toast('Please select an item'); return; }
    var selectedItem = document.querySelector('.ss-doc-select-item.selected');
    var docType = selectedItem ? selectedItem.dataset.docType : 'studydoc';
    var url, body;
    if (docType === 'resource') {
      url = '/ajax/study-space/' + SPACE_ID + '/resource/add/';
      body = JSON.stringify({ resource_id: selectedDocId });
    } else {
      url = '/ajax/study-space/' + SPACE_ID + '/document/add/';
      body = JSON.stringify({ document_id: selectedDocId });
    }
    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: body
    }).then(function (r) { return r.json() })
      .then(function (data) {
        if (data.error) { toast(data.error); return; }
        $('ssSelectDocModal').style.display = 'none';
        loadSpace();
      });
  }

  document.addEventListener('click', function (e) {
    var item = e.target.closest('.ss-doc-select-item');
    if (item) {
      $$('.ss-doc-select-item').forEach(function (i) { i.classList.remove('selected'); });
      item.classList.add('selected');
      selectedDocId = item.dataset.docId || item.dataset.resourceId;
      return;
    }
    var tab = e.target.closest('[data-action="ss-doc-tab"]');
    if (tab) {
      docSelectTab = tab.dataset.tab;
      $$('.ss-doc-tab').forEach(function (t) { t.classList.toggle('ss-doc-tab-active', t.dataset.tab === docSelectTab); });
      $('ssDocSelectList').style.display = docSelectTab === 'docs' ? '' : 'none';
      $('ssResourceSelectList').style.display = docSelectTab === 'resources' ? '' : 'none';
      selectedDocId = null;
      $$('.ss-doc-select-item').forEach(function (i) { i.classList.remove('selected'); });
    }
  });

  // ── Keyboard shortcuts ──
  var KEY_TO_LETTER = { '1': 'A', '2': 'B', '3': 'C', '4': 'D' };
  document.addEventListener('keydown', function (e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (CURRENT_TAB === 'quiz' && $('ssQuizActive') && $('ssQuizActive').style.display !== 'none') {
      var key = e.key.toUpperCase();
      if (KEY_TO_LETTER[key]) key = KEY_TO_LETTER[key];
      if (key === 'A' || key === 'B' || key === 'C' || key === 'D') {
        e.preventDefault();
        var q = QUIZ_DATA && QUIZ_DATA.questions && QUIZ_DATA.questions[QUIZ_CURRENT];
        if (q) {
          QUIZ_ANSWERS[q.id] = key;
          renderQuiz();
        }
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        if (QUIZ_CURRENT > 0) { QUIZ_CURRENT--; renderQuiz(); }
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        if (QUIZ_DATA && QUIZ_DATA.questions && QUIZ_CURRENT < QUIZ_DATA.questions.length - 1) { QUIZ_CURRENT++; renderQuiz(); }
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (QUIZ_DATA && QUIZ_DATA.questions && QUIZ_CURRENT === QUIZ_DATA.questions.length - 1) submitQuiz();
        else if (QUIZ_DATA && QUIZ_DATA.questions && QUIZ_CURRENT < QUIZ_DATA.questions.length - 1) { QUIZ_CURRENT++; renderQuiz(); }
      }
    }
    if (CURRENT_TAB === 'flashcards' && $('ssFlashDeck') && $('ssFlashDeck').style.display !== 'none') {
      if (e.key === ' ') {
        e.preventDefault();
        var card = document.querySelector('.sl-flash-card');
        if (card) card.classList.toggle('sl-flash-flipped');
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        flashNav(-1);
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        flashNav(1);
      } else if (e.key.toUpperCase() === 'H') {
        e.preventDefault();
        flashConfidence('hard');
      } else if (e.key.toUpperCase() === 'O') {
        e.preventDefault();
        flashConfidence('medium');
      } else if (e.key.toUpperCase() === 'E') {
        e.preventDefault();
        flashConfidence('easy');
      }
    }
  });

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();