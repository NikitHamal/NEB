// Canvas roundRect throws on a negative radius or size, which a sim drawing into a stage that is
// still 0 px wide (mid-layout, or collapsed on a phone) produces for a frame. One guard here keeps
// every 2D lab alive through that instead of each one clamping its own maths.
if (typeof CanvasRenderingContext2D !== 'undefined' && CanvasRenderingContext2D.prototype.roundRect && !CanvasRenderingContext2D.prototype.__safeRoundRect) {
  const raw = CanvasRenderingContext2D.prototype.roundRect;
  const fix = (r) => (Array.isArray(r) ? r.map(fix) : (typeof r === 'number' ? Math.max(0, r || 0) : r));
  CanvasRenderingContext2D.prototype.roundRect = function (x, y, w, h, radii) {
    if (!(w > 0) || !(h > 0)) return this.rect(x, y, Math.max(0, w || 0), Math.max(0, h || 0));
    return raw.call(this, x, y, w, h, radii === undefined ? 0 : fix(radii));
  };
  CanvasRenderingContext2D.prototype.__safeRoundRect = true;
}

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
  const simUrl = root.dataset.simUrl;
  const stage = document.getElementById('sim-stage');
  const loading = document.getElementById('ix-sim-loading');
  let simHandle = null;
  let simDisposed = false;

  /* A phone on a slow line used to see one failed import and a dead panel. The module graph is
     retried twice with a short back-off, the wait is explained after 8 s, and the failure
     screen has a Retry button instead of "refresh the page". */
  function hasWebGL() {
    try {
      const c = document.createElement('canvas');
      return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
    } catch (e) { return false; }
  }

  function setLoading(html) {
    if (!loading) return;
    if (!loading.parentNode && stage) stage.appendChild(loading);
    loading.innerHTML = html;
  }

  function showLoadError(text) {
    setLoading('<span class="material-symbols-outlined" style="font-size:40px;" aria-hidden="true">cloud_off</span>' +
      '<p>' + text + '</p>' +
      '<button type="button" class="ix-sim-retry" id="ix-sim-retry">Try again</button>');
    const btn = document.getElementById('ix-sim-retry');
    if (btn) btn.addEventListener('click', () => {
      setLoading('<div class="ix-spinner md-loader md-loader-screen"></div><p>Loading simulation…</p>');
      startSim(0);
    });
  }

  function startSim(attempt) {
    attempt = attempt || 0;
    simDisposed = false;
    const slow = setTimeout(() => {
      const p = loading && loading.querySelector('p');
      if (p) p.textContent = 'Still loading. Slow connection? It keeps going in the background.';
    }, 8000);
    import(simUrl)
      .then((mod) => {
        clearTimeout(slow);
        const init = mod.default || mod.init;
        if (typeof init === 'function') {
          simHandle = init(stage, { courseSlug, lessonSlug }) || null;
        }
        if (loading && loading.parentNode) loading.remove();
      })
      .catch((err) => {
        clearTimeout(slow);
        console.error('Sim failed to load:', err);
        if (attempt < 2) {
          setTimeout(() => startSim(attempt + 1), 700 * (attempt + 1));
          return;
        }
        showLoadError(hasWebGL()
          ? 'The simulation could not load. Check your connection and try again. The lesson text below still works.'
          : 'This device cannot draw 3D here. The lesson text below still works.');
      });
  }

  startSim(0);

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
      startSim(0);
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

    /* Every canvas measures itself on resize; without this the stage stayed at its small size
       (black bars) after entering or leaving fullscreen. Two frames: layout first, then measure. */
    function settle() {
      requestAnimationFrame(() => requestAnimationFrame(() => window.dispatchEvent(new Event('resize'))));
    }

    /* position:fixed is relative to the nearest ancestor with a transform, filter or containment,
       which made fullscreen open as a small box on some lessons. Strip those while it is open. */
    function freeAncestors(on) {
      document.documentElement.classList.toggle('ix-fs-open', on);
      for (let el = shell.parentElement; el && el !== document.body; el = el.parentElement) {
        el.classList.toggle('ix-fs-ancestor', on);
      }
    }

    const android = /NEBiansAndroid/.test(navigator.userAgent);

    function enterFake() {
      freeAncestors(true);
      shell.classList.add('ix-fake-fullscreen');
      document.body.classList.add('ix-no-scroll');
      renderFsState(true);
      document.addEventListener('keydown', onFakeEscape);
      if (android) { try { window.alert('NEBY_FULLSCREEN_ENTER'); } catch (e) {} }
      settle();
    }

    function exitFake() {
      shell.classList.remove('ix-fake-fullscreen');
      document.body.classList.remove('ix-no-scroll');
      freeAncestors(false);
      renderFsState(false);
      document.removeEventListener('keydown', onFakeEscape);
      if (android) { try { window.alert('NEBY_FULLSCREEN_EXIT'); } catch (e) {} }
      settle();
    }

    fsBtn.addEventListener('click', () => {
      if (document.fullscreenElement === shell) {
        document.exitFullscreen();
      } else if (shell.classList.contains('ix-fake-fullscreen')) {
        exitFake();
      } else if (!android && shell.requestFullscreen) {
        shell.requestFullscreen().catch(() => enterFake());
      } else {
        enterFake();
      }
    });
    document.addEventListener('fullscreenchange', () => {
      renderFsState(document.fullscreenElement === shell);
      settle();
    });
    window.addEventListener('nebfullscreenexit', () => { if (shell.classList.contains('ix-fake-fullscreen')) exitFake(); });
  }

  const completeBtn = document.getElementById('ix-complete-btn');
  const completeLabel = document.getElementById('ix-complete-label');
  const completeIcon = document.getElementById('ix-complete-icon');

  function renderComplete(done) {
    if (!completeBtn) return;
    completeBtn.classList.toggle('ix-completed', done);
    if (completeLabel) completeLabel.textContent = done ? 'Completed!' : 'Mark complete';
    if (completeIcon) completeIcon.textContent = done ? 'done' : 'done';
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
