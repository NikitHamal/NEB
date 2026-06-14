import { runPython } from './python-runner.js';
import { createGuide } from './guide.js';
import { launchConfetti } from './maze-game.js';

export function createPyLesson(stage, config) {
  stage.classList.add('ix-coding', 'ix-coding-playground', 'ix-coding-py');
  const goals = (config.goals || []).map((g) => ({ ...g, met: false }));
  let allMetFired = false;

  const root = document.createElement('div');
  root.className = 'ix-coding-root ix-pg';
  root.innerHTML =
    '<div class="ix-pg-main">' +
    '<div class="ix-pg-editors">' +
    '<div class="ix-pg-tabs"><span class="ix-pg-tab ix-pg-tab-active ix-pg-tab-static"><span class="material-symbols-outlined">data_object</span>main.py</span></div>' +
    '<div class="ix-pg-editor-host"></div>' +
    '<div class="ix-pg-actions">' +
    '<button type="button" class="ix-run-btn ix-btn-run ix-py-run"><span class="material-symbols-outlined">play_arrow</span>Run</button>' +
    '<button type="button" class="ix-run-btn ix-btn-reset ix-py-reset"><span class="material-symbols-outlined">restart_alt</span>Start over</button>' +
    '</div>' +
    '</div>' +
    '<div class="ix-pg-output">' +
    '<div class="ix-pg-out-tabs"><span class="ix-pg-out-label">Output</span></div>' +
    '<div class="ix-pg-out-body"><div class="ix-pg-console ix-py-out"><div class="ix-pg-console-empty">Press Run to see your program\'s output!</div></div></div>' +
    '</div>' +
    '</div>' +
    '<div class="ix-pg-goals"><div class="ix-pg-goals-title"><span class="material-symbols-outlined">checklist</span>Your goals</div><ul class="ix-pg-goals-list"></ul></div>';
  stage.appendChild(root);

  const editor = document.createElement('textarea');
  editor.className = 'ix-pg-editor';
  editor.spellcheck = false;
  editor.autocapitalize = 'off';
  editor.autocomplete = 'off';
  editor.value = config.starter || '';
  editor.setAttribute('aria-label', 'Python editor');
  editor.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const s = editor.selectionStart;
      editor.value = editor.value.slice(0, s) + '  ' + editor.value.slice(editor.selectionEnd);
      editor.selectionStart = editor.selectionEnd = s + 2;
    }
  });
  root.querySelector('.ix-pg-editor-host').appendChild(editor);

  const outEl = root.querySelector('.ix-py-out');
  const goalsList = root.querySelector('.ix-pg-goals-list');
  const guide = createGuide(stage, { name: 'Neby' });

  function renderGoals() {
    goalsList.innerHTML = '';
    goals.forEach((g) => {
      const li = document.createElement('li');
      li.className = 'ix-pg-goal' + (g.met ? ' ix-pg-goal-met' : '');
      const icon = document.createElement('span');
      icon.className = 'material-symbols-outlined';
      icon.textContent = g.met ? 'done' : 'radio_button_unchecked';
      const label = document.createElement('span');
      label.textContent = g.label;
      li.appendChild(icon);
      li.appendChild(label);
      goalsList.appendChild(li);
    });
  }
  renderGoals();

  function printLine(text, cls) {
    const empty = outEl.querySelector('.ix-pg-console-empty');
    if (empty) empty.remove();
    const div = document.createElement('div');
    div.className = 'ix-pg-con-line' + (cls ? ' ' + cls : '');
    div.textContent = text;
    outEl.appendChild(div);
    outEl.scrollTop = outEl.scrollHeight;
  }

  function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

  function doRun() {
    outEl.innerHTML = '';
    const source = editor.value;
    const result = runPython(source, {
      onOutput: (line) => printLine(line),
      inputs: config.inputs,
    });
    if (!result.ok) {
      printLine(result.error, 'ix-pg-con-error');
      guide.say(pick(config.errorLines || ['Oops, there\'s an error! Read the red message — it tells you the line number to check.']), { mood: 'thinking' });
      return;
    }
    if (!result.output.length) printLine('(no output — try adding a print!)', 'ix-pg-con-dim');
    const ctx = {
      source,
      output: result.output,
      run: (extra) => runPython(source + '\n' + extra, { inputs: config.inputs }),
    };
    let newly = false;
    goals.forEach((g) => {
      if (g.met) return;
      let ok = false;
      try { ok = !!g.test(ctx); } catch (e) { ok = false; }
      if (ok) { g.met = true; newly = true; }
    });
    renderGoals();
    const metCount = goals.filter((g) => g.met).length;
    if (!allMetFired && metCount === goals.length) {
      allMetFired = true;
      launchConfetti(stage, 50);
      guide.say(config.allDoneLine || 'All goals complete! You\'re a real Python programmer now!', { mood: 'celebrate' });
    } else if (newly) {
      guide.say(pick(config.goalLines || ['Goal ticked! ' + metCount + ' of ' + goals.length + ' done — keep going!']), { mood: 'celebrate' });
    } else if (config.onRunNoGoal) {
      config.onRunNoGoal(ctx, guide);
    }
  }

  root.querySelector('.ix-py-run').addEventListener('click', doRun);
  root.querySelector('.ix-py-reset').addEventListener('click', () => {
    editor.value = config.starter || '';
    outEl.innerHTML = '<div class="ix-pg-console-empty">Press Run to see your program\'s output!</div>';
    guide.say('Back to the starter code. Experiment away!', { mood: 'happy', duration: 3000 });
  });

  if (config.intro) guide.say(config.intro, { mood: 'happy' });

  return {
    dispose() {
      guide.dispose();
      root.remove();
      stage.classList.remove('ix-coding', 'ix-coding-playground', 'ix-coding-py');
    },
  };
}
