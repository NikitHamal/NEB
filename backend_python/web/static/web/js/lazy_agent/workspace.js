/* Lazy workspace — controller.
 *
 * Owns all mutable state: which thread is open, whether a run is live, what
 * has been rendered into the conversation. Everything visual goes through
 * LazyDom; everything networked goes through LazyApi.
 */

(() => {
  'use strict';

  const api = window.LazyApi;
  const dom = window.LazyDom;
  const { RunStream } = window.LazyStream;
  const fmt = api.fmt;

  const SUGGESTIONS = [
    {
      title: 'Write an assignment',
      text: 'NEB-standard structure with research, tables and references — delivered as .docx and .pdf.',
      prompt: 'Write a complete NEB assignment on the topic: [TOPIC]. Include introduction, main body with headings, a comparison table, conclusion and references.',
    },
    {
      title: 'Lab report',
      text: 'Objective, theory, apparatus, procedure, observation table, calculation, result, precautions.',
      prompt: 'Write a NEB Grade 12 lab report on the experiment: [TOPIC]. Include objective, theory, apparatus, procedure, observation table, calculation, result, discussion, conclusion and precautions.',
    },
    {
      title: 'Build a presentation',
      text: 'A real .pptx with slide order, speaker notes and a clean theme.',
      prompt: 'Build a 12-slide presentation on [TOPIC] for a NEB class. Include title, agenda, key concepts, worked example, common mistakes, summary and speaker notes.',
    },
    {
      title: 'Analyse my data',
      text: 'Attach a CSV or Excel file and get statistics, charts and a written interpretation.',
      prompt: 'Analyse the attached data file. Report the shape, key statistics, any correlations, and what the numbers actually mean.',
    },
  ];

  class Workspace {
    constructor() {
      this.cfg = window.LAZY_AGENT_CONFIG || {};
      this.state = {
        sessionId: null,
        runId: null,
        status: 'idle',
        artifacts: [],
        files: [],
        plan: [],
        activity: 0,
        startedAt: 0,
        sources: [],
        pendingTools: {},
        stream: null,
      };

      this.dom = {
        root: document.getElementById('lzRoot'),
        rail: document.getElementById('lzRail'),
        railToggle: document.getElementById('lzRailToggle'),
        newBtn: document.getElementById('lzNew'),
        newThread: document.getElementById('lzNewThread'),
        threads: document.getElementById('lzThreads'),
        threadName: document.getElementById('lzThreadName'),
        credits: document.getElementById('lzCredits'),
        status: document.getElementById('lzStatus'),
        model: document.getElementById('lzModel'),
        stream: document.getElementById('lzStream'),
        prompt: document.getElementById('lzPrompt'),
        send: document.getElementById('lzSend'),
        cancel: document.getElementById('lzCancel'),
        attach: document.getElementById('lzAttach'),
        fileInput: document.getElementById('lzFileInput'),
        attachments: document.getElementById('lzAttachments'),
        chips: document.getElementById('lzChips'),
        pill: document.getElementById('lzPill'),
        plan: document.getElementById('lzPlan'),
        planMeta: document.getElementById('lzPlanMeta'),
        activity: document.getElementById('lzActivity'),
        activityMeta: document.getElementById('lzActivityMeta'),
        files: document.getElementById('lzFiles'),
        filesMeta: document.getElementById('lzFilesMeta'),
        viewer: document.getElementById('lzViewer'),
        viewerTitle: document.getElementById('lzViewerTitle'),
        viewerBody: document.getElementById('lzViewerBody'),
        viewerOpen: document.getElementById('lzViewerOpen'),
        viewerDownload: document.getElementById('lzViewerDownload'),
        viewerClose: document.getElementById('lzViewerClose'),
      };

      this.bind();
      this.renderThreads(this.cfg.sessions || []);
      this.renderCredits(this.cfg.credits || {});
      this.showWelcome();
      this.autoResize();
    }

    // ------------------------------------------------------------------
    // Wiring
    // ------------------------------------------------------------------

    bind() {
      const d = this.dom;

      d.prompt.addEventListener('input', () => this.autoResize());
      d.prompt.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.submit();
        }
      });
      d.send.addEventListener('click', () => this.submit());
      d.cancel.addEventListener('click', () => this.cancel());
      d.newBtn.addEventListener('click', () => this.newThread());
      d.newThread.addEventListener('click', () => this.newThread());
      d.railToggle.addEventListener('click', () => d.rail.classList.toggle('lz-rail--open'));

      d.attach.addEventListener('click', () => d.fileInput.click());
      d.fileInput.addEventListener('change', () => this.handleFiles(d.fileInput.files));

      d.chips.addEventListener('click', (e) => {
        const chip = e.target.closest('.lz-chip');
        if (chip) this.applyTemplate(chip.dataset.template);
      });
      d.stream.addEventListener('click', (e) => {
        const suggest = e.target.closest('.lz-suggest');
        if (suggest) {
          d.prompt.value = suggest.dataset.prompt;
          this.autoResize();
          d.prompt.focus();
        }
      });

      d.viewerClose.addEventListener('click', () => this.closeViewer());
      d.viewer.addEventListener('click', (e) => {
        if (e.target === d.viewer) this.closeViewer();
      });
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') this.closeViewer();
      });

      window.addEventListener('beforeunload', () => {
        if (this.state.stream) this.state.stream.close();
      });
    }

    // ------------------------------------------------------------------
    // Composer
    // ------------------------------------------------------------------

    autoResize() {
      const ta = this.dom.prompt;
      ta.style.height = 'auto';
      ta.style.height = `${Math.min(ta.scrollHeight, 220)}px`;
    }

    applyTemplate(name) {
      const map = {
        assignment: SUGGESTIONS[0].prompt,
        lab: SUGGESTIONS[1].prompt,
        slides: SUGGESTIONS[2].prompt,
        sheet: 'Build a spreadsheet: [TOPIC]. Include styled headers, sample data, formulas for totals and averages, and a chart.',
        code: 'Build a small project: [TOPIC]. Create the files, write the code, run it to verify it works, and package it as a .zip.',
        research: 'Research [TOPIC] thoroughly from credible sources and write a structured brief with key findings, evidence and citations.',
      };
      const text = map[name];
      if (!text) return;
      this.dom.prompt.value = text;
      this.autoResize();
      this.dom.prompt.focus();
    }

    async handleFiles(fileList) {
      const files = Array.from(fileList || []);
      for (const file of files) {
        try {
          this.setPill(`Uploading ${file.name}…`);
          const res = await api.upload(file);
          const srcId = res.srcId || res.src_id;
          if (!srcId) throw new Error('upload returned no reference');
          this.state.sources.push({ name: file.name, size: file.size, srcId });
        } catch (err) {
          this.setPill(`Could not attach ${file.name}: ${err.message}`);
        }
      }
      this.renderAttachments();
      this.dom.fileInput.value = '';
      if (this.state.sources.length) {
        this.setPill(`${this.state.sources.length} file(s) attached. Say what to do with them.`);
      }
    }

    renderAttachments() {
      const box = this.dom.attachments;
      box.innerHTML = '';
      if (!this.state.sources.length) {
        box.hidden = true;
        return;
      }
      box.hidden = false;
      this.state.sources.forEach((src) => {
        const chip = dom.el('span', 'lz-att');
        chip.appendChild(dom.el('span', 'lz-att-name', src.name));
        const remove = dom.el('button', 'lz-att-x', '✕');
        remove.type = 'button';
        remove.addEventListener('click', () => {
          this.state.sources = this.state.sources.filter((s) => s !== src);
          this.renderAttachments();
        });
        chip.appendChild(remove);
        box.appendChild(chip);
      });
    }

    // ------------------------------------------------------------------
    // Threads
    // ------------------------------------------------------------------

    renderThreads(sessions) {
      const list = this.dom.threads;
      list.innerHTML = '';
      if (!sessions.length) {
        list.appendChild(dom.el('li', 'lz-thread-empty', 'No threads yet.'));
        return;
      }
      sessions.forEach((s) => {
        const li = dom.threadItem(s, s.id === this.state.sessionId);
        li.addEventListener('click', () => this.loadSession(s.id));
        list.appendChild(li);
      });
    }

    async loadSession(sessionId) {
      if (sessionId === this.state.sessionId && this.dom.stream.children.length > 1) {
        this.dom.rail.classList.remove('lz-rail--open');
        return;
      }
      try {
        const data = await api.sessionHistory(sessionId);
        this.state.sessionId = sessionId;
        this.dom.threadName.textContent = data.session.title || 'Thread';
        this.clearConversation();
        this.renderReplay(data);
        this.renderThreads(this.cfg.sessions.map((s) => (s.id === sessionId ? { ...s, title: data.session.title } : s)));
        this.dom.rail.classList.remove('lz-rail--open');
      } catch (err) {
        this.setPill(`Could not open that thread: ${err.message}`);
      }
    }

    /** Rebuild a past thread from persisted messages, runs and artifacts. */
    renderReplay(data) {
      const messages = data.messages || [];
      let lastRole = null;
      messages.forEach((msg) => {
        if (msg.role === 'user') {
          const atts = (msg.meta && msg.meta.attachments) || [];
          this.append(dom.userMessage(msg.content, atts, msg.createdAt));
        } else if (msg.role === 'assistant') {
          this.append(dom.agentMessage(msg.content, msg.createdAt));
        }
        lastRole = msg.role;
      });

      (data.runs || []).forEach((run) => {
        if (run.plan && (run.plan.items || []).length) {
          this.state.plan = run.plan.items;
        }
        this.append(
          dom.activityRow({
            icon: run.status === 'done' ? '✓' : run.status === 'cancelled' ? '■' : '!',
            label: run.goal || run.title || 'Run',
            detail: `${run.status} · ${run.toolCalls || 0} tool calls · ${fmt.formatDay(run.createdAt)}`,
            tone: run.status === 'done' ? 'ok' : run.status === 'failed' ? 'err' : '',
          }),
        );
      });
      this.renderPlan();

      (data.artifacts || []).forEach((art) => {
        this.addArtifact(art, false);
      });
      if (lastRole === 'user' && !(data.artifacts || []).length) {
        this.append(
          dom.narration('This thread has no completed reply yet — send a message to continue it.'),
        );
      }
      this.scrollToEnd();
    }

    newThread() {
      if (this.state.stream) this.state.stream.close();
      this.state.sessionId = null;
      this.state.runId = null;
      this.state.sources = [];
      this.state.artifacts = [];
      this.state.files = [];
      this.state.plan = [];
      this.state.activity = 0;
      this.state.status = 'idle';
      this.dom.threadName.textContent = 'New thread';
      this.dom.prompt.value = '';
      this.renderAttachments();
      this.clearConversation();
      this.showWelcome();
      this.setStatus('idle', 'Idle');
      this.setPill('Lazy never asks what to do next — it works until the file is real.');
      this.renderThreads(this.cfg.sessions || []);
      this.autoResize();
      this.dom.prompt.focus();
    }

    // ------------------------------------------------------------------
    // Running
    // ------------------------------------------------------------------

    async submit() {
      const text = (this.dom.prompt.value || '').trim();
      if (!text || this.state.status === 'running') return;

      this.dom.prompt.value = '';
      this.autoResize();
      this.setBusy(true);
      this.setStatus('running', 'Working…');
      this.setPill('Lazy is working. It will research, plan, build and check before delivering.');

      const sources = this.state.sources.slice();
      const attachments = sources.map((s) => ({ name: s.name, size: s.size }));
      this.append(dom.userMessage(text, attachments, Date.now()));

      this.state.sources = [];
      this.renderAttachments();

      try {
        const data = await api.startRun({
          goal: text,
          sessionId: this.state.sessionId,
          modelKey: this.dom.model.value,
          sources,
        });
        this.state.runId = data.runId;
        this.state.sessionId = data.sessionId;
        this.upsertThread({ id: data.sessionId, title: text.slice(0, 60), updatedAt: Date.now() });
        this.dom.threadName.textContent = text.slice(0, 48);
        this.openStream();
      } catch (err) {
        this.setStatus('error', 'Failed to start');
        this.setPill(err.message || 'Could not start the agent.');
        this.setBusy(false);
      }
    }

    openStream() {
      if (this.state.stream) this.state.stream.close();
      const stream = new RunStream(this.state.runId, (frame) => this.onFrame(frame), {
        onError: (err) => {
          this.setStatus('error', 'Connection lost');
          this.setPill(err.message);
          this.setBusy(false);
        },
      });
      this.state.stream = stream;
      stream.open();
    }

    async cancel() {
      if (!this.state.runId) return;
      this.setPill('Stopping…');
      try {
        await api.cancelRun(this.state.runId);
      } catch (err) { /* the stream will report the final state */ }
      if (this.state.stream) this.state.stream.close();
      this.setBusy(false);
      this.setStatus('idle', 'Stopped');
      this.setPill('Stopped. Everything produced so far is still available below.');
    }

    onFrame(frame) {
      switch (frame.type) {
        case 'run_start':
          this.state.startedAt = Date.now();
          this.setStatus('running', 'Working…');
          break;

        case 'think':
          this.addActivity('🧠', (frame.content || '').slice(0, 160), '');
          break;

        case 'plan':
          this.state.plan = Array.isArray(frame.items) ? frame.items : [];
          this.renderPlan();
          if (frame.summary) this.setPill(frame.summary);
          break;

        case 'status':
          this.setPill(frame.label || this.dom.pill.textContent);
          break;

        case 'tool_start':
          this.startTool(frame);
          break;

        case 'tool_end':
          this.endTool(frame);
          break;

        case 'artifact':
          this.addArtifact(frame, true);
          break;

        case 'doc':
          this.renderDocument(frame);
          break;

        case 'message':
          this.append(dom.agentMessage(frame.content || '', Date.now()));
          this.scrollToEnd();
          break;

        case 'error':
          this.addActivity('⚠️', frame.message || 'Something went wrong', '', 'err');
          this.setPill(frame.message || 'Something went wrong.');
          break;

        case 'done':
          this.finish(frame);
          break;

        default:
          break;
      }
    }

    startTool(frame) {
      const card = dom.toolCard(frame);
      this.append(card);
      this.state.pendingTools[frame.name] = card;
      this.addActivity(dom.artifactEmoji('file'), frame.label || fmt.toolLabel(frame.name, frame.args), '');
      this.scrollToEnd();
    }

    endTool(frame) {
      const key = frame.name;
      const card = this.state.pendingTools[key];
      dom.settleToolCard(card, frame.ok, frame.summary, frame.durationMs);
      delete this.state.pendingTools[key];
      if (!frame.ok) {
        this.addActivity('⚠️', `${frame.name} failed`, (frame.summary || '').slice(0, 160), 'err');
      }
      this.scrollToEnd();
    }

    addArtifact(artifact, live) {
      const existing = this.state.artifacts.find(
        (a) => a.name === artifact.name && a.url === artifact.url,
      );
      if (existing) return;
      this.state.artifacts.push(artifact);

      const card = dom.artifactCard(artifact, (a) => this.openViewer(a));
      this.append(card);

      const entry = { name: artifact.name, size: artifact.size, url: artifact.url, path: artifact.path };
      if (!this.state.files.some((f) => f.name === entry.name)) {
        this.state.files.push(entry);
      }
      this.renderFiles();
      if (live) this.scrollToEnd();
    }

    /** Inline document preview, rendered exactly as the exported file looks. */
    renderDocument(frame) {
      const html = frame.html || '';
      if (!html) return;
      let holder = this.dom.stream.querySelector('.lz-doc-preview');
      if (!holder) {
        holder = dom.el('div', 'lz-doc-preview');
        const head = dom.el('div', 'lz-doc-preview-head');
        head.appendChild(dom.el('span', null, frame.title || 'Document'));
        const expand = dom.el('button', 'lz-btn lz-btn--sm', 'Open full size');
        expand.type = 'button';
        expand.addEventListener('click', () => this.openHtmlDocument(frame.title || 'Document', html));
        head.appendChild(expand);
        holder.appendChild(head);
        const frameEl = dom.el('iframe', 'lz-doc-frame');
        frameEl.setAttribute('sandbox', 'allow-same-origin');
        frameEl.setAttribute('title', frame.title || 'Document preview');
        holder.appendChild(frameEl);
        this.append(holder);
      }
      const iframe = holder.querySelector('iframe');
      iframe.srcdoc = html;
      this.scrollToEnd();
    }

    finish(frame) {
      const elapsed = this.state.startedAt ? Date.now() - this.state.startedAt : 0;
      this.setBusy(false);
      if (this.state.stream) this.state.stream.close();

      if (frame.ok) {
        this.setStatus('done', `Done in ${fmt.formatDuration(elapsed)}`);
        if (frame.summary) this.append(dom.agentMessage(frame.summary, Date.now()));
        const count = this.state.artifacts.length;
        this.setPill(
          count
            ? `Done in ${fmt.formatDuration(elapsed)} · ${count} file${count === 1 ? '' : 's'} ready.`
            : `Done in ${fmt.formatDuration(elapsed)}.`,
        );
      } else {
        this.setStatus('error', 'Failed');
        this.append(dom.agentMessage(frame.error || 'The run could not be completed.', Date.now()));
        this.setPill(frame.error || 'The run could not be completed.');
      }
      this.refreshRunFiles();
      this.upsertThread({ id: this.state.sessionId, title: this.dom.threadName.textContent, updatedAt: Date.now() });
      this.scrollToEnd();
    }

    async refreshRunFiles() {
      if (!this.state.runId) return;
      try {
        const data = await api.runFiles(this.state.runId);
        const files = data.files || [];
        files.forEach((f) => {
          if (!this.state.files.some((x) => x.path === f.path)) this.state.files.push(f);
        });
        this.renderFiles();
      } catch (err) { /* non-critical */ }
    }

    // ------------------------------------------------------------------
    // Viewer
    // ------------------------------------------------------------------

    openHtmlDocument(title, html) {
      this.dom.viewerTitle.textContent = title;
      this.dom.viewerBody.innerHTML = `<iframe class="lz-viewer-frame" sandbox="allow-same-origin" title="${dom.escapeHtml(title)}"></iframe>`;
      this.dom.viewerBody.querySelector('iframe').srcdoc = html;
      this.dom.viewerOpen.hidden = true;
      this.dom.viewerDownload.hidden = true;
      this.dom.viewer.hidden = false;
    }

    openViewer(artifact) {
      const kind = artifact.kind || fmt.kindOf(artifact.name, artifact.mime);
      this.dom.viewerTitle.textContent = artifact.name || 'Preview';
      this.dom.viewerBody.innerHTML = '';
      this.dom.viewerOpen.hidden = false;
      this.dom.viewerDownload.hidden = false;
      this.dom.viewerOpen.href = artifact.url || '#';
      this.dom.viewerDownload.href = artifact.url || '#';
      this.dom.viewerDownload.setAttribute('download', artifact.name || '');

      if (kind === 'image') {
        const img = dom.el('img', 'lz-viewer-image');
        img.src = artifact.url;
        img.alt = artifact.name || '';
        this.dom.viewerBody.appendChild(img);
      } else if (kind === 'pdf') {
        const frame = dom.el('iframe', 'lz-viewer-frame');
        frame.src = artifact.url;
        this.dom.viewerBody.appendChild(frame);
      } else if (kind === 'code' || kind === 'html') {
        this.renderTextPreview(artifact, kind);
      } else {
        const box = dom.el('div', 'lz-viewer-binary');
        box.appendChild(dom.el('div', 'lz-viewer-huge', dom.artifactEmoji(kind)));
        box.appendChild(
          dom.emptyState(
            `${artifact.name || 'This file'} is ready`,
            'Word, PowerPoint, Excel and archive files open in their own app — download to view them.',
          ),
        );
        this.dom.viewerBody.appendChild(box);
      }
      this.dom.viewer.hidden = false;
    }

    async renderTextPreview(artifact, kind) {
      try {
        const res = await fetch(artifact.url, { credentials: 'same-origin' });
        const text = await res.text();
        if (kind === 'html') {
          const frame = dom.el('iframe', 'lz-viewer-frame');
          frame.setAttribute('sandbox', 'allow-same-origin');
          this.dom.viewerBody.appendChild(frame);
          frame.srcdoc = text;
          return;
        }
        const pre = dom.el('pre', 'lz-viewer-code');
        pre.textContent = text.slice(0, 200000);
        this.dom.viewerBody.appendChild(pre);
      } catch (err) {
        this.dom.viewerBody.appendChild(dom.emptyState('Preview unavailable', err.message));
      }
    }

    closeViewer() {
      this.dom.viewer.hidden = true;
      this.dom.viewerBody.innerHTML = '';
    }

    // ------------------------------------------------------------------
    // Panels and small renders
    // ------------------------------------------------------------------

    renderPlan() {
      const list = this.dom.plan;
      list.innerHTML = '';
      if (!this.state.plan.length) {
        list.appendChild(dom.el('li', 'lz-empty', 'Lazy will publish a plan when it starts.'));
        this.dom.planMeta.textContent = '';
        return;
      }
      this.state.plan.forEach((item) => list.appendChild(dom.planItem(item)));
      const done = this.state.plan.filter((i) => i.status === 'done').length;
      this.dom.planMeta.textContent = `${done}/${this.state.plan.length}`;
    }

    addActivity(icon, label, detail, tone) {
      const list = this.dom.activity;
      if (!list.querySelector('.lz-empty') && list.children.length === 0) {
        list.innerHTML = '';
      }
      const empty = list.querySelector('.lz-empty');
      if (empty) empty.remove();
      list.appendChild(dom.activityRow({ icon, label, detail, tone }));
      this.state.activity += 1;
      this.dom.activityMeta.textContent = String(this.state.activity);
      list.scrollTop = list.scrollHeight;
    }

    renderFiles() {
      const list = this.dom.files;
      list.innerHTML = '';
      this.dom.filesMeta.textContent = String(this.state.files.length);
      if (!this.state.files.length) {
        list.appendChild(dom.el('li', 'lz-empty', 'Files appear here as Lazy creates them.'));
        return;
      }
      this.state.files.forEach((file) => {
        list.appendChild(
          dom.fileRow(file, (f) => this.openViewer({
            name: f.name, url: f.url, size: f.size, mime: '', kind: fmt.kindOf(f.name, ''),
          })),
        );
      });
    }

    renderCredits(credits) {
      if (!this.dom.credits) return;
      if (credits.unlimited) {
        this.dom.credits.textContent = 'Unlimited credits';
        return;
      }
      this.dom.credits.textContent = `${credits.remaining || 0} / ${credits.allowance || 0} credits left`;
    }

    upsertThread(session) {
      if (!session || !session.id) return;
      const list = this.cfg.sessions || (this.cfg.sessions = []);
      const index = list.findIndex((s) => s.id === session.id);
      if (index >= 0) {
        list[index] = { ...list[index], ...session };
        list.unshift(list.splice(index, 1)[0]);
      } else {
        list.unshift(session);
      }
      this.renderThreads(list);
    }

    showWelcome() {
      const wrap = dom.el('div', 'lz-welcome');
      wrap.appendChild(dom.el('h1', null, 'What should Lazy build for you?'));
      wrap.appendChild(
        dom.el('p', null, 'Lazy researches, plans, writes, runs code and ships finished files — assignments, reports, decks, spreadsheets, data analyses and whole projects.'),
      );
      const grid = dom.el('div', 'lz-suggest-grid');
      SUGGESTIONS.forEach((s) => grid.appendChild(dom.suggestionCard(s.title, s.text, s.prompt)));
      wrap.appendChild(grid);
      this.append(wrap);
    }

    clearConversation() {
      this.state.pendingTools = {};
      this.state.activity = 0;
      this.dom.activityMeta.textContent = '0';
      this.dom.activity.innerHTML = '';
      this.dom.stream.innerHTML = '';
      this.state.artifacts = [];
      this.state.files = [];
      this.renderPlan();
      this.renderFiles();
    }

    append(node) {
      const welcome = this.dom.stream.querySelector('.lz-welcome');
      if (welcome) welcome.remove();
      this.dom.stream.appendChild(node);
    }

    scrollToEnd() {
      const el = this.dom.stream;
      el.scrollTop = el.scrollHeight;
    }

    setStatus(state, text) {
      this.state.status = state;
      const dot = this.dom.status.querySelector('.lz-dot');
      if (dot) dot.className = `lz-dot lz-dot--${state}`;
      const label = this.dom.status.querySelector('.lz-status-text');
      if (label) label.textContent = text;
    }

    setPill(text) {
      this.dom.pill.textContent = text;
    }

    setBusy(busy) {
      this.dom.send.disabled = busy;
      const text = this.dom.send.querySelector('.lz-send-text');
      const spinner = this.dom.send.querySelector('.lz-spinner');
      if (text) text.hidden = busy;
      if (spinner) spinner.hidden = !busy;
      this.dom.cancel.hidden = !busy;
      this.dom.prompt.disabled = busy;
    }
  }

  const boot = () => {
    if (!window.LazyApi || !window.LazyDom || !window.LazyStream) {
      console.error('Lazy workspace failed to load its modules.');
      return;
    }
    window.LazyWorkspace = new Workspace();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
