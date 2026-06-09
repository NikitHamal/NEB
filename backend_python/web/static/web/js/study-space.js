(function(){
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

  function csrf(){
    return document.querySelector('meta[name="csrf-token"]')?.content ||
      document.cookie.split('csrftoken=').pop()?.split(';')[0] || '';
  }

  function esc(t){
    var d=document.createElement('div'); d.textContent=t; return d.innerHTML;
  }

  function $(id){ return document.getElementById(id); }
  function $$(sel){ return document.querySelectorAll(sel); }

  function init(){
    var el = $('ssTitle');
    if(!el) return;
    SPACE_ID = el.dataset.spaceId || window.location.pathname.split('/')[2];
    if(!SPACE_ID) return;
    loadSpace();
  }

  function loadSpace(){
    fetch('/ajax/study-space/'+SPACE_ID+'/',{headers:{'X-CSRFToken':csrf(),'Accept':'application/json'}})
    .then(function(r){return r.json()})
    .then(function(data){
      SPACE_DATA = data;
      renderFiles();
      renderLinkedGen();
      loadExistingContent();
    })
    .catch(function(e){ console.error('Failed to load space:',e); });
  }

  function renderFiles(){
    var list = $('ssFileList');
    if(!list) return;
    var docs = SPACE_DATA.documents || [];
    if(!docs.length){
      list.innerHTML = '<div style="text-align:center;padding:12px;color:var(--md-on-surface-variant);font-size:0.8125rem;">No documents yet</div>';
      return;
    }
    var html = '';
    docs.forEach(function(d){
      var icon = d.status==='ready'?'description':d.status==='processing'?'hourglass_top':'error';
      html += '<div class="ss-file-item" data-doc-id="'+d.id+'">'
        + '<span class="material-symbols-outlined">'+icon+'</span>'
        + '<span class="ss-file-name">'+esc(d.title||d.fileName||'Untitled')+'</span>'
        + '<button class="ss-file-remove" data-action="ss-remove-doc" data-doc-id="'+d.id+'" title="Remove"><span class="material-symbols-outlined">close</span></button>'
        + '</div>';
    });
    list.innerHTML = html;
  }

  function renderLinkedGen(){
    var section = $('ssLinkedGen');
    if(!section) return;
    var docs = SPACE_DATA.documents || [];
    section.style.display = docs.length ? '' : 'none';
  }

  function loadExistingContent(){
    if(SPACE_DATA.linkSummaryCompact || SPACE_DATA.linkSummaryDetailed){
      showSummary(SPACE_DATA.linkSummaryDetailed || SPACE_DATA.linkSummaryCompact);
    }
    if(SPACE_DATA.linkMindmapJson){
      try{
        MINDMAP_DATA = JSON.parse(SPACE_DATA.linkMindmapJson);
        showMindmap(MINDMAP_DATA);
      }catch(e){}
    }
  }

  // ── Tab switching ──
  document.addEventListener('click',function(e){
    var el=e.target.closest('[data-action]');
    if(!el) return;
    var action=el.getAttribute('data-action');

    switch(action){
      case 'ss-switch-tab':
        switchTab(el.dataset.tab);
        break;
      case 'ss-summary-mode':
        SUMMARY_MODE = el.dataset.mode;
        $$('.ss-mode-btn').forEach(function(b){b.classList.remove('ss-mode-active')});
        el.classList.add('ss-mode-active');
        $('ssSummaryGenerateLabel').textContent = SUMMARY_MODE==='detailed'?'Generate Detailed Summary':'Generate Summary';
        $('ssSummaryPromptText').textContent = SUMMARY_MODE==='detailed'?'Generate a detailed, comprehensive summary from all documents.':'Generate a compact, high-yield summary from all documents.';
        break;
      case 'ss-generate-summary':
        generateSummary();
        break;
      case 'ss-edit-summary':
        $('ssSummaryEditor').style.display='block';
        $('ssSummaryTextarea').value = $('ssSummaryText').innerText;
        break;
      case 'ss-save-summary':
        saveSummary();
        break;
      case 'ss-cancel-summary-edit':
        $('ssSummaryEditor').style.display='none';
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
        generateQuiz();
        break;
      case 'ss-generate-flashcards':
        generateFlashcards();
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
      case 'ss-close-select-doc':
        $('ssSelectDocModal').style.display='none';
        break;
      case 'ss-submit-select-doc':
        submitDocSelection();
        break;
      case 'ss-share':
        openShareModal();
        break;
      case 'ss-close-share':
        $('ssShareModal').style.display='none';
        break;
      case 'ss-copy-share-link':
        var link=$('ssShareLink'); link.select(); document.execCommand('copy');
        break;
      case 'ss-save-share':
        saveShare();
        break;
      case 'ss-rename':
        openRenameModal();
        break;
      case 'ss-close-rename':
        $('ssRenameModal').style.display='none';
        break;
      case 'ss-submit-rename':
        submitRename();
        break;
      case 'ss-delete-space':
        $('ssDeleteModal').style.display='flex';
        break;
      case 'ss-close-delete':
        $('ssDeleteModal').style.display='none';
        break;
      case 'ss-confirm-delete':
        deleteSpace();
        break;
      // Mindmap zoom
      case 'ss-mm-zoom-in':
        if(window.studyMindmap) window.studyMindmap.zoomIn();
        break;
      case 'ss-mm-zoom-out':
        if(window.studyMindmap) window.studyMindmap.zoomOut();
        break;
      case 'ss-mm-fit':
        if(window.studyMindmap) window.studyMindmap.fitToView();
        break;
      case 'ss-mm-export':
        if(window.studyMindmap) window.studyMindmap.exportPNG();
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
        if(card) card.classList.toggle('sl-flash-flipped');
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
    }
  });

  // ── Share modal radio toggle ──
  document.addEventListener('change',function(e){
    if(e.target.name==='ssShareMode'){
      $('ssShareSpecific').style.display = e.target.value==='specific'?'block':'none';
      var linkBox = e.target.closest('.modal-box')?.querySelector('.sl-share-linkbox');
      if(linkBox) linkBox.style.display = e.target.value==='private'?'none':'block';
    }
  });

  // ── Upload ──
  document.addEventListener('DOMContentLoaded',function(){
    var fi=$('ssFileInput');
    if(fi) fi.addEventListener('change',function(){
      if(this.files.length) uploadFile(this.files[0]);
      this.value='';
    });
  });

  function uploadFile(file){
    $('ssUploadProgress').style.display='flex';
    $('ssUploadProgressBar').style.width='0%';
    $('ssUploadProgressPercent').textContent='0%';
    $('ssUploadProgressSubtitle').textContent='Uploading '+file.name+'...';
    var fd=new FormData();
    fd.append('file',file);
    var xhr=new XMLHttpRequest();
    xhr.open('POST','/ajax/study-space/'+SPACE_ID+'/upload/');
    xhr.setRequestHeader('X-CSRFToken',csrf());
    xhr.upload.onprogress=function(e){
      if(e.lengthComputable){
        var pct=Math.round(e.loaded/e.total*100);
        $('ssUploadProgressBar').style.width=pct+'%';
        $('ssUploadProgressPercent').textContent=pct+'%';
      }
    };
    xhr.onload=function(){
      $('ssUploadProgress').style.display='none';
      if(xhr.status>=200&&xhr.status<300){
        loadSpace();
      } else {
        try{ var d=JSON.parse(xhr.responseText); alert(d.error||'Upload failed'); }catch(e){ alert('Upload failed'); }
      }
    };
    xhr.onerror=function(){
      $('ssUploadProgress').style.display='none';
      alert('Upload failed — network error');
    };
    xhr.send(fd);
  }

  function removeDoc(docId){
    if(!confirm('Remove this document from the space?')) return;
    fetch('/ajax/study-space/'+SPACE_ID+'/document/'+docId+'/remove/',{
      method:'POST', headers:{'X-CSRFToken':csrf(),'Content-Type':'application/json'}
    }).then(function(r){return r.json()})
    .then(function(data){
      if(data.error) alert(data.error);
      else loadSpace();
    });
  }

  // ── Tab switching ──
  function switchTab(tab){
    CURRENT_TAB = tab;
    $$('.ss-tab').forEach(function(t){ t.classList.toggle('ss-tab-active', t.dataset.tab===tab); });
    $$('.ss-tab-content').forEach(function(c){ c.classList.remove('ss-tab-content-active'); });
    var panel = $('ssTab'+tab.charAt(0).toUpperCase()+tab.slice(1));
    if(panel) panel.classList.add('ss-tab-content-active');
  }

  // ── Summary ──
  function generateSummary(){
    $('ssSummaryPrompt').style.display='none';
    $('ssSummaryLoading').style.display='block';
    $('ssSummaryContent').style.display='none';
    fetch('/ajax/study-space/'+SPACE_ID+'/summary/',{
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf()},
      body:JSON.stringify({mode:SUMMARY_MODE})
    }).then(function(r){return r.json()})
    .then(function(data){
      $('ssSummaryLoading').style.display='none';
      if(data.error){ $('ssSummaryPrompt').style.display=''; alert(data.error); return; }
      showSummary(data.summary);
      SPACE_DATA.linkSummaryCompact = data.summaryCompact || data.summary;
      SPACE_DATA.linkSummaryDetailed = data.summaryDetailed || data.summary;
    }).catch(function(e){
      $('ssSummaryLoading').style.display='none';
      $('ssSummaryPrompt').style.display='';
      alert('Failed to generate summary');
    });
  }

  function showSummary(text){
    $('ssSummaryPrompt').style.display='none';
    $('ssSummaryContent').style.display='block';
    $('ssSummaryText').innerHTML = renderMarkdown(text);
    renderMathInElement($('ssSummaryText'));
  }

  function renderMarkdown(text){
    if(!text) return '';
    var html = esc(text);
    html = html.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>');
    html = html.replace(/\*(.+?)\*/g,'<em>$1</em>');
    html = html.replace(/^### (.+)$/gm,'<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm,'<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm,'<h1>$1</h1>');
    html = html.replace(/^- (.+)$/gm,'<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/s,'<ul>$1</ul>');
    html = html.replace(/\n\n/g,'</p><p>');
    html = html.replace(/\n/g,'<br>');
    return '<p>'+html+'</p>';
  }

  function renderMathInElement(el){
    if(typeof renderMathInElement==='function'){
      renderMathInElement(el,{
        delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],
        throwOnError:false
      });
    }
  }

  function saveSummary(){
    var text=$('ssSummaryTextarea').value.trim();
    if(!text){ alert('Summary cannot be empty'); return; }
    fetch('/ajax/study-space/'+SPACE_ID+'/summary/edit/',{
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf()},
      body:JSON.stringify({summary:text, mode:SUMMARY_MODE})
    }).then(function(r){return r.json()})
    .then(function(data){
      if(data.error){ alert(data.error); return; }
      $('ssSummaryEditor').style.display='none';
      showSummary(data.summary);
    });
  }

  // ── Mindmap ──
  function generateMindmap(){
    $('ssMindmapPrompt').style.display='none';
    $('ssMindmapLoading').style.display='block';
    $('ssMindmapContent').style.display='none';
    fetch('/ajax/study-space/'+SPACE_ID+'/mindmap/',{
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf()}
    }).then(function(r){return r.json()})
    .then(function(data){
      $('ssMindmapLoading').style.display='none';
      if(data.error){ $('ssMindmapPrompt').style.display=''; alert(data.error); return; }
      MINDMAP_DATA = data.mindmap;
      showMindmap(data.mindmap);
    }).catch(function(e){
      $('ssMindmapLoading').style.display='none';
      $('ssMindmapPrompt').style.display='';
      alert('Failed to generate mindmap');
    });
  }

  function showMindmap(data){
    if(!data) return;
    $('ssMindmapPrompt').style.display='none';
    $('ssMindmapContent').style.display='block';
    var tree=$('ssMindmapTree');
    if(tree && window.StudyMindmap){
      window.studyMindmap = new StudyMindmap(tree, data);
    } else if(tree){
      tree.innerHTML = '<pre style="white-space:pre-wrap;font-size:0.8125rem;">'+esc(JSON.stringify(data,null,2))+'</pre>';
    }
  }

  // ── Quiz ──
  function generateQuiz(){
    $('ssQuizPrompt').style.display='none';
    $('ssQuizLoading').style.display='block';
    $('ssQuizActive').style.display='none';
    $('ssQuizResults').style.display='none';
    var count = parseInt($('ssQuizCount')?.value||'10');
    fetch('/ajax/study-space/'+SPACE_ID+'/quiz/',{
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf()},
      body:JSON.stringify({count:count})
    }).then(function(r){return r.json()})
    .then(function(data){
      $('ssQuizLoading').style.display='none';
      if(data.error){ $('ssQuizPrompt').style.display=''; alert(data.error); return; }
      QUIZ_DATA = data.quiz;
      QUIZ_ANSWERS = {};
      QUIZ_CURRENT = 0;
      renderQuiz();
    }).catch(function(e){
      $('ssQuizLoading').style.display='none';
      $('ssQuizPrompt').style.display='';
      alert('Failed to generate quiz');
    });
  }

  function renderQuiz(){
    if(!QUIZ_DATA) return;
    $('ssQuizActive').style.display='block';
    var qs = QUIZ_DATA.questions||[];
    if(!qs.length){ $('ssQuizActive').innerHTML='<p>No questions generated.</p>'; return; }
    var q = qs[QUIZ_CURRENT];
    var answered = Object.keys(QUIZ_ANSWERS).length;
    $('ssQuizActive').innerHTML = '<div class="sl-quiz-progress"><span>Question '+(QUIZ_CURRENT+1)+' of '+qs.length+'</span><span>Answered: '+answered+'</span></div>'
      + '<div class="sl-quiz-question">'+esc(q.questionText)+'</div>'
      + '<div class="sl-quiz-options-list">'
      + formatOption('A',q.optionA,QUIZ_ANSWERS[q.id]==='A')
      + formatOption('B',q.optionB,QUIZ_ANSWERS[q.id]==='B')
      + formatOption('C',q.optionC,QUIZ_ANSWERS[q.id]==='C')
      + formatOption('D',q.optionD,QUIZ_ANSWERS[q.id]==='D')
      + '</div>'
      + '<div class="sl-quiz-nav">'
      + '<button class="md-btn md-btn-outlined" data-action="ss-quiz-prev" '+(QUIZ_CURRENT===0?'disabled':'')+'>Previous</button>'
      + '<button class="md-btn md-btn-filled" data-action="ss-quiz-next" '+(QUIZ_CURRENT>=qs.length-1?'disabled':'')+'>Next</button>'
      + '<button class="md-btn md-btn-filled" data-action="ss-quiz-submit" '+(answered<qs.length?'':'')+'>Submit Quiz</button>'
      + '</div>';
  }

  function formatOption(letter,text,selected){
    var sel = selected?' sl-quiz-opt-selected':'';
    return '<div class="sl-quiz-opt'+sel+'" data-action="ss-quiz-select" data-qid="" data-answer="'+letter+'">'
      +'<span class="sl-quiz-opt-letter">'+letter+'</span><span>'+esc(text)+'</span></div>';
  }

  // ── Flashcards ──
  function generateFlashcards(){
    $('ssFlashPrompt').style.display='none';
    $('ssFlashLoading').style.display='block';
    $('ssFlashDeck').style.display='none';
    var count = parseInt($('ssFlashCount')?.value||'8');
    fetch('/ajax/study-space/'+SPACE_ID+'/flashcards/',{
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf()},
      body:JSON.stringify({count:count})
    }).then(function(r){return r.json()})
    .then(function(data){
      $('ssFlashLoading').style.display='none';
      if(data.error){ $('ssFlashPrompt').style.display=''; alert(data.error); return; }
      FLASHCARDS = data.flashcards||[];
      FLASH_INDEX = 0;
      renderFlashcard();
    }).catch(function(e){
      $('ssFlashLoading').style.display='none';
      $('ssFlashPrompt').style.display='';
      alert('Failed to generate flashcards');
    });
  }

  function renderFlashcard(){
    if(!FLASHCARDS.length){ $('ssFlashDeck').style.display='none'; return; }
    $('ssFlashDeck').style.display='block';
    var c = FLASHCARDS[FLASH_INDEX];
    $('ssFlashDeck').innerHTML = '<div class="sl-flash-topbar">'
      + '<div class="sl-flash-counter">'+(FLASH_INDEX+1)+' / '+FLASHCARDS.length+'</div>'
      + '<button class="md-btn md-btn-tonal" data-action="ss-flash-more"><span class="material-symbols-outlined">add</span> More cards</button>'
      + '</div>'
      + '<div class="sl-flash-card" data-action="ss-flip-card">'
      + '<div class="sl-flash-card-inner">'
      + '<div class="sl-flash-front"><span class="sl-flash-label">Question</span><p>'+esc(c.front)+'</p></div>'
      + '<div class="sl-flash-back"><span class="sl-flash-label">Answer</span><p>'+esc(c.back)+'</p></div>'
      + '</div></div>'
      + '<div class="sl-flash-confidence">'
      + '<button class="sl-conf-btn sl-conf-hard" data-action="ss-flash-confidence" data-level="hard"><span class="material-symbols-outlined">close</span> Hard</button>'
      + '<button class="sl-conf-btn sl-conf-medium" data-action="ss-flash-confidence" data-level="medium"><span class="material-symbols-outlined">remove</span> Okay</button>'
      + '<button class="sl-conf-btn sl-conf-easy" data-action="ss-flash-confidence" data-level="easy"><span class="material-symbols-outlined">check</span> Easy</button>'
      + '</div>'
      + '<div class="sl-flash-nav">'
      + '<button class="md-btn md-btn-outlined" data-action="ss-flash-prev" '+(FLASH_INDEX===0?'disabled':'')+'><span class="material-symbols-outlined">arrow_back</span> Previous</button>'
      + '<button class="md-btn md-btn-outlined" data-action="ss-flash-next" '+(FLASH_INDEX>=FLASHCARDS.length-1?'disabled':'')+'>Next <span class="material-symbols-outlined">arrow_forward</span></button>'
      + '</div>';
  }

  function flashNav(dir){
    FLASH_INDEX = Math.max(0, Math.min(FLASHCARDS.length-1, FLASH_INDEX+dir));
    renderFlashcard();
  }

  function flashConfidence(level){
    if(!FLASHCARDS.length) return;
    var c = FLASHCARDS[FLASH_INDEX];
    fetch('/ajax/study-space/flashcard/'+c.id+'/review/',{
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf()},
      body:JSON.stringify({confidence:level})
    });
    if(FLASH_INDEX < FLASHCARDS.length-1){
      FLASH_INDEX++;
      renderFlashcard();
    }
  }

  function quizNav(dir){
    if(!QUIZ_DATA) return;
    QUIZ_CURRENT = Math.max(0, Math.min(QUIZ_DATA.questions.length-1, QUIZ_CURRENT+dir));
    renderQuiz();
  }

  function submitQuiz(){
    if(!QUIZ_DATA) return;
    fetch('/ajax/study-space/quiz/'+QUIZ_DATA.id+'/submit/',{
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf()},
      body:JSON.stringify({answers:QUIZ_ANSWERS})
    }).then(function(r){return r.json()})
    .then(function(data){
      if(data.error){ alert(data.error); return; }
      showQuizResults(data.attempt);
    });
  }

  function showQuizResults(attempt){
    $('ssQuizActive').style.display='none';
    $('ssQuizResults').style.display='block';
    var html = '<div class="sl-quiz-results-header">'
      + '<span class="material-symbols-outlined" style="font-size:48px;color:var(--md-primary);">emoji_events</span>'
      + '<h2>Quiz Complete</h2>'
      + '<div class="sl-quiz-score-display"><span class="sl-quiz-score-num">'+attempt.score+'</span><span class="sl-quiz-score-total">/'+attempt.totalQuestions+'</span></div>'
      + '<div class="sl-quiz-xp">+'+attempt.xpEarned+' XP</div></div>'
      + '<div class="sl-quiz-results-list">';
    (attempt.answers||[]).forEach(function(a){
      var icon = a.isCorrect?'check_circle':'cancel';
      var color = a.isCorrect?'var(--md-primary)':'var(--md-error)';
      html += '<div class="sl-quiz-result-item" style="color:'+color+'"><span class="material-symbols-outlined">'+icon+'</span> '
        + esc(a.questionId) + ' — Your answer: '+a.given+' (Correct: '+a.correct+')</div>';
    });
    html += '</div><div class="sl-quiz-results-actions">'
      + '<button class="md-btn md-btn-outlined" data-action="ss-quiz-retake">Retake Quiz</button>'
      + '<button class="md-btn md-btn-tonal" data-action="ss-quiz-new">Generate New Quiz</button>'
      + '</div>';
    $('ssQuizResults').innerHTML = html;
  }

  function retakeQuiz(){
    QUIZ_ANSWERS = {};
    QUIZ_CURRENT = 0;
    $('ssQuizResults').style.display='none';
    renderQuiz();
  }

  // ── Share ──
  function openShareModal(){
    if(!SPACE_DATA) return;
    var modal = $('ssShareModal');
    var radios = modal.querySelectorAll('input[name="ssShareMode"]');
    radios.forEach(function(r){ r.checked = r.value===SPACE_DATA.shareMode; });
    $('ssShareSpecific').style.display = SPACE_DATA.shareMode==='specific'?'block':'none';
    var linkBox = modal.querySelector('.sl-share-linkbox');
    if(linkBox) linkBox.style.display = SPACE_DATA.shareMode!=='private'?'block':'none';
    if(SPACE_DATA.shareToken){
      $('ssShareLink').value = window.location.origin+'/study-space/shared/'+SPACE_DATA.shareToken+'/';
    }
    modal.style.display='flex';
  }

  function saveShare(){
    var modal = $('ssShareModal');
    var mode = modal.querySelector('input[name="ssShareMode"]:checked').value;
    var users = [];
    if(mode==='specific'){
      users = $('ssShareUsers').value.split(',').map(function(u){return u.trim()}).filter(Boolean);
    }
    fetch('/ajax/study-space/'+SPACE_ID+'/share/',{
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf()},
      body:JSON.stringify({mode:mode, users:users})
    }).then(function(r){return r.json()})
    .then(function(data){
      if(data.error){ alert(data.error); return; }
      SPACE_DATA = data;
      modal.style.display='none';
      if(data.shareToken){
        $('ssShareLink').value = window.location.origin+'/study-space/shared/'+data.shareToken+'/';
      }
    });
  }

  // ── Rename ──
  function openRenameModal(){
    $('ssRenameTitle').value = SPACE_DATA.title||'';
    $('ssRenameDesc').value = SPACE_DATA.description||'';
    $('ssRenameModal').style.display='flex';
  }

  function submitRename(){
    var title = $('ssRenameTitle').value.trim();
    var desc = $('ssRenameDesc').value.trim();
    fetch('/ajax/study-space/'+SPACE_ID+'/update/',{
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf()},
      body:JSON.stringify({title:title, description:desc})
    }).then(function(r){return r.json()})
    .then(function(data){
      if(data.error){ alert(data.error); return; }
      SPACE_DATA = data;
      $('ssTitle').textContent = data.title||'Untitled Space';
      $('ssRenameModal').style.display='none';
    });
  }

  // ── Delete ──
  function deleteSpace(){
    fetch('/ajax/study-space/'+SPACE_ID+'/delete/',{
      method:'POST',
      headers:{'X-CSRFToken':csrf()}
    }).then(function(r){return r.json()})
    .then(function(data){
      if(data.success) window.location.href='/study-lab/';
      else alert(data.error||'Failed to delete');
    });
  }

  // ── Document selection ──
  var selectedDocId = null;
  var docSelectTab = 'docs';

  function openDocSelectModal(){
    var modal = $('ssSelectDocModal');
    var list = $('ssDocSelectList');
    var rlist = $('ssResourceSelectList');
    list.innerHTML = '<div class="ss-doc-select-empty"><span class="material-symbols-outlined">hourglass_top</span><p>Loading documents...</p></div>';
    rlist.innerHTML = '<div class="ss-doc-select-empty"><span class="material-symbols-outlined">hourglass_top</span><p>Loading resources...</p></div>';
    selectedDocId = null;
    modal.style.display='flex';
    loadDocSelectDocs();
    loadDocSelectResources();
  }

  function loadDocSelectDocs(){
    var list = $('ssDocSelectList');
    fetch('/ajax/study-space/'+SPACE_ID+'/document/list/',{headers:{'X-CSRFToken':csrf(),'Accept':'application/json'}})
    .then(function(r){return r.json()})
    .then(function(data){
      var docs = data.documents || [];
      if(!docs.length){
        list.innerHTML = '<div class="ss-doc-select-empty"><span class="material-symbols-outlined">description</span><p>No study documents yet</p></div>';
        return;
      }
      var html = '';
      docs.forEach(function(d){
        var icon = d.status==='ready'?'description':'error';
        var inSpace = d.spaceId === SPACE_ID;
        var selClass = inSpace ? ' selected' : '';
        var meta = [];
        if(d.fileName) meta.push(d.fileName);
        if(d.fileSize) meta.push((d.fileSize/1024).toFixed(0)+'KB');
        html += '<div class="ss-doc-select-item'+selClass+'" data-doc-id="'+d.id+'" data-doc-type="studydoc" data-action="ss-select-doc-item">'
          + '<span class="material-symbols-outlined">'+icon+'</span>'
          + '<div class="ss-doc-select-info">'
          + '<span class="ss-doc-select-title">'+esc(d.title)+'</span>'
          + (meta.length ? '<span class="ss-doc-select-meta">'+esc(meta.join(' · '))+'</span>' : '')
          + '</div>'
          + (inSpace ? '<span class="material-symbols-outlined ss-doc-select-check">check_circle</span>' : '')
          + '</div>';
      });
      list.innerHTML = html;
    }).catch(function(e){
      list.innerHTML = '<div class="ss-doc-select-empty"><span class="material-symbols-outlined">error</span><p>Failed to load documents.</p></div>';
    });
  }

  function loadDocSelectResources(){
    var list = $('ssResourceSelectList');
    fetch('/ajax/study-space/'+SPACE_ID+'/resource/list/',{headers:{'X-CSRFToken':csrf(),'Accept':'application/json'}})
    .then(function(r){return r.json()})
    .then(function(data){
      var resources = data.resources || [];
      if(!resources.length){
        list.innerHTML = '<div class="ss-doc-select-empty"><span class="material-symbols-outlined">folder_off</span><p>No resources uploaded yet</p></div>';
        return;
      }
      var html = '';
      resources.forEach(function(r){
        var icon = r.type==='PDF'?'picture_as_pdf':r.type==='Video'?'play_circle':'article';
        var meta = [];
        if(r.subject) meta.push(r.subject);
        if(r.type) meta.push(r.type);
        if(r.fileSize) meta.push((r.fileSize/1024).toFixed(0)+'KB');
        html += '<div class="ss-doc-select-item" data-resource-id="'+r.id+'" data-doc-type="resource" data-action="ss-select-doc-item">'
          + '<span class="material-symbols-outlined">'+icon+'</span>'
          + '<div class="ss-doc-select-info">'
          + '<span class="ss-doc-select-title">'+esc(r.title)+'</span>'
          + (meta.length ? '<span class="ss-doc-select-meta">'+esc(meta.join(' · '))+'</span>' : '')
          + '</div>'
          + '</div>';
      });
      list.innerHTML = html;
    }).catch(function(e){
      list.innerHTML = '<div class="ss-doc-select-empty"><span class="material-symbols-outlined">error</span><p>Failed to load resources.</p></div>';
    });
  }

  function submitDocSelection(){
    if(!selectedDocId){ alert('Please select an item'); return; }
    var selectedItem = document.querySelector('.ss-doc-select-item.selected');
    var docType = selectedItem ? selectedItem.dataset.docType : 'studydoc';
    var url, body;
    if(docType === 'resource'){
      url = '/ajax/study-space/'+SPACE_ID+'/resource/add/';
      body = JSON.stringify({resource_id: selectedDocId});
    } else {
      url = '/ajax/study-space/'+SPACE_ID+'/document/add/';
      body = JSON.stringify({document_id: selectedDocId});
    }
    fetch(url,{
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf()},
      body: body
    }).then(function(r){return r.json()})
    .then(function(data){
      if(data.error){ alert(data.error); return; }
      $('ssSelectDocModal').style.display='none';
      loadSpace();
    });
  }

  document.addEventListener('click',function(e){
    var item = e.target.closest('.ss-doc-select-item');
    if(item){
      $$('.ss-doc-select-item').forEach(function(i){ i.classList.remove('selected'); });
      item.classList.add('selected');
      selectedDocId = item.dataset.docId || item.dataset.resourceId;
      return;
    }
    var tab = e.target.closest('[data-action="ss-doc-tab"]');
    if(tab){
      docSelectTab = tab.dataset.tab;
      $$('.ss-doc-tab').forEach(function(t){ t.classList.toggle('ss-doc-tab-active', t.dataset.tab===docSelectTab); });
      $('ssDocSelectList').style.display = docSelectTab==='docs'?'':'none';
      $('ssResourceSelectList').style.display = docSelectTab==='resources'?'':'none';
      selectedDocId = null;
      $$('.ss-doc-select-item').forEach(function(i){ i.classList.remove('selected'); });
    }
  });

  // ── Quiz option selection (event delegation) ──
  document.addEventListener('click',function(e){
    var opt = e.target.closest('.sl-quiz-opt');
    if(!opt) return;
    var qid = opt.dataset.qid;
    var answer = opt.dataset.answer;
    if(QUIZ_DATA && QUIZ_DATA.questions && QUIZ_DATA.questions[QUIZ_CURRENT]){
      qid = QUIZ_DATA.questions[QUIZ_CURRENT].id;
    }
    if(qid) QUIZ_ANSWERS[qid] = answer;
    renderQuiz();
  });

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);
  else init();
})();