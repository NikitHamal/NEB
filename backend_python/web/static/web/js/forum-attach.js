/* NebAttach: the attachment tray every forum writer uses.
 *
 *   var tray = NebAttach.mount(el, {
 *     items: [{ kind, url, name, size, thumb }],   // what is already attached
 *     images: true,        // image files go to the post-image store and stay kind "image"
 *     maxMedia: 4,         // video / audio / file slots
 *     maxImages: 3,
 *     onChange: function (tray) {}
 *   });
 *   tray.pick();           // open the file chooser (multiple)
 *   tray.add(fileList);    // same, for a drop
 *   tray.items();          // finished items, in order
 *   tray.media();          // those that are not images, as the edit API wants them
 *   tray.imageUrls();      // image urls, in order
 *   tray.busy();           // anything still uploading
 *   tray.dirty();          // differs from what it was mounted with
 *   tray.count();
 *
 * One row per attachment: thumbnail or kind icon, name, size, and while it
 * uploads a progress track along the row's bottom edge. Each row has a grip
 * (drag, or focus it and use the arrow keys), a replace button that swaps the
 * file in the same slot, and a remove button. Rows re-flow with a FLIP
 * transition so a reorder reads as movement, not a jump.
 */
(function () {
  'use strict';

  var LIMITS = { video: 150 * 1024 * 1024, audio: 40 * 1024 * 1024, file: 30 * 1024 * 1024, image: 20 * 1024 * 1024 };
  var LIMIT_TEXT = { video: 'Videos are limited to 150 MB', audio: 'Audio is limited to 40 MB', file: 'Attachments are limited to 30 MB', image: 'Images are limited to 20 MB' };
  var ICONS = { video: 'movie', audio: 'audio_file', file: 'description', image: 'image' };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }
  function csrf() {
    var m = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
    return m ? decodeURIComponent(m[1]) : (typeof window.CSRF_TOKEN === 'string' ? window.CSRF_TOKEN : '');
  }
  function bytes(n) {
    if (!n) return '';
    if (n < 1024) return n + ' B';
    if (n < 1048576) return (n / 1024).toFixed(1) + ' KB';
    if (n < 1073741824) return (n / 1048576).toFixed(1) + ' MB';
    return (n / 1073741824).toFixed(2) + ' GB';
  }
  function say(msg) {
    if (window.showSnackbar) window.showSnackbar(msg);
    else if (window.NebToast && NebToast.show) NebToast.show(msg);
  }
  function kindOf(file, images) {
    if (images && /^image\//.test(file.type)) return 'image';
    var ext = (file.name.split('.').pop() || '').toLowerCase();
    if (['mp4', 'm4v', 'webm', 'mov'].indexOf(ext) >= 0) return 'video';
    if (['mp3', 'm4a', 'aac', 'ogg', 'opus', 'wav', 'flac'].indexOf(ext) >= 0) return 'audio';
    return 'file';
  }
  function norm(a) {
    return {
      kind: a.kind || 'file', url: a.url || '', name: a.name || '',
      size: a.size || a.sizeBytes || a.size_bytes || 0, mime: a.mime || a.mimeType || a.mime_type || '',
      thumb: a.thumb || a.thumbnailUrl || a.thumbnail_url || (a.kind === 'image' ? a.url : '') || '',
      thumbnail_url: a.thumbnail_url || a.thumbnailUrl || ''
    };
  }

  function mount(el, opts) {
    if (el._nebAttach) return el._nebAttach;
    opts = opts || {};
    var maxMedia = opts.maxMedia == null ? 4 : opts.maxMedia;
    var maxImages = opts.images ? (opts.maxImages == null ? 3 : opts.maxImages) : 0;
    var seq = 0;
    var rows = (opts.items || []).map(function (a) { var n = norm(a); n.id = ++seq; return n; });
    var start = signature();
    var picking = null;

    el.classList.add('na');
    el.innerHTML = '<ul class="na-list" role="list"></ul><div class="na-live" aria-live="polite"></div>' +
      '<input type="file" class="na-input" multiple hidden>';
    var list = el.querySelector('.na-list');
    var live = el.querySelector('.na-live');
    var input = el.querySelector('.na-input');

    function signature() { return rows.filter(function (r) { return r.url; }).map(function (r) { return r.url; }).join('|'); }
    function countKind(isImage) { return rows.filter(function (r) { return (r.kind === 'image') === isImage; }).length; }

    function rowHtml(r) {
      var thumb = r.thumb && (r.kind === 'image' || r.kind === 'video')
        ? '<img src="' + esc(r.thumb) + '" alt="" loading="lazy">'
        : '<span class="material-symbols-outlined" aria-hidden="true">' + ICONS[r.kind] + '</span>';
      var meta = r.error ? 'Upload failed' : (r.uploading ? 'Uploading ' + (r.pct || 0) + '%' : (r.kind + (r.size ? ' \u00b7 ' + bytes(r.size) : '')));
      return '<li class="na-row' + (r.uploading ? ' is-uploading' : '') + '" data-id="' + r.id + '">' +
        '<button type="button" class="na-grip" aria-label="Reorder ' + esc(r.name) + '. Use the up and down arrow keys." data-na="grip"' + (rows.length < 2 ? ' hidden' : '') + '>' +
          '<span class="material-symbols-outlined" aria-hidden="true">drag_indicator</span></button>' +
        '<span class="na-thumb na-' + r.kind + '">' + thumb + '</span>' +
        '<span class="na-text"><span class="na-name" title="' + esc(r.name) + '">' + esc(r.name || 'Attachment') + '</span>' +
          '<span class="na-meta">' + esc(meta) + '</span></span>' +
        '<button type="button" class="na-btn" data-na="replace" aria-label="Replace ' + esc(r.name) + '" title="Replace"' + (r.uploading ? ' disabled' : '') + '>' +
          '<span class="material-symbols-outlined" aria-hidden="true">swap_horiz</span></button>' +
        '<button type="button" class="na-btn" data-na="remove" aria-label="Remove ' + esc(r.name) + '" title="Remove">' +
          '<span class="material-symbols-outlined" aria-hidden="true">close</span></button>' +
        '<span class="na-track" aria-hidden="true"><i style="width:' + (r.uploading ? (r.pct || 0) : 0) + '%"></i></span>' +
      '</li>';
    }

    function render(flip) {
      var before = flip ? rects() : null;
      list.innerHTML = rows.map(rowHtml).join('');
      el.classList.toggle('is-empty', !rows.length);
      if (before) play(before);
    }
    function rects() {
      var m = {};
      list.querySelectorAll('.na-row').forEach(function (li) { m[li.getAttribute('data-id')] = li.getBoundingClientRect().top; });
      return m;
    }
    function play(before) {
      if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      list.querySelectorAll('.na-row').forEach(function (li) {
        var was = before[li.getAttribute('data-id')];
        if (was == null || li.classList.contains('is-dragging')) return;
        var d = was - li.getBoundingClientRect().top;
        if (!d) return;
        li.style.transition = 'none';
        li.style.transform = 'translateY(' + d + 'px)';
        requestAnimationFrame(function () {
          li.style.transition = 'transform .38s var(--spring, cubic-bezier(.34,1.4,.64,1))';
          li.style.transform = '';
        });
      });
    }
    function changed() {
      if (opts.onChange) opts.onChange(api);
      el.dispatchEvent(new CustomEvent('na:change', { bubbles: true }));
    }
    function byId(id) { return rows.filter(function (r) { return String(r.id) === String(id); })[0]; }
    function rowEl(id) { return list.querySelector('.na-row[data-id="' + id + '"]'); }
    function setPct(r, pct) {
      r.pct = pct;
      var li = rowEl(r.id);
      if (!li) return;
      li.querySelector('.na-track i').style.width = pct + '%';
      li.querySelector('.na-meta').textContent = 'Uploading ' + pct + '%';
    }

    function upload(r, file, previous) {
      var isImage = r.kind === 'image';
      var fd = new FormData();
      var xhr = new XMLHttpRequest();
      if (isImage) { fd.append('image', file); xhr.open('POST', '/ajax/post/upload-image/'); }
      else { fd.append('file', file); if (r.kind === 'audio') fd.append('kind_hint', 'audio'); xhr.open('POST', '/api/forum/uploads/'); }
      var t = csrf();
      if (t) xhr.setRequestHeader('X-CSRFToken', t);
      xhr.upload.onprogress = function (e) { if (e.lengthComputable) setPct(r, Math.round(e.loaded / e.total * 100)); };
      function fail(msg) {
        say(msg);
        if (previous) { rows[rows.indexOf(r)] = previous; } else { rows.splice(rows.indexOf(r), 1); }
        render(true); changed();
      }
      xhr.onload = function () {
        var d = null;
        try { d = JSON.parse(xhr.responseText); } catch (e) { /* not json */ }
        if (isImage && xhr.status === 200 && d && d.url) {
          r.url = d.url; r.thumb = d.url;
        } else if (!isImage && xhr.status === 201 && d && d.ok && d.attachment) {
          var a = d.attachment;
          r.url = a.url; r.kind = a.kind || r.kind; r.name = a.name || r.name; r.size = a.size || r.size;
          r.mime = a.mime || ''; r.thumbnail_url = a.thumbnail_url || ''; r.thumb = a.thumbnail_url || r.thumb;
        } else { fail((d && d.error) || ('Could not upload ' + file.name)); return; }
        r.uploading = false; r.pct = 100;
        render(); changed();
      };
      xhr.onerror = function () { fail('Network error uploading ' + file.name); };
      xhr.send(fd);
    }

    function accept(file, replacing) {
      var kind = kindOf(file, !!maxImages);
      if (file.size > LIMITS[kind]) { say(LIMIT_TEXT[kind]); return null; }
      var isImage = kind === 'image';
      var others = rows.filter(function (r) { return r !== replacing; });
      var inKind = others.filter(function (r) { return (r.kind === 'image') === isImage; }).length;
      if (inKind >= (isImage ? maxImages : maxMedia)) {
        say(isImage ? 'Up to ' + maxImages + ' images' : 'Up to ' + maxMedia + ' attachments');
        return null;
      }
      if (kind === 'video' && others.some(function (r) { return r.kind === 'video'; })) { say('Only one video per post or reply'); return null; }
      var r = { id: ++seq, kind: kind, name: file.name, size: file.size, url: '', mime: file.type || '', uploading: true, pct: 0,
        thumb: kind === 'image' ? URL.createObjectURL(file) : '' };
      return r;
    }

    function addFiles(files) {
      Array.prototype.slice.call(files || []).forEach(function (f) {
        var r = accept(f, null);
        if (!r) return;
        rows.push(r);
        render(true);
        upload(r, f, null);
      });
      changed();
    }

    function replaceFile(id, file) {
      var old = byId(id);
      if (!old) return;
      var r = accept(file, old);
      if (!r) return;
      rows[rows.indexOf(old)] = r;
      render();
      upload(r, file, old);
      changed();
    }

    function move(id, to) {
      var from = rows.indexOf(byId(id));
      if (from < 0 || to < 0 || to >= rows.length || to === from) return false;
      var before = rects();
      rows.splice(to, 0, rows.splice(from, 1)[0]);
      var li = rowEl(id);
      var ref = list.children[to + (to > from ? 1 : 0)] || null;
      list.insertBefore(li, ref);
      play(before);
      return true;
    }

    /* Drag by the grip: the row follows the pointer, the others slide out of the way. */
    function drag(e, li) {
      e.preventDefault();
      var id = li.getAttribute('data-id');
      var grab = e.clientY - li.getBoundingClientRect().top;
      li.classList.add('is-dragging');
      li.setPointerCapture(e.pointerId);
      function place(y) {
        li.style.transition = 'none';
        li.style.transform = '';
        var natural = li.getBoundingClientRect().top;
        li.style.transform = 'translateY(' + (y - grab - natural) + 'px)';
      }
      function follow(ev) {
        place(ev.clientY);
        var sibs = Array.prototype.slice.call(list.children);
        var idx = sibs.indexOf(li);
        var over = -1;
        sibs.forEach(function (s, i) {
          if (s === li) return;
          var b = s.getBoundingClientRect();
          if (ev.clientY > b.top && ev.clientY < b.bottom) over = i;
        });
        if (over >= 0 && over !== idx) { move(id, over); place(ev.clientY); }
      }
      function end() {
        li.removeEventListener('pointermove', follow);
        li.removeEventListener('pointerup', end);
        li.removeEventListener('pointercancel', end);
        li.classList.remove('is-dragging');
        li.style.transition = 'transform .38s var(--spring, cubic-bezier(.34,1.4,.64,1))';
        li.style.transform = '';
        live.textContent = 'Moved to position ' + (rows.indexOf(byId(id)) + 1) + ' of ' + rows.length;
        changed();
      }
      li.addEventListener('pointermove', follow);
      li.addEventListener('pointerup', end);
      li.addEventListener('pointercancel', end);
    }

    list.addEventListener('pointerdown', function (e) {
      var g = e.target.closest('[data-na="grip"]');
      if (g && e.button === 0) drag(e, g.closest('.na-row'));
    });
    list.addEventListener('keydown', function (e) {
      var g = e.target.closest('[data-na="grip"]');
      if (!g || (e.key !== 'ArrowUp' && e.key !== 'ArrowDown')) return;
      e.preventDefault();
      var id = g.closest('.na-row').getAttribute('data-id');
      var at = rows.indexOf(byId(id));
      if (move(id, at + (e.key === 'ArrowUp' ? -1 : 1))) {
        rowEl(id).querySelector('[data-na="grip"]').focus();
        live.textContent = 'Moved to position ' + (rows.indexOf(byId(id)) + 1) + ' of ' + rows.length;
        changed();
      }
    });
    list.addEventListener('click', function (e) {
      var b = e.target.closest('[data-na]');
      if (!b) return;
      var li = b.closest('.na-row');
      var id = li.getAttribute('data-id');
      if (b.dataset.na === 'remove') {
        li.classList.add('is-leaving');
        var done = function () { rows.splice(rows.indexOf(byId(id)), 1); render(true); changed(); };
        if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) done(); else setTimeout(done, 200);
      } else if (b.dataset.na === 'replace') {
        picking = id; input.multiple = false; input.click();
      }
    });
    input.addEventListener('change', function () {
      var files = input.files;
      if (picking) { if (files[0]) replaceFile(picking, files[0]); }
      else addFiles(files);
      picking = null; input.value = ''; input.multiple = true;
    });

    var api = {
      el: el,
      pick: function () { picking = null; input.multiple = true; input.click(); },
      add: addFiles,
      items: function () { return rows.filter(function (r) { return r.url && !r.uploading; }); },
      media: function () {
        return rows.filter(function (r) { return r.url && !r.uploading && r.kind !== 'image'; }).map(function (r) {
          return { url: r.url, kind: r.kind, name: r.name, mime: r.mime, size: r.size, thumbnail_url: r.thumbnail_url };
        });
      },
      imageUrls: function () { return rows.filter(function (r) { return r.url && !r.uploading && r.kind === 'image'; }).map(function (r) { return r.url; }); },
      busy: function () { return rows.some(function (r) { return r.uploading; }); },
      dirty: function () { return signature() !== start || api.busy(); },
      count: function () { return rows.length; },
      room: function () { return (maxMedia - countKind(false)) > 0 || (maxImages - countKind(true)) > 0; }
    };
    start = signature();
    el._nebAttach = api;
    render();
    return api;
  }

  window.NebAttach = { mount: mount, bytes: bytes };
})();
