const TAB_LABELS = { html: 'HTML', css: 'CSS', js: 'JS' };

export function createPlayground(stage, config) {
  stage.classList.add('ix-coding', 'ix-coding-playground');
  const tabs = config.tabs || ['html', 'css', 'js'];
  const mode = config.mode || 'web';
  const starter = config.starter || {};
  const goals = (config.goals || []).map((g) => ({ ...g, met: false }));
  let frameReady = false;
  let pendingRun = null;
  let lastConsole = [];
  let allMetFired = false;
  let disposed = false;
  let runId = 0;
  let watchdog = null;
  let suppressAutoRun = false;

  const root = document.createElement('div');
  root.className = 'ix-coding-root ix-pg';
  root.innerHTML =
    '<div class="ix-pg-main">' +
    '<div class="ix-pg-editors">' +
    '<div class="ix-pg-tabs" role="tablist"></div>' +
    '<div class="ix-pg-editor-host"></div>' +
    '<div class="ix-pg-actions">' +
    '<button type="button" class="ix-run-btn ix-btn-run ix-pg-run"><span class="material-symbols-outlined">play_arrow</span>Run</button>' +
    '<button type="button" class="ix-run-btn ix-btn-reset ix-pg-reset"><span class="material-symbols-outlined">restart_alt</span>Start over</button>' +
    '</div>' +
    '</div>' +
    '<div class="ix-pg-output">' +
    '<div class="ix-pg-out-tabs"></div>' +
    '<div class="ix-pg-out-body"></div>' +
    '</div>' +
    '</div>' +
    '<div class="ix-pg-goals"><div class="ix-pg-goals-title"><span class="material-symbols-outlined">checklist</span>Your goals</div><ul class="ix-pg-goals-list"></ul></div>';
  stage.appendChild(root);

  const tabsEl = root.querySelector('.ix-pg-tabs');
  const editorHost = root.querySelector('.ix-pg-editor-host');
  const outTabsEl = root.querySelector('.ix-pg-out-tabs');
  const outBody = root.querySelector('.ix-pg-out-body');
  const goalsList = root.querySelector('.ix-pg-goals-list');

  const editors = {};
  tabs.forEach((key, i) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'ix-pg-tab' + (i === 0 ? ' ix-pg-tab-active' : '');
    btn.textContent = TAB_LABELS[key] || key;
    btn.dataset.key = key;
    btn.addEventListener('click', () => selectTab(key));
    tabsEl.appendChild(btn);

    const ta = document.createElement('textarea');
    ta.className = 'ix-pg-editor';
    ta.spellcheck = false;
    ta.autocapitalize = 'off';
    ta.autocomplete = 'off';
    ta.value = starter[key] || '';
    ta.hidden = i !== 0;
    ta.setAttribute('aria-label', (TAB_LABELS[key] || key) + ' editor');
    ta.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        e.preventDefault();
        const s = ta.selectionStart;
        ta.value = ta.value.slice(0, s) + '  ' + ta.value.slice(ta.selectionEnd);
        ta.selectionStart = ta.selectionEnd = s + 2;
      }
    });
    editorHost.appendChild(ta);
    editors[key] = ta;
  });

  function selectTab(key) {
    tabsEl.querySelectorAll('.ix-pg-tab').forEach((b) => b.classList.toggle('ix-pg-tab-active', b.dataset.key === key));
    tabs.forEach((k) => { editors[k].hidden = k !== key; });
  }

  let frame = null;
  let consoleEl = null;
  const showPreview = mode === 'web';
  const showConsole = mode === 'js' || config.showConsole;

  if (showPreview) {
    frame = document.createElement('iframe');
    frame.className = 'ix-pg-frame';
    frame.src = '/interactive/sandbox/frame/';
    frame.setAttribute('sandbox', 'allow-scripts');
    frame.setAttribute('title', 'Live preview');
    outBody.appendChild(frame);
  } else {
    frame = document.createElement('iframe');
    frame.className = 'ix-pg-frame ix-pg-frame-hidden';
    frame.src = '/interactive/sandbox/frame/';
    frame.setAttribute('sandbox', 'allow-scripts');
    frame.setAttribute('title', 'Code runner');
    outBody.appendChild(frame);
  }
  if (showConsole) {
    consoleEl = document.createElement('div');
    consoleEl.className = 'ix-pg-console';
    consoleEl.innerHTML = '<div class="ix-pg-console-empty">Console output appears here — press Run!</div>';
    outBody.appendChild(consoleEl);
  }

  if (showPreview && showConsole) {
    const pvBtn = document.createElement('button');
    pvBtn.type = 'button';
    pvBtn.className = 'ix-pg-tab ix-pg-tab-active';
    pvBtn.textContent = 'Preview';
    const cnBtn = document.createElement('button');
    cnBtn.type = 'button';
    cnBtn.className = 'ix-pg-tab';
    cnBtn.textContent = 'Console';
    outTabsEl.appendChild(pvBtn);
    outTabsEl.appendChild(cnBtn);
    consoleEl.classList.add('ix-pg-out-hidden');
    pvBtn.addEventListener('click', () => {
      pvBtn.classList.add('ix-pg-tab-active'); cnBtn.classList.remove('ix-pg-tab-active');
      frame.classList.remove('ix-pg-out-hidden'); consoleEl.classList.add('ix-pg-out-hidden');
    });
    cnBtn.addEventListener('click', () => {
      cnBtn.classList.add('ix-pg-tab-active'); pvBtn.classList.remove('ix-pg-tab-active');
      consoleEl.classList.remove('ix-pg-out-hidden'); frame.classList.add('ix-pg-out-hidden');
    });
  } else {
    outTabsEl.innerHTML = '<span class="ix-pg-out-label">' + (showPreview ? 'Live preview' : 'Console') + '</span>';
  }

  function renderGoals() {
    goalsList.innerHTML = '';
    goals.forEach((g) => {
      const li = document.createElement('li');
      li.className = 'ix-pg-goal' + (g.met ? ' ix-pg-goal-met' : '');
      const icon = document.createElement('span');
      icon.className = 'material-symbols-outlined';
      icon.textContent = g.met ? 'check_circle' : 'radio_button_unchecked';
      const label = document.createElement('span');
      label.textContent = g.label;
      li.appendChild(icon);
      li.appendChild(label);
      goalsList.appendChild(li);
    });
  }
  renderGoals();

  function appendConsole(level, text) {
    if (!consoleEl) return;
    const empty = consoleEl.querySelector('.ix-pg-console-empty');
    if (empty) empty.remove();
    const line = document.createElement('div');
    line.className = 'ix-pg-con-line ix-pg-con-' + level;
    line.textContent = text;
    consoleEl.appendChild(line);
    consoleEl.scrollTop = consoleEl.scrollHeight;
  }

  function getSource() {
    return {
      html: editors.html ? editors.html.value : '',
      css: editors.css ? editors.css.value : '',
      js: editors.js ? editors.js.value : '',
    };
  }

  function evaluateGoals(src) {
    let doc = null;
    try { doc = new DOMParser().parseFromString(src.html || '', 'text/html'); } catch (e) {}
    const ctx = { ...src, doc, console: lastConsole.slice(), output: lastConsole.map((l) => l.text) };
    let newlyMet = false;
    goals.forEach((g) => {
      if (g.met) return;
      let ok = false;
      try { ok = !!g.test(ctx); } catch (e) { ok = false; }
      if (ok) { g.met = true; newlyMet = true; }
    });
    renderGoals();
    if (newlyMet && config.onGoalMet) config.onGoalMet(goals.filter((g) => g.met).length, goals.length);
    if (!allMetFired && goals.length && goals.every((g) => g.met)) {
      allMetFired = true;
      if (config.onAllGoals) config.onAllGoals();
    }
    if (config.onRun) config.onRun(ctx);
  }

  function post(msg) {
    if (!frame.contentWindow) return;
    frame.contentWindow.postMessage({ source: 'nebians-host', ...msg }, '*');
  }

  let runSrc = null;

  function clearWatchdog() {
    if (watchdog) { clearTimeout(watchdog); watchdog = null; }
  }

  function showTimeoutError() {
    const msg = 'Your code ran too long — check for infinite loops!';
    if (consoleEl) { appendConsole('error', msg); return; }
    let warn = outBody.querySelector('.ix-pg-timeout');
    if (!warn) {
      warn = document.createElement('div');
      warn.className = 'ix-pg-con-line ix-pg-con-error ix-pg-timeout';
      outBody.appendChild(warn);
    }
    warn.textContent = msg;
  }

  function armWatchdog() {
    clearWatchdog();
    watchdog = setTimeout(() => {
      watchdog = null;
      if (disposed) return;
      runId += 1;
      frameReady = false;
      pendingRun = false;
      suppressAutoRun = true;
      showTimeoutError();
      frame.src = frame.src;
    }, 3500);
  }

  function run() {
    const src = getSource();
    runSrc = src;
    runId += 1;
    lastConsole = [];
    if (consoleEl) consoleEl.innerHTML = '';
    const warn = outBody.querySelector('.ix-pg-timeout');
    if (warn) warn.remove();
    armWatchdog();
    if (mode === 'web') {
      post({ type: 'run-web', runId, payload: { html: src.html, css: src.css, js: src.js } });
    } else {
      const code = config.harness ? config.harness(src.js) : src.js;
      post({ type: 'run-js', runId, payload: { code } });
    }
  }

  function requestRun() {
    if (!frameReady) { pendingRun = true; return; }
    run();
  }

  function onMessage(e) {
    const data = e.data || {};
    if (data.source !== 'nebians-sandbox') return;
    if (e.source !== frame.contentWindow) return;
    if (data.type === 'ready') {
      frameReady = true;
      const shouldRun = pendingRun || (!suppressAutoRun && config.autoRun !== false);
      suppressAutoRun = false;
      if (shouldRun) { pendingRun = false; run(); }
    } else if (data.type === 'console') {
      if (data.runId !== runId) return;
      lastConsole.push(data.payload);
      if (!config.consoleFilter || config.consoleFilter(data.payload)) appendConsole(data.payload.level, data.payload.text);
    } else if (data.type === 'done') {
      if (data.runId !== runId) return;
      clearWatchdog();
      if (runSrc) evaluateGoals(runSrc);
    }
  }
  window.addEventListener('message', onMessage);

  root.querySelector('.ix-pg-run').addEventListener('click', requestRun);
  root.querySelector('.ix-pg-reset').addEventListener('click', () => {
    tabs.forEach((k) => { editors[k].value = starter[k] || ''; });
    goals.forEach((g) => { g.met = false; });
    allMetFired = false;
    renderGoals();
    if (config.onReset) config.onReset();
    requestRun();
  });

  return {
    el: root,
    run: requestRun,
    getSource,
    goalsMet: () => goals.filter((g) => g.met).length,
    dispose() {
      if (disposed) return;
      disposed = true;
      clearWatchdog();
      window.removeEventListener('message', onMessage);
      root.remove();
      stage.classList.remove('ix-coding', 'ix-coding-playground');
    },
  };
}
