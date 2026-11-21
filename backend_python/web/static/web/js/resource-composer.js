/* ResourceComposer: the one surface that shares a resource (upload) and edits one (edit).
 *
 * Markup: templates/web/components/_resource_composer.html. The tray rows are the forum editor's (.na-row), the
 * pickers are NebChoice sheets, the save bar is .fe-bar -- this file only wires them together:
 *
 *   - files: add by browse or by dropping anywhere on the surface, images are compressed before they leave the
 *     device, duplicates are skipped, each row shows its own progress while the form uploads;
 *   - chips: one per choice (subject, level, type, tags, price, more), each shows its answer and nothing else;
 *   - the form posts as one multipart request, so the server contract is the one the upload and edit views
 *     always had (file[], thumbnail, thumbnail_url, file_url, is_paid, price ...).
 */
(function () {
  'use strict';

  var form = document.getElementById('rc-form');
  if (!form) return;

  var edit = form.dataset.mode === 'edit';
  var MAX_FILES = edit ? 1 : 5;
  var MAX_BYTES = 50 * 1024 * 1024;
  var IMAGE_RE = /^image\/(jpeg|png|webp|bmp)$/;

  function $(id) { return document.getElementById(id); }
  var titleEl = $('rc-title'), descEl = $('rc-description');
  var rowsEl = $('rc-rows'), trayEl = $('rc-tray'), dropEl = $('rc-drop');
  var fileInput = $('rc-file-input'), coverInput = $('rc-cover-input');
  var fileUrl = $('rc-file-url'), coverUrl = $('rc-cover-url');
  var statusEl = $('rc-status'), badge = $('rc-badge'), submit = $('rc-submit');
  var errorsEl = $('rc-errors'), errorList = $('rc-error-list');

  var current = { file: null, cover: '' };
  var seed = $('rc-current');
  if (seed) { try { current = JSON.parse(seed.textContent) || current; } catch (e) { /* keep the empty default */ } }

  var files = [];          // { id, file, saved, preview }
  var coverFile = null, coverPreview = '';
  var replacing = '';      // the row whose Replace button opened a chooser
  var pending = 0, busy = false, dirty = false, done = false, uid = 0;
  var known = {};          // row key -> { el, sig }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }
  function say(msg) {
    if (window.showSnackbar) window.showSnackbar(msg);
    else if (window.NebToast && NebToast.show) NebToast.show(msg);
  }
  function bytes(n) {
    if (!n) return '';
    if (n < 1024) return n + ' B';
    if (n < 1048576) return (n / 1024).toFixed(1) + ' KB';
    return (n / 1048576).toFixed(1) + ' MB';
  }
  function kindOf(name, type) {
    var ext = (String(name).split('.').pop() || '').toLowerCase();
    if (/^image\//.test(type || '') || ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'heic', 'heif'].indexOf(ext) >= 0) return 'image';
    if (['mp4', 'mkv', 'avi', 'mov', 'webm', 'wmv', 'flv', '3gp'].indexOf(ext) >= 0) return 'video';
    if (['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a', 'wma'].indexOf(ext) >= 0) return 'audio';
    return 'file';
  }
  var ICONS = { video: 'movie', audio: 'audio_file', image: 'image', link: 'link', file: 'description', pdf: 'picture_as_pdf' };
  function iconFor(kind, name) { return /\.pdf$/i.test(name || '') ? ICONS.pdf : ICONS[kind] || ICONS.file; }
  function host(url) { try { return new URL(url).hostname.replace(/^www\./, ''); } catch (e) { return url; } }
  function prettyName(name) {
    var base = name.replace(/\.[^/.]+$/, '').replace(/[_\-]+/g, ' ').replace(/\s+/g, ' ').trim();
    return base ? base.charAt(0).toUpperCase() + base.slice(1) : '';
  }
  function csrf() {
    var f = form.querySelector('[name=csrfmiddlewaretoken]');
    return f ? f.value : '';
  }

  /* ── Image compression: the old page's behaviour, minus the PNG-goes-black bug ───────── */
  function compress(file) {
    return new Promise(function (resolve) {
      if (!IMAGE_RE.test(file.type)) { resolve({ file: file }); return; }
      var url = URL.createObjectURL(file), img = new Image();
      img.onload = function () {
        URL.revokeObjectURL(url);
        var scale = Math.min(1, 3000 / Math.max(img.width, img.height));
        var canvas = document.createElement('canvas');
        canvas.width = Math.max(1, Math.round(img.width * scale));
        canvas.height = Math.max(1, Math.round(img.height * scale));
        var ctx = canvas.getContext('2d');
        var webp = file.type === 'image/webp';
        if (!webp) { ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, canvas.width, canvas.height); }
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        canvas.toBlob(function (blob) {
          if (blob && blob.size < file.size * 0.95) {
            var name = file.name.replace(/\.[^/.]+$/, '') + (webp ? '.webp' : '.jpg');
            resolve({ file: new File([blob], name, { type: blob.type, lastModified: Date.now() }), saved: Math.round((1 - blob.size / file.size) * 100) });
          } else resolve({ file: file });
        }, webp ? 'image/webp' : 'image/jpeg', 0.85);
      };
      img.onerror = function () { URL.revokeObjectURL(url); resolve({ file: file }); };
      img.src = url;
    });
  }

  /* ── The tray: one keyed row per thing that will be sent ─────────────────────────────── */
  function rowsNow() {
    var rows = [], link = fileUrl && !fileUrl.disabled && fileUrl.value.trim();
    if (edit && !files.length && current.file) {
      rows.push({ key: 'cur', kind: current.file.kind || 'file', name: current.file.name, meta: bytes(current.file.size), open: current.file.url, replace: true });
    }
    files.forEach(function (f) {
      var kind = kindOf(f.file.name, f.file.type);
      rows.push({
        key: f.id, kind: kind, name: f.file.name, replace: edit,
        meta: bytes(f.file.size) + (f.saved > 0 ? ' · ' + f.saved + '% smaller' : ''),
        thumb: kind === 'image' ? f.preview : '', remove: true
      });
    });
    if (!files.length && link && !(edit && current.file)) rows.push({ key: 'link', kind: 'link', name: host(link), meta: 'Link', remove: true });
    var cover = coverFile ? coverPreview : (coverUrl && coverUrl.value.trim()) || (!coverUrl && current.cover) || '';
    if (cover) rows.push({ key: 'cover', kind: 'image', name: 'Cover', meta: coverFile ? coverFile.name : host(cover), thumb: cover, replace: true, remove: true, cover: true });
    return rows;
  }

  function rowHtml(r) {
    var thumb = r.thumb ? '<img src="' + esc(r.thumb) + '" alt="">' : '<span class="material-symbols-outlined" aria-hidden="true">' + iconFor(r.kind, r.name) + '</span>';
    return '<span class="na-thumb na-' + r.kind + '">' + thumb + '</span>' +
      '<span class="na-text"><span class="na-name">' + esc(r.name) + '</span><span class="na-meta">' + esc(r.meta) + '</span></span>' +
      (r.open ? '<a class="na-btn" href="' + esc(r.open) + '" target="_blank" rel="noopener" aria-label="Open" title="Open"><span class="material-symbols-outlined">open_in_new</span></a>' : '') +
      (r.replace ? '<button type="button" class="na-btn" data-rc="replace" aria-label="Replace ' + esc(r.name) + '" title="Replace"><span class="material-symbols-outlined">swap_horiz</span></button>' : '') +
      (r.remove ? '<button type="button" class="na-btn" data-rc="remove" aria-label="Remove ' + esc(r.name) + '" title="Remove"><span class="material-symbols-outlined">close</span></button>' : '') +
      '<span class="na-track" aria-hidden="true"><i></i></span>';
  }

  function paintTray() {
    var rows = rowsNow(), live = {};
    rows.forEach(function (r) {
      live[r.key] = true;
      var sig = JSON.stringify(r), k = known[r.key];
      if (!k) {
        var li = document.createElement('li');
        li.className = 'na-row';
        li.dataset.key = r.key;
        li.innerHTML = rowHtml(r);
        rowsEl.appendChild(li);
        k = known[r.key] = { el: li, sig: sig };
      } else if (k.sig !== sig) {
        k.el.innerHTML = rowHtml(r);
        k.sig = sig;
      }
    });
    Object.keys(known).forEach(function (key) {
      if (live[key]) return;
      var el = known[key].el;
      delete known[key];
      el.classList.add('is-leaving');
      setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 200);
    });
    rows.forEach(function (r) { rowsEl.appendChild(known[r.key].el); });   // keep tray order = send order
    trayEl.hidden = !rows.length;
    if (dropEl) dropEl.hidden = files.length > 0 || rows.some(function (r) { return r.key === 'link'; });
    var n = files.length || (edit && current.file ? 1 : 0);
    badge.hidden = n < 2;
    badge.textContent = n;
    if (fileUrl) fileUrl.disabled = files.length > 0;
  }

  function progress(pct) {
    var left = files.reduce(function (s, f) { return s + f.file.size; }, 0), sent = left * pct, cum = 0;
    files.forEach(function (f) {
      var el = known[f.id] && known[f.id].el;
      if (!el) return;
      var p = f.file.size ? Math.max(0, Math.min(1, (sent - cum) / f.file.size)) : 1;
      cum += f.file.size;
      el.classList.add('is-uploading');
      el.querySelector('.na-track i').style.width = Math.round(p * 100) + '%';
    });
  }
  function clearProgress() {
    rowsEl.querySelectorAll('.na-row').forEach(function (el) {
      el.classList.remove('is-uploading');
      var bar = el.querySelector('.na-track i');
      if (bar) bar.style.width = '0';
    });
  }

  /* ── Adding things ────────────────────────────────────────────────────────────────────── */
  function touch() { dirty = true; hideErrors(); }

  function addFiles(list, replaceKey) {
    var incoming = Array.prototype.slice.call(list || []);
    if (!incoming.length) return;
    var chain = Promise.resolve();
    incoming.forEach(function (file) {
      chain = chain.then(function () {
        if (file.size > MAX_BYTES) { say(file.name + ' is over 50 MB'); return; }
        if (!edit && !replaceKey && files.length >= MAX_FILES) { say('Up to ' + MAX_FILES + ' files at a time'); return; }
        var dup = files.some(function (f) { return f.file.name === file.name && f.file.size === file.size; });
        if (dup) { say(file.name + ' is already added'); return; }
        pending++;
        statusEl.textContent = IMAGE_RE.test(file.type) ? 'Preparing ' + file.name : '';
        return compress(file).then(function (res) {
          var item = { id: 'f' + (++uid), file: res.file, saved: res.saved || 0, preview: '' };
          if (kindOf(item.file.name, item.file.type) === 'image') item.preview = URL.createObjectURL(item.file);
          if (edit) { drop(files); files = [item]; }
          else if (replaceKey && replaceKey !== 'cur') {
            var at = files.map(function (f) { return f.id; }).indexOf(replaceKey);
            if (at >= 0) { drop([files[at]]); files.splice(at, 1, item); } else files.push(item);
          } else files.push(item);
          if (!titleEl.value.trim()) { titleEl.value = prettyName(item.file.name); titleEl.dispatchEvent(new Event('input', { bubbles: true })); }
        }).then(function () { pending--; });
      });
    });
    chain.then(function () { statusEl.textContent = ''; touch(); paintTray(); });
  }
  function drop(list) { list.forEach(function (f) { if (f.preview) URL.revokeObjectURL(f.preview); }); }

  function setCover(file) {
    if (!file) return;
    if (file.size > 10 * 1024 * 1024) { say('Cover images are limited to 10 MB'); return; }
    if (coverPreview) URL.revokeObjectURL(coverPreview);
    coverFile = file;
    coverPreview = URL.createObjectURL(file);
    if (coverUrl) coverUrl.value = '';
    touch(); paintTray();
  }
  function clearCover() {
    if (coverPreview) URL.revokeObjectURL(coverPreview);
    coverFile = null; coverPreview = '';
    if (coverUrl) coverUrl.value = '';
    current.cover = '';
    touch(); paintTray();
  }

  function pickFiles(key) {
    replacing = key || '';
    fileInput.value = '';
    fileInput.click();
  }

  $('rc-attach').addEventListener('click', function () { pickFiles(edit ? 'cur' : ''); });
  $('rc-cover-btn').addEventListener('click', function () { coverInput.value = ''; coverInput.click(); });
  if ($('rc-drop-pick')) $('rc-drop-pick').addEventListener('click', function () { pickFiles(''); });
  fileInput.addEventListener('change', function () { addFiles(fileInput.files, replacing); replacing = ''; });
  coverInput.addEventListener('change', function () { setCover(coverInput.files && coverInput.files[0]); });

  rowsEl.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-rc]');
    if (!btn) return;
    var key = btn.closest('.na-row').dataset.key, act = btn.dataset.rc;
    if (key === 'cover') {
      if (act === 'remove') clearCover();
      else { coverInput.value = ''; coverInput.click(); }
    } else if (act === 'replace') {
      pickFiles(key);
    } else if (key === 'link') {
      fileUrl.value = ''; touch(); paintTray(); paintChips();
    } else {
      var at = files.map(function (f) { return f.id; }).indexOf(key);
      if (at >= 0) { drop([files[at]]); files.splice(at, 1); touch(); paintTray(); }
    }
  });

  /* Drag anywhere on the surface. */
  var depth = 0;
  function hasFiles(e) { return e.dataTransfer && Array.prototype.indexOf.call(e.dataTransfer.types || [], 'Files') >= 0; }
  form.addEventListener('dragenter', function (e) { if (hasFiles(e)) { e.preventDefault(); depth++; form.classList.add('is-dropping'); } });
  form.addEventListener('dragover', function (e) { if (hasFiles(e)) e.preventDefault(); });
  form.addEventListener('dragleave', function () { depth = Math.max(0, depth - 1); if (!depth) form.classList.remove('is-dropping'); });
  form.addEventListener('drop', function (e) {
    if (!hasFiles(e)) return;
    e.preventDefault(); depth = 0; form.classList.remove('is-dropping');
    addFiles(Array.prototype.slice.call(e.dataTransfer.files), edit ? 'cur' : '');
  });

  /* ── Chips ────────────────────────────────────────────────────────────────────────────── */
  function csv(v) { return String(v || '').split(',').map(function (s) { return s.trim(); }).filter(Boolean); }
  function paintChips() {
    form.querySelectorAll('[data-rc-chip]').forEach(function (chip) {
      var vals = csv($(chip.dataset.rcChip).value), text = chip.querySelector('.rc-chip-text');
      text.textContent = !vals.length ? chip.dataset.rcLabel : vals.length > 2 ? vals[0] + ' +' + (vals.length - 1) : vals.join(', ');
      chip.classList.toggle('is-set', vals.length > 0);
      if (vals.length) chip.removeAttribute('aria-invalid');
    });
    form.querySelectorAll('[data-rc-group]').forEach(function (chip) {
      var n = Array.prototype.filter.call($(chip.dataset.rcGroup).querySelectorAll('[data-rc-f]'), function (i) { return i.value.trim(); }).length;
      chip.querySelector('.rc-chip-text').textContent = chip.dataset.rcLabel + (n ? ' · ' + n : '');
      chip.classList.toggle('is-set', n > 0);
    });
    var price = form.querySelector('[data-rc-price]');
    if (price) {
      var flag = form.querySelector('[data-neb-price-flag]'), amount = form.querySelector('[data-neb-price-field]');
      var paid = flag && flag.value === '1', n = parseFloat(amount && amount.value);
      price.querySelector('.rc-chip-text').textContent = paid ? (n > 0 ? 'Rs. ' + Math.round(n) : 'Set price') : 'Free';
      price.classList.toggle('is-set', !!paid);
    }
  }
  form.addEventListener('change', function () { touch(); paintChips(); paintTray(); });
  form.addEventListener('input', function (e) { touch(); if (e.target === fileUrl || e.target === coverUrl) paintTray(); paintChips(); });
  var priceSheet = $('rc-price');
  if (priceSheet) ['click', 'input', 'change'].forEach(function (t) {
    priceSheet.addEventListener(t, function () { requestAnimationFrame(paintChips); });
  });

  titleEl.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') { e.preventDefault(); descEl.focus(); }
  });

  /* ── Errors and status ────────────────────────────────────────────────────────────────── */
  function showErrors(list) {
    errorList.innerHTML = list.map(function (t) { return '<li>' + esc(t) + '</li>'; }).join('');
    errorsEl.hidden = false;
    errorsEl.classList.remove('is-in'); void errorsEl.offsetWidth; errorsEl.classList.add('is-in');
    errorsEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
  function hideErrors() { if (!errorsEl.hidden) errorsEl.hidden = true; }

  function validate() {
    var errs = [], paid = form.querySelector('[data-neb-price-flag]'), amount = form.querySelector('[data-neb-price-field]');
    if (!titleEl.value.trim()) { errs.push('Add a title.'); titleEl.focus(); }
    var subject = form.querySelector('[data-rc-chip="rc-subject-value"]');
    if (!$('rc-subject-value').value.trim()) { errs.push('Pick at least one subject.'); subject.setAttribute('aria-invalid', 'true'); }
    if (!edit && !files.length && !(fileUrl && fileUrl.value.trim())) errs.push('Add a file or paste a link.');
    if (paid && paid.value === '1' && !(parseFloat(amount && amount.value) > 0)) errs.push('Set a price above Rs. 0, or switch to free.');
    if (pending) errs.push('Your files are still being prepared.');
    return errs;
  }

  /* ── Sending ──────────────────────────────────────────────────────────────────────────── */
  function lock(on) {
    busy = on;
    form.classList.toggle('is-saving', on);
    submit.disabled = on;
    submit.querySelector('span:last-child').textContent = on ? (edit ? 'Saving' : 'Sharing') : (edit ? 'Save' : 'Share');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (busy) return;
    var errs = validate();
    if (errs.length) { showErrors(errs); return; }
    hideErrors();

    var fd = new FormData(form);
    fd.delete('file'); fd.delete('thumbnail');
    files.forEach(function (f) { fd.append('file', f.file, f.file.name); });
    if (coverFile) fd.append('thumbnail', coverFile, coverFile.name);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', form.getAttribute('action'));
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    lock(true);
    statusEl.textContent = files.length ? 'Uploading 0%' : 'Saving';
    xhr.upload.onprogress = function (ev) {
      if (!ev.lengthComputable) return;
      var pct = ev.loaded / ev.total;
      progress(pct);
      statusEl.textContent = pct >= 1 ? 'Processing' : 'Uploading ' + Math.round(pct * 100) + '%';
    };
    xhr.onload = function () {
      var data = {};
      try { data = JSON.parse(xhr.responseText); } catch (err) { /* handled below */ }
      if (xhr.status >= 200 && xhr.status < 300 && data.status === 'success') {
        done = true;
        form.classList.add('is-done');
        statusEl.textContent = edit ? 'Saved' : 'Shared';
        setTimeout(function () { window.location.href = data.redirect || '/'; }, 420);
        return;
      }
      lock(false); clearProgress(); statusEl.textContent = '';
      showErrors(data.errors || (data.error ? [data.error] : ['Something went wrong. Try again.']));
    };
    xhr.onerror = function () {
      lock(false); clearProgress(); statusEl.textContent = '';
      showErrors(['The connection dropped. Check it and try again.']);
    };
    xhr.send(fd);
  });

  /* Delete (edit only) */
  var del = $('rc-delete-confirm');
  if (del) del.addEventListener('click', function () {
    del.disabled = true;
    fetch(del.dataset.url, { method: 'POST', headers: { 'X-CSRFToken': csrf(), 'X-Requested-With': 'XMLHttpRequest' }, credentials: 'same-origin' })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (res) {
        if (res.ok && res.d.status === 'success') { done = true; window.location.href = res.d.redirect; return; }
        del.disabled = false;
        var close = $('rc-delete').querySelector('.neb-sheet-close');
        if (close) close.click();
        showErrors([res.d.error || 'Could not delete this resource.']);
      })
      .catch(function () { del.disabled = false; showErrors(['The connection dropped. Try again.']); });
  });

  window.addEventListener('beforeunload', function (e) {
    if (dirty && !done && !busy) { e.preventDefault(); e.returnValue = ''; }
  });

  paintChips();
  paintTray();
  dirty = false;
  if (errorList.children.length) errorsEl.hidden = false;

  document.querySelectorAll('[data-neb-price]').forEach(function (root) {
    if (root.dataset.nebPriceReady) return;
    root.dataset.nebPriceReady = '1';
    var modes = root.querySelectorAll('[data-neb-price-mode]');
    var flag = root.querySelector('[data-neb-price-flag]');
    var amountWrap = root.querySelector('[data-neb-price-amount]');
    var field = root.querySelector('[data-neb-price-field]');
    var earnings = root.querySelector('[data-neb-price-earnings]');
    var presets = root.querySelectorAll('[data-neb-price-preset]');
    var commission = parseFloat(root.dataset.commission || '0') || 0;
    function isPaid() {
      var checked = root.querySelector('[data-neb-price-mode]:checked');
      return !!checked && checked.value === 'paid';
    }
    function refresh() {
      var paid = isPaid();
      if (flag) flag.value = paid ? '1' : '0';
      if (amountWrap) amountWrap.hidden = !paid;
      root.classList.toggle('is-unset', paid && !(parseFloat(field && field.value) > 0));
      if (field) field.required = paid;
      var price = parseFloat(field && field.value) || 0;
      if (earnings) {
        if (!paid) earnings.textContent = 'Free for every Nebian.';
        else if (price > 0) {
          var keeps = Math.round((price - (price * commission) / 100) * 100) / 100;
          earnings.textContent = 'You receive Rs. ' + String(keeps).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + ' per sale after the ' + commission + '% platform fee.';
        } else earnings.textContent = '';
      }
      presets.forEach(function (chip) {
        chip.classList.toggle('is-chosen', paid && parseFloat(chip.dataset.nebPricePreset) === price);
      });
    }
    modes.forEach(function (inp) { inp.addEventListener('change', refresh); });
    if (field) field.addEventListener('input', refresh);
    presets.forEach(function (chip) {
      chip.addEventListener('click', function () {
        if (!field) return;
        field.value = chip.dataset.nebPricePreset;
        refresh();
      });
    });
    refresh();
  });
})();
