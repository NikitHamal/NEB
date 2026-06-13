const STORE_KEY = 'nebians_interactive_progress';

function loadStore() {
  try { return JSON.parse(localStorage.getItem(STORE_KEY) || '{}'); } catch (e) { return {}; }
}

function saveStore(store) {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(store)); } catch (e) {}
}

function getRecord(courseSlug, lessonSlug) {
  const store = loadStore();
  return (store[courseSlug] || {})[lessonSlug] || {};
}

function setRecord(courseSlug, lessonSlug, patch) {
  const store = loadStore();
  store[courseSlug] = store[courseSlug] || {};
  store[courseSlug][lessonSlug] = Object.assign({}, store[courseSlug][lessonSlug], patch);
  saveStore(store);
}

const root = document.getElementById('ix-lesson-root');

if (root) {
  const courseSlug = root.dataset.courseSlug;
  const lessonSlug = root.dataset.lessonSlug;
  const simUrl2d = root.dataset.simUrl;
  const simUrl3d = root.dataset.sim3dUrl || null;
  const stage = document.getElementById('sim-stage');
  const loading = document.getElementById('ix-sim-loading');
  const dimSwitch = document.getElementById('ix-dim-switch');
  const DIM_KEY = 'nebians_interactive_dim';
  let simHandle = null;
  let simDisposed = false;
  // Active view dimension. Restore the learner's last choice when a 3D companion exists.
  let activeDim = '2d';
  if (simUrl3d) {
    try { if (localStorage.getItem(DIM_KEY) === '3d') activeDim = '3d'; } catch (e) {}
  }

  function currentSimUrl() {
    return activeDim === '3d' && simUrl3d ? simUrl3d : simUrl2d;
  }

  function showLoading(msg) {
    if (!loading) return;
    loading.innerHTML = '<div class="ix-spinner"></div><p>' + (msg || 'Loading simulation…') + '</p>';
    if (!loading.parentNode) stage.appendChild(loading);
  }

  function disposeSim() {
    if (simHandle && typeof simHandle.dispose === 'function') {
      try { simHandle.dispose(); } catch (e) {}
    }
    simHandle = null;
  }

  function startSim() {
    simDisposed = false;
    const url = currentSimUrl();
    import(url)
      .then((mod) => {
        // Guard against a switch/teardown that happened while importing.
        if (simDisposed || url !== currentSimUrl()) return;
        if (loading && loading.parentNode) loading.remove();
        const init = mod.default || mod.init;
        if (typeof init === 'function') {
          simHandle = init(stage, { courseSlug, lessonSlug, dim: activeDim }) || null;
        }
      })
      .catch((err) => {
        console.error('Sim failed to load:', err);
        if (loading) {
          loading.innerHTML = '<span class="material-symbols-outlined" style="font-size:40px;">cloud_off</span>' +
            '<p>The simulation could not load. Check your connection and refresh — the lesson text below still works!</p>';
        }
      });
  }

  function switchDim(dim) {
    if (dim === activeDim || (dim === '3d' && !simUrl3d)) return;
    activeDim = dim;
    try { localStorage.setItem(DIM_KEY, dim); } catch (e) {}
    if (dimSwitch) {
      dimSwitch.querySelectorAll('.ix-dim-btn').forEach((b) => {
        const on = b.dataset.dim === dim;
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    }
    const hint = document.getElementById('ix-sim-hint');
    if (hint) {
      hint.innerHTML = dim === '3d'
        ? '<span class="material-symbols-outlined">touch_app</span>Drag to rotate · pinch or scroll to zoom'
        : '<span class="material-symbols-outlined">tune</span>Adjust the controls and watch what happens';
    }
    disposeSim();
    showLoading();
    startSim();
  }

  if (dimSwitch && simUrl3d) {
    // Reflect the restored preference in the switch UI before first render.
    dimSwitch.querySelectorAll('.ix-dim-btn').forEach((b) => {
      const on = b.dataset.dim === activeDim;
      b.classList.toggle('is-active', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    dimSwitch.addEventListener('click', (e) => {
      const btn = e.target.closest('.ix-dim-btn');
      if (btn) switchDim(btn.dataset.dim);
    });
  }

  startSim();

  window.addEventListener('pagehide', (e) => {
    if (e.persisted) return;
    if (simHandle && typeof simHandle.dispose === 'function') {
      try { simHandle.dispose(); } catch (e2) {}
      simHandle = null;
      simDisposed = true;
    }
  });

  window.addEventListener('pageshow', (e) => {
    if (e.persisted && simDisposed && !simHandle) {
      startSim();
    }
  });

  const shell = document.getElementById('ix-sim-shell');
  const fsBtn = document.getElementById('ix-fullscreen-btn');
  if (fsBtn && shell) {
    const icon = fsBtn.querySelector('.material-symbols-outlined');

    function renderFsState(active) {
      icon.textContent = active ? 'fullscreen_exit' : 'fullscreen';
      const label = active ? 'Exit fullscreen' : 'Fullscreen';
      fsBtn.setAttribute('aria-label', label);
      fsBtn.setAttribute('title', label);
    }

    function onFakeEscape(e) {
      if (e.key === 'Escape') exitFake();
    }

    function enterFake() {
      shell.classList.add('ix-fake-fullscreen');
      document.body.classList.add('ix-no-scroll');
      renderFsState(true);
      document.addEventListener('keydown', onFakeEscape);
    }

    function exitFake() {
      shell.classList.remove('ix-fake-fullscreen');
      document.body.classList.remove('ix-no-scroll');
      renderFsState(false);
      document.removeEventListener('keydown', onFakeEscape);
    }

    fsBtn.addEventListener('click', () => {
      if (document.fullscreenElement === shell) {
        document.exitFullscreen();
      } else if (shell.classList.contains('ix-fake-fullscreen')) {
        exitFake();
      } else if (shell.requestFullscreen) {
        shell.requestFullscreen().catch(() => enterFake());
      } else {
        enterFake();
      }
    });
    document.addEventListener('fullscreenchange', () => {
      renderFsState(document.fullscreenElement === shell);
    });
  }

  const completeBtn = document.getElementById('ix-complete-btn');
  const completeLabel = document.getElementById('ix-complete-label');
  const completeIcon = document.getElementById('ix-complete-icon');

  function renderComplete(done) {
    if (!completeBtn) return;
    completeBtn.classList.toggle('ix-completed', done);
    if (completeLabel) completeLabel.textContent = done ? 'Completed!' : 'Mark complete';
    if (completeIcon) completeIcon.textContent = done ? 'task_alt' : 'check';
  }

  function markDone(done) {
    setRecord(courseSlug, lessonSlug, { done });
    renderComplete(done);
  }

  renderComplete(!!getRecord(courseSlug, lessonSlug).done);

  if (completeBtn) {
    completeBtn.addEventListener('click', () => {
      markDone(!completeBtn.classList.contains('ix-completed'));
    });
  }

  const quiz = document.getElementById('ix-quiz');
  if (quiz) {
    const questions = [...quiz.querySelectorAll('.ix-quiz-q')];
    const result = document.getElementById('ix-quiz-result');
    let answered = 0;
    let correct = 0;
    const record = getRecord(courseSlug, lessonSlug);
    const savedAnswers = record.quizAnswers || {};

    function showResult() {
      if (answered !== questions.length || !result) return;
      result.hidden = false;
      const pct = Math.round((correct / questions.length) * 100);
      let msg, icon;
      if (pct === 100) { icon = 'emoji_events'; msg = `Perfect! ${correct}/${questions.length} — you mastered this lesson!`; }
      else if (pct >= 60) { icon = 'sentiment_very_satisfied'; msg = `Nice work! You scored ${correct}/${questions.length}.`; }
      else { icon = 'replay'; msg = `You scored ${correct}/${questions.length}. Explore the simulation again and you'll get it!`; }
      result.innerHTML = `<span class="material-symbols-outlined">${icon}</span><span>${msg}</span>`;
      result.classList.toggle('ix-result-great', pct >= 60);
      setRecord(courseSlug, lessonSlug, { quiz: pct, quizAnswers: savedAnswers });
      if (pct >= 60) markDone(true);
    }

    function lockQuestion(q, chosenIdx) {
      const answer = parseInt(q.dataset.answer, 10);
      const explain = q.querySelector('.ix-quiz-explain');
      const opts = [...q.querySelectorAll('.ix-quiz-opt')];
      const isCorrect = chosenIdx === answer;
      const chosenOpt = opts[chosenIdx];
      if (chosenOpt) chosenOpt.classList.add(isCorrect ? 'correct' : 'wrong');
      if (!isCorrect && opts[answer]) opts[answer].classList.add('correct');
      opts.forEach((o) => {
        o.classList.add('locked');
        o.setAttribute('aria-disabled', 'true');
        o.disabled = true;
      });
      if (explain) explain.hidden = false;
    }

    questions.forEach((q, qi) => {
      const opts = [...q.querySelectorAll('.ix-quiz-opt')];
      if (qi in savedAnswers) {
        answered++;
        if (savedAnswers[qi] === parseInt(q.dataset.answer, 10)) correct++;
        lockQuestion(q, savedAnswers[qi]);
      } else {
        opts.forEach((opt) => {
          opt.addEventListener('click', () => {
            const idx = parseInt(opt.dataset.index, 10);
            answered++;
            if (idx === parseInt(q.dataset.answer, 10)) correct++;
            lockQuestion(q, idx);
            savedAnswers[qi] = idx;
            setRecord(courseSlug, lessonSlug, { quizAnswers: savedAnswers });
            showResult();
          });
        });
      }
    });

    if (answered === questions.length) showResult();
  }
}
