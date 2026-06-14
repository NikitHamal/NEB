/* Study Lab interactions. Keep this file modular and near 500-600 lines; move large new features to dedicated modules. */
(function() {
  'use strict';

  var currentDocId = null;
  var currentDocData = null;
  var currentTab = 'summary';
  var currentSummaryMode = 'compact';
  var quizQuestions = [];
  var quizAnswers = {};
  var currentQuizIdx = 0;
  var currentQuizId = null;
  var flashcards = [];
  var currentFlashIdx = 0;
  var isFlipped = false;
  var currentShareSettings = null;

  var fileInput = document.getElementById('slFileInput');
  if (fileInput) {
    fileInput.addEventListener('change', function(e) {
      var file = e.target.files[0];
      if (!file) return;
      var overlay = document.getElementById('slUploadProgress');
      var bar = document.getElementById('slUploadProgressBar');
      var pctEl = document.getElementById('slUploadProgressPercent');
      var sizeEl = document.getElementById('slUploadProgressSize');
      var subtitleEl = document.getElementById('slUploadProgressSubtitle');
      if (overlay) { overlay.style.display = 'flex'; }
      if (bar) { bar.style.width = '0%'; }
      if (pctEl) { pctEl.textContent = '0%'; }
      if (sizeEl) { sizeEl.textContent = formatSize(0) + ' / ' + formatSize(file.size); }
      if (subtitleEl) { subtitleEl.textContent = 'Please wait while your file is being uploaded...'; }
      var formData = new FormData();
      formData.append('file', file);
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/ajax/study-lab/upload/', true);
      xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
      xhr.withCredentials = true;
      xhr.upload.addEventListener('progress', function(evt) {
        if (evt.lengthComputable) {
          var pct = Math.round((evt.loaded / evt.total) * 100);
          if (bar) bar.style.width = pct + '%';
          if (pctEl) pctEl.textContent = pct + '%';
          if (sizeEl) sizeEl.textContent = formatSize(evt.loaded) + ' / ' + formatSize(evt.total);
        }
      });
      xhr.addEventListener('load', function() {
        try {
          var data = JSON.parse(xhr.responseText);
          if (xhr.status >= 200 && xhr.status < 300 && !data.error) {
            if (bar) bar.style.width = '100%';
            if (pctEl) pctEl.textContent = '100%';
            if (subtitleEl) subtitleEl.textContent = 'Processing document...';
            setTimeout(function() {
              if (overlay) overlay.style.display = 'none';
              showSnackbar('Document uploaded');
              addDocToList(data.document);
              selectDoc(data.document.id);
            }, 600);
          } else {
            if (overlay) overlay.style.display = 'none';
            showSnackbar((data && data.error) || 'Upload failed');
          }
        } catch (err) {
          if (overlay) overlay.style.display = 'none';
          showSnackbar('Upload failed');
        }
      });
      xhr.addEventListener('error', function() {
        if (overlay) overlay.style.display = 'none';
        showSnackbar('Network error during upload');
      });
      xhr.send(formData);
      e.target.value = '';
    });
  }

  function handleJson(r) {
    return r.json().then(function(data) {
      if (!r.ok || data.error) throw new Error(data.error || 'Request failed');
      return data;
    });
  }

  function addDocToList(doc) {
    var empty = document.getElementById('slEmptyDocs');
    if (empty) empty.style.display = 'none';
    var list = document.getElementById('slDocList');
    var div = document.createElement('div');
    div.className = 'sl-doc-item';
    div.dataset.docId = doc.id;
    div.dataset.action = 'sl-select-doc';
    var ps = doc.parseStatus || 'pending';
    var icon = 'description';
    var statusHtml = '';
    if (ps === 'uploading' || ps === 'parsing' || ps === 'extracting') {
      icon = 'hourglass_top';
      statusHtml = '<span class="sl-doc-parse-status sl-doc-parsing">Parsing...</span>';
    } else if (ps === 'failed') {
      icon = 'error';
      statusHtml = '<span class="sl-doc-parse-status sl-doc-failed">Parse failed</span>';
    }
    div.innerHTML = '<span class="material-symbols-outlined sl-doc-icon' + (ps === 'uploading' || ps === 'parsing' || ps === 'extracting' ? ' sl-icon-spin' : '') + '">' + icon + '</span>' +
      '<div class="sl-doc-info"><div class="sl-doc-title">' + escapeHtml(doc.title) + '</div>' + statusHtml + '</div>';
    list.insertBefore(div, list.firstChild);
    // Start polling if parsing
    if (ps === 'uploading' || ps === 'parsing' || ps === 'extracting') {
      _pollParseStatus(doc.id);
    }
  }

  function selectDoc(docId) {
    currentDocId = docId;
    document.querySelectorAll('.sl-doc-item').forEach(function(el) { el.classList.toggle('sl-doc-active', el.dataset.docId === docId); });
    document.getElementById('slWelcome').style.display = 'none';
    document.getElementById('slDetail').style.display = '';
    fetch('/ajax/study-lab/document/' + docId + '/', { headers: {'X-CSRFToken': CSRF_TOKEN}, credentials: 'same-origin' })
      .then(handleJson)
      .then(function(data) { currentDocData = data; renderDocDetail(data); })
      .catch(function(err) { showSnackbar(err.message || 'Failed to load document'); });
  }

  function renderDocDetail(data) {
    var doc = data.document;
    document.getElementById('slDetailTitle').textContent = doc.title;
    var meta = [];
    if (doc.fileName) meta.push(doc.fileName);
    if (doc.fileSize) meta.push(formatSize(doc.fileSize));
    meta.push(doc.summaryGenerated ? 'Summary available' : 'No summary yet');
    if (doc.mindmapGenerated) meta.push('Mindmap available');
    document.getElementById('slDetailMeta').textContent = meta.join(' · ');

    currentSummaryMode = 'compact';
    renderSummaryPanel();
    renderMindmapPanel();

    var quizPrompt = document.getElementById('slQuizPrompt');
    var quizList = document.getElementById('slQuizList');
    if (data.quizzes && data.quizzes.length > 0) {
      quizPrompt.style.display = 'none';
      quizList.style.display = '';
      renderQuizList(data.quizzes);
    } else {
      quizPrompt.style.display = '';
      quizList.style.display = 'none';
    }
    document.getElementById('slQuizActive').style.display = 'none';
    document.getElementById('slQuizResults').style.display = 'none';

    flashcards = data.flashcards || [];
    if (flashcards.length > 0) {
      document.getElementById('slFlashPrompt').style.display = 'none';
      document.getElementById('slFlashDeck').style.display = '';
      currentFlashIdx = 0;
      renderFlashcard();
    } else {
      document.getElementById('slFlashPrompt').style.display = '';
      document.getElementById('slFlashDeck').style.display = 'none';
    }

    switchTab('summary');
  }

  function switchTab(tab) {
    currentTab = tab;
    document.querySelectorAll('.sl-tab').forEach(function(t) { t.classList.toggle('sl-tab-active', t.dataset.tab === tab); });
    document.getElementById('slTabSummary').style.display = tab === 'summary' ? '' : 'none';
    document.getElementById('slTabMindmap').style.display = tab === 'mindmap' ? '' : 'none';
    document.getElementById('slTabQuiz').style.display = tab === 'quiz' ? '' : 'none';
    document.getElementById('slTabFlashcards').style.display = tab === 'flashcards' ? '' : 'none';
  }

  function renderSummaryPanel() {
    var doc = currentDocData && currentDocData.document ? currentDocData.document : {};
    var text = getSummaryText();
    document.querySelectorAll('.sl-mode-btn').forEach(function(btn) { btn.classList.toggle('sl-mode-active', btn.dataset.mode === currentSummaryMode); });
    document.getElementById('slSummaryPromptText').textContent = currentSummaryMode === 'detailed'
      ? 'Generate a detailed summary with fuller explanations, examples, and exam notes.'
      : 'Generate a compact, high-yield summary of your document.';
    document.getElementById('slSummaryGenerateLabel').textContent = currentSummaryMode === 'detailed' ? 'Generate Detailed Summary' : 'Generate Compact Summary';
    document.getElementById('slSummaryLoadingText').textContent = currentSummaryMode === 'detailed' ? 'Generating detailed summary...' : 'Generating compact summary...';
    document.getElementById('slSummaryEditor').style.display = 'none';
    document.getElementById('slSummaryText').style.display = '';
    if (text) {
      document.getElementById('slSummaryPrompt').style.display = 'none';
      document.getElementById('slSummaryContent').style.display = '';
      var el = document.getElementById('slSummaryText');
      el.innerHTML = renderMarkdown(text);
      renderMath(el);
    } else {
      document.getElementById('slSummaryPrompt').style.display = '';
      document.getElementById('slSummaryContent').style.display = 'none';
    }
    doc.summaryGenerated = Boolean(doc.summaryCompact || doc.summaryDetailed || doc.summary);
  }

  function renderMath(el) {
    if (typeof renderMathInElement === 'function') {
      try {
        renderMathInElement(el, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false},
            {left: '\\(', right: '\\)', display: false},
            {left: '\\[', right: '\\]', display: true}
          ],
          ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'annotation', 'semantics']
        });
      } catch(e) {}
    }
  }

  function getSummaryText() {
    var doc = currentDocData && currentDocData.document ? currentDocData.document : {};
    return currentSummaryMode === 'detailed' ? (doc.summaryDetailed || '') : (doc.summaryCompact || doc.summary || '');
  }

  function generateSummary() {
    document.getElementById('slSummaryPrompt').style.display = 'none';
    document.getElementById('slSummaryContent').style.display = 'none';
    document.getElementById('slSummaryLoading').style.display = '';
    fetch('/ajax/study-lab/document/' + currentDocId + '/summary/', {
      method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}, credentials: 'same-origin',
      body: JSON.stringify({mode: currentSummaryMode})
    }).then(handleJson).then(function(data) {
      document.getElementById('slSummaryLoading').style.display = 'none';
      currentDocData.document.summaryCompact = data.summaryCompact || currentDocData.document.summaryCompact || '';
      currentDocData.document.summaryDetailed = data.summaryDetailed || currentDocData.document.summaryDetailed || '';
      if (data.mode === 'compact') currentDocData.document.summary = data.summary;
      currentDocData.document.summaryGenerated = true;
      renderSummaryPanel();
      
    }).catch(function(err) {
      document.getElementById('slSummaryLoading').style.display = 'none';
      renderSummaryPanel();
      showSnackbar(err.message || 'Failed to generate summary');
    });
  }

  function startSummaryEdit() {
    document.getElementById('slSummaryTextarea').value = getSummaryText();
    document.getElementById('slSummaryText').style.display = 'none';
    document.getElementById('slSummaryEditor').style.display = '';
  }

  function cancelSummaryEdit() {
    document.getElementById('slSummaryEditor').style.display = 'none';
    document.getElementById('slSummaryText').style.display = '';
  }

  function saveSummaryEdit() {
    var value = document.getElementById('slSummaryTextarea').value.trim();
    if (!value) { showSnackbar('Summary cannot be empty'); return; }
    fetch('/ajax/study-lab/document/' + currentDocId + '/summary/edit/', {
      method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}, credentials: 'same-origin',
      body: JSON.stringify({mode: currentSummaryMode, summary: value})
    }).then(handleJson).then(function(data) {
      currentDocData.document.summaryCompact = data.summaryCompact || currentDocData.document.summaryCompact || '';
      currentDocData.document.summaryDetailed = data.summaryDetailed || currentDocData.document.summaryDetailed || '';
      if (data.mode === 'compact') currentDocData.document.summary = data.summary;
      currentDocData.document.summaryGenerated = true;
      renderSummaryPanel();
      
      showSnackbar('Summary updated');
    }).catch(function(err) { showSnackbar(err.message || 'Failed to save summary'); });
  }

  function renderMindmapPanel() {
    if (currentDocData && currentDocData.mindmap) {
      document.getElementById('slMindmapPrompt').style.display = 'none';
      document.getElementById('slMindmapContent').style.display = '';
      renderMindmapStage();
    } else {
      document.getElementById('slMindmapPrompt').style.display = '';
      document.getElementById('slMindmapContent').style.display = 'none';
    }
  }

  function getMindmapOptions() {
    return {};
  }

  function renderMindmapStage() {
    var el = document.getElementById('slMindmapTree');
    if (!el || !currentDocData || !currentDocData.mindmap || !window.NEBiansMindmap) return;
    window.NEBiansMindmap.render(el, currentDocData.mindmap, getMindmapOptions());
  }

  function generateMindmap() {
    document.getElementById('slMindmapPrompt').style.display = 'none';
    document.getElementById('slMindmapContent').style.display = 'none';
    document.getElementById('slMindmapLoading').style.display = '';
    fetch('/ajax/study-lab/document/' + currentDocId + '/mindmap/', { method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}, credentials: 'same-origin' })
      .then(handleJson)
      .then(function(data) {
        document.getElementById('slMindmapLoading').style.display = 'none';
        currentDocData.mindmap = data.mindmap;
        currentDocData.document.mindmapGenerated = true;
        renderMindmapPanel();
        
      })
      .catch(function(err) {
        document.getElementById('slMindmapLoading').style.display = 'none';
        renderMindmapPanel();
        showSnackbar(err.message || 'Failed to generate mindmap');
      });
  }


  function renderQuizList(quizzes) {
    var html = '<div class="sl-list-head"><h3 class="sl-section-title">Your Quizzes</h3><button class="md-btn md-btn-tonal" data-action="sl-new-quiz"><span class="material-symbols-outlined">add</span> Fresh Quiz</button></div><div class="sl-quiz-cards">';
    quizzes.forEach(function(q) {
      html += '<div class="sl-quiz-card" data-action="sl-start-quiz" data-quiz-id="' + q.id + '">' +
        '<div class="sl-quiz-card-title">' + escapeHtml(q.title) + '</div>' +
        '<div class="sl-quiz-card-meta">' + q.questionCount + ' questions · ' + (q.attemptCount || 0) + ' attempt' + ((q.attemptCount || 0) === 1 ? '' : 's') + '</div>' +
        '<div class="sl-quiz-card-score">Best: ' + (q.bestScore || 0) + '/' + q.questionCount + '</div></div>';
    });
    html += '</div>';
    document.getElementById('slQuizList').innerHTML = html;
  }

  function showQuizPrompt() {
    document.getElementById('slQuizList').style.display = 'none';
    document.getElementById('slQuizActive').style.display = 'none';
    document.getElementById('slQuizResults').style.display = 'none';
    document.getElementById('slQuizPrompt').style.display = '';
  }

  function generateQuiz() {
    var count = parseInt(document.getElementById('slQuizCount').value, 10) || 10;
    document.getElementById('slQuizPrompt').style.display = 'none';
    document.getElementById('slQuizList').style.display = 'none';
    document.getElementById('slQuizResults').style.display = 'none';
    document.getElementById('slQuizLoading').style.display = '';
    fetch('/ajax/study-lab/document/' + currentDocId + '/quiz/', {
      method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}, credentials: 'same-origin', body: JSON.stringify({count: count})
    }).then(handleJson).then(function(data) {
      document.getElementById('slQuizLoading').style.display = 'none';
      currentDocData.quizzes = currentDocData.quizzes || [];
      currentDocData.quizzes.unshift({id: data.quiz.id, title: data.quiz.title, questionCount: data.quiz.questionCount, attemptCount: 0, bestScore: 0, createdAt: data.quiz.createdAt});
      
      startQuiz(data.quiz);
    }).catch(function(err) {
      document.getElementById('slQuizLoading').style.display = 'none';
      showQuizPrompt();
      showSnackbar(err.message || 'Failed to generate quiz');
    });
  }

  function startQuiz(quiz) {
    currentQuizId = quiz.id;
    quizQuestions = quiz.questions || [];
    quizAnswers = {};
    currentQuizIdx = 0;
    document.getElementById('slQuizPrompt').style.display = 'none';
    document.getElementById('slQuizList').style.display = 'none';
    document.getElementById('slQuizResults').style.display = 'none';
    document.getElementById('slQuizActive').style.display = '';
    renderQuizQuestion();
  }

  function renderQuizQuestion() {
    if (!quizQuestions.length) return;
    var q = quizQuestions[currentQuizIdx];
    var answeredCount = Object.keys(quizAnswers).filter(function(k) { return quizAnswers[k]; }).length;
    document.getElementById('slQuizProgress').textContent = 'Question ' + (currentQuizIdx + 1) + ' of ' + quizQuestions.length;
    document.getElementById('slQuizScore').textContent = 'Answered: ' + answeredCount + '/' + quizQuestions.length;
    var qEl = document.getElementById('slQuizQuestion');
    qEl.innerHTML = renderMarkdown(q.question);
    renderMath(qEl);
    var opts = [{key:'A', text:q.optionA}, {key:'B', text:q.optionB}, {key:'C', text:q.optionC}, {key:'D', text:q.optionD}];
    var html = '';
    opts.forEach(function(opt) {
      var selected = quizAnswers[q.id] === opt.key;
      html += '<button class="sl-quiz-option' + (selected ? ' sl-quiz-option-selected' : '') + '" data-action="sl-quiz-answer" data-qid="' + q.id + '" data-answer="' + opt.key + '">' +
        '<span class="sl-quiz-option-letter">' + opt.key + '</span><span class="sl-quiz-option-text">' + renderMarkdown(opt.text || '') + '</span></button>';
    });
    document.getElementById('slQuizOptions').innerHTML = html;
    renderMath(document.getElementById('slQuizOptions'));
    document.getElementById('slQuizPrev').disabled = currentQuizIdx === 0;
    var isLast = currentQuizIdx === quizQuestions.length - 1;
    document.getElementById('slQuizNext').style.display = isLast ? 'none' : '';
    document.getElementById('slQuizSubmit').style.display = isLast ? '' : '';
  }

  function submitQuiz() {
    if (!currentQuizId) { showSnackbar('Quiz not ready'); return; }
    var answers = {};
    quizQuestions.forEach(function(q) { if (quizAnswers[q.id]) answers[q.number] = quizAnswers[q.id]; });
    fetch('/ajax/study-lab/quiz/' + currentQuizId + '/submit/', {
      method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}, credentials: 'same-origin', body: JSON.stringify({answers: answers})
    }).then(handleJson).then(function(data) { showQuizResults(data.attempt); }).catch(function(err) { showSnackbar(err.message || 'Failed to submit quiz'); });
  }

  function showQuizResults(attempt) {
    document.getElementById('slQuizActive').style.display = 'none';
    document.getElementById('slQuizResults').style.display = '';
    document.getElementById('slQuizFinalScore').textContent = attempt.score;
    document.getElementById('slQuizFinalTotal').textContent = '/' + attempt.totalQuestions;
    document.getElementById('slQuizXpEarned').textContent = '+' + attempt.xpEarned + ' XP';
    var html = '';
    Object.keys(attempt.results).forEach(function(num) {
      var r = attempt.results[num];
      var cls = r.isCorrect ? 'sl-result-correct' : 'sl-result-wrong';
      var icon = r.isCorrect ? 'done' : 'cancel';
      var expl = r.explanation ? '<p class="sl-result-explanation">' + renderMarkdown(r.explanation) + '</p>' : '';
      html += '<div class="sl-result-item ' + cls + '"><span class="material-symbols-outlined">' + icon + '</span>' +
        '<div><strong>Q' + num + ': ' + (r.userAnswer || 'Skipped') + '</strong><span class="sl-result-answer">Correct: ' + r.correctAnswer + '</span>' +
        expl + '</div></div>';
    });
    var el = document.getElementById('slQuizResultsList');
    el.innerHTML = html;
    renderMath(el);
  }

  function generateFlashcards(append) {
    var count = parseInt(document.getElementById('slFlashCount').value, 10) || 15;
    var oldLength = flashcards.length;
    document.getElementById('slFlashPrompt').style.display = 'none';
    document.getElementById('slFlashMoreWrap').style.display = 'none';
    document.getElementById('slFlashLoading').style.display = '';
    fetch('/ajax/study-lab/document/' + currentDocId + '/flashcards/', {
      method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}, credentials: 'same-origin', body: JSON.stringify({count: count})
    }).then(handleJson).then(function(data) {
      document.getElementById('slFlashLoading').style.display = 'none';
      flashcards = append ? flashcards.concat(data.flashcards || []) : (data.flashcards || []);
      if (currentDocData) currentDocData.flashcards = flashcards;
      currentFlashIdx = append && oldLength ? oldLength : 0;
      document.getElementById('slFlashDeck').style.display = '';
      renderFlashcard();
      
    }).catch(function(err) {
      document.getElementById('slFlashLoading').style.display = 'none';
      if (!flashcards.length) document.getElementById('slFlashPrompt').style.display = '';
      showSnackbar(err.message || 'Failed to generate flashcards');
    });
  }

  function renderFlashcard() {
    if (!flashcards.length) return;
    var card = flashcards[currentFlashIdx];
    var atEnd = currentFlashIdx === flashcards.length - 1;
    document.getElementById('slFlashCounter').textContent = (currentFlashIdx + 1) + ' / ' + flashcards.length;
    var frontEl = document.getElementById('slFlashFrontText');
    frontEl.innerHTML = renderMarkdown(card.front);
    renderMath(frontEl);
    var backEl = document.getElementById('slFlashBackText');
    backEl.innerHTML = renderMarkdown(card.back);
    renderMath(backEl);
    isFlipped = false;
    document.getElementById('slFlashCard').classList.remove('sl-flash-flipped');
    document.getElementById('slFlashPrev').disabled = currentFlashIdx === 0;
    document.getElementById('slFlashNext').disabled = atEnd;
    document.getElementById('slFlashMoreWrap').style.display = atEnd ? '' : 'none';
    document.querySelectorAll('.sl-conf-btn').forEach(function(btn) { btn.classList.toggle('sl-conf-active', card.confidence === btn.dataset.level); });
  }

  function flipCard() {
    isFlipped = !isFlipped;
    document.getElementById('slFlashCard').classList.toggle('sl-flash-flipped', isFlipped);
  }

  function flashcardConfidence(level) {
    if (!flashcards.length) return;
    var card = flashcards[currentFlashIdx];
    fetch('/ajax/study-lab/flashcard/' + card.id + '/review/', {
      method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}, credentials: 'same-origin', body: JSON.stringify({confidence: level})
    }).catch(function() {});
    card.confidence = level;
    if (currentFlashIdx < flashcards.length - 1) { currentFlashIdx++; renderFlashcard(); }
    else { renderFlashcard(); showSnackbar('Deck finished. Generate more new cards when ready.'); }
  }


  function openShareDialog() {
    if (!currentDocId) return;
    var modal = document.getElementById('slShareModal');
    modal.style.display = 'flex';
    modal.classList.add('active');
    fetch('/ajax/study-lab/document/' + currentDocId + '/share/', { headers: {'X-CSRFToken': CSRF_TOKEN}, credentials: 'same-origin' })
      .then(handleJson)
      .then(function(data) { currentShareSettings = data; renderShareDialog(data); })
      .catch(function(err) { showSnackbar(err.message || 'Failed to load sharing settings'); });
  }

  function closeShareDialog() {
    var modal = document.getElementById('slShareModal');
    if (modal) { modal.classList.remove('active'); modal.style.display = 'none'; }
  }

  function renderShareDialog(data) {
    var mode = data.mode || 'private';
    document.querySelectorAll('input[name="slShareMode"]').forEach(function(radio) { radio.checked = radio.value === mode; });
    var link = document.getElementById('slShareLink');
    if (link) link.value = data.shareUrl || '';
    var usersBox = document.getElementById('slShareUsers');
    if (usersBox) usersBox.value = (data.users || []).map(function(u) { return u.username; }).join(', ');
    updateShareSpecificVisibility();
    var current = document.getElementById('slShareCurrent');
    if (current) {
      if (mode === 'private') current.innerHTML = 'Current access: only you.';
      else if (mode === 'link') current.innerHTML = 'Current access: signed-in users with this link.';
      else if (data.users && data.users.length) current.innerHTML = 'Shared with: ' + data.users.map(function(u) { return '<span class="sl-share-chip">@' + escapeHtml(u.username) + '</span>'; }).join('');
      else current.innerHTML = 'Specific-user sharing is selected, but no users are added yet.';
    }
  }

  function updateShareSpecificVisibility() {
    var selected = document.querySelector('input[name="slShareMode"]:checked');
    var specific = document.getElementById('slShareSpecific');
    if (specific) specific.style.display = selected && selected.value === 'specific' ? '' : 'none';
  }

  function saveShareDialog() {
    if (!currentDocId) return;
    var selected = document.querySelector('input[name="slShareMode"]:checked');
    var mode = selected ? selected.value : 'private';
    var users = document.getElementById('slShareUsers') ? document.getElementById('slShareUsers').value : '';
    fetch('/ajax/study-lab/document/' + currentDocId + '/share/', {
      method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}, credentials: 'same-origin',
      body: JSON.stringify({mode: mode, users: users})
    }).then(handleJson).then(function(data) {
      currentShareSettings = data;
      if (currentDocData && currentDocData.document) currentDocData.document.shareMode = data.mode;
      renderShareDialog(data);
      showSnackbar('Sharing updated');
    }).catch(function(err) {
      if (err.missing) showSnackbar('Some users were not found');
      else showSnackbar(err.message || 'Failed to update sharing');
    });
  }

  function copyStudyShareLink() {
    var link = document.getElementById('slShareLink');
    if (!link || !link.value) return;
    navigator.clipboard.writeText(link.value).then(function() { showSnackbar('Share link copied'); }).catch(function() { showSnackbar('Could not copy link'); });
  }

  function deleteDoc() {
    if (!currentDocId || !confirm('Delete this document and all its quizzes, summaries, mindmap, and flashcards?')) return;
    fetch('/ajax/study-lab/document/' + currentDocId + '/delete/', { method: 'POST', headers: {'X-CSRFToken': CSRF_TOKEN}, credentials: 'same-origin' })
      .then(handleJson)
      .then(function() {
        var item = document.querySelector('.sl-doc-item[data-doc-id="' + currentDocId + '"]');
        if (item) item.remove();
        currentDocId = null; currentDocData = null;
        document.getElementById('slDetail').style.display = 'none';
        document.getElementById('slWelcome').style.display = '';
        showSnackbar('Document deleted');
      })
      .catch(function(err) { showSnackbar(err.message || 'Failed to delete document'); });
  }

  function escapeHtml(text) {
    var div = document.createElement('div');
    div.textContent = text == null ? '' : String(text);
    return div.innerHTML;
  }

  function formatSize(bytes) {
    bytes = Number(bytes) || 0;
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
  }

  function renderMarkdown(text) {
    var html = typeof marked !== 'undefined' ? marked.parse(String(text || '')) : escapeHtml(text || '').replace(/\n/g, '<br>');
    return sanitizeRendered(html);
  }

  function sanitizeRendered(html) {
    var template = document.createElement('template');
    template.innerHTML = html;
    template.content.querySelectorAll('script,style,iframe,object,embed').forEach(function(el) { el.remove(); });
    template.content.querySelectorAll('*').forEach(function(el) {
      Array.prototype.slice.call(el.attributes).forEach(function(attr) {
        var name = attr.name.toLowerCase();
        var value = String(attr.value || '').trim().toLowerCase();
        if (name.indexOf('on') === 0 || value.indexOf('javascript:') === 0) el.removeAttribute(attr.name);
      });
    });
    return template.innerHTML;
  }

  document.querySelectorAll('input[name="slShareMode"]').forEach(function(radio) { radio.addEventListener('change', updateShareSpecificVisibility); });

  document.addEventListener('keydown', function(e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
    if (currentTab === 'quiz' && document.getElementById('slQuizActive').style.display !== 'none') {
      var key = e.key.toUpperCase();
      if (key === 'A' || key === 'B' || key === 'C' || key === 'D') {
        e.preventDefault();
        var q = quizQuestions[currentQuizIdx];
        if (q && !quizAnswers[q.id]) {
          quizAnswers[q.id] = key;
          renderQuizQuestion();
        }
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        if (currentQuizIdx > 0) { currentQuizIdx--; renderQuizQuestion(); }
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        if (currentQuizIdx < quizQuestions.length - 1) { currentQuizIdx++; renderQuizQuestion(); }
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (currentQuizIdx === quizQuestions.length - 1) submitQuiz();
        else if (currentQuizIdx < quizQuestions.length - 1) { currentQuizIdx++; renderQuizQuestion(); }
      }
    }
    if (currentTab === 'flashcards' && document.getElementById('slFlashDeck').style.display !== 'none') {
      if (e.key === ' ') {
        e.preventDefault();
        flipCard();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        if (currentFlashIdx > 0) { currentFlashIdx--; renderFlashcard(); }
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        if (currentFlashIdx < flashcards.length - 1) { currentFlashIdx++; renderFlashcard(); }
      } else if (e.key.toUpperCase() === 'H') {
        e.preventDefault();
        flashcardConfidence('hard');
      } else if (e.key.toUpperCase() === 'O') {
        e.preventDefault();
        flashcardConfidence('medium');
      } else if (e.key.toUpperCase() === 'E') {
        e.preventDefault();
        flashcardConfidence('easy');
      }
    }
  });

  registerActions({
    'sl-upload': function() { document.getElementById('slFileInput').click(); },
    'sl-select-doc': function(el) { selectDoc(el.dataset.docId); },
    'sl-switch-tab': function(el) { switchTab(el.dataset.tab); },
    'sl-summary-mode': function(el) { currentSummaryMode = el.dataset.mode === 'detailed' ? 'detailed' : 'compact'; renderSummaryPanel(); },
    'sl-generate-summary': function() { generateSummary(); },
    'sl-regenerate-summary': function() { generateSummary(); },
    'sl-edit-summary': function() { startSummaryEdit(); },
    'sl-save-summary': function() { saveSummaryEdit(); },
    'sl-cancel-summary-edit': function() { cancelSummaryEdit(); },
    'sl-open-share': function() { openShareDialog(); },
    'sl-close-share': function() { closeShareDialog(); },
    'sl-save-share': function() { saveShareDialog(); },
    'sl-copy-share-link': function() { copyStudyShareLink(); },
    'sl-generate-mindmap': function() { generateMindmap(); },
    'sl-regenerate-mindmap': function() { generateMindmap(); },
    'sl-mm-zoom-in': function() { if (window.NEBiansMindmap) window.NEBiansMindmap.setZoom(document.getElementById('slMindmapTree'), 0.12, currentDocData.mindmap); },
    'sl-mm-zoom-out': function() { if (window.NEBiansMindmap) window.NEBiansMindmap.setZoom(document.getElementById('slMindmapTree'), -0.12, currentDocData.mindmap); },
    'sl-mm-fit': function() { if (window.NEBiansMindmap) window.NEBiansMindmap.fitView(document.getElementById('slMindmapTree'), currentDocData.mindmap); },
    'sl-mm-export': function() { if (window.NEBiansMindmap) window.NEBiansMindmap.downloadPng(document.getElementById('slMindmapTree')); },
    'sl-generate-quiz': function() { generateQuiz(); },
    'sl-new-quiz': function() { showQuizPrompt(); },
    'sl-quiz-new': function() { showQuizPrompt(); },
    'sl-delete-doc': function() { deleteDoc(); },
    'sl-quiz-answer': function(el) { quizAnswers[el.dataset.qid] = el.dataset.answer; renderQuizQuestion(); },
    'sl-quiz-prev': function() { if (currentQuizIdx > 0) { currentQuizIdx--; renderQuizQuestion(); } },
    'sl-quiz-next': function() { if (currentQuizIdx < quizQuestions.length - 1) { currentQuizIdx++; renderQuizQuestion(); } },
    'sl-quiz-submit': function() { submitQuiz(); },
    'sl-quiz-retake': function() { startQuiz({id: currentQuizId, questions: quizQuestions, questionCount: quizQuestions.length}); },
    'sl-start-quiz': function(el) {
      fetch('/ajax/study-lab/quiz/' + el.dataset.quizId + '/', { headers: {'X-CSRFToken': CSRF_TOKEN}, credentials: 'same-origin' })
        .then(handleJson).then(function(data) { startQuiz(data.quiz); }).catch(function(err) { showSnackbar(err.message || 'Failed to load quiz'); });
    },
    'sl-generate-flashcards': function() { generateFlashcards(false); },
    'sl-flash-more': function() { generateFlashcards(true); },
    'sl-flip-card': function() { flipCard(); },
    'sl-flash-confidence': function(el) { flashcardConfidence(el.dataset.level); },
    'sl-flash-prev': function() { if (currentFlashIdx > 0) { currentFlashIdx--; renderFlashcard(); } },
    'sl-flash-next': function() { if (currentFlashIdx < flashcards.length - 1) { currentFlashIdx++; renderFlashcard(); } },
    'sl-retry-parse': function(el) { retryParse(el.dataset.docId); }
  });

  // ── Parse status polling ──
  function _pollParseStatus(docId) {
    setTimeout(function() {
      fetch('/ajax/study-lab/document/' + docId + '/parse-status/', { headers: {'X-CSRFToken': CSRF_TOKEN, 'Accept': 'application/json'}, credentials: 'same-origin' })
        .then(handleJson)
        .then(function(data) {
          if (data.error) return;
          var el = document.querySelector('.sl-doc-item[data-doc-id="' + docId + '"]');
          if (!el) return;
          var icon = el.querySelector('.sl-doc-icon');
          var ps = data.status || 'pending';
          if (ps === 'ready') {
            if (icon) { icon.textContent = 'description'; icon.classList.remove('sl-icon-spin'); }
            var statusEl = el.querySelector('.sl-doc-parse-status');
            if (statusEl) statusEl.remove();
          } else if (ps === 'failed') {
            if (icon) { icon.textContent = 'error'; icon.classList.remove('sl-icon-spin'); }
            var statusEl = el.querySelector('.sl-doc-parse-status');
            if (statusEl) { statusEl.textContent = 'Parse failed'; statusEl.className = 'sl-doc-parse-status sl-doc-failed'; }
          } else {
            if (ps === 'uploading') { if (icon) icon.textContent = 'hourglass_top'; }
            else if (ps === 'parsing') { if (icon) icon.textContent = 'hourglass_top'; }
            else if (ps === 'extracting') { if (icon) icon.textContent = 'hourglass_top'; }
            _pollParseStatus(docId);
          }
        })
        .catch(function() { _pollParseStatus(docId); });
    }, 3000);
  }

  function retryParse(docId) {
    fetch('/ajax/study-lab/document/' + docId + '/reparse/?force=true', {
      method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN}, credentials: 'same-origin'
    }).then(handleJson)
    .then(function(data) {
      if (data.error) { showSnackbar(data.error); return; }
      // Update icon and start polling
      var el = document.querySelector('.sl-doc-item[data-doc-id="' + docId + '"]');
      if (el) {
        var icon = el.querySelector('.sl-doc-icon');
        if (icon) { icon.textContent = 'hourglass_top'; icon.classList.add('sl-icon-spin'); }
        var statusEl = el.querySelector('.sl-doc-parse-status');
        if (statusEl) { statusEl.textContent = 'Parsing...'; statusEl.className = 'sl-doc-parse-status sl-doc-parsing'; }
      }
      _pollParseStatus(docId);
    })
    .catch(function() { showSnackbar('Failed to retry parsing'); });
  }
})();
