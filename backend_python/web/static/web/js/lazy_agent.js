/* Lazy agent workspace — main controller.
 *
 * Vanilla JS class that wires the prompt bar, SSE event stream and the
 * right-rail plan/activity/artifacts panels together. No framework, no build
 * step — matches the rest of the project.
 */

(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const config = window.LAZY_AGENT_CONFIG || {};
  const csrf = () => config.csrfToken || document.querySelector('meta[name="csrf-token"]')?.content || '';

  const TEMPLATES = {
    assignment: 'Write a NEB-grade assignment on the topic: [TOPIC]. Cover the topic thoroughly with a proper introduction, main body, discussion and conclusion, and include a references section.',
    lab: 'Write a NEB Grade 12 lab report on the experiment: [TOPIC]. Include objective, theory, apparatus, procedure, observation table, calculation, result, discussion, conclusion, precautions.',
    slides: 'Build a NEB-class presentation on [TOPIC]. 10-12 slides with a clear structure: title, agenda, key concepts, worked examples, common mistakes, summary. Include speaker notes for each slide.',
    code: 'Build a small project: [TOPIC]. Create the project files inside a single folder, write the code, run it to verify it works, and return a downloadable .zip.',
  };

  class LazyWorkspace {
    constructor() {
      this.state = {
        runId: null,
        sessionId: null,
        status: 'idle',
        artifacts: [],
        plan: [],
        steps: 0,
        docHtml: '',
        startedAt: 0,
        eventSource: null,
      };
      this.dom = {
        root: $('lzAgentRoot'),
        prompt: $('lzPrompt'),
        send: $('lzSend'),
        cancel: $('lzCancel'),
        model: $('lzModel'),
        newBtn: $('lzNew'),
        newThread: $('lzNewThread'),
        threads: $('lzThreads'),
        tabs: document.querySelectorAll('.lz-tab'),
        panes: document.querySelectorAll('.lz-tabs-pane'),
        docFrame: $('lzDocFrame'),
        slidesFrame: $('lzSlidesFrame'),
        sheetsFrame: $('lzSheetsFrame'),
        codeFrame: $('lzCodeFrame'),
        files: $('lzFiles'),
        plan: $('lzPlan'),
        steps: $('lzSteps'),
        stepsCount: $('lzStepsCount'),
        artifacts: $('lzArtifacts'),
        status: $('lzStatus'),
        pill: $('lzPill'),
      };
      this.bind();
    }

    bind() {
      this.dom.prompt.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.submit();
        }
      });
      this.dom.prompt.addEventListener('input', () => this.autoresize());
      this.dom.send.addEventListener('click', () => this.submit());
      this.dom.cancel.addEventListener('click', () => this.cancel());
      this.dom.newBtn.addEventListener('click', () => this.reset());
      this.dom.newThread.addEventListener('click', () => this.reset());
      this.dom.tabs.forEach((tab) => tab.addEventListener('click', () => this.activateTab(tab.dataset.tab)));
      document.querySelectorAll('.lz-chip').forEach((chip) => chip.addEventListener('click', () => this.applyTemplate(chip.dataset.template)));
      this.populateThreads((config.sessions || []).map((s) => ({ id: s.id, title: s.docTitle || s.title, messageCount: s.messageCount, updatedAt: s.updatedAt })));
    }

    applyTemplate(name) {
      const tmpl = TEMPLATES[name];
      if (!tmpl) return;
      const input = this.dom.prompt;
      input.value = input.value.trim() ? `${input.value.trim()} — ${tmpl.split(':')[0]}` : tmpl;
      this.autoresize();
      input.focus();
    }

    autoresize() {
      const ta = this.dom.prompt;
      ta.style.height = 'auto';
      ta.style.height = Math.min(ta.scrollHeight, 240) + 'px';
    }

    reset() {
      this.state.runId = null;
      this.state.sessionId = null;
      this.state.artifacts = [];
      this.state.plan = [];
      this.state.steps = 0;
      this.state.docHtml = '';
      this.state.status = 'idle';
      this.renderPlan();
      this.renderSteps();
      this.renderArtifacts();
      this.renderDoc();
      this.renderFiles();
      this.setStatus('idle', 'Idle');
      this.setPill('Lazy is idle. Tell it what to build.');
      this.dom.prompt.value = '';
      this.autoresize();
    }

    populateThreads(sessions) {
      if (!sessions.length) {
        this.dom.threads.innerHTML = '<li class="lz-empty">No threads yet. Ask Lazy anything to start.</li>';
        return;
      }
      this.dom.threads.innerHTML = sessions
        .map((s) => `<li data-session="${s.id}"><strong>${escape(s.title || 'Untitled')}</strong><span class="meta">${s.messageCount || 0} messages · ${formatTime(s.updatedAt)}</span></li>`)
        .join('');
      this.dom.threads.querySelectorAll('li[data-session]').forEach((li) => {
        li.addEventListener('click', () => this.loadSession(li.dataset.session));
      });
    }

    async loadSession(sessionId) {
      // For brevity, in this build a "click" just highlights the thread;
      // history replay is the next iteration. Show a hint instead.
      this.dom.threads.querySelectorAll('li').forEach((li) => li.classList.toggle('active', li.dataset.session === sessionId));
      this.setPill('Thread selected. History replay coming soon — start a new message in this thread to continue.');
    }

    activateTab(name) {
      this.dom.tabs.forEach((t) => t.classList.toggle('active', t.dataset.tab === name));
      this.dom.panes.forEach((p) => {
        if (p.dataset.pane === name) p.removeAttribute('hidden');
        else p.setAttribute('hidden', '');
      });
    }

    setStatus(state, text) {
      this.state.status = state;
      const dot = this.dom.status.querySelector('.lz-dot');
      dot.className = 'lz-dot lz-dot--' + state;
      this.dom.status.querySelector('.lz-status-text').textContent = text;
    }

    setPill(text) {
      this.dom.pill.textContent = text;
    }

    setBusy(busy) {
      this.dom.send.disabled = busy;
      this.dom.send.querySelector('.lz-send-text').hidden = busy;
      this.dom.send.querySelector('.lz-send-spinner').hidden = !busy;
      this.dom.cancel.hidden = !busy;
    }

    async submit() {
      const text = (this.dom.prompt.value || '').trim();
      if (!text) return;
      if (this.state.status === 'running') return;
      this.dom.prompt.value = '';
      this.autoresize();
      this.reset();
      this.setBusy(true);
      this.setStatus('running', 'Starting…');
      this.setPill('Lazy is working. It will research, plan, draft and review before delivering.');
      this.appendUserEcho(text);

      const payload = {
        goal: text,
        title: text.slice(0, 80),
        sessionId: this.state.sessionId,
        modelKey: this.dom.model.value || 'neby-pro',
      };
      try {
        const res = await fetch(config.endpoints.run, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf(),
          },
          body: JSON.stringify(payload),
          credentials: 'same-origin',
        });
        const data = await res.json();
        if (!res.ok || !data.ok) {
          this.setStatus('error', 'Failed to start');
          this.setPill(data.error || 'Failed to start a run.');
          this.setBusy(false);
          return;
        }
        this.state.runId = data.runId;
        this.state.sessionId = data.sessionId;
        this.openStream();
      } catch (err) {
        this.setStatus('error', 'Network error');
        this.setPill(`Network error: ${err.message}`);
        this.setBusy(false);
      }
    }

    appendUserEcho(text) {
      const frame = this.dom.docFrame;
      frame.insertAdjacentHTML('beforeend', `<div class="lz-msg lz-msg--user">${escape(text)}</div>`);
      frame.scrollTop = frame.scrollHeight;
    }

    openStream() {
      if (this.state.eventSource) {
        this.state.eventSource.close();
      }
      const url = config.endpoints.stream.replace('__ID__', this.state.runId);
      const es = new EventSource(url, { withCredentials: true });
      this.state.eventSource = es;
      es.onmessage = (msg) => {
        if (!msg.data || msg.data === '{}') return;
        let frame;
        try { frame = JSON.parse(msg.data); } catch (e) { return; }
        this.onFrame(frame);
      };
      es.onerror = () => {
        // EventSource will auto-reconnect; if status reached final, we close on 'done'.
      };
    }

    closeStream() {
      if (this.state.eventSource) {
        try { this.state.eventSource.close(); } catch (e) { /* noop */ }
        this.state.eventSource = null;
      }
    }

    onFrame(frame) {
      const t = frame.type;
      if (t === 'run_start') {
        this.state.startedAt = Date.now();
        this.setStatus('running', 'Running…');
        return;
      }
      if (t === 'think') {
        this.addStep({ kind: 'think', title: (frame.content || '').slice(0, 100) });
        return;
      }
      if (t === 'plan') {
        this.state.plan = Array.isArray(frame.items) ? frame.items : [];
        this.renderPlan();
        return;
      }
      if (t === 'status') {
        this.setPill((frame.label || '').trim() || this.dom.pill.textContent);
        return;
      }
      if (t === 'tool_start') {
        this.addStep({ kind: 'tool', name: frame.name, args: frame.args, label: frame.label, running: true });
        return;
      }
      if (t === 'tool_end') {
        this.completeStep(frame.name, frame.ok, frame.summary, frame.durationMs);
        return;
      }
      if (t === 'artifact') {
        this.state.artifacts.push(frame);
        this.renderArtifacts();
        this.activateTabForKind(frame.kind);
        this.renderFiles();
        return;
      }
      if (t === 'doc') {
        this.state.docHtml = frame.html || '';
        this.renderDoc();
        return;
      }
      if (t === 'message') {
        this.setPill((frame.content || '').slice(0, 240));
        return;
      }
      if (t === 'error') {
        this.setStatus('error', 'Error');
        this.setPill(frame.message || 'The agent reported an error.');
        return;
      }
      if (t === 'done') {
        const elapsed = this.state.startedAt ? Math.round((Date.now() - this.state.startedAt) / 1000) : 0;
        if (frame.ok) {
          this.setStatus('done', `Done in ${elapsed}s`);
          this.setPill(this.composeFinalPill(frame, elapsed));
        } else {
          this.setStatus('error', 'Failed');
          this.setPill(frame.error ? `Failed: ${frame.error}` : 'Run failed.');
        }
        this.setBusy(false);
        this.closeStream();
      }
    }

    addStep(step) {
      const li = document.createElement('li');
      li.dataset.kind = step.kind;
      li.dataset.name = step.name || step.title || '';
      const row = document.createElement('div');
      row.className = 'row';
      const name = document.createElement('span');
      name.className = 'name';
      name.textContent = step.kind === 'think' ? 'Reasoning' : (step.label || step.name || step.title || 'step');
      row.appendChild(name);
      const pill = document.createElement('span');
      pill.className = 'pill';
      pill.textContent = step.running ? 'running' : 'ok';
      row.appendChild(pill);
      li.appendChild(row);
      if (step.kind === 'tool' && step.args) {
        const argLine = document.createElement('div');
        argLine.className = 'summary';
        argLine.textContent = `↳ ${summariseArgs(step.args)}`;
        li.appendChild(argLine);
      }
      this.dom.steps.appendChild(li);
      this.dom.steps.parentElement.scrollTop = this.dom.steps.parentElement.scrollHeight;
      this.state.steps += 1;
      this.dom.stepsCount.textContent = this.state.steps;
    }

    completeStep(name, ok, summary, duration) {
      const li = this.dom.steps.querySelector(`li[data-name="${cssEscape(name)}"]:last-of-type`);
      if (li) {
        const pill = li.querySelector('.pill');
        pill.textContent = ok ? `ok ${duration}ms` : `err ${duration}ms`;
        pill.className = 'pill ' + (ok ? 'ok' : 'err');
        if (summary) {
          const line = document.createElement('div');
          line.className = 'summary';
          line.textContent = (summary || '').slice(0, 220);
          li.appendChild(line);
        }
      }
    }

    renderPlan() {
      if (!this.state.plan.length) {
        this.dom.plan.innerHTML = '<li class="lz-empty">Waiting for the plan…</li>';
        return;
      }
      this.dom.plan.innerHTML = this.state.plan
        .map((it) => `<li data-status="${escape(it.status || 'pending')}"><span class="id">${escape(it.id || '')}</span><span>${escape(it.text || '')}</span></li>`)
        .join('');
    }

    renderSteps() {
      this.dom.steps.innerHTML = '';
      this.dom.stepsCount.textContent = '0';
    }

    renderArtifacts() {
      if (!this.state.artifacts.length) {
        this.dom.artifacts.innerHTML = '<div class="lz-empty">No artifacts yet.</div>';
        return;
      }
      this.dom.artifacts.innerHTML = this.state.artifacts
        .map((a) => `<div class="lz-art"><div><div class="kind">${escape(a.kind || '')}</div><div class="name">${escape(a.name || '')}</div></div><div class="size">${formatSize(a.size)}</div><a href="${escape(a.url || '#')}" target="_blank" rel="noopener">Open</a></div>`)
        .join('');
    }

    renderFiles() {
      if (!this.state.artifacts.length) {
        this.dom.files.innerHTML = '<li class="lz-empty">No files yet. Artifacts Lazy produces will appear here.</li>';
        return;
      }
      this.dom.files.innerHTML = this.state.artifacts
        .map((a) => `<li><span>${escape(a.name || '')}</span><span><a href="${escape(a.url || '#')}" target="_blank" rel="noopener">${escape(a.kind || '')} · ${formatSize(a.size)}</a></span></li>`)
        .join('');
    }

    renderDoc() {
      if (!this.state.docHtml) return;
      this.dom.docFrame.innerHTML = this.state.docHtml;
    }

    activateTabForKind(kind) {
      const map = { doc: 'document', pdf: 'document', slides: 'slides', sheet: 'sheets', code: 'code', archive: 'files' };
      const tab = map[kind] || 'files';
      this.activateTab(tab);
    }

    composeFinalPill(frame, elapsed) {
      const count = (frame.artifacts || []).length || this.state.artifacts.length;
      if (count) return `Done in ${elapsed}s · ${count} artifact${count === 1 ? '' : 's'} ready below.`;
      return `Done in ${elapsed}s.`;
    }

    async cancel() {
      if (!this.state.runId) return;
      try {
        await fetch(config.endpoints.cancel.replace('__ID__', this.state.runId), {
          method: 'POST',
          headers: { 'X-CSRFToken': csrf() },
          credentials: 'same-origin',
        });
      } catch (e) { /* noop */ }
      this.closeStream();
      this.setStatus('idle', 'Cancelled');
      this.setPill('Run cancelled. Send a new message when ready.');
      this.setBusy(false);
    }
  }

  function escape(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function cssEscape(s) {
    return String(s || '').replace(/[^a-zA-Z0-9_-]/g, '\\$&');
  }

  function formatTime(ms) {
    if (!ms) return '—';
    try {
      const d = new Date(Number(ms));
      const today = new Date();
      if (d.toDateString() === today.toDateString()) {
        return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      }
      return d.toLocaleDateString([], { month: 'short', day: 'numeric' });
    } catch (e) {
      return '—';
    }
  }

  function formatSize(bytes) {
    if (!bytes) return '—';
    const units = ['B', 'KB', 'MB', 'GB'];
    let value = Number(bytes);
    let unit = 0;
    while (value >= 1024 && unit < units.length - 1) { value /= 1024; unit += 1; }
    return `${value < 10 ? value.toFixed(1) : Math.round(value)} ${units[unit]}`;
  }

  function summariseArgs(args) {
    if (!args || typeof args !== 'object') return '';
    return Object.entries(args)
      .slice(0, 3)
      .map(([k, v]) => `${k}=${typeof v === 'string' ? (v.length > 40 ? v.slice(0, 40) + '…' : v) : JSON.stringify(v).slice(0, 40)}`)
      .join(', ');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new LazyWorkspace());
  } else {
    new LazyWorkspace();
  }
})();
