(function () {
  'use strict';

  function qs(selector, root) { return (root || document).querySelector(selector); }
  function qsa(selector, root) { return Array.from((root || document).querySelectorAll(selector)); }
  function csrfToken() {
    var match = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : '';
  }
  async function api(url, options) {
    var opts = Object.assign({ credentials: 'same-origin' }, options || {});
    opts.headers = Object.assign({ Accept: 'application/json' }, opts.headers || {});
    var method = String(opts.method || 'GET').toUpperCase();
    if (method !== 'GET' && method !== 'HEAD') opts.headers['X-CSRFToken'] = csrfToken();
    var response = await fetch(url, opts);
    var data;
    try { data = await response.json(); } catch (error) { data = { error: 'Invalid server response' }; }
    if (!response.ok || data.ok === false) {
      var err = new Error(data.error || ('Request failed (' + response.status + ')'));
      err.status = response.status;
      throw err;
    }
    return data;
  }
  function json(url, payload) {
    return api(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload || {}) });
  }
  function toast(message, type, region) {
    var host = region || qs('#ba-global-toast') || document.body;
    var node = document.createElement('div');
    node.className = 'ba-toast ' + (type || '');
    node.textContent = message;
    host.appendChild(node);
    setTimeout(function () { node.remove(); }, 4200);
  }
  function formatBytes(value) {
    var bytes = Number(value || 0);
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(bytes < 10240 ? 1 : 0) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(bytes < 10 * 1024 * 1024 ? 1 : 0) + ' MB';
  }
  function timeAgo(value) {
    var timestamp = Number(value || 0);
    if (!timestamp) return '';
    var seconds = Math.max(0, Math.round((Date.now() - timestamp) / 1000));
    if (seconds < 45) return 'just now';
    if (seconds < 3600) return Math.round(seconds / 60) + 'm ago';
    if (seconds < 86400) return Math.round(seconds / 3600) + 'h ago';
    if (seconds < 604800) return Math.round(seconds / 86400) + 'd ago';
    return new Date(timestamp).toLocaleDateString();
  }
  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }
  function renderInline(value) {
    return value
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*]+)\*/g, '<em>$1</em>')
      .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
  }
  function renderMarkdown(text) {
    var escaped = escapeHtml(text || '');
    var codeBlocks = [];
    escaped = escaped.replace(/```([^\n]*)\n([\s\S]*?)```/g, function (_, language, code) {
      var index = codeBlocks.push('<pre><code data-language="' + language.trim() + '">' + code.replace(/^\n|\n$/g, '') + '</code></pre>') - 1;
      return '\n@@BA_CODE_' + index + '@@\n';
    });
    var lines = escaped.split('\n');
    var output = [];
    var list = null;
    function closeList() { if (list) { output.push('</' + list + '>'); list = null; } }
    lines.forEach(function (line) {
      var codeMatch = line.match(/^@@BA_CODE_(\d+)@@$/);
      if (codeMatch) { closeList(); output.push(codeBlocks[Number(codeMatch[1])]); return; }
      var heading = line.match(/^(#{1,3})\s+(.+)$/);
      if (heading) { closeList(); var level = heading[1].length; output.push('<h' + level + '>' + renderInline(heading[2]) + '</h' + level + '>'); return; }
      var bullet = line.match(/^\s*[-*]\s+(.+)$/);
      if (bullet) { if (list !== 'ul') { closeList(); list = 'ul'; output.push('<ul>'); } output.push('<li>' + renderInline(bullet[1]) + '</li>'); return; }
      var ordered = line.match(/^\s*\d+\.\s+(.+)$/);
      if (ordered) { if (list !== 'ol') { closeList(); list = 'ol'; output.push('<ol>'); } output.push('<li>' + renderInline(ordered[1]) + '</li>'); return; }
      closeList();
      if (/^&gt;\s?/.test(line)) output.push('<blockquote>' + renderInline(line.replace(/^&gt;\s?/, '')) + '</blockquote>');
      else if (line.trim()) output.push('<p>' + renderInline(line) + '</p>');
    });
    closeList();
    return output.join('');
  }
  function fileIcon(name, kind) {
    var ext = String(name || '').toLowerCase().split('.').pop();
    if (kind === 'image' || ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'bmp'].includes(ext)) return 'image';
    if (kind === 'pdf' || ext === 'pdf') return 'picture_as_pdf';
    if (['md', 'markdown'].includes(ext)) return 'markdown';
    if (['js', 'jsx', 'ts', 'tsx', 'py', 'java', 'kt', 'go', 'rs', 'c', 'cpp', 'h', 'hpp', 'html', 'css', 'json', 'yaml', 'yml'].includes(ext)) return 'code';
    if (kind === 'audio') return 'audio_file';
    if (kind === 'video') return 'video_file';
    return 'draft';
  }
  function createAttachmentController(config) {
    var input = config.input;
    var list = config.list;
    var dropZone = config.dropZone;
    var files = [];
    var maxFiles = Number(config.maxFiles || 5);
    var maxBytes = Number(config.maxBytes || 20 * 1024 * 1024);
    function key(file) { return [file.name, file.size, file.lastModified].join(':'); }
    function render() {
      list.innerHTML = '';
      list.hidden = files.length === 0;
      files.forEach(function (file, index) {
        var chip = document.createElement('div');
        chip.className = 'ba-attachment-chip';
        chip.innerHTML = '<span class="material-symbols-outlined">' + fileIcon(file.name) + '</span><span></span><button type="button" aria-label="Remove"><span class="material-symbols-outlined">close</span></button>';
        chip.children[1].textContent = file.name + ' · ' + formatBytes(file.size);
        chip.querySelector('button').addEventListener('click', function () { files.splice(index, 1); render(); });
        list.appendChild(chip);
      });
    }
    function add(incoming) {
      var existing = new Set(files.map(key));
      Array.from(incoming || []).forEach(function (file) {
        if (files.length >= maxFiles) return toast('You can attach up to ' + maxFiles + ' files.', 'error');
        if (file.size > maxBytes) return toast(file.name + ' is larger than ' + formatBytes(maxBytes) + '.', 'error');
        if (!existing.has(key(file))) { files.push(file); existing.add(key(file)); }
      });
      render();
    }
    input.addEventListener('change', function () { add(input.files); input.value = ''; });
    if (dropZone) {
      ['dragenter', 'dragover'].forEach(function (name) { dropZone.addEventListener(name, function (event) { event.preventDefault(); dropZone.classList.add('dragging'); }); });
      ['dragleave', 'drop'].forEach(function (name) { dropZone.addEventListener(name, function (event) { event.preventDefault(); dropZone.classList.remove('dragging'); }); });
      dropZone.addEventListener('drop', function (event) { add(event.dataTransfer.files); });
      dropZone.addEventListener('paste', function (event) {
        var pasted = Array.from(event.clipboardData?.files || []);
        if (pasted.length) add(pasted);
      });
    }
    return { files: function () { return files.slice(); }, clear: function () { files = []; render(); }, add: add };
  }
  function splitDiff(diff) {
    var source = String(diff || '');
    if (!source.trim()) return [];
    var chunks = source.split(/(?=^diff --git )/m).filter(Boolean);
    return chunks.map(function (chunk) {
      var header = chunk.match(/^diff --git a\/(.+?) b\/(.+)$/m);
      var plus = chunk.match(/^\+\+\+ b\/(.+)$/m);
      var minus = chunk.match(/^--- a\/(.+)$/m);
      var path = (plus && plus[1]) || (header && header[2]) || (minus && minus[1]) || 'Changed file';
      var added = 0, removed = 0;
      chunk.split('\n').forEach(function (line) {
        if (line.startsWith('+') && !line.startsWith('+++')) added += 1;
        if (line.startsWith('-') && !line.startsWith('---')) removed += 1;
      });
      return { path: path, added: added, removed: removed, text: chunk };
    });
  }

  window.BA = { qs: qs, qsa: qsa, api: api, json: json, toast: toast, formatBytes: formatBytes, timeAgo: timeAgo, escapeHtml: escapeHtml, renderMarkdown: renderMarkdown, fileIcon: fileIcon, createAttachmentController: createAttachmentController, splitDiff: splitDiff };
})();
