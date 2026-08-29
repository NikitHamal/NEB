/* Lazy workspace — DOM builders.
 *
 * Pure functions that turn data into elements. No state, no network. Keeping
 * rendering separate means the controller can stay readable and the same card
 * can be reused for a live run and for a replayed one.
 */

(() => {
  'use strict';

  const fmt = () => window.LazyApi.fmt;

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = String(text);
    return node;
  }

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  /** Very small markdown-ish renderer: headings, lists, code, bold, italic. */
  function renderRichText(text) {
    const source = String(text || '');
    if (!source.trim()) return '';
    const lines = source.split('\n');
    const out = [];
    let inList = null;
    let inCode = false;

    const closeList = () => {
      if (inList) {
        out.push(`</${inList}>`);
        inList = null;
      }
    };

    for (const raw of lines) {
      const line = raw.trimEnd();
      if (/^\s*```/.test(line)) {
        closeList();
        out.push(inCode ? '</code></pre>' : '<pre class="lz-md-code"><code>');
        inCode = !inCode;
        continue;
      }
      if (inCode) {
        out.push(`${escapeHtml(raw)}\n`);
        continue;
      }
      if (!line.trim()) {
        closeList();
        continue;
      }
      const heading = line.match(/^(#{1,4})\s+(.*)$/);
      if (heading) {
        closeList();
        const level = Math.min(heading[1].length + 1, 5);
        out.push(`<h${level}>${inline(heading[2])}</h${level}>`);
        continue;
      }
      const bullet = line.match(/^\s*[-*•]\s+(.*)$/);
      const numbered = line.match(/^\s*\d+[.)]\s+(.*)$/);
      if (bullet || numbered) {
        const tag = bullet ? 'ul' : 'ol';
        if (inList !== tag) {
          closeList();
          out.push(`<${tag}>`);
          inList = tag;
        }
        out.push(`<li>${inline((bullet || numbered)[1])}</li>`);
        continue;
      }
      closeList();
      out.push(`<p>${inline(line)}</p>`);
    }
    closeList();
    if (inCode) out.push('</code></pre>');
    return out.join('');
  }

  function inline(text) {
    return escapeHtml(text)
      .replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g, (m, label, url) => {
        return `<a href="${url}" target="_blank" rel="noopener">${label}</a>`;
      })
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/(^|\W)_([^_]+)_(?=\W|$)/g, '$1<em>$2</em>');
  }

  // ------------------------------------------------------------------
  // Conversation pieces
  // ------------------------------------------------------------------

  function userMessage(content, attachments, at) {
    const wrap = el('div', 'lz-msg lz-msg--user');
    const bubble = el('div', 'lz-bubble');
    bubble.textContent = content;
    wrap.appendChild(bubble);
    if (attachments && attachments.length) {
      const row = el('div', 'lz-msg-attachments');
      attachments.forEach((a) => {
        const chip = el('span', 'lz-att-chip');
        chip.textContent = a.name || 'file';
        row.appendChild(chip);
      });
      wrap.appendChild(row);
    }
    if (at) wrap.appendChild(el('time', 'lz-msg-time', fmt().formatClock(at)));
    return wrap;
  }

  function agentMessage(content, at) {
    const wrap = el('div', 'lz-msg lz-msg--agent');
    const avatar = el('div', 'lz-avatar', 'L');
    const body = el('div', 'lz-msg-body');
    const rich = el('div', 'lz-rich');
    rich.innerHTML = renderRichText(content);
    body.appendChild(rich);
    wrap.appendChild(avatar);
    wrap.appendChild(body);
    if (at) body.appendChild(el('time', 'lz-msg-time', fmt().formatClock(at)));
    return wrap;
  }

  /** A running narration line ("Researching sources…") shown while working. */
  function narration(text) {
    const node = el('div', 'lz-narration');
    node.appendChild(el('span', 'lz-narration-dot'));
    node.appendChild(el('span', 'lz-narration-text', text));
    return node;
  }

  /** Collapsible record of one tool call. */
  function toolCard({ name, args, label }) {
    const card = el('div', 'lz-tool lz-tool--running');
    card.dataset.tool = name || '';

    const head = el('button', 'lz-tool-head');
    head.type = 'button';
    head.appendChild(el('span', 'lz-tool-icon', toolIcon(name)));
    head.appendChild(el('span', 'lz-tool-label', label || fmt().toolLabel(name, args)));
    const badge = el('span', 'lz-tool-badge', 'running');
    head.appendChild(badge);
    head.appendChild(el('span', 'lz-tool-caret', '›'));
    card.appendChild(head);

    const body = el('div', 'lz-tool-body');
    if (args && Object.keys(args).length) {
      const pre = el('pre', 'lz-tool-args');
      pre.textContent = fmt().summariseArgs(args);
      body.appendChild(pre);
    }
    card.appendChild(body);

    head.addEventListener('click', () => {
      card.classList.toggle('lz-tool--open');
    });
    return card;
  }

  function settleToolCard(card, ok, summary, durationMs) {
    if (!card) return;
    card.classList.remove('lz-tool--running');
    card.classList.add(ok ? 'lz-tool--ok' : 'lz-tool--err');
    const badge = card.querySelector('.lz-tool-badge');
    if (badge) badge.textContent = ok ? (durationMs ? fmt().formatDuration(durationMs) : 'done') : 'failed';
    const body = card.querySelector('.lz-tool-body');
    if (summary && body) {
      const line = el('pre', 'lz-tool-result');
      line.textContent = String(summary).slice(0, 600);
      body.appendChild(line);
    }
  }

  function toolIcon(name) {
    const map = {
      web_search: '🔎', web_fetch: '🌐', build_document: '📄', create_document: '📄',
      create_pdf: '📕', create_slides: '📊', create_spreadsheet: '📗', create_diagram: '🗺️',
      create_chart: '📈', write_file: '✍️', read_file: '📖', read_upload: '📎',
      list_files: '📂', run_python: '🐍', run_command: '⚙️', zip_files: '🗜️',
      pdf_tool: '🧾', analyze_data: '🔬', humanize_text: '✨', translate_text: '🌏',
      spawn_subagents: '🧠', save_preview: '👁️',
    };
    return map[name] || '⚡';
  }

  /**
   * Artifact card. `onClick` opens the inline viewer; the download link is a
   * plain anchor so the browser handles it natively.
   */
  function artifactCard(artifact, onClick) {
    const { name, size, kind, url, mime } = artifact;
    const resolvedKind = kind || fmt().kindOf(name, mime);
    const card = el('div', 'lz-art');
    card.dataset.kind = resolvedKind;

    const icon = el('div', 'lz-art-icon', artifactEmoji(resolvedKind));
    card.appendChild(icon);

    const mid = el('div', 'lz-art-mid');
    mid.appendChild(el('div', 'lz-art-name', name || 'file'));
    mid.appendChild(el('div', 'lz-art-meta', `${kindLabel(resolvedKind)} · ${fmt().formatSize(size)}`));
    card.appendChild(mid);

    const actions = el('div', 'lz-art-actions');
    if (url) {
      const view = el('button', 'lz-btn lz-btn--sm', 'Preview');
      view.type = 'button';
      view.addEventListener('click', () => onClick && onClick(artifact));
      actions.appendChild(view);

      const link = el('a', 'lz-btn lz-btn--sm lz-btn--solid', 'Download');
      link.href = url;
      link.setAttribute('download', name || '');
      actions.appendChild(link);
    }
    card.appendChild(actions);
    return card;
  }

  function artifactEmoji(kind) {
    const map = {
      image: '🖼️', pdf: '📕', doc: '📘', slides: '📊', sheet: '📗',
      archive: '🗜️', html: '🌐', code: '⌨️', file: '📄',
    };
    return map[kind] || '📄';
  }

  function kindLabel(kind) {
    const map = {
      image: 'Image', pdf: 'PDF', doc: 'Word', slides: 'Slides',
      sheet: 'Spreadsheet', archive: 'Archive', html: 'Page', code: 'Code', file: 'File',
    };
    return map[kind] || 'File';
  }

  function planItem(item) {
    const li = el('li', 'lz-plan-item');
    li.dataset.status = item.status || 'pending';
    li.appendChild(el('span', 'lz-plan-tick', planTick(item.status)));
    li.appendChild(el('span', 'lz-plan-text', item.text || ''));
    return li;
  }

  function planTick(status) {
    if (status === 'done') return '✓';
    if (status === 'failed') return '!';
    if (status === 'active') return '◐';
    return '○';
  }

  function activityRow({ icon, label, detail, tone }) {
    const li = el('li', 'lz-act');
    if (tone) li.dataset.tone = tone;
    li.appendChild(el('span', 'lz-act-icon', icon || '•'));
    const body = el('div', 'lz-act-body');
    body.appendChild(el('div', 'lz-act-label', label || ''));
    if (detail) body.appendChild(el('div', 'lz-act-detail', detail));
    li.appendChild(body);
    return li;
  }

  function fileRow(file, onOpen) {
    const li = el('li', 'lz-file');
    const ext = fmt().extensionOf(file.name);
    li.appendChild(el('span', 'lz-file-icon', artifactEmoji(fmt().kindOf(file.name, ''))));
    const name = el('span', 'lz-file-name', file.name);
    li.appendChild(name);
    li.appendChild(el('span', 'lz-file-size', fmt().formatSize(file.size)));
    li.addEventListener('click', () => onOpen && onOpen(file));
    li.dataset.ext = ext;
    return li;
  }

  function threadItem(session, active) {
    const li = el('li', 'lz-thread' + (active ? ' lz-thread--active' : ''));
    li.dataset.session = session.id;
    li.appendChild(el('div', 'lz-thread-title', session.title || 'New thread'));
    const meta = el('div', 'lz-thread-meta');
    meta.textContent = fmt().formatDay(session.updatedAt);
    li.appendChild(meta);
    return li;
  }

  function emptyState(title, text) {
    const wrap = el('div', 'lz-empty');
    wrap.appendChild(el('h2', null, title));
    wrap.appendChild(el('p', null, text));
    return wrap;
  }

  function suggestionCard(title, text, prompt) {
    const card = el('button', 'lz-suggest');
    card.type = 'button';
    card.appendChild(el('div', 'lz-suggest-title', title));
    card.appendChild(el('div', 'lz-suggest-text', text));
    card.dataset.prompt = prompt;
    return card;
  }

  window.LazyDom = {
    el, escapeHtml, renderRichText,
    userMessage, agentMessage, narration, toolCard, settleToolCard,
    artifactCard, planItem, activityRow, fileRow, threadItem,
    emptyState, suggestionCard,
    kindLabel, artifactEmoji,
  };
})();
