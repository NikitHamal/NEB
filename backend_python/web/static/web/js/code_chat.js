(function () {
  'use strict';

  function cleanSecondary(target) {
    if (!target || typeof target !== 'string') return '';
    var trimmed = target.trim();
    if (trimmed.length <= 40) return trimmed;
    var base = trimmed.split(/[\\/]/).pop();
    if (base && base.length <= 36) return base;
    return trimmed.slice(0, 36) + '…';
  }

  function mapToolToChip(data) {
    var tool = data.tool || data.name || '';
    var args = data.args || {};
    var icon = 'run';
    var label = 'Run';
    var chip = '';
    var mono = true;
    var detailMono = true;
    var detail = [];

    if (tool === 'list_dir') {
      icon = 'read';
      label = 'List';
      chip = cleanSecondary(args.path || args.DirectoryPath || '.');
      if (data.result) {
        detail.push({ text: 'Listed files in ' + chip });
      }
    } else if (tool === 'view_file' || tool === 'read_file') {
      icon = 'read';
      label = 'Read';
      chip = cleanSecondary(args.path || args.AbsolutePath || '');
      if (args.StartLine && args.EndLine) {
        label = 'Read L' + args.StartLine + '-' + args.EndLine;
      }
      if (data.result) {
        var linesCount = String(data.result).split('\n').length;
        detail.push({ text: 'Read ' + linesCount + ' lines' });
      }
    } else if (tool === 'write_file' || tool === 'edit_file' || tool === 'replace_file_content' || tool === 'multi_replace_file_content') {
      icon = 'write';
      chip = cleanSecondary(args.path || args.TargetFile || args.file || '');
      var content = args.content || args.ReplacementContent || args.CodeContent || '';
      var lines = content ? content.split('\n').length : (data.lines || 1);
      label = 'Write ' + lines + ' line' + (lines === 1 ? '' : 's');
      if (args.TargetContent) {
        detail.push({ text: '- ' + String(args.TargetContent).trim().slice(0, 80), tone: 'del' });
      }
      if (args.ReplacementContent) {
        detail.push({ text: '+ ' + String(args.ReplacementContent).trim().slice(0, 80), tone: 'add' });
      }
    } else if (tool === 'run_command' || tool === 'exec' || tool === 'terminal') {
      icon = 'run';
      label = 'Run';
      chip = cleanSecondary(args.command || args.CommandLine || args.cmd || '');
      if (data.result) {
        var firstLine = String(data.result).trim().split('\n')[0];
        if (firstLine) detail.push({ text: '✓ ' + firstLine.slice(0, 80) });
      }
    } else if (tool === 'grep_search' || tool === 'search') {
      icon = 'read';
      label = 'Search';
      chip = cleanSecondary(args.query || args.Query || args.pattern || '');
      if (data.result) {
        detail.push({ text: 'Found matches for ' + chip });
      }
    } else {
      icon = 'run';
      label = tool || 'Tool';
      chip = cleanSecondary(args.path || args.Query || args.CommandLine || JSON.stringify(args));
    }

    return {
      icon: icon,
      label: label,
      chip: chip,
      mono: mono,
      detailMono: detailMono,
      detail: detail
    };
  }

  function extractThoughts(raw) {
    var thought = '';
    var content = String(raw || '');

    var thoughtMatch = content.match(/<(?:thought|thinking)>([\s\S]*?)<\/(?:thought|thinking)>/i);
    if (thoughtMatch) {
      thought = thoughtMatch[1].trim();
      content = content.replace(/<(?:thought|thinking)>[\s\S]*?<\/(?:thought|thinking)>/gi, '').trim();
    } else {
      var unclosed = content.match(/<(?:thought|thinking)>([\s\S]*)$/i);
      if (unclosed) {
        thought = unclosed[1].trim();
        content = content.replace(/<(?:thought|thinking)>[\s\S]*$/gi, '').trim();
      }
    }
    return { thought: thought, content: content };
  }

  function NebyCodeChat(options) {
    this.UI = window.CodeUI;
    this.Panels = window.CodePanels;
    this.transcript = options.transcript;
    this.onPrompt = options.onPrompt || function () {};
    this.live = null;
    this.liveText = '';
    this.liveTools = {};
    this.livePlan = null;
    this.toolChips = null;
    this.trace = null;
    this.startTime = 0;
    this._bindCopy();
  }

  NebyCodeChat.prototype.markdown = function (text) {
    var self = this;
    var raw = String(text || '');
    var tokens = [];

    // 1. Process code fences (3 or 4 backticks, closed or unclosed during stream)
    raw = raw.replace(/(?:````|```)([\w.+-]*)\n?([\s\S]*?)(?:(?:````|```)|$)/g, function (match, lang, code) {
      var token = '@@NC_CODE_' + tokens.length + '@@';
      var highlighted = self.Panels ? self.Panels.highlight(code.replace(/\n$/, ''), lang || '') : self.UI.esc(code);
      tokens.push(
        '<div class="nc-code-block">' +
          '<div class="nc-code-header">' +
            '<span class="nc-code-lang">' + self.UI.esc(lang || 'code') + '</span>' +
            '<button type="button" class="nc-copy-btn"><span class="material-symbols-outlined">content_copy</span><span>Copy</span></button>' +
          '</div>' +
          '<pre><code>' + highlighted + '</code></pre>' +
        '</div>'
      );
      return token;
    });

    // 2. Process Markdown tables
    raw = raw.replace(/(?:^|\n)(\|[^\n]+\|\r?\n\|[-:\s|]+\|\r?\n(?:\|[^\n]+\|\r?\n?)*)/g, function (match, tableBlock) {
      var lines = tableBlock.trim().split(/\r?\n/).filter(Boolean);
      if (lines.length < 2) return match;
      var headerCols = lines[0].split('|').slice(1, -1).map(function (c) { return c.trim(); });
      var bodyLines = lines.slice(2);

      var tableHtml = '<div class="nc-table-wrap"><table class="nc-table"><thead><tr>' +
        headerCols.map(function (c) {
          var h = self.UI.esc(c).replace(/`([^`\n]+)`/g, '<code>$1</code>').replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>');
          return '<th>' + h + '</th>';
        }).join('') +
        '</tr></thead><tbody>' +
        bodyLines.map(function (row) {
          var rowCols = row.split('|').slice(1, -1).map(function (c) { return c.trim(); });
          return '<tr>' + rowCols.map(function (c) {
            var cell = self.UI.esc(c)
              .replace(/`([^`\n]+)`/g, '<code>$1</code>')
              .replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>')
              .replace(/\*([^*\n]+)\*/g, '<em>$1</em>');
            return '<td>' + cell + '</td>';
          }).join('') + '</tr>';
        }).join('') +
        '</tbody></table></div>';

      var token = '@@NC_CODE_' + tokens.length + '@@';
      tokens.push(tableHtml);
      return '\n\n' + token + '\n\n';
    });

    // 3. Escape HTML
    var html = self.UI.esc(raw);

    // 4. Inline formatting
    html = html
      .replace(/`([^`\n]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*\n]+)\*/g, '<em>$1</em>')
      .replace(/^###\s+(.+)$/gm, '<h4>$1</h4>')
      .replace(/^##\s+(.+)$/gm, '<h3>$1</h3>')
      .replace(/^#\s+(.+)$/gm, '<h2>$1</h2>')
      .replace(/^[-*]\s+(.+)$/gm, '<li>$1</li>')
      .replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>')
      .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');

    // 5. Group list items into ul
    html = html.replace(/(?:<li>[\s\S]*?<\/li>\s*)+/g, function (items) {
      return '<ul>' + items + '</ul>';
    });

    // 6. Break into paragraphs
    html = html.split(/\n{2,}/).map(function (block) {
      block = block.trim();
      if (!block) return '';
      if (/^<(?:div|h2|h3|h4|ul|ol|blockquote)/.test(block) || /^@@NC_CODE_\d+@@$/.test(block)) return block;
      return '<p>' + block.replace(/\n/g, '<br>') + '</p>';
    }).join('');

    // 7. Restore tokens
    tokens.forEach(function (value, index) {
      html = html.replace('@@NC_CODE_' + index + '@@', value);
    });

    return html;
  };

  NebyCodeChat.prototype.thread = function () {
    var node = this.transcript.querySelector('.nc-thread');
    if (!node) {
      node = document.createElement('div');
      node.className = 'nc-thread';
      this.transcript.appendChild(node);
    }
    return node;
  };

  NebyCodeChat.prototype.scrollBottom = function () {
    var transcript = this.transcript;
    requestAnimationFrame(function () { transcript.scrollTop = transcript.scrollHeight; });
  };

  NebyCodeChat.prototype.renderHero = function () {
    var self = this;
    this.resetLive();
    this.transcript.innerHTML = '<div class="nc-empty-hero"><div class="nc-empty-kicker"><span class="material-symbols-outlined">terminal</span><span>Neby Code · local agent</span></div><h1>Build directly in your workspace.</h1><p>Connect your machine, then let Neby inspect the repository, edit files, use Git, and run commands without an artificial tool-call budget.</p><div class="nc-quick-grid"><button class="nc-quick-action" data-prompt="Inspect this repository and explain the architecture, entry points, and important development commands."><span class="material-symbols-outlined">account_tree</span><span><strong>Understand the codebase</strong><small>Map architecture and entry points before making changes.</small></span></button><button class="nc-quick-action" data-prompt="Run the relevant checks, find the current failures, fix them, and verify the result end to end."><span class="material-symbols-outlined">build</span><span><strong>Fix what is broken</strong><small>Run checks, patch the root cause, and verify.</small></span></button><button class="nc-quick-action" data-prompt="Review the current git diff for correctness, regressions, maintainability, and performance. Fix any issues you find."><span class="material-symbols-outlined">difference</span><span><strong>Review my changes</strong><small>Inspect the real working tree and improve it.</small></span></button><button class="nc-quick-action" data-prompt="Implement the feature I describe next using the existing architecture and conventions. Inspect the relevant files first."><span class="material-symbols-outlined">code</span><span><strong>Implement a feature</strong><small>Work from the existing patterns instead of scaffolding noise.</small></span></button></div></div>';
    this.transcript.querySelectorAll('[data-prompt]').forEach(function (button) {
      button.addEventListener('click', function () { self.onPrompt(button.getAttribute('data-prompt')); });
    });
  };

  NebyCodeChat.prototype.addUser = function (text) {
    var node = document.createElement('div');
    node.className = 'msg-user';
    node.textContent = text;
    this.thread().appendChild(node);
    this.scrollBottom();
  };

  NebyCodeChat.prototype.addAssistant = function (text, thoughtText) {
    var extracted = extractThoughts(text);
    var cleanContent = extracted.content || text;
    var thoughts = thoughtText || extracted.thought;

    var wrap = document.createElement('div');
    wrap.className = 'msg-assistant';

    if (thoughts && window.AIWidgets && window.AIWidgets.Trace) {
      var lines = thoughts.split(/\n+/).filter(Boolean).slice(0, 10);
      var rows = lines.map(function (line) {
        return { primary: line.trim() };
      });
      var trace = window.AIWidgets.Trace.create({
        variant: 'reasoning',
        active: 'Thinking…',
        done: 'Thought Process',
        rows: rows,
        settleDelay: 0,
      });
      trace.settle('Thought Process');
      wrap.appendChild(trace.el);
    }

    var mdNode = document.createElement('div');
    mdNode.className = 'nc-md';
    mdNode.innerHTML = this.markdown(cleanContent);
    wrap.appendChild(mdNode);

    this.thread().appendChild(wrap);
    this.scrollBottom();
  };

  NebyCodeChat.prototype.addError = function (text) {
    var node = document.createElement('div');
    node.className = 'msg-error';
    node.textContent = text;
    this.thread().appendChild(node);
    this.scrollBottom();
  };

  NebyCodeChat.prototype.renderTranscript = function (messages) {
    var self = this;
    this.resetLive();
    this.transcript.innerHTML = '';
    if (!messages || !messages.length) {
      this.renderHero();
      return;
    }

    var turns = [];
    var currentAssistantTurn = null;

    messages.forEach(function (msg) {
      if (msg.role === 'user') {
        currentAssistantTurn = null;
        turns.push({ type: 'user', content: msg.content || '' });
      } else if (msg.role === 'event') {
        var meta = msg.meta || {};
        if (meta.type === 'error' && msg.content) {
          turns.push({ type: 'error', content: msg.content });
        } else if (meta.type === 'tool_call' || meta.type === 'tool_result' || meta.type === 'plan') {
          if (!currentAssistantTurn) {
            currentAssistantTurn = { type: 'assistant', tools: [], plans: [], thoughts: [], texts: [] };
            turns.push(currentAssistantTurn);
          }
          if (meta.type === 'tool_call') {
            currentAssistantTurn.tools.push(meta);
          } else if (meta.type === 'plan') {
            currentAssistantTurn.plans.push(meta.todos || []);
          }
        }
      } else if (msg.role === 'assistant') {
        if (!currentAssistantTurn) {
          currentAssistantTurn = { type: 'assistant', tools: [], plans: [], thoughts: [], texts: [] };
          turns.push(currentAssistantTurn);
        }
        var extracted = extractThoughts(msg.content || '');
        if (extracted.thought) currentAssistantTurn.thoughts.push(extracted.thought);
        if (msg.meta && msg.meta.thought) currentAssistantTurn.thoughts.push(msg.meta.thought);
        if (extracted.content) currentAssistantTurn.texts.push(extracted.content);
      }
    });

    turns.forEach(function (turn) {
      if (turn.type === 'user') {
        self.addUser(turn.content);
      } else if (turn.type === 'error') {
        self.addError(turn.content);
      } else if (turn.type === 'assistant') {
        var wrap = document.createElement('div');
        wrap.className = 'msg-assistant';

        // 1. Render ToolChips / Trace for tools
        if (turn.tools && turn.tools.length) {
          if (window.AIWidgets && window.AIWidgets.ToolChips) {
            var chipRows = turn.tools.map(mapToolToChip);
            var tc = window.AIWidgets.ToolChips.create({
              reveal: 'instant',
              calls: chipRows.length,
              messages: turn.texts ? turn.texts.length : 1,
              rows: chipRows,
              open: true,
            });
            wrap.appendChild(tc.el);
          } else if (window.AIWidgets && window.AIWidgets.Trace) {
            var rows = turn.tools.map(function (t) {
              var c = mapToolToChip(t);
              return { primary: c.label, secondary: c.chip, mono: true };
            });
            var trace = window.AIWidgets.Trace.create({
              variant: 'reasoning',
              active: 'Ran ' + rows.length + ' tools',
              done: 'Ran ' + rows.length + ' tools',
              rows: rows,
              settleDelay: 0,
            });
            trace.settle('Ran ' + rows.length + ' tools');
            wrap.appendChild(trace.el);
          }
        }

        // 2. Render Reasoning Thoughts if any
        if (turn.thoughts && turn.thoughts.length) {
          if (window.AIWidgets && window.AIWidgets.Trace) {
            var tRows = [];
            turn.thoughts.forEach(function (th) {
              th.split(/\n+/).filter(Boolean).slice(0, 6).forEach(function (l) {
                tRows.push({ primary: l.trim() });
              });
            });
            var tTrace = window.AIWidgets.Trace.create({
              variant: 'reasoning',
              active: 'Thought Process',
              done: 'Thought Process',
              rows: tRows,
              settleDelay: 0,
            });
            tTrace.settle('Thought Process');
            wrap.appendChild(tTrace.el);
          }
        }

        // 3. Render Plans if any
        if (turn.plans && turn.plans.length) {
          var latestPlan = turn.plans[turn.plans.length - 1];
          var planEl = document.createElement('div');
          planEl.className = 'nc-plan';
          var complete = latestPlan.filter(function (it) { return it.status === 'completed'; }).length;
          planEl.innerHTML = '<div class="nc-plan-head"><span class="material-symbols-outlined">checklist</span><span>Plan · ' + complete + '/' + latestPlan.length + '</span></div><div class="nc-plan-list">' + latestPlan.map(function (item) {
            var icon = item.status === 'completed' ? 'check_circle' : (item.status === 'in_progress' ? 'progress_activity' : 'radio_button_unchecked');
            return '<div class="nc-plan-row ' + String(item.status || 'pending') + '"><span class="material-symbols-outlined">' + icon + '</span><span>' + window.CodeUI.esc(item.content || '') + '</span></div>';
          }).join('') + '</div>';
          wrap.appendChild(planEl);
        }

        // 4. Render Assistant Response Markdown
        var fullText = (turn.texts || []).join('\n\n').trim();
        if (fullText) {
          var mdNode = document.createElement('div');
          mdNode.className = 'nc-md';
          mdNode.innerHTML = self.markdown(fullText);
          wrap.appendChild(mdNode);
        }

        self.thread().appendChild(wrap);
      }
    });

    this.scrollBottom();
  };

  NebyCodeChat.prototype.ensureLive = function () {
    if (this.live) return this.live;
    var wrap = document.createElement('div');
    wrap.className = 'msg-assistant';

    this.startTime = Date.now();
    if (window.AIWidgets && window.AIWidgets.ToolChips) {
      this.toolChips = window.AIWidgets.ToolChips.create({
        reveal: 'instant',
        calls: 0,
        messages: 1,
        rows: [],
      });
      wrap.appendChild(this.toolChips.el);
    } else if (window.AIWidgets && window.AIWidgets.Trace) {
      this.trace = window.AIWidgets.Trace.create({
        variant: 'reasoning',
        active: 'Thinking…',
        settleDelay: 86400000,
        rows: [],
      });
      wrap.appendChild(this.trace.el);
    }

    var text = document.createElement('div');
    text.className = 'nc-md';
    wrap.appendChild(text);

    this.thread().appendChild(wrap);
    this.live = { wrap: wrap, text: text };
    this.liveText = '';
    this.liveTools = {};
    this.livePlan = null;
    this.scrollBottom();
    return this.live;
  };

  NebyCodeChat.prototype.setStatus = function (data) {
    this.ensureLive();
    var phase = data.phase || 'working';
    var count = Number(data.tool_count || Object.keys(this.liveTools).length || 0);
    var label = phase === 'thinking' ? 'Thinking…' : phase === 'retrying' ? 'Switching model provider…' : phase === 'cancelling' ? 'Stopping…' : 'Working…';
    if (count) label = 'Working · ' + count + ' step' + (count === 1 ? '' : 's');

    if (this.trace && this.trace.setLabel) {
      this.trace.setLabel(label);
    }
    this.scrollBottom();
  };

  NebyCodeChat.prototype.appendDelta = function (text) {
    var live = this.ensureLive();
    this.liveText += String(text || '');

    var extracted = extractThoughts(this.liveText);

    if (extracted.thought && this.trace) {
      var lines = extracted.thought.split(/\n+/).filter(Boolean).slice(-6);
      var rows = lines.map(function (line) { return { primary: line.trim() }; });
      this.trace.setRows(rows);
      this.trace.setLabel('Thinking…');
    }

    live.text.innerHTML = this.markdown(extracted.content);
    this.scrollBottom();
  };

  NebyCodeChat.prototype.toolCall = function (data) {
    this.ensureLive();
    var callId = data.call_id || ('call_' + Math.random().toString(36).slice(2));
    this.liveTools[callId] = data;

    var chipRow = mapToolToChip(data);

    if (this.toolChips && this.toolChips.addRow) {
      this.toolChips.addRow(chipRow);
    } else if (this.trace && this.trace.addRow) {
      this.trace.addRow({
        primary: chipRow.label,
        secondary: chipRow.chip,
        mono: true,
      });
      var count = Object.keys(this.liveTools).length;
      this.trace.setLabel('Working · ' + count + ' step' + (count === 1 ? '' : 's'));
    }
    this.scrollBottom();
  };

  NebyCodeChat.prototype.toolResult = function (data) {
    if (data.call_id && this.liveTools[data.call_id]) {
      this.liveTools[data.call_id].result = data.result || data.output || '';
    }
  };

  NebyCodeChat.prototype.renderPlan = function (todos) {
    this.ensureLive();
    if (!this.livePlan) {
      this.livePlan = document.createElement('div');
      this.livePlan.className = 'nc-plan';
      this.live.wrap.insertBefore(this.livePlan, this.live.text);
    }
    var complete = (todos || []).filter(function (item) { return item.status === 'completed'; }).length;
    this.livePlan.innerHTML = '<div class="nc-plan-head"><span class="material-symbols-outlined">checklist</span><span>Plan · ' + complete + '/' + (todos || []).length + '</span></div><div class="nc-plan-list">' + (todos || []).map(function (item) {
      var icon = item.status === 'completed' ? 'check_circle' : (item.status === 'in_progress' ? 'progress_activity' : 'radio_button_unchecked');
      return '<div class="nc-plan-row ' + String(item.status || 'pending') + '"><span class="material-symbols-outlined">' + icon + '</span><span>' + window.CodeUI.esc(item.content || '') + '</span></div>';
    }).join('') + '</div>';
    this.scrollBottom();
  };

  NebyCodeChat.prototype.finishLive = function () {
    if (this.toolChips && this.toolChips.setHeader) {
      var count = Object.keys(this.liveTools).length;
      this.toolChips.setHeader(count, 1);
    } else if (this.trace && this.trace.settle) {
      var elapsed = Math.max(0.6, ((Date.now() - (this.startTime || Date.now())) / 1000)).toFixed(1);
      var count = Object.keys(this.liveTools).length;
      var doneText = count ? ('Completed ' + count + ' step' + (count === 1 ? '' : 's') + ' in ' + elapsed + 's') : ('Thought for ' + elapsed + 's');
      this.trace.settle(doneText);
    }
  };

  NebyCodeChat.prototype.removeLive = function () {
    if (this.live && this.live.wrap && this.live.wrap.parentNode) this.live.wrap.remove();
    this.resetLive();
  };

  NebyCodeChat.prototype.resetLive = function () {
    this.live = null;
    this.liveText = '';
    this.liveTools = {};
    this.livePlan = null;
    this.toolChips = null;
    this.trace = null;
    this.startTime = 0;
  };

  NebyCodeChat.prototype._bindCopy = function () {
    var self = this;
    this.transcript.addEventListener('click', function (event) {
      var button = event.target.closest('.nc-copy-btn');
      if (!button) return;
      var block = button.closest('.nc-code-block');
      var code = block && block.querySelector('code');
      if (!code) return;
      navigator.clipboard.writeText(code.textContent || '').then(function () {
        var oldHtml = button.innerHTML;
        button.innerHTML = '<span class="material-symbols-outlined" style="font-size:13.5px;color:var(--ncu-accent)">check</span><span style="color:var(--ncu-accent)">Copied!</span>';
        setTimeout(function () { button.innerHTML = oldHtml; }, 1800);
      }).catch(function () { self.UI.toast('Unable to copy'); });
    });
  };

  window.NebyCodeChat = NebyCodeChat;
})();
