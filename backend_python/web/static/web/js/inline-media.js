'use strict';
;(function () {
  var TOKEN_RE = /\[\[img:(\d{1,10})\]\]/g;

  var SKIP_SELECTOR = '[data-neb-skip],#neby-input,#chat-input,#bs-followup,#ba-goal,'
    + '#agent_chat_input,#agent_new_task,#agent_home_task_input,'
    + '#ssTutorQuestion,#cbAiInput,.ss-ai-input,.cb-ai-input,'
    + '.reply-input-wrapper textarea,.reply-input-wrapper,#mainReplyContent,#threadSidebarTextarea,#threadSheetTextarea';

  function isSkipped(el) {
    if (!el || el.nodeType !== 1) return false;
    if (el.hasAttribute && el.hasAttribute('data-neb-skip')) return true;
    try {
      if (el.closest && (el.closest('[data-neb-skip]') || el.closest('.reply-input-wrapper') || el.closest('.fp-compose'))) return true;
      if (el.matches && el.matches(SKIP_SELECTOR)) return true;
    } catch (_) {}
    return false;
  }

  function isEnabled() {
    if (typeof window.NEB_INLINE_ENABLED === 'boolean') return window.NEB_INLINE_ENABLED;
    try { var v = localStorage.getItem('neb_inline_enabled'); if (v === '0') return false; if (v === '1') return true; } catch(_){}
    return true;
  }

  function esc(s) {
    var d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }
  function imageUrl(id) {
    return '/media/content_images/' + id + '.webp';
  }
  function thumbUrl(id) {
    return '/media/content_images/' + id + 't.webp';
  }

  function extractIds(text) {
    var re = new RegExp(TOKEN_RE, 'g'), ids = [], seen = {}, m;
    while ((m = re.exec(text || ''))) {
      var iid = m[1];
      if (!seen[iid]) { seen[iid] = 1; ids.push(+iid); }
    }
    return ids;
  }

  function plainText(text) {
    return (text || '').replace(new RegExp(TOKEN_RE, 'g'), '[image]');
  }
  function stripTokens(text) {
    return (text || '').replace(new RegExp(TOKEN_RE, 'g'), '');
  }

  function chipHtml(id, opts) {
    var full = imageUrl(id);
    var thumb = thumbUrl(id);
    var extra = (opts && opts.editor) ? ' neb-chip-editor' : '';
    var removeBtn = extra ? '<button type="button" class="neb-chip-remove" data-neb-remove="' + esc('' + id) + '" aria-label="Remove image"><span class="material-symbols-outlined">close</span></button>' : '';
    return (
      '<span class="neb-chip' + extra + '" data-neb-img="' + esc('' + id) + '"' +
      ' data-neb-full="' + esc(full) + '" draggable="true" contenteditable="false" role="button" tabindex="0" aria-label="Attached image">' +
      '<img src="' + esc(thumb) + '" alt="Image" loading="lazy" decoding="async">' + removeBtn + '</span>'
    );
  }

  function chipElement(id, opts) {
    var wrap = document.createElement('div');
    wrap.innerHTML = chipHtml(id, opts || {});
    return wrap.firstElementChild;
  }

  function splitRender(text, piecer) {
    if (!text) return '';
    var re = new RegExp(TOKEN_RE, 'g'), out = [], last = 0, m;
    while ((m = re.exec(text))) {
      if (m.index > last) out.push(piecer(text.slice(last, m.index)));
      out.push(chipHtml(parseInt(m[1], 10)));
      last = m.index + m[0].length;
    }
    if (last < text.length) out.push(piecer(text.slice(last)));
    return out.join('');
  }

  function showSnackbar(msg) {
    if (typeof window.showSnackbar === 'function') return window.showSnackbar(msg);
    if (typeof window.showToast === 'function') return window.showToast(msg);
  }

  var _activeLightbox = null;
  function openLightbox(url) {
    if (_activeLightbox) _activeLightbox.remove();
    var ov = document.createElement('div');
    ov.className = 'neb-lightbox';
    ov.setAttribute('role', 'dialog');
    ov.setAttribute('aria-label', 'Image preview');
    var frame = document.createElement('div');
    frame.className = 'neb-lightbox-frame';
    var img = document.createElement('img');
    img.className = 'neb-lightbox-img';
    img.src = url;
    img.alt = 'Image';
    frame.appendChild(img);
    var bar = document.createElement('div');
    bar.className = 'neb-lightbox-bar';
    var closeBtn = document.createElement('button');
    closeBtn.className = 'neb-lightbox-btn';
    closeBtn.title = 'Close';
    closeBtn.innerHTML = '<span class="material-symbols-outlined">close</span>';
    closeBtn.setAttribute('aria-label', 'Close');
    var dlBtn = document.createElement('a');
    dlBtn.className = 'neb-lightbox-btn';
    dlBtn.href = url;
    dlBtn.target = '_blank';
    dlBtn.rel = 'noopener';
    dlBtn.title = 'Open original';
    dlBtn.setAttribute('aria-label', 'Open original');
    dlBtn.innerHTML = '<span class="material-symbols-outlined">open_in_new</span>';
    bar.appendChild(dlBtn);
    bar.appendChild(closeBtn);
    var hint = document.createElement('div');
    hint.className = 'neb-lightbox-hint';
    hint.textContent = 'Scroll to zoom - drag to pan - Esc to close';
    ov.appendChild(frame);
    ov.appendChild(bar);
    ov.appendChild(hint);
    document.body.appendChild(ov);
    document.body.style.overflow = 'hidden';
    _activeLightbox = ov;

    var scale = 1, tx = 0, ty = 0, panning = false, startX = 0, startY = 0;
    function apply() {
      img.style.transform = 'translate(' + tx + 'px,' + ty + 'px) scale(' + scale + ')';
    }
    function resetZoom() { scale = 1; tx = 0; ty = 0; apply(); }
    ov.addEventListener('wheel', function (e) {
      e.preventDefault();
      var delta = e.deltaY > 0 ? -0.12 : 0.12;
      scale = Math.max(0.2, Math.min(8, scale * (1 + delta)));
      apply();
    }, { passive: false });
    img.addEventListener('dblclick', function (e) {
      e.stopPropagation();
      if (scale > 1.05) resetZoom(); else { scale = 2.4; apply(); }
    });
    frame.addEventListener('pointerdown', function (e) {
      if (e.button !== 0) return;
      panning = true;
      startX = e.clientX - tx;
      startY = e.clientY - ty;
      try { frame.setPointerCapture(e.pointerId); } catch (_) {}
      e.preventDefault();
    });
    frame.addEventListener('pointermove', function (e) {
      if (!panning) return;
      tx = e.clientX - startX;
      ty = e.clientY - startY;
      apply();
    });
    function stopPan(e) {
      if (!panning) return;
      panning = false;
      try { frame.releasePointerCapture(e.pointerId); } catch (_) {}
    }
    frame.addEventListener('pointerup', stopPan);
    frame.addEventListener('pointercancel', stopPan);
    var pinchDist = 0;
    ov.addEventListener('touchmove', function (e) {
      if (e.touches.length === 2) {
        e.preventDefault();
        var d = Math.hypot(e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY);
        if (pinchDist && d) { scale = Math.max(0.2, Math.min(8, scale * (d / pinchDist))); apply(); }
        pinchDist = d;
      }
    }, { passive: false });
    ov.addEventListener('touchstart', function (e) {
      if (e.touches.length === 2) {
        pinchDist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY);
      }
    });
    ov.addEventListener('touchend', function () { pinchDist = 0; });

    function close() {
      ov.remove();
      document.body.style.overflow = '';
      if (_activeLightbox === ov) _activeLightbox = null;
      document.removeEventListener('keydown', onKey);
    }
    function onKey(e) { if (e.key === 'Escape') close(); }
    document.addEventListener('keydown', onKey);
    closeBtn.addEventListener('click', close);
    ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
  }

  function uploadInlineImage(file, cb) {
    var fd = new FormData();
    fd.append('image', file);
    var tok = typeof window.CSRF_TOKEN === 'string' && window.CSRF_TOKEN
      ? window.CSRF_TOKEN
      : (document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/) || [])[1] || '';
    fetch('/ajax/inline-image/upload/', {
      method: 'POST',
      headers: tok ? { 'X-CSRFToken': tok } : {},
      credentials: 'same-origin',
      body: fd
    }).then(function (r) { return r.json().then(function (d) { return { status: r.status, data: d }; }); })
      .then(function (res) {
        if (res.status >= 200 && res.status < 300 && res.data && res.data.id) cb(null, res.data);
        else cb(new Error((res.data && res.data.error) || 'Upload failed'));
      }).catch(function (e) { cb(e || new Error('Network error')); });
  }

  function serializeEditor(editor) {
    if (!editor) return '';
    var parts = [];
    function walk(node) {
      if (node.nodeType === 3) {
        parts.push(node.textContent || '');
        return;
      }
      if (node.nodeType !== 1) return;
      if (node.classList && node.classList.contains('neb-chip')) {
        var iid = node.getAttribute('data-neb-img');
        if (iid) parts.push('[[img:' + iid + ']]');
        return;
      }
      if (node.tagName === 'BR') { parts.push('\n'); return; }
      if (node.tagName === 'DIV' || node.tagName === 'P' || node.tagName === 'LI') {
        for (var i = 0; i < node.childNodes.length; i++) walk(node.childNodes[i]);
        if (parts.length && parts[parts.length - 1] !== '\n') parts.push('\n');
        return;
      }
      for (var j = 0; j < node.childNodes.length; j++) walk(node.childNodes[j]);
    }
    for (var i = 0; i < editor.childNodes.length; i++) walk(editor.childNodes[i]);
    var text = parts.join('').replace(/\n{3,}/g, '\n\n').trim();
    return text;
  }

  function loadEditor(editor, text) {
    editor.innerHTML = '';
    if (!text) return;
    var lines = text.split('\n');
    for (var li = 0; li < lines.length; li++) {
      var line = lines[li];
      var container;
      if (li > 0) {
        var brOr = editor;
        if (editor.children.length) {
          var wrapper = document.createElement('div');
          editor.appendChild(wrapper);
          container = wrapper;
        } else {
          container = editor;
        }
      } else {
        container = document.createElement('div');
        editor.appendChild(container);
      }
      var re = new RegExp(TOKEN_RE, 'g'), last = 0, m;
      while ((m = re.exec(line))) {
        if (m.index > last) container.appendChild(document.createTextNode(line.slice(last, m.index)));
        var iid = parseInt(m[1], 10);
        if (iid) container.appendChild(chipElement(iid, { editor: true }));
        last = m.index + m[0].length;
      }
      if (last < line.length) container.appendChild(document.createTextNode(line.slice(last)));
      if (!container.hasChildNodes()) container.appendChild(document.createElement('br'));
    }
    if (editor.childNodes.length === 1 && editor.firstElementChild && editor.firstElementChild.tagName === 'DIV') {
      var only = editor.firstElementChild;
      var frag = document.createDocumentFragment();
      while (only.firstChild) frag.appendChild(only.firstChild);
      editor.removeChild(only);
      editor.appendChild(frag);
    }
  }

  function insertChipAtCaret(editor, id) {
    editor.focus();
    var sel = window.getSelection();
    var chip = chipElement(id, { editor: true });
    if (!sel || !sel.rangeCount) {
      editor.appendChild(chip);
      var rng = document.createRange();
      rng.setStartAfter(chip);
      rng.collapse(true);
      sel.removeAllRanges(); sel.addRange(rng);
      return;
    }
    var range = sel.getRangeAt(0);
    if (!editor.contains(range.commonAncestorContainer) && range.commonAncestorContainer !== editor) {
      editor.appendChild(chip);
      return;
    }
    range.deleteContents();
    range.insertNode(chip);
    var after = document.createTextNode('\u200B');
    if (chip.nextSibling) chip.parentNode.insertBefore(after, chip.nextSibling);
    else chip.parentNode.appendChild(after);
    var rng = document.createRange();
    rng.setStartAfter(chip);
    rng.setEndAfter(after);
    rng.collapse(false);
    sel.removeAllRanges(); sel.addRange(rng);
  }

  function insertPlaceholder(editor) {
    var ph = document.createElement('span');
    ph.className = 'neb-chip neb-chip-editor neb-chip-uploading';
    ph.textContent = '…';
    ph.style.cssText += ';padding:0 8px;font-size:.75rem;color:var(--md-on-surface-variant)';
    editor.focus();
    var sel = window.getSelection();
    if (!sel || !sel.rangeCount) { editor.appendChild(ph); return ph; }
    var range = sel.getRangeAt(0);
    if (!editor.contains(range.commonAncestorContainer) && range.commonAncestorContainer !== editor) {
      editor.appendChild(ph); return ph;
    }
    range.deleteContents();
    range.insertNode(ph);
    var rng = document.createRange();
    rng.setStartAfter(ph); rng.collapse(true);
    sel.removeAllRanges(); sel.addRange(rng);
    return ph;
  }

  var MAX_COMPOSER_IMAGES = 8;

  function bindEditor(editor) {
    if (isSkipped(editor)) return;
    if (!isEnabled()) return;
    if (!editor || editor.dataset.nebBound === '1') return;
    editor.dataset.nebBound = '1';
    editor.setAttribute('contenteditable', 'true');
    editor.setAttribute('role', 'textbox');
    editor.setAttribute('aria-multiline', 'true');

    var dragSrcId = null, dragSrcEl = null, lastDragEnd = 0;

    function pointRange(x, y) {
      try {
        if (document.caretRangeFromPoint) return document.caretRangeFromPoint(x, y);
        if (document.caretPositionFromPoint) {
          var p = document.caretPositionFromPoint(x, y);
          if (!p) return null;
          var r = document.createRange();
          r.setStart(p.offsetNode, p.offset);
          r.collapse(true);
          return r;
        }
      } catch (_) {}
      return null;
    }

    editor.addEventListener('dragstart', function (e) {
      var chip = e.target.closest('.neb-chip');
      if (!chip || !editor.contains(chip)) return;
      dragSrcId = chip.getAttribute('data-neb-img');
      dragSrcEl = chip;
      if (e.dataTransfer) {
        e.dataTransfer.setData('application/x-neb-img', dragSrcId);
        e.dataTransfer.setData('text/plain', '[image]');
        e.dataTransfer.effectAllowed = 'move';
      }
      chip.classList.add('neb-chip-editor-dragging');
    });
    editor.addEventListener('dragend', function (e) {
      editor.classList.remove('neb-drop-active');
      var chip = e.target.closest && e.target.closest('.neb-chip');
      if (chip) chip.classList.remove('neb-chip-editor-dragging');
      lastDragEnd = Date.now();
      dragSrcId = null; dragSrcEl = null;
    });
    editor.addEventListener('dragover', function (e) {
      var types = (e.dataTransfer && e.dataTransfer.types) || [];
      var hasImageFile = false;
      for (var i = 0; i < types.length; i++) if (types[i] === 'Files') hasImageFile = true;
      var internal = !!(dragSrcId || (types.indexOf && types.indexOf('application/x-neb-img') >= 0));
      if (!hasImageFile && !internal) return;
      e.preventDefault();
      e.dataTransfer.dropEffect = hasImageFile ? 'copy' : 'move';
      editor.classList.add('neb-drop-active');
      if (internal && e.clientX && e.clientY) {
        var r = pointRange(e.clientX, e.clientY);
        if (r) {
          try {
            var inside = editor.contains(r.startContainer) || r.startContainer === editor;
            if (inside) {
              var sel2 = window.getSelection();
              sel2.removeAllRanges();
              sel2.addRange(r);
            }
          } catch (_) {}
        }
      }
    });
    editor.addEventListener('dragleave', function (e) {
      if (!editor.contains(e.relatedTarget)) editor.classList.remove('neb-drop-active');
    });
    editor.addEventListener('drop', function (e) {
      editor.classList.remove('neb-drop-active');
      var dt = e.dataTransfer;
      if (!dt) return;
      if (dt.files && dt.files.length) {
        var imgFiles = [];
        for (var i = 0; i < dt.files.length; i++) {
          if ((dt.files[i].type || '').indexOf('image/') === 0) imgFiles.push(dt.files[i]);
        }
        if (imgFiles.length) {
          e.preventDefault();
          handleFiles(imgFiles);
          return;
        }
      }
      var nebId = (dt.getData && dt.getData('application/x-neb-img')) || dragSrcId;
      if (nebId) {
        e.preventDefault();
        if (dragSrcEl && dragSrcEl.parentNode) dragSrcEl.remove();
        insertChipAtCaret(editor, parseInt(nebId, 10));
        dispatchInput(editor);
        dragSrcId = null; dragSrcEl = null;
      }
    });

    editor.addEventListener('paste', function (e) {
      var dt = e.clipboardData;
      if (!dt) return;
      if (dt.files && dt.files.length) {
        var imgFs = [];
        for (var i = 0; i < dt.files.length; i++) {
          if ((dt.files[i].type || '').indexOf('image/') === 0) imgFs.push(dt.files[i]);
        }
        if (imgFs.length) {
          e.preventDefault();
          handleFiles(imgFs);
          return;
        }
      }
      var html = dt.getData('text/html');
      if (html && html.indexOf('data-neb-img') >= 0) {
        e.preventDefault();
        var tmp = document.createElement('div');
        tmp.innerHTML = html;
        var collected = [];
        function walkPaste(node, inherited) {
          if (!node) return;
          if (node.nodeType === 3) {
            collected.push({ t: 'text', v: node.textContent || '' });
            return;
          }
          if (node.nodeType !== 1) return;
          if (node.hasAttribute && node.hasAttribute('data-neb-img')) {
            collected.push({ t: 'chip', id: parseInt(node.getAttribute('data-neb-img'), 10) });
            return;
          }
          if (node.tagName === 'BR') { collected.push({ t: 'text', v: '\n' }); return; }
          if (node.tagName === 'DIV' || node.tagName === 'P' || node.tagName === 'LI') {
            var kids = node.childNodes;
            for (var i = 0; i < kids.length; i++) walkPaste(kids[i]);
            collected.push({ t: 'text', v: '\n' });
            return;
          }
          for (var i = 0; i < node.childNodes.length; i++) walkPaste(node.childNodes[i]);
        }
        for (var i = 0; i < tmp.childNodes.length; i++) walkPaste(tmp.childNodes[i]);
        var sel = window.getSelection();
        if (!sel || !sel.rangeCount) { editor.focus(); sel = window.getSelection(); }
        var range = sel.rangeCount ? sel.getRangeAt(0) : null;
        if (!range || (!editor.contains(range.commonAncestorContainer) && range.commonAncestorContainer !== editor)) {
          range = document.createRange(); range.selectNodeContents(editor); range.collapse(false);
          sel.removeAllRanges(); sel.addRange(range);
        }
        range.deleteContents();
        var frag = document.createDocumentFragment();
        collected.forEach(function (c) {
          if (c.t === 'text' && c.v) frag.appendChild(document.createTextNode(c.v));
          else if (c.t === 'chip' && c.id) frag.appendChild(chipElement(c.id, { editor: true }));
        });
        range.insertNode(frag);
        var end = document.createRange();
        end.setStartAfter(range.endContainer.childNodes[range.endOffset - 1] || frag.lastChild || editor);
        end.collapse(true); sel.removeAllRanges(); sel.addRange(end);
        dispatchInput(editor);
      }
    });

    editor.addEventListener('click', function (e) {
      var rmBtn = e.target.closest('[data-neb-remove]');
      if (rmBtn && editor.contains(rmBtn)) {
        e.preventDefault(); e.stopPropagation();
        var chipR = rmBtn.closest('.neb-chip');
        if (chipR) chipR.remove();
        dispatchInput(editor);
        return;
      }
      if (Date.now() - lastDragEnd < 300) return;
      var chip = e.target.closest('.neb-chip[data-neb-full]');
      if (chip && editor.contains(chip)) {
        e.preventDefault(); e.stopPropagation();
        openLightbox(chip.getAttribute('data-neb-full'));
      }
    });
    editor.addEventListener('input', function () {
      if (!editor.querySelector('.neb-chip') && editor.textContent === '') {
        if (editor.firstChild) { editor.innerHTML = ''; }
      }
    });
    editor.addEventListener('keydown', function (e) {
      if (e.key === 'Backspace' || e.key === 'Delete') {
        var sel = window.getSelection();
        if (!sel || !sel.rangeCount) return;
        var range = sel.getRangeAt(0);
        if (!range.collapsed) {
          var frag = range.cloneContents();
          if (frag.querySelector && frag.querySelector('.neb-chip')) {
            var chips = frag.querySelectorAll('.neb-chip-editor-dragging');
          }
        } else {
          var focusNode = sel.focusNode;
          var offset = sel.focusOffset;
          if (e.key === 'Backspace' && offset === 0 && focusNode) {
            var prev = focusNode.previousSibling || focusNode.parentElement && focusNode.parentElement.previousSibling;
            if (prev && prev.classList && prev.classList.contains('neb-chip')) {
              e.preventDefault(); prev.remove(); dispatchInput(editor);
            }
          }
        }
      }
    });

    function countChips() {
      return editor.querySelectorAll('.neb-chip').length;
    }
    function handleFiles(files) {
      var imgs = [];
      for (var i = 0; i < files.length; i++) {
        if ((files[i].type || '').indexOf('image/') === 0) imgs.push(files[i]);
      }
      if (!imgs.length) return;
      if (countChips() + imgs.length > MAX_COMPOSER_IMAGES) {
        if (typeof window.showSnackbar === 'function') window.showSnackbar('Maximum ' + MAX_COMPOSER_IMAGES + ' images');
        imgs = imgs.slice(0, Math.max(0, MAX_COMPOSER_IMAGES - countChips()));
      }
      imgs.forEach(function (file) {
        var ph = insertPlaceholder(editor);
        dispatchInput(editor);
        uploadInlineImage(file, function (err, data) {
          if (err || !data || !data.id) {
            if (ph && ph.parentNode) ph.remove();
            dispatchInput(editor);
            showSnackbar(err ? err.message : 'Upload failed');
            return;
          }
          var chip = chipElement(data.id, { editor: true });
          if (ph && ph.parentNode) ph.parentNode.replaceChild(chip, ph);
          dispatchInput(editor);
        });
      });
    }
    editor._nebHandleFiles = handleFiles;
    editor._nebInsertChip = function (id) { insertChipAtCaret(editor, id); dispatchInput(editor); };
  }

  function dispatchInput(editor) {
    ['input', 'change'].forEach(function (evt) {
      editor.dispatchEvent(new Event(evt, { bubbles: true }));
    });
    if (editor._nebPairedTA) {
      editor._nebPairedTA.dispatchEvent(new Event('input', { bubbles: true }));
      editor._nebPairedTA.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }

  function enhanceTextarea(ta) {
    if (isSkipped(ta)) return;
    if (!isEnabled()) return;
    if (!ta || ta.dataset.nebEnhanced === '1') return;
    if (ta.tagName !== 'TEXTAREA') {
      if (ta.getAttribute && ta.getAttribute('contenteditable') === 'true') { bindEditor(ta); return; }
      return;
    }
    ta.dataset.nebEnhanced = '1';

    var ed = document.createElement('div');
    ed.className = 'neb-seamless';
    ed.contentEditable = 'true';
    ed.setAttribute('role', 'textbox');
    ed.setAttribute('aria-multiline', 'true');
    var ph = ta.getAttribute('placeholder') || '';
    if (ph) ed.setAttribute('data-placeholder', ph);

    var cs = getComputedStyle(ta);
    ['fontFamily','fontSize','fontWeight','fontStyle','lineHeight','letterSpacing','textTransform',
     'color','backgroundColor',
     'borderTopWidth','borderTopStyle','borderTopColor',
     'borderRightWidth','borderRightStyle','borderRightColor',
     'borderBottomWidth','borderBottomStyle','borderBottomColor',
     'borderLeftWidth','borderLeftStyle','borderLeftColor',
     'borderTopLeftRadius','borderTopRightRadius','borderBottomRightRadius','borderBottomLeftRadius',
     'paddingTop','paddingRight','paddingBottom','paddingLeft',
     'marginTop','marginRight','marginBottom','marginLeft',
     'minHeight','maxWidth','textAlign','boxSizing'
    ].forEach(function (p) { try { ed.style[p] = cs[p]; } catch (_) {} });
    ed.style.height = 'auto';
    ed.style.overflowY = 'hidden';
    ed.style.overflowX = 'hidden';
    ed.style.resize = 'none';
    ed.style.display = 'block';
    if (!(parseFloat(cs.minHeight) > 0)) {
      var rows = parseInt(ta.getAttribute('rows'), 10);
      var lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.4 || 20;
      ed.style.minHeight = (((rows > 0) ? rows : 2) * lh) + 'px';
    }
    try {
      var pd = getComputedStyle(ta.parentNode).display;
      if (pd.indexOf('flex') >= 0 || pd.indexOf('grid') >= 0) {
        ed.style.flex = cs.flex;
        ed.style.alignSelf = cs.alignSelf;
      } else {
        ed.style.width = cs.width;
      }
    } catch (_) {}

    ta.parentNode.insertBefore(ed, ta);
    loadEditor(ed, ta.value || '');
    ta.style.display = 'none';
    ta._nebEditor = ed;
    ed._nebPairedTA = ta;
    bindEditor(ed);
    ed.addEventListener('focus', function () { ed.classList.add('neb-focus'); });
    ed.addEventListener('blur', function () { ed.classList.remove('neb-focus'); });

    Object.defineProperty(ta, 'value', {
      get: function () { return serializeEditor(ed); },
      set: function (v) { loadEditor(ed, v || ''); },
      configurable: true
    });
    ta.getAttribute = (function (orig) {
      return function (name) {
        if (name === 'value') return serializeEditor(ed);
        return orig.call(this, name);
      };
    })(ta.getAttribute.bind(ta));

    ta._nebGetSerialize = function () { return serializeEditor(ed); };
    var origFocus = ta.focus.bind(ta);
    ta.focus = function () { ed.focus(); };
    ta._origFocus = origFocus;

    var fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/jpeg,image/png,image/webp,image/gif';
    fileInput.style.display = 'none';
    document.body.appendChild(fileInput);
    ta._nebFileInput = fileInput;
    fileInput.addEventListener('change', function () {
      var fs = Array.from(fileInput.files || []);
      fileInput.value = '';
      if (fs.length && ed._nebHandleFiles) ed._nebHandleFiles(fs);
    });
    ta._nebPickImage = function () { fileInput.click(); };
  }

  function enhanceAll(root) {
    if (!root) root = document;
    var tas = root.querySelectorAll('textarea');
    tas.forEach(enhanceTextarea);
  }

  document.addEventListener('click', function (e) {
    var chip = e.target.closest && e.target.closest('.neb-chip[data-neb-full]');
    if (!chip) return;
    if (chip.classList.contains('neb-chip-editor')) return;
    try { if (chip.closest('[contenteditable="true"]')) return; } catch (_) {}
    e.preventDefault();
    var full = chip.getAttribute('data-neb-full');
    if (full) openLightbox(full);
  });
  document.addEventListener('keydown', function (e) {
    if ((e.key === 'Enter' || e.key === ' ') && e.target.closest && e.target.closest('.neb-chip[data-neb-full]:not(.neb-chip-editor)')) {
      e.preventDefault();
      var full = e.target.getAttribute('data-neb-full');
      if (full) openLightbox(full);
    }
  });

  document.addEventListener('copy', function (e) {
    var sel = window.getSelection();
    if (!sel || sel.rangeCount === 0 || sel.isCollapsed) return;
    var anchor = sel.anchorNode, focus = sel.focusNode;
    function isInNeb(node, cls) {
      while (node && node !== document.documentElement) {
        if (node.classList && node.classList.contains && node.classList.contains(cls)) return true;
        node = node.parentNode;
      }
      return false;
    }
    var bodySelectors = '.fp-post-body,.fp-reply-body,.comment-text,.rd-description,.fp-thread-reply,.fp-reply-body';
    var inside = false;
    var anc = sel.anchorNode;
    while (anc && anc !== document.documentElement) {
      if (anc.matches && anc.matches(bodySelectors)) { inside = true; break; }
      anc = anc.parentNode;
    }
    if (!inside) return;
    if (!e.clipboardData) return;
    var range = sel.getRangeAt(0);
    var frag = range.cloneContents();
    var holder = document.createElement('div');
    holder.appendChild(frag);

    function buildPlain(node) {
      if (node.nodeType === 3) return node.textContent || '';
      if (node.nodeType !== 1) return '';
      if (node.classList && node.classList.contains('neb-chip')) return '[image]';
      if (node.tagName === 'BR') return '\n';
      if (node.tagName === 'DIV' || node.tagName === 'P' || node.tagName === 'LI') {
        var s = '';
        for (var i = 0; i < node.childNodes.length; i++) s += buildPlain(node.childNodes[i]);
        return s + '\n';
      }
      var out = '';
      for (var i = 0; i < node.childNodes.length; i++) out += buildPlain(node.childNodes[i]);
      return out;
    }
    function buildHtml(node) {
      if (node.nodeType === 3) return esc(node.textContent || '').replace(/\n/g, '<br>');
      if (node.nodeType !== 1) return '';
      if (node.classList && node.classList.contains('neb-chip')) {
        var iid = node.getAttribute('data-neb-img') || '';
        var full = node.getAttribute('data-neb-full') || imageUrl(iid);
        return '<span data-neb-img="' + esc(iid) + '"><img src="' + esc(full) + '" alt="Image"></span>';
      }
      if (node.tagName === 'BR') return '<br>';
      if (node.tagName === 'DIV' || node.tagName === 'P') {
        var inner = '';
        for (var i = 0; i < node.childNodes.length; i++) inner += buildHtml(node.childNodes[i]);
        return '<div>' + inner + '</div>';
      }
      var tag = node.tagName.toLowerCase();
      if (tag === 'a' || tag === 'strong' || tag === 'em' || tag === 'code' || tag === 'b' || tag === 'i' || tag === 'span' || tag === 'blockquote' || tag === 'ul' || tag === 'ol' || tag === 'li' || tag === 'h3') {
        var kids = '';
        for (var i = 0; i < node.childNodes.length; i++) kids += buildHtml(node.childNodes[i]);
        var cls = node.className ? ' class="' + esc(node.className) + '"' : '';
        var href = node.getAttribute('href') ? ' href="' + esc(node.getAttribute('href')) + '"' : '';
        return '<' + tag + cls + href + '>' + kids + '</' + tag + '>';
      }
      var inner2 = '';
      for (var i = 0; i < node.childNodes.length; i++) inner2 += buildHtml(node.childNodes[i]);
      return inner2;
    }

    var plain = buildPlain(holder).replace(/\n{3,}/g, '\n\n').replace(/^\n+|\n+$/g, '');
    if (!plain) return;
    var html = '<div data-neb-copy="1">' + buildHtml(holder) + '</div>';
    e.preventDefault();
    try {
      e.clipboardData.setData('text/plain', plain);
      e.clipboardData.setData('text/html', html);
    } catch (_) {}
  });

  window.InlineMedia = {
    VERSION: '1.0.0',
    imageUrl: imageUrl,
    thumbUrl: thumbUrl,
    extractIds: extractIds,
    plainText: plainText,
    stripTokens: stripTokens,
    chipHtml: chipHtml,
    splitRender: splitRender,
    serializeEditor: serializeEditor,
    loadEditor: loadEditor,
    enhanceTextarea: enhanceTextarea,
    enhanceAll: enhanceAll,
    bindEditor: bindEditor,
    openLightbox: openLightbox,
    upload: uploadInlineImage
  };

  if (document.readyState !== 'loading') setTimeout(function () { enhanceAll(document); if(!isEnabled()){ try{ document.querySelectorAll('[data-action="attach-inline-image"]').forEach(function(b){ b.style.display='none'; }); }catch(_){} } }, 40);
  else document.addEventListener('DOMContentLoaded', function () { enhanceAll(document); if(!isEnabled()){ try{ document.querySelectorAll('[data-action="attach-inline-image"]').forEach(function(b){ b.style.display='none'; }); }catch(_){} } });

  var _mo = null;
  try {
    _mo = new MutationObserver(function (mutations) {
      mutations.forEach(function (m) {
        m.addedNodes.forEach(function (n) {
          if (n.nodeType !== 1) return;
          if (n.tagName === 'TEXTAREA') enhanceTextarea(n);
          else {
            var tas = n.querySelectorAll ? n.querySelectorAll('textarea') : [];
            tas.forEach(enhanceTextarea);
            if (n.matches && n.matches('.fp-reply,.fp-reply-actions,.fp-thread-reply,.rd-inline-reply-box')) {
              var tas2 = n.querySelectorAll ? n.querySelectorAll('textarea') : [];
              tas2.forEach(enhanceTextarea);
            }
          }
        });
      });
    });
    _mo.observe(document.body, { childList: true, subtree: true });
  } catch (_) {}

})();
